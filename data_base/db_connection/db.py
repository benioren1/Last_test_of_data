from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:1234@localhost:5432/terror_db"
engine = create_engine(DATABASE_URL)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

def check_db_connection():
    try:
        with engine.connect() as conn:
            print("Connection to database is successful.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)