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
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `email_address`, `password`, `security_level`, `date_created`, `date_last_login`, `date_last_password_change`) VALUES
(1, 'Admin', '', 'admin@example.com', '1241e31dde1d9dba781038f7dcb1a869', 1, '2021-11-18 11:39:37', NULL, NULL),
(2, 'Eric', 'Hoang', 'hoanger@oregonstate.edu', 'Password1', 1, '2022-01-18 00:24:25', NULL, NULL),
(3, 'cire', 'goanh', 'egoanh@gmail.com', 'Password1', 0, '2022-01-18 00:24:25', NULL, NULL),
(4, 'dummy1', 'boop', 'dummy1boop@oregonstate.edu', 'Password1', 1, '2022-01-18 00:24:25', NULL, NULL),
(5, 'dummy2', 'boop', 'dummy2boop@oregonstate.edu', 'Password1', 2, '2022-01-18 00:24:25', NULL, NULL),
(6, 'dummy3', 'boop', 'dummy3boop@oregonstate.edu', 'Password1', 2, '2022-01-18 00:24:25', NULL, NULL),
(7, 'dummy4', 'boop', 'dummy4boop@oregonstate.edu', 'Password1', 2, '2022-01-18 00:24:25', NULL, NULL),
(8, 'dummy5', 'boop', 'dummy5boop@oregonstate.edu', 'Password1', 3, '2022-01-18 00:24:25', NULL, NULL);

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
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
