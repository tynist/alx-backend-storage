-- Script creates a new 'users' table a given required attributes:
-- id, email, name, and country (country column is set of allowed
values using an enumeration)
-- The table is only created if it doesn't already exist

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
