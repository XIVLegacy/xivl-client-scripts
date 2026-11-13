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
