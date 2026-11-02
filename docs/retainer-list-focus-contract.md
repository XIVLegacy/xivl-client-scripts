# Ask RetainerItemListWidget list and focus contract

The Ask resource `lua/scripts/widget/ask/retaineritemlistwidget.lua` is a
member of the published `eventTalkRetainerItemList(2)` Ask route. The selected
methods contain local list, tab, display, filtering, and focus utilities whose
conditional compositions are described below. Route membership does not prove
that every utility is invoked on every route execution. This contract reports
only recovered Lua instructions. It does not assign native storage, rendering,
widget lifetime, server acceptance, inventory mutation, or settlement behavior.

Local compositions require the selected pinned Lua closures and normal
completion of intervening accesses and calls. The caller context does not
establish runtime construction or native helper binding.

## Pinned resource

The source identity is anchored by these records:

- LPB path `n1635q/9rz/s5q91w5s1q5xy1rqn1635q.le.lpb`, 50376 bytes,
  SHA-256 `CF7DA0872C6EB1743C9A2C73C11769022D030BDCE1F67CFA4FE2A8EF9127E81E`:
  `manifests/retail_lua_coverage.json:26642-26655`.
- Authenticated decoded payload, 50363 bytes, SHA-256
  `408CF496ED3FCDA95C53A6925CC9C8E689C517E37893E6D566E55E0A64AAE469`.
- Canonical LF source, 156026 bytes and 6813 lines, SHA-256
  `854328615DFAC84F08861DA2157300EDFAD67D63010783EBD7F520969C2521E6`:
  `manifests/scripts.json:15140-15144`.
- Class and base metadata: `lua/registry.json:39614-39700` and
  `xivl-client-structs:manifests/lua_api_contract.json:152947-153908`.

Instruction and prototype offsets use
`tools/build_quest_contracts.py:ChunkReader` and `instruction`. The complete
reader-derived method ledger and curated direct-call rows are included below.

## Root bindings and scope

The resource root has 76 direct children. The thirteen admitted methods are
bound by root `SETTABLE` attempts at PCs 24, 27, 30, 33, 48, 51, 54, 57, 60,
63, 66, 69, and 72, with payload offsets 128, 140, 152, 164, 224, 236, 248,
260, 272, 284, 296, 308, and 320. These are source-level binding attempts and
do not prove class installation or runtime readback.

The selected methods are direct children 5, 6, 7, 8, 13, 14, 15, 16, 17,
18, 19, 20, and 21. Each has zero nested children. No other method body was
used. The already published Ask selection, cancel, close, focus continuation,
code-22 result, delay, and repricing facts remain in
`retainer-item-list-cancel-contract.md`, `retainer-widget-results.md`, and
`bazaar-retainer-client-contracts.md`.

## Reader-derived method ledger

Source locators below use the canonical LF member
`lua/scripts/widget/ask/retaineritemlistwidget.lua`. Prototype indices and
instruction words are zero-based. Arity includes the receiver. Reader spans
are the starts of the first and last four-byte instruction words in each
selected prototype; the last word occupies its start offset through start+3.
`debug` is the recovered first-last source line pair.

| Method | Source locator | Prototype | Debug | Arity | Stack | Upvalues | Code words | Nested children | First word start / PC | Last word start / PC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `getListPropertyName` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:794-823` | `root/proto5` | 327-347 | 2 | 3 | 0 | 40 | 0 | 7788 / PC0 | 7944 / PC39 |
| `updateWindowDisplay` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:826-873` | `root/proto6` | 356-372 | 2 | 6 | 0 | 37 | 0 | 8227 / PC0 | 8371 / PC36 |
| `updateListFocus` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:876-1004` | `root/proto7` | 379-441 | 1 | 13 | 0 | 107 | 0 | 8643 / PC0 | 9067 / PC106 |
| `setGridVisibility` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1007-1085` | `root/proto8` | 449-473 | 2 | 6 | 0 | 83 | 0 | 9597 / PC0 | 9925 / PC82 |
| `getSelectedTab` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1243-1253` | `root/proto13` | 578-580 | 1 | 4 | 0 | 6 | 0 | 11655 / PC0 | 11675 / PC5 |
| `getListBoxName` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1256-1282` | `root/proto14` | 589-607 | 2 | 3 | 0 | 33 | 0 | 11775 / PC0 | 11903 / PC32 |
| `getListBoxItemNum` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1285-1296` | `root/proto15` | 617-619 | 2 | 7 | 0 | 7 | 0 | 12145 / PC0 | 12169 / PC6 |
| `getListBoxFocusNum` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1299-1335` | `root/proto16` | 631-644 | 2 | 10 | 0 | 30 | 0 | 12264 / PC0 | 12380 / PC29 |
| `focusToIndex` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1338-1366` | `root/proto17` | 654-663 | 3 | 10 | 0 | 26 | 0 | 12554 / PC0 | 12654 / PC25 |
| `indexToFocus` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1369-1401` | `root/proto18` | 673-684 | 3 | 11 | 0 | 24 | 0 | 12843 / PC0 | 12935 / PC23 |
| `initListBox` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1404-1474` | `root/proto19` | 692-710 | 2 | 9 | 0 | 55 | 0 | 13147 / PC0 | 13363 / PC54 |
| `resetListBox` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1477-1522` | `root/proto20` | 719-735 | 2 | 14 | 0 | 36 | 0 | 13757 / PC0 | 13897 / PC35 |
| `getPackageFromList` | `lua/scripts/widget/ask/retaineritemlistwidget.lua:1525-1542` | `root/proto21` | 744-758 | 2 | 3 | 0 | 22 | 0 | 14135 / PC0 | 14219 / PC21 |

## Curated direct-call matrix

The rows below cover every direct CALL or TAILCALL in the thirteen selected
prototypes. Each entry is `PC@byte target(receiver; actual prefix) B/C ->
result-width`, where the prefix is the actual Lua argument prefix including the
receiver for method calls. `C=1` is zero results, `C=2` is one result, and
`C=0` is open results. `B=0,C=0` on the `getListPropertyCount` tailcall
passes the fixed receiver `self` followed by all live results from the
preceding open `getListPropertyName` call; it does not reserve a fixed
`propertyName` slot. For unsupported listbox 7, that getter returns zero
results, so the count request receives only `self`; multiple live results all
propagate.
`propertyName`, `listBoxName`, `noContents`, and `child` are selected helper
results; `gridHelp`, `itemName`, and `detail3` are source-computed operands.

| Method and source locator | Actual CALL prefix and result width |
| --- | --- |
| `getListPropertyName` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:794-823`) | No direct call. |
| `updateWindowDisplay` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:826-873`) | `2@8235 setGridVisibility(self; self,8) B3/C1 -> 0`; `10@8267 setVisibility(self; self,"Grid_MateriaEquipList",true) B4/C1 -> 0`; `14@8283 setVisibility(self; self,"Grid_TabList",false) B4/C1 -> 0`; `22@8315 setVisibility(self; self,"Button_SortStatus",true) B4/C1 -> 0`; `26@8331 displaySortType(self; self,self.work.sorttype) B3/C1 -> 0`; `31@8351 setVisibility(self; self,"Button_SortStatus",false) B4/C1 -> 0`; `35@8367 updateListFocus(self; self) B2/C1 -> 0`. |
| `updateListFocus` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:876-1004`) | `3@8655 getListBoxFocusNum(self; self,self.work.listbox) B3/C5 -> 4`; `7@8671 getListBoxName(self; self,self.work.listbox) B3/C2 -> 1`; `12@8691 global tostring(no receiver; self.work.listbox) B2/C2 -> 1`; `22@8731 closeBazaarEdit(self; self,1) B3/C1 -> 0`; `30@8763 closeItemEdit(self; self,1) B3/C1 -> 0`; `42@8811 closeItemShare(self; self,1) B3/C1 -> 0`; `49@8839 getChildWidgetByWindowName(self; self,"ItemSubWidget") B3/C2 -> 1`; `53@8855 hide(child; child) B2/C1 -> 0`; `59@8879 setVisibility(self; self,noContents,true) B4/C1 -> 0`; `63@8895 displayFocusedItemHelp(self; self) B2/C1 -> 0`; `66@8907 setWindowFocus(self; self,noContents) B3/C1 -> 0`; `71@8927 setVisibility(self; self,noContents,false) B4/C1 -> 0`; `85@8983 focusToIndex(self; self,self.work.listbox,self.work.focus) B4/C2 -> 1`; `95@9023 setControlProperty(self; self,listBoxName,"SqwtFocusedIndex",self.work.focus) B5/C1 -> 0`; `100@9043 setFocusedIndex(self; self,listBoxName,self.work.focus) B4/C1 -> 0`; `103@9055 setWindowFocus(self; self,listBoxName) B3/C1 -> 0`; `105@9063 displayFocusedItemHelp(self; self) B2/C1 -> 0`. |
| `setGridVisibility` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1007-1085`) | `3@9609 setVisibility(self; self,"Grid_TabList",true) B4/C1 -> 0`; `7@9625 setVisibility(self; self,"Grid_ActorName",true) B4/C1 -> 0`; `22@9685 setVisibility(self; self,"Grid_Help",gridHelp) B4/C1 -> 0`; `26@9701 setVisibility(self; self,"Grid_BackpackAndGil",true) B4/C1 -> 0`; `39@9753 setVisibility(self; self,"Grid_ItemNameBase",itemName) B4/C1 -> 0`; `44@9773 setVisibility(self; self,"Grid_ItemDetail1",self.work.bonus1) B4/C1 -> 0`; `49@9793 setVisibility(self; self,"Grid_ItemDetail2",self.work.bonus2) B4/C1 -> 0`; `62@9845 setVisibility(self; self,"Grid_ItemDetail3",detail3) B4/C1 -> 0`; `67@9865 setVisibility(self; self,"Label_ItemBonus5",self.work.bonus3) B4/C1 -> 0`; `72@9885 setVisibility(self; self,"Grid_ItemLife",self.work.itemlife) B4/C1 -> 0`; `77@9905 setVisibility(self; self,"Grid_ItemBazaarInformation",self.work.bazaar) B4/C1 -> 0`; `81@9921 setVisibility(self; self,"Grid_MateriaAttachBazaarInformation",false) B4/C1 -> 0`. |
| `getSelectedTab` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1243-1253`) | `2@11663 getSelectedIndex(self; self,"TabControl_ItemList") B3/C2 -> 1`. |
| `getListBoxName` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1256-1282`) | No direct call. |
| `getListBoxItemNum` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1285-1296`) | `3@12157 getListPropertyName(self; self,listbox) B3/C0 -> open`; `4@12161 TAILCALL getListPropertyCount(self; self + all live getListPropertyName results) B0/C0 -> open`. |
| `getListBoxFocusNum` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1299-1335`) | `2@12272 getListBoxItemNum(self; self,listbox) B3/C2 -> 1`; `5@12284 getListPropertyName(self; self,listbox) B3/C2 -> 1`; `16@12328 getControlProperty(self; self,propertyName,"FilteredCount") B4/C2 -> 1`. |
| `focusToIndex` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1338-1366`) | `2@12562 getListPropertyName(self; self,listbox) B3/C2 -> 1`; `5@12574 getListBoxFocusNum(self; self,listbox) B3/C2 -> 1`; `19@12630 setControlProperty(self; self,propertyName,"FilteredIndex",index) B5/C1 -> 0`; `23@12646 TAILCALL getControlProperty(self; self,propertyName,"Index") B4/C0 -> open`. |
| `indexToFocus` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1369-1401`) | `3@12855 getListPropertyName(self; self,listbox) B3/C2 -> 1`; `6@12867 getListBoxItemNum(self; self,listbox) B3/C2 -> 1`; `9@12879 getListBoxFocusNum(self; self,listbox) B3/C2 -> 1`; `16@12907 setControlProperty(self; self,propertyName,"Index",index) B5/C1 -> 0`; `20@12923 getControlProperty(self; self,propertyName,"FilteredIndex") B4/C2 -> 1`. |
| `initListBox` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1404-1474`) | `2@13155 getListBoxName(self; self,index) B3/C2 -> 1`; `9@13183 setControlProperty(self; self,listBoxName,"IntData.Value0",index) B5/C1 -> 0`; `13@13199 setControlCommandCondition(self; self,listBoxName,"UILuaCommands.MouseEnteredItem") B4/C1 -> 0`; `17@13215 setControlCommandCondition(self; self,listBoxName,"UILuaCommands.AnchoredItem") B4/C1 -> 0`; `21@13231 setControlCommandCondition(self; self,listBoxName,"UILuaCommands.Selection") B4/C1 -> 0`; `24@13243 setCancelCondition(self; self,listBoxName) B3/C1 -> 0`; `28@13259 setVisibility(self; self,listBoxName,true) B4/C1 -> 0`; `32@13275 global tostring(no receiver; index) B2/C2 -> 1`; `37@13295 setVisibility(self; self,noContents,false) B4/C1 -> 0`; `40@13307 setCancelCondition(self; self,noContents) B3/C1 -> 0`; `45@13327 setControlProperty(self; self,noContents,"IsTabStop",true) B5/C1 -> 0`; `49@13343 setControlCommandCondition(self; self,listBoxName,"UILuaCommands.Previous") B4/C1 -> 0`; `53@13359 setControlCommandCondition(self; self,listBoxName,"UILuaCommands.Next") B4/C1 -> 0`. |
| `resetListBox` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1477-1522`) | `2@13765 getListBoxItemNum(self; self,index) B3/C2 -> 1`; `5@13777 getListPropertyName(self; self,index) B3/C2 -> 1`; `8@13789 getListBoxName(self; self,index) B3/C2 -> 1`; `12@13805 global tostring(no receiver; index) B2/C2 -> 1`; `17@13825 setVisibility(self; self,noContents,true) B4/C1 -> 0`; `30@13877 deleteListProperty(self; self,propertyName,currentCount) B4/C1 -> 0`; `34@13893 updateListProperty(self; self,propertyName) B3/C1 -> 0`. |
| `getPackageFromList` (`lua/scripts/widget/ask/retaineritemlistwidget.lua:1525-1542`) | No direct call. |

## Local method behavior

### List-property and display names

`getListPropertyName(self,listbox)` returns one string only for exact numeric
listbox values 1 through 6, 8, and 9. Values 1 through 6 map to
`TabItem_1_Maker` through `TabItem_6_Maker`; 8 maps to `SlotItem_Maker`; 9 maps
to `HelpCache_Maker`. Every other input reaches the zero-result return.

`getListBoxName(self,listbox)` returns one string for every normal path. Exact
values 1 through 6 map to `ListBox_TabItem_1` through `ListBox_TabItem_6`.
Every other input returns one empty string. This differs from the unsupported
path of `getListPropertyName`, which returns zero values.

`getSelectedTab(self)` requests
`getSelectedIndex(self,"TabControl_ItemList")` for one result. For an ordinary
numeric result it adds 1 and returns one result. Coercion and metamethod
behavior for other result types is outside the modeled domain.

`getPackageFromList(self,listbox)` returns one package value. Exact values map
as follows: 1 -> 1, 2 -> 100, 3 -> 8, 4 -> 5, and 5 -> 100. All other inputs
retain the default 1.

### Window and grid visibility

`updateWindowDisplay(self,focusFlag)` first requests
`setGridVisibility(self,8)`. When `self.work.isMateriaList` is truthy, it then
requests `setVisibility(self,"Grid_MateriaEquipList",true)` and
`setVisibility(self,"Grid_TabList",false)`. For listbox 1 it requests
`setVisibility(self,"Button_SortStatus",true)` and
`displaySortType(self,self.work.sorttype)`; all other listbox values request
`setVisibility(self,"Button_SortStatus",false)`. Exact Lua `focusFlag == true`
then requests `updateListFocus(self)`. It returns zero values on all normal
paths.

`setGridVisibility(self,listbox)` requests the following properties in order,
with zero results from every request:

1. `Grid_TabList = true`.
2. `Grid_ActorName = true`.
3. `Grid_Help = true` only for exact listbox values 1, 2, 4, 5, or 7.
4. `Grid_BackpackAndGil = true`.
5. `Grid_ItemNameBase = true` only for exact listbox values 6, 8, 9, or 10.
6. `Grid_ItemDetail1 = self.work.bonus1`.
7. `Grid_ItemDetail2 = self.work.bonus2`.
8. `Grid_ItemDetail3 = self.work.bonus3 or self.work.itemlife or
   self.work.bazaar`, using Lua truthiness.
9. `Label_ItemBonus5 = self.work.bonus3`.
10. `Grid_ItemLife = self.work.itemlife`.
11. `Grid_ItemBazaarInformation = self.work.bazaar`.
12. `Grid_MateriaAttachBazaarInformation = false`.

The work-derived visibility operands are passed through as their raw Lua
values; the code does not normalize `bonus1`, `bonus2`, `bonus3`, `itemlife`,
or `bazaar` to booleans before requesting visibility. `gridHelp` and `itemName`
are the separate equality-derived boolean operands, while `detail3` preserves
Lua's `or` result value.

The table reads and visibility requests are local Lua behavior. They do not
prove that a native control applied, rendered, or retained any value.

### Focus and filter conversion

`getListBoxItemNum(self,listbox)` open-calls
`getListPropertyName(self,listbox)`, then tailcalls `getListPropertyCount`
with the fixed receiver `self` followed by all live results from that open
getter. For unsupported listbox 7 the getter returns zero values, so the
count request receives exactly one argument, the receiver `self`; a one-nil
getter result would instead produce `self,nil`, and multiple getter results
would all propagate. The tailcall has open arguments and open results, so the
external count request's zero-result, one-nil, or other result width is
preserved.

`getListBoxFocusNum(self,listbox)` first requests
`getListBoxItemNum(self,listbox)` and `getListPropertyName(self,listbox)`, each
for one result. If the item count is exactly zero it returns four literal
zeroes. Otherwise it requests
`getControlProperty(self,propertyName,"FilteredCount")` for one result. It
captures the first `self.work.focus` read as `F1` for the returned local, then
performs an independent second `self.work.focus` read as `F2` for the guard
`FilteredCount < F2`. Only the local is clamped to `FilteredCount - 1`; when
the guard is false it retains `F1`. It then returns the fixed four-value tuple
`(FilteredCount, FilteredCount - 1, 0, clamped-or-F1)`. The numeric comparison
and subtraction use ordinary Lua numeric semantics; coercion and metamethod
behavior outside that domain were not modeled.

`focusToIndex(self,listbox,index)` resolves the property name and focus count,
each for one result. In short-circuit order, exact zero focus count, numeric
`index >= focusCount`, or numeric `index < 0` returns one literal `-1` and
requests no control update. Otherwise it requests
`setControlProperty(self,propertyName,"FilteredIndex",index)` with zero
results and tailcalls
`getControlProperty(self,propertyName,"Index")` with open results. The
tailcall therefore preserves zero results versus one nil and other result
widths.

`indexToFocus(self,listbox,index)` initializes a local result to `-1`, then
requests the property name, item count, and focus count, each for one result.
When `0 < focusCount`, it requests
`setControlProperty(self,propertyName,"Index",index)` with zero results and
then requests `getControlProperty(self,propertyName,"FilteredIndex")` for
one result, returning that one value. Otherwise it returns one literal `-1`.
The fixed one-result request pads an empty external result to one nil under
ordinary Lua call semantics. There is no restore-`Index` request after this
read.

The fixtures also pass two values through the open count tailcall and assert
that the enclosing fixed one-result `getListBoxItemNum` call retains only the
first value; the unsupported-listbox7 fixture asserts the exact receiver-only
prefix. Fixed padding/truncation is therefore kept separate from the open
tailcall widths.

### Empty-list display and list initialization

`updateListFocus(self)` obtains the four-value focus tuple from
`getListBoxFocusNum` and one listbox name from `getListBoxName`, then builds
`TextBlock_NoContents_` plus `tostring(self.work.listbox)`.

The helper arguments are captured while each CALL is assembled: the first
focus request receives the current `self.work.listbox`, and the listbox-name
request receives a separate current read. The `tostring` expression performs a
fresh `self.work.listbox` read. On the nonempty branch, the clamp reads
`self.work.focus`, then `focusToIndex` receives fresh `self.work.listbox` and
`self.work.focus` reads; the later control-property and focused-index requests
read `self.work.focus` again. The callback order is therefore
`focusToIndex`, `setControlProperty`, `setFocusedIndex`, `setWindowFocus`, and
`displayFocusedItemHelp` after the nonempty visibility/clamp work. These are
ordinary table reads and do not establish a native snapshot or callback
application.

When the first focus value is exactly zero, it closes one local editor when
`editWidgetOpen` is 2 (`closeBazaarEdit(self,1)`), 1
(`closeItemEdit(self,1)`), 3, or 4 (`closeItemShare(self,1)`). It then checks
exact `submenu == true`; if true, it requests
`getChildWidgetByWindowName(self,"ItemSubWidget")` for one result. A nonnil
child receives `hide(child)`, and only then does the code set
`self.work.submenu = false`. The branch requests
`setVisibility(self,noContents,true)`, writes `self.work.editWidgetOpen = 0`,
then requests `displayFocusedItemHelp(self)` and
`setWindowFocus(self,noContents)`. It returns zero values.

When the first focus value is nonzero, it requests
`setVisibility(self,noContents,false)`. If `self.work.focus > focusCount - 1`,
it writes `self.work.focus = focusCount - 1`. It then requests
`focusToIndex(self,self.work.listbox,self.work.focus)` for one result. A result
with `0 <= result` writes `self.work.index = result`; the branch then requests
`setControlProperty(self,listboxName,"SqwtFocusedIndex",self.work.focus)`,
`setFocusedIndex(self,listboxName,self.work.focus)`,
`setWindowFocus(self,listboxName)`, and
`displayFocusedItemHelp(self)`. It returns zero values. These writes and
requests do not prove applied native focus or rendered state.

`initListBox(self,index)` first requests `getListBoxName(self,index)` for one
result. The exact guard is `listBoxName ~= ""`; no separate nil test is
present. For a name passing that guard it requests, in order,
`setControlProperty(name,"IntData.Value0",index)`, the three
`setControlCommandCondition` calls for `UILuaCommands.MouseEnteredItem`,
`UILuaCommands.AnchoredItem`, and `UILuaCommands.Selection`,
`setCancelCondition(name)`, and
`setVisibility(name,true)`. It builds
`TextBlock_NoContents_` plus `tostring(index)`, then requests
`setVisibility(noContents,false)`, `setCancelCondition(noContents)`,
`setControlProperty(noContents,"IsTabStop",true)`, and the `Previous` and
`Next` command conditions on the listbox name, using the full literals
`UILuaCommands.Previous` and `UILuaCommands.Next`. For an empty string it
performs no later requests. It returns zero values.

`resetListBox(self,index)` requests the item count, list property name, listbox
name, and `tostring(index)` for one result each, then requests
`setVisibility(noContents,true)` for zero results. An exact zero item count
returns zero values before any deletion or list update. For a positive integer
count, the numeric loop decrements a local copy and requests
`deleteListProperty(self,propertyName,currentCount)` for indices `count - 1`
down through 0, then requests `updateListProperty(self,propertyName)`. It
returns zero values. Lua numeric-for coercion and metamethod outcomes outside
this modeled numeric domain are not inferred.

## Fixture evidence and limits

Additional controls reject numeric payloads encoded as booleans, integer
identity flags, wrong editor/focus arguments and writes, a non-strict outer
focus clamp, and a wrong child identity. These checks preserve numeric
integer/float equivalence and keep booleans distinct inside nested structures.

Focus/editor fixtures assert complete ordered receiver/argument vectors and
work writes with recursively typed scalar expectations and actual self/child
identity flags. The count-2/focus-1 boundary follows PCs 75, 76, 80 without
a focus assignment; it still requests the later index and focus operations.

The bounded original-word fixture set executed the admitted instructions
through `ChunkReader` and passed 54 cases, including the inner and outer
strict-LT equality boundaries and an ordinary visibility callback that
observes `submenu=false` after its assignment. It records literal recursive Lua-aware result
types, actual call prefixes and receivers, writes, paths, and nested
selected-helper calls. Cases cover mapped and unsupported list names,
empty and nonempty focus, editor and submenu guards, visibility filters,
tab/package mappings, zero versus one-nil/open result widths, filtered focus
clamping, index guards, list initialization, and reset loops. Checks record
the matched guard locations; the selected equality boundaries assert
their successors, and the callback case asserts the write/call interleaving.

Four in-memory negative controls failed as intended for a wrong init command,
wrong boolean tag, wrong receiver identity, and a non-strict focus boundary;
they did not modify the original payload or source.

The fixtures use ordinary tables without metamethods and explicit mock request
results. Unsupported coercion, metamethod comparison, callable values, and
native implementation remain explicit gaps. Requests and `SETTABLE` writes do
not prove applied control properties, storage/readback, rendering, focus
achievement, widget lifetime, historical ward/retainer/roster state,
transaction acceptance, inventory or currency mutation, server reply, or
settlement. ItemSelect, ItemUse, ordinary RetainerItemList, and
RetainerTrade behavior are not authorities for this Ask resource.

The existing Ask result and continuation remain unchanged: the published
`eventTalkRetainerItemList(2)` route consumes the Ask widget's four-value code
22 tuple and local selection delay
(`bazaar-retainer-client-contracts.md:563-608`). This list/focus contract
supplies only the local utility inputs, guards, requests, writes, and result
widths for the selected methods; resource membership and these conditional
compositions do not establish invocation of all thirteen utilities.

The delayed-submenu-store control failed when the visibility callback observed
`true` instead of `false`, despite the same eventual work values and
separately ordered call and write lists. This tests the ordinary mock
table execution and does not establish native setter application.
