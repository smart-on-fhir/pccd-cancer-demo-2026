from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from cumulus_library_glioma.tools import filetool, fhir2sql
from cumulus_library_glioma.tools.filetool import PREFIX

def cube_patient_min10(source_table='study_population', table_cols=None, table_name=None, min_subject=10) -> Path:
    return cube_patient(source_table, table_cols, table_name, min_subject)

def cube_encounter(source_table='study_population', table_cols=None, table_name=None, min_subject=1) -> Path:
    """
    CUBE counts contain unique numbers of
        * FHIR Encounter --> "select count(distinct encounter_ref)"

    :param source_table: line-level cohort to derive counts from
    :param table_cols: columns to include in the CUBE group by expression
    :param table_name: output CUBE table
    :param min_subject: minimum number of subjects to include
    :return: Path to CUBE table
    """
    if not table_name:
        table_name = fhir2sql.name_cube(source_table, 'encounter')

    table_cols = sorted(list(set(table_cols)))
    sql = CountsBuilder(PREFIX).count_encounter(
        table_name=table_name,
        source_table=source_table,
        table_cols=table_cols,
        min_subject=min_subject
    )
    sql = as_view(sql, table_name)
    return filetool.save_athena_view(table_name, sql)

def cube_patient(source_table='study_population', table_cols=None, table_name=None, min_subject=1) -> Path:
    """
    CUBE counts contain unique numbers of
        * FHIR Patient --> "select count(distinct subject_ref)"

    :param source_table: line-level cohort to derive counts from
    :param table_cols: columns to include in the CUBE group by expression
    :param table_name: output CUBE table
    :param min_subject: minimum number of subjects to include
    :return: Path to CUBE table
    """
    if not table_name:
        table_name = fhir2sql.name_cube(source_table, 'patient')

    table_cols = sorted(list(set(table_cols)))
    sql = CountsBuilder(PREFIX).count_patient(
        table_name=table_name,
        source_table=source_table,
        table_cols=table_cols,
        min_subject=min_subject
    )
    sql = as_view(sql, table_name)
    return filetool.save_athena_view(table_name, sql)

def as_view(sql:str, table_name:str) -> str:
    """
    Hackish temp replacement for faster dev lifecycle
    """
    create_table = f'CREATE TABLE {table_name} AS ('
    replace_view = f'CREATE or replace VIEW {table_name} AS '
    return sql.replace(create_table, replace_view).replace(');', ';')

def make() -> List[Path]:
    return [
        cube_patient(source_table='glioma__cohort_casedef',
                     table_cols=['dx_display', 'dx_category_code',
                                 'age_at_visit',
                                 'gender', 'race_display']),

        cube_encounter(source_table='glioma__cohort_casedef',
                     table_cols=['dx_display', 'dx_category_code',
                                 'age_at_dx_min',
                                 'enc_period_ordinal', 'enc_class_code']),
    ]

if __name__ == "__main__":
    target_files = make()
