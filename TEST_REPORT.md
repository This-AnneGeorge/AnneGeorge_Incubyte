# Test Report

## Environment

- Platform: Windows
- Python: 3.13.4
- Test framework: pytest
- Database used by API tests: temporary SQLite files

## Command

Run from the `backend` directory:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-report=term-missing