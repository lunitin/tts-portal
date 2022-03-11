-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 18, 2021 at 07:42 PM
-- Server version: 10.0.34-MariaDB
-- PHP Version: 7.1.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tts_portal`
--
CREATE DATABASE IF NOT EXISTS `tts_portal` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `tts_portal`;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `first_name` varchar(60) NOT NULL,
  `last_name` varchar(60) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `security_level` int(2) NOT NULL DEFAULT 0,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_last_login` datetime DEFAULT NULL,
  `date_last_password_change` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `access`
--
DROP TABLE IF EXISTS `access`;

CREATE TABLE `access` (
  `access_id` int(10) UNSIGNED NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `coverage_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `coverage`
--
DROP TABLE IF EXISTS `coverage`;

CREATE TABLE `coverage` (
  `coverage_id` int(10) UNSIGNED NOT NULL,
  `coverage_name` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `region`
--
DROP TABLE IF EXISTS `region`;

CREATE TABLE `region` (
  `region_id` int(10) UNSIGNED NOT NULL,
  `coverage_id` int(10) UNSIGNED DEFAULT NULL,
  `region_name` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `signals`
-- 
DROP TABLE IF EXISTS `signals`;

CREATE TABLE `signals` (
  `signal_id` int(10) UNSIGNED NOT NULL,
  `region_id` int(10) UNSIGNED NOT NULL,
  `SignalID` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `vehicle`
--
DROP TABLE IF EXISTS `vehicle`;

CREATE TABLE `vehicle` (
  `vehicledata_id` int(10) UNSIGNED NOT NULL,
  `vehID` varchar(64) NOT NULL,
  `Delay` double(7,3) NOT NULL,
  `RedArrival` char(3) DEFAULT NULL,
  `SplitFailure` char(3) DEFAULT NULL,
  `SignalID` int(10) UNSIGNED NOT NULL,
  `ApproachDirection` char(10) NOT NULL,
  `TravelDirection` char(8) NOT NULL,
  `ETT` double(7,3) NOT NULL,
  `TravelTime` double(7,3) NOT NULL,
  `ExitStatus` char(6) DEFAULT NULL,
  `Day` int(10) NOT NULL,
  `EntryTime` datetime NOT NULL,
  `ExitTime` datetime NOT NULL,
  `Stops` int(10) DEFAULT NULL,
  `Uturn` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `email_address`, `password`, `security_level`, `date_created`, `date_last_login`, `date_last_password_change`) VALUES
(1, 'Admin', 'Test', 'admin@example.com', 'pbkdf2:sha256:310000$rsUk9ZZNwCWVJzYpx9fF5pueJReAmauubDNLvgZAyWbEB640nKkwbqGyqSOMNQ2soZGcG0raFTBm9zMpZXVOSbHD3NvEkYzKhhD2SmIbbMRayH3Z2fOUIIkAeYBio92B$48f8e075fbad9537ea964d7a01e016b3be78f2690d419eacf3235737ac59658e', 1, '2022-02-23 04:25:13', NULL, '2022-02-23 04:25:13' );
INSERT INTO `coverage` (`coverage_id`, `coverage_name`) VALUES (1,'District 1'),(2, 'District 2'),(3, 'District 3'),(4, 'District 4'),(5, 'District 5'),(6, 'District 6');
INSERT INTO `region` (`region_id`, `coverage_id`, `region_name`) VALUES (1, 5, 'IndianRIver'), (2, 5, 'Stlucie'),(3, 5, 'Palm Beach'),(4, 5, 'District 4'),(5, 5, 'Broward');
INSERT INTO `signals` (`signal_id`, `region_id`, `SignalID`) VALUES (1, 5, 1037), (2, 5, 1113),(3, 5, 3084);
--
-- INSERT INTO `coverage` (`coverage_id`, `coverage_name`, `signal_id`) VALUES ()
--
-- Indexes for dumped tables
--
--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email_address` (`email_address`);

--
-- Indexes for table `access`
--
ALTER TABLE `access`
  ADD PRIMARY KEY (`access_id`),
  ADD KEY `FK_Users` (`user_id`),
  ADD KEY `FK_Coverage` (`coverage_id`);

--
-- Indexes for table `coverage`
--
ALTER TABLE `coverage`
  ADD PRIMARY KEY (`coverage_id`);

--
-- Indexes for table `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`region_id`),
  ADD KEY `FK_coverage` (`coverage_id`);

--
-- Indexes for table `signals`
--
ALTER TABLE `signals`
  ADD PRIMARY KEY (`signal_id`),
  ADD UNIQUE KEY `SignalID` (`SignalID`),
  ADD KEY `FK_Region` (`region_id`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicledata_id`),
  ADD UNIQUE KEY `SignalID` (`SignalID`),
  ADD KEY `FK_SignalVeh` (`SignalID`);

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

--
-- AUTO_INCREMENT for table `access`
--
ALTER TABLE `access`
  MODIFY `access_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

--
-- AUTO_INCREMENT for table `coverage`
--
ALTER TABLE `coverage`
  MODIFY `coverage_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

--
-- AUTO_INCREMENT for table `region`
--
ALTER TABLE `region`
  MODIFY `region_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

--
-- AUTO_INCREMENT for table `signals`
--
ALTER TABLE `signals`
  MODIFY `signal_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;
--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicledata_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

--
-- Constraints for table `access`
--
ALTER TABLE `access`
  ADD CONSTRAINT `FK_CoverageAccess` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`coverage_id`),
  ADD CONSTRAINT `FK_UserAccess` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

--
-- Constraints for table `region`
--
ALTER TABLE `region`
  ADD CONSTRAINT `FK_CoverageRegion` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`coverage_id`);
COMMIT;

--
-- Constraints for table `signals`
--
ALTER TABLE `signals`
  ADD CONSTRAINT `FK_SignalRegion` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`);
COMMIT;

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `FK_VehSignal` FOREIGN KEY (`SignalID`) REFERENCES `signals` (`SignalID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
