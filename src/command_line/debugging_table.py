from img2table.tables.objects.extraction import ExtractedTable

from src.blood_tests_extractor.analysis_table import AnalysisTable


class DebuggingTable(AnalysisTable):
    def __init__(self, extracted_table: ExtractedTable, page_nb: int, table_idx: int):
        super().__init__(extracted_table)
        self.page_nb = page_nb
        self.table_idx = table_idx
        self.html_table = extracted_table.html
        self.title = extracted_table.title
