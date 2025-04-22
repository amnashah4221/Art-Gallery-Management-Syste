import pyodbc as odbc

# Define lists for Admin attributes
admin_ids = [101, 202]
addresses = ["Muslim Town, Karachi", "Gulshan-e-Iqbal, Lahore"]
first_names = ["Iqra", "Aisha"]
last_names = ["Ahmed", "Khan"]
emails = ["iqra.ahmed@example.com", "aisha.khan@example.com"]
phone_numbers = ["92 333 2987301", "92 334 2987302"]

# Database connection details
SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
DATABASE_NAME = 'xyz'

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

# Create Admin table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Admin')
               CREATE TABLE Admin
               (
                   Admin_ID INT PRIMARY KEY,
                   Login_ID INT,
                   Ad_Address VARCHAR(255),
                   Ad_FirstName VARCHAR(100),
                   Ad_LastName VARCHAR(100),
                   Ad_Email VARCHAR(255) UNIQUE,
                   Ad_PhoneNo VARCHAR(20) UNIQUE,
                   FOREIGN KEY (Login_ID) REFERENCES Login(Login_ID)
               )
               ''')

cursor.execute('SELECT Login_ID FROM Login')
login_ids = [row[0] for row in cursor.fetchall()]

# Create a list of records to insert
admin_records = list(zip(admin_ids, login_ids, addresses, first_names, last_names, emails, phone_numbers))

# Insert records into the Admin table
for record in admin_records:
    cursor.execute('''
                   INSERT INTO Admin (Admin_ID, Login_ID, Ad_Address, Ad_FirstName, Ad_LastName, Ad_Email, Ad_PhoneNo)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], record[2], record[3], record[4], record[5], record[6])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
