# ShopSell opening and selection flow

`ShopBaseClass` provides separate sale opening, selection and explicit close
methods. Selection adapts four widget results into exactly five caller
results: an item-helper result, a count, a normalized mode, a package and an
item index. Cancellation and a desktop failure both become
`(nil, 0, 0, 0, 0)`. None of these values establishes a completed sale.

The [ShopSellWidget contract](shop-sell-widget-contract.md) owns the complete
55-method local behavior, work declarations, selection guards and supplied
price handling. The [ShopBuy flow](shop-buy-selection-contract.md) is a
different contract. Its opening actor, shop ID, currency, catalog rows and
buy-price inputs do not supply missing sale operands.

## Selected inputs

This is static evidence from retail 1.23b extraction `2012.09.19.0001`.
The selected in-memory archive members matched
[scripts.json](../manifests/scripts.json). The archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json): 14,385,427
bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonicalization replaces CRLF byte pairs with LF only. Original LPBs and
decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical path under `lua/scripts/` | SHA-256 |
| --- | --- |
| `chara/npc/populace/shop/shopbaseclass.lua` | `483220C5E7914B2406FC8184B69448980E46004945A7315203406475E52A5C9F` |
| `widget/desktopwidget_connector.lua` | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/ask/shopsellwidget.lua` | `DE0B1BD6BF32ADAFD2F6FE8ED71C64E7753DCFFE3BF709E3661FD069C4EB5766` |
| `widget/ask/askbaseclass.lua` | `642F3112D4663004FDC0B79DAF0A5FAF8B7588EAD58D2CD8E6747821BDA54ADB` |

The ShopBase original is
`client/script/729s9/wu7/uvupy975/r2vu/r2vu89r57y9rr.le.lpb`, 3,090
bytes, SHA-256
`892476F7224A23C641BC814CAEA749E9902CBF65C7831B8D0A2A134A2D2974EA`.
Its decoded payload is 3,077 bytes, SHA-256
`DC70138516C59ED823B5DEB79224F037721D3064266EC441150E0488221D0B58`.
The [ShopSell resource identity](shop-sell-widget-contract.md#resource-identity)
and [Ask base identity](ask-widget-result-state.md#source-identity) own those
original input pins. The connector identities are recorded in
[occupancy desktop wrappers](content-director-ui-contracts.md#occupancy-desktop-wrappers).

All compositions below require actual dynamic dispatch to the named methods
and normal completion. Lua assignment operands and later fresh work reads do
not establish applied native storage, preserved values or the same instance.
Reached lookups, comparisons and calls can raise, suspend or fail to return.

## Opening and rearming

`openShopSell` has two fixed parameters, including its receiver, and no
varargs. Both parameters are unused. It requests
`openEventModeWidgetYield(desktopWidget, "Ask/ShopSellWidget")`, discards all
results and returns zero values (`shopbaseclass.lua:136-145`). It supplies no
NPC, shop ID, currency or price operand and has no default or local guard.

The nominal desktop wrapper requests
`openWidgetYield(D, 4, "Ask/ShopSellWidget", nil, nil, false)` with no extra
tail. Only a nil first helper result becomes false; every nonnil first result,
including false or numeric zero, becomes true. The sale opener discards that
Boolean. The [generic opening contract](content-director-ui-contracts.md#desktop-widget-admission-and-close)
owns admission, creation requests, retries and lookup limits. Opening is
separate from waiting for a sale selection.

The selected widget resource requires `/Widget/Ask/AskBaseClass` and requests
the `ShopSellWidget`/`AskBaseClass` class relationship. Under the
[shared initialization route](gil-shop-widget-opening.md#item-list-initialization),
nominal Ask initialization declares the base result fields and calls the
dynamic `initAsk` with its extra tail. The pinned ShopSell initializer has
only its receiver, performs the published local setup and calls
`setInitialData`. This supplies no shop assignment through an initializer
argument. Class registration, actual initialization dispatch and native work
installation remain conditional.

`selectShopSell` subsequently requests
`selectEventModeWidgetYield(desktopWidget, "Ask/ShopSellWidget")`, with no
extra initializer arguments. Nominal initialization looks up slot 4 and this
literal name. For a nonnil widget W, it calls `resetBaseAskResult(W)`,
`setAskParameter(W)` and `show(W, true, true)` in that order, discarding their
results, then returns W. Nil skips those calls.

The [Ask base contract](ask-widget-result-state.md#selected-state-and-calls)
owns the zero result reset, exact-true input-control flag and completion
predicate. `ShopSellWidget.setAskParameter` requests redraw, assigns
`askstatus=true`, requests `selectedBorder()` only when the current
`editWidgetOpen` equals zero, then assigns `waitNext=false`. It does not clear
`waitForPrice`, `chosenPackage`, `chosenItem` or `buycount`
(`shopsellwidget.lua:2823-2842`). These are distinct writes and later reads.

The desktop passes W to `selectWidgetYield` with its optional show operand
omitted. That path skips the helper's child-show branch and requests
`selectWidgetTimerYield(D, W, nil)`, retaining only its first result. The
[published wait contract](fishing-input-flow-contract.md#wait-result-width-and-cleanup)
owns the alive/completion polling and literal `_wait(0.1)` operand. With the
nominal inherited Ask predicate, a later base result differing from numeric
zero finishes the poll; this includes cancellation -1 and does not itself
identify acceptance.

## Four widget results to five caller results

The desktop returns one false when initialization yields nil or selection
returns exactly false. Otherwise it returns true followed by all results of
W's dynamic `getAskResult()`. `selectShopSell` captures exactly five values:
desktop status S and four values P, N, Q and F. Missing results are adjusted
to nil and additional results are discarded.

Only S exactly equal to Boolean false replaces P, N, Q and F with numeric
zeros. Nil, numeric zero and other non-false statuses do not take that branch.
The caller then computes these five results (`shopbaseclass.lua:160-198`):

```text
(I, Q, M, P, N)
```

I starts nil. Only nonnil N satisfying `0 < N` requests
`A:_getItem(P, N)`, where A is the caller's second total argument. The first
helper result becomes I unchanged, including nil, false or numeric zero.
Zero helper results become nil. The receiver of `selectShopSell` is unused;
this lookup does not use the shop receiver or a fresh global player lookup.
The actual supplied actor and native item identity remain unbound.

P has no nil, positivity or package-membership guard. Q is forwarded without
validation or a default. N equal to nil, zero or a negative number skips the
item request but remains in the fifth return position. A nonnil N must
support the reached numeric comparison; Boolean N does not become a numeric
sentinel. M is numeric 0 only when F equals numeric 0, numeric 1 only when F
equals numeric 1, and nil otherwise. Boolean false and true are not those
numeric values. The caller does not return a price or convert N to a catalog
ID, filtered focus or zero-based row.

The pinned widget getter returns exactly four values after one base-result
read (`shopsellwidget.lua:2781-2820`):

| Getter condition | Widget tuple P, N, Q, F | Caller result under normal helper completion |
| --- | --- | --- |
| Base result exactly -1 | `(0, 0, 0, 0)` | `(nil, 0, 0, 0, 0)` without an item request |
| Other base result; current `waitForPrice == true` | `(chosenPackage, chosenItem, 1, 1)` | `(I, 1, 1, chosenPackage, chosenItem)` |
| Other base result; current `waitForPrice` not exactly true | `(chosenPackage, chosenItem, buycount, nil)` | `(I, buycount, nil, chosenPackage, chosenItem)` |
| Desktop status exactly false | Four caller-local numeric zeros | `(nil, 0, 0, 0, 0)` without an item request |

Both non-cancel getter paths first assign `askstatus=false`. The final path
also assigns `waitupdate=true`. The price-wait path does not. Neither clears
the chosen fields. Numeric zero as `waitForPrice` takes the final path. These
are later field reads, not a snapshot captured when selection occurred.

## Selection, supplied price and cancellation

The [local widget contract](shop-sell-widget-contract.md#complete-55-method-contract)
owns selection eligibility and focus mapping. An admitted selection assigns
the mapped package and `index+1` to the chosen fields, then calls
`operateSell`. That method requests base result 1, assigns
`waitForPrice=true` and `lastsub=8`, and saves a fresh server-time result.
If later reads preserve those values, selection yields the price-wait row
above. This connects a local price-request result to the caller; it does not
identify a request transport or a price producer.

`setPrice` consumes a supplied price and matching package/item operands. Its
selected successful child-open branch uses `ShopEditWidget` mode 11 and
clears `waitForPrice`. `setShopEditData` stores supplied operation and count.
With an omitted or nil optional operand, `closeShopEdit` finishes the Ask
only when the current operation equals 1. That branch requests base result
1, input disablement and `waitNext=true`. Another operation clears the edit
flag and requests input enablement without finishing the Ask. A nonnil
optional operand, including false or zero, skips both operation branches.
The local contract owns the common child-close attempts and resets. These
conditional parent methods do not establish child callback delivery, applied
numeric bounds or an actual parent/child relationship.

Parent Cancel refuses cancellation when `editWidgetOpen ~= 0`,
`waitNext == true` or `isAskFinish()` returns exactly true. Otherwise it
calls `previousSequence`. Parent Close calls that method without those Cancel
guards. `previousSequence` requests `saveSortType()` and then base result -1,
discarding both results. The base setter can request input disablement before
the result write. Neither cancellation nor a finished wait closes the parent
widget or proves that any write was read back.

### Sale quantity in ShopEditWidget

The mode-11 child uses the standard `widget/ShopEditWidget.form`.
It imports `common/LABBasisNumberInputBox.tpl` at line 5.
`Label_NumberInput_1` selects `ControlTemplate_Label_NumberInputBox`
and wraps `CustomControl_NumberInput` of type `NumberInputBox` at
lines 76-77. The template's ValueChanged action at lines 5-6 matches
SourceType Slider and supplies one Int from the effective Value.
`Button_Done` and `Button_Back` declare UILuaCommands.Operate at
lines 122-123. The arrows are constructed RepeatButtons in the numeric
control. A short admitted release on the selected ones arrow requests
+1 for Up or -1 for Down. The ordinary preview-down focus search
can select the numeric control before that release.
[NumberInputBox pointer and focus route](https://github.com/XIVLegacy/xivl-decomp/blob/af764a34b28dbebf43e971212d2e8c5a0f464af1/docs/resource/sqwt-number-input-pointer-edit.md)

| SQWT path under `client/sqwt/` | Installed bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `widget/ShopEditWidget.form` | 9177, `23fb6f4c044126501e718779db8f2fe8512f5a3acdfc5c13cc70c2fc00c75fc5` | 9169, `1009c0fdfc908746c26f1c1b5e854c8f8bc07fbc67a0cdfb32f4f32168370c13` |
| `common/LABBasisNumberInputBox.tpl` | 1059, `91c6aec1f2c3445faad6570d934eb4392afcd0aabdff36ae8cfbc69a48d269af` | 1051, `546672a02cb526a810bbe191a574832499b3208ff294df5940c184fb3e729922` |

ShopEdit `root/proto1` stores `work.mode` from the supplied mode
at PC1 (offset 1492) and admits mode 11 at PC132 (2016).
PC161 (2132) requests `stackCount` as Int from the supplied parent.
The helper `root/proto12` PC6 (10297) tailcalls that parent's
`getItemContent(-1, "stackCount", "Int")`. ShopSell `root/proto42`
PC79 (22548) passes the current list maker name, `work.index` and
property name to the list getter with the extra type operand.
The nominal shared list getter `root/proto170` PC4 (31286) forwards
only the maker, index and property to `_getListProperty`.

The row producer `ShopSellWidget.setItemToXmlLight` (`root/proto20`)
reads `_isStackable` and `_countStack` at PCs28 and 31 (11124 and
11136), then supplies them at PC69 (11288) with the row write flag
true and subtype 7 or 8 for lists 1 and 2. On that normal
`DesktopWidget.setItemToXml` branch in `desktopwidget_itemdetail.lua`
(`root/proto0`), the truthy stackability arm requests numeric
`stackable=1` and the supplied `stackCount` at PCs243 and 249
(4188 and 4212). The other arm requests `stackable=0` and
`stackCount=1` at PCs271 and 277 (4300 and 4324).

ShopEdit sets the maximum from the selected row's count. When the
supplied catalog is strictly between 1000002 and 1000101 and the
count exceeds 999, PC178 (2200) caps it at 999. PC182 (2216) sets
`work.num1` to that maximum. PC199 (2284) requests
`setNumberInput("CustomControl_NumberInput", maximum, 1, maximum)`.
The helper `root/proto4` requests Minimum, Maximum and Value in
that order at PCs6, 12 and 16 (7409, 7433 and 7449).
PC228 (2400) requires numeric `stackable == 1` for the branch
that shows the numeric control at PC233 (2420). The other branch
requests that control hidden at PC328 (2800). The initialized
quantity is therefore the full selected stack, subject to the stated
cap. The supplied unit price is multiplied by the selected count for
`TextBlock_TotalPrice` at PCs190-191 (2248-2252).

ShopEdit `root/proto0` PCs68-71 (941-953) register the named numeric
control for `NumberInputBox.ValueChanged` before initialization.
The shared condition helper `root/proto55` PC4 (17114) supplies
priority 5. ShopEdit `root/proto8` PCs0-14 (8516-8572) requires
parent wait status other than exact false and child operation zero.
For the exact command it forwards the fifth total argument to
`updateNumber`. In `root/proto9` PCs0-8 (8735-8767), the count
write requires `CustomControl_NumberInput.IsKeyboardFocusWithin`
to read exact true. The ordinary mode-11 unit is 1 (PC105 of
`root/proto1`), so a successful edit also requests the new total
as unit price times the current count at PCs29-37 (8851-8883).

Done uses the same wait and operation gates, checks the name
`Button_Done`, then writes child operation 1. ShopEdit `root/proto7`
PC20 (8204) calls the retrieved parent with `setShopEditData(1, num1)`
and PC22 (8212) requests `closeShopEdit()` with the optional operand
omitted. In ShopSell `root/proto40`, the admitted confirm branch
requests base result 1 and input disable, then sets `waitNext=true`
at PCs8, 11 and 13 (21231, 21243 and 21251). The common continuation
checks the named child lookup at PCs34-36 (21335-21343), requests
`closeChildWidget` for a nonnil result at PC41 (21363), and clears
`editWidgetOpen` at PC43 (21371). Connector `root/proto537`
PC5 (207573) forwards the parent's widget index and name
`ShopEditWidget` to `closeWidget`.
[Close helper conditions](content-director-ui-contracts.md#closewidgetdirect-behavior)

The ShopEdit and ItemDetail inputs are pinned in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json)
under `n1635q/r2vu561qn1635q.le.lpb` and
`n1635q/65rzqvun1635q_1q5x65q91y.le.lpb`. Reproduce the operands
with the decoder below. Decode the SQEX assets using their basenames
as Blowfish keys and require byte-exact re-encryption before inspecting
the named metadata. Native focus acceptance, later child lifetime and
frame visibility remain unverified.

### Rearm relative to a package change

Connector `root/proto556` calls `resetBaseAskResult` at PC 7,
`setAskParameter` at PC 10 and `show` at PC 14. ShopSell
`setAskParameter` calls `updateWindowDisplay(true)` at PC 2 before it
assigns `askstatus=true`, requests a border reset when admitted, and
assigns `waitNext=false`. The full refresh reaches `updateListFocus` at
`root/proto5` PC 35. See [Focus after removal from the current package](shop-sell-widget-contract.md#focus-after-removal-from-the-current-package)
for the list mapping and pending-count guards.

In the main lane of the tracked `sell_item.pcapng` extract, server-to-client
opcode runs 96 through 104 of `xivl-captures:derived/sequences.json`
`perCapture.sell_item.pcapng.collapsed` contain `0x0153`, `0x0146`,
`0x0148`, `0x0146`, `0x014E`, `0x0147` three times, `0x016E`, `0x0169`,
and `0x0130` in order. The tracked call census counts three
`selectShopSell` calls in the capture. The identity of the specific
`0x0130` in run 104 and its frame separation remain unverified. See
`xivl-captures:studies/local-guildleve-dialogue/derived/accounting.json`,
`sell_item.pcapng`.

The native item-command queue preserves received operation order. Its
admitted, nondeferred UpdateEnd path integrates staged storage before
requesting the dirty-package callback. An admitted `0x0130` can take its
own immediate dispatch path or wait in the event receiver queue. See
`xivl-decomp:docs/net/retainer-item-storage.md`, Refresh and packet ordering,
and `xivl-decomp:docs/event/start-event-fn-receiver.md`, Submission, retry
and execution. The captured stream order leaves the relative execution
of the two queues, package callback completion, and the earliest safe
rearm unresolved.

## Explicit close and evidence limits

`selectShopSell` contains no parent-close request. Separate
`closeShopSell`, whose two fixed parameters are unused, calls
`closeEventModeWidget(desktopWidget, "Ask/ShopSellWidget")`, discards every
result and returns zero values (`shopbaseclass.lua:148-157`). The nominal
desktop method tail-forwards `closeWidget(D, 4, name)`. The
[generic close contract](content-director-ui-contracts.md#desktop-widget-admission-and-close)
owns its nil lookup rejection and conditional
[direct-close requests](content-director-ui-contracts.md#closewidgetdirect-behavior).
Normal return does not establish completed destruction or lifetime cleanup.

This joins the conditional sale helpers to their widget result producer and
the supplied actor's item lookup. It does not bind an actual NPC or shop,
historical invocation, player/widget instance, native work storage or item
identity. The supplied price, authoritative sale eligibility, item removal,
currency credit, server acceptance and settlement remain separate evidence
boundaries. No sale formula or static selling-price data is inferred from the
BUY publication or from these UI result positions.

## Original locators and reproduction

PCs and prototype indices are zero-based. Code starts are byte offsets in the
decoded payload, excluding the LPB wrapper. Fixed CALL B/C operands count one
more than their argument/result widths; zero retains an open tail.

| Method | Prototype / code start | Consequential original operands |
| --- | --- | --- |
| ShopBase `openShopSell` | `root/proto7` / 1734 | Root binding PC30; CALL PC3 B=3,C=1; RETURN PC4 B=1 |
| ShopBase `closeShopSell` | `root/proto8` / 1867 | Root binding PC33; CALL PC3 B=3,C=1; RETURN PC4 B=1 |
| ShopBase `selectShopSell` | `root/proto9` / 1996 | Root binding PC36; desktop CALL PC3 B=3,C=6; status EQ4; index EQ11/LT13; item CALL18 B=4,C=2; mode EQ20/22/26; RETURN34 B=6 |
| Desktop `openEventModeWidgetYield` | `root/proto551` / 210799 | CALL6 B=0,C=2; nil EQ7; one Boolean result |
| Desktop `initEventModeWidget` | `root/proto556` / 211614 | getWidget CALL3 B=4,C=2; reset CALL7; initializer CALL10 B=0,C=1; show CALL14 B=4,C=1 |
| Desktop `selectEventModeWidgetYield` | `root/proto554` / 211193 | init CALL4 B=0,C=2; selection CALL9 B=3,C=2; getter CALL17 B=2,C=0; RETURN18 B=0 |
| Desktop `closeEventModeWidget` | `root/proto553` / 211103 | TAILCALL3 B=4,C=0 forwards slot 4/name and all results |

The selected widget getter, rearming and inherited Ask locators remain in
their canonical contracts. Reproduction uses `decode_lpb` from
`tools/retail_script.py` and `ChunkReader`, `instruction`, `states_for` and
`call_record` from `tools/build_quest_contracts.py`. Authenticate the selected
source/LPB/payload triples and complete root assignments before checking
receiver, branch and arity operands in memory. Focused static fixtures reject
changed five-result capture, status polarity, positive-index admission, mode
normalization and opening-result discard. They characterize supplied helper
results without executing the client or proving native effects.
