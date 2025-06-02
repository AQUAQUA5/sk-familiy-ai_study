CREATE DATABASE sk15;

USE sk15;


CREATE TABLE productlines (
  productLine varchar(50),
  textDescription varchar(4000) DEFAULT NULL,
  htmlDescription mediumtext,
  image mediumblob,
  PRIMARY KEY (productLine)
);


CREATE TABLE products (
  productCode varchar(15),
  productName varchar(70) NOT NULL,
  productLine varchar(50) NOT NULL,
  productScale varchar(10) NOT NULL,
  productVendor varchar(50) NOT NULL,
  productDescription text NOT NULL,
  quantityInStock smallint(6) NOT NULL,
  buyPrice decimal(10,2) NOT NULL,
  MSRP decimal(10,2) NOT NULL,
  PRIMARY KEY (productCode),
  FOREIGN KEY (productLine) REFERENCES productlines (productLine)
);


CREATE TABLE offices (
  officeCode varchar(10),
  city varchar(50) NOT NULL,
  phone varchar(50) NOT NULL,
  addressLine1 varchar(50) NOT NULL,
  addressLine2 varchar(50) DEFAULT NULL,
  state varchar(50) DEFAULT NULL,
  country varchar(50) NOT NULL,
  postalCode varchar(15) NOT NULL,
  territory varchar(10) NOT NULL,
  PRIMARY KEY (officeCode)
);

