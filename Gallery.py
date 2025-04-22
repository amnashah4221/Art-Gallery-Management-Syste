import random
import pyodbc as odbc

# Define lists for Gallery attributes
g_ids = list(range(1, 101))
gallery_names = [
    "Artful Ancestry", "Skarstedt Fine Art", "Modern Masterpieces", "Creative Expressions",
    "Heritage Gallery", "Visionary Art"
]
statuses = ["Open", "Closed"]
locations = [
    "Block C, Cornellia St.", "Avenue 5, Blueberry Hill", "Sector 10, Riverside", "Lot 23, Maple Street"
]

# Database connection details
SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
DATABASE_NAME = 'ArtGalleryManagementSystem'

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

# Create Gallery table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Gallery')
               CREATE TABLE Gallery
               (
                   GID INT PRIMARY KEY,
                   UserID INT,
                   GalleryName VARCHAR(255),
                   Status VARCHAR(50),
                   Location VARCHAR(255),
                   FOREIGN KEY (UserID) REFERENCES Users(UserID)
               )
               ''')

# Fetch UserID values from Users table where the role is 'admin'
cursor.execute('SELECT UserID FROM Users WHERE Role = \'admin\'')
admin_user_ids = [row[0] for row in cursor.fetchall()]

if len(admin_user_ids) < 2:
    raise ValueError("Not enough admin users to assign to galleries")

# Randomly select 2 admin UserID values
selected_user_ids = random.sample(admin_user_ids, 2)

# Randomly select 2 values from the customized lists
selected_gallery_names = random.sample(gallery_names, 2)
selected_statuses = random.sample(statuses, 2)
selected_locations = random.sample(locations, 2)

# Generate records by cycling through the selected values
gallery_records = list(zip(
    random.sample(g_ids, 5),
    [selected_user_ids[i % 2] for i in range(5)],
    [selected_gallery_names[i % 2] for i in range(5)],
    [selected_statuses[i % 2] for i in range(5)],
    [selected_locations[i % 2] for i in range(5)]
))

# Insert records into the Gallery table
for record in gallery_records:
    cursor.execute('''
                   INSERT INTO Gallery (GID, UserID, GalleryName, Status, Location)
                   VALUES (?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], record[2], record[3], record[4])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
