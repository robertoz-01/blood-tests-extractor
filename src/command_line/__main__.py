import os, glob
import sys
from pathlib import Path

from img2table.tables.objects.extraction import ExtractedTable
from jinja2 import Environment, FileSystemLoader

from src.command_line.debugging_table import DebuggingTable
from src.blood_tests_extractor.extractor import Extractor

this_path = os.path.dirname(os.path.abspath(__file__))
project_path = f"{this_path}/../.."


def prepare_output_path(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for output_file in glob.glob(f"{output_path}/*.html"):
        os.remove(output_file)


def read_pdf(file_name) -> bytes:
    with open(file_name, "r+b") as f:
        return f.read()


def build_debugging_tables(
    page_and_tables: dict[int, list[ExtractedTable]],
) -> list[DebuggingTable]:
    debugging_tables: list[DebuggingTable] = []
    for page_nb, tables in page_and_tables.items():
        for idx, t in enumerate(tables):
            debugging_tables.append(DebuggingTable(t, page_nb, idx))
    return debugging_tables


def render_tables_to_html(output_path: str, debugging_tables: list[DebuggingTable]):
    environment = Environment(
        loader=FileSystemLoader(f"{project_path}/examples/output_templates/")
    )
    template = environment.get_template("tables.html.jinja")

    file_name = Path(output_path).name
    content = template.render(tables=debugging_tables, title=file_name)
    with open(f"{output_path}/tables.html", mode="w", encoding="utf-8") as message:
        message.write(content)


def main(example_input_file):
    file_name = Path(example_input_file).stem
    output_path = f"{project_path}/examples/output/{file_name}"

    prepare_output_path(output_path)
    pdf_bytes = read_pdf(example_input_file)
    extracted_tables = Extractor.extract_raw_tables_from_pdf(pdf_bytes)
    render_tables_to_html(output_path, build_debugging_tables(extracted_tables))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Missing input file argument\n")
        sys.exit(1)

    main(sys.argv[1])
