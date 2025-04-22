import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_client_record(used_ids):
    while True:
        random_client_id = random.randint(1, 1000)
        if random_client_id not in used_ids:
            break
    used_ids.add(random_client_id)
    random_address = fake.address()
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_email = fake.email()
    random_phone_number = "+92 " + fake.random_element(("300", "301", "302", "303", "304", "305", "306", "307", "308", "309")) + " " + str(fake.random_number(digits=7))
    return {"C_ID": random_client_id, "C_Address": random_address,
            "C_FirstName": random_first_name, "C_LastName": random_last_name,
            "C_Email": random_email, "C_PhoneNo": random_phone_number}

# Generate 30 client records
used_ids = set()
client_records = [generate_client_record(used_ids) for _ in range(30)]

SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
DATABASE_NAME = 'Business'

# Define connection string
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    r'Trusted_Connection=yes;'
)

conn = odbc.connect(conn_str)
cursor = conn.cursor()

# Create client table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Client')
               CREATE TABLE Client
               (C_ID INT PRIMARY KEY,
                C_Email VARCHAR(255) UNIQUE,
                C_FirstName VARCHAR(100),
                C_LastName VARCHAR(100),
                C_PhoneNo VARCHAR(20) UNIQUE,
                C_Address VARCHAR(255))
                ''')

for record in client_records:
    cursor.execute('''
                   INSERT INTO Client (C_ID, C_Email, C_FirstName, C_LastName, C_PhoneNo, C_Address)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record["C_ID"], record["C_Email"], record["C_FirstName"], record["C_LastName"], record["C_PhoneNo"], record["C_Address"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
