from enum import StrEnum
from typing import Annotated
from typing import Optional
from pydantic import BaseModel, Field, StringConstraints

###############################################################################
# Evidence citation
###############################################################################
class SpanAugmentedMention(BaseModel):
    has_mention: bool = Field(
        False,
        description="Whether there is any mention of this variable in the text."
    )
    spans: list[str] = Field(
        default_factory=list,
        description="The text spans where this variable is mentioned."
    )

###############################################################################
# Topology
###############################################################################
ICDOTopographyCode = Annotated[
    str,
    StringConstraints(pattern=r"^C\d{2}(\.\d)?$")
]

class CancerTopologyMention(SpanAugmentedMention):
    """
    ICD-O Oncology topography for a cancer lesion, plus whether this site
    represents the primary tumor or a metastatic tumor.
    """
    code: ICDOTopographyCode = Field(
        None,
        description=(
            "ICD-O topography code (Cxx or Cxx.x) for the anatomic site of the malignant neoplasm, "
            "e.g., C18.0 for cecum."
        ),
    )
    description: str = Field(
        None,
        description="Human-readable ICD-O anatomic site description corresponding to the topography code."
    )

###############################################################################
# Morphology
###############################################################################
ICDOMorphologyCode = Annotated[
    str,
    StringConstraints(pattern=r"^\d{4}/[0-9]$")
]

class CancerMorphologyMention(BaseModel):
    """
    ICD-O Oncology Morphology (Histology + Behavior).

    Morphology represents the microscopic tumor cell type (e.g., adenocarcinoma,
    squamous cell carcinoma, lymphoma) combined with the behavior code.
    """
    code: ICDOMorphologyCode = Field(
        None,
        description=(
            "ICD-O morphology code (M-####/x). Example: 8140/3 = Adenocarcinoma, NOS (malignant)."
        )
    )
    description: str = Field(
        None,
        description="Human-readable ICD-O histologic type (e.g., 'Adenocarcinoma, NOS')."
    )

###############################################################################
# Behavior
###############################################################################
class ICDOBehaviorCode(StrEnum):
    BENIGN = "/0"
    UNCERTAIN = "/1"
    IN_SITU = "/2"
    MALIGNANT_PRIMARY = "/3"
    MALIGNANT_METASTATIC = "/6"
    MALIGNANT_RECURRENT = "/9"

class CancerBehaviorMention(SpanAugmentedMention):
    behavior: ICDOBehaviorCode = Field(
        None,
        description="ICD-O slash behavior code (e.g., /3 = malignant primary site)."
    )
    description: str = Field(
        None,
        description="Human-readable description of the cancer behavior."
    )


###############################################################################
# Grade
###############################################################################
class CancerGradeCode(StrEnum):
    GRADE_I = "1"     # Well differentiated
    GRADE_II = "2"    # Moderately differentiated
    GRADE_III = "3"   # Poorly differentiated
    GRADE_IV = "4"    # Undifferentiated / Anaplastic
    GRADE_UNKNOWN = "9"  # Not determined / Cannot be assessed

class CancerGradeMention(SpanAugmentedMention):
    """
    ICD-O Oncology Grade (Tumor cell differentiation grade).

    Grade reflects how closely the tumor cells resemble normal tissue:
      1 = Well differentiated
      2 = Moderately differentiated
      3 = Poorly differentiated
      4 = Undifferentiated / Anaplastic
      9 = Grade cannot be assessed
    """
    grade: CancerGradeCode = Field(
        None,
        description="ICD-O tumor differentiation grade (1, 2, 3, 4, or 9)."
    )
    description: str = Field(
        None,
        description="Human-readable ICD-O description of the tumor grade."
    )

###############################################################################
# TNM Stage (Pathological Stage)
###############################################################################
class TStage(StrEnum):
    TX = "TX"
    T0 = "T0"
    TIS = "Tis"
    T1 = "T1"
    T1A = "T1a"
    T1B = "T1b"
    T2 = "T2"
    T2A = "T2a"
    T2B = "T2b"
    T3 = "T3"
    T4 = "T4"

class NStage(StrEnum):
    NX = "NX"
    N0 = "N0"
    N1I = "N1i"
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"


class MStage(StrEnum):
    M0 = "M0"
    M1 = "M1"
    M1A = "M1a"
    M1B = "M1b"

class CancerTNMStageMention(SpanAugmentedMention):
    """
    TNM cancer staging using ICD-O / AJCC-style T, N, and M categories.

    T = Primary tumor size/extent
    N = Regional lymph node involvement
    M = Distant metastasis status
    """
    t: TStage = Field(None, description="T category (primary tumor).")
    n: NStage = Field(None, description="N category (regional lymph nodes).")
    m: MStage = Field(None, description="M category (distant metastasis).")

###############################################################################
# Clinical Stage
###############################################################################
class ClinicalStage(StrEnum):
    STAGE_0 = "0"
    STAGE_IA = "IA"
    STAGE_IB = "IB"
    STAGE_IIA = "IIA"
    STAGE_IIB = "IIB"
    STAGE_IIIA = "IIIA"
    STAGE_IIIB = "IIIB"
    STAGE_IV = "IV"

class CancerClinicalStage(SpanAugmentedMention):
    """
    Clinical stage grouping using ICD-O / AJCC-style global stage categories.
    These represent the overall clinical stage (not pathologic stage).

    Examples:
      - 0:     Carcinoma in situ
      - IA/IB: Early localized disease
      - II–III: Increasing local/regional extent
      - IV:     Metastatic disease
    """
    stage: ClinicalStage = Field(
        None,
        description="ICD-O / AJCC clinical stage group (0, IA, IB, IIA, IIB, IIIA, IIIB, IV)."
    )
    description: str = Field(
        None,
        description="Human-readable description of the clinical stage."
    )

###############################################################################
# Treatment: RxClass Cancer
###############################################################################
class RxClassCancer(StrEnum):
    CHEMO = 'Cytotoxic chemotherapy'
    CHECKPOINT = 'Checkpoint inhibitors, especially PD-1, PDL-1, CTLA-4'
    CYTOKINE = 'Cytokine therapy, especially IL-2 and interferon alpha'
    CAR_T = 'Chimeric antigen receptor (CAR-T)'
    OTHER = 'Other drug indicated for treatment of cancer(s)'
    NONE = 'None of the above'

###############################################################################
# Surgery
###############################################################################
class SurgicalType(StrEnum):
    BIOPSY = "BIOPSY"
    RESECTION = "RESECTION"
    DEBULKING = "DEBULKING"
    ABLATION = "ABLATION"              # LITT, RFA, etc.
    ENDOSCOPIC = "ENDOSCOPIC"
    CRANIOTOMY = "CRANIOTOMY"
    OTHER = "OTHER"
    NOT_MENTIONED = "NOT_MENTIONED"

class SurgicalApproach(StrEnum):
    OPEN = "OPEN"
    AWAKE = "AWAKE"
    ENDOSCOPIC = "ENDOSCOPIC"
    STEREOTACTIC = "STEREOTACTIC"
    LASER = "LASER"
    KEYHOLE = "KEYHOLE"
    NOT_MENTIONED = "NOT_MENTIONED"

class SurgicalExtentOfResection(StrEnum):
    GROSS_TOTAL = "GROSS_TOTAL"
    SUBTOTAL = "SUBTOTAL"
    PARTIAL = "PARTIAL"
    BIOPSY_ONLY = "BIOPSY_ONLY"
    SUPRATOTAL = "SUPRATOTAL"          # used in LGG for seizure control
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_MENTIONED = "NOT_MENTIONED"

class CancerSurgeryMention(SpanAugmentedMention):
    """
    Structured representation of a surgical procedure performed for a cancer
    (e.g., low-grade glioma). Includes surgical type, approach, and extent of
    resection when identifiable from the clinical note.
    """
    surgical_type: SurgicalType = Field(
        default=SurgicalType.NOT_MENTIONED,
        description="High-level categorization of the surgery (biopsy, resection, ablation, etc.)"
    )

    approach: SurgicalApproach = Field(
        default=SurgicalApproach.NOT_MENTIONED,
        description="Technical approach used during the surgery (open, awake, stereotactic, laser)."
    )

    extent_of_resection: SurgicalExtentOfResection = Field(
        default=SurgicalExtentOfResection.NOT_MENTIONED,
        description="Reported extent of tumor resection."
    )

    anatomical_site: Optional[str] = Field(
        default=None,
        description="Anatomical site of surgery (e.g., 'left frontal lobe', 'right temporal lobe')."
    )

    technique_details: Optional[str] = Field(
        default=None,
        description="Additional operative details (e.g., 'intraoperative mapping', 'iMRI-guided')."
    )

    complications: Optional[str] = Field(
        default=None,
        description="Intraoperative or postoperative complications if mentioned."
    )
