-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH teacher_assignments AS (
    SELECT teacher_id, COUNT(*) AS num_assignments
    FROM assignments
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
),
max_graded_teacher AS (
    SELECT teacher_id
    FROM teacher_assignments
    ORDER BY num_assignments DESC
    LIMIT 1
)

SELECT COUNT(*) AS grade_A_assignments
FROM assignments
WHERE grade = 'A'
  AND teacher_id = (SELECT teacher_id FROM max_graded_teacher);
