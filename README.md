# QA Automation Demo

A minimal Python QA automation project for teaching purposes.
Covers UI testing with Selenium and API testing with requests, all wired into GitHub Actions CI.

---

## Project structure

```
qa-demo/
├── tests/
│   ├── ui/
│   │   └── test_login.py      # Selenium UI tests (login page)
│   └── api/
│       └── test_api.py        # requests API tests (JSONPlaceholder)
├── requirements.txt           # Python dependencies
├── pytest.ini                 # pytest configuration
└── .github/
    └── workflows/
        └── tests.yml          # GitHub Actions CI pipeline
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10 or higher |
| Google Chrome | latest stable |
| pip | bundled with Python |

> **Note:** ChromeDriver is downloaded automatically by Selenium Manager (included in selenium >= 4.6).
> You do **not** need to install or manage ChromeDriver manually.

---

## Local setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd qa-demo

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the tests

```bash
# Run all tests
pytest

# Run only API tests
pytest tests/api

# Run only UI tests
pytest tests/ui

# Run with extra output (already the default via pytest.ini)
pytest -v

# Stop after the first failure
pytest -x
```

---

## What each test does

### UI tests — `tests/ui/test_login.py`

Site under test: <https://practicetestautomation.com/practice-test-login/>

| Test | Credentials | Expected result |
|------|-------------|-----------------|
| `test_valid_login` | student / Password123 | URL contains `logged-in-successfully`, page shows "Congratulations" |
| `test_invalid_login_wrong_username` | wronguser / Password123 | Error element shows "Your username is invalid!" |

### API tests — `tests/api/test_api.py`

API under test: <https://jsonplaceholder.typicode.com>

| Test | Endpoint | Expected result |
|------|----------|-----------------|
| `test_get_all_posts` | `GET /posts` | Status 200, returns list of 100 posts with `id`, `title`, `body`, `userId` |
| `test_get_single_post` | `GET /posts/1` | Status 200, correct field values for post id=1 |

---

## CI / GitHub Actions

The workflow file `.github/workflows/tests.yml` runs automatically on every push and pull request to `main`.

Pipeline steps:
1. Check out code
2. Set up Python 3.12
3. Install Python dependencies
4. Install Google Chrome
5. Run API tests
6. Run UI tests


Actualizacion de prueba. 2222