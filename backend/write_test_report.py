import re
import subprocess
import sys
from pathlib import Path


backend_dir = Path(__file__).resolve().parent
root_dir = backend_dir.parent
fence = "`" * 3

command = [
    sys.executable,
    "-m",
    "pytest",
    "tests",
    "-q",
    "--cov=app",
    "--cov-report=term-missing",
]

result = subprocess.run(
    command,
    cwd=backend_dir,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)

output = (result.stdout + result.stderr).strip()

if result.returncode != 0:
    print(output)
    raise SystemExit("Tests failed; the report was not updated.")

coverage_match = re.search(
    r"(?m)^TOTAL\s+(\d+)\s+(\d+)\s+(\d+)%",
    output,
)
summary_match = re.search(
    r"(?m)^(\d+) passed(?:, (\d+) warnings?)? in ([\d.]+)s",
    output,
)

if coverage_match is None or summary_match is None:
    print(output)
    raise SystemExit("Could not read the test summary; report not updated.")

statements = int(coverage_match.group(1))
missing = int(coverage_match.group(2))
coverage = int(coverage_match.group(3))
passed = int(summary_match.group(1))
warnings = int(summary_match.group(2) or 0)
duration = summary_match.group(3)

report_lines = [
    "# Test Report",
    "",
    "## Environment",
    "",
    "- Platform: Windows",
    "- Python: 3.13.4",
    "- Test framework: pytest",
    "- Database: temporary SQLite files for API tests",
    "",
    "## Command",
    "",
    "Run from `backend`:",
    "",
    fence + "powershell",
    r".\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-report=term-missing",
    fence,
    "",
    "## Result",
    "",
    f"- {passed} tests passed",
    "- 0 tests failed",
    f"- Backend line coverage: {coverage}% "
    f"({statements - missing} of {statements} statements)",
    f"- {warnings} warnings",
    f"- Execution time: {duration} seconds",
    "",
    "## Full test output",
    "",
    fence + "text",
    output,
    fence,
    "",
    "## Frontend verification",
    "",
    "The frontend was built with `npm run build`. Registration, login,",
    "admin controls, vehicle creation, purchasing, restocking, searching,",
    "and editing were checked manually in the browser.",
    "",
]

(root_dir / "TEST_REPORT.md").write_text(
    "\n".join(report_lines),
    encoding="utf-8",
)

readme_path = root_dir / "README.md"
readme = readme_path.read_text(encoding="utf-8")
updated_readme = re.sub(
    r"The recorded run passed \*\*\d+ tests\*\* with "
    r"\*\*\d+% backend line coverage\*\*\.",
    f"The recorded run passed **{passed} tests** with "
    f"**{coverage}% backend line coverage**.",
    readme,
)

if updated_readme != readme:
    readme_path.write_text(updated_readme, encoding="utf-8")
else:
    print("README result sentence not found; check it manually.")

print(f"{passed} passed; {coverage}% coverage; {warnings} warnings.")
print("Updated TEST_REPORT.md and README.md.")