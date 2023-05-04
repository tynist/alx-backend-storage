-- Script creates a stored procedure ComputeAverageScoreForUser 
-- that computes and store the average score for a student.
-- procedure takes 1 input parameter

drop procedure IF EXISTS ComputeAverageScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = users.id
    )
    WHERE id = user_id;
END //

DELIMITER ;
