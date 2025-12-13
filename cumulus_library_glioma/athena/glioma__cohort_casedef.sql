create  table glioma__cohort_casedef as
select  distinct
        casedef.code        as dx_code,
        casedef.display     as dx_display,
        casedef.system      as dx_system,
        DX.category_code    as dx_category_code,
        DX.recordeddate     as dx_recorded_date,
        SP.enc_period_start_day,
        SP.enc_period_ordinal,
        SP.enc_class_code,
        SP.enc_type_display,
        SP.enc_servicetype_display,
        SP.age_at_visit,
        SP.gender,
        SP.race_display,
        DX.subject_ref,
        DX.condition_ref,
        DX.encounter_ref
from    glioma__cohort_study_population as SP,
        glioma__valueset_casedef as casedef,
        core__condition as DX
where   DX.code = casedef.code
and     DX.system = casedef.system
and     DX.encounter_ref = SP.encounter_ref
;