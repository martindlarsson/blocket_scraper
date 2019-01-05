.headers ON
.mode csv
.output blocket_data_20181222.csv

SELECT
    brand
    ,model
    ,model_year
    ,gear
    ,fuel
    ,CASE
        WHEN milage BETWEEN 0 AND 999 THEN '0-999'
        WHEN milage BETWEEN 1000 AND 1999 THEN '1000-1999'
        WHEN milage BETWEEN 2000 AND 2999 THEN '2000-2999'
        WHEN milage BETWEEN 3000 AND 3999 THEN '3000-3999'
        WHEN milage BETWEEN 4000 AND 4999 THEN '4000-4999'
        WHEN milage BETWEEN 5000 AND 5999 THEN '5000-5999'
        WHEN milage BETWEEN 6000 AND 6999 THEN '6000-6999'
        WHEN milage BETWEEN 7000 AND 7999 THEN '7000-7999'
        WHEN milage BETWEEN 8000 AND 8999 THEN '8000-8999'
        WHEN milage BETWEEN 9000 AND 9999 THEN '9000-9999'
        -- 10000 +
        WHEN milage BETWEEN 10000 AND 10999 THEN '10000-10999'
        WHEN milage BETWEEN 11000 AND 11999 THEN '11000-11999'
        WHEN milage BETWEEN 12000 AND 12999 THEN '12000-12999'
        WHEN milage BETWEEN 13000 AND 13999 THEN '13000-13999'
        WHEN milage BETWEEN 14000 AND 14999 THEN '14000-14999'
        WHEN milage BETWEEN 15000 AND 15999 THEN '15000-15999'
        WHEN milage BETWEEN 16000 AND 16999 THEN '16000-16999'
        WHEN milage BETWEEN 17000 AND 17999 THEN '17000-17999'
        WHEN milage BETWEEN 18000 AND 18999 THEN '18000-18999'
        WHEN milage BETWEEN 19000 AND 19999 THEN '19000-19999'
        -- 20000 +
        WHEN milage BETWEEN 20000 AND 20999 THEN '20000-20999'
        WHEN milage BETWEEN 21000 AND 21999 THEN '21000-21999'
        WHEN milage BETWEEN 22000 AND 22999 THEN '22000-22999'
        WHEN milage BETWEEN 23000 AND 23999 THEN '23000-23999'
        WHEN milage BETWEEN 24000 AND 24999 THEN '24000-24999'
        WHEN milage BETWEEN 25000 AND 25999 THEN '25000-25999'
        WHEN milage BETWEEN 26000 AND 26999 THEN '26000-26999'
        WHEN milage BETWEEN 27000 AND 27999 THEN '27000-27999'
        WHEN milage BETWEEN 28000 AND 28999 THEN '28000-28999'
        WHEN milage BETWEEN 29000 AND 29999 THEN '29000-29999'
        -- 30000 +
        WHEN milage BETWEEN 30000 AND 30999 THEN '30000-30999'
        WHEN milage BETWEEN 31000 AND 31999 THEN '31000-31999'
        WHEN milage BETWEEN 32000 AND 32999 THEN '32000-32999'
        WHEN milage BETWEEN 33000 AND 33999 THEN '33000-33999'
        WHEN milage BETWEEN 34000 AND 34999 THEN '34000-34999'
        WHEN milage BETWEEN 35000 AND 35999 THEN '35000-35999'
        WHEN milage BETWEEN 36000 AND 36999 THEN '36000-36999'
        WHEN milage BETWEEN 37000 AND 37999 THEN '37000-37999'
        WHEN milage BETWEEN 38000 AND 38999 THEN '38000-38999'
        WHEN milage BETWEEN 39000 AND 39999 THEN '39000-39999'
        -- 40000 +
        WHEN milage BETWEEN 40000 AND 40999 THEN '40000-40999'
        WHEN milage BETWEEN 41000 AND 41999 THEN '41000-41999'
        WHEN milage BETWEEN 42000 AND 42999 THEN '42000-42999'
        WHEN milage BETWEEN 43000 AND 43999 THEN '43000-43999'
        WHEN milage BETWEEN 44000 AND 44999 THEN '44000-44999'
        WHEN milage BETWEEN 45000 AND 45999 THEN '45000-45999'
        WHEN milage BETWEEN 46000 AND 46999 THEN '46000-46999'
        WHEN milage BETWEEN 47000 AND 47999 THEN '47000-47999'
        WHEN milage BETWEEN 48000 AND 48999 THEN '48000-48999'
        WHEN milage BETWEEN 49000 AND 49999 THEN '49000-49999'
        -- 50000 +
        WHEN milage > 50000 THEN '50000 or more'
        ELSE 'Error'
    END as milage
    ,type
    ,hp
    ,price
FROM (
    SELECT
        brand
        ,model
        ,model_year
        ,gear
        ,fuel
        ,CASE
            WHEN milage like 'Mer%' THEN 50001
            WHEN INSTR(REPLACE(milage, ' ', ''),'-') = 0 THEN CAST(REPLACE(milage, ' ', '') as int)
            ELSE CAST(SUBSTR(REPLACE(milage, ' ', ''), 0, INSTR(REPLACE(milage, ' ', ''),'-')) as int)
        END as milage
        ,milage as milage_orig
        ,type
        ,hp
        ,add_date
        ,price
    FROM car_adds
    WHERE   brand != '-'
        AND model != '-'
        AND model_year != '-'
        AND make_year != '-'
        AND gear != '-'
        AND fuel != '-'
        AND milage != '-'
        AND type != '-'
        AND hp != '-'
        AND add_date != '-'
        AND model_year != 'model_year'
);