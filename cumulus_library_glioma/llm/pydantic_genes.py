from enum import StrEnum
from pydantic import BaseModel, Field

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
# Evidence citation
###############################################################################
class VariantInterpretation(StrEnum):
    B = 'BENIGN'
    LB = 'LIKELY BENIGN'
    VUS = 'VARIANT OF UNKNOWN SIGNIFICANCE'
    P = 'PATHOGENIC'
    LP = 'LIKELY PATHOGENIC'
    NOT_MENTIONED = 'NOT MENTIONED'

class GeneticVariantMention(SpanAugmentedMention):
    """
    Clinical interpretation of genetic variant
    """
    hgnc_name: str = Field(
        default=None,
        description="HGNC hugo gene naming convention")

    interpretation: VariantInterpretation = Field(
        VariantInterpretation.NOT_MENTIONED,
        description='Clinical interpretation of genetic variant or genetic test result'
    )

    hgvs_variant:str = Field(
        str,
        description="Human Genome Variation Society (HGVS) variant"
    )
