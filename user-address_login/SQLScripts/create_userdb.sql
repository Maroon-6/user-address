DROP DATABASE IF EXISTS `hw1_user`;
CREATE SCHEMA `hw1_user` ;

DROP TABLE IF EXISTS `hw1_user`.`addresses`;
CREATE TABLE `hw1_user`.`addresses` (
  `ID` INT NOT NULL,
  `streetNo` VARCHAR(45) NULL,
  `streetName1` VARCHAR(45) NULL,
  `streetName2` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `region` VARCHAR(45) NULL,
  `CountryCode` INT NULL,
  `postalCode` INT NULL,
  PRIMARY KEY (`ID`)
);

DROP TABLE IF EXISTS `hw1_user`.`users`;
CREATE TABLE `hw1_user`.`users` (
  `ID` INT NOT NULL,
  `nameLast` VARCHAR(45) NULL,
  `nameFirst` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `addressID` INT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE
  # FOREIGN KEY (`addressID`) REFERENCES `hw1_user`.`addresses` (`ID`)
);

# add some data
INSERT INTO `hw1_user`.`addresses`(ID) VALUES(
'11'
);
INSERT INTO `hw1_user`.`addresses`(ID) VALUES(
'22'
);
INSERT INTO `hw1_user`.`addresses`(ID) VALUES(
'33'
);
INSERT INTO `hw1_user`.`addresses`(ID) VALUES(
'44'
);
INSERT INTO `hw1_user`.`addresses`(ID) VALUES(
'55'
);


INSERT INTO `hw1_user`.`users` VALUES(
'1','jean','huang','123@gmail.com','11'
);
INSERT INTO `hw1_user`.`users` VALUES(
'2','jeann','huang','1233@gmail.com','22'
);
INSERT INTO `hw1_user`.`users` VALUES(
'3','jeane','huang','12f3@gmail.com','33'
);
INSERT INTO `hw1_user`.`users` VALUES(
'4','jeanwn','huang','12d33@gmail.com','44'
);
INSERT INTO `hw1_user`.`users` VALUES(
'5','jean','huang','12s3@gmail.com','44'
);
INSERT INTO `hw1_user`.`users` VALUES(
'105167723115783040334','jiaojiao','huang','huangjiaojiao1015@outlook.com','44'
);





