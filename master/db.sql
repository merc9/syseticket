CREATE TABLE Rate(
RateId INT IDENTITY(1,1) NOT NULL,
RateName VARCHAR(100),
RatePrice MONEY,
RateTime INT
)
GO

ALTER TABLE Rate
ADD CONSTRAINT pk_Rate
PRIMARY KEY(RateId)
GO

CREATE TABLE PaymentType(
PaymentId INT NOT NULL,
PaymentName VARCHAR(25) NOT NULL
)
GO

ALTER TABLE PaymentType
ADD CONSTRAINT pk_PaymentType
PRIMARY KEY(PaymentId)
GO

CREATE TABLE Invoice(
InvoiceId BIGINT NOT NULL,
CustomerName NVARCHAR(50),
CustomerId VARCHAR(10),
CustomerPhone VARCHAR(20),
CustomerAddress NVARCHAR(150),
InvoiceDate DATE NOT NULL,
InitHour VARCHAR(50) NOT NULL,
EndHour VARCHAR(50) NOT NULL,
ChosenRate INT NOT NULL,
Total MONEY,
Quantity INT,
PaymentType INT NOT NULL,
CustomerEmail NVARCHAR(75),
InvoiceActive BIT NULL,
Tax INT NULL
)
GO



ALTER TABLE Invoice
ADD CONSTRAINT pk_Invoice
PRIMARY KEY(InvoiceId),
CONSTRAINT fk_ChosenRate_Rate
FOREIGN KEY(ChosenRate) REFERENCES Rate(RateId),
CONSTRAINT fk_PaymentType_PaymentType
FOREIGN KEY(PaymentType) REFERENCES PaymentType(PaymentId)
GO

CREATE SEQUENCE Invoice_Sequence
  AS BIGINT
  START WITH 1000000000000000000
  INCREMENT BY 1
  MINVALUE 0
  NO MAXVALUE
  NO CYCLE
  NO CACHE
GO

INSERT INTO PaymentType(PaymentName) VALUES ('Efectivo')
INSERT INTO PaymentType(PaymentName) VALUES ('Tarjeta')


CREATE TABLE Company(
CompanyID VARCHAR(20) NOT NULL,
CompanyName VARCHAR(100) NOT NULL,
CompanyPhone VARCHAR(50) NOT NULL,
CompanyAddress VARCHAR(250) NOT NULL,
CompanyElectronicInvoiceCode NVARCHAR(300) NULL,
)
GO

ALTER TABLE Company
ADD CONSTRAINT pk_Company
PRIMARY KEY(CompanyID)
GO


INSERT INTO Company VALUES('8-0113-0999','Aventuras','+(506) 8785-6215','Mall plaza occidente','50610061900080113099900100001010000000013193372989')
GO

CREATE FUNCTION getCompanyID ()
RETURNS VARCHAR AS
BEGIN
	DECLARE @result VARCHAR(20)
    SET @result = (SELECT CompanyID FROM Company)
    RETURN @result
END

SELECT [dbo].getCompanyID() AS ID