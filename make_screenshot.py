# Run with: .venv/bin/python3 make_screenshot.py
"""Generate screenshot.svg — a headless capture of the Browser Dispatch TUI."""

import asyncio
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Load the main script as a module by exec-ing it in a controlled namespace.
# We skip the bootstrap block because we're already running in the venv.
# ---------------------------------------------------------------------------
SCRIPT = Path(__file__).parent / "browser-dispatch"
src = SCRIPT.read_text()

# Exec the full source. The bootstrap block checks sys.prefix against VENV_DIR;
# since we're already running from the venv, the check is False and os.execv
# is never called. main() is guarded by __name__ == "__main__" which we mask.
ns: dict = {"__name__": "__not_main__", "__file__": str(SCRIPT)}
exec(compile(src, str(SCRIPT), "exec"), ns)

BrowserDispatchApp = ns["BrowserDispatchApp"]

# ---------------------------------------------------------------------------
# Subclass the app to inject sample data without touching the real config.
# ---------------------------------------------------------------------------
SAMPLE_CONFIG = {
    "default_browser": "Firefox",
    "previous_default": "",
    "rules": [
        {"pattern": "*.google.com",    "type": "glob",  "browser": "Brave"},
        {"pattern": "*.youtube.com",   "type": "glob",  "browser": "Brave"},
        {"pattern": "*.work.internal", "type": "glob",  "browser": "Firefox"},
        {"pattern": "^jira\\.",        "type": "regex", "browser": "Firefox"},
    ],
}

SAMPLE_BROWSERS = {
    "Brave":   {"name": "Brave",   "exec": "brave",   "exec_args": ["brave"],   "desktop_file": "brave-browser.desktop"},
    "Firefox": {"name": "Firefox", "exec": "firefox", "exec_args": ["firefox"], "desktop_file": "firefox.desktop"},
}


class ScreenshotApp(BrowserDispatchApp):
    def __init__(self) -> None:
        super().__init__()
        self.config = SAMPLE_CONFIG.copy()
        self.config["rules"] = list(SAMPLE_CONFIG["rules"])
        self.browsers = SAMPLE_BROWSERS.copy()


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------
OUTPUT = Path(__file__).parent / "screenshot.svg"


async def capture() -> None:
    app = ScreenshotApp()
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.pause(0.5)      # let layout settle
        svg = app.export_screenshot()
    OUTPUT.write_text(svg)
    print(f"Saved {OUTPUT}  ({OUTPUT.stat().st_size:,} bytes)")


asyncio.run(capture())
