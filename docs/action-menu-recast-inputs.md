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
| `widget/widgetbaseclass_common.lua` | `n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 69077 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |

Use the same JAR's `--disassemble` on the decoded chunks to check the
function selectors and zero-based PCs below. PCs count instructions, excluding
labels and directives. The ActionMenu and shared-wrapper carrier and chunk
identities are recorded in the [coverage manifest](../manifests/retail_lua_coverage.json).

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
`2624-2642` (`main/f58`, PCs 0-12) returns the ordinary icon, timer icon, and grid paths, in that order. The suffixes are
`:IconControl_Command_1`, `:IconControl_Command_2`, and `:Grid_Command`.

### Initial icon writes

STATIC. `init` at canonical lines 209-211 (`main/f0`, PCs 152-154)
calls `clearSlots(1)`. `clearSlots` at 1508-1524 (`main/f21`,
PCs 0-12) rejects a starting value below 1 or above 30. Otherwise it
calls `removeSlot` for each index from that value through 30. On normal
return from the preceding calls, initialization therefore visits slots
1 through 30.

`removeSlot` at 2030-2049 (`main/f35`, PCs 6-21) selects the three
paths from `getSlotIconName`, then makes these requests in order.

| Receiver | Request | PCs |
| --- | --- | --- |
| Timer icon path | `IconDatas` numeric 0 | 9-13 |
| Timer icon path | `setHidden` | 14-16 |
| Ordinary icon path | `IconDatas` numeric 245 | 17-21 |

The shared `setControlProperty` at `widgetbaseclass_common.lua:1477-1488`
(`main/f68`, PCs 0-6) forwards nil, the control path, the property name
and the supplied values to `_setProperty`, with no requested result.
`setHidden` and `setItemHidden` at 1692-1715 (`main/f81`, PCs 0-4,
and `main/f82`, PCs 0-6) request `_setProperty` with nil, that timer
path, `Visibility`, and the string `Hidden`. Each request names a concrete part returned by `getSlotIconName`.

The [native property bridge](https://github.com/XIVLegacy/xivl-decomp/blob/5e98eddddba063ee4061105f51215270a5eb7c18/docs/script/status-effect-widget-lifecycle.md#exact-property-arguments)
selects current-form routing for nil and formats integer values with `%d`
at `0x005425B0` before the string property engine at `0x00537DE0`.
The [ordinary IconControl input and renderer](https://github.com/XIVLegacy/xivl-decomp/blob/5e98eddddba063ee4061105f51215270a5eb7c18/docs/resource/sqwt-icon-control-textures.md#observed-numeric-input-and-resource-resolution)
owns the numeric parser and guarded resource route. Zero follows the numeric image-ID path. Successful part lookup, property
admission, retained renderer identity, texture availability and actual
painting remain unresolved for these ActionMenu requests.

### Recast writes

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
appearance, cost and recast requests.

The action also omits `CommandParameter`. On the checked native route it
retains the kind-0 default record. If `Executed` reaches the matching root
subscription and the priority-5 Event path admits it, the native callback
passes exactly nil, `_widget` and `UILuaCommands.TimerEnd` after the Lua
receiver. The shared wrapper forwards five slots, so both payload slots
are nil. [Native default parameter and root Event](https://github.com/XIVLegacy/xivl-decomp/blob/c4ad63382f08e846b68b0dc1c074335b82d1ce52/docs/resource/action-menu-timer-icon-style.md#timerend-default-parameter-and-root-event)
Actual route admission, priority gating and live delivery remain unresolved.
