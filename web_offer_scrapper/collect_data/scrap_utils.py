import csv
import json
import os
import random

import requests
from bs4 import BeautifulSoup

from web_offer_scrapper.project_utils.logger import get_logger

logger = get_logger(__name__)


userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",  # noqa: E501
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",  # noqa: E501
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]


def request_url(url: str) -> requests.Response:
    logger.info(f"Sending GET request to url {url}.")
    response = requests.get(url, headers={"User-Agent": random.choice(userAgents)})

    if response.status_code != 200:
        message = f"Failed to fetch search results. Status code: {response.status_code}."
        logger.error(message)
        raise ConnectionError(message)

    logger.info("Response from GET request got successfully.")
    return response


def request_url_get_soup(url: str) -> BeautifulSoup:
    response = request_url(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def load_jsons_and_return_csv(base_path: str = os.path.join("data", "tabular")):
    files = os.listdir(base_path)
    data = []
    for file_name in files:
        file_path = os.path.join(base_path, file_name)
        with open(file_path) as f:
            file_data = json.load(f)
        for k, v in file_data.items():
            if isinstance(v, str):
                file_data[k] = v.replace(",", " ")

        data.append(file_data)

    keys = data[0].keys()
    with open("otodom_wroclaw.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
