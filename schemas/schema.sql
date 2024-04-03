CREATE DATABASE IF NOT EXISTS ClientInput;

USE ClientInput;

CREATE TABLE input (
  id INT AUTO_INCREMENT,
  date DATE,
  duration TIME,
  numberOfPeople INT,
  numberOfEngagedPeople INT,
  score FLOAT,
  image_data JSON,
);

CREATE TABLE backend (
    image_name VARCHAR(255),
    score int

);