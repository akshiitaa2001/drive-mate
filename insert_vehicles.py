from sqlalchemy.orm import sessionmaker
from database import engine, Vehicle

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample vehicles to insert
sample_vehicles = [
    Vehicle(make="Toyota", model="Corolla", year=2020, price_per_day=40),
    Vehicle(make="Honda", model="Civic", year=2019, price_per_day=35),
    Vehicle(make="Ford", model="Mustang", year=2021, price_per_day=70),
]

# Insert vehicles into the database
session.add_all(sample_vehicles)
session.commit()
session.close()

print("Sample vehicles added to the database.")
