# GC quest recoverability

The retail 1.23b extraction preserves 102 Grand Company-family resources. The
canonical [family census](quest-script-inventory.md#family-census) owns the
resource selection and handler counts:

| Family | Resources | With handler declarations |
| --- | ---: | ---: |
| `com` | 45 | 27 |
| `gcg` | 19 | 9 |
| `gcl` | 19 | 14 |
| `gcu` | 19 | 9 |
| **Total** | **102** | **59** |

All 102 `questId` values remain `null`. Family labels and decoded paths identify
retained client resources; they do not establish quest ownership, quest state,
or a complete server quest. The 43 resources without handler declarations
contribute initialization only.

The separate SAN/title join in
`xivl-client-data:docs/grand-company-quest-identities.md` maps 102 static
actor IDs to 92 of these resources, including five shared Gcl classes.
It does not change the generated contract's singular `questId` field.
The [United We Stand](united-we-stand-client-contract.md) and
[To Kill a Raven](to-kill-a-raven-client-contract.md) findings apply those
identities to the authenticated client methods and preserve their server
dispatch limits.

## Evidence boundary

The canonical [`data/quest_contracts.json`](../data/quest_contracts.json) is a
static analysis of the retail 1.23b extraction `2012.09.19.0001`. Its four
input pins are recorded in these manifests:

- [`manifests/scripts.json`](../manifests/scripts.json)
- [`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json)
- [`manifests/private_lua_corpus.json`](../manifests/private_lua_corpus.json)
- [`manifests/quest_selector_consumers.json`](../manifests/quest_selector_consumers.json)

For each retained resource, the contract records the decoded source path,
original resource path, LPB and decoded-payload hashes, declarations, callsites,
text calls, result comparisons, selector metadata, and per-prototype coverage.
Where a literal scene key is present, the contract records its case-sensitive
join to `xivl-client-data:csv/cutReplay.csv` and any matching row IDs.

A recovered method or presentation call establishes client-side presentation
metadata only. A scene join is a table relationship, not proof of playback or
quest ownership. The contract does not establish server dispatch, eligibility,
objective state, battle or spawn ownership, reward settlement, completion
mutation, or historical invocation. Inherited helpers and external callers
remain outside this chunk-local result.

## Focused client contracts

The focused pages provide detail without repeating the full inventory:

- [Quest event client contracts](quest-event-client-contracts.md)
- [Quest selector consumers](quest-selector-consumers.md)
- [Quest scene literal and replay-row joins](quest-scene-replay-joins.md)
- [Reward widget contracts](reward-widget-result-contracts.md)
- [Grand Company event contracts](job-grand-company-event-contracts.md#grand-company-distinctions), including Gcl105 selector paths

The [quest script inventory](quest-script-inventory.md) owns the complete family
census, null `questId` rule, source identities, field limits, and reproduction
checks. Its client-only result remains bounded by the metadata retained in the
canonical contract.
