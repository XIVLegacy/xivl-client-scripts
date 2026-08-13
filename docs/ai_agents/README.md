# AI-assisted contributions

AI-assisted changes follow this repository's contribution policy. The
contributor owns the change and must be able to explain its scope, evidence,
and verification.

Use [evidence and claims](evidence-and-claims.md) before promoting a fact into
tracked documentation or a generated product.

## Contribution policy

- Keep changes inside this repository's owned corpus, tools, schemas, and
  documentation unless a task explicitly names another surface.
- Treat `lua/` as published client evidence. Do not hand-edit scripts,
  sidecars, or generated indexes. Use the documented builders and run the
  repository gate.
- Keep explicit external `--lua-root` inputs in research runs only. They have
  no workspace-relative default and are not normal gate inputs.
- Preserve source and evidence citations verbatim, including dates. Cite a
  promoted artifact by its own name and a sha256 of the promoted content.
- Report the exact checks run. Do not claim client or runtime validation from
  the static corpus gate.
- Do not push unless the owner explicitly asks.

## Documentation policy

Tracked prose describes the current corpus contract, tool interfaces, evidence
classes, and verification boundary. Follow [comments and
prose](comments-and-prose.md) for current-state prose and comment rules.

Use ASCII punctuation and repo-relative links. Keep paragraphs short. Use a
list for a real sequence and a table for repeated mappings. Link the canonical
page instead of repeating a changing fact.

`docs/README.md` indexes the tracked Markdown tree in both directions. The
ignored `docs/ai_agents/local/` island is excluded from that index.

## Tracked and local boundaries

`docs/ai_agents/` is the tracked policy tier. Its pages define contribution,
comment, evidence, and verification rules for this repository.

`docs/ai_agents/local/` is an ignored maintainer working area. It may contain
re-entry notes and review audits, but it is not public policy or evidence. It
is excluded from the docs index and must not be linked as a current contract.

## Reading order

1. [Evidence and claims](evidence-and-claims.md)
2. [Comments and prose](comments-and-prose.md)
3. [Verification](verification.md)

The repository surfaces remain canonical for their subjects:
[the repo charter](../../README.md), [the Lua corpus contract](../../lua/README.md),
[the tool reference](../../tools/README.md), and [the docs index](../README.md).
