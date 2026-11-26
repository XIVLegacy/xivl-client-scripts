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
completes the opener partition and its conditional focus request, and
distinguishes module selection from command dispatch and native actor creation.

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

## Lesson text methods and the answer button

In `widget/ask/tutorialwidget.lua`, the 36 methods `setTextPad1` to
`setTextPad18` and `setTextKeyboard1` to `setTextKeyboard18` each name exactly
one of two initializers. The call to it is the last instruction before the
method's only return, and no path through the method reaches a return without
that call. The call passes the receiver alone and keeps no result. The same
initializer serves both controller families of an infoID.

| infoID | Initializer in the Pad and the Keyboard method |
| --- | --- |
| 1, 2, 3, 4, 5, 6, 7, 10, 15 | `initWidgetWithButton` |
| 8, 9, 11, 12, 13, 14, 16, 17, 18 | `initWidgetNoButton` |

The first row is the same set of infoIDs as the creation-and-selection wait
group of the [complete opener partition](#complete-opener-partition). The
second row is its open-only group. This is a static agreement of two
separately declared comparison lists. It does not prove that one invocation
reaches both, or that the widget receives the infoID that the opener passed.
The [dispatch methods](normal-tutorial-panel-completion.md#initialization-and-selected-text-branches)
`setTextPad` and `setTextKeyboard` compare the infoID with each number from 1
to 18 and call the matching method. They have no default text method.

Three methods in this module name the `work` field `autoAnim`.

| Method | Use |
| --- | --- |
| `initAsk` | Requests false before it dispatches to a text method. |
| `initWidgetNoButton` | Requests true, then requests `Focusable` false through `setProperty` and calls `disableButtonGrid`. |
| `processUICommandDefault` | Reads the field on the [Shown command](normal-tutorial-panel-completion.md#button-requests-and-operation). |

`initWidgetWithButton` does not name the field. Its requests are in
[button requests and operation](normal-tutorial-panel-completion.md#button-requests-and-operation).
Under the ordinary bindings and normal completion, an open-only lesson
therefore ends initialization with `autoAnim` requested true, and a wait lesson
with the false request of `initAsk`. These are requests of the local methods,
without proof of stored work values, a delivered command or a visible button.

The inputs are the Ask tutorial identities in
[input identities and original locators](normal-tutorial-panel-completion.md#input-identities-and-original-locators).
Root PCs are one-based and bind the named child closure. Child indices are
zero-based. Code starts are decoded payload byte offsets.

| infoID | Pad: binding PC, child, start, call PC | Keyboard: binding PC, child, start, call PC |
| --- | --- | --- |
| 1 | 25, 5, `0x1355`, 10 | 79, 23, `0x2739`, 10 |
| 2 | 28, 6, `0x140D`, 21 | 82, 24, `0x27F1`, 21 |
| 3 | 31, 7, `0x1541`, 24 | 85, 25, `0x2925`, 24 |
| 4 | 34, 8, `0x1681`, 24 | 88, 26, `0x2A65`, 24 |
| 5 | 37, 9, `0x17C1`, 10 | 91, 27, `0x2BA5`, 10 |
| 6 | 40, 10, `0x1879`, 10 | 94, 28, `0x2C5D`, 10 |
| 7 | 43, 11, `0x1931`, 24 | 97, 29, `0x2D15`, 24 |
| 8 | 46, 12, `0x1A71`, 21 | 100, 30, `0x2E55`, 21 |
| 9 | 49, 13, `0x1BA3`, 10 | 103, 31, `0x2F87`, 10 |
| 10 | 52, 14, `0x1C59`, 22 | 106, 32, `0x303D`, 22 |
| 11 | 55, 15, `0x1DB7`, 26 | 109, 33, `0x319B`, 22 |
| 12 | 58, 16, `0x1F45`, 10 | 112, 34, `0x32F7`, 10 |
| 13 | 61, 17, `0x1FFB`, 22 | 115, 35, `0x33AD`, 22 |
| 14 | 64, 18, `0x2157`, 22 | 118, 36, `0x3509`, 22 |
| 15 | 67, 19, `0x22AB`, 21 | 121, 37, `0x365D`, 21 |
| 16 | 70, 20, `0x23E0`, 23 | 124, 38, `0x3792`, 23 |
| 17 | 73, 21, `0x2551`, 21 | 127, 39, `0x3903`, 21 |
| 18 | 76, 22, `0x2683`, 10 | 130, 40, `0x3A35`, 10 |

`initAsk` is child 0 at `0x7A4`. Its PC16 stores false, and its first text
dispatch call is at PC35. `initWidgetNoButton` is child 50 at `0x4281`, bound
at root PC160, and its PC2 stores true. `processUICommandDefault` is child 2
and reads the field at its PC5. A search of every prototype in the chunk finds
the constant `autoAnim` in these three only. Reproduce the census with
`tools/retail_script.py:decode_lpb` and the reader and instruction decoder in
`tools/build_quest_contracts.py`. For each text method, require one `SELF` that
names an initializer, locate its `CALL` with `B=2,C=1`, and require that every
path from entry to a `RETURN` passes that call.

## Conditional return-to-desktop focus request

The selected opener call supplies exactly `changeFocusedWidget(D,D)` and
discards all results. If that method resolves to the connector implementation
at canonical source 7055-7100, its four fixed parameters are adjusted to
`(D,D,nil,nil)`. There is no vararg tail or optional-argument default. With
normal method lookup and prerequisite returns, this call follows three steps:

1. Request `checkActor(D,D)` and take only its first result. Exact nil returns
   one false immediately. The result is used only for this guard; it does not
   replace the supplied target D. False or zero from a different implementation
   would pass the guard without local validation.
2. Read `_getKeyboardFocusedWidget(D)` afresh, taking one result F. If Lua
   equality reports `F == D`, return one true without calling the setter.
3. Otherwise tailcall `_setKeyboardFocusedWidget(D,D)`, preserving its complete
   result sequence. The opener discards that sequence just as it discards the
   two local Boolean returns.

The published [checkActor contract](item-use-command-flow.md#item-and-actor-operands)
returns nil for nil input or an exact-false `_isAlive()` result, otherwise the
original input. Applying it here still requires the actual binding and normal
completion of its lookup and native-named call. The focus helper does not
equate checkActor's result with the later focus read.

For this D,D call, the target compares equal to the receiver, so the helper
skips `setInputEnable`. Its omitted third argument is nil, so it also skips
`isShow` and `show`. These skips follow the original comparisons rather than
a current visibility or input-state observation. More generally, with receiver
D and supplied target T, a target unequal to D requests
`setInputEnable(T,true)` and discards its results. Only an exactly Boolean-true
third argument requests `isShow(T)`. Only an exactly Boolean-false first
visibility result then requests `show(T,true,S)`, where S is the fourth fixed
argument, including nil when omitted. An exactly Boolean-false first show
result returns one false before the focus read. Nil or zero from either call
does not satisfy that false comparison. The focus read follows these reached
requests and compares its first result with the original target T.

The comparisons are Lua equality, including applicable `__eq` behavior; they
do not authenticate raw object identity. A true local return does not establish
actual keyboard ownership, and a setter result is forwarded without a local
success test or readback. The contract stops at the dynamic getter/setter
requests. Actual receiver and parent identity, native focus semantics and
acceptance, callback scheduling and hardware input remain unestablished.
The normal panel's
[completion composition](normal-tutorial-panel-completion.md#composition-with-the-ask-poll-and-desktop-wait)
therefore reaches this conditional request, without proving native restoration.

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
| Connector `changeFocusedWidget` | 368 -> 369 | 122 / `0x12E29`, 37 words | 3: actor CALL `B=3,C=2`; 4: exact nil; 8: target/receiver equality; 13: exact-true optional argument; 17/23: exact-false visibility/show results; 28: fresh focus CALL `B=2,C=2`; 29: focus/target equality; 35: setter TAILCALL `B=3,C=0`. |
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

For the focus helper, the original prototype has four fixed parameters and no
varargs; its debug-line range 5472-5498 is distinct from canonical source lines.
PC12 requests input enablement with `B=3,C=1`; PC16 requests visibility with
`B=2,C=2`; PC22 requests show with `B=4,C=2`. PCs7/26 return one false and
PC32 returns one true. PC36 is the open-result return after the tailcall;
PC37 is the final zero-value return instruction. Check the selected caller's
receiver/target setup as well as its PC56 result discard, the nil-adjusted
optional arguments, ordered requests, first-result tests and tailcall result
preservation. Guard, getter/setter receiver and request-operand mutations must
be rejected. Synthetic replies check these local instruction paths, not native
focus state or a delivered tutorial invocation. The connector's exact original
LPB and payload pins are also recorded in the
[item-use input table](item-use-command-flow.md#evidence-and-reproduction).

These contracts stop at actual command/factory dispatch, callback scheduling,
native creation and focus acceptance, rendering and external event selection.
They do not establish a historical invocation of either tutorial module.
