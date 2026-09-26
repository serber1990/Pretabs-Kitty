# Pretabs-Kitty

[![CI](https://github.com/serber1990/Pretabs-Kitty/actions/workflows/ci.yml/badge.svg)](https://github.com/serber1990/Pretabs-Kitty/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/serber1990/Pretabs-Kitty?style=social)](https://github.com/serber1990/Pretabs-Kitty/stargazers)

Open your [Kitty](https://sw.kovidgoyal.net/kitty/) terminal with your tabs already there: named, in order,
with the right one focused. Pretabs-Kitty is a small wizard that generates the layout script and, if you want,
hooks it into your shell.

<p align="center">
  <img src="https://raw.githubusercontent.com/serber1990/Pretabs-Kitty/main/docs/demo.gif" alt="Pretabs-Kitty demo: setup wizard and generated layout script" width="820">
</p>

---

## ✨ Features

- 🧙 **Interactive wizard** — or fully scriptable with command-line options
- 🏷️ **Any number of named tabs** — titles with spaces, quotes or symbols are handled safely
- 🎯 **Focus control** — choose which tab is active after launch
- 🚀 **Auto-launch** — opens the layout when Kitty starts, **once per Kitty instance** (no tab explosions)
- ⌨️ **Or a command** — add a shell function such as `worktabs` and run it whenever you want
- 🧹 **Clean uninstall** — hooks are wrapped in markers; `--uninstall` removes them
- 🐚 **zsh and bash** — detected from `$SHELL`, or pick the file with `--rc`

---

## 📥 Prerequisites

Install [Kitty](https://sw.kovidgoyal.net/kitty/) and enable remote control in `~/.config/kitty/kitty.conf`:

```
allow_remote_control yes
```

Restart Kitty after changing it.

---

## 🚀 Quick start

```bash
git clone https://github.com/serber1990/Pretabs-Kitty.git
cd Pretabs-Kitty
./pretabs-kitty.sh
```

The wizard asks:

| Step | Question |
|------|----------|
| 1 | How many tabs? |
| 2 | A name for each tab |
| 3 | Which tab gets focus after launch |
| 4 | Layout name *(default: `kitty-tabs`)* |
| 5 | **1** Launch when Kitty starts · **2** Add a shell command · **3** Just save the script |

### Example session

```
How many tabs do you want? 3
Name each tab:
  Tab 1 name: Dev
  Tab 2 name: Logs
  Tab 3 name: Git

Which tab should have focus after launch?
  1) Dev
  2) Logs
  3) Git
Tab number [1-3]: 1

Layout name [kitty-tabs]: work

  ✔ Layout script: /home/you/.config/pretabs-kitty/work.sh

What would you like to do with it?
  1) Launch it automatically when Kitty starts (once per Kitty instance)
  2) Add a shell command that launches it
  3) Nothing else — I'll run it myself
Choose [1/2/3]: 1
  ✔ Added to /home/you/.zshrc
```

---

## ⚙️ Non-interactive usage

Every question has an option, so you can script or version your setup:

```bash
# Auto-launch Dev / Logs / Git with Dev focused
./pretabs-kitty.sh --tabs "Dev,Logs,Git" --focus 1 --name work --install auto

# Add a `worktabs` command instead
./pretabs-kitty.sh -t "Dev,Logs,Git" -n work -i command -c worktabs

# Remove the hook and the generated script
./pretabs-kitty.sh --uninstall work
```

| Option | Description |
|--------|-------------|
| `-t`, `--tabs "A,B,C"` | Tab titles, comma-separated |
| `-f`, `--focus N` | Tab (1-based) focused after launch (default: 1) |
| `-n`, `--name NAME` | Layout name (default: `kitty-tabs`) |
| `-o`, `--output-dir DIR` | Where to write it (default: `~/.config/pretabs-kitty`) |
| `-i`, `--install auto\|command\|none` | Shell integration mode |
| `-c`, `--command NAME` | Function name for `--install command` |
| `--rc FILE` | Shell startup file to edit (default: `~/.zshrc` or `~/.bashrc`) |
| `-y`, `--yes` | Overwrite an existing layout without asking |
| `--uninstall NAME` | Remove the hook and the script |

---

## 📝 How it works

The generated `~/.config/pretabs-kitty/work.sh` uses Kitty's remote control:

```bash
ids=("$KITTY_WINDOW_ID")
kitty @ set-tab-title --match "window_id:$KITTY_WINDOW_ID" Dev
ids+=("$(kitty @ launch --type=tab --keep-focus --tab-title Logs)")
ids+=("$(kitty @ launch --type=tab --keep-focus --tab-title Git)")
kitty @ focus-window --match "id:${ids[0]}"
```

With `--install auto`, this block is added to your shell startup file:

```bash
# >>> pretabs-kitty: work >>>
if [ -n "${KITTY_PID:-}" ] && [ -n "${KITTY_WINDOW_ID:-}" ]; then
    _pretabs_marker="${XDG_RUNTIME_DIR:-/tmp}/pretabs-kitty-$(id -u)-${KITTY_PID}-work"
    if [ ! -e "$_pretabs_marker" ]; then
        : > "$_pretabs_marker"
        bash /home/you/.config/pretabs-kitty/work.sh
    fi
    unset _pretabs_marker
fi
# <<< pretabs-kitty: work <<<
```

The marker file is created before any tab is opened, so the shells started in the new tabs skip the
layout. It runs again only when a new Kitty instance starts, and never outside Kitty (SSH, other terminals).

---

## 🧪 Development

```bash
shellcheck pretabs-kitty.sh
pip install pytest && pytest      # uses a fake `kitty`, no Kitty needed
```

See [CHANGELOG.md](CHANGELOG.md) for release notes.

---

## 📝 License

MIT — see [LICENSE](LICENSE).

---

## 💬 Feedback

Open an issue or reach out via GitHub.

## 🌐 Connect

[![GitHub](https://img.shields.io/badge/GitHub-@serber1990-181717?style=flat-square&logo=github)](https://github.com/serber1990)
