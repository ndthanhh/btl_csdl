CREATE TABLE hotel_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    image_path VARCHAR(500),
    is_main BOOLEAN DEFAULT FALSE, -- Đánh dấu là ảnh chính
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);


CREATE TABLE room_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT,
    image_path VARCHAR(500),
    is_main BOOLEAN DEFAULT FALSE, -- Ảnh chính của loại phòng
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);
