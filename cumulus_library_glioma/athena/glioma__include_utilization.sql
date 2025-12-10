create or replace view glioma__include_utilization as
select * from (values
(1,1000,1,365000)
) AS t (enc_min,enc_max,days_min,days_max) ;