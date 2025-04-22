import random
import pyodbc as odbc
from faker import Faker

fake = Faker()

def generate_loan_record(used_ids, artwork_ids):
    while True:
        random_loan_id = random.randint(1, 1000)
        if random_loan_id not in used_ids:
            break
    used_ids.add(random_loan_id)
    random_artwork_id = random.choice(artwork_ids)
    loan_agreement = fake.sentence(nb_words=4)
    duration = random.randint(1, 12)  # Assuming loan duration is between 1 to 12 months
    expiry_date = fake.date_between(start_date='+1M', end_date='+2y')
    transport_tracking = fake.word()
    monitoring_status = fake.random_element(["On track", "Delayed", "Completed"])
    return {"Loan_ID": random_loan_id, "Art_ID": random_artwork_id,
            "LoanAgreement": loan_agreement, "Duration": duration,
            "ExpiryDate": expiry_date, "TransportTracking": transport_tracking,
            "MonitoringStatus": monitoring_status}

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

# Generate 30 loan records
used_ids = set()
loan_records = [generate_loan_record(used_ids, artwork_ids) for _ in range(30)]

# Create Loan table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Loan')
               CREATE TABLE Loan (
                   Loan_ID INT PRIMARY KEY,
                   Art_ID INT,
                   LoanAgreement VARCHAR(255),
                   Duration INT,
                   ExpiryDate DATE,
                   TransportTracking VARCHAR(100),
                   MonitoringStatus VARCHAR(50),
                   FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID)
               )
               ''')

for record in loan_records:
    cursor.execute('''
                   INSERT INTO Loan (Loan_ID, Art_ID, LoanAgreement, Duration, ExpiryDate, TransportTracking, MonitoringStatus)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record["Loan_ID"], record["Art_ID"], record["LoanAgreement"], record["Duration"],
                   record["ExpiryDate"], record["TransportTracking"], record["MonitoringStatus"])
    print("Inserted Successfully")

conn.commit()

cursor.close()
conn.close()
