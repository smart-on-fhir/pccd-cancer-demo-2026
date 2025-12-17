create  table glioma__cohort_comorbidity as
WITH
casedef as
(
    select distinct
            dx_code,
            dx_display,
            dx_system,
            subject_ref,
            encounter_ref
    from    glioma__cohort_casedef
)
select  dx.*
from    casedef,
        glioma__cohort_study_population_dx as dx
where   casedef.subject_ref = dx.subject_ref
and     casedef.dx_code != dx.dx_code
and     casedef.dx_system != dx.dx_system
;