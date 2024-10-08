from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()


class Houses(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(String)
    location = Column(String)
    price = Column(String)
    details = Column(String)
    description = Column(String)
    house_size = Column(String)
    condition = Column(String)
    house_type = Column(String)
    rooms = Column(Integer)
    floors = Column(Integer)
    bathrooms = Column(Integer)
    lot_size = Column(Integer)
    built_year = Column(Integer)
    air_conditioning = Column(Integer)
    terrace = Column(Integer)
    garage = Column(Integer)
    heating = Column(Integer)
    garden = Column(Integer)
    storage_room = Column(Integer)
    swimming_pool = Column(Integer)
    elevator = Column(Integer)


class Garages(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    garage_id = Column(String)
    lat = Column(Integer)
    long = Column(Integer)
    price = Column(Integer)
    price_string = Column(String)
    size_in_m2 = Column(Integer)
    title = Column(String)
    details = Column(String)
    description = Column(String)
    type = Column(String)  # big car, motorcycle, small car, etc
    covered = Column(Boolean)
    security = Column(Boolean)
    expenses = Column(Integer)
    concesion = Column(Boolean)
    pictures = Column(String)
    address = Column(String)
    hood = Column(String)
    last_updated = Column(String)
    sell = Column(Integer)
    rent = Column(Integer)


current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "data", "scrapy_data.db")
db_path = os.path.normpath(db_path)

engine = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
