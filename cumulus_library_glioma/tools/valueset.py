import csv
import unittest
import pandas as pd
from pathlib import Path
from fhirclient.models.coding import Coding
from cumulus_library_glioma.tools import filetool,fhir2sql

UMLS_VOCAB = {
    "SNOMEDCT_US": "http://snomed.info/sct",
    "ICD10CM": "http://hl7.org/fhir/sid/icd-10-cm",
    "ICD9CM":  "http://hl7.org/fhir/sid/icd-9-cm",
    "RXNORM": "http://www.nlm.nih.gov/research/umls/rxnorm"
}

def make_valueset_morphology():
    file_in = filetool.path_resources('umls_morphology.bsv')
    file_out = filetool.path_resources('valueset_morphology.csv')
    make_valueset(file_in, file_out, UMLS_VOCAB)

def make_valueset_topography():
    file_in = filetool.path_resources('umls_topography.bsv')
    file_out = filetool.path_resources('valueset_topography.csv')
    make_valueset(file_in, file_out, UMLS_VOCAB)

def make_valueset(file_in:Path, file_out:Path, umls_vocab:dict):
    df = pd.read_csv(file_in, sep="|", dtype=str)
    df = df[df["SAB"].isin(umls_vocab.keys())]
    df["SAB"] = df["SAB"].replace(UMLS_VOCAB)
    df_out = df[["SAB", "CODE", "PREF"]]
    df_out = df_out.drop_duplicates()
    df_out = df_out.sort_values(["SAB", "CODE"], ascending=[True, True])
    df_out.to_csv(file_out, header=False, index=False)

def csv_to_sql(filename_csv:str) -> Path:
    """
    :param filename_csv: downloaded CSV results, filtered/curated by Andy@BCH
    :return: Path to SQL ValueSet
    """
    entries = list()
    csv_file = filetool.path_resources(filename_csv)
    for columns in filetool.read_csv(csv_file):
        c = Coding()
        c.system = columns[0]
        c.code = columns[1]
        c.display = columns[2]
        entries.append(c)

    viewname = filename_csv.replace('.csv', '')
    return fhir2sql.define(entries, viewname)

def make() -> list[Path]:
    make_valueset_topography()
    make_valueset_morphology()
    return [
        csv_to_sql('valueset_casedef.csv'),
        csv_to_sql('valueset_morphology.csv')
    ]

if __name__ == '__main__':
    make()
