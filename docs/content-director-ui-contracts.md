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

`GuildleveExecutionWidget.setArticleType` handles render type 6 by writing its
first value argument to `TextBlock_Bunshi_<row>` and
`ProgressBar_<row>.Value`, and its second value argument to
`TextBlock_Bunbo_<row>` and `ProgressBar_<row>.Maximum`. This records widget
writes only; render type 6 and the values have no assigned objective or server
meaning here.

Source identity: `lua/scripts/widget/guildleveexecutionwidget.lua`, method
`setArticleType`, maps to
`client/script/n1635q/3p1y6y5o55m57pq1vwn1635q.le.lpb` (LPB SHA-256
`8EED436E9058CBA2BC7EA92603A1A493CF10BE7ACE8B676EA66B5F384326C8CD`, decoded
payload SHA-256
`58812BFCCC48E5D651569F55382DE88C55A365EC91D0A9171FFE93E751EFCE13`;
`retail_lua_coverage.json:25263-25275`).

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

### Guildleve timer, card, and instruction helpers

`GuildleveBaseClass.getTimeLimit` returns the retained `timeLimit`, and
`getTimeDataOnGuildleveInfo` returns the start time plus 60 times that value,
then the same sum minus 60 (`guildlevebaseclass.lua:565-572,821-837`).
`GuildleveExecutionWidget.init` passes both results to `setTimer`
(`guildleveexecutionwidget.lua:63-66`). `setTimer` subtracts
`worldMaster:_getServerTime()` from each value, sets `IntData.Value0` of
`CustomControl_TimerLabel` to 1, writes the first difference to
`FloatData.Value0`, zero to `FloatData.Value1`, and the gap between the two
differences, 60, to `FloatData.Value2` (`:280-323`). The client therefore
scales sheet column 21 by 60 against the server clock. This makes the column
a minute count only if the start time and server time are in seconds, which
the corpus does not establish. A prior external lead,
`Guildleves/00-guildleves-overview.md` and `Guildleves/40-faction-leves.md` at
revision `d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, gives 30- and 40-minute
guildleve timers; stored column values are in
`xivl-client-data:docs/guildleve-selected-row-values.md`.

When the director has a guildleve ID, the same `init` reads `guildleve_UI`
columns 76, 77, and 75 for it and passes them to `setCard`
(`guildleveexecutionwidget.lua:88-122`).
`setCard` writes them to `IconControl_Card`, `IconControl_Plate`, and
`IconControl_TownName` and shows `Label_GLPlate`. When the first value is nil
or not positive, it clears all three icons and hides the label instead
(`:230-277`).

`getIdForInstruction` (`guildlevebaseclass.lua:855-913`) maps the keys
`sweep`, `gather`, `chase`, `detect`, `orb`, `survive`, `hunt`, `round`, and
`follow` to 10011, 10021, 10031, 10041, 10051, 10061, 10071, 10081, and 10091,
maps `glText` to 50003, and returns 10011 for any other key. Six director
subclasses call it, all passing `glText`. `getTextIdForInfo`
(`:1019-1052`) maps `glText`, `glOrder`, `enemy`, `enemyParty`, and `item` to
50003, 50089, 50001, 50099, and 50002, and returns 50047 otherwise; the base
class and 19 director subclasses call it. Neither method names the text sheet.
The 100xx values equal objective row IDs of `xtx_guildleveText.csv`; all but
10091 also occur in `guildleve.csv` column 17.

Evidence: `lua/scripts/director/guildleve/guildlevebaseclass.lua` (pinned
above) and `lua/scripts/widget/guildleveexecutionwidget.lua` (17,377 bytes,
SHA-256 `E01C200DB8DEBC404B103C72C95F02E736BD57419E25AB2CF5653936A7631510`,
`manifests/scripts.json:15470-15475`).

## Content-group map-open and finalization

`PlayerBaseClass.postMapOpen` enumerates the player's groups and calls
`processMapOpenMessage()` for each `ContentGroupBaseClass` whose
`getDirector()` result is non-null (`playerbaseclass.lua:2699-2726`). This
establishes a client dispatch path, not which director or map marker was active
in a particular retail session.

The [party continuity contract](guildleve-party-continuity.md#content-group-and-party-are-separate-state)
owns the content-group work, membership and finalization callbacks. The player
and content-group decoded sources and their retail LPBs are pinned in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json).

### Owned content-widget slots

`DesktopWidget.getFreeContentsIndex` scans slots 1 through 4 for an empty
owner, and `getContentsIndex` searches the same range for a valid owner and
matching content type. `getContentsWidgetIndex` returns `slot + 5`, so slots
1 through 4 produce values 6 through 9. `openContentsWidget` passes that
result to `openWidget`; when that call does not return false and the
slot had no owner, it stores the actor and content type at that slot. Bytecode
locators: `getFreeContentsIndex` root/proto202 PCs 3-15, offsets
`0x019E00`-`0x019E30`;
`getContentsIndex` root/proto203 PCs 3-21, offsets `0x019EA3`-`0x019EEB`;
`getContentsWidgetIndex` root/proto548 PCs 0-2, offsets `0x0335B2`-`0x0335BA`;
`openContentsWidget` root/proto546 PCs 30-54, offsets `0x03338E`-`0x0333EE`.
These are static slot and ownership operations; they do not establish a
historical open or visible widget.

## Map navigation widget

`MapNavigationWidget.init` stores its mode on `CustomControl_MapNavigation`.
For mode 2 it sets the widget nonmodal and disables focus, widget input, and hit
testing on both the widget and map control. `DesktopWidget.openMapForCutScene`
opens `MapNavigationWidget` on layer 11 in mode 2 with the supplied map argument
when cutscene mode is active and the desktop cutscene-map flag is clear. This is
a static client configuration and open route; no historical invocation or
visible map is established here.

The piece-menu path calls `getAchieveAetheryteID(regionId, false)` before
requesting `aetheryte2DmapSheet`. Its piece-list helper reads positive values
from columns 17 through 20, and `updateAetheryteList` makes a row visible only
when the player's `getAchieveAetheryte(rowID)` returns true.
`mapNaviDataSheetLoaded` reads columns 1 and 2 for the selected row and passes
them to `setDisplayLocation`, which writes them to the map control's `Layout`
and `Rect` properties. The selected row and column values are not assigned
domain meanings here.

`DesktopWidget.setMapNavigationWidgetMarkerData` looks up a layer-3
`MapNavigationWidget`, forwards six supplied values to its marker-data method,
and returns true when the widget exists. `MapNavigationWidget` routes selector
value 2 to `setActiveGuildleveMarker`. The available Lua does not assign
meanings to those positional values. Separately, when its menu category is 1,
`addMarkerList` stores a value as list-item data; `setQuestMarker` writes a
value to `ssd_marker_data.Row`, and
`dispMarker` writes a value to `CustomControl_MapNavigation.QuestMapIndex`. These
properties and values remain uninterpreted; no server field meaning or
historical response/invocation is established here.

`DesktopWidget.processRecievedRequestedDataForWidget` also handles the `qtmap`
vararg branch (bytecode PC `009`-`065`, offsets `0x01225F`-`0x01233F`). It looks
up `MapNavigationWidget` on layer 3 and stops if the widget is absent or there
are no varargs. It calls `initMarkerList` with the vararg count, then passes
each `(index, value)` pair to `addMarkerList`. It builds a comma-separated row
from `tostring` of every vararg and passes it to `setQuestMarker`; `dispMarker`
receives `tostring` of the first vararg. `MapNavigationWidget.initMarkerList`
has no Lua instructions beyond return. `addMarkerList` writes the item text
with key `5208`, stores the selected value, and shows the item only when
`getMenuCategory() == 1` (bytecode offsets `0x003B90`-`0x003BD4`). This is a
client-side argument route. It does not establish what the varargs represent,
whether the route is reached historically, or whether the property writes
produce visible markers.

Source identities are pinned in `manifests/retail_lua_coverage.json`:

- `lua/scripts/widget/mapnavigationwidget.lua` (`init`,
  `callbackSelectRegionMenuList`, `setSelectPieceMenuList`,
  `pushSelectPieceMenuListItem`, `updateAetheryteList`,
  `mapNaviDataSheetLoaded`, `setDisplayLocation`,
  `setMapNavigationWidgetMarkerData`, `setActiveGuildleveMarker`,
  `addMarkerList`, `setQuestMarker`, `dispMarker`):
  `client/script/n1635q/x9uw9o139q1vwn1635q.le.lpb`, LPB SHA-256
  `873EE821C979B9C0959743BC619444EC01BD39C96F71235235278BB602B4D0BB`, decoded
  payload SHA-256 `21CC7F2F9C6E2A56E02620E18748FA9DD70BF02DAB6A889FD6083826D60528C2`
  (`retail_lua_coverage.json:27888-27900`).
- `lua/scripts/widget/desktopwidget_connector.lua`
  (`setMapNavigationWidgetMarkerData`, `openMapForCutScene`,
  `getFreeContentsIndex`, `getContentsIndex`, `getContentsWidgetIndex`,
  `openContentsWidget`):
  `client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, LPB SHA-256
  `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425`, decoded
  payload SHA-256 `685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`
  (`retail_lua_coverage.json:25443-25455`).

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

The base director's [data-packet callback](#instance-raid-data-packet-callback)
returns early when its initialization flag equals false. Selector 3 forwards
the remaining arguments to `processUserMessage`. In
`InstanceRaidHamletDefense.processUserMessage`, the
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
| 10 | Calls the director's `dispInformation` helper with the remaining values, then returns. Its exact lookup and ordered popup/notice calls are recorded below; rendered text and historical trigger meanings remain unbound. |

The HUD maps line-status values 1/2/3 to normal, danger, and line-fall
commands; goods-status values 1/2/3 map to normal, danger, and goods-lost
commands. The update remaps goods slots in the order 1, 2, 4, 3, and maps a
zero cargo target to no selected goods. These are client UI mappings, not a
server scoring or state contract.

The client code does not support a false-to-1 / true-to-3 line-status
mapping. It maps numeric 0 to 3 and numeric 1 to 2, with all other values
mapped to 1. Whether a historical server sent booleans, these numeric values,
or any particular sequence is unknown.

### Hamlet information helper

`InstanceRaidHamletDefense.dispInformation(self,key,...)` constructs its lookup
inside the method. Keys 1 through 18 select numeric notice IDs 11 through 28
in order. The remaining two row values are passed to the popup as follows:

| Input key | Notice ID | Boolean argument | Numeric argument |
| --- | --- | --- | ---: |
| 1 through 10 | 11 through 20, respectively | false | 0 |
| 11 | 21 | true | 1019 |
| 12 | 22 | true | 1091 |
| 13 | 23 | true | 1022 |
| 14 | 24 | true | 1063 |
| 15 | 25 | true | 1013 |
| 16 | 26 | true | 1018 |
| 17 | 27 | true | 1017 |
| 18 | 28 | true | 1063 |

The helper retains exactly one result of
`desktopWidget:getHamletPopupWidget()`, then constructs and indexes the lookup.
There is no missing-key fallback or conversion of string keys to numbers.
A missing row fails during indexing before either display call, including
when the popup result is nil.

For a valid key and a non-nil popup, the first call is
`popup:dispInformation(row[2],self.work.hamletID,row[3],self,row[1],...)`.
A false Boolean table value does not skip that call. The availability test
compares the popup result with nil, rather than testing general Lua falsiness.
The continuing path then calls `worldMaster:notify(self,row[1],...)`.
A nil popup skips the popup call and Hamlet-ID read but still reaches notify.
The helper catches no exception; a failing popup call does not establish
delivery of the later notice.

Both calls forward the complete variadic tail, including nil positions,
and discard their results. The helper returns zero Lua values. Its supplied
provider is the director receiver; it does not substitute WorldMaster as the
explicit provider. The [log-argument contract](worldmaster-message-arguments.md#countdown-log-arguments)
owns the common forwarding/native contract, subject to its typed-capture and
source-readiness conditions. These numeric arguments do not prove rendered
text, item identity, historical key selection or a server event policy.

The original helper is `root/proto10`, `[0x1133,0x12FF)`, 115 instructions.
Its local R4 lookup is produced at PCs 3-94, `[0x113F,0x12AF)`, within that
same body. Root PCs 37-39, `[0xB4,0xC0)`, bind the class/name/closure. These
are zero-based PCs and half-open decoded-payload offsets. The director LPB,
payload and canonical source are pinned below. Focused static replay checked
all 18 keys, popup nil/present cases, full tails, invalid-key failure and
return arity; it did not execute the client.

The decoded-chunk pins below are the inputs used for the bytecode checks. The
instruction offsets locate the inspected methods within those decoded Lua 5.1
chunks; they do not establish a runtime packet or its effects.

| Method | LPB resource | LPB SHA-256 | Decoded payload SHA-256 | Inspected bytecode offsets |
| --- | --- | --- | --- | --- |
| `InstanceRaidBaseClass._onReceiveDataPacket` | `61s57qvs/1wrq9w75s916/1wrq9w75s91689r57y9rr.le.lpb` | `820F421AEF68BDCB48C082A2C1B91521903D0E82956C273CABC462B6B3271F2F` | `697419B9ABE065C5B77E67938F7AB4188B0C61B61F4B0E87F2D0FC05A6083941` | `0x0016D3-0x001787` |
| `InstanceRaidHamletDefense.processUserMessage` | `61s57qvs/1wrq9w75s916/1wrq9w75s91629xy5q6545wr5.le.lpb` | `2DDEDC8FAD4DAC5FAC4C800425DD8685F83E3DBF4CD8BD0AC996D265D540881E` | `FF329E9DEC60838A0D0FD5E2C42A27ABA60365BF52B44BCB8D6D43C709EB1A00` | `0x000A51-0x000E65` |
| `InstanceRaidHamletDefense.dispInformation` | Same director resource above | Same director LPB above | Same director payload above | `[0x001133,0x0012FF)` |
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

The separate `InstanceRaidGuideBaseClass.askEnterInstanceRaid` question,
its supplied display value and exact return arity are owned by the
[primal entry boundary](primal-entry-client-contract.md#generic-question-and-answer).

`clearEvent` stops countdown, orders desktop mode 126, closes the widget,
and notifies world-master row 52021 with content ID. `failedEvent` closes
the widget and selects a notification from rows 52065, 52054, 52010, and
52093 by its failure argument; non-first failure paths include fade and
effect calls.

### Instance-raid data-packet callback

Original `_onReceiveDataPacket` bytecode returns immediately when
`instanceRaidWork.initFlag == false`. This is an exact boolean comparison,
not a truthiness test. R0 is self, R1 is the selector, and the remaining
arguments form the vararg tail. The callback compares the selector with
literal numbers without converting strings.

| Selector | Ordered writes and calls |
| --- | --- |
| 1 | Set `instanceRaidWork.clearFlag=true`; retain the first result of each `select(1,...)` and `select(2,...)`; call `self:setCountDownTimer(first,second,false)`; call `self:closeInformationWidget()`; return. |
| 2 | Set `instanceRaidWork.clearFlag=true`; set `instanceRaidWork.countdownStatus=0`; call `self:closeInformationWidget()`; return. This branch reads no varargs. |
| 3 | Call `self:processUserMessage(...)` with all remaining arguments, preserving their positions; return. |

Every normal path returns no Lua results. Other selectors return without
these writes or calls. There is no reachable fallthrough between selectors
or loop in this callback. Selectors 1 and 2 do not call `clearEvent` or
`failedEvent`; their state changes do not establish the full clear/failure
presentation or settlement sequence.

The authenticated decoded payload has SHA-256
`697419b9abe065c5b77e67938f7ab4188b0c61b61f4b0e87f2d0fc05a6083941`.
Its `root/proto13` contains 46 instructions in `[0x16D3,0x178B)`, with
zero-based PCs. The guard is PCs 0-4; selector-1 writes/calls are 8-24;
selector-2 writes/call are 29-34; selector-3 forwarding is 39-41. Completion
jumps at PCs 25/35/42 target return PC 45. PCs 26/36/43 are unreachable
jumps, which explains the damaged `break` rendering without assigning it
runtime behavior. The LPB and canonical source identities are pinned above.
The conditional native caller is qualified in
`xivl-decomp:docs/event/user-data-receiver.md`, Requested Lua frame.
The mapped actor `0x0133` path requests `_onReceiveDataPacket` with binding
value O followed by actual materialized values D0, D1 and later arguments.
If that lookup selects this InstanceRaid function, R0 is O, R1 is D0 and the
vararg tail begins at D1. The native profile owns the ordinary supported-value
conditions and the distinct unresolved-actor/error-marker limits. This
composition does not select an actual actor/class, caller variant, supplied
time values, message provider, clear policy or historical packet sequence.

### Instance-raid countdown and notices

Original bytecode resolves the countdown comparisons and notification operands
lost in the decompile. Let S and F be the retained start and finish times,
N the first result of `worldMaster:_getServerTime()`, and H the first result
of `self:getHalfTime()`. `getRestTimeStatus` samples N before H and tests
`M=[1,3,5,10,20,30]` in ascending index order. It returns the first index i
for which both `F-60*M[i] <= N` and `60*M[i] < H` hold. Only when none
qualifies does `S+H <= N` return 7; otherwise it returns 0. Fixed thresholds
therefore take precedence over half-time, and equality with H excludes a
fixed threshold. There is no separate `F <= N` expiry branch.

`getHalfTime` returns the single value 5940 when `clearFlag` is exactly
Boolean true. Otherwise it tail-calls `_math.ceil((F-S)/2)`, forwarding that
callee's results. The selected callers retain only its first result. The
[clock qualification](player-command-event-routes.md#clock-qualification)
establishes whole-second samples for N only under the documented native
binding, including its signed return conversion. The supplied S/F producers
and their compatible clock domain remain unbound.

`setCountDownTimer(self,S,F,flag)` writes the times first. Exactly Boolean
false sets `countdownStatus=7` without calling the status getter. Every other
flag value uses the getter: nonzero status r stores r-1, while zero stores 7.
The setter does not notify or write the clear/initialization flags.

`_onLoop` returns when retained status is 0 or the getter returns 0. Otherwise
it proceeds only when r is at most the retained status, storing r-1 before
notification. This suppresses repeated statuses and emits only the current
status when an update skips thresholds. Moving time backward to a larger
status does not restore retained state or emit. After status 1 stores 0,
further loop countdown work is suppressed until another writer changes it.
This selected loop does not test `initFlag`; its second formal argument is
unused.

| Status r | Row | Last explicit argument |
| --- | ---: | --- |
| 1 through 6 | 52009 | `M[r]` |
| 7 | 52092 | First result of `_math.ceil(self:getHalfTime()/60)` |

The call is `worldMaster:notify(worldMaster,row,self:getContentID(),value)`.
The underlying function receives exactly five arguments in order:
worldMaster receiver, explicit worldMaster, row, first content-ID result,
and value. `SELF A5` and `CALL A5 B6 C1` at `_onLoop` PCs 38/44 preserve
that duplicate worldMaster and discard notify results. The half-time branch
recomputes H for its value. The loop and setter return zero Lua results;
`getRestTimeStatus` returns exactly one. These operands alone do not assign native
provider meaning to the explicit worldMaster or prove rendered notices.

The [countdown log-argument composition](worldmaster-message-arguments.md#countdown-log-arguments)
joins this tuple to `notify`, `showLog` and the already qualified native
log-pool entry, preserving the explicit provider and conditional source lookup.

The same pinned LPB and decoded payload above contain these four methods.
The following code intervals are half-open decoded-payload offsets; PCs are
zero-based. Root CLOSURE/SETTABLE pairs at PCs 20/21, 23/24, 26/27 and 29/30
bind the listed names.

| Method | Prototype | PCs / code interval |
| --- | --- | --- |
| `_onLoop` | `root/proto3` | 0-45 / `[0x739,0x7F1)` |
| `getRestTimeStatus` | `root/proto4` | 0-37 / `[0x913,0x9AB)` |
| `getHalfTime` | `root/proto5` | 0-16 / `[0xA8F,0xAD3)` |
| `setCountDownTimer` | `root/proto6` | 0-18 / `[0xB68,0xBB4)` |

Focused static instruction replay checked threshold equality, strict half-time
exclusion, exact Boolean flags, repeats, time reversal, skipped thresholds,
return arity and notification argument order. Comparison and argument-operand
mutations failed the corresponding expectations. This was not client execution.
The class proves a conditional presentation lifecycle, not server timer authority,
content creation, participant management, clear/failure policy, exit
movement, or rewards. The [scene helper](#instance-raid-cutscene-helper) records its original
creator, argument and saved-result contract.

### Instance-raid cutscene helper

Original `InstanceRaidBaseClass.executeCutScene` calls
`worldMaster.createCutScene` once and retains only its first result C. The
creator receives exactly `(worldMaster, scene, subject)`; when the supplied
subject is nil, the helper substitutes self. False and other non-nil subjects
are preserved. The helper selects mode 2 only when its flag is exactly
Boolean false; every other flag selects mode 1.

It then calls `startCutScene` with `(C, 1, 63, mode, ...)`, preserving the
complete variadic tail, including nil holes. There is no nil, false or
truthiness guard on C before the method lookup. On normal return from start,
it calls `_delete` with the same saved C. Both calls discard their results,
and the helper returns no Lua values. There is no local protected cleanup
path if a lookup or called method raises an error.

The retained `InstanceRaidLesserWhiteGeneral.processCutSceneEvent` call with
flag true therefore selects mode 1 in this helper. This resolves the repeated
creator expression in the decompile as one Lua creator invocation; it does
not establish native allocation count, successful playback, native object
destruction or a historical invocation.

The pinned base-director LPB and decoded payload above contain this helper at
`root/proto16`, zero-based PCs 0-20, half-open payload interval
`[0x1935,0x1989)`: 21 words/84 bytes. Root PCs 58-60 load the class and bind
the named child, at `[0x108,0x114)`. PCs 1-6 select mode and subject;
creator CALL 11 is at `0x1961`, start CALL 17 at `0x1979`, delete CALL 19 at
`0x1981`, and zero-result RETURN 20 at `0x1985`.

Focused static instruction replay checked exact Boolean/nil distinctions,
one creator call, first-result retention, same-object start/delete, complete
variadic argument order and zero-result returns. Saved-result, branch,
argument-count and duplicate-creator mutations failed their checks. These
checks authenticate a conditional Lua contract, without client execution.

The LPB was decoded with `tools/retail_script.py` (`decode_lpb`), and
instructions were read with `ChunkReader` and `instruction` in
`tools/build_quest_contracts.py`, at revision
`6a19d5909c1a454b9b0656ef75e311c5d7501f31`.

#### WorldMaster scene factory

Original `WorldMaster.createCutScene` has three fixed formal slots: receiver,
scene and subject. It has no variadic tail and does not read its receiver.
The wrapper resolves global `_createActor` and tail-calls it once with exactly
five arguments: `(nil, "CutScene", false, scene, subject)`. The explicit nil
and false retain their positions. Nil or false scene/subject values pass
through unchanged, with no fallback or conditional test in this factory.
Extra incoming arguments beyond its fixed formal slots are not forwarded.

The wrapper propagates all results of that call, including zero results and
nil positions. It performs no subsequent Lua initialization call or result
check. The instance helper and occupancy callers retain only the first result
at their own call sites; their later method lookups do not imply that this
factory validated or initialized that result. Native construction and any
initialization inside `_createActor` remain outside this Lua contract.

The canonical source `lua/scripts/world/worldmaster.lua` is 2479 bytes,
SHA-256
`c0a7e0460ef969fe5c10de5593e3237a279258a5849df3d2b7f534b08732a4ba`
(`manifests/scripts.json:16023-16026`). Its original resource is
`client/script/nvsy6/nvsy6x9rq5s.le.lpb`, SHA-256
`da3adccea066061a6289b89af65bde92db13a5eabbdd1f0072565576d5414d20`;
the decoded payload has SHA-256
`6dca2434550518b09fe58d4878da3f0f0a77c1124808c231ad399b87089e420d`
(`manifests/retail_lua_coverage.json:28083-28095`).

Exact root PCs 21-23 bind WorldMaster, the child closure and method name at
half-open decoded-payload interval `[0x74,0x80)`. The factory is
`root/proto6`, PCs 0-8, `[0x525,0x549)`, nine words/36 bytes. The fixed
five-argument `TAILCALL` is PC 6 at `0x53D`, followed by the open `RETURN`
at PC 7. Producing tools were `tools/retail_script.py` (`decode_lpb`) and
`ChunkReader`/`instruction` in `tools/build_quest_contracts.py`, at revision
`a8d88abef3b659281c13adc95fd4d362a50d6005`.

Focused static operand checks and replay verified fixed argument positions,
nil/false distinctions and complete factory result propagation. The existing
caller proofs establish their first-result retention. Argument, flag and
return-arity mutations failed the corresponding checks. These are conditional
Lua instruction facts, without client execution, native allocation/playback/
destruction proof or historical event attribution.

#### CutScene initializer inputs

Original `CutScene._onInit` has three fixed formal slots `(self, scene,
subject)`, no upvalues and no variadic tail. It calls
`self:_callSuperClassFunc("_onInit")` without forwarding either payload value
and discards the results. It then fetches `self.work` and assigns its `_temp` an ordered table
of three pairs: `("textOwner", "actor")`,
`("isPreviewTextOwner", "boolean")` and `("actorclassSheet", "actor")`.
This assignment alone does not establish native member registration.

It calls `self:_setFilename(scene)` and discards the results. The
`CutScene` overload's filename store and later `_play` consumer are owned by
`xivl-client-structs:docs/stub-overload-native-contract.md`, CutScene
_setFilename. Next it fetches `self.work` into a saved register, calls global
`_createActor(nil, "SpreadSheet", false, "actorclass")`, and assigns only
the first result to that saved value's `actorclassSheet`. Zero returned
values supply nil to this assignment. The following assignments each fetch
`self.work` again: `textOwner` receives `subject`, then `isPreviewTextOwner`
receives Boolean false. These separate work lookups need not return the same
value across opaque calls, yields or metamethods.

All 36 instructions form one local path ending in a zero-result return.
There is no local result test or protected cleanup. The sequence assumes
successful lookups and normally returning calls. The native payload handoff
is recorded in `xivl-decomp:docs/actor/world-master.md`, Native scene-creation
handoff, at revision `500b02ea661743b8826f4a264dadbf3e97bd5690`.
Here scene and subject name its incoming converted payload values; the
subject store does not prove identity with the original caller object or a
world player. Spreadsheet construction and readiness remain conditional on
the native contract in
`xivl-client-structs:docs/create-actor-native-contract.md`.

The canonical `lua/scripts/gamedata/cutscene.lua:7-53` has SHA-256
`89a7ec2df66697ffe012b17200194bf1851147b234fd240d738138b249ad4264`
(`manifests/scripts.json:9513-9516`). Its 727-byte original resource
`client/script/39x569q9/7pqr75w5.le.lpb` has SHA-256
`cfb5ad38220b3b9a1dd8ae3ba8cae05feef84be3a845d56a2954efedb2d807c2`;
the 714-byte decoded payload has SHA-256
`fae5ec95e85f0de381a366d1ec76643444b181173747fa11ba7d0019c2379b1d`
(`manifests/retail_lua_coverage.json:799-811`). Root PCs 3-5 at
`[0x2C,0x38)` bind `CutScene._onInit` to `root/proto0`; its complete
PCs 0-35 occupy `[0xBC,0x14C)`, 36 words/144 bytes. CALL PCs 2, 21
and 29 encode superclass, filename and Spreadsheet calls respectively.
Focused offline operand checks and register replay verified the ordered
inputs, first-result retention, saved work reference, separate work lookups,
typed false and zero-result return. Fourteen decoded semantic mutations
were rejected independently of the original-byte hash check. The LPB and
instruction decoders are `tools/retail_script.py` and
`tools/build_quest_contracts.py` at revision
`5507da1522e173f7fcad29d6b0bc7294b64b6ea5`.

#### Caption clip arguments

Original `CutScene._onShowUIClip(self, tag, actorClass, ...)` selects its
caption arm for either exact tag `Caption` or `CaptionClip`. It keeps only
the first result of `self.getNameByActorClass(self, actorClass)`, then calls
the global named `select` with `(1, ...)` and keeps only its first result.
Zero returned values at either call supply nil to that saved position.
It next prepares `desktopWidget.showCaption`, loads `self.work.textOwner`
and separately resolves global `select` for `(2, ...)`. Every result from
this second select becomes the open tail of the caption call.

The call's fixed positions are `(desktopWidget, derivedName, owner,
firstSelectResult)`, followed by that complete tail. With the standard Lua
5.1 `select` binding, these are the receiver, derived name, owner, first
vararg and every remaining vararg. Explicit and trailing nil positions keep
their argument extent. With no varargs, the first-vararg position is nil and
the tail adds no arguments. The decompiler's expanded temporary list does
not limit this open tail to its printed register count. The caption call
discards all results and the selected arm returns no values after normal
completion of its calls.

The owner lookup occurs after the opaque name lookup and first select. It
does not cache the [initializer's subject store](#cutscene-initializer-inputs)
or establish that the owner and derived name identify the same actor. The
two select globals are loaded separately. Name lookup, select bindings and
the widget callee remain conditional. Argument positions do not establish
actual text, actor identity, a rendered caption, scene invocation, encounter
mode or native callee behavior.

The canonical `lua/scripts/gamedata/cutscene_common.lua:502-525` is
46,939 bytes, SHA-256
`f6db9559b3f805d2738c073c7db9dd102fd5c33a056e789ff2fb2f8aff395bd1`.
Its 9,125-byte resource
`client/script/39x569q9/7pqr75w5_7vxxvw.le.lpb` has SHA-256
`a5279136c0ee8f6ef2342fd22af2b9cd12f9b6aff5a4feff4bc0fc21367f5321`;
the 9,112-byte decoded chunk has SHA-256
`7ef33408c579f2d1ede120d9751851bd39b77dd1b6ca6a0aa821b413fe11b4fd`.
Root PCs 9-11 at `[68,80)` bind the method to `root/proto3`, which has
three fixed formal slots, no upvalues and a variadic tail. Its PCs 0-23 at
`[3262,3358)` and PC 302 at `[4470,4474)` establish the caption route.
PC 23 jumps directly to that zero-result return, skipping the other arms.
All PCs and decoded-payload offsets are zero-based and intervals are
half-open. The LPB and instruction decoders are `tools/retail_script.py`
and `tools/build_quest_contracts.py` at revision
`5507da1522e173f7fcad29d6b0bc7294b64b6ea5`.
Focused offline operand and tuple checks covered absent results, absent
varargs, nil positions and a tail beyond the printed temporaries. Twenty-five
decoded semantic mutations were rejected independently of the byte pins.

## Instance-raid guide and event methods

The following client contracts are pinned by their LPB and decoded payload
hashes. The canonical decoded-script paths and payload digests are recorded
in `manifests/retail_lua_coverage.json`; canonical Lua source hashes are in
`manifests/scripts.json`.

| Script | LPB path / SHA-256 | Decoded payload SHA-256 |
| --- | --- | --- |
| `chara/npc/populace/instanceraidguide/noquestguidebaseclass.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/wvtp5rq3p16589r57y9rr.le.lpb` / `7856f1aeaeccaddc9962404542d5aa934837b2817a4da3eb910303eb8a771487` | `b2a9c1df037d9cc8af191db06dfd262342407ceda92a092b883106a15c08e788` |
| `chara/npc/populace/instanceraidguide/instanceraidguideaurumvale.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p1659pspxo9y5.le.lpb` / `f86bad44fca4b253223a639f8806d57ca24582d819a8b20471a1c2be612de1f4` | `80e49a71894d6745e2ae5c63f522c7ac94925f6e0666606ab9a9b4e738c8e1c9` |
| `chara/npc/populace/instanceraidguide/instanceraidguidecutterscry.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p1657pqq5sr7sl.le.lpb` / `48f066b5a25749c1d0fc39ac0ad78c93b7d0b099ec73ddb8535dffb11b4b6f1a` | `5e9d5aeff9035c499d7f3f960ae666b97de40289ae5d7b171c46371eac281ee2` |
| `chara/npc/populace/occupancyguide/raidfst0dungeon03guide.lua` | `729s9/wu7/uvupy975/v77pu9w7l3p165/s9164rqj6pw35vwjg3p165.le.lpb` / `85314278a3c09261bd567826016723dfbaff2720ff42f4d8cf1d7191dd1b62ef` | `e1e6398cee8d2af33a8fb9d97ca6adf2acffc19ee6eccba345cadff779ca4a77` |
| `chara/npc/populace/occupancyguide/raidroc0dungeon01guide.lua` | `729s9/wu7/uvupy975/v77pu9w7l3p165/s916sv7j6pw35vwji3p165.le.lpb` / `6a647ecc1a4d925a1b72f29659a669d9aa61840d6b7c193aeb719f138d0ac50a` | `0646209eddf7d31d1c804da74ad1d11fe136e5e906b1fc2ec8c122057587581d` |
| `director/instanceraid/instanceraidlesserwhitegeneral.lua` | `61s57qvs/1wrq9w75s916/1wrq9w75s916y5rr5sn21q535w5s9y.le.lpb` / `f6e5631947f42562dcb6b865f45c9122c4e50bc002235c28a04846e174e272e7` | `5f5d1b3e8dfe776d208803166eed1b92c987817a43112a26d5ba50c7290433d4` |

`NoQuestGuideBaseClass.askExplainInstanceRaid` (prototype `0x17A`, zero-based
PCs 0-55) obtains its choices from `createExplainSelection_` and repeatedly
passes the selected value to `processExplainSelected_`. When the packed
return table has length zero, it finishes client talk and returns false.
After a selection, a false callback result continues the loop. A true result
finishes and returns true; nil finishes and returns false. The method
finishes client talk after the loop. This is a
client prompt flow; it does not prove a server launch or instance result.

`InstanceRaidGuideAurumVale.createExplainSelection_` says row 2 and returns
prompt row 3, choices 4-7, and three copies of its input argument
(prototype `0x214`, zero-based PCs 0-17). Its `processExplainSelected_`
(prototype `0x2CC`, zero-based PCs 0-99) returns false for choices 1 and 2, true for
choice 3 after self say row 22, and nil for choice 4 or other values.
Choice 1 says self rows 8-11. Choice 2 says self row 12, calls
world-master row 13 or 19 according to an argument comparison, then calls
world-master rows 18, 15, and 17 and self rows 14 and 16 before returning
false. These row IDs do not assign text meaning or server outcome.

`InstanceRaidGuideCuttersCry.createExplainSelection_` calls
`doSalute(3, 17)`, conditionally schedules `353959936` when that call returns
zero, waits 1, and calls `sayText_(2, 22)` before returning prompt row 3,
choices 4-7, and three copies of its input (prototype `0x230`, zero-based
PCs 0-28). Its `processExplainSelected_` (prototype `0x36E`, zero-based
PCs 0-90) makes
choice-specific say-text and world-master calls; choices 1 and 2 return
false, choice 3 calls `sayText_(19, 31)` and returns true, and choice 4 or
other values return nil. `sayText_` selects between its two row arguments
using `isUpperRank(3, 17)` (prototype `0x614`, zero-based PCs 0-17). The scheduler ID
and row values are client literals, not proven text or action semantics.

Both `RaidFst0Dungeon03Guide.askMainMenu` and
`RaidRoc0Dungeon01Guide.askMainMenu` (prototype `0x228`, zero-based PCs
0-129 in each
payload) first call `askExtendWidget` with leading arguments `(2, 4)`. When
that call returns 3, they call it again with leading arguments `(17, 2)`.
Each call also receives the method's final parameter. Both methods return the
first call's selected value. These literal arguments do not establish their
prompt or choice semantics, an instance launch, or a server result.

`InstanceRaidLesserWhiteGeneral.processCutSceneEvent` (prototype `0x1B6`,
zero-based PCs 0-23) calls `worldMaster:_getMyPlayer()`, fades out and waits for
fading, passes its weather argument to `_setWeather` with a second argument
of 0, calls `executeCutScene` with its two supplied arguments and `true`,
fades in, and waits 1. The inherited
[scene helper](#instance-raid-cutscene-helper) records its inner call contract.
This is call order in the client method; it does not establish a successful
scene or weather effect.

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
finalizing with `directNumber=0`. Original bytecode resolves their
`processUIUpdate` branches (`root/proto2`, instruction array at decoded
payload offset `0x47C`, zero-based PCs 0-37). When `directNumber` is 20,
PCs 4-7 request the director-specific effect above; when it is -1, PCs
12-15 request effect 20. Both branches jump directly to return at PC 37
(PCs 8 and 16), without starting or updating content information.
For every other direct number, the argument after `self` equal to `"time"`
selects `desktopWidget:processUpdateContentsInformation(self, "start")`
(PCs 18-25), regardless of `limitTime`. Other argument values select
`desktopWidget:processUpdateContentsInformation(self, "update", 1)` only
when `self.work.limitTime > 0` (PCs 26-36); otherwise the method returns
without a call. The jumps at PCs 9 and 17 are unreachable from entry,
so they do not create fall-through between effect and information branches.
These are static client call paths, not server encounter rules. Wrapper and
decoded payload identities are pinned by the three `resourcePath` rows in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).

`QuestDirectorNMRush01/02` synchronize `directNumber` and `limitTime`,
retain a local timer flag, and report kind 1 with maximum article index 0.
Their title rows are 51143 and 51144 respectively; both return instruction
row 51145. Their recovered bodies request content-information start for
direct numbers 1 or 2 when the timer flag is false and cancel for 3 or
finalization. The [NMRush guide and director contracts](nmrush-guide-director-contract.md)
establish both directors' exact update branches from their original bytecode.
The Director02 finding also owns its initialization, finalization and
two-result time getter; these UI branches do not select server encounter rules.

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

`RaidFst0Dungeon03.eventNoticeCutScene` and
`RaidRoc0Dungeon01.eventNoticeCutScene` each call `createCutScene` once,
retain its first result and use that same value for `startCutScene` and
`_delete`. Neither method tests the creator result before indexing it for
`startCutScene`; there is no encoded nil/false skip path. The original
instructions resolve the repeated creator expression in the recovered Lua.
They establish a single Lua creator invocation, without establishing how many
native allocations that invocation performs.

Both methods have five formal slots. Using `p1` through `p5` for those
slots, including the receiver, their common sequence is
`worldMaster:createCutScene(p3, p1)`, then
`result:startCutScene(1, 61, 1, 0, p4)`, `result:_delete()` and
`p2:_fadeIn(1)`. Each call after creation discards its results; the methods
return no values. The continuation assumes that the returned value supports
the indexed methods and that the opaque calls return normally.

The exact scene comparisons control the calls before and after that sequence:

| Director | Opening scene | Close scenes | Opening widget inputs |
| --- | --- | --- | --- |
| `RaidFst0Dungeon03` | `rad0f300` | `rad0f306`, `rad0f307`, `rad0f308` | `(2123, 1, p5)` |
| `RaidRoc0Dungeon01` | `rad0r100` | `rad0r106` | `(4102, 2, p5)` |

For its opening scene, each method skips `_fadeOut` and `_waitForFading`.
After the common sequence it calls
`desktopWidget:openRaidDungeonExecutionWidget` with the table's three inputs,
then `desktopWidget:processUpdateGeneralNotificationDialog(3, nil, nil, 1)`.
For every other scene, including nil, it calls `p2:_fadeOut(1)` first,
conditionally calls `desktopWidget:closeRaidDungeonExecutionWidget()` for
its listed close scenes, then calls `p2:_waitForFading()` before creation.
Those non-opening paths do not make the two opening widget calls.

Each original root's `GETGLOBAL`/`CLOSURE`/`SETTABLE` PCs 13-15 bind the exact
class and method name to `root/proto2`. Decoded-payload code intervals are
`[0x259,0x329)` for Fst, PCs 0-51, and `[0x259,0x319)` for Roc, PCs 0-47.
Creator/start/delete CALL PCs are 24/31/33 and 20/27/29 respectively.
The canonical Roc source SHA-256 is
`7511e87f9e017cc93a7ae7a1a32c8a6280516f876839bb39fc2296f592e54071`,
recorded in `manifests/scripts.json:8229-8233`. The corresponding original
LPB identities are in the table above and in
`manifests/retail_lua_coverage.json:5479-5506`; decoded-payload SHA-256 values
are `b64ca62a6ed4ee20ac42001e270c596f74044c9ef7f84beca18000b16be4938c`
and `27fc9ec035033acf5822bf0b8595ba7c7e5b3f2a0c35558e0e7bbeaa2fe50077`.

Both `relogin` methods request the corresponding widget open when their
fourth argument is false. Both `processUIFinalize` and `widgetSetOff` request
close. The Fst `relogin` method calls
`_fadeInNowLoadingForNoticeEventJustInArea`, as does
`CutScene.startCutScene` immediately before `_loadCutScene`. Those existing
source findings remain separate from the conditional original instruction
contracts above.
The director source is `director/occupancy/raidfst0dungeon03.lua:29-78,93-107`
(SHA-256 `A01AF800CC925D858191AAC416EBDA2CA79DAF52F1148DA45CAB1F2A552D6C4C`);
the common source is `gamedata/cutscene_common.lua:1064-1075,1316` (SHA-256
`F6DB9559B3F805D2738C073C7DB9DD102FD5C33A056E789FF2FB2F8AFF395BD1`). Both
are pinned in `manifests/scripts.json:8223-8226,9519-9522` and joined to
retail resources by `manifests/retail_lua_coverage.json:5480-5492,815-826`.

These are conditional client call sequences. Native allocation, successful
playback, visible fades or widget rendering, historical event invocation,
scene actor selection and server policy remain unobserved. No cited evidence
joins `rad0f300` to native spawn types 16 or 21; the separate dispatcher
branches establish capability
(`xivl-decomp:docs/actor/animation-bank-routing.md`).

The original-bytecode decoding tools are the same pinned LPB and Lua 5.1
decoders identified in the [instance helper](#instance-raid-cutscene-helper).

### Occupancy desktop wrappers

The original DesktopWidget wrappers refine these opening and close requests.
The connector's source and LPB identities are recorded in
[quest content-information directors](#quest-content-information-directors).
Its decoded payload SHA-256 is
`685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`
(`manifests/retail_lua_coverage.json:25443-25455`). Exact root
GETGLOBAL/CLOSURE/SETTABLE PCs 684-686 bind
`DesktopWidget.openRaidDungeonExecutionWidget` to `root/proto228`, and
PCs 687-689 bind `closeRaidDungeonExecutionWidget` to `root/proto229`.
Their decoded-payload code intervals are `[0x1badc,0x1bb00)` and
`[0x1bb66,0x1bb8a)`, respectively, with PCs 0-8 in each body.
The selected bodies contain 18 instruction words/72 bytes in total;
the exact root binding metadata contains six words/24 bytes.

Open has four formal slots including receiver `p1`. It calls
`p1:openWidgetYield(15, "RaidDungeonExecutionWidget", nil, nil, true, p3, p4)`.
The first non-receiver input `p2` is unused. Thus the two opening scenes above
forward 1 or 2 and their `p5` value to that boundary; the 2123/4102 input
does not reach it. Open CALL PC7 has B=9, C=1, so it passes eight arguments
including the receiver and discards all results.

Close calls `p1:closeWidget(15, nil)` at PC3, then separately looks up and calls
`p1:closeWidget(16, nil)` at PC7. Both CALLs have B=4, C=1 and discard all
results. If the first call returns nil or false normally, the second request
still follows. The second method lookup occurs after the first call.
If the first call raises an error or does not return, the second request is
not reached.

Neither wrapper contains a conditional gate, a widget-handle store, a local
state write or a result test. Both end with zero-result RETURN PC8, B=1.
Nil, false, true, opaque handles and multiple results from normally returning calls
are discarded without branching. The open call's true input is exactly a
Boolean; its meaning is not established here. These contracts assume callable
method lookups and normal opaque-call returns. They do not establish the
callees' admission rules, state changes, native factory, command completion,
widget rendering, server policy or historical invocation.

Focused offline instruction checks pin the tuples, arities, required Boolean
and nil inputs, unused input and separate close lookups. Argument, result,
return and method-name mutations are rejected. The
[callee contracts](#desktop-widget-admission-and-close) qualify admission,
arguments and returns. Reaching the widget's `init` remains unproved by these
wrapper bodies. The original LPB and instruction decoders are the tools
identified in the [instance helper](#instance-raid-cutscene-helper).

`RaidDungeonExecutionWidget.init` forwards its content and finish-time
arguments to `setContents` and `setTimer`. `setContents` uses text bank
10051 for `TextBlock_ContentsName`. `setTimer` writes
`finishTime - worldMaster:_getServerTime()` to timer-label
`FloatData.Value0`, with `FloatData.Value1 = 0`,
`FloatData.Value2 = 300`, `IntData.Value1 = 300`, and
`IntData.Value2 = 120`. Those are client widget inputs; the script does
not prove server timer authority, actual content duration, clear ownership,
exit cleanup, or reward policy.

The same [clock qualification](player-command-event-routes.md#clock-qualification)
applies to the clock operand. It does not bind the supplied finish-time
producer or its compatible clock domain.

### Desktop widget admission and close

The original `DesktopWidget.openWidgetYield` and `closeWidget` bodies are in
the same connector resource and decoded payload pinned in
[occupancy desktop wrappers](#occupancy-desktop-wrappers). Their canonical
source is `lua/scripts/widget/desktopwidget_connector.lua`, 660617 bytes,
SHA-256 `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`
(`manifests/scripts.json:15399-15402`). The selected source definitions are
lines 25912-25971 and 25300-25322, respectively. Original instructions establish
call and return arities. The canonical decompile truncates the displayed
extra-argument tail.

All PCs below are zero-based. Code intervals are half-open offsets in the
decoded payload. Each exact root binding is
`GETGLOBAL DesktopWidget`, `LOADK` of the named method, `CLOSURE`, `SETTABLE`.

| Method | Root binding PCs and interval | Selected body | Fixed slots and varargs |
| --- | --- | --- | --- |
| `openWidgetYield` | 1921-1924, `[0x1e24,0x1e34)` | `root/proto544`, PCs 0-50, `[0x330fd,0x331c9)`, 51 words/204 bytes | Six including receiver, vararg flag 3 |
| `closeWidget` | 1853-1856, `[0x1d14,0x1d24)` | `root/proto527`, PCs 0-16, `[0x32261,0x322a5)`, 17 words/68 bytes | Three including receiver, no varargs |

For open, call the fixed slots `p1` through `p6`, with `p1` the receiver.
Only `p5 == nil` calls `p1:isWidgetExec(p2)`. Only an exact first result true
returns one nil immediately. Otherwise that nil `p5` becomes `p1` locally.
Any supplied non-nil `p5`, including false, bypasses this precheck and remains
unchanged. The method then saves the first result of
`p1:getWidgetTypeByIndex(p2)`. Its saved lookup selector is `p3` when
`p4 == nil`, or `p4` otherwise, including false.

Each attempt calls `p1:openWidget(p2,p3,p4,p5,p6,...)` and keeps
only the first result. Original VARARG PC24 has B=0 and open CALL PC25 has
B=0, C=2, preserving the entire extra-argument tail, including nil positions.
Canonical lines 25942-25943 display one local for `...`; that displayed tail
is not the original argument contract.

Only an exact true open result calls `p1:waitWidgetCreateYield(p2)`, discards
its results, then calls `p1:getWidget(p2,saved-selector)`. Open returns exactly
the latter's first result, including nil or false. EQ PC36's two paths both
reach RETURN PC49, so a nil lookup result does not retry. Every other open
result reloads `p1.work.widgetEnableFlag[saved-type]`. Exact false ends with
one nil. Otherwise `p1:_wait(0.1)` precedes another attempt. Type and selector
remain saved, while work and the enable table are reloaded after each failed
attempt. Method lookups occur when their SELF instructions are reached.

The open body's EQ `(A,B,C)` operands are PC0 `(0,4,256)` for nil `p5`,
PC5 `(0,7,258)` for the precheck's true result, PC15 `(1,3,256)` for the
selector's nil test, PC26 `(0,10,258)` for open's true result, PC36
`(0,7,256)` for the final nil test, and PC42 `(0,10,265)` for the enable
flag's false test. RK256 is nil, RK258 is true and RK265 is false.
The retry JMP PC48 has sBx=-31 and targets PC18. The normal result returns
are PC8 and PC49, both A=7, B=2. PC50 is an unreachable empty terminator.

| Open call | PC | CALL A,B,C | Result handling |
| --- | ---: | --- | --- |
| `isWidgetExec(p2)` | 4 | `7,3,2` | First result |
| `getWidgetTypeByIndex(p2)` | 13 | `8,3,2` | First result, saved |
| `openWidget(p2,p3,p4,p5,p6,...)` | 25 | `10,0,2` | First result |
| `waitWidgetCreateYield(p2)` | 30 | `10,3,1` | Discarded |
| `getWidget(p2,saved-selector)` | 34 | `10,4,2` | First result, returned |
| `_wait(0.1)` | 47 | `10,3,1` | Discarded |

For the published raid wrapper, nil `p5` selects the precheck. After a
non-true result, the underlying call is
`p1:openWidget(15,"RaidDungeonExecutionWidget",nil,p1,true,p3,p4)`, where
the last two values are the wrapper's forwarded inputs. The saved lookup
selector is `"RaidDungeonExecutionWidget"`. This qualifies the literal true
input's position without assigning native creation or rendering semantics.

Close has a leading constant `nil == true` comparison, EQ PC0 A=0, B=256,
C=257. Its false-return block at PCs 2-3 is unreachable. It then calls
`p1:getWidget(p2,p3)` at PC7, A=3, B=4, C=2, retaining only the first result.
EQ PC8 A=0, B=3, C=256 tests equality with nil. A nil result returns exactly
one false at PC11, A=4, B=2. Every non-nil result, including false, reaches
`p1:closeWidgetDirect(result)` at TAILCALL PC14, A=4, B=3, C=0, followed by
open RETURN PC15, A=4, B=0. All normal callee results propagate, including
zero results, nil positions and multiple results. No fixed success value
is supplied by this path.

Neither selected body writes a receiver property, global or upvalue. The
calls remain opaque: they may mutate state, raise, suspend or fail to return.
Errors propagate without a local handler. The `_wait(0.1)` argument and
`waitWidgetCreateYield` call do not establish a measured delay or completion.
Close has no explicit wait or cleanup operation beyond its opaque helper.
The occupancy wrappers discard these callee results, so the composed path
does not establish native creation, destruction, widget initialization or
rendering, historical invocation, or server policy. The
[`openWidget` contract](#openwidget-inputs-and-results) qualifies the next
call. `waitWidgetCreateYield` and `getWidget` remain separate callee
boundaries. The [`closeWidgetDirect` contract](#closewidgetdirect-behavior)
qualifies its close request.

Focused original operand checks and static replays cover exact Boolean/nil
comparisons, complete varargs, saved and reloaded state, retries, result
arities and propagated errors. Ten open and eight close semantic mutations
are rejected. These checks use the LPB and instruction decoders identified
in the [instance helper](#instance-raid-cutscene-helper), without client
execution or interpretation of another helper body.

#### openWidget inputs and results

Original `DesktopWidget.openWidget` has six fixed formal slots, `p1` through
`p6`, including receiver `p1`, followed by varargs. It shares the connector
LPB, payload and canonical-source identities pinned above. The named source
and binding window is `widget/desktopwidget_connector.lua:25131-25183`.
Canonical lines 25173-25174 display a single extra-argument local; the
original preserves the complete tail.

Exact root PCs 1837-1840, `[0x1cd4,0x1ce4)`, bind `DesktopWidget.openWidget`
to `root/proto523`: GETGLOBAL R0,K0 (`DesktopWidget`), LOADK R1,K524
(`openWidget`), CLOSURE R2,child523, SETTABLE R0,R1,R2. The body is PCs 0-43,
`[0x31e52,0x31f02)`, 44 words/176 bytes, with vararg flag 3. PCs and
half-open decoded-payload offsets use the same conventions as above.

The first explicit opaque call is `p1:getWidgetTypeByIndex(p2)` at PC7,
A=8, B=3, C=2. Only its first result is saved. Exact nil returns one false.
Every non-nil type, including false, reaches a read of
`p1.work.widgetEnableFlag[saved-type]`. Only an exact false entry rejects
with false. This is a type-keyed read after the getter returns; no receiver
property is written.

Only nil `p5` causes a fresh lookup of `p1.work.rootWidget[p2]`. Any non-nil
root entry, including false, returns false. Every non-nil `p5`, including
false, bypasses that root check. This later work lookup is separate from
the earlier enable-table lookup. Its key is the original `p2`, while the
enable-table key is the saved type. This body does not normalize `p5`.

An admitted path resolves `openWidgetLocal` at SELF PC29 and calls
`p1:openWidgetLocal(p3,p4,p5,p2,p6,...)`. VARARG PC35 A=15, B=0 and CALL
PC36 A=8, B=0, C=2 forward the reordered fixed arguments and all extra
positions, including interior and trailing nils, then keep only the first
result. Exact false becomes one false result. Every other normal first
result becomes one true, including nil, zero or an opaque handle. Zero
callee results are adjusted to nil and also produce true. Additional results
are discarded. This Boolean does not validate a widget or prove creation.

| Test | EQ PC | A,B,C | Effect |
| --- | ---: | --- | --- |
| Literal nil versus true | 0 | `0,256,257` | False-return block at PCs 2-3 is unreachable |
| Saved type versus nil | 9 | `0,7,256` | Nil returns false at PC12 |
| Enable entry versus false | 16 | `0,8,261` | False returns false at PC19 |
| `p5` versus nil | 20 | `0,4,256` | Only nil reads rootWidget |
| Root entry versus nil | 25 | `1,8,256` | Non-nil returns false at PC28 |
| Local call result versus false | 37 | `0,8,261` | False returns false at PC40; otherwise true at PC42 |

RK256 is nil, RK257 is true and RK261 is false. Every reachable normal
RETURN at PCs 12, 19, 28, 40 and 42 has A=8, B=2: exactly one Boolean.
PC43's empty RETURN is unreachable. The body has no loop, explicit wait,
state store or local error handler. Lookups, indexing and calls can raise
or invoke opaque behavior; suspension or nonreturn prevents later work.

In the published occupancy composition, `openWidgetYield` has already
replaced its nil `p5` with the receiver. This body's rootWidget check is
therefore bypassed. If its own type and enable checks permit the request,
the tuple is
`p1:openWidgetLocal("RaidDungeonExecutionWidget",nil,p1,15,true,p3,p4)`,
where the last two inputs came from the occupancy wrapper. This body's type
lookup is distinct from the outer method's earlier lookup; equality of their
first results is not established. The resulting Boolean feeds the outer
exact-true test, without proving completion or a valid widget result.

`getWidgetTypeByIndex` remains opaque. The
[`openWidgetLocal` contract](#openwidgetlocal-creation-request) qualifies the
later call. These property names and forwarded values do not identify an
actual native control or table, or establish initialization, rendering,
lifetime, historical invocation or server policy.

Focused original operand checks and 33 static replay cases verify the
admission comparisons, separate state reads, fixed-argument order, full
varargs, Boolean result normalization and propagated errors. Sixteen semantic
mutations are rejected. The checks use the existing LPB and instruction
decoders at revision `9b4ed5282b403b0fbd1c1fdd3d6a64ecee75ad52`; they do
not execute the client or interpret another body.

#### openWidgetLocal creation request

Original `DesktopWidget.openWidgetLocal` has six fixed slots, `p1` through
`p6`, including receiver `p1`, plus varargs. Its connector LPB, payload and
canonical-source identities are pinned above. Only the named source and
binding window `widget/desktopwidget_connector.lua:25076-25130` supports
this contract. Canonical lines 25114-25115 display one extra-argument local;
the original forwards the complete tail.

Exact root PCs 1833-1836, `[0x1cc4,0x1cd4)`, bind the name to `root/proto522`:
GETGLOBAL R0,K0 (`DesktopWidget`), LOADK R1,K523 (`openWidgetLocal`), CLOSURE
R2,child522, SETTABLE R0,R1,R2. The body is PCs 0-45, `[0x31d12,0x31dca)`,
46 words/184 bytes, with vararg flag 3. PCs are zero-based; byte intervals
are half-open decoded-payload offsets.

Only nil `p3` defaults to `p2`. A local saved input value starts as Boolean
true. Only nil `p4` defaults to `p1`, bypassing the snapshot below. Supplied
non-nil values, including false, are preserved. When supplied `p4` compares
unequal to `p1`, the body calls `p4:isShow()`. Only an exact true first result
calls `p4:getInputEnable()`, saving its first result without normalization.
Otherwise the saved input value stays true. Equality here is the Lua
comparison; it does not establish distinct native object identities.

Every path then calls `p4:_isAlive()`. Only exact false rejects, returning
one false. Every other normal first result, including nil and zero results
adjusted to nil, continues. An admitted path freshly resolves and calls
`p1:commandCreateWidget(p2,false,p4,saved-input-value,p3,p5,p6,...)`.
The false is literal. VARARG PC31 A=17, B=0 and CALL PC32 A=8, B=0, C=2
preserve all extra positions, including trailing nils, then keep only the
first result. No native allocation or initialization follows from this call
name or its normally returned value alone.

Only an exact true creation result and `p4` comparing unequal to `p1`
reach a fresh `p4:isShow()` lookup and call. Only an exact true first result
then requests `p4:setInputEnable(false)`, discarding all setter results.
The two show lookups/results are separate; the earlier saved input value is
not refreshed before creation. The local values and references survive the
opaque calls without freezing their referenced objects.

| Call | SELF/CALL PCs | CALL A,B,C | Result handling |
| --- | --- | --- | --- |
| `p4:isShow()` | 10/11 | `8,2,2` | First result |
| `p4:getInputEnable()` | 14/15 | `8,2,2` | First result saved |
| `p4:_isAlive()` | 17/18 | `8,2,2` | First result |
| `p1:commandCreateWidget(...)` | 23/32 | `8,0,2` | Full tuple, first result saved |
| `p4:isShow()` | 37/38 | `9,2,2` | Fresh lookup, first result |
| `p4:setInputEnable(false)` | 41/43 | `9,3,1` | All results discarded |

EQ `(A,B,C)` operands are PC0 `(0,2,256)` for nil `p3`, PC4 `(0,3,256)`
for nil `p4`, PC8 `(1,3,0)` for `p4`/`p1` equality, PC12 `(0,8,258)`
for the first show result, PC19 `(0,8,261)` for liveness, PC33 `(0,8,258)`
for creation, PC35 `(1,3,0)` for the later equality test and PC39
`(0,9,258)` for the later show result. RK256 is nil, RK258 is true and
RK261 is false. RETURN PC22 and PC44 both have A=8, B=2: one false on
liveness rejection, or the saved first creation result otherwise. Zero
creation results become one nil; extra results are discarded. Normal
setter results cannot replace the saved result. PC45's empty RETURN is
unreachable.

The first explicit opaque call is conditional `p4:isShow()` at PC11; the
nil-defaulted or receiver-equal path first calls `_isAlive` at PC18. The body
has no property/global/upvalue store, loop, explicit wait or local handler.
The setter is an opaque request, not proof of an input-state change. Errors
propagate. A reached call that suspends or does not return prevents later
work; this includes post-creation calls before the saved result is returned.

The published occupancy tuple supplies `p3=nil` and `p4=p1`. It therefore
defaults `p3` to `"RaidDungeonExecutionWidget"`, keeps the saved input value
true, and first calls `p1:_isAlive()`. A non-false first result requests
`p1:commandCreateWidget("RaidDungeonExecutionWidget",false,p1,true,"RaidDungeonExecutionWidget",15,true,wrapper-p3,wrapper-p4)`.
It reaches neither show query nor the setter. Its first creation result then
meets `openWidget`'s separate normalization: exact false becomes false and
every other normal result becomes true. The outer and inner type lookups
remain distinct. These calls do not bind an actual native control/table or
prove creation, completion, rendering, lifetime, historical invocation or
server policy. The [conditional `_isAlive` profiles](#conditional-_isalive-lookups)
qualify possible results without selecting this receiver's actual surface. The
[`commandCreateWidget` contract](#commandcreatewidget-forwarding) qualifies
its request forwarding.

Focused original operand checks, 52 static replays and 28 rejected semantic
mutations verify defaults, comparisons, exact request arguments, full varargs,
saved values, fresh post-call lookups and result/error boundaries. The LPB
and instruction decoders at revision `3ad61ba2b38887b04f504b8b4561ea2eb9062a7f`
were used without client execution or interpretation of a dependency body.

#### commandCreateWidget forwarding

Original `DesktopWidget.commandCreateWidget` has three fixed slots, `p1`
through `p3`, including its unused receiver `p1`, plus varargs. Its canonical
source is `widget/desktopwidget.lua`, 7929 bytes, SHA-256
`5d3bfabf2e8a55ee2e64f607bdada5f04046c9528e9e9aca858e9ad9e232070a`
(`manifests/scripts.json:15393-15396`). The selected definition/binding window
is lines 117-141. Canonical lines 137-138 display a single local from the
variadic tail; the original forwards the complete tail.

Its original resource is `client/script/n1635q/65rzqvun1635q.le.lpb`,
4029 bytes, SHA-256
`be7b0959ba530027991b22308b1d6a84ce5db311bdb727f987678b5dbf810e51`.
The 4016-byte decoded payload has SHA-256
`92af6d4fe068c49efcb7f4b1df869e4b5846a86217915bb6cb798fe24c58d14e`
(`manifests/retail_lua_coverage.json:25413-25425`). Root PCs 24-26,
`[0x80,0x8c)`, bind DesktopWidget/name to `root/proto4` through GETGLOBAL
R0,K5, CLOSURE R1,child4, SETTABLE R0,K10,R1. K5 is `DesktopWidget` and
K10 is `commandCreateWidget`. The body is PCs 0-15, `[0x696,0x6d6)`,
16 words/64 bytes, with vararg flag 3. PCs are zero-based; byte intervals
are half-open decoded-payload offsets.

The first global `worldMaster` lookup supplies `w1`. Its separately resolved
`_getMyPlayer` call contributes first result `q1`. SELF PC3 saves both
`q1.commandAboutWidget` as function `F` and `q1` as its receiver before the
later calls. A fresh global lookup supplies `w2`; its `_getMyPlayer` call
contributes first result `q2`. The body then calls
`q2:getSystemCommand(24228)`, retaining only first result `c`.

The separate global loads and first player results are not proved equal.
The final call uses the function and receiver held in registers before the
later lookups; it does not resolve `commandAboutWidget` again. Those saved
references do not freeze their referenced objects.

| Operation | PC | A,B,C | Handling |
| --- | ---: | --- | --- |
| First `_getMyPlayer()` CALL | 2 | `4,2,2` | First result `q1` |
| Second `_getMyPlayer()` CALL | 6 | `6,2,2` | First result `q2` |
| `getSystemCommand(24228)` CALL | 9 | `6,3,2` | First result `c` |
| VARARG | 12 | `9,0,0` | Complete extra tail |
| Saved `commandAboutWidget` TAILCALL | 13 | `4,0,0` | All normal results forwarded |
| Open RETURN trailer | 14 | `4,0,0` | Tail results |

The exact final tuple is `F(q1,c,p3,p2,...)`, with all extra positions,
including trailing nils. Neither fixed inputs nor `c` are normalized or
checked. Each earlier CALL keeps one result: zero results become nil and
additional results are discarded. A nil command result is passed as nil.
The tail call propagates every normal result, including zero results and nil
positions; PC15's empty terminator has no independent normal path.

For the published occupancy request, the saved function receives
`(q1,c,false,"RaidDungeonExecutionWidget",receiver,true,"RaidDungeonExecutionWidget",15,true,wrapper-p3,wrapper-p4)`.
The original DesktopWidget receiver survives only in that tail position;
its relationship to either player result is unproved. The immediate caller's
separate first-result adjustment and outer Boolean normalization remain as
documented above.

The first explicit opaque call is `_getMyPlayer` at PC2. The body has no
conditional branch, local admission/type/default test, store, loop, wait or
error handler. Reached lookup/call errors propagate; suspension or nonreturn
prevents later work. The literal 24228 is the low ID in the existing
[WidgetOpenCommand finding](widget-open-command-boundary.md). This selector
does not establish the class of returned `c`, its dispatch by the saved
function, an actual native receiver/address, or historical execution.

Focused original operand checks, 44 static paths and 14 rejected semantic
mutations verify separate lookups, saved-method timing, exact request tuple,
full varargs/results and error boundaries. The LPB and instruction decoders
at revision `37114264126f9e342f78754c028ab78cc491c3ee` were used without
client execution or interpretation of a dependency body.

#### closeWidgetDirect behavior

Original `DesktopWidget.closeWidgetDirect` has two fixed slots, receiver `p1`
and widget argument `p2`, with no varargs. Its connector LPB, payload and
canonical-source identities are pinned above. Its selected definition and
binding window is `widget/desktopwidget_connector.lua:25322-25350`.
Exact root PCs 1857-1860, `[0x1d24,0x1d34)`, use GETGLOBAL
R0,K0 (`DesktopWidget`), LOADK R1,K529 (`closeWidgetDirect`), CLOSURE
R2,child528, SETTABLE R0,R1,R2. The selected body is `root/proto528`,
PCs 0-19, `[0x322f6,0x32346)`, 20 words/80 bytes. PCs are zero-based and
byte intervals are half-open decoded-payload offsets.

The literal nil-versus-true comparison at EQ PC0 A=0, B=256, C=257 makes
the false-return block at PCs 2-3 unreachable. EQ PC4 A=0, B=1, C=256
tests `p2 == nil`; nil returns exactly one false at PC7. Every non-nil
value, including false, reaches the `_isAlive` member lookup. False is not
rejected as nil: ordinary Boolean indexing without an applicable metatable
can raise there, and the selected body has no handler.

SELF PC8 A=2, B=1, C=258 resolves `p2._isAlive`. CALL PC9 A=2, B=2, C=2
calls it with only receiver `p2` and retains the first result. EQ PC10
A=0, B=2, C=259 rejects only exact false, returning one false at PC13.
Every other normal first result, including nil, zero or zero results padded
to nil, proceeds. The method name does not validate liveness.

Only then does SELF PC14 A=2, B=0, C=260 resolve `p1.closeWidgetLocal`.
PC15 copies the unchanged `p2`; CALL PC16 A=2, B=3, C=1 requests
`p1:closeWidgetLocal(p2)` and discards all results, including false or nil.
The [callee contract](#closewidgetlocal-cleanup-request) qualifies that request.
After normal return, LOADBOOL PC17 supplies true and RETURN PC18 returns it.
Normal RETURNs at PCs 7, 13 and 18 have A=2, B=2: one Boolean. PC19's
empty RETURN is unreachable. Extra actual arguments have no forwarding path.

The first `_isAlive` request is at PC9 for non-nil input. Its
[published lookup profiles](#conditional-_isalive-lookups) require their actual
dispatch and frame premises.
Its effects may change the later `closeWidgetLocal` lookup, which is not saved
before that call. Neither argument register is replaced. The body has no
persistent store, state-flag lookup, loop, explicit wait or error handler.
Lookup/call errors propagate; suspension or nonreturn prevents later work.
Returning true after the opaque close request proves no cleanup, native close
effect, destruction, rendering, lifetime completion or invalidation of `p2`.
This dynamic `_isAlive` receiver has no exact native implementation/control
binding established by the selected body or the token's catalog membership.

The published `closeWidget` caller rejects a nil first `getWidget` result,
then tail-forwards `closeWidgetDirect` results. Under this callee contract,
its non-nil path now has one Boolean normal result or a propagated lookup/
call boundary. A false lookup result reaches the `_isAlive` member lookup;
it does not become a normal false return solely because it is false.
The occupancy wrapper still discards results and reaches its separate slot-16
request only after the slot-15 request returns normally. A normal false result
does not itself stop that sequence.

Focused original operand checks, typed static replays, caller composition
checks and 16 rejected semantic mutations verify admission, first-result
handling, late lookup, discarded close results and one-Boolean returns. The
LPB and instruction decoders at revision
`37114264126f9e342f78754c028ab78cc491c3ee` were used without client execution,
native-body inspection or interpretation of either dependency body.

#### closeWidgetLocal cleanup request

Original `DesktopWidget.closeWidgetLocal` has two fixed slots, receiver `p1`
and widget argument `p2`, with no varargs. Its connector LPB, payload and
canonical-source identities are pinned above. The selected definition and
binding window is `widget/desktopwidget_connector.lua:25270-25296`, using
an anonymous-register function assignment. Exact root PCs 1849-1852,
`[0x1d04,0x1d14)`, use GETGLOBAL R0,K0 (`DesktopWidget`), LOADK R1,K527
(`closeWidgetLocal`), CLOSURE R2,child526, SETTABLE R0,R1,R2. The body is
`root/proto526`, PCs 0-15, `[0x3219d,0x321dd)`, 16 words/64 bytes.
PCs are zero-based and byte intervals are half-open decoded-payload offsets.

The first explicit opaque request is `p1:closeWidgetRecursive(p2)` at
SELF PC0 / CALL PC2. The argument is forwarded unchanged, without a local
nil/false test or argument indexing. Missing `p2` becomes nil; extra actual
arguments are not forwarded. Only the first recursive result is kept.
Only exact true reaches `p1:getThreadOwnerWidget()`. Every other normal
first result, including zero results adjusted to nil, skips owner cleanup.
The [recursive callee](#closewidgetrecursive-traversal-and-owner-result)
qualifies the traversal requests and meaning of that Boolean.

The getter is called on the original receiver, with no explicit argument.
Only its first result is saved. Nil skips the later requests. Every non-nil
result, including false, reaches `p1:setThreadOwnerWidget(nil)`, then
`savedOwner:close()`. The setter receives an explicit nil, and both later
calls discard all results. The getter is not repeated. The owner value stays
saved across the setter, while its `close` method is looked up only after
the setter returns. The same saved value is used as the close receiver even
if the setter changes other state; that late lookup can observe method changes.

| Call | SELF/CALL PCs | CALL A,B,C | Handling |
| --- | --- | --- | --- |
| `p1:closeWidgetRecursive(p2)` | 0/2 | `2,3,2` | First result |
| `p1:getThreadOwnerWidget()` | 5/6 | `3,2,2` | First result saved |
| `p1:setThreadOwnerWidget(nil)` | 9/11 | `4,3,1` | Explicit nil; all results discarded |
| `savedOwner:close()` | 12/13 | `4,2,1` | Late lookup; all results discarded |

EQ PC3 A=0, B=2, C=257 tests the recursive result against true. JMP PC4
has sBx=10 and targets the final return on non-true results. EQ PC7 A=1,
B=3, C=259 tests the owner against nil; JMP PC8 sBx=6 skips cleanup for nil.
RK257 is true and RK259 is nil. LOADNIL PC10 A=6, B=6 supplies the setter's
nil argument. Every normal path reaches RETURN PC15 A=0, B=1, C=0:
exactly zero values, with no recursive or owner-call result propagated.

The body has no direct property/global/upvalue store, loop, wait, handler or
rollback. Its close request remains opaque. The
[nominal thread-owner contract](#nominal-thread-owner-access) qualifies the
getter and setter when their dynamic lookups resolve to those methods. A false
owner passes the nil gate and reaches the setter before ordinary Boolean `close`
indexing can fail; special metatable behavior is unproved. Reached errors,
suspension or nonreturn prevent later requests and normal return. The saved
owner's identity, actual state mutation, destruction, native control/table/address
and lifetime completion are not established by this body.
No declared native receiver/argument chain is attributable from this body.

The published `closeWidgetDirect` caller discards these zero results and
returns true after normal return. It therefore also returns true when a
non-true recursive result or nil owner skips the cleanup branch. An error or
nonreturn here still prevents that caller return. This Boolean does not
report recursive-cleanup success or prove any close effect.

Focused original operand checks, seven semantic replay checks and 12 detected
semantic mutations verify exact gates, original argument forwarding, saved
owner/late lookup, explicit nil, discarded results and zero-result returns.
The LPB and instruction decoders at revision
`ae6a576e03412483f4efc4733e07cf4bb06545dd` were used without client
execution or interpretation of a dependency body.

#### Nominal thread-owner access

If dispatch reaches `DesktopWidget.getThreadOwnerWidget`, its one fixed
receiver supplies `W=receiver.work` at GETTABLE PC0, then
`O=W.threadOwnerWidget` at GETTABLE PC1. RETURN PC2, `A=1,B=2,C=0`, returns
exactly one unchanged O, including nil or false. The trailing zero-value
RETURN PC3 is unreachable. There is no default, truth conversion or validity
filter. Missing receiver is adjusted to nil; extra arguments are unused.

`DesktopWidget.setThreadOwnerWidget` has two fixed slots, receiver and value.
GETTABLE PC0 saves `W=receiver.work` in R2. SETTABLE PC1,
`A=2,B=257,C=1`, assigns `W.threadOwnerWidget=value`. RETURN PC2,
`A=0,B=1,C=0`, returns exactly zero values. Explicit nil reaches that assignment
unchanged; a missing value is adjusted to nil. Extra arguments are unused.

Each invocation looks up `work` once and uses its saved result. Getter and
setter invocations perform separate lookups, so their W values need not be
identical. These are ordinary Lua indexing and assignment operations, with
applicable metamethod and error behavior. Under ordinary table storage, nil
removes the `threadOwnerWidget` entry. There is no rawset, work creation,
validation, readback or success flag. Normal setter return does not prove a
particular effect through an unverified `__newindex` implementation.

Both prototypes have no varargs, upvalues or children, and no explicit
CALL/TAILCALL, branch, loop, protected call, handler or yield/wait operation.
The getter has no persistent store. The setter makes no close request for the
owner or native request. Applicable indirect effects, actual receiver and storage
binding, shared work aliases and owner identity remain unproved.

For [close-local cleanup](#closewidgetlocal-cleanup-request), nominal dispatch
makes the saved getter result exactly O from that invocation. The explicit-nil
setter has its own work lookup, and its zero results are discarded. The caller
retains its saved O and looks up O's `close` only after normal setter return.
For the [recursive caller](#closewidgetrecursive-traversal-and-owner-result),
the exact-false `_isAlive` result still selects the explicit-nil setter;
the subsequent local owner=nil action is separate from the field assignment.
Neither composition proves equality of the work objects, complete reference
release, cleanup, destruction or lifetime completion.

The connector LPB, decoded-payload and canonical-source identities above apply.
Canonical definitions and assignments are in `widget/desktopwidget_connector.lua`:

| Method | Class line | Complete body lines | Assignment line |
| --- | ---: | --- | ---: |
| `getThreadOwnerWidget` | 1142 | 1144-1149 | 1151 |
| `setThreadOwnerWidget` | 1133 | 1135-1139 | 1141 |

Each root binding uses GETGLOBAL R0,K0 (`DesktopWidget`), CLOSURE R1 and
SETTABLE R0,RK(method),R1. Root K22 binds child21 as the getter; K21 binds
child20 as the setter. Both body constant pools are K0=`work`,
K1=`threadOwnerWidget`. PCs are zero-based; payload ranges are half-open.

| Selected code | PCs | Payload interval | SHA-256 |
| --- | --- | --- | --- |
| Getter `root/proto21` body | [0,4) | [33094,33110) | `2e677feeb3fc915f3591651020158cbbddae6a8d99189e7cc084f667c0e6ace2` |
| Getter root binding | [63,66) | [284,296) | `f7f4573df317a759fa5a34769d445a88e3ae88947e0f1fe228a76ca4bfa5ca0a` |
| Setter `root/proto20` body | [0,3) | [33009,33021) | `d13a916208b98b2aa3d9b56cd9f9cc1bea3b921bcc20e8b813e7976a61f8f34a` |
| Setter root binding | [60,63) | [272,284) | `fe61de99e82ae897d89ae8bacf174d6f1fdce9434556511f61475afe82d2217d` |

The original bytecode and complete canonical bodies agree. The existing
[LPB decoder](../tools/retail_script.py) and
[Lua instruction decoder](../tools/build_quest_contracts.py) cover all seven
body words and six binding words without client execution.

#### Conditional _isAlive lookups

The published [script profiles](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/binding-map-native-contract.md#script-surfaces)
and [userdata query](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/player-world-native-contract.md#_isalive)
distinguish conditional results, rather than one universal native function:

| Reached lookup/call profile | Normal result |
| --- | --- |
| Class lookup reaches nominal `ActorBaseClass._isAlive` | true |
| Released-instance `__index` reaches the published global `__lge_isAlive` function | false |
| `IndividualRef` userdata reaches the documented engine-query closure/frame | Lua Boolean converted from the returned engine byte |

The [instance lookup contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/widget-work-members.md#instance-__index)
qualifies the released, hidden-cache and class/parent lookup paths. The
released-reference role of record `+0x7E` remains `INFERRED`. Actual receiver,
metatable/class chain, dynamic/global lookup, cast, call frame and engine-byte
conditions are not established here. The documented derived bare-`RET 8`
query path can produce true without proving object validity; its balanced
`IndividualRef` frame does not establish the distinct script-instance frame.

The query is reached through `openWidget` and `openWidgetLocal` in the nominal
`openWidgetYield` chain. Exact false rejects the local creation request;
the outer retry/wait/result logic retains its separate conditions. In
`closeWidgetDirect`, exact false rejects delegation to `closeWidgetLocal`.
In the recursive owner branch, exact false requests the nil setter and only
after normal setter return clears the saved local owner. Other dynamic results
keep the existing exact-false handling: nil, numeric zero and zero return values
adjusted to nil take the non-false path. That path proves no object validity.

These profiles select no actual `p4`, `p2` or saved-owner surface. They prove
no HP, death, server phase, creation, cleanup, destruction or lifetime result.
The nominal owner setter's separate work lookup, assignment/metamethod limits
and the close-local saved owner's later `close` lookup remain qualified above.

#### closeWidgetRecursive traversal and owner result

Original `DesktopWidget.closeWidgetRecursive` has two fixed slots, receiver
`p1` and input `p2`, with no varargs. The connector identities are pinned
above. Its canonical definition/binding window is
`widget/desktopwidget_connector.lua:25204-25269`. Root PCs 1845-1848,
`[0x1cf4,0x1d04)`, bind the exact name to child525 using GETGLOBAL
`DesktopWidget`, LOADK `closeWidgetRecursive`, CLOSURE and SETTABLE.
The complete `root/proto525` body is PCs 0-53, `[0x31ffb,0x320d3)`,
54 words/216 bytes. PCs are zero-based and payload ranges are half-open.

Only nil is rejected before any input or receiver lookup: it returns one
false at PC3. Missing input becomes nil; extra actual arguments are not
forwarded. False passes the nil gate and can fail ordinary method indexing;
special metatable behavior is unproved.

The first opaque request is `p2:_countChildWidgets()` at SELF4/CALL5.
Only its first result is saved. A fresh table receives the first result of
`p2:_getChildWidget(i)` for each numeric-loop index starting at 1, stepping
by 1, with the saved count as limit. This complete snapshot loop precedes
the recursive-request loop. Both loops reuse R5-R8 and reload their limit
from the retained R2 count result. An unusable numeric limit can error. A
zero-iteration count skips both loops and still reaches the owner decision.

For the nominal `WidgetBase` binding,
`xivl-client-structs:docs/talk-native-contract.md#parent-and-child-widgets`
and `xivl-client-structs:manifests/talk_native_call_contract.json`,
row `luaName=_countChildWidgets`, record a child-vector count read and an
`int` push. Applying that contract here requires SELF4 to resolve to the
registered descriptor/functor, a successful holder cast and a receiver
identity that resolves valid widget storage. Those conditions are unproved
for this `p2`, so its count remains the parameterized first result above.

`WidgetBaseClass._countChildWidgets_inl` is an executable descriptor closure
with one unused fixed argument and no varargs. It returns exactly two literal
strings in order, `"self"` and `"_countChildWidgets_cpp"`, without invoking a
native or counting widgets. Literal `self` is a string, not the receiver value.
The pair is distinct from the native `int` and this caller's count result.

Its canonical window is `widget/widgetbaseclass_u.lua:132-141`: class lookup
at 132, complete body at 134-139 and assignment at 141. Root PCs 39-41,
payload `[188,200)`, load `WidgetBaseClass`, create child13's closure and
assign it under `_countChildWidgets_inl`. The descriptor `root/proto13` has
PCs 0-3, payload `[2203,2219)`, four words/16 bytes. RETURN PC2 supplies both
strings; the zero-value RETURN PC3 is unreachable. PCs are zero-based and
payload byte ranges are half-open.

| Descriptor artifact | Size | SHA-256 |
| --- | --- | --- |
| `client/script/n1635q/n1635q89r57y9rr_p.le.lpb` | 3,210 bytes | `47325df731d3e0a9b6775dbfce8c5364d6dc1631f0518fbfc30e0c46a05a3757` |
| Decoded payload | 3,197 bytes | `e480408e273057f08bfe7854adca77ded50dfb53f806527caf01db38997f44f5` |
| Canonical `widget/widgetbaseclass_u.lua` | 4,394 bytes / 241 lines | `28385e6036059caa033670efde0eb9b3d162ab6fcee95503a353a8cd2943556b` |

`xivl-client-structs:docs/lua-class-system.md#pipeline-diagram` records
conditional `_inl` target/key lookup. This closure supplies its specific
literal outputs, but does not establish resolution of `self`, successful
`_countChildWidgets_cpp` lookup or alias installation. The actual `p2`
dispatch, holder cast and identity/storage requirements above remain unproved.

The second loop reads each saved child value and requests
`p1:closeWidgetRecursive(savedChild)` in the same numeric-loop order. A nil
child lookup result is later read and forwarded as nil. Only an exact-true
first recursive result sets a sticky local Boolean true. The Boolean starts
false and never resets; other results, including zero results adjusted to
nil, leave it unchanged. There is no early exit on either Boolean result.

Each child getter is looked up on `p2` for its iteration, and the recursive
method is looked up on `p1` for each saved child. If the recursive dispatches
resolve to this selected body, one child's complete recursive call precedes
the next sibling, and the current input's owner/close decision follows all
child calls. This establishes conditional depth-first request ordering.
The body has no visited set or explicit cycle guard. It does not establish
actual child identity, a stable runtime hierarchy or recursive destruction.

After child calls, `p1:getThreadOwnerWidget()` supplies one saved first result.
Nil skips the liveness request. Every non-nil value, including false, reaches
`savedOwner:_isAlive()`. Only exact false as its first result requests
`p1:setThreadOwnerWidget(nil)`, discarding all setter results. After that
setter returns normally, the saved local owner becomes nil. Nil, zero
results adjusted to nil and every other non-false liveness result retain the
saved owner. The owner getter is not repeated. The
[published `_isAlive` profiles](#conditional-_isalive-lookups) qualify possible
lookup results; this saved owner's actual surface and liveness remain unproved.

The [nominal owner methods](#nominal-thread-owner-access) supply the getter and
setter contracts only when those dynamic lookups resolve to them.

A retained non-nil owner that compares equal to the original input by Lua
`==` sets the Boolean true and suppresses this input's close. Applicable
equality metatable behavior and raw owner identity remain unproved. Every
other path that reaches the final decision requests `p2:close()` after the
child calls and owner decision, discarding all close results. Child results
do not themselves suppress that close. An exact-false liveness result followed by a normal
setter clears the saved owner and cannot itself suppress it.

The [nominal close contract](#nominal-widgetbaseclassclose-requests)
applies only if this dynamic `p2:close()` lookup resolves to that method.

| Request | SELF/CALL PCs | CALL A,B,C | Handling |
| --- | --- | --- | --- |
| `p2:_countChildWidgets()` | 4/5 | `2,2,2` | First result supplies both loop limits |
| `p2:_getChildWidget(i)` | 12/14 | `9,3,2` | First result saved in snapshot |
| `p1:closeWidgetRecursive(savedChild)` | 22/24 | `10,3,2` | Exact-true first result sets sticky Boolean |
| `p1:getThreadOwnerWidget()` | 29/30 | `5,2,2` | First result saved once |
| `savedOwner:_isAlive()` | 33/34 | `6,2,2` | Only exact false requests normalization |
| `p1:setThreadOwnerWidget(nil)` | 37/39 | `6,3,1` | Explicit nil; all results discarded |
| `p2:close()` | 50/51 | `7,2,1` | All results discarded |

Every reachable normal return is one Boolean: PC3 returns false for nil,
and PC52 returns the sticky flag. The zero-value fallback RETURN PC53 is
unreachable. For non-nil input whose operations finish normally, true means
an exact-true recursive first result or a retained non-nil owner equality
match. Otherwise the result is false, regardless of the close result.
There is no explicit wait, yield request, protected call, handler or rollback.
Reached errors propagate; supported suspension or nonreturn prevents later
requests and normal return until continuation completes. Native effects,
owner mutation effectiveness, lifetime and cleanup completion remain unproved.

The published `closeWidgetLocal` exact-true gate therefore observes this
Boolean, not a close result. Nil input normally skips its owner cleanup.
A non-nil input can return false after its close request, or return true
from a child result while still requesting its own close. An owner match
returns true while suppressing the current input close. On true, the caller
performs its own fresh owner getter; that value is not proved identical to
any owner saved by a recursive invocation. Its nil gate, explicit-nil setter,
late saved-owner close lookup and zero-value normal return remain as above.
`closeWidgetDirect` still returns true after normal local return, including
when a false recursive result skipped the local owner-cleanup branch.

Focused authenticated operand and control-flow checks cover all 54 body
words, four binding words and canonical body lines 25207-25267. The existing
LPB and instruction decoders were used without client execution or
interpretation of another function body. The next opaque dependency is the
input's `_countChildWidgets` request; no native receiver chain is established.

#### Nominal WidgetBaseClass.close requests

If the reached recursive-close `p2:close()` dispatch resolves to this nominal
`WidgetBaseClass.close` method, it makes these requests in order:

| Request | SELF/CALL PCs | CALL A,B,C | Results |
| --- | --- | --- | --- |
| `receiver:setInputEnable(false)` | 0/2 | `1,3,1` | All discarded |
| `receiver:processClosing()` | 3/4 | `1,2,1` | All discarded |
| `receiver:_delete()` | 5/6 | `1,2,1` | All discarded |

All three lookups use the unchanged receiver. Each later lookup follows
the preceding normal call return. Earlier requests can affect later lookups.
The method has one fixed receiver and no varargs, guard, default or normalization.
Missing receiver becomes nil; extra arguments are not forwarded. False, nil
and zero-result call returns are discarded and provide no success gate.
The sole RETURN PC7 returns exactly zero values after all calls return normally.
The recursive caller discards these results and keeps its earlier Boolean
and owner-decision result handling.

The body has no direct persistent write, branch, loop, explicit wait/yield,
protected call, handler or rollback. Reached errors propagate; supported
suspension or nonreturn prevents later requests and normal return until
continuation completes. The first opaque edge is `setInputEnable` lookup
at SELF0, then `receiver:setInputEnable(false)` at CALL2. Helper targets,
input/closing/deletion effects, destruction and lifetime completion remain
unproved, as do actual `p2` dispatch and native receiver identity.

The canonical window is `widget/widgetbaseclass_common.lua:842-858`, with
class lookup at 842, complete body at 844-856 and assignment at 858.
Root PCs 114-116, payload `[488,500)`, use GETGLOBAL `WidgetBaseClass`,
CLOSURE child38 and SETTABLE under `close`. The full `root/proto38` body
has PCs 0-7, payload `[13805,13837)`, eight words/32 bytes, no upvalues
or children. PCs are zero-based and payload byte ranges are half-open.

| Close artifact | Size | SHA-256 |
| --- | --- | --- |
| `client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32,996 bytes | `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` |
| Decoded payload | 32,983 bytes | `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |
| Canonical `widget/widgetbaseclass_common.lua` | 69,077 bytes / 3,361 lines | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |

#### Nominal processClosing return

If dispatch reaches `WidgetBaseClass.processClosing`, its complete body is
RETURN at PC 0, `A=0,B=1,C=0`, returning zero values. The one fixed receiver
is unused, including a missing receiver adjusted to nil. Extra arguments are
unused. This nominal body performs no closing operation, request, member/global
read or state write, and has no guard, branch, loop, explicit yield or handler.
After its normal return, `close` can reach `_delete` at SELF5/CALL6 without a
result gate. Actual dispatch and overrides remain conditional. The later
deletion, finalization and lifetime effects remain unproved.

The common-script identities above apply. Canonical class at 859, body at
861-863 and assignment at 865 bind this method. Root PCs 117-119, payload
`[500,512)`, bind child39 under `processClosing`. Full `root/proto39` has
PC 0, payload `[13930,13934)`, one word/four bytes, no varargs, upvalues,
children or constants. PCs are zero-based and payload ranges are half-open.

#### Nominal ActorBase delete descriptor

`ActorBaseClass._delete_inl` returns exactly the literal pair
`("self", "_delete_cpp")`. Its one fixed receiver is unused, including a
missing receiver adjusted to nil. Extra arguments are unused. LOADK PCs 0-1
load the strings into R1-R2; RETURN at PC 2, `A=1,B=3,C=0`, returns both.
The trailing RETURN at PC 3 is unreachable after that unconditional return.
The descriptor performs no lookup, call, state write or deletion.

The [published descriptor installer](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/lua-call-function-bridge.md#descriptor-resolution-and-alias-installation)
calls a descriptor with zero arguments and two requested results. Under its
registration/interception and context conditions, literal `self` selects the
original registration table, rather than a later actor receiver. `_delete_cpp`
is the raw key searched in that table and then its registered parents on nil.
If a function is found, applying the published `_inl` removal to this name
would install an `_delete` alias to that existing function. This is conditional
alias inference. The `_cpp` spelling and Lua function type 6 prove no native
identity. Failed lookup leaves ordinary registration available.

This ActorBase assignment does not establish successful alias installation or
actual WidgetBase dispatch. The canonical
[WidgetBase delete contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/fade-actor-group-native-contract.md#widget-delete-override)
records nominal `WidgetBaseClass` to `ActorBaseClass` parent registration and
the conditional virtual `+0x70` override at `0x006E3A00`, including its ordered
requests and AL-selected branches. Actual `p2`, `_delete_cpp` callable, later
`_delete` dispatch, alias/cast/override reach, native object identity and
deletion/finalization/lifetime effects remain unproved. The descriptor's
literal returns supply no deletion operation.

Its source is distinct from the common WidgetBase artifact above. Canonical
`actorbaseclass_u.lua` has class at 71, complete body at 73-78 and assignment
at 80. Root PCs 21-23, payload `[116,128)`, bind child7 under `_delete_inl`
on `ActorBaseClass`. Complete `root/proto7` has PCs 0-3, payload `[1082,1098)`,
four words/16 bytes, no varargs, upvalues or children. Canonical and original
agree on the two literal results. PCs are zero-based and ranges are half-open.

| ActorBase descriptor artifact | Size | SHA-256 |
| --- | --- | --- |
| `client/script/97qvs89r57y9rr_p.le.lpb` | 1,455 bytes | `008c68b70373b9d8decf53d6dc53f1f2d384ddf8ee7e6e5a5e9bddef6a34504c` |
| Decoded payload | 1,442 bytes | `28d5d3b3fcd26cdb18394b3e9d937b3a5514cf8ff0b3b4c4196efda82d4596b1` |
| Canonical `actorbaseclass_u.lua` | 1,887 bytes / 110 lines | `890997302a35d8217fb7c8f68105e9cc82dbfe7a77654348588bb7d4195986dd` |

#### Nominal setInputEnable forwarding

If `close`'s helper lookup resolves to `WidgetBaseClass.setInputEnable`, its
explicit false requests `receiver:setProperty("SqwtIsEnableInput", false)`.
The method has two fixed slots, receiver and value, with no varargs. It
forwards the value unchanged, including a missing value adjusted to nil.
Extra arguments are unused. There is no default, guard or normalization.
SELF0/CALL3 (`2,4,1`) supplies the literal key and value after the receiver,
discards all results and reaches the zero-value RETURN PC4 on normal return.
False, nil or zero helper results provide no success gate for close's later
`processClosing` lookup. Reached errors, supported suspension or nonreturn
can prevent that progression.

The method uses the common-script identities above. Its canonical window is
`widget/widgetbaseclass_common.lua:1565-1576`, with body 1567-1574. Root PCs
216-218, payload `[896,908)`, bind child72 under `setInputEnable`. The complete
`root/proto72` body has PCs 0-4, payload `[19502,19522)`, five words/20 bytes,
no upvalues or children. PCs are zero-based and payload ranges are half-open.

There is no body SETTABLE or other persistent store. The first opaque edge
is the `setProperty` lookup and request above. Its target, metatable behavior,
native input effects, raw persistence and lifetime remain unproved, separately
from actual `p2` and helper dispatch or native receiver identity.

#### Nominal setProperty forwarding

If the helper dispatch resolves to `WidgetBaseClass.setProperty`, SELF0 first
saves `F = receiver._setProperty` and the receiver. It then supplies nil and
reads `receiver.widgetWork`, that result's `common`, then its `widgetName`
at PCs 2-4. These dynamic reads occur after the function lookup. They do not
cause another lookup of `F`. CALL7 requests the saved function with this tuple:

```text
F(receiver, nil, widgetName, propertyName, ...complete extra tail)
```

The two fixed slots are receiver and property name. A missing property name
becomes nil in that fixed position. The full extra tail passes unchanged,
including zero extras, multiple values, false and trailing nil positions.
There is no local guard, default, normalization, persistent store, branch,
loop, explicit wait/yield, protected call, handler or rollback. CALL7 discards
all results and RETURN8 returns zero values on normal completion. The first
opaque edge is the saved `_setProperty` lookup. Errors, supported suspension
or nonreturn in that lookup, the later reads or the call can prevent progression.

Original VARARG6 `A=8,B=0` and CALL7 `A=3,B=0,C=1` establish full-tail
forwarding. Canonical lines 1455-1456 assign ellipsis to one local and pass
that local once, retaining one tail position and supplying nil for an empty
tail. That rendering alone does not express the original's complete tail.

With both nominal helper dispatches, the accepted input-enable request becomes
`F(receiver, nil, receiver.widgetWork.common.widgetName, "SqwtIsEnableInput", false)`.
Its single false tail value is unaffected by the rendering limitation. After
normal completion, the zero-result input-enable wrapper lets `close` reach
its later `processClosing` lookup. No returned success value gates that step.

The method uses the common-script identities above. Its canonical class is
at 1444, complete body at 1446-1457 and assignment at 1459. Root PCs 198-200,
payload `[824,836)`, bind child66 under `setProperty`. The full `root/proto66`
body has PCs 0-8, payload `[18602,18638)`, nine words/36 bytes, vararg flag 3,
no upvalues or children. PCs are zero-based and payload ranges are half-open.

Published [native property access](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/widget-native-call-contract.md#property-access)
supplies conditional context: if `F` is that binding and receiver/name
marshalling is valid, leading nil selects its `FUN_0075B810` setter route.
Actual callable and native receiver identity, name marshalling, resolved part,
descriptor/parser reach, Lua-false conversion, property update and delivered
input effects remain unproved by this Lua contract.

## Evidence boundary

No Behest or Skirmish script in this filing proves wave composition, routes,
objectives, timers, or rewards. Those systems, and the server-side behavior
behind the four recovered directors, remain unresolved and must not be filled
from analogy.
