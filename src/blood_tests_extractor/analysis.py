from dataclasses import dataclass
from functools import cached_property


@dataclass
class Analysis:
    """Data related to a single analysis"""

    original_name: str
    original_value: str
    original_unit: str
    original_reference: str

    # TODO, the following methods needs to be implemented parsing the original properties

    @cached_property
    def name(self):
        return self.original_name

    @cached_property
    def value(self):
        return self.original_value

    @cached_property
    def reference(self):
        return self.original_reference

    @cached_property
    def unit(self):
        return self.original_unit
