# Pretabs-Kitty

This script is designed to open the [Kitty](https://sw.kovidgoyal.net/kitty/) terminal emulator with four preconfigured tabs, each with a specific title. This setup is useful for users who want to quickly open multiple tabs with specific titles in a single command.

---

## ✨ Features

- 🖥 **Tab Management**: Automatically opens Kitty with four tabs  (or as many as you want), each pre-named for easy identification.
- 🎛 **Custom Titles**: Sets unique titles for each tab, allowing users to easily switch between tasks.

---

## 📥 Installation

### Prerequisites

This script requires the [Kitty terminal](https://sw.kovidgoyal.net/kitty/) to be installed on your system. Install it with:

```bash
# For Debian/Ubuntu-based systems
sudo apt-get install kitty
```

or follow the installation instructions on the [Kitty website](https://sw.kovidgoyal.net/kitty/).

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/serber1990/Pretabs-Kitty.git
cd Pretabs-Kitty
```

---

## 🛠 Usage

To run the script, use:

```bash
chmod +x pretabs-kitty.sh
./pretabs-kitty.sh
```

The script **by default** will open Kitty with four tabs, each named according to your preferences (`Tab1`, `Tab2`, `Tab3`, `Tab4`).

You need to modify the script and change the placeholders "TabX" with anything you want.

You can also copy and paste the last two lines...

`kitty @ focus-tab --match 'title:Tab3'`: Switches focus to the tab titled `Tab3`.
`kitty @ launch --type=tab --tab-title "Tab4" --keep-focus`: Opens a new tab with the title `Tab4`.

...as many times as you want to add more tabs, or simpy remove the ones you don't need.

Optional:

You can add this script into a function in your .bashrc / .zshrc file to execute this with a simple "oneWord" command.

---

## 📝 Script Breakdown

Below is an explanation of each command used in the script:

- `kitty @ set-tab-title 'Tab1'`: Sets the title of the first tab to `Tab1`.
- `kitty @ launch --type=tab --tab-title "Tab2" --keep-focus`: Opens a new tab with the title `Tab2` without changing focus.
- `kitty @ focus-tab --match 'title:Tab2'`: Switches focus to the tab titled `Tab2`.
- `kitty @ launch --type=tab --tab-title "Tab3" --keep-focus`: Opens a new tab with the title `Tab3` and keeps focus.
- `kitty @ focus-tab --match 'title:Tab3'`: Switches focus to the tab titled `Tab3`.
- `kitty @ launch --type=tab --tab-title "Tab4" --keep-focus`: Opens a new tab with the title `Tab4`.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Feedback

If you have any questions, issues, or suggestions, please feel free to open an issue in the repository or contact me directly via GitHub.

## 🌐 Connect with Me

[![GitHub](https://img.shields.io/badge/GitHub-@serber1990-181717?style=flat-square&logo=github)](https://github.com/serber1990)

---

### 🚀 Quickly manage multiple tabs in Kitty with custom titles using Pretabs-Kitty!
