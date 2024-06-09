from urllib.parse import urlencode, urlparse, parse_qs, unquote
import scrapy
from idealista.items import HouseItem
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv("SCRAPERAPI_API_KEY")


def get_scraperapi_url(url):
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


class HouseIdSpider(scrapy.Spider):
    name = "house_id_spider"
    start_urls = [
        # "http://www.idealista.com/venta-viviendas/valdemorillo-madrid/",
        # "https://www.idealista.com/venta-viviendas/robledo-de-chavela-madrid/",
        # "https://idealista.com//venta-viviendas/robledo-de-chavela-madrid/pagina-2.htm"
    ]

    def clean_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        target_url = unquote(query_params["url"][0])
        # Split the URL path and filter out page suffix if present
        parts = target_url.split("/")
        if parts[-1].startswith("pagina-"):
            location_part = parts[-2]
        else:
            location_part = parts[-1]

        return location_part

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(get_scraperapi_url(url), self.parse)

    def parse(self, response):
        for house in response.css("article.item"):
            house_item = HouseItem()
            house_item["house_id"] = house.attrib["data-element-id"]
            # take the last item from url query param ?url=location
            house_item["location"] = self.clean_url(response.url)
            yield house_item

        next_page = response.css("div.pagination li.next ::attr(href)").get()

        if next_page is not None:
            next_page_url = "http://idealista.com/" + next_page
            yield scrapy.Request(get_scraperapi_url(next_page_url), self.parse)
