import unittest

from src.blood_tests_extractor.analysis import Analysis
from src.http_api.analysis_view_model import AnalysisViewModel


class TestAnalysisCell(unittest.TestCase):
    def test_value(self):
        analysis = Analysis(
            original_name="Hemoglobin",
            original_value="16",
            original_unit="g/dl",
            original_reference="14.1 - 18.5",
        )
        view_model = AnalysisViewModel.build_from(analysis)
        self.assertEqual("Hemoglobin", view_model.name)
        self.assertEqual(16, view_model.value)
        self.assertEqual("g/dl", view_model.unit)
        self.assertEqual("14.1 - 18.5", view_model.reference)
