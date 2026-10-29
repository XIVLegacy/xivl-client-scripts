# Retainer widget result tuples

The retail client widgets return these local result tuples:

`RetainerTradeWidget` returns:

- `31`: emitted for a positive count when `chosenOwner == 4`. If `editmoney`
  is false, the tuple is `(31, chosenPackage, chosenItem, chosenCount)`; if
  true, it is `(31, 100, retainerMoneyIndex, chosenCount)`.
- `32`: emitted for a positive count otherwise. If `editmoney` is false, the
  tuple is `(32, chosenPackage, chosenItem, chosenCount)`; if true, it is
  `(32, 100, playerMoneyIndex, chosenCount)`.

`RetainerItemListWidget` returns:

- `13`: `(13, chosenPackage, chosenItem)` for the selected list item; it does
  not return a count.
- `21`: the ordered tuple `(21, chosenPackage, chosenItem, bazaartype,
  rewardPrice, rewardPackage, rewardItem, chosenCount, rewardCount)`.
- `22`: `(22, package, item, bazaartype)`. A nonzero `rewardPackage`
  selects `rewardPackage/rewardItem`; otherwise the ordinary widget uses
  `chosenPackage/chosenItem` and the Ask widget uses
  `resultPackage/resultItem`. No quantity or price is returned in this
  four-value widget result.

`Ask/RetainerItemListWidget` returns:

- `13`: `(13, chosenPackage, chosenItem)` for the selected list item; it does
  not return a count.
- `21`: the ordered tuple `(21, resultPackage, resultItem, bazaartype,
  rewardPrice, rewardPackage, rewardItem, resultCount, rewardCount)`. Its
  bazaar-edit setter copies the selected package and item into `resultPackage`
  and `resultItem`.
- `22`: `(22, package, item, bazaartype)`. A nonzero `rewardPackage`
  selects `rewardPackage/rewardItem`; otherwise the ordinary widget uses
  `chosenPackage/chosenItem` and the Ask widget uses
  `resultPackage/resultItem`. No quantity or price is returned in this
  four-value widget result.

These are UI result values and selected fields only. They do not establish
whether codes 31, 32, 13, 21, or 22 mean retrieve, entrust, list, remove, or any
other server operation. The retail client tuple alone does not establish
that a server accepted or applied it.

Evidence: `lua/scripts/widget/retainertradewidget.lua:3188-3294,3691-3763`,
`lua/scripts/widget/retaineritemlistwidget.lua:9111-9132,9185-9207,9370-9444`,
and `lua/scripts/widget/ask/retaineritemlistwidget.lua:6222-6263,6323-6350,6536-6620`.
The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.

## Code 22 issuer

Code `22` is selected by `operateBazaarAbort` only for `chosenPackage == 8`.
For a row with `bazaarkind == 0`, it follows the row's reward package/item
and takes the kind from the referenced row at `rewarditem - 1`. Otherwise it
uses the selected row's kind. The setter receives code `22`, that kind,
zero price, zero chosen count, the selected reward reference or zeroes,
and zero reward count. Those setter zeroes are not additional widget
return values. Sources: `widget/retaineritemlistwidget.lua:8229-8304,9370-9444`
and `widget/ask/retaineritemlistwidget.lua:5205-5284,6536-6620` below
`lua/scripts/`. Original prototypes are `0.55/0.70` and `0.50/0.66`.

The original chunks were decoded with `tools/retail_script.py:decode_lpb`
and read with `tools/build_quest_contracts.py:ChunkReader/instruction`
using Python 3.12.0. Prototype indices and PCs are zero-based. The
[retainer event contract](bazaar-retainer-client-contracts.md#retainer-withdrawal-event-result)
owns the caller interpretation and decoded payload identities.
