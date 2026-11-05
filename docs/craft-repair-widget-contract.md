# CraftRepairWidget local interaction contract

This contract describes the bounded local behavior recovered from one retail
`CraftRepairWidget` Lua resource: its Lua operands, predicates, local writes,
dynamic UI/child requests, and local result values. Native implementations,
caller dispatch, rendering, widget lifetime, item storage, server behavior, and
transaction settlement remain outside this contract.

## Reproducibility and public identity

The authenticated resource and generated source identity are:

- LPB: `client/script/n1635q/7s94qs5u91sn1635q.le.lpb`, 13607 bytes,
  SHA-256 `42FF0F97246C5FE6DB41834CCEE6F919C1FE1BC1180465C8B3FDB1A7CE094872`.
- Decoded Lua 5.1 payload: 13594 bytes, SHA-256
  `33109036DC439C105011DD6F12D6AA76BE0B38C886F2C3E6E0AE27DA2D704045`.
- Canonical LF source: `lua/scripts/widget/craftrepairwidget.lua`, 35844 bytes,
  1628 lines, SHA-256
  `4756FACC801EC743E43BC4EEBF53CB918751901AD533B7B52AA3F6F4AC226D0C`.
- Decoder route: `xivl-client-scripts:tools/retail_script.py`.
- Pinned JAR: `xivl-client-scripts:tools/vendor/unluac/unluac_2025_12_23.jar`,
  796256 bytes, SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
  Its public provenance record is
  `xivl-client-scripts:tools/vendor/unluac/PROVENANCE.json:2-5`.

The public manifest records the canonical source at
`xivl-client-scripts:manifests/scripts.json:15356-15361`. The retail resource
and payload pins are at
`xivl-client-scripts:manifests/retail_lua_coverage.json:25652-25666`.
The registry records `CraftRepairWidget`, its base path, and method names at
`xivl-client-scripts:lua/registry.json:40699-40738`. Formal arities and LF
windows are in
`xivl-client-structs:manifests/lua_api_contract.json:161581-161952`.

The chunk root has one `require("/Widget/WidgetBaseClass")` CALL with B=2,C=1
and one `_defineClass("CraftRepairWidget","WidgetBaseClass")` CALL with B=3,C=1.
It has 28 direct method prototypes, no method child prototypes, and no
TAILCALL. The root makes 28 method-name SETTABLE attempts in API order; those
attempts do not prove registry installation or successful binding. A bare
return is zero values, not one nil. All stated call widths are the original Lua
CALL B/C operands; helper result types remain dynamic.

## Complete method matrix

The receiver is the first argument in every row. The `arguments` names are
formal Lua slots, not native type claims. Every listed result assumes normal
local completion; an indexing, comparison, arithmetic or call failure is not
a method return.

| # | method | arguments / LF source | local behavior and decisive predicates | local result |
|---:|---|---|---|---|
| 1 | `init` | `self` / 11-298 | Declares `_temp` members `chosenSlot`, `chosenItem`, `chosenPackage`, `chosenOperation`, `focusedSlot`, `choosing`, `mode`, `isEnableQuest`, `isEnableRecipe`, `craftMode`, `editWidgetOpen`, `updatecount`, `repairitem`, `repairinum`, `repairicon`, `lastbutton`; first writes chosenItem 0, focusedSlot 0, choosing false, chosenOperation -1. For each slot i=1..8, requests ChooseSlot and ButtonFocused conditions, cancel condition, Value0=0, Value1=0, Value2=0, Value3=i, CommandParameter=i, two icon-0/hidden pairs, and NotEquiped_i/PolishMAX_i/Materia_i=false. It makes four `setButtonEvents` requests for Button_ClearMaterial, Button_CraftRepairByMain, Button_CraftRepairBySub, and Button_CraftRepairCancel, then requests the Label_IconSelected/ButtonFocused condition before child init tuple `CraftEditWidget,true,false,411`; nil equipped slot 2 or `isCraftWeapon() ~= true` requests sub repair hidden. | 0 values |
| 2 | `setInitialData` | `self,A1..A7` / 301-670 | Writes craftMode=A1 and isEnableRecipe=false; for comparable A3, positive shows skill text 3092 and two controls, nonpositive hides them, and nil is not safely admitted by the first strict numeric comparison. It calls the selected `setReadyMaterialInSlot(slot,0)` eight times; when each lookup selects the pinned helper, these request Value2=0 without requesting Value0/Value1. The first `CraftEditWidget` lookup at LF347 is nil-guarded. Non-nil A4 sets source-6 repair row, icon, permission/badge/materia, fitness/equipment properties, up to four exact-true fit points from 1..27, optional item life only when A5 is nonnil, unchanged A6 materia visibility including 0, and A7 as the fitness property, then writes repair item/count and performs a new unguarded lookup at LF558. If the numeric for-loop enters, LF567's `findItemSetSlot` receiver can fail under ordinary nil-indexing semantics at original SELF PC239 (offset 4179) before CALL PC243 or the LF575 icon refresh when that second lookup is nil. Nil A4 requests icon 0, Focusable false, and every empty-row default: catalog 0, quality 1, name empty, icon 0, lifemax 0, stack empty, stackable 0, stackCount 1, stackMax 0, and price empty; it does not write repairitem or repairinum. PolishMAX uses `A7 == 10000`: non-equal supplies false; equal with permission false/nil preserves that value; equal with truthy permission moves the boolean from the short-circuit hasItem tuples `(101,2001001)`, `(101,2001002)`, `(101,2001003)`, stopping at the first Lua-truthy result including 0. | 0 values on normal completion |
| 3 | `processBeforeShow` | `self,A1` / 673-690 | Exact `A1 == true` skips focus/help; all other values request main focus and help 3025,3026. | one `true` |
| 4 | `setButtonEvents` | `self,A1` / 693-717 | Reads the control Command and requests that command, ButtonFocused and cancel conditions. | 0 values |
| 5 | `setWindowFocus` | `self,A1` / 720-740 | Nil or empty A1 is a no-op. Otherwise requests logical focus; the desktop getter result is compared with self using Lua `==` at PC10, and only the equal branch requests keyboard control. This is a local request, not focus ownership or raw-identity proof. | 0 values |
| 6 | `openItemListWindow` | `self` / 743-798 | A nil child takes the opening-only branch and requests `desktopWidget.openChildWidget(desktopWidget,"CraftEditWidget",self,true,false)`; it does not set choosing or request focus change. A nonnil child becomes modal; slot Value0 zero opens its list, otherwise removes the item and refreshes icon/help, then sets choosing=true and requests `desktopWidget.changeFocusedWidget(desktopWidget,child,true)`. A false nonnil child is not the nil branch and can fail when the child method is indexed. | 0 values on normal completion |
| 7 | `countMaterialInSlot` | `self,A1,A2` / 801-819 | Scans slots 1..8 and counts only rows whose first and second slot values satisfy Lua `==` against A1 and A2; no raw-identity claim is made. | one count |
| 8 | `countEmptySlot` | `self` / 822-840 | Scans slots 1..8 and counts rows whose first slot value satisfies Lua `== 0`; nil is not equal to zero. | one count |
| 9 | `clearAllMaterialSlot` | `self` / 843-884 | Calls the selected `clearMaterialSlot` for slots 1..8, requests child stack output when the first child lookup is nonnil, then performs a second child lookup before refilling repair rows from repairitem/repairinum. If the numeric for-loop enters with that second result nil, ordinary nil indexing fails at SELF PC23 while preparing `findItemSetSlot`, before its CALL and final icon refresh; a nil-type `__index` can change that outcome. A positive fractional count below 1 skips the loop body. | 0 values on normal completion |
| 10 | `clearMaterialSlot` | `self,A1` / 887-929 | Nil A1 selects chosenSlot. If first slot value is zero, returns false. Otherwise writes 0,0, optionally requests child dummy row `slot+8`, refreshes using original A1, and returns true. | one `false` or one `true` |
| 11 | `setReadyMaterialInSlot` | `self,A1,A2` / 932-957 | Writes `IntData.Value2=A2` through `_setProperty` using the generated slot name without validation, then forwards A1,A2 to a present child. A false nonnil child passes the nil-only guard and can fail when the method is indexed/called. | 0 values on normal completion |
| 12 | `getSlotName` | `self,A1` / 960-972 | For comparable A1>0 executes `tostring(A1)` and `CONCAT("Button_MaterialSlot_",...)`; the result depends on dynamic conversion/concat completion and is not guaranteed to be a string. Nonpositive input takes the zero-result return. | one conditional concatenation result, or 0 values |
| 13 | `getSlotData` | `self,A1` / 975-1011 | Nil, nonpositive, and greater-than-8 A1 return three literal zeros. Valid A1 fresh-reads Value0, Value1, Value2. | three values |
| 14 | `setSlotData` | `self,A1,A2,A3` / 1014-1044 | Same slot guard as getter. Valid input writes Value0=A2 and Value1=A3 only, refreshes icons, and returns true. | one `false` or one `true` |
| 15 | `updateSlotIcon` | `self,A1` / 1047-1110 | A nil child result takes a bare return. A false nonnil child is not covered by that guard: an occupied-value path can fail when child icon indexing is reached, while an all-empty icon-0 path need not index the child. Nil A1 scans 1..8. Value0 not equal to literal zero, including Lua nil, selects child icon slot+8; otherwise Value2 not equal to zero selects child icon slot; otherwise icon 0. Icon 0 hides; another icon requests icon and visibility true. | 0 values on normal completion |
| 16 | `displaySlotItemHelp` | `self,A1` / 1113-1150 | Nil A1 selects chosenSlot. Both Value0 and Value2 zero displays help 3047,3048; otherwise present child receives left-item help at slot+8 or slot using strict `~= 0` semantics. | 0 values |
| 17 | `displayHelp` | `self,A1,A2,A3` / 1153-1168 | If child exists, forwards A1,A2 to displayLeftButtonHelp. A3 is unused. | 0 values |
| 18 | `processUICommandCancel` | `self,A1,A2,A3,A4` / 1171-1205 | `editWidgetOpen ~= 0` or `chosenOperation ~= -1` returns false. Exact cancel writes operation 0 and disables input. Other unguarded commands focus cancel and display 3029,3030. | one `false` on guards; otherwise 0 values |
| 19 | `processUICommandOperate` | `self,A1,A2,A3,A4` / 1208-1252 | `editWidgetOpen ~= 0` or positive updatecount returns false; nil/non-numeric updatecount can fail at the strict numeric comparison. Exact cancel writes operation 0; main/sub write operation 1/2 and lastbutton 1/2. Unknown commands leave those fields unchanged but still disable input. | one `false` on guards; otherwise one `true` |
| 20 | `processUICommandDefault` | `self,A1,A2,A3,A4,A5` / 1255-1340 | Its actual guards are `editWidgetOpen ~= 0` and `chosenOperation ~= -1`; it does not read updatecount. Thus editWidgetOpen=0, chosenOperation=0, updatecount=0 returns false before ClearSlot. At PCs12/18/26, A3 is the dispatcher event operand for ClearSlot, ChooseSlot, and ButtonFocused; A2 is the ButtonFocused control operand. When both guards pass, ClearSlot calls the dynamically selected `self.clearAllMaterialSlot` and returns true after normal completion, even if that binding is a no-op. ChooseSlot assigns A4, calls the selected `self.openItemListWindow` and returns true after normal completion. ButtonFocused uses A2: Label_IconSelected asks the child for item help at 0; ClearMaterial/Main/Sub/Cancel display 3023,3024 / 3025,3026 / 3027,3028 / 3029,3030; other controls read `IntData.Value3` and assign focusedSlot plus help only when that value is nonnil. | one `false` or one `true` for guards/clear/choose; 0 values for focus/other paths |
| 21 | `updatePlayerItem` | `self,A1,A2` / 1343-1359 | Forwards A1,A2 to an existing CraftEditWidget child; missing child is a bare return. | 0 values |
| 22 | `setInitialItems` | `self,A1..A8` / 1362-1425 | For each nonnil input, forwards it to ready slots 1..8. Zero is nonnil and is forwarded. Refreshes all icons. | 0 values |
| 23 | `setSlotItem` | `self,A1,A2,A3` / 1428-1480 | Numeric A3 outside 0..8 returns false; nil/non-numeric A3 can fail at the strict range comparisons; missing child returns zero values. It reads chosenSlot twice, once for loop start and again for end+8. Each iteration subtracts 8 at most once when the loop value exceeds 8 and reads slot data. Only the empty-slot arm requests `setSlotData(slot,A1,A2)` and child `setSlotItem(slot+8)` and decrements the counter at PC38. Every iteration then tests counter==0 at PC39, including an occupied first slot. With chosenSlot=0,count=1, getSlotData(0) yields zeros, setSlotData(0,...) returns false but is ignored, child still receives slot 8, and the counter reaches zero. Count 0 with an occupied first slot breaks immediately; count 0 after an empty write can continue filling later rows. | one `false` on guard; otherwise 0 values |
| 24 | `processWaitCallFunction` | `self` / 1483-1496 | Exact chosenOperation -1 returns false; every other value returns true. | one `false` or one `true` |
| 25 | `getCraftOperation` | `self` / 1499-1506 | Reads and returns the current chosenOperation, including -1, 0, 1, and 2. | one current value |
| 26 | `getCraftItems` | `self,A1` / 1509-1526 | Reads slot data. Value0 not equal to literal zero, including Lua nil, returns Value1, which may itself be nil; zero Value0 with Value2 not equal to zero returns literal 0; both zero returns literal -1. | one value: Value1, `0`, or `-1` |
| 27 | `returnFocus` | `self` / 1529-1579 | If choosing is exactly true, clears it and freshly reads chosenSlot for the guard at PC8. When that first value is 0 it jumps directly to return, with no main-button fallback even if lastbutton is 1. When the first value is nonzero, a second fresh chosenSlot read at PC13 supplies `getSlotName`; if that second value is 0, getSlotName returns zero results and the open focus CALL receives only its fixed receiver. The open focus CALL appends every returned name value without a value test. When choosing is not true, it freshly reads lastbutton for exact 1 and, only if that comparison is not 1, performs a second fresh read for exact 2, selecting main/sub help 3025,3026 or 3027,3028. | 0 values |
| 28 | `updateBuffInfo` | `self` / 1582-1628 | Scans status slots and stops at the first status in inclusive range 230002..230009. Requests both skill-information controls visible when found, hidden otherwise on numeric normal completion; nil/non-numeric status can fail at the ordered comparisons. | 0 values |

## Per-method CALL operand and result matrix

The entries are `target:B,C`; repeated loop calls use one prefix. `C=1` means
the call result is discarded, `C=2` requests one result, and `C=0` is an open
result sequence. `B=0` is an open argument sequence. Methods with no entry
have no CALL instruction.

| # | method | direct CALL prefixes | result width |
|---:|---|---|---|
| 1 | `init` | `setModal:3,1`; `setCancelCondition:2/3,1`; `tostring:2,2`; `setControlCommandCondition:4,1`; `setControlProperty:5,1`; `setIcon:4,1`; `setHidden:3,1`; `setVisibility:4,1`; `setButtonEvents:3,1`; `initChildWidget:6,1`; `_getMyPlayer:2,2`; `_getEquippingItem:3,2`; `isCraftWeapon:2,2` | 0 values |
| 2 | `setInitialData` | `setText:5,1`; `setVisibility:4,1` and open `0,1`; `setReadyMaterialInSlot:4,1`; `getChildWidgetByWindowName:3,2` twice (first LF347 nil-guarded, second LF558 unguarded); child `setItemToXml:9,1`; `getItemIcon:2,0`; `setIcon:0,1` in item arm and `setIcon:4,1` in nil-item arm; `getMaterializePermission:2,2`; `_getMyPlayer:2,2`; `hasItem:4,2`; `desktopWidget.cantEquipBadge(desktopWidget,...):6,0`; `getListPropertyName:3,2`; `setListProperty:6,1`; `canChangeFitness:2,2`; `isEquipment:2,2`; `isFitForEquipPoint:3,2`; `getItemRepairItem:2,2`; `getItemRepairItemNum:2,2`; `findItemSetSlot:4,1` after the second lookup; `updateSlotIcon:2,1` in item arm; `_setProperty:6,1`; `updateListProperty:3,1` | 0 values on normal completion, including first-child-nil bare return; ordinary second-child-nil receiver failure stops before any method return |
| 3 | `processBeforeShow` | `setWindowFocus:3,1`; `displayHelp:4,1` | one `true` |
| 4 | `setButtonEvents` | `_getProperty:5,2`; `setControlCommandCondition:4,1`; `setCancelCondition:3,1` | 0 values |
| 5 | `setWindowFocus` | `setLogicalFocus:3,1`; `_getKeyboardFocusedWidget:2,2`; Lua `==` at PC10; `setKeyboardFocusedControl:3,1` only on equal branch | 0 values |
| 6 | `openItemListWindow` | `getChildWidgetByWindowName:3,2`; `desktopWidget.openChildWidget(desktopWidget,...):6,1` on nil-child branch; `getSlotData:3,4`; child `setModal:3,1`; child `openItemList:2,1`; child `removeItem:2,1`; `updateSlotIcon:3,1`; `displaySlotItemHelp:3,1`; `desktopWidget.changeFocusedWidget(desktopWidget,...):4,2` only on nonnil-child branch | 0 values on normal completion; focus-change result discarded |
| 7 | `countMaterialInSlot` | `getSlotData:3,4` | one count |
| 8 | `countEmptySlot` | `getSlotData:3,2` | one count |
| 9 | `clearAllMaterialSlot` | `clearMaterialSlot:3,1`; `getChildWidgetByWindowName:3,2`; child `updateStackPrint:2,1`; child `findItemSetSlot:4,1`; `updateSlotIcon:2,1` | 0 values |
| 10 | `clearMaterialSlot` | `getSlotData:3,4`; `setSlotData:5,1`; `getChildWidgetByWindowName:3,2`; child `setDummyItem:3,1`; `updateSlotIcon:3,1` | one `false` or one `true` |
| 11 | `setReadyMaterialInSlot` | `getSlotName:3,2`; `_setProperty:6,1`; `getChildWidgetByWindowName:3,2`; child `setReadyItem:4,1` | 0 values |
| 12 | `getSlotName` | `tostring:2,2`; `CONCAT` combines the fixed prefix with the dynamic tostring result | one conditional concatenation result or 0 values |
| 13 | `getSlotData` | `getSlotName:3,2`; `getControlProperty:4,2` | three values |
| 14 | `setSlotData` | `getSlotName:3,2`; `setControlProperty:5,1`; `updateSlotIcon:3,1` | one `false` or one `true` |
| 15 | `updateSlotIcon` | `getChildWidgetByWindowName:3,2`; `tostring:2,2`; `getSlotData:3,4`; child `getSlotIcon:3,2`; `setHidden:3,1`; `setIcon:4,1`; `setVisibility:4,1` | 0 values |
| 16 | `displaySlotItemHelp` | `getSlotData:3,4`; `displayHelp:4,1`; `getChildWidgetByWindowName:3,2`; child `displayLeftItemHelp:3,1` | 0 values |
| 17 | `displayHelp` | `getChildWidgetByWindowName:3,2`; child `displayLeftButtonHelp:4,1` | 0 values |
| 18 | `processUICommandCancel` | `setInputEnable:3,1`; `setWindowFocus:3,1`; `displayHelp:4,1` | one `false` on guards; otherwise 0 values |
| 19 | `processUICommandOperate` | `setInputEnable:3,1` | one `false` on guards or one `true` |
| 20 | `processUICommandDefault` | `clearAllMaterialSlot:2,1`; `openItemListWindow:2,1`; `getChildWidgetByWindowName:3,2`; child `displayLeftItemHelp:3,1`; `displayHelp:4,1`; `getControlProperty:4,2`; `displaySlotItemHelp:3,1` | one `false` on guards, one `true` on clear/choose, otherwise 0 values |
| 21 | `updatePlayerItem` | `getChildWidgetByWindowName:3,2`; child `updatePlayerItem:4,1` | 0 values |
| 22 | `setInitialItems` | `setReadyMaterialInSlot:4,1`; `updateSlotIcon:2,1` | 0 values |
| 23 | `setSlotItem` | `getChildWidgetByWindowName:3,2`; `getSlotData:3,4`; `setSlotData:5,1`; child `setSlotItem:3,1`; `updateSlotIcon:2,1` | one `false` on guard; otherwise 0 values |
| 24 | `processWaitCallFunction` | none | one `false` or one `true` |
| 25 | `getCraftOperation` | none | one current value |
| 26 | `getCraftItems` | `getSlotData:3,4` | one Value1, literal `0`, or literal `-1` (Value1 may be nil) |
| 27 | `returnFocus` | `getSlotName:3,0`; `setKeyboardFocusedControl:0,1` on the open sequence; fixed focus `3,1`; `displayHelp:4,1` | 0 values |
| 28 | `updateBuffInfo` | `desktopWidget.getPlayerStatusSlotLength(desktopWidget):2,2`; `desktopWidget.getPlayerBufferStatus(desktopWidget,index):3,5`; `setVisibility:4,1` | 0 values |

## Operand-level details

The root call prefixes are fixed as stated above. The consequential open CALLs
are preserved exactly:

- In `setInitialData`, `getItemIcon` uses B=2,C=0. Its open results are
  forwarded to `setIcon` with B=0,C=1, whose results are discarded.
- `desktopWidget.cantEquipBadge(desktopWidget,child,"SlotItem_Maker",0,A4)` uses B=6,C=0.
  Its open results are forwarded as the suffix of `setVisibility` with B=0,C=1.
- In `returnFocus`, `getSlotName(self,chosenSlot)` uses B=3,C=0 and the
  resulting open sequence is forwarded to `setKeyboardFocusedControl` with
  B=0,C=1.
- `setReadyMaterialInSlot` calls `getSlotName` with B=3,C=2. Under that
  pinned helper, a nonpositive input returns zero values and the CALL pads
  the name with nil. The next CALL has B=6,C=1 and supplies the five
  explicit operands `_setProperty(self,nil,name,"IntData.Value2",A2)`.
  The literal nil prefix remains present even when the padded name is nil.

These widths do not establish typed native returns or a fixed callable-object
implicit argument convention. Lua `==`/`~=` predicates retain language
equality and possible shared `__eq` metamethod behavior; they are not raw
identity tests. No TAILCALL exists in the root or methods, so no
method inherits an unbounded callee result sequence by tail dispatch. A CALL
that requests one result can still have that result stored and then discarded,
as in the desktop focus-change request.

The SETTABLE attempts in `init` and the work-member reads/writes in later
methods establish only Lua-side assignment and fresh-read operands. They do
not prove registry installation, initial-value population, native storage,
setter application, or readback. Every description that composes a self-method body with its caller
requires each dynamic lookup to select the pinned local binding and every
operation to complete normally. This applies to all composed helper claims,
including Value2/getter/setter descriptions; the call itself does not prove
that its requested effect happened.
Conditions involving `worldMaster`, `desktopWidget`, inherited methods, child
methods, and item methods remain conditional on the actual selected binding
and the helper's normal completion. Child lookup/open/focus/help calls are
requests and do not prove rendering, focus ownership, child creation, or child
destruction.

## Local interaction groups

### Initialization and material slots

`init` establishes the local declaration and first-write sequence, while
`setInitialData` selects the skill-visible/hidden and item/non-item arms. Slot
data uses the three control fields Value0, Value1, and Value2. The setter writes
only Value0/Value1; ready-material writes Value2. Slot icon selection prefers
the child row (`slot+8`) when Value0 is nonzero, then the base row when Value2
is nonzero. These assignments and child calls are requests, not proof of
native storage or a successful child operation.

### Item selection and operation

The `UILuaCommands.*` command operands below are literal strings in this
resource. The published local command names are `UILuaCommands.ClearSlot`,
`UILuaCommands.ChooseSlot`, `UILuaCommands.ButtonFocused`,
`Button_CraftRepairByMain`, `Button_CraftRepairBySub`, and
`Button_CraftRepairCancel`. Clear and choose have one true result in the
default dispatcher. Operate returns one true for every unguarded command,
including unknown commands, after disabling input. Cancel's unguarded paths
return zero values. The count-0 behavior in `setSlotItem` follows the original
counter decrement and break order and should not be normalized by a caller.

### Wait, result, cancel, focus, and buff continuation

The wait/result pair exposes only chosenOperation. `getCraftItems` distinguishes
the nonzero item value from literal zero and literal -1. `returnFocus` has an
open result-forwarding focus call after `getSlotName` for a nonzero chosen slot;
only when `choosing` is not true does it select the last main/sub button, so
choosing=true/slot0 has no fallback. `updateBuffInfo` uses only the inclusive literal status
range and visibility requests. No local result is a craft success, server
acceptance, settlement, payment, durability, quality, reward, or inventory
mutation signal.

## Caller and evidence boundary

The published `CraftJudge.startRepair` continuation calls
`askCraftRepairWidget(0,0,A3,virtualItem,A6,A7,A8)` in the player branch at
`root/proto20`, CALL PC 34, B=9,C=5, and records its later mode/result remap at
`xivl-client-scripts:docs/repair-request-client-contract.md:180-192`. This
seven-operand tuple is retained exactly. It can be transferred into this
receiver's `setInitialData` only when actual helper creation/init dispatch
selects this pinned binding. The widget body alone does not prove that
selection, a server-selected callback, 24243/22012 settlement, debit, material
consumption, durability repair, payment, success, or destruction.

The [selected helper flow](craft-repair-selection-flow.md) owns the conditional
creation/init, result-width, wait and explicit-close composition. Actual
caller invocation, native application, rendering, lifetime, item identity and
server edges remain unresolved.
