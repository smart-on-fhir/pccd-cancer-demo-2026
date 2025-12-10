create or replace view ibd__include_utilization as
select * from (values
(3,1000,365,365000)
) AS t (enc_min,enc_max,days_min,days_max) ;