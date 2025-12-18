from pydantic import BaseModel, Field
from .pathology import TopographyMention, MorphologyMention, GradeMention, BehaviorMention
from .genes import TargetGeneticTestMention, VariantMention
from .drugs import CancerMedicationMention
from .surgery import SurgeryMention

class GliomaCaseAnnotation(BaseModel):
    """
    SCHEMA root of Glioma Case Annotation
    """
    topography_mention: TopographyMention
    morphology_mention: MorphologyMention
    behavior_mention: BehaviorMention
    grade_mention: GradeMention
    target_genetic_test_mention: list[TargetGeneticTestMention] = Field(
        default_factory=list,
        description="All mentions of Target Genetic Tests."
    )
    variant_mention: list[VariantMention] = Field(
        default_factory=list,
        description="All mentions of Genetic Variants."
    )
    cancer_medication_mention: list[CancerMedicationMention] = Field(
        default_factory=list,
        description="All mentions of Cancer Medications."
    )
    surgery_mention: list[SurgeryMention] = Field(
        default_factory=list,
        description="All mentions of Cancer related surgeries."
    )




