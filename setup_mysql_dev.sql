-- creates dev account and database for AgroMarket portfolio project

CREATE DATABASE IF NOT EXISTS agroMarket_dev_db;
CREATE USER IF NOT EXISTS 'agroMarket_dev'@'localhost' IDENTIFIED BY 'agroMarket_dev_secret';
GRANT ALL PRIVILEGES ON `agroMarket_dev_db`.* TO 'agroMarket_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'agroMarket_dev'@'localhost';
FLUSH PRIVILEGES;
