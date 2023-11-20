-- create the table statistics with all the data 
-- CREATE DATABASE statistics_table;
-- USE statistics_table;


-- CREATE TABLE statistics_table (
--     Statistic varchar(50),
--     Year int,
--     Teachers varchar(20),
--     Countries varchar(20),
--     Unit varchar(10),
--     Value decimal(4, 1)
-- );

-- CREATE DATABASE statistics_table;
-- USE statistics_table;

-- CREATE TABLE statistics_data (
--     Countries varchar(50),
--     Statistic varchar(50),
--     Teachers decimal(4, 1),
--     Year int,
--     Unit varchar(50),  -- Change the data type to accommodate the "Unit" field
--     Value decimal(4, 1)
-- );

CREATE DATABASE statistics_table;
USE statistics_table;

CREATE TABLE statistics_data (
    Countries varchar(50),
    Statistic varchar(50),
    Teachers varchar(50),  -- Change data type to decimal(4, 1) or INT if it's an integer
    Year int,
    Unit varchar(10),         -- Change data type to VARCHAR or TEXT if it's a string
    Value decimal(4, 1)
);

