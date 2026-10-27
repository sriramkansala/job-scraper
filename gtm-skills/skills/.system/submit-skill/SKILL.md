---
name: submit-skill
description: |
  Use this skill when the user wants to submit, contribute, or publish a GTM skill to the
  GTM Skills library (github.com/swan-gtm/gtm-skills, gtmskills.com), or update one of
  their existing skills or their creator profile there.
metadata:
  internal: true
---

Submit the user's GTM playbook to the GTM Skills library. The authoritative, always-current instructions live in the repo itself:

1. Fetch https://raw.githubusercontent.com/swan-gtm/gtm-skills/main/AGENTS.md
2. Follow its "Submitting a skill" flow exactly: interview the user (extract judgment, not just steps), draft the files from the repo's templates, run `node tools/validate.mjs`, then open a PR — or a "Submit a skill" issue if git isn't available.

Rules that never change:

- Only create or edit files under `skills/<the-user's-author-slug>/`.
- The skill folder name is permanent and globally unique — check for collisions first.
- Speak in GTM verbs in the skill body; never vendor tool names.
- Never include lifecycle or operational fields (`prefix`, `isDefault`, …) — content only.
- A `## What good looks like` section is mandatory; a skill without judgment gets rejected.
