# Cutscene replay and skip client contract

The client uses two distinct UI paths: skip is bound to the currently playing
CutScene actor, while replay selection starts from an inn journal and resolves
static `cutReplay` rows. Neither path is a generic widget-open entitlement.

## Skip actor binding

`DesktopWidget` creates `CutSceneSkipWidget` and
`CutSceneSkipWarningWidget` as static slots 12 and 13
(`desktopwidget_connector.lua:4198-4202`). In the common CutScene method,
only play mode 1 with skip argument 1 passes the CutScene actor to
`showCutSceneSkip` before `_play`; the method calls `hideCutSceneSkip` after
playback (`cutscene_common.lua:886-902`). The desktop bridge stores that
actor as slot 12's `argActor`, and its hide path calls the widget's `clear`
(`desktopwidget_connector.lua:5760-5775`).

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

## Inn replay selection

`AreaBaseClass` creates `cutReplaySheet` only when `_isInn()` is true and
deletes it on inn finalization (`areabaseclass.lua:185-192`, `215-220`).
`DesktopWidget.openCutSceneReplaySelectWidget` opens
`Ask/JournalListWidget` in mode 7 (`desktopwidget_connector.lua:5093-5098`).
For an ordinary replay quest, that journal opens
`Ask/ReplayCutsceneSelectWidget` as a child; quest 110820 has a separate
direct-finish branch (`journallistwidget.lua:159-171`). The child scans
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
