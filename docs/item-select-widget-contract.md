# ItemSelectWidget local interaction contract

This contract records local operations, branch guards, helper-call
operands, and result arities recovered from one named retail Lua
resource. It does not promote a caller, native implementation, server
interpretation, or runtime observation.

## Identity, pins, and metadata citations

- Resource: `client/script/n1635q/1q5xr5y57qn1635q.le.lpb`.
- LPB: 27362 bytes; SHA-256
  `0BD9A8D520D79B5D334810ACB5D22F0E496A4C2D195E66546166ECE568B3C972`.
- Decoded Lua 5.1 chunk: 27349 bytes; SHA-256
  `28804E6060ABFB44AEC1145AD587CEE203800A34411A247382B7CE569BC47DA5`.
- Canonical LF decompile: 77174 bytes, 3535 lines; SHA-256
  `C12BB32319F7526D9D2A2EC3B3F916D46B153F6B346348E0E02B2302269B28B8`.
- Pinned decoder route: `xivl-client-scripts/tools/retail_script.py`
  invoked once with
  `xivl-client-scripts/tools/vendor/unluac/unluac_2025_12_23.jar`
  (796256 bytes; SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`).
- Metadata citations: `xivl-client-scripts:manifests/scripts.json:15524-15529`;
  `xivl-client-scripts:manifests/retail_lua_coverage.json:25142-25156`;
  `xivl-client-scripts:lua/registry.json:41932-41991`;
  `xivl-client-structs:manifests/lua_api_contract.json:173594-174213`.
  These identify the resource and `/Widget/WidgetBaseClass`; they do not
  establish behavior by themselves.

## Root operations

The root performs `require("/Widget/WidgetBaseClass")` at decoded
chunk PC 2, offset 40, `CALL A=0 B=2 C=1`, discarding all results.
It performs `_defineClass("ItemSelectWidget", "WidgetBaseClass")`
at PC 6, offset 56, `CALL A=0 B=3 C=1`, also discarding all results.
It then makes 48 fresh `ItemSelectWidget[key] = closure` SETTABLE
attempts, one per method below. These are recovered root operations,
not proof of class installation or initialization dispatch.

## Complete 48-method behavior and result rows

| child | method | source | params | proto/codeoff | local behavior, guards, and result |
|---:|---|---:|---:|---:|---|
| 0 | `getFormName` | 11-17 | 1 | 1776/1796 | Returns the literal `"SubItemListWidget"`. |
| 1 | `init` | 20-392 | 6 | 1851/1871 | Creates local `work._temp` descriptors for 42 named fields. Writes `chosenItem=0`, `chosenOperation=0`, `isRewardMode=false`, `bonus1/2/3=false`, `itemlife=false`, `bazaar=false`, `closeok=false`, `demandSync=false`, `sorttype` from `desktopWidget.getConfigWork(9)`, `focus=0`, and `submenu=false`. It does not write `isRetainer`, `indexChange`, or `focusChange`. Calls `setDrag(true)`, `initForm()`, `initListBox(1..5)`, requests visibility false for `TabItem_3/4/5`, reads player capacities for packages 1 and 100, reads retainer capacities for packages 1 and 100 only when `A5 == 4`, then calls `setInitialData(A1..A5)`. Typed `_temp` descriptors are local literals; native first values and subsequent work readback remain conditional. No explicit result (zero results). |
| 2 | `setInitialData` | 395-620 | 6 | 4093/4113 | Calls `setModal(A1)`, stores `mode=A2`. For exact `A2 == 400`, sets reward mode, conditionally stores reward package/item, and for exact `A5 == 4` marks retainer and copies a non-nil `desktopWidget.getRetainerName()` to `TextBlock_ActorName` with 230; otherwise clears retainer. For exact `A2 == 440`, reads `getBazaarItem(A3,A4)`; if non-nil reads catalog, stack, quality, and proper package. Resets list boxes 1..5, writes SourceFirstIndex/SourceCount and FilteredSortKey for boxes 1 and 2 using retainer or player capacities, calls `makeListFromPackage()` and `operateSort(sorttype)`, selects box 2 only when mode 440 and proper package is exactly 100, otherwise box 1, then calls `changeList()`, `updateWindowDisplay(true)`, and requests title 3207 or 3208. No explicit result. |
| 3 | `processBeforeShow` | 623-635 | 2 | 5756/5776 | If `A1 == true`, calls `updateWindowDisplay(true)`; returns exact `true` on every path. |
| 4 | `getListPropertyName` | 638-664 | 2 | 5855/5875 | Exact lookup: 1..5 map to `TabItem_1_Maker`..`TabItem_5_Maker`, 8 to `SlotItem_Maker`, 9 to `HelpCache_Maker`; any other input falls through with zero results (nil in a value context, not an explicit one-nil return). |
| 5 | `initForm` | 667-745 | 1 | 6244/6264 | SELF setup/call sequence at PCs 0-3 invokes `self.setCancelCondition()` and `self.setCloseCondition()` with no control argument; the sequence at PCs 4-6 invokes `self.setConfirmCondition("Button_SortStatus")`, and PCs 41-43 invoke `self.setConfirmCondition("TOG_itemDetail")`. It separately sets cancel conditions on `TabItem_1`, `TabItem_2`, and `Button_Back`, confirms `Button_Back`, and registers only `UILuaCommands.TabChanged` for `TabControl_ItemList` and `UILuaCommands.ButtonFocused` for `Button_Back`. It requests content 3115, text 214/10091 and 214/10093, and `Focusable`/`IsTabStop` false for `Button_Back`, then calls `desktopWidget.setMateriaAttachSlotIconHelp(self)`. It has no `UILuaCommands.Cancel` registration; cancellation uses the self-method condition calls. No explicit result. |
| 6 | `updateWindowDisplay` | 748-794 | 2 | 7040/7060 | For mode 400 requests grid visibility 3 and requests sort status only for listbox 1 (also calls display sort type); for mode 440 requests grid visibility 8. If `A1 == true`, calls `updateListFocus()`. No explicit result. |
| 7 | `updateListFocus` | 797-898 | 1 | 7429/7449 | Reads the four-result `getListBoxFocusNum(listbox)`. On count 0, requests visibility for `TextBlock_NoContents_<listbox>` and the list, calls focus/help helpers, and requests `Button_Back` focus/tab stop. Otherwise requests list/empty-control visibility, clamps `work.focus` to count-1, calls `focusToIndex`, and stores `work.index` only when that result is >= 0; then requests `SqwtFocusedIndex`, calls `setFocusedIndex`, calls the list focus helper, and displays focused-item help. No explicit result. |
| 8 | `setGridVisibility` | 901-1004 | 2 | 8148/8168 | Requests actor-name visibility from `work.isRetainer`; Help only for exact A1 1; tab list for A1 1, 3, or 8; sort status only for listbox 1; requests backpack/gil and button grids true; item-name base for A1 3 or 8; detail grids from bonus flags and `itemlife`/`bazaar`; label/item-life grids from their flags; detail toggle and edit grid false. No explicit result. |
| 9 | `setWindowFocus` | 1007-1027 | 2 | 9049/9069 | For non-nil and non-empty `A1`, calls `setLogicalFocus(A1)`, reads `desktopWidget._getKeyboardFocusedWidget()`, and compares that result to self with Lua `==` (the EQ operation, so `__eq` behavior remains conditional). Only a true comparison calls `setKeyboardFocusedControl(A1)`; this does not prove raw identity or focus ownership. No explicit result. |
| 10 | `displayBagcapacityAndMoney` | 1030-1066 | 1 | 9262/9282 | Chooses player or retainer money count and bag capacity from `work.isRetainer`; calls text-property requests for gil (3263) and item-stack (3551) with listbox-1 item count and capacity. No explicit result. |
| 11 | `isExistItem` | 1069-1119 | 4 | 9653/9673 | For `A3` nil or exact 1, reads player item `(A1,A2)`; exact 2 reads bazaar item; exact 4 reads retainer item. Returns explicit true iff the selected helper result is non-nil, false iff nil; unsupported A3 falls through with zero results. |
| 12 | `checkPackageAndIndex` | 1122-1172 | 5 | 10025/10045 | For `A4` nil or exact 1, reads player `(A2,A3)` and returns explicit equality with `A1`; exact 2 and 4 do the same with bazaar/retainer helpers. Lua equality is the tested operation. Unsupported A4 falls through with zero results. |
| 13 | `getSelectedTab` | 1175-1185 | 1 | 10397/10417 | Returns `getSelectedIndex("TabControl_ItemList") + 1`; a nil/non-numeric helper result reaches the Lua `ADD` boundary unless an applicable arithmetic metamethod supplies it. |
| 14 | `getListBoxName` | 1188-1211 | 2 | 10517/10537 | Exact map 1..5 to `ListBox_TabItem_1`..`ListBox_TabItem_5`; any other input returns explicit empty string. |
| 15 | `getListBoxItemNum` | 1214-1225 | 2 | 10835/10855 | Calls `getListPropertyName(A1)` with `CALL B=3,C=0` (open result prefix), then tail-forwards `getListPropertyCount(self, dynamic results...)` with `TAILCALL B=0,C=0`; both argument and result widths are dynamic, not a fixed property-name/result tuple. |
| 16 | `getListBoxFocusNum` | 1228-1265 | 2 | 10954/10974 | Calls `getListBoxItemNum(A1)` and `getListPropertyName(A1)` before the exact-zero guard. If item count is exactly 0, returns four explicit zeros after both calls. Otherwise reads `_getProperty(nil, propertyName, "FilteredCount")`, then performs two fresh reads of `work.focus` (F1 for the return slot and F2 for the comparison). If `FilteredCount < F2`, only the local return slot is replaced with `FilteredCount - 1`; `work.focus` is not written. It returns four values: filtered count, filtered count minus one, zero, and F1 or the local replacement. |
| 17 | `focusToIndex` | 1268-1296 | 3 | 11242/11262 | Calls `getListPropertyName(A1)` before calling `getListBoxFocusNum(A1)`. If focus count is exactly 0 or `A2 >= count`, returns explicit -1; otherwise requests list `FilteredIndex=A2` and returns `getControlProperty(list,"Index")`. With positive focus count, nil `A2` reaches the ordinary `A2 >= count` numeric boundary rather than an implicit zero or -1. |
| 18 | `indexToFocus` | 1299-1338 | 3 | 11523/11543 | Starts at -1, then calls `getListPropertyName(A1)`, `getListBoxItemNum(A1)`, and `getListBoxFocusNum(A1)` before the positive-focus guard; item count is read but unused by the later guard. If focus count is positive, requests list `Index=A2`, reads `FilteredIndex`, and stores it; always requests list `Index=work.index`, then returns the stored index (or -1). |
| 19 | `initListBox` | 1341-1412 | 2 | 11872/11892 | If `getListBoxName(A1)` is non-empty, requests `IntData.Value0`, registers `UILuaCommands.MouseEnteredItem`, `UILuaCommands.AnchoredItem`, and `UILuaCommands.Selection`, requests `setCancelCondition(listbox)`, visibility, empty text 3140, tab stop, and `UILuaCommands.Previous`/`UILuaCommands.Next`. Unknown listbox names are a no-op. No explicit result. |
| 20 | `resetListBox` | 1415-1447 | 2 | 12508/12528 | Gets item count and property name. Exact zero is a no-op; otherwise requests deletion of indices from count-1 down to 0 and calls `updateListProperty`. No explicit result. |
| 21 | `getPackageFromList` | 1450-1467 | 2 | 12762/12782 | Exact listbox map: 1 -> 1, 2 -> 100, 3 -> 8, 4 -> 5, 5 -> 100; all other inputs retain default 1. |
| 22 | `setItemToXmlLight` | 1470-1708 | 6 | 12953/12973 | Calls `getListPropertyName(A1)` and `worldMaster._getMyPlayer()` before the numeric `A3 > 0 and A4 > 0` guard. Exact `A5 == 4` uses retainer lookup; every other source type uses player lookup. Nil `A3` reaches that ordinary numeric comparison after the preguard calls; a nil item is tested only after the numeric guard and returns explicit false. Reads catalog/icon/stackable/count/name. In reward mode, exact package/item match changes table name to `TBL_selectedItem`; catalog 1000001 stores money index/count. Sort defaults to `work.sorttype` and sort field 13 for listbox 1 and unrecognized listboxes; listbox 2 -> 11/14, 3/4 -> 0/13, 5 -> 12/15. In mode 440, the hidden count guard is `count < orderStack`: count 8 with orderStack 7 continues when catalog and quality match, while that count failure or either mismatch sets local visibility flag `R19=false`; visibility is still requested (PCs 115-120), XML is skipped, and normal return is explicit true. On a visible row it calls `desktopWidget.setItemToXml` with 19 total arguments including the desktop receiver, or 18 operands after that receiver: `(widgetSelf, propertyName, index, item, tableName, catalog, icon, stackable, count, nameIndex, sorttype, true, false, sortField, A3, A4, A5, false)`. Its exclusive/equipping/equipment checks use Lua TEST truthiness, so numeric 0 is true; damaged equipment additionally requires life max > 0 and life != max. Only mode 400 performs opacity checks (PCs 143-155), including selected-reward dimming; requests use exact strings `"0.5"` and `"1.0"`. A positive updatecount and matching listbox can set `focusChange` when filtered index < focus. Returns explicit true after success. |
| 23 | `getMoneyListIndex` | 1711-1843 | 2 | 14680/14700 | Exact ordered lookup returns explicit indices: 1000001 -> 1, 1000102 -> 2, 1000101 -> 3, 1000103 -> 4, 1000107 -> 5, 1000106 -> 6, 1000111 -> 11, 1000110 -> 12, and 1000113..1000123 -> 14..24. IDs 1000104, 1000108, 1000109, 1000105, 1000112, and unknown IDs return explicit -1. |
| 24 | `setSortType` | 1846-1886 | 5 | 15470/15490 | Reads retainer `(A4,A2+1)` or player `(A4,A2+1)` item. Nil item returns explicit false. Otherwise calls desktop `setSortType(self,A1,A2,work.sorttype,item)` and falls through with zero results (not one nil). |
| 25 | `updateSortType` | 1889-1921 | 1 | 15800/15820 | Always resolves list-1 property/package/count and loops each row calling `setSortType(property,index-1,sorttype,package)`, regardless of current `work.listbox`; then calls `updateListProperty`. No explicit result. |
| 26 | `makeListFromPackage` | 1924-2355 | 3 | 16082/16102 | Full-build list 1 is entered only when `A2 == nil` and (`A1 == nil` or exact `A1 == 1`); full-build list 2 is entered only when `A2 == nil` and (`A1 == nil` or exact `A1 == 100`). A supplied A2 takes the single-item path only for exact A1 1 or 100; unsupported A1=9 with non-nil A2 returns at PC267 before final display, while A1=9 with nil A2 skips both builds and reaches final display at PCs389-390. The initial `setItemToXmlLight` source-type argument is 4 only when `work.isRetainer == true`, otherwise 1, including nil or numeric 0. In the later single-item lookup gate, player `_getItem` is selected only by exact `work.isRetainer == false`; nil, numeric 0, and true instead select `getRetainerItem`. Full builds refresh zero capacity from helper reads, call `setItemToXmlLight` over capacity, request deletion of stale tail rows, and call the list update. A missing single item requests deletion at `count-1`, not `A2-1`. For player package 100, the missing-item branch compares A2 with `retainerMoneyIndex` before clearing `playerMoneyIndex/playerMoneyCount`; successful rows synchronize the selected money fields. Finally calls capacity/money display. |
| 27 | `displayHelp` | 2358-2367 | 2 | 18356/18376 | Sets `TextBlock_Help` to A1. No explicit result. |
| 28 | `displayFocusedItemHelp` | 2370-2572 | 1 | 18449/18469 | If focus count is zero, calls `displayHelp(3140)`, clears bonus/life flags and page, requests grid visibility 1, and returns explicit false. If item count <= focus, returns false. Its initial `work.isRetainer == true` read selects retainer type 4; nil, numeric 0, and false select player type 1, and the bazaar arm is unreachable. After `setItemDetail`, it performs an independent fresh `work.isRetainer == false` read at PC97; only exact false enters equipment and up to 27 fit-point checks. It calls `setItemDetailEquip` with the selected item/equipment candidate and assigns four results to bonus1/2/3/itemlife, calls `updateWindowDisplay(false)`, and returns true only on normal completion. With exact false and a nil player item, the first detail request occurs and the nil `isEquipment` receiver fails; for initial nil/0, an unchanged fresh nil/0 read skips that equipment call and can reach normal detail-equip completion, but if `setItemDetail` changes the fresh flag to exact false, the PC97 arm reaches the nil-receiver failure at PC103 before detail-equip. |
| 29 | `previousSequence` | 2575-2625 | 1 | 19833/19853 | Persists sort type only when it differs from `desktopWidget.getConfigWork(9)`. Exact mode 400 calls `closeWidget()` and returns true. Exact mode 440 gets parent; nil parent returns false, non-nil calls `setOrderItemData(1,0,0)` and tail-forwards `closeOrderItem` results. Other modes fall through with zero results. |
| 30 | `processUICommandOperate` | 2628-2668 | 5 | 20267/20287 | Retainer with `updatecountbaz > 0`, or player with `updatecount > 0`, returns explicit false. Exact `A2 == "Button_SortStatus"` calls `operateSort()` and, for a non-nil parent, `setParentSortType(sorttype)`. Exact `A2 == "Button_Back"` calls `previousSequence()`. Other commands have no result. |
| 31 | `processUICommandCancel` | 2671-2682 | 5 | 20660/20680 | Calls `setCommonTimer(nil)`, then `previousSequence()`. No explicit result. |
| 32 | `processUICommandClose` | 2685-2696 | 5 | 20766/20786 | Same timer-clear and `previousSequence()` continuation as cancel. No explicit result. |
| 33 | `processUICommandSelection` | 2699-2857 | 5 | 20872/20892 | Updatecount guards return false. Stores focus/listbox from A3/A4. Empty list updates display and returns; focus >= focus count updates focus and returns; otherwise updates display, rechecks non-empty focus, derives chosen package and one-based chosen item, and gates on `isOperateButtonEnable`. When that returns exact true, it first calls `saveSortType()` and `_getParentWidget()` before testing mode. Mode 400 then returns for an already-selected reward; otherwise calls `selectedBorder(index,true)`, parent `setReward(package,item)`, and `closeWidgetDirect(self)`. Mode 440 requires `chosenOperation == 0`, then borders, calls `setOrderItemData(2,package,item,orderStack)`, stores operation 2, and closes order item. A nil parent failure is reachable with a nonmatching reward in mode 400 or operation 0 in mode 440; other modes still perform the preguard calls. No explicit result. |
| 34 | `processUICommandDefault` | 2860-2930 | 6 | 22029/22049 | Updatecount guards return false. For exact `A3 == "UILuaCommands.MouseEnteredItem"` or `"UILuaCommands.AnchoredItem"`, nil A5 returns, nil or negative A4 returns, otherwise stores `work.listbox=A5`, `work.focus=A4`, and calls `setCommonTimer(0.2)`; A5=false is non-nil, but A4=false reaches the ordinary `A4 < 0` comparison and fails before storage/timer. Exact TabChanged calls `getSelectedTab`, then computes literal `0 + result` (child-34 PC42 B=K0,C=R7) and calls `changeList`; a nil/non-numeric selected-tab result reaches the arithmetic boundary. ButtonFocused enables both back properties; Previous/Next call `catalogSkip(-1/1)`. A5 is a formal sixth argument here. No explicit result. |
| 35 | `processTimer` | 2933-2969 | 1 | 22810/22830 | Calls `focusToIndex(listbox,focus)`, stores the result only when it is >= 0, sets page 0, calls `updateWindowDisplay(true)`, then calls `selectedBorder()` with no arguments, and enables `Button_Back` focus/tab stop. No explicit result. |
| 36 | `catalogSkip` | 2972-3075 | 2 | 23160/23180 | Reads focus count minus one; exact -1 returns. Uses 10-step movement for non-listbox-1 or sorttype 0. For sorted listbox 1, compares `desktopWidget.getItemSortKey` across candidate focus positions, moving by the first differing key or to the end/start on exhaustion. Clamps to [0,last], and when changed writes focus and updates display true. No explicit result. |
| 37 | `selectedBorder` | 3078-3134 | 3 | 23819/23839 | Resolves current list property. If A1 is non-nil, requests selected row at `work.index` as `Visible`, except exact A2 == false requests `Collapsed`, then stores `work.selected=work.index`. If A1 is nil and selected is -1, returns; otherwise requests collapse for every row and sets selected=-1. Thus nil or numeric 0 A2 requests `Visible` in the non-nil branch. Calls `updateListProperty` after the operation. No explicit result. |
| 38 | `changeList` | 3137-3163 | 1 | 24241/24261 | Calls `setText` with fixed prefix `(self,"TextBlock_Title")` followed by all results of `getControlProperty("TabItem_" .. tostring(work.listbox),"Header")`, including zero or multiple results; the source uses an open argument CALL for this prefix. It resets index/focus to 0 and tail-forwards all results from `updateWindowDisplay(true)`. |
| 39 | `operateSort` | 3166-3192 | 2 | 24542/24562 | Only listbox 1 is active. Calls `changeSortType()` when A1 is nil, otherwise stores A1; calls `updateSortType()` and `displaySortType(sorttype)`, then returns explicit true. |
| 40 | `isOperateButtonEnable` | 3195-3294 | 4 | 24770/24790 | Resolves list property and focus count; zero focus or A2 >= item count returns false. It computes local `getPackageFromList(A1)` and local item index `A2+1`, but the item lookup uses fresh `work.chosenPackage/work.chosenItem`; A3, when non-nil, overrides only after that lookup. Reward opacity compares exact string `"0.5"`; retainer/player lookup uses the chosen fields, and nil item returns false. `_isEquipping` and `isExclusiveItem` compare exact true; packages other than 1 or 100 return false. Otherwise returns the local boolean. |
| 41 | `closeWidget` | 3297-3320 | 2 | 25530/25550 | Only reward mode acts: gets parent, and if non-nil calls `setReward(nil,nil)` then `desktopWidget.closeWidgetDirect(self)`. No explicit result. |
| 42 | `updateItemList` | 3323-3394 | 3 | 25744/25764 | The entry guard returns only when `work.isRetainer == false`; true or nil continue to the retainer counter path. Exact A1 0 stores `updatecountbaz=A2` and returns. Exact A1 1/100 calls `makeListFromPackage` and records listbox 1/2; unrecognized A1 leaves the local listbox marker -1. A positive counter decrements, but an already-zero counter continues immediately. When the counter is zero, recognized A1 updates its property, matching list focus is refreshed, and capacity/money display is called; unrecognized A1 skips the property update but still displays capacity/money. No explicit result. |
| 43 | `updatePlayerItem` | 3397-3487 | 3 | 26281/26301 | Exact A1 0 stores `updatecount=A2` and returns. Only `work.isRetainer == false` permits recognized A1 1/100 list rebuilds; otherwise the local listbox marker remains -1. A positive counter decrements, but an already-zero counter continues. At zero, the exact false retainer guard is required; property update occurs only when the recognized-list marker is not -1 (mode 440 uses that marker, A1 100 uses list 2, otherwise the marker), while capacity/money display occurs unconditionally in that branch. `updateListFocus` refreshes only when the rebuilt marker equals `work.listbox` (PCs 73-80); an active A1=1 update with `work.listbox=2` can display capacity without focus refresh, and unknown A1 leaves marker -1. Explicit final `return` has zero results. |
| 44 | `syncItemWork` | 3490-3493 | 2 | 26902/26922 | Empty body; zero results. |
| 45 | `displaySortType` | 3496-3507 | 2 | 26946/26966 | Calls `desktopWidget.displaySortType(A1,self,"Button_SortStatus")`. No explicit result. |
| 46 | `changeSortType` | 3510-3522 | 1 | 27077/27097 | Stores `desktopWidget.changeSortType(work.sorttype)` back to `work.sorttype`. No explicit result. |
| 47 | `saveSortType` | 3525-3535 | 1 | 27212/27232 | Calls `desktopWidget.saveSortType(work.sorttype)`. No explicit result. |

## Distinct method call-prefix matrix

Each row groups distinct child `(opcode,A,B,C)` call prefixes. B is
argument count plus one and C is result count plus one under Lua 5.1;
zero is open width. Repeated identical prefixes carry an occurrence
count. Per-occurrence PCs and decoded offsets, controls, RK literals,
and RETURN vectors remain in the private operand proof.

| child | method | distinct call prefixes (opcode A/B/C, count) |
|---:|---|---|
| 0 | `getFormName` | none |
| 1 | `init` | `CALL A=6 B=2 C=1`; `CALL A=6 B=2 C=2`; `CALL A=6 B=3 C=1` x6; `CALL A=6 B=4 C=1` x3; `CALL A=7 B=3 C=2`; `CALL A=7 B=7 C=1`; `CALL A=8 B=3 C=2` x4 |
| 2 | `setInitialData` | `CALL A=6 B=3 C=1`; `CALL A=7 B=2 C=1`; `CALL A=7 B=2 C=2`; `CALL A=7 B=3 C=1` x6; `CALL A=7 B=4 C=2`; `CALL A=7 B=5 C=1` x8; `CALL A=8 B=2 C=1`; `CALL A=8 B=2 C=2`; `CALL A=8 B=3 C=1`; `CALL A=8 B=4 C=1` x4; `CALL A=8 B=5 C=1`; `CALL A=9 B=2 C=2` x3; `CALL A=9 B=3 C=2` x8 |
| 3 | `processBeforeShow` | `CALL A=2 B=3 C=1` |
| 4 | `getListPropertyName` | none |
| 5 | `initForm` | `CALL A=1 B=2 C=1` x2; `CALL A=1 B=3 C=1` x7; `CALL A=1 B=4 C=1` x3; `CALL A=1 B=5 C=1` x4 |
| 6 | `updateWindowDisplay` | `CALL A=2 B=2 C=1`; `CALL A=2 B=3 C=1` x3; `CALL A=2 B=4 C=1` x2 |
| 7 | `updateListFocus` | `CALL A=1 B=3 C=5`; `CALL A=5 B=3 C=2`; `CALL A=7 B=2 C=1`; `CALL A=7 B=2 C=2`; `CALL A=7 B=3 C=1`; `CALL A=7 B=4 C=1` x4; `CALL A=7 B=4 C=2`; `CALL A=7 B=5 C=1` x2; `CALL A=8 B=2 C=1`; `CALL A=8 B=3 C=1`; `CALL A=8 B=4 C=1`; `CALL A=8 B=5 C=1` |
| 8 | `setGridVisibility` | `CALL A=2 B=3 C=1`; `CALL A=2 B=4 C=1` x15 |
| 9 | `setWindowFocus` | `CALL A=2 B=2 C=2`; `CALL A=2 B=3 C=1` x2 |
| 10 | `displayBagcapacityAndMoney` | `CALL A=2 B=5 C=1`; `CALL A=3 B=6 C=1`; `CALL A=7 B=3 C=2` |
| 11 | `isExistItem` | `CALL A=4 B=2 C=2`; `CALL A=4 B=4 C=2` x2; `CALL A=5 B=4 C=2` |
| 12 | `checkPackageAndIndex` | `CALL A=5 B=2 C=2`; `CALL A=5 B=4 C=2` x2; `CALL A=6 B=4 C=2` |
| 13 | `getSelectedTab` | `CALL A=1 B=3 C=2` |
| 14 | `getListBoxName` | none |
| 15 | `getListBoxItemNum` | `CALL A=4 B=3 C=0`; `TAILCALL A=2 B=0 C=0` |
| 16 | `getListBoxFocusNum` | `CALL A=2 B=3 C=2`; `CALL A=3 B=3 C=2`; `CALL A=4 B=5 C=2` |
| 17 | `focusToIndex` | `CALL A=3 B=3 C=2`; `CALL A=4 B=3 C=2`; `CALL A=5 B=5 C=1`; `TAILCALL A=5 B=4 C=0` |
| 18 | `indexToFocus` | `CALL A=4 B=3 C=2`; `CALL A=5 B=3 C=2`; `CALL A=6 B=3 C=2`; `CALL A=6 B=4 C=2`; `CALL A=6 B=5 C=1` x2 |
| 19 | `initListBox` | `CALL A=2 B=3 C=2`; `CALL A=3 B=3 C=1`; `CALL A=3 B=4 C=1` x4; `CALL A=3 B=5 C=1`; `CALL A=4 B=2 C=2`; `CALL A=4 B=4 C=1` x4; `CALL A=4 B=5 C=1` |
| 20 | `resetListBox` | `CALL A=2 B=3 C=2`; `CALL A=3 B=3 C=2`; `CALL A=4 B=3 C=1`; `CALL A=8 B=4 C=1` |
| 21 | `getPackageFromList` | none |
| 22 | `setItemToXmlLight` | `CALL A=6 B=3 C=3`; `CALL A=12 B=2 C=2`; `CALL A=15 B=2 C=2` x5; `CALL A=15 B=4 C=2` x2; `CALL A=20 B=4 C=2`; `CALL A=20 B=5 C=1`; `CALL A=20 B=20 C=1`; `CALL A=21 B=2 C=2` x5; `CALL A=21 B=6 C=1` x2; `CALL A=22 B=2 C=2` |
| 23 | `getMoneyListIndex` | none |
| 24 | `setSortType` | `CALL A=6 B=2 C=2`; `CALL A=6 B=4 C=2` x2; `CALL A=6 B=7 C=1` |
| 25 | `updateSortType` | `CALL A=1 B=3 C=2`; `CALL A=2 B=3 C=2`; `CALL A=3 B=3 C=1`; `CALL A=4 B=3 C=2`; `CALL A=7 B=6 C=1` |
| 26 | `makeListFromPackage` | `CALL A=3 B=2 C=2`; `CALL A=10 B=2 C=1`; `CALL A=10 B=2 C=2` x2; `CALL A=10 B=3 C=1` x2; `CALL A=10 B=3 C=2` x4; `CALL A=10 B=5 C=1` x2; `CALL A=11 B=3 C=2` x3; `CALL A=11 B=5 C=1` x2; `CALL A=12 B=3 C=2` x6; `CALL A=12 B=4 C=2` x2; `CALL A=12 B=7 C=1` x2; `CALL A=13 B=3 C=1` x2; `CALL A=13 B=3 C=2` x2; `CALL A=13 B=4 C=1` x2; `CALL A=14 B=4 C=1` x2; `CALL A=14 B=7 C=2` x2 |
| 27 | `displayHelp` | `CALL A=2 B=4 C=1` |
| 28 | `displayFocusedItemHelp` | `CALL A=1 B=3 C=1` x2; `CALL A=1 B=3 C=2` x3; `CALL A=2 B=3 C=2`; `CALL A=5 B=2 C=2`; `CALL A=7 B=4 C=2` x3; `CALL A=7 B=7 C=1`; `CALL A=8 B=3 C=1`; `CALL A=11 B=3 C=2`; `CALL A=12 B=2 C=2`; `CALL A=12 B=3 C=2` x4; `CALL A=12 B=12 C=5`; `CALL A=16 B=3 C=2` x2 |
| 29 | `previousSequence` | `CALL A=1 B=2 C=1`; `CALL A=1 B=2 C=2`; `CALL A=1 B=4 C=1`; `CALL A=2 B=3 C=2`; `CALL A=2 B=5 C=1`; `TAILCALL A=2 B=2 C=0` |
| 30 | `processUICommandOperate` | `CALL A=5 B=2 C=1` x2; `CALL A=5 B=2 C=2`; `CALL A=6 B=3 C=1` |
| 31 | `processUICommandCancel` | `CALL A=5 B=2 C=1`; `CALL A=5 B=3 C=1` |
| 32 | `processUICommandClose` | `CALL A=5 B=2 C=1`; `CALL A=5 B=3 C=1` |
| 33 | `processUICommandSelection` | `CALL A=5 B=2 C=1`; `CALL A=5 B=3 C=1` x2; `CALL A=5 B=3 C=2` x2; `CALL A=5 B=4 C=2`; `CALL A=6 B=2 C=1`; `CALL A=6 B=2 C=2`; `CALL A=6 B=3 C=2` x2; `CALL A=7 B=2 C=1`; `CALL A=7 B=3 C=1`; `CALL A=7 B=4 C=1` x3; `CALL A=7 B=6 C=1` |
| 34 | `processUICommandDefault` | `CALL A=6 B=2 C=1`; `CALL A=6 B=3 C=1` x3; `CALL A=6 B=5 C=1` x2; `CALL A=7 B=2 C=2` |
| 35 | `processTimer` | `CALL A=1 B=4 C=2`; `CALL A=2 B=2 C=1`; `CALL A=2 B=3 C=1`; `CALL A=2 B=5 C=1` x2 |
| 36 | `catalogSkip` | `CALL A=3 B=3 C=2`; `CALL A=5 B=3 C=1`; `CALL A=6 B=3 C=2`; `CALL A=7 B=7 C=2`; `CALL A=13 B=4 C=2`; `CALL A=14 B=7 C=2` |
| 37 | `selectedBorder` | `CALL A=3 B=3 C=2`; `CALL A=4 B=3 C=1`; `CALL A=5 B=3 C=2`; `CALL A=5 B=6 C=1`; `CALL A=8 B=6 C=1` |
| 38 | `changeList` | `CALL A=1 B=0 C=1`; `CALL A=4 B=4 C=0`; `CALL A=7 B=2 C=2`; `TAILCALL A=1 B=3 C=0` |
| 39 | `operateSort` | `CALL A=2 B=2 C=1` x2; `CALL A=2 B=3 C=1` |
| 40 | `isOperateButtonEnable` | `CALL A=4 B=3 C=2`; `CALL A=5 B=3 C=2` x3; `CALL A=8 B=5 C=2`; `CALL A=9 B=2 C=2` x3; `CALL A=9 B=4 C=2`; `CALL A=10 B=4 C=2` |
| 41 | `closeWidget` | `CALL A=2 B=2 C=2`; `CALL A=3 B=3 C=1`; `CALL A=3 B=4 C=1` |
| 42 | `updateItemList` | `CALL A=4 B=2 C=1` x2; `CALL A=4 B=3 C=2` x2; `CALL A=4 B=4 C=1` x2; `CALL A=5 B=3 C=1` x2 |
| 43 | `updatePlayerItem` | `CALL A=4 B=2 C=1` x2; `CALL A=4 B=3 C=2` x3; `CALL A=4 B=4 C=1` x2; `CALL A=5 B=3 C=1` x3 |
| 44 | `syncItemWork` | none |
| 45 | `displaySortType` | `CALL A=2 B=5 C=1` |
| 46 | `changeSortType` | `CALL A=2 B=3 C=2` |
| 47 | `saveSortType` | `CALL A=1 B=3 C=1` |

## Open-width call boundaries

These are the complete CALL/TAILCALL occurrences with B=0 or C=0.
Their forwarded arguments or results cannot be reduced to a fixed
property-name tuple without the opaque helper behavior.

| child | method | opcode | pc | decoded offset | A | B | C |
|---:|---|---|---:|---:|---:|---:|---:|
| 15 | `getListBoxItemNum` | `CALL` | 3 | 10867 | 4 | 3 | 0 |
| 15 | `getListBoxItemNum` | `TAILCALL` | 4 | 10871 | 2 | 0 | 0 |
| 17 | `focusToIndex` | `TAILCALL` | 21 | 11346 | 5 | 4 | 0 |
| 29 | `previousSequence` | `TAILCALL` | 37 | 20001 | 2 | 2 | 0 |
| 38 | `changeList` | `CALL` | 10 | 24301 | 4 | 4 | 0 |
| 38 | `changeList` | `CALL` | 11 | 24305 | 1 | 0 | 1 |
| 38 | `changeList` | `TAILCALL` | 18 | 24333 | 1 | 3 | 0 |

## Consequential fixed receiver and argument tuples

- Root `require` receives exactly `/Widget/WidgetBaseClass`; root
  `_defineClass` receives exactly `ItemSelectWidget`,
  `WidgetBaseClass`.
- `init` calls `setDrag(true)`, `initListBox(1)` through
  `initListBox(5)`, requests `TabItem_3`, `TabItem_4`, and
  `TabItem_5` visibility false, and calls `setInitialData(A1..A5)`.
- `initForm` registers only the exact command literals
  `UILuaCommands.TabChanged` and `UILuaCommands.ButtonFocused`;
  `initListBox` registers MouseEnteredItem, AnchoredItem, Selection,
  Previous, and Next. `UILuaCommands.Cancel` is absent; `initForm`
  calls `self.setCancelCondition()`/`self.setCloseCondition()` with
  no control argument and uses self-method condition calls.
- `processUICommandDefault` tests exact
  `UILuaCommands.MouseEnteredItem`, `UILuaCommands.AnchoredItem`,
  `UILuaCommands.TabChanged`, `UILuaCommands.ButtonFocused`,
  `UILuaCommands.Previous`, and `UILuaCommands.Next`; A5 is its
  sixth formal argument. `processUICommandSelection` stores A3/A4
  as focus/listbox, calls `setReward(package,item)` in mode 400,
  and calls `setOrderItemData(2,package,item,orderStack)` in mode
  440. `previousSequence` calls `setOrderItemData(1,0,0)` in
  mode 440.
- `setItemToXmlLight` calls `desktopWidget.setItemToXml` with 19
  total arguments including its desktop receiver, hence 18 operands
  after that receiver: `(widgetSelf, propertyName, index, item,
  tableName, catalog, icon, stackable, count, nameIndex, sorttype,
  true, false, sortField, A3, A4, A5, false)` after the desktop
  receiver. Sorttype defaults from work for listbox 1/unrecognized
  listboxes; mode 440's hidden count failure is `count < orderStack`,
  and that failure or a catalog/quality mismatch sets local R19 false
  while normal return remains true. Opacity uses exact strings
  `"0.5"`/`"1.0"`.
- `isOperateButtonEnable` computes `getPackageFromList(A1)` and
  `A2+1` locally but fetches using fresh `work.chosenPackage` and
  `work.chosenItem`; non-nil A3 overrides after that lookup.
- `changeList` calls `setText(self,"TextBlock_Title",...)` with
  every open result from `getControlProperty(...,"Header")`,
  including zero or multiple results, then tail-forwards display.
- `setWindowFocus` requests `setLogicalFocus(A1)`, then reads
  `_getKeyboardFocusedWidget()` and uses Lua `==` before requesting
  `setKeyboardFocusedControl(A1)`; the comparison is not raw
  identity.

## Local limits

The body proves local state writes, helper call operands, local guards,
and the explicit result arities above. It does not prove any caller or
open tuple, native helper implementation, work metamethod or readback
semantics, UI rendering or child lifetime, inventory mutation, item or
currency identity, server acceptance, actual use/sale/settlement, or
historical invocation. Helper/self/global binding, comparison
metamethods, arithmetic/concatenation effects, and normal completion
remain conditional on opaque runtime objects.
