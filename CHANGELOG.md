# Changelog

## 2.1.0

### Fixed
- **Auto-launch opened tabs endlessly.** Every tab opened by the layout started a new shell that ran
  `.zshrc` again, which opened more tabs. The hook now runs the layout once per Kitty instance.
- The hook no longer runs (or prints errors) in shells outside Kitty, e.g. over SSH or in other terminals.
- Tab titles with quotes, spaces or `$` broke the generated script; they are now safely quoted.
- Focus used a regex title match, so "Dev" could focus "Dev2"; it now uses the window id returned by `kitty @ launch`.
- Invalid command names could corrupt the shell startup file; names are validated.

### Added
- Command-line options for non-interactive use (`--tabs`, `--focus`, `--name`, `--install`, `--command`, `--rc`, `--yes`).
- `--uninstall NAME` removes the shell hook and the generated script.
- Shell hooks are wrapped in `# >>> pretabs-kitty: NAME >>>` markers: re-running the wizard replaces them instead of duplicating.
- Bash support (`~/.bashrc`), detected from `$SHELL`.
- Test suite (runs with a fake `kitty`) and GitHub Actions CI with ShellCheck.

### Changed
- Generated scripts are stored in `${XDG_CONFIG_HOME:-~/.config}/pretabs-kitty/` instead of the repository folder.
- License file is now MIT, matching the README.

## 2.0.0

- Interactive setup wizard with three `.zshrc` integration options.
