# Content director UI contracts

The recovered 1.23b Lua corpus preserves client-side director state and UI
contracts for guildleves, request leves, caravan escort, and Hamlet defense.
A reproducible decompile of the manifest-listed canonical subset matched the
published corpus byte-for-byte after CRLF-to-LF normalization. Other
independent decompiles below have different text hashes. That subset's
source identities, locators, and claim boundaries are in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json).
The other canonical source identities below are pinned in
[`scripts.json`](../manifests/scripts.json) and
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).

## Guildleve and request directors

`GuildleveBaseClass` stores the guildleve identifier, start time, aim counts,
UI states, extra marker coordinates, and a time limit. During initialization it
loads the guildleve sheet for the selected identifier and reads column 21 into
the retained `timeLimit` field. Other helpers read the recommended rank and
word text from columns 5 and 19. The class drives guildleve-information UI and
map or minimap marker calls from retained state.

`RequestDirector` derives from `GuildleveBaseClass`, overrides the time limit
with the literal value 20, and supplies request-specific UI initialization,
update, article, state, and parameter methods. These scripts establish client
state layout, sheet consumption, and widget calls. They do not establish
server timers, objectives, acceptance rules, completion, or rewards.

`GuildleveBaseClass.processUIInit` first copies all four `aimNumNow` and
`uiState` entries into temporary comparison arrays. If `getStartTime()` is
positive and `uiStep` is zero, it sets `uiStep` to one, sends
`processUpdateContentsInformation(self, "start", guildleveId)`, and refreshes
the minimap marker (`guildlevebaseclass.lua:263-273`; decoded bytecode
`0x0018AE-0x001942`). A `guildleveWork/start` update takes the same one-time
gate before the remaining update path (`processUpdateWork`, bytecode
`0x001A7D-0x001AE1`). For each of four objective slots, that path compares
`aimNumNow` and `uiState` with their temporary copies and sends an `"update"`
only if either changed (bytecode `0x001B01-0x001BAD`). This corrects the
broken recovered-Lua control flow; it does not prove a historical server
packet order, objective producer, or rendered widget appearance.
The LPB at `client/script/61s57qvs/3p1y6y5o5/3p1y6y5o589r57y9rr.le.lpb`
decoded byte-for-byte to the recovered LUAC (SHA256
`BCAD3160D16813502529467CE5DA17BB3A9BC80C576CD71841708FE7859D7E84`);
the recovered source identity is in `manifests/content_director_ui_contracts.json`.

`GuildleveBaseClass` keeps three `markerX/Y/Z` slots. Marker coordinates use a
separate `marker` work update from the `infoVariable` update used for aim counts
and UI states. Marker updates refresh the minimap; the map-open path publishes
the populated slots and may publish a separate extra marker when `signal` is
positive. Marker size is selected from retained `aetheryteLocation`: value 6
returns `normal` and every other value returns `small`; the setter maps those
values to size codes 2 and 1. Initialization stores its second argument as
`aetheryteLocation`; the source does not establish what value 6 means.

These details are in `guildlevebaseclass.lua:211,285-364,380,395-453,456,465-472,625-746,1260-1342,1516-1560`
(30,822 bytes, SHA-256
`0CD9F9853D1F91C07B583DB2BB7FACC4CB6A0C9C900DD8CF1953435CD19ACA19`,
`manifests/scripts.json:7833-7836`). The LPB and its decoded
payload are pinned above.

## Content-group map-open and finalization

`PlayerBaseClass.postMapOpen` enumerates the player's groups and calls
`processMapOpenMessage()` for each `ContentGroupBaseClass` whose
`getDirector()` result is non-null (`playerbaseclass.lua:2699-2726`). This
establishes a client dispatch path, not which director or map marker was active
in a particular retail session.

`ContentGroupBaseClass._onFinalize` requests world-master notification 50012
when the local player is a member and the group kind is 30001 or 30006
(`contentgroupbaseclass.lua:343-381`). The Lua identifies the numeric client
request; it does not identify the displayed text or establish what caused
finalization. Both decoded sources and their retail LPBs are pinned in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json).

## Caravan escort director

`CaravanGuardDirector` retains `finishTime`, `progressPer`, three chocobo status
values, three chocobo HP status values, and marker coordinates. Its UI methods
return those retained values and update public-effect, minimap, and map
navigation widgets. This authenticates client presentation fields and their
widget routes, not escort movement, enemy waves, failure rules, rewards, or the
server authority that updates the fields.

`getUIDataOpen` returns `finishTime`, `town`, `placeStart`, `placeEnd`, and
`name1` through `name3` in that order. `getUIDataUpdate` selector 1 returns
`progressPer`; selector 2 returns `chocoboStatus[1..3]`; selector 3 returns
`chocoboHPStatus[1..3]` (`caravanguarddirector.lua:333-368`). The selector
values and tuple order are client contracts; their server producers and the
meanings of the numeric status values are not established here.

The caravan director's minimap and full-map marker writes use group 2 and
size 1 with retained `work.markerX/Y/Z` coordinates
(`caravanguarddirector.lua:107-112`, `185-203`, `365-394`). During step 70,
the status-update and map-open paths enumerate up to three entries and write
only those whose `work.chocoboStatus[i]` is 4. The minimap path clears the
group before rebuilding it; finalization clears it. The widget methods store
group-2 entries in `GLMakerData`, reject slots outside 0..8, floor each
coordinate, and map size 1/2/3 to stored `Radius` values 32/64/128
(`minimapwidget.lua:14-60`, `mapnavigationwidget.lua:570-576`, `649-693`).
Thus a caravan size-1 call writes `Radius=32`; this is the widget property
value, not an independently measured world-space distance. The separate
actor-attached `getMapMarkerRange` route is not evidence that these caravan
markers follow an actor automatically. The script calls do not establish
the server's active coordinates, update frequency, or historical escort path.

`ChocoboCaravanWidget` uses text banks 10051 and 204 for contents and place
names. Its timer method subtracts `_getServerTime()` from the supplied time and
writes literal `300` and `120` values to `CustomControl_TimerLabel` properties;
the code alone does not assign display semantics to those fields. Company input
values 1, 2, and 3 select icon IDs 833, 834, and 835. Movement values 1-5
select command strings `ChocoboWalk`, `ChocoboStop`, `ChocoboFlight`,
`ChocoboEscaped`, and `ChocoboReturn`; HP values 1-3 select `StatusNormal`,
`StatusCaution`, and `StatusDanger` (`chocobocaravanwidget.lua:39-143`). The
strings and icon IDs do not establish rendered wording or image identity.

The caravan director, its dedicated widget, and the two map widgets match their
LPBs byte-for-byte after wrapper decoding. Their decoded SHA256 values are
`6B4A3198115E785842F2932333A6815DE833CF9FE6A9F6327027826085D9FE17`
(`director/caravanguard/caravanguarddirector`), `6E85FA941A43B00C54809D6C00213C4E3249013FF5795AC1F2D99477B3713B2A`
(`widget/chocobocaravanwidget`), `DBC794E094EC052D537FA0DC32912C5DAFDC5FD0242DC775E8060BB0E8C994B4`
(`widget/minimapwidget`), and `21CC7F2F9C6E2A56E02620E18748FA9DD70BF02DAB6A889FD6083826D60528C2`
(`widget/mapnavigationwidget`). Recovered-source identities are in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json)
and `manifests/scripts.json:7724-7729,15237-15240,15638-15643,15668-15673`.

The separate `PopulaceCaravanManager` client script loads text bank 7520
and exposes entry, question, join-success/failure, full/other-party, and
cancel dialogue methods (`populacecaravanmanager.lua:3-266`). Its cancel
method asks text ID 55 once and returns that saved result; direct bytecode
`0x00133C-0x0013A8` corrects the repeated ask printed by the decompiler.
Its entry path calls `isUpperRank` with argument 25 and asks selector 16, then
conditionally selector 23; its question path also calls `isUpperRank` with
argument 25 and asks selector 4 (`populacecaravanmanager.lua:11-189`). The
numeric arguments are not assigned meanings here.
`PopulaceCaravanGuide` loads bank 7552 and exposes offer, thanks, success,
failure, reward/no-reward, and bonus-reward dialogue methods
(`populacecaravanguide.lua:3-161`). Its reward method asks text ID 33 once
and returns the saved result (bytecode `0x000613-0x00065B`). The same method
branches on incoming R1 equal to 9, equal to 0, or in 1-5, with a separate
other branch. It then branches on R5 greater than or equal to 50, or in the
range 40 <= R5 < 50; these comparisons do not identify the argument semantics
(`populacecaravanguide.lua:20-60`). `PopulaceCaravanAdviser.adviserSales`
reads `getMoneyOnHand(1000001)`, passes the returned value to `say` row 53013,
and asks selector 14 with literal 3011317 (`populacecaravanadviser.lua:48-72`).
`ChocoboCaravanGuard.chocoboCommand` loads bank 7680, starts a client talk
turn, asks restricted choices, and calls ask row 6 with three forwarded
arguments only when the first result is 2; it returns both results.
`getBattalion` returns 1 (`chocobocaravanguard.lua:3-23`). These are client
presentation and ask surfaces, not evidence of the server's signup, route,
reward, or pack-chocobo actor selection. The four NPC/guard LPBs matched the
recovered LUACs byte-for-byte; their decoded SHA256 values are respectively
`2F553CD0595DBF6F38527B72BA3916416581CAE16E35BF036AB1CE10C175FDAA`,
`97ECACFBCFC68AA2B2F1FCB6215E7966C5F553D8B16F83B8EC8CCB2DC5ACC483`,
`7992483C774BBD234ECF29F9F1F68A89252D66A1F5B8D84772AAD5FDEE9C8F37`, and
`E1E8C253A8A20C9A1479772F53541EF1B471874A4B514710D04ACAE6655DDC27`.
Recovered-source identities are in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json)
and `manifests/scripts.json:6255-6271,1466-1471`.

## Hamlet defense director

`InstanceRaidHamletDefense` derives from `InstanceRaidBaseClass`. It retains a
Hamlet identifier, rank, defense-line status, and goods status, opens the
Hamlet execution widget, and routes timer, defense-line, goods, and boss status
values to that widget. Its local clear path requests the local player's Hamlet
defense score and, when available, opens the score widget for the content ID.

These methods establish client UI consumption only. They do not establish
enemy waves, routes, scoring formulas, victory conditions, server ownership,
or rewards.

The base director ignores data packets until its initialization flag is set;
packet selector 3 then forwards the remaining arguments to
`processUserMessage`. In `InstanceRaidHamletDefense.processUserMessage`, the
first forwarded value selects these client-side updates:

| Selector | Client-side update |
| --- | --- |
| 1 | When the execution widget exists, sets its title from the director content ID, sets its timer from the finish time, and shows it. |
| 2 | Copies three values to `harvestTbl[1..3]`. |
| 3 | Zeros `harvestTbl[1..3]` and asks the execution widget to reset its gathering display when present. |
| 4 | Copies six values to `fieldBuffTbl[1..6]`. |
| 5 | Normalizes three values into `lineStatusTbl[1..3]`: numeric 0 becomes 3, numeric 1 becomes 2, and every other value becomes 1. |
| 6 | Copies four values to `goodsStatusTbl[1..4]`. |
| 7 | Stores the first value as `cargoTarget`. |
| 8 | Sets `bossFlag` to true. |
| 9 | Stores the first value as `battleValue`; the HUD refresh passes it to `cmdSetWarPotentialValue` with maximum 100. |
| 10 | Calls the director's `dispInformation` helper with the remaining values, then returns. The helper sends a `worldMaster:notify` call and, when the popup widget exists, calls its `dispInformation` using a lookup-table entry and the Hamlet ID. The notice-ID meanings are not established here. |

The HUD maps line-status values 1/2/3 to normal, danger, and line-fall
commands; goods-status values 1/2/3 map to normal, danger, and goods-lost
commands. The update remaps goods slots in the order 1, 2, 4, 3, and maps a
zero cargo target to no selected goods. These are client UI mappings, not a
server scoring or state contract.

The client code does not support a false-to-1 / true-to-3 line-status
mapping. It maps numeric 0 to 3 and numeric 1 to 2, with all other values
mapped to 1. Whether a historical server sent booleans, these numeric values,
or any particular sequence is unknown.

The decoded-chunk pins below are the inputs used for the bytecode checks. The
instruction offsets locate the inspected methods within those decoded Lua 5.1
chunks; they do not establish a runtime packet or its effects.

| Method | LPB resource | LPB SHA-256 | Decoded payload SHA-256 | Inspected bytecode offsets |
| --- | --- | --- | --- | --- |
| `InstanceRaidBaseClass._onReceiveDataPacket` | `61s57qvs/1wrq9w75s916/1wrq9w75s91689r57y9rr.le.lpb` | `820F421AEF68BDCB48C082A2C1B91521903D0E82956C273CABC462B6B3271F2F` | `697419B9ABE065C5B77E67938F7AB4188B0C61B61F4B0E87F2D0FC05A6083941` | `0x0016D3-0x001787` |
| `InstanceRaidHamletDefense.processUserMessage` | `61s57qvs/1wrq9w75s916/1wrq9w75s91629xy5q6545wr5.le.lpb` | `2DDEDC8FAD4DAC5FAC4C800425DD8685F83E3DBF4CD8BD0AC996D265D540881E` | `FF329E9DEC60838A0D0FD5E2C42A27ABA60365BF52B44BCB8D6D43C709EB1A00` | `0x000A51-0x000E65` |
| `HamletDefenseWidget` status and target methods | `n1635q/29xy5q6545wr5n1635q.le.lpb` | `882B2B249B3DE84A593E4084E8CB7E49FBB00B3BF4CBD0FC911D1A2814964286` | `A564717080911218C718EA28F4A8B604A9850B3F2DB27BCD73ED9CEC93715D9E` | `cmdSetDefenseLineStatus: 0x000F5A-0x000FE6`; `cmdSetGoodsStatus: 0x001321-0x0013A9`; `cmdSetTargetGoods: 0x0015AD-0x001621` |
| `HamletDefensePopupWidget.dispInformation` | `n1635q/29xy5q6545wr5uvupun1635q.le.lpb` | `49DC594F8AA976696D7C2B42A2D57BF11925F36A9075ADCC7D36D141AF92A754` | `EB49B7D2F956BA4F66ACF5DEB9DD86259154E716898C14C665145E5B05157066` | `0x0000EC-0x0001D8` |

The resource paths and hashes are pinned in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json): the base
director at rows 1355-1366, the Hamlet director at 1279-1290, and the Hamlet
HUD and popup at 25218-25230 and 25233-25245. The recovered-source identities
are pinned in `manifests/scripts.json` at rows 8061-8064 and 15483-15495.

## Generic instance-raid director

The canonical
`lua/scripts/director/instanceraid/instanceraidbaseclass.lua`
has SHA-256
`f172046b273fd0e41a5fd9c9002c36563945e885820f5e73ea3c0a6de4c42adc`.
The corresponding LPB at
`client/script/61s57qvs/1wrq9w75s916/1wrq9w75s91689r57y9rr.le.lpb`
has SHA-256
`820f421aef68bdcb48c082a2c1b91521903d0e82956c273cabc462b6b3271f2f`.
The canonical class and method inventory is in
[`registry.json`](../lua/registry.json) under
`director/instanceraid/instanceraidbaseclass`.

`InstanceRaidBaseClass.init` declares retained start and finish times,
content ID, event type, countdown status, clear flag, and initialization
flag. It sets a one-second loop interval. The ordered `startEvent` sequence
and subclass-owned widget endpoint are recorded in
`xivl-decomp:docs/event/instance-raid-widget-lifecycle.md` and are not
redefined here. `reloginEvent` restores the retained values and opens the
widget only when its clear flag is false. The widget call is
`openRaidDungeonExecutionWidget(nil, contentID, finishTime)`.

The separate `InstanceRaidGuideBaseClass.askEnterInstanceRaid(raidId)`
calls `desktopWidget:askForEventMode` with prompt 52045, choices
52046/52047, and the supplied raid ID. It returns true only for answer
1. The LPB at
`client/script/729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p16589r57y9rr.le.lpb`
has SHA-256
`b9be2c3b9f3d9e35f6aea60474e054f9690c1c17466c6bf0fb92791eca321894`;
its decoded Lua 5.1 chunk matches the independently recovered LUAC
byte-for-byte (SHA-256
`54467e44bd629033695c561e4bc0f2dbbcf898343641ee6dd415a3643020a9a4`).
The method locator is `chara/npc/populace/instanceraidguide/instanceraidguidebaseclass.lua:10-17`.
This is an entry prompt/result contract, not evidence that an answer
starts a raid, scene, or HUD.

`clearEvent` stops countdown, orders desktop mode 126, closes the widget,
and notifies world-master row 52021 with content ID. `failedEvent` closes
the widget and selects a notification from rows 52065, 52054, 52010, and
52093 by its failure argument; non-first failure paths include fade and
effect calls. The recovered data-packet handler ignores packets until the
initialization flag is set. Its visible subtype 1 and 2 paths set the clear
flag and close the widget; subtype 1 also accepts replacement start/finish
times, while subtype 2 stops countdown. Subtype 3 delegates to
`processUserMessage`. The decompiled handler contains invalid `break`
statements, so this is a bounded branch reading, not a recovered packet
wire format.

The loop and `getRestTimeStatus` reference one-, three-, five-, ten-,
twenty-, and thirty-minute thresholds and a half-time notification. Some
temporary references in that decompile are damaged; the exact threshold
ordering and notification arguments are not established here. The class
proves a client presentation lifecycle, not server timer authority,
content creation, participant management, clear/failure policy, exit
movement, or rewards. In particular, the duplicate `createCutScene`
expression in `executeCutScene` does not prove two runtime allocations.

## Quest content-information directors

Five canonical scripts under `lua/scripts/director/quest/` join the
following `client/script/` LPBs. Hashes are SHA-256; class and
method inventories are in [`registry.json`](../lua/registry.json), and source
hashes are in [`scripts.json`](../manifests/scripts.json).

| Class | LPB suffix / hash | Canonical Lua hash |
| --- | --- | --- |
| `QuestDirectorGcg70101` | `61s57qvs/tp5rq/tp5rq61s57qvs373cjiji.le.lpb` / `10035dfb8289937f2b4350becc5e61f453f4fa77525346ad5849689adf9bc34d` | `2c799db73a5a079d2bc38f6ed60b5af6cd9bc2461a166c3f76ae8f67755c59b0` |
| `QuestDirectorGcl70101` | `61s57qvs/tp5rq/tp5rq61s57qvs37ycjiji.le.lpb` / `e73b02ba4f98e11ce34dde7059222ae2a8cac96a735e2b36add33b14785de92d` | `359ab5472f4ba9a84c923926f7c58360aba049a8731991f9900c7fa51b210c2c` |
| `QuestDirectorGcu70101` | `61s57qvs/tp5rq/tp5rq61s57qvs37pcjiji.le.lpb` / `4922c5bf4e904e3194f066502add6ee1570e2971b7e62373c2cd7b75cfc7d046` | `19ecf0bc38622f18ce040dfeba9357cf06988203e65f77dfb3cb844569b6d6e7` |
| `QuestDirectorNMRush01` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2ji.le.lpb` / `5a0b0b7524e0a6b0b9fa1dadb5fb1d7a0708dc8864aa1fe1be9ab9248437d04e` | `e73abd30092591d113b0ef002a77417d5dfaaef13b4a0c106facfc16864ae24e` |
| `QuestDirectorNMRush02` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2jh.le.lpb` / `c65739da2cb6817c6333b9d5d69a4db3b7118649304d0f461e8319bc9dab3491` | `8753c016df079227adb24f55538095ef63164953bfce5f051e9107127071c083` |

The three `Gc*70101` directors synchronize `directNumber` (int8), `point`
(int16), and `limitTime` (int32). Each reports content-information kind 1,
guildleve ID 0, maximum article index 1, instruction row 51115, article
row 33621, and a point threshold of 1000. Their distinguishing constants
are:

| Director | Title row | Article ID | Initial effect | `directNumber=20` effect |
| --- | ---: | ---: | ---: | ---: |
| `Gcg70101` | 51112 | 11000425 | 15 | 18 |
| `Gcl70101` | 51113 | 11000426 | 14 | 17 |
| `Gcu70101` | 51114 | 11000427 | 16 | 19 |

All three request effect 20 for `directNumber=-1` and effect 13 when
finalizing with `directNumber=0`. The recovered UI-update bodies contain
invalid `break` statements, so their exact branch fall-through is not
established by this decompile.

`QuestDirectorNMRush01/02` synchronize `directNumber` and `limitTime`,
retain a local timer flag, and report kind 1 with maximum article index 0.
Their title rows are 51143 and 51144 respectively; both return instruction
row 51145. Their recovered bodies request content-information start for
direct numbers 1 or 2 when the timer flag is false and cancel for 3 or
finalization. Damaged control flow limits claims about exact fall-through.

The canonical
`lua/scripts/widget/desktopwidget_connector.lua` (SHA-256
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`)
matches `client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb` (SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`).
Its `processUpdateContentsInformation` checks the actor and dispatches
kind 1 to `GuildleveExecutionWidget` and kind 2 to
`ChocoboCaravanWidget` before calling `updateContentsInformation`.
Thus the five kind-1 directors request the guildleve execution widget
route, not a separately identified quest-specific widget.

These are client widget inputs, not proof of server score authority, timed
encounter ownership, quest completion, or reward grant. The contributor's
content-information adapter and widget-result security proposals are
server implementation, not retail observations.

## Raid dungeon occupancy widget

Two recovered occupancy directors and their widget have corresponding
`client/script/` LPBs and independent recovered-Lua SHA-256 identities:

| Class | LPB path / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `RaidFst0Dungeon03` | `61s57qvs/v77pu9w7l/s9164rqj6pw35vwjg.le.lpb` / `3fc7b9326942492a56c652ada5564b6eb9e528977a9d513ae1e794fa858f1652` | `5984f33d4328df277aa0accb8b310b9d18282423cb8c337646a73a0b3bd6d393` |
| `RaidRoc0Dungeon01` | `61s57qvs/v77pu9w7l/s916sv7j6pw35vwji.le.lpb` / `3b7e73d556fc9016951cb4897a85fad7ff2b93e5ccd570e2c229414e6f0e4cf2` | `ec6e626a70d41a976da06a327663581cc1473e35adb4b73e67079529bbb6d7db` |
| `RaidDungeonExecutionWidget` | `n1635q/s9166pw35vw5m57pq1vwn1635q.le.lpb` / `f02fdcd3ecbf7269937c19d664532afae94744aec33a104d364fdb795504f67d` | `8a2d239324a1ce8fc23dee64596f4ab94c1be9df862a967d522d68fe1e98e814` |

`RaidFst0Dungeon03.eventNoticeCutScene` treats `rad0f300` as its opening
scene and requests widget close for `rad0f306`, `rad0f307`, or `rad0f308`.
It then requests a cutscene in mode 61 and passes content ID 2123, type 1,
and the method's fifth argument to `openRaidDungeonExecutionWidget`.
For `rad0f300`, the method sets its local branch flag instead of calling
`_fadeOut`; after starting the cutscene and deleting its object, it calls
`_fadeIn`. `relogin` calls
`_fadeInNowLoadingForNoticeEventJustInArea`, as does
`CutScene.startCutScene` immediately before `_loadCutScene`. These are
recovered call sequences, not proof of visible loading or fade behavior.
The director source is `director/occupancy/raidfst0dungeon03.lua:29-78,93-107`
(SHA-256 `A01AF800CC925D858191AAC416EBDA2CA79DAF52F1148DA45CAB1F2A552D6C4C`);
the common source is `gamedata/cutscene_common.lua:1064-1075,1316` (SHA-256
`F6DB9559B3F805D2738C073C7DB9DD102FD5C33A056E789FF2FB2F8AFF395BD1`). Both
are pinned in `manifests/scripts.json:8223-8226,9519-9522` and joined to
retail resources by `manifests/retail_lua_coverage.json:5480-5492,815-826`.
No cited evidence joins `rad0f300` to native spawn types 16 or 21; their
separate dispatcher branches establish capability, not a historical scene
selection (`xivl-decomp:docs/actor/animation-bank-routing.md`).
`RaidRoc0Dungeon01` uses opening scene `rad0r100`, closes for
`rad0r106`, and opens with content ID 4102, type 2, and its fifth
argument. Both `relogin` methods request the same widget open when their
fourth argument is false. Both `processUIFinalize` and `widgetSetOff`
request close. The decompiled cutscene expression repeats
`createCutScene`; that output does not establish two runtime allocations.

`RaidDungeonExecutionWidget.init` forwards its content and finish-time
arguments to `setContents` and `setTimer`. `setContents` uses text bank
10051 for `TextBlock_ContentsName`. `setTimer` writes
`finishTime - worldMaster:_getServerTime()` to timer-label
`FloatData.Value0`, with `FloatData.Value1 = 0`,
`FloatData.Value2 = 300`, `IntData.Value1 = 300`, and
`IntData.Value2 = 120`. Those are client widget inputs; the script does
not prove server timer authority, actual content duration, clear ownership,
exit cleanup, or reward policy.

## Evidence boundary

No Behest or Skirmish script in this filing proves wave composition, routes,
objectives, timers, or rewards. Those systems, and the server-side behavior
behind the four recovered directors, remain unresolved and must not be filled
from analogy.
