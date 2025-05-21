-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bcs_sales_tracker
-- ------------------------------------------------------
-- Server version	5.5.68-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES latin1 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'bcs_sales_tracker'
--

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$216000$1CRLsThqcRdl$5buL2izwwjRWXbV8+52DtJDPrtJ5wxUe+cNJeT8msJE=','2023-07-31 10:06:21.623352',1,'pranit','pranit','dudhane','pranit.dudhane@brand-scapes.com',1,1,'2023-07-31 08:28:39.959343'),(3,'pbkdf2_sha256$216000$zN7wvRb8vMq7$ZpB3QwKMmuSW5v/a8NW3WHBzFKLcMkm/d/9F2sKq/gw=','2023-07-31 10:06:54.998295',0,'test','','','',1,1,'2023-07-31 10:06:01.346266'),(4,'pbkdf2_sha256$216000$3IYykVNiANox$9GT3HioNFp0/RwF5FIFNGIkX+v1EwhBCGxHDGHMAXxI=',NULL,1,'demo','','','demo@demo.com',1,1,'2023-09-13 13:01:15.794575'),(5,'pbkdf2_sha256$216000$esh5lEjtCDm6$gixradSWYpYkR8bIOntSblvMQmggr2vY33STjY9X0zg=','2024-09-05 10:45:58.138061',1,'admin','','','admin@admin.com',1,1,'2024-04-02 15:06:54.071571'),(6,'pbkdf2_sha256$216000$iloXeqbRLp7L$0yqGGk25tg7j5J5dhjFNStLwMIBsIlJUWslJQM2i02A=','2024-06-12 07:51:29.426792',1,'Lalatendu','','','lalatendu.mishra@brand-scapes.com',1,1,'2024-04-24 06:39:05.386940'),(7,'pbkdf2_sha256$216000$jkESUvHeMESC$w8WFimI0b+2/XLVVMMogfApVwCcR/DrzQo66bgauBUs=','2024-04-24 07:59:40.400826',1,'Satyendra','','','satyendra.singh@brand-scapes.com',1,1,'2024-04-24 06:39:41.105019'),(8,'pbkdf2_sha256$216000$46tPaEbvin57$fmUrO9EA2YsAjtzANnBmwI+/cVcKVNt6xa9e8CJpWw8=',NULL,1,'Vilas','','','vilas.kirve@brand-scapes.com',1,1,'2024-04-24 06:40:17.511061'),(9,'pbkdf2_sha256$216000$J3cVaHkEEGdp$pvT2LApLrTLyyOv4W/vMUBATNiRnQsqCCbL4fdG6m54=','2024-08-30 09:09:39.615514',1,'Mihir','','','mihir.pawar@brand-scapes.com',1,1,'2024-04-24 06:40:52.969889'),(10,'pbkdf2_sha256$216000$C3qrrQbuq8dQ$l9dSzzObuKmSbd/DxhqKDjPp9gXWucEIz4ZMpv0HPII=',NULL,1,'harshal','','','harshal.phansekar@brand-scapes.com',1,1,'2024-04-24 06:41:59.482823'),(11,'pbkdf2_sha256$216000$7L1pdfjDQ1Qm$/RQGEQOgvgXSfcMXSILxX51CCbIUly9cO4WXc2n/x2s=','2024-09-05 06:53:36.845576',0,'Sales','','','sales@brand-scapes.com',0,1,'2024-04-25 13:10:44.000000'),(12,'pbkdf2_sha256$216000$xzQPA6WtnEn3$Ho2DimdO8Gt2g98JFyFVYSLN23wkm42LZOKV0dftLs4=','2024-08-15 02:50:12.637282',0,'Promise','Promise','','promise.chen@shiseido.com.tw',0,1,'2024-07-29 08:00:40.000000'),(13,'pbkdf2_sha256$216000$w69aCvbfsAkf$MrDmuFkcWlI3+pVBLGYccMTRVu6tW8FMefZzGpM8JXI=','2024-08-14 09:21:17.121445',0,'Yunjin','Yunjin','','yunjin.park@shiseido.co.kr',0,1,'2024-07-29 08:12:31.000000'),(14,'pbkdf2_sha256$216000$1zF0YEVIDd76$M/W3AlWlXwZZWiojOaUEf9S6Y1RimKbgQScBUq922Qs=','2024-08-28 04:44:23.307250',0,'Duangkamol','Duangkamol','','duangkamol.sereeyothin@shiseido.co.th',0,1,'2024-07-29 08:13:16.000000'),(15,'pbkdf2_sha256$216000$ZyAPde4aArNk$A8CagI9X1Jb7qI6r6s5svJU15XvG3oQu1mpNxBx/ypI=','2024-08-16 02:34:27.234453',0,'Steffi','Steffi','','steffi.wong@sapac.shiseido.com',0,1,'2024-07-29 08:14:01.000000'),(16,'pbkdf2_sha256$216000$bqYn9H4Jza2i$NNNb3JkpozHFMy0JRcJmMgFgORI28tLpTHasZPrO9pc=','2024-08-14 01:57:37.237027',0,'Andrew','Andrew','','andrew.chua@sapac.shiseido.com',0,1,'2024-07-29 08:14:51.000000'),(17,'pbkdf2_sha256$216000$Dpt3ngkz9aTc$oBtpNIQBqARg3lm8rMoumuTmGMHavNVFvTqsXCRAnN8=','2024-07-29 08:17:09.210817',0,'Zulaikha','Zulaikha','','zulaikha.rahim@sapac.shiseido.com',0,1,'2024-07-29 08:15:39.000000'),(18,'pbkdf2_sha256$216000$538swDmR09Ir$2cJKPZyPY+VNURv4LgnISSyqdQxmJtmBNlZ8DIOXP+U=','2024-08-15 01:27:05.705368',0,'Pamela','Pamela','','pamela.koh@sapac.shiseido.com',0,1,'2024-08-12 10:15:29.000000'),(20,'pbkdf2_sha256$216000$iyIu3u2FGci4$x0PHqGYkYDs0VnE0xxB9zwNSaKT9hBNtLucwTo1LXUk=','2024-08-19 09:15:49.363244',0,'nicole','nicole','','nicole.tan@sapac.shiseido.com',0,1,'2024-08-19 09:15:10.000000'),(21,'pbkdf2_sha256$216000$hq8wCEaA3xYo$lCNSU+ZncQm53GhX9Iid3YcyeBkDojLk2ZfS/B5XOFg=','2024-08-23 05:23:50.999633',0,'sauleng','sauleng','','sauleng.tham@sapac.shiseido.com',0,1,'2024-08-23 05:22:21.000000'),(22,'pbkdf2_sha256$216000$sNAVHdFIYVxX$WVnk+nZvSkus45OiPI112Pi/MBvu0ZTZvzxGNiYMcHM=','2024-08-23 05:24:17.205038',0,'sharron','sharron','','sharron.tan@sapac.shiseido.com',0,1,'2024-08-23 05:23:01.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'bcs_sales_tracker'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-05 11:51:01
