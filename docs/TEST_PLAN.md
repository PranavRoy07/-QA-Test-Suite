# Test Plan — QA Automation Suite

## 1. Objective
Demonstrate end-to-end QA engineering practice: UI automation, API automation,
CI/CD gatekeeping, and structured reporting, across two applications under test.

## 2. Applications Under Test
| App | Type | URL |
|---|---|---|
| SauceDemo | E-commerce UI | https://www.saucedemo.com |
| DummyJSON | Public REST API | https://dummyjson.com |

> **Why DummyJSON and not FakeStoreAPI?** This suite originally targeted
> FakeStoreAPI. During a local run it returned Cloudflare `521` errors
> (origin server down) across every endpoint — a known, recurring issue for
> that service (see its GitHub issue tracker). DummyJSON is actively
> maintained with ~99.4% reported uptime, so the API suite was switched to
> it to keep the pipeline reliable for graders/interviewers running this on
> their own machine.

## 3. Tools & Stack
- **UI**: Playwright (sync API) + pytest, Page Object Model
- **API**: pytest + `requests`, plus a mirrored Postman/Newman collection
- **CI/CD**: GitHub Actions (runs on every push and PR)
- **Reporting**: `pytest-html` (self-contained HTML report) + JUnit XML, uploaded as CI artifacts

## 4. Scope — In
- **Login**: valid login, invalid password, locked-out user, empty required fields, unknown user
- **Cart**: add single/multiple items, badge count accuracy, cart contents, item removal, empty-cart state
- **Checkout**: full happy-path checkout, tax/total calculation, required-field validation (first name, last name, postal code)
- **Sort/filter**: name A–Z/Z–A, price low–high/high–low (see note below)
- **API — Products**: list, single-record fetch, schema validation, category filter, `limit` query param, invalid/nonexistent IDs, non-numeric IDs
- **API — Users/Auth**: list users, schema validation, user creation, login with valid/invalid/missing credentials
- **API — Errors**: malformed JSON body, negative IDs, unsupported HTTP methods, deleting nonexistent records

## 5. Scope — Out (explicitly)
- Cross-browser matrix (suite runs on Chromium only; Firefox/WebKit not covered)
- Performance/load testing
- Visual regression / pixel-diff testing
- Mobile viewport testing
- Accessibility (a11y) auditing
- Security testing (auth bypass, injection, etc.) beyond basic negative-input handling
- Database-level verification (both apps are black-box/third-party; no DB access)

### Scope note — "search and filter"
SauceDemo does not expose a free-text search box. Its equivalent control is the
product **sort** dropdown (name A–Z/Z–A, price low/high). Those four sort orders
are covered in `test_sort_and_filter.py` as the stand-in for this roadmap item.
If a search-capable target app is swapped in later, that file is the one to extend.

## 6. Environment Notes
- Live network access to `saucedemo.com` and `dummyjson.com` is required to run
  these suites (sandboxes with restricted egress will see connection failures —
  this is a network policy issue, not a test bug). CI runs on GitHub-hosted
  runners with unrestricted network, so the pipeline runs and reports normally
  there.
- SauceDemo credentials used: `standard_user` / `secret_sauce` (bug-free account),
  plus `locked_out_user` for the negative login case. See `docs/BUG_REPORTS.md`
  for other seeded-account behaviors.
- DummyJSON credentials used: `emilys` / `emilyspass` (one of its published
  test accounts — see dummyjson.com/docs/auth).
- Both subfolders (`ui-tests/`, `api-tests/`) and the repo root each have their
  own `pytest.ini`, so `pytest` works whether you run it from the root or from
  inside a subfolder. All three use `--import-mode=importlib` to avoid a
  module-name collision between the two `tests/` packages when run together
  from the root; the root config additionally sets `pythonpath = ui-tests` so
  the UI suite's `pages` package still resolves under that import mode.

## 7. How to Run Locally

```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium

# Run everything at once, from the repo root
pytest                               # all 38 tests (UI + API)
pytest -m smoke                      # smoke subset only, across both suites

# Or run a suite on its own
cd ui-tests && pytest && cd ..
cd api-tests && pytest -m negative && cd ..   # negative/error-path subset

# With an HTML report
pytest --html=report.html --self-contained-html

# Postman collection (requires Newman: npm install -g newman)
newman run postman/DummyJSON.postman_collection.json
```

## 8. Markers
Both suites share the same marker scheme so either can be filtered the same way:
- `smoke` — fast, critical-path checks
- `regression` — full functional coverage
- `negative` — invalid-input / error-path checks

## 9. CI/CD Gate
`.github/workflows/ci.yml` runs the UI suite, API suite, and Newman collection
as three parallel jobs on every push and pull request. Any test failure fails
the job (default pytest/newman exit-code behavior — nothing is suppressed),
so a red build blocks a merge rather than silently passing.
