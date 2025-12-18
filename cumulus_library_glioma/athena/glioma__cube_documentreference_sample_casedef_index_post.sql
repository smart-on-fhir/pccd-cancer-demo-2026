CREATE or replace VIEW glioma__cube_documentreference_sample_casedef_index_post AS 
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.documentreference_ref,
            e.class_display,
            --noqa: disable=RF03, AL02
            s."doc_type_code",
            s."doc_type_display",
            s."doc_type_system"
            --noqa: enable=RF03, AL02
        FROM glioma__sample_casedef_index_post AS s
        INNER JOIN core__encounter AS e
            ON s.encounter_ref = e.encounter_ref
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            documentreference_ref,
            coalesce(
                cast(class_display AS varchar), 
                'cumulus__none'
            ) AS class_display,
            coalesce(
                cast(doc_type_code AS varchar),
                'cumulus__none'
            ) AS doc_type_code,
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
            count(DISTINCT documentreference_ref) AS cnt_documentreference_ref,
            "doc_type_code",
            "doc_type_display",
            "doc_type_system",
            class_display
            ,
            concat_ws(
                '-',
                COALESCE("doc_type_code",''),
                COALESCE("doc_type_display",''),
                COALESCE("doc_type_system",''),
                COALESCE(class_display,'')
                
            ) AS id
        FROM null_replacement
        WHERE documentreference_ref IS NOT NULL
        GROUP BY
            cube(
            "doc_type_code",
            "doc_type_display",
            "doc_type_system",
            class_display
            
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "doc_type_code",
            "doc_type_display",
            "doc_type_system",
            class_display
            ,
            concat_ws(
                '-',
                COALESCE("doc_type_code",''),
                COALESCE("doc_type_display",''),
                COALESCE("doc_type_system",''),
                COALESCE(class_display,'')
                
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "doc_type_code",
            "doc_type_display",
            "doc_type_system",
            class_display
            
            )
    )

    SELECT
        s.cnt_documentreference_ref AS cnt,
        p."doc_type_code",
        p."doc_type_display",
        p."doc_type_system",
        p.class_display
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        p.cnt_subject_ref >= 10
        AND s.cnt_documentreference_ref >= 10
;