CREATE DATABASE ArtGalleryManagement
use ArtGalleryManagement
GO

CREATE TABLE Users (
	UserID INT PRIMARY KEY,
	UserEmail VARCHAR(255) UNIQUE,
	Username VARCHAR(100) UNIQUE,
	Password VARCHAR(255),
	Role VARCHAR(100),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
	Address VARCHAR(255),
    PhoneNo VARCHAR(20) UNIQUE,
);
 
-- Create Artist table
CREATE TABLE Artist (
    AID INT PRIMARY KEY,
	UserID INT,
    SocialMediaProfile VARCHAR(255),
    SignatureStyle VARCHAR(255),
	FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Artwork table
CREATE TABLE Artwork (
    ArtID INT PRIMARY KEY,
    AID INT,
    Title VARCHAR(255),
    Medium VARCHAR(100),
    Dimensions VARCHAR(100),
    DateCompleted DATE,
	Availability VARCHAR(20),
    Price DECIMAL(10, 2),
    FOREIGN KEY (AID) REFERENCES Artist(AID)
);

-- Create Gallery table
CREATE TABLE Gallery (
    GID INT PRIMARY KEY,
	UserID INT,
    GalleryName VARCHAR(255),
    Status VARCHAR(50),
    Location VARCHAR(255),
	FOREIGN KEY (UserID) REFERENCES Users(UserID),
);

-- Create Exhibition table
CREATE TABLE Exhibition (
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
);

-- Create Sales table
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
	UserID INT, 
    ArtID INT,
    Price DECIMAL(10, 2),
    SaleDate DATE,
    ArtistCommission DECIMAL(10, 2),
    FOREIGN KEY (ArtID) REFERENCES Artwork(ArtID),
	FOREIGN KEY (UserID) REFERENCES Users(UserID),
	CHECK (Price > 0)
);

-- Create Loan table
CREATE TABLE Loan (
    LoanID INT PRIMARY KEY,
	UserID INT, 
    ArtID INT,
	LoanAmount DECIMAL(10, 2),
    DurationInDays INT,
    ExpiryDate DATE,
    TransportTracking VARCHAR(100),
    MonitoringStatus VARCHAR(50),
    FOREIGN KEY (ArtID) REFERENCES Artwork(ArtID),
	FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

SELECT * FROM Users 

SELECT * FROM Artist

SELECT * FROM Artwork -- if not for sale then do null

SELECT * FROM Gallery

SELECT * FROM Exhibition

SELECT * FROM Sales

SELECT * FROM Loan

DELETE FROM Artwork
WHERE ArtID = 18;

-- Insert an artwork with 'Not For Sale' availability into the Sales table
INSERT INTO Sales (UserID, ArtID, Price, SaleDate, ArtistCommission)
VALUES (1, 16, 500, GETDATE(), 100);

-- This query should trigger the 'trg_PreventArtworkDeletion' trigger



GO
-- Trigger to prevent deletion of Artwork when its availability is 'Sold' or 'On Loan'
CREATE TRIGGER trg_PreventArtworkDeletion
ON Artwork
AFTER DELETE
AS
BEGIN
    -- Check if any of the deleted artworks are 'Sold' or 'On Loan'
    IF EXISTS (SELECT * FROM deleted WHERE Availability IN ('Sold', 'On Loan'))
    BEGIN
        -- If any deleted artwork is 'Sold' or 'On Loan', display a message and roll back the deletion
        RAISERROR ('Artwork cannot be deleted because it is either Sold or On Loan.', 16, 1);
        ROLLBACK TRANSACTION;
    END
    ELSE
    BEGIN
        -- If none of the deleted artworks are 'Sold' or 'On Loan', proceed with the deletion
        DELETE FROM Artwork WHERE ArtID IN (SELECT ArtID FROM deleted);
    END
END;

GO
-- Ensure Artwork Availability is updated upon purchase or loan
CREATE TRIGGER trg_UpdateArtworkAvailabilityOnPurchase
ON Sales
AFTER INSERT
AS
BEGIN
    UPDATE Artwork
    SET Availability = 'sold'
    WHERE ArtID IN (SELECT ArtID FROM inserted);
END;
GO

CREATE TRIGGER trg_UpdateArtworkAvailabilityOnLoan
ON Loan
AFTER INSERT
AS
BEGIN
    UPDATE Artwork
    SET Availability = 'on loan'
    WHERE ArtID IN (SELECT ArtID FROM inserted);
END;
GO

CREATE TRIGGER trg_SetPriceToNullForNotForSale
ON Artwork
AFTER UPDATE
AS
BEGIN
    IF EXISTS (SELECT * FROM inserted WHERE Availability = 'Not for Sale')
    BEGIN
        UPDATE Artwork
        SET Price = NULL
        WHERE ArtID IN (SELECT ArtID FROM inserted WHERE Availability = 'Not for Sale');
    END
END;
GO

CREATE TRIGGER trg_UpdateAvailabilityOnSale
ON Sales
AFTER INSERT
AS
BEGIN
    UPDATE Artwork
    SET Availability = 'Sold'
    WHERE ArtID IN (SELECT ArtID FROM inserted);

    DELETE FROM Exhibition
    WHERE ArtID IN (SELECT ArtID FROM inserted);
END;
GO

CREATE TRIGGER trg_UpdateAvailabilityOnLoan
ON Loan
AFTER INSERT
AS
BEGIN
    UPDATE Artwork
    SET Availability = 'On Loan'
    WHERE ArtID IN (SELECT ArtID FROM inserted);

    DELETE FROM Exhibition
    WHERE ArtID IN (SELECT ArtID FROM inserted);
END;
GO

CREATE TRIGGER trg_DeleteArtworkReferences
ON Artwork
AFTER DELETE
AS
BEGIN
    DECLARE @ArtID INT;
    SELECT @ArtID = ArtID FROM deleted;

    DELETE FROM Sales WHERE ArtID = @ArtID;
    DELETE FROM Loan WHERE ArtID = @ArtID;
    DELETE FROM Exhibition WHERE ArtID = @ArtID;
END;
GO

CREATE TRIGGER trg_DeleteArtistReferences
ON Artist
AFTER DELETE
AS
BEGIN
    DECLARE @AID INT;
    SELECT @AID = AID FROM deleted;

    DELETE FROM Artwork WHERE AID = @AID;

    DELETE FROM Sales WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID = @AID);
    DELETE FROM Loan WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID = @AID);
    DELETE FROM Exhibition WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID = @AID);
END;
GO


CREATE TRIGGER trg_DeleteStaffUserReferences
ON Users
AFTER DELETE
AS
BEGIN
    DECLARE @UserID INT;
    DECLARE @Role VARCHAR(100);
    
    SELECT @UserID = UserID, @Role = Role FROM deleted;

    IF @Role = 'staff'
    BEGIN
        DELETE FROM Sales WHERE UserID = @UserID;
        DELETE FROM Loan WHERE UserID = @UserID;
    END
END;
GO

CREATE TRIGGER trg_EnsureAvailableArtworkForPurchase
ON Sales
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN Artwork a ON i.ArtID = a.ArtID
        WHERE a.Availability != 'available'
    )
    BEGIN
        RAISERROR ('Artwork is not available for purchase.', 16, 1);
    END
    ELSE
    BEGIN
        INSERT INTO Sales (SaleID, UserID, ArtID, Price, SaleDate, ArtistCommission)
        SELECT SaleID, UserID, ArtID, Price, SaleDate, ArtistCommission
        FROM inserted;
        
        UPDATE Artwork
        SET Availability = 'sold'
        WHERE ArtID IN (SELECT ArtID FROM inserted);
        
        DELETE FROM Exhibition WHERE ArtID IN (SELECT ArtID FROM inserted);
    END
END;
GO


CREATE TRIGGER trg_EnsureAvailableArtworkForLoan
ON Loan
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN Artwork a ON i.ArtID = a.ArtID
        WHERE a.Availability != 'available'
    )
    BEGIN
        RAISERROR ('Artwork is not available for loan.', 16, 1);
    END
    ELSE
    BEGIN
        INSERT INTO Loan (LoanID, UserID, ArtID, LoanAmount, DurationInDays, ExpiryDate, TransportTracking, MonitoringStatus)
        SELECT LoanID, UserID, ArtID, LoanAmount, DurationInDays, ExpiryDate, TransportTracking, MonitoringStatus
        FROM inserted;
        
        UPDATE Artwork
        SET Availability = 'on loan'
        WHERE ArtID IN (SELECT ArtID FROM inserted);
        
        DELETE FROM Exhibition WHERE ArtID IN (SELECT ArtID FROM inserted);
    END
END;
GO

-- Trigger to delete dependent records in Sales, Loan, and Gallery tables when a User is deleted
CREATE TRIGGER trg_DeleteDependentRecordsOnUserDelete
ON Users
INSTEAD OF DELETE
AS
BEGIN
    DELETE FROM Sales WHERE UserID IN (SELECT UserID FROM deleted);
    DELETE FROM Loan WHERE UserID IN (SELECT UserID FROM deleted);
    DELETE FROM Gallery WHERE UserID IN (SELECT UserID FROM deleted);
    DELETE FROM Users WHERE UserID IN (SELECT UserID FROM deleted);
END;
GO

-- Trigger to delete dependent records in Exhibition table when an Artwork is deleted
CREATE TRIGGER trg_DeleteDependentRecordsOnArtworkDelete
ON Artwork
AFTER DELETE
AS
BEGIN
    DELETE FROM Exhibition WHERE ArtID IN (SELECT ArtID FROM deleted);
    DELETE FROM Sales WHERE ArtID IN (SELECT ArtID FROM deleted);
    DELETE FROM Loan WHERE ArtID IN (SELECT ArtID FROM deleted);
END;
GO


-- Trigger to delete dependent records in Artwork and other tables when an Artist is deleted
CREATE TRIGGER trg_DeleteDependentRecordsOnArtistDelete
ON Artist
AFTER DELETE
AS
BEGIN
    DELETE FROM Artwork WHERE AID IN (SELECT AID FROM deleted);
    DELETE FROM Exhibition WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID IN (SELECT AID FROM deleted));
    DELETE FROM Sales WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID IN (SELECT AID FROM deleted));
    DELETE FROM Loan WHERE ArtID IN (SELECT ArtID FROM Artwork WHERE AID IN (SELECT AID FROM deleted));
    DELETE FROM Artist WHERE AID IN (SELECT AID FROM deleted);
END;
GO


-- Drop existing foreign key constraints if any
ALTER TABLE Artist DROP CONSTRAINT IF EXISTS FK_Artist_UserID;
ALTER TABLE Artwork DROP CONSTRAINT IF EXISTS FK_Artwork_AID;
ALTER TABLE Exhibition DROP CONSTRAINT IF EXISTS FK_Exhibition_ArtID;
ALTER TABLE Exhibition DROP CONSTRAINT IF EXISTS FK_Exhibition_GID;
ALTER TABLE Sales DROP CONSTRAINT IF EXISTS FK_Sales_ArtID;
ALTER TABLE Sales DROP CONSTRAINT IF EXISTS FK_Sales_UserID;
ALTER TABLE Loan DROP CONSTRAINT IF EXISTS FK_Loan_ArtID;
ALTER TABLE Loan DROP CONSTRAINT IF EXISTS FK_Loan_UserID;
ALTER TABLE Gallery DROP CONSTRAINT IF EXISTS FK_Gallery_UserID;

-- Add foreign key constraints with cascading deletes

-- Artist to Users
ALTER TABLE Artist
ADD CONSTRAINT FK_Artist_UserID
FOREIGN KEY (UserID)
REFERENCES Users(UserID)
ON DELETE CASCADE;

-- Artwork to Artist
ALTER TABLE Artwork
ADD CONSTRAINT FK_Artwork_AID
FOREIGN KEY (AID)
REFERENCES Artist(AID)
ON DELETE CASCADE;

-- Exhibition to Artwork
ALTER TABLE Exhibition
ADD CONSTRAINT FK_Exhibition_ArtID
FOREIGN KEY (ArtID)
REFERENCES Artwork(ArtID)
ON DELETE CASCADE;

-- Exhibition to Gallery
ALTER TABLE Exhibition
ADD CONSTRAINT FK_Exhibition_GID
FOREIGN KEY (GID)
REFERENCES Gallery(GID)
ON DELETE CASCADE;

-- Sales to Artwork
ALTER TABLE Sales
ADD CONSTRAINT FK_Sales_ArtID
FOREIGN KEY (ArtID)
REFERENCES Artwork(ArtID)
ON DELETE CASCADE;

-- Loan to Artwork
ALTER TABLE Loan
ADD CONSTRAINT FK_Loan_ArtID
FOREIGN KEY (ArtID)
REFERENCES Artwork(ArtID)
ON DELETE CASCADE;

-- Sales to Users
ALTER TABLE Sales
ADD CONSTRAINT FK_Sales_UserID
FOREIGN KEY (UserID)
REFERENCES Users(UserID)
ON DELETE CASCADE;

-- Loan to Users
ALTER TABLE Loan
ADD CONSTRAINT FK_Loan_UserID
FOREIGN KEY (UserID)
REFERENCES Users(UserID)
ON DELETE CASCADE;

-- Gallery to Users
ALTER TABLE Gallery
ADD CONSTRAINT FK_Gallery_UserID
FOREIGN KEY (UserID)
REFERENCES Users(UserID)
ON DELETE CASCADE;

