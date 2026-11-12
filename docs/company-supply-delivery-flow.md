# Company supply delivery flow

`PopulaceCompanySupply` separates opening, selection and explicit close of
`Ask/QuestDeliveryWidget`. Its opener adapts two arguments when the supplied
mode exceeds 2. Its selector returns exactly five values after adapting seven
desktop results and looking up an item on a freshly obtained local player.
These client menu results do not establish an accepted delivery, inventory
mutation or seal grant.

The [delivery-widget result contract](reward-widget-result-contracts.md) owns
the child's seven result positions. Shared desktop opening, selection and Ask
state remain in these contracts:

- [Gil-shop opening](gil-shop-widget-opening.md)
- [ShopSell opening and selection](shop-sell-selection-flow.md)
- [Ask result and wait state](ask-widget-result-state.md)

The [Hamlet delivery flow](hamlet-delivery-selection-flow.md) concerns a
different actor class. Its additional materia and price methods do not supply
arguments or caller semantics for this Company flow.

## Selected inputs

This is static evidence from retail 1.23b extraction `2012.09.19.0001`.
Selected archive members matched [scripts.json](../manifests/scripts.json).
The archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json): 14,385,427
bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical source normalization replaces CRLF byte pairs with LF only.
Original LPBs and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical actor source | `lua/scripts/chara/npc/populace/populacecompanysupply.lua` | 10815 | `BE49DF8ED97BB99B79A274028BB0DAEDB1CE2AB06F108A77C0A4A5CDA535D118` |
| Actor LPB under `client/script/` | `729s9/wu7/uvupy975/uvupy9757vxu9wlrpuuyl.le.lpb` | 4820 | `7BB3F93A51BA80EDB64EE40FF1CE62244EC92B03E4B7FCB380245F7D94C38CC8` |
| Actor decoded Lua 5.1 payload | Same LPB, decoded payload | 4807 | `45ACF46CE1BD91738E33710D2C222320DD8BEA7BD1D6C8E7DA3010F62658ED29` |
| Canonical child source | `lua/scripts/widget/ask/questdeliverywidget.lua` | 92308 | `BA34706ADA144E2F7D2D91C7ACF6B4D6F31FCB9F9EC7A95A1A3D00345F35640D` |

The [delivery-widget identity](reward-widget-result-contracts.md) records the
child LPB and decoded-payload hashes. The source line locators below refer to
these canonical source hashes. Original prototype debug lines use a different
coordinate system.

Composition requires actual dynamic dispatch to the named implementations and
normal completion of every reached call. Assignments do not prove installed
native storage or later readback. A later player, item or work-field lookup
does not establish the identity or values of an earlier instance.

## Opening arguments and result

Here `A1`, `A2` and subsequent names denote arguments after the actor receiver.
`eventQuestItemMenuOpen(A1,A2,A3,A4)` first assigns the original `A4` to
`self.work.supplyMode`. When `2 < A4`, it substitutes numeric 0 for `A1` and
numeric 3 for `A4` in the opening request. Otherwise it preserves both. `A2`
and `A3` are forwarded unchanged on either path. It then requests:

```text
openEventModeWidgetYield(desktopWidget, "Ask/QuestDeliveryWidget",
                         computedA1, A2, A3, computedA4, self)
```

The original actor assignment precedes this substitution. For example, a
supplied mode of 4 requests the assignment `supplyMode=4` and sends 3 in the
fourth opening-tail position. The Lua contains no argument default or nil
guard. An omitted, nil or Boolean `A4` can fail at the numeric comparison
after the assignment request.

The opener captures and returns exactly the first desktop result. Zero
results become one nil value, and additional results are discarded. Under the
published desktop implementation this is one opening-status Boolean. That
desktop helper reports false only for a nil first widget-helper result and
true for every nonnil first result, including false or numeric zero. This is
an opening result, separate from a later selection result.

### Mode 1 first tab

For a positive order catalog and supplied mode 1, the opener retains both
operands. The widget's `initAsk` proto1 PCs 227-248 writes `work.mode=1`
with an omitted sixth operand and selects title row 8031. It stores
the catalog at PC323. Its `setInitialData` proto2 PCs 9-23 builds the
list, writes `work.listbox=1` at PC14, then sorts and refreshes it.
The positive-catalog branch (proto1 PCs 382-418) calls
`createVirtualItem(catalog,1):getItemProperPackage()`. Package 1 shows
`TabItem_1`, hides `TabItem_2` and requests zero-based
`TabControl_ItemList.SelectedIndex=0`. Package 100 requests the
second tab instead. A later admitted TabChanged writes
`getSelectedIndex("TabControl_ItemList")+1` to `work.listbox`
(proto41 PCs 62-70, proto21 PCs 0-4).

For the Company branch with zero shop ID, proto2 PCs 24-63 reads the
player's Grand Company membership and uses it for the banner, city,
company name, rank and points. The city and company text helpers
(proto5 and proto6) supply rows 100621-100623 and 8051-8053 for
membership 1-3. Rank (proto7 PCs 3-34) uses the player rank and sex.
Points (proto8 PCs 0-8) supplies the current and maximum values to row
3551. The initializer also writes the item-life and repair headers
through text row 214 with operands 10091 and 10093 and sets first-tab
header 3207 (proto1 PCs 304-313, 353-356).
[Shared form and first-tab selection](hamlet-delivery-selection-flow.md#inventory-selection-before-price)

## Selection and omitted arguments

`eventQuestItemMenuSelect(A1,A2,A3)` requests
`selectEventModeWidgetYield(desktopWidget,"Ask/QuestDeliveryWidget",A1,A2,A3)`.
It supplies no defaults and does not read back the opener's arguments or
`supplyMode`. Calling the opener with four values and then calling this
selector with no arguments sends three nil values to the selection helper.
Earlier opening values do not fill those selector positions.

The shared desktop route looks up the existing event widget in slot 4. For a
nonnil widget W, nominal `initEventModeWidget` calls
`resetBaseAskResult(W)`, `setAskParameter(W,A1,A2,A3)` and
`show(W,true,true)` in that order, discarding their results. Nil skips these
calls. This is rearming of the selected widget, separate from its opening
initializer. The [Ask contract](ask-widget-result-state.md#selected-state-and-calls)
owns the conditional input-enable request, zero base-result assignment and
later nonzero completion predicate.

The original child has its own directly bound
`QuestDeliveryWidget.setAskParameter`, with six fixed parameters after its
receiver and no varargs. It does not use its first five parameters. Only when
the sixth is nonnil and a fresh `work.shopid` read differs from numeric zero
does it request
`setText("TextBlock_CompanyPoint",8043,sixthArgument,100)`.
False and numeric zero are nonnil sixth arguments and would pass that first
guard. A nil sixth argument skips the shop-ID read and text request.

The Company selector's three-value tail cannot populate that sixth parameter
under nominal desktop forwarding. It therefore supplies nil there and skips
the optional text request, whether its own three arguments were explicit or
omitted. This does not prove what opening initialized or what remains visible.

After the optional text branch, the selected setter requests
`updateWindowDisplay(true)`, assigns `work.askstatus=true`, requests
`selectedBorder()` only when a later `work.editWidgetOpen` read equals numeric
zero, then assigns `work.waitNext=false`. It discards helper results and
returns zero values. Boolean false does not equal numeric zero in the border
guard. It directly assigns no shop ID, chosen package, chosen item, count or
`waitForPrice` field. Redraw, border effects and work readback remain dynamic
boundaries.

The desktop subsequently waits for selection and obtains the dynamic child
getter results. With the pinned Ask predicate, a later base result differing
from numeric zero completes the poll, including -1. A finished poll alone
does not identify an accepted delivery.

## Seven captured values to five caller results

Let `D1` through `D8` denote desktop selection results. The shared desktop
wrapper returns one false for its initialization/selection failure branches.
Otherwise it returns true followed by every result of the dynamic child
getter. Conditional on that success path and the pinned delivery getter:

| Desktop position | Value |
| --- | --- |
| `D1` | Desktop success discriminator. |
| `D2` | Chosen package. |
| `D3` | Chosen item slot. |
| `D4` | Chosen count. |
| `D5` | Item name index. |
| `D6` | Catalog ID. |
| `D7` | Attached materia count. |
| `D8` | Price-wait result, -1 or 0. |

The Company selector captures exactly `D1` through `D7`. Missing results
become nil, and later results are discarded. It returns exactly
`(false,nil,nil,nil,nil)` if `D1` equals Boolean false or `D3` equals numeric
zero. Otherwise it obtains a fresh `worldMaster:_getMyPlayer()` result and
requests that result's `_getItem(D2,D3)`. A nil first item-helper result returns
the same five-value fallback. A nonnil first item-helper result returns:

```text
(D1, D4, D5, D7, itemHelperResult)
```

The package and slot feed the fresh lookup. The return tuple carries the
desktop discriminator, count, name index, attached materia count and fresh
item-helper result. It omits the catalog ID and price-wait result. Under the
pinned child getter, cancellation or a missing child item supplies seven
zeroes, causing the selector's zero-slot fallback.

These guards use exact comparisons. Nil and numeric-zero `D1` do not equal
Boolean false. Nil or negative `D3` does not equal numeric zero and can reach
the item lookup. A Boolean-false item-helper result is nonnil and passes the
final guard. A missing player or another reached lookup failure can raise
instead of returning the fallback. No package-membership, positive-slot or
delivery-acceptance check is added by these wrappers.

## Explicit close and evidence limits

The selector contains no close request. Separate
`eventQuestItemMenuClose()` requests
`closeEventModeWidget(desktopWidget,"Ask/QuestDeliveryWidget")`, discards
every result and returns zero values. The shared desktop close route forwards
slot 4 and the name to its close helper. Normal return does not establish
completed destruction or cleanup.

These methods do not bind an authoritative NPC, native actor class, spawn,
historical event invocation, player/widget instance, item identity or native
work storage. Displayed company points, price authority, eligibility,
inventory mutation, accepted delivery, seal credit and settlement require
separate evidence. A matching method name alone does not establish the
dynamic binding assumed by this composition.

## Original locators and reproduction

Prototype indices and PCs are zero-based. Code starts are byte offsets in the
decoded payload, excluding the LPB wrapper. Each binding PC identifies the
root assignment of the named closure. Fixed CALL B/C operands are one greater
than their argument/result widths.

| Method | Canonical source lines | Binding PC | Prototype / code start | Selected original operands |
| --- | --- | ---: | --- | --- |
| Company item open | `populacecompanysupply.lua:338-359` | 27 | `root/proto6` / 3191 | PC1 assigns original mode; LT2 compares 2 with A4; CALL14 B=8,C=2; RETURN15 B=2. |
| Company item select | `:362-414` | 30 | `root/proto7` / 3430 | CALL6 B=6,C=8; EQ7/13 test false/zero; CALL20/24 get fresh player/item; EQ25 tests nil; RETURN35 B=6. |
| Company item close | `:417-426` | 33 | `root/proto8` / 3759 | CALL3 B=3,C=1 discards close results; RETURN4 B=1. |
| Child rearm | `questdeliverywidget.lua:3850-3882` | 171 | `root/proto54` / 30647 | EQ0 tests sixth argument nil; EQ4 tests shop ID zero; CALL11 requests text; CALL14 requests redraw; EQ19 tests edit flag zero; PC16/24 assign ask status/wait. |

Reproduction uses `decode_lpb` from `tools/retail_script.py` and
`ChunkReader`, `instruction`, `states_for`, `rk` and `call_record` from
`tools/build_quest_contracts.py`. Authenticate selected archive members, LPBs
and decoded payloads in memory, then check complete root assignments, call
operands, comparison jumps and return widths. Focused original-instruction
fixtures with synthetic dynamic results reject changed opening thresholds,
argument substitution, result widths, exact false/zero/nil guards, the sixth
setter argument boundary, rearm conditions and close-result discard. They do
not execute the retail Lua or prove native effects.
