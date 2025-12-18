# Glioma CUBE

CUBE(s) are simply the CUBE keyword in a [group by CUBE](https://prestodb.io/docs/current/sql/select.html#group-by-clause) clause resulting in a mathematical [PowerSet](https://en.wikipedia.org/wiki/Power_set).  

## SQL Tables as CSV 

### glioma__cube_patient_casedef
| column             | type    | description                                                                    |
|--------------------|---------|--------------------------------------------------------------------------------|
| `cnt`              | int     | count(distinct `subject`)                                                      |
| `age_at_dx_min`    | int     | patient age at the time of visit. Each patient can have multiple age_at_visit  |
| `dx_category_code` | varchar | FHIR Condition.category [`encounter-diagnosis`, `problem-list-item`]           |
| `dx_code`          | varchar | FHIR Condition.code code                                                       |
| `dx_display`       | varchar | FHIR Condition.code display                                                    |
| `dx_system`        | varchar | FHIR Condition.code system                                                     |
| `gender`           | varchar | HL7 Administrative Sex                                                         |
| `race_display`     | varchar | Patient Reported Race                                                          |


### glioma__cube_encounter_casedef
| column                     | type     | description                                   |
|----------------------------|----------|-----------------------------------------------|
| `cnt`                      | bigint   | count(distinct `encounter`)                   |
| `enc_class_code`           | varchar  | FHIR Encounter.class [AMB, EMER, OBSENC, IMP] |
| `enc_period_ordinal`       | varchar  | Calculated FHIR Encounter sequence number     |
| `enc_servicetype_display`  | varchar  | FHIR Encounter.serviceType display            |
| `enc_type_display`         | varchar  | FHIR Encounter.type display                   |

### glioma__cube_documentreference_sample_casedef_index_post
| column              | type    | description                                   |
|---------------------|---------|-----------------------------------------------|
| `cnt`               | bigint  | count(distinct `subject_ref`)                 |
| `doc_type_code`     | varchar | FHIR DocumentReference.type code              |
| `doc_type_display`  | varchar | FHIR DocumentReference.type display           |
| `doc_type_system`   | varchar | FHIR DocumentReference.type system            |
| `class_display`     | varchar | FHIR Encounter.class [AMB, EMER, OBSENC, IMP] |





