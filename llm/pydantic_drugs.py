from enum import StrEnum, auto
from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints

###############################################################################
# Evidence citation
###############################################################################
class RxClassCancer(StrEnum):
    CHEMO = 'Cytotoxic chemotherapy'
    CHECKPOINT = 'Checkpoint inhibitors, especially PD-1, PDL-1, CTLA-4'
    CYTOKINE = 'Cytokine therapy, especially IL-2 and interferon alpha'
    CAR_T = 'Chimeric antigen receptor (CAR-T)'
    OTHER = 'Other drug indicated for treatment of cancer(s)'
    NONE = 'None of the above'


###############################################################################
# Spans
class SpanAugmentedMention(BaseModel):
    has_mention: bool | None  # True, False, or None
    spans: list[str]

###############################################################################
# MedicationRequest.status

class RxStatus(StrEnum):
    """
    Medication Status (including Intent because chart review is NOT always identical to Med Request)
    https://build.fhir.org/valueset-medicationrequest-status.html
    https://build.fhir.org/valueset-medicationrequest-intent.html
    """
    ACTIVE = "Medication order is active (currently prescribed and intended for ongoing use)."
    INTENDED = "Medication is planned/ordered/prescribed but therapy has not yet started."
    COMPLETED = "Medication course is finished (all doses given or intended duration completed)."
    STOPPED = "Medication was stopped or permanently discontinued before completion."
    CANCELED = "Medication order was canceled/withdrawn before any doses were administered."
    ON_HOLD = "Medication is temporarily paused (on-hold, suspended, or interrupted)."
    NONE = "None of the above"


###############################################################################
# MedicationRequest.category

class RxCategory(StrEnum):
    """
    https://build.fhir.org/valueset-medicationrequest-admin-location.html
    """
    INPATIENT = "Medication ordered/administered during an inpatient/acute care setting"
    OUTPATIENT = 'Medication ordered/administered during an outpatient setting'
    COMMUNITY = "Medication ordered/consumed by the patient in their home (including long term care, nursing homes, etc)"
    NONE = "None of the above"

###############################################################################
# MedicationRequest.route

class RxRoute(StrEnum):
    """
    Route of Administration can "help" (but not deterministic) for drug metadata, examples
    * Injection --> antibody for induction/rescue therapy
    * Topical --> skin lesions
    * Inhalation --> Steroid
    https://build.fhir.org/valueset-route-codes.html
    """
    PO = "Oral (includes swallowed and sublingual routes)"
    NG = "Nasogastric/Feeding tube (NG/PEG)"
    INJECTION = "Injection (IV, SC, or IM)"
    INHALATION = "Inhalation (respiratory route)"
    TOPICAL = "Topical (skin or mucosal surface)"
    NONE = "None of the above"


###############################################################################
# MedicationRequest.dispenseRequest
#
# MedicationRequest.dispenseRequest.validityPeriod

class RxExpectedSupplyDaysMention(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.expectedSupplyDuration
    """
    expected_supply_days: int | None = Field(
        default=None,
        description='Number of days the medication supply is supposed to last (stale dating the prescription)')

# MedicationRequest.dispenseRequest.expectedSupplyDuration
class RxValidityPeriodMention(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.validityPeriod
    """
    start_date: str | None = Field(
        default=None,
        description='Start date of the prescribed or administered medication'
    )

    end_date: str | None = Field(
        default=None,
        description='End date of the prescribed or administered medication')

class RxQuantityUnit(StrEnum):
    # Mass
    MG  = "mg"
    G   = "g"
    UG  = "ug"   # microgram (mcg)
    KG  = "kg"

    # Volume
    ML  = "mL"
    L   = "L"

    # International Units
    U   = "U"
    IU  = "[iU]"

    # Countable units
    TABLET      = "{tablet}"
    CAPSULE     = "{capsule}"
    PUFF        = "{puff}"
    PATCH       = "{patch}"
    SUPPOSITORY = "{suppository}"

    # Ratios
    MG_PER_ML          = "mg/mL"
    MG_PER_KG          = "mg/kg"
    U_PER_KG           = "U/kg"
    UG_PER_KG_PER_MIN  = "ug/kg/min"

    # Time units (for infusion rates)
    H   = "h"
    MIN = "min"
    D   = "d"
    NONE = "None of the above"

# MedicationRequest.dispenseRequest.quantity
class RxQuantity(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.quantity
    """
    unit: RxQuantityUnit = Field(
        default=RxQuantityUnit.NONE,
        description="Medication prescribed unit (examples: 'mg', 'ug/kg/min', 'tablet', etc)")

    value: str | None = Field(
        default=None,
        description='Numeric amount of medication prescribed or administered (FHIR Quantity.value)')



###############################################################################
# Treatment Phase

class TreatmentPhase(StrEnum):
    """
    Treatment Phase
    """
    INDUCTION = "Induction therapy"
    MAINTENANCE = "Maintenance therapy"
    RESCUE = "Rescue therapy"
    NONE = "None of the above"

###############################################################################
# helper: Describe Drug Type (class or therapy modality) or drug ingredient.

def drug_type_field(default=None, description=None) -> str | None:
    return Field(default=default, description=drug_type_desc(description))

def ingredient_field(default=None, description=None) -> str | None:
    return Field(default=default, description=ingredient_desc(description))

def drug_type_desc(drug_type: str) -> str:
    return clean(
        f"Extract the {drug_type} class or therapy modality documented for this medication, if present")

def ingredient_desc(ingredient: str) -> str:
    return clean(
        f"Extract the {ingredient} ingredient documented for this medication, if present")

def clean(text:str) -> str | None:
    return text.replace('  ', ' ').strip()


###############################################################################
# Template
###############################################################################
class MedicationMention(SpanAugmentedMention):
    """
    https://build.fhir.org/valueset-medicationrequest-status.html
    https://build.fhir.org/valueset-medicationrequest-admin-location.html
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.expectedSupplyDuration
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.validityPeriod
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.numberOfRepeatsAllowed
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.quantity
    """
    status: RxStatus = Field(
        default=RxStatus.NONE,
        description='What is the status of this medication?'
    )

    category: RxCategory = Field(
        default=RxCategory.NONE,
        description='In which healthcare setting is this medication prescribed/administered?'
    )

    route: RxRoute = Field(
        default=RxRoute.NONE,
        description='What is the the route of administration for this medication?'
    )

    phase: TreatmentPhase = Field(
        default=TreatmentPhase.NONE,
        description='What is the treatment phase for this medication?'
    )

    expected_supply_days: int | None = Field(
        default=None,
        description='Number of days the medication supply is supposed to last (stale dating the prescription)'
    )

    number_of_repeats_allowed: int | None = Field(
        default=None,
        description='number of times (aka refills or repeats) that the patient can receive the prescribed medication'
    )

    frequency: RxFrequency = Field(
        default=RxFrequency.NONE,
        description='What is the frequency of this medication?'
    )

    start_date: str | None = Field(
        None,
        description='Start date of the prescribed or administered medication'
    )

    end_date: str | None = Field(
        None,
        description='End date of the prescribed or administered medication'
    )

    quantity_unit: RxQuantityUnit= Field(
        RxQuantityUnit.NONE,
        description="Medication prescribed unit"
    )

    quantity_value: str | None = Field(
        None,
        description='Numeric amount of medication prescribed or administered (FHIR Quantity.value)'
    )

class RxClassMention(MedicationMention):
    # abstract, extend to override
    drug_type: str | object | None = drug_type_field()

class IngredientMention(MedicationMention):
    # abstract, extend to override
    ingredient: str | object | None = ingredient_field()
