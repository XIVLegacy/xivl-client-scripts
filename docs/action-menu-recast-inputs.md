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

## WorkSync refresh

`CharaBaseClass.initCommonParameterSync` in
`chara/charabaseclass_parameter.lua` (`main/f40`, PCs 184-208) declares
`commandDetailForSelf` with interval 1 and the actor as receiver.
The group contains `parameterSave.commandSlot_recastTime`,
`parameterSave.commandSlot_compatibility`, `parameterTemp.maxCommandRecastTime`
and two force-control members. The recast arrays are integer32 and
integer16, respectively. Their getters (`main/f11` and `main/f12`,
PCs 0-4) read the supplied one-based slot directly from the respective
`charaWork` table. The parameter script is installed as
`729s9/729s989r57y9rr_u9s9x5q5s.le.lpb`. The manifests above pin this
script, `chara/charabaseclass.lua` and `chara/player/playerbaseclass.lua`.
[Work declarations](https://github.com/XIVLegacy/xivl-client-structs/blob/8a8930c6da61d1ff8b3d442fe169396805394d23/docs/work-binder-native-contract.md#tag-groups)

The retained `combat_skills.pcapng` record at lane 0, frame index 47,
subevent index 1, contains slot-zero maximum and deadline hashes
`0x620811c8` and `0x8d974f1c`, of widths 2 and 4, at stream offsets
1 and 8. Both precede the `charaWork/commandDetailForSelf` marker.
The following record starts at offset 48, consistent with the marker's
30-byte text and one-byte tag occupying offsets 17-47.
[Capture rows](https://github.com/XIVLegacy/xivl-captures/blob/9c827fd1d84e12f7a462e6cd5234d874c0e886c9/studies/property-stream-hash-catalog/derived/property-records.csv#L214-L217)
[Hash identities](https://github.com/XIVLegacy/xivl-client-structs/blob/8a8930c6da61d1ff8b3d442fe169396805394d23/manifests/gam_hash_names.json)

The ordinary actor `0x0137` path applies properties at `0x00775652`
before processing completion at `0x007756F2`. Its unindexed tag for
the 30-byte name is `0xA0`. The admitted callback receives
`charaWork` and `commandDetailForSelf` after the actor receiver.
`PlayerBaseClass._onUpdateWork` (`main/f30`, PCs 103-109) passes this
group to its superclass. `CharaBaseClass._onUpdateWork` (`main/f23`,
PCs 42-49) forwards the actor, table and tag to
`desktopWidget:processCharacterParameterUpdated`. The route still
depends on native target, readiness and owner admission.
[Actor completion contract](https://github.com/XIVLegacy/xivl-decomp/blob/bb704f191da2b02d7e9b46a1835209e5feb64d1a/docs/net/actor-work-completion-targets.md)

The Desktop callback (`main/f78`, PCs 108-115 and 141-145) requires
truthy `actor:isPlayer()` and `actor:isMyPlayer()`, then calls
`updateActionMenuWidget(false)`. The latter (`main/f168`, PCs 0-16)
uses static widget 7 and calls `updateActionMenuEnabled`. The false
argument skips the ready-command and slot rescan. The absent second
argument bypasses the Window visibility, sub-target and focus branch.
The enabled refresh (`actionmenuwidget.lua`, `main/f6`, PCs 0-3)
updates the current page's slots and then the battle-mode display.
The slot timer requests have no Window-show or sub-target guard in
that refresh.

## Deadline and remainder

`desktopwidget_connector.lua:12787-12827` (`main/f253`, PCs 26-45) implements the command-present
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

On the admitted timer start, `RunningValue` triggers the installed
TimerIcon style's `Percent` animation. The slot refresh makes no query of
`AnimeTime`. The Timeline-to-TimerIcon reverse binding is a separate
style path. A WidgetBase TimeSpan return is unnecessary for the sweep.
[TimerIcon style](https://github.com/XIVLegacy/xivl-decomp/blob/bb704f191da2b02d7e9b46a1835209e5feb64d1a/docs/resource/action-menu-timer-icon-style.md#observed-form-and-style-declarations)
[TimeSpan and repeated name lookup](https://github.com/XIVLegacy/xivl-decomp/blob/bb704f191da2b02d7e9b46a1835209e5feb64d1a/docs/resource/sqwt-timer-icon-recast-inputs.md#observed-widgetbase-lookup-boundaries)

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
