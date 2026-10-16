# Class, job, and Grand Company quest scripts

[`data/quest_contracts.json`](../data/quest_contracts.json) inventories 274
retained scenario scripts: 102 class-family candidates, 70 job-family members,
and 102 Grand Company-family members. Every selected member has a matching
canonical decoded source and retail LPB identity. No selected member has an
unresolved decode. The census also classifies the other 346 members of the
620-member scenario tree as outside these families.

The family labels select decoded resource paths. They do not establish that a
class was playable, a quest was active, or a placeholder was used. In particular,
`acn` and `exc` remain in the inventory as retained class-family candidates.
There are no separate `cls` or `job` directories in this census.

## Family census

All members in this table are decoded and matched. The handler column counts
scripts declaring a method besides `initText`, including empty method bodies.
The remaining 118 selected scripts declare only initialization. These counts
describe the retained chunks, not complete quest implementations.

| Group | Family | Scripts | With handler declarations |
|---|---|---:|---:|
| Class | `acn` | 6 | 0 |
| Class | `alc` | 6 | 3 |
| Class | `arc` | 6 | 3 |
| Class | `bsm` | 6 | 4 |
| Class | `cnj` | 6 | 3 |
| Class | `cul` | 6 | 4 |
| Class | `exc` | 6 | 4 |
| Class | `fsh` | 6 | 4 |
| Class | `gla` | 4 | 3 |
| Class | `gld` | 6 | 3 |
| Class | `hrv` | 6 | 3 |
| Class | `lnc` | 6 | 3 |
| Class | `min` | 6 | 3 |
| Class | `pgl` | 4 | 3 |
| Class | `tan` | 6 | 3 |
| Class | `thm` | 4 | 3 |
| Class | `wdk` | 6 | 3 |
| Class | `wvr` | 6 | 3 |
| Job | `blm` | 10 | 6 |
| Job | `brd` | 10 | 6 |
| Job | `drg` | 10 | 6 |
| Job | `mnk` | 10 | 6 |
| Job | `pld` | 10 | 6 |
| Job | `war` | 10 | 6 |
| Job | `whm` | 10 | 6 |
| Grand Company | `com` | 45 | 27 |
| Grand Company | `gcg` | 19 | 9 |
| Grand Company | `gcl` | 19 | 14 |
| Grand Company | `gcu` | 19 | 9 |

## Contract contents and evidence

Each script record copies its exact decoded-source pin from
[`manifests/scripts.json`](../manifests/scripts.json) and its original resource,
LPB hash, and decoded-payload hash from
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
The archive identity remains in
[`manifests/private_lua_corpus.json`](../manifests/private_lua_corpus.json).
These are the canonical source identities, independent of whether the decoded
Lua files are locally available.

The builder authenticates each selected original LPB, decodes its wrapper with
[`retail_script.py`](../tools/retail_script.py), and reads its Lua 5.1 bytecode.
A conservative control-flow analysis retains a value only when all incoming
paths agree. Supplied parameters, globals, member values, and call results
remain typed unknowns. The output retains no bytecode words or decompiled
function bodies.

The machine artifact contains:

- Class definitions and method declarations, including parameter counts,
  variadic flags, and declaration locations. Declaration parameters are not
  evidence of caller-supplied literals.
- Scene and presentation calls with their positional arguments, including
  widget calls, `showQuestInfomation`, and text initialization.
- Text calls and their arguments. For `say` and `ask`, the arguments include
  the receiver, text owner, and text row. The owner stays explicit, so a quest
  text row is not conflated with a `worldMaster` text row.
- Selector-result comparisons and return sites. A compared literal is an
  observed client branch, not a complete set of values the selector can return.
- Per-prototype instruction and call coverage, named call counts, direct
  actor-class calls, and explicit `work` member reads or writes.

Prototype paths use `root/proto0` for the first child, then repeat `/protoN`
for nested children. PCs are zero-based within the prototype. Offsets are byte
offsets in the decoded Lua chunk, not offsets in the LPB wrapper or executable.
Call argument arrays include the explicit receiver passed by Lua's method
calling convention. Null arities mark open argument or result lists.

All 18,407 reachable callsites have a recovered global or member name, and no
callsite is unreachable under this conservative analysis. A recovered member
name does not resolve the runtime implementation of an inherited method.
The selected chunks contain no direct `callClientFunction` call, actor-class
lookup call, or explicit `work` member access. Actor receivers are supplied
values, so the contracts establish no literal NPC or object actor-class IDs.
Inherited helpers and external callers remain outside this chunk-local result.

## Scene joins and quest identities

The inventory records 346 direct `startNQCutScene` calls using 328 distinct
literal scene keys. Exact case-sensitive matching against sheet column 0 of
`xivl-client-data:csv/cutReplay.csv` joins 308 calls. The other 38 calls retain
their unmatched literal keys. The report pins that CSV's SHA-256 and retains
its row IDs, keys, and physical line locators. A replay match establishes a
table relationship, not playback or quest ownership. The existing
[scene-join findings](quest-scene-replay-joins.md) describe the same join rule.

Every `questId` remains null because this analysis does not authenticate the
script's owning static actor ID. It does not derive IDs from filenames, scene
keys, or replay row arithmetic. The 91 existing job-selector message references
are copied from the pinned
[`quest_selector_consumers.json`](../manifests/quest_selector_consumers.json)
and checked against bytecode arguments. They remain presentation references,
not owner-ID joins. This preserves the `Drg0j4` 51132 reference to 111304 without
silently replacing it with a filename-derived value.

The [quest event contracts](quest-event-client-contracts.md),
[selector consumers](quest-selector-consumers.md), and
[reward widget contracts](reward-widget-result-contracts.md) own the focused
helper and widget findings. This inventory establishes client scene and UI
flow only. It establishes no server dispatch, eligibility, objectives, reward
grant, or historical invocation.

## Reproduction and validation

The portable check requires only this repository and its normal Python
dependency, `jsonschema`:

```text
python tools/build_quest_contracts.py --check
```

It validates the schema, source pins, complete family census, bytecode locator
relationships, argument arities, replay joins, presentation references, summary,
and content digest. The normal `tools/validate_corpus.py` gate includes these
checks and the focused tests. Portable validation does not reread retail bytes.

To reproduce the contract from authenticated retail inputs:

```text
python tools/build_quest_contracts.py --retail-root <client/script> --csv-root <csv-directory>
python tools/build_quest_contracts.py --check --retail-root <client/script> --csv-root <csv-directory>
```

Generation reads only the selected paths from the retained resource census.
`--csv-root` must contain the exact pinned `cutReplay.csv`. On a check, either
input can be supplied independently: the retail root re-derives bytecode
contracts against retained replay rows, while the CSV root re-derives those
rows. Optional `--lua-archive <archive.zip>` additionally authenticates the full
retained archive and all 620 canonical scenario-source members. No default
sibling checkout or installed client path is used.

The schema is
[`quest_contracts.schema.json`](../schemas/quest_contracts.schema.json).
Focused tests in
[`test_quest_contracts.py`](../tools/tests/test_quest_contracts.py) guard against
branch-dependent literals, case-insensitive scene joins, inferred caller
arguments, invented quest owners, omitted members, and altered locators.
