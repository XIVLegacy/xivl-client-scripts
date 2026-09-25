# Guildleve journal lifecycle and commands

The retail 1.23b Lua corpus distinguishes the state of a retained guildleve
journal entry from acceptance confirmation, activation, completion
presentation, and requests to retry or remove it. These scripts establish
client presentation and command arguments. They do not establish the server's
authoritative state changes.

## Bounded 12487 scenario

Static row 12487 is the regional battlecraft guildleve "Necrologos:
Celeritous Impetus." Its `guildleve` row has recommended rank 30 at field 5
and time limit 30 at field 21. Its `guildleve_UI` row maps field 78 to
aetheryte actor class ID 1280067. The retained `party_battle_leve.pcapng`
sample contains 12487 in its client and server event streams and later contains
the only retained GuildleveDirector finish sample. This identifies one
scenario; it does not make every packet or ordering in that capture universal.

Evidence: `xivl-client-data:csv/guildleve.csv`,
`xivl-client-data:csv/guildleve_UI.csv`,
`xivl-client-data:csv/xtx_guildleve.csv`, and
`xivl-captures:sources/pcap-1.23b/objects/party_battle_leve.pcapng`. The
bounded finish attribution is recorded in
`xivl-client-structs:manifests/guildleve_lifecycle.json`.

## Acceptance confirmation

`PopulaceGuildlevePublisher.eventTalkCard` accepts eight guildleve IDs in
arguments 1 through 8 and returns the selected card index. The publisher's
`eventTalkDetail` argument route is exact:

| Position | Client field or use |
|---:|---|
| 1 | guildleve ID |
| 2 | mark |
| 3 | displayed item ID |
| 4 | displayed item count |
| 5 | displayed secondary item ID |
| 6 | displayed secondary item count |
| 7 | boost point |
| 8 | complete flag |
| 9 | optional presentation variant; not forwarded to the detail widget |

The function calls `DesktopWidget.askJournalDetailWidget` with selector 9 and
arguments 1 through 8 in order. A non-nil result copies those values into the
publisher's presentation work and the result is returned unchanged. The widget
returns true only when its ask result is 1. No branch in this path inserts
12487 into `guildleveId`, changes `guildleveDone` or `guildleveChecked`, or
calls a mutation API. Therefore true means that the client confirmation UI
succeeded, not that authoritative acceptance completed.

Evidence: `lua/scripts/chara/npc/populace/populaceguildlevepublisher.lua` and
`lua/scripts/widget/desktopwidget_connector.lua`.

## Passive guildleve card selection

`PopulacePassiveGLPublisher` exposes up to eight card slots. It maps slots 1-8
to selector values `1, 2, 3, 4, 1, 2, 3, 4`; an out-of-range slot falls back
to selector 1. For a selected nonzero guildleve ID, the publisher passes that
selector to `askJournalDetailWidget` with selector 11 and returns the selected
slot only when the widget result is true. Empty IDs are skipped, and an
all-zero list returns `nil, 5`. This is the client's card-to-selector mapping; it does
not establish the visual distinction represented by each selector or a
server-side variant policy.

Evidence: `lua/scripts/chara/npc/populace/populacepassiveglpublisher.lua:11-59,216-290`
(11,836 bytes, SHA-256
`F4D7AB96F3932E41A9B6AFB6D21EA0270FED945FE1DDA1211807963EC13265F1`,
`manifests/scripts.json:6477-6480`). The retail resource census maps
`client/script/729s9/wu7/uvupy975/uvupy975u9rr1o53yup8y1r25s.le.lpb`
(5,122 bytes, SHA-256
`DED83220DC9E8A73ECDC6F6BB4E95E35A2FD74C459C49A09D03205D5105781BE`)
to this script and pins its 5,109-byte payload SHA-256 as
`F1463D12D9658ED49CFD15C2766DE5982D33FAB0502D48311267FE5A8E71539E`
(`manifests/retail_lua_coverage.json:7790-7801`).

## Journal state

`JournalDetailWidget.checkGuildleveProcess` returns `checked`, `done`, and
`failed`, where `failed = done and not checked`. The list widget uses the same
two stored bits to select its active, failed, and completed presentations. A
nonzero journal ID is required before either widget reaches this state logic.

| done | checked | Client presentation |
|---|---|---|
| false | false | Retained entry without an active, failed, or completed flag |
| false | true | Active |
| true | false | Failed |
| true | true | Completed |

For journal mode 1, regional type 1 and local type 2 entries expose Retry and
Break controls. Retry is enabled only for a failed entry when the supplied
`offerLimit` is positive. This is a client-side precondition, not evidence of
where or when an allowance is decremented.

Evidence: `lua/scripts/widget/ask/journaldetailwidget.lua`,
`lua/scripts/widget/ask/journallistwidget.lua`,
`lua/scripts/chara/player/player_work.lua`, and
`lua/scripts/chara/player/playerbaseclass_work.lua`.

### Type-1 detail payload

`JournalDetailWidget.setDetailData` (root/proto10) branches on
`work.journalType == 1`
(bytecode PC `000`-`003`, offsets `0x001FFE`-`0x00200A`). In this branch,
arguments A3/A4 go to `setRewardData("Item_RewardText", ...)` and A5/A6 go to
`setRewardData("Item_RewardText2", ...)` (PC `132`-`141`, offsets
`0x00220E`-`0x002232`). A7 at least 1 displays the evaluation title and calls
`setItemText` with text key `4236`; a lower A7 hides the evaluation title,
borders, and evaluation text (PC `142`-`175`, offsets `0x002236`-`0x0022BA`).
A8 controls `IconControl_StageIcon` visibility (PC `123`-`126`, offsets
`0x0021EA`-`0x0021F6`). In `setRewardData` root/proto12, a zero item value
hides the item text (PCs `000`-`001` and `016`-`020`, offsets
`0x003110`-`0x003114` and `0x003150`-`0x003160`); otherwise first value
`1000001` selects text key `4172`, and other values select `4182` (PCs
`003`-`014`, offsets `0x00311C`-`0x003148`). These are positional
presentation uses and do not assign server-field or item meanings.

Bytecode identity is pinned at `manifests/retail_lua_coverage.json:26192-26205`:
`client/script/n1635q/9rz/0vpsw9y65q91yn1635q.le.lpb`, LPB SHA-256
`0EB5C1F6B56AF27AE5CE02DE116A69602A6A60A009FCC92D3DDE3938CEA3EB2F`, decoded
payload SHA-256 `15E38590AA448B15055C6DF3452464E96695F6310C6FAA53AEEEADBEB65FDA32`.

### Type-2 detail payload

`JournalDetailWidget.setDetailData` selects type 2 at root/proto10 PCs 216-217
(offsets `0x00235E`-`0x002362`). In this branch, A1 is passed with
`work.journalID` to the employer text blocks using text keys 4226 and 4227
(PCs 336-351, offsets `0x00253E`-`0x00257A`), and to `Item_RewardText`
with key 4231 and `Item_DetailText` with key 4229 (PCs 373-389, offsets
`0x0025D2`-`0x002612`).

A3 and A4 are stringified for `TextBlock_NumberOfSuccessesValue` and
`TextBlock_NumberRemainingValue` (PCs 238-256, offsets
`0x0023B6`-`0x0023FE`). A5 controls `Item_Status`: nil or a nonpositive
value takes the hidden path, while a positive value populates the row (PCs
224-227 and 258-262, offsets `0x00237E`-`0x002416`). A7 is stored as
`work.offerLimit` and enables `Button_Localleve_Retry` only when
`work.guildleveFailed` is true and A7 is positive (PCs 394-408, offsets
`0x002626`-`0x00265E`). A2, A6, and A8 do not supply another use in this
branch. These positions and UI calls do not assign server-field meanings.

### Journal list entry points and history

`MainMenuWidget.init` assigns text ID 2104 and help ID 75726 to entry index 5.
`MainMenuWidget.processUICommandSelectionChanged` opens
`Ask/JournalListWidget` in mode 1 when that entry is selected.
`JournalListWidget.processUICommandOperate` opens `GuildleveHistoryWidget`
for `Button_History`.

`GuildleveHistoryWidget.processUICommandDefault` requests history when the
widget receives `UILuaCommands.Shown`. `DesktopWidget.executeCommandJournalHistoryInfo`
obtains system command 24212 and calls it with the `glHist` tag.
`GuildleveHistoryWidget.setDetailData` accepts eight positional IDs and writes
each nonzero value to the matching `Button_Leve` user-work entry; zero values
are not written by this method. `DesktopWidget.askNextGuildleveJournal`
forwards its journal ID and trailing arguments to
`askJournalDetailWidget` with selector 10.

### JournalListWidget modes and row arguments

`JournalListWidget.createList` (root/proto10 PCs 35-77, offsets
`0x1E20`-`0x1EC8`) calls these row builders. Selection behavior is in
`processUICommandSelection` (root/proto3 PCs 83-121, offsets
`0x0ACD`-`0x0B65`):

| Mode | List builder calls | Selection behavior |
|---:|---|---|
| 2 | `addActiveGuildleveList` | Calls `finish(JournalID)`. |
| 3 | `addQuestList`, then `addPassiveGuildleveList` | Sets `work.guildleveFlag` only when `JournalType == 2`, then calls `finish(JournalIndex)`. |
| 4 | `addActiveGuildleveList` | Calls `actor:selectGuildleveChangeBonus(JournalIndex)`, then `finish(JournalID)`; `finish` sets `resultSelectFlag` true in mode 4 (root/proto7 PCs 10-26, offsets `0x1269`-`0x12A9`). |
| 5 | `addQuestList` | Calls `finish(JournalID)`. |
| 6 | `addPassiveGuildleveList` | Calls `finish(JournalIndex)`. |

The active-list builder skips ID 0, reads each remaining ID from its player
slot, queries `isDoneGuildleveById` and `isCheckedGuildleveById`, and writes
type 1, the ID, and the slot as `JournalType`, `JournalID`, and
`JournalIndex` (root/proto12 PCs 7-42, offsets `0x2235`-`0x22C1`;
root/proto17 PCs 83-94, offsets `0x2E2A`-`0x2E56`). The passive-list
builder skips nil entries, gets each ID through `getQuestId`, queries
`isDoneLocalleveById` and `isCheckedLocalleveById`, and writes type 2 and the
slot index (root/proto13 PCs 7-44, offsets `0x2476`-`0x250A`). The quest
builder includes nonnil entries whose `_isAlive()` result is true, gets their
IDs through `getQuestId`, and writes type 3 and the scenario slot index
(root/proto14 PCs 7-39, offsets `0x26CD`-`0x274D`).

`addQuestCompleteList` writes type-3 rows with `JournalIndex` 0 for IDs where
`isQuestComplete(ID)` is not exactly true (root/proto15 PCs 3-29, offsets
`0x28D7`-`0x293F`). This records the method's predicate without assigning
the CSV candidate's `completed quest` label. `setListItem` writes `Name`
from its text-key argument and stores `JournalType` and `JournalID`
(root/proto17 PCs 0-94, offsets `0x2CDE`-`0x2E56`). In mode 3, when an actor
is present, it calls `actor:canUseGuildleve(player, JournalID)`; only a result
exactly false sets `ItemColor` to `tostring(0.5)` and `JournalType` to 0
(root/proto17 PCs 164-215, offsets `0x2F6E`-`0x303A`). These calls and row
values do not establish category labels, text-key meanings, or the meaning of
the color value.

### Detail selectors and map navigation

`DesktopWidget.askJournalDetailWidget` (root/proto368, PCs 0-42, offsets
`0x02425F`-`0x02430B`) selects values in R5 and R6, then passes R6, R5, the
journal ID, R7, and R8 to `openWidgetYield` at PCs 151-161 (offsets
`0x0244BB`-`0x0244E3`). R7 and R8 default to false at PCs 0-2; selector 10
sets R7 to literal true at PC 18. The dispatcher branches on these selector
values:

| Selector | R5 value | R6 value | R7 value | R8 value | Branch PCs |
|---:|---:|---:|---:|---:|---|
| 1 | 3 | 2 | false | false | 38-41 |
| 6 | 1 | 4 | false | false | 9-12 |
| 7 | 2 | 2 | false | false | 21-24 |
| 9 | 1 | 3 | false | false | 4-6 |
| 10 | 1 | 3 | true | false | 15-18 |
| 11 | 2 | 3 | false | false | 27-30 |
| 13 | 2 | 4 | false | false | 32-35 |

The values are opener arguments; these chunks do not prove how the native
widget-creation path maps them to `JournalDetailWidget.initAsk` parameters.
Selector 10's literal true and the separate `initAsk` branch where formal A6
sets `work.questCompleted` (root/proto0 PCs 148-151, offsets
`0x0580`-`0x058C`) are not joined by a Lua call in the recovered chunks.

`JournalDetailWidget.processUICommandOperate` opens child
`MapNavigationWidget` with mode 1, `work.questIndex`, and
`work.journalID` (root/proto1 PCs 20-32, offsets `0x0C82`-`0x0CAA`). The
map widget initializer separately stores its first three formals as mode
(root/proto2 PC 54, offset `0x08C2`), quest index (PCs 64-67, offsets
`0x08EA`-`0x08F6`), and journal ID (PCs 68-71, offsets
`0x08FA`-`0x0906`). On Activated in mode 1,
`MapNavigationWidget.processUICommandEvent` (root/proto3 PCs 79-96, offsets
`0x0EDE`-`0x0F22`) calls
`DesktopWidget.executeCommandJournalDetailInfo(3, journalID, questIndex, 2)`;
when that call returns false, the widget opens failure widget 5211.

The connector's `executeCommandJournalDetailInfo` type-3 branch (root/proto188
PCs 24-36, offsets `0x01876C`-`0x01879C`) obtains system command 24211 and
calls its `command` method with the journal ID, literal 2, and three nil
values. It does not forward `questIndex`. The connector's `qtmap`
requested-data branch is a separate route; these Lua chunks do not connect it
to command 24211. These calls do not establish server response semantics or
historical runtime invocation.

The `glHist`, selector-10, detail, and map calls above are static client routes
and arguments. They do not establish server semantics, a successful response,
or historical runtime invocation.

Source identity is pinned in `manifests/retail_lua_coverage.json`:

- `lua/scripts/widget/mainmenuwidget.lua` (`init`, `processUICommandSelectionChanged`):
  `client/script/n1635q/x91wx5wpn1635q.le.lpb`, LPB SHA-256
  `C0E1782A3CA183FCAA520A16320946F62D3FC861C74978CDE19EA20FCD064B0A`, decoded
  payload SHA-256 `185D856D406D46BA7416444DDC2212B68036F7D56D0EE62148BE2567630C90B2`
  (`retail_lua_coverage.json:27813-27825`).
- `lua/scripts/widget/ask/journallistwidget.lua` (`processUICommandOperate`,
  `processUICommandSelection`):
  `client/script/n1635q/9rz/0vpsw9yy1rqn1635q.le.lpb`, LPB SHA-256
  `A15C8BF36E8124C5C4F5BE2EF189037894C98342C7C7EEF5889ADE16D975E6F3`, decoded
  payload SHA-256 `549BC61FE3C206F1DD080057948A201F2824A785D039FB9F97878D8A31491D33`
  (`retail_lua_coverage.json:26208-26220`).
- `lua/scripts/widget/guildlevehistorywidget.lua` (`processUICommandDefault`,
  `setDetailData`):
  `client/script/n1635q/3p1y6y5o521rqvsln1635q.le.lpb`, LPB SHA-256
  `A4A341F5653F1EA2EBC06EC59BF885F437E4855A2F2E6023B9F99D939C59BC66`, decoded
  payload SHA-256 `F520CD90F18BDAD9314648CDEB053A0F109E9BE6E4617B9E6A9E706D468EAE87`
  (`retail_lua_coverage.json:25248-25260`).
- `lua/scripts/widget/desktopwidget_connector.lua`
  (`executeCommandJournalHistoryInfo`, `askNextGuildleveJournal`,
  `askJournalDetailWidget`, `executeCommandJournalDetailInfo`):
  `client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, LPB SHA-256
  `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425`, decoded
  payload SHA-256 `685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`
  (`retail_lua_coverage.json:25443-25455`).
- `lua/scripts/widget/mapnavigationwidget.lua`
  (`init`, `processUICommandEvent`): `client/script/n1635q/x9uw9o139q1vwn1635q.le.lpb`,
  LPB SHA-256 `873EE821C979B9C0959743BC619444EC01BD39C96F71235235278BB602B4D0BB`,
  decoded payload SHA-256
  `21CC7F2F9C6E2A56E02620E18748FA9DD70BF02DAB6A889FD6083826D60528C2`
  (`retail_lua_coverage.json:27889-27900`).

Acceptance first becomes client-visible when synchronized player work contains
the nonzero ID. `AetheryteBaseClass.canUseGuildleve(player, guildleveID)` then
requires `player:isUnusedGuildleveById(guildleveID)`, loads field 78 from
`guildleveUISheet`, and accepts only a live aetheryte whose actor class ID
matches that field. For 12487, unused means the ID is retained while both
state bits are false, and the required class ID is 1280067. The corpus does
not expose the server response that creates this state, so acceptance ordering
stops at that response boundary.

## Activation and director presentation

At a matching aetheryte, the strongest client-side order is:

1. `eventGLSelect(filter)` returns the journal-list selection status first and
   the selected retained guildleve ID second. A failed selection forces the
   second result to zero.
2. `eventGLSelectDetail` forwards arguments 1 through 7 and argument 9 to
   `askActiveGuildleveDetailWidget`; argument 8 is not forwarded. Its first
   result says whether the detail widget opened and its second is true only
   when the ask result is 1.
3. `eventGLDifficulty(guildleveID)` returns a selected difficulty or nil.
4. `eventGLStart(guildleveID, difficulty, arg3, ..., arg9)` opens
   `Ask/GuildleveStartWidget`. It forwards arguments 1 through 8, then literal
   zero, then argument 9. A widget result of 1 returns argument 2; every other
   result returns nil.
5. A concrete Guildleve director initializes `GuildleveBaseClass` with the
   guildleve ID, aetheryte location, and marker coordinates. The base class
   reads sheet field 21 as `timeLimit` and publishes start, objective, UI-state,
   and marker changes through `DesktopWidget.processUpdateContentsInformation`.
6. When synchronized `guildleveWork.signal` becomes signed -1, the base class
   emits UI `finish` and updates the minimap marker.

The corpus contains `GuildleveBaseClass` and concrete director classes such as
`PrivateGLBattleSweepNormal`. It contains no `GuildleveCommon` script and no
use or declaration of `GetGuildleveGamedata`. A server can supply a global or
an authored director outside this corpus, but those names are not recovered
retail Lua contracts. The retail sheet access shown here is
`guildleveSheet:_loadKeyTemporarily` plus `_getData`, not
`GetGuildleveGamedata`.

### Objective article tuple routing

`GuildleveExecutionWidget.updateArticle` calls
`GuildleveBaseClass.getArticleFullDataOnGuildleveInfo` for ten result slots.
It passes the article index and results 2, 4, 5, and 6 to `setArticleType`,
then the index and results 3, 1, and 7 through 10 to `setArticleState`
(widget `updateArticle` root/proto3 PCs 0-18, offsets `0x0006C9`-`0x000715`;
base-class provider root/proto39 PCs 0-32, offsets `0x002290`-`0x002310`).
This records the client's positional routing only; generated article-type,
condition, state, and text-field meanings are not assigned here.

The widget LPB is pinned as
`n1635q/3p1y6y5o55m57pq1vwn1635q.le.lpb`, SHA-256
`8EED436E9058CBA2BC7EA92603A1A493CF10BE7ACE8B676EA66B5F384326C8CD`, with
decoded payload SHA-256
`58812BFCCC48E5D651569F55382DE88C55A365EC91D0A9171FFE93E751EFCE13`
(`manifests/retail_lua_coverage.json:25274`). The base-class LPB is
`61s57qvs/3p1y6y5o5/3p1y6y5o589r57y9rr.le.lpb`, SHA-256
`73559543D4E2192180C28AC8F8F6F3FB69EBF8BCBB47B2C11A69C837CFE8F303`, with
decoded payload SHA-256
`BCAD3160D16813502529467CE5DA17BB3A9BC80C576CD71841708FE7859D7E84`
(`manifests/retail_lua_coverage.json:1620`).

Evidence: `lua/scripts/chara/npc/object/aetheryte/aetherytebaseclass.lua`,
`lua/scripts/director/guildleve/guildlevebaseclass.lua`, and
`lua/scripts/director/guildleve/privateglbattlesweepnormal.lua`.

### Parent and child playing choices

`AetheryteParent.processGuildlevePlaying` and
`AetheryteChild.processGuildlevePlaying` each show a restricted-choice prompt.
Their prompt text IDs and follow-up text/ask IDs differ:

| Class | Restricted-choice text ID | Choice 2 say / ask IDs | Choice 3 say / ask IDs | Choice 6 say / ask IDs |
|---|---:|---:|---:|---:|
| `AetheryteParent` | 146 | 153 / 154 | 26 / 27 | 158 / 159 |
| `AetheryteChild` | 35 | 42 / 43 | 15 / 16 | 47 / 48 |

For choices 2, 3, and 6, the method returns that choice only when its follow-up
ask returns 1; otherwise it repeats the restricted-choice prompt. Choice 4
with the supplied eighth argument equal to 1 says text ID 164 on the parent or
53 on the child, then repeats the prompt. Otherwise it says text ID 162 or 51
and opens `Ask/GuildleveSelectLevelWidget` in mode 1 with the eighth argument
minus one. It returns `(4, selectedLevel)` only when the widget succeeds and
the level is between 1 and 5. These numeric text IDs and argument gates do
not establish the meaning of the choices or the server-side start decision.

Evidence: `lua/scripts/chara/npc/object/aetheryte/aetheryteparent.lua` and
`lua/scripts/chara/npc/object/aetheryte/aetherytechild.lua`. Their decoded
payload SHA-256 values are pinned in
`manifests/retail_lua_coverage.json:8247-8251`
(`4824C5921D56B262D47B40B82BC8366A795860B4DD9944ECDB41AC7FEE4E33E3`) and
`manifests/retail_lua_coverage.json:8187-8191`
(`453A18028DBC5D1883954EA33EA1494DE1D83947212EE96DDDADA9DB8232D252`).

### Level-selection widget

The parent and child choice-4 branches pass their eighth argument minus one
to `Ask/GuildleveSelectLevelWidget` in mode 1. Its `initAsk` argument defaults
to 5 when nil. Level 1 is always confirmable; levels 2 through 5 are
confirmable only when the preceding integer is less than that argument, and
otherwise are hidden. The widget sets the title from text ID 50015, uses IDs
50016 through 50020 for the five level labels, and sets the cancel control
from ID 50021. Operating a level control sets the base ask result to its
number from 1 through 5; both the cancel control and cancel handler set it to
-1.

This identifies the level-selection control and result values, not the
semantic scale of the argument or a guildleve difficulty formula.

Evidence: `lua/scripts/widget/ask/guildleveselectlevelwidget.lua`; its decoded
payload SHA-256 is
`6172439C2F0C9EB2ABF7833452EC4BF36B60C13CE971EF02F0389EE19CE3F986`, pinned
at `manifests/retail_lua_coverage.json:26348-26355`.

## Completion and hand-in presentation

`AetheryteBaseClass.eventGLReward` receives 12 arguments after self. It copies
them into temporary presentation work in this order: guildleve ID, clear time,
mission bonus, difficulty bonus, faction number, faction bonus, faction credit,
displayed item ID, displayed item count, displayed secondary item ID, displayed
secondary item count, and difficulty. It then opens `Ask/ContentRewardWidget`
and returns the widget's two results. These assignments and widget results do
not prove item or currency grants, reward selection policy, authorization, or
persistence.

The separate completion-history route must not be confused with the active
guildleve state bits. `JournalListWidget.requestQuestComplete` obtains a range
and calls `DesktopWidget.updateQuestComplete`.
`PlayerBaseClass.updateQuestComplete`
maps IDs at or above 120001 to `questCompleteG` array indexes, calls
`_updateWork("playerWork", "questCompleteG", first, last)`, and rate-limits
the request. `_onUpdateWork` later routes a `questCompleteG` update to
`processUpdateQuestComplete`, which converts the indexes back to IDs and
refreshes the desktop widget. This is a request and callback for the
`questGuildleveComplete` completion-history array; it does not set
`guildleveDone` or `guildleveChecked` for journal ID 12487.

For requested journal detail data, `_onReceiveDataPacket("requestedData", ...)`
forwards the payload to `DesktopWidget.processRecievedRequestedDataForWidget`.
The `activegl` discriminator selects journal-detail presentation and forwards
the supplied ID and remaining values. This is another presentation update,
not evidence of a state mutation.

The bounded order is therefore synchronized retained ID -> aetheryte selection
and start confirmation -> director start/objective updates -> director finish
presentation -> server-supplied hand-in arguments and completion-history
updates. The first unsupplied acceptance response and the first unsupplied
hand-in policy response are server boundaries. No allowance consumption,
retention, abandon or retry mutation, reward grant, persistence, authorization,
or teardown follows from these client presentation paths.

Evidence: `lua/scripts/chara/npc/object/aetheryte/aetherytebaseclass.lua`,
`lua/scripts/chara/player/playerbaseclass.lua`,
`lua/scripts/chara/player/playerbaseclass_work.lua`,
`lua/scripts/widget/ask/journallistwidget.lua`, and
`lua/scripts/widget/desktopwidget_connector.lua`.

## Command mapping

After confirmation, the detail widget passes the journal type, journal ID, and
selected subindex to `DesktopWidget.executeJournalCommand`.

| Journal type | Subindex | Request |
|---|---:|---|
| 1, regional guildleve | 2 | Break |
| 2, local guildleve | 3 | Break |
| 1, regional guildleve | 4 | Retry |
| 2, local guildleve | 5 | Retry |
| 3, quest | 1 | Break |

Direct Lua 5.1 bytecode control flow establishes that valid journal types 1,
2, and 3 call system command 24241 as
`command(24241, journalID, subindex, nil, nil)`. The journal type validates the
route but is not forwarded. Invalid types and a missing command object return
false. The caller closes the detail widget only when the forwarded result is
exactly true; that result is not proof that a server mutation completed.

Evidence: `lua/scripts/widget/ask/journaldetailwidget.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`, and
`lua/scripts/chara/player/playerbaseclass.lua`. The published decompile
misstructures the type 1 and 2 branches in `executeJournalCommand`; the command
argument claim is therefore bounded to the decoded bytecode control flow.

## Ownership boundary

The command 24241 registration and player-facing text belong to
`xivl-client-data`. Native guildleve execution retirement and director object
finalization belong to `xivl-client-structs:manifests/guildleve_lifecycle.json`.
Neither owner currently maps subindices 2-5 to an outgoing packet or proves
Break and Retry server mutations. This page does not infer those behaviors from
widget closure or native director teardown.
