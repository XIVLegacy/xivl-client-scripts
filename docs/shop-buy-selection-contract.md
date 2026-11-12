# ShopBuy purchase selection

`ShopBaseClass.selectShopBuy` returns exactly two values: the widget's current
row index plus one and its current purchase quantity. A widget cancellation
and a failed desktop selection both become `(0, 0)` at this caller, through
different branches. These are client UI results, not a completed purchase.

The [opening contract](gil-shop-widget-opening.md#opening-and-selection-boundaries)
owns actor inheritance, currency defaults, creation waits and list initialization.
Opening and purchase selection are separate operations.

## Evidence identity

This is static evidence from retail 1.23b extraction `2012.09.19.0001`.
The selected archive members matched [scripts.json](../manifests/scripts.json).
The containing archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). The corresponding
original LPBs and decoded Lua 5.1 payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Canonical source normalization replaces CRLF byte pairs with LF only.

| Decoded path under `lua/scripts/` | Canonical SHA-256 |
| --- | --- |
| `chara/npc/populace/shop/shopbaseclass.lua` | `483220C5E7914B2406FC8184B69448980E46004945A7315203406475E52A5C9F` |
| `widget/ask/shopbuywidget.lua` | `032B0C06D57300A810B9953DAD04BF794DEC096360944F4A3683CB2DC9797091` |
| `widget/shopeditwidget.lua` | `36DEC15BFAC5653B80BC2E00264757C6B8F72D60387EE035769ECFFE14072EA1` |
| `widget/desktopwidget_connector.lua` | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |

## Arguments, wait and result positions

`selectShopBuy` declares a receiver and one further parameter, but uses neither
as a selection operand. It calls the global desktop's
`selectEventModeWidgetYield` with only its receiver and `Ask/ShopBuyWidget`
(`shopbaseclass.lua:117-133`). It requests three results: desktop status, row
and quantity. Only status exactly equal to Boolean false replaces row and
quantity with numeric zeros. Nil, false and numeric zero are distinct values.

The desktop initializes the existing widget in slot 4: it calls
`resetBaseAskResult()`, calls `setAskParameter()` with no explicit operands,
then requests `show(true, true)` and returns that widget
(`desktopwidget_connector.lua:26310-26335`). Calls resolve dynamically on the
retrieved widget. `ShopBuyWidget.setAskParameter` itself takes only its receiver.
If `work.editWidgetOpen` is exactly zero, it returns immediately. Otherwise it
assigns zero to that field, assigns true to `work.askstatus`, and requests
`updateWindowDisplay(true)` (`shopbuywidget.lua:2660-2677`). The initial Ask
setup assigns `editWidgetOpen=0`, `index=0` and `askstatus=true`.

The selection wrapper waits through `selectWidgetYield`. A nil initialized
widget or a selection status exactly equal to false returns one false value.
Otherwise it returns true followed by all results of dynamic `getAskResult()`
(`desktopwidget_connector.lua:26241-26265`). For this pinned ShopBuy getter,
that is exactly `(true, row, quantity)`. The caller requests exactly three
values and returns exactly two. The [Ask base contract](ask-widget-result-state.md#selected-state-and-calls)
owns scalar result reset and completion polling. A finished poll alone does
not mean an accepted selection.

| Layer and condition | Returned values |
| --- | --- |
| ShopBuy getter reads base result exactly -1 | `(0, 0)` |
| ShopBuy getter reads any other base result | `(work.index + 1, work.buycount)` |
| Desktop fails initialization or selection | One Boolean false |
| Desktop completes and calls the pinned getter | `true` followed by its two values |
| `selectShopBuy` receives desktop status exactly false | `(0, 0)` |
| `selectShopBuy` receives another desktop status | Its second and third received values |

The getter reads the base result once. On the -1 branch it leaves
`work.askstatus` unchanged. Otherwise it first assigns false to that field,
then reads `work.index` and `work.buycount` for its return
(`shopbuywidget.lua:2636-2657`). It does not require a positive base result,
convert a catalog ID, or validate quantity. These are later field reads,
not an atomic snapshot recorded when a button was pressed.

## Row and quantity selection

After its child-open, wait-next, finished-Ask and keyboard-focus guards,
`processUICommandSelection` stores its fourth and fifth total arguments in
`work.focus` and `work.listbox`. It checks the list and focus, updates the
selected border and internal item fields, then calls `operateBuy`
(`shopbuywidget.lua:1823-1921`). `updateListFocus` assigns a nonnegative result
of `focusToIndex(listbox, focus)` to `work.index`. `focusToIndex` requests a
`FilteredIndex` control property and reads its `Index` property
(`:642-747,1075-1103`). The native property mapping is a boundary. The returned
`index + 1` is not established as an item catalog ID or as the visible filtered
focus plus one.

`operateBuy` reads the current row's catalog, mask and price data. A mask equal
to 1 requests a notification and returns false. Otherwise it requests a child
`ShopEditWidget` with this parent and mode 12. On an opening result exactly
true, it stores `editWidgetOpen=12` and `lastsub=8`
(`shopbuywidget.lua:2121-2203`). Failure to open the child does not itself set
the parent's Ask result.

The reached mode-12 branch of `ShopEditWidget.setInitialData` starts
`work.num1` at 1 and requests numeric-input setup with that value and its
computed local maximum. `NumberInputBox.ValueChanged` calls
`updateNumber` with the fifth total command argument. That method stores the
supplied value in `work.num1` only when the numeric control's
`IsKeyboardFocusWithin` read equals true. The Done callback sends that current
field to the dynamically retrieved parent as `setShopEditData(1, num1)`.
The parent stores the operation and quantity in `work.chosenOperation` and
`work.buycount` (`shopeditwidget.lua`, selected mode-12 initialization and
`:1368-1420,1422-1496`; `shopbuywidget.lua:2553-2561`). Native control bounds
and callback delivery are not demonstrated by these Lua assignments.

## Anchored row refresh

STATIC. ShopBuy's `processUICommandDefault` (`main/f31`, PCs 26-44)
handles `UILuaCommands.MouseEnteredItem` and `UILuaCommands.AnchoredItem`
after the same child, wait, Ask and keyboard-focus gates. A nil list,
nil focus or negative focus returns before the two work writes.
The admitted arm assigns `work.listbox` and `work.focus` and calls
`setCommonTimer` with the literal operand `0.2`. Its work writes
precede the timer call. The arm does not write `SqwtFocusedIndex`.

`processTimer` (`main/f32`, PCs 0-15) requests `focusToIndex` with
the current list and focus. It stores a nonnegative result in
`work.index`, sets `work.page` to zero and calls
`updateWindowDisplay(true)`. That method's exact-true arm
(`main/f5`, PCs 7-10) calls `updateListFocus`. Its named list
`SqwtFocusedIndex` write, update-count gate and native scroll gates
are in `xivl-decomp:docs/resource/sqwt-listbox-constructed-parts.md`,
ShopBuy first-tab focus requests. The command return and the bound
index write occur on separate call paths.

The PCs are zero-based instructions in the decoded ShopBuy chunk
identified in that study. They were checked with unluac 2025-12-23.
Live timer delivery and the frame of the property write remain open.

## Confirmation, cancellation and cleanup

| Input or call | Local consequence |
| --- | --- |
| Child Done | Sends operation 1 and current quantity to its retrieved parent, then calls that parent's `closeShopEdit()` with the optional operand omitted. |
| Child Back through Operate or Cancel | Sends operation 2 and current quantity, then makes the same omitted-operand close call. It leaves the parent Ask unfinished. |
| Child Cancel with another control name | Requests focus on `Button_Back`. It does not immediately cancel the parent selection. |
| Parent UI Cancel | Returns false without cancellation when the child-open flag differs from zero, `waitNext` equals true, or `isAskFinish()` returns true. Otherwise it calls `previousSequence()`. |
| Parent UI Close | Calls `previousSequence()` without those Cancel guards. |
| `previousSequence()` | Requests `setBaseAskResult(-1)`. |
| Explicit `ShopBaseClass.closeShopBuy` | Calls desktop `closeEventModeWidget("Ask/ShopBuyWidget")`, ignores its declared extra parameter and returns no values. |

The child's callbacks first require parent wait status not exactly false and
child `chosenOperation` exactly zero. The child's wait getter dynamically
retrieves its parent and forwards `getAskWaitStatus()`; ShopBuy returns its
current `work.askstatus` (`shopeditwidget.lua:1326-1420,1700-1714`;
`shopbuywidget.lua:2749-2756`). This is conditional on those methods resolving
on that retrieved parent, not proof of a live instance relationship.

With the optional operand nil, `closeShopEdit` requests base result 1 and
records the current focus as `lastbuy` only when the current operation equals
1. That branch retains `editWidgetOpen=12`. Another operation clears the flag
to zero without finishing the Ask. An explicit false or numeric zero operand
is nonnil and skips both branches. All paths then refresh the display, clear
`chosenOperation`, call `selectedBorder()` without its optional operands,
and request child closure if a child is found
(`shopbuywidget.lua:2564-2606`). After a confirmed result, a subsequent
`setAskParameter` therefore clears the retained flag and rearms `askstatus`.

`selectShopBuy` does not close the parent widget. Its two-value return is a
local caller boundary. Explicit parent cleanup remains a separate operation
(`shopbaseclass.lua:105-133`). `closeEventModeWidget` forwards
`closeWidget(4, widgetName)`. That method looks up the slot/name and can forward
the found widget to `closeWidgetDirect`
(`desktopwidget_connector.lua:25300-25328,26228-26237`). The
[published close helper contract](content-director-ui-contracts.md#closewidgetdirect-behavior)
owns its conditional cleanup requests. Neither a normal close return nor this
selection tuple establishes completed destruction, debit, stock change, item
grant, authoritative price or server eligibility.

## Original bytecode locators

Prototype indices and PCs are zero-based. Offsets are byte offsets in the
decoded payload, excluding the LPB wrapper. These selected operands resolve
return widths and omitted arguments that flattened decompiled text can hide.

| Script and method | Prototype / code start | Selected operands |
| --- | --- | --- |
| ShopBase `selectShopBuy` | `root/proto6` / 1561 | PC3 `CALL B=3,C=4`; PC4 compares status with false; PC10 `RETURN B=3`. |
| ShopBuy `getAskResult` | `root/proto44` / 22000 | PC1 retains one base result; PC2 compares -1; PC6/15 return two values; PC12 adds 1 to the current index. |
| ShopBuy `setAskParameter` | `root/proto45` / 22209 | PC2 compares the open flag with zero; PC4 returns no values; PC6/8 store zero/true. |
| ShopBuy `closeShopEdit` | `root/proto42` / 21349 | PC0 compares the optional operand with nil; PC4 compares operation with 1; PC8 sets base result 1; PC15 clears the open flag only on the other-operation branch. |
| ShopEdit `setInitialData` | `root/proto1` / 1488 | PC360 selects mode 12; PC371 stores quantity 1; PC429 calls numeric-input setup. |
| ShopEdit `processUICommandOperate` | `root/proto7` / 8124 | PC20/35 supply operation 1/2 and current quantity; PC22/37 call parent close with receiver only. |
| Desktop `selectEventModeWidgetYield` | `root/proto554` / 211193 | PC17 `CALL B=2,C=0`; PC18 `RETURN B=0` preserves true plus the getter's results. |

Reproduction uses `decode_lpb` from `tools/retail_script.py` and the complete
Lua 5.1 reader in `tools/build_quest_contracts.py`. Authenticate the selected
inputs against the linked manifests, check root closure bindings, and inspect
these branch, call and return operands in memory. Static characterization
does not execute the retail UI or establish native storage and rendering.
