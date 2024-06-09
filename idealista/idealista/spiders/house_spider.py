from urllib.parse import urlencode
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


class HousespiderSpider(scrapy.Spider):
    name = "house_spider"
    start_urls = [
        # "http://www.idealista.com/venta-viviendas/valdemorillo-madrid/",
        "https://www.idealista.com/venta-viviendas/robledo-de-chavela-madrid/",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(get_scraperapi_url(url), self.parse)

    def parse(self, response):
        # only take 2 houses for testing
        for house in response.css("article.item")[:2]:
            # for house in response.css("article.item"):
            id = house.attrib["data-element-id"]

            yield scrapy.Request(
                get_scraperapi_url(f"http://www.idealista.com/inmueble/{id}/"),
                callback=self.parse_house_page,
            )

        # next_page = response.css("div.pagination li.next ::attr(href)").get()

        # if next_page is not None:
        #     next_page_url = "http://idealista.com/" + next_page
        #     yield response.follow(next_page_url, callback=self.parse)

    def parse_house_page(self, response):
        house_item = HouseItem()
        house_item["id"] = response.url.split("/")[-2]
        house_item["location"] = response.css(
            "section.detail-info span.main-info__title-minor ::text"
        ).get()
        house_item["url"] = response.url
        house_item["title"] = response.css(
            "section.detail-info span.main-info__title-minor ::text"
        ).get()
        house_item["price"] = response.css(
            "section.detail-info .info-data-price ::text"
        ).get()
        house_item["features"] = response.css(
            "section.detail-info .info-features ::text"
        ).get()
        house_item["details"] = response.css(
            "section.detail-info .details-property ::text"
        ).get()
        house_item["description"] = response.css(
            "section.detail-info .comment ::text"
        ).get()

        yield house_item
