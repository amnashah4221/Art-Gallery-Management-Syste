import random
import pyodbc as odbc

# Define customized list of Login IDs, emails, and usernames
login_ids = list(range(1, 101))  # 100 Login IDs from 1 to 100
emails = [
    "user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com", "user5@example.com",
    "user6@example.com", "user7@example.com", "user8@example.com", "user9@example.com", "user10@example.com",
    "user11@example.com", "user12@example.com", "user13@example.com", "user14@example.com", "user15@example.com",
    "user16@example.com", "user17@example.com", "user18@example.com", "user19@example.com", "user20@example.com",
    "user21@example.com", "user22@example.com", "user23@example.com", "user24@example.com", "user25@example.com",
    "user26@example.com", "user27@example.com", "user28@example.com", "user29@example.com", "user30@example.com",
    "user31@example.com", "user32@example.com", "user33@example.com", "user34@example.com", "user35@example.com",
    "user36@example.com", "user37@example.com", "user38@example.com", "user39@example.com", "user40@example.com",
    "user41@example.com", "user42@example.com", "user43@example.com", "user44@example.com", "user45@example.com",
    "user46@example.com", "user47@example.com", "user48@example.com", "user49@example.com", "user50@example.com",
    "user51@example.com", "user52@example.com", "user53@example.com", "user54@example.com", "user55@example.com",
    "user56@example.com", "user57@example.com", "user58@example.com", "user59@example.com", "user60@example.com",
    "user61@example.com", "user62@example.com", "user63@example.com", "user64@example.com", "user65@example.com",
    "user66@example.com", "user67@example.com", "user68@example.com", "user69@example.com", "user70@example.com",
    "user71@example.com", "user72@example.com", "user73@example.com", "user74@example.com", "user75@example.com",
    "user76@example.com", "user77@example.com", "user78@example.com", "user79@example.com", "user80@example.com",
    "user81@example.com", "user82@example.com", "user83@example.com", "user84@example.com", "user85@example.com",
    "user86@example.com", "user87@example.com", "user88@example.com", "user89@example.com", "user90@example.com",
    "user91@example.com", "user92@example.com", "user93@example.com", "user94@example.com", "user95@example.com",
    "user96@example.com", "user97@example.com", "user98@example.com", "user99@example.com", "user100@example.com"
]

# Manually define 100 unique usernames
usernames = [
    "user1", "user2", "user3", "user4", "user5",
    "user6", "user7", "user8", "user9", "user10",
    "user11", "user12", "user13", "user14", "user15",
    "user16", "user17", "user18", "user19", "user20",
    "user21", "user22", "user23", "user24", "user25",
    "user26", "user27", "user28", "user29", "user30",
    "user31", "user32", "user33", "user34", "user35",
    "user36", "user37", "user38", "user39", "user40",
    "user41", "user42", "user43", "user44", "user45",
    "user46", "user47", "user48", "user49", "user50",
    "user51", "user52", "user53", "user54", "user55",
    "user56", "user57", "user58", "user59", "user60",
    "user61", "user62", "user63", "user64", "user65",
    "user66", "user67", "user68", "user69", "user70",
    "user71", "user72", "user73", "user74", "user75",
    "user76", "user77", "user78", "user79", "user80",
    "user81", "user82", "user83", "user84", "user85",
    "user86", "user87", "user88", "user89", "user90",
    "user91", "user92", "user93", "user94", "user95",
    "user96", "user97", "user98", "user99", "user100"
]

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

# Create Login table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Login')
               CREATE TABLE Login
               (Login_ID INT PRIMARY KEY,
               Email VARCHAR(255) UNIQUE,
               Username VARCHAR(100))
               ''')

# Randomly select 100 values from the customized lists
login_records = random.sample(list(zip(login_ids, emails, usernames)), 30)

# Insert records into the Login table
for record in login_records:
    cursor.execute('''
                   INSERT INTO Login (Login_ID, Email, Username)
                   VALUES (?, ?, ?)
                   ''',
                   record[0], record[1], record[2])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
