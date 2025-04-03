from typing import Self

from pydantic import BaseModel

from src.blood_tests_extractor.analysis import Analysis


class AnalysisViewModel(BaseModel):
    name: str
    value: float | None
    unit: str
    reference: str

    @staticmethod
    def build_from(analysis: Analysis) -> "AnalysisViewModel":
        return AnalysisViewModel(
            name=analysis.name,
            value=analysis.value,
            unit=analysis.unit,
            reference=analysis.reference,
        )
