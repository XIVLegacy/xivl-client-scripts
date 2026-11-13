# Craft start material selection and results

The selected player path in `CraftJudge.start` opens and looks up the literal
`CraftStartWidget`. Its mode-1 result distinguishes a supplied material
(slot result 0), a selected item index (positive result), and an empty slot
(-1). Cancellation is operation 0 after successful selection; failed opening
or selection instead makes the judge's operation result nil.

The name `selectCraftItemSelectWidget` does not establish the distinct
[ItemSelectWidget module](item-select-widget-contract.md) as the runtime type. The opening and
lookup names do not prove that the returned object is a particular instance
or dispatches the methods recovered from `widget/craftstartwidget.lua`.
The contracts below are conditional on those dynamic bindings and normal
completion of the requested calls.

## Sources and established inputs

The [supplies contract](local-guildleve-supplies-contract.md#requested-items-and-recipe-presentation)
owns the initial mode/argument mapping, mode-1 `setInitialItems` behavior,
`setReadyMaterialInSlot`, and original LPB/decoded payload identities for
CraftJudge, CraftStartWidget and the desktop connector. The
[journal contract](guildleve-journal-lifecycle.md#return-node-retry-and-local-synthesis-prompts)
owns the mode-dependent Requested Items button labels. The
[CraftEdit contract](craft-edit-widget-contract.md#complete-72-method-matrix)
owns the child's local selection, virtual ready-item display and parent
requests. Those existing contracts do not establish native supply storage.

The retained archive matched the size and SHA-256 in
`manifests/private_lua_corpus.json`; each selected canonical LF source matched
`manifests/scripts.json`. Installed original LPBs and their in-memory decoded
payloads matched `manifests/retail_lua_coverage.json` before parsing.

| Source relative to `lua/scripts/` | Source manifest locator | Retail resource locator |
| --- | --- | --- |
| `judge/craft/craftjudge.lua` | `manifests/scripts.json:9903-9908` | `manifests/retail_lua_coverage.json:210-218` |
| `widget/craftstartwidget.lua` | `manifests/scripts.json:15363-15368` | `manifests/retail_lua_coverage.json:25634-25642` |
| `widget/desktopwidget_connector.lua` | `manifests/scripts.json:15399-15404` | `manifests/retail_lua_coverage.json:25454-25462` |

The following source windows and original-bytecode locators support the new
completion/result edges. Prototype paths, code offsets and PCs are zero-based
in the decoded Lua 5.1 payload. A1 etc. exclude self.

| Method | Canonical LF source lines | Prototype; code offset; selected PCs |
| --- | --- | --- |
| `CraftJudge.start` | 277-439 | `root/proto17`; 4367; 0-27, 60-151 |
| Desktop `selectCraftItemSelectWidget` | 11039-11110 | `root/proto208`; 106963; 7-57 |
| CraftStart `setButtonEvents` | 442-468 | `root/proto3`; 4975; 4-16 |
| CraftStart `openItemListWindow` | 493-541 | `root/proto5`; 5429; 2-35 |
| CraftStart `getSlotData` / `setSlotData` | 706-743 / 745-776 | `root/proto12` / `root/proto13`; 7170 / 7462; 0-31 / 0-25 |
| CraftStart `processUICommandCancel` | 1038-1079 | `root/proto17`; 9517; 0-33 |
| CraftStart `processUICommandDefault` | 1081-1303 | `root/proto18`; 9879; 0-34, 102-143 |
| CraftStart `setSlotItem` | 1548-1600 | `root/proto21`; 13492; 0-44 |
| CraftStart `processWaitCallFunction` | 1602-1616 | `root/proto22`; 13890; 0-8 |
| CraftStart `getCraftOperation` / `getCraftItems` | 1618-1631 / 1633-1651 | `root/proto23` / `root/proto24`; 14010 / 14144; 0-7 / 0-13 |
| `CraftJudge.closeCraftStartWidget` | 260-275 | `root/proto16`; 4208; 0-8 |

## Console icon tray entry

The standard `client/sqwt/widget/ConsoleIconTrayWidget.form` line 35
declares the visible `Button_CraftGathering` with
`UILuaCommands.Operate` and no explicit command parameter or target.
Its `ControlTemplate_Button_CraftGatheringIcon` at
`ConsoleIconTrayWidget.tpl` lines 194-201 binds the 32 by 32
`IconControl_Icon.IconDatas` to the Button's
`SqwtDesignData.StringValue0`. The standard-definition
`ConsoleIconTrayWidget.sd.form` has no `Button_CraftGathering`.
The [IconControl binding contract](https://github.com/XIVLegacy/xivl-decomp/blob/26b9fbe4b9e3571e06b634745786669f30980f2f/docs/resource/sqwt-icon-control-textures.md#direct-consoleicontray-design-data-binding)
owns the direct visual property transfer.

`ConsoleIconTrayWidget.init` calls `setConfirmCondition` with
`Button_CraftGathering`. When `updateCraftButton` receives a result
other than exact false from `desktopWidget:isExistCraftCommand()`, it
requests the craft icon, sets control user-work integer 1 to 22001, requests
help, and requests visibility true. Exact false enters the separate
gather-command lookup and can hide the same Button. For main skill 29,
`getCraftIconID` requests icon ID 875. The requests depend on the
current method bindings and subsequent property application.

When the installed `processUICommandOperate` reaches
`Button_CraftGathering`, it reads control user-work integer 1 for that
sender. Exact numeric 22001 calls `desktopWidget:executeCraftCommand()`
with no explicit argument. Another value reaches
`executePlayerSystemCommand` with that value. The synthesis branch
discards the result of `executeCraftCommand`.

The connector's `isExistCraftCommand` and `executeCraftCommand`
tailcall `craftCommand` with false and true respectively. Both require
the local player's `getMainSkillCategory()` to return numeric 29 and
`getReadyCommand(3)` to give a non-nil result. The latter looks up
`work.commandIndex[3]` and keeps the ready command only when the
equipped-command helper's third result is exactly true. The true
`craftCommand` route first returns false when
`cannotExecuteWithErrorMessage()` returns exactly true. With a non-nil
ready command it requests `executePlayerCommand` with the command,
four explicit nils and the open result of `worldMaster:_getMyPlayer()`.
This specifies the local request up to the player-command helper. Actual
input delivery, the wire request from a given press, and server acceptance
require separate evidence.

| Original locator | Observation |
| --- | --- |
| Tray `root/proto0` PCs 75-77, `0x0673-0x067B` | Named confirm registration |
| Tray `root/proto1` PCs 60-75, `0x0DE0-0x0E1C` | Current user-work integer read and two command requests |
| Tray `root/proto9` PCs 0-37, `0x1DBE-0x1E52` | Craft/gather switch and presentation requests |
| Tray `root/proto10` PCs 1-9, `0x1F99-0x1FB9` | Current main skill 29 selects icon 875 |
| Connector `root/proto64/65` PC 2, `0xDFE2/0xE030` | Read-only and execution tailcalls |
| Connector `root/proto66` PCs 0-33, `0xE076-0xE0FA` | Main skill category, execution gate, ready slot and argument order |
| Connector `root/proto68` PCs 0-11, `0xE359-0xE385` | Ready-index lookup and exact-true third result |

Authenticate the [tray LPB](../manifests/retail_lua_coverage.json#L25832-L25846)
and the connector listed under [sources](#sources-and-established-inputs).
Read the original Lua 5.1 chunks with `tools/retail_script.py`
(`decode_lpb`) and `tools/build_quest_contracts.py` (`ChunkReader`,
`instruction`). Decode the pinned markup by basename with `xivl extract-resource --as sqwt`.

| Markup under `client/sqwt/widget` | Carrier bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `ConsoleIconTrayWidget.form` | 11166, `180b7d709e588ec86fccead327aec813d4baab5b41ead05d2610cf318e787a0d` | 11158, `efbf73d1ac6307ca4983e9eeaf3170ab507d48e012d4c797ae360119d49d5f3e` |
| `ConsoleIconTrayWidget.tpl` | 20238, `f3c362bb64d9e9b07dd60b2ba95e1b868640e43c82558b83c24d1fd32d3378f1` | 20230, `9f1f5a2c79c2d8b35ea0d0b510c5536bcb43464da236ce1f9dea665f01937386` |
| `ConsoleIconTrayWidget.sd.form` | 2717, `775d4b4f107d7b5a2f7dc087eeb407bae8e57d79c21c5291dcf8d9903149289d` | 2709, `9508129e70a6e081b88246e9c3f6fed981217a34f6ca8e5504f479104a12faff` |

## Opening and material slots

For a player test returning exactly true, with A3 outside the special -1/-2
branches, `start` cancels the main target and calls
`openEventModeWidgetYield("CraftStartWidget")`. Only an exactly-true first
result reaches the normal selector call. A4 exactly true selects mode 1;
false, nil and numeric 0 select mode 0. The collected varargs omit nil values
and preserve false and numeric 0, compacting later values into consecutive
positions.

The connector keeps one result W from
`getWidget(4,"CraftStartWidget")`. Nil W returns exactly
`false,0,nil,emptyTable`. For the mode-1 call it requests
`W:setInitialData(1,0,A3)` and `W:setInitialItems(...)`, forwarding every result
of global `unpack(suppliedTable)` after the W receiver. The latter call has
open argument width (`CALL B=0`) and discards results. This branch does not
call `continue`. W is retained locally, but each method lookup is dynamic.
The separately opened widget and W are not proved identical.

For a valid slot number greater than 0 and at most 8, `getSlotData` obtains
the slot control name, then separately requests `IntData.Value0`,
`IntData.Value1` and `IntData.Value2`, keeping one result from each. It returns
those three values in that order. Nil or out-of-range numeric slot arguments
return `0,0,0` without property reads. The local guard does not enforce an
integer type. `setSlotData(slot,package,index)` requests writes only to
Value0 and Value1, calls `updateSlotIcon(slot)`, and returns true after normal
completion; it leaves ready Value2 alone. A true return does not prove native
acceptance or later readback.

An exact `UILuaCommands.ChooseSlot` callback stores A4 as `chosenSlot` and
calls `openItemListWindow`. With a nonnil looked-up `CraftEditWidget`, that
method reads the chosen slot. Package exactly 0 opens the child's item list,
requests modal true and child focus; other package results request
`removeItem` and refresh the selected slot icon/help. The
child's [setItem and parent requests](craft-edit-widget-contract.md#complete-72-method-matrix)
remain conditional on its independently obtained parent. No matching parent
identity follows merely from the child name.

The parent's `setSlotItem(package,index,count)` handles the selected
replacement request. With a nonnil child and admitted count in 0..8, it scans
from the current chosen slot, wrapping candidate slot numbers past 8. A slot
whose first `getSlotData` result is exactly 0 receives
`setSlotData(slot,package,index)` and child `setSlotItem(slot+8)` requests.
Ready Value2 is not the vacancy test and is not overwritten by this setter.
The local loop decrements count after each assignment and stops on exact 0;
an initial count of 0 therefore is not an immediate no-op. The parent's
`setSlotItem` returns zero values. Successful native storage and child
ownership remain unbound.

## Choice, completion and cancellation

The two command handlers first reject `editWidgetMode ~= 0`, then
`chosenOperation ~= -1`, then `recipemode == true`, returning one false on
each guard. These are separate current property reads. `setButtonEvents`
registers the control's dynamically read Command value, ButtonFocused and
cancel conditions; button names alone do not establish delivered commands.

| Delivered command/control after the guards | Local request and result |
| --- | --- |
| `UILuaCommands.CraftOperate`, `Button_CraftStartByMain` | Writes operation 1, edit mode 1, last button 1 and history mode false; disables input and returns true. |
| Same command, `Button_CraftStartBySub` | Writes operation 2, edit mode 2, last button 2 and history mode false; disables input and returns true. |
| Same command, `Button_CraftCancel` | Writes operation 0, disables input and returns true. |
| `UILuaCommands.Quest` | Writes operation 3, disables input and returns true. This is a local selection result, not a craft outcome. |
| Cancel callback for `Button_CraftCancel` | Writes operation 0 and disables input; returns zero values. |
| Cancel callback for another control | Requests focus on `Button_CraftCancel` and help 3029/3030; leaves the operation unchanged and returns zero values. |

`processWaitCallFunction` returns false only while its current operation read
equals -1. Other values, including numeric 0, nil and false, return true.
The already established
[selection wait helper](fishing-input-flow-contract.md#wait-result-width-and-cleanup)
polls the dynamically selected completion callback with no timeout and
distinguishes an exactly-false alive result from other values. Local
completion does not mean crafting succeeded.

The connector calls `selectWidgetYield(W,true)` and keeps one result S.
Only S exactly true invokes `getCraftOperation`, requesting exactly two
results O and R: missing results are nil-padded and extras discarded.
The recovered getter first captures a current chosenOperation, requests a
chosenOperation=-1 write through another work read, then returns the captured
operation and a subsequent chosenRecipe read. It does not freeze the work
receiver or recipe value before that write.

If O is numeric 0, the connector leaves the slot table empty. Otherwise it
requests `getCraftItems(i)` once for each i=1..8, retaining one result per
call. False and nil O also enter this arm; they are not numeric 0.

| Current `getSlotData(i)` results `(package,index,ready)` | One `getCraftItems(i)` result |
| --- | --- |
| package is not numeric 0 | index unchanged, including a nil or false index |
| package is numeric 0 and ready is not numeric 0 | numeric 0 |
| package and ready are numeric 0 | -1 |

The ready comparison is exact inequality: nil or false ready also selects
the numeric-0 result. These comparisons do not prove typed package/index
values. The connector always returns four values `S,O,R,slotTable`; O starts
at 0 and R at nil. S=false, nil or numeric 0 skips both result getters and
preserves that S with the initial O/R and an empty table.

## Judge result adjustment and cleanup

`start` requests exactly four selector results. If S is not exactly true,
it replaces O with nil and does not convert the slot table. R remains the
adjusted third result. Thus selection failure and successful operation-0
cancellation remain distinct.

For S exactly true, the judge traverses 1 through the Lua length of the
returned slot table. Numeric slot result 0 selects the corresponding compacted
supplied value; a positive result requests
`A1:_getExtendedTemporaryItem(1,slotResult)`, keeping one result. Other numeric
results leave the material at its initial 0, and a resulting nil is replaced
with 0. A false slot result is not 0 and can reach the ordinary numeric
comparison failure. Missing table entries and holes do not establish a dense
eight-slot sequence or a fixed Lua length.

The judge then makes two passes over its material values. Each pass freshly
calls global `_isInstanceOf(value,"ItemBaseClass")`, keeping one result:
the first appends truthy classifications, the second appends false/nil
classifications. With stable classifications this preserves relative order
inside each group and puts ItemBaseClass classifications first. Numeric 0
is truthy here. Rebinding or changed classification results can duplicate or
omit entries; no runtime class identity follows from this local call.

Finally `start` returns O and R followed by every result of global
`unpack(orderedTable)` (`CALL C=0`, `RETURN B=0`), rather than imposing a fixed
final result width. Under ordinary unpack and stable classification of the
dense local values, this is the two-value prefix plus eight material values.

Neither this `start` path nor its connector calls a close helper. The result
getter's operation reset is not destruction. The separate
`closeCraftStartWidget` calls `closeEventModeWidget("CraftStartWidget")` only
when A1's player test is exactly true, discards results and returns zero
values. Its invocation is not established by `start`; the
[generic close contract](fishing-input-flow-contract.md#wait-result-width-and-cleanup)
owns subsequent close requests. No selected script call proves item debit,
recipe acceptance, supply replenishment, XP, item grant, historical server
selection, or actual widget lifetime.
