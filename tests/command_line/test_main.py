import os
import unittest
from pathlib import Path

from lxml import html

from src.command_line.__main__ import main


class TestMain(unittest.TestCase):
    def setUp(self):
        os.remove(TestMain.output_file())

    def test_main(self):
        main(self.blood_check_pdf_filename())

        parsed_result = html.parse(TestMain.output_file())

        extracted_tables = parsed_result.xpath('//table[@class="extracted_table"]')
        self.assertEqual(1, len(extracted_tables))

        analyses = extracted_tables[0].xpath("./tbody/tr")
        self.assertEqual(20, len(analyses))

        first_analysis = [cell.text for cell in analyses[0].xpath("./td")]

        self.assertEqual("GLOBULI BIANCHI", first_analysis[0])
        self.assertEqual("6,73", first_analysis[1])
        self.assertEqual("x10^3/μl", first_analysis[2])
        self.assertEqual("4,00 - 9,50", first_analysis[3])

    @staticmethod
    def blood_check_pdf_filename() -> str:
        return f"{TestMain.this_path()}/../data/fake-blood-check.pdf"

    @staticmethod
    def output_file() -> str:
        return (
            f"{TestMain.this_path()}/../../examples/output/fake-blood-check/tables.html"
        )

    @staticmethod
    def this_path():
        return os.path.dirname(os.path.abspath(__file__))
