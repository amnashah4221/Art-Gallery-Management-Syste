import random
import pyodbc as odbc

# Define customized lists for Staff attributes
staff_ids = list(range(1, 101))  # 100 Staff IDs from 1 to 100
addresses = [
    "123 Scott Street, Main Town", "456 Elm Street, Downtown", "789 Maple Avenue, Westside",
    "321 Oak Lane, East End", "654 Pine Street, Riverside", "987 Cedar Avenue, Uptown",
    "246 Birch Road, Hillside", "135 Walnut Drive, Lakeside", "579 Cherry Lane, Parkview",
    "802 Spruce Boulevard, Central", "111 Pinecrest Road, Forest Hills", "222 Sunset Drive, Sunset Valley",
    "333 Riverside Drive, Riverfront", "444 Oakwood Lane, Oakville", "555 Lakeview Drive, Lakeville",
    "666 Elmwood Avenue, Elmwood Park", "777 Maplewood Drive, Maplewood", "888 Birchwood Lane, Birchwood",
    "999 Park Avenue, Parkside", "1010 Hillcrest Road, Hillcrest", "1212 Cedar Lane, Cedarville",
    "1313 Sunset Boulevard, Sunnyside", "1414 River Road, Riverview", "1515 Lake Street, Lakeshore",
    "1616 Forest Avenue, Forestview", "1717 Oak Avenue, Oakhill", "1818 Maple Street, Mapleton",
    "1919 Birch Lane, Birchville", "2020 Parkside Drive, Parkville", "2121 Hillside Avenue, Hilltop",
    "2323 Cedar Drive, Cedar Hill", "2424 Sunset Lane, Sunset Park", "2525 River Drive, Riverton",
    "2626 Lakeview Road, Lakeview Heights", "2727 Elmwood Drive, Elmwood Heights", "2828 Maplewood Lane, Maple Heights",
    "2929 Birchwood Road, Birchwood Heights", "3030 Parkview Avenue, Parkview Terrace", "3131 Hillcrest Boulevard, Hillcrest Heights",
    "3333 Cedarwood Drive, Cedarwood Terrace", "3434 Sunset Road, Sunset Heights", "3535 River Lane, Riverview Terrace",
    "3636 Lakeview Avenue, Lakeview Terrace", "3737 Elmwood Road, Elmwood Terrace", "3838 Maplewood Boulevard, Maplewood Terrace",
    "3939 Birchwood Street, Birchwood Terrace", "4040 Park Road, Park Terrace", "4141 Hillcrest Lane, Hillcrest Terrace",
    "4242 Cedar Boulevard, Cedar Terrace", "4343 Sunset Street, Sunset Terrace", "4444 River Avenue, Riverview Manor",
    "4545 Lakeview Boulevard, Lakeview Manor", "4646 Elmwood Lane, Elmwood Manor", "4747 Maplewood Drive, Maplewood Manor",
    "4848 Birchwood Avenue, Birchwood Manor", "4949 Park Lane, Park Manor", "5050 Hillcrest Drive, Hillcrest Manor"
]
first_names = [
    "John", "Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry", "Ivy",
    "Jack", "Linda", "Michael", "Susan", "Peter", "Sophia", "Robert", "Jennifer", "William", "Jessica",
    "Daniel", "Mary", "Christopher", "Karen", "Matthew", "Nancy", "Joshua", "Lisa", "Andrew", "Samantha",
    "James", "Karen", "Joseph", "Emily", "Ryan", "Nicole", "Richard", "Michelle", "David", "Angela",
    "Charles", "Kimberly", "Thomas", "Melissa", "Steven", "Patricia", "Donald", "Amy", "Mark", "Laura",
    "Paul", "Rebecca", "Kevin", "Stephanie", "George", "Elizabeth", "Brian", "Julie", "Edward", "Heather"
]
last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins",
    "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey"
]
emails = [
    "john@example.com", "alice@example.com", "bob@example.com", "carol@example.com", "david@example.com",
    "emma@example.com", "frank@example.com", "grace@example.com", "henry@example.com", "ivy@example.com",
    "jack@example.com", "linda@example.com", "michael@example.com", "susan@example.com", "peter@example.com",
    "sophia@example.com", "robert@example.com", "jennifer@example.com", "william@example.com", "jessica@example.com",
    "daniel@example.com", "mary@example.com", "christopher@example.com", "karen@example.com", "matthew@example.com",
    "nancy@example.com", "joshua@example.com", "lisa@example.com", "andrew@example.com", "samantha@example.com",
    "james@example.com", "karen@example.com", "joseph@example.com", "emily@example.com", "ryan@example.com",
    "nicole@example.com", "richard@example.com", "michelle@example.com", "david@example.com", "angela@example.com",
    "charles@example.com", "kimberly@example.com", "thomas@example.com", "melissa@example.com", "steven@example.com",
    "patricia@example.com", "donald@example.com", "amy@example.com", "mark@example.com", "laura@example.com",
    "paul@example.com", "rebecca@example.com", "kevin@example.com", "stephanie@example.com", "george@example.com",
    "elizabeth@example.com", "brian@example.com", "julie@example.com", "edward@example.com", "heather@example.com"
]
phone_numbers = [
    "92 300 1234567", "92 301 2345678", "92 302 3456789", "92 303 4567890", "92 304 5678901",
    "92 305 6789012", "92 306 7890123", "92 307 8901234", "92 308 9012345", "92 309 0123456",
    "92 310 9876543", "92 311 8765432", "92 312 7654321", "92 313 6543210", "92 314 5432109",
    "92 315 4321098", "92 316 3210987", "92 317 2109876", "92 318 1098765", "92 319 0987654",
    "92 320 9876543", "92 321 8765432", "92 322 7654321", "92 323 6543210", "92 324 5432109",
    "92 325 4321098", "92 326 3210987", "92 327 2109876", "92 328 1098765", "92 329 0987654",
    "92 330 9876543", "92 331 8765432", "92 332 7654321", "92 333 6543210", "92 334 5432109",
    "92 335 4321098", "92 336 3210987", "92 337 2109876", "92 338 1098765", "92 339 0987654",
    "92 340 9876543", "92 341 8765432", "92 342 7654321", "92 343 6543210", "92 344 5432109",
    "92 345 4321098", "92 346 3210987", "92 347 2109876", "92 348 1098765", "92 349 0987654",
    "92 350 9876543", "92 351 8765432", "92 352 7654321", "92 353 6543210", "92 354 5432109",
    "92 355 4321098", "92 356 3210987", "92 357 2109876", "92 358 1098765", "92 359 0987654",
    "92 360 9876543", "92 361 8765432", "92 362 7654321", "92 363 6543210", "92 364 5432109",
    "92 365 4321098", "92 366 3210987", "92 367 2109876", "92 368 1098765", "92 369 0987654",
    "92 370 9876543", "92 371 8765432", "92 372 7654321", "92 373 6543210", "92 374 5432109",
    "92 375 4321098", "92 376 3210987", "92 377 2109876", "92 378 1098765", "92 379 0987654",
    "92 380 9876543", "92 381 8765432", "92 382 7654321", "92 383 6543210", "92 384 5432109",
    "92 385 4321098", "92 386 3210987", "92 387 2109876", "92 388 1098765", "92 389 0987654",
    "92 390 9876543", "92 391 8765432", "92 392 7654321", "92 393 6543210", "92 394 5432109",
    "92 395 4321098", "92 396 3210987", "92 397 2109876", "92 398 1098765", "92 399 0987654",
    "92 400 9876543", "92 401 8765432", "92 402 7654321", "92 403 6543210", "92 404 5432109"
]

# Database connection details
SERVER_NAME = r'DESKTOP-8J774MH\SQLEXPRESS'
DATABASE_NAME = 'Shopping'

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

# Create Staff table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Staff')
               CREATE TABLE Staff
               (
                S_ID INT NOT NULL,
                S_Address VARCHAR(255),
                S_FirstName VARCHAR(100),
                S_LastName VARCHAR(100),
                S_Email VARCHAR(255) UNIQUE,
                S_PhoneNo VARCHAR(20) UNIQUE,
                CONSTRAINT PK_STAFF PRIMARY KEY (S_ID)
               )
               ''')

# Randomly select 30 values from the customized lists
staff_records = random.sample(list(zip(staff_ids, addresses, first_names, last_names, emails, phone_numbers)), 30)

# Insert records into the Staff table
for record in staff_records:
    cursor.execute('''
                   INSERT INTO Staff (S_ID, S_Address, S_FirstName, S_LastName, S_Email, S_PhoneNo)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], record[2], record[3], record[4], record[5])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()