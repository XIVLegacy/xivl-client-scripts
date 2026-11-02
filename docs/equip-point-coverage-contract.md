# Equip point coverage contract

The retail item helper `getEquipmentEquipPointDetail` returns two slot lists
for each equipment item: the slots the item fits and the slots it covers.
This page records both lists for every equip point the helper handles. It is
static script evidence for extraction `2012.09.19.0001`. It does not show a
server reply, a captured equip attempt, or the client's native equipment
panel.

## Evidence identity

The helper and its consumers belong to these decoded scripts, pinned by
`xivl-client-scripts:manifests/scripts.json`:

| Script | Lines in manifest | Bytes | SHA-256 |
|---|---|---:|---|
| `lua/scripts/item/itembaseclass_common.lua` | 9729-9732 | 87762 | `7620492917230C3E060ED84D3197BF164C234A3AB73E48A0939BC65107F6B7FA` |
| `lua/scripts/chara/charabaseclass_battle.lua` | 393-395 | 35086 | `CA7D9BD52320E8AA62ECD853A0CE8D9E2E0DDC76FC504729B501B14B9BFCD959` |
| `lua/scripts/chara/charabaseclass_parameter.lua` | 417-419 | 36465 | `748C02DBF42329DD0B942642B5FE68B35F422DB61C482954E3B00D0338F12893` |

Line numbers below refer to the decoded canonical Lua with those hashes.
The equip point values come from `equipment.csv`, identified by
`xivl-client-data:manifests/tables.json:1291-1297` (SHA-256
`ACB958EF75422726F84DE5A087B5F335EBE148AA5C3C754E7F8B8E26F6084B9B`,
4875 data rows). Item names come from `csv/xtx_itemName.csv`
(`xivl-client-data:manifests/tables.json:6162-6168`).

## Equip point source

`ItemBaseClass.getEquipmentEquipPoint` reads the equipment sheet at the
item's catalog ID and column `69`
(`item/itembaseclass_common.lua:2255-2267`). `equipment.csv` stores that
column with type `s32`. Its data rows hold exactly these values, with the
row count in parentheses:

`0` (393), `2` (85), `5` (23), `6` (43), `9` (795), `10` (106), `11` (783),
`12` (106), `13` (494), `14` (413), `15` (477), `16` (105), `17` (68),
`36` (166), `37` (237), `38` (59), `39` (178), `40` (92), `42` (35),
`43` (1), `44` (6), `45` (64), `47` (65), `49` (81).

## Slot lists

`getEquipmentEquipPointDetail` takes the equip point and returns
`(fit, covered)` (`item/itembaseclass_common.lua:2324-2550`).
`isEquipmentEquipPointSimple` is true for points up to `27`
(2312-2321). The numbers in both lists are script slot numbers, the same
numbers `CharaBaseClass._getEquippingItem` takes. The main hand is slot `1`
(`chara/charabaseclass_parameter.lua:683-708`) and the body is slot `11`
(711-731).

| Equip point | Fit slots | Covered slots | Locator |
|---|---|---|---|
| `27` and below, including `0` | the point itself | none (`nil`) | 2331-2335 |
| `28` to `33` | no return | no return | 2336-2398 |
| `34` | `6, 7` | none | 2383-2390 |
| `35` | `6` | `6, 7` | 2374-2382 |
| `36` | `1, 2` | none | 2391-2398 |
| `37` | `1` | `1, 2` | 2338-2346 |
| `38` | `1` | `1, 2` | 2347-2355 |
| `39` | `1` | `1, 3` | 2356-2364 |
| `40` | `2` | `2, 4` | 2365-2373 |
| `41` | `11` | `9, 11, 13, 14, 15, 16` | 2401-2413 |
| `42` | `11` | `9, 11` | 2414-2422 |
| `43` | `11` | `11, 13, 14, 15` | 2423-2433 |
| `44` | `13` | `13, 15` | 2434-2442 |
| `45` | `20, 21` | none | 2481-2488 |
| `46` | `20` | `20, 21` | 2445-2453 |
| `47` | `18, 19` | none | 2489-2496 |
| `48` | `18` | `18, 19` | 2454-2462 |
| `49` | `22, 23, 24, 25` | none | 2497-2506 |
| `50` | `22` | `22, 23` | 2463-2471 |
| `51` | `24, 25` | none | 2507-2514 |
| `52` | `24` | `24, 25` | 2472-2480, unreachable |
| `53` | `26, 27` | none | 2517-2530 |
| `54` | `1` to `27` | none | 2533-2546 |
| `55` and above | no return | no return | 2531-2547 |

Points of `27` and below, including `0`, take the first branch at line
2331 and return the point itself as the only fit slot. Points `28` to `33`
enter the branch at 2336 and match no test. Point `52` has a test inside the
branch for points up to `51` (2472), which a value of `52` never enters.
The next branch tests only `53` (2515-2517), so `52` returns nothing.

The covered list always includes the fit slot when it is present, and the
extra entries are the slots the piece also occupies. A fit list longer than
one entry (points `34`, `36`, `45`, `47`, `49`, `51`, `53`, `54`) names
alternative slots, and these points return no covered list.

Catalog examples from `equipment.csv` and `xtx_itemName.csv`:

| Equip point | Item ID | Item name |
|---:|---:|---|
| `9` | 8010012 | Darksteel Celata |
| `11` | 8030116 | Darksteel Cuirass |
| `42` | 8032805 | Heavy Darksteel Armor |
| `42` | 8031801 | Dated Hempen Cowl |
| `43` | 8032102 | Reindeer Suit |
| `44` | 8051503 | Heavy Darksteel Flanchard |

## Consumers of the covered list

`isFitForEquipPoint(slot)` is true only when the item is equipment and
`slot` is in the fit list (`item/itembaseclass_common.lua:2285-2309`).

`isEquippingTwoHandedWeapon` reads the item in slot `1` and is true when its
covered list begins `1, 2` (`chara/charabaseclass_parameter.lua:683-708`).
That matches points `37` and `38` and no other point in the table.
`isEquippingFullArmor` is true when the slot `11` item has equip point `41`
(711-731).

`CharaBaseClass.isExistRemoveItemFromEquip(slot, mode, item)` answers whether
equipping `item` removes whatever sits in `slot`
(`chara/charabaseclass_battle.lua:200-274`):

1. When `mode` is `1` and the item in `slot` has zero compatibility for the
   new item's main skill, it returns true (lines 202-236).
2. When the new item has a covered list and `slot` is in it, it returns true
   if `slot` currently holds an item and false otherwise (237-259).
3. When the new item has no covered list and `slot` equals `mode`, it
   returns true if `slot` holds an item (260-269).
4. Otherwise it returns false (270-271).

So the script treats every slot in a covering piece's covered list as one
that the piece clears. The function reads the worn items only. It performs no
bag-space check, and it does not state where the removed item goes.

## Limits

- The script names no destination for a removed item and no refusal path.
  The server reply to such an equip request has no capture and is not
  established here.
- The helper reports slot numbers, not slot names. The only slot names
  supported are main hand for `1` and body for `11`. The other slot meanings
  depend on a consumer or on data outside this page.
- The covered list is a client-side prediction. Whether retail servers
  applied it identically, including for points `39` and `40` and for the
  alternative slots of fit-only points, is not shown.
- The call sites of `isExistRemoveItemFromEquip` are not in the Lua corpus,
  so the native caller and the text it shows are not recovered.
