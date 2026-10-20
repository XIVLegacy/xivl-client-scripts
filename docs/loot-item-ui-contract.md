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
