-- Car Parking Management System (CPMS) - MySQL database setup
-- Run once:  mysql -u root -p < cpms_database.sql

DROP DATABASE IF EXISTS CPMS;
CREATE DATABASE CPMS;
USE CPMS;

-- 1. Parking slots
CREATE TABLE ParkingSlot (
    slot_id      INT AUTO_INCREMENT PRIMARY KEY,
    slot_number  VARCHAR(10) NOT NULL UNIQUE,
    level        INT NOT NULL,
    slot_type    ENUM('compact','large','EV') NOT NULL,
    is_occupied  TINYINT(1) NOT NULL DEFAULT 0
);

-- 2. Registered vehicles (vehicle_id = registration number, e.g. DL01AB1234)
CREATE TABLE Vehicle (
    vehicle_id    VARCHAR(15) PRIMARY KEY,
    owner_name    VARCHAR(50) NOT NULL,
    phone         VARCHAR(15),
    vehicle_type  ENUM('compact','large','EV') NOT NULL
);

-- 3. Hourly rate for each slot type (in Rs.)
CREATE TABLE RateCard (
    slot_type      ENUM('compact','large','EV') PRIMARY KEY,
    rate_per_hour  DECIMAL(6,2) NOT NULL
);

-- 4. Parking records (entry/exit history)
CREATE TABLE ParkingRecord (
    record_id   INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id  VARCHAR(15) NOT NULL,
    slot_id     INT NOT NULL,
    entry_time  DATETIME NOT NULL,
    exit_time   DATETIME NULL,
    fee         DECIMAL(8,2) NULL,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (slot_id)    REFERENCES ParkingSlot(slot_id)
);

-- Sample data
INSERT INTO RateCard VALUES ('compact', 20.00), ('large', 40.00), ('EV', 30.00);

INSERT INTO ParkingSlot (slot_number, level, slot_type) VALUES
('A1', 1, 'compact'), ('A2', 1, 'compact'), ('A3', 1, 'compact'),
('B1', 1, 'large'),   ('B2', 1, 'large'),
('E1', 2, 'EV'),      ('E2', 2, 'EV');

INSERT INTO Vehicle VALUES
('DL01AB1234', 'Rahul Sharma', '9876543210', 'compact'),
('UP16CD5678', 'Priya Singh',  '9123456780', 'large'),
('DL02EV9999', 'Amit Verma',   '9988776655', 'EV');
