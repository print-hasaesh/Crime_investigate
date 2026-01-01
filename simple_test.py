import os
import subprocess
import re

print("Running analysis script...")
result = subprocess.run(
    ["python", "simple_crime_analysis.py"],
    capture_output=True,
    text=True
)

output = result.stdout

# ----------------------------
# Test 1: Data Loading Check
# ----------------------------
match_loaded = re.search(r"Loaded (\d+) records", output)
if match_loaded and int(match_loaded.group(1)) > 0:
    print("Test 1 (Data loads): PASS")
else:
    print("Test 1 (Data loads): FAIL")

# ----------------------------
# Test 2: Data Cleaning Check
# ----------------------------
match_cleaned = re.search(r"After cleaning: (\d+) records", output)
if match_loaded and match_cleaned:
    if int(match_cleaned.group(1)) <= int(match_loaded.group(1)):
        print("Test 2 (Data cleans): PASS")
    else:
        print("Test 2 (Data cleans): FAIL")
else:
    print("Test 2 (Data cleans): FAIL")

# ----------------------------
# Test 3: Chart Creation Check
# ----------------------------
charts = [
    "chart1_outcomes.png",
    "chart2_areas.png",
    "chart3_solving_rates.png",
]

if all(os.path.exists(chart) for chart in charts):
    print("Test 3 (Charts created): PASS")
else:
    print("Test 3 (Charts created): FAIL")

# ----------------------------
# Test 4: Logical Results Check
# ----------------------------
match_with = re.search(r"WITH location: ([\d.]+)%", output)
match_without = re.search(r"WITHOUT location: ([\d.]+)%", output)

if match_with and match_without:
    if float(match_with.group(1)) > float(match_without.group(1)):
        print("Test 4 (Results logical): PASS")
    else:
        print("Test 4 (Results logical): FAIL")
else:
    print("Test 4 (Results logical): FAIL")
