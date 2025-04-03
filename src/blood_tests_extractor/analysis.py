from dataclasses import dataclass
from functools import cached_property


@dataclass
class Analysis:
    """Data related to a single analysis"""

    original_name: str
    original_value: str
    original_unit: str
    original_reference: str

    @cached_property
    def name(self) -> str:
        return self.original_name

    @cached_property
    def value(self) -> float | None:
        try:
            return float(self.original_value.replace(",", "."))
        except ValueError:
            return None

    @cached_property
    def unit(self) -> str:
        return self.original_unit

    @cached_property
    def reference(self) -> str:
        return self.original_reference
