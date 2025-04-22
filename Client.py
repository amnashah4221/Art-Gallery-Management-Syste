import random
import pyodbc as odbc

# Define customized lists for Client attributes
client_ids = list(range(1, 101))  # 100 Client IDs from 1 to 100
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
    "4848 Birchwood Avenue, Birchwood Manor", "4949 Park Lane, Park Manor", "5050 Hillcrest Drive, Hillcrest Manor",
    "5151 Cedar Street, Cedar Manor", "5252 Sunset Drive, Sunset Manor", "5353 River Boulevard, Riverview Heights",
    "5454 Lakeview Lane, Lakeview Heights", "5555 Elmwood Terrace, Elmwood Heights", "5656 Maplewood Avenue, Maplewood Heights",
    "5757 Birchwood Road, Birchwood Heights", "5858 Parkview Lane, Parkview Heights", "5959 Hillcrest Road, Hillcrest Heights",
    "6060 Cedar Avenue, Cedar Heights", "6161 Sunset Lane, Sunset Hills", "6262 River Road, Riverview Hills",
    "6363 Lakeview Drive, Lakeview Hills", "6464 Elmwood Road, Elmwood Hills", "6565 Maplewood Boulevard, Maplewood Hills",
    "6666 Birchwood Drive, Birchwood Hills", "6767 Park Lane, Park Hills", "6868 Hillcrest Boulevard, Hillcrest Hills",
    "6969 Cedar Drive, Cedar Hills", "7070 Sunset Road, Sunset Gardens", "7171 River Lane, Riverview Gardens",
    "7272 Lakeview Avenue, Lakeview Gardens", "7373 Elmwood Street, Elmwood Gardens", "7474 Maplewood Drive, Maplewood Gardens",
    "7575 Birchwood Boulevard, Birchwood Gardens", "7676 Park Road, Park Gardens", "7777 Hillcrest Lane, Hillcrest Gardens",
    "7878 Cedar Terrace, Cedar Gardens", "7979 Sunset Street, Sunset Valley", "8080 River Avenue, Riverview Valley"
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
    "92 333 2872837", "92 311 2769816", "92 300 5829084", "92 345 4380295", "92 312 7592038",
    "92 301 9857201", "92 334 8657932", "92 302 1275938", "92 313 9028476", "92 303 2378945",
    "92 346 8562314", "92 314 2378475", "92 304 7923845", "92 347 9203845", "92 315 2093847",
    "92 305 2380475", "92 348 3928574", "92 316 2103857", "92 306 2938475", "92 349 3298574",
    "92 317 3209857", "92 307 3209857", "92 350 3209857", "92 318 3209857", "92 308 3209857",
    "92 351 3209857", "92 319 3209857", "92 309 3209857", "92 352 3209857", "92 320 3209857",
    "92 353 3209857", "92 321 3209857", "92 354 3209857", "92 322 3209857", "92 355 3209857",
    "92 323 3209857", "92 356 3209857", "92 324 3209857", "92 357 3209857", "92 325 3209857",
    "92 358 3209857", "92 326 3209857", "92 359 3209857", "92 327 3209857", "92 360 3209857",
    "92 328 3209857", "92 361 3209857", "92 329 3209857", "92 362 3209857", "92 330 3209857",
    "92 363 3209857", "92 331 3209857", "92 364 3209857", "92 332 3209857", "92 365 3209857",
    "92 366 3209857", "92 367 3209857", "92 368 3209857", "92 369 3209857", "92 370 3209857",
    "92 371 3209857", "92 372 3209857", "92 373 3209857", "92 374 3209857", "92 375 3209857",
    "92 376 3209857", "92 377 3209857", "92 378 3209857", "92 379 3209857", "92 380 3209857",
    "92 381 3209857", "92 382 3209857", "92 383 3209857", "92 384 3209857", "92 385 3209857",
    "92 386 3209857", "92 387 3209857", "92 388 3209857", "92 389 3209857", "92 390 3209857",
    "92 391 3209857", "92 392 3209857", "92 393 3209857", "92 394 3209857", "92 395 3209857",
    "92 396 3209857", "92 397 3209857", "92 398 3209857", "92 399 3209857", "92 400 3209857",
    "92 401 3209857", "92 402 3209857", "92 403 3209857", "92 404 3209857"
]

# Database connection details
SERVER_NAME = r'DESKTOP-L5NG8PP\SQLEXPRESS'
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

# Create Client table if it doesn't exist
cursor.execute('''
               IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Client')
               CREATE TABLE Client
               (C_ID INT PRIMARY KEY,
               C_Email VARCHAR(255) UNIQUE,
               C_FirstName VARCHAR(100),
               C_LastName VARCHAR(100),
               C_PhoneNo VARCHAR(20) UNIQUE,
               C_Address VARCHAR(255))
               ''')

# Randomly select 100 values from the customized lists
client_records = random.sample(list(zip(client_ids, emails, first_names, last_names, phone_numbers, addresses)), 30)

# Insert records into the Client table
for record in client_records:
    cursor.execute('''
                   INSERT INTO Client (C_ID, C_Email, C_FirstName, C_LastName, C_PhoneNo, C_Address)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',
                   record[0], record[1], record[2], record[3], record[4], record[5])
    print("Inserted Successfully")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
