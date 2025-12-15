CREATE or replace VIEW glioma__cube_encounter_casedef AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."age_at_dx_min",
            s."dx_category_code",
            s."dx_display",
            s."enc_class_code",
            s."enc_period_ordinal"
            --noqa: enable=RF03, AL02
        FROM glioma__cohort_casedef AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(age_at_dx_min AS varchar),
                'cumulus__none'
            ) AS age_at_dx_min,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code,
            coalesce(
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(enc_period_ordinal AS varchar),
                'cumulus__none'
            ) AS enc_period_ordinal
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "age_at_dx_min",
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal",
            concat_ws(
                '-',
                COALESCE("age_at_dx_min",''),
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",''),
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_ordinal",'')
            ) AS id
        FROM null_replacement
        WHERE encounter_ref IS NOT NULL
        GROUP BY
            cube(
            "age_at_dx_min",
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "age_at_dx_min",
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal",
            concat_ws(
                '-',
                COALESCE("age_at_dx_min",''),
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",''),
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_ordinal",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_dx_min",
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."age_at_dx_min",
        p."dx_category_code",
        p."dx_display",
        p."enc_class_code",
        p."enc_period_ordinal"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        p.cnt_subject_ref >= 1
        AND s.cnt_encounter_ref >= 1
;