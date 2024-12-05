import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from database import engine, User, Vehicle, Rental

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all users and vehicles
users = session.query(User).all()
vehicles = session.query(Vehicle).all()

# Generate random rental records
rental_status_options = ["Completed", "Ongoing", "Cancelled"]

# Each user gets 5–10 rentals on average
for user in users:
    num_rentals = random.randint(5, 10)  # 5–10 rentals per user
    for _ in range(num_rentals):
        vehicle = random.choice(vehicles)

        # Generate random pickup and return dates
        pickup_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
        return_date = pickup_date + timedelta(days=random.randint(1, 14))  # 1-14 day rentals

        # Calculate total cost
        total_days = (return_date - pickup_date).days
        total_cost = total_days * float(vehicle.daily_rate)

        rental = Rental(
            user_id=user.user_id,
            vehicle_id=vehicle.vehicle_id,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=vehicle.location_city,
            return_location=vehicle.location_city,
            total_cost=total_cost,
            rental_status=random.choice(rental_status_options),
            created_at=datetime.utcnow()
        )
        session.add(rental)

# Commit and close the session
session.commit()
session.close()

print("Rental data populated successfully.")
