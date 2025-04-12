import unittest

from src.blood_tests_extractor.analysis import Analysis


class TestAnalysis(unittest.TestCase):
    def test_value(self):
        self.assertEqual(24, self.analysis_with(original_value="24").value)
        self.assertEqual(24.4, self.analysis_with(original_value="24.4").value)
        self.assertEqual(24.4, self.analysis_with(original_value="24,4").value)
        self.assertEqual(None, self.analysis_with(original_value="blah").value)

    def test_reference_only_lower(self):
        analysis = self.analysis_with(original_reference="> 40")
        self.assertEqual(40, analysis.reference_lower)
        self.assertEqual(None, analysis.reference_upper)

    def test_reference_only_upper(self):
        analysis = self.analysis_with(original_reference="< 100.5")
        self.assertEqual(None, analysis.reference_lower)
        self.assertEqual(100.5, analysis.reference_upper)

    def test_reference_lower_and_upper(self):
        analysis = self.analysis_with(original_reference="3,5 - 5,1")
        self.assertEqual(3.5, analysis.reference_lower)
        self.assertEqual(5.1, analysis.reference_upper)

    def test_reference_not_parsable_text(self):
        analysis = self.analysis_with(
            original_reference="< 20 carenza 21 – 29 insufficienza 30 – 100 sufficienza"
        )
        self.assertEqual(None, analysis.reference_lower)
        self.assertEqual(None, analysis.reference_upper)

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
