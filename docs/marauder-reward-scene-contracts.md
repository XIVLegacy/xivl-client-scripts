# Marauder reward and barrel scene contracts

Quest `110101` / `Exc300` is **Two-man Crew**. Quest `110102` / `Exc306` is
**Captain's Orders**. The decoded client evidence does not establish Two-man
Crew's gil-selection rule or the barrel scene's exact interaction placement.

## Two-man Crew reward branches

The condition selecting gil and the exact amount per branch are
**UNESTABLISHED**. The retained eLeMeN study reports `24000-30000` gil and
leaves the competing reduction conditions uncertain. It does not establish
that there are exactly two branches or assign either endpoint to a condition.

| Condition | Amount | Source | Status | Gap |
| --- | --- | --- | --- | --- |
| Four-noise failure | Unknown | `xivl-captures:studies/elemen-quest-rewards-walkthroughs/derived/quest-walkthroughs.csv:60`, quest `110101`; decoded `Exc300` member | UNESTABLISHED reward rule; wiki lead only | No terminal failure/noise-state observation is joined to awarded gil |
| Missing eastern herbs | Unknown | Same retained walkthrough row and its uncertain reduction statement; `xivl-client-data:csv/exc300.csv` | UNESTABLISHED reward rule; wiki lead only | No herb-state predicate or reward observation maps the condition to an amount |
| Four-of-five loot completion | Unknown; `30000` is only the wiki upper endpoint | Same walkthrough row; `xivl-client-data:csv/quest_new_reward.csv:110101` | UNESTABLISHED reward rule; completion route is a wiki report | No success/result-to-award join establishes `30000` |
| Failure or missing-herbs completion | Unknown; `24000` is only the wiki lower endpoint | Same sources | UNESTABLISHED reward rule | No endpoint attribution, exclusivity or branch count is proved |
| Unattributed reward range | `24000-30000` gil | Retained walkthrough row `60` | Established as a wiki-tier report, not a retail payout | No attributable retail reward event corroborates the range |
| Quest EXP | Up to / level-scaled `3420` | Retained walkthrough row `60`; `quest-exp-rewards.csv:197`; study README/glossary | Established wiki-tier report, not fixed retail EXP | No quest reward event at an identified player level |

Confidence is high for the literal decoded observations below. No retail
mechanics confidence is assigned to the wiki branch hypotheses.

`Exc300` loads text resource `117` / `exc300` at line 17. Its only recovered
conditional controls compare cutscene results at lines 34 and 62, and test
`trialObject` argument 3 at lines 1090, 1103 and 1116. The cutscene comparisons
select fade paths. The document selector preserves three variants:

| `trialObject` argument 3 | Selected `exc300` text rows | Meaning supported by the text |
| ---: | --- | --- |
| `1` | `147`, `148` | Watchman's log |
| `2` | `149`, `150` | Repair-services bill |
| `3` | `151`, `152` | Tattered parchment |

The bill's `3000` and `1500` gil amounts concern repair services, not the
quest's reward (`exc300.csv:150`, English column 1). Row `125`'s noise/gil
wording is moneylender/debt dialogue. Neither text supplies a reward selector.
The document argument's producer is not identified by this method.

`processEvent025`, lines 130-158, presents text `40/41` and a character
scheduler call. `processEvent030`, lines 161-178, calls `startNQCutScene`
with `exc30030`, `1`, then a fade helper. Neither method calculates gil.
The complete decoded member has no `gil`, `reward` or `Notice` identifier,
or numeric literal `24000` or `30000`. Its separate dialogue methods remain
`processEvent010_2`-`010_14`, `020_2`-`020_7`, `022_2`-`022_3`,
`023_2`-`023_7` and `025_2`-`025_9`; none adds a conditional reward call.
These are observations about the decoded member, not an original-bytecode or
server-implementation absence proof.

Reward row `110101` contains 16 equal groups of 13 numeric fields:
`301,-2,0,8090201,0,-1,-1,-1,-1,0,-5,2,2`. This is a structural observation.
No field meaning, gil formula or branch selector follows from these values.
The exact `QuestDirectorExc30001` companion is a class wrapper, while
`QuestObjectExc300` owns marker visibility. Neither supplies the missing
reward join.

The payment-contact identity is independently supported by marker `11010105`,
column 4 = display key `1400067`; `actorclass.csv:1000374`, column 5 =
`1400067`; and `xtx_displayName.csv:1400067`, English column 1 = `Rorojaru`.
The marker's float pair is `28.93/109.69` and its map pair is `104/421`.
These static joins identify a contact, not an award event.

The finite source set is the complete decoded Exc300 member and its two
named companions, selected Exc300 text, quest/title row `110101`, reward row
`110101`, marker rows `11010101`-`11010120`, the payment name/class rows,
and the retained eLeMeN study rows above. The missing evidence is a
quest-specific producer or attributable preserved retail observation joining
terminal outcome, herb or noise state to awarded gil. The selected original
LPB was unavailable, so no new bytecode control-flow claim is made. Missing
proof does not establish that either proposed condition is irrelevant.

## Captain's Orders barrel scene

The exact zone, private area, interaction actor and world position for
`Exc306.processEvent030` are **UNESTABLISHED**. The authenticated method
selects scene key `exc30630`. The marker and map rows establish Limsa context,
but do not select a unique numeric zone or a coordinate transform.

| Method | Zone/private area | Actor/position or map join | Source | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| `Exc306.processEvent030` | No literal zone or area argument | Calls `startNQCutScene` with `exc30630`, `1`; invokes fade helpers before and after it | `lua/scripts/quest/scenario/exc/exc306.lua:127-144`, especially 132, 137, 141 | Established direct client calls, high confidence | Invocation context and helper names do not supply a zone, actor spawn or position |
| Marker `11010202` | Pair `101/121`, shared by markers `11010201`-`11010220` | Sheet columns 2/3 = `603.58`, `627.71`; column 4 = `4000257`; columns 8/9 = `101`, `121`; column 10 = `0`; class `MapMarkerQuest` | `xivl-client-data:csv/quest_marker.csv`, row `11010202` | Established static values, high confidence | Marker coordinates have no proved actor/world-coordinate binding |
| Exact map-pair equality | Limsa map context | `2Dmap_data` rows `50,60,73,75,76,77` and `mapNavi_data` rows `800,820,827,829,830,850` all have columns 0/1 = `101/121` | `xivl-client-data:csv/2Dmap_data.csv`; `csv/mapNavi_data.csv`, named rows | Established equality, high confidence | Multiple rows preserve different column-2 values; no unique row or zone follows |
| Zone-group/place equality | Limsa Lominsa | Group `101` lists zones `133,230,134,232,140`; both `_zoneParam` rows `133/230` carry place key `1051`. Layouts `121/131/171` share that key | `xivl-client-data:csv/zoneGroupParam.csv:101`, `_zoneParam.csv:133,230`, `_layout.csv:121,131,171`, `xtx_placeName.csv:1051` | Established key joins, high confidence | Shared place keys do not choose zone `133` versus `230`, a private-area level or a transform |
| Narrative barrel context | Maelstrom Consortium aleholds | English text describes disposal in the aleholds and a return to a barrel | `xivl-client-data:csv/exc306.csv`, rows `18` and `25`, column `1` | Established text, high confidence | Text is not an actor initialization or placement record |

Column numbers in this section are zero-based sheet columns after the row
ID. Thus the marker's columns 2/3 are CSV fields 3/4. They are a float pair,
not a complete world position. No height or actor class is supplied by that
pair. The reported range of other zone-230 spawns does not establish a
conversion or justify moving this marker.

`processEvent030_2` through `processEvent030_12` preserve distinct dialogue
variants at lines 838-1120. Their selected text rows are respectively
`27/28`, `29/30`, `121/122/123`, `124`, `125`, `126/127`, `128/129`,
`130/131`, `132/133`, `134/135`, and `31`. Their direct calls have no literal
area or position argument. This does not establish the effects of their
callers or native helpers.

The [scene-key crosswalk](quest-scene-replay-joins.md#module-prefixed-scene-keys)
joins `exc30630` to `cutReplay` row `11010203`. That replay row is a separate
identity from quest marker `11010202`. Neither equality binds the method to
that marker or to an interaction actor.

The bounded source set comprises the named Exc306 methods and dialogue
variants, the quest/title binding, marker rows, exact map-pair matches,
Limsa group/place/layout rows and dialogue rows above. The
`xivl-client-data:docs/autotranslate-name-crosswalk.md#records-and-source-fields`
and `docs/zone-group-place-rows.md` preserve the shared-zone limitation.
An authenticated actor/private-area initialization or attributable preserved
retail observation must connect this method's receiver to an area and
position, or an exact marker consumer must map `101/121` to one zone and its
coordinate space. That join is missing.


## Source identity and reproduction

These findings use extraction `2012.09.19.0001`. Verify the decoded Lua
archive against [the fixed archive grant](../manifests/private_lua_corpus.json)
and each selected member against [scripts.json](../manifests/scripts.json).
The selected Lua identities are:

| Member below `lua/scripts/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `quest/scenario/exc/exc300.lua` | 20374 | `5f0cddd8ddbc1ac27e57c32749fe1db99c6dd5bc3d82098fef2cb7c7e84d2d8d` |
| `quest/scenario/exc/exc306.lua` | 25350 | `9ca53959191cf4c409c54dba100dba960043dd3f720b308c4a58b2842afc5632` |
| `director/quest/questdirectorexc30001.lua` | 197 | `daaafb2f72307af9282796c1a0d564d7310accc31e280d732a112aa6395021f5` |
| `chara/npc/object/questobjectexc300.lua` | 303 | `394c85d5bba915fbfa4016341e4e137b416f50af01769d23d25d1bde388f789e` |

CSV member sizes and SHA-256 pins belong to
`xivl-client-data:manifests/tables.json`; the archive is declared by
`manifests/private_csv_corpus.json`. Quest IDs map to the named scenario
paths in `xivl-client-data:manifests/staticactor_class_paths.json`, and English
titles come from `csv/xtx_quest.csv`, column 2. The eLeMeN study owns its
wiki-tier provenance and EXP notation. Its derived row is a report, not an
independently revalidated original transcript here.

The producing inspection uses Python 3.12 `hashlib` and `zipfile` for exact
archive/member authentication, `csv.reader` for row/column equality, and
local register-alias tracing of the named decoded Lua methods. No client
runtime or server award is reproduced. Column numbers are zero-based after
the row ID unless explicitly labeled as CSV fields.
