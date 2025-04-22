use University
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

DECLARE @l INT = 1
WHILE @l <= 30
BEGIN
    INSERT INTO Artist (A_ID, A_FirstName, A_LastName, A_PhoneNo, A_Email, A_Address, SocialMediaProfile, SignatureStyle)
    VALUES (@l, 'ArtistFirstName' + CAST(@l AS VARCHAR), 'ArtistLastName' + CAST(@l AS VARCHAR), '+92123456789', 'artist' + CAST(@l AS VARCHAR) + '@example.com', 'ArtistAddress' + CAST(@l AS VARCHAR), 'SocialMediaProfile' + CAST(@l AS VARCHAR), 'SignatureStyle' + CAST(@l AS VARCHAR))
    SET @l = @l + 1
END

-- Insert 30 records into the Artwork table
DECLARE @m INT = 1
WHILE @m <= 30
BEGIN
    INSERT INTO Artwork (Art_ID, A_ID, Title, Medium, Dimensions, DateCompleted, Price, Availability)
    VALUES (@m, @m, 'Title' + CAST(@m AS VARCHAR), 'Medium' + CAST(@m AS VARCHAR), 'Dimensions' + CAST(@m AS VARCHAR), GETDATE(), 100.00, 'Available')
    SET @m = @m + 1
END

DECLARE @q INT = 1
WHILE @q <= 30
BEGIN
    INSERT INTO Loan (Loan_ID, Art_ID, LoanAgreement, Duration, ExpiryDate, TransportTracking, MonitoringStatus)
    VALUES (@q, @q, 'LoanAgreement' + CAST(@q AS VARCHAR), 30, DATEADD(DAY, 30, GETDATE()), 'TransportTracking' + CAST(@q AS VARCHAR), 'MonitoringStatus' + CAST(@q AS VARCHAR))
    SET @q = @q + 1
END

DECLARE @w INT = 1
WHILE @w <= 30
BEGIN
    DECLARE @LoanAgreement VARCHAR(3)
    DECLARE @TransportTracking VARCHAR(20)
    DECLARE @MonitoringStatus VARCHAR(8)

    -- Randomly select values for LoanAgreement, TransportTracking, and MonitoringStatus
    SET @LoanAgreement = CASE WHEN ABS(CHECKSUM(NEWID())) % 2 = 0 THEN 'Yes' ELSE 'No' END
    SET @TransportTracking = CASE WHEN ABS(CHECKSUM(NEWID())) % 2 = 0 THEN 'Being transported' ELSE 'Reached destination' END
    SET @MonitoringStatus = CASE WHEN ABS(CHECKSUM(NEWID())) % 2 = 0 THEN 'Borrowed' ELSE 'Returned' END

    INSERT INTO Loan (Loan_ID, Art_ID, LoanAgreement, Duration, ExpiryDate, TransportTracking, MonitoringStatus)
    VALUES (@w, @w, @LoanAgreement, 30, DATEADD(DAY, 30, GETDATE()), @TransportTracking, @MonitoringStatus)
    SET @w = @w + 1
END


DECLARE @k INT = 1
WHILE @k <= 30
BEGIN
    INSERT INTO Client (C_ID, C_Email, C_FirstName, C_LastName, C_PhoneNo, C_Address)
    VALUES (@k, 'client' + CAST(@k AS VARCHAR) + '@example.com', 'ClientFirstName' + CAST(@k AS VARCHAR), 'ClientLastName' + CAST(@k AS VARCHAR), '+92123456789', 'ClientAddress' + CAST(@k AS VARCHAR))
    SET @k = @k + 1
END

DECLARE @p INT = 1
WHILE @p <= 30
BEGIN
    INSERT INTO Sales (Sale_ID, Art_ID, C_ID, SalePrice, SaleDate, ArtistCommission)
    VALUES (@p, @p, @p, 100.00, GETDATE(), 10.00)
    SET @p = @p + 1
END

DECLARE @n INT = 1
WHILE @n <= 30
BEGIN
    INSERT INTO Exhibition (E_ID, StartDate, EndDate, Location, E_Name, Theme, Art_ID)
    VALUES (@n, DATEADD(DAY, @n, GETDATE()), DATEADD(DAY, @n + 10, GETDATE()), 'Location' + CAST(@n AS VARCHAR), 'ExhibitionName' + CAST(@n AS VARCHAR), 'Theme' + CAST(@n AS VARCHAR), @n)
    SET @n = @n + 1
END

SELECT * FROM Client

SELECT * FROM LOAN

SELECT * FROM Login

SELECT * FROM SALES
select * from staff
select * from artist

select * from artwork

select * from exhibition
