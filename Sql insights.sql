create database job_data;
use job_data;
select * from naukri_jobs;
ALTER TABLE naukri_jobs
ADD COLUMN job_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

select * from naukri_jobs;

-- Location wise job
SELECT Location, COUNT(*) AS Job_Count
FROM naukri_jobs
GROUP BY Location
ORDER BY Job_Count DESC;

select location ,count(*) as job_count from
naukri_jobs 
group by location
order by job_count desc;

-- Experience requirement
SELECT Experience, COUNT(*) AS Count
FROM naukri_jobs
GROUP BY Experience
ORDER BY Count DESC;

-- salary disclosure condition
SELECT Salary_Disclosed, COUNT(*) 
FROM naukri_jobs
GROUP BY Salary_Disclosed;

select skills from naukri_jobs;

-- industry type breakdown
SELECT Industry_type, COUNT(*) AS Jobs
FROM naukri_jobs
GROUP BY Industry_type
ORDER BY Jobs DESC;

select * from naukri_jobs;
describe naukri_jobs;

ALTER TABLE naukri_jobs CHANGE `Industry type` Industry_Type VARCHAR(255);

select skills from naukri_jobs;

-- most skiils appear
WITH RECURSIVE split_skills AS (
    SELECT
        job_id,
        TRIM(SUBSTRING_INDEX(Skills, ',', 1)) AS skill,
        SUBSTRING(Skills, LENGTH(SUBSTRING_INDEX(Skills, ',', 1)) + 2) AS remaining
    FROM naukri_jobs
    
    UNION ALL
    
    SELECT
        job_id,
        TRIM(SUBSTRING_INDEX(remaining, ',', 1)) AS skill,
        SUBSTRING(remaining, LENGTH(SUBSTRING_INDEX(remaining, ',', 1)) + 2)
    FROM split_skills
    WHERE remaining <> ''
)

SELECT 
    LOWER(skill) AS skill,
    COUNT(*) AS frequency
FROM split_skills
WHERE skill <> ''
GROUP BY LOWER(skill)
ORDER BY frequency DESC
LIMIT 20;

-- fresh jobs
SELECT COUNT(*) AS Fresh_Jobs
FROM naukri_jobs
WHERE Posted_Days_Ago <= 3;

-- weekly jobs
SELECT COUNT(*) AS Week_Jobs
FROM naukri_jobs
WHERE Posted_Days_Ago <= 7;

-- avg job posting days
SELECT AVG(Posted_Days_Ago) AS Avg_Posted_Age
FROM naukri_jobs;

SELECT 
   CASE 
      WHEN Posted_Days_Ago <= 3 THEN '0-3 Days'
      WHEN Posted_Days_Ago <= 7 THEN '4-7 Days'
      WHEN Posted_Days_Ago <= 15 THEN '8-15 Days'
      ELSE '15+ Days'
   END AS Posting_Bucket,
   COUNT(*) AS Job_Count
FROM naukri_jobs
GROUP BY Posting_Bucket
ORDER BY Job_Count DESC;

-- top hiring companies
SELECT Company, COUNT(*) AS Job_Count
FROM naukri_jobs
GROUP BY Company
ORDER BY Job_Count DESC
LIMIT 10;








