
import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_login_record(used_ids):
    while True:
        random_login_id = random.randint(1, 1000)
        if random_login_id not in used_ids:
            break
    used_ids.add(random_login_id)
    random_email = fake.email()
    random_username = fake.user_name()
    return {"Login_ID": random_login_id, "Email": random_email, "Username": random_username}

# Generate 30 login records
used_ids = set()
login_records = [generate_login_record(used_ids) for _ in range(30)]

# Database connection details
SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
DATABASE_NAME = 'Business'

# Connection string
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    r'Trusted_Connection=yes;'
)

# Establish connection
conn = odbc.connect(conn_str)
cursor = conn.cursor()

# Create Login table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Login')
               CREATE TABLE Login
               (Login_ID INT PRIMARY KEY,
               Email VARCHAR(255) UNIQUE,
               Username VARCHAR(100))
               ''')

# Insert records into the Login table
for record in login_records:
    cursor.execute('''
                   INSERT INTO Login (Login_ID, Email, Username)
                   VALUES (?, ?, ?)
                   ''',
                   record["Login_ID"], record["Email"], record["Username"])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
