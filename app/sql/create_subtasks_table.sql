CREATE TABLE IF NOT EXISTS `subtasks` (
        pid INT,
        user_id INT,
        stid INT NOT NULL AUTO_INCREMENT,
        stname VARCHAR(255),
        stdescription LONGTEXT,
        ststatus VARCHAR(30),
        create_time VARCHAR(20),
        last_modified_time VARCHAR(20),
        completed_time VARCHAR(20),
        PRIMARY KEY (stid)
);
