# main.py
from datetime import datetime,time
import db
import menu
import bcrypt

def main():
    db.create_table_vehicles()
    db.create_table_admin()
    # while running this program for the first time 
    # make sure to add this below admin in db 

    # password="Shashvat@123"
    # hashed_password = db.hash_password(password)
    # db.insert_admin("spatel",hashed_password)
    menu.run_menu()
    

if __name__ == "__main__":
    main()
