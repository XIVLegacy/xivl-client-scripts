# Bazaar order-item selection

`BazaarListWidget.operateBazaarBuy()` requests an `ItemSelectWidget` child
in child mode `440`. An enabled child selection calls the returned parent's
`setOrderItemData(2,package,item,orderStack)`, then calls its
`closeOrderItem()`. Cancellation supplies `(1,0,0)` instead. The selected
parent callback can request `executeBazaarSell`; its result controls local
state and does not establish accepted fulfillment or settlement.

The [ItemSelectWidget contract](item-select-widget-contract.md) owns the
child's initializer, filtering and eligibility. The separate
[Bazaar reward choice](bazaar-reward-selection-flow.md) uses child mode
`400`. The existing [Bazaar command contract](bazaar-retainer-client-contracts.md#widget-callers-withdrawal-and-fulfillment)
owns `executeBazaarSell` beyond this call, and
[sale price modes](bazaar-price-modes.md) owns the priced-sale formulas.

## Selected creator

Let `B` be the Bazaar list widget and `D` the desktop receiver.
`operateBazaarBuy()` has no entry guard in its own body. It freshly reads
the chosen package and item and calls:

`openChildWidget(D,"ItemSelectWidget",B,true,true,440,B.work.chosenPackage,B.work.chosenItem,2)`.

The call retains exactly one result. Only an exact-true result writes
`B.work.editWidgetOpen=5`; false, nil, zero and numeric one leave that field
unchanged. The method returns the retained result as one value. The call
does not prove that a child was created, and this method establishes no
actual UI dispatch into itself.

Under the selected initializer contract, the second true is the modal
input, `440` is the child mode, and the package/item arguments feed
`getBazaarItem(package,item)`. A nonnil result supplies the child's catalog,
stack, quality and proper-package restrictions. The initializer selects
list 2 only for proper package `100`, otherwise list 1. Its list rows hide
catalog or quality mismatches and stacks smaller than `orderStack`.
This is a local filter, not authoritative availability. The final `2`
does not satisfy the initializer's exact `4` retainer selector. It does not
establish another owner role. Parent mode and child mode remain separate.
The first true and initializer dispatch remain opening-helper boundaries.

Source: `widget/bazaarlistwidget.lua:4812-4837` below `lua/scripts/`.
Prototype `0.52`, code start `35245`, opens at PC `13`, offset `35297`,
`CALL B=10,C=2`. Its exact-true comparison, state write and one-value
return are PCs `15,18,19`.

## Child callback and cancellation

The child selection path requires the published update, focus and exact-true
`isOperateButtonEnable` guards. After those guards it calls `saveSortType()`
and freshly requests `_getParentWidget()` before testing its mode. In mode
`440`, only `work.chosenOperation == 0` continues. It then requests the
selected border, calls the returned parent's
`setOrderItemData(parent,2,chosenPackage,chosenItem,orderStack)`, writes its
own `chosenOperation=2`, and calls `closeOrderItem(parent)` with no further
argument. Package, item and count are fresh child work reads for the callback.
Both parent calls discard every result. A normally returned false callback
therefore still permits the child write and close request. A callback error
does not establish that continuation. A nil parent has no protective guard
in this selected arm.

Cancel and Close both call `setCommonTimer(nil)`, then `previousSequence()`
and discard its results. That continuation can persist a changed sort type
before its mode test. In mode `440` it freshly requests the parent. A nil
parent returns one false value. A nonnil parent receives
`setOrderItemData(parent,1,0,0)`, whose results are discarded, followed by a
tail call to `closeOrderItem(parent)`. All close results are forwarded by
`previousSequence`, then discarded by the Cancel/Close wrapper. Cancellation
omits the count argument and uses numeric zeros rather than nil selections.

Source: `widget/itemselectwidget.lua:2575-2625,2671-2696,2699-2857`.
Prototype `0.33` saves sort at PC `72`, requests the parent at PC `74`,
tests child mode and operation at PCs `110/114`, calls the callback at PC
`130`, offset `21412`, writes child operation at PC `132`, and calls close
at PC `134`, offset `21428`. Callback `B=6,C=1` and close `B=2,C=1`
discard results. Prototype `0.29` requests the parent at PC `28`, calls
cancel callback at PC `35`, offset `19993`, `B=5,C=1`, and tail-calls close
at PC `37`, offset `20001`, `B=2,C=0`.

## Parent callback and local results

`B.setOrderItemData(operation,package,item)` has three fixed parameters
after self and is not variadic. The child's fourth operand, `orderStack`,
is consequently unused by this parent method. It first writes
`B.work.chosenOperation=operation`, then freshly reads that field. An exact
`1` returns zero values immediately. With ordinary field readback, the
child's cancellation takes that path, making no lookup or sell request.

Every other read value continues. It calls `getListPropertyName` with a
fresh `work.listbox`, retaining one result, then independently reads
`work.listbox` for `getListBoxFocusNum`, retaining only its first result.
Only an exact-zero focus result together with a fresh
`work.editWidgetOpen == 5` tail-forwards `closeOrderItem()` results.
Other combinations continue to the row-property lookups.

It requests `rewardpackage` and `rewarditem` separately from the retained
property name, with a fresh `work.index` for each call. Both results are
read before checking the package. No selected-row identity or snapshot
consistency check joins these reads to the creator's earlier package/item.

| Callback branch | Local effect and return |
| --- | --- |
| Row reward package is exactly `0` or false | Writes `chosenOperation=1`; returns one false value without a sell request. |
| Every other row package, including nil | Calls `executeBazaarSell(D,package,item,rowRewardPackage,rowRewardItem)`, retaining one result. No independent row-item validation occurs here. |
| Sell helper returns exact true | Writes `waitupdate=true`; returns one true value. |
| Sell helper returns any other value | Writes `chosenOperation=1`; returns one false value. |

The package/item in the sell call are the callback's supplied player-item
operands. The last pair comes from the parent's current row properties.
This method passes no count or price scalar. It does not clear an existing
`waitupdate` on its early or false-return paths.

Source: `widget/bazaarlistwidget.lua:5540-5609`, prototype `0.61`, code
start `40859`. Initial operation write/read test are PCs `1/4`. The
property/focus calls are PCs `10/14`; empty-focus close is TAILCALL PC
`22`, offset `40947`, `B=2,C=0`. Row reads are PCs `29/35`, package tests
PCs `36/38`, and sell call PC `50`, offset `41059`, `B=6,C=2`.
Exact-true test and wait write are PCs `51/54`; failure-operation write
is PC `59`. The cancellation return at PC `6` has zero results.

## Parent close and composed state

`B.closeOrderItem(argument)` first writes `editWidgetOpen=0` and
`chosenOperation=0`. Only a nil argument, including an omitted argument,
then calls `updateWindowDisplay(true)` followed by `selectedBorder()`.
False and numeric zero skip both calls. It next requests
`getChildWidgetByWindowName("ItemSelectWidget")`, retaining one result.
For any nonnil result it requests
`closeChildWidget(D,"ItemSelectWidget",B)` and discards the result.
The lookup result is a guard; it is not the close-call operand. Finally it
writes `closeok=false` and returns one true value, including when the lookup
returned nil. These are requests through runtime bindings, not proof of
native child lifetime or rendering.

When the returned child parent is `B` and these methods are the selected
bindings, both ordinary selection and cancellation call this close with an
omitted argument. Its reset overwrites the parent's earlier operation,
including the callback's normal-failure `1`. The child's separate
operation remains `2` after normal selection. An earlier `waitupdate=true`
survives this close. If the callback takes its empty-focus close path and
returns normally, the child still writes its operation and calls parent
close again. A close error can leave earlier resets or requests in
place and prevent the final flag write and true return. No rollback is
established.

Source: `widget/bazaarlistwidget.lua:5612-5645`, prototype `0.62`, code
start `41440`. Reset writes are PCs `1/3`; nil-argument test is PC `4`;
display/border calls are PCs `8/10`; child lookup/nil test are PCs `13/14`.
Close request is PC `20`, offset `41520`, `B=4,C=1`. The final flag write
and true return are PCs `22/24`.

## Evidence identity and limits

Extraction: retail 1.23b, `2012.09.19.0001`. Canonical decoded members were
authenticated in memory against [`manifests/scripts.json`](../manifests/scripts.json).
Installed LPBs and decoded payloads matched the selected `matched-script`
entries in [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
The [ItemSelectWidget identity](item-select-widget-contract.md#identity-pins-and-metadata-citations)
pins the selected child resource and payload.

| BazaarListWidget artifact | Identity |
| --- | --- |
| Canonical `widget/bazaarlistwidget.lua` | 131819 bytes; SHA-256 `f539b71353ee2860f535bc962ca2038ecf51bf99fdbeca314ed1eaa20bc39164` |
| Resource `client/script/n1635q/89k99sy1rqn1635q.le.lpb` | SHA-256 `8911334e4b425343fa491a3170c38fe6982449104eaea8f0c88860c97bd17a95` |
| Decoded Lua 5.1 payload | SHA-256 `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |

Prototype children and PCs are zero-based; offsets are bytes in the decoded
payload. The selected inspection used `tools/retail_script.py:decode_lpb`
and `tools/build_quest_contracts.py:ChunkReader,instruction,states_for,call_record`.
Original-call checks and synthetic execution with supplied bindings checked
the creator, callback, close and selected child continuations. Deliberate
mutations of exact guards, local state writes and result handling were
rejected. These checks establish static consistency, not retail execution.

Actual UI dispatch, dynamic method bindings, parent/widget/owner/item
identity, native creation and close, work storage/readback and metamethod
behavior, authoritative price or availability, listing acceptance, accepted
fulfillment, reward transfer, settlement and historical invocation remain
unestablished. This flow adds no command or wire binding from UI names.
