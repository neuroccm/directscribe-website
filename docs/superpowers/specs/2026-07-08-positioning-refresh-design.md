---
date: 2026-07-08
topic: directscribe-website-positioning-refresh
origin: user request, grounded in CohereMedicalScribe/docs/brainstorms/2026-07-02-directscribe-commercialization-requirements.md
---

# DirectScribe website — positioning refresh

## Summary

The original commercialization brainstorm scoped DirectScribe to "solo outpatient primary-care physicians in Canada." The product owner wants to broaden that: it's for **doctors of any specialty, in private practice, running their own clinic and EMR** — explicitly not hospitals or hospital-based clinics. Geographically the product is Canada-wide, rolling out to Ontario first (other provinces on request — that detail already lives on `/contact/` next to the CPSO ask and is unchanged by this pass). Also: rename the "audit log" feature away from audit/auditor language (keep the underlying feature and its PHIPA s.10.1 legal disambiguation), and weave in three value props that don't currently have a strong home on the site — template-conforms-to-you, cost/customization versus other scribes, and future-proofing versus EMRs.

## Decisions (resolved via brainstorming)

1. **Audit-log rename**: rename to "transparency log" everywhere it's *our* feature name. The legal phrase "PHIPA s.10.1 access-audit log" stays verbatim — that names the actual statute provision, not our product. `validate.py`'s `("/security", "s.10.1")` and `("/compliance/index", "s.10.1")` requirements need no change.
2. **Hospital-exclusion placement**: homepage hero + Compliance Centre. Not repeated on every page.
3. **Ontario-rollout placement**: unchanged — stays on `/contact/` only (rollout-phase/funnel detail, not a permanent identity claim).
4. **Value-prop content scope**: balanced pass — reword existing bullets for "template conforms to you" and "cost/customization" (both already partially present in spirit); add exactly one new homepage section for future-proofing/EMR-decoupling, since that idea has no home on the site today.

## Changes by file

### `src/layout.html`
Footer "about" blurb: `"...for solo outpatient primary-care physicians in Canada. Built by a physician."` → `"...for physicians in private practice across Canada. Built by a physician."`

### `src/pages/index.html`
- Meta description: drop "primary-care"/"outpatient," keep Canada-wide framing.
- Hero lead paragraph: insert "— the template molds to how you dictate, not the other way around —".
- Hero note: expand to carry the private-practice/not-hospitals boundary while preserving the required phrase "only the physician's voice":
  > "For doctors in private practice across Canada — running their own clinic and EMR, not hospitals or hospital-based clinics. Only the physician's voice is ever recorded — never the patient."
- Feature bullet "Dictate to your template": sharpen with the same "molds to you, not the other way around" framing.
- Feature bullet "Bring your own vendors": add a cost-effectiveness clause ("no per-seat markup like bundled AI scribes charge").
- Feature bullet "Built by a physician": drop "outpatient," keep the hospital-IT-department contrast (already thematically aligned).
- "audit log" → "transparency log" (1 occurrence).
- New section **"Built to outlast your EMR"**, placed after the existing "What runs where" section:
  - Eyebrow: "Built to outlast your EMR"
  - H2: "Speech-to-text and AI move faster than EMRs ever will"
  - Lead: EMRs are data repositories for clinical care, not innovation surfaces; DirectScribe stays deliberately separate — dictate, review, paste — and that gap is the point.
  - Two-column body: (a) vendor-swap freedom — switch STT/intelligence providers in Settings without waiting on an EMR vendor or migrating data; (b) EMR stays the system of record while DirectScribe stays free to move as fast as the AI landscape does.
  - Reuses existing `.grid-2` / `.sec-head` classes — no new CSS.

### `src/pages/security.html`
- Section heading "The audit log — and what it is not" → "The transparency log — and what it is not."
- All other "audit log" references (4 total) → "transparency log." The "PHIPA s.10.1 access-audit log" legal phrase is untouched.

### `src/pages/compliance/index.html`
- "audit log" → "transparency log" (2 occurrences); PHIPA s.10.1 legal phrase untouched.
- New short paragraph near the top, in the page's existing honest-boundary voice: built for physicians in private practice running their own clinic and EMR; not designed or licensed for hospital or hospital-based-clinic deployment — institutional use carries governance, security, and integration requirements this product doesn't address.

### `src/pages/pricing.html`
Table caption: "solo outpatient practice" → "solo private practice."

### `src/pages/cost.html`
Lead paragraph: "solo outpatient practice" → "solo private practice."

## Validation impact

- No `validate.py` REQUIRE/DENY changes needed. The s.10.1 requirement is satisfied by the untouched legal phrase; the `/index` requirements ("your dictation. your vendors. your mac.", "backups you configure may retain copies", "only the physician's voice") all remain present verbatim.
- Rebuild + `python3 validate.py` after edits; spot-check the new homepage section and hero note in a local preview before shipping.

## Out of scope this pass

- Any further Ontario/rollout copy changes beyond what already exists on `/contact/`.
- New dedicated sections for cost/customization beyond the existing `/pricing/` "honest all-in number" section and the reworded homepage bullet.
- Renaming "audit log" in the underlying app (CohereMedicalScribe/DirectScribe repo) or its planning docs — this pass is website copy only.
