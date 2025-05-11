-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hotel_management
-- ------------------------------------------------------
-- Server version	8.4.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `user_id` (`user_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel_images`
--

DROP TABLE IF EXISTS `hotel_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `hotel_id` int DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `is_main` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`image_id`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `hotel_images_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotels` (`hotel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_images`
--

LOCK TABLES `hotel_images` WRITE;
/*!40000 ALTER TABLE `hotel_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `hotel_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels`
--

DROP TABLE IF EXISTS `hotels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels` (
  `hotel_id` int NOT NULL AUTO_INCREMENT,
  `hotel_name` varchar(50) DEFAULT NULL,
  `address_hotel` varchar(150) DEFAULT NULL,
  `tel` varchar(13) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `descriptions` varchar(1000) DEFAULT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`hotel_id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `hotels_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels`
--

LOCK TABLES `hotels` WRITE;
/*!40000 ALTER TABLE `hotels` DISABLE KEYS */;
INSERT INTO `hotels` VALUES (1,'Swandor Cam Ranh Resort – Ultra All Inclusive','Km 11 Nguyen Tat Thanh Boulevard, Bai Dai Beach, Cam Lam District, Cam Ranh, Khanh Hoa, Vietnam','+842583988000',8.7,'Swandor Cam Ranh Resort – Ultra All Inclusive is a five-star beachfront resort located on Bai Dai Beach. The resort offers 510 modern rooms and suites with private balconies overlooking the ocean. Guests enjoy unlimited dining and drinks under the all-inclusive package, with multiple restaurants and bars on-site. Amenities include several swimming pools, a water park, a full-service spa, and daily entertainment programs for both adults and children. With its pristine beach setting, world-class service, and family-friendly facilities, this resort provides an unforgettable tropical getaway experience.'),(2,'Ana Mandara Cam Ranh','Slot D6A - Zone 2, Cam Ranh Peninsula, Cam Lam District, Khanh Hoa, Vietnam','+842583522222',9,'Ana Mandara Cam Ranh is a luxurious 5-star resort nestled along a tranquil private beach on the Cam Ranh Peninsula. Blending Vietnamese charm with modern comfort, the resort features elegant rooms and beachfront pool villas surrounded by lush landscaping. Guests can indulge in a beachfront infinity pool, holistic spa treatments, and gourmet dining that highlights local flavors. With panoramic ocean views, nature-inspired design, and attentive service, Ana Mandara Cam Ranh offers a serene coastal retreat for travelers seeking relaxation and luxury by the sea.'),(3,'Sheraton Grand Danang Resort & Convention Center','35 Truong Sa Street, Hoa Hai Ward, Ngu Hanh Son District, Da Nang, Vietnam','+842363988999',8.7,'Sheraton Grand Danang Resort & Convention Center is a prestigious five-star hotel situated on Non Nuoc Beach in Da Nang. Boasting Vietnam\'s longest infinity pool overlooking the East Sea, this resort provides an array of leisure facilities including a mini water park for kids, the Shine Spa, and a private beach area. Its spacious rooms and suites feature contemporary decor, plush bedding, and balconies with ocean or garden views. Multiple on-site restaurants serve international cuisine and local specialties. With exceptional service, extensive meeting facilities, and a prime beachfront location, the Sheraton Grand Danang is ideal for both leisure and business travelers.'),(4,'Imperial Hotel & Spa','44 Hang Hanh Street, Hoan Kiem District, Hanoi, Vietnam','+842439335555',9.1,'Imperial Hotel & Spa is an elegant boutique hotel located on a quiet street in Hanoi\'s Old Quarter, just a short walk from Hoan Kiem Lake. This hotel combines classic Vietnamese style with modern amenities. Each room is tastefully furnished with wooden decor, comfortable bedding, and marble bathrooms. Guests can enjoy services like a full-service spa, a rooftop restaurant with city views, and 24-hour concierge. Surrounded by cafes, shops, and cultural sites, the Imperial Hotel & Spa provides exceptional value, warm hospitality, and a convenient location for exploring Hanoi\'s historic charm.'),(5,'HOTEL de LAGOM','30B-C-D Ly Nam De Street, Cua Dong Ward, Hoan Kiem District, Hanoi, Vietnam','+842433133333',9.4,'HOTEL de LAGOM is a newly opened five-star boutique hotel in the heart of Hanoi, blending Scandinavian and French design elements. The hotel\'s name reflects the "Lagom" philosophy of balance and harmony, evident in its stylish yet cozy rooms and suites. Each unit offers modern comforts like a smart flat-screen TV, free high-speed Wi-Fi, premium bedding, and a spa-inspired bathroom. Guests can relax at the rooftop infinity pool and bar, indulge in treatments at the De Lush Spa, or dine at the on-site restaurant serving Vietnamese and international cuisine. With its prime Old Quarter location and personalized service, HOTEL de LAGOM promises a unique and luxurious stay in Hanoi.'),(6,'DeLaSea Ha Long Hotel','A9, Lot 1, Hung Thang Tourist Area, Ha Long City, Quang Ninh, Vietnam','+842033636999',9,'DeLaSea Ha Long Hotel is a contemporary 5-star hotel situated in the Bai Chay area of Ha Long City, offering stunning views of Ha Long Bay. The hotel features elegantly furnished rooms and suites equipped with large windows and modern amenities, some with private balconies overlooking the bay. Guests can enjoy a range of facilities including an indoor swimming pool, a fitness center, and a spa. The on-site restaurant offers local seafood and international dishes. Located near the marina and popular attractions, DeLaSea Ha Long Hotel is an excellent choice for travelers seeking comfort, convenience, and exceptional service during their visit to the UNESCO-listed bay.'),(7,'Legacy Yen Tu - MGallery','Thuong Yen Cong Commune, Uong Bi City, Quang Ninh Province, Vietnam','+842036259888',9,'Legacy Yen Tu - MGallery is a unique luxury resort nestled at the foot of Yen Tu Mountain in Quang Ninh Province. Designed by famed architect Bill Bensley, the resort recreates the ambiance of an ancient Vietnamese village with handcrafted materials and historic details. Its rooms feature imperial-style furnishings and tranquil mountain views. Guests can engage in meditation and yoga sessions, visit the nearby Yen Tu Zen monastery, or unwind at the tranquil spa. The resort offers farm-to-table Vietnamese cuisine in a grand dining hall. With its cultural significance, serene setting, and refined hospitality, Legacy Yen Tu provides an inspiring retreat into Vietnam\'s spiritual heritage.'),(8,'Seashells Phu Quoc Hotel & Spa','1 Vo Thi Sau Street, Duong Dong, Phu Quoc, Kien Giang, Vietnam','+842977300999',9,'Seashells Phu Quoc Hotel & Spa is a modern oceanfront hotel located in the heart of Duong Dong town on Phu Quoc Island. Designed in the shape of a ship, this iconic five-star hotel offers panoramic sea views and is just steps away from the island\'s night market and main attractions. Its bright, spacious rooms come with contemporary furnishings, private balconies, and views of the ocean or town. Guests can lounge by the outdoor infinity pool overlooking the beach, pamper themselves at the full-service spa, or savor fresh seafood at the on-site restaurant. With friendly service and an unbeatable central location, Seashells Phu Quoc is perfect for both leisure and business travelers seeking island luxury.'),(9,'Sailing Club Signature Resort Phu Quoc','Group 6, Duong Bao Hamlet, Duong To, Phu Quoc, Kien Giang, Vietnam','+842973660000',9.4,'Sailing Club Signature Resort Phu Quoc is an exclusive villa resort set amidst tropical gardens near Phu Quoc\'s Long Beach. This 5-star resort offers private pool villas designed in a sleek Scandinavian style, each featuring a spacious living area, fully-equipped kitchen, and a secluded patio with sun loungers. Guests have access to a range of facilities including a gourmet restaurant, a cocktail bar, a fitness center, and a kids\' playground. The resort\'s concierge can arrange island excursions, water sports, or romantic dining experiences. Ideal for families and groups, the tranquil atmosphere and personalized service at Sailing Club Signature Resort ensure a luxurious home-away-from-home island escape.'),(10,'Movenpick Resort Cam Ranh','Plot D12, Cam Hai Dong, Cam Lam District, Khanh Hoa 57615, Vietnam','+842583985888',8.7,'Movenpick Resort Cam Ranh is a family-friendly beachfront resort along Bai Dai Beach, known for its Swiss hospitality and extensive facilities. The resort offers a mix of stylish rooms, suites, and private pool villas, all with breathtaking sea and mountain views. Guests can spend days enjoying the water park with slides, multiple swimming pools, and a private beach, or relaxing at the wellness center offering massages and a Jacuzzi. There are several dining options, including an all-day dining restaurant, a seafood grill, and a fun chocolate hour each afternoon – a Movenpick signature. With a children\'s play zone, tennis courts, and attentive staff, Movenpick Resort Cam Ranh delivers a fun-filled and relaxing stay for guests of all ages.');
/*!40000 ALTER TABLE `hotels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `payment_status` varchar(10) DEFAULT NULL,
  `payment_method` enum('vnpay','momo') DEFAULT NULL,
  `amount` bigint DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `user_id` (`user_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `comment` varchar(200) DEFAULT NULL,
  `hotel_id` int DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `user_id` (`user_id`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`hotel_id`) REFERENCES `hotels` (`hotel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_images`
--

DROP TABLE IF EXISTS `room_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `room_id` int DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `is_main` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`image_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `room_images_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_images`
--

LOCK TABLES `room_images` WRITE;
/*!40000 ALTER TABLE `room_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `room_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `room_id` int NOT NULL,
  `room_type` varchar(35) DEFAULT NULL,
  `availableRooms` int DEFAULT NULL,
  `price` bigint DEFAULT NULL,
  `hotel_id` int DEFAULT NULL,
  PRIMARY KEY (`room_id`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotels` (`hotel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,'Deluxe Sea View Room',8,5000000,1),(2,'Deluxe Front Sea View Room',6,6000000,1),(3,'Deluxe Family Sea View Room',5,8000000,1),(4,'Deluxe Ocean View Room',6,5000000,2),(5,'1-Bedroom Beachfront Pool Villa',4,9000000,2),(6,'2-Bedroom Beachfront Pool Villa',3,10000000,2),(7,'Deluxe King Room with Balcony',10,4000000,3),(8,'Premier Ocean View Room',8,6000000,3),(9,'Executive Suite',5,8000000,3),(10,'Deluxe Room',9,2000000,4),(11,'Executive Room',7,2500000,4),(12,'Imperial Suite',5,4000000,4),(13,'Deluxe Window Room',10,3000000,5),(14,'Premium Balcony Room',8,3500000,5),(15,'Lagom Suite',5,5000000,5),(16,'Deluxe Twin Room',8,2500000,6),(17,'Executive Ocean View Room',6,3500000,6),(18,'Family Suite Ocean View',4,5000000,6),(19,'Superior King Room',10,3000000,7),(20,'Deluxe Twin Room',9,3500000,7),(21,'Executive Suite',5,6000000,7),(22,'Deluxe Double Ocean View',10,2500000,8),(23,'Premier Ocean View Room',9,3500000,8),(24,'Family Suite Sea View',6,5000000,8),(25,'One-Bedroom Pool Villa',5,6000000,9),(26,'Two-Bedroom Pool Villa',5,8000000,9),(27,'Three-Bedroom Pool Villa',5,10000000,9),(28,'Deluxe Sea View Room',10,4500000,10),(29,'Junior Suite Ocean View',8,6000000,10),(30,'Three-Bedroom Pool Villa',4,10000000,10);
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id_service` int NOT NULL,
  `serviceName` varchar(255) DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  PRIMARY KEY (`id_service`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `services_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Free Wi-Fi',1),(2,'Air conditioning',1),(3,'Flat-screen TV',1),(4,'Cable channels',1),(5,'Minibar',1),(6,'Coffee/tea maker',1),(7,'Complimentary bottled water',1),(8,'In-room safe',1),(9,'Private bathroom',1),(10,'Shower',1),(11,'Hair dryer',1),(12,'Slippers',1),(13,'Free toiletries',1),(14,'Desk',1),(15,'Telephone',1),(16,'Wardrobe/Closet',1),(17,'Ironing facilities',1),(18,'Daily housekeeping',1),(19,'24-hour room service',1),(20,'Smoke detector',1),(21,'Balcony/terrace',1),(22,'Ocean view',1),(23,'Satellite TV',1),(24,'Bathrobe',1),(25,'Wake-up service',1),(26,'Soundproofing',1),(27,'Key card access',1),(28,'Free Wi-Fi',2),(29,'Air conditioning',2),(30,'Flat-screen TV',2),(31,'Cable channels',2),(32,'Minibar',2),(33,'Coffee/tea maker',2),(34,'Complimentary bottled water',2),(35,'In-room safe',2),(36,'Private bathroom',2),(37,'Shower',2),(38,'Hair dryer',2),(39,'Slippers',2),(40,'Free toiletries',2),(41,'Desk',2),(42,'Telephone',2),(43,'Wardrobe/Closet',2),(44,'Ironing facilities',2),(45,'Daily housekeeping',2),(46,'24-hour room service',2),(47,'Smoke detector',2),(48,'Balcony/terrace',2),(49,'Ocean view',2),(50,'Satellite TV',2),(51,'Bathrobe',2),(52,'Wake-up service',2),(53,'Soundproofing',2),(54,'Key card access',2),(55,'Free Wi-Fi',3),(56,'Air conditioning',3),(57,'Flat-screen TV',3),(58,'Cable channels',3),(59,'Minibar',3),(60,'Coffee/tea maker',3),(61,'Complimentary bottled water',3),(62,'In-room safe',3),(63,'Private bathroom',3),(64,'Shower',3),(65,'Hair dryer',3),(66,'Slippers',3),(67,'Free toiletries',3),(68,'Desk',3),(69,'Telephone',3),(70,'Wardrobe/Closet',3),(71,'Ironing facilities',3),(72,'Daily housekeeping',3),(73,'24-hour room service',3),(74,'Smoke detector',3),(75,'Balcony/terrace',3),(76,'Ocean view',3),(77,'Satellite TV',3),(78,'Bathrobe',3),(79,'Wake-up service',3),(80,'Soundproofing',3),(81,'Key card access',3),(82,'Free Wi-Fi',4),(83,'Air conditioning',4),(84,'Flat-screen TV',4),(85,'Cable channels',4),(86,'Minibar',4),(87,'Coffee/tea maker',4),(88,'Complimentary bottled water',4),(89,'In-room safe',4),(90,'Private bathroom',4),(91,'Shower',4),(92,'Hair dryer',4),(93,'Slippers',4),(94,'Free toiletries',4),(95,'Desk',4),(96,'Telephone',4),(97,'Wardrobe/Closet',4),(98,'Ironing facilities',4),(99,'Daily housekeeping',4),(100,'24-hour room service',4),(101,'Smoke detector',4),(102,'Balcony/terrace',4),(103,'Ocean view',4),(104,'Private pool',4),(105,'Kitchenette',4),(106,'Living room',4),(107,'Dining area',4),(108,'Satellite TV',4),(109,'Bathrobe',4),(110,'Wake-up service',4),(111,'Soundproofing',4),(112,'Key card access',4),(113,'Free Wi-Fi',5),(114,'Air conditioning',5),(115,'Flat-screen TV',5),(116,'Cable channels',5),(117,'Minibar',5),(118,'Coffee/tea maker',5),(119,'Complimentary bottled water',5),(120,'In-room safe',5),(121,'Private bathroom',5),(122,'Shower',5),(123,'Hair dryer',5),(124,'Slippers',5),(125,'Free toiletries',5),(126,'Desk',5),(127,'Telephone',5),(128,'Wardrobe/Closet',5),(129,'Ironing facilities',5),(130,'Daily housekeeping',5),(131,'24-hour room service',5),(132,'Smoke detector',5),(133,'Balcony/terrace',5),(134,'Ocean view',5),(135,'Private pool',5),(136,'Kitchenette',5),(137,'Living room',5),(138,'Dining area',5),(139,'Satellite TV',5),(140,'Bathrobe',5),(141,'Wake-up service',5),(142,'Soundproofing',5),(143,'Key card access',5),(144,'Free Wi-Fi',6),(145,'Air conditioning',6),(146,'Flat-screen TV',6),(147,'Cable channels',6),(148,'Minibar',6),(149,'Coffee/tea maker',6),(150,'Complimentary bottled water',6),(151,'In-room safe',6),(152,'Private bathroom',6),(153,'Shower',6),(154,'Hair dryer',6),(155,'Slippers',6),(156,'Free toiletries',6),(157,'Desk',6),(158,'Telephone',6),(159,'Wardrobe/Closet',6),(160,'Ironing facilities',6),(161,'Daily housekeeping',6),(162,'24-hour room service',6),(163,'Smoke detector',6),(164,'Balcony/terrace',6),(165,'Ocean view',6),(166,'Satellite TV',6),(167,'Bathrobe',6),(168,'Wake-up service',6),(169,'Soundproofing',6),(170,'Key card access',6),(171,'Free Wi-Fi',7),(172,'Air conditioning',7),(173,'Flat-screen TV',7),(174,'Cable channels',7),(175,'Minibar',7),(176,'Coffee/tea maker',7),(177,'Complimentary bottled water',7),(178,'In-room safe',7),(179,'Private bathroom',7),(180,'Shower',7),(181,'Hair dryer',7),(182,'Slippers',7),(183,'Free toiletries',7),(184,'Desk',7),(185,'Telephone',7),(186,'Wardrobe/Closet',7),(187,'Ironing facilities',7),(188,'Daily housekeeping',7),(189,'24-hour room service',7),(190,'Smoke detector',7),(191,'Balcony/terrace',7),(192,'Ocean view',7),(193,'Seating area',7),(194,'Sofa',7),(195,'Bathtub',7),(196,'Satellite TV',7),(197,'Bathrobe',7),(198,'Wake-up service',7),(199,'Soundproofing',7),(200,'Key card access',7),(201,'Free Wi-Fi',8),(202,'Air conditioning',8),(203,'Flat-screen TV',8),(204,'Cable channels',8),(205,'Minibar',8),(206,'Coffee/tea maker',8),(207,'Complimentary bottled water',8),(208,'In-room safe',8),(209,'Private bathroom',8),(210,'Shower',8),(211,'Hair dryer',8),(212,'Slippers',8),(213,'Free toiletries',8),(214,'Desk',8),(215,'Telephone',8),(216,'Wardrobe/Closet',8),(217,'Ironing facilities',8),(218,'Daily housekeeping',8),(219,'24-hour room service',8),(220,'Smoke detector',8),(221,'Balcony/terrace',8),(222,'Ocean view',8),(223,'Seating area',8),(224,'Sofa',8),(225,'Bathtub',8),(226,'Satellite TV',8),(227,'Bathrobe',8),(228,'Wake-up service',8),(229,'Soundproofing',8),(230,'Key card access',8),(231,'Free Wi-Fi',9),(232,'Air conditioning',9),(233,'Flat-screen TV',9),(234,'Cable channels',9),(235,'Minibar',9),(236,'Coffee/tea maker',9),(237,'Complimentary bottled water',9),(238,'In-room safe',9),(239,'Private bathroom',9),(240,'Shower',9),(241,'Hair dryer',9),(242,'Slippers',9),(243,'Free toiletries',9),(244,'Desk',9),(245,'Telephone',9),(246,'Wardrobe/Closet',9),(247,'Ironing facilities',9),(248,'Daily housekeeping',9),(249,'24-hour room service',9),(250,'Smoke detector',9),(251,'Balcony/terrace',9),(252,'Ocean view',9),(253,'Private pool',9),(254,'Kitchenette',9),(255,'Living room',9),(256,'Dining area',9),(257,'Satellite TV',9),(258,'Bathrobe',9),(259,'Wake-up service',9),(260,'Soundproofing',9),(261,'Key card access',9),(262,'Free Wi-Fi',10),(263,'Air conditioning',10),(264,'Flat-screen TV',10),(265,'Cable channels',10),(266,'Minibar',10),(267,'Coffee/tea maker',10),(268,'Complimentary bottled water',10),(269,'In-room safe',10),(270,'Private bathroom',10),(271,'Shower',10),(272,'Hair dryer',10),(273,'Slippers',10),(274,'Free toiletries',10),(275,'Desk',10),(276,'Telephone',10),(277,'Wardrobe/Closet',10),(278,'Ironing facilities',10),(279,'Daily housekeeping',10),(280,'24-hour room service',10),(281,'Smoke detector',10),(282,'Balcony/terrace',10),(283,'Ocean view',10),(284,'Seating area',10),(285,'Sofa',10),(286,'Bathtub',10),(287,'Private pool',10),(288,'Kitchenette',10),(289,'Living room',10),(290,'Dining area',10),(291,'Satellite TV',10),(292,'Bathrobe',10),(293,'Wake-up service',10),(294,'Soundproofing',10),(295,'Key card access',10),(296,'Free Wi-Fi',11),(297,'Air conditioning',11),(298,'Flat-screen TV',11),(299,'Cable channels',11),(300,'Minibar',11),(301,'Coffee/tea maker',11),(302,'Complimentary bottled water',11),(303,'In-room safe',11),(304,'Private bathroom',11),(305,'Shower',11),(306,'Hair dryer',11),(307,'Slippers',11),(308,'Free toiletries',11),(309,'Desk',11),(310,'Telephone',11),(311,'Wardrobe/Closet',11),(312,'Ironing facilities',11),(313,'Daily housekeeping',11),(314,'24-hour room service',11),(315,'Smoke detector',11),(316,'Balcony/terrace',11),(317,'Ocean view',11),(318,'Seating area',11),(319,'Sofa',11),(320,'Bathtub',11),(321,'Satellite TV',11),(322,'Bathrobe',11),(323,'Wake-up service',11),(324,'Soundproofing',11),(325,'Key card access',11),(326,'Free Wi-Fi',12),(327,'Air conditioning',12),(328,'Flat-screen TV',12),(329,'Cable channels',12),(330,'Minibar',12),(331,'Coffee/tea maker',12),(332,'Complimentary bottled water',12),(333,'In-room safe',12),(334,'Private bathroom',12),(335,'Shower',12),(336,'Hair dryer',12),(337,'Slippers',12),(338,'Free toiletries',12),(339,'Desk',12),(340,'Telephone',12),(341,'Wardrobe/Closet',12),(342,'Ironing facilities',12),(343,'Daily housekeeping',12),(344,'24-hour room service',12),(345,'Smoke detector',12),(346,'Balcony/terrace',12),(347,'Ocean view',12),(348,'Seating area',12),(349,'Sofa',12),(350,'Bathtub',12),(351,'Satellite TV',12),(352,'Bathrobe',12),(353,'Wake-up service',12),(354,'Soundproofing',12),(355,'Key card access',12),(356,'Free Wi-Fi',13),(357,'Air conditioning',13),(358,'Flat-screen TV',13),(359,'Cable channels',13),(360,'Minibar',13),(361,'Coffee/tea maker',13),(362,'Complimentary bottled water',13),(363,'In-room safe',13),(364,'Private bathroom',13),(365,'Shower',13),(366,'Hair dryer',13),(367,'Slippers',13),(368,'Free toiletries',13),(369,'Desk',13),(370,'Telephone',13),(371,'Wardrobe/Closet',13),(372,'Ironing facilities',13),(373,'Daily housekeeping',13),(374,'24-hour room service',13),(375,'Smoke detector',13),(376,'Balcony/terrace',13),(377,'Ocean view',13),(378,'Satellite TV',13),(379,'Bathrobe',13),(380,'Wake-up service',13),(381,'Soundproofing',13),(382,'Key card access',13),(383,'Free Wi-Fi',14),(384,'Air conditioning',14),(385,'Flat-screen TV',14),(386,'Cable channels',14),(387,'Minibar',14),(388,'Coffee/tea maker',14),(389,'Complimentary bottled water',14),(390,'In-room safe',14),(391,'Private bathroom',14),(392,'Shower',14),(393,'Hair dryer',14),(394,'Slippers',14),(395,'Free toiletries',14),(396,'Desk',14),(397,'Telephone',14),(398,'Wardrobe/Closet',14),(399,'Ironing facilities',14),(400,'Daily housekeeping',14),(401,'24-hour room service',14),(402,'Smoke detector',14),(403,'Balcony/terrace',14),(404,'Ocean view',14),(405,'Satellite TV',14),(406,'Bathrobe',14),(407,'Wake-up service',14),(408,'Soundproofing',14),(409,'Key card access',14),(410,'Free Wi-Fi',15),(411,'Air conditioning',15),(412,'Flat-screen TV',15),(413,'Cable channels',15),(414,'Minibar',15),(415,'Coffee/tea maker',15),(416,'Complimentary bottled water',15),(417,'In-room safe',15),(418,'Private bathroom',15),(419,'Shower',15),(420,'Hair dryer',15),(421,'Slippers',15),(422,'Free toiletries',15),(423,'Desk',15),(424,'Telephone',15),(425,'Wardrobe/Closet',15),(426,'Ironing facilities',15),(427,'Daily housekeeping',15),(428,'24-hour room service',15),(429,'Smoke detector',15),(430,'Balcony/terrace',15),(431,'Ocean view',15),(432,'Satellite TV',15),(433,'Bathrobe',15),(434,'Wake-up service',15),(435,'Soundproofing',15),(436,'Key card access',15),(437,'Free Wi-Fi',16),(438,'Air conditioning',16),(439,'Flat-screen TV',16),(440,'Cable channels',16),(441,'Minibar',16),(442,'Coffee/tea maker',16),(443,'Complimentary bottled water',16),(444,'In-room safe',16),(445,'Private bathroom',16),(446,'Shower',16),(447,'Hair dryer',16),(448,'Slippers',16),(449,'Free toiletries',16),(450,'Desk',16),(451,'Telephone',16),(452,'Wardrobe/Closet',16),(453,'Ironing facilities',16),(454,'Daily housekeeping',16),(455,'24-hour room service',16),(456,'Smoke detector',16),(457,'Balcony/terrace',16),(458,'Ocean view',16),(459,'Satellite TV',16),(460,'Bathrobe',16),(461,'Wake-up service',16),(462,'Soundproofing',16),(463,'Key card access',16),(464,'Free Wi-Fi',17),(465,'Air conditioning',17),(466,'Flat-screen TV',17),(467,'Cable channels',17),(468,'Minibar',17),(469,'Coffee/tea maker',17),(470,'Complimentary bottled water',17),(471,'In-room safe',17),(472,'Private bathroom',17),(473,'Shower',17),(474,'Hair dryer',17),(475,'Slippers',17),(476,'Free toiletries',17),(477,'Desk',17),(478,'Telephone',17),(479,'Wardrobe/Closet',17),(480,'Ironing facilities',17),(481,'Daily housekeeping',17),(482,'24-hour room service',17),(483,'Smoke detector',17),(484,'Balcony/terrace',17),(485,'Ocean view',17),(486,'Satellite TV',17),(487,'Bathrobe',17),(488,'Wake-up service',17),(489,'Soundproofing',17),(490,'Key card access',17),(491,'Free Wi-Fi',18),(492,'Air conditioning',18),(493,'Flat-screen TV',18),(494,'Cable channels',18),(495,'Minibar',18),(496,'Coffee/tea maker',18),(497,'Complimentary bottled water',18),(498,'In-room safe',18),(499,'Private bathroom',18),(500,'Shower',18),(501,'Hair dryer',18),(502,'Slippers',18),(503,'Free toiletries',18),(504,'Desk',18),(505,'Telephone',18),(506,'Wardrobe/Closet',18),(507,'Ironing facilities',18),(508,'Daily housekeeping',18),(509,'24-hour room service',18),(510,'Smoke detector',18),(511,'Balcony/terrace',18),(512,'Ocean view',18),(513,'Satellite TV',18),(514,'Bathrobe',18),(515,'Wake-up service',18),(516,'Soundproofing',18),(517,'Key card access',18),(518,'Free Wi-Fi',19),(519,'Air conditioning',19),(520,'Flat-screen TV',19),(521,'Cable channels',19),(522,'Minibar',19),(523,'Coffee/tea maker',19),(524,'Complimentary bottled water',19),(525,'In-room safe',19),(526,'Private bathroom',19),(527,'Shower',19),(528,'Hair dryer',19),(529,'Slippers',19),(530,'Free toiletries',19),(531,'Desk',19),(532,'Telephone',19),(533,'Wardrobe/Closet',19),(534,'Ironing facilities',19),(535,'Daily housekeeping',19),(536,'24-hour room service',19),(537,'Smoke detector',19),(538,'Balcony/terrace',19),(539,'Ocean view',19),(540,'Satellite TV',19),(541,'Bathrobe',19),(542,'Wake-up service',19),(543,'Soundproofing',19),(544,'Key card access',19),(545,'Free Wi-Fi',20),(546,'Air conditioning',20),(547,'Flat-screen TV',20),(548,'Cable channels',20),(549,'Minibar',20),(550,'Coffee/tea maker',20),(551,'Complimentary bottled water',20),(552,'In-room safe',20),(553,'Private bathroom',20),(554,'Shower',20),(555,'Hair dryer',20),(556,'Slippers',20),(557,'Free toiletries',20),(558,'Desk',20),(559,'Telephone',20),(560,'Wardrobe/Closet',20),(561,'Ironing facilities',20),(562,'Daily housekeeping',20),(563,'24-hour room service',20),(564,'Smoke detector',20),(565,'Balcony/terrace',20),(566,'Ocean view',20),(567,'Satellite TV',20),(568,'Bathrobe',20),(569,'Wake-up service',20),(570,'Soundproofing',20),(571,'Key card access',20),(572,'Free Wi-Fi',21),(573,'Air conditioning',21),(574,'Flat-screen TV',21),(575,'Cable channels',21),(576,'Minibar',21),(577,'Coffee/tea maker',21),(578,'Complimentary bottled water',21),(579,'In-room safe',21),(580,'Private bathroom',21),(581,'Shower',21),(582,'Hair dryer',21),(583,'Slippers',21),(584,'Free toiletries',21),(585,'Desk',21),(586,'Telephone',21),(587,'Wardrobe/Closet',21),(588,'Ironing facilities',21),(589,'Daily housekeeping',21),(590,'24-hour room service',21),(591,'Smoke detector',21),(592,'Balcony/terrace',21),(593,'Ocean view',21),(594,'Seating area',21),(595,'Sofa',21),(596,'Bathtub',21),(597,'Satellite TV',21),(598,'Bathrobe',21),(599,'Wake-up service',21),(600,'Soundproofing',21),(601,'Key card access',21),(602,'Free Wi-Fi',22),(603,'Air conditioning',22),(604,'Flat-screen TV',22),(605,'Cable channels',22),(606,'Minibar',22),(607,'Coffee/tea maker',22),(608,'Complimentary bottled water',22),(609,'In-room safe',22),(610,'Private bathroom',22),(611,'Shower',22),(612,'Hair dryer',22),(613,'Slippers',22),(614,'Free toiletries',22),(615,'Desk',22),(616,'Telephone',22),(617,'Wardrobe/Closet',22),(618,'Ironing facilities',22),(619,'Daily housekeeping',22),(620,'24-hour room service',22),(621,'Smoke detector',22),(622,'Balcony/terrace',22),(623,'Ocean view',22),(624,'Seating area',22),(625,'Sofa',22),(626,'Bathtub',22),(627,'Satellite TV',22),(628,'Bathrobe',22),(629,'Wake-up service',22),(630,'Soundproofing',22),(631,'Key card access',22),(632,'Free Wi-Fi',23),(633,'Air conditioning',23),(634,'Flat-screen TV',23),(635,'Cable channels',23),(636,'Minibar',23),(637,'Coffee/tea maker',23),(638,'Complimentary bottled water',23),(639,'In-room safe',23),(640,'Private bathroom',23),(641,'Shower',23),(642,'Hair dryer',23),(643,'Slippers',23),(644,'Free toiletries',23),(645,'Desk',23),(646,'Telephone',23),(647,'Wardrobe/Closet',23),(648,'Ironing facilities',23),(649,'Daily housekeeping',23),(650,'24-hour room service',23),(651,'Smoke detector',23),(652,'Balcony/terrace',23),(653,'Ocean view',23),(654,'Seating area',23),(655,'Sofa',23),(656,'Bathtub',23),(657,'Satellite TV',23),(658,'Bathrobe',23),(659,'Wake-up service',23),(660,'Soundproofing',23),(661,'Key card access',23),(662,'Free Wi-Fi',24),(663,'Air conditioning',24),(664,'Flat-screen TV',24),(665,'Cable channels',24),(666,'Minibar',24),(667,'Coffee/tea maker',24),(668,'Complimentary bottled water',24),(669,'In-room safe',24),(670,'Private bathroom',24),(671,'Shower',24),(672,'Hair dryer',24),(673,'Slippers',24),(674,'Free toiletries',24),(675,'Desk',24),(676,'Telephone',24),(677,'Wardrobe/Closet',24),(678,'Ironing facilities',24),(679,'Daily housekeeping',24),(680,'24-hour room service',24),(681,'Smoke detector',24),(682,'Balcony/terrace',24),(683,'Ocean view',24),(684,'Seating area',24),(685,'Sofa',24),(686,'Bathtub',24),(687,'Satellite TV',24),(688,'Bathrobe',24),(689,'Wake-up service',24),(690,'Soundproofing',24),(691,'Key card access',24),(692,'Free Wi-Fi',25),(693,'Air conditioning',25),(694,'Flat-screen TV',25),(695,'Cable channels',25),(696,'Minibar',25),(697,'Coffee/tea maker',25),(698,'Complimentary bottled water',25),(699,'In-room safe',25),(700,'Private bathroom',25),(701,'Shower',25),(702,'Hair dryer',25),(703,'Slippers',25),(704,'Free toiletries',25),(705,'Desk',25),(706,'Telephone',25),(707,'Wardrobe/Closet',25),(708,'Ironing facilities',25),(709,'Daily housekeeping',25),(710,'24-hour room service',25),(711,'Smoke detector',25),(712,'Balcony/terrace',25),(713,'Satellite TV',25),(714,'Bathrobe',25),(715,'Wake-up service',25),(716,'Soundproofing',25),(717,'Key card access',25),(718,'Free Wi-Fi',26),(719,'Air conditioning',26),(720,'Flat-screen TV',26),(721,'Cable channels',26),(722,'Minibar',26),(723,'Coffee/tea maker',26),(724,'Complimentary bottled water',26),(725,'In-room safe',26),(726,'Private bathroom',26),(727,'Shower',26),(728,'Hair dryer',26),(729,'Slippers',26),(730,'Free toiletries',26),(731,'Desk',26),(732,'Telephone',26),(733,'Wardrobe/Closet',26),(734,'Ironing facilities',26),(735,'Daily housekeeping',26),(736,'24-hour room service',26),(737,'Smoke detector',26),(738,'Balcony/terrace',26),(739,'Satellite TV',26),(740,'Bathrobe',26),(741,'Wake-up service',26),(742,'Soundproofing',26),(743,'Key card access',26),(744,'Free Wi-Fi',27),(745,'Air conditioning',27),(746,'Flat-screen TV',27),(747,'Cable channels',27),(748,'Minibar',27),(749,'Coffee/tea maker',27),(750,'Complimentary bottled water',27),(751,'In-room safe',27),(752,'Private bathroom',27),(753,'Shower',27),(754,'Hair dryer',27),(755,'Slippers',27),(756,'Free toiletries',27),(757,'Desk',27),(758,'Telephone',27),(759,'Wardrobe/Closet',27),(760,'Ironing facilities',27),(761,'Daily housekeeping',27),(762,'24-hour room service',27),(763,'Smoke detector',27),(764,'Balcony/terrace',27),(765,'Satellite TV',27),(766,'Bathrobe',27),(767,'Wake-up service',27),(768,'Soundproofing',27),(769,'Key card access',27),(770,'Free Wi-Fi',28),(771,'Air conditioning',28),(772,'Flat-screen TV',28),(773,'Cable channels',28),(774,'Minibar',28),(775,'Coffee/tea maker',28),(776,'Complimentary bottled water',28),(777,'In-room safe',28),(778,'Private bathroom',28),(779,'Shower',28),(780,'Hair dryer',28),(781,'Slippers',28),(782,'Free toiletries',28),(783,'Desk',28),(784,'Telephone',28),(785,'Wardrobe/Closet',28),(786,'Ironing facilities',28),(787,'Daily housekeeping',28),(788,'24-hour room service',28),(789,'Smoke detector',28),(790,'Balcony/terrace',28),(791,'Ocean view',28),(792,'Satellite TV',28),(793,'Bathrobe',28),(794,'Wake-up service',28),(795,'Soundproofing',28),(796,'Key card access',28),(797,'Free Wi-Fi',29),(798,'Air conditioning',29),(799,'Flat-screen TV',29),(800,'Cable channels',29),(801,'Minibar',29),(802,'Coffee/tea maker',29),(803,'Complimentary bottled water',29),(804,'In-room safe',29),(805,'Private bathroom',29),(806,'Shower',29),(807,'Hair dryer',29),(808,'Slippers',29),(809,'Free toiletries',29),(810,'Desk',29),(811,'Telephone',29),(812,'Wardrobe/Closet',29),(813,'Ironing facilities',29),(814,'Daily housekeeping',29),(815,'24-hour room service',29),(816,'Smoke detector',29),(817,'Balcony/terrace',29),(818,'Ocean view',29),(819,'Satellite TV',29),(820,'Bathrobe',29),(821,'Wake-up service',29),(822,'Soundproofing',29),(823,'Key card access',29),(824,'Free Wi-Fi',30),(825,'Air conditioning',30),(826,'Flat-screen TV',30),(827,'Cable channels',30),(828,'Minibar',30),(829,'Coffee/tea maker',30),(830,'Complimentary bottled water',30),(831,'In-room safe',30),(832,'Private bathroom',30),(833,'Shower',30),(834,'Hair dryer',30),(835,'Slippers',30),(836,'Free toiletries',30),(837,'Desk',30),(838,'Telephone',30),(839,'Wardrobe/Closet',30),(840,'Ironing facilities',30),(841,'Daily housekeeping',30),(842,'24-hour room service',30),(843,'Smoke detector',30),(844,'Balcony/terrace',30),(845,'Ocean view',30),(846,'Seating area',30),(847,'Sofa',30),(848,'Bathtub',30),(849,'Private pool',30),(850,'Kitchenette',30),(851,'Living room',30),(852,'Dining area',30),(853,'Satellite TV',30),(854,'Bathrobe',30),(855,'Wake-up service',30),(856,'Soundproofing',30),(857,'Key card access',30);
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-29 16:06:19
