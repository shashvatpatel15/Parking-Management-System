import db
from datetime import datetime, date
import calendar

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

def run_menu():
    max_cars = 50
    max_bikes = 50

    def alloc_parking(vehicle_type):
        vehicle_type = vehicle_type.lower()
        if vehicle_type == "car":
            cars_parked = db.no_parked_cars()
            if cars_parked >= max_cars:
                print("Parking is full for cars!")
                return
            number_plate = input("Enter number plate of car: ").strip()
            if not number_plate:
                print("Number plate cannot be empty.")
                return
            cars = db.parked_cars_list()
            is_found = False
            for car in cars:
                if car["number_plate"] == number_plate:
                    print("Already Parked")
                    is_found = True
                    break
            if not is_found:
                entry_time = datetime.now()
                db.insert_car(number_plate, entry_time)
                print(f"Car '{number_plate}' parked successfully.")
        elif vehicle_type == "bike":
            bikes_parked = db.no_parked_bikes()
            if bikes_parked >= max_bikes:
                print("Parking is full for bikes!")
                return
            number_plate = input("Enter number plate of bike: ").strip()
            if not number_plate:
                print("Number plate cannot be empty.")
                return
            bikes = db.parked_bikes_list()
            is_found = False
            for bike in bikes:
                if bike["number_plate"] == number_plate:
                    print("Already Parked")
                    is_found = True
                    break
            if not is_found:
                entry_time = datetime.now()
                db.insert_bike(number_plate, entry_time)
                print(f"Bike '{number_plate}' parked successfully.")
        else:
            print("Invalid vehicle type.")

    def de_alloc_parking(number_plate):
        number_plate = number_plate.strip()
        if not number_plate:
            print("Number plate cannot be empty.")
            return
        
        is_found = False
        cars = db.parked_cars_list()
        for car in cars:
            if car["number_plate"] == number_plate:
                print("Found vehicle: Car")
                exit_time = datetime.now()
                difference = exit_time - car["entry_time"]
                hrs = int(difference.total_seconds() / 3600) + 1
                charges = 40 * hrs
                print("Charges: ₹", charges)
                db.dealloc_vehicle(number_plate, "car", exit_time)
                is_found = True
                break
                
        if not is_found:
            bikes = db.parked_bikes_list()
            for bike in bikes:
                if bike["number_plate"] == number_plate:
                    print("Found vehicle: Bike")
                    exit_time = datetime.now()
                    difference = exit_time - bike["entry_time"]
                    hrs = int(difference.total_seconds() / 3600) + 1
                    charges = 20 * hrs
                    print("Charges: ₹", charges)
                    db.dealloc_vehicle(number_plate, "bike", exit_time)
                    is_found = True
                    break
                    
        if not is_found:
            print("Vehicle not found or not currently parked.")

    while True:
        print("\nMENU: 1.ToPark 2.ToExit 3.PrintParkedCars 4.PrintParkedBikes 5.PrintAllParkingRecords 6.FilterPrintAllParkingRecords 7.AdminPanel 8.ChangeAdmin 9.Exit")
        try:
            choice_input = input("Enter your choice: ").strip()
            if not choice_input:
                continue
            n = int(choice_input)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
            
        if n == 1:
            vehicle_type = input("Enter type (car/bike): ").strip().lower()
            while vehicle_type not in ["car", "bike"]:
                print("Invalid vehicle type. Enter 'car' or 'bike'.")
                vehicle_type = input("Enter type (car/bike): ").strip().lower()
            alloc_parking(vehicle_type)
            
        elif n == 2:
            number_plate = input("Enter number plate: ").strip()
            de_alloc_parking(number_plate)
            
        elif n == 3:
            cars = db.parked_cars_list()
            if not cars:
                print("Zero Cars Parked")
            else:
                for car in cars:
                    for key, value in car.items():
                         print(f"{key}: {value}")
                    print("-" * 50)
                    
        elif n == 4:
            bikes = db.parked_bikes_list()
            if not bikes:
                print("Zero Bikes Parked")
            else:
                for bike in bikes:
                    for key, value in bike.items():
                        print(f"{key}: {value}")
                    print("-" * 50)
        
        elif n == 5:
            vehicles = db.get_all_parked_vehicles_details()
            if not vehicles:
                print("No vehicles recorded in history.")
            else:
                for vehicle in vehicles:
                    for key, value in vehicle.items():
                        print(f"{key}: {value}")
                    print("-" * 50)
                    
        elif n == 6:  
            try:
                entry_date = validate_date_input("Enter entry date (YYYY-MM-DD): ")
                exit_date = validate_date_input("Enter exit date (YYYY-MM-DD): ")

                if exit_date < entry_date:
                    raise ValueError("Exit date cannot be earlier than entry date.")

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

        elif n == 7:
            username = input("Enter admin's username: ").strip()
            password = input("Enter admin's password: ").strip()
            admins = db.get_admins()
            is_authenticated = False
            for admin in admins:
                if admin["username"] == username and db.verify_password(password, admin["password"]):
                    is_authenticated = True
                    break
            
            if is_authenticated:
                def compute(start_date, end_date):
                    vehicles = db.get_filter_parked_vehicles_details(
                        start_date.strftime("%Y-%m-%d"),
                        end_date.strftime("%Y-%m-%d")
                    )
                    num_cars = 0
                    num_bikes = 0
                    if vehicles:
                        for vehicle in vehicles:
                            if vehicle["type"] == "car" and vehicle["isParked"] == 0:
                                num_cars += 1
                            elif vehicle["type"] == "bike" and vehicle["isParked"] == 0:
                                num_bikes += 1
                    print("Revenue through cars: ₹", 40 * num_cars)
                    print("Revenue through bikes: ₹", 20 * num_bikes)
                    print("Total Revenue: ₹", 40 * num_cars + 20 * num_bikes)
                    
                while True:
                    print("\nADMIN PANEL: 1.Annual Revenue 2.Monthly Revenue 3.Current Month Revenue 4.Custom Revenue 5.Exit")
                    try:
                        choice_input = input("Enter your choice: ").strip()
                        if not choice_input:
                            continue
                        choice = int(choice_input)
                    except ValueError:
                        print("Invalid choice. Enter a number between 1 and 5.")
                        continue
                        
                    if choice == 1:
                         current_year = datetime.now().year
                         start_date = datetime(current_year, 1, 1)
                         end_date = datetime(current_year, 12, 31)
                         print(f"\n--- Annual Revenue ({current_year}) ---")
                         compute(start_date, end_date)
                    elif choice == 2:
                         current_year = datetime.now().year
                         print(f"\n--- Monthly Revenue Breakdown ({current_year}) ---")
                         for m in range(1, 13):
                             month_name = calendar.month_name[m]
                             start_date = datetime(current_year, m, 1)
                             last_day = calendar.monthrange(current_year, m)[1]
                             end_date = datetime(current_year, m, last_day)
                             print(f"\n* {month_name} {current_year}:")
                             compute(start_date, end_date)
                    elif choice == 3:    
                         current_time = datetime.now()
                         start_date = datetime(current_time.year, current_time.month, 1)
                         last_day = calendar.monthrange(current_time.year, current_time.month)[1]
                         end_date = datetime(current_time.year, current_time.month, last_day)
                         print(f"\n--- Current Month Revenue ({calendar.month_name[current_time.month]} {current_time.year}) ---")
                         compute(start_date, end_date)
                    elif choice == 4:
                         try:
                             start_date = validate_date_input("Enter start date (YYYY-MM-DD): ")
                             end_date = validate_date_input("Enter end date (YYYY-MM-DD): ")
                             if end_date < start_date:
                                 raise ValueError("End date cannot be earlier than start date.")
                             print(f"\n--- Custom Revenue ({start_date} to {end_date}) ---")
                             compute(start_date, end_date)
                         except ValueError as e:
                             print(f"Input Error: {e}")
                    else:
                         print("Exiting Admin Panel...")
                         break
            else:
                print("Incorrect username or password.")

        elif n == 8:
            username = input("Enter admin's username: ").strip()
            password = input("Enter admin's password: ").strip()          
            admins = db.get_admins()
            is_authenticated = False
            for admin in admins:
                if admin["username"] == username and db.verify_password(password, admin["password"]):
                    is_authenticated = True
                    break
            
            if is_authenticated:
                new_username = input("Enter new username: ").strip()
                new_password = input("Enter new password: ").strip()
                if not new_username or not new_password:
                    print("Username and password cannot be empty.")
                else:
                    new_password_hash = db.hash_password(new_password)
                    db.update_admin(new_username, new_password_hash)
                    print("Admin credentials updated successfully.")
            else:
                print("Incorrect password or username...")
        else:
            print("Exiting...")
            break


