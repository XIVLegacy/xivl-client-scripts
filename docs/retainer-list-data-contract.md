# Ask RetainerItemListWidget item sources and list data

The Ask resource `lua/scripts/widget/ask/retaineritemlistwidget.lua` contains
local item-source selection, list population, sorting, backup and comparison
helpers. The nine methods below describe Lua accesses, calls, writes and
returns. Conditional composition requires the selected pinned closures and
normal completion of intervening accesses and calls. The helper bodies alone
do not establish a caller or historical invocation.

Calls to outside helpers remain opaque. A UI request does not establish
rendering, storage, readback or focus. Neither a getter nor a local backup
establishes inventory truth, roster ownership, ward behavior, object lifetime,
accepted mutation or transaction settlement. Metamethods and native coercion
are outside the ordinary table and primitive-value cases described here.

## Resource identity

- LPB `n1635q/9rz/s5q91w5s1q5xy1rqn1635q.le.lpb`, 50376 bytes, SHA-256
  `CF7DA0872C6EB1743C9A2C73C11769022D030BDCE1F67CFA4FE2A8EF9127E81E`:
  `manifests/retail_lua_coverage.json:26642-26655`.
- Decoded payload, 50363 bytes, SHA-256
  `408CF496ED3FCDA95C53A6925CC9C8E689C517E37893E6D566E55E0A64AAE469`.
- Canonical LF source, 156026 bytes and 6813 lines, SHA-256
  `854328615DFAC84F08861DA2157300EDFAD67D63010783EBD7F520969C2521E6`:
  `manifests/scripts.json:15140-15144`.
- Class and method metadata: `lua/registry.json:39614-39700` and
  `xivl-client-structs:manifests/lua_api_contract.json:152947-153908`.

Decoding used `tools/retail_script.py`, SHA-256
`765327CF3DA90AACF8E36B185CE53AA0615F7705E9F9CCDC3A7243E3B6C0C391`,
and `tools/vendor/unluac/unluac_2025_12_23.jar`, 796256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
Instruction operands and offsets use
`tools/build_quest_contracts.py:ChunkReader` and `instruction`.

The [list and focus contract](retainer-list-focus-contract.md) owns its
separate helper methods. The [cancel contract](retainer-item-list-cancel-contract.md)
and [widget result contract](retainer-widget-results.md) own their selected
command and result paths.

## Item-source selection

`displayBagcapacityAndMoney(self)` captures the first result of
`self.getListBoxItemNum(self,1)`. It then requests
`self.setText(self,"TextBlock_Gil",3263,work.retainerMoneyCount)` and
`self.setText(self,"TextBlock_ItemStack_2",3551,count,work.retainerBagCapacity)`.
The count remains captured across the first text callback. Each work-field
read occurs at its later call preparation. Normal completion returns zero
values.

`isExistItem(self,A1,A2,A3)` selects these sources by exact mode equality:

| Mode A3 | Requests |
| --- | --- |
| nil or 1 | `worldMaster._getMyPlayer(worldMaster)`, then `_getItem(player,A1,A2)` |
| 2 | `desktopWidget.getBazaarItem(desktopWidget,A1,A2)` |
| 4 | `desktopWidget.getRetainerItem(desktopWidget,A1,A2)` |
| Other | No getter and zero return values |

Each supported source contributes its first result. Nil returns one literal
false. Every non-nil value, including false, returns one literal true. This
tests non-nil equality, rather than Lua truthiness or inventory existence.

`checkPackageAndIndex(self,A1,A2,A3,A4)` selects the same three sources using
A4 and supplies `(A2,A3)` to the item getter. It compares that first result
with A1 using Lua equality and returns one literal Boolean. Nil compared with
nil therefore returns true. Unsupported modes return zero values. Ordinary
table identity differs from structural equality; integer and floating-point
Lua numbers compare numerically, while false differs from zero.

## Literal money lookup

`getMoneyListIndex(self,A1)` makes no calls. Its ordered literal comparisons
return the values below. An unmatched input returns -1. The method supplies
no independent meaning or validity check for these identifiers.

| Input | Result | Input | Result |
| ---: | ---: | ---: | ---: |
| 1000001 | 1 | 1000102 | 2 |
| 1000101 | 3 | 1000103 | 4 |
| 1000107 | 5 | 1000106 | 6 |
| 1000104 | -1 | 1000108 | -1 |
| 1000109 | -1 | 1000105 | -1 |
| 1000111 | 11 | 1000110 | 12 |
| 1000112 | -1 | 1000113 | 14 |
| 1000114 | 15 | 1000115 | 16 |
| 1000116 | 17 | 1000117 | 18 |
| 1000118 | 19 | 1000119 | 20 |
| 1000120 | 21 | 1000121 | 22 |
| 1000122 | 23 | 1000123 | 24 |

## Sort requests

`setSortType(self,A1,A2,A3,A4)` requests
`desktopWidget.getRetainerItem(desktopWidget,A4,A2+1)`. A3 is unused.
A nil first result returns zero values immediately. Otherwise it requests
`desktopWidget.setSortType(desktopWidget,self,A1,A2,work.sorttype,item)`,
reading sorttype after the getter, and returns zero values.

`updateSortType(self)` captures, in order, the first results of
`getListPropertyName(self,1)`, `getPackageFromList(self,1)` and
`getListBoxItemNum(self,1)`. For row 1 through the captured count, it requests
`self.setSortType(self,property,row-1,work.sorttype,package)`. Sorttype is
read anew for each request. It then requests
`self.updateListProperty(self,property)` and returns zero values. A zero
count skips sorting but still requests the final property update. The local
composition with the preceding helper is conditional on that binding.

## Package list population

`makeListFromPackage(self,A1,A2)` uses full-list mode when A2 is nil and
one-row mode otherwise. Full-list mode processes these independent blocks:

| Package A1 | List | Capacity field |
| ---: | ---: | --- |
| 1 | 1 | `retainerBagCapacity` |
| 100 | 2 | `retainerMoneyCapacity` |
| 8 | 3 | `retainerBazaarCapacity` |

A nil A1 runs all three blocks in that order. Another package skips all
three blocks and still reaches the final display request.

Within each selected block, only a capacity exactly equal to numeric zero
requests `desktopWidget.getRetainerItemPackageCapacity(desktopWidget,package)`
and assigns its first result. The work-table destination is captured before
that getter. The `setControlProperty` function and receiver are captured
before requesting `getListBoxName(self,list)`. The later SourceCount request
uses the box result and a fresh capacity read:
`setter(self,box,"SourceCount",capacity)`.

The bag block captures property name and old row count before lazy capacity
handling, then reads the capacity after it. Money captures its property name
before that handling, then reads capacity and old count in that order. Bazaar
handles capacity first, then captures capacity, old count and property name in
that order. For source slot 1 through the captured capacity each block requests
`self.setItemToXmlLight(self,list,newCount,package,slot,4)`. Only a first
result exactly equal to literal true advances newCount. The first other
result breaks the population loop. If oldCount exceeds newCount, the method
uses a numeric loop from newCount through oldCount-1 with step 1. On each
iteration it decrements the captured oldCount and requests
`deleteListProperty(self,property,oldCount)`. For integer counts this deletes
oldCount-1 down through newCount; fractional counts retain the numeric loop's
unit-step behavior. The bag and money blocks then request
`updateListProperty(self,property)`. A nonempty Bazaar block instead requests
`updateBazaarLabel(self,3,4)`; an empty one requests the property update.

The money block sets `moneyIndex` and `moneyCount` to zero before population.
Afterward it copies fresh values of those fields into `retainerMoneyIndex`
and `retainerMoneyCount`. These are separate accesses and assignments.

In one-row mode, packages 1, 100 and 8 select lists 1, 2 and 3. Another package
returns zero values before the final display request. The same exact-zero
capacity handling applies. Within the money capacity-refill branch only,
A2 equal to `retainerMoneyIndex` clears `moneyIndex` and `moneyCount` to zero;
otherwise those fields receive fresh values from the retainer pair.

The method then captures the list property name and requests
`getRetainerItem(desktopWidget,A1,A2)`. A non-nil result, including false,
requests `setItemToXmlLight(self,list,A2-1,A1,A2,4)` and discards all results.
For money, it compares `moneyIndex` with `retainerMoneyIndex`. If those match,
it instead compares `moneyCount` with `retainerMoneyCount`. A difference in
the compared pair copies fresh local fields to the retainer pair. Those
comparisons do not write either local money field. A nil item
instead requests the list's current count, deletes index count-1, and requests
a property update. In that branch, money with A2 equal to the current
`retainerMoneyIndex` clears the retainer pair to zero.

Normal fallthrough requests `self.displayBagcapacityAndMoney(self)` and
returns zero values. There is no index-range validation here. Nil capacity
and other unsupported arithmetic or indexing values can fail before that
fallthrough, and the outside row helper's meaning remains opaque.

## Backup and comparison

`copyItem(self)` requests a retainer item using fresh `work.chosenPackage`
and `work.chosenItem`. There is no nil guard before the first item method.
It uses that captured item for these ordered getters and backup assignments:

| Item getter | Destination field |
| --- | --- |
| `_getCatalogID` | `bakcatalog` |
| `_getNameIndex` | `bakquality` |
| `_countStack` | `bakstack` |
| `isRareItem` | `bakrare` |
| `isExclusiveItem` | `bakex` |

For each row, the work-table destination is captured before invoking that
getter. Each call takes only the item receiver and uses its first result.
After those five callbacks, a fresh `chosenPackage == 8` comparison selects
the deal branch. That branch rereads chosen package and index, requests three
results from `getRetainerItemDealData`, and assigns the first two to
`bakbazaarkind` and `bakprice`. Their work destinations are read separately
after the deal call. The attachment destination is captured before the
`isRetainerItemAttached` call, whose package and index are read anew.
Its first result is assigned to `bakattached`. Normal completion returns
zero values. These reads and callbacks do not form an atomic snapshot.

`isSameItem(self,A1,A2)` gets the first result from
`getRetainerItem(desktopWidget,A1,A2)`. Nil returns one literal false. A
non-nil item is rejected only when its first `_isAlive` result equals literal
false. Nil and zero from that getter do not trigger this rejection.
The method then compares these backup fields and item getters in order:
`bakcatalog/_getCatalogID`, `bakquality/_getNameIndex`,
`bakrare/isRareItem`, `bakex/isExclusiveItem`, `bakstack/_countStack`.
Each backup value is read before the corresponding callback. The first
unequal comparison returns one literal false.

For A1 exactly 8, it requests three deal results and compares the first two
with the freshly read `bakbazaarkind` and `bakprice`, returning false on
either mismatch. It captures `bakattached` before requesting attachment and
compares that first result. All comparisons passing returns one literal true.
Compiler-emitted bare return words do not imply an additional reachable
zero-result outcome. The comparison uses Lua equality, not a native identity,
inventory generation or transaction check.

## Instruction and call records

The following ledger covers only direct children 10, 11, 12, 23, 24, 25, 30,
31 and 32. Each has zero nested children. Arity includes the receiver.
PCs are zero-based. Byte offsets name the first and last instruction-word
starts in the decoded payload; the last word extends three bytes further.
Root bindings are `SETTABLE` attempts, without runtime installation evidence.

| Method | Proto | LF lines | Debug lines | Arity | Stack | Words | First/last word starts | Root PC/offset |
| --- | ---: | --- | --- | ---: | ---: | ---: | --- | --- |
| `displayBagcapacityAndMoney` | 10 | 1111-1134 | 497-502 | 1 | 8 | 17 | 10635/10699 | 39/188 |
| `isExistItem` | 11 | 1137-1187 | 513-534 | 4 | 9 | 49 | 10911/11103 | 42/200 |
| `checkPackageAndIndex` | 12 | 1190-1240 | 548-569 | 5 | 10 | 49 | 11283/11475 | 45/212 |
| `getMoneyListIndex` | 23 | 1678-1810 | 852-977 | 2 | 4 | 129 | 15291/15803 | 78/344 |
| `setSortType` | 24 | 1813-1836 | 989-995 | 5 | 13 | 18 | 16081/16149 | 81/356 |
| `updateSortType` | 25 | 1839-1871 | 1003-1010 | 1 | 13 | 24 | 16284/16376 | 84/368 |
| `makeListFromPackage` | 30 | 2631-3031 | 1279-1431 | 3 | 18 | 366 | 21211/22671 | 99/428 |
| `copyItem` | 31 | 3034-3097 | 1439-1454 | 1 | 10 | 52 | 23262/23466 | 102/440 |
| `isSameItem` | 32 | 3100-3200 | 1461-1500 | 3 | 12 | 88 | 23873/24221 | 105/452 |

Each LF window includes both endpoint lines and retains LF terminators.

| Method | Window bytes | SHA-256 |
| --- | ---: | --- |
| `displayBagcapacityAndMoney` | 541 | `10216D6EDE537347EEA63771D6DF85011DEF12036687BD3487B344B4E00EBD3C` |
| `isExistItem` | 1008 | `85C5769109244CF0C3EA90F1C92FF7DD316DDA36B59BCEFD3CEA8ABA117B115D` |
| `checkPackageAndIndex` | 1026 | `227B09F61CA768152F4C886682CFC6F8A029B4669EFE0455F310369B5352EA79` |
| `getMoneyListIndex` | 1987 | `FEE5F4FCB7368E8205D6EECF12E16576A36C4325DED0856E804034516C04BBB2` |
| `setSortType` | 513 | `137EE44F1229D4ED288C3A3E65E7F443E912D1B2C2B7D1F30D5C6E602A5098E1` |
| `updateSortType` | 716 | `53DBC2C3C9AEE54AEF186BC5EA09BE4D06B7CF33F7BA0BB1DE3795510F947E75` |
| `makeListFromPackage` | 10478 | `9FA0CBD982C23C11CE2B8AD38D126E4F850EFC0A56C564FD22A630C9C7E65EC7` |
| `copyItem` | 1472 | `D919693D5A6237F62F926338AB9F47693DE3FD4187F302561A7A35809ADCAAAF` |
| `isSameItem` | 1977 | `D45B51A5D5DB4D99D2EEB9ABEF158151B9D1539DD7B4917803C24F21D1BC29F4` |

### Direct-call operands

All 76 direct CALL words have fixed arguments and fixed results. At a
CALL with base register A, R(A) is the captured function and registers
R(A+1) through R(A+B-1) are the complete actual argument vector, including
the receiver for SELF calls. C-1 is the requested result count. Short
returns are padded with nil; longer returns are truncated. A zero-result
request discards all results. The SELF column gives the preceding capture
of that function and receiver, rather than a native binding guarantee.

| Method | CALL PC/offset | A/B/C | Captured SELF PC/key/receiver register | Argument registers | Results |
| --- | --- | --- | --- | --- | ---: |
| `displayBagcapacityAndMoney` | 2/10643 | 1/3/2 | 0/`getListBoxItemNum`/R0 | R2,R3 | 1 |
| `displayBagcapacityAndMoney` | 8/10667 | 2/5/1 | 3/`setText`/R0 | R3,R4,R5,R6 | 0 |
| `displayBagcapacityAndMoney` | 15/10695 | 2/6/1 | 9/`setText`/R0 | R3,R4,R5,R6,R7 | 0 |
| `isExistItem` | 6/10935 | 4/2/2 | 5/`_getMyPlayer`/R4 | R5 | 1 |
| `isExistItem` | 10/10951 | 5/4/2 | 7/`_getItem`/R4 | R6,R7,R8 | 1 |
| `isExistItem` | 25/11011 | 4/4/2 | 22/`getBazaarItem`/R4 | R5,R6,R7 | 1 |
| `isExistItem` | 40/11071 | 4/4/2 | 37/`getRetainerItem`/R4 | R5,R6,R7 | 1 |
| `checkPackageAndIndex` | 6/11307 | 5/2/2 | 5/`_getMyPlayer`/R5 | R6 | 1 |
| `checkPackageAndIndex` | 10/11323 | 6/4/2 | 7/`_getItem`/R5 | R7,R8,R9 | 1 |
| `checkPackageAndIndex` | 25/11383 | 5/4/2 | 22/`getBazaarItem`/R5 | R6,R7,R8 | 1 |
| `checkPackageAndIndex` | 40/11443 | 5/4/2 | 37/`getRetainerItem`/R5 | R6,R7,R8 | 1 |
| `setSortType` | 4/16097 | 5/4/2 | 1/`getRetainerItem`/R5 | R6,R7,R8 | 1 |
| `setSortType` | 16/16145 | 6/7/1 | 9/`setSortType`/R6 | R7,R8,R9,R10,R11,R12 | 0 |
| `updateSortType` | 2/16292 | 1/3/2 | 0/`getListPropertyName`/R0 | R2,R3 | 1 |
| `updateSortType` | 5/16304 | 2/3/2 | 3/`getPackageFromList`/R0 | R3,R4 | 1 |
| `updateSortType` | 9/16320 | 4/3/2 | 7/`getListBoxItemNum`/R0 | R5,R6 | 1 |
| `updateSortType` | 18/16356 | 7/6/1 | 12/`setSortType`/R0 | R8,R9,R10,R11,R12 | 0 |
| `updateSortType` | 22/16372 | 3/3/1 | 20/`updateListProperty`/R0 | R4,R5 | 0 |
| `makeListFromPackage` | 9/21247 | 7/3/2 | 7/`getListPropertyName`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 13/21263 | 7/3/2 | 11/`getListBoxItemNum`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 23/21303 | 8/3/2 | 21/`getRetainerItemPackageCapacity`/R8 | R9,R10 | 1 |
| `makeListFromPackage` | 28/21323 | 9/3/2 | 26/`getListBoxName`/R0 | R10,R11 | 1 |
| `makeListFromPackage` | 32/21339 | 7/5/1 | 25/`setControlProperty`/R0 | R8,R9,R10,R11 | 0 |
| `makeListFromPackage` | 45/21391 | 11/7/2 | 39/`setItemToXmlLight`/R0 | R12,R13,R14,R15,R16,R17 | 1 |
| `makeListFromPackage` | 62/21459 | 11/4/1 | 59/`deleteListProperty`/R0 | R12,R13,R14 | 0 |
| `makeListFromPackage` | 66/21475 | 7/3/1 | 64/`updateListProperty`/R0 | R8,R9 | 0 |
| `makeListFromPackage` | 77/21519 | 7/3/2 | 75/`getListPropertyName`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 87/21559 | 8/3/2 | 85/`getRetainerItemPackageCapacity`/R8 | R9,R10 | 1 |
| `makeListFromPackage` | 92/21579 | 9/3/2 | 90/`getListBoxName`/R0 | R10,R11 | 1 |
| `makeListFromPackage` | 96/21595 | 7/5/1 | 89/`setControlProperty`/R0 | R8,R9,R10,R11 | 0 |
| `makeListFromPackage` | 102/21619 | 7/3/2 | 100/`getListBoxItemNum`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 114/21667 | 11/7/2 | 108/`setItemToXmlLight`/R0 | R12,R13,R14,R15,R16,R17 | 1 |
| `makeListFromPackage` | 131/21735 | 11/4/1 | 128/`deleteListProperty`/R0 | R12,R13,R14 | 0 |
| `makeListFromPackage` | 135/21751 | 7/3/1 | 133/`updateListProperty`/R0 | R8,R9 | 0 |
| `makeListFromPackage` | 156/21835 | 8/3/2 | 154/`getRetainerItemPackageCapacity`/R8 | R9,R10 | 1 |
| `makeListFromPackage` | 161/21855 | 9/3/2 | 159/`getListBoxName`/R0 | R10,R11 | 1 |
| `makeListFromPackage` | 165/21871 | 7/5/1 | 158/`setControlProperty`/R0 | R8,R9,R10,R11 | 0 |
| `makeListFromPackage` | 171/21895 | 7/3/2 | 169/`getListBoxItemNum`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 175/21911 | 7/3/2 | 173/`getListPropertyName`/R0 | R8,R9 | 1 |
| `makeListFromPackage` | 187/21959 | 11/7/2 | 181/`setItemToXmlLight`/R0 | R12,R13,R14,R15,R16,R17 | 1 |
| `makeListFromPackage` | 204/22027 | 11/4/1 | 201/`deleteListProperty`/R0 | R12,R13,R14 | 0 |
| `makeListFromPackage` | 211/22055 | 7/4/1 | 208/`updateBazaarLabel`/R0 | R8,R9,R10 | 0 |
| `makeListFromPackage` | 215/22071 | 7/3/1 | 213/`updateListProperty`/R0 | R8,R9 | 0 |
| `makeListFromPackage` | 229/22127 | 9/3/2 | 227/`getRetainerItemPackageCapacity`/R9 | R10,R11 | 1 |
| `makeListFromPackage` | 234/22147 | 10/3/2 | 232/`getListBoxName`/R0 | R11,R12 | 1 |
| `makeListFromPackage` | 238/22163 | 8/5/1 | 231/`setControlProperty`/R0 | R9,R10,R11,R12 | 0 |
| `makeListFromPackage` | 250/22211 | 9/3/2 | 248/`getRetainerItemPackageCapacity`/R9 | R10,R11 | 1 |
| `makeListFromPackage` | 255/22231 | 10/3/2 | 253/`getListBoxName`/R0 | R11,R12 | 1 |
| `makeListFromPackage` | 259/22247 | 8/5/1 | 252/`setControlProperty`/R0 | R9,R10,R11,R12 | 0 |
| `makeListFromPackage` | 289/22367 | 9/3/2 | 287/`getRetainerItemPackageCapacity`/R9 | R10,R11 | 1 |
| `makeListFromPackage` | 294/22387 | 10/3/2 | 292/`getListBoxName`/R0 | R11,R12 | 1 |
| `makeListFromPackage` | 298/22403 | 8/5/1 | 291/`setControlProperty`/R0 | R9,R10,R11,R12 | 0 |
| `makeListFromPackage` | 304/22427 | 8/3/2 | 302/`getListPropertyName`/R0 | R9,R10 | 1 |
| `makeListFromPackage` | 310/22451 | 8/4/2 | 307/`getRetainerItem`/R8 | R9,R10,R11 | 1 |
| `makeListFromPackage` | 319/22487 | 8/7/1 | 313/`setItemToXmlLight`/R0 | R9,R10,R11,R12,R13,R14 | 0 |
| `makeListFromPackage` | 345/22591 | 8/3/2 | 343/`getListBoxItemNum`/R0 | R9,R10 | 1 |
| `makeListFromPackage` | 349/22607 | 9/4/1 | 346/`deleteListProperty`/R0 | R10,R11,R12 | 0 |
| `makeListFromPackage` | 352/22619 | 9/3/1 | 350/`updateListProperty`/R0 | R10,R11 | 0 |
| `makeListFromPackage` | 364/22667 | 7/2/1 | 363/`displayBagcapacityAndMoney`/R0 | R8 | 0 |
| `copyItem` | 6/23286 | 1/4/2 | 1/`getRetainerItem`/R1 | R2,R3,R4 | 1 |
| `copyItem` | 9/23298 | 3/2/2 | 8/`_getCatalogID`/R1 | R4 | 1 |
| `copyItem` | 13/23314 | 3/2/2 | 12/`_getNameIndex`/R1 | R4 | 1 |
| `copyItem` | 17/23330 | 3/2/2 | 16/`_countStack`/R1 | R4 | 1 |
| `copyItem` | 21/23346 | 3/2/2 | 20/`isRareItem`/R1 | R4 | 1 |
| `copyItem` | 25/23362 | 3/2/2 | 24/`isExclusiveItem`/R1 | R4 | 1 |
| `copyItem` | 37/23410 | 2/4/4 | 32/`getRetainerItemDealData`/R2 | R3,R4,R5 | 3 |
| `copyItem` | 49/23458 | 6/4/2 | 44/`isRetainerItemAttached`/R6 | R7,R8,R9 | 1 |
| `isSameItem` | 4/23889 | 3/4/2 | 1/`getRetainerItem`/R3 | R4,R5,R6 | 1 |
| `isSameItem` | 10/23913 | 4/2/2 | 9/`_isAlive`/R3 | R5 | 1 |
| `isSameItem` | 18/23945 | 5/2/2 | 17/`_getCatalogID`/R3 | R6 | 1 |
| `isSameItem` | 26/23977 | 5/2/2 | 25/`_getNameIndex`/R3 | R6 | 1 |
| `isSameItem` | 34/24009 | 5/2/2 | 33/`isRareItem`/R3 | R6 | 1 |
| `isSameItem` | 42/24041 | 5/2/2 | 41/`isExclusiveItem`/R3 | R6 | 1 |
| `isSameItem` | 50/24073 | 5/2/2 | 49/`_countStack`/R3 | R6 | 1 |
| `isSameItem` | 61/24117 | 4/4/4 | 58/`getRetainerItemDealData`/R4 | R5,R6,R7 | 3 |
| `isSameItem` | 80/24193 | 8/4/2 | 77/`isRetainerItemAttached`/R8 | R9,R10,R11 | 1 |

### Verification boundary

The selected 792 instruction words contain no TEST or TESTSET. The
original-word fixtures check 69 authored cases and seven corruption
controls. All normal results use recursive typed comparisons; selected
cases additionally assert raw function or receiver identity, complete
argument vectors, branch successors, writes and chronological effects.
Callback cases distinguish captured counts, setters, backup values and
write destinations from later reads. Two cases demonstrate ordinary
nil-item indexing or nil-capacity arithmetic failure. This is finite
branch evidence, without exhaustive input or metamethod coverage.
