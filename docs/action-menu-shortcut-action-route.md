# ActionMenu ShortCutAction route

The Desktop connector forwards `UILuaCommands.ShortCutAction` and its fourth
handler argument to static widget 7, which the connector creates with the name
`ActionMenuWidget`. The ActionMenu handler resolves that argument to a slot
and, for an enabled custom slot, calls `executeGameCommand`. This page records
static script evidence. The key binding, native command delivery and server
handling remain unresolved.

## Desktop forward

`DesktopWidget.processUICommandEvent`
(`widget/desktopwidget_connector.lua:3199-4173`, `root/proto62`) returns unless
`work.mode` exceeds 1. It returns for `ShortCutAction` when
`_getKeyboardFocusedWidget` returns nil (lines 3207-3215), and it requires
control name `_widget` (lines 3220-3222).

The `ShortCutAction` arm at lines 3773-3798 (PCs 481-503) requires a nonnil
fourth handler argument. When the third handler argument is `ShortCutAction`
and no main target is set, it calls `setTargetCharacter(1, player)` (lines
3775-3788, PCs 485-496). It then calls `sendCommand` on `getStaticWidget(7)`
with those two handler arguments (PCs 497-503). The arm calls no
command-execution helper.

## Static widget 7

`DesktopWidget.setDefaultWidgetLocation` calls
`createStaticWidget(7, "ActionMenuWidget", nil, 2, false)` (lines 8166-8173,
`root/proto142`, PCs 63-69). See
`xivl-decomp:docs/resource/sqwt-window-trigger-order.md`, ActionMenu show and
focus retirement. `createStaticWidget` stores the `createWidget` result in
`work.widget[7]` (lines 25005-25022) and `getStaticWidget(7)` reads that entry
(lines 25051-25057).

`createWidget` requires `/Widget/ActionMenuWidget` and requests `_createActor`
with the name `ActionMenuWidget` (`widget/desktopwidget.lua:61-100`). `ActionMenuWidget` inherits
the nil `getFormName`, so `WidgetBaseClass` derives the form name from its
supplied name and stores `"Window_" .. formName` as `widgetName`
(`widget/widgetbaseclass_common.lua:42-63`). `sendCommand` passes `widgetName`
as its target (lines 1255-1266). The target is
`Window_ActionMenuWidget` when `_createActor` supplies that name.

## ActionMenu handler

`ActionMenuWidget.init` registers the command as listed in
[ActionMenu page controls](action-menu-page-controls.md#event-registration-and-page-dispatch).
The `ShortCutAction` arm of `processUICommandEvent`
(`widget/actionmenuwidget.lua:498-510`, `main/f1`, PCs 191-204) returns while
`work.slotMoving` is truthy. With `work.userMacroType` 0 it calls
`executeCustomCommandForShortCutNumber` with its fourth explicit argument. A
nonzero macro type takes the macro branch at PC 206.

`executeCustomCommandForShortCutNumber` (lines 1023-1089, `main/f14`) performs
these steps:

1. Builds `Button_Command_N` from that argument (PCs 0-2).
2. Calls `desktopWidget:updateActionMenuWidget(false, true)` (PCs 3-7). The
   false first argument skips the ready rescan. The Desktop method shows the
   widget when the second argument is true and no sub-target selection is
   active (lines 9485-9576).
3. Maps the button to a slot Label through `getSlotNameFromButton`, then calls
   `updatePlayerParameterCostData` and `isButtonEnabled` (PCs 21-29).
4. For a disabled slot, calls `playCommandExecuteSound(false)`, which sends
   `UILuaCommands.ExecuteCommandError`, and returns with no command call
   (PCs 32-35, lines 2516-2529).
5. For an enabled slot, reads the Label's `IntData.Value2` and
   `IntData.Value3` and passes them to `executeGameCommand`. Its result goes to
   `playCommandExecuteSound` (PCs 36-50).

## Slot data and enabled state

`updateMainSlot` (lines 1185-1218) calls `addSlot` for each nonnil custom
command with a truthy usable flag in slots 1 through 30, passing literal 2 as
its third argument.
`addSlot` (lines 1734-1843, `main/f28`) returns false when
`isStackIntoActionMenu` refuses the command. It writes only when the command
ID differs from the Label's current `IntData.Value0`:

| Control | Property | Value |
| --- | --- | --- |
| Slot Label | `IntData.Value0` | `getCommandID` result |
| Slot Label | `IntData.Value1` | Command category |
| Slot Label | `IntData.Value2` | The third argument |
| Slot Label | `IntData.Value3` | Slot number |
| `:IconControl_Command_2` | `IconDatas` | `getPlayerActionCommandData(command, 36)`, or 0 for nil |
| `:IconControl_Command_1` | `IconDatas` | `getHandIconNumber(category)` |

`getHandIconNumber` (lines 2715-2724, `main/f63`) maps category 1 to 243,
category 2 to 244 and any other value to 245.

`isButtonEnabled` (lines 2497-2511, `main/f50`) reads `getColor` on
`:IconControl_Command_1` and returns false when the first result is below 1.
`setButtonEnabled` (lines 2409-2492, `main/f49`) writes that control's color
and `VisualOpacity`. It writes `IconRed`, `IconBlue`, `IconGreen` and
`IconAlpha` on `:IconControl_Command_2`. An enabled slot receives 1 for each
value. A disabled slot receives color channels and icon channels of 0.5, with
`VisualOpacity` and `IconAlpha` of 0.9.

## Command arguments

For first argument 2, `executeGameCommand` (lines 859-1018, `main/f13`) reads
`getPlayerEquippedCustomCommand(slot)`, which returns the command, its category
and a usable flag (`widget/desktopwidget_connector.lua:12602-12650`).
`CharaBaseClass.getCustomCommand` reads `charaWork.command` and
`charaWork.commandCategory` at `commandBorder + slot`
(`chara/charabaseclass_cliprog.lua:232-247`, `root/proto14`).

`executeGameCommand` returns false for an exact true `isTutorialLock(5)` or
`isSubTargetSelectMode()` (PCs 0-14) and for a falsey usable flag (PCs 38-41).
With config flag 15 set, a repeat of the casting command with a positive cast
time calls `cancelCommand` and returns true (PCs 42-85). Past those checks,
when the command's target control mode is 0, it calls
`desktopWidget:executePlayerCommand(command, nil, 0, category)` (PC 117). A
nonzero mode takes the sub-target branch at lines 959-992 instead. The
[connector forwarding contract](equipment-cancel-command-contracts.md#callers-and-arguments)
then yields these submitted values:

```text
(nil, 0, category, nil, resolvedTarget, nil, nil, nil, nil)
```

With category 1 this is the typed shape
`nil,0,1,nil,reference,nil,nil,nil,nil` measured for the five default requests
in `xivl-captures:studies/c2s-012d-event-start/README.md`, Combat stance
request context. That capture does not identify the input that raised those
requests.

Within this script sequence, `ActionMenuWidget.processUICommandEvent` is the
handler that reaches `executePlayerCommand`. Actual callback delivery and any
resulting server request remain outside this static route.

## Local refusals

`PlayerBaseClass.canCommand` (`chara/player/playerbaseclass.lua:1978-2022`,
`root/proto45`) returns false while `playerWork.commandBurstBlocker` is
nonnil, except for a nil command or command IDs 12017 and 12009 (PCs 0-14).
`PlayerBaseClass.command` (lines 1911-1973, `root/proto44`) writes 1 to that
field after a `canCommand` pass (PC 54). The field is declared `timer` at lines
478-479. Its duration and clearing are not established here.

`canCommand` calls the command's `canFire`. In `GameCommandBaseClass`,
`canFire` calls `processCanFire`, which tailcalls `checkFireImpl` after its
earlier checks. These base methods apply the following refusals:

| Method | Lines | Refusal |
| --- | --- | --- |
| `processCanCommandForSkill` | `command/game/gamecommandbaseclass.lua:216-239`, `root/proto8`, PC 13 | `(false, 32527)` when `searchCommandSlot` finds a slot whose `getCommandSlotCompatibility` is falsey. |
| `checkFireImpl` | 2330-2454, `root/proto112`, PCs 18-28 and 74-90 | Calls the skill check, then returns `(false, 32546)` when the TP cost, after any combo scaling, exceeds `getTP`. |
| `processCanFireWithoutTarget` | 2517-2642, `root/proto114`, PCs 18-28 and 62-78 | Makes the same skill and TP checks for `isStackIntoActionMenu` (connector lines 15506-15543). |

`getCommandSlotCompatibility` reads
`charaWork.parameterSave.commandSlot_compatibility[slot]`
(`chara/charabaseclass_parameter.lua:141-148`, `root/proto10`). Subclass
overrides remain per command.

## Source identity

Inputs are from FINAL FANTASY XIV build `2012.09.19.0001`. Canonical sources
match [scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
Original resources and decoded payloads match
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
PCs are zero-based and count instructions. `root/protoN` is the prototype that
unluac prints as `main/fN`.

| Canonical source after `lua/scripts/` | Bytes / lines | SHA-256 |
| --- | --- | --- |
| `widget/actionmenuwidget.lua` | 61888 / 2773 | `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea` |
| `widget/desktopwidget_connector.lua` | 660617 / 26564 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/desktopwidget.lua` | 7929 / 402 | `5d3bfabf2e8a55ee2e64f607bdada5f04046c9528e9e9aca858e9ad9e232070a` |
| `command/game/gamecommandbaseclass.lua` | 55102 / 2698 | `75f366ca597f77a8e4b506fa8d7b214171cfdbb8d913fa12aa685d72a0b3256b` |
| `chara/charabaseclass_parameter.lua` | 36465 / 1867 | `748c02dbf42329dd0b942642b5fe68b35f422db61c482954e3b00d0338f12893` |
| `chara/charabaseclass_cliprog.lua` | 8202 / 454 | `ea04844921f8820562afd172845cab7baf2df235725d20ad179bb713754c87fd` |
| `chara/player/playerbaseclass.lua` | 66466 / 3020 | `6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
