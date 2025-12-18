CREATE or replace VIEW glioma__cube_encounter_casedef AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."enc_class_code",
            s."enc_period_ordinal",
            s."enc_servicetype_display",
            s."enc_type_display"
            --noqa: enable=RF03, AL02
        FROM glioma__cohort_casedef AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(enc_period_ordinal AS varchar),
                'cumulus__none'
            ) AS enc_period_ordinal,
            coalesce(
                cast(enc_servicetype_display AS varchar),
                'cumulus__none'
            ) AS enc_servicetype_display,
            coalesce(
                cast(enc_type_display AS varchar),
                'cumulus__none'
            ) AS enc_type_display
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "enc_class_code",
            "enc_period_ordinal",
            "enc_servicetype_display",
            "enc_type_display",
            concat_ws(
                '-',
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_ordinal",''),
                COALESCE("enc_servicetype_display",''),
                COALESCE("enc_type_display",'')
            ) AS id
        FROM null_replacement
        WHERE encounter_ref IS NOT NULL
        GROUP BY
            cube(
            "enc_class_code",
            "enc_period_ordinal",
            "enc_servicetype_display",
            "enc_type_display"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_class_code",
            "enc_period_ordinal",
            "enc_servicetype_display",
            "enc_type_display",
            concat_ws(
                '-',
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_ordinal",''),
                COALESCE("enc_servicetype_display",''),
                COALESCE("enc_type_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_class_code",
            "enc_period_ordinal",
            "enc_servicetype_display",
            "enc_type_display"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."enc_class_code",
        p."enc_period_ordinal",
        p."enc_servicetype_display",
        p."enc_type_display"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        p.cnt_subject_ref >= 1
        AND s.cnt_encounter_ref >= 1
;