# Tutorial controller and Ask widget values

The recovered Ask/TutorialWidget accepts controller value 1 for its keyboard
text branch and 2 for its gamepad text branch. The mode selector assigns
result 2 to Button_1 and result 1 to Button_2. It disables Button_1 when
`worldMaster:_isKeyboardOnlyTutorial()` is exactly true. Its operate handler
copies the supplied operation argument into the base ask result.

`DesktopWidget.askTutorialDeviceType` defaults to 1, stores the selected
result in `tutorialDeviceType`, and returns that value. The tutorial opener
uses the stored type in place of its formal controller argument and builds
the alias `TutorialWidgetK` or `TutorialWidgetP` followed by the infoID.
These selected consumers establish the two values, not a complete enumeration
of every native input-device domain.

`_isKeyboardOnlyTutorial` returns one Boolean, separate from the numeric
controller choice. The
[native keyboard-only test](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/talk-native-contract.md#keyboard-only-tutorial-test)
in `xivl-client-structs:docs/talk-native-contract.md` owns its callback,
refresh, field test and exact binary identity. Its constructor-based true
result depends on the `INFERRED` receiver identity as
`Application::Main::RaptureElementContainer` and the absence of an unknown
store through a computed address. This does not establish an always-true
runtime result or a fresh character's predicate value. The property meanings
and the object behind `0xC0000024` remain unknown.

The [normal city tutorial contracts](opening-normal-tutorial-city-contracts.md#shared-local-sequence)
compare separate global predicate reads around device selection and wait 3.
The selector's predicate reference at
`widget/ask/tutorialmodeselectwidget.lua:20` is separate from those scenario
reads. Equal scenario samples do not establish that the selector saw the
same value, or that the stored `tutorialDeviceType` later read by the opener
equals the local selector result. The button restriction does not validate
that result as 1 or 2 or establish actual widget selection, hardware
availability or accepted input.

The content values below belong to `widget/ask/tutorialwidget.lua` and its
infoID dispatchers. The distinct `widget/tutorialwidget.lua` declares the
same class name with a different base and must not be merged into this table
without its own content trace. English title text is from
`xivl-client-data:csv/xtx__text_ui.csv`, column 1. The row for NPCs also
contains an encoded icon control.

| infoID | Title key | English title text | Pad / keyboard method starts |
| ---: | ---: | --- | --- |
| 1 | 9001 | Moving the Camera | 399 / 952 |
| 2 | 9006 | Getting Around | 419 / 972 |
| 3 | 9011 | Targeting Friendly NPCs | 453 / 1006 |
| 4 | 9016 | Speaking to Friendly NPCs | 490 / 1043 |
| 5 | 9021 | The Main Menu | 527 / 1080 |
| 6 | 9026 | Active & Passive Modes | 547 / 1100 |
| 7 | 9031 | Targeting Enemy NPCs | 567 / 1120 |
| 8 | 9036 | Engaging in Combat | 604 / 1157 |
| 9 | 9041 | Battle Actions | 638 / 1191 |
| 10 | 9046 | Casting Spells | 658 / 1211 |
| 11 | 9051 | Actions | 694 / 1247 |
| 12 | 9056 | Tactical Points (TP) | 735 / 1283 |
| 13 | 9061 | Weaponskills | 755 / 1303 |
| 14 | 9071 | NPCs | 791 / 1339 |
| 15 | 9076 | NPC Linkpearls | 827 / 1375 |
| 16 | 9081 | Journal | 861 / 1409 |
| 17 | 9006 | Getting Around | 898 / 1446 |
| 18 | 9086 | Defeat the enemy! | 932 / 1480 |

Slot 17 is occupied. Its Pad and Keyboard methods reuse slot 2's title 9006
and bodies 9008/9009, obtain the initial town, and call getTutorial2TownNPC.
Slot 2 calls initWidgetWithButton; slot 17 calls initWidgetNoButton. The
supported distinction is the button initialization, not a different title
or a missing numeric value. No editorial enum identifier is assigned here.

The infoID dispatchers are at lines 127-396 and the mode dispatcher at
11-75. The desktop controller helper is at
`widget/desktopwidget_connector.lua:9415-9464` and opener type/alias selection
at 9325-9337. The [opening contract](tutorial-widget-opening-contract.md)
reconstructs the complete yield/non-yield partition against original bytecode
and distinguishes the selected path from runtime class/factory resolution.

The [Gridania opening contract](gridania-opening-tutorial-contract.md#selected-widget-calls)
resolves the directly selected infoID 6/7/11 paths against original bytecode,
including controller override, argument forwarding and selection-result limits.

All scripts below are extraction `2012.09.19.0001`, normalized by the
canonical CRLF-pair-to-LF rule and authenticated against
`manifests/scripts.json` before inspection:

| Script under lua/scripts | Bytes | SHA-256 |
| --- | ---: | --- |
| widget/ask/tutorialwidget.lua | 34132 | `73980DDC53C4DF37A35537020B0DFED620D090F281CA3084BB19CEFB73817D4F` |
| widget/ask/tutorialmodeselectwidget.lua | 1133 | `4767E5C1D5647C37FB39FC6E36FC7FAA66ED8299FB189DBD1E8E87FB6FB59A02` |
| widget/desktopwidget_connector.lua | 660617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| widget/tutorialwidget.lua | 24508 | `733EE99341554EB6B6E9C5ABCCC75995B189264CD48C98CE7EF8F2316A787CDC` |

Title keys 9001-9061 above occur at text-sheet physical lines 1965-2013;
9071,9076,9081,9086 occur at 2022,2026,2030,2034. Bodies 9008 and 9009
are at 1970 and 1971. `xtx__text_ui(2).csv` does not contain these selected
keys. Their static title association does not establish a historical tutorial
invocation or successful rendered display. The native control, wait and
camera contracts remain in
`xivl-client-structs:docs/tutorial-control-native-contract.md`.

## Mode selector opening and buttons

`DesktopWidget.askTutorialDeviceType` (`root/proto165`, code start
`0x16DC2`, root binding PC 497) saves 1, then requests
`openWidgetYield(D,12,"Ask/TutorialModeSelectWidget",nil,nil,false)` with
`CALL B=7,C=2` (PCs 0-6). A nil widget skips selection and close (PC7). A
nonnil widget W reaches `selectWidgetYield(D,W,true)`, keeping one result
(PCs 9-12). Only an exact `true` reads one `W:getAskResult()` result into
the saved value (PCs 13-17). `closeWidgetDirect(D,W)` follows on every
nonnil path (PCs 18-20). The method stores the saved value in
`work.tutorialDeviceType` (PC22). When that value equals 1 it also requests
`setConfigFlag(D,43,false)` (PCs 23-28). It returns the one saved value
(PC29). The meaning of configuration flag 43 is NOT TRACED here. The
[root slot contract](desktop-widget-root-slots.md#selection-show-pass)
owns the show pass that `selectWidgetYield` makes for its `true` flag.

`TutorialModeSelectWidget` is defined over `AskBaseClass`. Its `initAsk`
(`root/proto0`, code start `0x10B`) makes these requests, each discarding
results:

| PCs | Request |
| ---: | --- |
| 0-3 | `setCommandParameter(W,"Button_1",2)` |
| 4-7 | `worldMaster:_isKeyboardOnlyTutorial()`, one result compared with true |
| 9-12 | Exact true: `setEnable(W,"Button_1",false)` |
| 14-16 | Otherwise: `setConfirmCondition(W,"Button_1")` |
| 17-20 | `setCommandParameter(W,"Button_2",1)` |
| 21-23 | `setConfirmCondition(W,"Button_2")` |

`processUICommandOperate` (`root/proto1`, code start `0x236`) requests
`setBaseAskResult(W,x)` with its fourth formal x (PCs 0-2). The shared
`_onUICommandEvent` forwards `(W,t,c,cmd,i1,i2)` unchanged to
`processUICommandEvent`, whose Operate arm requests
`processUICommandOperate(W,t,c,i1,i2)`
(`widget/widgetbaseclass.lua` root/proto6 PCs 6-12,
`widget/widgetbaseclass_common.lua` root/proto13 PCs 0-8). The result is
therefore the event's first integer.

The shared helpers build the button parameter text:

- `setCommandParameter(W,control,a,b)` (common `root/proto121`) keeps one
  result of `packCommandParameter(W,a,b)` and requests
  `setControlProperty(W,control,"CommandParameter",text)`.
- `packCommandParameter(W,a,b)` (common `root/proto49`) returns one nil for
  a nil a (PCs 0-1, 23-24). For a nil b it returns
  `"{CommandParameter Int,"..tostring(a).."}"` (PCs 5-10). Otherwise it
  returns `"{CommandParameter Int,"..tostring(a)..","..tostring(b).."}"`
  (PCs 12-21). No type test is made on either operand.
- `setControlProperty(W,control,prop,...)` (common `root/proto68`)
  requests `_setProperty(W,nil,control,prop,...)` with the open tail.
- `setEnable(W,control,flag)` (common `root/proto77`) requests
  `setControlProperty(W,control,"IsEnabled",flag)`.
- `setConfirmCondition(W,control)` (common `root/proto56`) requests
  `_setUICommandCondition(W,control,"UILuaCommands.Operate",5)`.

The selector therefore sets `{CommandParameter Int,2}` on `Button_1` and
`{CommandParameter Int,1}` on `Button_2`. The
`xivl-decomp:docs/resource/sqwt-command-parameter-grammar.md` "Brace text"
and `xivl-decomp:docs/resource/sqwt-command-parameter-consumer.md` "Kind
switch" and "Script entry" sections own the native parse of that text and
the integer handed to the script. The join from the Lua property request to
a button's stored command record is conditional on that native property path.

Neither `TutorialModeSelectWidget.initAsk` nor `AskBaseClass.init` requests
`setCancelCondition` or any `UILuaCommands.Cancel` subscription. The shared
`initConsumedCommmand` writes a `ConsumedCommand` property whose text lists
`UILuaCommands.Cancel` (common `root/proto1` PCs 8-27, 65-68). That property
is not a subscription request, and its native role is NOT TRACED here. If a
Cancel were delivered to the script, the base `processUICommandCancel` would
forward to the base `processUICommandClose`, which requests
`desktopWidget:closeWidgetDirect(W)` without a result write, as the
[root slot contract](desktop-widget-root-slots.md#abort-sweep-and-deletion)
describes. The `Subscription gate` section of the consumer page returns
without a Lua call on a missing subscription.

Canonical windows: `desktopwidget_connector.lua:9415-9455`,
`tutorialmodeselectwidget.lua:11-45` and `48-56`, and
`widgetbaseclass_common.lua:1164-1193` (`packCommandParameter`),
`1312-1322` (`setConfirmCondition`), `1477-1488` (`setControlProperty`),
`1631-1641` (`setEnable`) and `2315-2330` (`setCommandParameter`). The
selector resource is `n1635q/9rz/qpqvs19yxv65r5y57qn1635q.le.lpb`, 649
bytes, SHA-256
`5325e333df3182ee2839a1807ce2415f9ebec48a2ae2ecd34140c02373824595`, with a
636-byte decoded payload, SHA-256
`b0da06584406330f78167546037200a3909a274a0187f8f2bf7c249adf04a779`. The
common resource identities are pinned in the
[CommonAsk answer-list page](common-ask-answer-list.md#source-identity-and-verification),
and the connector identities in the
[camp choice flow](camp-replacement-choice-flow.md#authenticated-inputs-and-locators).
Prototype indices and PCs are zero-based, and code starts are
decoded-payload offsets.
