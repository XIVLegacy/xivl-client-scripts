# Cutscene replay and skip client contract

The client uses two distinct UI paths: skip is bound to the currently playing
CutScene actor, while replay selection starts from an inn journal and resolves
static `cutReplay` rows. Neither path is a generic widget-open entitlement.

## Skip actor binding

`DesktopWidget` creates `CutSceneSkipWidget` and
`CutSceneSkipWarningWidget` as static slots 12 and 13
(`desktopwidget_connector.lua:4198-4202`). In the common CutScene method,
the third argument's raw values 1, 3, 5, and 7 normalize to selector 1, while
2, 4, 6, and 8 normalize to selector 2 (`startCutScene`, bytecode PCs 15-84,
offsets `0x001D4D`-`0x001E61`); this block does not normalize other raw values.
Only play mode 1 with normalized selector 1 passes the CutScene actor to
`showCutSceneSkip` before `_play`; the method
calls `hideCutSceneSkip` after the playback result path (PCs 225-235 and
251-272, offsets `0x002095`-`0x0020C1` and `0x002101`-`0x002151`). The desktop
bridge stores that actor as slot 12's `argActor`, and its hide path calls the
widget's `clear` (`desktopwidget_connector.lua:5760-5775`).

`CutSceneSkipWidget` opens a `CommonAskWidget` with text IDs 1022/1023/1024
for the skip button. Only ask result 1 with a nonnull `argActor` calls that
actor's `_skip`; it then clears the actor reference. Its `clear` method
closes a child ask if present, clears the reference, and hides the widget
(`cutsceneskipwidget.lua:6-40`). Slot 13 displays warning text 1027 and
hides on its animated-complete command
(`cutsceneskipwarningwidget.lua:3-15`). These are client lifecycle calls,
not proof of a particular retail cutscene's skip flag or server policy.
The common `CutScene.startCutScene` play-mode-1 branch awaits the same
`_play(...)` result after showing the skip widget, then hides the widget
and returns that result (`cutscene_common.lua:886-910`). The skip action
targets the bound actor's `_skip()` while that play call is in progress;
there is no separate quest-level return branch in this method. This does
not define the historical server's event-close or warp ordering.

## PlaneMap cutscene hook

`CutScene._onShowUIClip` passes its third argument to
`DesktopWidget.openMapForCutScene`; `_onHideUIClip` calls
`closeMapForCutScene` for PlaneMap (`cutscene_common.lua:622-638`). The
desktop open path rejects a second open while its cutscene-map flag is set
and acts only in cutscene mode; it opens root widget 11 as
`MapNavigationWidget` in mode 2 and sets the flag only when that open call
succeeds. The close path acts when the flag is set and cutscene mode is
active; it uses the same root and widget name, asks the desktop to cancel a
widget command if close returns false, and then clears the flag
(`desktopwidget_connector.lua:5017-5056`). These are static local client
calls; they do not establish runtime rendering or input behavior. The
mode-2 widget properties are documented with the MapNavigationWidget
contract in `content-director-ui-contracts.md`.

## Inn replay selection

`AreaBaseClass` creates `cutReplaySheet` only when `_isInn()` is true and
deletes it on inn finalization (`areabaseclass.lua:185-192`, `215-220`).
`DesktopWidget.openCutSceneReplaySelectWidget` opens
`Ask/JournalListWidget` in mode 7 (`desktopwidget_connector.lua:5093-5098`).
`JournalListWidget.initAsk` sets `work.questType` to 2 and
`work.requestResult` to true on its mode-7 path (`root/proto0` PCs 55-60,
offsets `0x0495`-`0x04A9`). Its `createList` method calls
`addQuestCompleteListForCutsceneReplay` for mode 7 (`root/proto10` PCs 79-84,
offsets
`0x1ED0`-`0x1EE4`). The row builder uses the numeric range returned by
`getQuestCompleteID`. For the `(110820, 20)` range returned by numeric
`questType` 32 (`root/proto20` PCs 183-188, offsets
`0x3823`-`0x3837`), it checks `cutReplaySheet` keys
`110820 * 100 + i` for `i` from 1 through 20. It adds a row only when the
key exists and `_isCompletedCutSceneReplayQuest(ID)` is not exactly true; the
row has `JournalType` 3, `JournalIndex` 0, and text key 5108
(`root/proto16` PCs 3-38, offsets `0x2A53`-`0x2ADF`).

For other returned ranges, the row builder tests IDs from the first value plus
1 through the second value minus 1, applies the same completion predicate,
and uses text key 5106. When the first value is 110600, it excludes IDs 110821
through 110824 (`root/proto16` PCs 41-73, offsets `0x2AEB`-`0x2B6B`).
These numeric values and text keys are not assigned category or wording
meanings.

In mode 7, selection calls `finish(JournalID)` when
`floor(JournalID / 100) == 110820`; otherwise it opens
`Ask/ReplayCutsceneSelectWidget` as a child with that ID
(`root/proto3` PCs 123-141, offsets `0x0B6D`-`0x0BB5`). This is a
numeric predicate on the journal ID, not a direct equality check with
110820. The child scans
`questId * 100 + 1` through `questId * 100 + 30` for existing
`cutReplaySheet` keys and stores selected cutscene IDs, not arbitrary
scene filenames (`replaycutsceneselectwidget.lua:65-133`).

`PopulaceCutScenePlayer.processCutScenePlay` opens this selector, reads the
selected ID, loads its `cutReplay` row, resolves sheet column 0, CSV field 1
after the row ID, as the cutscene name and columns 8..15 as playback
arguments, and selects NQ/HQ and SNPC
playback branches (`populacecutsceneplayer.lua:39-141`). The script also
unloads the row and closes the selector. This establishes a client-side
replay route, not which book entries a historical player had unlocked,
whether a contributor's completion-bit packet is retail-equivalent, or a
safe direct open outside the inn owner path. No runtime playback or music
restoration is inferred from the static calls.

## Quest replay argument helper

`QuestBaseClass.getCutSceneReplayData` (`main/f12` in the decoded chunk)
resolves several argument values through the local player object. Instruction
indexes below are one-based within that prototype.

| Input value | Instruction indexes | Client operation |
| ---: | --- | --- |
| `-201` | `4`, `6`-`8` | Call `_getCutSceneReplaySnpcNickname`. |
| `-202` | `10`, `12`-`14` | Call `_getCutSceneReplaySnpcCoordinate`. |
| `-203` | `16`, `18`-`20` | Call `_getCutSceneReplaySnpcSkin`. |
| `-204` | `22`, `24`-`26` | Call `_getCutSceneReplaySnpcPersonality`. |
| `-205` | `28`, `30`-`32` | Call `getInitialTown`. |
| `-217` | `180`, `182`-`187` | Call `_getCutSceneReplaySnpcSkin`, then pass its result to `getSnpcSexualityToSkin`. |
| `-200` | `197`, `199`-`200` | Return the literal value `0`. |

The method first obtains the player through `worldMaster:_getMyPlayer()`.
These branches establish only the client helper operations and literal
return. They do not assign field meanings to the values or establish replay
eligibility or runtime playback.

The LPB `tp5rq/tp5rq89r57y9rr.le.lpb` has SHA-256
`35293157c6bfd1edfc973bc0bd1986e83401d69e5cac39df2616041caff58674`.
Its 4,154-byte decoded payload has SHA-256
`6903eb4a86f200f5cd690cda2d4104476d72d1eeba86e3b03f3cd2631966ef88` and
matches `lua/scripts/quest/questbaseclass.lua` in
`manifests/retail_lua_coverage.json`. The method is listed in
`lua/registry.json` and the canonical script identity is in
`manifests/scripts.json`.

## Provenance

The recovered LUAC for `widget/cutsceneskipwidget`,
`widget/cutsceneskipwarningwidget`, `widget/ask/journallistwidget`,
`widget/ask/replaycutsceneselectwidget`, `area/areabaseclass`,
`chara/npc/populace/populacecutsceneplayer`, and `gamedata/cutscene_common`
matched the corresponding LPB payloads byte-for-byte after
wrapper decoding. The decoded SHA256 values for the skip widget, replay
selector, replay owner, and common CutScene chunk are respectively
`CEE2B2D522EF428D53F54A467DCAD75B9E5B1AB4B9DF52B99BD21272113741FC`,
`A4C7806E22AA956FAE4ACB8E1351BAE4109C0F6D5F093ACBB80C198E07B1A648`,
`18FBC24A732FEA85E4C43EA42CF6821B0550A4C312EA861C090B89867C0A7EC3`,
and `7EF33408C579F2D1EDE120D9751851BD39B77DD1B6CA6A0AA821B413FE11B4FD`.
Recovered-source identities and hashes are in `manifests/scripts.json` under
the matching `lua/scripts/` paths. The 1.23b client executable is pinned by
SHA-256:
`9341F2B4567440B310A4D494F5CC5599CA334BA51C8042247317FF466492F2E9`.
The PlaneMap hook also uses `gamedata/cutscene_common` resource
`39x569q9/7pqr75w5_7vxxvw.le.lpb` (LPB SHA256
`A5279136C0EE8F6EF2342FD22AF2B9CD12F9B6AFF5A4FEFF4BC0FC21367F5321`)
and `widget/desktopwidget_connector` resource
`n1635q/65rzqvun1635q_7vww57qvs.le.lpb` (LPB SHA256
`0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425`).
Both rows are pinned in `manifests/retail_lua_coverage.json` with their
decoded payload hashes (`retail_lua_coverage.json:814-827,25443-25456`).
