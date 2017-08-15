\set col testcol
-- unique count
select count(distinct :col) from marketing.test_table;
-- null count
select count(*) from t-- zeroes
select count(*) from marketing.test_table where :col = 0;
-- distribution
select :col,count(*) from marketing.test_table group by :col order by count;
-- basic stats from aggregate functions
select avg(:col),min(:col),max(:col),variance(:col) from marketing.test_table;
-- analytic function
-- select median(:col) from marketing.test_table;
-- select PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY :col) from marketing.test_table;
\set col testcol
-- select PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY :col) OVER (PARTITION BY :col) from marketing.test_table;
select distinct PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY :col) OVER () from marketing.test_table;
select PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY :col) OVER () from marketing.test_table limit 1;
select PERCENTILE_DISC(.05) WITHIN GROUP (ORDER BY :col) OVER ()
select
PERCENTILE_DISC(.05) WITHIN GROUP (ORDER BY :col) OVER () as '5',
PERCENTILE_DISC(.25) WITHIN GROUP (ORDER BY :col) OVER () as '25',
PERCENTILE_DISC(.5) WITHIN GROUP (ORDER BY :col) OVER () as '50',
PERCENTILE_DISC(.75) WITHIN GROUP (ORDER BY :col) OVER () as '75',
PERCENTILE_DISC(.95) WITHIN GROUP (ORDER BY :col) OVER () as '95'
from
marketing.test_table
limit 1;
-- the above is slow. only use this on continuous data (for categorical (ordinal) data where we already do the histogram, we have the relevant data already)

-- Standard deviation
-- Coef of variation
-- Kurtosis
-- MAD
-- Skewness

-- for a binned histogram... write the query using a case statement and ranges!

-- common and extreme values for continuous
