-- Script ranks the country origins of metal bands
-- based on the number of (non-unique) fans.
-- Output includes the country name and the total number
-- of fans from that country in descending order.

SELECT origin, SUM(nb_fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
