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

`Ask/RetainerItemListWidget` returns:

- `13`: `(13, chosenPackage, chosenItem)` for the selected list item; it does
  not return a count.
- `21`: the ordered tuple `(21, resultPackage, resultItem, bazaartype,
  rewardPrice, rewardPackage, rewardItem, resultCount, rewardCount)`. Its
  bazaar-edit setter copies the selected package and item into `resultPackage`
  and `resultItem`.

These are UI result values and selected fields only. They do not establish
whether codes 31, 32, 13, or 21 mean retrieve, entrust, list, remove, or any
other server operation. The retail client tuple does not by itself establish
that a server accepted or applied it.

Evidence: `lua/scripts/widget/retainertradewidget.lua:3188-3294,3691-3763`,
`lua/scripts/widget/retaineritemlistwidget.lua:9111-9132,9185-9207,9370-9444`,
and `lua/scripts/widget/ask/retaineritemlistwidget.lua:6222-6263,6323-6350,6536-6620`.
The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.
