import os
from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from cumulus_library_glioma.tools import filetool, fhir2sql
from cumulus_library_glioma.tools.filetool import PREFIX

MIN_SUBJECTS = int(os.environ.get("MIN_SUBJECTS") or 1)

def cube_fhir_resource(fhir_resource:str, source_table='study_population', table_cols=None, table_name=None, min_subject=MIN_SUBJECTS) -> Path:
    """Generates a counts table using a template

    :param fhir_resource: The type of FHIR resource to count
    :param source_table: The table to create counts data from
    :param table_cols: The columns from the source table to add to the count table
    :param table_name: The name of the table to create. Must start with study prefix
    :param min_subject: Minimum number of patients to include in result groupings
    """
    if not table_name:
        suffix = fhir_resource if (fhir_resource != 'documentreference') else 'document'
        table_name = fhir2sql.name_cube(source_table, suffix)

    table_cols = sorted(list(set(table_cols)))
    sql = CountsBuilder(PREFIX).get_count_query(
            table_name=table_name,
            source_table=source_table,
            table_cols=table_cols,
            min_subject=min_subject,
            fhir_resource=fhir_resource,
            filter_resource=True,
            skip_status_filter=True
    )
    sql = table_as_view(sql, table_name)
    return filetool.save_athena_view(table_name, sql)

def table_as_view(sql:str, table_name:str) -> str:
    """
    :param sql: CTAS (create table as)
    :param table_name: Table name to turn into a view
    :return: sql CVAS (create view as)
    """
    create_table = f'CREATE TABLE {table_name} AS ('
    replace_view = f'CREATE or replace VIEW {table_name} AS '
    return sql.replace(create_table, replace_view).replace(');', ';')

def cube_patient(source_table='study_population', table_cols=None, table_name=None, min_subject=MIN_SUBJECTS) -> Path:
    return cube_fhir_resource(
        fhir_resource='patient',
        source_table=source_table,
        table_cols=table_cols,
        table_name=table_name,
        min_subject=min_subject)

def cube_encounter(source_table='study_population', table_cols=None, table_name=None, min_subject=MIN_SUBJECTS) -> Path:
    return cube_fhir_resource(
        fhir_resource='encounter',
        source_table=source_table,
        table_cols=table_cols,
        table_name=table_name,
        min_subject=min_subject)

def cube_document(source_table='study_population', table_cols=None, table_name=None, min_subject=MIN_SUBJECTS) -> Path:
    return cube_fhir_resource(
        fhir_resource='documentreference',
        source_table=source_table,
        table_cols=table_cols,
        table_name=table_name,
        min_subject=min_subject)

def make() -> List[Path]:
    return [
        cube_patient(source_table='glioma__cohort_casedef',
                     table_cols=['dx_category_code',
                                 'dx_code',
                                 'dx_system',
                                 'dx_display',
                                 'age_at_dx_min',
                                 'gender',
                                 'race_display'],
                     min_subject=10),

        cube_patient(source_table='glioma__cohort_dx',
                     table_cols=['dx_category_code',
                                 'dx_code',
                                 'dx_system',
                                 'dx_display',
                                 'age_at_visit',
                                 'gender',
                                 'race_display'],
                     min_subject=10),

        cube_patient(source_table='glioma__cohort_rx',
                     table_cols=['rx_status',
                                 'rx_category_code',
                                 'rx_code',
                                 'rx_system',
                                 'rx_display',
                                 'age_at_visit',
                                 'gender',
                                 'race_display'],
                     min_subject=10),

        cube_encounter(source_table='glioma__cohort_casedef',
                       table_cols=['enc_class_code',
                                   'enc_type_display',
                                   'enc_servicetype_display',
                                   'enc_period_ordinal']),

        cube_document(source_table='glioma__sample_casedef_index_post',
                       table_cols=['doc_type_code',
                                   'doc_type_display',
                                   'doc_type_system'],
                      min_subject=10),

        cube_patient(source_table='glioma__llm',
                     table_cols=['topography_has_mention',
                                 'topography_display',
                                 'morphology_has_mention',
                                 'morphology_display',
                                 'behavior_has_mention',
                                 'behavior_code',
                                 'grade_has_mention',
                                 'grade_code']),

        cube_patient(source_table='glioma__llm_surgery',
                     table_cols=['has_mention',
                                 'surgical_type',
                                 'approach',
                                 'extent_of_resection',
                                 'anatomical_site',
                                 'technique_details',
                                 'complications']),

        cube_patient(source_table='glioma__llm_drug',
                     table_cols=['has_mention',
                                 'status',
                                 'category',
                                 'route',
                                 'phase',
                                 'rx_class']),

        cube_patient(source_table='glioma__llm_variant',
                     table_cols=['has_mention',
                                 'hgnc_name',
                                 'hgvs_variant',
                                 'interpretation']),

        cube_patient(source_table='glioma__llm_gene',
                     table_cols=['has_mention',
                                 'braf_altered',
                                 'braf_v600e',
                                 'braf_fusion',
                                 'idh_mutant',
                                 'h3k27m_mutant',
                                 'tp53_altered',
                                 'cdkn2a_deleted']),
    ]

if __name__ == "__main__":
    target_files = make()
