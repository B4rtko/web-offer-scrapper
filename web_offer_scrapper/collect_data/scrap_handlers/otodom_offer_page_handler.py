import json
import os
from typing import Any, Dict, Optional, Tuple

from bs4 import BeautifulSoup

from web_offer_scrapper.collect_data.converters.convert_data import Converter
from web_offer_scrapper.collect_data.scrap_utils import request_url, request_url_get_soup
from web_offer_scrapper.project_utils.logger import get_logger

from .config import offer_fields_config

logger = get_logger(__name__)


class OfferPageHandler:
    """
    Intention of the class is to be used for scrapping individual offer webpage and save the data to the storage.
    Class will be used by ListingPageHandler object which creates OfferPageHandler objects while scrapping offer urls
    from listing webpages.
    """

    url_base: str = "https://www.otodom.pl"
    url_extension: str
    page_scrapped_tabular: bool = False
    page_scrapped_image: bool = False
    _page_soup: Optional[BeautifulSoup] = None
    data_converter: Optional[Converter] = None

    def __init__(self, url_extension: str) -> None:
        self.url_extension = url_extension
        self.page_scrapped_tabular = self._check_if_page_under_url_was_scrapped_tabular()
        self.page_scrapped_image = self._check_if_page_under_url_was_scrapped_image()

        self._data_tabular: Dict[str, Any] = {}
        self._data_image: Dict[str, bytes] = {}

        logger.info(f"Initialized OfferPageHandler object for page {self.url_full}.")

    @property
    def page_soup(self) -> BeautifulSoup:
        if self._page_soup is None:
            self._page_soup = request_url_get_soup(url=self.url_full)
        return self._page_soup

    @property
    def data_tabular(self) -> Dict[str, Any]:
        return self._data_tabular.copy()

    @property
    def data_image(self) -> Dict[str, bytes]:
        return self._data_image.copy()

    @property
    def page_scrapped(self) -> bool:
        return self.page_scrapped_tabular and self.page_scrapped_image

    @property
    def url_full(self) -> str:
        return self.url_base + self.url_extension

    @property
    def data_tabular_converted(self) -> Dict[str, Any]:
        if self.data_converter is None:
            if not self.page_scrapped_tabular:
                message = f"OfferPageHandler object with url {self.url_full} has no converter and was not scrapped previously."  # noqa: E501
                logger.warning(message)
                raise Exception(message)
            else:
                # the tabular data is not a raw data, but the data loaded from json file, so after previous conversion
                return self._data_tabular.copy()
        else:
            if not self.data_converter.converted:
                self.data_converter.convert_all()
            return self.data_converter.converted_dictionary

    def get_tabular_data_base_path_and_file_name(self) -> Tuple[str, str]:
        base_path = os.path.join("data", "tabular")
        file_name = self.url_extension.replace("/", "_") + ".json"
        return base_path, file_name

    def get_image_data_base_path(self) -> str:
        return os.path.join("data", "images", self.url_extension.replace("/", "_"))

    def save_tabular_data(self, to_database: bool = True) -> None:
        if to_database:
            self._save_tabular_data_database()
        else:
            self._save_tabular_data_local()

    def _save_tabular_data_local(self) -> None:
        logger.info("Saving tabular data to local file..")
        base_path, file_name = self.get_tabular_data_base_path_and_file_name()
        full_path = os.path.join(base_path, file_name)
        os.makedirs(base_path, exist_ok=True)

        with open(full_path, "w") as f:
            json.dump(self.data_tabular_converted, f, sort_keys=True, indent=2)
        logger.info(f"Saving successful. File path is {full_path}")

    def _save_tabular_data_database(self) -> None:
        pass

    def save_image_data(self, to_google_drive: bool = True) -> None:
        if to_google_drive:
            self._save_image_data_google_drive()
        else:
            self._save_image_data_local()

    def _save_image_data_local(self) -> None:
        logger.info("Saving image data to local file..")
        base_path = self.get_image_data_base_path()
        os.makedirs(base_path, exist_ok=True)

        data_image = self.data_image
        for image_link, image in data_image.items():
            file_name = image_link.replace("/", "_") + ".png"
            full_path = os.path.join(base_path, file_name)

            with open(full_path, "wb") as f:
                f.write(image)
        logger.info(f"Saving successful. {len(data_image)} file/s saved to {base_path}")

    def _save_image_data_google_drive(self) -> None:
        pass

    def save_data(self, tabular_to_database: bool = True, image_to_google_drive: bool = True) -> None:
        self.save_tabular_data(to_database=tabular_to_database)
        self.save_image_data(to_google_drive=image_to_google_drive)

    def _find_in_soup(self, *args: Any) -> Optional[str]:
        """
        Method for searching through the soup for given args and returning found value.
        If an AttributeError occurs, it is cought and the None value is being returned.

        :param *args: all the latter arguments passed will be input to the BeautifulSoup find method
        :return: Value found with the given bs4 search parameters or None if an error occured during th search
        """
        try:
            result = self.page_soup.find(*args).get_text()
            assert isinstance(result, str)
            return result
        except AttributeError:
            logger.warning(f"Error in finding in soup by args={args}.")
            return None

    def scrap_page_tabular(self, skip_if_already_scrapped: bool = True) -> bool:
        """
        Method performs scrapping of the offer page that its extension_url points to.
        Results are saved to the object's data dictionary and the page_scrapped bool is being
        switched to True when succeeded. Method returns bool value. True value indicates that the scrapping
        was performed normally. False value indicates that the page was already scrapped and it was not explicitly said
        to scrap page inregardles of that.

        :param skip_if_already_scrapped: bool indicating if the scrapping shoudl be skipped
               if the page was already scrapped, defaults to True
        """
        logger.info(f"Started scrapping tabular data from offer page with url {self.url_full}")
        if self.page_scrapped_tabular and skip_if_already_scrapped:
            logger.info(
                "Scrapping tabular data from offer page aborted - page already scrapped and the "
                "tabular data is being stored."
            )
            return False

        self._data_tabular[offer_fields_config.price.data_name] = self._find_in_soup("strong", {"aria-label": "Cena"})
        self._data_tabular[offer_fields_config.address.data_name] = self._find_in_soup("a", {"aria-label": "Adres"})
        self._data_tabular[offer_fields_config.description.data_name] = self._find_in_soup(
            "div", {"data-cy": "adPageAdDescription"}
        )
        self._data_tabular[offer_fields_config.link_id.data_name] = self.url_extension

        for field in offer_fields_config.fields_with_html_name:
            self._data_tabular[field.data_name] = self._find_in_soup("div", {"data-testid": field.html_name})

        self.page_scrapped_tabular = True
        self.data_converter = Converter(dictionary=self.data_tabular)
        logger.info(f"Finished scrapping tabular data from offer page with url {self.url_full}.")
        return True

    def scrap_page_images(self, skip_if_already_scrapped: bool = True) -> bool:
        logger.info(f"Started scrapping image data from offer page with url {self.url_full}")
        if self.page_scrapped_image and skip_if_already_scrapped:
            logger.info(
                "Scrapping image data from offer page aborted - page already scrapped and the "
                "image data is being stored."
            )
            return False

        image_url = self.page_soup.picture.img["src"].split("/image;")[0] + "/image"
        self._data_image[image_url] = request_url(image_url).content

        self.page_scrapped_image = True
        logger.info(f"Finished scrapping image data from offer page with url {self.url_full}.")
        return True

    def _check_if_page_under_url_was_scrapped_tabular(self) -> bool:
        file_path = os.path.join(*self.get_tabular_data_base_path_and_file_name())
        if os.path.exists(file_path):
            logger.info(f"Found scrapped tabular data under {file_path}. Trying to load the data from file..")
            try:
                with open(file_path) as f:
                    self._data_tabular = json.load(f)
                logger.info("File loaded successfully.")
                return True
            except Exception:
                logger.warning(
                    f"Error when trying to load file {file_path}. Removing file and assuming the page wasn't scrapped"
                )
                os.remove(file_path)
                return False
        else:
            return False

    def _check_if_page_under_url_was_scrapped_image(self) -> bool:
        base_path = os.path.join(self.get_image_data_base_path())
        if os.path.exists(base_path):
            return bool(os.listdir(base_path))
        return False
