from img2table.tables.objects.extraction import TableCell
import re


class AnalysisCell:
    RANGE_SYMBOL_REGEX = re.compile(r"[><-]", re.UNICODE)
    UNIT_DICTIONARY = {
        "%",
        "#",
        "l",
        "dl",
        "g",
        "fl",
        "pg",
        "µl",
        "mg",
        "u",
        "mmol",
        "ng",
    }
    ANALYSIS_NAME_DICTIONARY = {
        "hemoglobin",
        "leucociti",
        "globuli bianchi",
        "globuli rossi",
        "eritrociti",
        "emoglobina",
        "ematocrito",
        "mch",
        "mcv",
        "mchc",
        "mpv",
        "piastrine",
        "neutrofili",
        "linfociti",
        "eosinofili",
        "basofili",
        "glucosio",
        "creatinina",
        "urato",
        "glutammiltransferasi",
        "colesterolo hdl",
        "trigliceridi",
        "bilirubina totale",
        "bilirubina diretta",
        "ast",
        "albumina",
        "alfa 1",
        "alfa 2",
        "beta 1",
        "beta 2",
        "tpsa",
        "proteina c reattiva",
        "p.c.r.",
        "tsh",
        "tireotropina",
        "colesterolo",
        "trigliceridi",
        "vitamina d",
        "sideremia",
        "ferritina",
        "potassiemia",
        "sodiemia",
    }
    ANALYSIS_NAME_REGEX = re.compile(
        f".*({"|".join(map(lambda name: f"({name})", ANALYSIS_NAME_DICTIONARY))}).*",
        flags=re.IGNORECASE,
    )

    def __init__(self, table_cell: TableCell):
        self.cell_value = (table_cell.value or "").lower()
        self.tokens = re.split(r"[\s+/]", self.cell_value)
        self.tokens = set(filter(lambda v: v is not None and v != "", self.tokens))

    def extract_numbers(self) -> list[float]:
        values = re.split(r"[^,.\d]+", self.cell_value)
        raw_numbers = filter(
            lambda v: v is not None and re.match(r"\d+([,.]\d+)?", v), values
        )
        return list(map(lambda raw: float(raw.replace(",", ".")), raw_numbers))

    def has_range_symbol(self) -> bool:
        return self.RANGE_SYMBOL_REGEX.search(self.cell_value) is not None

    def has_unit(self) -> bool:
        return len(self.tokens.intersection(self.UNIT_DICTIONARY)) > 0

    def has_analysis_name(self) -> bool:
        return self.ANALYSIS_NAME_REGEX.match(self.cell_value) is not None
