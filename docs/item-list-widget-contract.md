# ItemListWidget list rows and item objects

`ItemListWidget` (`widget/itemlistwidget.lua`) maps six list numbers to list
property sources, list controls and item packages. Its row writer reads one
player item and forwards its display values to the desktop XML helpers. Its
selection handler requires keyboard focus before it records the chosen item,
and its sub menu is positioned from window properties. The item objects it
reads belong to a small Lua class family. These are recovered Lua request
contracts, not proof of native list materialization, focus or layout.

The [ItemSelectWidget contract](item-select-widget-contract.md) describes a
different widget, `SubItemListWidget`, whose name and package maps differ.
The [gil-shop opening contract](gil-shop-widget-opening.md#sheets-bound-during-item-initialization)
owns the item `_onInit` sheet bindings and the `itemName` word request.

## Item object classes

`ItemBaseClass`, `NormalItemBaseClass`, `ImportantItemBaseClass` and
`MoneyItemBaseClass` are not declared by `_defineClass` in their own
scripts. Those scripts add methods to the existing global class tables. The
concrete classes below declare their base with `_defineClass` after a
`require` of the base path, for example `/Item/Normal/NormalItemBaseClass`.

| Base | Declared subclasses |
| --- | --- |
| `NormalItemBaseClass` | `AdditionalEffectEquipItem`, `CmnBadStatusItem`, `CmnGoodStatusItem`, `CmnHateControlItem`, `CmnRemoveStatusItem`, `DummyItem`, `EnchantItem`, `EnchantMedicineItem`, `FoodItem`, `MateriaItem`, `PotionItem`, `RaiseItem`, `ShieldItem`, `SpecialEquipItem`, `StandardItem`, `ToolItem` |
| `ImportantItemBaseClass` | `ImportantItemStandard` |
| `MoneyItemBaseClass` | `MoneyStandard` |

Each subclass is the single `_defineClass` call in its script under
`lua/scripts/item/normal/`, `item/important/` or `item/money/`. The parent of
the four base tables is not established by these scripts.

`NormalItemBaseClass.init` (`item/normal/normalitembaseclass_common.lua`,
`root/proto17`), which the normal-item `_onInit` calls, replaces
`normalItemWork._sync` with these declarations in order (PCs 0-65):

| Member | Declaration |
| --- | --- |
| `life` | `integer32` |
| `use` | `integer16` |
| `materiaId` | `integer32` |
| `materiaLife` | `integer32` |
| `mainQuality` | `integer8` |
| `subQuality` | `array`, 3, `integer8` |
| `polish` | `integer32` |
| `param1`, `param2`, `param3` | `integer32` each |
| `fitness` | `integer16` |
| `materiaType` | `array`, 5, `integer8` |
| `materiaGrade` | `array`, 5, `integer8` |
| `_assignForChild` | 18 |

These are Lua work declarations. They do not establish the wire layout,
native storage or the server producer of the values.

## List names and packages

For a list number n, `getListPropertyName` returns
`"TabItem_"..tostring(n).."_Maker"` and `getListBoxName` returns
`"ListBox_TabItem_"..tostring(n)`, with no range test. `getListBoxItemNum(n)`
tailcalls `getListPropertyCount` with the property name, and the shared
`getListPropertyCount` tailcalls `_getProperty(W,nil,name,"Count")`.

`getPackageFromList` returns one package number:

| List | 1 | 2 | 3 | 4 | 5 | 6 | Other |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Package | 1 | 100 | 8 | 6 | 5 | 100 | 1 |

`init` requests `initForm`, then `initListBox` for 1 through 6, then
`setInitialData(W,A1,A2)` (`root/proto0` PCs 207-230). `initForm` ends with
`initChildWidget(W,"ItemSubWidget",false,true)` (`root/proto1` PCs 61-65).
For a nonempty list name, `initListBox(n)` (`root/proto2`) requests:

1. `setControlProperty(W,name,"IntData.Value0",n)`, so the control carries
   its own list number.
2. `setControlCommandCondition` on the list for
   `UILuaCommands.MouseEnteredItem`, `UILuaCommands.AnchoredItem` and
   `UILuaCommands.Selection`, then `setCancelCondition(W,name)`.
3. `setVisibility(W,name,true)`, then for `"TextBlock_NoContents_"..n`
   visibility false, a cancel condition and `IsTabStop` true.
4. `setControlCommandCondition` on the list for `UILuaCommands.Previous` and
   `UILuaCommands.Next`.

## Row write

`setItemToXmlLight(W,list,row,package,slot,extra)` (`root/proto29`) saves
the list property name and the local player. Only when both package and slot
are greater than 0 does it read one `player:_getItem(package,slot)` result
(PCs 8-16). A nil item returns one `false` (PCs 17-20). Otherwise it reads
one result each of `_getCatalogID`, `getItemIcon`, `_isStackable`,
`_countStack` and `_getNameIndex` (PCs 21-34). The row style is
`TBL_selectedItem` when `work.isRewardMode` equals true and the reward
package and item equal package and slot, and `TBL_null` otherwise (PCs
35-48).

Two further operands S and K depend on the list number: list 1 gives
`(work.sorttype,1)`, list 2 `(11,2)`, list 3 `(0,3)`, list 4 `(0,26)`,
list 5 `(0,4)` and list 6 `(12,5)`. Any other value keeps the list 1 pair
(PCs 49-86). Their meaning is not assigned
here. The method then requests, discarding results:

```text
desktopWidget:setItemToXml(W,name,row,item,style,catalog,icon,stackable,
                           stack,nameIndex,S,true,false,K,package,slot,extra,false)
desktopWidget:setItemDetailToXml(W,name,row,item,nameIndex,extra,K,true)
```

at PCs 87-107 and 108-118. The later grand company visibility and return
branches (PCs 119-183) are not interpreted here.

## Selection and default gates

`processUICommandSelection(W,t,c,focus,list)` (`root/proto10`) returns
without a request when `work.editWidgetOpen` differs from 0, when
`work.updatecount` is greater than 0, when
`desktopWidget:checkKeyboardFocused(W)` returns exactly false, or when focus
is nil or negative (PCs 0-21). It then stores `work.focus` and
`work.listbox` (PCs 22-25). An empty list requests
`updateWindowDisplay(W,true)` and returns. A focus index at or beyond
`getListBoxFocusNum(list)` requests `updateListFocus` and returns (PCs
26-50). Otherwise it requests `updateWindowDisplay(W,true)` and returns when
`work.waittrash` differs from false (PCs 51-58). The surviving path stores
`chosenPackage` from `getPackageFromList(work.listbox)` and `chosenItem` as
`work.index+1` (PCs 59-69). For lists other than 6 it requests
`openSubWidget(W)` and `selectedBorder(W,work.index,true)` (PCs 70-80).

`processUICommandDefault` (`root/proto11`) returns one `false` for a nonzero
`editWidgetOpen` or a positive `updatecount`, and zero values for an exact
`false` from `checkKeyboardFocused` (PCs 0-18). Its MouseEnteredItem and
AnchoredItem arm returns for a nil list or a nil or negative focus, and
otherwise stores focus and list and requests `setCommonTimer(W,0.2)`.
TabChanged stores `0+getSelectedTab()` in `work.listbox` and requests
`changeList`. Previous and
Next request `catalogSkip(W,-1)` and `catalogSkip(W,1)` (PCs 19-59).

`DesktopWidget.checkKeyboardFocused(D,W)` (connector `root/proto121`) keeps
one result of `D:_getKeyboardFocusedWidget()` and returns one `true` when it
equals W under Lua equality, otherwise one `false`.

## Sub-widget positioning

`openSubWidget` (`root/proto60`) looks up the child by window name
`ItemSubWidget` and returns at once when it is nil (PCs 0-4). Before any
menu request it calls `setSubPosition(W)` (PCs 20-21).

`setSubPosition` (`root/proto59`) makes the same nil test, then requests
`child:setProperty("Margin","0,0,0,0")` (PCs 0-8). It reads two results each
from `W:getWindowPosition()`, `W:getWindowSize()` and
`desktopWidget:getWindowSize()` (PCs 9-15), then two from
`child:getWindowSize()` (PCs 31-32). The shared getters read
`Left` and `Top`, and `ActualWidth` and `ActualHeight`, through `getProperty`
(common `root/proto143` and `root/proto144`), when these calls resolve to
the shared definitions.

With window position (x,y), window width w, child size (cw,ch) and desktop
size (dw,dh), the requests are:

1. left = x+64+w and top = y+36+120 (PCs 16-17, 30-35).
2. The right limit is dw-64 and the bottom limit dh-36. Only for a desktop
   of exactly 640 by 480 are they replaced by `dw*0.85` and `dh*0.85` (PCs
   18-29).
3. When left+cw exceeds the right limit, left moves back by the excess. When
   top+ch exceeds the bottom limit, top moves back by the excess (PCs
   36-43).
4. `child:setProperty("Top",top)` and `child:setProperty("Left",left)`
   (PCs 44-51).

The values written to the two unused limit registers at PCs 19, 21, 27
and 29 are not read afterwards. No lower clamp is applied to left or top.

## Source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule,
including every script under `lua/scripts/item/` named above. Original
resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `widget/itemlistwidget.lua` | 163059 / 6991 | `7006a5b52342d3f9a1439007b05667fe377a75a72fc8680988675b8e59d6ad01` |
| `item/normal/normalitembaseclass_common.lua` | 14399 / 805 | `35a05383355d7205f58ad999710e5eaf92331c899c683873b823aead755645f0` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| `widget/desktopwidget_connector.lua` | 660617 / 26564 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/1q5xy1rqn1635q.le.lpb` | 51910 / `f905d03e5b54218f690e37bf36db3f71f289468ff973004e1f030b684115e647` | 51897 / `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |
| `1q5x/wvsx9y/wvsx9y1q5x89r57y9rr_7vxxvw.le.lpb` | 7026 / `d44575e450e425d34517e31e56b7712a83e20d5dfa9062f05b53c05a970fb77e` | 7013 / `f58830f3844e1fb588d8434a75c873c87ac550a94e41ec1a444b24ba08a4cb97` |

The common and connector resource identities are pinned in the
[root slot contract](desktop-widget-root-slots.md#source-identity-and-locators).
Prototype indices and PCs are zero-based, and code starts are
decoded-payload offsets with PC n at start plus 4n.

| Method | Canonical lines | Root binding PC | Prototype / code start |
| --- | --- | ---: | --- |
| `init` | `itemlistwidget.lua:11-333` | 9 | `root/proto0` / `0xC8C` |
| `initForm` | `itemlistwidget.lua:336-419` | 12 | `root/proto1` / `0x13CB` |
| `initListBox` | `itemlistwidget.lua:422-492` | 15 | `root/proto2` / `0x1730` |
| `processUICommandSelection` | `itemlistwidget.lua:810-903` | 39 | `root/proto10` / `0x22B1` |
| `processUICommandDefault` | `itemlistwidget.lua:906-966` | 42 | `root/proto11` / `0x25A5` |
| `getListPropertyName` | `itemlistwidget.lua:1102-1113` | 51 | `root/proto14` / `0x2BBD` |
| `getListBoxName` | `itemlistwidget.lua:1560-1570` | 78 | `root/proto23` / `0x3A89` |
| `getListBoxItemNum` | `itemlistwidget.lua:1573-1584` | 81 | `root/proto24` / `0x3AF1` |
| `getPackageFromList` | `itemlistwidget.lua:1692-1711` | 93 | `root/proto28` / `0x3ED3` |
| `setItemToXmlLight` | `itemlistwidget.lua:1714-1909` | 96 | `root/proto29` / `0x3FAB` |
| `setSubPosition` | `itemlistwidget.lua:5272-5334` | 186 | `root/proto59` / `0x9AF0` |
| `openSubWidget` | `itemlistwidget.lua:5337-5940` | 189 | `root/proto60` / `0x9CD9` |
| NormalItem `init` | `normalitembaseclass_common.lua:519-622` | 53 | `root/proto17` / `0x13CA` |
| Common `getWindowPosition` | `widgetbaseclass_common.lua:2638-2653` | 431 | `root/proto143` / `0x6C50` |
| Common `getWindowSize` | `widgetbaseclass_common.lua:2656-2671` | 434 | `root/proto144` / `0x6CC4` |
| Common `getListPropertyCount` | `widgetbaseclass_common.lua:3208-3218` | 533 | `root/proto177` / `0x7CA9` |
| Connector `checkKeyboardFocused` | `desktopwidget_connector.lua:7039-7052` | 365 | `root/proto121` / `0x12DBE` |

Reproduction uses `tools/retail_script.py:decode_lpb` and the
`ChunkReader` and `instruction` definitions in
`tools/build_quest_contracts.py`. Check the EQ and LT operands and jump
targets of the package map, the selection gates and the 640 by 480 test,
and the CALL widths of the two XML requests.
