"""Tests for pretabs-kitty.sh, run with a fake `kitty` binary (no Kitty needed)."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WIZARD = ROOT / "pretabs-kitty.sh"

FAKE_KITTY = r"""#!/usr/bin/env bash
# Logs every call. `launch` prints a new window id and, like a real new tab,
# starts an interactive shell that sources the rc file (this is what used to
# cause an endless cascade of tabs).
log="$FAKE_DIR/calls.log"
{ printf '[%s]' "$@"; echo; } >> "$log"
if [[ "$*" == *launch* ]]; then
    n=$(( $(cat "$FAKE_DIR/next_id" 2>/dev/null || echo 100) + 1 ))
    echo "$n" > "$FAKE_DIR/next_id"
    depth=$(( ${FAKE_DEPTH:-0} + 1 ))
    if [[ -n "${FAKE_RC:-}" && $depth -lt 5 ]]; then
        FAKE_DEPTH=$depth KITTY_WINDOW_ID=$n bash -c ". \"$FAKE_RC\"" >/dev/null 2>&1
    fi
    echo "$n"
fi
"""


@pytest.fixture
def env(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    kitty = fake_bin / "kitty"
    kitty.write_text(FAKE_KITTY)
    kitty.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    runtime = tmp_path / "run"
    runtime.mkdir()
    return {
        **{k: v for k, v in os.environ.items() if not k.startswith("KITTY")},
        "HOME": str(home),
        "SHELL": "/bin/zsh",
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_RUNTIME_DIR": str(runtime),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "FAKE_DIR": str(tmp_path),
        "NO_COLOR": "1",
    }


def wizard(env, *args):
    return subprocess.run(["bash", str(WIZARD), *args], env=env, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=30)


def calls(env):
    log = Path(env["FAKE_DIR"]) / "calls.log"
    return log.read_text().splitlines() if log.exists() else []


def layout(env, name="work"):
    return Path(env["XDG_CONFIG_HOME"]) / "pretabs-kitty" / f"{name}.sh"


def test_generates_layout_script(env):
    r = wizard(env, "--tabs", "Dev, Logs,Git", "--focus", "2", "--name", "work", "--install", "none")
    assert r.returncode == 0, r.stderr
    script = layout(env).read_text()
    assert os.access(layout(env), os.X_OK)
    assert "set-tab-title" in script and script.count("ids+=(") == 2
    assert 'focus-window --match "id:${ids[1]}"' in script


@pytest.mark.skipif(shutil.which("shellcheck") is None, reason="shellcheck not installed")
def test_generated_script_passes_shellcheck(env):
    wizard(env, "-t", "A,B'C,D \"E\"", "-n", "work", "-i", "none")
    subprocess.run(["shellcheck", str(layout(env))], check=True)


def test_layout_runs_with_exact_titles_and_focus(env):
    wizard(env, "-t", "Dev,it's \"quoted\",Logs", "-f", "2", "-n", "work", "-i", "none")
    r = subprocess.run(["bash", str(layout(env))], env={**env, "KITTY_WINDOW_ID": "7"},
                       capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, r.stderr
    assert calls(env) == [
        "[@][set-tab-title][--match][window_id:7][Dev]",
        "[@][launch][--type=tab][--keep-focus][--tab-title][it's \"quoted\"]",
        "[@][launch][--type=tab][--keep-focus][--tab-title][Logs]",
        "[@][focus-window][--match][id:101]",
    ]


def test_layout_refuses_to_run_outside_kitty(env):
    wizard(env, "-t", "A,B", "-n", "work", "-i", "none")
    r = subprocess.run(["bash", str(layout(env))], env=env, capture_output=True, text=True)
    assert r.returncode == 1 and "inside a Kitty window" in r.stderr
    assert calls(env) == []


def test_auto_launch_runs_once_per_kitty_instance(env):
    """Regression test: new tabs source .zshrc again; the layout must not re-run."""
    r = wizard(env, "-t", "A,B,C", "-n", "work", "-i", "auto")
    assert r.returncode == 0, r.stderr
    rc = Path(env["HOME"]) / ".zshrc"
    shell_env = {**env, "KITTY_PID": "4242", "KITTY_WINDOW_ID": "1", "FAKE_RC": str(rc)}
    for _ in range(3):  # three shells started in the same Kitty instance
        subprocess.run(["bash", "-c", f'. "{rc}"'], env=shell_env, check=True, timeout=30)
    launches = [c for c in calls(env) if "[launch]" in c]
    assert len(launches) == 2  # B and C, exactly once

    # A different Kitty instance gets its own layout.
    subprocess.run(["bash", "-c", f'. "{rc}"'], env={**shell_env, "KITTY_PID": "5555"},
                   check=True, timeout=30)
    assert len([c for c in calls(env) if "[launch]" in c]) == 4


def test_auto_block_is_silent_outside_kitty(env):
    wizard(env, "-t", "A,B", "-n", "work", "-i", "auto")
    rc = Path(env["HOME"]) / ".zshrc"
    subprocess.run(["bash", "-c", f'. "{rc}"'], env=env, check=True)
    assert calls(env) == []


def test_command_install_defines_function(env):
    r = wizard(env, "-t", "A,B", "-n", "work", "-i", "command", "-c", "worktabs")
    assert r.returncode == 0, r.stderr
    rc = Path(env["HOME"]) / ".zshrc"
    subprocess.run(["bash", "-c", f'. "{rc}" && worktabs'], env={**env, "KITTY_WINDOW_ID": "3"},
                   check=True, timeout=10)
    assert len(calls(env)) == 3


def test_reinstall_replaces_block_and_uninstall_cleans_up(env):
    rc = Path(env["HOME"]) / ".zshrc"
    rc.write_text("export KEEP_ME=1\n")
    wizard(env, "-t", "A,B", "-n", "work", "-i", "auto")
    wizard(env, "-t", "A,B,C", "-n", "work", "-i", "command", "--yes")
    text = rc.read_text()
    assert text.count(">>> pretabs-kitty: work >>>") == 1 and "work()" in text
    r = wizard(env, "--uninstall", "work")
    assert r.returncode == 0
    assert "pretabs-kitty" not in rc.read_text() and "KEEP_ME" in rc.read_text()
    assert not layout(env).exists()


def test_bash_users_get_bashrc(env):
    wizard(env, "-t", "A", "-n", "work", "-i", "command", "-c", "w")
    assert not (Path(env["HOME"]) / ".bashrc").exists()
    env["SHELL"] = "/bin/bash"
    wizard(env, "-t", "A", "-n", "other", "-i", "command", "-c", "o")
    assert "o()" in (Path(env["HOME"]) / ".bashrc").read_text()


@pytest.mark.parametrize("args, message", [
    (["-t", "A,B", "-f", "3"], "--focus must be between 1 and 2"),
    (["-t", "A", "-n", "bad name"], "Invalid name"),
    (["-t", "A", "-i", "sometimes"], "--install must be"),
    (["-t", "A", "-i", "command", "-c", "no-dashes"], "Invalid command name"),
    ([], "no terminal to ask"),
    (["--bogus"], "Unknown option"),
])
def test_invalid_input(env, args, message):
    r = wizard(env, *args)
    assert r.returncode == 1
    assert message in r.stderr


def test_existing_script_needs_yes(env):
    assert wizard(env, "-t", "A", "-n", "work", "-i", "none").returncode == 0
    r = wizard(env, "-t", "B", "-n", "work", "-i", "none")
    assert r.returncode == 1 and "--yes" in r.stderr
    assert wizard(env, "-t", "B", "-n", "work", "-i", "none", "-y").returncode == 0
