# Craft progress opening, refresh, and selection

`CraftJudge` opens the progress widget with progress fixed at zero and both
point maxima fixed at 1000. Its opening and refresh methods use different
supplied-value orders. A successful connector refresh return means that the
widget was found, even if the widget rejected the supplied values.

The [command classification summary](craft-command-progress-contracts.md)
owns command bands and class command sets. This page describes the selected
`CraftJudge` -> `CraftProgressWidget` flow from the 1.23b extraction
`2012.09.19.0001`.

## Opening and supplied positions

Positions below exclude the `CraftJudge` receiver. Position 1 is the actor.
`openCraftProgressWidget`, `updateInfo`, and `closeCraftProgressWidget` act only
when that actor's `isPlayer()` result equals boolean `true`. These methods do
not add a craft-class predicate.

| Supplied position | Opening use | Refresh use |
| --- | --- | --- |
| 2 | Unused | Unused |
| 3 | Craft point | Progress percentage |
| 4 | Quality point | Craft point |
| 5 | HQ-rate display argument | Quality point |
| 6 | Not declared | Item ID |
| 7 | Not declared | Item quality |
| 8 | Not declared | `param1` |
| 9 | Not declared | `param2`, also the HQ-rate display argument |
| 10 | Not declared | Unused |

Opening calls the current global `desktopWidget` receiver's
`openEventModeWidgetYield` with widget name `CraftProgressWidget`, followed by
six initializer values: progress 0, supplied position 5, supplied position 3,
maximum craft point 1000, supplied position 4, and maximum quality point 1000.
The Judge discards the helper's results. The selected body does not establish
the helper's creation, waiting, or native object-lifetime implementation.

Refresh calls the current `desktopWidget.orderCraftProgressWidgetUpdate` with
supplied positions 3 through 9, followed by literal 0. That last argument
becomes widget `param3`; supplied position 10 does not supply it. The Judge
discards this helper's return too.

Source: `judge/craft/craftjudge.lua`, `openCraftProgressWidget` lines 196-216,
`closeCraftProgressWidget` lines 219-233, and `updateInfo` lines 236-257.

## Initialization and refresh

The widget initializer requests modal and draggable behavior, initializes the
command list, sets `work.itemQuality` to 1, and passes its six values to
`setInitialData`. This setter
stores progress, craft point, and quality point, sets `maxProgress` to 100,
and substitutes 999 only when a supplied point maximum equals numeric 0 or
`nil`. Boolean `false` is not that fallback condition. The selected Judge
opening supplies 1000 for both maxima, so it does not take either fallback.

The setter marks `work.initialized` true, hides `Grid_Top_2`, and tail-calls
`updateProcess` with progress, craft point, quality point, three explicit
`nil` arguments, the initializer's second value as the HQ-rate argument, and
one final explicit `nil`. Its result is the update's result. The initializer
itself discards that result. The setter writes its fields before attempting
the update, so a rejected initial refresh does not undo those assignments.

`updateProcess` accepts eight arguments after its receiver:

| Position | Role |
| --- | --- |
| 1-3 | Progress, craft point, quality point |
| 4-5 | Item ID, item quality |
| 6-8 | `param1`, `param2`, `param3` |

Before writing work state or issuing display calls, it returns one boolean
`false` for progress below 0 or above `maxProgress`, craft point below 0 or
above `maxCraftPoint`, or quality above `maxQualityPoint`. There is no matching
lower-bound quality test in this body. These are numeric comparisons, not a
missing-value fallback or a clamp.

An accepted update stores the first three arguments and issues display calls
for `ProgressBar_Percentage`, `TextBlock_CraftPointValue`, and
`TextBlock_QualityPointValue`. It also supplies text ID 3006 and two formatting
arguments to `TextBlock_HQRate`: argument 7, defaulting to 0 only for this
display call when it is `nil`, followed by literal 0. An explicit `false` or
numeric 0 is preserved. The display fallback does not replace `param2` in work
state.

If item ID is `nil`, the update preserves the existing item and tuning fields
and does not call `proceedTuningPhase`. Otherwise:

- If `work.isTuningPhase` is not exactly true, it sets that flag true and seeds
  both `oldparam1..3` and `param1..3` from the new arguments 6-8.
- If the flag is exactly true, it first copies the prior `param1..3` into
  `oldparam1..3`, then replaces `param1..3` with arguments 6-8.
- It replaces `itemID` and `itemQuality` with arguments 4-5 and calls
  `proceedTuningPhase` without an explicit extra argument.

Finally, every accepted update copies the current `chosenCommand` into
`previousCommand` and returns one boolean `true`. Refresh does not reset
`chosenCommand`. The tuning display helper uses a freshly obtained
`worldMaster:_getMyPlayer()` result to create a virtual item and request item
presentation data. It substitutes item quality 1 when the stored quality is
numeric 0 or above 4. Those calls do not establish an inventory grant or a
crafting outcome. The update calls this helper without the boolean true that
requests its tuning-grid switch; `setCommand` supplies true when the tuning
flag is exactly true.

`orderCraftProgressWidgetUpdate` freshly calls
`getEventModeWidget("CraftProgressWidget")`. A `nil` lookup returns one
`false`. Otherwise it forwards all eight values to that object, discards
`updateProcess`'s result, and returns one `true`. Thus an out-of-range update
can leave the widget unchanged while the connector returns true.

Source: `widget/craftprogresswidget.lua`, `init` lines 11-172,
`setInitialData` lines 175-215, `proceedTuningPhase` lines 388-563, and
`updateProcess` lines 789-903. Connector source:
`widget/desktopwidget_connector.lua`, `orderCraftProgressWidgetUpdate`
lines 11339-11364.

### Progress property write

In the installed 1.23b `widget/craftprogresswidget` chunk, root PCs 46-48
register `updateProcess` from zero-based child 13. That child's PCs 28-31
at decoded offsets `0x1B3F..0x1B4B` call the receiver's `setValue` with
the literal control name `ProgressBar_Percentage` and the original first
argument. The call discards its results.

The installed `widget/widgetbaseclass_common` root PCs 312-314 register
`setValue` from zero-based child 104. Its PCs 0-4 at decoded offsets
`0x5AAA..0x5ABA` call `setControlProperty` with the forwarded name,
literal property `Value` and forwarded number. The call discards its
results. This is the script-side property request. Native setter admission,
event delivery and rendered values remain separate.

| Installed chunk | Wrapper bytes | Unwrapped SHA-256 |
| --- | ---: | --- |
| `n1635q/7s94qusv3s5rrn1635q.le.lpb` | 8029 | `b4d2f8d0a2f8e6ab6d6791ee012e57d432f8b4305a1d83cdd038d93c5abb1c53` |
| `n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 | `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |

Decode the `rle` wrapper with the payload starting at file offset 13 and
XOR key `0x73`. Walk Lua 5.1 prototypes using little-endian four-byte
`size_t` and compare the closure registrations, instruction operands and
constant references at the cited PCs.

## Selection, completion, and local results

The selected `craftCommandUI` and `craftTuningUI` callers pass a command count
of 10 and a constructed command table to
`selectCraftProgressWidgetDisplay`. The connector performs a separate fresh
`getWidget(4, "CraftProgressWidget")` lookup. This is not source proof that it
is the same object returned by the update lookup.

When the widget exists, the connector builds ten slots. A slot above the
supplied command count receives numeric 0; other slots receive the matching
input-table value. Original bytecode forwards the complete `unpack` result to
`setCommand`. The canonical decompile at lines 11316-11317 incorrectly
expresses only three unpack results and three command values. The original
open-result/open-argument CALL pair resolves that arity discrepancy.

`setCommand` configures ten command slots, resets `chosenCommand` to numeric
0, enables focus and the command list, and requests initial selection/help.
`setCommandList` hides a slot only for `nil`; numeric 0 and boolean `false`
are non-nil values that reach its visibility and `IntData.Value0` assignments.
The command accessor reads that property through the chosen button's name.
The property read remains a native boundary, not proof of readback identity.

The connector calls `selectWidgetYield(widget, true)`, consuming one result.
It reads `getCommand()` only if that result is exactly true. It always returns
two values: the selection result and the command, initially 0. A missing
widget returns `(false, 0)`. A false selection returns `(false, 0)` too; a
`nil` selection remains `(nil, 0)` rather than becoming false.

In the selected widget callbacks, `processUICommandOperate` returns without
choosing when focus is exactly false or `chosenCommand` is not numeric 0.
For `Button_Command`, it reads the selected command property into
`chosenCommand`, masks further command input, and updates help. Hover/anchor
handling in `processUICommandDefault` updates `focusedCommand`, not
`chosenCommand`. `processWaitCallFunction` returns false only while
`chosenCommand == 0`; it returns true for other values, including `nil` or
false. `getCommand` returns one value containing the current field. These
methods supply a local completion predicate, not proof of the yield helper's
internal wait scheduling.

Each Judge caller consumes the connector's two results and returns one value:
`craftCommandUI` substitutes 22507 if the selection result is exactly false or
the command is -1; `craftTuningUI` substitutes 22503 under those same tests.
Otherwise each returns the command unchanged. Numeric 0, `nil`, and boolean
false in the command result are not interchangeable with selection false.
Neither selected caller closes the progress widget or proves external command
execution, settlement, or server acceptance.

Source: `judge/craft/craftjudge.lua`, `craftCommandUI` lines 591-660 and
`craftTuningUI` lines 663-704; `widget/desktopwidget_connector.lua`,
`selectCraftProgressWidgetDisplay` lines 11290-11336; and
`widget/craftprogresswidget.lua`, `setCommandList` lines 277-325,
`getCommandId` lines 328-340, callbacks lines 589-667, `setCommand`
lines 683-786, and completion/getter lines 906-929.

## Ordinary opening and first Standard Synthesis

These are static observations of the installed HD keyboard form and original
Lua 5.1 chunks from build `2012.09.19.0001`. The progress window is
`CraftProgressWidget`, a `WidgetBaseClass` subclass. Its root chunk requires
`/Widget/WidgetBaseClass` and defines that class at PCs 0-6
(`0x0020..0x0038`). Its inherited default `getFormName` returns no values.
The shared initializer derives the form basename from the supplied widget
name, requests its load, and derives the window name from the same basename
(Common proto0 PCs 26-45). The selected HD form is
`widget/CraftProgressWidget.form`, root `Window_CraftProgressWidget`.

### Opening, selection wait, and explicit close

For an exactly true first `isPlayer()` result, Judge proto13 calls
`openEventModeWidgetYield` with `CraftProgressWidget` and six initializer
values `(0,A5,A3,1000,A4,1000)`. The Judge requests zero results and
returns zero values. The connector wrapper uses category 4 and requests
`openWidgetYield(D,4,"CraftProgressWidget",nil,nil,false,...)` with the
complete initializer tail. Its final Boolean reports whether the first
open result is nonnil. The
[shared root-slot contract](desktop-widget-root-slots.md) gives the guarded
slot store and the [desktop admission contract](content-director-ui-contracts.md#desktop-widget-admission-and-close)
gives the creation polling and later lookup. The widget initializer declares
Work, requests modal and drag true, initializes the command rows, sets
`itemQuality=1`, and forwards the six operands to `setInitialData`.
There is no numeric synthesis mode field in this opening argument tuple.
The connector's Boolean is discarded and the open call has no selection
wait. The later selection performs its own lookup of the category-4 instance.

`craftCommandUI` takes its class and order from A3/A4. Its first constructed
entries are the three available standard commands except 22502, followed by
nonnil supplied varargs, followed by any available-list entries equal to
22502. It calls `selectCraftProgressWidgetDisplay(10,table)` and reads two
results. Judge proto8 picks 22550 for class 29 and 22580 for class 34,
then appends base+1 and base+2. Its order helper returns false for exact
numeric 2 or 6 and true otherwise. The false branch adds 3 to the base.
Orders 1 and 2 also append 22506, so local server order 5 for the main tool
and order 6 for the off hand are distinct from that appended-command case.
The [command catalog](https://github.com/XIVLegacy/xivl-client-data/blob/aaee96e5d2633c30228be6efd6124f4ac38d9c14/derived/command_battle_params.csv#L72)
identifies 22550 as Standard Synthesis. The same title is present for
[22580](https://github.com/XIVLegacy/xivl-client-data/blob/aaee96e5d2633c30228be6efd6124f4ac38d9c14/derived/command_battle_params.csv#L102).

The selection connector freshly requests `getWidget(4,"CraftProgressWidget")`.
It forwards the complete list of unpacked entries to `setCommand`, then
requests `selectWidgetYield(W,true)`. The show pass requests show for
qualifying children and W. The timer helper uses a nil timeout, checks
exact-false liveness and polls the widget callback for exact true, waiting
0.1 between polls. Widget `chosenCommand == 0` keeps the ordinary call
parked. Only an exactly true selection result leads to the getter. The
connector returns the status and command, defaulting the latter to 0.
The Judge returns one value: the selected command, or 22507 when the
connector's status is exactly false or command is numeric -1. In particular,
22550 and 22580 are returned as command IDs, while 1 is the row operand.
The open, refresh and close Judge methods return zero values. Explicit
close requests `closeEventModeWidget("CraftProgressWidget")`, whose stock
wrapper forwards `closeWidget(D,4,"CraftProgressWidget")`. Selection does
not issue that close.

### Generated row and button command

The authenticated decoded HD form line 35 declares `ListBox_Commands` under
a Grid inside a Label whose own hit-test flag is false. It selects local
`TemplateControl_ListBox`, has tab stop false, and is 206 wide with both
height limits 140. The local template at decoded lines 18-31 contains a
ContentPresenter and routes `MouseEnteredItem`, `AnchoredItem`, and
`SelectionChanged` to `Selector.MouseEnteredItem`,
`Selector.AnchoredItem`, and `Selector.SelectedItem` using each named
index property. These selector events are distinct from the button
Operate command.

The template at decoded lines 14-17 is `Template_ListBoxItem`, targets
ListBoxItem, and sets its tab stop false. Its one unnamed-by-row Button is
named `Button_Command`, uses `BTN_basis_listboxSelect`, has height 20
and left content alignment, declares `UILuaCommands.Operate`, and omits
`CommandTarget`, `CommandParameter`, and `ClickMode`. `initCommandList` supplies the ten rows and registers
`setTemplateConfirmCondition("Template_ListBoxItem","Button_Command")`
then requests ten `_addItem` calls into `ListBox_Commands`. The row names
are `ListBox_Command_1` through `ListBox_Command_10`, formed by the
prefix and decimal ordinal. It hides each row, requests its tab stop false,
and sets its Button's `CommandParameter` to the one-based ordinal.
It sets tuning false and registers the ListBox's mouse-enter/anchor commands
through the plain control helper. The inherited template helper requests
`_setUICommandTemplateCondition("Template_ListBoxItem","Button_Command","UILuaCommands.Operate",5)`.
The plain hover/anchor helper also supplies priority 5.

For each nonnil command, including numeric 0, `setCommandList` shows
its row, writes the actual command ID to the **row's** `IntData.Value0`,
sets the Button's normal listbox skin, and requests Button content from
text key 3043 with the command ID. The first nonnil row sets
`firstChoise`. `setCommand` resets `chosenCommand` to 0, sets
`focusEnable` true, enables `ListBox_Commands`, writes `SelectedIndex`
as `firstChoise-1`, and requests focus on
`ListBox_Command_<firstChoise>:Button_Command`. Its widget override sets
logical focus, and requests keyboard control focus when the Desktop's
current focused widget is itself. It requests command help through
text key 1105 with the chosen ID. Thus stock initial selection 0 and
stock first button command parameter 1 are separate coordinates.
The stock code can show a zero-valued row. Zero is unsuitable for a
first-Standard-only admission.

On delivery through the named template registration, the native child
kind-1 variant passes exactly
`("Template_ListBoxItem","Button_Command","UILuaCommands.Operate",1)`
after self. No second integer is carried, and the inherited Lua method's
fifth parameter reads nil. See the
[native condition, kind switch, and argument pusher](https://github.com/XIVLegacy/xivl-decomp/blob/a580ee8c6cb2de2a4d130e44d799f32f36c760b1/docs/resource/sqwt-command-parameter-consumer.md#kind-switch).
WidgetBase dispatches Operate to `processUICommandOperate` and passes
the first integer as its row operand. It does not reread ListBox
`SelectedIndex` on this branch. The progress handler returns early for
exactly-false `focusEnable` or nonzero `chosenCommand`. For
`Button_Command` it reads the current `IntData.Value0` through
`getCommandId(1)`, stores that in `chosenCommand`, calls
`maskCommandList(1)` and refreshes help. Masking sets focus false, sets
the chosen Button skin to `BTN_basis_listboxSelect_cmdRunning`, and
disables the list. It does not take the command ID from the event
parameter. For row 1 the handler sets its `localBuf` false. Under the
stock values, the next wait poll completes and the Judge returns the
current nonzero command ID. The separate hover/anchor path only writes
`focusedCommand`.

### Original locators

Prototype IDs, PCs, and byte offsets below are zero-based in the decoded
payload.

| Method | Prototype / code start | Relevant original PCs |
| --- | --- | --- |
| Judge open | `root/proto13` / `0x0E46` | 0-3 exact player, 5-13 open operands and zero results, 14 return |
| Judge refresh | `root/proto15` / `0x0FB8` | 0-3 exact player, 5-14 A3-A9 and literal 0 |
| Judge close | `root/proto14` / `0x0F16` | 0-3 exact player, 5-7 named close, 8 return |
| Judge main-tool test | `root/proto7` / `0x0AC8` | 0-7 exact 2 or 6 yields false |
| Judge available commands | `root/proto8` / `0x0B26` | 2-32 class bases, 35-45 tool offset and three entries, 46-50 order 1/2 appends 22506 |
| Judge craftCommandUI | `root/proto21` / `0x18AD` | 3-17 class/order and initial commands, 19-35 nonnil varargs, 36-45 delayed 22502, 46-61 selection and result |
| Desktop event-mode open | `root/proto551` / `0x3376F` | 0-6 category and complete tail, 7-12 nil test and Boolean |
| Desktop select progress | `root/proto212` / `0x1A87A` | 2-7 fresh category/class, 20-24 full unpack, 25-33 show/wait and true-only getter, 37 return |
| Desktop select widget / timer | `root/proto539` / `0x32BE7`, `root/proto540` / `0x32CFA` | 539 PCs4-28 show and nil timer, 540 PCs7-19 and 35-41 liveness/completion/wait |
| Desktop update / close wrappers | `root/proto213` / `0x1A9D0`, `root/proto553` / `0x3389F` | 213 PCs0-18 fresh event-mode lookup and eight operands, 553 PCs0-4 close category and name |
| Widget init | `root/proto0` / `0x02CE` | 92-109 modal, drag, rows, quality and six initializer operands |
| Widget row registration and names | `root/proto2` / `0x0860`, `root/proto5` / `0x0CCD` | 2 PCs0-3 template registration, 8-32 add/hide/tab/parameter, 34-43 selector registrations; 5 PCs0-5 row path |
| Common template/plain registration | `root/proto60` / `0x455F`, `root/proto55` / `0x42CA` | 60 PCs0-5 template, button, Operate and 5; 55 PCs0-4 plain condition and 5 |
| Widget row values and getter | `root/proto3` / `0x0AB2`, `root/proto4` / `0x0C46` | 3 PCs3-26 nil branch, row IntData and button content; 4 PCs0-6 named row property lookup |
| Widget arm and focus | `root/proto12` / `0x17E2`, `root/proto8` / `0x13F2` | 12 PCs42-76 resets, enables, selects and focuses; 8 PCs4-14 logical and conditional keyboard focus |
| WidgetBase dispatcher / common Operate | `root/proto6` / `0x0A2A`, `root/proto13` / `0x26E6` | 6 PCs6-12 forwards A1-A5; 13 PCs1-8 Operate branch and A4 forwarding |
| Widget Operate and mask | `root/proto9` / `0x14C7`, `root/proto6` / `0x0D35` | 9 PCs0-19 guards, row getter and chosen/mask; 20-30 help and localBuf; 6 PCs0-21 focus false, running style, disabled list |
| Widget wait / getter | `root/proto14` / `0x1E8D`, `root/proto15` / `0x1F03` | 14 PCs0-8 chosen == 0 waits; 15 PCs0-2 returns selected command |

| Installed input | Wrapper bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `client/script/0p635/7s94q/7s94q0p635.le.lpb` | 10127 / `fda277d6626fd0c381100cadd75628cae7be508f150bb2558364fe647ba07147` | 10114 / `0dff8463d2b685ff65a23afcf5e52e451e531e6fac194fd088adba3d05dbd0ff` |
| `client/script/n1635q/7s94qusv3s5rrn1635q.le.lpb` | 8029 / `e7a24fdab44ecde4d35ee76075262025cb845a834693b218be1263e3eb05ca8d` | 8016 / `b4d2f8d0a2f8e6ab6d6791ee012e57d432f8b4305a1d83cdd038d93c5abb1c53` |
| `client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `client/script/n1635q/n1635q89r57y9rr.le.lpb` | 4080 / `aad807a42296e93301582defc8f15e4003b8093af672794282cd54950cc556ad` | 4067 / `11e5bab509c4dbbd7e2767d35cdf132a59b5c510c32c2e215f83cac713115140` |
| `client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 / `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` | 32983 / `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |
| `client/sqwt/widget/CraftProgressWidget.form` | 9565 / `ccd83bd31bf0885fa8b480bad84b454624f70598a1e5ad417c812ff56fb8fb42` | 9557 / `9db3d980959e3caa259d41270734e59bf5b2cf50abf9d131dd570ef7ba905197` |
| `client/sqwt/widget/CraftProgressWidget.tpl` | 4315 / `35820be4f2758f15c388d828d369fd86e668da143d6459724c761733f9fff983` | 4307 / `b09866509c602637aa4404ee1e3b994f2f148995601f6544925cf0b8d149282e` |

Authenticate with `manifests/retail_lua_coverage.json`. Decode the LPBs
using `tools/retail_script.py:decode_lpb` and walk the zero-based prototypes
with `tools/build_quest_contracts.py:ChunkReader` and `instruction`. The
[form declarations](https://github.com/XIVLegacy/xivl-client-data/blob/aaee96e5d2633c30228be6efd6124f4ac38d9c14/docs/craft-progress-form.md#installed-inputs)
give the basename-keyed SQEX recipe and installed form hashes.

### Captured opening

The [local guildleve capture](https://github.com/XIVLegacy/xivl-captures/blob/7163914b423c90369c18ddc18f7a02a66ca9cf3c/studies/local-guildleve-dialogue/README.md#recipe-selection-and-progress-opening)
records main s2c frame 90 / subevent 0 / packet 306 with type-0
`0x0130 delegateCommand`, owner `0xA0F055F1`, trigger `0x029B2941`,
Judge actor `0xA0F4E203`, and
`openCraftProgressWidget` tail `(100,0,0)`. Main c2s frame 100 / subevent
2 / packet 310 records an EventUpdate with one nil in the selected interval.
The same study's accounting lists `craftCommandUI` occurrences. The cited
selected rows do not pair a Standard Synthesis result to a particular
row, button press, or keyboard decision. The
static client callback returns the command ID to the active server call.

## Explicit close and evidence

`closeCraftProgressWidget` separately requests
`desktopWidget:closeEventModeWidget("CraftProgressWidget")` under the same
exact-player predicate and returns no values. The selected selection and
refresh paths do not issue that close. This establishes an explicit close
request, not destruction timing or complete native cleanup.

[Script identities](../manifests/scripts.json) authenticate the canonical
members. The [craft manifest](../manifests/craft_command_progress_contracts.json)
pins the Judge and progress-widget chunks. The
[retail coverage manifest](../manifests/retail_lua_coverage.json) pins all three
LPBs and decoded payloads, including connector resource
`n1635q/65rzqvun1635q_7vww57qvs.le.lpb` with decoded payload SHA-256
`685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`.
Its canonical source SHA-256 is
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`.

The following locators use zero-based instruction PCs and byte offsets in the
decoded Lua 5.1 chunk. They can be checked with `tools/retail_script.py`'s
`decode_lpb` and `tools/build_quest_contracts.py`'s `ChunkReader` and
`instruction`, without retaining decoded chunks or disassembly.

| Original locator | Supported distinction |
| --- | --- |
| Judge `root/proto13`, PC 13, offset 3706 | Opening argument order and discarded results |
| Judge `root/proto15`, PC 14, offset 4080 | Refresh positions 3-9, final literal 0, discarded results |
| Widget `root/proto1`, PC 35, offset 1866 | Eight explicit update arguments and tail-returned results |
| Connector `root/proto212`, PCs 23-24, offsets 108758/108762 | `unpack` CALL `C=0`, then `setCommand` CALL `B=0`: all unpack results flow onward |
| Connector `root/proto212`, PCs 28/33/37, offsets 108778/108798/108814 | One selection result, one command result, two return slots |
| Widget `root/proto14`, PC 2, offset 7829 | Completion compares `chosenCommand` with numeric 0 |

These static contracts stop at dynamically bound helper bodies, native UI
application and property readback, and external command execution. They do not
establish craft success, quality/durability formulas, item debit, experience,
or server acceptance.
