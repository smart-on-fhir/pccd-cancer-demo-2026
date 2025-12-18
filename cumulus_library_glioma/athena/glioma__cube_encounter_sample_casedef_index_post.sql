CREATE or replace VIEW glioma__cube_encounter_sample_casedef_index_post AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."doc_type_display",
            s."doc_type_system"
            --noqa: enable=RF03, AL02
        FROM glioma__sample_casedef_index_post AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(doc_type_display AS varchar),
                'cumulus__none'
            ) AS doc_type_display,
            coalesce(
                cast(doc_type_system AS varchar),
                'cumulus__none'
            ) AS doc_type_system
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "doc_type_display",
            "doc_type_system",
            concat_ws(
                '-',
                COALESCE("doc_type_display",''),
                COALESCE("doc_type_system",'')
            ) AS id
        FROM null_replacement
        WHERE encounter_ref IS NOT NULL
        GROUP BY
            cube(
            "doc_type_display",
            "doc_type_system"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "doc_type_display",
            "doc_type_system",
            concat_ws(
                '-',
                COALESCE("doc_type_display",''),
                COALESCE("doc_type_system",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "doc_type_display",
            "doc_type_system"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."doc_type_display",
        p."doc_type_system"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        p.cnt_subject_ref >= 1
        AND s.cnt_encounter_ref >= 1
;