# Test authoring

A test should catch a demonstrated bug or a distinct supported behavior or
failure path. Extend an existing check before adding a new fixture or runner.
Changed lines, including AI-authored changes, do not by themselves need tests.

## Choose the claim and oracle

- Name the defect or supported branch and the assertion that detects it.
- Keep expected values independent of the implementation under test. Use
  literal decoded fields, instruction operands, paths, output bytes, or errors
  supported by the contract. A round trip alone can preserve a shared mistake.
- Exercise malformed input only when it reaches a supported parser or failure
  mechanism. Another identifier through identical code is not new coverage.
- Keep preservation, atomic publication, root rejection, and intended error
  assertions when they protect distinct failure paths.

Keep claims within the [evidence policy](evidence-and-claims.md).

## Choose the smallest input

Start with a Python function or parser over authored text or bytes. For Lua
bytecode analysis, build a small synthetic chunk with the instructions needed
to distinguish the branch, literal, arity, or uncertainty under test. The
[quest tests](../../tools/tests/test_quest_contracts.py) show this pattern.
Use a temporary tree for builder publication and source-root behavior. Invoke
a CLI when argument selection, exit status, or process output is the claim.
Use synthetic input instead of the full corpus when it can expose the regression.

Check all relevant data rows and joins in a cheap integrity pass. Choose
integration cases by distinct parser, source mode, or publication path rather
than repeating a complete pipeline per row. Retain any row with unique logic.
When reducing cases, state omitted input/assertion combinations and resulting
coverage loss for review. Distinguish sampling loss from proven equivalent
deduplication, and retain applicable data-wide checks in the same change.

## Reuse baselines without weakening validation

Load an unchanged retained report and schema once and treat them as immutable.
Copy the branches a mutation changes, including every mutable ancestor. Use a
full copy when isolation requires it. Do not reparse an unchanged report for
each assertion or let one case change the baseline for another.

A localized schema check may replace a repeated full traversal only when it
preserves all applicable constraints. Resolve references through the complete
schema, validate the changed object, and account for ancestor and sibling
constraints. Keep a full positive report/schema integration check. If that
equivalence cannot be established, retain full validation.

Schema shape, semantic joins, content digests, provenance pins, and source
reproduction are separate responsibilities. Keep full semantic rejection
checks when narrowing schema work. Re-sign a mutated report when testing a
semantic error beyond its digest, then assert the intended error and that a
stale digest did not cause rejection. Regeneration parity does not replace an
independent mutation test. See [schema ownership](../../tools/README.md#schema-ownership).

## Keep public and source checks distinct

Public metadata, schema, and synthetic tests must run without private corpus
bytes. Do not place them under a class-wide private-source skip. Source
reconstruction and byte-identity tests need an explicit source mode and a
clear skip when optional inputs are absent. A missing or invalid explicitly
selected root must fail rather than silently use a retained report or another
root. Public metadata checks do not prove private source bytes.

Use the [tool reference](../../tools/README.md#validation) for public absence
and hydrated-root modes. Preserve source hashes, provenance, and reproduction
checks in their owning boundaries. The [retail validation policy](retail-input-validation.md)
owns restricted-input claims and output limits. Authored public fixtures must
contain synthetic or redistributable bytes, not copied retail inputs.

## Preserve entry points and price material costs

Use the existing unittest discovery and standalone contract runners. Keep
`tools/test_retail_script.py` directly runnable: normal and credentialed
workflows call it separately. Its real JAR runs compare deterministic output
against literal expected bytes, so matching two outputs alone is insufficient.

Keep the separate retail-script workflow invocation even though the corpus
gate also invokes it. Boundary or JSON errors can stop the gate before focused
tests, and the separate step preserves retail-contract failure diagnostics.
Grant schemas and verifier constants also enforce independent boundaries.

When setup, repeated report scans, or child processes create material cost,
use runtime, source, or process-count evidence to locate it. Do not invent
fixed test budgets or time every tiny test. Reuse a required validation run
when it can answer the cost question, and state unmeasured savings as such.

For tool changes, run the focused check and full corpus gate in the documented
source mode. Use the [tool reference](../../tools/README.md#commands) for commands and lint.
Fixture economy does not replace the full gate or expand the retail-input grant.
