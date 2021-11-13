-- QUERIES
-- Finding number of Successful TaskRuns used for Server (for Cloud estimates)
-- Ran against PostgresDB for Server users

select
date_trunc('month', start_time) as month,
count(*) FILTER (WHERE end_time-start_time >= INTERVAL '1 SECOND') as ">1 second",
COUNT(*) as "total"


select
       date_trunc('month', start_time) as month,
       extract(epoch from end_time-start_time) >= 1 as count_towards_quota,
       count(*)
from public.task_run
where true
    and state = 'Success'
    and start_time is not null
    and end_time is not null
    and extract(epoch from end_time-start_time) >= 1
group by 1,2
order by date_trunc('month', start_time);