create or replace view glioma__include_study_period as
select * from (values
(date('2016-01-01'),date('2025-02-01'),True)
) AS t (period_start, period_end, include_history) ;