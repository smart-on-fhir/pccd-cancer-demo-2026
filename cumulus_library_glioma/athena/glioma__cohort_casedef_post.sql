-- ###############################]#########################################
-- "IndexDate" is the technical term for cohort based studies
--
--  The index date is frequently the date when individuals enter the study cohort
--  (e.g., enrollment date or the start of exposure to a treatment or risk factor).
--
--
-- "Pre" = pre-exposure (for drug/treatment studies) or
-- "Pre" = pre-diagnosis (for disease studies)
-- "Post" = post-exposure (for drug/treatment studies) or
-- "Post" = post-diagnosis (for disease studies)
--
-- ########################################################################

create table glioma__cohort_casedef_post as
WITH
first_match as (
    select      min(enc_period_start_day) as index_date,
                subject_ref
    from        glioma__cohort_casedef
    where       dx_category_code is NOT NULL
    group by    subject_ref
)
select
        first_match.index_date,
        SP.*
from
        glioma__cohort_study_population as SP,
        first_match
where
        SP.subject_ref = first_match.subject_ref
and     SP.enc_period_start_day > first_match.index_date
;