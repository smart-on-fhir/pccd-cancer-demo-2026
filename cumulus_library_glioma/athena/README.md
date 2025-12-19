# Glioma CUBE

CUBE(s) are simply the CUBE keyword in a [group by CUBE](https://prestodb.io/docs/current/sql/select.html#group-by-clause) clause resulting in a mathematical [PowerSet](https://en.wikipedia.org/wiki/Power_set).  

## SQL Tables as CSV

CSV table naming conventions

| alias             | meaning                                           |
|-------------------|---------------------------------------------------|
| glioma__          | cumulus study prefix                              |
| cube              | powerset counts                                   |
| patient           | count distinct patients                           |
| encounter         | count distinct encounters                         |
| documentreference | count distinct clinical notes                     |
| casedef           | match case definition for LGG(Low Grade Glioma)   |
| sample            | sample LGG cohort                                 |
| index_post        | sample LGG cohort starting at first LGG diagnosis |

### glioma__cube_patient_casedef

Count distinct **FHIR Patient** in cohort matching LGG case definition.    
Stratified by demographics (age at diagnosis, gender, race) and diagnosis (code, display, system). 

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

Count distinct **FHIR encounter** in cohort matching LGG case definition.    
Stratified by FHIR Encounter class, type, and serviceType.   

| column                     | type     | description                                   |
|----------------------------|----------|-----------------------------------------------|
| `cnt`                      | bigint   | count(distinct `encounter`)                   |
| `enc_class_code`           | varchar  | FHIR Encounter.class [AMB, EMER, OBSENC, IMP] |
| `enc_period_ordinal`       | varchar  | Calculated FHIR Encounter sequence number     |
| `enc_servicetype_display`  | varchar  | FHIR Encounter.serviceType display            |
| `enc_type_display`         | varchar  | FHIR Encounter.type display                   |

### glioma__cube_document_sample_casedef_index_post

Count distinct **FHIR DocumentReference** in cohort matching LGG case definition.    
Stratified by FHIR DocumentReference.type and FHIR Encounter.class.   

| column              | type    | description                                   |
|---------------------|---------|-----------------------------------------------|
| `cnt`               | bigint  | count(distinct `subject_ref`)                 |
| `doc_type_code`     | varchar | FHIR DocumentReference.type code              |
| `doc_type_display`  | varchar | FHIR DocumentReference.type display           |
| `doc_type_system`   | varchar | FHIR DocumentReference.type system            |
| `class_display`     | varchar | FHIR Encounter.class [AMB, EMER, OBSENC, IMP] |





