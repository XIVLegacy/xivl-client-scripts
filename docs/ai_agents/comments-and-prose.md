# Comments and prose

Delete explanatory comments unless they preserve a fact the code cannot carry
on its own. This page is the canonical comment and prose doctrine for the
corpus builders, validator, workflow, and tracked documentation.

Deletion is the default. Keep a comment only when it records one of these:

- a current parser, corpus, or gate invariant
- a decompiler or client quirk that explains a non-obvious branch
- an evidence or provenance citation
- a safety or immutability constraint
- an API or command contract not inferable from names and types

Shorten the remaining comments to about one line at the use site. Move a longer
contract to this policy tier or the relevant corpus/tool page and leave a
short pointer. When unsure, keep one line and flag it in review notes.

Comment length and punctuation are style guidelines. Clarity, correctness,
source quotations, licensing, and provenance justify exceptions.

Source and evidence identifiers are exempt from shortening. Preserve them
verbatim, including dates and content hashes.

Generated output is data. Treat comments in `lua/scripts/`, sidecars,
`registry.json`, and `napi_index.json` as generated corpus content. Preserve it
exactly or update the owning builder and regenerate. Never hand-edit a
decompiled script to improve its prose.

Python docstrings and command help are runtime text. Treat them as public
contracts. Tighten them when needed, but keep the pointer to the tool or
artifact contract they describe.

Authored Markdown leads with the subject and describes the current contract.
It does not narrate a migration, a branch, a prior cleanup, or an agent's
research process.

Examples of the intended shape:

```python
# Re-derive lineCount from the published .lua.
```

```python
# Sort callsites by script and line for reproducible output.
```

Delete narration that repeats the code:

```python
# Build the inverted index below.
```

## Authored public prose

Public prose uses a plain, direct register.

Keep public claims timeless. Remove dates that only narrate our own
implementation, generation, retrieval, review, reconciliation, or
batch-processing history. Retain dates that belong to external source or
provenance metadata, actual evidence observations or captures, retail build or
source identity, legal metadata, or required vendor artifact names.

All tracked authored prose and structured descriptions state current evidence or
contracts. They are not prompts, assignments, review summaries, checkout state,
internal milestones, or work-session plans.

- Avoid awkward compounds and strings of modifiers. Rewrite the sentence
  rather than joining more words with hyphens. Preserve established technical
  terms, identifiers, and quoted source text.
- Use semicolons sparingly, preferring periods, commas, or short lists.

Internal working docs are outside this public policy tier.
