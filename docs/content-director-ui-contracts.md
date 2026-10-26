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
literal scaling by 60 does not independently establish the native clock unit.

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
