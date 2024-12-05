import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import engine, Vehicle

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read the CSV file
vehicle_data = pd.read_csv("CarRentalData.csv")

# Filter or limit vehicles to 1,500 rows (adjust as needed)
filtered_vehicle_data = vehicle_data.head(150)

# Iterate through the CSV and add data to the database
for index, row in filtered_vehicle_data.iterrows():
    vehicle = Vehicle(
        make=row['make'],
        model=row['model'],
        type=row['type'],
        year=int(row['year']),
        daily_rate=float(row['daily_rate']),
        status=row['status'] if row['status'] else "Available",
        location_city=row['location_city'],
        location_state=row['location_state'],
        location_latitude=row['location_latitude'],
        location_longitude=row['location_longitude'],
    )
    session.add(vehicle)

# Commit and close the session
session.commit()
session.close()

print("Vehicle data populated successfully.")
