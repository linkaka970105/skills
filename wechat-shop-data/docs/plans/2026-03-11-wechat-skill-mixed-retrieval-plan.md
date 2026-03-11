# WeChat Skill Mixed Retrieval Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the WeChat Shop skill so large list-to-detail workflows use deterministic mixed-mode retrieval rules instead of model-specific ad hoc expansion.

**Architecture:** Add a retrieval mode section and domain strategy matrix to the skill, then update reference docs so list endpoints explicitly point to the mixed-mode expansion policy and batch-capable endpoints are prioritized. The implementation is documentation-only but should be structured like a retrieval orchestration contract.

**Tech Stack:** Markdown documentation, Git

---

### Task 1: Add design and planning artifacts

**Files:**
- Create: `docs/plans/2026-03-11-wechat-skill-mixed-retrieval-design.md`
- Create: `docs/plans/2026-03-11-wechat-skill-mixed-retrieval-plan.md`

**Step 1: Create the design document**

Describe the mixed retrieval modes, deterministic thresholds, domain strategy matrix, and export workflow.

**Step 2: Create the implementation plan**

Capture the documentation update steps for `SKILL.md` and the relevant references.

**Step 3: Verify both files exist**

Run: `Get-ChildItem docs/plans`
Expected: both March 11 plan files are present

### Task 2: Update the main skill contract

**Files:**
- Modify: `SKILL.md`

**Step 1: Add a retrieval mode section**

Document `summary_only`, `detail_on_demand`, and `full_export`.

**Step 2: Add explicit expansion thresholds**

Document the fixed record-count rules so models do not improvise.

**Step 3: Add a domain strategy matrix**

Explain the required list/detail pairing for orders, products, and gift products, and the batch-first rule for stock.

**Step 4: Add large-task workflow guidance**

Document time slicing, pagination, de-duplication, chunking, concurrency, and retry guidance for export tasks.

### Task 3: Update reference docs to reinforce the policy

**Files:**
- Modify: `references/order-apis.md`
- Modify: `references/product-apis.md`
- Modify: `references/stock-apis.md`
- Modify: `references/marketing-apis.md`

**Step 1: Update order references**

Clarify that order list/search are collection stages and full-field exports require staged detail expansion.

**Step 2: Update product and gift references**

Clarify that list APIs return IDs and should enter bounded or export-mode detail expansion, not blind per-item conversational loops.

**Step 3: Update stock references**

Emphasize `batchgetstock` as the default bulk retrieval path.

**Step 4: Update marketing references**

Clarify whether list results are sufficient and how to treat them under the mixed retrieval policy.

### Task 4: Verify and publish

**Files:**
- Modify: `SKILL.md`
- Modify: `references/*.md`

**Step 1: Review the diff**

Run: `git diff -- docs/plans SKILL.md references`
Expected: documentation matches the mixed retrieval design

**Step 2: Check repository status**

Run: `git status --short`
Expected: only intended documentation files are modified or added

**Step 3: Commit**

Run: `git add docs/plans SKILL.md references && git commit -m "docs: optimize mixed retrieval strategy for wechat skill"`
Expected: commit created successfully

**Step 4: Push**

Run: `git push origin main`
Expected: remote branch updated
