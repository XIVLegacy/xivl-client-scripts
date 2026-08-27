# Docs index

Use this index to find the corpus contract, tooling reference, repository
charter, and contribution policy.

| Need | File |
|---|---|
| Lua Script Corpus | [../lua/README.md](../lua/README.md) |
| Tooling | [../tools/README.md](../tools/README.md) |
| XIVLegacy Client Scripts | [../README.md](../README.md) |
| AI-assisted contributions | [ai_agents/README.md](ai_agents/README.md) |
| Comments and prose | [ai_agents/comments-and-prose.md](ai_agents/comments-and-prose.md) |
| Evidence and claims | [ai_agents/evidence-and-claims.md](ai_agents/evidence-and-claims.md) |
| Retail-input validation | [ai_agents/retail-input-validation.md](ai_agents/retail-input-validation.md) |
| Guildleve journal lifecycle | [guildleve-journal-lifecycle.md](guildleve-journal-lifecycle.md) |
| MyPlayer timer consumers | [myplayer-timer-consumers.md](myplayer-timer-consumers.md) |
| Retail Lua resource coverage | [retail-lua-coverage.md](retail-lua-coverage.md) |
| Vendored client-structs input | [../data/vendor/client-structs/README.md](../data/vendor/client-structs/README.md) |

`tools/validate_corpus.py` checks this index against the Markdown tree under
`docs/` in both directions, excluding the ignored `docs/ai_agents/local/`
island. Add a row for each tracked page and remove its row when the page is
removed.
