from urllib.parse import urlencode
import scrapy
from idealista.items import GarageItem
import os
import dotenv

from db.functions import get_garage_ids_without_size

dotenv.load_dotenv()
API_KEY = os.getenv("SCRAPERAPI_API_KEY")


class GarageSpider(scrapy.Spider):
    name = "garage_ai_spider"

    custom_settings = {
        "ITEM_PIPELINES": {
            "idealista.pipelines.OpenAIPipeline": 300,
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://webscraper.io/test-sites/e-commerce/allinone/product/18",
            self.parse,
        )

    def parse(self, response):

        garages = get_garage_ids_without_size()

        for garage in garages:
            garage_item = GarageItem()
            garage_item["garage_id"] = garage[0]
            yield garage_item

        # garage_item = GarageItem()
        # garage_item["garage_id"] = "105972398"
        # yield garage_item
