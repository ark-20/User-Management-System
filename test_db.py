from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:admin@localhost/user_management"  # Replace with your actual URL

engine = create_engine(DATABASE_URL)

try:
    engine.connect()  # Try to connect
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection error: {e}")