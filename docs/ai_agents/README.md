# AI-assisted contributions

AI-assisted changes follow this repository's contribution policy. The
contributor owns the change and must be able to explain its scope and evidence.

Use [evidence and claims](evidence-and-claims.md) before promoting a fact into
tracked documentation or a generated product.

## Contribution policy

- Keep changes inside this repository's owned surfaces: corpus, tools, schemas,
  documentation. A task may explicitly name another surface.
- Treat `lua/` as published client evidence. Do not hand-edit scripts,
  sidecars, or generated indexes. Use the documented builders and run all
  repository checks.
- Keep explicit external `--scripts-root` inputs (or the
  `XIVL_LUA_SCRIPTS_DIR` setting) as research inputs. They are read-only Lua
  sources; annotation writes generated `.calls.json` sidecars under the
  repository's `lua/scripts/` tree and keeps the N-API index repository-owned.
  Repository-local `lua/scripts` remains the default for compatibility.
- Preserve source and evidence citations verbatim, including dates. Cite a
  promoted artifact by its own name and a sha256 of the promoted content.
- Do not push unless the owner explicitly asks.

## Documentation policy

Tracked prose describes the current corpus contract, tool interfaces, and
evidence classes. Follow [comments and prose](comments-and-prose.md) for
current-state prose and comment rules.

Use ASCII punctuation and repo-relative links. Keep paragraphs short. Use a
list for a real sequence and a table for repeated mappings. Link the canonical
page instead of repeating a changing fact.

`docs/README.md` provides entry points into the public documentation. The
ignored `docs/ai_agents/local/` island is outside the public tree.

## Tracked and local boundaries

`docs/ai_agents/` is the tracked policy tier. Its pages define contribution,
comment, and evidence rules for this repository.

`docs/ai_agents/local/` is an ignored maintainer working area. It may contain
working notes and review audits, but it is not public policy or evidence and
must not be linked as a current contract.

## Reading order

1. [Evidence and claims](evidence-and-claims.md)
2. [Comments and prose](comments-and-prose.md)

The repository surfaces remain canonical for their subjects: [the repo
charter](../../README.md), [the Lua corpus contract](../../lua/README.md), [the
tool reference](../../tools/README.md), and [the docs index](../README.md).
