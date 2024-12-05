from sqlalchemy.orm import Session
from database import SessionLocal, Rental, User, Vehicle, RentalSummary
from datetime import datetime
import pytz

# Define time zones
utc = pytz.utc
est = pytz.timezone('US/Eastern')

def extract_data(session: Session):
    """
    Extracts data from the rentals, users, and vehicles tables.
    """
    rentals = session.query(Rental).all()
    return rentals

def transform_data(rentals, session: Session):
    """
    Transforms the extracted data into the format required for the RentalSummary table.
    """
    transformed_data = []
    
    for rental in rentals:
        # Fetch related user and vehicle data
        user = session.query(User).filter(User.user_id == rental.user_id).first()
        vehicle = session.query(Vehicle).filter(Vehicle.vehicle_id == rental.vehicle_id).first()

        if not user or not vehicle:
            continue  # Skip if user or vehicle is not found

        # Calculate rental duration in days
        rental_duration = (rental.return_date - rental.pickup_date).days
        rental_duration = max(rental_duration, 1)  # Ensure at least 1 day

        # Generate rental category (Optional: Add your own logic here)
        rental_category = "Luxury" if vehicle.type.lower() == "suv" else "Economy"

        # Get the current UTC time and convert it to EST
        current_utc_time = datetime.now(utc)
        last_updated_est = current_utc_time.astimezone(est)
        
        # Create a transformed record
        transformed_record = RentalSummary(
            rental_id=rental.rental_id,
            user_name=f"{user.first_name} {user.last_name}",
            user_location=f"{user.city}, {user.state}",
            vehicle_details=f"{vehicle.make} {vehicle.model} - {vehicle.type}",
            rental_duration=rental_duration,
            total_cost=rental.total_cost,
            rental_status=rental.rental_status,
            rental_category=rental_category,
            last_updated=last_updated_est  # Store in EST
        )

        transformed_data.append(transformed_record)

    return transformed_data

def load_data(transformed_data, session: Session):
    """
    Loads transformed data into the RentalSummary table.
    """
    for record in transformed_data:
        # Check if the rental_id already exists in the summary table
        existing_record = session.query(RentalSummary).filter(RentalSummary.rental_id == record.rental_id).first()
        if existing_record:
            # Update the existing record
            existing_record.user_name = record.user_name
            existing_record.user_location = record.user_location
            existing_record.vehicle_details = record.vehicle_details
            existing_record.rental_duration = record.rental_duration
            existing_record.total_cost = record.total_cost
            existing_record.rental_status = record.rental_status
            existing_record.rental_category = record.rental_category
            existing_record.last_updated = record.last_updated
        else:
            # Insert new record
            session.add(record)

    session.commit()

def run_etl():
    """
    Runs the ETL process to populate the RentalSummary table.
    """
    session = SessionLocal()

    try:
        # Step 1: Extract
        rentals = extract_data(session)

        # Step 2: Transform
        transformed_data = transform_data(rentals, session)

        # Step 3: Load
        load_data(transformed_data, session)

        print("ETL process completed successfully!")
    except Exception as e:
        print(f"An error occurred during the ETL process: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()
