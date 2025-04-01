import unittest

from img2table.tables.objects.extraction import TableCell, BBox

from src.blood_tests_extractor.analysis_cell import AnalysisCell


class TestAnalysisCell(unittest.TestCase):
    def test_extract_number(self):
        self.assertEqual([12], self.cell_with("12").extract_numbers())
        self.assertEqual([12.3], self.cell_with("12.3").extract_numbers())
        self.assertEqual([12.323], self.cell_with("12,323").extract_numbers())
        self.assertEqual([1], self.cell_with("1").extract_numbers())
        self.assertEqual([12.3, 12], self.cell_with("12,3 12").extract_numbers())
        self.assertEqual([12.3, 12], self.cell_with("12,3 - 12").extract_numbers())
        self.assertEqual([], self.cell_with("Hemoglobin").extract_numbers())
        self.assertEqual([], self.cell_with("#").extract_numbers())
        self.assertEqual([], self.cell_with("").extract_numbers())
        self.assertEqual([], self.cell_with(None).extract_numbers())

    def test_has_range_symbol(self):
        self.assertFalse(self.cell_with("Hemoglobin").has_range_symbol())
        self.assertTrue(self.cell_with("< 30.3").has_range_symbol())
        self.assertTrue(self.cell_with("12,3 - 12").has_range_symbol())
        self.assertFalse(self.cell_with("#").has_range_symbol())
        self.assertFalse(self.cell_with("").has_range_symbol())
        self.assertFalse(self.cell_with(None).has_range_symbol())

    def test_has_unit(self):
        self.assertTrue(self.cell_with("#").has_unit())
        self.assertTrue(self.cell_with("mg").has_unit())
        self.assertTrue(self.cell_with("x10^6/µl").has_unit())
        self.assertTrue(self.cell_with("g/dl").has_unit())
        self.assertTrue(self.cell_with("10^9/L").has_unit())
        self.assertFalse(self.cell_with("Hemoglobin").has_unit())
        self.assertFalse(self.cell_with("").has_unit())
        self.assertFalse(self.cell_with("12,3 - 12").has_unit())

    def test_has_analysis_name(self):
        self.assertTrue(self.cell_with("Hemoglobin").has_analysis_name())
        self.assertTrue(self.cell_with("hemoglobin").has_analysis_name())
        self.assertTrue(self.cell_with("globuli bianchi").has_analysis_name())
        self.assertTrue(self.cell_with("mchc").has_analysis_name())
        self.assertFalse(self.cell_with("12,3 - 12").has_analysis_name())
        self.assertFalse(self.cell_with("%").has_analysis_name())
        self.assertFalse(self.cell_with(None).has_analysis_name())

    @staticmethod
    def cell_with(value: str | None) -> AnalysisCell:
        bbox = BBox(0, 0, 10, 10)
        return AnalysisCell(TableCell(bbox=bbox, value=value))
