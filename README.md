# Bowser 🏎️

A lightweight URL-dispatching browser router for Linux. Bowser sits in place of your default browser and routes URLs to different browsers based on hostname matching rules.

## Features

- **Hostname-based routing** — glob-style patterns (e.g. `*.work.com`) matched against the URL hostname
- **Modular browsers** — adding a new browser requires one file and a config entry
- **Per-browser flags** — custom command-line arguments per browser in config
- **Zero dependencies** — uses only Python 3.11+ stdlib (`tomllib`, `urllib`, `fnmatch`)

## Requirements

- Python 3.11+
- Fedora 44 (or any Linux with `xdg-mime`)
- Google Chrome and/or Microsoft Edge installed

## Installation

```bash
git clone https://github.com/pbergene/bowser.git
cd bowser
bash install.sh
```

`install.sh` will:
1. Copy files to `~/.local/lib/bowser/`
2. Create a `~/.local/bin/bowser` wrapper
3. Install `bowser.desktop` to `~/.local/share/applications/`
4. Register Bowser as the default handler for `http://` and `https://` URLs
5. Copy the default config to `~/.config/bowser/config.toml` (if not already present)

Verify registration:
```bash
xdg-settings get default-web-browser   # should print: bowser.desktop
```

## Configuration

Edit `~/.config/bowser/config.toml`:

```toml
# Fallback browser when no rule matches
default_browser = "chrome"

# Rules — evaluated top-to-bottom, first match wins
# Patterns use glob syntax matched against the URL hostname
[[rules]]
pattern = "*.work.com"
browser = "edge"

[[rules]]
pattern = "sharepoint.com"
browser = "edge"

# Browser definitions
[browsers.chrome]
command = "google-chrome"
flags = []

[browsers.edge]
command = "microsoft-edge"
flags = ["--inprivate"]   # example: always open Edge in InPrivate mode
```

## Adding a New Browser

1. Create `browsers/<name>.py`:

```python
from .base import BrowserBase

class FirefoxBrowser(BrowserBase):
    DEFAULT_COMMAND = "firefox"

    @property
    def name(self) -> str:
        return "firefox"
```

2. Register it in `browsers/__init__.py`:

```python
from .firefox import FirefoxBrowser

REGISTRY: dict[str, type[BrowserBase]] = {
    "chrome": ChromeBrowser,
    "edge": EdgeBrowser,
    "firefox": FirefoxBrowser,   # ← add this line
}
```

3. Add a section to `~/.config/bowser/config.toml`:

```toml
[browsers.firefox]
command = "firefox"
flags = []
```

4. Re-run `install.sh` to push the updated `browsers/` directory to `~/.local/lib/bowser/`.

## Manual usage

```bash
bowser https://example.com
bowser https://internal.work.com/dashboard
```

## How it works

```
URL → urlparse → hostname → fnmatch rules → browser name → get_browser() → subprocess.Popen
```

If no rule matches, the `default_browser` is used. The first rule whose `pattern` glob-matches the hostname wins.
