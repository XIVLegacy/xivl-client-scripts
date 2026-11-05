# Ul'dah opening tutorial and Judge contracts

The [normal tutorial flow](uldah-normal-tutorial-flow.md) owns the separate
normal/withHQ device, scene, scheduler, camera and movement-lesson sequence.

`Man0u0` selects battle lesson infoID 10 for skill category 21, 11 for
categories 29/39, 9 for skill 7 after those category tests fail, and 8
otherwise. The category helpers label 29 as crafter and 39 as gatherer.
The same ordered predicates occur in `processTtrBtlMagic001` and
`processTtrBtl002`. Their method names do not select a class or establish
which method an external event invoked.

Two separate scenario methods have direct member calls on the result of
global `_getTutorialJudge()`. Matching declarations in `TutorialJudge` use
the actor supplied by the scenario as their talk receiver. They do not
operate the battle tutorial widgets or choose a battle continuation.
The getter's runtime class binding remains unproved. This contract covers those
two calls and `processTtrBtl001`, `processTtrBtlMagic001`,
`processTtrBtl002/003/004`, not every opening navigation method.

## Input identity

The inputs are extraction `2012.09.19.0001`, game version `1.23b`.
Selected canonical source members were authenticated against
[scripts.json](../manifests/scripts.json), their archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json), and original
retail LPBs and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Canonicalization replaces CRLF byte pairs with LF only.

| Input | Representation | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Man0u0 | `lua/scripts/quest/scenario/man/man0u0.lua`, 2630 lines | 53162 | `0CA29669ACAB5E7F5CCF12A5AE1F692552E51F308D9DC704E2B161E57907A71F` |
| Man0u0 LPB | `client/script/tp5rq/r75w9s1v/x9w/x9wjpj.le.lpb` | 21956 | `B954F9735DA9EF38401872562074482FFEB510DA44441FEBAA4FBA959052F0CC` |
| Man0u0 decoded Lua 5.1 | XOR-0x73 payload | 21943 | `850591E834AB2849DC8B53C949D5DB743E829264EA90CED0EA83C6EBBBFB1A4C` |
| TutorialJudge | `lua/scripts/judge/tutorialjudge.lua`, 62 lines | 1111 | `14D09A7F45C426DFCE5A5AA8AE9353473B37ED0ABEEE17F83A880BD50526B494` |
| TutorialJudge LPB | `client/script/0p635/qpqvs19y0p635.le.lpb` | 680 | `A1CACDAC405462E1FB1E9022D63381E4E4962FEDDB872A21A515B41BB6736423` |
| TutorialJudge decoded Lua 5.1 | XOR-0x73 payload | 667 | `03E0B3A697801725F3B5A001E0010600049F77F0FAAC19C1B1F37A133092F60B` |

The directly inspected helpers below are relative to `lua/scripts/`.
Their separate LPB and decoded-payload identities remain in the coverage
manifest. Authentication of selected members does not claim a new
full-corpus validation or decompilation.

| Helper | Bytes | Canonical source SHA-256 |
| --- | ---: | --- |
| `chara/charabaseclass_battle.lua` | 35086 | `CA7D9BD52320E8AA62ECD853A0CE8D9E2E0DDC76FC504729B501B14B9BFCD959` |
| `chara/charabaseclass_cliprog.lua` | 8202 | `EA04844921F8820562AFD172845CAB7BAF2DF235725D20AD179BB713754C87FD` |
| `widget/desktopwidget_connector.lua` | 660617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/ask/tutorialwidget.lua` | 34132 | `73980DDC53C4DF37A35537020B0DFED620D090F281CA3084BB19CEFB73817D4F` |

## Scenario and Judge roles

The scenario declares `Man0u0` with base `ScenarioBaseClass`; the Judge
declares `TutorialJudge` with base `JudgeBaseClass`. In the selected scenario
methods, A0 is the scenario receiver, A1 the supplied player-like receiver,
A2 a supplied actor and A3 the formal controller where present. These are
call roles, not authenticated runtime identities.

At `man0u0.lua:70-82`, `processEvent000_3` calls the
global `_getTutorialJudge` with **zero** arguments.
It retains one result, then calls its `man0u0processEvent000_3` member with
the fetched receiver followed by scenario A0, A1 and A2. The matching
`TutorialJudge` declaration at
`tutorialjudge.lua:15-33` uses the forwarded A2 as talk receiver, starts its
talk turn with operands `(2,A1)`, says scenario text 126 with trailing
numeric 0, and finishes the turn. That declaration and the scenario wrapper
return zero values; the wrapper discards any callee results.

`processEvent020_8`, `man0u0.lua:650-663`, performs the corresponding
lookup and forwarding. The matching declaration, `tutorialjudge.lua:36-62`, starts
the same talk turn, says scenario text 128 then 127, each with trailing
numeric 0, and finishes the turn. It returns exactly one value, **numeric
2**. The scenario retains and returns exactly one callee result, so this
declaration supplies 2 when it is the resolved method. This is not Boolean true,
a widget ask result, or evidence that an external caller accepted it.

The fetched receiver and forwarded talk receiver have distinct operand
origins; equality between them is not established. The selected Judge
declarations have no class test, widget call,
or call to a battle tutorial method. The native getter's implementation and
the actual objects supplied to either scenario event remain outside this
contract.

## Class predicates

Let `s` be the first result of `A1:getStateMainSkill()` and `c` the result
of `A1:getSkillCategory(s)`. Both class-selecting battle methods retain
exactly one result from each call and use these ordered predicates:

| First matching predicate | Local branch | Selected infoID |
| --- | ---: | ---: |
| `c == 21` | 3 | 10 |
| `c == 29` or `c == 39` | 4 | 11 |
| Previous predicates false and `s == 7` | 2 | 9 |
| All previous predicates false | 1 | 8 |

`charabaseclass_cliprog.lua:68-81` returns
`charaWork.parameterSave.state_mainSkill[1]` and `[2]` in that order.
`charabaseclass_battle.lua:53-77` returns category 0 for skill 0, then tests
the thresholds 39, 29, 21 and 1 in descending order, returning the matched
threshold or otherwise 0. For numeric inputs, category 29 therefore covers
`29 <= s < 39`, and category 39 covers `s >= 39`.
`isCrafter` and `isGatherer`, in the same helper at `:93-122`, compare the
main-skill category with 29 and 39 respectively. This does not supply a
finite valid class enumeration or prove a fresh character's property value.

`processTtrBtl001` has no class test and opens infoID 6.
`processTtrBtl003` repeats the four-way classification but opens infoID 12
only for local branch 1 or 2. Categories 21/29/39 still execute its initial
cancel, close and wait before returning. `processTtrBtl004` has no class
test and opens infoID 13.

## Selected widget arguments and results

All scenario calls target global `desktopWidget`. The Btl001,
BtlMagic001 and Btl002 methods pass A3 as the controller. Btl003 and Btl004
pass literal numeric 2. The reached
`DesktopWidget.openTutorialWidget`, connector `:9325-9400`, overwrites that
formal operand with `self.work.tutorialDeviceType`. Exactly numeric 2
selects alias `TutorialWidgetP` plus infoID; every other stored value selects
`TutorialWidgetK` plus infoID. A literal 2 at the scenario call therefore
does not prove gamepad text was selected.

In this table, `D` is the helper receiver, `type` its stored controller and
`alias` that computed name. Nil, false and true occupy distinct argument
positions.

| Selected infoIDs | Ordered helper tuple | Result handling |
| --- | --- | --- |
| 6, 7, 10 | `openWidgetYield(D,12,"Ask/TutorialWidget",alias,nil,false,type,infoID)` | Retains one widget result. If non-nil, calls `selectWidgetYield(D,widget,true)`, discards its results and restores focus with `changeFocusedWidget(D,D)`. |
| 8, 9, 11, 12, 13 | `openWidget(D,12,"Ask/TutorialWidget",alias,nil,true,type,infoID)` | Discards results. No explicit subsequent selection wait or focus-restoration call in this opener branch. |

The opener and all five selected scenario battle methods return zero values.
None reads `getAskResult` or branches on a cancellation value. For the
yielding path, a nil widget skips selection and focus restoration. A non-nil
widget restores focus even if selection reports failure.

The reached creation wrappers can reject invalid type, disabled type or
occupied root slots. `openWidgetYield` retries failed opening with
`_wait(0.1)` until the type's enable flag is exactly false. Following
accepted creation, it polls the creation command and looks the widget up;
that lookup may still yield nil. `selectWidgetYield` passes a nil timeout
to `selectWidgetTimerYield` and returns only its first result. The timer
helper waits 0.1 between attempts until `processWaitCallFunction` returns
exactly true or the widget is lost. Loss produces false. These paths have
no fixed timeout. The shared
[creation and selection lifecycle](gridania-opening-tutorial-contract.md#selected-widget-calls)
records the lower wrapper argument forwarding and its native boundary.

The selected class string is `Ask/TutorialWidget`. Its `TutorialWidget`
class uses `AskBaseClass`; the distinct `widget/tutorialwidget.lua` is not
substituted. The selected Pad/Keyboard methods for infoIDs 6/7/10 call
`initWidgetWithButton`; 8/9/11/12/13 call `initWidgetNoButton`.
The former sets modal and focusable true and enables the button grid.
The latter sets `autoAnim` true, focusable false and disables the grid.
The operate handler disables modal/focus/button interaction, requests
animation and sets base ask result 1. That value is not returned by the
selected opener. Neither animation nor a normal script return proves
rendering, input acceptance or completion.

InfoID titles and controller text keys are owned by
[Tutorial widget values](tutorial-widget-vocabularies.md). InfoID 13's icon
helper uses the first state-main-skill result of a player fetched anew via
`worldMaster:_getMyPlayer()`. Equality with scenario A1 is unproved.

## Local order and cleanup

`processTtrBtl001`, source `:1698-1801`, closes tutorial slot 12, starts
`MAN0U010` with operand 1, fades in with A1, sets music operands
`(A1,25,1)` and waits 2. After its selected camera/scheduler/dialogue
sequence with operand 1000010, it cancels desktop mode 16, sets mask
`(true,true,true,false,true,4)`, opens infoID 6 and reasserts that mask.
It has no final tutorial close.

`processTtrBtlMagic001`, `:1804-2037`, closes slot 12, sets the same
initial mask and performs the same cutscene, fade, music and wait setup.
Its dialogue uses operand 1000010 and text 150. It then follows the shared
target/lesson sequence below. `processTtrBtl002`, `:2040-2246`, instead
begins by cancelling mode 16, closing slot 12, waiting 1 and ordering mode
16. Its camera/scheduler/dialogue uses operand 1200024 and text 104, while
its camera-cancel operand is 1000010. These operands are preserved without
assigning an actor identity to them.

Both methods then execute this conditional normal-return sequence:

1. Cancel mode 16, open infoID 7, set mask
   `(true,false,true,true,true,4)` and close event-mode widgets.
2. Unlock the desktop target cursor and A1's lockon/player controls, then
   call `_waitForTargetTutorial` on the desktop with integer 3203301.
3. After that call resumes, close slot 12, wait 1, lock the target cursor,
   order mode 16 and lock A1's player/lockon controls.
4. Compute the class branch, cancel mode 16, open its selected lesson,
   set mask `(false,false,false,false,false,3)` and return.

The target-wait integer is distinct from both presentation operands.
`xivl-client-structs:docs/tutorial-control-native-contract.md`,
`_waitForTargetTutorial`, records a yielding int argument and no Lua return;
the target-name interpretation remains INFERRED.

`processTtrBtl003`, `:2249-2323`, cancels mode 16, closes slot 12 and waits
3 before classification. Only branch 1/2 then orders mode 16, displays
text 110 with operand 1000010, cancels mode 16, opens `(2,12)` and sets the
all-false/menu-3 mask. The other branches return without that final mask.

`processTtrBtl004`, `:2326-2365`, cancels mode 16, closes slot 12 and calls
`openTutorialSuccessWidget(4305,true)`. That connector helper at
`:9295-9308` gets static widget 22 and calls its `setData(4305,true)`;
it is not another slot-12 creation. The scenario waits 3, invokes its
`processInformDialogAsQuest` with scenario A0 and text 117, cancels mode 16
and opens `(2,13)`. Its local inform helper at `:2607-2630` opens the
public inform dialog, waits 2, obtains static widget 8 and calls `hide`.
No selected method waits on or reads a result from either static widget.

`closeTutorialWidget`, connector `:9403-9412`, requests
`closeWidget(self,12,nil)` and discards the result. The reached close path
requires a found/live widget before requesting closure, without establishing
native close completion. The final masks request control/menu changes;
they do not close slot 12 or prove balanced native lock counters.
The selected battle methods have no call edges to one another. A later
method's initial close is not proof it followed an earlier overlay.

## Bytecode locators and reproduction

`tools/retail_script.py` decoded the wrappers. The fixed Lua 5.1 reader in
`tools/build_quest_contracts.py` consumed each selected payload completely.
The header is `1B4C75615100010404040800`. Child indices below are zero-based,
PCs one-based, and instruction starts refer to the decoded payload without
the LPB wrapper. A PC's offset is `start + 4*(PC-1)`.

| Script / method | Root closure -> assignment PCs | Child / instruction start | Selected evidence |
| --- | --- | --- | --- |
| Man0u0 / processEvent000_3 | 18 -> 19 | 3 / `0x943` | PC2 getter has `CALL B=1 C=2`; PC7 forwards four operands and discards results; PC8 returns zero values. |
| Man0u0 / processEvent020_8 | 81 -> 82 | 24 / `0x1B60` | PC7 retains one result; PC8 returns exactly that result. |
| TutorialJudge / man0u0processEvent000_3 | 9 -> 10 | 1 / `0x120` | PCs4/9/11 start, say and finish on formal 3; PC12 returns zero values. |
| TutorialJudge / man0u0processEvent020_8 | 12 -> 13 | 2 / `0x1CF` | PCs9/14 say 128/127; PC18 returns literal numeric 2. |
| Man0u0 / processTtrBtl001 | 117 -> 118 | 36 / `0x391D` | PC69 opens infoID 6; PC85 returns zero values. |
| Man0u0 / processTtrBtlMagic001 | 120 -> 121 | 37 / `0x3C56` | PC98 target wait; PCs118/121 retain one skill/category result; comparisons at 122/126/128/132; PC184 opens the selected lesson. |
| Man0u0 / processTtrBtl002 | 123 -> 124 | 38 / `0x4345` | PC74 target wait; comparisons at 98/102/104/108; PC154 opens the selected lesson; PC180 returns zero values. |
| Man0u0 / processTtrBtl003 | 126 -> 127 | 39 / `0x496F` | PCs32/34 admit branch 1/2; PC53 opens `(2,12)`; PC69 returns zero values. |
| Man0u0 / processTtrBtl004 | 129 -> 130 | 40 / `0x4BF9` | PC12 requests success `(4305,true)`; PC28 opens `(2,13)`; PC29 returns zero values. |
| Connector / openTutorialWidget | 491 -> 492 | 163 / `0x16A56` | PCs1/2 replace controller; PC47 has `CALL B=9 C=2`; PC93 has `CALL B=9 C=1`; PC97 returns zero values. |

Authenticate inputs before inspecting these locators. Parse complete
constant tables and verify root closure assignments rather than identifying
methods by adjacent child numbers. Follow each comparison's skip and jump
semantics: the flattened decompilation alone does not establish the lesson
partition. Execute the selected paths with distinct category/skill inputs
and retain only assertion outcomes, identities and semantic locators.
Keep source bodies, decoded chunks and disassemblies outside the tracked
tree.

The remaining boundary is external selection: no selected source establishes
which scenario method a historical server invoked, its supplied receivers,
the fetched Judge object's native identity, target-wait completion, widget
acceptance or a later same-player event. Numeric return 2 and local method
names do not resolve that boundary.
