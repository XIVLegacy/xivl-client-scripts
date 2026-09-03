# Grand Company shop lifecycle

This report recovers the retail Lua boundary for `PopulaceCompanyShop` and
`Ask/GrandCompanyShopWidget`. It distinguishes observed presentation and intent
state from purchase fulfillment that is not present in the published scripts.
The safe conclusion is narrow: a completed ask yields a Grand Company seal shop
sheet row ID, but the Lua does not expose a purchase quantity, debit seals, add
an item, send a purchase command, or define an acknowledgement.

## Evidence scope

The primary evidence is the immutable retail Lua corpus and its generated call
sidecars. The callback classification is cross-checked against
`xivl-client-structs:manifests/lua_callback_contract.json` and
`xivl-client-structs:manifests/lua_api_contract.json`. Catalog column meanings
and row coverage are independently documented by
`xivl-client-data:docs/shop-catalogs.md`.

On 2026-09-02, an exact native string-reference export was attempted for
`eventShopMenuOpen`, `eventShopMenuAsk`, and `eventShopMenuClose`. The committed
wrapper could not run because this checkout has no configured
`BCS_GHIDRA_HOME`, and no local Ghidra project was discoverable. No native owner
or caller is therefore assigned from names, proximity, or convention.

## Lifecycle and state ordering

1. `PopulaceCompanyShop.initForEvent` maps actor classes to company/town IDs and
   four catalog ranges, sets the displayed company rank ceiling to 25, and
   preloads the applicable seal-shop rows
   (`lua/scripts/chara/npc/populace/populacecompanyshop.lua:11-323`). The actor
   mapping is 1500202 -> 1, 1500203 -> 2, and 1500201 -> 3
   (`:113-177`).
2. `eventTalkMainMenu` performs presentation flow and stores the selected rank
   division in `work.rankDiv`; accepted divisions return 1, a shop-menu branch
   returns 2, and cancellation returns -1 (`:863-1074`). Its `isUpperRank`
   helper compares the requested threshold with the local player's company
   rank; rank 127 is normalized to zero
   (`lua/scripts/chara/npc/npcbaseclass_event.lua:883-904`). These are observed
   client gates, not proof of server authorization.
3. `eventShopMenuOpen` snapshots `_getSpecialEventWork(9)` into
   `work.eventFlag`: only values 8 and 11 survive, otherwise it stores zero.
   It then opens `Ask/GrandCompanyShopWidget` with the actor as owner
   (`populacecompanyshop.lua:1077-1110`).
4. The widget reads the actor's company number and maps company 1/2/3 to point
   item 1000201/1000202/1000203
   (`lua/scripts/widget/ask/grandcompanyshopwidget.lua:145-165`). It reads the
   local rank and counts that point item in package 100 for display and local
   affordability UI (`:410-556`, `:1587-1620`).
5. List construction asks the actor for a tab maximum and then for each row's
   seven detail values (`:799-920`). The actor derives the sheet row as
   `start + ordinal - 1` and returns item ID, columns 1-4, a Boolean admission
   flag, and the sheet row ID
   (`populacecompanyshop.lua:2275-2401`). Category 3 has zero rows while
   `eventFlag` is zero (`:2247-2272`). A row is inserted only when its column 6
   requirement is no greater than `eventFlag`; category 4 also applies local
   key-item ownership conditions (`:2294-2398`).
6. Each inserted list row preserves the source ordinal as `itemIndex`, column 4
   as `essentialRank`, the row ID as `sheetIndex`, and column 3 as `pricedata`
   (`grandcompanyshopwidget.lua:923-1074`). `isMaskItem` masks a row only when
   its essential rank exceeds the locally displayed rank (`:2065-2076`).
7. Selecting an unmasked row opens `ShopEditWidget` in mode 13 with the row
   price, locally counted points, icon data, point ID, item catalog ID, and
   owner. A successful open stores the selected row's `sheetIndex`
   (`:1959-2051`). The child Done action reports operation 1 plus `work.num1`;
   Back reports operation 2 plus the same value
   (`lua/scripts/widget/shopeditwidget.lua:1381-1415`).
8. `GrandCompanyShopWidget.setShopEditData` stores the operation and child
   numeric value in fields named `chosenOperation` and `buyCount`.
   Operation 1 causes `closeShopEdit` to set the base ask result to 1. Any
   other operation returns to the list and clears the selected row. The stored
   `buyCount` is not consumed by this widget (`grandcompanyshopwidget.lua:2232-2288`).
9. `GrandCompanyShopWidget.getAskResult` returns one value: the selected sheet
   row ID when the base result is complete, otherwise -1 (`:2139-2152`). The
   generic connector wraps it as `(true, rowId)`; widget selection failure is
   just `false` (`lua/scripts/widget/desktopwidget_connector.lua:26241-26265`).
   `eventShopMenuAsk` normalizes that failure to `(false, -1)`
   (`populacecompanyshop.lua:1113-1128`).
10. `eventShopMenuClose` closes the event-mode widget (`:1131-1140`). Actor
    finalization releases its spreadsheet container and unloads the retained
    ranges before calling the superclass (`:326-437`).

`PopulaceBlackMarketeer` is a second consumer of the same widget. Its
`eventSealShopMenuOpen`, `eventSealShopMenuAsk`, and close flow have the same
ask-result shape, while its company number comes from the player's current
company (`lua/scripts/chara/npc/populace/populaceblackmarketeer.lua:357-468`).

## Result shape and quantity boundary

The catalog fields relevant to this path are:

| Sheet value | Observed meaning |
|---|---|
| row ID | Company/category-local inventory key returned by the ask |
| column 0 | Item catalog ID |
| column 1 | Virtual-item quality |
| column 2 | Item quantity per catalog purchase |
| column 3 | Seal price shown by the widget |
| column 4 | Widget rank requirement |
| column 5 | Company ID; retained in the derived catalog, not read here |
| column 6 | Event-flag admission threshold |
| column 8 | Category; retained in the derived catalog, not read here |

These meanings and the complete 402-row extraction are independently fixed by
`xivl-client-data:docs/shop-catalogs.md:21-68`.

The result boundary is exactly:

| Stage | Observed values |
|---|---|
| Child Done | operation 1, local `num1` |
| Grand Company widget state | `chosenOperation`, `buyCount`, selected sheet row ID |
| Grand Company `getAskResult` | selected sheet row ID only |
| Actor `eventShopMenuAsk` | success Boolean, selected sheet row ID |

The name `buyCount` does not establish the child value's semantics for mode 13.
For a stackable item, mode 13 initializes `num1` from the selected virtual
item's existing `stackCount` (`shopeditwidget.lua:751-817`), and the published
`updateNumber` branch has an unresolved price comparison (`:1494-1523`). The
generic gil-shop widget returns both its selected ordinal and its field named
`buycount`
(`lua/scripts/widget/ask/shopbuywidget.lua:2636-2657`), while the Grand Company
widget omits the mode-13 numeric value entirely. The published Lua therefore
cannot establish a requested purchase quantity from this result path. It also
cannot establish whether retail always bought one catalog bundle or relied on a
native/server path absent from this corpus.

## Local update boundary

`GrandCompanyShopWidget.updatePlayerItem` contains display-refresh state. A
kind 0 update initializes a pending update count; kind 100 marks the point
balance dirty; subsequent updates decrement the count, then refresh bag space,
points, the list, and any open child balance
(`grandcompanyshopwidget.lua:2079-2136`). It contains no inventory or currency
mutation.

The published connector does name `Ask/GrandCompanyShopWidget` in
`processUpdateItemInformation` (`desktopwidget_connector.lua:5861-6046`), but
the called helper invokes `DesktopWidget.updatePlayerItem(widget, kind, value)`
rather than `widget.updatePlayerItem(kind, value)` (`:6157-6175`). The published
`DesktopWidget.updatePlayerItem` body at `:6371-6382` does not establish a
working dispatch to the Grand Company method. Treat the refresh method as a
local presentation handler whose actual native/runtime delivery remains
unproved; do not turn it into an acknowledgement contract.

## Callback and N-API census

The generated client-structs callback contract classifies only
`PopulaceCompanyShop._onFinalize` as a callback. It classifies
`eventShopMenuOpen`, `eventShopMenuAsk`, and `eventShopMenuClose` as ordinary
methods. `GrandCompanyShopWidget` and `ShopEditWidget` have no callback records.
The four callbacks on `DesktopWidget` are target-selection callbacks and none is
shop-specific. Consequently, the available manifests provide no native
registration mapping for the three shop lifecycle method names.

The call sidecars show only local state/query and presentation-facing N-API
families on this path: `_getSpecialEventWork`, `_getMyPlayer`, item-package
capacity and free-space reads, `_getData`, spreadsheet key loading, server-time
display state, and widget helpers. The client-structs N-API index associates
these with WorldMaster, CharaBase, ItemBase, Spreadsheet, and DesktopWidget
tables. Neither the actor nor widget sidecar contains a purchase command,
server-command call, item add/remove call, or work-update emitter.

## Consumer-safe minimum

A consumer can reproduce the observed boundary without claiming more:

- Preserve the actor/company-to-row mapping and treat the returned value as a
  sheet row ID, not a list ordinal or item ID.
- Treat `(true, rowId)` as client purchase intent only. Re-resolve the row from
  an authoritative catalog and reject unknown or cross-company rows.
- Mirror rank, event, ownership, inventory-space, and point checks only as
  defensive policy. Lua proves their client presentation use, not their
  authoritative server order or failure behavior.
- Keep catalog `itemQuantity` separate from the unreturned ShopEdit numeric
  value. The catalog field proves bundle yield; it does not prove how many
  bundles a completed ask requested. A one-row-bundle purchase is a consumer
  policy unless another evidence source resolves that channel.
- Perform currency and inventory changes atomically under consumer-owned rules;
  do not describe that mutation order as retail-recovered from these scripts.

## No-go claims

The current evidence does not justify any of the following:

- a purchase opcode, packet layout, request command, or native purchase owner;
- an acknowledgement, failure code, retry, rollback, or close-on-failure order;
- the authoritative order of rank, company, event, ownership, capacity,
  currency, or inventory checks;
- a proved quantity of one, a proved use of the ShopEdit count, or multiplication
  of seal price by that count;
- client-side inventory grant, key-item grant, seal debit, or final state
  authority;
- interpreting `updatePlayerItem` delivery as a purchase acknowledgement;
- attribution of the ordinary `eventShopMenu*` method names to native callers
  without a completed exact-address reference trace.

## Reproduction

Run:

```text
python -m unittest tools.tests.test_grand_company_shop_lifecycle
python tools/validate_corpus.py
```

The focused test fixes the actor/widget result shape, child count omission,
catalog admission gates, connector ambiguity, and absence of mutation/command
APIs in the relevant sidecars.
