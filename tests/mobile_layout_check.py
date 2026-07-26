from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
HTML_URL = (ROOT / "index.html").as_uri()
SCREENSHOT_DIR = Path("/private/tmp/fiscalizacion-mobile-review")
VIEWPORTS = (
    ("iphone-13", 390, 844),
    ("iphone-15-pro-max", 430, 932),
)


def main() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)

        for name, width, height in VIEWPORTS:
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                is_mobile=True,
            )
            page.goto(HTML_URL)
            page.wait_for_load_state("networkidle")

            metrics = page.evaluate(
                """() => ({
                    viewportWidth: document.documentElement.clientWidth,
                    documentWidth: document.documentElement.scrollWidth,
                    bodyWidth: document.body.scrollWidth,
                    pageWidths: [...document.querySelectorAll('.page')]
                        .map((node) => Math.ceil(node.getBoundingClientRect().width)),
                    overflowingElements: [...document.querySelectorAll('body *')]
                        .filter((node) => {
                            const rect = node.getBoundingClientRect();
                            return rect.right > document.documentElement.clientWidth + 1
                                || rect.left < -1;
                        })
                        .slice(0, 10)
                        .map((node) => node.className || node.tagName)
                })"""
            )

            page.screenshot(
                path=str(SCREENSHOT_DIR / f"mobile-{name}-viewport.png"),
                full_page=False,
            )
            page.screenshot(
                path=str(SCREENSHOT_DIR / f"mobile-{name}-full.png"),
                full_page=True,
            )
            page.close()

            if metrics["documentWidth"] > metrics["viewportWidth"] + 1:
                failures.append(f"{name}: document overflow {metrics}")
            if any(page_width > metrics["viewportWidth"] + 1 for page_width in metrics["pageWidths"]):
                failures.append(f"{name}: fixed-width page {metrics}")
            if metrics["overflowingElements"]:
                failures.append(f"{name}: overflowing elements {metrics}")

        desktop_page = browser.new_page(viewport={"width": 1440, "height": 1000})
        desktop_page.goto(HTML_URL)
        desktop_page.wait_for_load_state("networkidle")
        desktop_metrics = desktop_page.locator(".page").first.evaluate(
            """(node) => ({
                width: Math.round(node.getBoundingClientRect().width),
                height: Math.round(node.getBoundingClientRect().height)
            })"""
        )
        desktop_page.screenshot(
            path=str(SCREENSHOT_DIR / "desktop-viewport.png"),
            full_page=False,
        )
        desktop_page.close()

        if desktop_metrics != {"width": 1056, "height": 816}:
            failures.append(f"desktop: report dimensions changed {desktop_metrics}")

        browser.close()

    if failures:
        raise AssertionError("\n".join(failures))

    print(f"Mobile layout passed for {len(VIEWPORTS)} viewports.")


if __name__ == "__main__":
    main()
