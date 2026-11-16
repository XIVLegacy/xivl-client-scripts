# Action bar placement gate

Retail 1.23b does not register a placement confirmation event for current-class or
job-action icons. `ActionSettingWidget.init` assigns control work to the ClassAction and
JobAction controls, but calls `setButtonEvent` only for AddAction, ProductionCommand,
BattleCommand, and Godsend. `setButtonEvent` installs the confirmation condition and
command parameter; without it, an action icon can provide focus and detail state without
dispatching placement.

| Control | Control work | Confirmation binding | Operation |
| --- | --- | --- | --- |
| ClassAction | `actionsettingwidget.lua:118-122` | none | none |
| AddAction | `actionsettingwidget.lua:124-128` | `actionsettingwidget.lua:160-164` | 3 |
| JobAction | `actionsettingwidget.lua:154-158` | none | none |
| BattleCommand | `actionsettingwidget.lua:142-146` | `actionsettingwidget.lua:172-176` | 1 |

The shared list builder stores each displayed command ID in control user-work integer 3
(`actionsettingwidget.lua:3893-4023`). `setClassAction` and `setJobAction` both call
that builder (`actionsettingwidget.lua:2930-2940`, `3043-3053`), so their list data does
not create a placement event. `processUICommandOperate` dispatches operation 3 to
`equipAction(0, command)` (`actionsettingwidget.lua:433-443`); operation 1 handles a
bar-slot click (`actionsettingwidget.lua:321-391`). This explains why an Additional
Action can select and place immediately while a current-class action can show selection
or detail state and then do nothing on a slot click.

The list builder uses negative level entries to call `isAcquiredAdditionalCommand`
(`actionsettingwidget.lua:3909-3916`); positive class-action levels do not take that
branch. That is an availability/display distinction, not the placement gate.

The script identity is pinned by
`xivl-client-scripts:manifests/scripts.json:14841-14844`
(`lua/scripts/widget/actionsettingwidget.lua`, SHA256
`875CA1651F984A6135D8C2439FFE1DD9DD997898720D9C2C5559A9FA57F3CABF`). The retail text
table is pinned by `xivl-client-data:manifests/tables.json:5891-5896`
(`csv/worldMaster.csv`, SHA256
`2E2E2DD5CD9651388F6FA575B4229081AD0452165E78B725DF0A5B5B7CF7C643`); row 30745 at
decoded table line 801 states, `Actions of your current class or job cannot be removed.`
The same policy appears in the [Patch 1.20
notes](https://forum.square-enix.com/ffxiv/threads/32606), which describe current-class
actions as automatically set and not voluntarily removable while allowing them to move
and reapplying them on class change.

## Actions and Traits lists and help panel

`MainMenuWidget.processUICommandSelectionChanged` opens `ActionSettingWidget`
for `ListBox_MainMenu` item 2 (`mainmenuwidget.lua:416-695`), and the desktop
connector's `processUICommandEvent` opens it for
`UILuaCommands.ShortCutActionActionMenu` (`desktopwidget_connector.lua:3199-4175`).

`setBattleGrid` passes class IDs 3, 2, 4, 8, 7, 23, and 22 to `setClassButton`
with the prefix `Button_FighterSorcerer_` (`actionsettingwidget.lua:945-970`).
`setCraftGrid` passes IDs 29 through 36 and `setGatherGrid` passes 39 through
41 with `Button_GathererCrafter_`; the gather grid hides buttons 4 through 8
(`:973-1032`).

`setJobAction` hides `Grid_JobAction` unless `isJob` accepts the actor's
`getMainClassOrJob` value (`:2943-3053`). It selects a base index by job ID:
15 to 11, 16 to 1, 17 to 6, 18 to 21, 19 to 16, 26 to 31, and 27 to 26. For
`n` from 0 through 4 it tests `isAcquiredAdditionalCommand(base + n)` and
takes the matching entry of the 36-entry `getAdditionalCommandList`
(`chara/charabaseclass_ffxivbattle.lua:317-395`) for the five
`Button_JobAction_` slots. `setClassAction` and `setSpecialSkill` hold literal
command and level lists selected by class ID. `setClassAction` takes that ID
as an argument defaulting to `getStateMainSkill`; `setSpecialSkill` reads
`getStateMainSkill` (`:2153-2940`, `:3056-3430`). A job overlay therefore does
not select the trait list.

`setHelp` loads `gameCommandBasicSheet` for the command ID (`:4084-4109`).
`processSpreadSheetDataAsync` reads position 119 first. A nonzero value
passes only position 39 to `setCommandInfo`; zero passes positions 38, 39,
40, 76, 79, 115, and 114 (`:551-622`). `setCommandInfo` shows position 38 in
`TextBlock_SkillName`, 39 in `Grid_BestLevel`, 40 in `Grid_Compatibility`, 76
as cast time, 79 as recast time, 115 as TP cost, and 114 as MP cost through
`calculateCommandCost`; it hides each grid whose value is not positive
(`:625-783`). Position 119 is nonzero in 624 of the 1,611
`gameCommandBasic.csv` rows; its meaning is not established.
`equipAction(a, b)` and `equipGodsend(a, b)` call `executePlayerEquipAction`
with first argument 0 and 1 respectively, then `a`, `b`, and 0
(`:4112-4139`).

A prior external lead,
`docs/job_system_soulstone_actionbar_battle_regimen_2026-09-27.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, listed the grid and job-window
limits and the help-panel positions as open. `mainmenuwidget.lua` is pinned by
SHA256 `7DFD161C2852A56FD598F47469CC2D7597BA9F0E4B228555A09274674B2B4E41`
and `xivl-client-data:csv/gameCommandBasic.csv` by SHA256
`4D2D75D88E96D56D1B4812B27D1D8CBA68919EC9A4D4E2527647F4AE38CF7424`.

## Acquisition state is independent of placement

The pinned `ffxivgame.exe` is retail 1.23b, image base `0x00400000`, SHA256
`9341F2B4567440B310A4D494F5CC5599CA334BA51C8042247317FF466492F2E9`.
Its decoded scripts declare `charaWork.commandAcquired` as a 4,096-element boolean
array (`charabaseclass.lua:558-565`) and bind it as work id 3001
(`playerbaseclass.lua:1037-1041`). `isCommandAcquired` maps command ids below 30000 to
`commandAcquired[commandId - 26000]`; ids at or above 30000 return true without reading
the array (`charabaseclass_cliprog.lua:205-229`). Thus command 27100 maps to index 1100.
The declaration and work-id binding establish layout and initialization routing, but not
the initial value: no retained retail property record resolves to
`charaWork.commandAcquired[1100]` (backward-Murmur2 id `0x9D32B3C6`).

`charaWork.additionalCommandAcquired` is a separate 36-element boolean array
(`charabaseclass.lua:724-743`). `isAcquiredAdditionalCommand` reads that array directly
(`playerbaseclass.lua:1112-1120`). The Actions and Traits list builder uses the latter
for negative availability entries (`actionsettingwidget.lua:3909-3916`), while the
Additional Action class chooser uses `checkClassCommandPermission`
(`actionsettingwidget.lua:1181-1195`). The decoded script corpus has no call site for
`isCommandAcquired`; in particular, neither list construction nor placement/removal
calls it.

The class chooser passes each class button's user-work integer 4 to
`CharaBaseClass.checkClassCommandPermission` (`actionsettingwidget.lua:1181-1195`).
The method accepts every class when `_getJob()` is zero. For the seven listed jobs,
it accepts only the following class IDs; all other tested IDs return false:

| Job ID and name | Accepted class IDs and names |
| --- | --- |
| 15 Monk | 2 Pugilist, 8 Lancer, 7 Archer |
| 16 Paladin | 3 Gladiator, 4 Marauder, 23 Conjurer |
| 17 Warrior | 4 Marauder, 3 Gladiator, 2 Pugilist |
| 18 Bard | 7 Archer, 23 Conjurer, 22 Thaumaturge |
| 19 Dragoon | 8 Lancer, 2 Pugilist, 7 Archer |
| 26 Black Mage | 22 Thaumaturge, 2 Pugilist, 7 Archer |
| 27 White Mage | 23 Conjurer, 3 Gladiator, 2 Pugilist |

This is a client chooser visibility rule, not proof of server acceptance or of an
individual action's equip eligibility. The source is
`chara/charabaseclass_ffxivbattle.lua:113-220` (manifest
`manifests/scripts.json:410-414`, SHA256
`D1DB23D11F911EA3205CA72868CC9FCA22CEFE0D3F88A6706CBB035D92130BDA`).
The LPB is `client/script/729s9/729s989r57y9rr_44m1o89qqy5.le.lpb`
(SHA256 `E64BE9F43A2659E81FC93D3CD08BA58EA646A24F6B43C109B75B6F9E59F9CE3E`);
its decoded LUAC SHA256 is
`98DEEFF94BB4C526A6018F22379DDBE146B55394EB8FCF198B4B0E1D2D316976`.
Bytecode method `checkClassCommandPermission` explicitly returns false at
`0x0008B6-0x0008BA` and `0x0008C2-0x0008C6`, where the recovered Lua prints
`_FOR_`. Names are from `xivl-client-data:csv/xtx_text_jobName.csv` (manifest
`manifests/tables.json:6346-6351`, SHA256
`61535798445DDB716CD16E8B68B06D9C6A67F76C321FE0DD5E9840C143DE8B57`).

The removal button passes `(slot, 0, kind)` to `executePlayerEquipAction`
(`actionequiplistwidget.lua:121-144`). That connector invokes the normal command path
and does not update either acquisition array
(`desktopwidget_connector.lua:17462-17527`). The nearby
`updatePlayerCommandAcquired` method is a separate bridge to
`PlayerBase.updateCommandAcquired`, and the decoded corpus contains no call site for it
(`desktopwidget_connector.lua:17564-17579`). `updateCommandAcquired` subtracts 26000
from both requested command-id bounds and calls `_updateWork` for
`charaWork/commandAcquired` (`charabaseclass.lua:1532-1566`); it is an explicit work
request, not part of slot removal.

On the native receive path, s2c opcode `0x0137` enters
`SyncMemoryReceiver` at `FUN_0089E550`, then follows
`FUN_00775A30 -> FUN_00775180`. Its conditional Lua notification path reaches
`FUN_00774220 -> FUN_00773F10` (`_onUpdateWork`). The script callback treats
`charaWork/commandAcquired` specially only by forwarding its changed index range to the
desktop UI (`charabaseclass.lua:1182-1188`, `1569-1579`). Other work, including
`charaWork/command`, follows the generic parameter-update callback. The explicit
client-to-server `_updateWork` path is the N-API implementation at `FUN_006E7670`, with
the `0x012F` builder at `FUN_0075E770`; it is not reached by the removal button path.

The retained `action_and_traits.pcapng` specimen (SHA256
`C3D30FE46D69996DC74E4864245C42675CDE2388525C03063DAC180DF528352F`)
contains two relevant transactions, not a true remove/re-add pair:

| UTC | Pcap frames | Direct observation |
| --- | --- | --- |
| 2012-12-31 01:26:11.657-12.470 | 95, 99, 103 | `commandForced` requests `(13, 27194)`; the reply clears `charaWork.command[43]`, sets `[44]` to `0xA0F06A3A`, updates only the paired recast/compatibility fields, and acknowledges `(13, 27194)`. |
| 2012-12-31 01:26:13.418-13.980 | 126, 129 | `commandForced` requests `(12, 27194)` and reverses those two slot writes before acknowledging `(12, 27194)`. |

Neither `0x0137` reply contains a `commandAcquired` or
`additionalCommandAcquired` property. The second placement succeeds after the first
transaction cleared the old slot, directly showing that a move does not require an
acquisition reassertion. A scan of the retained 1.23b capture corpus found no
`EquipAbilityCommand` request with command id zero, so the exact retail reply to a pure
Additional Action removal remains uncaptured.

The supported conclusion is that acquisition and hotbar occupancy are orthogonal.
Direct script evidence shows that removal does not write acquisition state and that the
relevant action-list checks do not consume `commandAcquired`; capture evidence shows a
slot clear followed by successful replacement without an acquisition property. It is
therefore redundant for a server to reassert `commandAcquired[commandId - 26000]` solely
because it cleared that command's hotbar slot. Whether retail redundantly included such
a property in a pure-remove acknowledgement is still unknown, but that wire-parity gap
does not make the value necessary for client behavior.

Script identities are pinned in `manifests/scripts.json`: `charabaseclass.lua` SHA256
`F17B3E62A137D8F524BA88D55296E1FB064512DC803F7A85DC980DD4BCBC9625`,
`charabaseclass_cliprog.lua` SHA256
`EA04844921F8820562AFD172845CAB7BAF2DF235725D20AD179BB713754C87FD`,
`playerbaseclass.lua` SHA256
`6226B3FA15DFDBAD279B7DBA453F8A3B76FCB8B68BAD6E14F5403D52987F76E4`,
`actionequiplistwidget.lua` SHA256
`782D96D9F92E012913300E484250F3A6D7063E366F7B8B5EE5A9931755426EEF`,
and `desktopwidget_connector.lua` SHA256
`9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01`.

## Command icon text and detail work

`setIconList`, the shared list builder (`actionsettingwidget.lua:3893-4023`),
calls `setText` on `<prefix><n>:TextBlock_CommandData` with text row 10214
and the arguments command ID and 36 (`:3926-3933`) for an entry that passes
the level test at `:3924`.
`setCommandIcon` writes the same row and arguments when its command is not 0,
then sets the visibility of `:IconControl_CommandIcon` to whether it wrote
(`:2019-2049`). `setCommandInfo` writes row 10214 with the help command ID
and 36 to `TextBlock_CommandHelpIcon` (`:625-783`).

The template `client/sqwt/widget/ActionSettingWidget.tpl` (7433 stored
bytes, SHA256
`CC07F15DF3C5C2FCABD08D4E0FD0FBD4AFAB83863008B68557B65EBEF6444ECA`, 7425
decoded bytes, SHA256
`DEF8486A5E91A804EC6B470767E1B61E998A95D66B9F4D2CBFA77276071AA42C`)
declares a hidden `TextBlock_CommandData` and an `IconControl_CommandIcon`
with `IconDatas="{Binding Path=Text Mode=OneWay ElementName=TextBlock_CommandData}"`
in `ControlTemplate_Button_BattleCommand` (decoded lines 2-11),
`ControlTemplate_Button_BattleCommand_2` (lines 23-38) and
`ControlTemplate_Button_Command` (lines 50-65).
`ControlTemplate_Button_Class` (line 77) declares `IconDatas="0"` instead.
The form `client/sqwt/widget/ActionSettingWidget.form` (65519 stored
bytes, SHA256
`7E5053EBAF8918CDAB08CC51AC3A6D0ABACBE5E16E84E64C5AB84935D9D98638`, 65511
decoded bytes, SHA256
`1CA68AE60818FA14044DDC809AD192BFFF242843F15F07EBA061BD8D7C9155AF`) gives
the ClassAction, JobAction, AddAction, BattleCommand and Godsend buttons the
`_BattleCommand_2` template, the ProductionCommand and PropertyCommand
buttons `_Command`, and the FighterSorcerer and GathererCrafter class
buttons `_Class`. Its help panel binds `IconDatas` to
`TextBlock_CommandHelpIcon` the same way (decoded line 520). Decode each
SQWT file with its basename as the Blowfish key after the eight-byte
wrapper, or with `xivl-cli extract-resource --as sqwt`.

String columns 0 to 3 of `xtx/_text_ui` row 10214 each hold the single
frame `022817ff1167616d65436f6d6d616e644261736963e802e80303`, written as a
`[@sheet:...]` cell, and column 4 is empty
(`xivl-client-data:csv/xtx__text_ui.csv`, SHA256
`23762A422118D99C4144A48B3495C52511B1B1B865E4FC50FDC61A973E3C6ECE` in
`xivl-client-data:manifests/tables.json`). It is a `0x28` named-sheet
request whose sheet name is the string `gameCommandBasic`, whose row is
`0xE8 0x02` and whose field is `0xE8 0x03`. The handler decodes the name,
then the row, then the field
(`xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03),
and `0xE8` selects a supplied argument by its one-based index
(`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-04).
Read with the literal bytes `0x02` and `0x03` as indexes 1 and 2, the row
is the command ID and the field is 36.
In `xivl-client-data:csv/gameCommandBasic.csv` (SHA256
`4D2D75D88E96D56D1B4812B27D1D8CBA68919EC9A4D4E2527647F4AE38CF7424`),
column 36 holds 30086 for command 27150 and 30021 for command 27100.

INFERRED. Each row's icon is the `gameCommandBasic` field 36 of its command,
which the bound `IconDatas` reads as text. That logical field 36 maps to
decoded CSV column 36 is not checked against the field map of the handler,
and the native `IconDatas` parse of the text is not traced here.

`update` (`:786-856`) reads `getControlUserWorkString(1, "Grid_Detail")` and,
when the result is not `""`, reads `getControlUserWorkInt(3, result)` and
passes it to `setHelp` (`:838-853`). The only writer of that string slot is
`processUICommandEnterFocus` (`:511-546`). When user work integer 1 of the
focused control is 1 to 4, it calls `setHelp` with that control's user work
integer 3 and then stores the control name there (`:536-545`). An `update`
before the first such focus therefore reads a slot the script never wrote.
The value the native call returns for such a slot is not established here.

## Button markup command

The form `client/sqwt/widget/ActionSettingWidget.form`, pinned in the
section above, declares 140 Buttons. Every one carries the markup attribute
`Command="UILuaCommands.Operate"`, and none carries a `CommandParameter`, a
`CommandTarget` or a trigger. The form declares no trigger element at all.
By name family the Buttons are `Button_BattleCommand_` 30, `Button_ClassAction_`
20, `Button_AddAction_` 20, `Button_PropertyCommand_` 20,
`Button_ProductionCommand_` 20, `Button_Godsend_` 10,
`Button_GathererCrafter_` 8, `Button_FighterSorcerer_` 7 and
`Button_JobAction_` 5. The template `ActionSettingWidget.tpl`, pinned above,
declares eight EventTriggers, a `MouseEnter` with `SourceType="Button"` and a
`GotAnchor` in each of its four ControlTemplates, and no other trigger.

`setButtonEvent` (`actionsettingwidget.lua:1335-1358`) calls
`setConfirmCondition` and `setCommandParameter`. The Operate a placement
Button raises carries no markup parameter, so its integer is inferred to be
the one `setButtonEvent` writes. The native delivery of
that integer is in
`xivl-decomp:docs/resource/sqwt-command-parameter-consumer.md`, sections
"Kind switch" and "Script entry". A ClassAction or JobAction Button raises
the same markup command with no `setButtonEvent` write, which the
[placement gate](#action-bar-placement-gate) above leaves without an
operation.

Decode the form and template as the section above states and count the
`Button` elements and their attributes.

## Keyboard focus mark

Each of the four ControlTemplates of `ActionSettingWidget.tpl`, pinned above,
sets the templated Button's `IsTabStop` to `False` and its `Anchor` to
`None` through Setters, and holds a `Label_IconEffect` with
`IsTabStop="True"` and the style `LAB_basis_iconHoverEffect` (decoded lines
10, 36, 63 and 86). Each template's `GotAnchor` EventTrigger (decoded lines
17, 44, 71 and 93) runs `ExecuteCommandAction` with
`Command="UILuaCommands.EnterKeyboardFocus"` and the templated parent's
`Name` as `CommandParameter`, then a `SoundPlayerAction` with
`FileNumber="3"`.

The style `LAB_basis_iconHoverEffect` of `client/sqwt/common/default.style`
(identity in [point allotment Ask](point-allotment-ask-contract.md#installed-form),
decoded line 2097) draws the skin `LAB_basis_iconHoverEffect` for
`SkinHover`, `SkinActive` and `SkinAnchored` and `NULL` for `SkinNormal`,
`SkinDisabled`, `SkinFocused`, `SkinReserved` and `SkinDroppable`.

INFERRED. The keyboard anchor of an action Button sits on its
`Label_IconEffect`, whose skin marks it, and `GotAnchor` routes the focus to
`processUICommandEnterFocus` (`:511-548`). The native step that puts the
anchor on the Label when a key moves the focus is not traced here.

## Update after a command change

In `DesktopWidget.processCharacterParameterUpdated`
(`widget/desktopwidget_connector.lua:4841-5340`), the local player arm
treats the update groups `command` and `commandEquip` alike
(`:4979-5003`). It calls `updateActionMenuWidget(true)` and
`updateMainMenuWidget()`, then `getWidget(3, "ActionSettingWidget")` and,
when that answers a widget, its `update`. The group `commandDetailForSelf`
calls only `updateActionMenuWidget(false)` (`:5007-5011`).

`update` (`:786-856`) calls `setEquipAction` (`:1900-1938`), which asks
`desktopWidget:getPlayerEquippedCustomCommand(slot)` for slots 1 to 30. A
slot whose first answer is not nil and whose third answer is true takes
`desktopWidget:getCommandID` of the first answer, any other slot takes 0,
and the script calls `setCommandIcon` and `setCommandIconEquipBar` on
`Button_BattleCommand_<slot>` with that ID either way.

INFERRED. Each `command` update repaints all 30 bar slots of an open
Actions and Traits window from the native equipped list.
