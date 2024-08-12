from typing import List, Optional

from bs4 import BeautifulSoup

from web_offer_scrapper.project_utils.logger import get_logger

from ..scrap_utils import request_url_get_soup
from .otodom_offer_page_handler import OfferPageHandler

logger = get_logger(__name__)


class ListingPageHandler:
    """Class for handling scrapping of the listing pages with offers on otodom.pl website."""

    listed_pages_count_per_page: Optional[int]

    page_num_current: int = 1
    page_num_max: Optional[int] = None

    url_base: str = "https://www.otodom.pl"
    url_extension: str = "/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing"

    _page_num_max_without_limit_set = 10

    def __init__(
        self,
        listed_pages_count_per_page: Optional[int] = None,
        already_scrapped_link_extensions: Optional[List[str]] = None,
        page_num_max: Optional[int] = None,
    ) -> None:
        self._listed_pages_link_extensions: List[str] = already_scrapped_link_extensions or []
        self._listed_pages_offer_handlers: List[OfferPageHandler] = []
        self.listed_pages_count_per_page = listed_pages_count_per_page
        self.page_num_max = page_num_max

        logger.info(
            f"Initialized ListingPageHandler object with args "
            f"listed_pages_count_per_page={listed_pages_count_per_page}, page_num_max={page_num_max}."
        )

    @property
    def listed_pages_link_extensions(self) -> List[str]:
        """Returns list with link extension of offers that were find on scrapped listing pages."""
        return self._listed_pages_link_extensions.copy()

    @property
    def listed_pages_offer_handlers(self) -> List[OfferPageHandler]:
        """Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website."""  # noqa: E501
        return self._listed_pages_offer_handlers.copy()

    @property
    def listed_pages_offer_handlers_not_scrapped(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        but not yet have fully scrapped.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if not handler.page_scrapped]

    @property
    def listed_pages_offer_handlers_scrapped(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        and fully scrapped.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if handler.page_scrapped]

    @property
    def listed_pages_offer_handlers_not_scrapped_tabular(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        but not yet have scrapped tabular data.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if not handler.page_scrapped_tabular]

    @property
    def listed_pages_offer_handlers_scrapped_tabular(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        and scrapped tabular data.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if handler.page_scrapped_tabular]

    @property
    def listed_pages_offer_handlers_not_scrapped_image(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        but not yet have scrapped images.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if not handler.page_scrapped_image]

    @property
    def listed_pages_offer_handlers_scrapped_image(self) -> List[OfferPageHandler]:
        """
        Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website,
        and scrapped images.
        """
        return [handler for handler in self._listed_pages_offer_handlers.copy() if handler.page_scrapped_image]

    @property
    def url_current(self) -> str:
        """Returns full url for the page with the current configuration."""
        url = self.url_base + self.url_extension

        if self.page_num_current > 1:
            url += f"&page={self.page_num_current}"
        if self.listed_pages_count_per_page is not None:
            url += f"&limit={self.listed_pages_count_per_page}"

        return url

    def _update_meta(
        self,
        soup_page: BeautifulSoup,
        increment_page_num_current: bool = True,
        update_page_num_max_once_set: bool = False,
    ) -> None:
        """
        Method updates the object's metadata that is used to iterate over scrapped pages. The intention is to run the
        method ater every successful request to the listing website.

        :param soup_page: BeautifulSoup object created with the response of response from listing website
        :param increment_page_num_current: bool if the object's page_num_current should be incremented, defaults to True
        :param update_page_num_max_once_set: bool if the object's page_num_max should be overwritten if it is
        already set, defaults to False
        """
        logger.info(
            f"Started updating ListingPageHandler metadata. Current metadata: "
            f"page_num_current={self.page_num_current}, page_num_max={self.page_num_max}.."
        )
        if increment_page_num_current:
            self.page_num_current += 1

        # Update 'page_num_max' only if the value was found on the page and if it is not already set.
        # One exception to the latter is when explicitly said to overwrite 'page_num_max' by
        # 'update_page_num_max_once_set'
        page_num_max = self._get_page_num_max(soup=soup_page)
        if page_num_max is not None and (self.page_num_max is None or update_page_num_max_once_set):
            self.page_num_max = page_num_max
        logger.info(
            f"Finished updating ListingPageHandler metadata. Current metadata: "
            f"page_num_current={self.page_num_current}, page_num_max={self.page_num_max}.."
        )

    def _get_page_num_max(self, soup: BeautifulSoup) -> Optional[int]:
        """
        Method for getting the information about total number of pages in listing website.

        :param soup: BeautifulSoup object created with the response of response from listing website
        :return: Total number of pages in listing website.
        """
        try:
            return int(soup.find("ul", {"class": "css-1vdlgt7"}).find_all("li")[-2].text)
        except Exception:
            logger.error("Error from ListingPageHandler with getting page_num_max parameter.")
            return None

    def _get_offer_links_from_soup(self, soup: BeautifulSoup) -> List[str]:
        """
        Method for getting url link extensions to the offer pages from listing website.

        :param soup: BeautifulSoup object created with the response of response from listing website
        :return: List with url link extensions of offers listed on the page of the given soup
        """
        logger.info("Getting offer links from the ListingPageHandler current page's soup..")
        try:
            links = soup.find("div", {"data-cy": "search.listing.organic"}).find_all(
                "a", {"data-cy": "listing-item-link"}
            )
            links = [link["href"] for link in links]
            logger.info(f"Success getting offer links. Offer count is {len(links)}.")
            return links
        except Exception:
            logger.error("Error getting offer links - returning empty list.")
            return []

    def scrap_next(self) -> bool:
        """
        Method performs scrapping of the listing page that the current configuration ponits to. Results are saved to the
        object's lists and the metadata is being updated accordingly. Method returns bool value. True value indicates
        that the scrapping was performed normally. False value indicates that there are no more pages to scrap
        (for various reasons).
        """
        logger.info(f"Started scrapping offer listing page of number {self.page_num_current}..")
        if self.page_num_max and self.page_num_current > self.page_num_max:
            logger.info(
                f"Scrapping offer listing page aborted - page_num_current ({self.page_num_current}) is greater than "
                f"page_num_max ({self.page_num_max})."
            )
            return False
        if self.page_num_max is None and self.page_num_current > self._page_num_max_without_limit_set:
            logger.info(
                f"Scrapping offer listing page aborted - page_num_max is not set and "
                f"page_num_current ({self.page_num_current}) is greater than the default "
                f"max ({self._page_num_max_without_limit_set})."
            )
            return False

        soup = request_url_get_soup(url=self.url_current)
        self._update_meta(soup_page=soup)

        links = self._get_offer_links_from_soup(soup=soup)
        for url_extension in links:
            self._listed_pages_link_extensions.append(url_extension)

            offer_handler = OfferPageHandler(url_extension=url_extension)
            self._listed_pages_offer_handlers.append(offer_handler)
        logger.info("Finished scrapping offer listing page.")
        return True
