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
        self.assertEqual(parties["Movimiento Ciudadano"]["total"], 316)
        self.assertEqual(parties["Morena"]["total"], 288)
        self.assertEqual(parties["PAN"]["cobertura"], "parcial")
        self.assertIsNone(parties["PAN"]["campana"])
        self.assertIn("no se verificó", data["designaciones"]["conclusion"].lower())
        self.assertGreaterEqual(
            sum(1 for item in sources if item["autoridad"] == "INE"),
            4,
        )
        self.assertGreaterEqual(
            sum(1 for item in sources if item["autoridad"] == "TEPJF"),
            3,
        )

    def test_html_contains_twelve_page_analysis_and_montserrat(self) -> None:
        html = HTML_PATH.read_text(encoding="utf-8")

        self.assertEqual(html.count('class="page '), 12)
        self.assertIn("Movimiento Ciudadano", html)
        self.assertIn("316", html)
        self.assertIn("SUP-RAP-342/2024", html)
        self.assertIn("SM-RAP-168/2024", html)
        self.assertIn("Insaculación", html)
        self.assertIn("cédula secreta", html)
        self.assertIn("Montserrat-Regular.ttf", html)
        self.assertNotIn("assets/pagina-", html)

    def test_tepjf_outcome_uses_audited_thirty_seven_conclusions(self) -> None:
        html = HTML_PATH.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        findings = (
            ROOT / "research" / "HALLAZGOS_AUDITABLES.md"
        ).read_text(encoding="utf-8")

        for text in (html, readme, findings):
            self.assertIn("30", text)
            self.assertRegex(text, r"\b7\b|siete")
            self.assertNotRegex(
                text,
                r"revoc[óa]\s+seis|seis\s+revocadas|"
                r"<strong>6</strong><span>Conclusiones revocadas",
            )
        self.assertIn("revocadas para efectos", html)

    def test_pdf_is_letter_landscape_with_selectable_text(self) -> None:
        document = fitz.open(PDF_PATH)
        self.assertEqual(document.page_count, 12)
        self.assertTrue(
            all(page.rect == fitz.Rect(0, 0, 792, 612) for page in document)
        )
        report_text = "".join(page.get_text() for page in document)
        embedded_fonts = {
            font[3]
            for page in document
            for font in page.get_fonts(full=True)
        }
        self.assertIn("Movimiento Ciudadano", report_text)
        self.assertIn("SUP-RAP-342/2024", report_text)
        self.assertIn("insaculación", report_text.lower())
        self.assertIn("cédula secreta", report_text.lower())
        self.assertTrue(any("Montserrat" in name for name in embedded_fonts))


if __name__ == "__main__":
    unittest.main()
