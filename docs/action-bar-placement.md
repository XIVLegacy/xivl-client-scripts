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
