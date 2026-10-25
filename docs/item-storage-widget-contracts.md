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
unchanged (`objectitemstorage.lua:73-86`). `selectStoreItem` requests one
result from `Ask/ItemStoragePutWidget`, and `selectReceiveItem` requests one
result from `Ask/ItemStorageGetWidget`, passing their third argument
unchanged. Each returns the widget's second yield value only when the first
yield value is true, and otherwise returns nil
(`objectitemstorage.lua:89-130`). This actor prototype calls the generic
storage widgets directly and contains no Entrust API call or native category
mapping; those meanings remain outside this Lua contract.

The returned catalog ID or nil is a callback result, not a mutation
acknowledgement. If this actor callback is invoked through the normal event
callback path, the existing generic contract collects typed callback results
and serializes them into c2s `0x012E` EventUpdate, including the typed nil path
(`passivegl-dialogue-producer.md:145-171`; `xivl-client-structs:structs/network/event-update.md:1-6,35-38`).
No Armoire invocation of that native event route or successful storage
mutation was observed here.

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

## Confirmation and transaction boundary

The put selection handler opens `ItemStorageDialogWidget` with dialog type `1`
and the presentation tuple `catalog, icon, quality, name, cantEquip,
canChangeFitness, polishProgress, materializePermission`. The get selection
handler opens the same child with dialog type `2` and the selected stored-item
value. These calls select a row and populate a modal; they do not submit a
storage operation (`itemstorageputwidget.lua:2081-2101` and
`itemstoragegetwidget.lua:1732-1751`).

The dialog's OK and Cancel conditions call the parent's confirmation methods.
`processUICommandOperate` maps `Button_OK` to operation `1` and
`Button_Cancel` to operation `2`; the keyboard cancel path maps
`Button_Cancel` to operation `2` as well (`itemstoragedialogwidget.lua:366-435`).
The put and get widgets only store that operation in `work.chosenOperation`
(`itemstorage{put,get}widget.lua:2723-2729,2145-2151`).

On close, both widgets treat operation `1` as local confirmation: they call
`setBaseAskResult(1)`, disable input, and set `waitNext`. Operation `2` clears
the edit state, clears the selected border, and re-enables input. Both paths
then reset the operation, close `ItemStorageDialogWidget`, update the server
time field, and refresh the window (`itemstorageputwidget.lua:2732-2796`,
`itemstoragegetwidget.lua:2154-2218`). No request, command ID, item removal,
item insertion, or result callback is emitted by these inspected confirmation
handlers. The dialog's `_sendStoryboardCommand` calls are presentation effects
only (`itemstoragedialogwidget.lua:335,344`).

The storage widgets' own operate and cancel handlers likewise only handle
sorting, focus, and previous-sequence state; they do not hand off a request
(`itemstorageputwidget.lua:1722-1796`, `itemstoragegetwidget.lua:1584-1620`).

The generic `DesktopWidget.askEventModeWidgetYield` helper is also a local
widget continuation. It delegates to `askWidgetYield`, which opens and selects
the widget, reads `widget.getAskResult()`, closes the widget, and returns the
local values (`desktopwidget_connector.lua:25787-25856`). It is not a server
request or a persistence acknowledgement.

The inspected bodies establish selection, confirmation, cancellation, and
local result return. The generic event contract supplies the conditional
reply transport. The server's store/retrieve handling, successful inventory
and storage transition, and update ordering remain unbound. The mapped native
`SetPlayerItemStoragePacket` entry (`0x01A5`) is a clientbound state receiver,
not evidence of a Lua request. The opcode record in
`xivl-opcodes:opcodes.json:5250-5261` and the capture index entry in
`xivl-captures:derived/opcode_names.json:3177-3185` have no observed capture;
the opcode record explicitly has `observedIn: []` and `payloadLengths: []`,
while the capture index has `observedIn: []`. Therefore actual retail storage
or retrieval mutation status is unresolved here; the absent 0x01A5 sample only
limits indexed capture evidence. A selected ID, presentation tuple, or
returned ask value is not persistence proof.

The retained actor and event-caller evidence is recorded in
`xivl-captures:studies/armoire-event-caller-census/README.md`.

| Decoded script | Canonical source SHA-256 | Reviewed decompile output SHA-256 | LPB and decoded-payload identity |
| --- | --- | --- | --- |
| `lua/scripts/widget/ask/itemstorageputwidget.lua` | `4086c717edd9828ca9eb054aade1c327c7878742cf12cd483bb1f105f43a55f8` | `782ab27bea7969bc2ecf8b91b8f7e5a44fa0fa044ec43557e8a9b9b9ba8d7f1f` | `n1635q/9rz/1q5xrqvs935upqn1635q.le.lpb`; LPB SHA-256 `8e835166f07c2e5204efbf1d7dd2ebba1fc4477bf0ed836bade956e3c51170f6`; decoded payload SHA-256 `756d290ad8b1a89711e095fcc11b65dbaa633992419e3d9abd3d5e0072b4a0ab` |
| `lua/scripts/widget/ask/itemstoragegetwidget.lua` | `c3f63428d9fa499e77b8bbbd1f79ff2d9c519cc1a601804f8d44fadd81a08640` | `9cacb12d4a04769facc779389ada0e54b221053c7be4cfe74c813846d0c8249f` | `n1635q/9rz/1q5xrqvs93535qn1635q.le.lpb`; LPB SHA-256 `b768c0719f38fc1555d29eeb3a9d3bad3af31ab28aa1a368fc09364e8c277c31`; decoded payload SHA-256 `f3de6468acee403b381a16a8451f6a33d484bf5333eb65e75fc7bc52a9093585` |
| `lua/scripts/widget/itemstoragedialogwidget.lua` | `3382e5472aa63a954b9569df58543a09b5fdf710b79e5ac856a022a7617b02ae` | `3382e5472aa63a954b9569df58543a09b5fdf710b79e5ac856a022a7617b02ae` | `n1635q/1q5xrqvs935619yv3n1635q.le.lpb`; LPB SHA-256 `f01e4b59b2fb97d424e7746dbe1d3cdf002f61f2190afe9eb53b23f907a1871`; decoded payload SHA-256 `e4ffbf1855d4ce52860a1a0fc0541e7049bf4374a6bf7a06dff294acc5cbe804` |
| `lua/scripts/widget/desktopwidget_connector.lua` | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`; LPB SHA-256 `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`; decoded payload SHA-256 `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
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

## Ul'dah inn desk return boundary

`DftWil.defaultTalkWithInn_Desk` and `defaultTalkWithInn_Desk_2` have different
return contracts. The former returns no values. Its menu call is
`worldMaster:askRestrictChoices(self, self, 588, false, true, true, false, true)`.
Results 2 and 3 select explanatory dialogue and repeat the menu. Result 5 or
nil finishes the talk and returns zero values; other results repeat the menu.
A caller cannot obtain an entry or homepoint selector from this method's return.

`defaultTalkWithInn_Desk_2` asks the supplied actor with
`askExtendWidget(self, 588, 5, 1, 1)`. Result 1 says row 648 and returns that
single value immediately, without finishing the talk. Results 2 and 3 display
explanatory rows and repeat. Result 4 opens a second question using
`askExtendWidget(worldMaster, 60016, 2, 1, 1)`. Confirmation 1 finishes the
talk and returns numeric 2; other confirmation results repeat the first menu.
First-menu results 5, -3 or nil finish the talk and return zero values.
Other first-menu results repeat. Neither method performs a zone change or
storage transaction; the caller owns any action on a returned value.

Original source: `client/script/tp5rq/r75w9s1v/6549pyqq9yz/64qn1y.le.lpb`,
SHA-256 `f9305122e98522b72baee7bf405a04ebf30468d4c52187dc1445acea7daa93c2`;
decoded payload SHA-256
`577dcc3f9fa49b22f92a1ad160253cf2ee6df9473d47d666cf8dbe536e0a7bb1`.
The resource is pinned in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) as
`lua/scripts/quest/scenario/defaulttalk/dftwil.lua`.
`root/proto284` starts at decoded offset 78408; its only return is zero-based
PC 72, `RETURN R0 B=1`. `root/proto287` starts at offset 79365: PC 34 returns
the saved result 1, PCs 83-86 load and return 2 after finishing, and PCs 89-91
finish and return zero values. These are original-bytecode paths, not evidence
of server handling or equivalence with similarly named methods in other classes.
