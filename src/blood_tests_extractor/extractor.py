from img2table.document import PDF
from img2table.ocr import TesseractOCR
from img2table.tables.objects.extraction import ExtractedTable

from src.blood_tests_extractor.analysis import Analysis
from src.blood_tests_extractor.analysis_table import AnalysisTable


class Extractor:

    # TODO, they should come from a configuration
    MIN_CONFIDENCE = 30
    LANG = "ita"
    N_THREADS = 4

    @classmethod
    def extract_analyses_from_pdf(cls, file: bytes) -> list[Analysis]:
        tables_per_page = cls.extract_raw_tables_from_pdf(file)
        analyses: list[Analysis] = []

        for extracted_tables in tables_per_page.values():
            for t in extracted_tables:
                analysis_table = AnalysisTable(t)
                if analysis_table.is_analysis_table():
                    for a in analysis_table.analyses:
                        analyses.append(a)

        return analyses

    @classmethod
    def extract_raw_tables_from_pdf(
        cls, file: bytes
    ) -> dict[int, list[ExtractedTable]]:
        pdf = PDF(file, detect_rotation=False, pdf_text_extraction=True)

        ocr = TesseractOCR(n_threads=cls.N_THREADS, lang=cls.LANG)

        return pdf.extract_tables(
            ocr=ocr,
            implicit_rows=False,
            implicit_columns=False,
            borderless_tables=True,
            min_confidence=cls.MIN_CONFIDENCE,
        )
