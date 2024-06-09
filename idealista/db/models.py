from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

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

engine = create_engine("sqlite:///idealista/data/scrapy_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
