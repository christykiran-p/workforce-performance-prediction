import subprocess
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


print("=" * 70)
print("WORKFORCE PERFORMANCE PREDICTION")
print("QUALITY ENGINEERING PIPELINE")
print("=" * 70)

# =====================================================
# Run Tests + Generate Reports
# =====================================================

print("\nRunning Automated Tests...\n")

subprocess.run(
    [
        "pytest",
        "--junitxml=test-results.xml",
        "--cov=src",
        "--cov-report=term",
        "--cov-report=xml",
        "--cov-report=html"
    ],
    check=True
)

print("\nTests Completed Successfully")

# =====================================================
# Read Coverage XML
# =====================================================

coverage_file = Path("coverage.xml")

if not coverage_file.exists():

    raise FileNotFoundError(
        "coverage.xml not found"
    )

tree = ET.parse(
    coverage_file
)

root = tree.getroot()

coverage_pct = round(
    float(
        root.attrib["line-rate"]
    ) * 100,
    2
)

# =====================================================
# Update Coverage History
# =====================================================

reports_dir = Path("reports")
reports_dir.mkdir(
    exist_ok=True
)

history_file = reports_dir / "coverage_history.csv"

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

new_row = pd.DataFrame(
    {
        "timestamp": [timestamp],
        "coverage": [coverage_pct]
    }
)

if history_file.exists():

    history_df = pd.read_csv(
        history_file
    )

    history_df = pd.concat(
        [
            history_df,
            new_row
        ],
        ignore_index=True
    )

else:

    history_df = new_row

history_df.to_csv(
    history_file,
    index=False
)

# =====================================================
# Read Test Results XML
# =====================================================

test_file = Path(
    "test-results.xml"
)

total_tests = 0
failures = 0
errors = 0

if test_file.exists():

    tree = ET.parse(
        test_file
    )

    root = tree.getroot()

    for testsuite in root.findall(
        ".//testsuite"
    ):

        total_tests += int(
            testsuite.attrib.get(
                "tests",
                0
            )
        )

        failures += int(
            testsuite.attrib.get(
                "failures",
                0
            )
        )

        errors += int(
            testsuite.attrib.get(
                "errors",
                0
            )
        )

passed_tests = (
    total_tests
    - failures
    - errors
)

# =====================================================
# Summary
# =====================================================

print("\n" + "=" * 70)

print("QUALITY SUMMARY")

print("=" * 70)

print(
    f"Total Tests      : {total_tests}"
)

print(
    f"Passed Tests     : {passed_tests}"
)

print(
    f"Failed Tests     : {failures + errors}"
)

print(
    f"Code Coverage    : {coverage_pct}%"
)

print(
    f"Coverage History : {history_file}"
)

print(
    f"HTML Report      : htmlcov/index.html"
)

print("\nQuality Pipeline Completed Successfully")

print("=" * 70)

# =====================================================
# Open HTML Coverage Report Automatically
# =====================================================

html_report = Path(
    "htmlcov/index.html"
)

if html_report.exists():

    print(
        "\nOpening HTML Coverage Report..."
    )

    try:

        import webbrowser

        webbrowser.open(
            str(
                html_report.resolve()
            )
        )

    except Exception:

        print(
            "Unable to auto-open browser."
        )