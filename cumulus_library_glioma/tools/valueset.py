from pathlib import Path
from fhirclient.models.coding import Coding
from cumulus_library_glioma.tools import filetool, fhir2sql

def csv_to_sql(filename_csv:str) -> Path:
    """
    :param filename_csv: downloaded CSV results, filtered/curated by Andy@BCH
    :return: Path to SQL ValueSet
    """
    entries = list()
    csv_file = filetool.path_valueset(filename_csv)
    print(csv_file)
    for columns in filetool.read_csv(csv_file):
        c = Coding()
        c.system = columns[0]
        c.code = columns[1]
        c.display = columns[2]
        entries.append(c)

    viewname = filename_csv.replace('glioma__', '').replace('.csv', '')
    return fhir2sql.define(entries, viewname)


def make() -> Path:
    return csv_to_sql('glioma__valueset_topography.csv')

if __name__ == '__main__':
    make()
