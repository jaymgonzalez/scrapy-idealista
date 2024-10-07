# test_db_query.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from idealista.db.models import Garages  # Import your Garage model

# Create an engine and session
engine = create_engine("sqlite:///idealista/data/scrapy_data.db")
Session = sessionmaker(bind=engine)
session = Session()

# Query the database for the garage_id 'PGRB4'
garage_id = "104633874"
record = session.query(Garages).filter_by(garage_id=garage_id).first()

if record:
    print(
        f"Record found: garage_id={record.garage_id}, price={record.price}, details={record.details}"
    )
else:
    print(f"Record with garage_id={garage_id} not found.")

# Close the session
session.close()
