# EventItemSelectWidget contract

The widget presents up to 16 positive catalog IDs, tracks one numeric input per
heading-enabled row, and returns a 17-value producer tuple: acceptance followed
by `inputNumberTbl[1..16]`. Operate records values for rows whose
`headingEnableTbl[i] == true` and requests base result 1. `Button_Close` in
operate, or Cancel with `Button_Close` focused, requests base result -1; other
cancel paths navigate or no-op. A completed `askEventModeWidgetYield`
call with requested count 11 exposes only opening status, acceptance, and the
first ten numeric slots to its caller. No item consumption or server outcome
is established here.

## Source identity

The retail resource is recorded as
`n1635q/9rz/5o5wq1q5xr5y57qn1635q.le.lpb` in
`manifests/retail_lua_coverage.json:26433-26445`.
The resource is 8581 bytes with LPB SHA256
`EF8455C951DA987798A70C1F6D3C7EB4ABA1B8053B5C4682B48AC3F1E34D7CF1`; its
decoded payload is 8568 bytes with SHA256
`DB18B5D64C6127086C9D8CBDC71C3255405E76E25EBF375E92E7CB98354F4576`.
The canonical LF decompile is 27632 bytes, 1140 lines, and SHA256
`960C03CE273F37A80F9AF84E2F6BC1324035FD8537B316AB344DDDBBFC409160`,
matching `manifests/scripts.json:14907-14910`.

The registry identifies the class as `EventItemSelectWidget`, requiring
`/Widget/Ask/AskBaseClass`, with the 14 methods listed at
`lua/registry.json:38590-38614`. The API catalog confirms the receiver and
method windows at
`xivl-client-structs:manifests/lua_api_contract.json:145224-145313` and
`xivl-client-structs:manifests/lua_api_contract.json:145418-145426`.

## Initialization

`initAsk` has 19 fixed parameters. It creates four work properties:

- `updatecount`, initialized to 0;
- `catalogIdTbl[1..16]`, initialized to 0;
- `headingEnableTbl[1..16]`, initialized to false; and
- `inputNumberTbl[1..16]`, initialized to 0.

The fixed argument shape offers `A3..A18` as 16 catalog positions, but the
original copy loop processes only `1..#candidateTable` (proto0 PCs 59-84).
A nil hole can leave a positive later argument outside that Lua length scan, so
the body does not prove that all 16 positions are copied. A copied position is
heading-enabled only when its catalog value is greater than 0. `A1` and `A2`
are forwarded to the window-title helper. The method requests configuration of
16 item rows, operate/close controls, an `ItemDetailWidget` child, detail
positioning, and modal state. Heading-enabled catalogs are passed to an opaque
`worldMaster._getMyPlayer` virtual-item helper for icon/name presentation. A nil virtual-item result returns one
`false`; successful initialization returns no values.

## Item display and controls

`updateWindowDisplay` requests reset/visibility/property calls for every row,
including `setNumberInput(control, 0, 0, 0)` first, then computes package 1's
`filled = capacity - freeSpace` using opaque player helpers. Only `filled > 0`
enters the package scan; zero or negative `filled` makes no package-item calls.
It calls
`desktopWidget.getPlayerItemInPackage(1, index)` with four requested results.
The published connector contract identifies them as catalog ID, icon,
stackability, and stack count, and records `(0,0,false,0)` for a missing
package or out-of-range slot
(`xivl-decomp:docs/script/status-attributes-key-items.md:101-107`).
The widget compares catalog ID with each heading-enabled catalog, uses stackability as
the boolean branch, and uses stack count as the available count. It sums
matching earlier stack counts for a stackable item and uses count 1 for a
non-stackable item. It requests matching-row visibility, then assigns the
subsequent `getValue` return to local `current`. When `current > available`, it
first sets `current = available` and then requests `setValue(current)`. The
remaining matching-row path requests
`setNumberInput(control, 0, available, current)`, including when no clamp was
needed. In that no-clamp case, only the additional direct `setValue(current)`
request in `updateWindowDisplay` is skipped; the helper still requests
`Minimum`, `Maximum`, and `Value` in order. On the clamp path both the direct
request and the helper's `Value` request occur. It then requests the item-number
text and Grid `IsEnabled`. For example, a read of 5 with available 2 sets local
`current` to 2 and passes 2 to both setter requests independently
of whether the earlier reset took effect. It then requests operate-button
enablement. The heading
flag is independent of Grid `IsEnabled` and Label visibility; operate,
cancel-navigation, and operate-button checks use that heading flag even when a
grid is disabled or no inventory match exists.

The other item helpers have existing published native contracts. `_getItem`
uses 1-based package and slot integers and returns an item control or nil; an
absent package yields nil, while slot zero or past-end can reach the native
invalid-vector path (`xivl-client-structs:docs/scheduler-item-native-contract.md:287-355`).
`_getItemPackageCapacity(1)` returns an integer and zero for an absent package;
the capacity interpretation is inferred from the native name, just as the
free-space interpretation is
(`xivl-client-structs:docs/scheduler-item-native-contract.md:348-351`).
`_getItemPackageFreeSpace(1)` returns zero for an absent package; its
interpretation as a count of free slots is explicitly inferred from the native
name (`xivl-client-structs:docs/nameplate-group-native-contract.md:337-355`,
`xivl-client-structs:docs/chara-desktop-native-contract.md:88-107`). These
contracts establish helper inputs/results only, not widget eligibility or an
applied inventory effect.

`processAfterShow` calls the window refresh and requests focus on the first
visible label whose independent heading flag is true, or requests focus on
`Button_Close` when none is visible. It returns one `true`.

`setOperateButtonEnable` always requests `Button_Operate` `IsEnabled`, with true
when any input for a row whose `headingEnableTbl[i] == true` is greater than 0
and false otherwise, including all-zero input; Grid `IsEnabled` and inventory
matches do not gate this check. `setNumberInput` requests property
calls for `Minimum`, `Maximum`, and `Value` on a control in that order; it does
not prove those values were applied. `setWindowTitle` calls opaque
`_setProperty` only when its title argument is non-nil. `updatePlayerItem`
stores argument 2 and returns without refresh when argument 1 is numeric 0;
other updates decrement only a positive counter and refresh when it was zero or
becomes zero, not merely when a negative counter is nonpositive.

`setDetailPosition` requests parent position, parent size, desktop size, and
child size. It uses fallback parent width 500, child width 382, child height
280, with `initialLeft = parentLeft + 32 + parentWidth` and
`initialTop = parentTop + 32`. If `initialLeft + childWidth` exceeds desktop
width it subtracts that right-edge overflow from left. Its vertical comparison
is `initialTop + 400` against `0.95 * desktopHeight`, not child height; the
calculated child-height value is unused by that comparison. It then requests
child `Top` and `Left` in that order; these adjustments do not prove rendered
containment.

## Commands

`processUICommandOperate` recognizes the third argument as a control name.
For `Button_Operate`, it clears the 16 input slots, copies current values for
rows whose independent `headingEnableTbl[i] == true`, and calls
`setBaseAskResult(1)`. This test is independent of Grid `IsEnabled` and Label
visibility. For `Button_Close`, it calls
`setBaseAskResult(-1)`. Other names do nothing. It returns no values.

`processUICommandCancel` reads keyboard focus and returns immediately when it
is nil, before item-help close or focus fallback. `Button_Close` requests base
result -1. `Button_Operate` requests focus on `Button_Close`. An input-control
event requests focus on a different heading-enabled input; otherwise the helper
requests item-help close and requests focus on `Button_Close`. It does not set a result for these
navigation branches and returns no values.

`processUICommandDefault` dispatches `NumberInputBox.ValueChanged` to operate
enablement, `UILuaCommands.ButtonFocused` to item help, and
`UILuaCommands.LostFocus` to item-help close. It returns no values.

## Item help

`displayItemHelp` requires an `ItemDetailWidget` child and proceeds only when
the child is hidden. A nil control name returns one `false` when the child is
present. Otherwise it matches `Label_HitArea_i` or `Label_i` for
heading-enabled rows and scans package 1. At the first matching catalog it
calls player `_getItem(1, index)` and stops, even when that first item is nil;
there is no later-match retry. For a non-nil item it requests child
`displayItemHelp(item, 1, index, 1)` (four arguments after the receiver), sets
the local found flag, and requests title text 3207. These are opaque UI
requests, not proof of rendered output. With no match or a nil first match, it
requests `displayEmpty(7)`. It then requests detail positioning, modal false,
and show. Normal paths return no values. `closeItemHelp` calls `hide` when the
child exists and `isShow()` is true; the call does not prove completed hiding.

## Result tuple

`getAskResult` reads opaque `getBaseAskResult()`. The first result is false
exactly when the later getter returns base result -1, and true otherwise. The
remaining 16 results
are read from the current `inputNumberTbl[1]` through `[16]` values at producer
time. Its exact 17-value tuple is:

```text
(accepted, inputNumberTbl[1], inputNumberTbl[2], ..., inputNumberTbl[16])
```

The table starts all-zero. Operate updates it. The operate/cancel setter calls
are opaque requests and do not themselves prove what a later getter returns.
The cancel body has no local clear, but the producer makes no
blanket-preservation promise across outside calls: it reads the values present
when `getAskResult` runs. Neither a cancel call nor an accepted flag alone
proves a completed choice. The widget does not return an
item object, catalog ID, or separate inventory count; its numeric slots are the
selected UI input values. It does not return a consumption result or reward
outcome.

## Sources and methods

The LPB was decoded with `tools/retail_script.py` and the pinned
`tools/vendor/unluac/unluac_2025_12_23.jar` (796256 bytes, SHA256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`). The
original decoded chunk was parsed with `ChunkReader` and its words were
decoded with `instruction` from `tools/build_quest_contracts.py`. The checks
covered root closure/settable bindings, fixed parameters, code-vector starts,
raw CALL/RETURN operands, comparisons, loops, and result widths. The 14 method
locators are:

| Method | Root closure PC | Prototype | Code start byte | Instruction count |
| --- | ---: | --- | ---: | ---: |
| `initAsk` | 8 | `root/proto0` | 683 | 281 |
| `updateWindowDisplay` | 11 | `root/proto1` | 2769 | 185 |
| `processAfterShow` | 14 | `root/proto2` | 4051 | 39 |
| `processUICommandOperate` | 17 | `root/proto3` | 4420 | 39 |
| `processUICommandCancel` | 20 | `root/proto4` | 4826 | 54 |
| `processUICommandDefault` | 23 | `root/proto5` | 5339 | 14 |
| `updatePlayerItem` | 26 | `root/proto6` | 5598 | 23 |
| `setWindowTitle` | 29 | `root/proto7` | 5800 | 10 |
| `setNumberInput` | 32 | `root/proto8` | 5930 | 14 |
| `setOperateButtonEnable` | 35 | `root/proto9` | 6093 | 28 |
| `setDetailPosition` | 38 | `root/proto10` | 6425 | 50 |
| `displayItemHelp` | 41 | `root/proto11` | 6889 | 126 |
| `closeItemHelp` | 44 | `root/proto12` | 7920 | 12 |
| `getAskResult` | 47 | `root/proto13` | 8087 | 61 |

The decisive original operands include `root/proto13` PC 59, decoded byte
8323, `RETURN B=18,C=0` (17 values), and `root/proto0` PC 170, byte 1363,
`CALL B=2,C=0` followed by PC 171, byte 1367, `CALL B=0,C=1` (dynamic
arguments and zero results). No `CALL B=0,C=0` occurs in this resource.
These are static extraction checks, not runtime observations.

## Caller and evidence boundary

The published `Spl101.askEgg` caller sends ten scalar item IDs and retains
twelve slots from one widget-yield call; see
`docs/scrambled-eggs-askegg-contract.md:27-40`.
The published wrapper contract proves that the second
`askEventModeWidgetYield` argument is `requestedCount`, category 4 is supplied,
remaining arguments are forwarded through `askWidgetYield` and
`AskBaseClass.init`, open/select failure returns one `false`, and completed
selection returns `true,unpack(widgetResults,1,requestedCount)` after closing
(`docs/materia-meld-client-contract.md:134-143`,
`docs/materia-meld-client-contract.md:159-168`,
`docs/materia-meld-client-contract.md:196-202`).

For this call's `requestedCount=11`, completed forwarding is exactly 12 values:
opening `true`, then widget results 1 through 11. Conditionally on the
published same helper/class route, `initAsk` receives `A1=p0`, `A2=201`,
`A3..A12` as the ten catalog IDs in original order, and `A13..A18` as omitted
or nil. Caller slots map as `w1=true`, `w2=accepted`, and
`w3..w12=inputNumberTbl[1..10]`; six widget numeric slots are omitted. Here
`w2` is false exactly when the later `getBaseAskResult()` returns -1, and true
otherwise. Thus the completed-cancel tuple
`(nil,w8,w9,w10,w11,w12,nil,false)` is conditional on that later -1 getter
result, not on the setter call alone or on `accepted` by itself; the producer
reads current slots at that time and the cancel body performs no local clear.
A one-false open/select failure produces nil-adjusted retained slots and
`(nil,nil,nil,nil,nil,nil,nil,false)`. When the wrapper completes with
`w1/w2` both true, the existing four-selector mapping forwards input slots 6
through 10 in `w8..w12`; that gate does not prove the result came from an
operate call because the getter maps nil/0 to true as well.

AskBase result ownership, close/destruction, inventory eligibility, applied
inventory effects, item consumption, server acceptance, and reward settlement
are outside this script contract. The sidecar's six API names and ten callsites
are a dependency index only:
`lua/scripts/widget/ask/eventitemselectwidget.calls.json:7-32`.
