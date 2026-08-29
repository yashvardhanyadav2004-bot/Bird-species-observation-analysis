USE bird_species_analysis;
DESCRIBE bird_observations;
-- Q1. Total number of bird observations kitne hain?--
SELECT COUNT(*) AS Total_Records
FROM bird_observations;
SELECT *
FROM bird_observations
LIMIT 10;

-- Q2. Total unique bird species kitni hain?--
SELECT COUNT(DISTINCT Scientific_Name) AS Unique_Species
FROM bird_observations;

-- Q3. Har habitat/location type mein kitni observations hain?--
SELECT
    Location_Type,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Location_Type
ORDER BY Observation_Count DESC;

-- Q4. Kaunse bird species sabse zyada observe hue?--
SELECT
    Common_Name,	
    COUNT(*) AS Observation_Count
FROM bird_observations
WHERE Common_Name IS NOT NULL
GROUP BY Common_Name
ORDER BY Observation_Count DESC
LIMIT 10;

-- Q5. Year-wise bird observations ka trend kya hai?--
SELECT
    Year,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Year
ORDER BY Year;

-- Q6. Kaunse plots mein sabse zyada bird observations hain?--
SELECT
    Plot_Name,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Plot_Name
ORDER BY Observation_Count DESC
LIMIT 10;

-- Q7. Kaunsa observation method sabse commonly used hai?--
SELECT
    ID_Method,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY ID_Method
ORDER BY Observation_Count DESC;

-- Q8. Male/Female/Undetermined observations ka distribution kya hai?--
SELECT
    Sex,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Sex
ORDER BY Observation_Count DESC;

-- Q9. Temperature ke according bird observations kaise vary karte hain?--
SELECT
    Temperature,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Temperature
ORDER BY Temperature;

-- Q10. Humidity ke according observations ka distribution kya hai?--
SELECT
    Humidity,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Humidity
ORDER BY Humidity;

-- Q11. Flyover observations kitni hain?--
SELECT
    Flyover_Observed,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Flyover_Observed
ORDER BY Observation_Count DESC;
SELECT
    COUNT(*) AS Flyover_Observations
FROM bird_observations
WHERE Flyover_Observed = TRUE;

-- Q12. Kaunse species sabse zyada first-three-minute count mein observe hue?--
SELECT
    Common_Name,
    SUM(Initial_Three_Min_Cnt) AS Total_Three_Min_Count
FROM bird_observations
GROUP BY Common_Name
ORDER BY Total_Three_Min_Count DESC
LIMIT 10;

-- Q13. Kaunse observers sabse zyada observations record karte hain?--
SELECT
    Observer,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Observer
ORDER BY Observation_Count DESC;

-- Q14. Different visits par observations kaise change hoti hain?--
SELECT
    PIF_Watchlist_Status,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Scientific_Name) AS Unique_Species
FROM bird_observations
GROUP BY PIF_Watchlist_Status;

-- Q15. Watchlist par kitni observations/species hain?--
SELECT
    Visit,
    COUNT(*) AS Observation_Count
FROM bird_observations
GROUP BY Visit
ORDER BY Visit;
SELECT
    COUNT(DISTINCT Scientific_Name) AS Watchlist_Species
FROM bird_observations
WHERE PIF_Watchlist_Status = TRUE;

-- Q16. Regional stewardship status ka distribution kya hai?--
SELECT
    Regional_Stewardship_Status,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Scientific_Name) AS Unique_Species
FROM bird_observations
GROUP BY Regional_Stewardship_Status
ORDER BY Observation_Count DESC;