# db.py
import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)

def create_table_vehicles():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS vehicles_parked (
                number_plate VARCHAR(10) PRIMARY KEY,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                type VARCHAR(10) NOT NULL,   
                isParked INTEGER DEFAULT 1
            )
        """))

def insert_car(number_plate, entry_time):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO vehicles_parked (number_plate, entry_time, type)
                VALUES (:number_plate, :entry_time, 'car')
            """),
            {"number_plate": number_plate, "entry_time": entry_time}
        )

def insert_bike(number_plate, entry_time):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO vehicles_parked (number_plate, entry_time, type)
                VALUES (:number_plate, :entry_time, 'bike')
            """),
            {"number_plate": number_plate, "entry_time": entry_time}
        )

def dealloc_vehicle(number_plate, vehicle_type, exit_time):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE vehicles_parked 
                SET isParked = 0, exit_time = :exit_time 
                WHERE number_plate = :number_plate AND type = :type
            """),
            {"exit_time": exit_time, "number_plate": number_plate, "type": vehicle_type}
        )
        
def parked_cars_list():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM vehicles_parked WHERE isParked = 1 AND type = 'car'"))
        return result.mappings().all()

def parked_bikes_list():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM vehicles_parked WHERE isParked = 1 AND type = 'bike'"))
        return result.mappings().all()

def no_parked_cars():
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM vehicles_parked WHERE type = 'car' AND isParked = 1"))
        return count.scalar()

def no_parked_bikes():
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM vehicles_parked WHERE type = 'bike' AND isParked = 1"))
        return count.scalar()

def get_all_parked_vehicles_details():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM vehicles_parked"))
        return result.mappings().all()
    
def get_filter_parked_vehicles_details(entry_date, exit_date):
    start = datetime.strptime(entry_date, "%Y-%m-%d")
    end = datetime.strptime(exit_date, "%Y-%m-%d") + timedelta(days=1)

    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM vehicles_parked
                WHERE entry_time >= :start
                  AND exit_time <= :end
            """),
            {
                "start": start,
                "end": end
            }
        )
        return result.mappings().all()
  
def create_table_admin():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS admin (
                username VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) 
            )
        """))

def insert_admin(username, password):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO admin (username, password)
                VALUES (:username, :password)
            """),
            {"username": username, "password": password}
        )

def get_admins():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM admin"))
        return result.mappings().all()
    
def update_admin(new_username, new_password):
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE admin SET username = :new_username, password = :new_password"),
            {"new_username": new_username, "new_password": new_password}
        )

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

