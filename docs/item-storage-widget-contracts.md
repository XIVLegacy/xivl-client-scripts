# Item-storage widget contracts

The official [Patch 1.22 notes](https://forum.square-enix.com/ffxiv/threads/43599),
2012-04-25, `[dev1357]`, introduced the inn-room Armoire for storing and
retrieving selected gear in four categories. This supplies the product
context for these generic client widgets. A specific spawned actor and a
successful server transaction remain separate evidence questions.

`ItemStoragePutWidget` and `ItemStorageGetWidget` expose item-selection values
through their ask results and read player-storage APIs for presentation. These
client calls do not establish a completed storage mutation or its persistence
policy.

## ObjectItemStorage actor boundary

The original `ObjectItemStorage` actor initializes its work state, loads text
data 10272 named `objectItemStorage`, and turns its ground state off in
`initForEvent` (`objectitemstorage.lua:11-31`). Its `storageMenu` calls
`worldMaster:ask(self, self, 1, 4)` and returns 1, 2, 3, or 4; result 3 also
issues `worldMaster:say` calls with numeric IDs 6 and 7
(`objectitemstorage.lua:34-70`). The script does not assign product meanings
to those numeric menu results.

`selectCategory` returns the result of `worldMaster:ask(self, self, 8, 5)`
unchanged (`objectitemstorage.lua:73-86`). `selectStoreItem` yields
`Ask/ItemStoragePutWidget` in mode 1 and `selectReceiveItem` yields
`Ask/ItemStorageGetWidget` in mode 1, passing their third argument unchanged;
each returns the widget's second yield value only when the first yield value is
true, and otherwise returns nil (`objectitemstorage.lua:89-130`). This actor
prototype calls the generic storage widgets directly and contains no Entrust
API call or native category mapping; those meanings remain outside this Lua
contract.

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
| `lua/scripts/chara/npc/object/objectitemstorage.lua` | `fc331b51bc957ae1a663a5a7edaab667d85004ef32011f5f37572a6161add5e4` | `fc331b51bc957ae1a663a5a7edaab667d85004ef32011f5f37572a6161add5e4` | `729s9/wu7/v8057q/v8057q1q5xrqvs935.le.lpb`; LPB SHA-256 `e0b4270c835a12bc2ee2f9eb04e761e98872ae7b4e8bb7e759dba0063764c562`; decoded payload SHA-256 `f2b1b7c117862d6a55428925e412937a7d69ce66b2f1367688a96ac5fada1d31` |

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

The actor boundary above was decompiled from the pinned
`ObjectItemStorage` LPB; its 1,299-byte decoded payload has SHA-256
`f2b1b7c117862d6a55428925e412937a7d69ce66b2f1367688a96ac5fada1d31`, and
the reviewed output has SHA-256
`fc331b51bc957ae1a663a5a7edaab667d85004ef32011f5f37572a6161add5e4`.
The method locators are `initForEvent:11-31`, `storageMenu:34-70`,
`selectCategory:73-86`, `selectStoreItem:89-108`, and
`selectReceiveItem:111-130` in that output.
