import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "..", "cloudup.py")


def run(args, cwd, env_extra=None):
    env = {"PATH": os.environ["PATH"], "HOME": str(cwd), "XDG_CONFIG_HOME": str(cwd / "xdg")}
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, TOOL, *args], cwd=cwd, env=env, capture_output=True, text=True
    )


def test_defaults(tmp_path):
    result = run(["config"], tmp_path)
    assert result.returncode == 0
    assert "region=eu-north-1" in result.stdout
