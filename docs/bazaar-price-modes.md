# Bazaar sale price modes

This record fixes the unit-versus-stack meaning of sale modes `11`, `12`, and
`13`, and separates those command modes from the row and native item fields
that the UI also calls a kind or a dealing value.

## Established sale contract

Let `Q` be the value read from `CustomControl_NumberInput_ItemSource` when
the seller presses Done, and let `R` be the price operand passed to
`setItemDeal(package, slot, mode, R, Q)`. The mode constants are named in the
native inventory manifest: `11` is `MODE_SELL_SINGLE`, `12` is
`MODE_SELL_PSTACK`, and `13` is `MODE_SELL_FSTACK`
(`xivl-client-structs:manifests/inventory_subsystem.json:148-163`).

| Sale mode | Seller quantity `Q` | Seller price `R` | Meaning of `R` | Dialog consumer |
| --- | --- | --- | --- | --- |
| `11` | `1` | `TotalGil` | Total for the one item; unit and total are equal | `ItemSource` is fixed to `1`; the editable price is `TotalGil` |
| `12` | Chosen `ItemSource` count, from `1` through the dialog maximum | `Gil` | Unit price | `ItemSource` is quantity; `Gil` is editable and `TotalGil = Q * Gil` |
| `13` | Chosen `ItemSource` count, from `1` through the dialog maximum | `TotalGil` | Total for the chosen stack quantity | `ItemSource` is quantity; `TotalGil` is editable and `Gil = floor(TotalGil / Q)` |

`BazaarEditWidget` captures `Q` before selecting the sale mode. Its mode-1
branch reads `TotalGil` and assigns mode `13` for the whole-stack choice,
reads `Gil` and assigns mode `12` for the per-unit choice, and reads
`TotalGil` and assigns mode `11` for a non-stackable item
(`lua/scripts/widget/bazaareditwidget.lua:2293-2342`). The common player call
passes the selected package, slot, mode, price and captured count in that
order (`lua/scripts/widget/bazaareditwidget.lua:2387-2396`). Thus `R` is
already a unit price for mode `12` and already a total price for modes `11`
and `13`; `setItemDeal` does not multiply or divide these values.

The source dialog initializes `ItemSource` from `1` through the source stack,
capped at `999` for crystals, and uses `unit = 1` for non-stackable items or
`unit = 3` for stackable items
(`lua/scripts/widget/bazaareditwidget.lua:651-686,760-881`). For a stackable
item, combo value `1` selects the per-unit presentation and combo value `0`
selects the whole-stack presentation. A quantity or `Gil` edit recomputes
`TotalGil` as `Q * Gil`; a `TotalGil` edit computes
`Gil = floor(TotalGil / Q)`. The combo value `1` then normalizes the total
back to `Q * Gil`, while value `0` preserves the entered total
(`lua/scripts/widget/bazaareditwidget.lua:3061-3378`). The Done branch checks
the same field that the selected presentation exposes before making the call
(`lua/scripts/widget/bazaareditwidget.lua:1951-2042`).

The mode `11` branch fixes `ItemSource` to `1`, sets both price controls from
the same `rewardprice`-style value, and displays a single-item label. The
mode `12` branch displays the unit price, limits the quantity by available
money when this is a buyer dialog, and sets the total maximum to
`unitPrice * sourceStack`. The mode `13` branch displays
`floor(totalPrice / sourceStack)`, fixes the quantity to `sourceStack`, and
keeps the total price as the visible value
(`lua/scripts/widget/bazaareditwidget.lua:1166-1495`).

## Bazaar rows and the buyer dialog

`BazaarListWidget.setItemToXmlLight` reads the bazaar item and its stack count,
then calls `DesktopWidget.setItemToXml` with the stackable flag and that count.
`makeBazaarItemList` iterates package `8` and invokes this helper for each local
bazaar slot (`lua/scripts/widget/bazaarlistwidget.lua:2435-2570`).
For this bazaar row kind, `setItemToXml` stores `stackCount` as the item count
when stackable and as `1` otherwise (`lua/scripts/widget/bazaarlistwidget.lua:1451-1536`; `lua/scripts/widget/desktopwidget_itemdetail.lua:185-305`).
`setItemToXmlLight` also reads the three deal-data returns for row visibility;
the list-property assignment is in `updateBazaarLabel`
(`lua/scripts/widget/bazaarlistwidget.lua:1550-1576,1947-2029`).
`BazaarListWidget.updateBazaarLabel` calls `getBazaarItemDealData`, stores its first return as
`bazaarkind`, and stores its second return as `rewardprice`. It classifies
kinds `11` and `12` as row status `1`, kind `13` as status `7`, and hides
numeric reward kinds `20` and `30`
(`lua/scripts/widget/bazaarlistwidget.lua:1947-2029`).

For the priced sale rows, the received field mapping is:

| Displayed kind | `TAG_DEALING` -> `bazaarkind` | `dealingAttached2 (+0x18)` -> `rewardprice` | Row `stackCount` -> buyer `ItemSource` |
| --- | ---: | --- | --- |
| `11` | `11` | Seller total `R` | Item count, then dialog forces `1` |
| `12` | `12` | Seller unit price `R` | Item count, then dialog allows `1..stackCount` |
| `13` | `13` | Seller stack total `R` | Item count, then dialog fixes `stackCount` |

`BazaarListWidget.getItemBazaarData` reads `bazaarkind`, `rewardprice`,
`rewardpackage`, and `rewarditem` directly from list properties. When a reward
package is present it reads the preceding reward row's `stackCount` and item
display fields (`lua/scripts/widget/bazaarlistwidget.lua:3075-3208`). The
selected-row path treats `bazaarkind` values `11`, `12`, and `13` as the sale
row family, compares that row's `rewardprice` with player money, and opens
`BazaarEditWidget` in mode `6` (`lua/scripts/widget/bazaarlistwidget.lua:4355-4428,4760-4809`).
The enable check repeats the same `rewardprice` comparison for each of the
three kinds, with no native dealing-field lookup
(`lua/scripts/widget/bazaarlistwidget.lua:4074-4182`).

In the mode-6 buyer dialog, the row's `bazaarkind`, `rewardprice`, and
`stackCount` are loaded into the work record, while player money is loaded
separately (`lua/scripts/widget/bazaareditwidget.lua:1166-1204`). The field
consumers are:

| Row kind | Row `rewardprice` | Buyer quantity | Buyer total field |
| --- | --- | --- | --- |
| `11` | `dealingAttached2` (`+0x18`) total for one item | Fixed `1` | Fixed to `rewardprice` |
| `12` | `dealingAttached2` (`+0x18`) unit price | Editable `1..stackCount`, capped by `money / rewardprice` | Recomputed as `quantity * rewardprice` |
| `13` | `dealingAttached2` (`+0x18`) total for the offered stack | Fixed to `stackCount` | Fixed to `rewardprice` |

For kind `13`, the dialog only derives a display unit value with
`floor(rewardprice / stackCount)`; it does not replace the total with that
unit value. For kind `12`, the source uses the direct division
`money / rewardprice` for the quantity cap and multiplies the chosen count by
the unit price when the quantity changes
(`lua/scripts/widget/bazaareditwidget.lua:1210-1417`; original-LPB PCs are
listed below).
On Done, mode `6` reads `ItemSource` first and `TotalGil` second, then calls
`executeBazaarBuy(package, slot, TotalGil, ItemSource)`
(`lua/scripts/widget/bazaareditwidget.lua:2877-2905`). The connector forwards
those arguments as ordinary command operands, with total price before the
chosen quantity (`lua/scripts/widget/desktopwidget_connector.lua:18452-18484`).

## Connector and native dealing fields

The ordinary sale price semantics are owned by the widget caller. The
connector's `setItemDeal` resolves the Bazaar item and defaults only a nil
quantity to its current stack count. Its mode-specific branch is only for
modes `20` and `30`; the original bytecode has a separate fallback for every
other mode, including `11`, `12`, and `13`
(`lua/scripts/widget/desktopwidget_connector.lua:18255-18339`). In the
fallback, the command tuple is `(24214, I, 1000001, mode, nil, B, Q, R)`;
there is no connector-side price multiplication or division.

The connector's `getItemDealDataLocal` calls the native-bound
`_getDealingInfo()` and `_getDealingAttached()` methods. For a numeric priced
tuple it copies the tuple's third value into its second Lua return; for a
referenced tuple it resolves the first value to an item and returns zero for
the numeric price (`lua/scripts/widget/desktopwidget_connector.lua:18095-18159`).
The Lua wrappers bind these calls to `_getDealingInfo_cpp` and
`_getDealingAttached_cpp` (`lua/scripts/item/itembaseclass_u.lua:114-131`).
`getItemDealData` supplies `worldMaster._getMyPlayer()` as the actor, while
`getBazaarItemDealData` supplies `getBazaarActor()` before calling the same
local helper (`lua/scripts/widget/desktopwidget_connector.lua:18164-18220`).
The promoted ItemBase bindings are `_getDealingInfo` firer `0x0074EBA0`
with implementation `0x00701E90`, and `_getDealingAttached` firer
`0x0074ECF0` with implementation `0x00701F20`
(`xivl-client-structs:manifests/control_class_napi_map.json:1064-1068`,
`xivl-client-structs:manifests/direct_emission.json:2013-2021`).

The native item record is a `0x70`-byte record. Its dealing fields are
`dealingValue` at `+0x12`, `dealingMode` at `+0x13`, `dealingAttached1` at
`+0x14`, `dealingAttached2` at `+0x18`, `dealingAttached3` at `+0x1c`,
`tags[4]` at `+0x20`, and `tagValues[4]` at `+0x24`
(`xivl-client-structs:manifests/inventory_subsystem.json:599-608`). The
native manifest names dealing modes `NONE=0`, `REFERENCED=1`, and
`PRICED=2`, separately from the sale command modes `11`, `12`, and `13`
(`xivl-client-structs:manifests/inventory_subsystem.json:148-163`).

The bounded native getter trace maps `_getDealingInfo()` to the
`TAG_DEALING=0xC9` tag/value lookup and returns one scalar tag value, rather
than a `(mode, value)` pair. The `updateBazaarLabel` path stores that first return directly
as `bazaarkind`, so the three sale rows have exact C9 tag values `11`, `12`,
and `13` for displayed kinds `11`, `12`, and `13`. This is the read-side row
mapping; the native writer is not inferred from the Lua command call. The
values are distinct from the record's `dealingMode` and `dealingValue` byte.

The canonical native trace records the priced `_getDealingAttached()` tuple as
`(dealingAttached1, dealingValue, dealingAttached2)`. Therefore the connector
second return used for row `rewardprice` is wire `dealingAttached2` at
`+0x18`; it is not `dealingValue` or `dealingAttached3`. Referenced mode
resolves `dealingAttached1` to an item and leaves the numeric positions empty.
The native constructor and getter identity, tool, and locators are recorded in
`xivl-client-structs:docs/bazaar-native-wire-contract.md#dealing-fields-read-by-lua`.
`BazaarListWidget.bazaarkind` is a list display
property and must not be substituted for native `dealingMode` or
`dealingValue`.

All three ordinary priced sale kinds use the same native field roles:

| Received field | Read-side role for kinds `11`, `12`, `13` |
| --- | --- |
| `tags[i]=0xC9`, `tagValues[i]` | Select the sale kind `11`, `12`, or `13`. |
| `dealingMode=2` at `+0x13` | Select the numeric attachment tuple. This is not a sale kind. |
| `dealingAttached1` at `+0x14` | Supplies the first numeric tuple value. The connector tests it for nonnil and distinguishes a number from an item; it does not use this number as the price or chosen quantity. |
| `dealingValue` at `+0x12` | Supplies the second tuple value, which this connector helper does not consume. |
| `dealingAttached2` at `+0x18` | Supplies the third tuple value, used as the row price. Its unit/total meaning follows the sale kind above. |
| `dealingAttached3` at `+0x1C` | Does not supply a price or quantity to this getter/dialog path. |
| Item quantity at `+0x08` | Supplies the listed stack count. The buyer takes one, a chosen portion, or the entire count according to kind `11`, `12`, or `13`. |

This is the client's read contract. It does not infer a server-side writer or
require an untested value for an attachment that the dialog ignores.

## Original bytecode crosschecks

The source member reader authenticated each named Lua member against
`manifests/scripts.json`. The original-LPB reader authenticated the wrapper
and decoded payload against `manifests/retail_lua_coverage.json` before
dumping prototype instructions. LPB decoding is the documented
`tools/retail_script.py:decode_lpb` path; instruction inspection uses the
repository's Lua bytecode tooling. The identities used here are:

| Decoded script | Script sha256 | Original LPB resource | LPB sha256 | Decoded payload sha256 |
| --- | --- | --- | --- | --- |
| `widget/bazaareditwidget.lua` | `13d066fe61bdf0d2a387fca7e221ba4fa2ce60dc3be0f9ca0a5c5b10fd6c9370` | `n1635q/89k99s561qn1635q.le.lpb` | `5ad478c18b05eda1d1be6869383666b05227769a45814aa079cf7b827bae7798` | `083f7cfea5a479cb882d6315cdcc4738996b23de82a161de5c0b55ae03161ac8` |
| `widget/bazaarlistwidget.lua` | `f539b71353ee2860f535bc962ca2038ecf51bf99fdbeca314ed1eaa20bc39164` | `n1635q/89k99sy1rqn1635q.le.lpb` | `8911334e4b425343fa491a3170c38fe6982449104eaea8f0c88860c97bd17a95` | `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |
| `widget/desktopwidget_itemdetail.lua` | `b1e5066fef70d5b7002abcd0fcb5440348f3db46062a8d2f23704957d2cc6dad` | `n1635q/65rzqvun1635q_1q5x65q91y.le.lpb` | `402e6e371a374441a9f6a391223f47a649b4ba5007e15b6a62378af2acfa5805` | `dea088111249bdfe99c5dae618a674c112859e1587f60bc1c57917f9b01cc180` |
| `widget/desktopwidget_connector.lua` | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `command/system/bazaardealcommand.lua` | `b48bf0b6a0e0a645f333576700cf06c84828550a5af66bfa1b8470c903c0126a` | `7vxx9w6/rlrq5x/89k99s659y7vxx9w6.le.lpb` | `dc9db8b89c5e0af3c883c0e2f10b3226a04336ef78a5c93ad0065f24e633bc3b` | `01e86c9adcee297a23c7e887b5c81b470869a58d7f6d49befff7cb6bc078c504` |

The ambiguous decompile branches are resolved by these original instructions:

- `BazaarEditWidget` prototype `0.10` begins at `0x344d`. Mode assignments
  are PC `238 / 0x3805` -> `13`, PC `244 / 0x381d` -> `12`, and PC
  `258 / 0x3855` -> `11`; the shared sale call is PC `308 / 0x391d`.
- `BazaarEditWidget` prototype `0.1` begins at `0x0aa4`. Its mode-6
  initialization compares kind `13` at PC `791 / 0x1700`, divides total by
  source count at PC `826 / 0x178c`, compares kind `12` at PC
  `875 / 0x1850`, divides money by unit price and clamps the count at PCs
  `943 / 0x1960` and `946 / 0x196c`, and multiplies unit price by source
  count at PC `963 / 0x19b0`. The kind `11` branch compares at PC
  `966 / 0x19bc` and sets `ItemSource=1`, `Gil=rewardprice`, and
  `TotalGil=rewardprice` at PCs `1013 / 0x1a78`, `1019 / 0x1a90`, and
  `1025 / 0x1aa8`.
- `DesktopWidget.setItemDeal` prototype `0.414` begins at `0x26b65`.
  PCs `17-22` at `0x26ba9-0x26bbd` test modes `20` and `30`; the calls at
  PCs `37 / 0x26bf9`, `54 / 0x26c3d`, and `67 / 0x26c71` include the
  numeric-reward, item-reward, and other-mode fallback branches.
- `BazaarDealCommand.canFire` prototype `0.0` computes
  `floor(mode / 10) * 10` at PCs `44-48 / 0x1a3-0x1b3` and tests the item
  family at PC `92 / 0x263`. Modes `11`, `12`, and `13` therefore share the
  family-10 item validation and have no distinct price validation branch.
