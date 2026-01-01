import subprocess
import sys

print("=== Starting Simple Crime Data Analysis ===\n")

# Step 1: Run the main analysis (GUI version)
print("Running analysis script (close the chart window to continue)...\n")
try:
    # Use sys.executable to ensure correct Python version
    subprocess.run([sys.executable, "simple_crime_analysis.py"], check=True)
except subprocess.CalledProcessError:
    print("Error: Analysis script failed.")
    exit()

# Step 2: Run automated tests after GUI window is closed
print("\nRunning automated tests...\n")
try:
    subprocess.run([sys.executable, "simple_test.py"], check=True)
except subprocess.CalledProcessError:
    print("Error: Test script failed.")
    exit()

print("\n=== Project execution completed ===")
