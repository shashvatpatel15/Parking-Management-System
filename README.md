# Parking Management System

A comprehensive Command-Line Interface (CLI) application for managing vehicle parking, calculating revenues, and maintaining structured records. The system provides role-based functionality with dedicated features for parking operators and administrative oversight.

## Features

### Core Parking Operations
- **Allocate Parking**: Park cars and bikes if capacity allows (e.g., maximum 50 cars, 50 bikes). Prevents duplicate entry of the same vehicle.
- **De-allocate Parking**: Automatically calculates parking duration and corresponding charges upon exit (₹40/hr for cars, ₹20/hr for bikes).
- **In-Memory Tracking**: Keep an updated catalog of vehicles currently parked, tracking their initial entry time.

### Analytics and Reporting
- **List Current Vehicles**: Display real-time lists of currently parked cars and bikes.
- **View All Records**: Fetch and display historical records of all parking activities.
- **Filter Records**: Filter parking activities by specific entry and exit dates.

### Secure Admin Panel
- **Authentication**: Password-protected access using industry-standard `bcrypt` hashing.
- **Revenue Calculation**: Compute generated revenue over flexible timeframes:
  - Annual Revenue
  - Monthly Revenue
  - Current Month Revenue
  - Custom Date Range Revenue
- **Credential Management**: Admins have the ability to securely change to a new username and password.

## Tech Stack
- **Language**: Python 3
- **Database**: MySQL (via SQLAlchemy & PyMySQL)
- **Security**: bcrypt (Password Hashing)
- **Environment Management**: python-dotenv for secure credentials.

## Setup Instructions

### Prerequisites
1. Ensure **Python 3.x** is installed on your system.
2. Install and run **MySQL Server**.
3. Create a blank database in your MySQL server to be used by the application.

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Parking-Management-System-main
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure your requirements include `SQLAlchemy`, `PyMySQL`, `bcrypt`, and `python-dotenv`.)*

4. **Environment Setup:**
   Create a `.env` file in the root directory (alongside `main.py`) and carefully add your configuration:
   ```env
   # Database Configuration
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=your_parking_db_name

   # Default Administrative Account (used for first-time initialization)
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_password
   ```

5. **Run the Application:**
   ```bash
   python main.py
   ```

## First Time Configuration

The very first time you run `python main.py`, the system will automatically create the necessary database tables (`vehicles_parked` and `admin`). 

It will also initialize the administrative account using the credentials provided in your `.env` file (`ADMIN_USERNAME` and `ADMIN_PASSWORD`):
- **Default Username:** `spatel` (or whatever you set in `.env`)
- **Default Password:** `Shashvat@123` (or whatever you set in `.env`)

*Note: It is highly recommended to log into the Admin panel (Option 7) and modify these credentials (Option 8) during initial setup.*

## Menu Usage Options

When you run the application, you'll be presented with the following options:

1. **ToPark**: Park a bike or car. Provide type and number plate.
2. **ToExit**: Provide the number plate of an exiting vehicle to calculate total hours and bill.
3. **PrintParkedCars**: Prints all currently parked cars.
4. **PrintParkedBikes**: Prints all currently parked bikes.
5. **PrintAllParkingRecords**: Prints a complete overall list of everything parked or exited historically.
6. **FilterPrintAllParkingRecords**: Filter historic parking by customized entry and exit time.
7. **AdminPanel**: Specialized analytics for an authenticated administrator (e.g., revenue calculation).
8. **ChangeAdmin**: Used by existing admins to securely modify login credentials.
9. **Exit**: Terminate the application.
