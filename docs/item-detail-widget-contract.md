# ItemDetailWidget contract

`ItemDetailWidget` is a local item-detail and count-edit widget. Its script
stores item selection, owner, display mode, count-edit state, and materia-list
state in `self.work`. It requests UI and desktop-widget operations, but this
script does not establish that those requests rendered, changed inventory, or
completed a widget lifetime.

## Source identity

The registry identifies `ItemDetailWidget` at `lua/registry.json:41780-41812`,
with the required base `/Widget/WidgetBaseClass` and 17 methods. The decoded
script is `lua/scripts/widget/itemdetailwidget.lua` at
`manifests/scripts.json:15506-15511`. The retail resource identity is
`n1635q/1q5x65q91yn1635q.le.lpb` at
`manifests/retail_lua_coverage.json:25098-25112`.

The LPB is 11779 bytes with SHA256
`39A799BDCA3EFC413B8D5FBA665F2AC9003B4A920D39C7C68C019BDDE1159231`.
Its decoded payload is 11766 bytes with SHA256
`02765094626F6CC314FD735031ED8C1464DC3D083E4BB85C00F928EB823782A1`.
The canonical LF decompile is 34088 bytes, 1519 lines, with SHA256
`D30231DD5B41777A0C10BF3E78D04C4309C88FAA03291A97DE236E529B022673`.

The LPB was reproduced with `tools/retail_script.py` and
`tools/vendor/unluac/unluac_2025_12_23.jar`, pinned at 796256 bytes with SHA256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
`retail_script.py` decodes the LPB, runs that JAR once, and applies the exact
CRLF-pair-to-LF canonicalization. The reader then parsed the decoded Lua 5.1
chunk with `ChunkReader` and `instruction` from
`tools/build_quest_contracts.py`.

## Local state

`init` declares these `_temp` fields on `self.work`:

| Field | Type | Field | Type |
| --- | --- | --- | --- |
| `chosenItem` | `integer32` | `chosenPackage` | `integer32` |
| `chosenOwner` | `integer8` | `chosenOperation` | `integer32` |
| `mode` | `integer16` | `index` | `integer32` |
| `listbox` | `integer8` | `listSelectStep` | `integer8` |
| `listColumnVisibility` | `integer32` | `page` | `integer8` |
| `bonus1` | `boolean` | `bonus2` | `boolean` |
| `bonus3` | `boolean` | `itemlife` | `boolean` |
| `bazaar` | `boolean` | `isRewardMode` | `boolean` |
| `rewardItem` | `integer32` | `rewardItemPackage` | `integer32` |
| `orderCatalog` | `integer32` | `orderStack` | `integer32` |
| `editWidgetMode` | `integer8` | `updatecount` | `integer32` |
| `slot` | `integer32` | `updatenexttime` | `boolean` |
| `closeok` | `boolean` | `demandSync` | `boolean` |
| `num1` | `integer32` | `num1max` | `integer32` |
| `num2` | `integer32` | `num2max` | `integer32` |

`init` explicitly initializes `chosenItem=0`, `chosenOperation=0`,
`isRewardMode=false`, `bonus1=false`, `bonus2=false`, `bonus3=false`,
`itemlife=false`, `bazaar=false`, and `mode=0`. Other declared fields are not
directly assigned by this method, although selected own calls can subsequently
write fields such as `mode`, `index`, `listSelectStep`, and display flags. This
list is not a claim about `work`'s global end state. These declarations and
writes are script-local; they do not prove native storage or readback.

## Methods

The arguments below are after the receiver. `ignored` means that the argument
is present in the fixed prototype but is not read by the method body.

| Method | Arguments after `self` | Local result |
| --- | --- | --- |
| `init` | `A1_2,A2_2,A3_2,A4_2` | zero values |
| `setInitialData` | `modal,mode` | zero values |
| `setButtonEvents` | `control` | zero values |
| `setGridVisibility` | `mode` | zero values |
| `setWindowFocus` | `controlName` | zero values |
| `setButtonContent` | `control,content` | zero values |
| `displayHelp` | `value` | zero values |
| `getListPropertyName` | `ignored` | one string, `WidgetInternal` |
| `displayName` | `owner` | zero values |
| `displayItemHelp` | `item,package,index,owner,title` | local tailcall; zero values for the nil branch and one `true` through the normal non-nil child method |
| `displayEmpty` | `owner` | zero values |
| `displayFocusedItemHelp` | `item,package,index,owner,ignored` | one literal `true` on normal completion; a nil lookup can error before return |
| `processUICommandEvent` | `ignored,control,command,value,ignored` | zero values on local normal paths; tailcall prefixes have open bytecode result width |
| `updateNumber` | `value,control` | zero values |
| `editCount` | `package,item,owner` | one literal `false` on missing item, otherwise one literal `true` on normal completion |
| `showMateriaList` | `item` | zero values |
| `closeMateriaList` | none | zero values |

The method and bytecode ledger below records the complete source, prototype, and
byte spans. The method bodies are `lua/scripts/widget/itemdetailwidget.lua:11-1517`
and their class bindings are at lines 415-1519.

Composed statements about these own methods require the selected pinned class
closures and normal completion; an opaque or replaced callee does not inherit
the composed result. The direct call rows retain open bytecode widths even when
the selected local callee has a known normal result.

## Initialization and display requests

`init` configures drag, edit-button command properties, button event/cancel
conditions, header text, an empty help text, and a materia-slot icon-help
request. It then forwards `A1_2,A2_2` to `setInitialData`. When `A2_2==620` and
`A3_2` is non-nil, it requests `worldMaster._getMyPlayer().createVirtualItem(A3_2,1,1,100)`,
passes that result to `displayItemHelp`, hides the two item-life icons, and
positions the widget next to `A4_2` using `getWindowPosition`, `getWindowSize`,
and desktop/widget sizes. The requested position uses
`parentX + parentWidth + 24` for left and `parentY + 32 + 20` (that is,
`parentY + 52`) for top; when the requested right or bottom would exceed the
desktop bounds, it clamps left with fixed width 446 and top with the widget height.
It requests title 12013 with `A3_2`, item-life text
3553 with 100, and style `TBL_parameterPlus`. If the desktop width is below
1280 it requests modal true, shows `Grid_Edit`, hides `Grid_ItemStack` and
`Grid_NumberInput_Gil`, and requests `setVisibility("Button_EditCommand",false)`.

`setInitialData` requests modal state, stores `mode`, resets `index` and
`listSelectStep` to zero, requests grid mode 1, and requests `hide` when the
mode is not 620. `setButtonEvents` reads the control `Command` property and
passes it to `setControlCommandCondition`, then requests `setCancelCondition`.

`setGridVisibility` requests these exact predicates:

- `Grid_Edit`: mode 6, 7, 8, or 9;
- `Grid_ItemStack`: mode 7;
- `Grid_NumberInput_Gil`: mode 8;
- `Grid_ActorName`: always true;
- `Grid_Help`: mode 2 or 3;
- `Grid_BackpackAndGil`: always false;
- `Grid_ItemNameBase`: mode 1, 4, 5, 6, 7, 8, 9, or 10;
- `Grid_ItemDetail1`, `Grid_ItemDetail2`: `work.bonus1`, `work.bonus2`;
- `Grid_ItemDetail3`: `bonus3 or itemlife or bazaar`;
- `Label_ItemBonus5`: `work.bonus3`;
- `Grid_ItemLife`: `work.itemlife`;
- `TOG_itemDetail`: always false.

`setWindowFocus` requests logical focus only for a non-nil, non-empty control
name. Nil and empty names skip the desktop read and both focus requests. For
other names it reads the desktop keyboard-focused widget and requests keyboard
focus on the control only when Lua equality compares that read equal to `self`. `setButtonContent`
requests `setContent(control,content)`. `displayHelp` requests
`setText("TextBlock_Help",value)`. `getListPropertyName` returns the exact
string `WidgetInternal` and ignores its second argument.

## Names, item help, and materia

`displayName(1)` reads `desktopWidget.getPlayerName()`, writes the actor name
with format 230 when non-nil or an empty string otherwise, requests style
`TBL_null`, and title 3510. `displayName(2)` does the same with
`getTargetName`, fallback `???`, style `TBL_null`, and title 3511.
`displayName(4)` uses `getRetainerName`, fallback `???`, style
`TBL_myRetainer`, and title 3511. Other owner values do nothing.

`displayItemHelp` resets `work.listSelectStep`. For a nil `item`, package `1`
selects title 3207 and every other package selects 3208, then the method
tailcalls `displayHelp(3140)` and does not proceed to positioning or showing.
For a non-nil item, a positive non-nil `title`
requests title text 215 with that title, then tailcalls
`displayFocusedItemHelp(item,package,index,owner,title)`. The tailcall has
open bytecode result width; under the pinned local binding and normal
completion, the nil helper path has zero results and the focused path has one
`true` result.

`displayEmpty(owner)` requests `displayName(owner)`, help 3140, clears
`bonus1`, `bonus2`, `bonus3`, and `itemlife` to false, sets `page=0`, and
requests grid mode 2. It returns zero values.

`displayFocusedItemHelp` first calls `getListPropertyName()` for one result
that is not used later, resets `work.index=0`, and captures the player from
`worldMaster._getMyPlayer()`. When `item` is nil, it
fetches one item from `_getItem(package,index)` for owner 1,
`getBazaarItem(package,index)` for owner 2, or
`getRetainerItem(package,index)` for owner 4. A still-nil item requests
`displayEmpty()` with no post-receiver argument and then still requests
`displayName(owner)`. It next performs the ordinary `item.isEquipment` member
access at PC54 on the nil value when owner is not 7, so an owner-1 fresh nil
lookup can fail there. Owner 7 skips that access, makes both detail requests,
and then reaches the nil-member access at PC169. The literal `true` result
requires normal completion.

For owner values other than 7, an equipment item is tested with
`isEquipment() == true` at PC55. The method scans equip points 1 through 27, records
the first four points whose `isFitForEquipPoint(point)` is exactly true, and
tries `_getEquippingItem(point)` in recorded order until one non-nil result is
found. For owner 7 it uses the original `item` argument as the comparison item,
not the fetched local item. It then requests `setItemDetail` with the selected
item, the helper result from PC123, and `work.index`, and requests
`setItemDetailEquip(self,selectedItem,resultFromPC149,work.index,comparisonItem,
false,false,false,false,owner==7,nil,nil,nil,mode==620 or mode==621)`.
The four results are stored in `bonus1`, `bonus2`, `bonus3`, and `itemlife`.

After the four-result detail call, PC170 tests `isEquipment()` with ordinary
Lua truthiness, so numeric `0` takes the materia-count path even though PC55's
exact-true scan did not. If that later test is truthy and
`desktopWidget.getAttachedMateriaCountByItem(item)>0`, it requests
`showMateriaList(item)`; otherwise it requests `closeMateriaList()`. Owner 7
requests grid mode 10, hides both equip icons, and requests `show`. Other
owners request grid mode 4. The method returns one literal true.

## Evaluation order and captures

Each call prefix evaluates its function lookup, receiver, and fixed arguments
before the requested call. At PC123 the desktop `setItemDetail` function and
receiver are captured before the `getListPropertyName` helper at PC123. The
index is freshly read at PCs124-125 after that helper and before PC126, which
passes both values. At PC149
the desktop `setItemDetailEquip` function and receiver are captured before the
helper at PC149. PCs150-151 freshly read `work.index` after that helper and
before PC163, which passes both values. The four `work` destinations for the PC163 results are captured
before PC149, so a helper that replaces `self.work` cannot retarget those
writes; C=5 selects four result slots, nil-padding missing slots and discarding
extras. A callback can still change the current global desktop or `self.work`
for later reads, so the source does not promise a frozen table or global
snapshot.

The command handler similarly obtains a parent widget before reading the
selected count and owner for `setItemCount`; the parent call is a request. This
ordering preserves captured receiver and argument values without claiming
native callback effects, readback, rendering, or lifetime.

`showMateriaList(item)` requests `desktopWidget.setMateriaListItems(self,item)`
and shows `Grid_MateriaEquipList` for a non-nil item. A nil item only hides that
grid. `closeMateriaList` hides the grid.

## Count editing and UI commands

`updateNumber(value,control)` handles the two number controls independently.
For `CustomControl_NumberInput`, it reads
`_getProperty(nil,control,"IsKeyboardFocusWithin")` and stores `value` in
`work.num1` only when the result is exactly true. The Gil control uses the same
guard and stores `work.num2`. Regardless of control name, value zero requests
`Button_EditCommand` disabled and every other value requests it enabled.

`editCount(package,item,owner)` stores all three chosen values. Owner nil or 1
uses button text 3510 and `worldMaster._getMyPlayer()._getItem(package,item)`;
other owners use text 3511 and `desktopWidget.getRetainerItem(package,item)`.
A nil item returns one false before any detail or focus request. A non-nil item
requests focused detail, shows `Grid_Edit`, reads catalog ID, icon, stackability,
and stack count, and hides or shows `Grid_ItemStack`. Catalog 1000001 enters Gil
mode: it calls `displayItemHelp`, hides the stack grid, shows the Gil grid,
sets `editWidgetMode=2`, `listSelectStep=1`, `num2=0`, and configures the Gil
control with minimum 0, value 0, maximum 1, then maximum `num2max` and value
`num2`. It requests grid mode 8 and disables the edit command.

Other catalogs hide the Gil grid, set `editWidgetMode=1`,
`listSelectStep=2`, and set `num1=num1max=count`. Only exact `false`
stackability forces count 1 and requests grid mode 6; exact `true` requests
grid mode 7, while nil or numeric `0` keeps the count and shows the stack grid
but still requests grid mode 6. The method writes ItemStackMax text 225 before
the special catalog clamp. In the Gil branch it assigns `num2max=count` before
the Gil control requests. Catalogs strictly between 1000002 and 1000101 clamp
`num1max` to 999 when it exceeds 999. The later `num1 > num1max` comparison at
PC115 is outside that catalog guard, so a callback can replace current work and
still be clamped for another catalog. It configures the normal control in the
exact request order minimum 1, value 1, maximum 1, maximum `num1max`, and value
`num1`, then enables the edit command. Both branches finally request modal
true, `desktopWidget.changeFocusedWidget(self,true)`, and focus the selected
control. Successful completion returns one literal true.

`processUICommandEvent` uses `command` as the dispatch key. Cancel hides in
modes 610 and 621, closes directly through `desktopWidget` in mode 620, and
otherwise focuses `Button_EditBack` unless that control is already supplied.
The edit-back path requests modal false, hides `Grid_Edit`, hides again only
when `editWidgetMode==2`, and tailcalls parent `setItemCount(0,chosenOwner)`.
Operate in mode 620 closes directly. `Button_EditBack` follows the same modal
and grid requests, but its mode-2 conditional is empty in the original body;
it does not request `hide` there. It then tailcalls parent
`setItemCount(0,chosenOwner)`. `Button_EditCommand` requests modal false and
hides `Grid_Edit`, then requests parent `setItemCount(num2,chosenOwner)` in
mode 2 or `setItemCount(num1,chosenOwner)` otherwise. The parent edit-back
calls are tailcalls with open result width and preserve the parent's arbitrary
result tuple. `Button_Back` hides only
in modes 610 and 621. A `NumberInputBox.ValueChanged` command calls
`updateNumber(value,control)`. These command branches make requests and do not
establish parent acceptance or applied count changes.

## Call and result evidence

The decoded reader found 17 child prototypes with 1249 method instructions,
177 direct `CALL` or `TAILCALL` instructions, and 33 `RETURN` instructions.
Lua 5.1 call prefixes are retained exactly: `CALL A B C` has `B-1` fixed
arguments and `C-1` fixed results, while `B=0` or `C=0` is open. This resource
has no direct `CALL` with `B=0`; its open result prefixes are tailcalls and
explicit open returns.

Material rows include `displayFocusedItemHelp` proto11 PC163, byte 7326,
`CALL A=19 B=16 C=5` for the four-result `setItemDetailEquip` request;
proto11 PC208, byte 7506, `RETURN A=16 B=2` for one literal true;
`editCount` proto14 PC37, byte 9773, one false result; and proto14 PC233,
byte 10557, one true result. The complete receiver, argument-register state,
prefix, and result-width rows are recorded in the direct-call rows below.
The ledger counts every return instruction; the public call section lists
direct calls rather than individual return or guard/control rows.

## Conditional child context and limits

The accepted `EventItemSelectWidget` contract supplies only conditional child
consumer context at `docs/event-item-select-widget-contract.md:147-159`: it
requests `displayItemHelp(item,1,index,1)`, `displayEmpty(7)`, title and
position requests, and modal/show/hide requests. That context does not
establish a native child binding or a historical invocation. Under only the
selected pinned `displayItemHelp` closure and normal completion, the omitted
fifth formal is the nil `title` argument; the caller evidence does not establish
that binding or execution occurred.

The script establishes local declarations, branch predicates, call operands,
captured work writes, literal results, and UI/help/count/materia requests. It
does not establish native initial values, native `_setProperty` or UI storage
and readback, rendered output,
focus completion, actual stat or inventory edits, accepted edits, server
settlement, item consumption, or widget lifetime. The behavior of
`worldMaster`, `desktopWidget`, item controls, parent widgets, base-widget
methods, and all native calls remains opaque. Unsupported coercion,
metamethod, callable, and native behavior remains unknown.

## Method and bytecode ledger

The following table is the complete 17-method ledger. `source` locates the
canonical decompile function body and binding; `debug` is the reader's
prototype line range; `arity` excludes the receiver; and `code` is the
reader-derived instruction byte span with an exclusive end.

| Method | source | prototype | debug | arity | stack | code | words | return instructions |
| --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: |
| `init` | `lua/scripts/widget/itemdetailwidget.lua:11-413; binding 415` | `root/proto0` | 64-187 | 4 | 39 | 744-1968 | 306 | 1 |
| `setInitialData` | `lua/scripts/widget/itemdetailwidget.lua:418-439; binding 441` | `root/proto1` | 196-206 | 2 | 6 | 3663-3731 | 17 | 1 |
| `setButtonEvents` | `lua/scripts/widget/itemdetailwidget.lua:444-460; binding 462` | `root/proto2` | 214-218 | 1 | 7 | 3896-3944 | 12 | 1 |
| `setGridVisibility` | `lua/scripts/widget/itemdetailwidget.lua:465-545; binding 547` | `root/proto3` | 227-287 | 1 | 6 | 4077-4489 | 103 | 1 |
| `setWindowFocus` | `lua/scripts/widget/itemdetailwidget.lua:550-568; binding 570` | `root/proto4` | 297-304 | 1 | 5 | 4981-5045 | 16 | 1 |
| `setButtonContent` | `lua/scripts/widget/itemdetailwidget.lua:573-580; binding 582` | `root/proto5` | 314-316 | 2 | 7 | 5194-5214 | 5 | 1 |
| `displayHelp` | `lua/scripts/widget/itemdetailwidget.lua:585-592; binding 594` | `root/proto6` | 324-326 | 1 | 6 | 5270-5290 | 5 | 1 |
| `getListPropertyName` | `lua/scripts/widget/itemdetailwidget.lua:597-601; binding 603` | `root/proto7` | 335-337 | 1 | 3 | 5363-5375 | 3 | 2 |
| `displayName` | `lua/scripts/widget/itemdetailwidget.lua:606-696; binding 698` | `root/proto8` | 346-375 | 1 | 8 | 5435-5747 | 78 | 1 |
| `displayItemHelp` | `lua/scripts/widget/itemdetailwidget.lua:701-741; binding 743` | `root/proto9` | 388-403 | 5 | 13 | 6042-6194 | 38 | 3 |
| `displayEmpty` | `lua/scripts/widget/itemdetailwidget.lua:746-770; binding 772` | `root/proto10` | 411-420 | 1 | 5 | 6398-6478 | 20 | 1 |
| `displayFocusedItemHelp` | `lua/scripts/widget/itemdetailwidget.lua:775-995; binding 997` | `root/proto11` | 433-539 | 5 | 35 | 6674-7514 | 210 | 2 |
| `processUICommandEvent` | `lua/scripts/widget/itemdetailwidget.lua:1000-1158; binding 1160` | `root/proto12` | 554-619 | 5 | 11 | 8190-8766 | 144 | 11 |
| `updateNumber` | `lua/scripts/widget/itemdetailwidget.lua:1163-1201; binding 1203` | `root/proto13` | 628-639 | 2 | 8 | 9254-9394 | 35 | 1 |
| `editCount` | `lua/scripts/widget/itemdetailwidget.lua:1206-1479; binding 1481` | `root/proto14` | 650-729 | 3 | 16 | 9625-10565 | 235 | 3 |
| `showMateriaList` | `lua/scripts/widget/itemdetailwidget.lua:1484-1505; binding 1507` | `root/proto15` | 737-750 | 1 | 6 | 11469-11537 | 17 | 1 |
| `closeMateriaList` | `lua/scripts/widget/itemdetailwidget.lua:1510-1517; binding 1519` | `root/proto16` | 758-765 | 0 | 5 | 11668-11688 | 5 | 1 |

## Direct call rows

Call shorthand is exact: `f(receiver; arg1, arg2)` names the resolved
function and separates its explicit receiver from fixed arguments; a
bare `f(arg1, arg2)` would mean no receiver, while `global.name` preserves
a global receiver. Each bracket retains raw `A`, `B`, and `C` operands;
`results=open` means `C=0`, otherwise the fixed result width is `C-1`.
A `nil` is an original nil operand, not a guessed default. The 17 rows
below include every direct call in each method, grouped by method and
located by its source function span; `A0_2` is the source receiver formal
and `A1_2` through `A5_2` are the source argument formals where shown.

- `init` source `lua/scripts/widget/itemdetailwidget.lua:11-413`: pc144/byte1320: setDrag(self; true) [A=5,B=3,C=1; results=0]; pc149/byte1340: setControlProperty(self; 'Button_EditBack', 'Command', 'UILuaCommands.Operate') [A=5,B=5,C=1; results=0]; pc152/byte1352: setButtonEvents(self; 'Button_EditBack') [A=5,B=3,C=1; results=0]; pc156/byte1368: setButtonContent(self; 'Button_EditBack', 3318) [A=5,B=4,C=1; results=0]; pc161/byte1388: setControlProperty(self; 'Button_EditCommand', 'Command', 'UILuaCommands.Operate') [A=5,B=5,C=1; results=0]; pc164/byte1400: setButtonEvents(self; 'Button_EditCommand') [A=5,B=3,C=1; results=0]; pc168/byte1416: setControlCommandCondition(self; 'CustomControl_NumberInput', 'NumberInputBox.ValueChanged') [A=5,B=4,C=1; results=0]; pc172/byte1432: setControlCommandCondition(self; 'CustomControl_NumberInput_Gil', 'NumberInputBox.ValueChanged') [A=5,B=4,C=1; results=0]; pc175/byte1444: setCancelCondition(self; 'CustomControl_NumberInput') [A=5,B=3,C=1; results=0]; pc178/byte1456: setCancelCondition(self; 'CustomControl_NumberInput_Gil') [A=5,B=3,C=1; results=0]; pc183/byte1476: setText(self; 'TextBlock_ItemLifeHeader', 214, 10091) [A=5,B=5,C=1; results=0]; pc188/byte1496: setText(self; 'TextBlock_RepairMaterialHeader', 214, 10093) [A=5,B=5,C=1; results=0]; pc192/byte1512: setText(self; 'TextBlock_Help', '') [A=5,B=4,C=1; results=0]; pc196/byte1528: setMateriaAttachSlotIconHelp(global.desktopWidget; self) [A=5,B=3,C=1; results=0]; pc200/byte1544: setInitialData(self; A1_2, A2_2) [A=5,B=4,C=1; results=0]; pc207/byte1572: _getMyPlayer(global.worldMaster) [A=5,B=2,C=2; results=1]; pc213/byte1596: createVirtualItem(result@pc207[0]; A3_2, 1, 1, 100) [A=6,B=6,C=2; results=1]; pc216/byte1608: displayItemHelp(self; result@pc213[0]) [A=7,B=3,C=1; results=0]; pc220/byte1624: setVisibility(self; 'Border_ItemLife_IconCaution', false) [A=7,B=4,C=1; results=0]; pc224/byte1640: setVisibility(self; 'Border_ItemLife_IconDanger', false) [A=7,B=4,C=1; results=0]; pc226/byte1648: getWindowPosition(A4_2) [A=7,B=2,C=3; results=2]; pc228/byte1656: getWindowSize(A4_2) [A=9,B=2,C=3; results=2]; pc236/byte1688: setProperty(self; 'Margin', '0,0,0,0') [A=13,B=4,C=1; results=0]; pc239/byte1700: getWindowSize(global.desktopWidget) [A=13,B=2,C=3; results=2]; pc241/byte1708: getWindowSize(self) [A=15,B=2,C=3; results=2]; pc253/byte1756: setProperty(self; 'Top', post-clamp top: T0=parentY+32+20; desktopHeight<T0+widgetHeight selects desktopHeight-widgetHeight, otherwise T0) [A=17,B=4,C=1; results=0]; pc257/byte1772: setProperty(self; 'Left', post-clamp left: L0=parentX+parentWidth+24; desktopWidth<L0+446 selects desktopWidth-446, otherwise L0) [A=17,B=4,C=1; results=0]; pc261/byte1788: setVisibility(self; 'Grid_ActorName', false) [A=17,B=4,C=1; results=0]; pc265/byte1804: setVisibility(self; 'Grid_BackpackAndGil', false) [A=17,B=4,C=1; results=0]; pc269/byte1820: setVisibility(self; 'Grid_Help', false) [A=17,B=4,C=1; results=0]; pc274/byte1840: setText(self; 'TextBlock_Title', 12013, A3_2) [A=17,B=5,C=1; results=0]; pc279/byte1860: setText(self; 'TextBlock_ItemLife', 3553, 100) [A=17,B=5,C=1; results=0]; pc283/byte1876: setStyle(self; 'TextBlock_ItemLife', 'TBL_parameterPlus') [A=17,B=4,C=1; results=0]; pc288/byte1896: setModal(self; true) [A=17,B=3,C=1; results=0]; pc292/byte1912: setVisibility(self; 'Grid_Edit', true) [A=17,B=4,C=1; results=0]; pc296/byte1928: setVisibility(self; 'Grid_ItemStack', false) [A=17,B=4,C=1; results=0]; pc300/byte1944: setVisibility(self; 'Grid_NumberInput_Gil', false) [A=17,B=4,C=1; results=0]; pc304/byte1960: setVisibility(self; 'Button_EditCommand', false) [A=17,B=4,C=1; results=0]
- `setInitialData` source `lua/scripts/widget/itemdetailwidget.lua:418-439`: pc2/byte3671: setModal(self; A1_2) [A=3,B=3,C=1; results=0]; pc11/byte3707: setGridVisibility(self; 1) [A=3,B=3,C=1; results=0]; pc15/byte3723: hide(self) [A=3,B=2,C=1; results=0]
- `setButtonEvents` source `lua/scripts/widget/itemdetailwidget.lua:444-460`: pc3/byte3908: getControlProperty(self; A1_2, 'Command') [A=2,B=4,C=2; results=1]; pc7/byte3924: setControlCommandCondition(self; A1_2, result@pc3[0]) [A=3,B=4,C=1; results=0]; pc10/byte3936: setCancelCondition(self; A1_2) [A=3,B=3,C=1; results=0]
- `setGridVisibility` source `lua/scripts/widget/itemdetailwidget.lua:465-545`: pc12/byte4125: setVisibility(self; 'Grid_Edit', mode==6 or mode==7 or mode==8 or mode==9) [A=2,B=4,C=1; results=0]; pc19/byte4153: setVisibility(self; 'Grid_ItemStack', mode==7) [A=2,B=4,C=1; results=0]; pc26/byte4181: setVisibility(self; 'Grid_NumberInput_Gil', mode==8) [A=2,B=4,C=1; results=0]; pc30/byte4197: setVisibility(self; 'Grid_ActorName', true) [A=2,B=4,C=1; results=0]; pc39/byte4233: setVisibility(self; 'Grid_Help', mode==2 or mode==3) [A=2,B=4,C=1; results=0]; pc43/byte4249: setVisibility(self; 'Grid_BackpackAndGil', false) [A=2,B=4,C=1; results=0]; pc64/byte4333: setVisibility(self; 'Grid_ItemNameBase', mode in {1,4,5,6,7,8,9,10}) [A=2,B=4,C=1; results=0]; pc69/byte4353: setVisibility(self; 'Grid_ItemDetail1', self.work.bonus1) [A=2,B=4,C=1; results=0]; pc74/byte4373: setVisibility(self; 'Grid_ItemDetail2', self.work.bonus2) [A=2,B=4,C=1; results=0]; pc87/byte4425: setVisibility(self; 'Grid_ItemDetail3', work.bonus3 or work.itemlife or work.bazaar) [A=2,B=4,C=1; results=0]; pc92/byte4445: setVisibility(self; 'Label_ItemBonus5', self.work.bonus3) [A=2,B=4,C=1; results=0]; pc97/byte4465: setVisibility(self; 'Grid_ItemLife', self.work.itemlife) [A=2,B=4,C=1; results=0]; pc101/byte4481: setVisibility(self; 'TOG_itemDetail', false) [A=2,B=4,C=1; results=0]
- `setWindowFocus` source `lua/scripts/widget/itemdetailwidget.lua:550-568`: pc6/byte5005: setLogicalFocus(self; A1_2) [A=2,B=3,C=1; results=0]; pc9/byte5017: _getKeyboardFocusedWidget(global.desktopWidget) [A=2,B=2,C=2; results=1]; pc14/byte5037: setKeyboardFocusedControl(self; A1_2) [A=2,B=3,C=1; results=0]
- `setButtonContent` source `lua/scripts/widget/itemdetailwidget.lua:573-580`: pc3/byte5206: setContent(self; A1_2, A2_2) [A=3,B=4,C=1; results=0]
- `displayHelp` source `lua/scripts/widget/itemdetailwidget.lua:585-592`: pc3/byte5282: setText(self; 'TextBlock_Help', A1_2) [A=2,B=4,C=1; results=0]
- `getListPropertyName` source `lua/scripts/widget/itemdetailwidget.lua:597-601`: none
- `displayName` source `lua/scripts/widget/itemdetailwidget.lua:606-696`: pc4/byte5451: getPlayerName(global.desktopWidget) [A=2,B=2,C=2; results=1]; pc11/byte5479: setText(self; 'TextBlock_ActorName', 230, result@pc4[0]) [A=3,B=5,C=1; results=0]; pc16/byte5499: setText(self; 'TextBlock_ActorName', '') [A=3,B=4,C=1; results=0]; pc20/byte5515: setStyle(self; 'TextBlock_ActorName', 'TBL_null') [A=3,B=4,C=1; results=0]; pc24/byte5531: setText(self; 'TextBlock_Title', 3510) [A=3,B=4,C=1; results=0]; pc30/byte5555: getTargetName(global.desktopWidget) [A=2,B=2,C=2; results=1]; pc37/byte5583: setText(self; 'TextBlock_ActorName', 230, result@pc30[0]) [A=3,B=5,C=1; results=0]; pc42/byte5603: setText(self; 'TextBlock_ActorName', '???') [A=3,B=4,C=1; results=0]; pc46/byte5619: setStyle(self; 'TextBlock_ActorName', 'TBL_null') [A=3,B=4,C=1; results=0]; pc50/byte5635: setText(self; 'TextBlock_Title', 3511) [A=3,B=4,C=1; results=0]; pc56/byte5659: getRetainerName(global.desktopWidget) [A=2,B=2,C=2; results=1]; pc63/byte5687: setText(self; 'TextBlock_ActorName', 230, result@pc56[0]) [A=3,B=5,C=1; results=0]; pc68/byte5707: setText(self; 'TextBlock_ActorName', '???') [A=3,B=4,C=1; results=0]; pc72/byte5723: setStyle(self; 'TextBlock_ActorName', 'TBL_myRetainer') [A=3,B=4,C=1; results=0]; pc76/byte5739: setText(self; 'TextBlock_Title', 3511) [A=3,B=4,C=1; results=0]
- `displayItemHelp` source `lua/scripts/widget/itemdetailwidget.lua:701-741`: pc9/byte6078: setText(self; 'TextBlock_Title', 3207) [A=6,B=4,C=1; results=0]; pc14/byte6098: setText(self; 'TextBlock_Title', 3208) [A=6,B=4,C=1; results=0]; pc17/byte6110: displayHelp(self; 3140) [A=6,B=3,C=0; results=open]; pc28/byte6154: setText(self; 'TextBlock_Title', 215, A5_2) [A=6,B=5,C=1; results=0]; pc35/byte6182: displayFocusedItemHelp(self; A1_2, A2_2, A3_2, A4_2, A5_2) [A=6,B=7,C=0; results=open]
- `displayEmpty` source `lua/scripts/widget/itemdetailwidget.lua:746-770`: pc2/byte6406: displayName(self; A1_2) [A=2,B=3,C=1; results=0]; pc5/byte6418: displayHelp(self; 3140) [A=2,B=3,C=1; results=0]; pc18/byte6470: setGridVisibility(self; 2) [A=2,B=3,C=1; results=0]
- `displayFocusedItemHelp` source `lua/scripts/widget/itemdetailwidget.lua:775-995`: pc1/byte6678: getListPropertyName(self) [A=6,B=2,C=2; results=1]; pc9/byte6710: _getMyPlayer(global.worldMaster) [A=10,B=2,C=2; results=1]; pc18/byte6746: _getItem(result@pc9[0]; A2_2, A3_2) [A=12,B=4,C=2; results=1]; pc27/byte6782: getBazaarItem(global.desktopWidget; A2_2, A3_2) [A=12,B=4,C=2; results=1]; pc36/byte6818: getRetainerItem(global.desktopWidget; A2_2, A3_2) [A=12,B=4,C=2; results=1]; pc42/byte6842: displayEmpty(self) [A=12,B=2,C=1; results=0]; pc45/byte6854: displayName(self; A4_2) [A=12,B=3,C=1; results=0]; pc55/byte6894: isEquipment(selected item L11) [A=18,B=2,C=2; results=1]; pc64/byte6930: isFitForEquipPoint(selected item L11; loop point L21) [A=22,B=3,C=2; results=1]; pc88/byte7026: _getEquippingItem(result@pc9[0]; fitting point L14) [A=18,B=3,C=2; results=1]; pc96/byte7058: _getEquippingItem(result@pc9[0]; fitting point L15) [A=18,B=3,C=2; results=1]; pc104/byte7090: _getEquippingItem(result@pc9[0]; fitting point L16) [A=18,B=3,C=2; results=1]; pc112/byte7122: _getEquippingItem(result@pc9[0]; fitting point L17) [A=18,B=3,C=2; results=1]; pc123/byte7166: getListPropertyName(self; self.work.listbox) [A=18,B=3,C=2; results=1]; pc126/byte7178: setItemDetail(desktopWidget function/receiver captured before pc123; self, selected item L11, result@pc123[0], work.index read afterward) [A=14,B=6,C=1; results=0]; pc149/byte7270: getListPropertyName(self; self.work.listbox) [A=23,B=3,C=2; results=1]; pc163/byte7326: setItemDetailEquip(desktopWidget function/receiver captured before pc149; self, selected item L11, result@pc149[0], work.index read afterward, comparison item L13, false, false, false, false, owner==7, nil, nil, nil, mode==620 or mode==621) [A=19,B=16,C=5; results=4]; pc170/byte7354: isEquipment(selected item L11) [A=16,B=2,C=2; results=1]; pc176/byte7378: getAttachedMateriaCountByItem(global.desktopWidget; selected item L11) [A=16,B=3,C=2; results=1]; pc184/byte7410: showMateriaList(self; selected item L11) [A=16,B=3,C=1; results=0]; pc187/byte7422: closeMateriaList(self) [A=16,B=2,C=1; results=0]; pc192/byte7442: setGridVisibility(self; 10) [A=16,B=3,C=1; results=0]; pc196/byte7458: setVisibility(self; 'IconControl_Equiped', false) [A=16,B=4,C=1; results=0]; pc200/byte7474: setVisibility(self; 'IconControl_NotEquiped', false) [A=16,B=4,C=1; results=0]; pc202/byte7482: show(self) [A=16,B=2,C=1; results=0]; pc206/byte7498: setGridVisibility(self; 4) [A=16,B=3,C=1; results=0]
- `processUICommandEvent` source `lua/scripts/widget/itemdetailwidget.lua:1000-1158`: pc7/byte8218: hide(self) [A=6,B=2,C=1; results=0]; pc17/byte8258: closeWidgetDirect(global.desktopWidget; self) [A=6,B=3,C=1; results=0]; pc25/byte8290: hide(self) [A=6,B=2,C=1; results=0]; pc32/byte8318: setWindowFocus(self; 'Button_EditBack') [A=6,B=3,C=0; results=open]; pc36/byte8334: setModal(self; false) [A=6,B=3,C=1; results=0]; pc40/byte8350: setVisibility(self; 'Grid_Edit', false) [A=6,B=4,C=1; results=0]; pc46/byte8374: hide(self) [A=6,B=2,C=1; results=0]; pc48/byte8382: _getParentWidget(self) [A=6,B=2,C=2; results=1]; pc53/byte8402: setItemCount(result@pc48[0]; 0, self.work.chosenOwner) [A=7,B=4,C=0; results=open]; pc64/byte8446: closeWidgetDirect(global.desktopWidget; self) [A=6,B=3,C=1; results=0]; pc70/byte8470: setModal(self; false) [A=6,B=3,C=1; results=0]; pc74/byte8486: setVisibility(self; 'Grid_Edit', false) [A=6,B=4,C=1; results=0]; pc80/byte8510: _getParentWidget(self) [A=6,B=2,C=2; results=1]; pc85/byte8530: setItemCount(result@pc80[0]; 0, self.work.chosenOwner) [A=7,B=4,C=0; results=open]; pc92/byte8558: setModal(self; false) [A=6,B=3,C=1; results=0]; pc96/byte8574: setVisibility(self; 'Grid_Edit', false) [A=6,B=4,C=1; results=0]; pc98/byte8582: _getParentWidget(self) [A=6,B=2,C=2; results=1]; pc108/byte8622: setItemCount(result@pc98[0]; self.work.num2, self.work.chosenOwner) [A=7,B=4,C=1; results=0]; pc115/byte8650: setItemCount(result@pc98[0]; self.work.num1, self.work.chosenOwner) [A=7,B=4,C=1; results=0]; pc125/byte8690: hide(self) [A=6,B=2,C=1; results=0]; pc135/byte8730: hide(self) [A=6,B=2,C=1; results=0]; pc142/byte8758: updateNumber(self; A4_2, A2_2) [A=6,B=4,C=1; results=0]
- `updateNumber` source `lua/scripts/widget/itemdetailwidget.lua:1163-1201`: pc6/byte9278: _getProperty(self; nil, A2_2, 'IsKeyboardFocusWithin') [A=3,B=5,C=2; results=1]; pc18/byte9326: _getProperty(self; nil, A2_2, 'IsKeyboardFocusWithin') [A=3,B=5,C=2; results=1]; pc28/byte9366: setEnable(self; 'Button_EditCommand', false) [A=3,B=4,C=1; results=0]; pc33/byte9386: setEnable(self; 'Button_EditCommand', true) [A=3,B=4,C=1; results=0]
- `editCount` source `lua/scripts/widget/itemdetailwidget.lua:1206-1479`: pc14/byte9681: setButtonContent(self; 'Button_EditCommand', 3510) [A=10,B=4,C=1; results=0]; pc17/byte9693: _getMyPlayer(global.worldMaster) [A=10,B=2,C=2; results=1]; pc21/byte9709: _getItem(result@pc17[0]; A1_2, A2_2) [A=11,B=4,C=2; results=1]; pc27/byte9733: setButtonContent(self; 'Button_EditCommand', 3511) [A=10,B=4,C=1; results=0]; pc32/byte9753: getRetainerItem(global.desktopWidget; A1_2, A2_2) [A=10,B=4,C=2; results=1]; pc43/byte9797: displayFocusedItemHelp(self; selected item L9, A1_2, A2_2, A3_2) [A=10,B=6,C=1; results=0]; pc47/byte9813: setVisibility(self; 'Grid_Edit', true) [A=10,B=4,C=1; results=0]; pc49/byte9821: _getCatalogID(selected item L9) [A=10,B=2,C=2; results=1]; pc52/byte9833: getItemIcon(selected item L9) [A=10,B=2,C=2; results=1]; pc55/byte9845: _isStackable(selected item L9) [A=10,B=2,C=2; results=1]; pc58/byte9857: _countStack(selected item L9) [A=10,B=2,C=2; results=1]; pc66/byte9889: setVisibility(self; 'Grid_ItemStack', false) [A=10,B=4,C=1; results=0]; pc71/byte9909: setVisibility(self; 'Grid_ItemStack', true) [A=10,B=4,C=1; results=0]; pc77/byte9933: setVisibility(self; 'Grid_NumberInput_Gil', false) [A=10,B=4,C=1; results=0]; pc90/byte9985: setGridVisibility(self; 7) [A=10,B=3,C=1; results=0]; pc94/byte10001: setGridVisibility(self; 6) [A=10,B=3,C=1; results=0]; pc100/byte10025: setText(self; 'TextBlock_ItemStackMax', 225, self.work.num1max) [A=10,B=5,C=1; results=0]; pc126/byte10129: _setProperty(self; nil, 'CustomControl_NumberInput', 'Minimum', 1) [A=10,B=6,C=1; results=0]; pc132/byte10153: _setProperty(self; nil, 'CustomControl_NumberInput', 'Value', 1) [A=10,B=6,C=1; results=0]; pc138/byte10177: _setProperty(self; nil, 'CustomControl_NumberInput', 'Maximum', 1) [A=10,B=6,C=1; results=0]; pc145/byte10205: _setProperty(self; nil, 'CustomControl_NumberInput', 'Maximum', self.work.num1max) [A=10,B=6,C=1; results=0]; pc152/byte10233: _setProperty(self; nil, 'CustomControl_NumberInput', 'Value', self.work.num1) [A=10,B=6,C=1; results=0]; pc157/byte10253: setEnable(self; 'Button_EditCommand', true) [A=10,B=4,C=1; results=0]; pc164/byte10281: displayItemHelp(self; selected item L9, A1_2, A2_2, A3_2) [A=10,B=6,C=1; results=0]; pc168/byte10297: setVisibility(self; 'Grid_ItemStack', false) [A=10,B=4,C=1; results=0]; pc172/byte10313: setVisibility(self; 'Grid_NumberInput_Gil', true) [A=10,B=4,C=1; results=0]; pc186/byte10369: _setProperty(self; nil, 'CustomControl_NumberInput_Gil', 'Minimum', 0) [A=10,B=6,C=1; results=0]; pc192/byte10393: _setProperty(self; nil, 'CustomControl_NumberInput_Gil', 'Value', 0) [A=10,B=6,C=1; results=0]; pc198/byte10417: _setProperty(self; nil, 'CustomControl_NumberInput_Gil', 'Maximum', 1) [A=10,B=6,C=1; results=0]; pc205/byte10445: _setProperty(self; nil, 'CustomControl_NumberInput_Gil', 'Maximum', self.work.num2max) [A=10,B=6,C=1; results=0]; pc212/byte10473: _setProperty(self; nil, 'CustomControl_NumberInput_Gil', 'Value', self.work.num2) [A=10,B=6,C=1; results=0]; pc215/byte10485: setGridVisibility(self; 8) [A=10,B=3,C=1; results=0]; pc220/byte10505: setEnable(self; 'Button_EditCommand', false) [A=10,B=4,C=1; results=0]; pc223/byte10517: setModal(self; true) [A=10,B=3,C=1; results=0]; pc228/byte10537: changeFocusedWidget(global.desktopWidget; self, true) [A=10,B=4,C=1; results=0]; pc231/byte10549: setWindowFocus(self; selected control L8) [A=10,B=3,C=1; results=0]
- `showMateriaList` source `lua/scripts/widget/itemdetailwidget.lua:1484-1505`: pc6/byte11493: setMateriaListItems(global.desktopWidget; self, A1_2) [A=2,B=4,C=1; results=0]; pc10/byte11509: setVisibility(self; 'Grid_MateriaEquipList', true) [A=2,B=4,C=1; results=0]; pc15/byte11529: setVisibility(self; 'Grid_MateriaEquipList', false) [A=2,B=4,C=1; results=0]
- `closeMateriaList` source `lua/scripts/widget/itemdetailwidget.lua:1510-1517`: pc3/byte11680: setVisibility(self; 'Grid_MateriaEquipList', false) [A=1,B=4,C=1; results=0]
