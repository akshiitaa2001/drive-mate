#setting up a connection to PostgreSQL using SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, DateTime, DECIMAL
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

#DATABASE_URL = "postgresql+psycopg2://postgres:Akshit%4001@localhost:5432/vehicle_rental_database"
#DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@vehicle-rental-database.cdy2k0g8ajwp.us-east-1.rds.amazonaws.com/vehicle_rental_database"

# Fetch the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Set up the database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)  # Unique username for login
    password_hash = Column(String(255), nullable=False)  # Store hashed password
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    registered_on = Column(DateTime, default=datetime.utcnow)
    age = Column(Integer, nullable=False)
    license_number = Column(String, nullable=False, unique=True)

    # Relationship with rentals
    rentals = relationship("Rental", back_populates="user")

    # Method to set the password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Define Vehicle model
class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    daily_rate = Column(DECIMAL, nullable=False)
    status = Column(String, nullable=False, default="Available")  # Default to Available
    location_city = Column(String, nullable=False)
    location_state = Column(String, nullable=False)
    location_latitude = Column(Float, nullable=True)
    location_longitude = Column(Float, nullable=True)

    # Relationships
    rentals = relationship("Rental", back_populates="vehicle")

# Define Rental model
class Rental(Base):
    __tablename__ = 'rentals'
    rental_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    pickup_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    pickup_location = Column(String, nullable=False)
    return_location = Column(String, nullable=False)
    total_cost = Column(DECIMAL, nullable=False)
    rental_status = Column(String, nullable=False, default="Ongoing")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="rentals")
    vehicle = relationship("Vehicle", back_populates="rentals")

# Define RentalSummary model
class RentalSummary(Base):
    __tablename__ = 'rental_summary'
    summary_id = Column(Integer, primary_key=True, index=True)
    rental_id = Column(Integer, ForeignKey('rentals.rental_id'), nullable=False)
    user_name = Column(String, nullable=False)
    user_location = Column(String, nullable=False)
    vehicle_details = Column(String, nullable=False)
    rental_duration = Column(Integer, nullable=False)
    total_cost = Column(DECIMAL, nullable=False)
    rental_status = Column(String, nullable=False)
    rental_category = Column(String, nullable=True)  # Optional category field
    last_updated = Column(DateTime, default=datetime.utcnow)

# Define VehicleRecommendations model
class VehicleRecommendations(Base):
    __tablename__ = 'vehicle_recommendations'
    recommendation_id = Column(Integer, primary_key=True, index=True)
    vehicle_id_1 = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    vehicle_id_2 = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    co_rent_count = Column(Integer, nullable=False)  # Number of times both vehicles were rented together
    recommendation_score = Column(Float, nullable=True)  # Optional score for recommendation strength
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships with vehicles
    vehicle1 = relationship("Vehicle", foreign_keys=[vehicle_id_1])
    vehicle2 = relationship("Vehicle", foreign_keys=[vehicle_id_2])

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
