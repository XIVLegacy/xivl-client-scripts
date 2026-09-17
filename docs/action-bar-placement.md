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

This evidence establishes the UI event gate and the retail removal policy. It does not
establish command-acquisition packet encoding or a downstream native replacement
predicate; those are separate from the missing ClassAction and JobAction confirmation
binding.
