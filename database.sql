-- CREATE DATABASE
CREATE DATABASE IF NOT EXISTS leafguard_db;
USE leafguard_db;

-- USERS TABLE
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);

-- FARMS TABLE
CREATE TABLE farms (
    farm_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    farm_name VARCHAR(100) NOT NULL,
    location_details VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- TREES TABLE
CREATE TABLE trees (
    tree_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    tree_name VARCHAR(100) NOT NULL,
    age_years INT,
    planting_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
);

-- IMAGES TABLE
CREATE TABLE images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tree_id INT,
    file_path VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'analyzed', 'archived') DEFAULT 'analyzed',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (tree_id) REFERENCES trees(tree_id) ON DELETE SET NULL
);

-- PREDICTIONS TABLE
CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT NOT NULL,
    predicted_class VARCHAR(50) NOT NULL,
    confidence_score DECIMAL(5, 4) NOT NULL,
    raw_output TEXT,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE
);

-- FEEDBACK TABLE
CREATE TABLE feedbacks (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('new', 'in_review', 'resolved') DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- DISEASES TABLE
CREATE TABLE diseases (
    disease_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    organic_treatment TEXT,
    chemical_treatment TEXT,
    is_trained BOOLEAN DEFAULT TRUE
);

-- ARCHIVED IMAGES TABLE
CREATE TABLE archived_images (
    archive_id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT NOT NULL,
    user_id INT NOT NULL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- INSERT DISEASE DATA
INSERT INTO diseases (name, description, organic_treatment, chemical_treatment) VALUES
('Anthracnose','Fungal disease','Neem oil','Fungicide'),
('Healthy','No disease','Maintenance','None');

-- ✅ FIXED PART (NO ERROR NOW)

-- First create a dummy user
INSERT INTO users (username, email, password_hash)
VALUES ('admin','admin@gmail.com','123');

-- Then create farm
INSERT INTO farms (user_id, farm_name)
VALUES (1,'Default Farm');

-- Then create tree (SAFE now)
INSERT INTO trees (farm_id, tree_name, age_years)
VALUES (1,'Old Mango Tree',5);

-- ADD EXTRA COLUMNS
ALTER TABLE farms
ADD COLUMN latitude DECIMAL(10,8),
ADD COLUMN longitude DECIMAL(11,8);

ALTER TABLE images
ADD COLUMN scan_latitude DECIMAL(10,8),
ADD COLUMN scan_longitude DECIMAL(11,8);