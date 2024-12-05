from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Base, engine, SessionLocal, init_db, User, Vehicle, Rental, RentalSummary, VehicleRecommendations
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from etl_process import run_etl

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages
app.config['SESSION_TYPE'] = 'filesystem'  # To store session data on the filesystem

# Create all tables
Base.metadata.create_all(engine)

# Initialize database tables
def init_database():
    from database import init_db
    init_db()  # Create tables if they don't already exist

# Home Route (only one route for '/')
@app.route('/')
def index():
    if 'user_id' in session:
        # If user is already logged in, redirect to the rent_vehicle page
        return redirect(url_for('rent_vehicle'))
    # If not logged in, show options to log in or register
    return render_template('index.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    session_db = SessionLocal()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        age = request.form['age']
        # Collect additional demographic data
        city = request.form['city']
        state = request.form['state']
        postal_code = request.form['postal_code']
        country = request.form['country']  # Default is USA
        license_number = request.form['license_number']
        
        # Check if username already exists
        existing_user = session_db.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please log in instead.")
            session_db.close()
            return redirect(url_for('login'))

        # Create and add new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password_hash=generate_password_hash(password),
            email=email,
            phone_number=phone_number,
            age=age,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            license_number=license_number
        )
        
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    session_db = SessionLocal()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Retrieve user by username
        user = session_db.query(User).filter_by(username=username).first()
        
        if user:
            if user.check_password(password):
                # Set session with user_id
                session['user_id'] = user.user_id
                flash("Login successful!")
                session_db.close()
                return redirect(url_for('rent_vehicle'))
            else:
                flash("Incorrect password. Please try again.")
        else:
            flash("Username does not exist. Please check or register.")

        session_db.close()
        return redirect(url_for('login'))

    return render_template('login.html')

# Add User Route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    session = SessionLocal()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        license_number = request.form['license_number']
        
        new_user = User(name=name, age=int(age), license_number=license_number)
        session.add(new_user)
        session.commit()
        session.close()
        return redirect(url_for('user_added'))

    return render_template('add_user.html')

@app.route('/user_added')
def user_added():
    return "User added successfully!"

# Rent Vehicle Route
@app.route('/rent_vehicle', methods=['GET', 'POST'])
def rent_vehicle():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to rent a vehicle.")
        return redirect(url_for('login'))
    
    session_db = SessionLocal()
    user_id = session['user_id']
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        customer_id = session['user_id']  # Get user ID from the session
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']

        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Validate vehicle_id
        vehicle = session_db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
        if not vehicle_id:
            session_db.close()
            return "Vehicle selection is required.", 400
        
        # Convert vehicle_id to integer if not empty
        vehicle_id = int(vehicle_id)
        
        # Check if the vehicle is available for the specified dates
        overlapping_rentals = session_db.query(Rental).filter(
            Rental.vehicle_id == vehicle_id,
            Rental.return_date >= start_date,
            Rental.pickup_date <= end_date
        ).all()

        if overlapping_rentals:
            session_db.close()
            return "Vehicle is already rented for the selected dates."

        # Use vehicle location as pickup/return location
        pickup_location = f"{vehicle.location_city}, {vehicle.location_state}"
        return_location = pickup_location  # Assume same location for now

        # Calculate rental days and cost
        rental_days = (end_date - start_date).days
        if rental_days <= 0:
            session_db.close()
            return "Invalid rental duration. End date must be after start date.", 400
            
        total_cost = rental_days * float(vehicle.daily_rate)

        # Create a new rental record
        rental = Rental(
            user_id=customer_id,
            vehicle_id=vehicle_id,
            pickup_date=start_date,
            return_date=end_date,
            pickup_location=pickup_location,
            return_location=return_location,
            total_cost=total_cost,
            rental_status="Ongoing"
        )
        
        session_db.add(rental)
        session_db.commit()

        # Redirect to the confirmation page with the rental ID
        rental_id = rental.rental_id
        session_db.close()
        return redirect(url_for('rental_confirmation', rental_id=rental_id))

    # Fetch all vehicles for the dropdown in GET request
    vehicles = session_db.query(Vehicle).all()

    # Fetch recommendations
    recommended_vehicles = get_recommended_vehicles(user_id)

    session_db.close()
    return render_template('rent_vehicle.html', vehicles=vehicles, recommended_vehicles=recommended_vehicles)

# Rental Confirmation Route
@app.route('/rental_confirmation/<int:rental_id>')
def rental_confirmation(rental_id):
    session = SessionLocal()
    
    # Retrieve the rental
    rental = session.query(Rental).filter(Rental.rental_id == rental_id).first()
    if not rental:
        session.close()
        return "Rental not found!"
    
    # Retrieve the associated user and vehicle
    user = session.query(User).filter(User.user_id == rental.user_id).first()
    vehicle = session.query(Vehicle).filter(Vehicle.vehicle_id == rental.vehicle_id).first()

    # Calculate the total cost
    pickup_date = rental.pickup_date
    return_date = rental.return_date
    rental_days = (return_date - pickup_date).days
    total_cost = rental_days * vehicle.daily_rate if rental_days > 0 else vehicle.daily_rate
    
    session.close()
    
    return render_template(
        'rental_confirmation.html', 
        rental=rental, 
        user=user, 
        vehicle=vehicle, 
        total_cost=total_cost,
        price_per_day=vehicle.daily_rate
    )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user session
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))

@app.route('/etl_status', methods=['GET', 'POST'])
def etl_status():
    session = SessionLocal()
    last_updated = None
    total_records = 0

    if request.method == 'POST':
        # Trigger the ETL process manually
        try:
            run_etl()
            flash("ETL process completed successfully!", "success")
        except Exception as e:
            flash(f"Error running ETL process: {e}", "error")

    try:
        # Fetch the last update timestamp and record count
        summary_records = session.query(RentalSummary).all()
        total_records = len(summary_records)
        if total_records > 0:
            last_updated = max(record.last_updated for record in summary_records)
    except Exception as e:
        flash(f"Error fetching ETL status: {e}", "error")
    finally:
        session.close()

    return render_template(
        'etl_status.html',
        total_records=total_records,
        last_updated=last_updated
    )

from sqlalchemy.orm import joinedload

def get_recommended_vehicles(user_id):
    session = SessionLocal()
    try:
        # Fetch the user's rental history
        user_rentals = session.query(Rental).filter(Rental.user_id == user_id).all()
        rented_vehicle_ids = {rental.vehicle_id for rental in user_rentals}

        # Fetch recommendations based on rented vehicles
        recommendations = session.query(VehicleRecommendations).filter(
            VehicleRecommendations.vehicle_id_1.in_(rented_vehicle_ids)
        ).order_by(VehicleRecommendations.recommendation_score.desc()).limit(5).all()

        # Fetch the recommended vehicle details
        recommended_vehicle_ids = {rec.vehicle_id_2 for rec in recommendations}
        recommended_vehicles = session.query(Vehicle).filter(
            Vehicle.vehicle_id.in_(recommended_vehicle_ids)
        ).all()

        return recommended_vehicles
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)