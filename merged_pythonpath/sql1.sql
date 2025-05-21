-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.27-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.4.0.6659
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for loreal
CREATE DATABASE IF NOT EXISTS `loreal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `loreal`;

-- Dumping structure for table loreal.tbl_selection_logs
CREATE TABLE IF NOT EXISTS `tbl_selection_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_name` text DEFAULT NULL,
  `timeperiod` varchar(200) DEFAULT NULL,
  `timeperiod_data` longtext DEFAULT NULL,
  `market` longtext DEFAULT NULL,
  `category` longtext DEFAULT NULL,
  `sub_category` longtext DEFAULT NULL,
  `division` longtext DEFAULT NULL,
  `brand` longtext DEFAULT NULL,
  `platform` longtext DEFAULT NULL,
  `language` varchar(200) DEFAULT NULL,
  `output_file` varchar(200) DEFAULT NULL,
  `create_flag` varchar(200) DEFAULT '0',
  `create_date` timestamp NULL DEFAULT current_timestamp(),
  `status` smallint(6) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
