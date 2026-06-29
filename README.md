# Dakota Chrome Extension — UI Automation

Automated UI tests for the **Dakota Marketplace** Chrome extension using **Selenium**, **pytest**, and **Allure**.

The suite installs the extension in Chrome, logs into the Dakota portal, opens the sidebar, and validates search, company profiles, tabs, contacts, and LinkedIn auto-search — **43 tests** in a fixed order (~15–20 minutes for the full suite).

---

## Table of contents

1. [Quick start (30 seconds)](#quick-start-30-seconds)
2. [What this project tests](#what-this-project-tests)
3. [Requirements](#requirements)
4. [Local setup (step by step)](#local-setup-step-by-step)
5. [How to run tests locally](#how-to-run-tests-locally)
6. [View reports](#view-reports)
7. [Jenkins setup and runs](#jenkins-setup-and-runs)
8. [Test execution order](#test-execution-order)
9. [Configuration reference](#configuration-reference)
10. [How a test run works](#how-a-test-run-works)
11. [Troubleshooting](#troubleshooting)
12. [Project layout](#project-layout)
13. [License](#license)

---

## Quick start (30 seconds)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy credentials.env.example credentials.env
python preflight_check.py --download-extension
pytest -m smoke -v
```

---

## What this project tests

| Area | What is verified |
|------|------------------|
| **Setup** | Extension installs via WebDriver BiDi; portal login; extension SSO |
| **Search** | Sidebar search results, scroll to end, load more |
| **Company** | Company details, General tab stats, account overview, type, metro area, website, LinkedIn, billing address |
| **Investors** | Tab visibility, results, count, load more button, load more data, metro areas |
| **Investment details** | Tab data, geography, industry, check size |
| **Platform details** | Platform description |
| **Contacts** | Results, count, load more, roles, URLs, emails, search, detail fields, back navigation |
| **LinkedIn** | Auto-search from a LinkedIn company page |

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or newer (3.11+ recommended) |
| **Google Chrome** | Latest stable build |
| **Internet** | Portal, extension download, and test sites (e.g. LinkedIn) |
| **Dakota account** | Valid Marketplace username and password |
| **Allure CLI** | Optional — only needed to open HTML reports locally |
| **Jenkins** | Optional — for CI runs on `windows-ui` |

---

## Local setup (step by step)

### Step 1 — Clone the repository

```bash
git clone https://github.com/TestWithMani/dakota_chrome_ext_ui.git
cd dakota_chrome_ext_ui
```

### Step 2 — Create a virtual environment

**Windows (PowerShell / CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Confirm Python version:

```bash
python --version
```

### Step 3 — Install Python packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Installed packages: `selenium`, `pytest`, `webdriver-manager`, `requests`, `allure-pytest`.

### Step 4 — Configure credentials

Copy the template and add your Dakota portal login:

**Windows:**

```bash
copy credentials.env.example credentials.env
```

**macOS / Linux:**

```bash
cp credentials.env.example credentials.env
```

Edit `credentials.env`:

```env
DAKOTA_USERNAME=your.email@dakota.com
DAKOTA_PASSWORD=your-password
```

| File | Purpose |
|------|---------|
| `credentials.env` | **Real** credentials — used by local `pytest` (gitignored) |
| `credentials.env.example` | **Template only** — safe to commit, no real passwords |

Jenkins does **not** read `credentials.env`. It uses the Jenkins secret `dakota-portal-creds`.

### Step 5 — Download the Chrome extension

```bash
python download_extension.py
```

Expected output:

- `extensions/dakota.crx` — downloaded package
- `extensions/dakota/` — unpacked extension (includes `manifest.json`)

> Tests also auto-download the extension if `extensions/dakota/manifest.json` is missing.

### Step 6 — Verify setup (optional)

```bash
pytest --collect-only -q
```

You should see **43 tests collected**.

Run only the first two setup tests (~2–3 min):

```bash
pytest tests/test_dakota_extension_installation.py tests/test_login_to_dakota.py -v
```

---

## How to run tests locally

### Preflight check (recommended before every run)

Run this first to validate Python version, credentials, extension files, and network access:

```bash
python preflight_check.py
```

If extension files are missing and you want auto-download:

```bash
python preflight_check.py --download-extension
```

### Full suite (recommended)

Runs all **43 tests** in order (install → login → search → company → tabs → contacts → LinkedIn):

```bash
pytest
```

With verbose output:

```bash
pytest -v
```

### Smoke suite (quick CI sanity)

Runs the critical test subset only:

```bash
pytest -m smoke -v
```

### Run a single test file

```bash
pytest tests/test_dakota_search_results.py -v
```

### Run a single test by name

```bash
pytest tests/test_dakota_search_results.py::test_dakota_search_results -v
```

### Run with visible Chrome (non-headless)

By default, Chrome opens **with a window** on your machine. Headless is only forced when `DAKOTA_HEADLESS=1`, `CI=true`, or `JENKINS_URL` is set.

To force headless locally:

```bash
set DAKOTA_HEADLESS=1
pytest
```

**macOS / Linux:**

```bash
export DAKOTA_HEADLESS=1
pytest
```

### Debug — pause after extension loads

Keeps Chrome open so you can inspect the floating button on `example.com`:

```bash
pytest --pause 30
```

Or set seconds via environment:

```bash
set DAKOTA_PAUSE_SECONDS=30
pytest tests/test_dakota_extension_installation.py
```

### What happens during a local run

1. **Session start** — extension downloaded if needed.
2. **Test 0** — `shared_driver` installs extension via BiDi, opens `example.com`.
3. **Test 1** — portal login + extension SSO on `shared_driver`.
4. **Tests 2–42** — `logged_in_driver` session logs in once; each test gets a fresh `dakota_sidebar` reset.
5. **After each test** — Allure captures steps, screenshots, and failure evidence.
6. **Outputs** — `allure-results/`, `test-results/pytest.xml`.

> **Note:** Failed tests are marked **skipped** in pytest/JUnit so the full suite continues. Original failure details remain in Allure and console logs.

---

## View reports

### Allure (recommended)

**Install Allure CLI** (one time):

- **Windows:** `scoop install allure` or download from [Allure releases](https://github.com/allure-framework/allure2/releases)
- **macOS:** `brew install allure`
- **Linux:** see Allure documentation

After `pytest`, open the report:

```bash
allure serve allure-results
```

This opens a browser with steps, screenshots, failure attachments, and environment info.

### JUnit XML

Generated at:

```text
test-results/pytest.xml
```

Used by Jenkins and other CI tools.

### Email template preview (design only)

Open in a browser — not used by pytest:

```text
jenkins/email-template-preview.html
```

---

## Jenkins setup and runs

### Jenkins overview

| Item | Value |
|------|-------|
| Jenkins URL | `http://110.93.205.18:8080` (default in `jenkins_setup.py`) |
| GitHub repo | `https://github.com/TestWithMani/dakota_chrome_ext_ui` |
| Branch | `main` |
| Job name | `Dakota-Chrome-Extension-UI` |
| Agent label | `windows-ui` |
| Credential ID | `dakota-portal-creds` |
| Chrome mode | Headless 1920×1080 |
| Duration | ~15–20 minutes (full suite) |

### One-time Jenkins provisioning

**Prerequisites:**

- Jenkins user with permission to create jobs and credentials
- `credentials.env` filled in **or** `DAKOTA_USERNAME` / `DAKOTA_PASSWORD` env vars set
- Network access to Jenkins from your machine

**Windows:**

```bash
cd dakota_chrome_ext_ui
.venv\Scripts\activate
pip install requests

set JENKINS_PASSWORD=your-jenkins-api-password
py -3 jenkins_setup.py
```

This script:

1. Creates or updates Jenkins credential `dakota-portal-creds` (username/password from `credentials.env`)
2. Creates or updates pipeline job `Dakota-Chrome-Extension-UI` with SCM → [TestWithMani/dakota_chrome_ext_ui](https://github.com/TestWithMani/dakota_chrome_ext_ui) (`main`, `Jenkinsfile`)

**Trigger first build from CLI:**

```bash
py -3 jenkins_setup.py --trigger-build
```

**Optional environment overrides:**

```bash
set JENKINS_URL=http://110.93.205.18:8080
set JENKINS_USER=your-jenkins-username
set GITHUB_BRANCH=main
```

### Run a build from Jenkins UI

1. Open Jenkins → job **Dakota-Chrome-Extension-UI**
2. Click **Build with Parameters**
3. Set parameters (or use defaults):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DEFAULT_EMAIL` | `usman.arshad@rolustech.com` | Primary email recipient |
| `ADDITIONAL_EMAILS` | (empty) | Extra recipients, comma-separated |
| `DAKOTA_CREDENTIALS_ID` | `dakota-portal-creds` | Jenkins credential for portal login |
| `INFRA_RETRY_COUNT` | `3` | Retries for timeout/WebDriver infra errors |
| `RUN_SMOKE_ONLY` | `false` | `true` = run 8 smoke tests only; `false` = full 43-test suite |
| `RUN_ALLURE` | `true` | Publish Allure report in Jenkins |
| `SEND_EMAIL` | `true` | Send HTML summary email after build |

**Quick PR / sanity check:** set `RUN_SMOKE_ONLY=true` (~5–8 min).  
**Full regression:** leave `RUN_SMOKE_ONLY=false` (~15–20 min).

4. Click **Build**
5. When finished, open:
   - **Allure Report** — steps, screenshots, failures
   - **Pytest HTML** / **JUnit** — under build artifacts
   - **Email** — pass rate, duration, report links

### Jenkins pipeline stages

| Stage | What it does |
|-------|----------------|
| **Checkout** | Pulls code from GitHub |
| **Resolve Python** | Finds Python 3.10+ on the agent |
| **Setup Python Environment** | Creates `.venv-jenkins`, installs `requirements.txt` + `requirements-ci.txt` |
| **Download Extension** | Runs `download_extension.py` |
| **Prepare Report Directories** | Clears `test-results/`, `allure-results/`, Chrome profile |
| **Static Validation** | `pytest --collect-only` — confirms smoke (8) or full (43) selection |
| **Run Tests** | Smoke or full suite with portal credentials from Jenkins |
| **Publish Reports** | JUnit, HTML, JSON, Allure |
| **Post** | Email notification, archive artifacts |

Scheduled cron is **disabled** in the Jenkinsfile. Builds are manual or parameterized only.

---

## Test execution order

Tests always run in this order (defined in `conftest.py`):

| # | Test |
|---|------|
| 0 | `test_dakota_extension_installation` |
| 1 | `test_login_to_dakota` |
| 2 | `test_dakota_search_results` |
| 3 | `test_dakota_search_scroll` |
| 4 | `test_dakota_search_load_more` |
| 5 | `test_dakota_company_details` |
| 6 | `test_dakota_company_general_tab` |
| 7 | `test_dakota_company_contacts_count` |
| 8 | `test_dakota_company_account_overview` |
| 9–13 | General tab fields (type, metro, website, LinkedIn, billing) |
| 14–16 | Company tabs (investors, investment details, platform details) |
| 17–21 | Investors tab tests |
| 22–25 | Investment details tab tests |
| 26 | Platform description |
| 27–41 | Contacts tab tests |
| 42 | `test_dakota_linkedin_company_auto_search` |

Search terms used by tests are in `utils/config.py` (e.g. BlackRock, Microsoft, Databricks).

---

## Configuration reference

| Variable / file | Default | Purpose |
|-----------------|---------|---------|
| `credentials.env` | — | Local `DAKOTA_USERNAME`, `DAKOTA_PASSWORD` |
| `utils/config.py` | — | Company names and URLs for each scenario |
| `DAKOTA_HEADLESS` | off locally | `1` / `true` → headless Chrome |
| `DAKOTA_PAUSE_SECONDS` | `0` | Pause after extension load (debug) |
| `CHROME_WINDOW_WIDTH` | `1920` | Browser width |
| `CHROME_WINDOW_HEIGHT` | `1080` | Browser height |
| `CHROME_USER_DATA_DIR` | temp dir | Persistent Chrome profile path |
| `CHROME_USER_DATA_CLEANUP` | off locally | `true` → delete profile after session |
| `CI` | off locally | Set by Jenkins; enables headless |
| `JENKINS_URL` | — | If set, enables headless (Jenkins agent) |
| `BUILD_URL` | — | Jenkins only; linked in Allure reports |

**Pytest CLI options** (see `pytest.ini`):

- `--alluredir=allure-results` — always on
- `--junitxml=test-results/pytest.xml` — always on
- `--pause N` — visual pause after extension install

---

## How a test run works

```text
download_extension.py
        ↓
conftest: install extension (BiDi) → open example.com
        ↓
test_login_to_dakota: portal login → open sidebar → Salesforce SSO
        ↓
logged_in_driver (session): one browser for tests 2–42
        ↓
Each test: dakota_sidebar.reset_for_test()
        → navigate portal → ensure logged in → open sidebar
        → run verify_* steps (Allure steps + screenshots)
        ↓
Reports: allure-results/ + test-results/pytest.xml
```

Portal URL: [Dakota Marketplace](https://dakotanetworks.my.site.com/dakotaMarketplace/s/)

Extension ID: `pkjcjmhoaajnghcgbkkdfgakcbdnpefj` (Dakota Marketplace)

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `Dakota credentials not found` | Create `credentials.env` from `credentials.env.example` |
| Extension not found | Run `python download_extension.py` |
| Chrome / ChromeDriver mismatch | Update Chrome to latest; `webdriver-manager` fetches matching driver |
| Login fails | Check username/password; confirm account works in a normal browser |
| Tests timeout on LinkedIn | Known flaky test; check Allure screenshot and network |
| Headless when you want UI | Unset `DAKOTA_HEADLESS`, `CI`, and `JENKINS_URL` |
| Jenkins: agent offline | Ensure `windows-ui` node is connected and online |
| Jenkins: wrong credentials | Verify `dakota-portal-creds` in Jenkins → Credentials |
| Allure `command not found` | Install Allure CLI or view report from Jenkins build |

---

## Project layout

```text
dakota_chrome_ext_ui/
├── conftest.py                 # Fixtures, Chrome setup, test ordering, Allure hooks
├── download_extension.py       # Download .crx from Chrome Web Store
├── preflight_check.py          # Fast setup/network/credentials validation
├── credentials.env.example     # Credential template (commit this)
├── credentials.env             # Real credentials (gitignored — do not commit)
├── pages/
│   ├── dakota_auth.py          # Portal login + extension SSO
│   ├── dakota_extension_actions.py
│   └── dakota_sidebar_page.py  # Main page object + verify methods
├── tests/                      # 43 test modules
├── utils/
│   ├── allure_helpers.py       # Steps, screenshots, failure bundles
│   ├── company_types.py
│   ├── config.py
│   └── credentials.py
├── jenkins/email-template-preview.html
├── Jenkinsfile                 # CI pipeline
├── jenkins_setup.py            # Provision Jenkins job + credential
├── pytest.ini
├── requirements.txt            # Local + core deps
├── requirements-ci.txt         # Jenkins-only pytest plugins
└── LICENSE
```

---

## License

This project is licensed under the [MIT License](LICENSE).
