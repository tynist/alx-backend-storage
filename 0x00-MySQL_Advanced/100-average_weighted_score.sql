-- script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
-- Procedure ComputeAverageScoreForUser is taking 1 input.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_score FLOAT;
    
    SELECT SUM(corrections.score * projects.weight) INTO total_score, SUM(projects.weight) INTO total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    SET avg_score = total_score / total_weight;
    
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END//

DELIMITER ;
