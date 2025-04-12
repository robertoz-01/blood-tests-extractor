import re
from dataclasses import dataclass
from functools import cached_property

from src.blood_tests_extractor import parser


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

    @cached_property
    def reference_lower(self) -> float | None:
        numbers = parser.extract_numbers(self.reference)
        if len(numbers) == 1 and self._has_lower_bound_reference():
            return numbers[0]
        elif len(numbers) == 2 and self._has_range_reference():
            return numbers[0]
        else:
            return None

    @cached_property
    def reference_upper(self) -> float | None:
        numbers = parser.extract_numbers(self.reference)
        if len(numbers) == 1 and self._has_upper_bound_reference():
            return numbers[0]
        elif len(numbers) == 2 and self._has_range_reference():
            return numbers[1]
        else:
            return None

    def _has_upper_bound_reference(self):
        return re.match(r"^\s*<", self.reference)

    def _has_lower_bound_reference(self):
        return re.match(r"^\s*>", self.reference)

    def _has_range_reference(self):
        return re.match(r"\d+.*-.*\d+", self.reference)
