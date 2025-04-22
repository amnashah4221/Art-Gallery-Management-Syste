import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_artist_record(used_ids):
    while True:
        random_artist_id = random.randint(1, 1000)
        if random_artist_id not in used_ids:
            break
    used_ids.add(random_artist_id)
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_email = fake.email()
    random_phone_number = "+92 " + fake.random_element(("300", "301", "302", "303", "304", "305", "306", "307", "308", "309")) + " " + str(fake.random_number(digits=7))
    random_address = fake.address()
    random_social_media_profile = fake.uri()
    random_signature_style = fake.word()
    return {"A_ID": random_artist_id, "A_FirstName": random_first_name,
            "A_LastName": random_last_name, "A_Email": random_email,
            "A_PhoneNo": random_phone_number, "A_Address": random_address,
            "SocialMediaProfile": random_social_media_profile,
            "SignatureStyle": random_signature_style}

# Generate 30 artist records
used_ids = set()
artist_records = [generate_artist_record(used_ids) for _ in range(30)]

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

# Create artist table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Artist')
               CREATE TABLE Artist
               (A_ID INT PRIMARY KEY,
                A_FirstName VARCHAR(100),
                A_LastName VARCHAR(100),
                A_PhoneNo VARCHAR(20),
                A_Email VARCHAR(255) UNIQUE,
                A_Address VARCHAR(255),
                SocialMediaProfile VARCHAR(255),
                SignatureStyle VARCHAR(255))
                ''')

for record in artist_records:
    cursor.execute('''
                   INSERT INTO Artist (A_ID, A_FirstName, A_LastName, A_PhoneNo, A_Email, A_Address, SocialMediaProfile, SignatureStyle)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record["A_ID"], record["A_FirstName"], record["A_LastName"], record["A_PhoneNo"],
                   record["A_Email"], record["A_Address"], record["SocialMediaProfile"], record["SignatureStyle"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
