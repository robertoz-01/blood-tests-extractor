from pydantic import BaseModel

from src.blood_tests_extractor.analysis import Analysis


class AnalysisViewModel(BaseModel):
    name: str
    value: float | None
    unit: str
    reference_lower: float | None
    reference_upper: float | None

    @staticmethod
    def build_from(analysis: Analysis) -> "AnalysisViewModel":
        return AnalysisViewModel(
            name=analysis.name,
            value=analysis.value,
            unit=analysis.unit,
            reference_lower=analysis.reference_lower,
            reference_upper=analysis.reference_upper,
        )
