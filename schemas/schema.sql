CREATE DATABASE IF NOT EXISTS `ClientInput`;

use ClientInput;

create table input (
    input_id INT, 
    image_score INT,
    input_name VARCHAR(255),
    input_image_path  VARCHAR(225),
    client_name VARCHAR(225)
);

