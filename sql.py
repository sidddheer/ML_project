import sqlite3
import pandas as pd

# Path to the normalized database
db_path = 'normalized_database.db'  # Replace with your database path

# Connect to the database
conn = sqlite3.connect(db_path)

# SQL query to join tables and fetch data
query = """
SELECT 
    c.customerID,
    c.gender,
    c.SeniorCitizen,
    c.Partner,
    c.Dependents,
    cn.tenure,
    cn.ContractType,
    cn.PaperlessBilling,
    cn.PaymentMethod,
    cn.MonthlyCharges,
    cn.TotalCharges,
    s.PhoneService,
    s.MultipleLines,
    s.InternetService,
    s.OnlineSecurity,
    s.OnlineBackup,
    s.DeviceProtection,
    s.TechSupport,
    s.StreamingTV,
    s.StreamingMovies,
    ch.Churn
FROM Customer c
LEFT JOIN Contract cn ON c.customerID = cn.customerID
LEFT JOIN Services s ON c.customerID = s.customerID
LEFT JOIN Churn ch ON c.customerID = ch.customerID
"""

# Execute the query and load the result into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the first few rows of the DataFrame
print(df.head())
