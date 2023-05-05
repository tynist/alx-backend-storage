-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and stores the average weighted score for all students

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;

    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE average_score FLOAT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN user_cursor;

    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        SET total_weighted_score = 0;
        SET total_weight = 0;

        SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;

        SELECT SUM(projects.weight) INTO total_weight
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;

        IF total_weight = 0 THEN
            SET average_score = 0;
        ELSE
            SET average_score = total_weighted_score / total_weight;
        END IF;

        UPDATE users SET average_score = average_score WHERE id = user_id;
    END LOOP;

    CLOSE user_cursor;
END $$
DELIMITER ;
