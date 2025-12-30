import db
from datetime import datetime,time,date
import bcrypt

def run_menu():
    # max_cars=int(input("Enter cars capacity for parking:"))
    # max_bikes=int(input("Enter bikes capacity for parking:"))
    max_cars=5
    max_bikes=5
    cars_parked=db.no_parked_cars()
    bikes_parked=db.no_parked_bikes()

    def alloc_parking(type):
        isFound=0
        if(type.lower()=="car" and (cars_parked<max_cars)):
            number_plate=input("Enter number plate of car:")
            cars=db.parked_cars_list()
            for car in cars:
                if(car["number_plate"]==number_plate):
                    print("Already Parked")
                    isFound=1
                    break
            if(isFound==0):
                entry_time = datetime.now()
                db.insert_car(number_plate,entry_time)   
        elif(type.lower()=="bike" and (bikes_parked<max_bikes)):
            number_plate=input("Enter number plate of bike:")
            entry_time = datetime.now()
            bikes=db.parked_bikes_list()
            for bike in bikes:
                if(bike["number_plate"]==number_plate):
                    print("Already Parked")
                    isFound=1
                    break
            if(isFound==0):
                entry_time = datetime.now()
                db.insert_bike(number_plate,entry_time)
        else:
            print("invalid input...")

    def de_alloc_parking(number_plate):
        isFound=0
        cars=db.parked_cars_list()
        for car in cars:
            if(car["number_plate"]==number_plate):
                print("Found")
                exit_time = datetime.now()
                difference=exit_time-car["entry_time"]
                hrs=(int(difference.total_seconds()/3600)+1)
                charges=40*hrs
                print("Charges:",charges)
                db.dealloc_vehicle(number_plate,"car",exit_time)
                isFound=1
        if(isFound==0):
            bikes=db.parked_bikes_list()
            for bike in bikes:
                if(bike["number_plate"]==number_plate):
                    exit_time = datetime.now()
                    difference=exit_time-bike["entry_time"]
                    hrs=(int(difference.total_seconds()/3600)+1)
                    charges=20*hrs
                    print("Charges:",charges)
                    db.dealloc_vehicle(number_plate,"bike",exit_time)

    while(1):
        print("MENU: 1.ToPark 2.ToExit 3.PrintParkedCars 4.PrintParkedBikes 5.PrintAllParkingRecords 6.FilterPrintAllParkingRecords 7.AdminPanel 8.ChangeAdmin 9.Exit")
        try:
            n=int(input("Enter your choice:"))
        except ValueError:
            print("invalid input...")
            
        if(n==1):
            type=input("Enter type:")
            while(1):
                if(type.lower() in ["car","bike"] ):
                    alloc_parking(type)
                    break
                else:
                    print("invalid input...")
                    type=input("Enter type:")
        elif(n==2):
            number_plate=input("Enter number plate:")
            de_alloc_parking(number_plate)
        elif(n==3):
            cars=db.parked_cars_list()
            
            if not cars:
                print("Zero Car Parked")
            else:
                for car in cars:
                    for key, value in car.items():
                        print(f"{key}: {value}")
                    print("-" * 50)
        elif(n==4):
            bikes=db.parked_bikes_list()
            
            if not bikes:
                print("Zero Bikes Parked")
            else:
                for bike in bikes:
                    for key, value in bike.items():
                        print(f"{key}: {value}")
                    print("-" * 50)
        
        elif(n==5):
            vehicles=db.get_all_parked_vehicles_details()
            for vehicle in vehicles:
                for key, value in vehicle.items():
                    print(f"{key}: {value}")
                print("-" * 50)
        elif(n==6):  
            def validate_date_input(prompt):
                user_input = input(prompt).strip()

                # Empty input check
                if not user_input:
                    raise ValueError("Date cannot be empty.")

                # Format + calendar date validation
                try:
                    parsed_date = datetime.strptime(user_input, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD.")

                # Future date validation 
                if parsed_date > date.today():
                    raise ValueError("Date cannot be in the future.")

                return parsed_date

            try:
                # Validate inputs
                entry_date = validate_date_input("Enter entry date (YYYY-MM-DD): ")
                exit_date = validate_date_input("Enter exit date (YYYY-MM-DD): ")

                if exit_date < entry_date:
                    raise ValueError("Exit date cannot be earlier than entry date.")

                # Convert back to string if DB expects string
                vehicles = db.get_filter_parked_vehicles_details(
                    entry_date.strftime("%Y-%m-%d"),
                    exit_date.strftime("%Y-%m-%d")
                )

                if not vehicles:
                    print("No vehicles found.")
                else:
                    for vehicle in vehicles:
                        for key, value in vehicle.items():
                            print(f"{key}: {value}")
                        print("-" * 50)
            except ValueError as e:
                print(f"Input Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")

        elif(n==7):
            username=input("Enter admin's username:")
            password=input("Enter admin's password:")
            admins=db.get_admins()
            isFound=0
            for admin in admins:
                if(db.verify_password(password,admin["password"]) and admin["username"]==username):
                    isFound=1
                    def compute(entry_date,exit_date):
                        
                        vehicles = db.get_filter_parked_vehicles_details(
                            entry_date.strftime("%Y-%m-%d"),
                            exit_date.strftime("%Y-%m-%d")
                        )
                        num_cars=0
                        num_bikes=0
                        if not vehicles:
                            print("No vehicles found.")
                        else:
                            for vehicle in vehicles:
                                if(vehicle["type"]=="car" and vehicle["isParked"]==False):
                                    num_cars+=1
                                elif(vehicle["type"]=="bike" and vehicle["isParked"]==False):
                                    num_bikes+=1
                            print("revenue through cars:",40*num_cars)
                            print("revenue through bikes:",20*num_bikes)
                    while(1):
                        print("MENU: 1.Annual Revenue 2.Monthly Revenue 3.Current Month Revenue 4.Custom Revenue 5.Exit")
                        choice=int(input("Enter your choice:"))   
                        if(choice==1):
                            entry_date = datetime(2025, 1, 1, 0, 0, 0)
                            exit_date   = datetime(2025, 12, 31, 23, 59, 59)
                            compute(entry_date,exit_date)
                        elif(choice==2):
                            for i in range(1,13):
                                if(i==2):
                                    entry_date = datetime(2025, 2, 1, 0, 0, 0)
                                    exit_date   = datetime(2025, 2, 28, 23, 59, 59)
                                else:
                                    entry_date = datetime(2025, i, 1, 0, 0, 0)
                                    exit_date   = datetime(2025, i, 31, 23, 59, 59)
                                compute(entry_date,exit_date)
                        elif(choice==3):                            
                            compute(entry_date,exit_date)
                        elif(choice==4):
                            try:
                                # Validate inputs
                                entry_date = validate_date_input("Enter entry date (YYYY-MM-DD): ")
                                exit_date = validate_date_input("Enter exit date (YYYY-MM-DD): ")

                                if exit_date < entry_date:
                                    raise ValueError("Exit date cannot be earlier than entry date.")

                                # Convert back to string if DB expects string
                                vehicles = db.get_filter_parked_vehicles_details(
                                    entry_date.strftime("%Y-%m-%d"),
                                    exit_date.strftime("%Y-%m-%d")
                                )
                                num_cars=0
                                num_bikes=0
                                if not vehicles:
                                    print("No vehicles found.")
                                else:
                                    for vehicle in vehicles:
                                        if(vehicle["type"]=="car" and vehicle["isParked"]==False):
                                            num_cars+=1
                                        elif(vehicle["type"]=="bike" and vehicle["isParked"]==False):
                                            num_bikes+=1
                                    print("revenue through cars:",40*num_cars)
                                    print("revenue through bikes:",20*num_bikes)
                            except ValueError as e:
                                print(f"Input Error: {e}")
                            except Exception as e:
                                print(f"Unexpected Error: {e}")
                        else:
                            print("exiting...")
            if(isFound==0):
                print("no found...")

        elif(n==8):
            username=input("Enter admin's username:")
            password=input("Enter admin's password:")          
            # converting password to array of bytes
            bytes = password.encode('utf-8')
            # generating the salt
            salt = bcrypt.gensalt()
            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)

            isFound=0
            admins=db.get_admins()
            for admin in admins:
                if(db.verify_password(password,admin["password"]) and admin["username"]==username):
                    new_username=input("Enter new username:")
                    new_password=input("Enter new password:")
                    new_password=db.hash_password(new_password)
                    db.update_admin(new_username,new_password)
                else:
                    print("incorrect password or username...")
        else:
            print("exiting...")
            break

