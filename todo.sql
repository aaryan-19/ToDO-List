--
-- Table structure for table `to_do_tasks`
--
DROP TABLE IF EXISTS `to_do_tasks`;
CREATE TABLE `to_do_tasks` (
  `task_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `task_name` varchar(300) DEFAULT NULL,
  `status` varchar(15) DEFAULT 'Not Completed',
  `category` varchar(15) DEFAULT NULL,
  `date_of_entry` date DEFAULT NULL,
  `date_of_completion` date DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `to_do_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `email_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;