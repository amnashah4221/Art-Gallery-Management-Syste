import random
import pyodbc as odbc

# Database connection details
SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
DATABASE_NAME = 'ArtGalleryDatabaseManagementSystem'

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

# Create Sales table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Sales')
               CREATE TABLE Sales
               (
                   SaleID INT,
                   UserID INT, 
                   ArtID INT,
                   Price DECIMAL(10, 2),
                   SaleDate DATE,
                   ArtistCommission DECIMAL(10, 2),
                   CONSTRAINT PKSALES PRIMARY KEY (SaleID),
                   CONSTRAINT FKSALESUSER FOREIGN KEY (UserID) REFERENCES Users(UserID),
                   CONSTRAINT FKSALESART FOREIGN KEY (ArtID) REFERENCES Artwork(ArtID),
                   CHECK (Price > 0)
               )
               ''')

# Fetch ArtID values and their corresponding prices from Artwork table for artworks that are available
cursor.execute('SELECT ArtID, Price FROM Artwork WHERE Availability = \'Available\'')
artworks = cursor.fetchall()
art_ids = [row[0] for row in artworks]
art_prices = {row[0]: row[1] for row in artworks}

# Fetch UserID values from Users table where the role is 'client'
cursor.execute('SELECT UserID FROM Users WHERE Role = \'client\'')
user_ids = [row[0] for row in cursor.fetchall()]

# Define lists for Sales attributes
sale_ids = list(range(1, 121))
sale_dates = [
    "2022-01-15", "2022-02-20", "2022-03-18", "2022-04-22", "2022-05-05", "2022-06-11", "2022-07-19",
    "2022-08-24", "2022-09-30", "2022-10-14", "2022-11-23", "2022-12-02", "2023-01-15", "2023-02-20",
    "2023-03-18", "2023-04-22", "2023-05-05", "2023-06-11", "2023-07-19", "2023-08-24", "2023-09-30",
    "2023-10-14", "2023-11-23", "2023-12-02", "2024-01-15", "2024-02-20", "2024-03-18", "2024-04-22",
    "2024-05-05", "2024-06-11"
]
artist_commissions = [
    1500, 2500, 350, 4500, 5500, 65000, 7500, 8500, 95000, 10500,
    11500, 12500, 13500, 14500, 1550, 16500, 17500, 18500, 19500, 20500,
    21500, 22500, 23500, 24500, 25500, 26500, 27500, 28500, 29500, 30500,
    31500, 32500, 33500, 34500, 35500, 36500, 37500, 38500, 39500, 40500,
    41500, 42500, 43500, 44500, 45500, 46500, 47500, 48500, 49500, 50000
]

# Randomly select 120 values from the customized lists
sales_records = list(zip(
    random.sample(sale_ids, 120),
    random.choices(user_ids, k=120),
    random.choices(art_ids, k=120),
    random.choices(sale_dates, k=120),
    random.choices(artist_commissions, k=120)
))

# Insert records into the Sales table
for record in sales_records:
    art_id = record[2]
    price = art_prices[art_id]  # Use the price from the Artwork table
    cursor.execute('''
                   INSERT INTO Sales (SaleID, UserID, ArtID, Price, SaleDate, ArtistCommission)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], art_id, price, record[3], record[4])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
