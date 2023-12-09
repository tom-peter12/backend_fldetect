from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


SQLALCHEMY_DATABASE_URL = "postgresql://lyujcpfjqbvnex:381d732db3e80acfda4c9b081a8f9f2390474ec799b90b0ddac7e1eda24a645f@ec2-54-163-217-185.compute-1.amazonaws.com:5432/d3tgbj32opm6ne"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:

    try:
        conn = psycopg2.connect(host='ec2-54-163-217-185.compute-1.amazonaws.com', database='d3tgbj32opm6ne', user='lyujcpfjqbvnex',
                                password='381d732db3e80acfda4c9b081a8f9f2390474ec799b90b0ddac7e1eda24a645f', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


def check_database_connection() -> bool:
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(host='ec2-54-163-217-185.compute-1.amazonaws.com', database='d3tgbj32opm6ne', user='lyujcpfjqbvnex',
                password='381d732db3e80acfda4c9b081a8f9f2390474ec799b90b0ddac7e1eda24a645f', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return True
        except Exception as error:
            print("Connecting to database failed")
            print("Error: ", error)
            time.sleep(2)
            retries -= 1
    return False