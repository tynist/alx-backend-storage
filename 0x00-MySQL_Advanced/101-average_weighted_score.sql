-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and stores the average weighted score for all students

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS Us, (
    SELECT Us.id, SUM(score * weight) / SUM(weight) AS weight_avg 
    FROM users AS Us
    JOIN corrections as Cor ON Us.id = Correct.user_id 
    JOIN projects AS Proj ON Correct.project_id = Proj.id 
    GROUP BY Us.id
  ) AS WeighA
  SET Us.average_score = WeighA.weight_avg 
  WHERE Us.id = WeighA.id;
END;

DELIMITER ;
