# Item-storage widget contracts

`ItemStoragePutWidget` and `ItemStorageGetWidget` expose item-selection values
through their ask results and read player-storage APIs for presentation. These
client calls do not establish a completed storage mutation or its persistence
policy.

`ItemStoragePutWidget.getAskResult` returns a value only when the base ask
result is `1`. It resolves the selected package and item index, reads the live
item's `_getCatalogID()` when that item exists, and otherwise reads the
selected row's `catalog` property. A nonpositive catalog ID becomes `nil`.
The item-display path also calls `MyPlayer._canStoreItem(category,
catalogId)` and rejects the item when the call returns false. Neither call
reveals the native eligibility rule or proves that a selected item was stored.

`ItemStorageGetWidget` populates its list using
`MyPlayer._countStoredItem(category)` and
`MyPlayer._getStoredItem(category, index)`. On base ask result `1`,
`getAskResult` returns the selected `_getStoredItem` value for the category;
nonpositive values become `nil`. The Lua does not establish the native value's
full semantics or a successful removal transaction.

| Decoded script | Canonical source SHA-256 | Reviewed decompile output SHA-256 | LPB and decoded-payload identity |
| --- | --- | --- | --- |
| `lua/scripts/widget/ask/itemstorageputwidget.lua` | `4086c717edd9828ca9eb054aade1c327c7878742cf12cd483bb1f105f43a55f8` | `782ab27bea7969bc2ecf8b91b8f7e5a44fa0fa044ec43557e8a9b9b9ba8d7f1f` | `n1635q/9rz/1q5xrqvs935upqn1635q.le.lpb`; LPB SHA-256 `8e835166f07c2e5204efbf1d7dd2ebba1fc4477bf0ed836bade956e3c51170f6`; decoded payload SHA-256 `756d290ad8b1a89711e095fcc11b65dbaa633992419e3d9abd3d5e0072b4a0ab` |
| `lua/scripts/widget/ask/itemstoragegetwidget.lua` | `c3f63428d9fa499e77b8bbbd1f79ff2d9c519cc1a601804f8d44fadd81a08640` | `9cacb12d4a04769facc779389ada0e54b221053c7be4cfe74c813846d0c8249f` | `n1635q/9rz/1q5xrqvs93535qn1635q.le.lpb`; LPB SHA-256 `b768c0719f38fc1555d29eeb3a9d3bad3af31ab28aa1a368fc09364e8c277c31`; decoded payload SHA-256 `f3de6468acee403b381a16a8451f6a33d484bf5333eb65e75fc7bc52a9093585` |

Source locators in the reviewed decompile outputs: `ItemStoragePutWidget` item
eligibility and `getAskResult` (`itemstorageputwidget.lua:461-484,1399-1444`);
stored-item list and result (`itemstoragegetwidget.lua:532-554,959-976`). The
output hashes pin these line locators. The canonical call maps separately list
`_canStoreItem` at source line `1122` and `_getCatalogID` at `1118, 1556,
1959, 2136, 2651` (`itemstorageputwidget.calls.json:11-12,20-28`), plus
`_countStoredItem` at `1302` and `_getStoredItem` at `1340, 1733, 2086`
(`itemstoragegetwidget.calls.json:14-15,56-60`). Those are source callsite
indexes, not decompile-output line locators; in particular, the call map does
not distinguish which `_getStoredItem` call supplies the selected result.
Canonical source hashes are pinned in `manifests/scripts.json`, and LPB
identities and decoded payload hashes are pinned in
`manifests/retail_lua_coverage.json`.
