import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_gallery_record(used_ids):
    while True:
        random_gallery_id = random.randint(1, 1000)
        if random_gallery_id not in used_ids:
            break
    used_ids.add(random_gallery_id)
    gallery_name = fake.company()
    status = fake.random_element(["Active", "Inactive"])
    location = fake.address()
    return {"G_ID": random_gallery_id, "GalleryName": gallery_name,
            "Status": status, "Location": location}

used_ids = set()
gallery_records = [generate_gallery_record(used_ids) for _ in range(30)]

for record in gallery_records:
    print(record)  # Check if the records are generated correctly

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

# Create Gallery table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Gallery')
               CREATE TABLE Gallery
               (G_ID INT PRIMARY KEY,
                GalleryName VARCHAR(255),
                Status VARCHAR(50),
                Location VARCHAR(255))
                ''')

for record in gallery_records:
    cursor.execute('''
                   INSERT INTO Gallery (G_ID, GalleryName, Status, Location)
                   VALUES (?, ?, ?, ?)
                   ''',
                   record["G_ID"], record["GalleryName"], record["Status"], record["Location"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
