from typing import Annotated

from fastapi import FastAPI, File

from src.blood_tests_extractor.extractor import Extractor
from src.http_api.analysis_view_model import AnalysisViewModel

app = FastAPI()


@app.post("/blood-test-pdf")
def extract_from_pdf(file: Annotated[bytes, File()]) -> list[AnalysisViewModel]:
    return [
        AnalysisViewModel.build_from(analysis)
        for analysis in Extractor.extract_analyses_from_pdf(file)
    ]
