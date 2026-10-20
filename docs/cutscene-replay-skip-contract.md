# Cutscene replay and skip client contract

The official [Patch 1.21 notes](https://forum.square-enix.com/ffxiv/threads/39024),
2012-03-08, `[dev1301]`, named the inn-room replay tome The Unending Journey
and described selecting completed quests and replaying their event scenes.
That is documented intent; the client route below establishes the generic
selector and replay actor contract without identifying a historical spawned
tome or its server unlock state.

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
`getQuestCompleteID`. The two original bytecode bodies used by this contract
are `addQuestCompleteListForCutsceneReplay` (`root/proto16`, 76 code words,
304 instruction bytes, offsets `0x2A47`-`0x2B73`) and `getQuestCompleteID`
(`root/proto20`, 194 code words, 776 instruction bytes, offsets
`0x3547`-`0x384B`).

For numeric `questType` 32, `getQuestCompleteID` returns `(110820, 20)`
(`root/proto20` PCs 183-188, offsets `0x3823`-`0x3837`). The row builder
checks `cutReplaySheet` keys `110820 * 100 + i` for `i` from 1 through 20.
The original `TEST` and `EQ` instructions gate the row as follows:

In the type-32 path, `_isExistKey` is called at `root/proto16` PC 18,
offset `0x2A8F`, and its result is tested at PC 19, offset `0x2A93`. The
completion call is at PC 23, offset `0x2AA3`; PC 24, offset `0x2AA7`, uses
`EQ A=0` against the Lua constant `true`, and its following jump skips row
construction when the result is unequal (the jump is PC 25, offset
`0x2AAB`). The generic path repeats that exact comparison at PC 57, offset
`0x2B2B`, and PC 58, offset `0x2B2F`, with its skip jump at PC 59, offset
`0x2B33`. The PCs in this paragraph are zero-based, matching the preceding
contract locators.

| Value returned by `_isCompletedCutSceneReplayQuest` | Type-32 key exists | Type-32 key missing | Other included ID | Type-3 excluded ID |
| --- | --- | --- | --- | --- |
| exactly `true` | Add the row. | Do not call the API and add no row. | Add the row. | Do not call the API and add no row. |
| `false` | Add no row. | Do not call the API and add no row. | Add no row. | Do not call the API and add no row. |
| `nil` | Add no row. | Do not call the API and add no row. | Add no row. | Do not call the API and add no row. |

Thus the published row condition is exact boolean `true`, which includes the
ID when the completion API reports true. A missing `cutReplaySheet` key is
tested only by the type-32 branch; other included IDs are passed to the
completion API without a row-existence test. The type-32 row has `JournalType`
3, `JournalIndex` 0,
and text key 5108 (`root/proto16` PCs 3-38, offsets `0x2A53`-`0x2ADF`).

For all other returned ranges, the row builder iterates the first and second
values inclusively and uses text key 5106. When the first value is 110600, it
skips IDs 110821 through 110824 before calling the completion API
(`root/proto16` PCs 41-73, offsets `0x2AEB`-`0x2B6B`). The complete range
mapping from `getQuestCompleteID` is:

| `questType` | Returned pair | IDs tested by the row builder |
| ---: | --- | --- |
| 2 | `(110001, 110059)` | 110001-110059 |
| 3 | `(110600, 110971)` | 110600-110820 and 110825-110971 |
| 4 | `(111401, 111599)` | 111401-111599 |
| 5 | `(111601, 111799)` | 111601-111799 |
| 6 | `(111801, 111999)` | 111801-111999 |
| 7 | `(111200, 111219)` | 111200-111219 |
| 8 | `(111220, 111239)` | 111220-111239 |
| 9 | `(111240, 111259)` | 111240-111259 |
| 10 | `(111260, 111279)` | 111260-111279 |
| 11 | `(111280, 111299)` | 111280-111299 |
| 12 | `(111300, 111319)` | 111300-111319 |
| 13 | `(111320, 111339)` | 111320-111339 |
| 14 | `(110080, 110099)` | 110080-110099 |
| 15 | `(110060, 110079)` | 110060-110079 |
| 16 | `(110100, 110119)` | 110100-110119 |
| 17 | `(110180, 110199)` | 110180-110199 |
| 18 | `(110160, 110179)` | 110160-110179 |
| 19 | `(110260, 110279)` | 110260-110279 |
| 20 | `(110240, 110259)` | 110240-110259 |
| 21 | `(110300, 110319)` | 110300-110319 |
| 22 | `(110320, 110339)` | 110320-110339 |
| 23 | `(110360, 110379)` | 110360-110379 |
| 24 | `(110380, 110399)` | 110380-110399 |
| 25 | `(110400, 110419)` | 110400-110419 |
| 26 | `(110420, 110439)` | 110420-110439 |
| 27 | `(110440, 110459)` | 110440-110459 |
| 28 | `(110460, 110479)` | 110460-110479 |
| 29 | `(110480, 110499)` | 110480-110499 |
| 30 | `(110500, 110519)` | 110500-110519 |
| 31 | `(110821, 110824)` | 110821-110824 |
| 32 | `(110820, 20)` | 11082001-11082020 (`110820 * 100 + 1..20`) |
| Any other value | `(0, 0)` | 0 |

The native predicate evidence proves integer-key membership and publishes that
membership result unchanged as the Lua boolean: `0x00706370` forwards the ID
to `0x00764F90`, which reports true when the ID is found in the state
container at `+0x20`. The `0x01A3` producer rebuilds a key set with the same
published layout and replaces it on each packet, making it the leading
producer candidate. Actual owner equality between packet wrapper
`0x00576140`'s `[ECX+4]` and the predicate's resolved `GameEngine +0x220`
holder `+4` remains unproved. This establishes client-side membership only;
server award rules, persistence and a historical player's unlock state remain
unproved (`xivl-decomp:docs/event/cutscene-replay-state.md`, sections
`Predicate and state pointer`, `Incoming state producer`, and `Evidence and
limits`).

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
playback branches (`populacecutsceneplayer.lua:116-333`). The script unloads
each selected row before returning to the selector loop and closes the
selector after that loop exits. This establishes a client-side
replay route, not which book entries a historical player had unlocked,
whether a contributor's completion-bit packet is retail-equivalent, or a
safe direct open outside the inn owner path. No runtime playback or music
restoration is inferred from the static calls.

## Populace actor callback boundary

The original `PopulaceCutScenePlayer` prototype registers a `saveQuestId`
`integer32` work field, loads text data 9984 named
`populaceCutScenePlayer`, initializes that field to zero, and turns its ground
state off in `initForEvent` (`populacecutsceneplayer.lua:11-38`). Its
`_onTalkEvent` optionally lock-on targets the actor, calls
`processClientTalkEvent`, clears the target, and cancels desktop targeting
(`populacecutsceneplayer.lua:41-73`). `processClientTalkEvent` loops
`askExtendWidget(self, 1, 3, 1, 1)`; result 1 calls `processCutScenePlay`,
result 2 says text IDs 5 and 6 before asking again, and any other result exits
(`populacecutsceneplayer.lua:76-113`).

`processCutScenePlay` opens the replay selector and consumes the pair returned
by `selectCutSceneReplaySelectWidget`; it exits the selector loop when the
first value is exactly false or the selected ID is nonpositive, and processes
the row only when neither exit condition holds
(`populacecutsceneplayer.lua:116-148`).
For each accepted ID it saves `floor(selectedID / 100)`, loads the matching
`cutReplay` row, obtains the name through `_getData(selectedID, 0)` in
`getCutName`, and resolves columns 8 through 15 through the replay actor's
`getCutSceneReplayData` (`populacecutsceneplayer.lua:149-193,336-346`). A
`-202` argument selects the SNPC path and is converted with
`getSnpcActorClassID`; `-206` maps `getStateMainSkill() == 41` to 1 or 0,
`-207` resolves `getInitialTown`, and `-208` has no additional branch
(`populacecutsceneplayer.lua:177-219`). The method sets music 7/2, treats row
column 6 equal to 2 as the HQ choice, invokes the NQ or HQ cutscene starter,
then hides widget 14, fades in, resets `saveQuestId`, deletes the replay actor,
sets music 61/2, unloads the row, and returns to the selector loop; the
selector closes after that loop exits
(`populacecutsceneplayer.lua:220-331`).

This closes the actor-side callback and result contract. The method itself does
not test `_isInn`; inn ownership remains established by area setup and its
caller, and these static branches do not prove unlock state, packet
equivalence, persistence, or runtime playback behavior.

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
The `PopulaceCutScenePlayer` LPB
`729s9/wu7/uvupy975/uvupy9757pqr75w5uy9l5s.le.lpb` has SHA-256
`D165D71D84A9C629C96DADF1FCDC6BB0C7043D1677BADF81DF327697FBD0CFF0`; its
3,079-byte decoded payload is
`18FBC24A732FEA85E4C43EA42CF6821B0550A4C312EA861C090B89867C0A7EC3`,
and the reviewed decompile output is
`0080CAFDA1B0174612D464308A33E1CE4489CFBA6BAFB6C7ADFFF209E5E69747`; the
canonical source SHA-256 is
`0080CAFDA1B0174612D464308A33E1CE4489CFBA6BAFB6C7ADFFF209E5E69747`.
The `JournalListWidget` carrier is
`n1635q/9rz/0vpsw9yy1rqn1635q.le.lpb`, 15,297 bytes, with LPB SHA-256
`A15C8BF36E8124C5C4F5BE2EF189037894C98342C7C7EEF5889ADE16D975E6F3`; its
15,284-byte decoded payload has SHA-256
`549BC61FE3C206F1DD080057948A201F2824A785D039FB9F97878D8A31491D33`.
The canonical `lua/scripts/widget/ask/journallistwidget.lua` output is 37,468
bytes with SHA-256
`C103432E8671EE20493B4060D5D0958F608C967F211C2F73BEE8AEC6AF96DE87`
(`manifests/retail_lua_coverage.json:26208-26220`,
`manifests/scripts.json:15009-15012`).
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
