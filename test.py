from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal, User, Vehicle, Rental, VehicleRecommendations

def get_user_recommendations(user_id):
    session = SessionLocal()
    try:
        # Fetch the user's rental history
        user_rentals = session.query(Rental).filter(Rental.user_id == user_id).all()
        rented_vehicle_ids = {rental.vehicle_id for rental in user_rentals}

        if not rented_vehicle_ids:
            print(f"No rental history found for user ID: {user_id}")
            return

        # Fetch recommendations based on rented vehicles
        recommendations = session.query(VehicleRecommendations).filter(
            VehicleRecommendations.vehicle_id_1.in_(rented_vehicle_ids)
        ).order_by(VehicleRecommendations.recommendation_score.desc()).all()

        if not recommendations:
            print(f"No recommendations found for user ID: {user_id}")
            return

        # Fetch the recommended vehicle details
        recommended_vehicle_ids = {rec.vehicle_id_2 for rec in recommendations}
        recommended_vehicles = session.query(Vehicle).filter(
            Vehicle.vehicle_id.in_(recommended_vehicle_ids)
        ).all()

        print(f"Recommendations for User ID: {user_id}")
        for vehicle in recommended_vehicles:
            print(f"- {vehicle.make} {vehicle.model} ({vehicle.type}) - ${vehicle.daily_rate}/day")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    user_id = int(input("Enter the User ID to fetch recommendations: "))
    get_user_recommendations(user_id)


