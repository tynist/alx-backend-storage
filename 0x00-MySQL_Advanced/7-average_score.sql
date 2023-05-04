-- Script creates a stored procedure ComputeAverageScoreForUser that computes and
-- store the average score for a student. Note: An average score can be a decimal.
-- procedure takes 1 input parameter user_id and updates the average_score
-- column for the user with the given ID in the users table.

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = user_id
    )
    WHERE id = user_id;
END //

DELIMITER ;
