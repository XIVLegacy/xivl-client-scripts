# ActionMenu recast inputs

`ActionMenuWidget.updateMainSlotEnabled` sends the remaining recast time to
the second icon part of each qualifying action slot. It uses the recast
deadline to decide whether to restart that slot's timer.

## Source identity

These canonical decoded scripts are pinned by [the script manifest](../manifests/scripts.json).
For build `2012.09.19.0001`, decode their installed LPBs with
`tools/retail_script.py` and the [pinned unluac JAR](../tools/vendor/unluac/PROVENANCE.json). Match the canonical
output against the manifest before checking the cited lines.

| Decoded path under `lua/scripts/` | Installed path under `client/script/` | Canonical bytes | Canonical SHA-256 |
| --- | --- | --- | --- |
| `widget/actionmenuwidget.lua` | `n1635q/97q1vwx5wpn1635q.le.lpb` | 61888 | `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |

## Deadline and remainder

`desktopwidget_connector.lua:12787-12827` implements the command-present
path of `getRecastTimeForCustomCommand`. It returns early if the custom
command is missing or its `_isAlive` call returns false. It reads the
player's `getCommandRecastTime` and `getMaxCommandRecastTime` for the slot and subtracts
`WorldMaster._getServerTime` from the deadline. If the maximum is positive
and the remainder exceeds it, the method caps the remainder at that
maximum and leaves the deadline unchanged. The method returns the deadline
and the remainder, in that order.

## Slot writes

`actionmenuwidget.lua:2598-2608` constructs the slot label name from
`Label_CommandIcon_` and the slot number. `getSlotIconName` at
`2624-2642` returns the ordinary icon, timer icon, and grid paths, in
that order. The second path appends `:IconControl_Command_2` to the label.

In `updateMainSlotEnabled` at `1248-1304`, the script selects that second
path, calls `getRecastTimeForCustomCommand`, and reads integer user work
slot 2 from the timer icon. It treats missing deadline and remainder as
zero and requires both values to be positive and command-slot
compatibility to differ from false. When the deadline differs from the
stored value, `1305-1342` makes these requests in order.

| Receiver path | Request |
| --- | --- |
| Timer icon | Store the deadline in integer user work slot 2 |
| Timer icon | Write the remainder to `StartTime` |
| Timer icon | Write zero to `EndTime` |
| Timer icon | Write `RunningValue` 0, then 1 |
| Timer icon path with a second `:IconControl_Command_2` suffix | Write `Percent` 0 |

When the deadline matches, `1343-1360` reads `Percent` with that same
repeated suffix and checks whether it has reached 100. The reset branch
at `1370-1393` writes zero to the timer icon's integer user work slot 2,
`StartTime`, `EndTime`, and `RunningValue`, in that order.

The command handler at `553-556` calls `updateMainSlotEnabled` when it
receives `UILuaCommands.TimerEnd`. These are script request and consumer
edges. Native lookup of the repeated suffix, property admission, timer
math, and delivery of that command require native evidence.
