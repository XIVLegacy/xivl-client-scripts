# Loot item command contract

The Main Menu checks package 5's count before adding command 0, then maps that
command to the desktop connector's `ItemListWidget` mode-3 opener. The count
check therefore gates this menu route indirectly. In mode 3, the widget
selects listbox 5, which reads capacity and item entries from package 5.

`ItemListWidget.operateGetDrop` calls the local command helper with the tuple
`(24223, item, item:getItemProperPackage(), 5, nil, nil, count)`. The share
widget also uses 24223 for self-claim/leave paths. Its other-member path calls
24225 with `(24225, item, 5, 5, nil, targetActor)`, where the helper resolves
the actor from the selected party-member index. The share widget's breakup
path resolves a package-5 item and calls `executePlayerItemWaste(5, slot)`;
the desktop connector then passes `(24226, item, 5)` to the local command
helper. `ItemSubWidget.Button_Trash` routes through
`ItemListWidget.operateTrash` to `ItemEditWidget`. The widget initializes
`chosenOperation` to 0; its Button_OK branch reaches the same waste helper only
when that field is still 0, Button_OK is enabled, `commandThrow` is active, and
`checkCertainItem` passes. Its count argument is not forwarded by the
connector helper. These are Lua helper arguments, not a recovered wire
payload or server effect.

These routes establish a package number and client-side arguments. The command
predicates and conditional request representation below do not identify
package 5 with a server-side inventory, establish a global package alias or
prove a command's server effect.

## Main Menu Booty and the initial list

`MainMenuWidget.processBeforeShow` requests `updateMainMenu` (`root/proto4`
PCs 28-29). `update` makes the same request (`root/proto7` PCs 0-1).
`updateMainMenu` resets the command count and Booty flag, runs the main,
ready and system command builders, and publishes `SystemMenu` (`root/proto15`
PCs 5-28 and 93-95). The system builder returns early when
`desktopWidget:isMyPlayerDead()` is truthy. Its next branch sets
`isBootyCommandShow` and adds system command 0 with text key 2127 and icon
289 only when `isExistDropItemCommand()` is exactly true (`root/proto12`
PCs 36-69). `addSystemCommand` refuses at a count of 15 or more, otherwise
uses the incremented count minus 1 as the row. For command 0 it writes
Help 74617 along with `SystemIcon`, `SystemEnable` as `True`, and
`SystemCommandID` as 0 (`root/proto17` PCs 0-24 and 136-192).

The connector's `isExistDropItemCommand` tests `getItemPackageCount(5) > 0`
(`root/proto69` PCs 0-7). The count helper reads the local player through
`_getMyPlayer`, returns 0 for exact false from `_hasItemPackage`, and
otherwise subtracts `_getItemPackageFreeSpace` from `_getItemPackageCapacity`
for the requested package (`root/proto404` PCs 0-17, assigned at root
PCs 1361-1364). This is the menu's occupied-slot check.

The standard `MainMenuWidget.form` lines 6 and 29 bind `ListBox_SystemMenu`
to the `SystemMenu` maker through `/System`. The template uses `SystemEnable`
on `Button_Command` at line 155 and formats `SelectedIndex` as the integer
parameter of `UILuaCommands.SelectionChanged` at lines 189-192. `init`
subscribes to that command on `ListBox_SystemMenu` (`root/proto0` PCs 48-51).
The handler hides the menu, reads `SystemCommandID`, `SystemCommandInfo` and
`SystemSubTarget` at the supplied row index, and passes them to
`executeCommand` (`root/proto1` PCs 210-235). Command 0 calls
`desktopWidget:openDropItemWidget()` (`root/proto16` PCs 202-206).
The command identity comes from the row data.

`openDropItemWidget` requests `openMainMenuRootWidget` with `ItemListWidget`,
nil, true and 3 (`desktopwidget_connector` `root/proto70` PCs 0-5).
The wrapper refuses while static widget 17 reports shown, otherwise uses
root opener kind 3 with the nil parent and the mode tail (`root/proto538`
PCs 0-15). The shared root opener requires an empty slot 3
(`root/proto535` PCs 4-18). [Root widget slots](desktop-widget-root-slots.md#occupancy-test-and-root-opener).

`ItemListWidget.init` requests form setup and initializes all six list boxes
before `setInitialData` (`root/proto0` PCs 207-230). Form setup includes
opening its `ItemSubWidget` child through `initChildWidget` (`root/proto1`
PCs 61-65). `setInitialData` requests the modal state, resets all six lists,
and calls `makeListFromPackage`, `makeDropItemList` and `makeMoneyList`
before the mode test (`root/proto3` PCs 0-27). Mode 3 writes raw selected
tab index 4 on `TabControl_ItemList` and sets `work.listbox` to 5
(PCs 29-36). `changeList` sets internal `work.mode` to 100 and title
text key 3213 for list 5, then seeds the index and focus place to 0 and
requests `updateWindowDisplay(true)` (`root/proto45` PCs 0-10 and 31-37).
The display request hides `Button_SortStatus` for list 5 and requests
`updateListFocus` (`root/proto15` PCs 15-35).

For its initial population, `makeDropItemList` reads package 5 capacity,
requests `SourceFirstIndex=0` and `SourceCount=capacity` on the list, and
writes `FilteredSortKey=sorttype` on the maker (`root/proto37` PCs 0-28).
It reads physical slots from 1 through capacity into zero-based rows. Only
an exact true from `setItemToXmlLight` advances the row. The other path
exits the loop before checking the stale suffix and publishing the maker
(PCs 29-65). A nil `_getItem(5,slot)` therefore ends the initial walk at
the first empty slot (`root/proto29` PCs 4-20). Each admitted item needs
`_getCatalogID`, `getItemIcon`, `_isStackable`, `_countStack` and
`_getNameIndex` before the two desktop XML helpers (PCs 21-34 and 87-118).
The builder finally sets the `TabItem_5` header using text key 3231 and
the package count (`root/proto37` PCs 89-102).

The standard `ItemListWidget.form` lines 10, 62 and 115-117 connect
`TabItem_5`, `ListBox_TabItem_5` and `TabItem_5_Maker` through `/TabItem_5`.
The published [list and item contract](item-list-widget-contract.md#row-write)
identifies the row arguments and conditional focus/detail callbacks. The
script requests establish a path to populate the form before an item
action. Physical row targeting, native item availability and the first
live draw remain unobserved.

### Reproduction

Verify the installed resources under `client/script`. Use
`tools/retail_script.py:decode_lpb` and `ChunkReader` and `instruction` in
`tools/build_quest_contracts.py`. PCs are zero-based. Check the cited call
operands and the loop exit at `ItemListWidget` `root/proto37` PC 45.

| Resource | LPB bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/x91wx5wpn1635q.le.lpb` | 19491 / `c0e1782a3ca183fcaa520a16320946f62d3fc861c74978cde19ea20fcd064b0a` | 19478 / `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2` |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `n1635q/1q5xy1rqn1635q.le.lpb` | 51910 / `f905d03e5b54218f690e37bf36db3f71f289468ff973004e1f030b684115e647` | 51897 / `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |

Decode the installed forms and templates with the SQEX basename rule.
Their identities are recorded in `xivl-decomp:docs/script/main-menu-command-route.md`,
Input and method, and `xivl-decomp:docs/resource/sqwt-xpath-data-sources.md`,
ItemListWidget.

## Command classes and eligibility

`xivl-client-data:manifests/staticactor_class_paths.json` maps these IDs to
the three named `/Command/System/` classes. Each authenticated leaf chunk
requires `SystemCommandBaseClass` and assigns only `canFire`. The inherited
`command` and `fire` false returns and shared player-command dispatch are
owned by the [shared command contract](linkshell-party-command-contracts.md#shared-dispatch-and-wire-representation).

For `canFire`, R0 is the command, R1 the initiating actor, and R2-R10 the nine
values after the command object. The published callers supply these complete
tuples; unsupplied trailing positions remain explicit nil:

| ID and class | Nine values after the command object |
| --- | --- |
| `24223`, `ItemMovePackageCommand` | `(item,destination,5,nil,nil,count,nil,nil,nil)`; destination is `item:getItemProperPackage()` |
| `24225`, `ItemTransferCommand` | `(item,5,5,nil,targetActor,nil,nil,nil,nil)` |
| `24226`, `ItemWasteCommand` | `(item,5,nil,nil,nil,nil,nil,nil,nil)` |

Move's source-package operand is R4, the literal 5. R3 is its destination,
rather than a second source identifier. Transfer also checks R4 as source;
its R3 value is not inspected by the leaf.

| Leaf | Refusal tests, in order |
| --- | --- |
| Move | R1 `isPlayer()` or `isMyPlayer()` is falsey; R1 `_hasItemPackage(R4)` equals false; R1 `_hasItemPackage(R3)` equals false; R2 `_isAlive()` equals false; R2 `_getPackage()` differs from R4; or R7 `< 1`. |
| Transfer | If R1 `isPlayer()` is truthy, `isMyPlayer()` must be truthy; otherwise `isRetainer()` must be truthy. Then refuse when R1 `_isAlive()`, R6 `_isAlive()`, R1 `_hasItemPackage(R4)` or R2 `_isAlive()` equals false, or R2 `_getPackage()` differs from R4. |
| Waste | R1 `isPlayer()` or `isMyPlayer()` is falsey, or R1 `_hasItemPackage(R3)` equals false. |

Each refusal returns one false; the remaining path returns one true. The
package and `_isAlive` tests compare exactly with false. The issuer-class
tests use Lua truthiness. These methods add no nil/type guard. Waste does
not inspect the item, while Move adds no available-quantity or count upper
bound check. The literal `< 1` rejection is not a universal numeric-domain
or server authorization rule. Shared admission and native predicates remain
separate.

## Conditional request representation

The authenticated `command.csv` source column 29 contains `-1,4,-1` for
`24223,24225,24226` respectively (physical lines `799,801,802`; numbered CSV
header 29 is field index 30 after the row key). Its SHA-256 is
`14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848`,
pinned by `xivl-client-data:manifests/tables.json`, entry `command.csv`.
The inherited desktop-mode default is false. For these system classes,
`CharaBaseClass.getCommandName` selects `commandRequest` for Move/Waste and
`commandContent` for Transfer. The latter therefore retains the additional
native `_canExecuteCommand` admission path described in the
[Bazaar command route](bazaar-retainer-client-contracts.md#command-identity-and-route).
A matching name does not establish the descriptor selected from the actual
player's vector.

If the shared block/nonblock dispatch and direct server fallback execute,
`xivl-client-structs:manifests/player_command_wire_contract.json` establishes
Map serverbound `0x012D`, its command-control-reference envelope and 128-byte
typed tail. The command sheet ID is not an extra scalar tail operand. For
ordinary integral numeric inputs, the three tuples become:

| Command | Typed values before finalization |
| --- | --- |
| Move | `T(item) I(destination) I(5) N N I(count) N N N` |
| Transfer | `T(item) I(5) I(5) N A(targetActor) N N N N` |
| Waste | `T(item) I(5) N N N N N N N` |

`I(v)` is tag `00` plus int32 bits in the normal big-endian branch; `N` is
explicit nil tag `05`; `A(a)` is tag `06` plus the resolved binding-reference
u32. A single item `T` is `07 R:u32be S:u16be P:u8`, with the item's resolved
binding reference, slot and native package byte. Those fields are not a
pending-drop ID or catalog item ID. The separate numeric package arguments
remain numbers. Serializer-generated `09 M1:u64be M2:u64be` can follow when
the canonical finalizer's flags permit it, before END `0F` and untouched
zero padding. That metadata is not another Lua argument or a quantity.
The canonical manifest owns grouping, metadata and endian conditions.

This supplies a conditional request-construction contract. The complete
retained EventStart owner census has 126 fields and no owner
`0xA0F05E9F`, `0xA0F05EA1` or `0xA0F05EA2`, the static command encodings for
these IDs (`xivl-captures:studies/director-wire-identity/derived/event-role-candidates.csv`).
It does not establish absence from arbitrary typed arguments or other caller
forms. No inspected record causally joins one of these commands to a reply,
pending-drop/session identity, ownership change, cancellation or settlement.
These client routes do not establish a lot/pass protocol.

## Evidence

- `lua/scripts/widget/desktopwidget_connector.lua:4386-4413,13454-13474,14800-14935`
- `lua/scripts/widget/mainmenuwidget.lua:1346-1358,2141-2145`
- `lua/scripts/widget/itemlistwidget.lua:495-574,1692-1711,2905-3031,4613-4677,4680-4750`
- `lua/scripts/widget/itemsharewidget.lua:203-264,294-313,331-368`
- `lua/scripts/widget/itemeditwidget.lua:162-165,207-251,666-740`
- `lua/scripts/widget/itemsubwidget.lua:354-362`
- `lua/scripts/command/system/itemmovepackagecommand.lua:11-65`
- `lua/scripts/command/system/itemtransfercommand.lua:11-73`
- `lua/scripts/command/system/itemwastecommand.lua:11-39`
- `lua/scripts/chara/charabaseclass.lua:399-496`, `getCommandName`
- `lua/scripts/command/commandbaseclass.lua:146-152`, inherited desktop-mode default

The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.

For the three leaf chunks, original LPB, decoded-payload and reproduced-source
identities matched those manifest entries at revision
`c25c9a6ffac823c7fa23d5c23ae8d9ed4a558be9`. Decoding used
`tools/retail_script.py:decode_lpb`; source reproduction and independent
instruction comparison used the pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
Offsets below are decoded-payload offsets; PCs are zero-based. Each root has
11 instructions at `0x20..0x48`, including the sole `canFire` assignment.

| Leaf `root/proto0` | Instructions, first through last start | Predicate PCs | Source assignment |
| --- | --- | --- | --- |
| Move | 45 at `0xF8..0x1A8` | Source package 12-18; destination 19-25; item/package 26-37; count 38-41; true return 42-43 | 65 |
| Transfer | 51 at `0xF5..0x1BD` | Issuer branch 0-16; issuer/target 17-28; source/item 29-47; true return 48-49 | 73 |
| Waste | 22 at `0xF2..0x146` | Issuer 0-11; package 12-18; true return 19-20 | 39 |

The name-selection recheck used only CharaBaseClass `root/proto17`, 95
instructions at `[0x12CC,0x1448)`: system priority tests at PCs 59/63 and
`commandContent` load at PC 65. The inherited desktop-mode default used only
CommandBaseClass `root/proto13`, three instructions at `[0x747,0x753)`,
including `LOADBOOL false` and a one-value return. Both raw and decoded
identities matched the same coverage manifest; no other shared body was
needed for this finding. Existing native serialization and dispatch evidence
was reused without reopening native bodies.
