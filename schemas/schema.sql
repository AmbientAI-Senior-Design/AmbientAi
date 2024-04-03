CREATE DATABASE IF NOT EXISTS ClientInput;

USE ClientInput;

CREATE TABLE Post (
    id INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE EngagementReport (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    duration INT,
    numberOfPeople INT,
    numberOfEngagedPeople INT,
    score FLOAT,
    fk_post_id INT,
    FOREIGN KEY (fk_post_id) REFERENCES Post(id)
);

CREATE TABLE Slide (
    id INT AUTO_INCREMENT PRIMARY KEY,
    path VARCHAR(255),
    description TEXT,
    fk_post_id INT,
    FOREIGN KEY (fk_post_id) REFERENCES Post(id),
    slide_index INT
);


CREATE TABLE backend (
    image_name VARCHAR(255),
    score int


);