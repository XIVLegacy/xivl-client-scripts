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
