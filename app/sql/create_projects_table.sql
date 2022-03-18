CREATE TABLE IF NOT EXISTS `projects` (
	pid INT AUTO_INCREMENT,
	user_id INT,
	pname VARCHAR(255),
	pdescription LONGTEXT,
	pstatus VARCHAR(30),
	create_time VARCHAR(20),
	last_modified_time VARCHAR(20),
	completed_time VARCHAR(20),
	PRIMARY KEY (pid)
);
