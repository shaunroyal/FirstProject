---
name: pr-description
description: Draft a pull request description from the issue, plan, review notes and diff, following .github/pull_request_template.md. Outputs text for the developer to edit and submit.
argument-hint: "<issue-id>"
disable-model-invocation: true
---

# /pr-description

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, every file in `docs/work/<issue-id>/`, and `.github/pull_request_template.md`.

## Steps

1. Read the diff: `git diff <base>...HEAD` and `git log <base>..HEAD --oneline`.
2. Fill in **every** section of the PR template, in its order and with its headings:
   - **Summary:** what changed and why, in 2–5 bullets, from `issue.md` and the diff.
   - **Issue:** the link or ID.
   - **Work files:** replace `<issue-id>` with the real ID.
   - **Testing:** commands actually run and their results, from `plan.md` step notes. Don't claim tests you have no evidence of.
   - **Risks and follow-ups:** from `plan.md` risks, and `review.md` items marked Won't fix or Defer.
   - **Definition of done:** tick only items you can see evidence for. Leave the rest unticked and say what's missing.
3. Flag blockers at the top of your reply, not inside the PR text: a plan that isn't `Approved`, unticked plan steps, or unresolved Critical or High findings.

## Output

Return the PR body as one Markdown code block, ready to paste. Don't create or update the PR yourself. The developer edits and submits it.
