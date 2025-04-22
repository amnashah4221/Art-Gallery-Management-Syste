import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_artwork_record(used_ids, artist_ids):
    while True:
        random_artwork_id = random.randint(1, 1000)
        if random_artwork_id not in used_ids:
            break
    used_ids.add(random_artwork_id)
    random_artist_id = random.choice(artist_ids)
    title = fake.sentence(nb_words=3)
    medium = fake.word()
    dimensions = fake.word()
    date_completed = fake.date_between(start_date='-5y', end_date='today')
    price = round(random.uniform(100, 10000), 2)
    availability = fake.random_element(["Available", "Sold"])
    return {"Art_ID": random_artwork_id, "A_ID": random_artist_id,
            "Title": title, "Medium": medium, "Dimensions": dimensions,
            "DateCompleted": date_completed, "Price": price, "Availability": availability}


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

# Fetch existing artist IDs from the Artist table
cursor.execute("SELECT A_ID FROM Artist")
artist_ids = [row.A_ID for row in cursor.fetchall()]

# Generate 30 artwork records
used_ids = set()
artwork_records = [generate_artwork_record(used_ids, artist_ids) for _ in range(30)]

# Create artwork table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Artwork')
               CREATE TABLE Artwork
               (Art_ID INT PRIMARY KEY,
                A_ID INT,
                Title VARCHAR(255),
                Medium VARCHAR(100),
                Dimensions VARCHAR(100),
                DateCompleted DATE,
                Price DECIMAL(10, 2),
                Availability VARCHAR(20),
                FOREIGN KEY (A_ID) REFERENCES Artist(A_ID))
                ''')

for record in artwork_records:
    cursor.execute('''
                   INSERT INTO Artwork (Art_ID, A_ID, Title, Medium, Dimensions, DateCompleted, Price, Availability)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record["Art_ID"], record["A_ID"], record["Title"], record["Medium"],
                   record["Dimensions"], record["DateCompleted"], record["Price"], record["Availability"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
