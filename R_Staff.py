import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_staff_record(used_ids):
    while True:
        random_staff_id = random.randint(1, 1000)
        if random_staff_id not in used_ids:
            break
    used_ids.add(random_staff_id)
    random_address = fake.address()
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_email = fake.email()
    random_phone_number = "+92 " + fake.random_element(("300", "301", "302", "303", "304", "305", "306", "307", "308", "309")) + " " + str(fake.random_number(digits=7))
    return {"S_ID": random_staff_id, "S_Address": random_address,
            "S_FirstName": random_first_name, "S_LastName": random_last_name,
            "S_Email": random_email, "S_PhoneNo": random_phone_number}

# Generate 30 login records
used_ids = set()
staff_records = [generate_staff_record(used_ids) for _ in range(30)]

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

# Create staff table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Staff')
               CREATE TABLE Staff
               (S_ID INT PRIMARY KEY,
                S_Address VARCHAR(255),
                S_FirstName VARCHAR(100),
                S_LastName VARCHAR(100),
                S_Email VARCHAR(255) UNIQUE,
                S_PhoneNo VARCHAR(20) UNIQUE)
                ''')

for record in staff_records:
    cursor.execute('''
                   INSERT INTO Staff (S_ID, S_Address, S_FirstName, S_LastName, S_Email, S_PhoneNo)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record["S_ID"], record["S_Address"], record["S_FirstName"], record["S_LastName"], record["S_Email"], record["S_PhoneNo"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
