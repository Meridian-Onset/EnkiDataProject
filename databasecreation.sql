CREATE TABLE atl16_10_2018(
	GranuleID INT AUTO_INCREMENT PRIMARY KEY,
    Latitude INT NOT NULL,
	Longitude INT,
	asr_obs INT,
    aerosol_frac FLOAT,
	asr FLOAT,
    cloud_aerosol_obs INT,
    cloud_frac FLOAT,
    column_od FLOAT,
	grnd_detect FLOAT,
	tcod_obs INT,
    datekey INT FOREIGN KEY REFERENCES timedata(Id) DEFAULT 1
    );
    
    CREATE TABLE atl16_11_2018(
	GranuleID INT AUTO_INCREMENT PRIMARY KEY,
    Latitude INT NOT NULL,
	Longitude INT,
	asr_obs INT,
    aerosol_frac FLOAT,
	asr FLOAT,
    cloud_aerosol_obs INT,
    cloud_frac FLOAT,
    column_od FLOAT,
	grnd_detect FLOAT,
	tcod_obs INT,
    datekey INT FOREIGN KEY DEFAULT 2);

CREATE TABLE timedata(
	Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    occured DATE):

SELECT * FROM atl16_11_2018;
SELECT * FROM atl16_10_2018;PREPARE stmt FROM 'INSERT INTO `nasahost`.`atl16_10_2018` (`cloud_frac`,`asr`,`grnd_detect`,`cloud_aerosol_obs`,`GranuleID`,`Longitude`,`aerosol_frac`,`Latitude`,`tcod_obs`,`column_od`,`asr_obs`) VALUES(?,?,?,?,?,?,?,?,?,?,?)';
DEALLOCATE PREPARE stmt;

SELECT * FROM atl16_10_2018
WHERE Latitude = 44 AND 
Longitude BETWEEN 44 AND 60; 