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
flag. It sets a one-second loop interval. The ordered `startEvent` sequence
and subclass-owned widget endpoint are recorded in
`xivl-decomp:docs/event/instance-raid-widget-lifecycle.md` and are not
redefined here. `reloginEvent` restores the retained values and opens the
widget only when its clear flag is false. The widget call is
`openRaidDungeonExecutionWidget(nil, contentID, finishTime)`.

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

Five independently recovered scripts under
`tools/outputs/lpb/decomp_more_20260617/lua/director/quest/` join the
following installed `client/script/` LPBs. Hashes are SHA-256; class and
method inventories are in [`registry.json`](../lua/registry.json).

| Class | Installed LPB suffix / hash | Recovered Lua hash |
| --- | --- | --- |
| `QuestDirectorGcg70101` | `61s57qvs/tp5rq/tp5rq61s57qvs373cjiji.le.lpb` / `10035dfb8289937f2b4350becc5e61f453f4fa77525346ad5849689adf9bc34d` | `fd20c2d7c98689983a0378fbdadf5c032854c734db8858f6723176cfad3d9d17` |
| `QuestDirectorGcl70101` | `61s57qvs/tp5rq/tp5rq61s57qvs37ycjiji.le.lpb` / `e73b02ba4f98e11ce34dde7059222ae2a8cac96a735e2b36add33b14785de92d` | `fd5ccdaee7735c07e285da73cde7e3095a704baa79eb9a2a5fb86e768bd0fe75` |
| `QuestDirectorGcu70101` | `61s57qvs/tp5rq/tp5rq61s57qvs37pcjiji.le.lpb` / `4922c5bf4e904e3194f066502add6ee1570e2971b7e62373c2cd7b75cfc7d046` | `660d558a25d78d10cfc3b26132fb9423f3083242d060aafbf15f8cc5170d6ec5` |
| `QuestDirectorNMRush01` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2ji.le.lpb` / `5a0b0b7524e0a6b0b9fa1dadb5fb1d7a0708dc8864aa1fe1be9ab9248437d04e` | `a8031ff68c5883bab600a0696055c14da4906a1fb442d5b55cd321e71685b35f` |
| `QuestDirectorNMRush02` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2jh.le.lpb` / `c65739da2cb6817c6333b9d5d69a4db3b7118649304d0f461e8319bc9dab3491` | `3825849ba435251849abd112c6b6ebfc6be654d749cd91db021625eb5ee6cf57` |

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

The independently recovered
`tools/outputs/lpb/focused/widget/desktopwidget_connector.lua` (SHA-256
`c5480f97a81c08f8640b4d250c0e20694b2a697c4dc9b1e0d343a230c8cbcbe0`)
matches installed
`client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb` (SHA-256
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
