import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_sales_record(used_ids, artwork_ids, client_ids):
    while True:
        random_sale_id = random.randint(1, 1000)
        if random_sale_id not in used_ids:
            break
    used_ids.add(random_sale_id)
    random_artwork_id = random.choice(artwork_ids)
    random_client_id = random.choice(client_ids)
    sale_price = round(random.uniform(100, 10000), 2)
    sale_date = fake.date_between(start_date='-1y', end_date='today')
    artist_commission = round(sale_price * 0.1, 2)  # Assuming artist commission is 10%
    return {"Sale_ID": random_sale_id, "Art_ID": random_artwork_id,
            "C_ID": random_client_id, "SalePrice": sale_price,
            "SaleDate": sale_date, "ArtistCommission": artist_commission}

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

# Fetch existing client IDs from the Client table
cursor.execute("SELECT C_ID FROM Client")
client_ids = [row.C_ID for row in cursor.fetchall()]

# Generate 30 sales records
used_ids = set()
sales_records = [generate_sales_record(used_ids, artwork_ids, client_ids) for _ in range(30)]

# Create Sales table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Sales')
               CREATE TABLE Sales (
                   Sale_ID INT PRIMARY KEY,
                   Art_ID INT,
                   C_ID INT,
                   SalePrice DECIMAL(10, 2),
                   SaleDate DATE,
                   ArtistCommission DECIMAL(10, 2),
                   FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID),
                   FOREIGN KEY (C_ID) REFERENCES Client(C_ID)
               )
               ''')

for record in sales_records:
    cursor.execute('''
                   INSERT INTO Sales (Sale_ID, Art_ID, C_ID, SalePrice, SaleDate, ArtistCommission)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record["Sale_ID"], record["Art_ID"], record["C_ID"], record["SalePrice"],
                   record["SaleDate"], record["ArtistCommission"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
