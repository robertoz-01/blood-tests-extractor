import unittest
from collections import OrderedDict

from img2table.tables.objects.extraction import ExtractedTable, BBox, TableCell

from extract_table.analysis_table import AnalysisTable

bbox = BBox(0, 0, 100, 100)
title = None

analysis_row_1 = [
    TableCell(bbox=bbox, value="EOSINOFILI"),
    TableCell(bbox=bbox, value="1,5"),
    TableCell(bbox=bbox, value="%"),
    TableCell(bbox=bbox, value="0,7 - 4,7"),
    TableCell(bbox=bbox, value=None),
]

analysis_row_2 = [
    TableCell(bbox=bbox, value="BASOFILI"),
    TableCell(bbox=bbox, value="0,6"),
    TableCell(bbox=bbox, value="%"),
    TableCell(bbox=bbox, value="0,0 - 1,1"),
    TableCell(bbox=bbox, value=None),
]

analysis_row_unknown_name = [
    TableCell(bbox=bbox, value="blah-blah"),
    TableCell(bbox=bbox, value="0,6"),
    TableCell(bbox=bbox, value="%"),
    TableCell(bbox=bbox, value="0,0 - 1,1"),
    TableCell(bbox=bbox, value=None),
]

analysis_row_3 = [
    TableCell(bbox=bbox, value="(Sg)Er-EMOGLOBINA"),
    TableCell(bbox=bbox, value="11.0 *"),
    TableCell(bbox=bbox, value="g/dL"),
    TableCell(bbox=bbox, value="13.0 - 17.5"),
]

wrong_analysis_row = [
    TableCell(bbox=bbox, value="BASOFILI"),
    TableCell(bbox=bbox, value="0,6"),
    TableCell(bbox=bbox, value="**EXTRA UNKNOWN VALUE**"),
    TableCell(bbox=bbox, value="%"),
    TableCell(bbox=bbox, value="0,0 - 1,1"),
    TableCell(bbox=bbox, value=None),
]


class TestStringMethods(unittest.TestCase):
    def test_is_analysis_table_false_when_different_width(self):
        content = OrderedDict([(1, analysis_row_1), (2, wrong_analysis_row)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertFalse(at.is_analysis_table())

    def test_is_analysis_table_true_when_all_widths_are_5(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_2)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertTrue(at.is_analysis_table())

    def test_is_analysis_table_true_when_all_widths_are_4(self):
        content = OrderedDict([(1, analysis_row_3)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertTrue(at.is_analysis_table())

    def test_is_analysis_table_true_when_all_widths_are_not_4_or_5(self):
        content = OrderedDict([(1, wrong_analysis_row)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertFalse(at.is_analysis_table())

    def test_name_col(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_2)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertEqual(0, at.name_col)

    def test_name_col_missing(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_unknown_name)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertEqual(None, at.name_col)

    def test_value_col(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_2)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertEqual(1, at.value_col)

    def test_reference_col(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_2)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertEqual(3, at.reference_col)

    def test_unit_col(self):
        content = OrderedDict([(1, analysis_row_1), (2, analysis_row_2)])

        at = AnalysisTable(ExtractedTable(bbox, title, content))
        self.assertEqual(2, at.unit_col)
