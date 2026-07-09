# DirectScribe — feature list

Compiled from what's actually live on directscribe.ca (not aspirational). Each
item cites the page it's advertised on, so this stays traceable back to the
source copy rather than drifting into its own thing. Update this alongside
the site — if a feature's wording changes there, it should change here too.

## Core dictation workflow

- **Dictate to your own template, not the other way around.** Speak the
  encounter in free-form, out of order, with asides — DirectScribe molds the
  dictation into your SOAP note, periodic health exam, or referral letter.
  The template conforms to how you talk; you don't conform to the template.
  *(Home, Guide: templates)*
- **Two-step pipeline: transcription, then intelligence.** Your chosen STT
  vendor turns audio into text; your chosen intelligence provider — on-device
  Apple Intelligence, a cloud vendor, or a local LM Studio model — shapes that
  text into your template. *(Home, Security)*
- **Review and paste — no EMR integration.** The finished note pastes into
  your EMR as plain text. DirectScribe never integrates with or writes to
  your EMR directly. *(Home, Security)*
- **Your dictation, not the room.** The physician dictates into the mic and
  DirectScribe captures their voice — it isn't an ambient scribe, with no
  microphone left open on the visit. *(Home, Security, Compliance)*
- **Illustrative in-app mockup on the homepage** shows the dictation → SOAP
  note flow with ALL-CAPS headings and a bracketed placeholder token.
  *(Home)*

## Bring-your-own-vendor (BYOK)

- **Choose your own transcription and intelligence vendors and pay them
  directly** — no DirectScribe markup on top of vendor API pricing, unlike
  bundled AI scribes. *(Home, Pricing)*
- **No vendor lock-in.** Switch STT or intelligence providers in Settings at
  any time; no data migration, no reinstall. *(Home, Compliance, Support)*
- **Launch transcription vendors:** Deepgram (recommended default, BAA on
  request, ~CAD $8/mo at ~440 notes), ElevenLabs (BAA on enterprise plans
  only, ~CAD $7–12/mo), and Cohere (high-quality; confirm terms/pricing with
  Cohere). *(Vendor guides, Cost)*
- **Intelligence providers:** Apple Intelligence for on-device note-shaping
  (built into macOS 26+, no key, no API cost, no BAA needed — the transcript
  stays on your Mac; Private Cloud Compute fallback planned for macOS 27),
  OpenAI (BAA by email to individuals, ~CAD $2–8/mo), Anthropic (small-customer
  BAA status unverified — treated as conditional), and LM Studio for fully
  local note-shaping via a local model. *(Vendor guides, Cost)*
- **API keys live in the macOS Keychain** — never in plain files, never sent
  to DirectScribe. There is no DirectScribe account and no DirectScribe
  server. *(Home, Security)*
- **Step-by-step vendor setup guides** for each supported vendor, including
  what privacy paperwork (BAA) each does and does not offer at individual
  scale. *(Vendor guides)*

## Templates

- **Plain-text templates, no code.** Two conventions: ALL-CAPS lines become
  section headings; `[bracketed text]` marks a placeholder described in
  plain language. Takes about five minutes to author one. *(Guide:
  templates)*
- **The app never silently invents templates.** If a dictation mentions a
  note type with no matching template, the note still saves — the template
  library stays exactly what you authored. *(Guide: templates)*
- **Worked examples included** for SOAP visit, periodic health exam, and
  referral letter templates. *(Guide: templates)*
- **Starter template set referenced in the in-app mockup:** periodic health
  exam, SOAP visit, chronic disease follow-up, referral letter, prescription
  refill. *(Home)*

## Retention and deletion

- **Retention on your schedule: 7, 30, or 90 days**, or clear a whole
  session immediately once the note is safely in your EMR. *(Home, Security,
  Compliance)*
- **Deletion honesty, stated precisely.** "Deleted" means deleted from the
  file system on your schedule; FileVault protects residual storage; backups
  you configure may retain copies. Never claimed as "gone from every disk."
  *(Home, Security, Compliance, PIA template)*
- **FileVault-aware design.** DirectScribe's data directories are excluded
  from Time Machine; the app explains the APFS copy-on-write residue
  trade-off rather than overclaiming secure erase. *(Security)*

## Transparency log

- **PHI-free, tamper-evident transparency log** of every transmission (what
  was sent, to which vendor, when) and every deletion (what, when, trigger).
  Hash-chained with a Keychain sequence checkpoint to catch tail-truncation.
  *(Home, Security, Compliance, PIA template)*
- **Never logs PHI, filenames, or template names** — only opaque identifiers
  and artifact types. *(Security)*
- **Explicitly scoped honesty:** not a PHIPA s.10.1 access-audit log (that
  provision covers who *views* a record; DirectScribe logs sends and
  deletes, not access). The EMR remains the system of record. *(Security,
  Compliance)*

## Security and privacy design

- **No DirectScribe servers.** PHI never touches DirectScribe infrastructure
  because none exists in the data path — recordings and notes go straight
  from your Mac to the vendors you chose. *(Home, Security, Compliance)*
- **Sandboxed app** — runs in the macOS App Sandbox with least-privilege
  system access. *(Home, Security)*
- **No telemetry, no analytics, no crash reporting, no phone-home.** The
  only self-initiated network call is a weekly version-check against
  `directscribe.ca/version.json` (has an off switch, doesn't render or
  follow any URL from that file). *(Security)*
- **Canada-first compliance framing** — PIPEDA plus provincial health-privacy
  law (PHIPA in Ontario); not marketed against US HIPAA. *(Security,
  Compliance)*

## Licensing

- **Offline license validation** — a cryptographically signed license key
  checked on your Mac. No account, no sign-in, no server that can lock you
  out mid-clinic. *(Home, Security, Pricing)*
- **Licensing is honesty enforcement, not DRM.** No binary obfuscation,
  anti-debugging, or scattered secret checks. Apple notarization is the real
  integrity control. *(Security)*
- **Every license state stays functional for viewing.** Viewing, search,
  export, and deletion always work — even unlicensed or expired. Only
  recording, transcription, and note generation are license-gated.
  *(Security, Support)*
- **7-day trial**, started explicitly (never silent). *(Home, Pricing,
  Contact)*

## Built to outlast your EMR

- **Deliberately decoupled from your EMR's release pace.** EMRs are framed
  as data repositories for clinical care, not innovation surfaces — speech-
  to-text and AI move faster than EMRs ever will, so DirectScribe stays
  separate (dictate, review, paste) rather than integrating in a way that
  ties its pace to the EMR vendor's. *(Home)*
- **Vendor swaps without EMR migration** — when a better or cheaper
  transcription/intelligence vendor arrives, switch in Settings; the EMR
  keeps being the system of record throughout. *(Home)*

## Data-pathway control (Support page framing)

- **You control the data pathways** — built-in provider settings put the
  choice of who ever sees patient audio/text in the physician's hands, not
  DirectScribe's. *(Support)*
- **Support promise, stated plainly:** email responses and batched
  fixes/feature changes on a monthly cadence — no 24/7 line, no live chat,
  no same-day SLA. Framed as a consequence of the app not requiring
  hour-to-hour dependence. *(Support)*
- **Custom feature requests accepted** as part of support, as long as they
  don't change the app's overall nature or how it's designed to work.
  *(Pricing, Support)*

## Compliance Centre

- **Privacy Impact Assessment (PIA) template** aligned to Ontario IPC
  AI-scribe guidance (January 2026), with DirectScribe-specific prompts.
  *(Compliance)*
- **Patient-consent wording** plus a clinic-responsibility checklist
  (FileVault, network protection, signed vendor agreements). *(Compliance)*
- **"How the design maps to common assessment questions"** — a table
  mapping typical PIA questions directly to DirectScribe's design choices.
  *(Compliance)*
- **Explicit practice-scope boundary:** built for physicians in private
  practice running their own clinic and EMR; not designed or licensed for
  hospital or hospital-based-clinic deployment. *(Compliance)*
- **Not-legal-advice framing** throughout — general information to support
  the clinic's own assessment, not a substitute for a privacy lawyer or
  professional college guidance. *(site-wide footer, Compliance)*

## Pricing

- **Single flat tier, no feature gating.** CAD $39/month or $399/year
  (~2 months free). Every feature included regardless of plan. *(Pricing)*
- **Honest all-in cost framing** — software fee shown separately from
  typical vendor API spend (~CAD $10–15/month), landing around CAD $49–55
  all-in versus $99–215/month bundled incumbents (Heidi Health, Scribeberry,
  Tali AI, Dragon Medical One). *(Pricing, Cost breakdown)*
- **Cost breakdown page** with static tables by vendor choice and patient
  volume, using figures verified July 2026. *(Cost breakdown)*
- **License key delivered by email** — no account, no checkout system.
  *(Pricing)*

## Trial and onboarding

- **Not a self-serve download.** Early access is a manual, vetted intake
  flow via the Contact page rather than an instant DMG download. *(Contact)*
- **CPSO-verified intake.** Requires a College of Physicians and Surgeons of
  Ontario registration number to confirm the applicant is a real,
  currently-registered physician — framed as the current Ontario-first
  rollout mechanic, not a permanent restriction (DirectScribe itself targets
  private-practice physicians across Canada). *(Contact)*
- **Secure server-side contact form** — submits over HTTPS directly to a
  Cloudflare Worker with no third-party form service and no data stored in
  between. *(Contact)*
