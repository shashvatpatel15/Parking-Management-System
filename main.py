# main.py
import os
import db
import menu
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("ADMIN_PASSWORD")
username = os.getenv("ADMIN_USERNAME")

def main():
    db.create_table_vehicles()
    db.create_table_admin()
    if not db.get_admins():
        hashed_password = db.hash_password(password)
        db.insert_admin(username, hashed_password)

    menu.run_menu()

if __name__ == "__main__":
    main()

