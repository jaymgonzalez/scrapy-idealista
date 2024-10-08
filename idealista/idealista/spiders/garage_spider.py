from urllib.parse import urlencode
import scrapy
from idealista.items import GarageItem
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv("SCRAPERAPI_API_KEY")


def get_scraperapi_url(url):
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


class GarageSpider(scrapy.Spider):
    name = "garage_spider"
    start_urls = [
        "https://www.idealista.com/alquiler-garajes/madrid/barrio-de-salamanca/fuente-del-berro/pagina-1.htm"
    ]

    def clean_and_join(self, text_list):
        cleaned_list = [
            text.strip() for text in text_list if text.strip() and text.strip() != "\n"
        ]
        # Join into a single string
        return " ".join(cleaned_list)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(get_scraperapi_url(url), self.parse)

    def parse(self, response):
        garage_ids = response.css("article.item ::attr(data-element-id)").getall()
        for garage in garage_ids:
            url = f"http://www.idealista.com/inmueble/{garage}/"
            yield scrapy.Request(get_scraperapi_url(url), self.parse_garage)

        next_page = response.css("div.pagination li.next ::attr(href)").get()

        if next_page is not None:
            next_page_url = "http://idealista.com/" + next_page
            yield scrapy.Request(get_scraperapi_url(next_page_url), self.parse)

    def parse_garage(self, response):
        garage_item = GarageItem()

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

        garage_item["garage_id"] = response.url.split("%2F")[-2]
        garage_item["price_string"] = self.clean_and_join(raw_price)
        garage_item["details"] = self.clean_and_join(raw_details)
        garage_item["description"] = self.clean_and_join(raw_description)
        garage_item["address"] = self.clean_and_join(raw_address)
        garage_item["title"] = self.clean_and_join(raw_title)
        garage_item["hood"] = raw_hood.split(",")[0]

        if garage_item["title"].lower().startswith("alquiler"):
            garage_item["sell"] = 0
            garage_item["rent"] = 1
        else:
            garage_item["sell"] = 1
            garage_item["rent"] = 0

        yield garage_item
