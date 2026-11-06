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

## TimerEnd refresh

`actionmenuwidget.lua` registers `UILuaCommands.TimerEnd` through
`setUICommandCondition` at lines 160-163 (`main/f0`, zero-based PCs
110-112). The shared wrapper in `widgetbaseclass_common.lua` at
1286-1296 (`main/f54`, PCs 0-4) passes `_widget`, the command and
numeric `5` to the plain `_setUICommandCondition` native. Successful
registration keys the subscription to the ActionMenu form root and sets
condition byte `+0x54` to 0 and priority byte `+0x55` to 5. Matching
delivery selects the Event path at `0x00896AF0`, subject to the
native gates. The shared `_onUICommandEvent` in `widgetbaseclass.lua`
at 250-257 (`main/f6`, PCs 6-12) forwards five argument slots to
`processUICommandEvent`. [Shared registration and callback](https://github.com/XIVLegacy/xivl-client-scripts/blob/a99d17dc70e7017347c8ab2619537117ca0d9593/docs/action-menu-page-controls.md#L60-L88)

On the checked normal-return completion path, the template's
`TimerIcon.PercentAnimeEnd` trigger requests Sparkle sequences
`No_anime` and `Effect_start` at lines 577-578 before issuing
`UILuaCommands.TimerEnd` at 579. [Native completion action order](https://github.com/XIVLegacy/xivl-decomp/blob/2ee3fa0e087724da7e7b89274c955f04e5c37c48/docs/resource/action-menu-timer-icon-style.md#L116-L151)

The `TimerEnd` action omits `CommandTarget`. The native fallback at
`0x009B2B40` uses the trigger event source on a successful
FrameworkElement cast. With that cast and a retained `RoutedCommand`,
the checked completion path starts at the TimerIcon. If `PreviewExecuted`
leaves the event unhandled, `Executed` bubbles from that TimerIcon and can
reach the Window handler if the route continues. The `_widget` key applies
at that root subscription. [Native action target and route](https://github.com/XIVLegacy/xivl-decomp/blob/2ee3fa0e087724da7e7b89274c955f04e5c37c48/docs/resource/sqwt-command-parameter-consumer.md#L404-L430)

On an admitted `TimerEnd`, `processUICommandEvent` at lines 553-556
(`main/f1`, PCs 241-245) calls `updateMainSlotEnabled` with the
widget receiver alone. The refresh visits the current page's ten
slots (1225-1232 and 2760-2770) and recomputes the applicable icon
appearance, cost and recast requests. Live delivery to the root and
the native payload defaults remain unresolved.
