
Loading older messages…
(.venv) PS C:\AnneData\Placements\AnneGeorge_Incubyte\backend> .\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-report=term-missing
............                                                                [100%]
================================ warnings summary ================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\AnneData\Placements\AnneGeorge_Incubyte\backend\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_search.py::test_search_filters_by_make_and_maximum_price
  C:\Program Files\Python313\Lib\asyncio\windows_events.py:430: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x00000213C3BD2110>
    def _check_closed(self):
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

tests/test_search.py::test_search_filters_by_make_and_maximum_price
  C:\Program Files\Python313\Lib\asyncio\windows_events.py:430: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x00000213C3C3F880>
    def _check_closed(self):
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================= tests coverage =================================
________________ coverage: platform win32, python 3.13.4-final-0 _________________

Name          Stmts   Miss  Cover   Missing
-------------------------------------------
app\main.py     172     13    92%   117-118, 124, 152, 178, 233, 243, 247, 251, 268, 293, 323, 353
-------------------------------------------
TOTAL           172     13    92%
12 passed, 3 warnings in 6.98s
…
Worked for 22s
The backend is at 12 passing tests and 92% line coverage. That meets the kata’s high-coverage goal. The three warnings did not fail the suite; we’ll record them accurately in the test report.

Step 92: Save Python dependencies
Where: In the VS Code PowerShell terminal, with the prompt ending in AnneGeorge_Incubyte\backend, run this command:

.\.venv\Scripts\python.exe -c "import pathlib, subprocess, sys; pathlib.Path('requirements.txt').write_text(subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True), encoding='utf-8')"
This creates backend/requirements.txt with the exact packages installed in your backend environment, so someone else can install them.

Check that requirements.txt appears under backend in the VS Code File Explorer, then say “next.”

(.venv) PS C:\AnneData\Placements\AnneGeorge_Incubyte\backend> .\.venv\Scripts\python.exe -c "import pathlib, subprocess, sys; pathlib.Path('requirements.txt').write_text(subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True), encoding='utf-8')"
The command completed successfully; backend/requirements.txt should now be present.

Step 93: Create the test report
Where: In the VS Code File Explorer, create TEST_REPORT.md directly inside AnneGeorge_Incubyte (beside the backend and frontend folders). Paste this complete content and save it:

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
Result
12 tests passed
0 tests failed
Backend line coverage: 92% (159 of 172 statements)
Execution time: 6.98 seconds
The coverage output reported:

Name          Stmts   Miss  Cover
---------------------------------
app\main.py     172     13    92%
---------------------------------
TOTAL           172     13    92%

12 passed, 3 warnings in 6.98s
Tested behavior
User registration and invalid email rejection
Login and bearer token issuance
Authentication required for vehicle listing
Vehicle creation and database persistence
Search by make and maximum price
Vehicle updates
Purchasing, stock reduction, and sold-out rejection
Admin-only vehicle deletion
Admin-only restocking and invalid amount rejection
Current-user profile and role response
Warnings
The run showed one Starlette deprecation warning concerning httpx and two SQLite connection resource warnings on Windows. They did not cause test failures. These warnings are included here rather than omitted from the report.

Frontend check
The frontend compiled with npm run build. Registration, login, the admin dashboard, adding a vehicle, purchasing, restocking, searching, and editing were also checked manually in the browser.


Say **“next”** after saving it. Next we’ll prepare screenshots for the README.
next
Worked for 12s
Step 94: Save an inventory screenshot
Where: In the VS Code File Explorer, create a folder named screenshots directly inside AnneGeorge_Incubyte.

Then, in your web browser at http://localhost:5173/:

Click Clear in the search form so the Corolla Hybrid card is visible.
Scroll until the search controls and vehicle card are on screen.
Press Windows + Shift + S and select that part of the page.
Click the screenshot notification, then press Ctrl+S in Snipping Tool.
Save it as C:\AnneData\Placements\AnneGeorge_Incubyte\screenshots\inventory.png.
Check that inventory.png appears in the VS Code File Explorer. Say “next” when it is saved.

what is this screenshot folder for
Your assignment requires screenshots of the final application in the README. The screenshots folder keeps those image files in the GitHub repository so the README can display them.

For example, the README will include:

![Vehicle inventory](screenshots/inventory.png)
Capture only the app interface; crop out your email or other personal details if you prefer. Once inventory.png is saved in that folder, say “next.”

next
Step 95: Save an admin dashboard screenshot
Where: In your web browser at http://localhost:5173/, scroll up until the Admin badge and Add a vehicle form are visible.

Press Windows + Shift + S, select that part of the page, click the screenshot notification, and press Ctrl+S in Snipping Tool. Save the image as:

C:\AnneData\Placements\AnneGeorge_Incubyte\screenshots\admin-dashboard.png
Check that the file appears in the VS Code File Explorer. Say “next” when it is saved.

next
Step 96: Save a login screenshot
Where: In your web browser at http://localhost:5173/:

Click Sign out.
Press Windows + Shift + S and capture the login screen.
Open the screenshot notification and press Ctrl+S.
Save it as C:\AnneData\Placements\AnneGeorge_Incubyte\screenshots\login.png.
You can sign back in afterward. Check that login.png appears under screenshots in VS Code, then say “next.”

next
Step 97: Create the README
Where: In the VS Code File Explorer, create README.md directly inside AnneGeorge_Incubyte. Paste all of the following content and save with Ctrl+S:

# Motora — Car Dealership Inventory System

A full-stack car dealership inventory application built with FastAPI, SQLite, React, Vite, and Tailwind CSS. Users can register, sign in, search vehicles, and purchase available stock. Admins can manage inventory through the dashboard.

## Screenshots

### Login

![Login screen](screenshots/login.png)

### Inventory

![Vehicle inventory](screenshots/inventory.png)

### Admin dashboard

![Admin dashboard](screenshots/admin-dashboard.png)

## Features

- User registration and login with password hashing and JWT bearer tokens
- SQLite-backed vehicle inventory
- Search by make, model, category, and minimum or maximum price
- Vehicle purchasing that decreases stock and rejects sold-out purchases
- Admin-only deletion and restocking
- Responsive React dashboard with Tailwind CSS
- Admin interface for adding and editing vehicles
- Purchase buttons disabled when stock is zero

## Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Python, FastAPI, SQLModel, SQLAlchemy |
| Database | SQLite file |
| Authentication | Argon2 password hashing, JWT |
| Frontend | React, HTML5, CSS3, Tailwind CSS, Vite |
| Testing | pytest, FastAPI TestClient, pytest-cov |

## Requirements

- Python 3.10 or newer
- Node.js 20.19+ or 22.12+
- npm
- Git

## Run locally

Clone the repository:

```powershell
git clone https://github.com/This-AnneGeorge/AnneGeorge_Incubyte.git
cd AnneGeorge_Incubyte
```

### 1. Start the backend

Open a terminal in the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set a JWT signing secret for this terminal session:

```powershell
$env:JWT_SECRET_KEY = (& .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))")
```

Start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`. The SQLite database file, `backend/dealership.db`, is created automatically and is excluded from Git.

Keep the backend terminal open. If you restart it with a newly generated JWT secret, sign in again because tokens signed with the previous secret will no longer work. Set a stable secret through your environment when persistent sessions are needed.

### 2. Start the frontend

Open a **second terminal** in the repository root:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173/` in your browser. During local development, Vite forwards `/api` requests to the backend on port 8000. Keep both servers running.

### 3. Create an admin account

Register normally in the frontend first. Registration always creates a regular user.

Then, in a terminal inside `backend`, promote that existing account:

```powershell
.\.venv\Scripts\python.exe promote_admin.py "your-email@example.com"
```

Replace the example email with the email you registered. Sign out and sign in again to display the admin controls. Do not expose an admin promotion endpoint to public users.

## API endpoints

All vehicle endpoints require an `Authorization: Bearer <token>` header.

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| POST | `/api/auth/register` | Register with email and password | Public |
| POST | `/api/auth/login` | Receive an access token | Public |
| GET | `/api/auth/me` | Get current user and role | Signed-in user |
| POST | `/api/vehicles` | Add a vehicle | Signed-in user |
| GET | `/api/vehicles` | List vehicles, including sold-out entries | Signed-in user |
| GET | `/api/vehicles/search` | Filter vehicles | Signed-in user |
| PUT | `/api/vehicles/{id}` | Replace vehicle details | Signed-in user |
| DELETE | `/api/vehicles/{id}` | Delete a vehicle | Admin |
| POST | `/api/vehicles/{id}/purchase` | Purchase one unit | Signed-in user |
| POST | `/api/vehicles/{id}/restock` | Add units to stock | Admin |

Search accepts optional query parameters: `make`, `model`, `category`, `min_price`, and `max_price`. Text matching is case-insensitive and supports partial matches. Filters can be combined.

A vehicle has a database-generated unique ID, make, model, category, price, and quantity. Prices in the UI are displayed in USD. To restock, send JSON such as `{"amount": 3}`. A purchase does not need a request body.

The API uses `401` for missing or invalid authentication, `403` for insufficient permission, `404` for missing vehicles, `409` for conflicts such as sold-out purchases, and `422` for invalid input.

## Tests

From the `backend` directory, run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-report=term-missing
```

The recorded run passed **12 tests** with **92% backend line coverage**. See [TEST_REPORT.md](TEST_REPORT.md) for the measured output, tested behaviors, and warnings.

To check the frontend build, run from `frontend`:

```powershell
npm run build
```

The backend tests use temporary SQLite files, so they do not change your local `dealership.db`. The purchase endpoint uses a conditional database update to avoid selling stock below zero.

## Project structure

```text
AnneGeorge_Incubyte/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── promote_admin.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── index.css
│   └── vite.config.js
├── screenshots/
├── TEST_REPORT.md
├── PROMPTS.md
└── README.md
```

## My AI Usage

I used **ChatGPT** as a step-by-step coding assistant for this project. It helped draft the FastAPI endpoints, React interface, pytest cases, setup commands, and documentation. I ran the commands and tests locally, checked the app in my browser, and worked through errors such as an incorrectly named test file and a stopped backend server.

AI made it faster to scaffold and iterate through the Red–Green steps of TDD. I still needed to verify the output: a generated answer does not prove that code runs, that permissions are correct, or that the frontend reaches the API. The test results and browser checks in this repository reflect that verification.

The raw AI conversation or its public link is provided in [PROMPTS.md](PROMPTS.md).
Before submitting, read the “My AI Usage” section and adjust its first-person wording if any detail does not match what you personally did.

Say “next” after saving the README. Then we’ll make PROMPTS.md contain the required raw conversation link.




