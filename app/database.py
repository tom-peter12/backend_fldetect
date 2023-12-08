from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


SQLALCHEMY_DATABASE_URL = "postgresql://rutfjftynzisze:ee18d1ac530ddd10241af9264c81be1306a83175cb760431a973faedc3e80a1a@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d2p75n9db98v6"


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
        conn = psycopg2.connect(host='ec2-3-210-173-88.compute-1.amazonaws.com', database='d2p75n9db98v6', user='rutfjftynzisze',
                                password='ee18d1ac530ddd10241af9264c81be1306a83175cb760431a973faedc3e80a1a', cursor_factory=RealDictCursor)
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
            conn = psycopg2.connect(host='ec2-3-210-173-88.compute-1.amazonaws.com', database='d2p75n9db98v6', user='rutfjftynzisze',
                password='ee18d1ac530ddd10241af9264c81be1306a83175cb760431a973faedc3e80a1a', cursor_factory=RealDictCursor)
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