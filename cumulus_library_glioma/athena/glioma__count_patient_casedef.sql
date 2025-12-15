CREATE or replace VIEW glioma__count_patient_casedef AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."dx_category_code",
            s."dx_display",
            s."enc_class_code",
            s."enc_period_ordinal"
            --noqa: enable=RF03, AL02
        FROM glioma__cohort_casedef AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
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

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal",
            concat_ws(
                '-',
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",''),
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_ordinal",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "dx_category_code",
            "dx_display",
            "enc_class_code",
            "enc_period_ordinal"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."dx_category_code",
        p."dx_display",
        p."enc_class_code",
        p."enc_period_ordinal"
    FROM powerset AS p
    WHERE 
        p.cnt_subject_ref >= 1
;