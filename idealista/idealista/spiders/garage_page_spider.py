from urllib.parse import urlencode
import scrapy
from idealista.items import GarageItem
import os
import dotenv

from db.functions import get_garage_ids

dotenv.load_dotenv()
API_KEY = os.getenv("SCRAPERAPI_API_KEY")


def get_scraperapi_url(url):
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


class GarageSpider(scrapy.Spider):
    name = "garage_page_spider"

    def clean_and_join(self, text_list):
        cleaned_list = [
            text.strip() for text in text_list if text.strip() and text.strip() != "\n"
        ]
        # Join into a single string
        return " ".join(cleaned_list)

    def start_requests(self):

        garage_ids = get_garage_ids()
        start_urls = [
            f"http://www.idealista.com/inmueble/{garage_id[0]}/"
            for garage_id in garage_ids
        ]

        for url in start_urls:
            yield scrapy.Request(get_scraperapi_url(url), self.parse)

    def parse(self, response):
        garage_item = GarageItem()

        garage_item["garage_id"] = response.url.split("%2F")[-2]
        raw_price = response.css(
            "section.price-features__container p.flex-feature ::text"
        ).getall()
        raw_details = response.css("#details .details-property ::text").getall()
        raw_description = response.css(".comment ::text").getall()
        raw_address = response.css("#mapWrapper ::text").getall()
        raw_title = response.css(".main-info__title ::text").getall()
        raw_hood = response.css(
            ".main-info__title .main-info__title-minor ::text"
        ).get()

        garage_item["price_string"] = self.clean_and_join(raw_price)
        garage_item["details"] = self.clean_and_join(raw_details)
        garage_item["description"] = self.clean_and_join(raw_description)
        garage_item["address"] = self.clean_and_join(raw_address)
        garage_item["title"] = self.clean_and_join(raw_title)
        garage_item["hood"] = raw_hood.split(",")[0]

        yield garage_item
