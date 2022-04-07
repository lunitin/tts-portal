-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tts_portal
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB-1:10.6.5+maria~focal

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access`
--

DROP TABLE IF EXISTS `access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access` (
  `access_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `coverage_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access`
--

LOCK TABLES `access` WRITE;
/*!40000 ALTER TABLE `access` DISABLE KEYS */;
/*!40000 ALTER TABLE `access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coverage`
--

DROP TABLE IF EXISTS `coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coverage` (
  `coverage_id` int(10) unsigned NOT NULL,
  `coverage_name` varchar(24) NOT NULL,
  `signal_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coverage`
--

LOCK TABLES `coverage` WRITE;
/*!40000 ALTER TABLE `coverage` DISABLE KEYS */;
/*!40000 ALTER TABLE `coverage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signals`
--

DROP TABLE IF EXISTS `signals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signals` (
  `signal_id` int(10) unsigned NOT NULL,
  `signal_name` varchar(24) NOT NULL,
  `signal_number` int(10) unsigned NOT NULL,
  `vehicledata_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signals`
--

LOCK TABLES `signals` WRITE;
/*!40000 ALTER TABLE `signals` DISABLE KEYS */;
/*!40000 ALTER TABLE `signals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL,
  `first_name` varchar(60) NOT NULL,
  `last_name` varchar(60) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `security_level` int(2) NOT NULL DEFAULT 0,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_last_login` datetime DEFAULT NULL,
  `date_last_password_change` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Admin','','admin@example.com','1241e31dde1d9dba781038f7dcb1a869',1,'2021-11-18 11:39:37',NULL,NULL),(2,'Eric','Hoang','hoanger@oregonstate.edu','Password1',1,'2022-01-18 00:24:25',NULL,NULL),(3,'cire','goanh','egoanh@gmail.com','Password1',0,'2022-01-18 00:24:25',NULL,NULL),(4,'dummy1','boop','dummy1boop@oregonstate.edu','Password1',1,'2022-01-18 00:24:25',NULL,NULL),(5,'dummy2','boop','dummy2boop@oregonstate.edu','Password1',2,'2022-01-18 00:24:25',NULL,NULL),(6,'dummy3','boop','dummy3boop@oregonstate.edu','Password1',2,'2022-01-18 00:24:25',NULL,NULL),(7,'dummy4','boop','dummy4boop@oregonstate.edu','Password1',2,'2022-01-18 00:24:25',NULL,NULL),(8,'dummy5','boop','dummy5boop@oregonstate.edu','Password1',3,'2022-01-18 00:24:25',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle` (
  `vehicledata_id` int(10) unsigned NOT NULL,
  `vehID` varchar(64) NOT NULL,
  `Delay` double(7,3) NOT NULL,
  `RedArrival` char(3) DEFAULT NULL,
  `SplitFailure` char(3) DEFAULT NULL,
  `SignalID` int(4) NOT NULL,
  `ApproachDirection` char(10) NOT NULL,
  `TravelDirection` char(8) NOT NULL,
  `ETT` double(7,3) NOT NULL,
  `TravelTime` double(7,3) NOT NULL,
  `ExitStatus` char(6) DEFAULT NULL,
  `Day` int(3) NOT NULL,
  `EntryTime` datetime NOT NULL,
  `ExitTime` datetime NOT NULL,
  `Stops` int(3) DEFAULT NULL,
  `Uturn` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-07  9:43:24
