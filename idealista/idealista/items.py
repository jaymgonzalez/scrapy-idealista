# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class HouseItem(Item):
    house_id = Field()
    location = Field()
    price = Field()
    details = Field()
    description = Field()


class GarageItem(Item):
    garage_id = Field()
    price_string = Field()
    title = Field()
    details = Field()
    description = Field()
    address = Field()
    hood = Field()
    sell = Field()
    rent = Field()
