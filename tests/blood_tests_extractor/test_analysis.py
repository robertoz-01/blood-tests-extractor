import unittest

from src.blood_tests_extractor.analysis import Analysis


class TestAnalysisCell(unittest.TestCase):
    def test_value(self):
        self.assertEqual(24, self.analysis_with(original_value="24").value)
        self.assertEqual(24.4, self.analysis_with(original_value="24.4").value)
        self.assertEqual(24.4, self.analysis_with(original_value="24,4").value)
        self.assertEqual(None, self.analysis_with(original_value="blah").value)

    @staticmethod
    def analysis_with(
        original_name="Hemoglobin",
        original_value="12",
        original_unit="mL",
        original_reference=">3",
    ) -> Analysis:
        return Analysis(
            original_name, original_value, original_unit, original_reference
        )
