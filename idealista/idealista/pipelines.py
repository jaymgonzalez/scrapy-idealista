from sqlalchemy.orm import sessionmaker
from db.models import Houses, engine, Garages
from utils.open_ai_functions import extract_item_attributes, GarageAttributes
import logging


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
            print("Couldnt find record with house_id: ", item.house_id)
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


class IdealistaIdGaragePipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        id = Garages(garage_id=item["garage_id"])
        self.session.add(id)
        return item


class IdealistaGaragePipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # find record by garage_id
        record = (
            self.session.query(Garages).filter_by(garage_id=item["garage_id"]).first()
        )
        # find if the columns in record for price and details are empty
        if record is None:
            spider.logger.error(
                f"Record with garage_id {item['garage_id']} not found in database."
            )
            return
        else:
            spider.logger.info(
                f"Record found: garage_id={record.garage_id}, price={record.price}, details={record.details}"
            )

            # update record
            record.price_string = item["price_string"]
            record.details = item["details"]
            record.description = item["description"]
            record.address = item["address"]
            record.title = item["title"]

            self.session.add(record)

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

        if record is None:
            logging.error(f"Couldn't find record with garage_id: {item['garage_id']}")
            return

        fields = [record.price, record.details, record.description]
        data = "".join(field or "" for field in fields)

        response = extract_item_attributes(data, GarageAttributes)

        print(response)

        response = GarageAttributes.model_validate(response)
        # Update the existing record

        record.price = response.price
        record.size_in_m2 = response.size_in_m2
        record.type = response.type
        record.covered = response.covered
        record.security = response.security
        record.expenses = response.expenses
        record.concesion = response.concesion
        record.hood = response.hood

        # Commit the changes
        self.session.commit()
