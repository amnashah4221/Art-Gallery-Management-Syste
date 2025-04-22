import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_exhibition_record(used_ids, artwork_ids):
    while True:
        random_exhibition_id = random.randint(1, 1000)
        if random_exhibition_id not in used_ids:
            break
    used_ids.add(random_exhibition_id)
    start_date = fake.date_between(start_date='-5y', end_date='today')
    end_date = fake.date_between(start_date=start_date, end_date='+1y')
    location = fake.address()
    e_name = fake.company()
    theme = fake.sentence(nb_words=3)
    random_artwork_id = random.choice(artwork_ids)
    return {"E_ID": random_exhibition_id, "StartDate": start_date, "EndDate": end_date,
            "Location": location, "E_Name": e_name, "Theme": theme, "Art_ID": random_artwork_id}

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

# Fetch existing artwork IDs from the Artwork table
cursor.execute("SELECT Art_ID FROM Artwork")
artwork_ids = [row.Art_ID for row in cursor.fetchall()]

# Generate 30 exhibition records
used_ids = set()
exhibition_records = [generate_exhibition_record(used_ids, artwork_ids) for _ in range(30)]

# Create exhibition table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Exhibition')
               CREATE TABLE Exhibition
               (E_ID INT PRIMARY KEY,
                StartDate DATE,
                EndDate DATE,
                Location VARCHAR(255),
                E_Name VARCHAR(255),
                Theme VARCHAR(255),
                Art_ID INT,
                FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID))
                ''')

for record in exhibition_records:
    cursor.execute('''
                   INSERT INTO Exhibition (E_ID, StartDate, EndDate, Location, E_Name, Theme, Art_ID)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record["E_ID"], record["StartDate"], record["EndDate"], record["Location"],
                   record["E_Name"], record["Theme"], record["Art_ID"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
