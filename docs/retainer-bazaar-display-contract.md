# Ask RetainerItemListWidget row and Bazaar display contract

The Ask resource `widget/ask/retaineritemlistwidget` contains seven local
methods that prepare item rows, check reward references, and request Bazaar
labels or detail values. The recovered contract describes Lua instruction
behavior only. It does not assign native storage, rendering, focus, widget
lifetime, server, inventory, currency, transaction, withdrawal, settlement, or
reply behavior.

## Pinned resource

The public manifest identifies the source as
`lua/scripts/widget/ask/retaineritemlistwidget.lua`, 156026 bytes, 6813 LF
lines, SHA-256
`854328615DFAC84F08861DA2157300EDFAD67D63010783EBD7F520969C2521E6`:
`xivl-client-scripts:manifests/scripts.json:15140-15144`.

The selected LPB is the manifest entry for
`n1635q/9rz/s5q91w5s1q5xy1rqn1635q.le.lpb`, 50376 bytes, SHA-256
`CF7DA0872C6EB1743C9A2C73C11769022D030BDCE1F67CFA4FE2A8EF9127E81E`.
Its authenticated decoded payload is 50363 bytes, SHA-256
`408CF496ED3FCDA95C53A6925CC9C8E689C517E37893E6D566E55E0A64AAE469`.
The class and method name inventory is
`xivl-client-scripts:lua/registry.json:39614-39700`, and the resource requires
`/Widget/Ask/AskBaseClass`.

All offsets below are decoded payload byte offsets. Prototype PCs are zero
based. The reader first and last word starts are inclusive and use four-byte
instruction words.

| Method | Proto | Source LF | Window SHA256 | Debug lines | Arity | Stack | Reader first word | Reader last word | Words | CALL/TAILCALL | RETURN words | Nested | Root binding attempt |
| --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `setItemToXmlLight` | 22 | 1545-1675 | `46a83799962a7193ad52fe13fb1e8bf7c758f0050a5f488aa507099a360ecf91` | 771-843 | 6 | 39 | 14326 | 14774 | 113 | 11 | 5 | 0 | root PC75, offset332 |
| `setBazaarLabelVisibility` | 26 | 1874-2014 | `cab8e394146971ce9ff4c9e3cbd6ca78d4a3faf90bcafcfdf8d98bc871232010` | 1021-1049 | 4 | 14 | 16566 | 17066 | 126 | 19 | 1 | 0 | root PC87, offset380 |
| `updateBazaarLabel` | 27 | 2017-2324 | `5ef8197cf04f99bc04751797d233290b774a3af060dcd950cbbca2e5bf1d7a65` | 1060-1156 | 3 | 28 | 17467 | 18591 | 282 | 37 | 1 | 0 | root PC90, offset392 |
| `checkRewardDependency` | 28 | 2327-2553 | `4360089dc86b10c665d868629fe7978f8ad7f5ba528c5a729c449a794e22519a` | 1170-1228 | 4 | 19 | 19272 | 20108 | 210 | 25 | 8 | 0 | root PC93, offset404 |
| `isRewardItemActor` | 29 | 2556-2628 | `25c9aad854d4695837e510c7f13e5d57ca8a6531133d6692dc44aa96c1d2b8e3` | 1242-1270 | 6 | 14 | 20619 | 20943 | 82 | 7 | 8 | 0 | root PC96, offset416 |
| `getItemBazaarData` | 33 | 3203-3339 | `19425c8aeda3bafdb2c85ef9818cb768cd5079d6b2ab0d0e969d1535181522b1` | 1527-1599 | 7 | 35 | 24610 | 25118 | 128 | 14 | 2 | 0 | root PC108, offset464 |
| `displayBazaarGrid` | 34 | 3342-3932 | `05c7e73cc705319de6a4f982611c8c3a38e8dbf74dcafe52bfb57bdcd04707ce` | 1613-1782 | 7 | 36 | 25404 | 27396 | 499 | 105 | 2 | 0 | root PC111, offset476 |

The seven rows contain 1440 words, 218 direct CALL or TAILCALL words, and no
nested children. The root assignments are source-level binding attempts only;
they do not prove class installation or runtime readback.

All result statements require normal completion of the reads, comparisons,
arithmetic and calls on that path. An error is not a return. Any description
that composes these local helper bodies requires every dynamic lookup to
select the pinned local binding; the call request does not establish that
selection or its applied effects.

## Local behavior

### `setItemToXmlLight(self, listbox, item, package, index, bazaartype)`

The method first requests `self.getListPropertyName(listbox)` for two results,
then requests `worldMaster._getMyPlayer()` for one result. It evaluates
`0 < package` and then `0 < index`; a false comparison returns one literal
`false`. On success it always requests
`desktopWidget.getRetainerItem(package,index)`, regardless of `bazaartype`.
Nil item and an exact `false` result from `item._isAlive()` each return one
literal `false`. Catalog, icon, stackability result, count, and name index
are loaded independently from the item. Catalog `1000001` requests writes of
`self.work.moneyIndex = index` and `self.work.moneyCount = count`.

The sort value starts as a fresh `self.work.sorttype` with sort field `20`.
Listbox `2` selects sort `11` and field `21`; listbox `3` selects sort `0` and
keeps field `20`; listbox `1` keeps the fresh sort and field `20`. Other values
also keep the fresh sort and field. The desktop XML request has 19 total call
arguments including its receiver: `desktopWidget`, `self`, property name, item
argument, item, `TBL_null`, catalog, icon, stackable, count, name index, sort,
`true`, `false`, sort field, package, index, `bazaartype`, and `false`. The
`bazaartype` argument is forwarded only at this point.

After XML, a positive fresh `self.work.updatecountbaz` and equal fresh
`self.work.listbox == listbox` request `self.getControlProperty(property,
"FilteredIndex")`; when that result is less than a fresh `self.work.focus`, the
method attempts `self.work.focusChange = true`. Normal completion returns one
literal `true`.

### `setBazaarLabelVisibility(self, listname, row, status)`

Numeric status `1` requests `bazaarStatus = 378` and
`priceStyle = "TBL_parameterPlus"`; status `7` requests `bazaarStatus = 453`
and the same price style; status `2` requests `bazaarStatus = 379` and
`priceStyle = "TBL_parameterMinus"`; status `3` requests `bazaarStatus = 380`
and `priceStyle = "TBL_guildleveBonus"`. Status `7` and status `2` each read
`stackCount` before `stackable`. Only numeric `stackable == 1` requests
`tostring(captured stackCount)` and then a `stack = "(" .. tostring .. ")"`
property. Boolean `true` is not numeric one here. Unsupported status reads
`nameStyle`, copies it to `priceStyle`, and selects `Hidden`. Every path then
requests `bazaarStatusVisibility` with literal `Visible` or `Hidden`.

### `updateBazaarLabel(self, listbox, owner)`

The method requests one list-name result and a list item count, then scans
package `8` from slot `1` through that count. It breaks only when
`self.isExistItem(8, slot, owner)` is exactly `false`. For owner nil or `1` it
requests `desktopWidget.isDealingItem(8,slot)`; owner `2` selects
`isBazaarDealingItem`; owner `4` selects `isRetainerDealingItem`. Only exact
`true` enters the deal-data path, which requests three results from
`getRetainerItemDealData(8,slot)`, stores `bazaarkind`, and maps deal kinds
`11,12,13,20,30` to local label statuses `1,1,7,4,4`.

For status other than `4`, the method requests reward price, price text with
format `225`, zero reward package and item, and visible row properties. For
status `4`, it requests visible row properties, selected-item name style,
opacity `"0.5"`, zero reward price/package/item, and empty price text. When no
deal is present, it requests `isRetainerItemAttached`; an exact `true` requests
selected `checkRewardDependency` method and requests four results. A first
result unequal to numeric zero enters the dependency path, including nil or
false. Kinds 20 and 30 select statuses 2 and 3. It supplies reward package/item
from results two and three. A fourth result unequal to numeric zero, including
nil or false, requests price format `225` with that value; exact numeric zero
requests format `3144`. A first result equal to numeric zero clears reward
package/item and price. The no-attachment path also clears those fields. Both
attached and unattached no-deal paths then clear Bazaar kind and reward price
and request visible row properties. Each scanned row requests the selected
`setBazaarLabelVisibility`, and normal completion requests
`updateListProperty(listname)` with zero results.

### `checkRewardDependency(self, package, index, owner)`

Exact numeric `0` or exact boolean `false` in either package or index returns
four numeric zeroes. Nil is not rejected by this guard. Owner nil or `1`
requests `worldMaster._getMyPlayer()`, captures `_getItem(package,index)` as
the comparison target, and scans player package `8` up to
`_getItemPackageCapacity(8)`. Owner `2` uses the desktop Bazaar item and
capacity helpers; owner `4` uses the desktop retainer item and capacity
helpers. The player branch calls
`isExistItem(8,slot)`; Bazaar and retainer branches call
`isExistItem(8,slot,owner)`. Each breaks only on exact `false`; only exact `true` from the selected dealing
predicate requests its three-result deal-data helper. The third deal result is
compared with the captured target item. On a match, a fresh listing-item fetch
for the loop slot supplies catalog and (only for catalog `1000001`) stack
reads; the method returns the first deal result, numeric `8`, slot, and the
local stack result (otherwise its initialized numeric zero). No match
returns four numeric zeroes. Unsupported owners reach a bare return with zero
results.

### `isRewardItemActor(self, package, index, dealPackage, dealIndex, owner)`

Exact numeric `0` or exact boolean `false` in any of the first four reference
operands returns one literal `false`. Nil and other values are not rejected by
this guard. Owner nil or `1` selects `getItemDealData` and the player item;
owner `2` selects Bazaar deal data and Bazaar item; owner `4` selects retainer
deal data and retainer item. The returned item is compared with the third deal
result and the method returns one literal boolean. Unsupported owners reach a
bare return with zero results. Two nil values compare equal in the local Lua
comparison; that equality is not evidence of an item, actor, reward, or
eligibility.

### `getItemBazaarData(self, item, listname, row, unused1, unused2, unused3)`

The method initializes a fourteen-value tuple to zeros, empty string, and
false values. A non-nil `item` takes the empty local branch and returns that
tuple without getter calls. With nil `item`, it independently reads
`bazaarkind`, `rewardprice`, `rewardpackage`, and `rewarditem` at the supplied
list row. A reward package that compares unequal to literal zero then reads ten properties from the row
referenced by `rewarditem - 1`: Bazaar kind, catalog, icon, stack count, name,
stackable, polish visibility, materia count, equipment visibility, and materia
visibility. The result is exactly fourteen values in local order:
kind, package, item, reward price, row kind, catalog, icon, stack count, name,
stackable, polish-visible, materia count, equipment-visible, and
materia-visible. The `polmax`, `equipx` and `mpvisible` getter results
each compare to the literal string `"Visible"`, producing Boolean tuple
slots. Boolean true does not match that string and produces false. A zero
package returns the initialized defaults for the last ten values.

### `displayBazaarGrid(self, item, listname, row, unused1, unused2, mode)`

The method first calls the selected `getItemBazaarData` with a nil item and the
five list/mode arguments, then requests six results from
`desktopWidget.getItemRepairData(self,item,listname,row)`. For a non-nil item it
requests `isExclusiveItem`, `isRareItem`, and, when mode is nil or numeric `1`,
`_isEquipping`. For nil item it derives the same three flags from list
properties equal to numeric `1`. It then requests the three base visibility
clears before selecting the display branch.

Kinds `11`, `12`, and `13` select the single, separate, and set Bazaar labels,
respectively, request icons `378`, `378`, and `453`, show reward money, set
reward money text format `3201` with the fourth data result, and attempt
`self.work.bazaar = true`. Kinds `20` and `30` clear the Bazaar labels, hide
the status icon and reward grids, and return local boolean `true`. For other
kinds, a reward package that compares unequal to literal zero attempts `self.work.bazaar = true` and shows a
money grid for catalog `1000001`, otherwise an item icon/name path. Numeric
stackable `== 1` requests stack text format `3189`; boolean `true` does not
enter that branch. Positive materia count takes precedence over item stack
display, and otherwise a true materia-visible flag selects the base icon
path. The method then selects buy or repair labels for row kinds `20` and
`30`. With no reward package it attempts `self.work.bazaar = false` and clears
all Bazaar and reward visibility. It returns the local boolean at normal
completion. UI setters, field writes, and close/display requests remain
requests; no native first value, storage, readback, render, focus, lifetime,
roster, item, currency, or server effect is established.

## Context and limits

The published `eventTalkRetainerItemList(2)` material is selection context for
the Ask resource only. It does not prove invocation of these seven utilities.
Shared BazaarListWidget method names and native price-mode pages are separate
resources and are not used as semantics here. All outside methods, including
`isExistItem` and list-property helpers, are opaque dependencies.

The original-word fixture set contains 33 cases and six corruption controls.
All normal results use recursive typed comparisons. Selected cases also check
complete actual arguments, raw function/receiver identity, branch successors,
write destinations and chronological call/write events. These assertions do
not cover every call or edge in every case. Specific cases distinguish the
package-zero and index-zero guards, attached and unattached no-deal branches,
numeric-zero dependency tests, string visibility tests, setter captures across
tostring callbacks, fixed result padding/truncation and an open tostring tail.

The static branch ledger contains 101 conditional or numeric-loop words,
including TEST at prototype 34 PC32. Its false/nil edge resolves through JMP
to PC60; a truthy value, including numeric zero, reaches PC34. That instruction
controls the local equipped flag. The fourteen-result data call and six-result
repair call remain fixed-width. The tostring call at PC343 instead returns an
open result tail that the PC344 setText request forwards after self and
`TextBlock_MateriaNumber`, including a zero-result or multiple-result tail.

Every outside call is mocked. These fixtures establish finite ordinary Lua
paths, without native behavior, metamethod, coercion or exhaustive input
coverage. The complete direct-call operand matrix follows.

## Complete CALL and TAILCALL matrix

Each row is one original CALL or TAILCALL word in the seven selected prototypes. PC is zero-based within the prototype and offset is the decoded payload word start. B and C are original operands; a nonzero B consumes R(A+1) through R(A+B-1), B=0 is the open active-top tail. The prefix column records the actual preceding SELF or GETGLOBAL prefix and the receiver column records whether that prefix supplies a receiver. Result width is C-1, or dynamic for C=0.

| Method | PC | Payload offset | Word | A/B/C | CALL prefix | Receiver | Arguments (register/value) | Results |
| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: |
| `setItemToXmlLight` | 2 | 14334 | `CALL` | `6/3/3` | `pc0 SELF A6 B0 K='getListPropertyName'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1` | 2 |
| `setItemToXmlLight` | 6 | 14350 | `CALL` | `12/2/2` | `pc5 SELF A12 B12 K='_getMyPlayer'` | `R13=global worldMaster (SELF receiver)` | `R13=global worldMaster` | 1 |
| `setItemToXmlLight` | 16 | 14390 | `CALL` | `15/4/2` | `pc13 SELF A15 B15 K='getRetainerItem'` | `R16=global desktopWidget (SELF receiver)` | `R16=global desktopWidget, R17=parameter A3, R18=parameter A4` | 1 |
| `setItemToXmlLight` | 26 | 14430 | `CALL` | `15/2/2` | `pc25 SELF A15 B13 K='_isAlive'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 32 | 14454 | `CALL` | `15/2/2` | `pc31 SELF A15 B13 K='_getCatalogID'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 35 | 14466 | `CALL` | `15/2/2` | `pc34 SELF A15 B13 K='getItemIcon'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 38 | 14478 | `CALL` | `15/2/2` | `pc37 SELF A15 B13 K='_isStackable'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 41 | 14490 | `CALL` | `15/2/2` | `pc40 SELF A15 B13 K='_countStack'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 50 | 14526 | `CALL` | `15/2/2` | `pc49 SELF A15 B13 K='_getNameIndex'` | `R16=result pc16[0] (SELF receiver)` | `R16=result pc16[0]` | 1 |
| `setItemToXmlLight` | 91 | 14690 | `CALL` | `19/20/1` | `pc72 SELF A19 B19 K='setItemToXml'` | `R20=global desktopWidget (SELF receiver)` | `R20=global desktopWidget, R21=parameter A0, R22=result pc2[0], R23=parameter A2, R24=result pc16[0], R25='TBL_null', R26=result pc32[0], R27=result pc35[0], R28=result pc38[0], R29=result pc41[0], R30=result pc50[0], R31=path-dependent register value, R32=True, R33=False, R34=path-dependent register value, R35=parameter A3, R36=parameter A4, R37=parameter A5, R38=False` | 0 |
| `setItemToXmlLight` | 103 | 14738 | `CALL` | `19/4/2` | `pc100 SELF A19 B0 K='getControlProperty'` | `R20=parameter A0 (SELF receiver)` | `R20=parameter A0, R21=result pc2[0], R22='FilteredIndex'` | 1 |
| `setBazaarLabelVisibility` | 8 | 16598 | `CALL` | `5/6/1` | `pc3 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='bazaarStatus', R10=378` | 0 |
| `setBazaarLabelVisibility` | 14 | 16622 | `CALL` | `5/6/1` | `pc9 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='priceStyle', R10='TBL_parameterPlus'` | 0 |
| `setBazaarLabelVisibility` | 23 | 16658 | `CALL` | `5/6/1` | `pc18 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='bazaarStatus', R10=453` | 0 |
| `setBazaarLabelVisibility` | 29 | 16682 | `CALL` | `5/6/1` | `pc24 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='priceStyle', R10='TBL_parameterPlus'` | 0 |
| `setBazaarLabelVisibility` | 34 | 16702 | `CALL` | `5/5/2` | `pc30 SELF A5 B0 K='getListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='stackCount'` | 1 |
| `setBazaarLabelVisibility` | 39 | 16722 | `CALL` | `6/5/2` | `pc35 SELF A6 B0 K='getListProperty'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1, R9=parameter A2, R10='stackable'` | 1 |
| `setBazaarLabelVisibility` | 49 | 16762 | `CALL` | `12/2/2` | `pc47 GETGLOBAL A12 K='tostring'` | `none (global function)` | `R13=result pc34[0]` | 1 |
| `setBazaarLabelVisibility` | 52 | 16774 | `CALL` | `6/6/1` | `pc42 SELF A6 B0 K='setListProperty'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1, R9=parameter A2, R10='stack', R11=path-dependent register value` | 0 |
| `setBazaarLabelVisibility` | 61 | 16810 | `CALL` | `5/6/1` | `pc56 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='bazaarStatus', R10=379` | 0 |
| `setBazaarLabelVisibility` | 67 | 16834 | `CALL` | `5/6/1` | `pc62 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='priceStyle', R10='TBL_parameterMinus'` | 0 |
| `setBazaarLabelVisibility` | 72 | 16854 | `CALL` | `5/5/2` | `pc68 SELF A5 B0 K='getListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='stackCount'` | 1 |
| `setBazaarLabelVisibility` | 77 | 16874 | `CALL` | `6/5/2` | `pc73 SELF A6 B0 K='getListProperty'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1, R9=parameter A2, R10='stackable'` | 1 |
| `setBazaarLabelVisibility` | 87 | 16914 | `CALL` | `12/2/2` | `pc85 GETGLOBAL A12 K='tostring'` | `none (global function)` | `R13=result pc72[0]` | 1 |
| `setBazaarLabelVisibility` | 90 | 16926 | `CALL` | `6/6/1` | `pc80 SELF A6 B0 K='setListProperty'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1, R9=parameter A2, R10='stack', R11=path-dependent register value` | 0 |
| `setBazaarLabelVisibility` | 99 | 16962 | `CALL` | `5/6/1` | `pc94 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='bazaarStatus', R10=380` | 0 |
| `setBazaarLabelVisibility` | 105 | 16986 | `CALL` | `5/6/1` | `pc100 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='priceStyle', R10='TBL_guildleveBonus'` | 0 |
| `setBazaarLabelVisibility` | 111 | 17010 | `CALL` | `5/5/2` | `pc107 SELF A5 B0 K='getListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='nameStyle'` | 1 |
| `setBazaarLabelVisibility` | 117 | 17034 | `CALL` | `6/6/1` | `pc112 SELF A6 B0 K='setListProperty'` | `R7=parameter A0 (SELF receiver)` | `R7=parameter A0, R8=parameter A1, R9=parameter A2, R10='priceStyle', R11=result pc111[0]` | 0 |
| `setBazaarLabelVisibility` | 124 | 17062 | `CALL` | `5/6/1` | `pc119 SELF A5 B0 K='setListProperty'` | `R6=parameter A0 (SELF receiver)` | `R6=parameter A0, R7=parameter A1, R8=parameter A2, R9='bazaarStatusVisibility', R10=path-dependent register value` | 0 |
| `updateBazaarLabel` | 2 | 17475 | `CALL` | `10/3/2` | `pc0 SELF A10 B0 K='getListPropertyName'` | `R11=parameter A0 (SELF receiver)` | `R11=parameter A0, R12=parameter A1` | 1 |
| `updateBazaarLabel` | 7 | 17495 | `CALL` | `14/3/2` | `pc5 SELF A14 B0 K='getListBoxItemNum'` | `R15=parameter A0 (SELF receiver)` | `R15=parameter A0, R16=parameter A1` | 1 |
| `updateBazaarLabel` | 18 | 17539 | `CALL` | `19/5/2` | `pc14 SELF A19 B0 K='isExistItem'` | `R20=parameter A0 (SELF receiver)` | `R20=parameter A0, R21=8, R22=path-dependent register value, R23=parameter A2` | 1 |
| `updateBazaarLabel` | 32 | 17595 | `CALL` | `20/4/2` | `pc29 SELF A20 B20 K='isDealingItem'` | `R21=global desktopWidget (SELF receiver)` | `R21=global desktopWidget, R22=8, R23=path-dependent register value` | 1 |
| `updateBazaarLabel` | 41 | 17631 | `CALL` | `20/4/2` | `pc38 SELF A20 B20 K='isBazaarDealingItem'` | `R21=global desktopWidget (SELF receiver)` | `R21=global desktopWidget, R22=8, R23=path-dependent register value` | 1 |
| `updateBazaarLabel` | 50 | 17667 | `CALL` | `20/4/2` | `pc47 SELF A20 B20 K='isRetainerDealingItem'` | `R21=global desktopWidget (SELF receiver)` | `R21=global desktopWidget, R22=8, R23=path-dependent register value` | 1 |
| `updateBazaarLabel` | 58 | 17699 | `CALL` | `20/4/4` | `pc55 SELF A20 B20 K='getRetainerItemDealData'` | `R21=global desktopWidget (SELF receiver)` | `R21=global desktopWidget, R22=8, R23=path-dependent register value` | 3 |
| `updateBazaarLabel` | 67 | 17735 | `CALL` | `20/6/1` | `pc62 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='bazaarkind', R25=result pc58[0]` | 0 |
| `updateBazaarLabel` | 94 | 17843 | `CALL` | `20/6/1` | `pc89 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewardprice', R25=result pc58[1]` | 0 |
| `updateBazaarLabel` | 101 | 17871 | `CALL` | `20/7/1` | `pc95 SELF A20 B0 K='setListText'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='price', R25=225, R26=result pc58[1]` | 0 |
| `updateBazaarLabel` | 107 | 17895 | `CALL` | `20/6/1` | `pc102 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewardpackage', R25=0` | 0 |
| `updateBazaarLabel` | 113 | 17919 | `CALL` | `20/6/1` | `pc108 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewarditem', R25=0` | 0 |
| `updateBazaarLabel` | 118 | 17939 | `CALL` | `20/5/1` | `pc114 SELF A20 B0 K='setListPropertyVisibility'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24=True` | 0 |
| `updateBazaarLabel` | 124 | 17963 | `CALL` | `20/5/1` | `pc120 SELF A20 B0 K='setListPropertyVisibility'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24=True` | 0 |
| `updateBazaarLabel` | 130 | 17987 | `CALL` | `20/6/1` | `pc125 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='nameStyle', R25='TBL_selectedItem'` | 0 |
| `updateBazaarLabel` | 136 | 18011 | `CALL` | `20/6/1` | `pc131 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='opacity', R25='0.5'` | 0 |
| `updateBazaarLabel` | 142 | 18035 | `CALL` | `20/6/1` | `pc137 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewardprice', R25=0` | 0 |
| `updateBazaarLabel` | 148 | 18059 | `CALL` | `20/6/1` | `pc143 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewardpackage', R25=0` | 0 |
| `updateBazaarLabel` | 154 | 18083 | `CALL` | `20/6/1` | `pc149 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='rewarditem', R25=0` | 0 |
| `updateBazaarLabel` | 160 | 18107 | `CALL` | `20/6/1` | `pc155 SELF A20 B0 K='setListProperty'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24='price', R25=''` | 0 |
| `updateBazaarLabel` | 167 | 18135 | `CALL` | `21/4/2` | `pc164 SELF A21 B21 K='isRetainerItemAttached'` | `R22=global desktopWidget (SELF receiver)` | `R22=global desktopWidget, R23=8, R24=path-dependent register value` | 1 |
| `updateBazaarLabel` | 175 | 18167 | `CALL` | `21/5/5` | `pc171 SELF A21 B0 K='checkRewardDependency'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=8, R24=path-dependent register value, R25=parameter A2` | 4 |
| `updateBazaarLabel` | 197 | 18255 | `CALL` | `21/7/1` | `pc191 SELF A21 B0 K='setListText'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='price', R26=225, R27=result pc175[3]` | 0 |
| `updateBazaarLabel` | 204 | 18283 | `CALL` | `21/6/1` | `pc199 SELF A21 B0 K='setListText'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='price', R26=3144` | 0 |
| `updateBazaarLabel` | 210 | 18307 | `CALL` | `21/6/1` | `pc205 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewardpackage', R26=result pc175[1]` | 0 |
| `updateBazaarLabel` | 216 | 18331 | `CALL` | `21/6/1` | `pc211 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewarditem', R26=result pc175[2]` | 0 |
| `updateBazaarLabel` | 223 | 18359 | `CALL` | `21/6/1` | `pc218 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewardpackage', R26=0` | 0 |
| `updateBazaarLabel` | 229 | 18383 | `CALL` | `21/6/1` | `pc224 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewarditem', R26=0` | 0 |
| `updateBazaarLabel` | 235 | 18407 | `CALL` | `21/6/1` | `pc230 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='price', R26=''` | 0 |
| `updateBazaarLabel` | 242 | 18435 | `CALL` | `21/6/1` | `pc237 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewardpackage', R26=0` | 0 |
| `updateBazaarLabel` | 248 | 18459 | `CALL` | `21/6/1` | `pc243 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewarditem', R26=0` | 0 |
| `updateBazaarLabel` | 254 | 18483 | `CALL` | `21/6/1` | `pc249 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='price', R26=''` | 0 |
| `updateBazaarLabel` | 260 | 18507 | `CALL` | `21/6/1` | `pc255 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='bazaarkind', R26=0` | 0 |
| `updateBazaarLabel` | 266 | 18531 | `CALL` | `21/6/1` | `pc261 SELF A21 B0 K='setListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25='rewardprice', R26=0` | 0 |
| `updateBazaarLabel` | 271 | 18551 | `CALL` | `21/5/1` | `pc267 SELF A21 B0 K='setListPropertyVisibility'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=result pc2[0], R24=path-dependent register value, R25=True` | 0 |
| `updateBazaarLabel` | 276 | 18571 | `CALL` | `20/5/1` | `pc272 SELF A20 B0 K='setBazaarLabelVisibility'` | `R21=parameter A0 (SELF receiver)` | `R21=parameter A0, R22=result pc2[0], R23=path-dependent register value, R24=path-dependent register value` | 0 |
| `updateBazaarLabel` | 280 | 18587 | `CALL` | `15/3/1` | `pc278 SELF A15 B0 K='updateListProperty'` | `R16=parameter A0 (SELF receiver)` | `R16=parameter A0, R17=result pc2[0]` | 0 |
| `checkRewardDependency` | 23 | 19364 | `CALL` | `8/2/2` | `pc22 SELF A8 B8 K='_getMyPlayer'` | `R9=global worldMaster (SELF receiver)` | `R9=global worldMaster` | 1 |
| `checkRewardDependency` | 27 | 19380 | `CALL` | `9/4/2` | `pc24 SELF A9 B8 K='_getItem'` | `R10=result pc23[0] (SELF receiver)` | `R10=result pc23[0], R11=parameter A1, R12=parameter A2` | 1 |
| `checkRewardDependency` | 31 | 19396 | `CALL` | `11/3/2` | `pc29 SELF A11 B8 K='_getItemPackageCapacity'` | `R12=result pc23[0] (SELF receiver)` | `R12=result pc23[0], R13=8` | 1 |
| `checkRewardDependency` | 37 | 19420 | `CALL` | `14/4/2` | `pc34 SELF A14 B0 K='isExistItem'` | `R15=parameter A0 (SELF receiver)` | `R15=parameter A0, R16=8, R17=path-dependent register value` | 1 |
| `checkRewardDependency` | 46 | 19456 | `CALL` | `14/4/2` | `pc43 SELF A14 B14 K='isDealingItem'` | `R15=global desktopWidget (SELF receiver)` | `R15=global desktopWidget, R16=8, R17=path-dependent register value` | 1 |
| `checkRewardDependency` | 53 | 19484 | `CALL` | `14/4/4` | `pc50 SELF A14 B14 K='getItemDealData'` | `R15=global desktopWidget (SELF receiver)` | `R15=global desktopWidget, R16=8, R17=path-dependent register value` | 3 |
| `checkRewardDependency` | 62 | 19520 | `CALL` | `14/4/2` | `pc59 SELF A14 B8 K='_getItem'` | `R15=result pc23[0] (SELF receiver)` | `R15=result pc23[0], R16=8, R17=path-dependent register value` | 1 |
| `checkRewardDependency` | 64 | 19528 | `CALL` | `15/2/2` | `pc63 SELF A15 B14 K='_getCatalogID'` | `R16=result pc62[0] (SELF receiver)` | `R16=result pc62[0]` | 1 |
| `checkRewardDependency` | 68 | 19544 | `CALL` | `15/2/2` | `pc67 SELF A15 B14 K='_countStack'` | `R16=result pc62[0] (SELF receiver)` | `R16=result pc62[0]` | 1 |
| `checkRewardDependency` | 88 | 19624 | `CALL` | `8/4/2` | `pc85 SELF A8 B8 K='getBazaarItem'` | `R9=global desktopWidget (SELF receiver)` | `R9=global desktopWidget, R10=parameter A1, R11=parameter A2` | 1 |
| `checkRewardDependency` | 93 | 19644 | `CALL` | `10/3/2` | `pc91 SELF A10 B10 K='getBazaarItemPackageCapacity'` | `R11=global desktopWidget (SELF receiver)` | `R11=global desktopWidget, R12=8` | 1 |
| `checkRewardDependency` | 100 | 19672 | `CALL` | `13/5/2` | `pc96 SELF A13 B0 K='isExistItem'` | `R14=parameter A0 (SELF receiver)` | `R14=parameter A0, R15=8, R16=path-dependent register value, R17=parameter A3` | 1 |
| `checkRewardDependency` | 109 | 19708 | `CALL` | `13/4/2` | `pc106 SELF A13 B13 K='isBazaarDealingItem'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 1 |
| `checkRewardDependency` | 116 | 19736 | `CALL` | `13/4/4` | `pc113 SELF A13 B13 K='getBazaarItemDealData'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 3 |
| `checkRewardDependency` | 126 | 19776 | `CALL` | `13/4/2` | `pc123 SELF A13 B13 K='getBazaarItem'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 1 |
| `checkRewardDependency` | 128 | 19784 | `CALL` | `14/2/2` | `pc127 SELF A14 B13 K='_getCatalogID'` | `R15=result pc126[0] (SELF receiver)` | `R15=result pc126[0]` | 1 |
| `checkRewardDependency` | 132 | 19800 | `CALL` | `14/2/2` | `pc131 SELF A14 B13 K='_countStack'` | `R15=result pc126[0] (SELF receiver)` | `R15=result pc126[0]` | 1 |
| `checkRewardDependency` | 152 | 19880 | `CALL` | `8/4/2` | `pc149 SELF A8 B8 K='getRetainerItem'` | `R9=global desktopWidget (SELF receiver)` | `R9=global desktopWidget, R10=parameter A1, R11=parameter A2` | 1 |
| `checkRewardDependency` | 157 | 19900 | `CALL` | `10/3/2` | `pc155 SELF A10 B10 K='getRetainerItemPackageCapacity'` | `R11=global desktopWidget (SELF receiver)` | `R11=global desktopWidget, R12=8` | 1 |
| `checkRewardDependency` | 164 | 19928 | `CALL` | `13/5/2` | `pc160 SELF A13 B0 K='isExistItem'` | `R14=parameter A0 (SELF receiver)` | `R14=parameter A0, R15=8, R16=path-dependent register value, R17=parameter A3` | 1 |
| `checkRewardDependency` | 173 | 19964 | `CALL` | `13/4/2` | `pc170 SELF A13 B13 K='isRetainerDealingItem'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 1 |
| `checkRewardDependency` | 180 | 19992 | `CALL` | `13/4/4` | `pc177 SELF A13 B13 K='getRetainerItemDealData'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 3 |
| `checkRewardDependency` | 190 | 20032 | `CALL` | `13/4/2` | `pc187 SELF A13 B13 K='getRetainerItem'` | `R14=global desktopWidget (SELF receiver)` | `R14=global desktopWidget, R15=8, R16=path-dependent register value` | 1 |
| `checkRewardDependency` | 192 | 20040 | `CALL` | `14/2/2` | `pc191 SELF A14 B13 K='_getCatalogID'` | `R15=result pc190[0] (SELF receiver)` | `R15=result pc190[0]` | 1 |
| `checkRewardDependency` | 196 | 20056 | `CALL` | `14/2/2` | `pc195 SELF A14 B13 K='_countStack'` | `R15=result pc190[0] (SELF receiver)` | `R15=result pc190[0]` | 1 |
| `isRewardItemActor` | 24 | 20715 | `CALL` | `6/2/2` | `pc23 SELF A6 B6 K='_getMyPlayer'` | `R7=global worldMaster (SELF receiver)` | `R7=global worldMaster` | 1 |
| `isRewardItemActor` | 29 | 20735 | `CALL` | `7/4/4` | `pc26 SELF A7 B7 K='getItemDealData'` | `R8=global desktopWidget (SELF receiver)` | `R8=global desktopWidget, R9=parameter A3, R10=parameter A4` | 3 |
| `isRewardItemActor` | 33 | 20751 | `CALL` | `10/4/2` | `pc30 SELF A10 B6 K='_getItem'` | `R11=result pc24[0] (SELF receiver)` | `R11=result pc24[0], R12=parameter A1, R13=parameter A2` | 1 |
| `isRewardItemActor` | 48 | 20811 | `CALL` | `6/4/4` | `pc45 SELF A6 B6 K='getBazaarItemDealData'` | `R7=global desktopWidget (SELF receiver)` | `R7=global desktopWidget, R8=parameter A3, R9=parameter A4` | 3 |
| `isRewardItemActor` | 53 | 20831 | `CALL` | `9/4/2` | `pc50 SELF A9 B9 K='getBazaarItem'` | `R10=global desktopWidget (SELF receiver)` | `R10=global desktopWidget, R11=parameter A1, R12=parameter A2` | 1 |
| `isRewardItemActor` | 68 | 20891 | `CALL` | `6/4/4` | `pc65 SELF A6 B6 K='getRetainerItemDealData'` | `R7=global desktopWidget (SELF receiver)` | `R7=global desktopWidget, R8=parameter A3, R9=parameter A4` | 3 |
| `isRewardItemActor` | 73 | 20911 | `CALL` | `9/4/2` | `pc70 SELF A9 B9 K='getRetainerItem'` | `R10=global desktopWidget (SELF receiver)` | `R10=global desktopWidget, R11=parameter A1, R12=parameter A2` | 1 |
| `getItemBazaarData` | 21 | 24694 | `CALL` | `21/5/2` | `pc17 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=parameter A3, R25='bazaarkind'` | 1 |
| `getItemBazaarData` | 27 | 24718 | `CALL` | `21/5/2` | `pc23 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=parameter A3, R25='rewardprice'` | 1 |
| `getItemBazaarData` | 33 | 24742 | `CALL` | `21/5/2` | `pc29 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=parameter A3, R25='rewardpackage'` | 1 |
| `getItemBazaarData` | 39 | 24766 | `CALL` | `21/5/2` | `pc35 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=parameter A3, R25='rewarditem'` | 1 |
| `getItemBazaarData` | 47 | 24798 | `CALL` | `21/5/2` | `pc43 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='bazaarkind'` | 1 |
| `getItemBazaarData` | 53 | 24822 | `CALL` | `21/5/2` | `pc49 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='catalog'` | 1 |
| `getItemBazaarData` | 59 | 24846 | `CALL` | `21/5/2` | `pc55 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='icon'` | 1 |
| `getItemBazaarData` | 65 | 24870 | `CALL` | `21/5/2` | `pc61 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='stackCount'` | 1 |
| `getItemBazaarData` | 71 | 24894 | `CALL` | `21/5/2` | `pc67 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='name'` | 1 |
| `getItemBazaarData` | 77 | 24918 | `CALL` | `21/5/2` | `pc73 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='stackable'` | 1 |
| `getItemBazaarData` | 83 | 24942 | `CALL` | `21/5/2` | `pc79 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='polmax'` | 1 |
| `getItemBazaarData` | 92 | 24978 | `CALL` | `21/5/2` | `pc88 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='mcount'` | 1 |
| `getItemBazaarData` | 98 | 25002 | `CALL` | `21/5/2` | `pc94 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='equipx'` | 1 |
| `getItemBazaarData` | 107 | 25038 | `CALL` | `21/5/2` | `pc103 SELF A21 B0 K='getListProperty'` | `R22=parameter A0 (SELF receiver)` | `R22=parameter A0, R23=parameter A2, R24=path-dependent register value, R25='mpvisible'` | 1 |
| `displayBazaarGrid` | 7 | 25432 | `CALL` | `7/8/15` | `pc0 SELF A7 B0 K='getItemBazaarData'` | `R8=parameter A0 (SELF receiver)` | `R8=parameter A0, R9=nil, R10=parameter A2, R11=parameter A3, R12=parameter A4, R13=parameter A5, R14=parameter A6` | 14 |
| `displayBazaarGrid` | 14 | 25460 | `CALL` | `21/6/7` | `pc9 SELF A21 B21 K='getItemRepairData'` | `R22=global desktopWidget (SELF receiver)` | `R22=global desktopWidget, R23=parameter A0, R24=parameter A1, R25=parameter A2, R26=parameter A3` | 6 |
| `displayBazaarGrid` | 21 | 25488 | `CALL` | `30/2/2` | `pc20 SELF A30 B1 K='isExclusiveItem'` | `R31=parameter A1 (SELF receiver)` | `R31=parameter A1` | 1 |
| `displayBazaarGrid` | 24 | 25500 | `CALL` | `30/2/2` | `pc23 SELF A30 B1 K='isRareItem'` | `R31=parameter A1 (SELF receiver)` | `R31=parameter A1` | 1 |
| `displayBazaarGrid` | 31 | 25528 | `CALL` | `30/2/2` | `pc30 SELF A30 B1 K='_isEquipping'` | `R31=parameter A1 (SELF receiver)` | `R31=parameter A1` | 1 |
| `displayBazaarGrid` | 40 | 25564 | `CALL` | `30/5/2` | `pc36 SELF A30 B0 K='getListProperty'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32=parameter A2, R33=parameter A3, R34='ex'` | 1 |
| `displayBazaarGrid` | 48 | 25596 | `CALL` | `30/5/2` | `pc44 SELF A30 B0 K='getListProperty'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32=parameter A2, R33=parameter A3, R34='rare'` | 1 |
| `displayBazaarGrid` | 56 | 25628 | `CALL` | `30/5/2` | `pc52 SELF A30 B0 K='getListProperty'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32=parameter A2, R33=parameter A3, R34='isEquipping'` | 1 |
| `displayBazaarGrid` | 63 | 25656 | `CALL` | `30/4/1` | `pc60 SELF A30 B0 K='setVisibility'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32='IconControl_NotEquiped_2', R33=False` | 0 |
| `displayBazaarGrid` | 67 | 25672 | `CALL` | `30/4/1` | `pc64 SELF A30 B0 K='setVisibility'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32='IconControl_PolishMAX_2', R33=False` | 0 |
| `displayBazaarGrid` | 71 | 25688 | `CALL` | `30/4/1` | `pc68 SELF A30 B0 K='setVisibility'` | `R31=parameter A0 (SELF receiver)` | `R31=parameter A0, R32='Grid_MateriaNumber', R33=False` | 0 |
| `displayBazaarGrid` | 78 | 25716 | `CALL` | `31/4/1` | `pc75 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=True` | 0 |
| `displayBazaarGrid` | 82 | 25732 | `CALL` | `31/4/1` | `pc79 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 86 | 25748 | `CALL` | `31/4/1` | `pc83 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 90 | 25764 | `CALL` | `31/4/1` | `pc87 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 94 | 25780 | `CALL` | `31/4/1` | `pc91 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 98 | 25796 | `CALL` | `31/4/1` | `pc95 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=False` | 0 |
| `displayBazaarGrid` | 102 | 25812 | `CALL` | `31/4/1` | `pc99 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=378` | 0 |
| `displayBazaarGrid` | 106 | 25828 | `CALL` | `31/4/1` | `pc103 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=True` | 0 |
| `displayBazaarGrid` | 110 | 25844 | `CALL` | `31/4/1` | `pc107 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 114 | 25860 | `CALL` | `31/4/1` | `pc111 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=True` | 0 |
| `displayBazaarGrid` | 119 | 25880 | `CALL` | `31/5/1` | `pc115 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardMoney', R34=3201, R35=result pc7[3]` | 0 |
| `displayBazaarGrid` | 128 | 25916 | `CALL` | `31/4/1` | `pc125 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 132 | 25932 | `CALL` | `31/4/1` | `pc129 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=True` | 0 |
| `displayBazaarGrid` | 136 | 25948 | `CALL` | `31/4/1` | `pc133 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 140 | 25964 | `CALL` | `31/4/1` | `pc137 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 144 | 25980 | `CALL` | `31/4/1` | `pc141 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 148 | 25996 | `CALL` | `31/4/1` | `pc145 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=False` | 0 |
| `displayBazaarGrid` | 152 | 26012 | `CALL` | `31/4/1` | `pc149 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=378` | 0 |
| `displayBazaarGrid` | 156 | 26028 | `CALL` | `31/4/1` | `pc153 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=True` | 0 |
| `displayBazaarGrid` | 160 | 26044 | `CALL` | `31/4/1` | `pc157 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 164 | 26060 | `CALL` | `31/4/1` | `pc161 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=True` | 0 |
| `displayBazaarGrid` | 169 | 26080 | `CALL` | `31/5/1` | `pc165 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardMoney', R34=3201, R35=result pc7[3]` | 0 |
| `displayBazaarGrid` | 178 | 26116 | `CALL` | `31/4/1` | `pc175 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 182 | 26132 | `CALL` | `31/4/1` | `pc179 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 186 | 26148 | `CALL` | `31/4/1` | `pc183 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=True` | 0 |
| `displayBazaarGrid` | 190 | 26164 | `CALL` | `31/4/1` | `pc187 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 194 | 26180 | `CALL` | `31/4/1` | `pc191 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 198 | 26196 | `CALL` | `31/4/1` | `pc195 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=False` | 0 |
| `displayBazaarGrid` | 202 | 26212 | `CALL` | `31/4/1` | `pc199 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=453` | 0 |
| `displayBazaarGrid` | 206 | 26228 | `CALL` | `31/4/1` | `pc203 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=True` | 0 |
| `displayBazaarGrid` | 210 | 26244 | `CALL` | `31/4/1` | `pc207 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 214 | 26260 | `CALL` | `31/4/1` | `pc211 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=True` | 0 |
| `displayBazaarGrid` | 219 | 26280 | `CALL` | `31/5/1` | `pc215 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardMoney', R34=3201, R35=result pc7[3]` | 0 |
| `displayBazaarGrid` | 230 | 26324 | `CALL` | `31/4/1` | `pc227 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 234 | 26340 | `CALL` | `31/4/1` | `pc231 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 238 | 26356 | `CALL` | `31/4/1` | `pc235 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 242 | 26372 | `CALL` | `31/4/1` | `pc239 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 246 | 26388 | `CALL` | `31/4/1` | `pc243 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 250 | 26404 | `CALL` | `31/4/1` | `pc247 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=False` | 0 |
| `displayBazaarGrid` | 254 | 26420 | `CALL` | `31/4/1` | `pc251 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=False` | 0 |
| `displayBazaarGrid` | 258 | 26436 | `CALL` | `31/4/1` | `pc255 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 262 | 26452 | `CALL` | `31/4/1` | `pc259 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=False` | 0 |
| `displayBazaarGrid` | 272 | 26492 | `CALL` | `31/4/1` | `pc269 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=True` | 0 |
| `displayBazaarGrid` | 278 | 26516 | `CALL` | `31/4/1` | `pc275 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 282 | 26532 | `CALL` | `31/4/1` | `pc279 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=True` | 0 |
| `displayBazaarGrid` | 287 | 26552 | `CALL` | `31/5/1` | `pc283 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardMoney', R34=3201, R35=result pc7[7]` | 0 |
| `displayBazaarGrid` | 292 | 26572 | `CALL` | `31/4/1` | `pc289 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=True` | 0 |
| `displayBazaarGrid` | 296 | 26588 | `CALL` | `31/4/1` | `pc293 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=False` | 0 |
| `displayBazaarGrid` | 300 | 26604 | `CALL` | `31/4/1` | `pc297 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_RewardItemIcon', R34=result pc7[6]` | 0 |
| `displayBazaarGrid` | 304 | 26620 | `CALL` | `31/4/1` | `pc301 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemName', R34=result pc7[8]` | 0 |
| `displayBazaarGrid` | 311 | 26648 | `CALL` | `31/5/1` | `pc307 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemStack', R34=3189, R35=result pc7[7]` | 0 |
| `displayBazaarGrid` | 315 | 26664 | `CALL` | `31/4/1` | `pc312 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemStack', R34=True` | 0 |
| `displayBazaarGrid` | 320 | 26684 | `CALL` | `31/4/1` | `pc317 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemStack', R34=''` | 0 |
| `displayBazaarGrid` | 324 | 26700 | `CALL` | `31/4/1` | `pc321 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_PolishMAX_2', R34=result pc7[10]` | 0 |
| `displayBazaarGrid` | 330 | 26724 | `CALL` | `31/4/1` | `pc327 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_MateriaNumber', R34=True` | 0 |
| `displayBazaarGrid` | 334 | 26740 | `CALL` | `31/4/1` | `pc331 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemStack', R34=False` | 0 |
| `displayBazaarGrid` | 338 | 26756 | `CALL` | `31/4/1` | `pc335 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_MateriaNumber', R34=True` | 0 |
| `displayBazaarGrid` | 343 | 26776 | `CALL` | `34/2/0` | `pc341 GETGLOBAL A34 K='tostring'` | `none (global function)` | `R35=result pc7[11]` | open/dynamic |
| `displayBazaarGrid` | 344 | 26780 | `CALL` | `31/0/1` | `pc339 SELF A31 B0 K='setText'` | `R32=parameter A0 (SELF receiver)` | `open from R32 through active top` | 0 |
| `displayBazaarGrid` | 348 | 26796 | `CALL` | `31/4/1` | `pc345 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaBase', R34=False` | 0 |
| `displayBazaarGrid` | 352 | 26812 | `CALL` | `31/4/1` | `pc349 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaIcon', R34=True` | 0 |
| `displayBazaarGrid` | 359 | 26840 | `CALL` | `31/4/1` | `pc356 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_MateriaNumber', R34=True` | 0 |
| `displayBazaarGrid` | 363 | 26856 | `CALL` | `31/4/1` | `pc360 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_MateriaNumber', R34=False` | 0 |
| `displayBazaarGrid` | 367 | 26872 | `CALL` | `31/4/1` | `pc364 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_RewardItemStack', R34=False` | 0 |
| `displayBazaarGrid` | 371 | 26888 | `CALL` | `31/4/1` | `pc368 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaBase', R34=True` | 0 |
| `displayBazaarGrid` | 375 | 26904 | `CALL` | `31/4/1` | `pc372 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaIcon', R34=False` | 0 |
| `displayBazaarGrid` | 380 | 26924 | `CALL` | `31/4/1` | `pc377 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaBase', R34=False` | 0 |
| `displayBazaarGrid` | 384 | 26940 | `CALL` | `31/4/1` | `pc381 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_MateriaIcon', R34=False` | 0 |
| `displayBazaarGrid` | 388 | 26956 | `CALL` | `31/4/1` | `pc385 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_NotEquiped_2', R34=result pc7[12]` | 0 |
| `displayBazaarGrid` | 394 | 26980 | `CALL` | `31/4/1` | `pc391 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 398 | 26996 | `CALL` | `31/4/1` | `pc395 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 402 | 27012 | `CALL` | `31/4/1` | `pc399 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 406 | 27028 | `CALL` | `31/4/1` | `pc403 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=True` | 0 |
| `displayBazaarGrid` | 410 | 27044 | `CALL` | `31/4/1` | `pc407 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 414 | 27060 | `CALL` | `31/4/1` | `pc411 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=True` | 0 |
| `displayBazaarGrid` | 418 | 27076 | `CALL` | `31/4/1` | `pc415 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=379` | 0 |
| `displayBazaarGrid` | 422 | 27092 | `CALL` | `31/4/1` | `pc419 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=True` | 0 |
| `displayBazaarGrid` | 429 | 27120 | `CALL` | `31/4/1` | `pc426 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 433 | 27136 | `CALL` | `31/4/1` | `pc430 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 437 | 27152 | `CALL` | `31/4/1` | `pc434 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 441 | 27168 | `CALL` | `31/4/1` | `pc438 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 445 | 27184 | `CALL` | `31/4/1` | `pc442 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=True` | 0 |
| `displayBazaarGrid` | 449 | 27200 | `CALL` | `31/4/1` | `pc446 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=True` | 0 |
| `displayBazaarGrid` | 453 | 27216 | `CALL` | `31/4/1` | `pc450 SELF A31 B0 K='setIcon'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=380` | 0 |
| `displayBazaarGrid` | 457 | 27232 | `CALL` | `31/4/1` | `pc454 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=True` | 0 |
| `displayBazaarGrid` | 464 | 27260 | `CALL` | `31/4/1` | `pc461 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSingle', R34=False` | 0 |
| `displayBazaarGrid` | 468 | 27276 | `CALL` | `31/4/1` | `pc465 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSeparate', R34=False` | 0 |
| `displayBazaarGrid` | 472 | 27292 | `CALL` | `31/4/1` | `pc469 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarSet', R34=False` | 0 |
| `displayBazaarGrid` | 476 | 27308 | `CALL` | `31/4/1` | `pc473 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarBuy', R34=False` | 0 |
| `displayBazaarGrid` | 480 | 27324 | `CALL` | `31/4/1` | `pc477 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarRepair', R34=False` | 0 |
| `displayBazaarGrid` | 484 | 27340 | `CALL` | `31/4/1` | `pc481 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='TextBlock_ItemBazaarReward', R34=False` | 0 |
| `displayBazaarGrid` | 488 | 27356 | `CALL` | `31/4/1` | `pc485 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='IconControl_ItemBazaarStatus', R34=False` | 0 |
| `displayBazaarGrid` | 492 | 27372 | `CALL` | `31/4/1` | `pc489 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardItem', R34=False` | 0 |
| `displayBazaarGrid` | 496 | 27388 | `CALL` | `31/4/1` | `pc493 SELF A31 B0 K='setVisibility'` | `R32=parameter A0 (SELF receiver)` | `R32=parameter A0, R33='Grid_RewardMoney', R34=False` | 0 |
