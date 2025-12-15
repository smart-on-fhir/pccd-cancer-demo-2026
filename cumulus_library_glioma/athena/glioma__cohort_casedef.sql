create  table glioma__cohort_casedef as
with cohort as
(
    select  distinct
            casedef.code        as dx_code,
            casedef.display     as dx_display,
            casedef.system      as dx_system,
            DX.category_code    as dx_category_code,
            DX.recordeddate     as dx_recorded_date,
            SP.age_at_visit,
            SP.gender,
            SP.race_display,
            SP.status,
            SP.enc_period_start_day,
            SP.enc_period_ordinal,
            SP.enc_class_code,
            SP.enc_type_display,
            SP.enc_servicetype_display,
            DX.subject_ref,
            DX.condition_ref,
            DX.encounter_ref
    from    glioma__cohort_study_population as SP,
            glioma__valueset_casedef as casedef,
            core__condition as DX
    where   DX.code = casedef.code
    and     DX.system = casedef.system
    and     DX.encounter_ref = SP.encounter_ref
),
age_at_dx as
(
    select  min(age_at_visit) as age_at_dx_min,
            max(age_at_visit) as age_at_dx_max,
            dx_code,
            dx_system,
            subject_ref
    from    cohort
    group by
            dx_code, dx_system, subject_ref
)
select  age_at_dx.age_at_dx_min,
        age_at_dx.age_at_dx_max,
        cohort.*
from    cohort, age_at_dx
where   age_at_dx.subject_ref   = cohort.subject_ref
and     age_at_dx.dx_code       = cohort.dx_code
and     age_at_dx.dx_system     = cohort.dx_system
;
