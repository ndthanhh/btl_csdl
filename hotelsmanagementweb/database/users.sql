SELECT * FROM hotel_management.users;
-- CREATE TABLE user_security (
--     user_id INT PRIMARY KEY,
--     email_verified BOOLEAN DEFAULT FALSE,
--     email_verification_token VARCHAR(100),
--     password_reset_token VARCHAR(100),
--     password_reset_expires DATETIME,
--     last_login DATETIME,
--     login_attempts INT DEFAULT 0,
--     locked_until DATETIME,


--     FOREIGN KEY (user_id) REFERENCES users(user_id)
-- );