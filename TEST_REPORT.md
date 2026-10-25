# Test Report

## Environment

- Platform: Windows
- Python: 3.13.4
- Test framework: pytest
- Database: temporary SQLite files for API tests

## Command

Run from `backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-report=term-missing
```

## Result

- 15 tests passed
- 0 tests failed
- Backend line coverage: 93% (166 of 179 statements)
- 3 warnings
- Execution time: 8.38 seconds

## Full test output

```text
...............                                                          [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\AnneData\Placements\AnneGeorge_Incubyte\backend\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_search.py::test_search_filters_by_make_and_maximum_price
  C:\AnneData\Placements\AnneGeorge_Incubyte\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py:288: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x000002A7FB9B9210>
    for index, (name, extras) in enumerate(zip(self._keys, extra))
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

tests/test_search.py::test_search_filters_by_make_and_maximum_price
  C:\AnneData\Placements\AnneGeorge_Incubyte\backend\.venv\Lib\site-packages\sqlalchemy\engine\result.py:288: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x000002A7FBA216C0>
    for index, (name, extras) in enumerate(zip(self._keys, extra))
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.4-final-0 _______________

Name          Stmts   Miss  Cover   Missing
-------------------------------------------
app\main.py     179     13    93%   130-131, 137, 165, 191, 246, 256, 260, 264, 281, 306, 336, 366
-------------------------------------------
TOTAL           179     13    93%
15 passed, 3 warnings in 8.38s
```

## Frontend verification

The frontend was built with `npm run build`. Registration, login,
admin controls, vehicle creation, purchasing, restocking, searching,
and editing were checked manually in the browser.
