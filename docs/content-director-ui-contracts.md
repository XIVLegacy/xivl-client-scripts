# Content director UI contracts

The recovered 1.23b Lua corpus preserves client-side director state and UI
contracts for guildleves, request leves, caravan escort, and Hamlet defense.
A reproducible decompile of the decoded chunks matched the canonical corpus
byte-for-byte after CRLF-to-LF normalization. The source identities, hashes,
locators, and claim boundaries are in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json).

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

## Caravan escort director

`CaravanGuardDirector` retains `finishTime`, `progressPer`, three chocobo status
values, three chocobo HP status values, and marker coordinates. Its UI methods
return those retained values and update public-effect, minimap, and map
navigation widgets. This authenticates client presentation fields and their
widget routes, not escort movement, enemy waves, failure rules, rewards, or the
server authority that updates the fields.

## Hamlet defense director

`InstanceRaidHamletDefense` derives from `InstanceRaidBaseClass`. It retains a
Hamlet identifier, rank, defense-line status, and goods status, opens the
Hamlet execution widget, and routes timer, defense-line, goods, and boss status
values to that widget. Its local clear path requests the local player's Hamlet
defense score and, when available, opens the score widget for the content ID.

These methods establish client UI consumption only. They do not establish
enemy waves, routes, scoring formulas, victory conditions, server ownership,
or rewards.

## Generic instance-raid director

The independent recovered
`tools/outputs/lpb/decomp_more_20260617/lua/director/instanceraid/instanceraidbaseclass.lua`
has SHA-256
`2f6ea8cff45b471ed8ce05c8905af75bbe199e61a712cf6f0e96c9a653badeb9`.
The corresponding installed
`client/script/61s57qvs/1wrq9w75s916/1wrq9w75s91689r57y9rr.le.lpb`
has SHA-256
`820f421aef68bdcb48c082a2c1b91521903d0e82956c273cabc462b6b3271f2f`.
The canonical class and method inventory is in
[`registry.json`](../lua/registry.json) under
`director/instanceraid/instanceraidbaseclass`.

`InstanceRaidBaseClass.init` declares retained start and finish times,
content ID, event type, countdown status, clear flag, and initialization
flag. It sets a one-second loop interval. `startEvent` stores content ID and
event type, sets the countdown from its time arguments, invokes login and
start hooks, optionally executes a cutscene, opens the information widget,
and marks initialization complete. `reloginEvent` restores the retained
values and opens the widget only when its clear flag is false. The widget
call is `openRaidDungeonExecutionWidget(nil, contentID, finishTime)`.

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

## Raid dungeon occupancy widget

Two recovered occupancy directors and their widget have these installed
`client/script/` LPB and independent recovered-Lua SHA-256 identities:

| Class | Installed LPB path / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `RaidFst0Dungeon03` | `61s57qvs/v77pu9w7l/s9164rqj6pw35vwjg.le.lpb` / `3fc7b9326942492a56c652ada5564b6eb9e528977a9d513ae1e794fa858f1652` | `5984f33d4328df277aa0accb8b310b9d18282423cb8c337646a73a0b3bd6d393` |
| `RaidRoc0Dungeon01` | `61s57qvs/v77pu9w7l/s916sv7j6pw35vwji.le.lpb` / `3b7e73d556fc9016951cb4897a85fad7ff2b93e5ccd570e2c229414e6f0e4cf2` | `ec6e626a70d41a976da06a327663581cc1473e35adb4b73e67079529bbb6d7db` |
| `RaidDungeonExecutionWidget` | `n1635q/s9166pw35vw5m57pq1vwn1635q.le.lpb` / `f02fdcd3ecbf7269937c19d664532afae94744aec33a104d364fdb795504f67d` | `8a2d239324a1ce8fc23dee64596f4ab94c1be9df862a967d522d68fe1e98e814` |

`RaidFst0Dungeon03.eventNoticeCutScene` treats `rad0f300` as its opening
scene and requests widget close for `rad0f306`, `rad0f307`, or `rad0f308`.
It then requests a cutscene in mode 61 and passes content ID 2123, type 1,
and the method's fifth argument to `openRaidDungeonExecutionWidget`.
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
