# test_db_query.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from idealista.db.models import Garages  # Import your Garage model
from idealista.utils.open_ai_functions import GarageAttributes, extract_item_attributes

# Create an engine and session
engine = create_engine("sqlite:///idealista/data/scrapy_data.db")
Session = sessionmaker(bind=engine)
session = Session()

# Query the database for the garage_id 'PGRB4'
garage_id = "103111781"
record = session.query(Garages).filter_by(garage_id=garage_id).first()

if record:
    print(
        f"Record found: garage_id={record.garage_id}, price={record.price}, details={record.details}"
    )

    fields = [record.price_string, record.details, record.description]
    data = "".join(field or "" for field in fields)

    response = extract_item_attributes(data, GarageAttributes)

    # print(response)

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
    session.commit()
else:
    print(f"Record with garage_id={garage_id} not found.")

# Close the session
session.close()
