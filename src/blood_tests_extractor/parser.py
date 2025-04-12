import re


def extract_numbers(text: str) -> list[float]:
    values = re.split(r"[^,.\d]+", text)
    raw_numbers = filter(
        lambda v: v is not None and re.match(r"\d+([,.]\d+)?", v), values
    )
    return list(map(lambda raw: float(raw.replace(",", ".")), raw_numbers))
