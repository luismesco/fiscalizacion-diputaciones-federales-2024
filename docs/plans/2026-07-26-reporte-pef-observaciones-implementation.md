# Reporte de observaciones del PEF 2023–2024 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reemplazar el facsímil publicado por un reporte analítico editable de nueve páginas que responda A/B/C con fuentes oficiales y conserve la identidad gráfica del referente.

**Architecture:** El sitio será un HTML autónomo con CSS de impresión para carta horizontal y contenido seleccionable. Los datos comparativos y fuentes se conservarán en un JSON legible por máquina; una prueba validará conteos, estructura, enlaces y número de páginas del PDF generado por Chrome.

**Tech Stack:** HTML5, CSS3, JSON, Python 3, PyMuPDF, Google Chrome headless, Git y GitHub Pages.

---

### Task 1: Matriz de datos y fuentes

**Files:**
- Create: `data/analisis_pef_2023_2024.json`
- Create: `tests/test_report.py`

**Step 1: Write the failing test**

Crear una prueba que cargue el JSON, confirme siete partidos y verifique:

```python
assert partidos["Morena"]["total"] == 194
assert partidos["Movimiento Ciudadano"]["total"] == 121
assert sum(1 for item in fuentes if item["autoridad"] == "INE") >= 4
assert sum(1 for item in fuentes if item["autoridad"] == "TEPJF") >= 3
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: FAIL because `data/analisis_pef_2023_2024.json` does not exist.

**Step 3: Write minimal data file**

Registrar por partido los conteos de precampaña, campaña y total:

```json
{
  "Morena": {"precampana": 26, "campana": 168, "total": 194},
  "Movimiento Ciudadano": {"precampana": 21, "campana": 100, "total": 121},
  "PAN": {"precampana": 25, "campana": 91, "total": 116},
  "PT": {"precampana": 7, "campana": 99, "total": 106},
  "PRD": {"precampana": 14, "campana": 83, "total": 97},
  "PRI": {"precampana": 26, "campana": 65, "total": 91},
  "PVEM": {"precampana": 16, "campana": 65, "total": 81}
}
```

Añadir INE/CG212/2024, INE/CG213/2024, INE/CG1928/2024,
INE/CG1929/2024, SUP-RAP-88/2024, SUP-RAP-413/2024,
INE/CG319/2025 y SUP-RAP-104/2025 con URL oficial.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: PASS for data counts and source coverage.

**Step 5: Commit**

```bash
git add data/analisis_pef_2023_2024.json tests/test_report.py
git commit -m "data: registrar análisis federal de fiscalización"
```

### Task 2: HTML editorial de nueve páginas

**Files:**
- Modify: `index.html`
- Modify: `tests/test_report.py`

**Step 1: Extend the failing test**

Comprobar que el HTML contiene nueve elementos `.page`, texto seleccionable y
las claves:

```python
assert html.count('class="page') == 9
assert "Morena" in html
assert "194" in html
assert "SUP-RAP-413/2024" in html
assert "SUP-RAP-104/2025" in html
assert "Conclusión 7_C75_FD" in html
assert "assets/pagina-" not in html
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: FAIL because the current page is an image facsimile.

**Step 3: Implement the report**

Reemplazar `index.html` con nueve secciones fijas que sigan el diseño aprobado.
Usar:

```css
@page { size: letter landscape; margin: 0; }
.page { width: 11in; height: 8.5in; break-after: page; overflow: hidden; }
@media print { .download-pdf { display: none; } }
```

Incluir:

- portada;
- metodología;
- ranking;
- respuestas A, B y C;
- coaliciones;
- inventario documental;
- fuentes y límites.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: PASS for nine pages, required findings and editable text.

**Step 5: Commit**

```bash
git add index.html tests/test_report.py
git commit -m "feat: crear reporte editorial del PEF 2023-2024"
```

### Task 3: Conversión y validación del PDF

**Files:**
- Create: `scripts/build_pdf.sh`
- Create: `reporte_observaciones_pef_2023_2024.pdf`
- Modify: `tests/test_report.py`
- Delete: `reporte_desde_html.pdf`

**Step 1: Extend the failing test**

Validar con PyMuPDF:

```python
doc = fitz.open("reporte_observaciones_pef_2023_2024.pdf")
assert doc.page_count == 9
assert all(page.rect == fitz.Rect(0, 0, 792, 612) for page in doc)
assert "Morena" in "".join(page.get_text() for page in doc)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: FAIL because the corrected PDF has not been generated.

**Step 3: Implement PDF build**

El script ejecutará Chrome headless:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/reporte_observaciones_pef_2023_2024.pdf" \
  "file://$PWD/index.html"
```

Actualizar el botón HTML para descargar ese archivo.

**Step 4: Run build and tests**

Run:

```bash
bash scripts/build_pdf.sh
python3 -m unittest tests/test_report.py -v
```

Expected: PDF de nueve páginas, tamaño carta horizontal y pruebas PASS.

**Step 5: Commit**

```bash
git add index.html scripts/build_pdf.sh tests/test_report.py reporte_observaciones_pef_2023_2024.pdf
git rm reporte_desde_html.pdf
git commit -m "build: generar PDF del análisis de observaciones"
```

### Task 4: Revisión visual

**Files:**
- Create: `artifacts/revision/page-01.png`
- Create: `artifacts/revision/page-03.png`
- Create: `artifacts/revision/page-05.png`
- Create: `artifacts/revision/page-09.png`

**Step 1: Render representative pages**

Usar PyMuPDF para renderizar páginas 1, 3, 5 y 9 a 144 dpi.

**Step 2: Inspect images**

Verificar:

- ausencia de desbordamientos;
- identidad gráfica consistente;
- tablas legibles;
- pies y numeración correctos;
- URLs sin cortar información esencial.

**Step 3: Correct defects**

Ajustar solo reglas CSS o densidad de texto necesarias y regenerar el PDF.

**Step 4: Run full verification**

Run: `python3 -m unittest tests/test_report.py -v`

Expected: all tests PASS.

**Step 5: Commit**

```bash
git add index.html reporte_observaciones_pef_2023_2024.pdf artifacts/revision/
git commit -m "fix: ajustar legibilidad del reporte publicado"
```

### Task 5: Sustituir GitHub Pages

**Files:**
- Modify: `README.md`
- Delete: `assets/pagina-01.png` through `assets/pagina-09.png`
- Delete: `que_se_sanciono_diputaciones_federales_2024.pdf`

**Step 1: Update README**

Explicar que el repositorio contiene el análisis PEF completo y enlazar el nuevo
PDF.

**Step 2: Remove obsolete facsimile assets**

Eliminar del repositorio público las imágenes y PDF que hicieron pasar el
referente por el producto final.

**Step 3: Verify clean repository**

Run:

```bash
git status --short
python3 -m unittest tests/test_report.py -v
```

Expected: only intended README/removal changes, tests PASS.

**Step 4: Commit and push**

```bash
git add README.md
git rm -r assets que_se_sanciono_diputaciones_federales_2024.pdf
git commit -m "docs: sustituir facsímil por análisis de fiscalización"
git push origin main
```

**Step 5: Verify GitHub Pages**

Confirmar build `built` y respuestas HTTP 200 para:

- `/`
- `/reporte_observaciones_pef_2023_2024.pdf`

