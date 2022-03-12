
--
-- Table structure for table `github_table`
--

DROP TABLE IF EXISTS `github_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `github_table` (
  `Date` datetime DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Stars` int DEFAULT NULL,
  `Forks` int DEFAULT NULL,
  `Open_Issues` int DEFAULT NULL,
  `Closed_Issues` int DEFAULT NULL,
  `Total_Commits` int DEFAULT NULL,
  `Contributors` int DEFAULT NULL,
  `Release_Date` datetime DEFAULT NULL,
  `RL_Days_Ago` int DEFAULT NULL,
  `Language` varchar(50) DEFAULT NULL,
  `Watchers` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=312 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

