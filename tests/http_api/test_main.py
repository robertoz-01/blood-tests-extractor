import os
import unittest

from fastapi.testclient import TestClient
from src.http_api.main import app

client = TestClient(app)


class TestApp(unittest.TestCase):
    def test_post_blood_test_pdf(self):
        with open(self.blood_check_pdf_filename(), "rb") as f:
            response = client.post(
                "/blood-test-pdf", files={"file": ("f.pdf", f, "application/pdf")}
            )

        json_body = response.json()
        self.assertEqual(200, response.status_code)
        self.assertIn(
            {
                "name": "GLOBULI BIANCHI",
                "reference": "4,00 - 9,50",
                "unit": "x10^3/μl",
                "value": 6.73,
            },
            json_body,
        )

        self.assertIn(
            {
                "name": "LINFOCITI",
                "reference": "20,0 - 48,0",
                "unit": "%",
                "value": 33.3,
            },
            json_body,
        )

        self.assertEqual(20, len(json_body))

    @staticmethod
    def blood_check_pdf_filename() -> str:
        this_path = os.path.dirname(os.path.abspath(__file__))
        return f"{this_path}/../data/fake-blood-check.pdf"
