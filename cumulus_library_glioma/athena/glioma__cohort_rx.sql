create  table glioma__cohort_rx as
select  distinct
        rx.*
from    glioma__cohort_casedef as casedef,
        glioma__cohort_study_population_rx as rx
where   casedef.subject_ref = rx.subject_ref
;