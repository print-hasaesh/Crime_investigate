import sys
import subprocess

print("=== Crime Data Dashboard ===\n")

try:
    subprocess.run([sys.executable, "dashboard.py"], check=True)
except subprocess.CalledProcessError:
    print("Application failed")
    sys.exit(1)

print("\n=== Execution completed successfully ===")