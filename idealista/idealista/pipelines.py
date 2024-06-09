from sqlalchemy.orm import sessionmaker
from idealista.db.models import HouseLocation, HouseDetails, engine


class IdealistaPipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        location = HouseLocation(house_id=item["id"], location=item["location"])
        self.session.add(location)
        self.session.flush()  # Ensure location.id is available

        details = HouseDetails(
            id=location.id,
            title=item.get("title"),
            price=item.get("price"),
            features=item.get("features"),
            details=item.get("details"),
            description=item.get("description"),
        )
        self.session.add(details)
        return item


class IdealistaIdPipeline:
    def open_spider(self, spider):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        id = HouseLocation(house_id=item["house_id"], location=item["location"])
        self.session.add(id)
        return item
