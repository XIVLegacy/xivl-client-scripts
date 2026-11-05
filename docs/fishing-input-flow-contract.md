# Selected Fishing input workflow

`HarvestJudge.askInputWidget` returns the selected command, an input value,
and the desktop selection status, in that order. Fishing's supplied HP is a
separate input to phase 2. The widget's Cancel command does not finish
the ask and can move focus in phase 1. Selecting command 22709 completes the
ask through the same base-result value as other immediate command choices.

All local compositions require the described dynamic bindings and normal helper
returns. Assignments and UI calls are requests; they do not prove native
storage, focus, visibility or rendering. Repeated work reads remain fresh.

This contract joins one selected caller and widget. The
[gathering overview](gathering-marker-fishing-ui.md) owns marker and text
context. The [Mining](mining-input-widget-contract.md) and
[Felling](felling-input-widget-contract.md) contracts are separate controls.
The shared [Ask result state](ask-widget-result-state.md) and
[widget opening route](gil-shop-widget-opening.md#opening-and-selection-boundaries)
qualify their inherited and desktop dependencies.

## Caller arguments and Fishing command selection

Write the judge signature as
`askInputWidget(self,A1,A2,A3,A4,A5,A6,A7,A8,A9)`. A1 is the actor queried by
`isPlayer`, A2 is unused, A3 selects the gathering widget, and A4 is forwarded
as the phase. Fishing is the exact numeric command 22004 and the literal
path `Ask/FishingInputWidget`. Only an exactly-true first `A1:isPlayer()`
result reaches the desktop selection call. No additional class or controller
predicate appears in this selected judge branch.

The eight arguments after the widget path are exactly
`(primary,secondary,extra,22709,nil,A4,A8,A9)`:

| Judge predicate | primary | secondary |
| --- | ---: | --- |
| A4 equals numeric 1 | 22711 | nil |
| A4 differs from 1, A6 is exactly true, A7 is exactly false | 22711 | nil |
| A4 differs from 1, A6 is exactly true, A7 is exactly true | 22711 | 22708 |
| All other cases | 22708 | nil |

`extra` is nil only when A5 equals numeric zero; otherwise it is 22710.
Thus nil and false A5 both select 22710. Numeric 1 in A6 does not satisfy
its Boolean test, and nil A7 satisfies neither Boolean branch. A4 is forwarded
without normalization: a non-1 value chooses the latter command branches,
but only numeric 2 selects the widget's phase-2 setup. A9 is the rare-effect
operand. These identifiers and flags do not establish gameplay meanings for
the unused or externally supplied positions.

The adjacent selected judge helpers have different argument roles:

| Judge method | Fishing selection and forwarded arguments | Normal local return |
| --- | --- | --- |
| `openInputWidget(self,A1,A2,A3,A4)` | Exact-true player test and A3=22004 call `openEventModeWidgetYield(desktopWidget,"Ask/FishingInputWidget",A4)`. | Exactly one first helper result, default false if no branch is selected. |
| `orderInputWidget(self,A1,A2,A3,A4,A5)` | Exact-true player test and A5=22004 call `updateEventModeWidget(desktopWidget,"Ask/FishingInputWidget",A3,A4)`. | Exactly one first helper result, default false. |
| `closeInputWidget(self,A1,A2,A3)` | Exact-true player test and A3=22004 call `closeEventModeWidget(desktopWidget,"Ask/FishingInputWidget")`. | Exactly one first helper result, default false. |

The open wrapper forwards
`openWidgetYield(D,4,"Ask/FishingInputWidget",nil,nil,false,A4)`, where D is
its desktop receiver. It returns false for a nil first open result and true
for every nonnil first result. The selected initialization therefore supplies
A4 as the first `initAsk` data argument, used for the optional grade text.
The creation polling and command/factory boundaries remain those of the
linked opening contract. These separate judge methods do not establish their
historical event order or the identity of an actual constructed instance.

## Phase setup and input completion

`FishingInputWidget.initAsk` requests HP range/value 0/100/100 and slider
value 50, attempts stored HP=100, current/previous angle=0 and phase/focus=0,
and requests `setInputContorlFlag(false)`. It registers the named cancel,
operate, selector and slider-focus commands. The misspelled inherited flag
setter is the one described by the Ask result contract. If that binding and
storage apply, later base-result setters and resetters do not request whole
widget input enablement while the flag reads false.

The event initializer obtains `getWidget(D,4,path)`. For a nonnil first
result W it requests, in order, `resetBaseAskResult(W)`,
`setAskParameter(W,...)` with the complete tail, and `show(W,true,true)`.
It discards each result and returns W. In particular, a false
`setAskParameter` result does not make this wrapper refuse selection.

The tail maps to widget parameters as follows: slots 1-5 are command rows,
slot 6 is phase, slot 7 is supplied HP, and slot 8 is rare-effect control.
`setAskParameter` attempts command count zero, calls `setCommandList` for all
five slots, enables the command list, and resets current angle to zero.
The selected row helper counts every nonnil command, including false or zero.
A fresh command-count read equal to zero then returns false. Otherwise it
sets focus=1 and requests angle-gauge focusability false before phase setup:

| Phase operand | Selected requests and assignments |
| --- | --- |
| Numeric 1 | If the fresh previous phase is 2, requests the previous effect and `PhaseBtoA`. Sets phase=1 and requests phase-A visibility, slider focusability/enabled state, slider focus and help. The supplied HP does not replace stored HP. |
| Numeric 2 | Freshly tests phase=1 for `PhaseAtoB`, then phase=2 for the previous effect. Stores supplied HP if nonnil, otherwise numeric zero, sets phase=2 and requests command focus. False and zero HP are preserved as supplied operands. |
| Every other value | Performs neither phase branch and makes no local phase assignment. |

A nonnil rare operand selects the applicable phase's start request only for
exact true; every other nonnil value selects stop. Nil makes no rare-effect
request. Every normally completed nonzero-command path then calls
`displayBait()` and returns true, including an unrecognized phase operand.
Bait display queries the local player and its equipped slot 6. A nil item
requests the bait grid hidden; a nonnil item supplies the icon, name and stack
presentation. Neither outcome identifies a catch or proves native readback.

In `processUICommandEvent(self,A1,A2,A3,A4,A5)`, A3 is the command string,
A2 is the control identifier, and A4 is the supplied row/selector operand.
An exactly-true `isAskFinish()` result returns immediately. The selected
completion paths are:

| Input branch | Local continuation |
| --- | --- |
| `UILuaCommands.Cancel` | In phase 1, a keyboard-focused control other than `Slider_PhaseA` requests slider focus and help; the slider-focused case requests `focusFirstCommand(true)`. Other phases make no such request. All return without setting a base result, changing the chosen command or closing. |
| `ApplicationCommands.Operate` | Only phase 1 with keyboard focus exactly `Slider_PhaseA` requests `focusFirstCommand()`. It does not finish the ask. |
| `UILuaCommands.Operate`, A2=`TemplateButton_Power`, focus=2 | Requests `stopAngleGauge()`. Only an exactly-true first result then requests base result 1 and gauge focusability false. Focus is set to zero even for a normally returned non-true stop result. |
| Other `UILuaCommands.Operate`, A4 nonnil, focus not 2 | Stores the row, obtains one `getCommandId(row)` result, stores that command, collapses the list and requests command help. Phase 1 disables slider focusability/enabled state and requests base result 1. In other phases, only command 22708 satisfies `isUseGauge`: it sets focus=2 and starts the gauge. After that gauge start, stored HP differing from zero is passed to `updateHP`, then stored HP is set to zero, even if that helper normally returns false. Every nongauge command instead requests base result 1 immediately. |

The power-control branch is consumed even when focus is not 2. Row operations
while focus=2 are ignored. Command 22709 is not translated to a false status,
zero command, nil input or base result -1 in these selected methods. It is a
nongauge command and reaches the immediate completion route. The result still
contains its command and the phase-dependent input value.

`startAngleGauge` resets current angle to zero before the focus/start
requests. `stopAngleGauge` requests `Stop_PowerGauge`, passes the open
`RenderTransform.AngleZ` getter results to `tonumber`, and keeps one conversion
result. Positive and negative values request `_math.floor(angle+0.5)` and
`_math.floor(angle-0.5)` respectively; zero does not replace the stored angle.
It compares fresh stored angle and good-range reads for the sound request,
then returns true. Conversion/comparison failures can prevent completion.
This is UI input conversion, not a fishing success or probability formula.

`orderInputWidget` reaches `updateAskParameter(HP,effectFlag)` on the looked-up
widget. That method discards `updateHP(HP)` results, then requests
`displayEffect()` only for exact true effectFlag. A numeric HP outside 0..100
returns false from `updateHP`; this does not suppress the later effect request.
Unlike its Mining/Felling counterparts, Fishing's `updateHP` has no local
`work.hp` assignment. Its valid path requests only the progress-bar value.
The desktop update wrapper returns true after any normal nonnil-widget update,
including such a refusal, and false when its widget lookup returns nil.

## Wait, result width and cleanup

`selectEventModeWidgetYield` initializes W, then calls
`selectWidgetYield(D,W)` without its optional show operand. That helper calls
`selectWidgetTimerYield(D,W,nil)` and retains only its first result. With no
timeout, the timer helper rejects an exactly-false `_isAlive()` result,
otherwise polls `processWaitCallFunction()` for exact true with `_wait(0.1)`
between incomplete polls. The inherited Ask callback reads base-result
completion, as described by the linked Ask contract. Base result 1 finishes
that predicate if read back; completion is not a server success result.

| Boundary | Actual result adjustment |
| --- | --- |
| Fishing `getAskResult`, stored phase=1 | Returns `chosenCommand` followed by the complete open result sequence of `getControlProperty(self,"Slider_PhaseA","Value")`. Zero getter values produce only the command; one nil produces command,nil. |
| Fishing `getAskResult`, every other phase | Exactly `chosenCommand,currentAngle`. |
| Desktop selection wrapper, W nil or selection's first result exactly false | Returns exactly one false, without reading widget results. |
| Desktop selection wrapper, other normal selection result | Returns literal true followed by the complete open `W:getAskResult()` sequence. No widget acceptance Boolean is inserted. |
| HarvestJudge selection call | Requests exactly three values, nil-padding missing values and discarding extras. If they are `status,command,input`, returns `command,input,status`. Only status exactly false replaces command and input with numeric zero. |

Thus normal wrapper failure becomes exactly `(0,0,false)`. An unsupported
judge command or non-true player test also returns that tuple without a
selection call. A normally returning substituted wrapper with nil or zero
status would preserve its adjusted command/input; the judge's test is not
Lua truthiness. The pinned wrapper itself supplies Boolean status on its
normal paths. Extra phase-A getter results are cut off by the judge's
three-result request, not by Fishing's producer. Missing input becomes nil,
not numeric zero, on a true-status path.

Neither the selected ask wrapper nor Fishing's completion/cancel handler
closes the widget. Cleanup requires a separate close call. The explicit judge
close selects category 4 and the same literal path, and tail-forwards through
`closeEventModeWidget` to `closeWidget(D,4,path)` before the judge keeps one
result. A nil lookup returns false. A nonnil lookup reaches
[closeWidgetDirect](content-director-ui-contracts.md#closewidgetdirect-behavior)
and its
[conditional recursive and owner cleanup](content-director-ui-contracts.md#closewidgetlocal-cleanup-request).
Those published contracts qualify the normal true return as a completed Lua
close request, rather than proof of destruction or successful cleanup.
No subsequent judge return here selects another event or establishes how an
external caller consumes the command/input/status tuple.

## Source identity and reproduction

The extraction is retail 1.23b `2012.09.19.0001`. Read only selected archive
members in memory, authenticating the archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json) and the member
identities against [scripts.json](../manifests/scripts.json):

| Canonical member under `lua/scripts/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `judge/harvest/harvestjudge.lua` | 9902 | `e097de09274574430d14fcafe02ce520cca1ba14ccf8cc42c57413d5cd9ca814` |
| `widget/ask/fishinginputwidget.lua` | 25416 | `89c780d8f680438b58bb920257303bdcd5366ac211baaa7da573b5faee3fc14a` |
| `widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |

The judge's original resource is
`0p635/29so5rq/29so5rq0p635.le.lpb`, SHA-256
`2797ec20a0f9ba01633332ddcc30c72154420f591832c234ff1b7f90b1c5d8c5`.
Fishing's is `n1635q/9rz/41r21w31wupqn1635q.le.lpb`, SHA-256
`4c2dd967f7b581ab5fadb39df1567ded1b2fda4bc8e80ad4d6da2211ac66cf76`.
The connector's is `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns their
sizes and decoded-payload identities. Authenticate both representations, decode
with `tools/retail_script.py:decode_lpb`, and parse to complete consumption
with `tools/build_quest_contracts.py:ChunkReader/instruction`.

Prototype indices and PCs below are zero-based. Offsets locate the start of
the prototype's instructions in the decoded payload; PC n is at offset+4*n.
Canonical source ranges include the method binding for the two selected
resources. Connector entries use their original root child identities.

| Resource/method | Canonical source | Child / offset | Decisive PCs |
| --- | --- | --- | --- |
| Judge `openInputWidget` | 69-108 | 4 / `0x43A` | 3 exact-player test; 29 Fishing call, B=4,C=2; 34 one-value return |
| Judge `orderInputWidget` | 111-153 | 5 / `0x5A3` | 32 Fishing update, B=5,C=2; 37 one-value return |
| Judge `askInputWidget` | 156-265 | 6 / `0x715` | 4-56 command predicates; 58-59 actor call/test; 110 Fishing call B=11,C=4; 114 false test; 122 RETURN B=4 |
| Judge `closeInputWidget` | 383-419 | 9 / `0xE21` | 26 Fishing close, B=3,C=2; 31 one-value return |
| Fishing `initAsk` | 11-204 | 0 / `0x381` | 103-149 HP/angle/phase/focus/slider and flag requests |
| Fishing input handler | 243-417 | 3 / `0xAE3` | 5-24 Cancel; 38-57 power; 59-121 row selection and completion |
| Fishing `setAskParameter` | 750-924 | 13 / `0x1AAF` | 30-33 count refusal; 39/93 phases; 118-126 HP and phase; 143 bait request |
| Fishing `getAskResult` | 927-949 | 14 / `0x2051` | 9 CALL C=0 and 10 RETURN B=0; 16 RETURN B=3 |
| Fishing `stopAngleGauge` | 691-747 | 12 / `0x189C` | 8 CALL C=0; 9 CALL B=0,C=2; 10/19 sign tests; 49 true return |
| Fishing `updateHP` | 952-968 | 15 / `0x213A` | 0-4 range predicates; 10 progress request; no SETTABLE |
| Connector open/init/update | Selected wrappers | 551 / `0x3376F`; 556 / `0x33A9E`; 557 / `0x33B5A` | Open PC6 B=0,C=2; init PC10 B=0,C=1; update PC9 B=0,C=1 |
| Connector selection | Selected wrapper | 554 / `0x338F9` | 4 init; 9 select C=2; 11 false test; 14 one false; 17 getAskResult C=0; 18 RETURN B=0 |
| Connector selection wait | Shared wait | 539 / `0x32BE7`; 540 / `0x32CFA` | Yield PC27 nil-timeout call C=3; timer PC11 alive false, PC16 callback true, PC37 wait |
| Connector close | Explicit close | 553 / `0x3389F`; 527 / `0x32261` | Event PC3 tailcall B=4,C=0; close PC14 tailcall to direct close |

Bounded original-bytecode fixtures checked the command partition, strict
actor/Boolean predicates, explicit nil operands, phase/HP requests, Cancel
navigation versus quit completion, gauge completion, wrapper failure width,
open getter results and the judge's three-slot adjustment. Negative controls
rejected a changed command constant and a truncated phase-A getter result.
These ordinary-table fixtures use explicit mock helper results. They do not
model native storage, metamethods, conversion/coercion beyond the supplied
numeric cases, callback delivery or actual actor/widget identity.

The first unsupported edges are actual instance selection and native property
readback/application. Historical event selection, server validation, fish or
catch identity, yield, success/probability formulas and settlement remain
outside this contract.
