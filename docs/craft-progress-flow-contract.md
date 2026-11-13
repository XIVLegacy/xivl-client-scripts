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
