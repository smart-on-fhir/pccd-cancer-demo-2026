CREATE or replace VIEW glioma__cube_patient_casedef AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."age_at_visit",
            s."dx_category_code",
            s."dx_display",
            s."gender",
            s."race_display"
            --noqa: enable=RF03, AL02
        FROM glioma__cohort_casedef AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code,
            coalesce(
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "age_at_visit",
            "dx_category_code",
            "dx_display",
            "gender",
            "race_display",
            concat_ws(
                '-',
                COALESCE("age_at_visit",''),
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",''),
                COALESCE("gender",''),
                COALESCE("race_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_visit",
            "dx_category_code",
            "dx_display",
            "gender",
            "race_display"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."age_at_visit",
        p."dx_category_code",
        p."dx_display",
        p."gender",
        p."race_display"
    FROM powerset AS p
    WHERE 
        p.cnt_subject_ref >= 1
;