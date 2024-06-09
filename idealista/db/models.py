from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()


class HouseLocation(Base):
    __tablename__ = "house_location"
    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(String)
    location = Column(String)

    details = relationship("HouseDetails", back_populates="location", uselist=False)


class HouseDetails(Base):
    __tablename__ = "house_details"
    id = Column(Integer, ForeignKey("house_location.id"), primary_key=True)
    url = Column(String)
    price = Column(String)
    features = Column(String)
    details_description = Column(String)
    title = Column(String)
    rooms = Column(String)
    baths = Column(String)
    size = Column(String)
    house_type = Column(String)
    description = Column(String)
    terrace = Column(String)
    land = Column(String)
    floors = Column(String)
    garage = Column(String)
    condition = Column(String)
    swimming_pool = Column(String)
    garden = Column(String)

    location = relationship("HouseLocation", back_populates="details")


engine = create_engine("sqlite:///scrapy_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
