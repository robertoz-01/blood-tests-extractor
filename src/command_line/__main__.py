import os, glob
from pathlib import Path

from img2table.tables.objects.extraction import ExtractedTable
from jinja2 import Environment, FileSystemLoader

from src.blood_tests_extractor.analysis_table import AnalysisTable
from src.blood_tests_extractor.extractor import Extractor


# Add some debugging information on top of AnalysisTable
class DebuggingTable(AnalysisTable):
    def __init__(self, extracted_table: ExtractedTable, page_nb: int, table_idx: int):
        super().__init__(extracted_table)
        self.page_nb = page_nb
        self.table_idx = table_idx
        self.html_table = extracted_table.html
        self.title = extracted_table.title


#
# Setup path variables
#

this_path = os.path.dirname(os.path.abspath(__file__))
project_path = f"{this_path}/../.."
example_input_file = f"{project_path}/examples/input/RZ.pdf"
# example_input_file = f"{project_path}/examples/input/AZ.pdf"
file_name = Path(example_input_file).stem
output_path = f"{project_path}/examples/output/{file_name}"
with open(example_input_file, "r+b") as f:
    pdf_bytes = f.read()

#
# Function definitions
#


def prepare_output_path():
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for output_file in glob.glob(f"{output_path}/*.html"):
        os.remove(output_file)


def build_debugging_tables(
    page_and_tables: dict[int, list[ExtractedTable]],
) -> list[DebuggingTable]:
    debugging_tables: list[DebuggingTable] = []
    for page_nb, tables in page_and_tables.items():
        for idx, t in enumerate(tables):
            debugging_tables.append(DebuggingTable(t, page_nb, idx))
    return debugging_tables


def render_tables_to_html(debugging_tables: list[DebuggingTable]):
    environment = Environment(
        loader=FileSystemLoader(f"{project_path}/examples/output_templates/")
    )
    template = environment.get_template("tables.html.jinja")

    content = template.render(tables=debugging_tables, title=file_name)
    with open(f"{output_path}/tables.html", mode="w", encoding="utf-8") as message:
        message.write(content)


#
# Run it!
#

prepare_output_path()
extracted_tables = Extractor.extract_raw_tables_from_pdf(pdf_bytes)
render_tables_to_html(build_debugging_tables(extracted_tables))
