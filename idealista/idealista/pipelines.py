from sqlalchemy.orm import sessionmaker
from db.models import Houses, engine, Garages
from utils.open_ai_functions import extract_item_attributes, GarageAttributes


class IdealistaPipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # find record by house_id
        record = self.session.query(Houses).filter_by(house_id=item.house_id).first()
        # find if the columns in record for price and details are empty
        if record.price is None or record.details is None:
            # update record
            record.price = item.price
            record.details = item.details
            record.description = item.description
            self.session.add(record)
        else:
            spider.logger.error("Couldnt find record with house_id: ", item.house_id)
        return item


class IdealistaIdHousesPipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        id = Houses(house_id=item["house_id"], location=item["location"])
        self.session.add(id)
        return item


# class IdealistaIdGaragePipeline:
#     def open_spider(self, spider):
#         self.Session = sessionmaker(bind=engine)
#         self.session = self.Session()

#     def close_spider(self, spider):
#         self.session.commit()
#         self.session.close()

#     def process_item(self, item, spider):
#         id = Garages(garage_id=item["garage_id"])
#         self.session.add(id)
#         return item


# class IdealistaGetDetailsGaragePipeline:
#     def open_spider(self, spider):
#         self.Session = sessionmaker(bind=engine)
#         self.session = self.Session()

#     def close_spider(self, spider):
#         self.session.commit()
#         self.session.close()

#     def clean_and_join(self, text_list):
#         cleaned_list = [
#             text.strip() for text in text_list if text.strip() and text.strip() != "\n"
#         ]
#         # Join into a single string
#         return " ".join(cleaned_list)

#     def process_item(self, item, spider):
#         url = f"http://www.idealista.com/inmueble/{item['garage_id']}/"

#         yield scrapy.Request(get_scraperapi_url(url), self.parse_garage)


class IdealistaGaragePipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        record = (
            self.session.query(Garages).filter_by(garage_id=item["garage_id"]).first()
        )
        if record is None:
            record = Garages(
                garage_id=item["garage_id"],
                price_string=item["price_string"],
                details=item["details"],
                description=item["description"],
                address=item["address"],
                title=item["title"],
                hood=item["hood"],
            )
            self.session.add(record)
        else:
            # If the record exists, you can update fields if needed
            record.garage_id = item["garage_id"]
            record.price_string = item["price_string"]
            record.details = item["details"]
            record.description = item["description"]
            record.address = item["address"]
            record.title = item["title"]
            record.hood = item["hood"]

            self.session.add(record)

        self.session.commit()

        return item


class OpenAIPipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        record = (
            self.session.query(Garages).filter_by(garage_id=item["garage_id"]).first()
        )

        fields = [record.price_string, record.details, record.description]
        data = "".join(field or "" for field in fields)

        response = extract_item_attributes(data, GarageAttributes)

        response = GarageAttributes.model_validate(response)

        record.price = response.price
        record.size_in_m2 = response.size_in_m2
        record.type = response.type
        record.covered = response.covered
        record.security = response.security
        record.expenses = response.expenses
        record.concesion = response.concesion

        self.session.commit()
