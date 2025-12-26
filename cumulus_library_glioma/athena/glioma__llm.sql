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

create or replace view glioma__llm_variant as
select      distinct
            variant.has_mention,
            variant.hgnc_name,
            variant.hgvs_variant,
            variant.interpretation,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.variant_mention) AS t(variant)
ON TRUE;

create or replace view glioma__llm_genetics as
select      distinct
            genetics.has_mention,
            genetics.braf_altered,
            genetics.braf_v600e,
            genetics.braf_fusion,
            genetics.idh_mutant,
            genetics.h3k27m_mutant,
            genetics.tp53_altered,
            genetics.cdkn2a_deleted,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.target_genetic_test_mention) AS t(genetics)
ON TRUE;

create or replace view glioma__llm_drug as
select      distinct
            drug.has_mention,
            drug.status,
            drug.category,
            drug.route,
            drug.phase,
            drug.expected_supply_days,
            drug.number_of_repeats_allowed,
            drug.frequency,
            drug.start_date,
            drug.end_date,
            drug.quantity_unit,
            drug.quantity_value,
            drug.rx_class,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.cancer_medication_mention) AS t(drug)
ON TRUE;

create or replace view glioma__llm_surgery as
select      distinct
            surgery.has_mention,
            surgery.surgical_type,
            surgery.approach,
            surgery.extent_of_resection,
            surgery.anatomical_site,
            surgery.technique_details,
            surgery.complications,
            nlp.note_ref,
            nlp.encounter_ref,
            nlp.subject_ref
from        glioma__nlp_gpt_oss_120b as nlp
LEFT JOIN   UNNEST(nlp.result.surgery_mention) AS t(surgery)
ON TRUE;

