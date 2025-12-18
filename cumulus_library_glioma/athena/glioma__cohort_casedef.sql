create  table glioma__cohort_casedef as
WITH
match_casedef as
(
    select  distinct
            casedef.code        as dx_code,
            casedef.display     as dx_display,
            casedef.system      as dx_system,
            dx.category_code    as dx_category_code,            
            sp.age_at_visit,
            dx.subject_ref,            
            dx.encounter_ref
    from    glioma__valueset_casedef as casedef,
            glioma__cohort_study_population_dx as SP,            
            core__condition as dx
    where   casedef.code = dx.code
    and     casedef.system = dx.system
    and     dx.encounter_ref = sp.encounter_ref
),
calculate_age as
(
    select  min(age_at_visit) as age_at_dx_min,
            max(age_at_visit) as age_at_dx_max,
            dx_code,
            dx_system,
            subject_ref
    from    match_casedef
    group by
            dx_code, dx_system, subject_ref
), 
cohort as 
(
    select  calculate_age.age_at_dx_min,
            calculate_age.age_at_dx_max,
            match_casedef.*
    from    match_casedef, 
            calculate_age 
    where   calculate_age.subject_ref   = match_casedef.subject_ref
    and     calculate_age.dx_code       = match_casedef.dx_code
    and     calculate_age.dx_system     = match_casedef.dx_system
), 
longitudinal as
(
    select  distinct
            sp.age_at_visit,
            sp.gender,
            sp.race_display,
            sp.status,
            sp.enc_period_start_day,
            sp.enc_period_start_year,
            sp.enc_period_ordinal,
            sp.enc_class_code,
            sp.enc_type_display,
            sp.enc_servicetype_display,
            sp.subject_ref,            
            sp.encounter_ref
    from    match_casedef,
            glioma__cohort_study_population as SP
    where   match_casedef.subject_ref = sp.subject_ref
)
select      distinct
            cohort.age_at_dx_min,
            cohort.age_at_dx_max, 
            cohort.dx_category_code, 
            cohort.dx_code,
            cohort.dx_system,
            cohort.dx_display,
            longitudinal.*
from        longitudinal
left join   cohort
       on   longitudinal.encounter_ref = cohort.encounter_ref
;
