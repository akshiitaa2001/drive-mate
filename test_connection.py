from sqlalchemy.sql import text
from database import SessionLocal, User

def test_connection():
    # Create a database session
    db = SessionLocal()
    try:
        # Attempt a simple query to test the connection
        result = db.execute(text("SELECT 1;"))
        # Fetch the result
        val = result.scalar()
        print("Connection test successful. Result:", val)
    except Exception as e:
        print("Connection test failed:", e)
    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    test_connection()
