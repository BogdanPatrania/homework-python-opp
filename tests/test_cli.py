import subprocess
import sys

def run_cli(args):
    result = subprocess.run([sys.executable, "cli.py"] + args, capture_output=True, text=True)
    return result

def test_cli_pow():
    result = run_cli(["pow", "--base", "2", "--exp", "3"])
    assert "→ 2.0^3.0 = 8.0" in result.stdout

def test_cli_fibonacci():
    result = run_cli(["fibonacci", "--n", "10"])
    assert "→ Fibonacci(10) = 55" in result.stdout

def test_cli_factorial():
    result = run_cli(["factorial", "--n", "5"])
    assert "→ 5! = 120" in result.stdout