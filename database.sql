CREATE DATABASE IF Not EXISTS 
hospital_db;
USE hospital_db;

CREATE TABLE IF Not EXISTS appointment 
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    age INT,
    doctor VARCHAR(100),
    appointment_date DATE,
    appointment_time TIME
);