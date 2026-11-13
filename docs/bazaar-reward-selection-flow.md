# Bazaar reward item selection

`BazaarEditWidget` has a local reward-item choice for parent editor modes
`2` and `3`. Its `Button_Extra` branch requests an `ItemSelectWidget` child
in child mode `400`. A changed, enabled child selection calls the parent's
`setReward(package,item)` before requesting child close. Cancel supplies
`setReward(nil,nil)`. These callbacks update editor state and display requests.
The separate [listing contract](bazaar-retainer-client-contracts.md#widget-callers-withdrawal-and-fulfillment)
owns submission, and [sale price modes](bazaar-price-modes.md) owns the price
and quantity formulas.

## Selected opening

The event method first requests its parent through `_getParentWidget()`.
It then returns zero values when a fresh `work.rewardWidgetOpen` read is
exactly true. This flag test applies whether the returned parent is nil or
nonnil. After the Cancel/Back and other button branches, the selected
`Button_Extra` arm requires:

- The control name is exactly `"Button_Extra"`.
- `work.extraIsDraw == false`.
- A fresh `work.mode == 2`, or a second fresh `work.mode == 3` read.
- `work.rewardIsItem == false`.

Nil and numeric zero do not satisfy these exact-false guards. Parent mode
`400` does not satisfy the `2/3` test. Each field read remains a separate
operation, including the two possible parent-mode reads.

Let `B` be this Bazaar editor. The calls below include the desktop receiver
as their first argument. Both retain exactly one result.

| Owner guard | `openChildWidget` arguments |
| --- | --- |
| Fresh `B.work.isRetainer == false` | `(desktopWidget,"ItemSelectWidget",B,true,true,400,B.work.chosenPackage,B.work.chosenItem)` |
| Every other value | The same tuple followed by `4` |

The chosen package and item are fresh reads for that call. An exact-true
opening result writes `B.work.rewardItemSelectReturn=0`. False, nil, zero,
and numeric one leave it unchanged. This branch does not reset the reward
package field or assign `rewardWidgetOpen=true`; its normal return is one
true value. A returned opening result is not proof that a child was created.

The [ItemSelectWidget contract](item-select-widget-contract.md) owns its
initializer and local list behavior. Under that initializer contract, the
second true is the modal input, `400` is the child mode, and nonnil selected
package/item inputs seed the child's reward-reference fields. The optional `4`
selects its retainer path. The first true and the association between the
supplied parent and a later `_getParentWidget()` result remain opening-helper
boundaries. No native factory, instance construction, or dynamic method
binding is established here.

Source: `widget/bazaareditwidget.lua:2051-2071,2940-3005` below
`lua/scripts/`. Original prototype `0.10` has code start `13389`.
The entry flag comparison is PC `8`; selected guards are PCs
`791,795,799,803,807,811`. Opening calls are PC `824`, offset `16685`,
`CALL B=9,C=2`, and PC `842`, offset `16757`, `CALL B=10,C=2`.
The result comparisons and writes are PCs `825/828` and `843/846`.

### Player inventory entry

The standard `widget/ItemSubWidget.form` line 15 gives `Button_BazaarBuy`
`UILuaCommands.Operate`. `ItemSubWidget.initForm` (`root/proto1` PCs 6-8)
registers it through `setButtonEvents`, which reads the Button's `Command`
and requests its condition (`root/proto2` PCs 0-8). In `ItemListWidget`, the
ordinary package-1 menu branch gives this control state 2 when the chosen
item's `_isEquipping`, `isRareItem` and `isExclusiveItem` each return false
(`root/proto60` PCs 104-131, 346-349). The submenu interprets 2 as visible
and enabled (`root/proto4` PCs 25-34). This is one admitted item shape.

The submenu's `processUICommandOperate` (`root/proto5` PCs 22-29) calls its
parent `operateBazaarBuy` and requests submenu close when the result equals
true. `ItemListWidget.operateBazaarBuy` (`root/proto47` PCs 3-16) opens
`BazaarEditWidget` under itself with operands `(true,true,2,package,item,nil,self)`
after the parent. An exact true writes `editWidgetOpen=2` and `lastsub=3`
(PCs 18-23). The editor declares `Button_Extra` with `UILuaCommands.Operate`
in `widget/BazaarEditWidget.form` line 239. Its init registers the control
(`root/proto0` PCs 150-152), and mode 2 initialization requests title 3127
and extra-button content 3124 (`root/proto1` PCs 647-663). The mode-400
child then follows the selected opening above. The shared
[widget-open helper](content-director-ui-contracts.md#commandcreatewidget-forwarding)
qualifies the command request and owner operands.

### Seek Item source validation

`BazaarEditWidget.setInitialData` (`root/proto1` PC 60) reads the selected
package and one-based slot from `MyPlayer._getItem` for the ordinary owner.
PCs 116-149 set `work.error` when the source is nil, source liveness is
exact false, the supplied parent is nil, parent liveness is exact false,
or the parent's `checkChosenItem(item)` returns exact false. That call
supplies the item alone. The latter refusal reaches the epilogue before
mode-2 presentation requests.

`ItemListWidget.checkChosenItem` (`root/proto70`) requires its chosen
package to match the active list at PC 22 and its chosen slot to match
`work.index + 1` at PC 31. PC 43 rereads the chosen item, and PC 44 compares
the resulting Lua value with the supplied item. The [held NormalItem return](https://github.com/XIVLegacy/xivl-client-structs/blob/62c7d759e6e2b7231f012112f3fe5d3e75a6446f/docs/item-native-contract.md#held-normalitem-table-identity)
can reuse an admitted Lua table by record identity. The successful comparison
returns true at PCs 46-47.

When the admitted first show finds `work.error` exact true, the editor
hides `Grid_Base` and requests close. The ordinary parent path records
operation 1 and calls `closeBazaarEdit` with the optional argument omitted
(`BazaarEditWidget` `root/proto2` PCs 9-36). The parent clears the open and
operation state before resolving the child (`ItemListWidget` `root/proto64`
PCs 0-19). The separate matching package-update route sets `closeok`
(`root/proto62` PCs 60-77), and the list focus update may consume it by
calling `closeBazaarEdit(true)` (`root/proto16` PCs 20-47). These script
requests establish conditional branches. Native close completion and its
frame remain unverified.

### Standard mode-2 Bazaar editor

The authenticated `BazaarEditWidget.form` merges `common/COMBasisLabel.tpl`
at line 5. `Grid_Unit` starts Collapsed at line 90 and contains
`ComboBox_Select`, with its selected ComboBox template and initial text
row 3116 at line 91. Its only item children, `ComboBoxItem_1` and
`ComboBoxItem_2` at lines 92-93, supply content rows 3102 and 3103,
Stretch content alignment, and select `ControlTemplate_ComboBoxItem`.
Neither item supplies a local visibility, trigger, or input binding.

The selected ComboBoxItem template at `COMBasisLabel.tpl` lines 30-35
has one direct setter, `IsTabStop=False`, and one visual root. The root
is `Button_XXX` with left content alignment, retail style
`BTN_basis_listboxSelect`, margin zero, minimum height 20 and minimum
width 100. Its sole child is an unnamed Binding element with Path
`Content`, mode OneWay and RelativeSource TemplatedParent. The XML
provides no explicit binding target property. This selected item
has no event or command trigger. Admission of this resource can
preserve that exact structure while the ancestor is hidden. The
default target of the child Binding and expanded-dropdown interaction
remain outside this static declaration contract.

The separate ComboBox template at lines 2-29 declares SelectionChanged
with `UILuaCommands.SelectComboBoxItem` and sound 3, and an Operate
command trigger with `ComboBox.OpenDropDown` and sound 3. Its two
ToggleButtons and Popup bind to IsDropDownOpen. The label reads the
ComboBox Text property and has an OpenDropDown mouse binding. The Popup
has a CloseDropDown Escape binding. The nested ListBox selects
`Style_ListBox_Commands`, whose Cancel trigger requests CloseDropDown
with sound 1 at lines 36-43. The Popup PlacementTarget attribute is
missing the final outer Binding brace in the decoded asset. These are
separate owners from the selected ComboBoxItem.

`BazaarEditWidget.init` registers `UILuaCommands.SelectComboBoxItem` on
`ComboBox_Select` (`root/proto0` PCs 172-175) through the common priority-5
helper (`widgetbaseclass_common` `root/proto55` PCs 0-4). The matching
handler needs that exact command, sender and `work.mode == 1`
(`root/proto10` PCs 52-59). Mode 2 keeps the ComboBox ancestor hidden
regardless of the popup's state.

| Mode-2 initialization requests | `BazaarEditWidget.setInitialData` `root/proto1` |
| --- | --- |
| Show `Grid_Price` and `Grid_RewardTitle`. Hide `Grid_Unit`, `TextBlock_OpenBlacket`, `Grid_NumberInput_Gil` and `Grid_Tax`. | PCs 601-632 |
| Source package 8 writes error true and returns false. For other packages show `Label_NumberInput_ItemSource` and hide `TextBlock_ItemStack_ItemSource`. | PCs 633-646 |
| Set title 3127 and `Button_Extra` content 3124. | PCs 647-663 |
| Hide `Grid_RewardItemName` and `Grid_ItemStack`. Show `Grid_NumberInput_TotalGil`, `Label_NumberInput_3` and `CustomControl_NumberInput_TotalGil`. Hide `TextBlock_NumberInput_TotalGil`. | PCs 678-701 |

Earlier PCs 355-367 show the source-count ancestor `Grid_ItemSourceStack`
when `work.bakstackable` differs from exact false, and hide it otherwise.
The package-8 error path can hide `Grid_Base` and request close from
`processBeforeShow` on the admitted first-show/error branch (`root/proto2`
PCs 0-9 and 35-41). The ordinary mode-2 presentation and `Button_Extra`
entry require the non-error path. No mode-2 ComboBox event is required
by these selected paths.

The installed `common/COMBasisLabel.tpl` is 3612 bytes, SHA-256
`06fceb84b53604b04a8c5f66c6e6899f425389d003795ddf9079081b9d940e83`.
The decoded member is 3604 bytes, SHA-256
`88dc2e1de05802b80c478a2c0faacc3630fe14059e607855a4512cab22857a0b`.
The form and dictionary matched a basename Blowfish round trip and
namespace-aware XML parse. The BazaarEditWidget and common base LPBs
matched their coverage manifest entries before instruction inspection.
Live native attachment, event delivery and paint remain unverified.

#### ComboBox help and comment field

`ComboBox_Select` at form line 91 declares Help.Type 1 and Help.Value0
`@75345`. These are its only Help fields. Neither ComboBoxItem child at
lines 92-93 declares a Help field. Mode 2 requests `Grid_Unit` Collapsed
at `root/proto1` PC 612. The selected mode-2 script does not read or
write the ComboBox's Help fields.

The only TextBox is `TextBox_BazaarComment` at line 228, a direct child
of `Grid_BazaarComment` (line 221). It declares TextWrapping Wrap,
MaxLines 3, CaretIndex 0, CharacterCasing Normal, and retail style
`TEB_basis_input`, with height 52 and minimum width 480. The declaration
supplies no MaxLength, IsReadOnly, IsEnabled, Focusable, IsTabStop,
AcceptsReturn, AcceptsTab, input binding or local Visibility. The parent
starts Collapsed. Neither name occurs in the BazaarEditWidget LPB, and
the selected mode-2 path leaves the comment grid collapsed. Runtime
TextBox defaults and editing behavior remain unverified.

#### Polish badges in the standard form

Two direct IconControls use icon 800 and bind Visibility with XPath
`@polmax`, OneWay. The declarations have no Path, explicit Source,
ElementName, RelativeSource or converter. `IconControl_PolishMAX` is at
form line 74 under the anonymous Grid at line 65, inside `Grid_ItemName`
(line 53) and `Grid_ItemSource` (line 43). That ancestry remains present
on the ordinary mode-2 path. `IconControl_PolishMAX_2` is at line 135
under the anonymous Grid at line 126, inside `Grid_RewardItemName`
(line 114). Mode 2 requests that ancestor Collapsed at `root/proto1`
PC 681. The form and its three direct dictionaries declare no
DataContext or XmlDataSource.

`BazaarEditWidget.setInitialData` writes the first icon's visibility
through `setVisibility` (`root/proto1` PCs 184-223). Its operand is the
Lua conjunction of the local equipment-fitness test, ownership of any
of catalogs 2001001, 2001002 and 2001003 in package 101, and the selected
item's `getMaterializePermission` result. The fitness flag requires
truthy `isEquipment` and `getNormalItemFitness` equal to 10000. A
nonnil reward-selection callback requests `Grid_RewardItemName` Visible
(`setReward` `root/proto17` PCs 24-27) and writes the second icon's
visibility from the corresponding tests on the selected reward item
(PCs 134-173). Common `setVisibility` and `setItemVisibility`
(`root/proto79` PC 4 and `root/proto80` PCs 0-10) use Visible for exact
true and Collapsed otherwise. The selected LPB has no `polmax` or
DataContext literal. The [direct ShopEdit carrier](https://github.com/XIVLegacy/xivl-decomp/blob/c9c0088e5d3b412b3b0ae1f427f7494bdf573f7e/docs/resource/sqwt-xpath-data-sources.md#separate-quantity-window)
records the native source-less binding path under a null DataContext.
The Bazaar declarations and direct requests leave the live DataContext
and the order of binding evaluation and direct writes unverified.

### Standard selector carrier

`ItemSelectWidget.getFormName` (`root/proto0` PCs 0-1) selects
`widget/SubItemListWidget.form`. The standard form merges
`widget/ItemListWidget.tpl`, `common/WINBasis_noGrayout.tpl` and
`common/LABBasisNumberInputBox.tpl` at lines 21-23, and selects
`ControlTemplate_Window_WINBasis` at line 28. The form's first tab uses
`TabItem_1_Maker` at line 7 and `ListBox_TabItem_1` at line 72, with
XPath `/TabItem_1`, `DataTemplate_ItemList`, `ControlTemplate_ListBox`, and
height 200. Mode 400 chooses listbox 1 and tab index 0 (`root/proto2`
PCs 151-176). This list maps to player package 1 on the non-retainer path.

The shared list template turns its `Selection` event into
`UILuaCommands.Selection` with `SelectedIndex` and `IntData.Value0` in that
order (lines 75-76). `ItemSelectWidget.initListBox` writes the tab number to
that second property and registers Selection and Cancel (`root/proto19`
PCs 5-24). Its nonempty focus branch writes `SqwtFocusedIndex` and requests
window focus on the list (`root/proto7` PCs 66-79). The shared dispatcher
rereads the sender's `SelectedIndex` and suppresses a negative index
(`widgetbaseclass_common` `root/proto13` PCs 41-55). The child maps the
resulting filtered row through its source index to a one-based item slot.
The [ListBox Operate path](reward-widget-result-contracts.md#rewardselectwidget-opening-and-keyboard-selection)
records the native Selection producer for an admitted row.

The child registers Cancel and Close on the root, and Cancel on the list
and `Button_Back` (`root/proto5` PCs 0-3 and 17-22, `root/proto19`
PCs 22-24). The Back button at form line 448 also declares Operate, whose
receiver calls `previousSequence` after the update-counter guard
(`root/proto30` PCs 0-16, 30-33). Cancel reaches the separate timer-clear
path below. Native focus admission, visible pixels and child teardown
remain conditional.

### Selector command operands and window name

For the ordinary Inventory parent, `openChildWidget` forwards widget index 3,
a nil window-name override, the Bazaar editor as parent, and visible true
(`desktopwidget_connector` `root/proto536` PCs 0-9). The local opener replaces
the nil override with `ItemSelectWidget`. At `root/proto522` PC 32 it requests
`commandCreateWidget(D,"ItemSelectWidget",false,B,E,"ItemSelectWidget",3,true,true,400,package,slot)`.
D is Desktop and B is the editor. E defaults to true. If the first
`B:isShow()` returns exact true and B compares unequal to D, E is the first
unadjusted `B:getInputEnable()` result. The two `ItemSelectWidget` values
occupy the command path and window-name positions respectively.

The [player request](player-widget-command-request.md) consumes the false
force and forwards the complete tail to `_executeCommand`. The selected
WidgetOpenCommand class overrides the request name to `widgetCreate` in
`CharaBaseClass.getCommandName` (`root/proto17` PCs 67-80). On admitted
[command delivery](widget-open-command-boundary.md#command-formal-frame-and-factory-tail),
the factory request is
`_createActor(nil,"ItemSelectWidget",false,B,E,"ItemSelectWidget",3,true,true,400,package,slot)`.
The last native joins require the selected callback and value conversions.

The child loads `SubItemListWidget.form` and requests the root name
`Window_ItemSelectWidget` (`widgetbaseclass_common` `root/proto0` PCs 26-58).
The declared root name is `Window_SubItemListWidget` at form line 1. On the
admitted base initializer path the child `init` receives `(true,400,package,slot)`
after its receiver (`widgetbaseclass` `root/proto0` PCs 83-98). The omitted
retainer operand becomes nil in the initializer. The selector's Cancel
callback asks only to close the child. No parent input or keyboard-focus
request occurs in its nil-reward callback. The separate creation callback can
request parent `setInputEnable(E)` before testing child visibility
(`desktopwidget_connector` `root/proto532` PCs 0-8). The native ordering of
that request and the opener's input-disable request remains unverified.

### First bag data owner

The ordinary selector reads MyPlayer capacities for packages 1 and 100
(`ItemSelectWidget` `root/proto1` PCs 234-246). The first-bag build supplies
listbox 1, a compacted row index, package 1, a one-based slot and owner 1 to
`setItemToXmlLight` (`root/proto26` PCs 73-89). `root/proto22` PC 24 reads
`MyPlayer._getItem(1,slot)`. A nil item skips the slot without advancing the
row index. The named data owner is `TabItem_1_Maker`, declared at form line 7.
The visual `ListBox_TabItem_1` at line 72 binds to its `/TabItem_1` node.
`focusToIndex` writes `FilteredIndex` and reads `Index` on the maker
(`root/proto17` PCs 13-21). On the nonempty focus path, focused-item help
rereads the slot and can reach an item method call with no nil test
(`root/proto28` PCs 38-104). The ordinary empty list uses the separate empty
control and Back focus path (`root/proto7` PCs 14-38).

### Inventory ownership and keyboard cancellation

`MainMenuWidget` row 4 calls `setBazaarActor` and opens
`openMainMenuRootWidget("ItemListWidget",self,true)` (`root/proto1`
PCs 38-48). The Desktop connector inserts category index 3
(`root/proto538` PCs 9-15) and checks that root slot before opening
(`root/proto535` PCs 4-18). On the admitted creation callback,
`processWidgetCreated` can publish the inventory in empty
`work.rootWidget[3]` (`root/proto532` PCs 17-27). The inventory's
`initForm` precreates a retained ItemSubWidget child with
`initChildWidget("ItemSubWidget",false,true)` (`root/proto1`
PCs 61-65). The normal inventory selection handler needs a result
other than exact false from Desktop `checkKeyboardFocused(self)`.
An admitted selected row supplies chosen package and source index plus
one, then requests `openSubWidget` (`root/proto10` PCs 10-21 and 59-75).

`openSubWidget` finds that child by window name (`root/proto60` PCs 0-4),
requests the row-dependent button states, and calls `setModal(true)` and
`show()` (PCs 398-402). It requests focus on `Button_BazaarBuy` when
`work.lastsub == 3` and that button's state is 2 (PCs 423-431).
Other admitted saved actions have separate focus arms. The fallback
requests `Button_Cancel` at PCs 543-545. The standard submenu Window
at form line 1 declares directional navigation Cycle. Its
`StackPanel_ButtonPanel` holds `Button_BazaarBuy` at line 15 and
`Button_Cancel` at line 27. The exact first directional focus result
is conditional on the row-dependent visible and enabled controls.

The editor and selector both use `openChildWidget`
(`desktopwidget_connector` `root/proto536` PCs 0-9), which takes the
supplied parent's `getWidgetIndex()` and tail-forwards that index and
parent to `openWidget`. This gives the parent chain ItemListWidget,
BazaarEditWidget, ItemSelectWidget. ItemSubWidget is a separate child
of the inventory. Its admitted Seek operation requests that submenu
hidden after the editor open returns true. Both later children inherit
index 3 for the ordinary Main Menu path. The supplied parent bypasses
the nil-parent slot-occupancy rejection (`root/proto523` PCs 20-28).
An existing live inventory remains the root. On an exact-true creation
request, `openWidgetLocal` may disable a shown parent's input without
hiding it (`root/proto522` PCs 33-43). The admitted child creation
callback can show a child with a true visible flag (`root/proto532`
PCs 28-60). These are requests for nested separate windows. Paint
order, exact overlap and native focus handoff remain unverified.

With the default Layout0 bindings, [Enter and Escape](https://github.com/XIVLegacy/xivl-decomp/blob/77084a4baa020f0777d58df84e1d783d66f201d0/docs/script/main-menu-command-route.md#key-bindings)
include no-parameter `ApplicationCommands.Operate` and
`UILuaCommands.Cancel` at rows 11 and 20 respectively. The
[Button Operate path](https://github.com/XIVLegacy/xivl-decomp/blob/77084a4baa020f0777d58df84e1d783d66f201d0/docs/script/main-menu-command-route.md#decide-and-chat-input)
raises Click on an admitted Button at `0x0097EE90`. The Click handler
runs the declared `UILuaCommands.Operate` on `Button_BazaarBuy` or
`Button_Extra` when the respective control receives Enter. The editor
form declares `Button_Extra` at line 239 and `init` registers its
confirm condition at `root/proto0` PCs 150-152. The editor's mode-2
initialization does not request initial focus on `Button_Extra`.
Default focus and a fixed number of arrow presses remain unverified.

The mode-400 selector's nonempty-list branch requests the filtered
focus and the selected list at `root/proto7` PCs 66-81. Its
`setWindowFocus` requests logical focus and requests keyboard focus
only if Desktop's current keyboard-focused widget compares equal to
self (`root/proto9` PCs 4-14). Cancel subscriptions include the root,
active list, first tab, and Back. They use priority 5 through
`widgetbaseclass_common` `root/proto58` PCs 0-7. On admitted delivery,
the inherited dispatcher calls `processUICommandCancel`
(`root/proto13` PCs 21-28). The selector clears its timer and requests
`previousSequence` (`root/proto31` PCs 0-4), then the mode-400 branch
requests `closeWidget` (`root/proto29` PCs 14-21). The latter calls
`setReward(nil,nil)` on the nonnil current Bazaar parent and passes the
selector itself to `closeWidgetDirect` (`root/proto41` PCs 0-14).
The request does not close the editor or inventory. On the admitted
finalize callback, Desktop clears an indexed root only if it is dead or
compares equal to the deleted widget (`root/proto534` PCs 0-25). A live
inventory root therefore survives deletion of its selector child. The
native completion time and parent input restoration remain separate.

## Child selection and cancellation

The complete child eligibility, focus, update-counter, and opacity rules
remain in [ItemSelectWidget](item-select-widget-contract.md). In particular,
`isOperateButtonEnable` must return exact true before the selection path
continues. It rejects a nil fetched item, exact-true equipped/exclusive
tests, unsupported packages, and the selected reward's exact opacity string
`"0.5"`. It does not establish authoritative owner availability.

After eligibility, the child saves its sort type and freshly requests its
parent before testing mode `400`. An exact match between its selected
package/item and its seeded reward-reference pair returns without a reward
callback or close request. Otherwise it requests the selected border,
calls `parent.setReward(parent,chosenPackage,chosenItem)`, and requests
`desktopWidget.closeWidgetDirect(desktopWidget,child)`.
The callback's results are discarded, including an explicit false result.
The close request follows a normally returning callback; an error does not
establish that continuation. A nil parent has no protective guard in this
changed-selection arm.

Cancel and Close both request `setCommonTimer(nil)` and `previousSequence()`.
In mode `400`, that continuation calls the child's `closeWidget()` and
returns true. Reward-mode `closeWidget()` freshly requests its parent.
Only a nonnil parent receives `setReward(nil,nil)` followed by the direct
child-close request. A nil parent receives neither request. The nil tuple
therefore denotes cancellation of this choice, rather than a zero-valued
item selection.

These are calls through self, desktop, and returned-parent objects. Their
composition with `B.setReward` is conditional on those bindings and on the
returned parent being the supplied Bazaar editor. Inherited methods are
call boundaries, not independently established implementations.

Source: `widget/itemselectwidget.lua:2575-2682,2685-2696,2699-2857,3297-3320`.
The selection's prototype `0.33` requests its parent at PC `74`, offset
`21188`, calls `setReward` at PC `101`, offset `21296`, and requests direct
close at PC `105`, offset `21312`. Callback `B=4,C=1` and close `B=3,C=1`
discard all results. Reward-mode close prototype `0.41` requests its parent
at PC `5`, calls `setReward(nil,nil)` at PC `10`, and requests close at
PC `14`, offsets `25570,25590,25606`.

## Bazaar callback and local counts

`BazaarEditWidget.setReward(package,item)` tests only whether package is
nonnil before entering its selection-update body. False and zero packages
enter that body. It does not independently validate the item argument.

For a nonnil package it first writes `rewardItemPackageSelectReturn` and
`rewardItemSelectReturn`. It requests the item-reward button/title/help
presentation, shows `Grid_RewardItemName`, hides `Grid_NumberInput_TotalGil`,
and sets `rewardIsItem=true` before resolving the selected item.
It freshly obtains the player, then chooses its lookup as follows:

| Fresh callback owner guard | Local lookup and result use |
| --- | --- |
| `work.isRetainer == true` | `desktopWidget.getRetainerItem(package,item)`, one result. Nil returns false immediately; otherwise catalog, icon, stackability and stack count are read from this item. |
| Every other value | `desktopWidget.getPlayerItemInPackage(package,item)`, exactly four metadata results, then a separate `player._getItem(package,item)` read. There is no corresponding nil-item early return. |

The callback's exact-true owner test differs from the creator's exact-false
test. Nil or numeric zero therefore selects the retainer opening tuple but
the player callback lookup. No consistency or availability check bridges
these independent reads.

For exact-true stackability, the callback requests the reward count control
as `(current=1,min=1,max=stackCount)`. If `isItemCrystal(catalog)` returns
exact true and the count exceeds `999`, only that maximum is capped to
`999`. The other stackability values request `(1,1,1)` and write
`work.stack=1`. The stackable path does not make that `work.stack` write.
It then requests equipment/materia indicators, calls `displayPrice()`,
reads the selected item's name index, and requests item icon/name display.
The helper's price calculations remain outside this callback contract.

| Callback outcome | Local result |
| --- | --- |
| Package nil, including child cancellation | Skips selection writes, lookups, and display calls. Writes `rewardWidgetOpen=false` and returns true. Existing reward fields and `rewardIsItem` remain unchanged. |
| Nonnil package, lookup/display path completes normally | Writes `rewardWidgetOpen=false` and returns true after the updates above. |
| Retainer lookup returns nil | Returns false after the earlier reward writes and presentation requests. Does not clear `rewardWidgetOpen`. The child still requests close after this normal false return. |

A nil player item can reach an unguarded item-method call. Opaque helper or
receiver failures can interrupt the remaining display and flag updates.
No rollback or retry is established.

Source: `widget/bazaareditwidget.lua:3549-3872`, prototype `0.17`, code
start `21697`. The nil-package comparison is PC `0`; selection writes are
PCs `3/5`, `rewardIsItem=true` is PC `33`, and the exact-true owner test is
PC `40`. Retainer lookup/nil-test/false-return are PCs `46/48/51`.
Player metadata and object lookups are PCs `69/77`. Count requests are
PCs `103/133`; the nonstackable `stack=1` write is PC `123`.
The final flag write and true return are PCs `267/269`.

## Evidence identity and limits

The standard Sqwt resources were decrypted by basename Blowfish and parsed
as XML. Line numbers refer to the complete decoded documents.

| Client-relative resource | Bytes | SHA-256 |
| --- | ---: | --- |
| `client/sqwt/widget/ItemSubWidget.form` | 4331 | `39f34b32d9fdeb1aa1d83cc3cc6085446f33a07b806ae9e0d5419a4ab4c017f1` |
| `client/sqwt/widget/BazaarEditWidget.form` | 20047 | `2e51fc3bd2a2caa86293acca9f896afa413734ff4cec8f33e6c17ed1e90f4d92` |
| `client/sqwt/widget/SubItemListWidget.form` | 44072 | `b2de27032e31b5266f9ddf593005630387a456257b8ec4bf0851c8881bf56c38` |
| `client/sqwt/widget/ItemListWidget.tpl` | 16943 | `ba8b86dbf36558e6086721524833d17528be08b11bf72c062d0b76fd318de7d5` |

The installed `widget/itemsubwidget.lua`, `widget/itemlistwidget.lua` and
`widget/widgetbaseclass_common.lua` LPBs and decoded payloads match their
entries in [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).

Extraction: retail 1.23b, `2012.09.19.0001`. Canonical decoded members were
authenticated in memory against [`manifests/scripts.json`](../manifests/scripts.json).
Installed LPBs and decoded payloads matched the selected `matched-script`
entries in [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
`ItemSelectWidget` identities are pinned in its
[local contract](item-select-widget-contract.md#identity-pins-and-metadata-citations).

| BazaarEditWidget artifact | Identity |
| --- | --- |
| Canonical `widget/bazaareditwidget.lua` | 110132 bytes; SHA-256 `13d066fe61bdf0d2a387fca7e221ba4fa2ce60dc3be0f9ca0a5c5b10fd6c9370` |
| Resource `client/script/n1635q/89k99s561qn1635q.le.lpb` | SHA-256 `5ad478c18b05eda1d1be6869383666b05227769a45814aa079cf7b827bae7798` |
| Decoded Lua 5.1 payload | SHA-256 `083f7cfea5a479cb882d6315cdcc4738996b23de82a161de5c0b55ae03161ac8` |

Instruction locators use zero-based prototype children and PCs, with byte
offsets in the decoded payload. The inspection used
`tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader,instruction,states_for,call_record`.
Synthetic execution with supplied bindings checked the selected creator and
callback predicates, raw nil/false/zero distinctions, fresh reads, result
widths, and update order. Mutations of owner guards, opening-result tests,
nil selection, final flag clearing, and the crystal cap were independently
rejected. These checks establish static contract consistency, not retail
execution.

These operations establish a local choice and display contract. They do not
establish a listing submission or reward grant.
Native child creation/close, runtime parent identity, inherited or dynamic
method binding, work readback/metamethod behavior, historical UI invocation,
authoritative inventory availability, server acceptance, reward transfer,
and settlement remain unestablished.
