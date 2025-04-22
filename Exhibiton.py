import random
import pyodbc as odbc
from datetime import datetime

# Define lists for Exhibition attributes
e_ids = list(range(1, 101))
start_dates = [
     "2024-01-15", "2024-02-20", "2024-03-18", "2024-04-22", "2024-05-05", "2024-06-11", "2024-07-19",
    "2024-08-24", "2024-09-3", "2024-10-14", "2024-11-23", "2024-12-02"
]
end_dates = [
    "2024-01-17", "2024-02-22", "2024-03-19", "2024-04-24", "2024-05-06", "2024-06-12", "2024-07-20",
    "2024-08-28", "2024-09-4", "2024-10-15", "2024-11-25", "2024-12-03"
]
locations = [
    "Hyde Park, London", "Louvre, Paris", "Museum of Modern Art, New York", "Tate Modern, London",
    "The Met, New York", "Uffizi Gallery, Florence"
]
e_names = [
    "Solstice", "Artistry Showcase", "Creative Expression Expo", "Visual Delights Exhibition",
    "Palette Perfection Showcase", "Imagination Unleashed Expo", "Cultural Fusion Exhibition", "Canvas Creations Showcase", "Eclectic Artistry Expo",
    "Vibrant Visions Exhibition", "Artisanal Craftsmanship Showcase", "Gallery Galore Expo", "Modern Masterpieces Exhibition",
    "Abstract Adventures Showcase", "Surreal Splendor Expo", "Contemporary Perspectives Exhibition",
    "Artful Endeavors Showcase", "Fusion of Colors Expo", "Urban Artistry Exhibition", "Ephemeral Elegance Showcase",
    "Timeless Treasures Expo", "Harmony in Hues Exhibition", "Nature's Canvas Showcase", "Captivating Contrasts Expo",
    "Whimsical Wonders Exhibition", "Ethereal Essence Showcase", "Serene Symmetry Expo", "Dynamic Dimensions Exhibition",
    "Radiant Realms Showcase", "Enigmatic Expressions Expo", "Transcendent Textures Exhibition",
]
themes = [
    "Nature and Landscapes",
    "Portraits and Figures",
    "Abstract Expressionism",
    "Surrealism",
    "Still Life",
    "Urban Scenes",
    "Mythology and Folklore",
    "Fantasy and Science Fiction",
    "Impressionism",
    "Realism",
    "Wildlife and Animals",
    "Historical Events",
    "Religious and Spiritual",
    "Social and Political Commentary",
    "Romance and Love",
    "Dreams and Imagination",
    "Symbolism",
    "Contemporary Issues",
    "Pop Culture",
    "Environmental Conservation",
    "Cultural Diversity",
    "Technological Advancement",
    "Human Emotions and Psychology",
    "Architectural Wonders",
    "Celestial Bodies and Space Exploration",
    "Mysticism and Esotericism",
    "Nostalgia and Memory",
    "Identity and Self-Discovery",
    "Abstract Concepts and Ideas",
    "Seasons and Weather"
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

# Create Exhibition table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Exhibition')
               CREATE TABLE Exhibition
               (
                   EID INT PRIMARY KEY,
                   GID INT,
                   StartDate DATE,
                   EndDate DATE,
                   Location VARCHAR(255),
                   EName VARCHAR(255),
                   Theme VARCHAR(255),
                   ArtID INT,
                   FOREIGN KEY (ArtID) REFERENCES Artwork(ArtID),
                   FOREIGN KEY (GID) REFERENCES Gallery(GID)
               )
               ''')

# Fetch ArtID values from Artwork table where Availability is 'Available' or 'Not for Sale'
cursor.execute('SELECT ArtID FROM Artwork WHERE Availability IN (?, ?)', 'Available', 'Not for Sale')
art_ids = [row[0] for row in cursor.fetchall()]

# Fetch GID values from Gallery table
cursor.execute('SELECT GID FROM Gallery')
gallery_ids = [row[0] for row in cursor.fetchall()]

# Randomly select 30 values from the customized lists
exhibition_records = list(zip(
    random.sample(e_ids, 30),
    random.choices(gallery_ids, k=30),
    random.choices(start_dates, k=30),
    random.choices(end_dates, k=30),
    random.choices(locations, k=30),
    random.choices(e_names, k=30),
    random.choices(themes, k=30),
    random.choices(art_ids, k=30)
))

# Insert records into the Exhibition table
for record in exhibition_records:
    cursor.execute('''
                   INSERT INTO Exhibition (EID, GID, StartDate, EndDate, Location, EName, Theme, ArtID)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
