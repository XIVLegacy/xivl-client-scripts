# ActionMenu page controls

The standard ActionMenu arrows send `PushSlotPrev` and `PushSlotNext`.
The Lua handler changes its page index and sends the transition command to
the outgoing page label. The form supplies the neighboring label names
through bindings.

## Source identity and replay

These inputs are from FINAL FANTASY XIV build `2012.09.19.0001`.

| Input or output | Bytes | SHA-256 |
| --- | --- | --- |
| `client/script/n1635q/97q1vwx5wpn1635q.le.lpb` | 25126 | `bceeae7dc8ac024767ba65a7c1ecbf8682f7c4e89b5c4eb55310d4e00e58af31` |
| Decoded Lua 5.1 chunk | 25113 | `826b09ef44102a51a34f53276ecafed348744688b8ce987831e82f7833fdcecc` |
| Canonical `lua/scripts/widget/actionmenuwidget.lua` | 61888 | `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea` |
| `client/sqwt/widget/ActionMenuWidget.form` | 40815 | `d8a9dffea87cf0d5cea066a7f3d27b4749d7c2ac8b8fff33ecf5bc40fc0711b1` |
| Decoded form | 40807 | `c576f44ef70c45cf50fd1b8a4b0dcaf813b665a607fb647482521a43dc5a8286` |
| `client/sqwt/widget/ActionMenuWidget.tpl` | 47246 | `18c4967b39ebce0c0b8a82d5d706b569bd538a2a5ea6b8c54bcb434612538be6` |
| Decoded template | 47238 | `2c239989bd6bfc4022cd4a18499f78f9957b1791165f806644da4581698c4871` |

The LPB and canonical script match the
[coverage manifest](../manifests/retail_lua_coverage.json) and
[script manifest](../manifests/scripts.json). Use `xivl-cli`
`extract-resource --as lpb` or `--as sqwt` and replay each named carrier
with `verify-extraction --source`. The markup identities also appear in
`xivl-decomp:docs/resource/action-menu-timer-icon-style.md`, Inputs and method.
Pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`,
produces the canonical script after CRLF-to-LF normalization.
Use the same JAR's `--disassemble` for instruction order and Expat for
decoded form and template line locations.

Replay the shared wrapper and callback from
`n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` and
`n1635q/n1635q89r57y9rr.le.lpb` under `client/script` by the same
LPB method. Their carrier, chunk and canonical script identities are in
the coverage and script manifests above under `widgetbaseclass_common.lua`
and `widgetbaseclass.lua`.

## Input and dispatch

The standard form declares these input sources under `Window_ActionMenuWidget`.
The two pad bindings are in the outer `Grid.InputBindings`. The command-bar
arrows are under `Grid_ActionCommands` and `Grid_MenuSlotChange`.

| Form line | Input declaration | Routed command |
| --- | --- | --- |
| 22 | `PadAction=LUp`, `IsRepeat=True` | `UILuaCommands.PushSlotPrev` |
| 23 | `PadAction=LDown`, `IsRepeat=True` | `UILuaCommands.PushSlotNext` |
| 38 | `Button_MenuSlotChange_Up` | `UILuaCommands.PushSlotPrev` |
| 39 | `Button_MenuSlotChange_Down` | `UILuaCommands.PushSlotNext` |

The buttons leave local `ClickMode` and `CommandTarget` unspecified. The native
Button mouse-to-command route and Lua subscription gates are in
`xivl-decomp:docs/resource/sqwt-command-parameter-consumer.md`, Button mouse
source and Subscription gate. The macro arrows at form lines 200 and 201
declare the same Push commands.

## Event registration and page dispatch

In `actionmenuwidget.lua`, `init` calls `setUICommandCondition` for
these `UILuaCommands` in order, passing only each command name.
PCs are zero-based in `main/f0`.

| Command suffix | PCs | Canonical lines |
| --- | --- | --- |
| `PushSlotNext` | 84-86 | 125-128 |
| `PushSlotPrev` | 87-89 | 129-132 |
| `FinishAnimation` | 107-109 | 156-159 |
| `ShortCutAction` | 116-118 | 168-171 |
| `ActionBarSlotPrev` | 119-121 | 172-175 |
| `ActionBarSlotNext` | 122-124 | 176-179 |

The wrapper in `widgetbaseclass_common.lua` at 1286-1296 (`main/f54`,
PCs 0-4) passes `_widget`, the command, and numeric `5` to
`_setUICommandCondition` without a separate template argument.
The native uses the form root name as the template key and `_widget`
for the root control. For each successful
registration the numeric arm supplies condition byte `+0x54=0` and
priority byte `+0x55=5`. [Native registration](https://github.com/XIVLegacy/xivl-decomp/blob/813128f03f2b83fe941caad04c760a11c0cb352c/docs/resource/sqwt-command-parameter-consumer.md#L670-L691)

A matching command that reaches the native condition dispatch uses the
Event path at `0x00896AF0`. Admission still depends on the native
gates, including the active and pending priority comparisons. The callback
`_onUICommandEvent` in `widgetbaseclass.lua` at 250-257 (`main/f6`, PCs 6-12)
forwards five argument slots to the widget's `processUICommandEvent`. The registration
and callback paths are static evidence. Actual callback delivery remains
unresolved. [Native event admission](https://github.com/XIVLegacy/xivl-decomp/blob/813128f03f2b83fe941caad04c760a11c0cb352c/docs/resource/sqwt-command-parameter-consumer.md#L886-L899)
The [ShortCutAction route](action-menu-shortcut-action-route.md) owns the
`ShortCutAction` handler.

`init` initializes `slotMoving` false, `slotPage` to 1 and
`slotMaxPage` to 3 at 184-195.

`processUICommandEvent` admits both Push and ActionBar aliases for each
direction. In its unluac disassembly, both next comparisons at `l59`
and `l62` reach `l64` on a match. Both previous comparisons at `l78`
and `l81` reach `l83`. This shared branch is obscured in the canonical
decompile at lines 344-381. Each shared block returns if `isShow()`
is false or `slotMoving` is truthy. It otherwise calls `changeNextSlot`
or `changePrevSlot`, which passes true or false to `changeSlotPage`
(lines 1848-1867).

1. With `userMacroType` nonzero, `changeSlotPage` changes and refreshes
   the macro page and returns at lines 1872-1888.
2. On the command-bar path, a nonempty cursor control causes a leave
   animation request at 1889-1902. The script saves the old index,
   computes the wrapped next or previous index and stores `work.slotPage`
   at 1924.
3. At 1926-1933 it calls `sendControlCommand` with the outgoing
   `Label_MenuSlot_N` and `UILuaCommands.ChangePageNext` or
   `UILuaCommands.ChangePagePrev`. It sets `work.slotMoving` true at
   1935 after the call. Bytecode block `l46` preserves this order.
4. It conditionally requests the cursor enter animation and updates cost
   data, then refreshes the main slots and page display at 1936-1956.
   `changeSlotPageDisplay` writes the new page number to
   `TextBlock_SlotNumber` at 1962-1975.

The shared wrapper at `widgetbaseclass_common.lua:1255-1283` forwards
the widget, a nil context, the target name, the command and two optional
arguments. The downstream native command processor looks up the named
control in the form context, casts it to FrameworkElement and calls the
registered command's `+8` with target `element+0xB4` when the cast
succeeds, or with a null target on the fallback arm. This processor is
conditional on the Lua registration and argument conversion reaching it.
See `xivl-client-structs:docs/native-input-ui-boundaries.md`,
Storyboard-command re-execution.

The selected template triggers at lines 314 and 333 start the outgoing
label's next and previous storyboards. Their storyboards declare
`UILuaCommands.FinishAnimation` and bind `CompletedCommandTarget` to
`TemplatedParent` at 316 and 335. The Lua `FinishAnimation` branch
clears `slotMoving` at 547-550. The handler therefore allows another
turn after an admitted finish reaches it.

## Command Button slot data

The standard form declares `IntData.Value0` literals 1 through 10 on
`Button_Command_1` through `Button_Command_10` at lines 177-186.
The [native attached-property finding](https://github.com/XIVLegacy/xivl-decomp/blob/8cfde48ae1b2b2e7527bbf3debc3f5a4a20cb3bd/docs/resource/sqwt-qualified-property-lookup.md#actionmenu-button-integer-data)
owns the receiver storage, default zero and literal conversion. These values
are separate from the Buttons' declared command-parameter records.

`getSlotNumberFromButton` at canonical lines 2693-2712 is `main/f62`.
PCs 0-3 call `getControlProperty` with the supplied control name and
`IntData.Value0`, requesting one result `v`. PCs 4-9 return nil when
`v < 1` or `10 < v`. PCs 10-15 otherwise return
`10 * work.slotPage - 10 + v`. Both returns contain one value.
The helper performs its comparisons directly, without a nil guard or
integer conversion. `getSlotNameFromButton` at 2674-2690
(`main/f61`, PCs 0-10) returns nil when this helper returns nil,
and otherwise forwards the result to `getSlotLabelCommandIconName`.

On the `UILuaCommands.EnterButton` arm, `processUICommandEvent`
(`main/f1`, PCs 23-45, canonical lines 305-330) passes its fourth
explicit argument to `getSlotNameFromButton`. A nil result skips the
selected block. The accepted block requests the enter animation, updates
cost data and calls `setOnCursorControl`, in that order. PCs 41-45
then call `getControlProperty` on that same handler argument with
`IntData.Value0`, request one result and store it in `work.slotSelectIndex`.
This value is read again after the preceding calls. It is not the global
slot number computed by `main/f62`.

The shared `getControlProperty` wrapper at
`widgetbaseclass_common.lua:1491-1501` is `main/f69`, PCs 0-5.
It tail-calls `_getProperty` with three explicit arguments after self,
namely nil, control name and property name, and forwards all results.
The two callers above each select one result. The native nil-name
property route is recorded in
`xivl-client-structs:docs/widget-native-call-contract.md`, Property access.
The source identity and replay method above apply to both scripts.
PCs are zero-based and count instructions, excluding labels and directives.
Actual event delivery, the returned native value and intervening property
writes remain unresolved.

## Page names and peer bindings

The ordinary `changeSlotPage` sequence performs no `Name` or peer
`StringData` write. The page labels under the Canvas at form line 43
declare the following `ElementName` bindings with `Path=Name` and
`Mode=OneWay`. The table uses the suffixes of `Label_MenuSlot_N`.

| Form line | Page suffix | `StringData.Value0` next peer | `StringData.Value1` previous peer |
| --- | --- | --- | --- |
| 44 | 1 | 2 | 3 |
| 76 | 2 | 3 | 1 |
| 108 | 3 | 1 | 2 |
| 140 | 4 | 1 | 3 |

The template's outgoing animations bind to the owner's `Name`.
The incoming animations bind to the owner's `StringData.Value0` for
next and `StringData.Value1` for previous. See
`xivl-decomp:docs/resource/sqwt-keyframe-target-binding.md`,
Observed ActionMenu declarations. Lua's `setOnCursorControl` and
`getOnCursorControl` at 2729-2757 access the widget-root
`StringData.Value0` for cursor bookkeeping.

The physical producer of the ActionBar aliases, pad hardware mapping,
live arrow eligibility and routing, actual peer binding initialization,
the no-parameter native wrapper lane, and live completion delivery
remain unresolved.
