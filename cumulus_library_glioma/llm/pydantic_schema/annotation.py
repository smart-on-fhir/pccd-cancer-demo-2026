from pydantic import BaseModel
from .pathology import TopographyMention, MorphologyMention, GradeMention, BehaviorMention
from .genes import TargetGeneticTestMention, VariantMention
from .drugs import MedicationMention, RxClassCancerMention
from .surgery import SurgeryMention

class GliomaCaseAnnotation(BaseModel):
    """
    SCHEMA root of Glioma Case Annotation
    """
    topography_mention: TopographyMention
    morphology_mention: MorphologyMention
    behavior_mention: BehaviorMention
    grade_mention: GradeMention
    target_genetic_test_mention: TargetGeneticTestMention
    variant_mention: VariantMention
    rx_class_cancer_mention: RxClassCancerMention
    surgery_mention: SurgeryMention




