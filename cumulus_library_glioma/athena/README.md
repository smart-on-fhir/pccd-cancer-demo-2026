# CUBE DATA

## glioma__cube_patient_casedef
column| type    |description
------|---------|------
`cnt`| int     |count(distinct `subject_ref`)
`age_at_dx_min`| int     |patient age at the time of visit. Each patient can have multiple age_at_visit     
`dx_category_code` | varchar | FHIR Condition.category ['encounter-diagnosis' , 'problem-list-item']
`dx_code`| varchar |FHIR Condition.code code
`dx_display`| varchar |FHIR Condition.code display
`dx_system`| varchar |FHIR Condition.code system
`gender`| varchar |HL7 Administrative Sex
`race_display`| varchar |Patient Reported Race

