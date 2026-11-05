# Additional Gridania battle tutorial contracts

`Man0g0.processTtrBtlMagic001` independently selects infoID 10 for category
21, 11 for categories 29/39, 9 for skill 7 after those category tests fail,
and 8 otherwise. `processTtrBtl003` requests infoID 1 only for its default
and skill-7 branches. `processTtrBtl004` requests success presentation and
an inform dialog before infoID 1, without testing class or setting a
tutorial mask.

These are three separately callable source and original-bytecode contracts.
They do not establish their historical invocation order or a same-player
continuation from the [initial Gridania methods](gridania-opening-tutorial-contract.md).
In particular, Btl003's initial close does not establish that it followed
Btl002's final overlay.

## Inputs and call roles

The extraction is `2012.09.19.0001`, game version `1.23b`. The selected
`quest/scenario/man/man0g0.lua` and `widget/desktopwidget_connector.lua`
members were authenticated in memory against
[scripts.json](../manifests/scripts.json), their containing archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json), and original
installed LPBs and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). Canonical
source normalization replaces CRLF byte pairs with LF only. The
[Gridania input table](gridania-opening-tutorial-contract.md#input-identity-and-method)
owns their exact source, resource and payload pins. This selected-input
check does not reproduce full-corpus validation or regeneration.

A0 denotes the scenario receiver, A1 the supplied player-like receiver,
A2 an unused formal, and A3 the formal controller in Magic001. These are
operand roles, not authenticated runtime identities. Widget calls use the
global `desktopWidget`. All three methods return zero values and discard
their widget, mask, target-wait and presentation results. None reads a
tutorial ask result or tests an acceptance/cancellation value.

## Independent class predicates

Magic001 and Btl003 each retain the first result `s` of
`A1:getStateMainSkill()`, then one result `c` of
`A1:getSkillCategory(s)`. Each applies this ordered partition independently:

| First matching predicate | Local branch | Magic001 infoID | Btl003 continuation |
| --- | ---: | ---: | --- |
| `c == 21` | 3 | 10 | Return after initial close/wait and classification. |
| `c == 29` or `c == 39` | 4 | 11 | Return after initial close/wait and classification. |
| Previous predicates false and `s == 7` | 2 | 9 | Dialogue, infoID 1 and final mask. |
| All previous predicates false | 1 | 8 | Dialogue, infoID 1 and final mask. |

The [shared state/category contract](gridania-opening-tutorial-contract.md#state-derived-category-selection)
owns the getter's two-result order, category thresholds and client labels
crafter/gatherer for 29/39. This partition does not establish the supplied
receiver's state, a finite valid class enumeration, or a class-based external
method selector. Magic001's name does not restrict its local branches to
category 21. Btl004 has no state getter or class predicate.

## Magic001 order and waits

`processTtrBtlMagic001`, canonical source `:1271-1514`, executes this
conditional normal-return sequence:

1. Close tutorial slot 12 and set mask
   `(true,true,true,false,true,4)`. Start `MAN0G010` with operand 1, fade in
   with A1, call `setMusic(A0,A1,13,1)` and `A0:_wait(2)`.
2. Use world-master presentation operand 2300120 for camera aim, player
   look, two scheduler calls with operand 403087360, dialogue
   `A0:sayFreeDisplayName(2300120,A0,120)`, and camera cancellation.
3. Cancel desktop mode 16, open tutorial `(A3,7)`, set mask
   `(true,false,true,true,true,4)` and close event-mode widgets. Unlock the
   desktop target cursor, then A1's lockon and player controls. Call
   `desktopWidget:_waitForTargetTutorial(3201406)`.
4. After that call resumes, close slot 12, wait 1 on A0, lock the desktop
   target cursor, order mode 16, then lock A1's player and lockon controls.
   Read the state and category and select the lesson independently.
5. Cancel mode 16, set mask `(true,true,true,true,true,4)`, open
   `(A3,selectedInfoID)`, set `(false,false,false,false,false,3)` and return.

The final lesson has no subsequent local close request. The target-wait
integer is distinct from presentation operand 2300120. The native authority
`xivl-client-structs:docs/tutorial-control-native-contract.md`,
`_waitForTargetTutorial`, records a yielding int argument and no Lua return.
Its target-name interpretation remains INFERRED. A normal script continuation
does not authenticate a target object or establish live wait completion.

## Btl003 and Btl004

`processTtrBtl003`, source `:1732-1806`, cancels desktop mode 16, closes
slot 12 and waits 3 before reading state and category. Only branches 1/2
order mode 16, say `A0:sayFreeDisplayName(2300120,A0,110)`, cancel mode 16,
request `openTutorialWidget(2,1)`, and set the all-false/menu-3 mask.
Categories 21/29/39 skip that entire continuation, including its mask.
There is no success-widget request in this method. Every branch returns
zero values.

`processTtrBtl004`, source `:1886-1925`, cancels mode 16, closes slot 12,
calls `openTutorialSuccessWidget(4305,true)` and waits 3 on A0. It then calls
`A0:processInformDialogAsQuest(A0,90)`, cancels mode 16 again and requests
`openTutorialWidget(2,1)`. It returns zero values, without a tutorial-mask
call or final tutorial close.

The reached local `processInformDialogAsQuest`, source `:1928-1951`, calls
`desktopWidget:openPublicInformDialogWidget(A0,A0,90)` for this invocation,
discards its results, waits 2 on A0, obtains static widget 8 and calls
`hide()` on that result without a nil test. It returns zero values. The
[public inform helper contract](job-grand-company-event-contracts.md#dont-hate-the-messenger-selector-paths)
owns its failed-actor-check early return and otherwise tail-returned show
results. This caller proceeds after either normal return without consuming
those results.

The reached `openTutorialSuccessWidget`, connector `:9295-9308`, obtains
static widget 22 and calls its `setData(4305,true)` for this invocation.
It has no nil test, wait, close, or returned value. This is a static-widget
request, not another slot-12 creation. The two fetched static-widget
receivers are unresolved runtime objects.

## Shared widget and cleanup behavior

The tuples `(2,1)` mean formal controller 2 and infoID 1, Moving the Camera.
The [controller vocabulary](tutorial-widget-vocabularies.md) owns its title
and the stored input-device values. The
[shared opener](tutorial-widget-opening-contract.md#complete-opener-partition)
overwrites the formal controller with `D.work.tutorialDeviceType` before
computing its P/K alias. Literal 2 therefore does not prove gamepad content.

For the selected calls, the complete helper tuples, including receiver D, are:

| infoID | Ordered arguments | Local result/wait behavior |
| --- | --- | --- |
| 1, 7, 10 | `openWidgetYield(D,12,"Ask/TutorialWidget",alias,nil,false,type,infoID)` | Keep one result W. If `W ~= nil`, call `selectWidgetYield(D,W,true)` and restore focus. Discard selection results. |
| 8, 9, 11 | `openWidget(D,12,"Ask/TutorialWidget",alias,nil,true,type,infoID)` | Discard results, without a following explicit selection wait or focus restoration. |

Both opener paths return zero values. The exact nil test also admits false
or numeric zero to the selection call if returned as W. Creation can fail;
the creation/selection wait paths have no fixed timeout. The
[shared wrapper contract](gridania-opening-tutorial-contract.md#selected-widget-calls)
owns forwarding, enable/occupancy guards and the native boundary.

The [mask and close contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup)
owns the control/menu effects and `closeWidget(D,12,nil)` request. A final
mask neither closes the overlay nor proves balanced native lock counters.
A close request does not establish native closure completion. None of these
three methods locally invokes another battle tutorial method.

The [Limsa contract](limsa-opening-tutorial-contract.md) also selects infoID
1 in its Btl003/004 continuations, but requests success in Btl003 before its
class test. Gridania does not. The [Ul'dah contract](uldah-opening-tutorial-contract.md)
instead selects infoIDs 12 and 13 in its Btl003 and Btl004. These differences
describe local requests, without joining any city's methods into a
historical event order.

## Original-bytecode locators and verification

`tools/retail_script.py:decode_lpb` decoded the wrappers in memory.
`tools/build_quest_contracts.py:ChunkReader` consumed both complete Lua 5.1
payloads with header `1B4C75615100010404040800`. Root closure assignments
were checked against their actual method keys. Child indices are zero-based,
PCs one-based, and instruction starts address the decoded payload without
the LPB wrapper. A PC's byte offset is `start + 4*(PC-1)`.

| Method | Root closure -> assignment PCs | Child / instruction start | Selected evidence |
| --- | --- | --- | --- |
| Man0g0 Magic001 | 75 -> 76 | 22 / `0x2978` | PC98 target wait; PCs118/121 retain one skill/category result; comparisons at 122/126/128/132; PC193 opens the selected lesson; PC218 returns no values. |
| Man0g0 Btl003 | 81 -> 82 | 24 / `0x36C0` | PCs13/16 retain one skill/category result; comparisons at 17/21/23/27; PCs32/34 admit branch 1/2; PC53 opens `(2,1)`; PC69 returns no values. |
| Man0g0 Btl004 | 90 -> 91 | 27 / `0x3BAE` | PC12 requests success; PC19 calls the inform helper; PC28 opens `(2,1)`; PC29 returns no values. |
| Man0g0 processInformDialogAsQuest | 93 -> 94 | 28 / `0x3D2B` | PCs6/9/13/15 call public inform, wait, static lookup and hide; PC16 returns no values. |
| Connector openTutorialSuccessWidget | 485 -> 486 | 161 / `0x1697B` | PC3 retains static lookup result; PC7 discards setData results; PC8 returns no values. |

Authenticate the selected inputs, parse complete constant tables and follow
comparison skips and jumps before reproducing these paths. Focused checks
covered both categories 29/39, category-21 precedence over skill 7, the
skill-7/default branches, skill 22 within category 21, exact call/return
arities, ordered masks/waits and Btl003's skipped continuation. Mutating the
category comparison or Btl004 return arity caused the corresponding checks
to reject the changed contract. No retail source body, payload or instruction
listing was retained for this verification.

The remaining boundary is external selection, actual supplied and re-fetched
receiver/property/controller identities, native application of the requests,
callback delivery, target-wait completion and widget acceptance. No gameplay
execution or historical same-player progression is established here.
