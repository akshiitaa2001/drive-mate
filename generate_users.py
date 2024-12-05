from faker import Faker
from sqlalchemy.orm import sessionmaker
from database import engine, User

# Initialize Faker and session
fake = Faker()
Session = sessionmaker(bind=engine)
session = Session()

# Generate 1000 fake users
generated_usernames = set()  # Track generated usernames to avoid duplicates
generated_emails = set()     # Track generated emails to avoid duplicates

for _ in range(1000):
    while True:
        username = fake.user_name()
        email = fake.email()
        # Check if the username or email already exists in the database or the generated sets
        if username not in generated_usernames and email not in generated_emails:
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            if not existing_user:
                generated_usernames.add(username)
                generated_emails.add(email)
                break

    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        username=username,
        email=email,
        phone_number=fake.phone_number(),
        address=fake.address(),
        city=fake.city(),
        state=fake.state(),
        postal_code=fake.postcode(),
        country="USA",  # Keep country consistent
        registered_on=fake.date_time_this_decade(),
        age=fake.random_int(min=18, max=70),
        license_number=fake.license_plate(),
    )
    # Hash the password
    user.set_password(fake.password())
    session.add(user)

# Commit and close the session
session.commit()
session.close()

print("User data generated successfully.")

