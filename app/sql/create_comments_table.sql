CREATE TABLE IF NOT EXISTS `comments` (
        stid INT,
        user_id INT,
        cmid INT NOT NULL AUTO_INCREMENT,
        comment LONGTEXT,
        create_time VARCHAR(20),
        last_modified_time VARCHAR(20),
        PRIMARY KEY (cmid)
);
