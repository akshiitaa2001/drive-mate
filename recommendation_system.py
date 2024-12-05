from sqlalchemy.orm import Session
from database import SessionLocal, Rental, Vehicle, VehicleRecommendations
from collections import defaultdict
from datetime import datetime


def extract_rental_data(session: Session):
    """
    Extract rental data from the database.
    """
    rentals = session.query(Rental).all()
    return rentals


def map_phase(rentals):
    """
    Map phase: Generate (vehicle_id_1, vehicle_id_2) pairs from rentals.
    """
    vehicle_pairs = defaultdict(int)

    # Group rentals by user
    user_rentals = defaultdict(list)
    for rental in rentals:
        user_rentals[rental.user_id].append(rental.vehicle_id)

    # Generate vehicle pairs for each user's rentals
    for vehicle_list in user_rentals.values():
        vehicle_list = list(set(vehicle_list))  # Remove duplicate rentals
        for i in range(len(vehicle_list)):
            for j in range(i + 1, len(vehicle_list)):
                pair = tuple(sorted((vehicle_list[i], vehicle_list[j])))
                vehicle_pairs[pair] += 1

    return vehicle_pairs


def reduce_phase(vehicle_pairs):
    """
    Reduce phase: Consolidate and calculate recommendation scores.
    """
    recommendations = []
    for (vehicle_id_1, vehicle_id_2), co_rent_count in vehicle_pairs.items():
        recommendations.append({
            'vehicle_id_1': vehicle_id_1,
            'vehicle_id_2': vehicle_id_2,
            'co_rent_count': co_rent_count,
            'recommendation_score': co_rent_count  # Basic score based on co-rent count
        })
    return recommendations


def load_recommendations(recommendations, session: Session):
    """
    Load recommendations into the VehicleRecommendations table.
    """
    for rec in recommendations:
        existing_rec = session.query(VehicleRecommendations).filter(
            VehicleRecommendations.vehicle_id_1 == rec['vehicle_id_1'],
            VehicleRecommendations.vehicle_id_2 == rec['vehicle_id_2']
        ).first()

        if existing_rec:
            # Update existing record
            existing_rec.co_rent_count = rec['co_rent_count']
            existing_rec.recommendation_score = rec['recommendation_score']
            existing_rec.last_updated = datetime.utcnow()
        else:
            # Insert new record
            new_rec = VehicleRecommendations(
                vehicle_id_1=rec['vehicle_id_1'],
                vehicle_id_2=rec['vehicle_id_2'],
                co_rent_count=rec['co_rent_count'],
                recommendation_score=rec['recommendation_score'],
                last_updated=datetime.utcnow()
            )
            session.add(new_rec)

    session.commit()


def run_recommendation_system():
    """
    Run the recommendation system using MapReduce.
    """
    session = SessionLocal()

    try:
        # Step 1: Extract data
        rentals = extract_rental_data(session)

        # Step 2: Map phase
        vehicle_pairs = map_phase(rentals)

        # Step 3: Reduce phase
        recommendations = reduce_phase(vehicle_pairs)

        # Step 4: Load recommendations into the database
        load_recommendations(recommendations, session)

        print("Recommendation system updated successfully!")
    except Exception as e:
        print(f"An error occurred during the recommendation process: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run_recommendation_system()
