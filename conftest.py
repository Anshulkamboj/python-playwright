# from playwright.async_api import async_playwright, Page, expect
# import pytest
# import logging


# @pytest.fixture
# async def page():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         yield page

#         await browser.close()

# @pytest.fixture
# async def logger(request):
#     return logging.getLogger(request.node.name)
    


import logging
from pathlib import Path
import yaml
import pytest
from playwright.async_api import async_playwright
from pytest_html import extras


ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)


@pytest.fixture
def logger(request):
    return logging.getLogger(request.node.name)


@pytest.hookimpl(hookwrapper=True)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Store test result for the fixture
    setattr(item, f"rep_{report.when}", report)

    # Attach artifacts after test teardown
    if report.when == "teardown":
        call_report = getattr(item, "rep_call", None)

        if call_report and call_report.failed:
            report.extras = getattr(report, "extras", [])

            screenshot_path = getattr(item, "screenshot_path", None)
            video_path = getattr(item, "video_path", None)
            trace_path = getattr(item, "trace_path", None)

            # Screenshot attachment
            if screenshot_path and Path(screenshot_path).exists():
                report.extras.append(
                    extras.image(
                        str(Path(screenshot_path).resolve()),
                        name="Screenshot"
                    )
                )

            # Video link
            if video_path and Path(video_path).exists():
                report.extras.append(
                    extras.url(
                        Path(video_path).resolve().as_uri(),
                        name="Video"
                    )
                )

            # Trace link
            if trace_path and Path(trace_path).exists():
                report.extras.append(
                    extras.url(
                        Path(trace_path).resolve().as_uri(),
                        name="Trace"
                    )
                )


@pytest.fixture
async def page(request, browser_name, config):
    async with async_playwright() as p:
        selected_browser = getattr(p, browser_name)
        browser = await selected_browser.launch(headless=True)
        context = await browser.new_context(
            base_url=config["base_url"],
            record_video_dir=str(ARTIFACTS_DIR / "videos")
        )
        page = await context.new_page()
        video = page.video

        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )

        try:
            yield page
        finally:
            call_report = getattr(request.node, "rep_call", None)
            test_failed = call_report is not None and call_report.failed

            if test_failed:
                screenshot_path = (
                    ARTIFACTS_DIR / f"{request.node.name}.png"
                )
                await page.screenshot(path=str(screenshot_path), full_page=True)
                request.node.screenshot_path = str(screenshot_path)

                trace_path = ARTIFACTS_DIR / f"{request.node.name}.zip"
                await context.tracing.stop(path=str(trace_path))
                request.node.trace_path = str(trace_path)
            else:
                await context.tracing.stop()

            await context.close()
            await browser.close()

            if test_failed and video:
                video_path = await video.path()
                request.node.video_path = str(video_path)
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        choices=["dev", "qa", "stage", "prod"],
        help="Environment to run tests against",
    )


@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")

    config_path = (
        Path(__file__).parent
        / "resources"
        / "configs"
        / f"{env}.yaml"
    )

    with config_path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)