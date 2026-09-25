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

The function calls `DesktopWidget.askJournalDetailWidget` with mode 9 and
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
selector to `askJournalDetailWidget` with mode 11 and returns the selected slot
only when the widget result is true. Empty IDs are skipped, and an all-zero
list returns `nil, 5`. This is the client's card-to-selector mapping; it does
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
are not written by this method. `JournalListWidget.processUICommandSelection`
in mode 4 calls `selectGuildleveChangeBonus` with the selected `JournalIndex`.
`DesktopWidget.askNextGuildleveJournal` forwards its journal ID and trailing
arguments to `askJournalDetailWidget` with selector 10.

These are static client routes and arguments. They do not establish a server
meaning for `glHist` or selector 10, a successful response, or historical
runtime invocation.

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
  (`executeCommandJournalHistoryInfo`, `askNextGuildleveJournal`):
  `client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, LPB SHA-256
  `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425`, decoded
  payload SHA-256 `685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`
  (`retail_lua_coverage.json:25443-25455`).

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
