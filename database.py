import sqlite3
import csv

# Define the path for the new SQLite database
db_path = 'normalized_database.db'

# Create a new database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: Define the schema for a normalized database (3NF)
# Customer Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner TEXT,
    Dependents TEXT
)
''')

# Contract Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Contract (
    contractID INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    tenure INTEGER,
    ContractType TEXT,
    PaperlessBilling TEXT,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges REAL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
)
''')

# Services Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Services (
    serviceID INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    PhoneService TEXT,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
)
''')

# Churn Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Churn (
    churnID INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    Churn TEXT,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
)
''')

# Step 2: Read the CSV file and populate the tables
csv_file_path = 'expanded_dataset.csv'  # Path to the CSV file
with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Insert data into Customer table
        cursor.execute('''
        INSERT OR IGNORE INTO Customer (customerID, gender, SeniorCitizen, Partner, Dependents)
        VALUES (?, ?, ?, ?, ?)
        ''', (row['customerID'], row['gender'], row['SeniorCitizen'], row['Partner'], row['Dependents']))

        # Insert data into Contract table
        cursor.execute('''
        INSERT INTO Contract (customerID, tenure, ContractType, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['customerID'], row['tenure'], row['Contract'], row['PaperlessBilling'],
              row['PaymentMethod'], row['MonthlyCharges'], row['TotalCharges']))

        # Insert data into Services table
        cursor.execute('''
        INSERT INTO Services (customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, 
        OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['customerID'], row['PhoneService'], row['MultipleLines'], row['InternetService'],
              row['OnlineSecurity'], row['OnlineBackup'], row['DeviceProtection'], row['TechSupport'],
              row['StreamingTV'], row['StreamingMovies']))

        # Insert data into Churn table
        cursor.execute('''
        INSERT INTO Churn (customerID, Churn)
        VALUES (?, ?)
        ''', (row['customerID'], row['Churn']))

# Commit the transactions and close the connection
conn.commit()
conn.close()

print(f"Database has been created and saved as '{db_path}'")
