# Bug Reports

These are real, reproducible findings from exploring the two applications
under test. SauceDemo intentionally ships several of its bugs behind specific
seeded test accounts (a common QA-practice pattern); DummyJSON's is a
documented API contract gotcha that's easy to miss and worth flagging to
anyone writing tests against it.

---

### BUG-001 — `problem_user` account renders broken product images
**App**: SauceDemo
**Severity**: Medium
**Component**: Inventory page

**Steps to reproduce**:
1. Go to https://www.saucedemo.com
2. Log in with `problem_user` / `secret_sauce`
3. Observe the inventory page

**Expected**: Each product shows its own distinct product photo.
**Actual**: All products render the same broken/mismatched placeholder image (a dog photo), regardless of item.

**Notes**: Not covered by the automated suite (which uses `standard_user`) —
flagging here as a manual-exploration finding worth a dedicated negative-path
test if `problem_user` coverage is added later.

---

### BUG-002 — `error_user` breaks the checkout "Remove" flow
**App**: SauceDemo
**Severity**: High
**Component**: Cart / Checkout

**Steps to reproduce**:
1. Log in with `error_user` / `secret_sauce`
2. Add any item to the cart
3. Go to the cart page and click "Remove" on that item

**Expected**: Item is removed from the cart, badge count updates.
**Actual**: The remove action fails silently (or throws a JS error in console)
— the item and/or badge count does not update correctly.

**Impact**: High — this account represents a user who cannot reliably manage
their own cart, which would block a real checkout.

---

### BUG-003 — `visual_user` shows layout/rendering regressions
**App**: SauceDemo
**Severity**: Low
**Component**: Inventory page layout

**Steps to reproduce**:
1. Log in with `visual_user` / `secret_sauce`
2. Compare the inventory page layout against the `standard_user` session

**Expected**: Consistent spacing, alignment, and cart icon rendering.
**Actual**: Noticeable layout drift (misaligned cart icon, inconsistent
spacing) versus the standard account.

**Notes**: A good candidate for visual-regression tooling (out of scope for
this suite — see `docs/TEST_PLAN.md` §5) rather than functional assertions.

---

### BUG-004 — `performance_glitch_user` has an anomalous load delay
**App**: SauceDemo
**Severity**: Low / Performance
**Component**: Login → Inventory transition

**Steps to reproduce**:
1. Log in with `performance_glitch_user` / `secret_sauce`
2. Time the delay between submitting login and the inventory page becoming interactive

**Expected**: Load time comparable to `standard_user` (near-instant).
**Actual**: Multi-second delay before the inventory page is usable.

**Impact**: Low functionally, but worth a dedicated performance-budget test
(e.g. asserting page-interactive time is under a threshold) if this account
is folded into the automated suite.

---

### BUG-005 — DummyJSON write endpoints (`add`/`update`/`delete`) don't actually persist
**App**: DummyJSON
**Severity**: Medium (API contract gotcha — documented, but easy to miss)
**Component**: `POST /products/add`, `PUT /products/{id}`, `DELETE /products/{id}` (and the equivalent `users`/`posts` endpoints)

**Steps to reproduce**:
1. `POST https://dummyjson.com/products/add` with a new product body
2. Note the `id` returned in the `201` response
3. `GET https://dummyjson.com/products/{that id}`

**Expected**: The newly created product is retrievable (standard REST
create-then-read behavior).
**Actual**: The write call returns a convincing success response with a new
`id`, but nothing is actually persisted server-side — a follow-up `GET` for
that id returns `404`, and the global product list never includes it.
DummyJSON's own docs confirm this is intentional ("will not add it into the
server... will simulate a POST request").

**Impact**: Medium — any test written assuming create-then-read semantics
(a common pattern) will silently pass on the create step and then fail or
give false confidence on the read step. Worth calling out explicitly to
whoever inherits this suite, since it's easy to assume a `201` means the
record is really there. `test_create_user_returns_201` in
`api-tests/tests/test_users.py` only asserts the simulated response shape,
not persistence, for exactly this reason.

---

## Summary Table

| ID | App | Severity | Status |
|---|---|---|---|
| BUG-001 | SauceDemo | Medium | Documented, not yet automated |
| BUG-002 | SauceDemo | High | Documented, not yet automated |
| BUG-003 | SauceDemo | Low | Documented, not yet automated |
| BUG-004 | SauceDemo | Low | Documented, not yet automated |
| BUG-005 | DummyJSON | Medium | Documented gotcha, reflected in test design |
