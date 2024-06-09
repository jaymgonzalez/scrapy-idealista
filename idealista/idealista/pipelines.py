from sqlalchemy.orm import sessionmaker
from idealista.db.models import Houses, engine


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


class IdealistaIdPipeline:
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
