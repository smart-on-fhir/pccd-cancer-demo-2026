create or replace view glioma__llm as
select      distinct
            result.topography_mention.has_mention   as topography_has_mention,
            result.topography_mention.code          as topography_code,
            result.topography_mention.display       as topography_display,
            result.morphology_mention.has_mention   as morphology_has_mention,
            result.morphology_mention.code          as morphology_code,
            result.morphology_mention.display       as morphology_display,
            result.behavior_mention.has_mention     as behavior_has_mention,
            result.behavior_mention.code            as behavior_code,
            result.behavior_mention.display         as behavior_display,
            result.grade_mention.has_mention        as grade_has_mention,
            result.grade_mention.code               as grade_code,
            result.grade_mention.display            as grade_display,
            note_ref,
            encounter_ref,
            subject_ref
from        glioma__nlp_gpt_oss_120b;



create or replace view glioma__llm_drug as
select      distinct
            coalesce(drug.has_mention, False)           as has_mention,
            coalesce(drug.rx_class, 'NOT_MENTIONED')    as rx_class,
            coalesce(drug.status, 'NOT_MENTIONED')      as status,
            coalesce(drug.category, 'NOT_MENTIONED')    as category,
            coalesce(drug.route, 'NOT_MENTIONED')       as route,
            coalesce(drug.phase, 'NOT_MENTIONED')       as phase,
            coalesce(drug.frequency, 'NOT_MENTIONED')   as frequency,
            drug.start_date,
            drug.end_date,
            drug.quantity_unit,
            drug.quantity_value,
            drug.expected_supply_days,
            drug.number_of_repeats_allowed,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.cancer_medication_mention) AS t(drug)
ON TRUE;

create or replace view glioma__llm_surgery as
select      distinct
            coalesce(surgery.has_mention, False)                as has_mention,
            coalesce(surgery.anatomical_site, 'NOT_MENTIONED')  as anatomical_site,
            coalesce(surgery.surgical_type, 'NOT_MENTIONED')    as surgical_type,
            coalesce(surgery.approach, 'NOT_MENTIONED')         as approach,
            coalesce(surgery.extent_of_resection, 'NOT_MENTIONED')  as extent_of_resection,
            coalesce(surgery.technique_details, 'NOT_MENTIONED')    as technique_details,
            coalesce(surgery.complications, 'NOT_MENTIONED')        as complications,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.surgery_mention) AS t(surgery)
ON TRUE;

-- ############################################################################
-- DNA sequencing
-- See also glioma__llm_gene

create or replace view glioma__llm_variant as
select      distinct
            coalesce(variant.has_mention, False)                as has_mention,
            coalesce(variant.hgnc_name, 'NOT_MENTIONED')        as hgnc_name,
            coalesce(variant.hgvs_variant, 'NOT_MENTIONED')     as hgvs_variant,
            coalesce(variant.interpretation, 'NOT_MENTIONED')   as interpretation,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.variant_mention) AS t(variant)
ON TRUE;

-- ############################################################################
-- NOTE: BRAF fusion or V600E implies --> braf_altered

create or replace view glioma__llm_gene as
select      distinct
            coalesce(genetics.has_mention, False)     as has_mention,
            case genetics.braf_altered
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as braf_altered,
            case genetics.braf_v600e
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as braf_v600e,
            case genetics.braf_fusion
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as braf_fusion,
            case genetics.idh_mutant
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as idh_mutant,
            case genetics.h3k27m_mutant
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as h3k27m_mutant,
            case genetics.tp53_altered
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as tp53_altered,
            case genetics.cdkn2a_deleted
                when True   then 'positive'
                when False  then 'negative'
                else 'NOT_MENTIONED' end as cdkn2a_deleted,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.target_genetic_test_mention) AS t(genetics)
ON TRUE;
