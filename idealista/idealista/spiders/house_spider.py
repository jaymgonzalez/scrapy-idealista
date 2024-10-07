# from urllib.parse import urlencode
# import scrapy
# from idealista.items import HouseItem
# import os
# import dotenv
# from idealista.db.functions import get_house_ids

# dotenv.load_dotenv()
# API_KEY = os.getenv("SCRAPERAPI_API_KEY")


# def get_scraperapi_url(url):
#     payload = {"api_key": API_KEY, "url": url}
#     proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
#     return proxy_url


# class HousespiderSpider(scrapy.Spider):
#     name = "house_spider"

#     def start_requests(self):

#         house_ids = get_house_ids()
#         start_urls = [f"http://www.idealista.com/inmueble/{house_id[0]}/" for house_id in house_ids]
#         for url in start_urls:
#             yield scrapy.Request(get_scraperapi_url(url), self.parse)

#     def parse(self, response):
#         house_item = HouseItem()
#         house_item["house_id"] = response.css(
#             "section.module-contact .ad-reference-container .txt-ref ::text"
#         ).get()
#         house_item["price"] = response.css(
#             "section.detail-info .info-data-price ::text"
#         ).get()
#         house_item["details"] = response.css(
#             "section.detail-info .details-property ::text"
#         ).get()
#         house_item["description"] = response.css(
#             "section.detail-info .comment ::text"
#         ).get()

#         yield house_item
