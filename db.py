# db.py
import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime,time,timedelta

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)

def create_table_vehicles():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS vehicles_parked (
                number_plate VARCHAR(10) PRIMARY KEY,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                type ENUM('car','bike') not null,   
                isParked BOOLEAN default true
            )
        """))

def insert_car(number_plate, entry_time):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                INSERT INTO vehicles_parked (number_plate, entry_time,type)
                VALUES ('{number_plate}', '{entry_time}','car')
            """),
        )

def insert_bike(number_plate, entry_time):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                INSERT INTO vehicles_parked (number_plate, entry_time,type)
                VALUES ('{number_plate}', '{entry_time}','bike')
            """), 
        )

def dealloc_vehicle(number_plate,type,exit_time):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                UPDATE vehicles_parked SET isParked=false, exit_time='{exit_time}' where number_plate='{number_plate}' and type='{type}'
            """),
        )
        
def parked_cars_list():
    with engine.begin() as conn:
        result=conn.execute(text("SELECT * FROM vehicles_parked where isParked=true and type='car'"))
        cars = result.mappings().all()
        return cars

def parked_bikes_list():
    with engine.begin() as conn:
        result=conn.execute(text("SELECT * FROM vehicles_parked  where isParked=true and type='bike'"))
        bikes = result.mappings().all()
        return bikes

def no_parked_cars():
    with engine.begin() as conn:
        count=conn.execute(text("SELECT COUNT(*) FROM vehicles_parked where type='car'"))
        num = count.scalar()
        return num

def no_parked_bikes():
    with engine.begin() as conn:
        count=conn.execute(text("SELECT COUNT(*) FROM vehicles_parked where type='bike'"))
        num = count.scalar()
        return num

def get_all_parked_vehicles_details():
    with engine.begin() as conn:
        result=conn.execute(text("SELECT * FROM vehicles_parked"))
        vehicles = result.mappings().all()
        return vehicles
    
def get_filter_parked_vehicles_details(entry_date, exit_date):
    start = datetime.strptime(entry_date, "%Y-%m-%d")
    end   = datetime.strptime(exit_date, "%Y-%m-%d") + timedelta(days=1)

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
                username VARCHAR(255) primary key,
                password VARCHAR(255) 
            )
        """))

def insert_admin(username, password):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                INSERT INTO admin (username, password)
                VALUES ('{username}', '{password}')
            """),
        )

def get_admins():
    with engine.begin() as conn:
        result=conn.execute(text("SELECT * FROM admin"))
        admins = result.mappings().all()
        return admins
    
def update_admin(new_username,new_password):
    with engine.begin() as conn:
        conn.execute(text(f"UPDATE admin SET username='{new_username}' ,password='{new_password}'"))

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
