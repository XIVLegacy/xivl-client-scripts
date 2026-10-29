# Ingram and Morys private-scene contracts

The private-area **NAME** and **LEVEL** required by the reported methods are
**UNESTABLISHED**. `Cnj306` matches the combined Ingram/Morys and
`processEvent010/045/050` signature. `processEvent010` alone does not uniquely
identify the requested quest: both `Cnj300` and `Cnj306` mention Ingram and
contain that method. No private area is assigned to an unidentified variant.

## Quest and resource identity

The authenticated static-actor table directly binds these numeric quest IDs
to scenario class paths. The title join is separate.

| Quest ID | Scenario class path | English title |
| ---: | --- | --- |
| `110261` | `/Quest/Scenario/Cnj/Cnj300` | Good Knight, Sweet Dreams |
| `110262` | `/Quest/Scenario/Cnj/Cnj306` | The Call of Nature |

Sources: `xivl-client-data:manifests/staticactor_class_paths.json`, records
`110261/110262`; `csv/xtx_quest.csv`, rows `110261/110262`, column 2. The
static-actor records reproduce from `client/script/rq9q1797qvs.san` using
`tools/extract_staticactor_san.py:parse_san`. The selected original spans are
`[73304,73335)` and `[73335,73366)` in that file. This is a quest-to-class-path
binding, not an actor-to-method dispatch or private-area allocation.

`Cnj306.initText` loads resource `487` / `cnj306` at line 17. Its English text
column 1 names Stillglade Fane in row `1`, Ingram in rows `6/8`, and Morys in
rows `34/35`; row `91` mentions both people. Fane is a place in this evidence.
`Cnj300` also mentions Ingram and Morys, and has `processEvent010/050`.
There is no recovered `processEvent045` binding in that authenticated member.

The Morys text-name query also retains `Arc200` as a `processEvent050`
metadata candidate. `Cnj200` and the Ingram text candidate `Tan500` have none
of these three recovered method bindings. Thus `010` or `050` plus one actor
name is insufficient. The combined three-method signature selects `Cnj306`
within this finite source set; an independently supplied quest ID or actor
dispatch record is still needed to attribute the isolated Ingram `010`.

## Area name and level

Column numbers are zero-based sheet columns after the row ID. Confidence is
high for the direct decoded calls and exact static joins. No required area
name or level follows from them.

| Quest/method | Area name | Level | Source | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| Requested Fane/Ingram `processEvent010`, without quest ID | UNESTABLISHED | UNESTABLISHED | `Cnj300` and `Cnj306` text and method bindings above | Quest identity UNESTABLISHED for this label alone | Exact quest ID or actor-to-method dispatch selecting the variant |
| `110261 / Cnj300.processEvent010`, candidate | UNESTABLISHED | UNESTABLISHED | `lua/scripts/quest/scenario/cnj/cnj300.lua:382-398`, call at 392 | Established call to `startNQCutScene` with `cnj30010`, `1` | Scene-to-private-area construction/initialization join |
| `110262 / Cnj306.processEvent010`, candidate | UNESTABLISHED | UNESTABLISHED | `lua/scripts/quest/scenario/cnj/cnj306.lua:385-402`, call at 395 | Established call to `startNQCutScene` with `cnj30610`, `1` | Same join, plus attribution of the requested isolated method |
| `110262 / Cnj306.processEvent045` | UNESTABLISHED | UNESTABLISHED | Same member, lines 649-671; ask 658, comparison 659, scheduler 663 | Established ask/result branch and scheduler call; matches the combined signature | Accepted transition to a named private-area instance and its level |
| `110262 / Cnj306.processEvent050` | UNESTABLISHED | UNESTABLISHED | Same member, lines 674-691; scene call 684, helper 688 | Established call with `cnj30650`, `1`, then `startFadeInCutSceneAfterWarp` | Scene-to-private-area initialization and actor dispatch |
| `110261 / Cnj300.processEvent050`, alternative | UNESTABLISHED | UNESTABLISHED | `cnj300.lua:958-1015`; ask 978, scheduler 983, scene 992 | Established accepted-result path with `cnj30050`, `2`; separate from Cnj306 | No unique attribution from the isolated Morys `050` label, and no area initialization join |
| `Arc200.processEvent050`, text-name candidate | UNESTABLISHED | UNESTABLISHED | [Registry](../lua/registry.json), `quest/scenario/arc/arc200`; `xivl-client-data:csv/arc200.csv:44`, Morys text-name match | Metadata candidate only; no scene attributed | Actor dispatch and exact quest selection before scene interpretation |

`Cnj306.processEvent045` asks `worldMaster` with message `51030`, mode `2`.
Result `1` invokes `runCharaSchedulerPastAreaIn` and returns that result; the
other path returns `0`. The direct helper in
`lua/scripts/quest/questbaseclass_common.lua:551-559` invokes the supplied
actor's `_runCharaScheduler` with `67111866`. It supplies no area name, level,
zone ID or class name. This call is not proof of a completed area transition.

`QuestBaseClass.startNQCutScene`, lines 21-47 of the same common member,
forwards its scene key to `worldMaster.createCutScene` at line 28. Neither
that bounded wrapper nor the named Cnj306 calls supplies an area name or
level literal. The following scene-call arguments `1` and `2` are not proved
private-area levels.

`cnj30610` and `cnj30650` exactly match `cutReplay.csv` rows `11026201` and
`11026205`. The [scene-key crosswalk](quest-scene-replay-joins.md) owns the
replay joins. A replay ID or scene key is not a private-area name or level.
Likewise `quest.csv:110262`, column 51 = `36`, is a
`xivl-client-data:docs/quest-gating-findings.md` quest-gating value. It is not
an area level.

`PrivateAreaMasterPast` declares `PrivateAreaBaseClass` as its base and has
an empty `init` at lines 11-14. The base `_onInit` forwards initialization,
prepares work storage and calls `init(_getZoneName())`; its own `init` is
empty. The [area initialization contract](area-base-client-initialization.md)
owns those base facts. A class identifier does not establish a private-area
instance NAME, and these bodies do not select a Cnj306 area LEVEL. Zone
`206` separately shares Gridania's place key with `155`, as recorded by
`xivl-client-data:docs/zone-group-place-rows.md`; it does not supply either
missing value.

## Source identity and finite scope

The sources use extraction `2012.09.19.0001`. Archive identities are declared
by [private_lua_corpus.json](../manifests/private_lua_corpus.json) and
`xivl-client-data:manifests/private_csv_corpus.json`. Each selected member is
size/hash authenticated before parsing, against [scripts.json](../manifests/scripts.json)
or `xivl-client-data:manifests/tables.json`.

| Member below `lua/scripts/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `quest/scenario/cnj/cnj306.lua` | 18628 | `dbf1b35b62117fdbfc90a082dc71472c5acddf5347603a8ddb06751a4adb811a` |
| `quest/scenario/cnj/cnj300.lua` | 21814 | `a44c38d7da66fe8b50241ae04da58c002527354b63bede04c7ba545ed7a8050a` |
| `quest/questbaseclass_common.lua` | 35511 | `cf61a5687dbc7b6accd26c8cd3a138decc0372fb72518ac6f2054f125bc1465e` |
| `area/privatearea/privateareamasterpast.lua` | 279 | `0cf88fb0e965f9b157a40afc58913c8dd792a396dac199d3aa6d1e319e0818f7` |
| `area/privatearea/privateareabaseclass.lua` | 756 | `3261a08d2c5fabfd300d75b5427047038549971e80ecf4b605026af7c56346c2` |

The SAN is 108911 bytes with SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`,
pinned by `xivl-client-data:manifests/retail_inputs.json`. Its parser output
matches the complete tracked class-path catalog. The selected identity joins
above do not depend on inferring quest ownership from a replay-row prefix.

The finite identity query authenticates 558 manifest-listed CSV members
whose stems match scenario resources, plus `_quest/quest/quest_new` families.
Whole-word, case-insensitive `Ingram`, `Morys` and `Fane` matches preserve
all 87 matching rows across 22 members and all localized variants. Follow-up
interpretation is limited to the two named Cnj resources, their selected
identity/title/replay rows, the direct common helpers and private-area base
initialization. The five name-hit candidate method inventories preserve
alternatives; no actor dispatch or source body is inferred from the registry.

The producing inspection uses Python 3.12 `zipfile`, `hashlib`, `csv`, `json`
and `re`, with local alias tracing of decoded methods. It is not runtime Lua
execution. The exact missing evidence is an authenticated construction or
initialization record joining the selected transition or scene to its
private-area instance NAME and LEVEL. The isolated actor/method labels also
need an exact quest ID or dispatch record where the variants above remain.
