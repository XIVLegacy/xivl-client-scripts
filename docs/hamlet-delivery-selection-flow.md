# Hamlet delivery selection flow

`PopulaceHamletSupply` separates opening, selection, price updates and explicit
close requests for `Ask/QuestDeliveryWidget`. Its item and materia selectors
adapt different result positions and return different tuple widths. These
are client menu contracts. They do not establish an accepted Hamlet supply,
inventory mutation, payment or reward.

The [Hamlet supply and score contract](hamlet-supply-ui-contract.md) owns the
supply-sheet lookups, ranking and score routes. The
[delivery-widget result contract](reward-widget-result-contracts.md) owns the
child's seven result positions. Generic creation, selection and Ask polling
remain in the [Gil-shop opening](gil-shop-widget-opening.md),
[ShopSell flow](shop-sell-selection-flow.md) and
[Ask result state](ask-widget-result-state.md) contracts.

## Selected inputs

This is static evidence from retail 1.23b extraction `2012.09.19.0001`.
Selected archive members matched [scripts.json](../manifests/scripts.json).
The retained archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json): 14,385,427
bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical source normalization replaces CRLF byte pairs with LF only.
Original LPBs and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical actor source | `lua/scripts/chara/npc/populace/populacehamletsupply.lua` | 6945 | `A784DEEEE3F170A01675DB153F7AA9FFAE31E82A2775C3518E1189AA18B7FAAD` |
| Actor LPB under `client/script/` | `729s9/wu7/uvupy975/uvupy97529xy5qrpuuyl.le.lpb` | 3416 | `7E8B077BBEE566EED963E26AED31A17F803362653A2AB184812ADFFBADC61A62` |
| Actor decoded Lua 5.1 payload | Same LPB, decoded payload | 3403 | `E9CC7C69A6B0409BD6FD5D63AC42B243CC2BC526F72E243B54E02C83AECF8FD1` |
| Canonical child source | `lua/scripts/widget/ask/questdeliverywidget.lua` | 92308 | `BA34706ADA144E2F7D2D91C7ACF6B4D6F31FCB9F9EC7A95A1A3D00345F35640D` |

The [delivery-widget identity](reward-widget-result-contracts.md) records the
child LPB and decoded-payload hashes. Source line locators below refer to
these canonical source hashes. Original prototype debug lines are a different
coordinate system.

Compositions require dynamic dispatch to the named implementations and normal
return of every reached call. Values read from native work storage can differ
from earlier assignments. The selected Lua does not prove applied storage,
stable object identity, callback delivery or native helper behavior.

## Opening, selection and close

Here `A1`, `A2`, and subsequent names denote arguments after the actor receiver.
They are positional labels, not inferred event-parameter meanings.

| Method | Desktop request after its receiver | Returned results |
| --- | --- | --- |
| `eventQuestItemMenuOpen(A1,A2,A3,A4,A5)` | `openEventModeWidgetYield("Ask/QuestDeliveryWidget",A1,A2,A3,A4,self,A5)` | All results from the dynamic opener, through a tailcall. |
| `eventQuestItemMenuSelect(A1,A2,A3)` | `selectEventModeWidgetYield("Ask/QuestDeliveryWidget",A1,A2,A3)` | Captures exactly seven results, then applies the item adaptation below. |
| `eventQuestMateriaMenuOpen(A1)` | `openEventModeWidgetYield("Ask/QuestDeliveryWidget",0,0,0,1,self,A1)` | All results from the dynamic opener, through a tailcall. |
| `eventQuestMateriaMenuSelect(A1)` | `selectEventModeWidgetYield("Ask/QuestDeliveryWidget",0,0,0,1,self,A1)` | Captures exactly eight results, then applies the materia adaptation below. |
| `eventQuestItemMenuClose()` and `eventQuestMateriaMenuClose()` | `closeEventModeWidget("Ask/QuestDeliveryWidget")` | Discard the close helper's results and return zero values. |

The selected methods have fixed parameters and no varargs. Opening uses the
creation-yield operation. Selection uses the separate operation that rearms
the existing event widget, waits and reads its result. Materia selection
supplies its opening operands again. Item selection supplies only its three
arguments. Neither selector requests an explicit close. A returned tuple,
completed Ask poll or price update therefore does not establish that the
widget closed.

## Result positions and adaptation

Let `D1` through `D8` denote desktop selection results in order. The generic
desktop wrapper contributes its own success discriminator at `D1`; the
child getter does not return that discriminator. Conditional on a successful
desktop selection resolving the pinned child getter, the remaining positions
are:

| Desktop position | Child result |
| --- | --- |
| `D2` | Chosen package. |
| `D3` | Chosen item slot. |
| `D4` | Chosen count. |
| `D5` | Item name index. |
| `D6` | Catalog ID. |
| `D7` | Attached materia count. |
| `D8` | `-1` when `waitForPrice` reads exactly Boolean true, otherwise `0`. |

The original getter returns seven numeric zeroes when the base result is
exactly `-1` or its item lookup returns nil. Otherwise it assigns
`askstatus=false`, reads the price-wait flag, obtains the local player and
looks up the chosen package and slot. It obtains the catalog and name from
that item. The attached count starts at zero and is replaced by the desktop
helper result only when both `isEquipment()` and
`getMateriaBindPermission()` return truthy values. These dynamic helper
results and fresh work reads remain conditional. Neither a returned package
and slot nor a successful lookup establishes an accepted delivery.

### Item selection

The item selector captures `D1` through `D7`, discarding any later values.
It returns exactly `(false,nil,nil,nil,nil)` when `D1` equals Boolean false,
or `D3` equals numeric zero. Otherwise it calls `worldMaster:_getMyPlayer()`
and requests `_getItem(D2,D3)` on that fresh result. A nil item-helper result
also returns the same five-value fallback. A non-nil result returns exactly:

`(D1,D4,D5,D7,itemHelperResult)`

Thus the composed success tuple carries the discriminator, chosen count,
name index, attached materia count and a freshly resolved item-helper result.
The package and slot feed the lookup. The catalog ID is omitted, and the
price-wait flag is beyond the seven-result capture and is discarded.

The comparisons are exact. A nil or numeric-zero `D1` does not satisfy the
false guard. A negative or nil `D3` does not satisfy the zero guard and can
reach the item helper. A Boolean-false item-helper result is non-nil and
passes the final guard. A missing player or another reached lookup failure
can raise instead of producing the five-value fallback.

### Materia selection

The materia selector captures `D1` through `D8`. Exactly Boolean-false `D1`
returns **one nil value**, before any player lookup. Otherwise it initializes
a local item result to nil and looks up a fresh local player's `_getItem(D2,D3)`
only when `D3 > 0`. After normal completion it returns exactly:

`(itemHelperResultOrNil,D2,D3,D8)`

A zero or negative slot skips the lookup and retains nil in the first
position. A nil slot reaches an invalid numeric comparison rather than a
special cancellation branch. A nil item-helper result preserves the other
three positions. There is no item-selector-style missing-item fallback.
Count, name index, catalog ID and attached materia count are omitted.

Under the pinned child getter and a successful desktop discriminator, a
canceled ask or missing child item yields `(nil,0,0,0)` here. The item
selector instead maps the same child result to its five-value false
fallback. The materia tuple's fourth value preserves the price-wait flag;
it is not a delivery acceptance result.

## Price update boundary

`eventQuestMateriaMenuSetPrice(A1,A2,A3)` first requests
`getChildWidgetByWindowName("Ask/QuestDeliveryWidget")`. Exactly nil skips
the setter and returns zero values. Otherwise it calls
`child:setPrice(A1,A2,A3)`, discards all results and returns zero values on
normal completion. It does not turn the child result into a success flag.
A false child is not skipped and can fail at the reached method lookup.

For the pinned `QuestDeliveryWidget.setPrice`, the supplied package and slot
must equal the current reads of `work.chosenPackage` and `work.chosenItem`.
A mismatch returns zero values before calls or work writes. On a match it
first assigns `work.price=A3` and `work.waitForPrice=false`. Only packages
`1` and `100` continue into the list and item operations. Other packages
return zero values after those two assignments.

The continuing path obtains the list property name, a fresh local player and
`_getItem(A1,A2)`, then reads the item's catalog and name. There is no nil
item guard before those reads. A later failure can therefore occur after the
price and wait assignments, without a Lua rollback. The method also reaches
the selected Grand Company or Hamlet display helpers according to later work
reads, and requests a `ShopEditWidget` child. Their native behavior, returned
values and price authority are not established here.

Only an open-child result equal to Boolean true enters the success branch.
That branch requests a selected border, assigns `editWidgetOpen=11`,
requests input disablement, stores `_getServerTime()` in `lastcommandtime`
and conditionally requests a materia list for equipment with an attached
count above zero. It returns one Boolean true. Other open-child results
assign `editWidgetOpen=0`, store a fresh server-time result and return zero
values. The Hamlet wrapper discards either normal result shape. None of
these assignments establishes readback, rendered state, an applied price,
an inventory mutation or settlement.

## Original locators and reproduction

Prototype indices and PCs are zero-based. Offsets identify decoded payload
bytes. Each binding PC is the root assignment of the named closure.

| Method | Canonical source lines | Binding PC | Prototype / code start | Selected PCs |
| --- | --- | ---: | --- | --- |
| Item open | `populacehamletsupply.lua:27-42` | 12 | `root/proto1` / `0x3C2` | 9 tailcalls the opener. |
| Item select | `:45-97` | 15 | `root/proto2` / `0x468` | 6 captures seven; 7/13 test false/zero; 20/24 get player/item; 25 tests nil; 35 returns five. |
| Item close | `:100-109` | 18 | `root/proto3` / `0x5B1` | 3 discards close results; 4 returns zero. |
| Materia open | `:112-127` | 21 | `root/proto4` / `0x637` | 9 tailcalls the opener. |
| Materia select | `:130-167` | 24 | `root/proto5` / `0x6EF` | 9 captures eight; 10 tests false; 13 returns one nil; 15 tests positive slot; 19/23 get player/item; 29 returns four. |
| Materia price | `:170-187` | 27 | `root/proto6` / `0x828` | 3 gets child; 4 tests nil; 10 discards setter results; 11 returns zero. |
| Materia close | `:190-199` | 30 | `root/proto7` / `0x8DF` | 3 discards close results; 4 returns zero. |
| Child getter | `questdeliverywidget.lua:3764-3847` | 168 | `root/proto53` / `0x752A` | 2 tests -1; 18 tests exact true; 30/31 look up item/test nil; 61 returns seven. |
| Child price setter | `:3885-4051` | 174 | `root/proto55` / `0x7904` | 2/6 compare slot/package; 9/11 write price/wait; 13/17 admit package; 31 gets item; 106/107 request child/test true; 138 returns true. |

Reproduction uses `decode_lpb` from `tools/retail_script.py` and
`ChunkReader`, `instruction`, `states_for`, `rk` and `call_record` from
`tools/build_quest_contracts.py`. Authenticate the selected archive members,
LPBs and decoded payloads in memory. Check complete root closure bindings,
call operands, comparison jumps, result capture widths and return widths.
Focused instruction-model fixtures with supplied dynamic call results reject
changes to the selected guards, tuple widths, opening-result propagation,
price matching and wait clearing. They do not execute the retail Lua or
validate native storage.

Actual actor identity, the selected historical event call, item identity and
ownership, helper binding, native state and readback, price authority,
accepted supply and settlement remain unestablished by this selected flow.
