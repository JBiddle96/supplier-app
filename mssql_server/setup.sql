/*

Enter custom T-SQL here that would run after SQL Server has started up. 

*/


CREATE DATABASE SupplierInfo;
GO

USE SupplierInfo;
CREATE TABLE SupplierMasking (
    SupplierID INT,
    SupplierTypeID INT,
    Address BIT,
    Phone BIT,
    Postcode BIT,
    Email BIT
);

INSERT INTO SupplierMasking(
        SupplierID,
        SupplierTypeID,
        Address,
        Phone,
        Postcode,
        Email
    )
VALUES
(NULL, 1, 0, 1, 0, 0),
(NULL, 2, 0, 1, 0, 0),
(NULL, 3, 0, 1, 0, 0),
(10001, 1, 1, 1, 0, 0),
(10002, 1, 0, 1, 0, 1),
(10003, 3, 1, 1, 1, 1),
(10004, 3, 1, 1, 1, 1);
GO

USE SupplierInfo;
CREATE TABLE SupplierID (
    SupplierID INT,
    SupplierName NVARCHAR(255),
    SupplierTypeID INT
);
INSERT INTO SupplierID(
        SupplierID,
        SupplierName,
        SupplierTypeID
    )
VALUES
(10001, "Hilton", 1),
(10002, "Ibis", 1),
(10003, "Darwin Harbour Cruises", 3),
(10004, "Hughes Limos", 3),
(10005, "Sydney Harbour Cruises", 3)
GO

USE SupplierInfo
CREATE TABLE SupplierTypeID (
    SupplierTypeID INT,
    SupplierType NVARCHAR(255)
);
INSERT INTO SupplierTypeID(
        SupplierTypeID,
        SupplierType
    )
VALUES
(1, "Hotel"),
(2, "Transfers"),
(3, "Tours")
GO