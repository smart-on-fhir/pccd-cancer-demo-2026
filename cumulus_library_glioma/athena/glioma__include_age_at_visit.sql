create or replace view glioma__include_age_at_visit as
select * from (values
(0,18)
) AS t (age_min,age_max) ;