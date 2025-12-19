import base64
import json
from typing import Any
from pathlib import Path
from datetime import datetime

INPUT_DIR = Path('./cumulus_library_glioma/llm/examples')
INPUT_FILES = [
    'glioma-1.txt',
    'glioma-2.txt.clean.txt',
    'glioma-consult.txt',
]
INPUT_SUBJECTS = [
    'patient-1',
    'patient-2',
    'patient-3',
]
INPUT_ENCS = [
    'enc-1',
    'enc-2',
    'enc-3',
]

OUTPUT_DIR = Path('cumulus_library_glioma/llm/examples/fhir')

def make_fhir_documentreference(doc_id: str, subject_id: str, enc_id: str, note: str) -> dict[str, Any]:
    mimetype = "text/plain"
    encoding = "utf-8"
    attachment: dict[str, Any] = {
        "data": base64.standard_b64encode(note).decode("ascii"),
        "contentType": f"{mimetype}; charset={encoding}",
        "title": f"{doc_id}",
    }

    doc_ref: dict[str, Any] = {
        "resourceType": "DocumentReference",
        "id": doc_id,
        "subject": {"reference": f"Patient/{subject_id}"},
        "encounter": {"reference": f"Encounter/{enc_id}"},
        "date": datetime.now().isoformat(),
        "type": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "display": 'GARBAGE'
                }
            ]
        },
        "content": [{"attachment": attachment}]
    }
    return doc_ref

if __name__ == '__main__': 
    for i, file in enumerate(INPUT_FILES):
        file_path = INPUT_DIR / file
        doc_id = file.replace('.txt', '').replace('.clean', '')
        subject_id = INPUT_SUBJECTS[i]
        enc_id = INPUT_ENCS[i]
        docref = make_fhir_documentreference(doc_id=doc_id, subject_id=subject_id, enc_id=enc_id, note=file_path.read_bytes())
        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        output_path = OUTPUT_DIR / (doc_id + '.ndjson')
        output_path.write_text(json.dumps(docref))
