# Gridania opening tutorial widget contracts

`Man0g0.processTtrBtl002` selects tutorial infoID 11 for skill categories 29
and 39. The client labels those categories crafter and gatherer. Both request the
Actions lesson in `Ask/TutorialWidget`, with a skill-dependent icon. The
selected opener uses `openWidget` without a subsequent selection wait and
discards its results. The scenario performs no later local close request,
sets its final tutorial mask and returns no values. Creation success and slot
occupancy are not established by that return.

These are authenticated Lua and original-bytecode contracts. They do not
establish a historical server invocation, rendered widget acceptance, or the
event that follows the lesson. The shared titles/controller vocabulary is
owned by [Tutorial widget values](tutorial-widget-vocabularies.md).

The [additional battle tutorial contracts](gridania-battle-tutorial-branches.md)
own Magic001, Btl003 and Btl004. Their callable branches do not establish a
historical continuation from the two methods inspected here.

The [normal tutorial flow](gridania-normal-tutorial-flow.md) owns the separate
normal/withHQ device loop, scene requests, camera wait and one-value return.

## Input identity and method

The extraction is `2012.09.19.0001`, game version `1.23b`. The exact source
members were checked against [scripts.json](../manifests/scripts.json), the
containing archive against [private_lua_corpus.json](../manifests/private_lua_corpus.json),
and each installed resource and decoded payload against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). Canonical
source normalization replaces CRLF byte pairs with LF only. Selected member
authentication does not claim a new full-corpus validation or regeneration.

| Man0g0 input | Path or representation | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical source | `lua/scripts/quest/scenario/man/man0g0.lua` | 39838 | `BD367F6606CFF7EB4D43D76B15726B5075B3BF786E53C4B8EBF64D90DD65FD0B` |
| Retail LPB | `client/script/tp5rq/r75w9s1v/x9w/x9wj3j.le.lpb` | 15881 | `0180A8E3C55086B1B0C5CF2C17A7907846CE0B8854FB540BAE57298B6F03A8E5` |
| Decoded Lua 5.1 | XOR-0x73 payload of that LPB | 15868 | `A6770C85F650B05B0993704E7EEB8BB3456BB59A77A113BA9BA0D6B1DE43D0EF` |

The canonical scenario has 1951 lines. The directly inspected helper members
below are relative to `lua/scripts/`. Their matching LPB/payload coordinates
and separate hashes remain in the coverage manifest.

| Helper member | Bytes | Canonical source SHA-256 |
| --- | ---: | --- |
| `chara/charabaseclass_battle.lua` | 35086 | `CA7D9BD52320E8AA62ECD853A0CE8D9E2E0DDC76FC504729B501B14B9BFCD959` |
| `chara/charabaseclass_cliprog.lua` | 8202 | `EA04844921F8820562AFD172845CAB7BAF2DF235725D20AD179BB713754C87FD` |
| `widget/desktopwidget_connector.lua` | 660617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/ask/tutorialwidget.lua` | 34132 | `73980DDC53C4DF37A35537020B0DFED620D090F281CA3084BB19CEFB73817D4F` |
| `widget/ask/tutorialmodeselectwidget.lua` | 1133 | `4767E5C1D5647C37FB39FC6E36FC7FAA66ED8299FB189DBD1E8E87FB6FB59A02` |
| `widget/desktopwidget.lua` | 7929 | `5D3BFABF2E8A55EE2E64F607BDADA5F04046C9528E9E9ACA858E9AD9E232070A` |
| `widget/desktoputil.lua` | 614 | `27A6E37714093D2C344A5B4DBACB7ABD09DB2029E3DA277F19B3608D74EAB90F` |

`tools/retail_script.py` decoded the wrappers. The fixed Lua 5.1 reader and
instruction decoder in `tools/build_quest_contracts.py` consumed every
selected payload completely. The header is `1B4C75615100010404040800`:
little-endian Lua 5.1, four-byte integers, size_t and instructions, and
eight-byte floating numbers. Source statements were checked against call,
return, comparison and jump operands, including actual closure assignments.

All child indices below are zero-based, PCs are one-based within a prototype,
and offsets refer to the decoded payload, excluding the LPB wrapper.

## State-derived category selection

In the two scenario methods, A0 denotes the scenario receiver, A1 the supplied
player-like receiver, A2 an unused formal and A3 the formal controller operand.
These names describe call roles; they do not authenticate runtime identities.

Let `s` be the first result of `A1:getStateMainSkill()`, and `c` the result
of `A1:getSkillCategory(s)`. `processTtrBtl001` has no class test and opens
infoID 6. `processTtrBtl002` applies these ordered branches:

| Predicate | Local branch value | Selected infoID |
| --- | ---: | ---: |
| `c == 21` | 3 | 10 |
| `c == 29` or `c == 39` | 4 | 11 |
| Prior predicates false and `s == 7` | 2 | 9 |
| All prior predicates false | 1 | 8 |

`getStateMainSkill`, in `charabaseclass_cliprog.lua:68-81`, returns
`charaWork.parameterSave.state_mainSkill[1]` and `[2]` in that order.
The scenario retains only the first result. In
`charabaseclass_battle.lua:53-77`, `getSkillCategory` returns 0 for zero,
then tests `s >= 39`, `s >= 29`, `s >= 21` and `s >= 1` in that order,
returning the matched threshold; otherwise it returns 0. For numeric inputs,
category 29 therefore covers `29 <= s < 39`, and category 39 covers `s >= 39`.
This does not establish a finite supported class enumeration or property range.

The same helper's `getMainSkillCategory` forwards the state getter;
`isGatherer` compares its category with 39 and `isCrafter` with 29
(`:80-122`). These supply the client's labels. The property writer, actual A1
object and its state at character creation remain outside this trace.

## Selected widget calls

`DesktopWidget.openTutorialWidget(self, formalController, infoID)` is at
`desktopwidget_connector.lua:9325-9398`. It replaces the formal controller
with `self.work.tutorialDeviceType`. Exactly numeric 2 selects alias
`TutorialWidgetP` plus the infoID; every other value selects `TutorialWidgetK`
plus the infoID. That alias fallback does not establish controller value 1.

The tuples below include the helper receiver and preserve the nil operand.
`type` denotes the stored controller value.

| Earned infoID | Helper and ordered arguments | Result handling |
| ---: | --- | --- |
| 6 or 7; 10 as branch control | `openWidgetYield(self,12,"Ask/TutorialWidget",alias,nil,false,type,infoID)` | Retains one widget result. When non-nil, calls `selectWidgetYield(self,widget,true)`, discards its result and restores focus with `changeFocusedWidget(self,self)`. |
| 11; 8/9 as branch controls | `openWidget(self,12,"Ask/TutorialWidget",alias,nil,true,type,infoID)` | Discards results and performs no explicit selection wait or close in this opener branch. |

Both branches return zero values. Neither reads `getAskResult` or closes the
widget. For infoID 11, subsequent scenario work follows the normal return of
`openWidget`; this does not prove that an untraced native creation routine
cannot yield or that creation/rendering succeeded.

The directly reached creation wrappers at `:25105-25180` substitute the
desktop receiver for a nil parent and forward the selected tuple as
`commandCreateWidget(self,"Ask/TutorialWidget",false,self,true,alias,12,shown,type,infoID)`.
The final varargs preserve both controller and infoID. Index/type, enable and
root-occupancy checks can reject creation. `openWidgetYield` at `:25912-25970`
retries failed opens with `_wait(0.1)` until the type's enable flag is exactly
false. On accepted creation it polls the creation command, then looks up the
widget; the lookup can still return nil. These loops have no fixed timeout.

`selectWidgetYield` at `:25694-25730` calls its timer helper with a nil timeout.
While the widget is alive, that helper calls `processWaitCallFunction` until
it returns exactly true, otherwise waiting 0.1 before retrying. Loss of the
widget produces false. Only its first result is returned to the opener, which
ignores it and restores focus whenever the original widget result was non-nil.
These script outcomes are not user-acceptance or rendered-state evidence.

The named stored-value producer, `askTutorialDeviceType` at `:9415-9453`,
defaults to 1, opens the mode selector, conditionally reads its ask result,
closes it and stores/returns that value. The mode selector maps Button_1 to 2
and Button_2 to 1; `_isKeyboardOnlyTutorial() == true` disables Button_1.
This establishes a possible producer, not that it ran before this invocation.

## Actions lesson contents

The selected class-path operand is `Ask/TutorialWidget`, whose source defines
`TutorialWidget` with `AskBaseClass`. The [opening contract](tutorial-widget-opening-contract.md)
distinguishes that operand from runtime class/factory resolution and from
the separate `widget/tutorialwidget.lua`. `initAsk` stores infoID as an `integer8` field,
initializes `autoAnim` false and dispatches controller 2 to Pad text and
controller 1 to Keyboard text. Other controller values take neither text
branch despite receiving a K alias.

For infoID 11, Pad uses title key 9051 and body key 9053; Keyboard uses title
key 9051 and body key 9054 (`ask/tutorialwidget.lua:694-732,1247-1280`). Both
initialize the skill icon from the first state-main-skill result of a player
fetched again through `worldMaster:_getMyPlayer()`, then call
`initWidgetNoButton`. Pad also explicitly hides `Button_OK`; Keyboard has
no matching explicit visibility call in its selected method.

`getTutorial11SkillIcon` at `:1598-1633` returns 583 by default, 938 for
skill 39, 972 for 40 and 973 for 41. The apparent 29-36 decompiler branch
chain contains no alternate icon assignment in the original instructions.
These are selector values, without an inferred asset-name or live-skill join.

`initWidgetNoButton` at `:1784-1798` sets `autoAnim` true, `Focusable` false
and disables the button grid. The Shown handler requests `AnimationStart`
when `autoAnim` is truthy. The operate handler requests animation, disables
the grid and sets base ask result 1. No selected infoID-11 opener consumes
that result. Equality between the newly fetched player and scenario A1, actual
Shown/operate delivery and successful rendering remain unproved.

## Scenario order and cleanup

`processTtrBtl001`, canonical source `:1165-1266`, closes tutorial slot 12,
starts `MAN0G010` with operand 1, fades in with A1, sets music operands
`(A1,13,1)`, waits 2, and performs the selected camera/scheduler/dialogue
sequence. It then cancels desktop mode 16, sets tutorial mask
`(true,true,true,false,true,4)`, opens infoID 6 with A3, reasserts that mask,
and returns no values. It has no final widget-close call.

`processTtrBtl002`, source `:1517-1728`, follows this conditional normal-return
order:

1. Cancel desktop mode 16, close slot 12, wait 1, order mode 16 and perform
   the selected camera/scheduler/dialogue sequence using operand 1400004.
2. Cancel mode 16, open infoID 7, set mask `(true,false,true,true,true,4)`,
   close event-mode widgets, unlock the desktop target cursor and A1's
   lockon/player controls, and call `_waitForTargetTutorial(3201406)`.
3. After that call resumes, close slot 12, wait 1, lock the desktop target
   cursor, order mode 16 and lock A1's player/lockon controls.
4. Compute the category branch, cancel mode 16, open its selected infoID,
   set mask `(false,false,false,false,false,3)` and return no values.

The target-wait integer 3201406 is distinct from camera/scheduler operand
1400004. `xivl-client-structs:docs/tutorial-control-native-contract.md`,
`_waitForTargetTutorial`, records a yielding int argument and no Lua return;
its target-name interpretation remains INFERRED.

`setTutorialMask`, connector `:9106-9200`, handles five Boolean flags and a
menu type. Flags 1/2 change player/target-cursor control locks; flag 3 is
stored, flag 4 refreshes menu masks and flag 5 refreshes the static-7 mask.
Menu type updates static 1; a changed flag 4 or menu type refreshes static 15.
It compares stored flags before issuing lock/unlock calls and fetches its own
player through the world master. The final all-false mask requests unlocked
flags and menu type 3. It does not close slot 12, cancel tutorial mode, clear
`tutorialFlag`, or prove balanced native counters after the explicit calls.

`closeTutorialWidget`, connector `:9403-9410`, requests
`closeWidget(self,12,nil)` and discards its result. The close helpers require
a found/live widget before requesting closure. They do not prove native close
completion. The two scenario methods contain no local call edge to each other.
After requesting infoID 11, Btl002 does not select or invoke Btl003 and does not
locally close that overlay.

## Bytecode locators and reproduction

Root PCs bind each closure to its full method key. Instruction-start offsets
are sufficient to reproduce a selected PC as `start + 4*(PC-1)`.

| Script / method | Root closure -> assignment PCs | Child / instruction start | Selected evidence |
| --- | --- | --- | --- |
| Man0g0 / processTtrBtl001 | 72 -> 73 | 21 / `0x263F` | PC69 calls the opener with receiver/A3/6 and discards results; PCs65-85 contain its final mask/open/mask/return sequence. |
| Man0g0 / processTtrBtl002 | 78 -> 79 | 23 / `0x308B` | PC79 calls the target wait; PC99 retains only one state result; PC102 retains one category; PCs103/107/109/113 compare 21/29/39/7; PC159 opens 11 in branch 4; PC185 returns no values. |
| Connector / openTutorialWidget | 491 -> 492 | 163 / `0x16A56` | PCs1-2 overwrite the controller; 3-11 choose alias; jumps at 30/33/36 reach PC39, while 61/64/67 reach PC85. PC47 is `CALL B=9 C=2`; PC93 is `CALL B=9 C=1`; PC97 returns no values. |
| Connector / closeTutorialWidget | 494 -> 495 | 164 / `0x16D6C` | PC4 discards the close result; PC5 returns no values. |
| Connector / setTutorialMask | 464 -> 465 | 154 / `0x163D1` | Stored-flag comparisons and selected control/mask calls. |
| Chara battle / getSkillCategory | 14 -> 15 | 3 / `0xA72` | Ordered threshold comparisons at PCs5/10/15/20. |
| Chara client progress / getStateMainSkill | 11 -> 12 | 3 / `0x52E` | PC9 has `RETURN B=3`, returning two values. |
| Ask tutorial / Pad11 and Keyboard11 | 54 -> 55; 108 -> 109 | 15 / `0x1DB7`; 33 / `0x319B` | Exact title/body/icon and no-button initialization calls. |
| Ask tutorial / getTutorial11SkillIcon | 141 -> 142 | 44 / `0x3D3A` | Default 583 and only the 39/40/41 alternate values. |

Authenticate the selected source members and original LPBs before analysis.
Use `decode_lpb` from `tools/retail_script.py`, check the decoded size/hash,
and parse the fixed header and closure assignments with
`tools/build_quest_contracts.py`. Inspect the referenced PCs and their complete
constant tables; do not identify methods from adjacent prototype numbering or
truncated disassembler comments. The pinned unluac disassembler can provide an
independent listing as described in [Notice helper reproduction](notice-helper-contract.md#reproduction).
Keep payloads, listings and source bodies outside the tracked tree.

This establishes the selected static widget contracts. The native creation
command and creation-status implementations, actual receiver/property/controller
identities, callback scheduling, target-wait completion and later event/server
selection remain untraced. Named Btl003 metadata is not a causal continuation.
No conclusion extends these branches to other cities, all infoIDs, historical
server policy or accepted fresh-character progression.
