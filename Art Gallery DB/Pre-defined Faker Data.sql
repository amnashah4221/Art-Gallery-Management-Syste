use Business
GO


-- Create Login table
CREATE TABLE Login (
    Login_ID INT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE,
    Username VARCHAR(100) UNIQUE
);

-- Create Staff table
CREATE TABLE Staff (
    S_ID INT PRIMARY KEY,
    S_Address VARCHAR(255),
    S_FirstName VARCHAR(100),
    S_LastName VARCHAR(100),
    S_Email VARCHAR(255) UNIQUE,
    S_PhoneNo VARCHAR(20) UNIQUE
);


-- Create Client table
CREATE TABLE Client (
    C_ID INT PRIMARY KEY,
    C_Email VARCHAR(255) UNIQUE,
    C_FirstName VARCHAR(100),
    C_LastName VARCHAR(100),
    C_PhoneNo VARCHAR(20) UNIQUE,
    C_Address VARCHAR(255)
);

-- Create Artist table
CREATE TABLE Artist (
    A_ID INT PRIMARY KEY,
    A_FirstName VARCHAR(100),
    A_LastName VARCHAR(100),
    A_PhoneNo VARCHAR(20),
    A_Email VARCHAR(255) UNIQUE,
    A_Address VARCHAR(255),
    SocialMediaProfile VARCHAR(255),
    SignatureStyle VARCHAR(255)
);

-- Create Artwork table
CREATE TABLE Artwork (
    Art_ID INT PRIMARY KEY,
    A_ID INT,
    Title VARCHAR(255),
    Medium VARCHAR(100),
    Dimensions VARCHAR(100),
    DateCompleted DATE,
    Price DECIMAL(10, 2),
    Availability VARCHAR(20),
    FOREIGN KEY (A_ID) REFERENCES Artist(A_ID)
);

-- Create Exhibition table
CREATE TABLE Exhibition (
    E_ID INT PRIMARY KEY,
    StartDate DATE,
    EndDate DATE,
    Location VARCHAR(255),
    E_Name VARCHAR(255),
    Theme VARCHAR(255),
    Art_ID INT,
    FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID)
);

-- Create Gallery table
CREATE TABLE Gallery (
    G_ID INT PRIMARY KEY,
    GalleryName VARCHAR(255),
    Status VARCHAR(50),
    Location VARCHAR(255)
);

-- Create Sales table
CREATE TABLE Sales (
    Sale_ID INT PRIMARY KEY,
    Art_ID INT,
    C_ID INT,
    SalePrice DECIMAL(10, 2),
    SaleDate DATE,
    ArtistCommission DECIMAL(10, 2),
    FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID),
    FOREIGN KEY (C_ID) REFERENCES Client(C_ID)
);

-- Create Loan table
CREATE TABLE Loan (
    Loan_ID INT PRIMARY KEY,
    Art_ID INT,
    LoanAgreement VARCHAR(255),
    Duration INT,
    ExpiryDate DATE,
    TransportTracking VARCHAR(100),
    MonitoringStatus VARCHAR(50),
    FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID)
);

SELECT * FROM Login

SELECT * FROM Staff

SELECT * FROM Client

SELECT * FROM Artist

SELECT * FROM Artwork

SELECT * FROM Exhibition

SELECT * FROM Gallery

SELECT * FROM Sales

SELECT * FROM Loan