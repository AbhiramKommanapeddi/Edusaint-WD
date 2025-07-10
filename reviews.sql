-- School Reviews Database Schema
-- Database: school_reviews

CREATE DATABASE
IF NOT EXISTS school_reviews;
USE school_reviews;

-- Table structure for reviews
CREATE TABLE
IF NOT EXISTS reviews
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR
(100) NOT NULL,
    reviewer_name VARCHAR
(100) NOT NULL,
    rating INT CHECK
(rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data for testing
INSERT INTO reviews
    (school_name, reviewer_name, rating, comment)
VALUES
    ('ABC International School', 'John Doe', 5, 'Excellent school with great faculty and infrastructure. My child loves going to school every day.'),
    ('Springfield Elementary', 'Jane Smith', 4, 'Good academic programs but could improve extracurricular activities.'),
    ('Green Valley High School', 'Mike Johnson', 3, 'Average school with decent facilities. Teachers are supportive but need more resources.');