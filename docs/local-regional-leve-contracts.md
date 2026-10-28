# Guildleve 12468 reveal and 12487 objective contracts

12468, "Leaders of the Pack", is a regional battlecraft guildleve in the
selected client rows. Calling it a local leve would conflate two distinct
publisher contracts. 12487, "Necrologos: Celeritous Impetus", has a retained
retail activation bound to `PrivateGLBattleOrbNormal`. Its objective methods
describe UI data, without establishing enemy placement or kill/spawn policy.

## Static identities

All field positions exclude row_ID and are zero-based. Sources are extraction
`2012.09.19.0001`, class `client_extraction`.

| Row | Exact selected fields in guildleve.csv | Interpretation boundary |
| --- | --- | --- |
| 12468 | 1=1, 2=2, 5=20, 6=1280066, 7=20028, 8=20004, 17=10041, 21=30, 39-42=`4,0,0,0`, 55-58=`0,0,0,12000101`, 59-62=`3202603,3200105,0,3205803` | Mapping labels classType/location/level/aetheryte/plate/border/objective/timeLimit/aimNum/item/mob do not establish runtime predicates. |
| 12487 | 1=1, 2=2, 5=30, 6=1280067, 7=20023, 8=20005, 17=10051, 21=30, 39-42=`3,3,0,0`, 55-58=`12000003,12000001,0,12000004`, 59-62=`0,0,0,0` | The aim tuple is not independently an enemy, page, kill or spawn count. |

The English titles are `xtx_guildleve.csv` field 10 at the same IDs.
`guildleve_UI.csv` row 12487 fields 75-78 are
`20012,20023,20005,1280067`. Objective text row 10041 says to uncover and
eliminate target enemies. Row 10051 says to locate missing Necrologos pages,
release their creatures and eliminate them. Source:
`xivl-client-data:docs/guildleve-12468-client-rows.md`;
`xivl-client-data:docs/guildleve-selected-row-values.md`;
`xivl-client-data:tools/mappings/guildleve.py`;
and the authenticated named CSV rows.

## 12468 reveal boundary

`guildleve.58 = 12000101` joins by row ID to `xtx_itemName`, `_item`, and
`itemData`: Evenfall Firefly. `_item` fields 0-3 are
`Normal/DummyItem,1,false,true`; mapped itemData isUseable field 43 is 0.
This does not rule out a separate content command presenting the item.
The English journal narrative, `xtx_guildleve` 12468 field 14, describes
collecting fireflies and dissolving an imp's glamour. It establishes intended
presentation, not an executed item transaction.

`xtx_command_content` rows 10002 and 40002 both label Detect.
`xivl-client-scripts:docs/content-command-client-route.md` establishes the
director `contentCommand`/`contentCommandSub` mirror and menu route for
static command 24302, `/Command/System/ContentCommand`. A 10000-19999 variation
requires no supplied target; 40000-49999 requires a non-null non-player target.
The recovered `fire` returns false. No selected producer picks 10002 or 40002
for 12468, and text equality does not pick one. No exact reveal request packet,
typed arguments, returned answer or server reply is established here.

The static mob-name joins are 3202603 -> firestarter imp -> actorclass 2202603,
3200105 -> ringtail pteroc -> 2200105, and
3205803 -> evenfall firefly -> 2205803. Same-ID graphic fields 6/7/32/33 are
`10038,3,0,1024`, `10002,2,0,1056`, and `10515,3,0,1024` respectively.
These are static correlations, not a historical roster or transformation.
Source and exact field locators:
`xivl-client-data:docs/guildleve-12468-client-rows.md#target-name-and-actor-row-correlations`.

The first missing edge is the producer selecting 12468's content variation.
Discriminating evidence must identify the active Director/command work,
variation and target context. Separate joins are required for invocation,
item supply/consumption, the reply and visible actor transition. No exact
Director class, disguise resource producer, spawn coordinates or completion
predicate is established for 12468 by this selection.

## 12487 retained activation

The packet source is `party_battle_leve.pcapng`, source `pcap-1.23b`,
evidence class `packet-capture`, SHA-256
`6327e5e1f5cbd51a9baaa9bcbacf53ca51c50a98fe4b66ae3e6bdecd9198089f`.
All locators here are main connection 0. Frames/subevents are zero-based,
completing capture packets one-based. Source:
`xivl-captures:studies/regional-guildleve-publisher-contract/README.md#retail-client-director-binding-for-12487`
and `xivl-captures:studies/regional-guildleve-publisher-contract/derived/timeline.csv`.

| Observation | Exact supported carrier and values |
| --- | --- |
| Activation prompt | s2c `0x0130`, frame 40/subevent 2, packet 94, eventGLStart owner `0x4510000C`. Nine typed integers: `(12487,1,3,3,12,0,0,0,0)`, END. |
| Client answer | c2s `0x012E`, frame 42/subevent 2, packet 110. One result: integer 1, END. |
| Class binding | s2c `0x00CC`, frame 50/subevent 17, packet 118. Transport source `0x45100D44`, fixed class text `PrivateGLBattleOrbNormal`. Typed stream: string `/Director/Guildleve/PrivateGLBattleOrbNormal`, five false Booleans, integers `(20005,12487,6,0,0,0)`, END. No nil/reference token. |

The eventGLStart slots mean Guildleve ID, difficulty, faction ID, displayed
area faction standing, faction-credit reward estimate, then four warning
inputs. The widget receives slots 1-8, inserted zero, then slot 9. It returns
the supplied difficulty only when its confirmation result is 1, otherwise nil.
These are presentation meanings, not deductions of Favor or eligibility.
Source: `xivl-client-scripts:docs/aetheryte-guildleve-events.md#eventglstart-and-widget-argument-reshuffling`.

Conditional on the separately documented native vector transfer and invocation,
`DirectorBaseClass._onInit` consumes 20005 as directorId and forwards the tail.
`GuildleveBaseClass.init` stores 12487, location 6 and extra-marker XYZ 0/0/0.
OrbNormal's non-vararg `initAsGuildleve(self)` consumes no further values and
returns zero results (root/proto0 PC0, decoded offset `0x152`). Five controls
and the path are not Lua initializer arguments. Historical vector lifetime,
branch/endian state and completed invocation retain their documented boundary.
Source: `xivl-client-scripts:docs/guildleve-initializer-arguments.md`, operand
table and retained 12487 vector.

The class and content-group membership do not prove a separately instanced
world, server implementation class, or a shared binding for other leve IDs.

## Objective consumption and finish

OrbNormal's `getArticleDataOnGuildleveInfo(index)`, root/proto1, returns six
values. Indices 3 and 4 select
`(getArticleTypeForInfo("barFraction"),worldMaster,getTextIdForInfo("item"),getGuildleveId(),index,0)`.
The common return is PC52, offset `0x24E`, `RETURN B=7`.
Other indices retain the initialized tuple `(0,nil,0,0,0,0)`.
`getArticleCondition(index)`, root/proto2, returns `get` for 3 and `smash`
for 4 (calls PC12/20, offsets `0x34C/0x36C`), with a one-value return at
PC24 / `0x37C`. Other indices return 0. The base helpers map item -> text
50002, get -> 2 and smash -> 1.
These are article type/text/condition selectors, not collection or kill code.
Sources: authenticated `director/guildleve/privateglbattleorbnormal.lua:18-113`
and `guildlevebaseclass.lua:1019-1052,1192-1225`, with original LPB operands.

The inherited `guildleveWork` consumer watches `aimNumNow` and `uiState`
for four slots under `infoVariable`, compares temporary copies and sends
`DesktopWidget.processUpdateContentsInformation(self,"update",index)` only
for a changed value. A `signal` update equal to signed -1 emits `"finish"`
and refreshes the marker. Source:
`xivl-client-scripts:docs/content-director-ui-contracts.md#guildleve-and-request-directors`,
bytecode `0x1B01..0x1BAD`, and `guildlevebaseclass.lua:667-740`.
The widget consumes ten results from `getArticleFullDataOnGuildleveInfo` and
routes positions as recorded in
`docs/guildleve-journal-lifecycle.md#objective-article-tuple-routing`.

The retained finish is s2c `0x0137`, frame 3374/subevent 0, packet 5244,
source actor `0x45100D44`: hash `0xAFEDF257` receives `FF`, and
`0xD2C67973` receives `00000000`. The study identifies this as the director
finish update. It does not retain an attributable per-objective increment
tuple here. No exact objective-progress packet field-to-slot join, historical
kill callback, mob identity/roster, spawn rule or page-selection policy follows
from the article methods, the static aim tuple or the finish sample.

Reward presentation follows as `0x0130` eventGuildleveReward at frame
3420/subevent 0, packet 5384. The timeline retains c2s `0x012E` at frame
1769/subevent 1, packet 5397, subsequent warp presentation and retirement.
This does not establish publisher hand-in, payout or journal removal.
`AetheryteBaseClass.eventGLReward`'s 12 supplied presentation slots and two
widget results remain the client contract in
`xivl-client-scripts:docs/guildleve-journal-lifecycle.md#completion-and-hand-in-presentation`.

## Regional and true local comparison

`accept_leve.pcapng` uses owner `0x44D8000A`, `eventTalk*` callbacks,
card indexes 1/4 and Boolean true detail confirmations, followed by s2c
`0x0137` writes of 12483/12482 into `work.guildleveId[3]/[4]`.
This records synchronized client journal insertion for those IDs, without
joining their acceptance to 12487 activation or proving persistence.

The true local publisher comparison, `accept_local_leve.pcapng`, uses owner
`0x44D80009`, `talkOfferWelcome`/`askOffer*`/`talkOfferDecide`, offers
120222/120202 and returns slot 2. It writes `work.guildleveId[8]=202` with a
separate `playerWork.questGuildleve[0]` record. Source:
`xivl-captures:studies/regional-guildleve-publisher-contract/derived/verdicts.md`.
`PopulacePassiveGLPublisher` is the distinct local consumer, documented in
`xivl-client-scripts:docs/local-guildleve-publisher-contract.md`.

`local_leve_complete.pcapng` retains three main s2c `0x0130`
delegateEvent/processPgEvent calls, frames 14/25/497, packets 38/79/1734.
Each has actor values `0x029B2941,0xA0F1D58A`, the method string, integer
365/366/368 respectively, integer `0x151A9000/0x04136000/0x04140000`,
nil, nil, END. Owner `0x44B00005` is separate from those actor values.
Craft calls explicitly name quest 120202; the study does not bind journal
slot 8 to that quest. Source:
`xivl-captures:studies/local-guildleve-dialogue/README.md`, Calls and
Intervening observations. None of this is a 12468 or 12487 objective packet.

The complete retained JournalCommand census found no structurally attributable
24241 request in 54 captures/84 game lanes. The client route and native-derived
candidate carrier do not turn absent runtime requests into observed Break/Retry
mutations. Source:
`xivl-captures:studies/guildleve-journal-command-wire/derived/verdicts.md`.
The remaining discriminators are an identified 12468 variation producer and
reply, 12487 objective property writes joined to slot semantics and an
attributable gameplay action, and identified allowance, grant and journal
transitions for the corresponding transaction.

## Source identity and reproduction

The named canonical Lua members and CSV members matched their complete size
and SHA-256 records in [scripts.json](../manifests/scripts.json) and
`xivl-client-data:manifests/tables.json`. The original OrbNormal LPB and decoded
payload matched [retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
`tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` supplied the cited article and
return operand observations.

The retained capture members matched
`xivl-captures:sources/pcap-1.23b/manifest.yaml`. The cited study products own
the packet interpretation and direction-local transaction boundaries.
The archive/member authentication does not reclassify those packets or add
unobserved gameplay actions. Reproduction selects the exact fields and
prototype sites above and the cited studies' bounded timeline rows.
