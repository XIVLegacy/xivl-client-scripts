# Item sub menu and discard flow

The [loot item UI contract](loot-item-ui-contract.md) opens `ItemListWidget` on
list 5 and names the Trash route in outline. This page records which sub menu
buttons the list shows for the loot list and for the bag, how each button
routes, and the discard confirmation branches. Line ranges are in the scripts
reproduced from the installed LPB files and cited in
[Evidence](#evidence). The values are Lua helper arguments. They are not a
recovered wire payload or a server effect.

## Sub menu button states

`openSubWidget` (`itemlistwidget.lua:5337-5940`) keeps one state value per
sub widget button and publishes each through `ItemSubWidget.setSubMenuVisibility`
(`itemsubwidget.lua:187-236`). The values are 0 (hidden and disabled), 1 (shown
and disabled) and 2 (shown and enabled). The focus request after the publish
selects the remembered button only when its state is 2, otherwise
`Button_Cancel`.

| List | Button states |
| --- | --- |
| 5 (loot) | `Button_DropItemGetAll` 2. `Button_DropItemGiveAll` 2 when `desktopWidget:countPartyMember()` is above 1, else 1. `Button_Trash` 2. `Button_Sort` stays 0 (`:5363-5376`) |
| 1 (bag), chosen package 1, item not equipped | `Button_Trash` 2 (`:5448-5456`) |
| 1 (bag), chosen package 1, item equipped | `Button_Trash` 1 (`:5471-5474`) |
| every list other than 3, 4 and 5 | `Button_Sort` 2 (`:5508`) |

`Button_Cancel` starts at 2 for every list. The state of `Button_Trash` for a
chosen package other than 1 is left at its initial 0 by the branches read.

## Button routing

`ItemSubWidget.processUICommandOperate` (`itemsubwidget.lua:239-384`) maps the
buttons to the parent widget and closes the sub widget when the parent returns
exactly true:

- `Button_DropItemGetAll` to `operateGetDrop`.
- `Button_DropItemGiveAll` to `operateShareDrop`.
- `Button_Trash` to `operateTrash`.
- `Button_Sort` opens the child widget `SortChangeWidget`.

`operateGetDrop` (`itemlistwidget.lua:4680-4722`) reads
`worldMaster:_getMyPlayer():_getItem(5, work.chosenItem)`. For a non-nil item it
takes `_countStack()` and `getItemProperPackage()` and calls
`desktopWidget:executePlayerItemMovePackage(5, chosenItem, properPackage, stack)`.
It sets `work.lastsub` to 6 when that call returns true and returns true
whether or not it did. A nil item returns nothing.

`operateTrash` (`itemlistwidget.lua:4613-4677`) opens `ItemEditWidget` through
`desktopWidget:openChildWidget("ItemEditWidget", W, true, true, 3,
chosenPackage, chosenItem, nil, W)`. On a true result it sets
`work.editWidgetOpen` to 1 and `work.lastsub` to 8, then opens the materia
list when the chosen item is equipment with attached materia.

## Item edit confirmation

`ItemEditWidget.setInitialData` (`itemeditwidget.lua:207-565`) sets
`work.error` to true when the owner's `checkChosenItem(item)` returns exactly
false (`:293-298`). `processBeforeShow` (`:568-609`) on a first show with
`work.error` true sets `work.chosenOperation` to 12, hands it to the parent's
`setItemEditData` and calls the parent's `closeItemEdit`.

`ItemListWidget.checkChosenItem` (`itemlistwidget.lua:6325-6383`) returns true
only when the optional package and item arguments equal the chosen ones, the
chosen package equals the list's package, the chosen item equals `work.index`
plus 1 and `_getItem(chosenPackage, chosenItem)` equals its item argument with
the Lua `==` operator. A package whose `_getItem` returns a fresh table on each
call therefore fails the last comparison.

`Button_OK` (`itemeditwidget.lua:666-810`) returns false while `work.enableOK`
is false. With `work.commandThrow` true it runs `checkCertainItem`
(`:850-988`):

- False: `work.chosenOperation` becomes 12, the parent's `setItemEditData`
  receives it with `work.mode`, the widget leaves modal state, focus returns
  to the parent and `closeItemEdit` runs. No waste request is made.
- True: `desktopWidget:executePlayerItemWaste(chosenPackage, chosenItem, num1)`
  runs. A true result sets `work.chosenOperation` to `work.mode`, calls
  `setItemEditData` with it and the mode, and calls `closeItemEdit`.

## Reproduction

Decode the three installed resources with `tools/retail_script.py` and the
pinned unluac jar, and compare the identities below with
`manifests/retail_lua_coverage.json`.

| Resource | LPB bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/1q5x561qn1635q.le.lpb` (`ItemEditWidget`) | 7538 / `8fa196b080212d6f720525b868ea6bb0bf68ffa36b7522eaad791c2719b1be75` | 7525 / `ae1ee7ba0f128c3128a1695b99177755e5a6590d240bb21e7f8de29b5c06fdf8` |
| `n1635q/1q5xrp8n1635q.le.lpb` (`ItemSubWidget`) | 3987 / `7f8b1c5d31b03d3718c84d7f8c101d1fa0c97050fcb7b200c426f568217e8ea4` | 3974 / `21bfcfbf2fcb5370e639c2154918a3e72c5bd69e8d6d5df25182f38f7ac5827b` |
| `n1635q/1q5xy1rqn1635q.le.lpb` (`ItemListWidget`) | 51910 / `f905d03e5b54218f690e37bf36db3f71f289468ff973004e1f030b684115e647` | 51897 / `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |

Read the functions at the line ranges above in the reproduced text. Search
for the button names and confirm that only the branch at `:5508` assigns the
`Button_Sort` state.

## Evidence

- `lua/scripts/widget/itemlistwidget.lua:4613-4722,5337-5940,6325-6383`
- `lua/scripts/widget/itemsubwidget.lua:187-236,239-384`
- `lua/scripts/widget/itemeditwidget.lua:207-609,666-810,850-988`
