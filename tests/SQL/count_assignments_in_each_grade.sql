SELECT grade, COUNT(*) AS assignment_count
FROM assignments
GROUP BY grade
ORDER BY grade;
