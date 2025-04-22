import random
import pyodbc as odbc

# Define customized lists for Artist attributes

social_media_profiles = [
    "@theartones", "@creativebrush", "@artbyali", "@masterpieces", "@urbanartist", "@canvascreations",
    "@abstractvisions", "@portraitpioneer", "@modernmuse", "@classiccreations", "@studioexpressions",
    "@dynamicdesigns", "@visualvoyager", "@artisthub", "@creativecorner", "@artisticadventures",
    "@inspiredillustrations", "@timelessart", "@artisticjourney", "@fineartfocus", "@artsyvibes",
    "@colorfulcreations", "@artfusion", "@avantgardeartist", "@modernartmovement", "@artisticendeavors",
    "@vibrantvisions", "@expressiveart", "@urbanexpressions", "@creativecanvas", "@artisticflair",
    "@soulfulsketches", "@artisticimpressions", "@uniqueartistry", "@visualmastery", "@artfulconcepts",
    "@boldbrushstrokes", "@artisticnarratives", "@artisticfusion", "@modernartist", "@artgal"
    "@modernartist", "@inspiredcreations", "@abstractexpressions", "@creativevisions", "@colorfulcreations",
    "@urbanartistry", "@timelesscreations", "@modernmasterpieces", "@dynamicart", "@classiccreations",
    "@studioexpressions", "@fineartfocus", "@artisthub", "@artisticadventures", "@artisticjourney",
    "@artisticnarratives", "@creativecanvas", "@visualvoyager", "@artisticflair", "@uniqueartistry"
]

signature_styles = [
    "impressionist", "classical", "abstract", "realism", "cubism", "surrealism", "expressionism", "pop art",
    "minimalism", "modernism", "post-impressionism", "art nouveau", "baroque", "rococo", "fauvism", "dada",
    "constructivism", "futurism", "conceptual art", "contemporary", "graffiti", "street art", "photorealism",
    "neo-expressionism", "hyperrealism", "symbolism", "mannerism", "romanticism", "abstract expressionism",
    "art deco", "renaissance", "op art", "kinetic art", "outsider art", "naïve art", "land art", "installation art",
    "performance art", "digital art", "video art", "sound art", "interactive art", "cyber art", "media art",
    "process art", "happenings", "fluxus", "assemblage", "readymade", "collage", "mixed media", "arte povera",
    "brutalism", "lowbrow", "psychedelic art", "urban art", "post-modernism", "neo-dada"
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

# Create Artist table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Artist')
               CREATE TABLE Artist
               (AID INT PRIMARY KEY,
                UserID INT,
                SocialMediaProfile VARCHAR(255),
                SignatureStyle VARCHAR(255),
                FOREIGN KEY (UserID) REFERENCES Users(UserID))
               ''')

# Retrieve UserIDs where Role is 'Artist'
cursor.execute('SELECT UserID FROM Users WHERE Role = ?', 'Artist')
artist_user_ids = [row[0] for row in cursor.fetchall()]

# Randomly select attributes for artists
num_artists = min(len(artist_user_ids), 30)  # Ensure we don't exceed the number of user IDs
selected_user_ids = random.sample(artist_user_ids, num_artists)

artist_records = []
for user_id in selected_user_ids:
    artist_records.append((
        random.randint(101, 200),  # Random AID
        user_id,
        random.choice(social_media_profiles),
        random.choice(signature_styles)
    ))

# Insert records into the Artist table
for record in artist_records:
    cursor.execute('''
                   INSERT INTO Artist (AID, UserID, SocialMediaProfile, SignatureStyle)
                   VALUES (?, ?, ?, ?)
                   ''', record)
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
