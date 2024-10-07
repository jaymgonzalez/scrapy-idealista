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


class GarageIdSpider(scrapy.Spider):
    name = "garage_id_spider"
    start_urls = [
        # "http://www.idealista.com/venta-viviendas/valdemorillo-madrid/",
        # "https://www.idealista.com/venta-viviendas/robledo-de-chavela-madrid/",
        # "https://idealista.com//venta-viviendas/robledo-de-chavela-madrid/pagina-2.htm"
        "https://www.idealista.com/venta-garajes/madrid/barrio-de-salamanca/fuente-del-berro/pagina-1.htm"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(get_scraperapi_url(url), self.parse)

    def parse(self, response):
        for garage in response.css("article.item"):
            garage_item = GarageItem()
            garage_item["garage_id"] = garage.attrib["data-element-id"]
            yield garage_item

        next_page = response.css("div.pagination li.next ::attr(href)").get()

        if next_page is not None:
            next_page_url = "http://idealista.com/" + next_page
            yield scrapy.Request(get_scraperapi_url(next_page_url), self.parse)
