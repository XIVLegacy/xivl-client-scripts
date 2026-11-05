# Limsa opening tutorial widget contracts

The [normal tutorial flow](limsa-normal-tutorial-flow.md) owns the separate
normal/withHQ device, scene, tribe-dialogue, camera and movement-lesson sequence.

`Man0l0.processTtrBtlMagic001` and `processTtrBtl002` both select the Actions
lesson, infoID 11, for the crafter and gatherer categories 29 and 39. They
wait for targeting before reading the supplied player's class state. The
separately callable `processTtrBtl003` displays success for every class, but
only its default and skill-7 branches continue to dialogue and tutorial
infoID 1. `processTtrBtl004` always continues through an inform dialog to
infoID 1.

These are authenticated source and original-bytecode contracts. Method
names do not establish invocation order, an actual receiver, historical
server selection, or successful rendering. Shared titles and controller
values are in [Tutorial widget values](tutorial-widget-vocabularies.md);
the [tutorial opener contract](tutorial-widget-opening-contract.md) owns
the desktop opener's branch and creation details.

## Input identity and locators

The extraction is `2012.09.19.0001`, game version `1.23b`. The selected
source was authenticated against [scripts.json](../manifests/scripts.json),
its archive against [private_lua_corpus.json](../manifests/private_lua_corpus.json),
and its original LPB and decoded payload against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Authentication selected members in memory; it did not regenerate or
validate the entire corpus.

| Man0l0 representation | Path or representation | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical source | `lua/scripts/quest/scenario/man/man0l0.lua`, 2533 lines | 51507 | `0F3165390756B2DAF960B978E3C05F094B1FF1A068E3468757A82A6AD3F25F39` |
| Retail LPB | `client/script/tp5rq/r75w9s1v/x9w/x9wjyj.le.lpb` | 20735 | `30352866FCA599CD199263E3E8253472C4230509C1E2B8C2755506690563F4EC` |
| Decoded Lua 5.1 | XOR-0x73 LPB payload | 20722 | `19A7EF9877A314ED296A918AEA709C57B2CF89B6F46A543C17D51A8E29DF17A1` |

The directly inspected desktop connector is the same authenticated member
and original payload identified in the
[Gridania input table](gridania-opening-tutorial-contract.md#input-identity-and-method).
Its canonical source SHA-256 is
`9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01`.
All child indices below are zero-based, PCs are one-based, and instruction
offsets address the decoded payload. An instruction is at
`instruction start + 4*(PC-1)`.

| Method | Canonical source lines | Root closure -> assignment PCs | Child / instruction start |
| --- | --- | --- | --- |
| `processTtrBtl001` | 1792-1894 | 123 -> 124 | 38 / `0x3B07` |
| `processTtrBtlMagic001` | 1898-2140 | 126 -> 127 | 39 / `0x3E44` |
| `processTtrBtl002` | 2144-2381 | 129 -> 130 | 40 / `0x454E` |
| `processTtrBtl003` | 2385-2464 | 132 -> 133 | 41 / `0x4BE7` |
| `processTtrBtl004` | 2468-2506 | 135 -> 136 | 42 / `0x4EA4` |
| `processInformDialogAsQuest` | 2510-2531 | 138 -> 139 | 43 / `0x5021` |

## Class predicates and selected lessons

A0 denotes the scenario receiver, A1 the supplied player-like receiver,
A2 an unused formal, and A3 the formal controller in the first three
methods. These are argument roles, without an established runtime identity.
Let `s` be the first result of `A1:getStateMainSkill()` and `c` the one
result retained from `A1:getSkillCategory(s)`.

Magic001 reads these at source lines 2043-2047 and Btl002 at 2294-2298.
Both apply the following ordered predicates, then map the branch value to
an infoID:

| Predicate | Branch value | infoID |
| --- | ---: | ---: |
| `c == 21` | 3 | 10 |
| Prior predicate false and `(c == 29 or c == 39)` | 4 | 11 |
| Prior predicates false and `s == 7` | 2 | 9 |
| Otherwise | 1 | 8 |

The exact comparisons are at Magic001
PCs122/126/128/132 and Btl002 PCs128/132/134/138. Their state and category
calls each retain exactly one result (`CALL C=2`). Thus category 21 takes
precedence over skill 7, as do categories 29/39.

The [shared state/category helper contract](gridania-opening-tutorial-contract.md#state-derived-category-selection)
owns the getter's two results, ordered numeric thresholds and the client
labels crafter/gatherer for 29/39. These predicates do not establish a
finite class enumeration or the supplied receiver's actual state.

Btl003 repeats the same class partition at source lines 2408-2423,
PCs18/21/22/26/28/32. Only branch values 1 and 2 enter its final dialogue,
open and mask block. Btl001 and Btl004 perform no class test.

## Waits, results and local continuation

Every selected scenario method returns zero values. All tutorial, success,
mask and target-wait call results are discarded. The sequences below
describe normal return from each call; they do not establish completion
of a native or external operation.

`processTtrBtl001` closes tutorial slot 12, starts `MAN0L010` with operand
1, performs cinematic setup including `_wait(2)`, cancels desktop mode 16,
sets mask `(true,true,true,false,true,4)`, opens infoID 6 with A3, reasserts
that mask and returns. Its final open is PC70 and return is PC86. It has no
final tutorial close.

`processTtrBtlMagic001` closes the tutorial, sets the same initial mask,
performs cinematic setup with `_wait(2)`, cancels mode 16 and opens infoID
7 with A3. It then sets `(true,false,true,true,true,4)`, closes event-mode
widgets, unlocks target-cursor and A1 player/lockon controls, and calls
`_waitForTargetTutorial(3205403)` at source line 2015, PC98. After that
call resumes it closes tutorial slot 12, waits 1, relocks those controls,
orders mode 16 and reads the class state. It cancels mode 16, sets
`(true,true,true,true,true,4)`, opens the selected infoID at PC193, sets
`(false,false,false,false,false,3)` and returns at PC218. The final lesson
has no later local close.

`processTtrBtl002` cancels mode 16, closes slot 12, waits 1, orders mode 16
and performs cinematic setup. It cancels mode 16, sets the all-true mask
with menu type 4, opens infoID 7 with A3, reasserts that mask, then sets
`(true,false,true,true,true,4)`. It uses the same event-widget close,
unlock, target wait and relock sequence as Magic001. Its target-wait
operand is also 3205403 (source line 2266, PC104). After class selection it
cancels mode 16, opens the selected infoID at PC184, sets the all-false
mask with menu type 3 and returns at PC210. It has no final tutorial close.

`processTtrBtl003` cancels mode 16, closes slot 12, requests
`openTutorialSuccessWidget(4305,true)` and waits 3 before reading the
class. Branches 1/2 order mode 16, say row 109 with speaker operand
1600179, cancel mode 16, call `openTutorialWidget(2,1)` at source line
2442, PC58, and set the all-false mask with menu type 3. Branches 3/4 skip
that entire block, including its mask. All branches return at PC74.

`processTtrBtl004` cancels mode 16, closes slot 12, requests the same
success presentation and waits 3. It calls
`A0:processInformDialogAsQuest(A0,110)` at source line 2490, PC19, cancels
mode 16 again, calls `openTutorialWidget(2,1)` at source line 2501, PC28,
and returns at PC29. It has no tutorial-mask call or final tutorial close.

In the last two methods, the literal tuple `(2,1)` is formal controller 2
and infoID 1, whose shared title is Moving the Camera. It is not infoID 2.
The opener replaces the formal controller with its stored controller
value. For selected infoID 1 it uses
`openWidgetYield(self,12,"Ask/TutorialWidget",alias,nil,false,type,1)`,
retains one widget result and, only when it is not nil, calls
`selectWidgetYield(self,widget,true)` and restores desktop focus. Selection
results are discarded; the opener returns zero values and does not close
the widget. InfoIDs 6/7/10 use this same yield branch, while 8/9/11 use the
non-selection branch documented in the
[shared opener contract](tutorial-widget-opening-contract.md).

The all-false mask requests the control/menu changes described in
[Gridania's mask contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup).
It does not establish native counter balance, close completion or a later
event selection. None of the five methods locally calls another of the
five.

## Success and inform helpers

`DesktopWidget.openTutorialSuccessWidget`, connector lines 9295-9306,
gets static widget 22 and calls the returned receiver's
`setData(4305,true)`. It does not test that receiver for nil, wait, close,
or return a value. The original binding is root PCs485 -> 486, child 161,
instruction start `0x1697B`: PC3 retains the lookup's one result, PC7
discards the setData result, and PC8 returns no values. This identifies
the static lookup operand, without authenticating a runtime widget object
or presentation completion.

`processInformDialogAsQuest` forwards its operands to
`desktopWidget:openPublicInformDialogWidget(A0,A0,110)`, discards that
helper's results, waits 2, then gets static widget 8 and calls `hide()`
without a nil test. In child 43, PCs6/9/13/15 identify the open/wait/lookup/hide
calls; PC16 returns no values. The public inform helper's nil guard and
tail-return behavior are already documented in
[the inform-dialog contract](job-grand-company-event-contracts.md#dont-hate-the-messenger-selector-paths).
The scenario proceeds to the wait and hide after a normal helper return,
including its failed-actor-check early return; it does not consume the helper's
show result or establish the actual static-widget identity.

## Reproduction and limits

Authenticate the archive, selected canonical members and original LPBs
against their manifests. Decode the wrappers in memory with
`tools/retail_script.py`, then parse the fixed Lua 5.1 header, full payload
and closure assignments with `tools/build_quest_contracts.py`. Check the
referenced original instruction operands, including `CALL C=2` for state
and category, `CALL C=1` for discarded widget results, and `RETURN B=1`
for each selected method. Check both category 29 and 39, the prior
category-21 branch, skill 7 after category failure, and the Btl003 skip
path. Retain no raw source, payload or instruction listing.

These checks establish static branch, argument, wait, result and cleanup
contracts. They do not join scenario A1 to a world-master player fetched
inside a helper, prove a stored controller producer ran, identify the
external dispatcher, establish target-wait completion or validate a fresh
character's accepted progression. Btl003 and Btl004 remain separately
callable methods, without a recovered historical selection edge.
