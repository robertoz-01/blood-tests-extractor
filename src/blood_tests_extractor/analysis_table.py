from functools import cached_property

from img2table.tables.objects.extraction import ExtractedTable, TableCell

from .analysis import Analysis
from .analysis_cell import AnalysisCell


class AnalysisTable:
    CONFIDENCE_THRESHOLD = 0.7

    def __init__(self, extracted_table: ExtractedTable):
        self._extracted_table = extracted_table

    def is_analysis_table(self) -> bool:
        if not self.has_expected_columns_number():
            return False

        return (
            self.name_col is not None
            and self.value_col is not None
            and self.unit_col is not None
            and self.reference_col is not None
        )

    def has_expected_columns_number(self):
        return self.table_width is not None and self.table_width in [4, 5]

    @cached_property
    def name_col(self) -> int | None:
        return self.find_column_by_condition(
            lambda analysis_cell: analysis_cell.has_analysis_name()
        )

    @cached_property
    def value_col(self) -> int | None:
        return self.find_column_by_condition(
            lambda analysis_cell: len(analysis_cell.extract_numbers()) == 1
        )

    @cached_property
    def reference_col(self) -> int | None:
        return self.find_column_by_condition(
            lambda analysis_cell: (
                len(analysis_cell.extract_numbers()) >= 1
                and analysis_cell.has_range_symbol()
            )
        )

    def find_column_by_condition(self, condition):
        for column_idx in range(self.table_width):
            name_cells = filter(
                lambda row: condition(AnalysisCell(row[column_idx])),
                self.rows,
            )

            rows_number = len(self.rows)
            if rows_number > 1:
                # exclude the first row, that might be a header
                rows_number -= 1

            if len(list(name_cells)) / rows_number > self.CONFIDENCE_THRESHOLD:
                return column_idx
        return None

    @cached_property
    def unit_col(self) -> int | None:
        return self.find_column_by_condition(
            lambda analysis_cell: analysis_cell.has_unit()
        )

    @cached_property
    def table_width(self) -> int | None:
        """
        :return: The table width if all the rows have the same number of cells. Otherwise, None.
        """
        widths = set()
        for row in self.rows:
            widths.add(len(row))
        if len(widths) != 1:
            return None

        return widths.pop()

    @cached_property
    def rows(self) -> list[list[TableCell]]:
        all_rows = self._extracted_table.content.values()
        useful_rows: list[list[TableCell]] = []
        for row in all_rows:
            if len(list(filter(lambda cell: cell.value, row))) / len(row) > 0.5:
                useful_rows.append(row)

        return useful_rows

    @cached_property
    def analyses(self) -> list[Analysis]:
        complete_analyses: list[Analysis] = []
        for row in self.rows:
            if (
                row[self.value_col].value
                and row[self.unit_col].value
                and row[self.reference_col].value
                and row[self.name_col].value
            ):
                entry = Analysis(
                    original_name=row[self.name_col].value,
                    original_value=row[self.value_col].value,
                    original_unit=row[self.unit_col].value,
                    original_reference=row[self.reference_col].value,
                )
                complete_analyses.append(entry)
        return complete_analyses
