create database Company
use Company
GO

-- Create Login table
CREATE TABLE Login (
    Login_ID INT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE,
    Username VARCHAR(100) UNIQUE
);
-- Drop the existing primary key constraint 
ALTER TABLE Login DROP CONSTRAINT PK__Login__D7886867EF8C4E51;

GO

-- Create a new clustered index on the "Username" column
CREATE CLUSTERED INDEX IX_Login_Username ON Login (Username ASC);
GO



--Create Table Staff
CREATE TABLE Staff (
    S_ID INT NOT NULL,
    S_Address VARCHAR(255),
    S_FirstName VARCHAR(100),
    S_LastName VARCHAR(100),
    S_Email VARCHAR(255) UNIQUE,
    S_PhoneNo VARCHAR(20) UNIQUE,
	CONSTRAINT PK_STAFF PRIMARY KEY (S_ID)
);

-- Drop the existing primary key constraint
ALTER TABLE Staff DROP CONSTRAINT PK_Staff;

-- Create a new clustered index on the "S_FirstName" column
CREATE CLUSTERED INDEX IX_Staff_FirstName ON Staff (S_FirstName ASC);




-- Create Client table
CREATE TABLE Client (
    C_ID INT NOT NULL,
    C_Email VARCHAR(255) UNIQUE,
    C_FirstName VARCHAR(100),
    C_LastName VARCHAR(100),
    C_PhoneNo VARCHAR(20) UNIQUE,
    C_Address VARCHAR(255)

);
-- Create a clustered index on the FirstName column
CREATE CLUSTERED INDEX IX_ClientFirstName ON Client (C_FirstName ASC);

-- Add the primary key constraint on Client_ID after creating the clustered index
ALTER TABLE Client ADD CONSTRAINT PK_Client PRIMARY KEY (C_ID);




-- Create Artist table
CREATE TABLE Artist (
    A_ID INT NOT NULL,
    A_FirstName VARCHAR(100),
    A_LastName VARCHAR(100),
    A_PhoneNo VARCHAR(20),
    A_Email VARCHAR(255) UNIQUE,
    A_Address VARCHAR(255),
    SocialMediaProfile VARCHAR(255),
    SignatureStyle VARCHAR(255),
);

-- Create a clustered index on the Artist FirstName column
CREATE CLUSTERED INDEX IX_Artist_FirstName ON Artist (A_Firstname ASC);

-- Add the primary key constraint on Art_ID after creating the clustered index
ALTER TABLE Artist ADD CONSTRAINT PK_Artist PRIMARY KEY (A_ID);




-- Create Artwork table
CREATE TABLE Artwork (
    Art_ID INT NOT NULL,
    A_ID INT,
    Title VARCHAR(255),
    Medium VARCHAR(100),
    Dimensions VARCHAR(100),
    DateCompleted DATE,
    Price DECIMAL(10, 2),
    Availability VARCHAR(20),
    CONSTRAINT FK_Artwork_Artist FOREIGN KEY (A_ID) REFERENCES Artist(A_ID)
);

-- Create a clustered index on the Availability column
CREATE CLUSTERED INDEX IX_Artwork_Availability ON Artwork (Availability ASC);

-- Add the primary key constraint on Art_ID after creating the clustered index
ALTER TABLE Artwork ADD CONSTRAINT PK_Artwork PRIMARY KEY (Art_ID);




-- Create Exhibition table
CREATE TABLE Exhibition (
    E_ID INT,
    StartDate DATE,
    EndDate DATE,
    Location VARCHAR(255),
    E_Name VARCHAR(255),
    Theme VARCHAR(255),
    Art_ID INT,
    CONSTRAINT PK_EXHIBITION PRIMARY KEY (E_ID),
    CONSTRAINT FK_EXHIBITION FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID)
);

-- Drop the existing primary key constraint
ALTER TABLE Exhibition DROP CONSTRAINT PK_Exhibition;

-- Add a clustered index on the StartDate column
CREATE CLUSTERED INDEX IX_StartDate ON Exhibition (StartDate ASC);




-- Create Gallery table
CREATE TABLE Gallery (
    G_ID INT,
    GalleryName VARCHAR(255),
    Status VARCHAR(50),
    Location VARCHAR(255),
	CONSTRAINT PK_Gallery PRIMARY KEY (G_ID)
);

-- Drop the existing primary key constraint
ALTER TABLE Gallery DROP CONSTRAINT PK_Gallery;

-- Create a new clustered index on the "Gallery Status" column
CREATE CLUSTERED INDEX IX_Gallery_Status ON Gallery (Status);




-- Create Sales table
CREATE TABLE Sales (
    Sale_ID INT,
    Art_ID INT,
    C_ID INT,
    SalePrice DECIMAL(10, 2),
    SaleDate DATE,
    ArtistCommission DECIMAL(10, 2),
	CONSTRAINT PK_SALE PRIMARY KEY (Sale_ID),
    CONSTRAINT FK_SaleArt FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID),
    CONSTRAINT FK_SaleClient FOREIGN KEY (C_ID) REFERENCES Client(C_ID)
);

-- Drop the existing primary key constraint
ALTER TABLE Sales DROP CONSTRAINT PK_SALE;

-- Add a clustered index on the SalesDate column
CREATE CLUSTERED INDEX IX_SalesDate ON Sales (SaleDate ASC);




-- Create Loan table
CREATE TABLE Loan (
	 Loan_ID INT,
     Art_ID INT,
     LoanAgreement VARCHAR(255),
     DurationInDays INT NULL,
     ExpiryDate DATE NULL,
     TransportTracking VARCHAR(100) NULL,
     MonitoringStatus VARCHAR(50) NULL,
     CONSTRAINT PK_LOAN PRIMARY KEY (Loan_ID),
     CONSTRAINT FK_LOAN_ART FOREIGN KEY (Art_ID) REFERENCES Artwork(Art_ID)
);

-- Drop the foreign key constraint in the Loan table
ALTER TABLE Loan DROP CONSTRAINT FK_LOAN_ART;

-- Drop the existing primary key constraint
ALTER TABLE Loan DROP CONSTRAINT PK_LOAN;

-- Add clustered index on the LoanAgreement column
CREATE CLUSTERED INDEX IX_Loan_DurationINDays ON Loan (DurationInDays DESC);


SELECT * FROM Login

SELECT * FROM Staff

SELECT * FROM Client

SELECT * FROM Artist

SELECT * FROM Artwork

SELECT * FROM Exhibition

SELECT * FROM Gallery

SELECT * FROM Sales

SELECT * FROM Loan

