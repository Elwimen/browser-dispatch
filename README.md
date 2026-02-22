# browser-dispatch

A smart browser dispatcher for Linux. Route URLs to different browsers based on domain rules — send work sites to Firefox, Google services to Brave, everything else wherever you want.

Configured through an interactive terminal UI built with [Textual](https://github.com/Textualize/textual).

![Browser Dispatch TUI](https://raw.githubusercontent.com/Elwimen/browser-dispatch/main/screenshot.svg)

## Features

- **Domain rules** — glob patterns (`*.google.com`) or full regex (`^mail\.google\.com$`)
- **Priority ordering** — rules are matched top-to-bottom; drag to reorder with `Ctrl+↑/↓`
- **Live URL testing** — press `t` to test any URL and see which browser would handle it
- **One-click install** — registers itself as the system default browser via xdg
- **Self-bootstrapping** — automatically creates a `.venv` and installs dependencies on first run
- **Cross-distro** — works on any Linux distro that uses xdg-open (Manjaro, Ubuntu, Fedora, Arch, etc.)

## Requirements

- Python 3.8+
- `xdg-utils` (pre-installed on most desktop Linux distros)

No other dependencies needed — the script sets up its own virtual environment on first run.

## Installation

```bash
git clone https://github.com/Elwimen/browser-dispatch.git
cd browser-dispatch
chmod +x browser-dispatch
./browser-dispatch --config
```

On first run it will create a `.venv/` and install [Textual](https://github.com/Textualize/textual) automatically, then open the configuration UI.

## Usage

```bash
# Open the configuration TUI
./browser-dispatch --config

# Dispatch a URL (called automatically by xdg-open once installed)
./browser-dispatch https://example.com
```

### TUI keybindings

| Key | Action |
|-----|--------|
| `a` | Add a new rule |
| `e` | Edit selected rule |
| `d` | Delete selected rule |
| `Ctrl+↑` / `Ctrl+↓` | Move rule up / down |
| `t` | Test a URL against current rules |
| `i` | Install as system default browser |
| `u` | Uninstall (restores previous default) |
| `q` | Quit |

## How it works

### Rule matching

Rules are evaluated in order — the first match wins. Each rule has:

- **Pattern** — a glob (`*.example.com`) or regex (`^(mail|drive)\.google\.com$`) matched against the hostname
- **Browser** — which installed browser to open the URL in

URLs that match no rule go to the **default browser**.

### System integration

Pressing `i` in the TUI:

1. Writes `~/.local/share/applications/browser-dispatch.desktop`
2. Sets `x-scheme-handler/http` and `x-scheme-handler/https` in `~/.config/mimeapps.list`
3. Calls `xdg-settings set default-web-browser browser-dispatch.desktop`

After that, any link you click anywhere on the desktop routes through browser-dispatch. Pressing `u` reverses all of this and restores your previous default browser.

### Config file

Rules are stored in `~/.config/browser-dispatch/config.json`:

```json
{
  "default_browser": "Firefox",
  "rules": [
    { "pattern": "*.google.com",  "type": "glob",  "browser": "Brave" },
    { "pattern": "*.work.internal", "type": "glob", "browser": "Firefox" }
  ]
}
```

## License

MIT
