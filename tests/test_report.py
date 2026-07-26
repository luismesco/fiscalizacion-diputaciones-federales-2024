import json
from pathlib import Path
import unittest

import fitz


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "analisis_pef_2023_2024.json"
HTML_PATH = ROOT / "index.html"
PDF_PATH = ROOT / "reporte_observaciones_pef_2023_2024.pdf"


class ReportDataTests(unittest.TestCase):
    def test_party_counts_and_source_coverage(self) -> None:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        parties = data["partidos"]
        sources = data["fuentes"]

        self.assertEqual(len(parties), 7)
        self.assertEqual(parties["Morena"]["total"], 194)
        self.assertEqual(parties["Movimiento Ciudadano"]["total"], 121)
        self.assertGreaterEqual(
            sum(1 for item in sources if item["autoridad"] == "INE"),
            4,
        )
        self.assertGreaterEqual(
            sum(1 for item in sources if item["autoridad"] == "TEPJF"),
            3,
        )

    def test_html_contains_new_nine_page_analysis(self) -> None:
        html = HTML_PATH.read_text(encoding="utf-8")

        self.assertEqual(html.count('class="page '), 9)
        self.assertIn("Morena", html)
        self.assertIn("194", html)
        self.assertIn("SUP-RAP-413/2024", html)
        self.assertIn("SUP-RAP-104/2025", html)
        self.assertIn("Conclusión 7_C75_FD", html)
        self.assertNotIn("assets/pagina-", html)

    def test_pdf_is_letter_landscape_with_selectable_text(self) -> None:
        document = fitz.open(PDF_PATH)
        self.assertEqual(document.page_count, 9)
        self.assertEqual(document[0].rect, fitz.Rect(0, 0, 792, 612))
        report_text = "".join(page.get_text() for page in document)
        self.assertIn("Morena", report_text)
        self.assertIn("SUP-RAP-104/2025", report_text)


if __name__ == "__main__":
    unittest.main()
