# Tutorial widget module selection and opening

`DesktopWidget.openTutorialWidget` selects the path operand
`Ask/TutorialWidget` for every infoID that reaches an open helper. Original bytecode divides
infoIDs 1-18 into a creation-and-selection wait group and an open-only group.
It returns no values and reads no tutorial answer. The separate
`widget/tutorialwidget.lua` is not selected by either literal opener call.
The two modules' shared `TutorialWidget` declaration does not establish a
shared runtime class or interchangeable initialization.

The [controller and content vocabulary](tutorial-widget-vocabularies.md) owns
the stored-controller override, K/P alias convention and Ask lesson titles.
The [Gridania contract](gridania-opening-tutorial-contract.md) owns that
scenario's calls and the shared creation/selection helper behavior. This page
completes the opener partition and distinguishes module selection from command
dispatch and native actor creation.

## Static module and creation relationships

All source paths below are relative to `lua/scripts/`.

| Module | Root require | Class declaration | Initializer |
| --- | --- | --- | --- |
| `widget/ask/tutorialwidget.lua` | `/Widget/Ask/AskBaseClass` | `TutorialWidget`, base `AskBaseClass` | `initAsk`, source 11-75 |
| `widget/tutorialwidget.lua` | `/Widget/WidgetBaseClass` | `TutorialWidget`, base `WidgetBaseClass` | `init`, source 11-39 |

In each original chunk, root PC3 performs the require and root PC7 performs
the two-argument `_defineClass` call. Root PCs9-10 bind child 0 to the
respective initializer. These are declarations and static dependencies, not
observations of a live object. The Ask initializer's data operands are
controller and infoID. The separate initializer also takes two data operands,
but a matching signature does not establish caller selection or shared content.
The normal shared initialization route is described in
[widget initialization](gil-shop-widget-opening.md#item-list-initialization);
applying it requires the actual instance to resolve the corresponding methods.

The desktop root requires `/Widget/DesktopUtil` and
`/Widget/DesktopWidget_connector` at original PCs3 and 6. The connector's
`openTutorialWidget`, canonical source 9325-9400, passes the literal
`Ask/TutorialWidget` at source lines 9353 and 9386. Its creation wrappers
forward that path to `commandCreateWidget`; the
[shared wrapper contract](gridania-opening-tutorial-contract.md#selected-widget-calls)
records the exact tuple, enable/occupancy checks and creation polling.

`commandCreateWidget` obtains a command using low ID 24228 and forwards the
path through a previously saved player method. Its two player lookups are
separate. The exact saved receiver, force operand, full varargs and result
forwarding are owned by
[commandCreateWidget forwarding](content-director-ui-contracts.md#commandcreatewidget-forwarding).
That lookup does not prove the returned command's runtime identity or dispatch.
The static actor path mapping and the independently recovered
[WidgetOpenCommand body](widget-open-command-boundary.md) establish a
conditional continuation: if that body receives `Ask/TutorialWidget`, it
requires `/Widget/Ask/TutorialWidget` and supplies basename `TutorialWidget`
to `_createActor`. The require path preserves the Ask distinction; the basename
alone does not.

The separate generic `DesktopWidget.createWidget`, source 61-102, also requires
`/Widget/` plus its supplied path before calling
`_createActor(nil,basename,false,operand,true,...)`. Here `operand` is its
third fixed parameter, counting the helper receiver as the first.
Original bytecode forwards the complete variadic tail and returns only the
first factory result. Supplying either `Ask/TutorialWidget` or
`TutorialWidget` to this helper constructs different require paths and the
same basename. This parameterized helper is not an attributable invocation
of the unprefixed tutorial module.

A bounded exact-reference search over the authenticated archive found only
the two class-name declarations and the two Ask path operands above. It found
no literal unprefixed tutorial require or creation caller. This does not
exclude dynamically assembled paths, external commands or native selection.
The first unsupported edge for that module is an actual caller selecting its
path. For the Ask opener, the selected path is established, while actual
command dispatch, factory class resolution and native creation acceptance
remain unsupported. Neither declaration identifies the created runtime type.

## Complete opener partition

Let `D` be the helper receiver, `t = D.work.tutorialDeviceType`, `i` the infoID
operand and `alias` the stored-controller alias described by the vocabulary.
The formal controller is overwritten before any branch. On normal execution:

| Exact numeric infoID | Operation and ordered arguments | Following local behavior |
| --- | --- | --- |
| 1, 2, 3, 4, 5, 6, 7, 10, 15 | `openWidgetYield(D,12,"Ask/TutorialWidget",alias,nil,false,t,i)` | Keep one result `W`. If `W ~= nil`, call `selectWidgetYield(D,W,true)`, then `changeFocusedWidget(D,D)`. Discard both results. |
| 8, 9, 11, 12, 13, 14, 16, 17, 18 | `openWidget(D,12,"Ask/TutorialWidget",alias,nil,true,t,i)` | Discard all results. No explicit selection wait or focus restoration follows. |
| Every value unequal to all listed numeric constants | Neither open call | No selection or focus call. |

The comparison list contains every integer from 1 through 18 exactly once.
There is no default open branch. Nil, false, zero and string `"1"` therefore
do not select infoID 1; the alias computation still precedes these comparisons.
This is a partition of the original equality tests, not a declaration that
every possible Lua operand is a valid input or that alias conversion cannot
fail or suspend.

Every normally reached final return has arity zero. The yield branch's nil
test is exact: false or numeric zero would also reach selection if returned
as its first open result. The helper does not validate that such a value is
a widget. A nil result skips both selection and focus. When selection returns
normally, focus restoration is requested regardless of its Boolean result.
It is a request to the focus helper, not proof of successful native focus.

The shared [creation and selection waits](gridania-opening-tutorial-contract.md#selected-widget-calls)
have no fixed timeout for this call. Selection uses the nil-timeout helper
and can end when the widget is no longer alive or its wait callback returns
exactly true. The opener ignores that distinction. It has no `getAskResult`,
cancel-result comparison, close or destroy call. Thus it returns neither an
accept/cancel result nor a creation-success flag. Any close or cleanup requires
another call path. No unconditional cleanup is established by this opener.
The explicit close helper is documented in the
[Gridania cleanup contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup).

## Original-bytecode locators and reproduction

The extraction is `2012.09.19.0001`, retail version `1.23b`. Authenticate the
archive against [private_lua_corpus.json](../manifests/private_lua_corpus.json),
the five selected source members against [scripts.json](../manifests/scripts.json),
and the original resources and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). The members
are the two tutorial modules, `widget/desktopwidget_connector.lua`,
`widget/desktopwidget.lua` and `widget/desktoputil.lua`. Their canonical source
pins are recorded in the
[vocabulary](tutorial-widget-vocabularies.md) and
[Gridania input table](gridania-opening-tutorial-contract.md#input-identity-and-method).
Selected-member authentication does not reproduce the full corpus check.

Use `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` and `instruction`. Check complete
payload consumption and root closure assignments. Child indices are
zero-based below. PCs are one-based; offsets exclude the LPB wrapper.

| Method | Root closure -> assignment PCs | Child / instruction start | Selected PCs |
| --- | --- | --- | --- |
| Connector `openTutorialWidget` | 491 -> 492 | 163 / `0x16A56` | 13/16/19/22/25/28/31/34/37 test 1/2/3/4/5/6/7/10/15; 59/62/65/68/71/74/77/80/83 test 8/9/11/12/13/14/16/17/18. |
| Same opener | Same | Same | 47: open CALL `B=9,C=2`; 48: exact nil EQ `A=1`; 53: selection CALL `B=4,C=1`; 56: focus CALL `B=3,C=1`; 93: open CALL `B=9,C=1`; 97: RETURN `B=1`. |
| Ask `initAsk` | 9 -> 10 | 0 / `0x7A4` | Root PCs3/7 require Ask base and declare TutorialWidget/AskBaseClass. |
| Separate tutorial `init` | 9 -> 10 | 0 / `0x4D7` | Root PCs3/7 require Widget base and declare TutorialWidget/WidgetBaseClass. |
| Desktop `createWidget` | 20 -> 21 | 2 / `0x4B7` | 16: dynamic require; 28: full VARARG; 29: factory CALL `B=0,C=2`; 35: one-result RETURN `B=2`. |

Reproduce the partition by following each equality and jump to the two call
sites and final return. Check all 18 numeric branches, a value unequal to
all constants, the exact nil-result branch, stored controller 2 versus other
values, full factory varargs and each result adjustment. Changing an infoID
comparison, module operand, open-result count, nil-test polarity or final
return count must change the corresponding assertion. No raw source,
payload or instruction listing is needed in the retained result.

These contracts stop at actual command/factory dispatch, callback scheduling,
native creation and focus acceptance, rendering and external event selection.
They do not establish a historical invocation of either tutorial module.
