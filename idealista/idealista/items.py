# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class HouseItem(Item):
    id = Field()
    house_id = Field()
    url = Field()
    location = Field()
    price = Field()
    features = Field()
    title = Field()
    details = Field()
    details_description = Field()
    rooms = Field()
    baths = Field()
    size = Field()
    house_type = Field()
    description = Field()
    terrace = Field()
    land = Field()
    floors = Field()
    garage = Field()
    condition = Field()
    swimming_pool = Field()
    garden = Field()
