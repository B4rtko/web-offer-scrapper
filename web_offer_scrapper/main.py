from typing import List

from web_offer_scrapper.collect_data.scrap_handlers.otodom_listing_page_handler import ListingPageHandler
from web_offer_scrapper.collect_data.scrap_handlers.otodom_offer_page_handler import OfferPageHandler
from web_offer_scrapper.project_utils.logger import get_logger

logger = get_logger(__name__)


def main():
    listing_page_handler = ListingPageHandler(page_num_max=None)
    scrap_flag = True

    while scrap_flag:
        scrap_flag = scrap_next_list(listing_page_handler)

    return listing_page_handler


def scrap_next_list(listing_page_handler: ListingPageHandler) -> bool:
    scrap_flag = listing_page_handler.scrap_next()

    offer_handlers_not_scrapped: List[OfferPageHandler] = listing_page_handler.listed_pages_offer_handlers_not_scrapped

    for offer_page_handler in offer_handlers_not_scrapped:
        try:
            offer_page_handler.scrap_page_tabular()
            offer_page_handler.scrap_page_images()
            offer_page_handler.save_data(tabular_to_database=False, image_to_google_drive=False)
        except Exception as e:
            logger.error(f"Error occured during scrapping page {offer_page_handler.url_full}.\n{repr(e)}")

    return scrap_flag


if __name__ == "__main__":
    main()
