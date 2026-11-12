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

### Company banner

With shop ID zero, `QuestDeliveryWidget.setInitialData` proto2 reads
`_getBelongGrandCompany()` at PC30, stores it as `work.townID` at PC32
and passes it to `displayGrandCompanyName` at PC57. That method
(proto3 PCs 0-13) calls `getGrandCompanyBanner` and writes its result
to `Label_GrandCompanyBanner.SqwtStyle`.

| Membership | Style | `getGrandCompanyBanner` proto4 PC | `common/default.style` line | `common/default.skin` line |
| --- | --- | --- | --- | --- |
| 1 | `LAB_profile_stateBanner_LimsaLominsa` | 3 | 2325 | 967 |
| 2 | `LAB_profile_stateBanner_Gridania` | 8 | 2349 | 977 |
| 3 | `LAB_profile_stateBanner_Uldah` | 13 | 2337 | 972 |

Other membership values reach the same return at PC17 with nil.
The standard `GrandCompanyShopWidget.form` line 44 declares the label
with the Limsa Lominsa style. The three runtime names are declared in the
standard common style sheet and each references its same-name three-cell
skin. The
[shared form and QuestDelivery script identities](hamlet-delivery-selection-flow.md#inventory-selection-before-price)
pin the selected inputs. Decode the following SQWT files with the
basename Blowfish key and remove the eight-byte wrapper.

| Client-relative asset | Stored bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `client/sqwt/common/default.style` | 353783, `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` | 353775, `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |
| `client/sqwt/common/default.skin` | 141967, `6788f2986d9cc8aeab83fcdbcf7a9115d3576ecfabf40529cc861f41f0df5640` | 141959, `929e65e9d5f191292d9b044e3e659ba115f18f6b3d8a82894046a7c75cbcad5a` |

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

## Mode 1 quantity selection

This route uses a positive order catalog with proper package 1, shop ID
zero and mode 1. `QuestDeliveryWidget.initAsk` proto1 PCs 323-329
stores the catalog, the two opening rewards as `rewardCS` and
`rewardHQCS`, and bundle 1. The first-tab row producer reads the held
item's stackability and count (proto30 PCs 27-31) and supplies them
to the [shared row writer](shop-sell-selection-flow.md#sale-quantity-in-shopeditwidget)
at PC63. In the positive-catalog arm, an exact catalog match selects
a visible row and the opener reward for that item's name index.
The display uses reward times stack count for a stackable item and
the reward alone for a nonstackable item. The `pricedata` field is
the unit reward (proto30 PCs 101-146, 231-235).

The standard first-tab
[Selection trigger](hamlet-delivery-selection-flow.md#inventory-selection-before-price)
passes `SelectedIndex` and `IntData.Value0` in that order, with tab
number 1. The inherited adapter rereads the named sender's selected
index before calling the child handler. The
[ordinary Layout0 Enter path](reward-widget-result-contracts.md#rewardselectwidget-opening-and-keyboard-selection)
supplies Selection when a focused list row is admitted. The markup's
separate `MouseEnteredItem` and `AnchoredItem` triggers update focus
and do not themselves select a row.

For a closed quantity child, QuestDelivery Selection proto40 PCs 23-84
reject exact-true `waitNext`, an already finished ask, exact-false
widget keyboard focus, a zero list count, focus at or beyond the
filtered count, exact-true `waitupdate`, or less than one server-clock
second since `lastcommandtime`. It assigns the incoming focus and tab
before refreshing. The refresh maps filtered focus through
`FilteredIndex` to source `Index` and stores a nonnegative result
(proto15 PCs 34-35, proto16 PCs 60-69, proto25 PCs 13-21). Proto40
PCs 85-113 take package 1 from tab 1 and slot `work.index+1`.
They look up that held item and require exact false from
`_isEquipping()`. For shop ID zero and mode 1, PCs 173-203 choose
`rewardCS` when `_getNameIndex()==1`, otherwise `rewardHQCS`,
and call `setPrice(package,slot,reward)`.

`setPrice` proto55 PCs 0-11 require matching chosen package and slot,
save the reward and clear `waitForPrice`. At PCs 47-106, shop ID zero
selects child mode 14. Membership 1, 2 and 3 select icon/seal catalog
pairs (530,1000201), (531,1000202) and (532,1000203).
`getGrandCompanyPoint` proto10 PCs 29-54 obtains the first result from
the matching held seal count in package 100, defaulting to zero.
The child-open request takes these twelve arguments after the Desktop
receiver, and captures exactly one result:

```text
ShopEditWidget, parent, true, 14, unitReward, currentPoints,
companyIcon, sealCatalog, parent, itemCatalog, nil, bundle
```

Desktop connector proto536 PCs 0-9 uses the parent's widget index,
passes the parent and shown flag to `openWidget`, and forwards the
nine initializer operands. Only an exact-true open result admits the
highlight, `editWidgetOpen=11`, parent input disable and timestamp
write (QuestDelivery proto55 PCs 107-124). The edit flag is 11 while
the child mode is 14.

### Quantity, focus and completion

`ShopEditWidget.setInitialData` proto1 saves mode at PC1 and selects
title 8034 for mode 14 at PCs 54-59. PCs 682-751 set Done/Back text
8035/8036, copy a nonnil unit reward, and initialize quantity and
maximum to the selected row's `stackCount`. Its helper requests
`parent:getItemContent(-1,"stackCount","Int")` (proto12 PC6), and
QuestDelivery proto52 PCs 69-79 forwards the named list maker,
source index and property. The numeric input requests minimum 1,
maximum equal to that count, and starts at the full stack. Mode 14
retains unit 1 and shows the unit reward times quantity as total.
There is no points-based quantity cap or 999 cap in this branch.
The quantity control is shown only for numeric `stackable == 1`
(proto1 PCs 775-785 and 877-880). The shared numeric setter writes
Minimum, Maximum then Value (proto4 PCs 6, 12, 16).

The same
[standard ShopEdit form, template and pointer controls](shop-sell-selection-flow.md#sale-quantity-in-shopeditwidget)
supply the quantity input and Done/Back buttons. The named
`CustomControl_NumberInput` registers `NumberInputBox.ValueChanged`
at priority 5 (ShopEdit proto0 PCs 68-71, common proto55 PC4).
A short admitted press and release on its selected ones arrow
requests +1 or -1 and can focus the numeric control before its
changed effective Value is sent as one Int. Proto8 PCs 0-14 require
parent wait status other than exact false, child operation zero and
the exact command. Proto9 PCs 0-8 require exact true from
`IsKeyboardFocusWithin` before storing that Int, then PCs 29-37
refresh the mode-14 total. An unchanged effective value has no
new ValueChanged event. This joins the selected markup to the
[static pointer route](https://github.com/XIVLegacy/xivl-decomp/blob/af764a34b28dbebf43e971212d2e8c5a0f464af1/docs/resource/sqwt-number-input-pointer-edit.md#short-primary-button-gesture).

`processAfterShow` proto3 PCs 0-4 skips the focus request when its
explicit argument is exact true. Otherwise it requests
`Button_Back`. Proto5 PCs 4-14 requests logical focus first and
keyboard focus only when the Desktop's focused widget equals this
child. The
[normal creation callback](desktop-widget-root-slots.md#creation-callback)
calls `show()` without arguments when admitted. Common show proto40
PCs 38-40 forwards its omitted third operand to this callback.
Focus acceptance remains conditional.

Under the same wait and operation guards, ordinary Button activation
can send `UILuaCommands.Operate` to the named Done or Back recipient.
ShopEdit proto7 PCs 10-39 checks the name, calls the parent
`setShopEditData(1,num1)` for Done or `setShopEditData(2,num1)`
for Back, then calls `closeShopEdit()` with no extra operand.
Each call discards all results, and the admitted child callback returns
one true. Layout0 Escape supplies `UILuaCommands.Cancel`. ShopEdit
proto6 PCs 10-28 gives the same Back outcome for sender
`Button_Back`; a different sender only requests Back focus.
[Button mouse command path](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-command-parameter-consumer.md#button-mouse-source)

QuestDelivery proto49 PCs 1 and 3 store operation and count.
For the omitted close operand, proto50 PCs 0-23 set base result 1,
disable input and set `waitNext=true` on Done. Back re-enables parent
input and leaves the Ask unfinished. Both reset operation, request
`closeChildWidget("ShopEditWidget",parent)` for a nonnil named
child, clear the edit flag and stamp server time (PCs 30-48).
The connector proto537 PC5 forwards the parent's widget index and
name to `closeWidget`. This is a child close request. Explicit
Company close still owns the outer widget. The QuestDelivery getter returns
seven values, Desktop prepends true, and the Company selector
captures seven and emits five as described above.

A bounded fixture uses one unequipped stack of three units with name
index 1 in package 1 slot 1, a matching positive order catalog and
supplied normal/alternate rewards 20 and 35. Enter on the first row
opens at 3 and total 60. A focused ones-arrow decrement yields 2
and total 40. Done can return `(true,2,1,0,item)` through the
Company selector for an ordinary non-equipment item. A separate Back
case requests child close and leaves the parent wait pending.
These are supplied fixture operands. Historical Company invocation,
original live focus/detach, server eligibility and settlement remain
unverified.

The installed ShopEdit LPB and decoded payload identities are in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json)
under `n1635q/r2vu561qn1635q.le.lpb`. The linked shop and Hamlet
pages pin the standard SQWT carriers. Reproduce the selected PCs
using the original-instruction reader below.

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
