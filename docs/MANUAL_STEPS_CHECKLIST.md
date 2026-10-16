# Manual Steps Checklist — Phases 1 & 7

These are the roadmap items I can't do for you (they live on accounts I don't
have access to). Everything else in this repo is done — this is the last mile.

## Phase 1 — surface what already exists (do this first, it's the 5-minute
highest-ROI item on the whole roadmap)

- [ ] Go to your **AutoShop QA Suite** GitHub repo → make sure it's **public**
- [ ] On your GitHub profile → **Customize your pins** → pin AutoShop QA Suite
- [ ] Add AutoShop QA Suite to your **portfolio site** (link + one-line description
      + CI badge if it has one)
- [ ] Add it as a line item under Projects on your **resume**

Don't wait for the rest of this checklist — do this part today, independent
of everything else.

## Phase 7 — ship this new project

- [ ] Push this `qa-test-suite` folder to a new public GitHub repo
- [ ] In `README.md`, replace `YOUR_USERNAME/YOUR_REPO` in the badge URL with
      your real path so the badge goes live
- [ ] Confirm the badge renders green on the repo's GitHub page (push once,
      let Actions run, refresh)
- [ ] Pin this repo alongside AutoShop QA Suite
- [ ] Add it to your portfolio site with the **CI badge visible** — that's the
      fastest trust signal a reviewer scans for
- [ ] Add this resume bullet (edit as needed):

  > Built and automated a UI and API test suite (Playwright, pytest) with
  > CI/CD via GitHub Actions across two applications, including test
  > reporting and documented bug reports.

## Before pushing — quick local sanity check

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
cd ui-tests && pytest -m smoke && cd ..
cd api-tests && pytest -m smoke && cd ..
```

If both smoke subsets pass locally, CI will pass too — push with confidence.
