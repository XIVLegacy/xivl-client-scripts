# Bazaar and retainer client contracts

The client routes Bazaar listing, withdrawal and fulfillment through system
commands. Their operands are item/control references, numbers and explicit
nil positions. The native direct fallback conditionally serializes these in
serverbound `0x012D`. The native receive queue, package numbering and
publication dependencies are recorded in
`xivl-client-structs:docs/bazaar-native-wire-contract.md`. A complete
route-specific retail reply sequence is not established.

The [sale-price mode record](bazaar-price-modes.md) owns mode `11/12/13`
price, quantity and dealing-field consumers. The native record's "Purchase
freshness and the amount echo", "Settlement update dependencies", and "Command completion and item
locks" sections own the start discriminator, safe package publication and
command-lifetime findings. The actor sign and its false-value clear are in
`xivl-client-structs:docs/bazaar-appearance-contract.md`.

[Repair requests](repair-request-client-contract.md) distinguish equipment
request 24243 from Bazaar repair listing, withdrawal and fulfillment inputs.

## Command identity and route

| Command ID | Class path | Client role established here |
| --- | --- | --- |
| `24214` | `/Command/System/BazaarDealCommand` | Listing and materia attachment request `canFire` checks |
| `24215` | `/Command/System/BazaarCheckCommand` | Bazaar inspection eligibility and display methods |
| `24216` | `/Command/System/BazaarUndealCommand` | Withdrawal command with `canFire` returning true |
| `24227` | `/Command/System/BazaarTradeCommand` | Fulfillment command with `canFire` returning true |

The priorities come from `xivl-client-data:csv/command.csv`, rows
`24214,24215,24216,24227`, column `29`, pinned by
`xivl-client-data:manifests/tables.json` (source SHA-256
`14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848`).
The IDs and class paths are rows of
`xivl-client-data:manifests/staticactor_class_paths.json`. These are not
numeric network opcodes. `DesktopWidget.executePlayerCommandLocal` calls
`executeCommand` for the local player, checks `canCommand`, then calls
`PlayerBaseClass.command`. Inherited `CharaBaseClass.getCommandName` selects
`commandRequest` for a system command with priority `-1`. The listing,
withdrawal and fulfillment rows have that priority; inspection `24215` has
priority `4` and selects `commandContent`. `canCommand` skips
`_canExecuteCommand` for `commandRequest`
but still invokes the command's Lua `canFire` method. The command method
calls native `_executeCommand`.

Sources: `lua/scripts/widget/desktopwidget_connector.lua`, methods
`executeCommand`, `executePlayerCommandLocal`;
`lua/scripts/chara/charabaseclass.lua`, method `getCommandName`;
`lua/scripts/command/commandbaseclass.lua:117-125`, method `getPriority`; and
`lua/scripts/chara/player/playerbaseclass.lua`, methods
`canCommand`, `command`, `_onCommandRequest`, `_onCommandEvent`.
Bytecode: connector prototypes `0.272,0.273`; player prototypes `0.44,0.45`.
The local wrapper has ten formal arguments after self (command ID and nine
tail operands). It forwards the unsupplied trailing positions as nil.

The canonical native contract is
`xivl-client-structs:manifests/player_command_wire_contract.json`:
`nativeBindings`, `execution`, `directFallback`, `wire`, and `serializer`.
It distinguishes the blocking `_onCommandEvent` and nonblocking
`_onCommandRequest` descriptor routes, and the direct
`_callServerOnCommand` / `_doServerOnCommand` fallbacks. The retained
`commandRequest` definition has priority input 0 and selector 1. Under a zero
native selector global it constructs `CommandNonBlock`, as recorded in
`xivl-client-structs:manifests/command_descriptor_registration.json`. The
descriptor selected for a later invocation remains unobserved.

## Listing operands

Let `B = getBazaarActor()`, `I = getItem(B,package,slot)`, `m = mode`,
`R = reward`, `Q = chosen count`, and `RQ = reward count`.
`setItemDeal(package,slot,m,R,Q,RQ)` returns false if `I` is nil and defaults
only nil `Q` to `I._countStack()`. Numeric zero stays zero.

The following are exact calls to `executePlayerCommandLocal`; every literal
nil is an argument position.

| Condition | Call |
| --- | --- |
| `m == 20 or m == 30`, numeric `R` | `(24214,1000001,I,m,nil,B,R,Q)` |
| `m == 20 or m == 30`, item `R` | `(24214,R,I,m,nil,B,RQ,Q)`; nil `RQ` defaults to `R._countStack()` |
| Other modes, including `0` | `(24214,I,1000001,m,nil,B,Q,R)` |

The reward-first branch for both `20` and `30`, and the item-first fallback,
are established by original bytecode. The canonical decompile misstructures
these branches and must not be interpreted as requiring only mode `30` or
as removing the fallback. Connector prototype `0.414`, zero-based PCs
`17-22` at `0x26BA9-0x26BBD` select both modes; calls are PCs `37,54,67`
at `0x26BF9,0x26C3D,0x26C71`, each CALL `B=10,C=2`.
Canonical source: `desktopwidget_connector.lua:18255-18339`.

`BazaarDealCommand.canFire` requires the actor to be the local player, and
the Bazaar target to be that player or a `RetainerBaseClass` instance. Nil
mode defaults to `10`; numeric mode is preserved. It checks exact `40` as
the materia request, the `floor(m/10)*10 == 10` family as item-first, and
otherwise numeric first operands for positivity and available money when
the catalog is `1000001`. This does not supply a general server settlement
rule. See [Materia meld client contract](materia-meld-client-contract.md)
for the separate mode `40` callers.

## Widget callers, withdrawal and fulfillment

`BazaarEditWidget.processUICommandEvent` initializes its local mode operand to
`0`. Its mode-1 branch can replace it with `11`, `12`, or `13`; widget
modes `2` and `3` set `20` and `30`. Five direct `setItemDeal` calls pass
the selected package, slot, mode, reward and chosen stack. The item-reward
calls additionally pass a reward count. The initial `0` is a real fallback
operand and must not be normalized to `10`.

| Canonical caller lines in `widget/bazaareditwidget.lua` | Prototype `0.10` CALL PC / offset | Arguments after self |
| --- | --- | ---: |
| `2387-2396` | `308 / 0x391D` | 5 |
| `2497-2506` | `409 / 0x3AB1` | 5 |
| `2599-2609` | `502 / 0x3C25` | 6 |
| `2712-2721` | `603 / 0x3DB9` | 5 |
| `2814-2824` | `696 / 0x3F2D` | 6 |

The mode operand register is initialized at PC `0`, `0x344D`, and its
`11,12,13,20,30` assignments are at PCs `258,244,238,346,540`.
Back/Cancel selects operation `1`, returns it to the parent through
`setBazaarEditData`, and closes the edit UI. That local cancel path is
separate from withdrawing an existing listing and emits no `24216` command.

`setItemUndeal(package,slot,m)` requires a nonnil dealing item and calls
`(24216,I,nil,m,nil,B,I._countStack(),attachedCount)`. The attached count
starts at `1`, uses an attached item's stack when the attachment is an item,
and otherwise uses the third `_getDealingAttached()` result for a nonnil
attachment. Connector prototype `0.415`, TAILCALL PC `44`, `0x26DE9`.

`executeBazaarBuy(package,slot,value,extra)` resolves the Bazaar item and
calls `(24227,I,value,nil,nil,B,extra,catalog,nameIndex1,nameIndex2)`.
The mode-6 buy dialog supplies `TotalGil` as `value` and its chosen
`ItemSource` quantity as `extra`. It therefore echoes the amount selected by
the dialog; no fresh request ID or purchase counter is added. The native
record gives the conditional wire offsets and separates this amount echo
from a replay discriminator.
`executeBazaarSell(playerPackage,playerSlot,bazaarPackage,bazaarSlot)` resolves
both the Bazaar and player items, reads the Bazaar stack and attached-item
stack (default `1`), and calls
`(24227,bazaarItem,playerItem,attachedCount,nil,B,bazaarStack,catalog,nameIndex1,nameIndex2)`.
These are different operand shapes sharing one command ID. No total-price
scalar is computed at these call sites. A nil item returns false.
On a true command result, both record server time and add `3` for a local
Bazaar refresh delay. That boolean and timer are not a purchase receipt.

`BazaarListWidget.lua:5590-5595` calls `executeBazaarSell`, not `setItemDeal`.
The original bytecode is prototype `0.61`, CALL PC `50` at `0xA063`.
Connector buy/sell prototypes are `0.418` and `0.419`.
Canonical sources: `desktopwidget_connector.lua:18342-18397,18452-18597`.

## Conditional native wire construction

For the direct fallback, application offsets exclude the 16-byte game-message
prefix. The `0x012D` application payload is `184` bytes:

| Offset | Size | Proven input |
| --- | ---: | --- |
| `0x00` | 4 | Self actor object `+0x10`, little-endian |
| `0x04` | 4 | Resolved command control binding reference, little-endian |
| `0x08` | 4 | Self actor object `+0x14`, little-endian |
| `0x0C` | 4 | CRC32 over the exact 128-byte typed tail |
| `0x10` | 1 | Descriptor type reference |
| `0x11` | 32 | Inline descriptor name |
| `0x31` | 128 | Ordered typed argument stream |
| `0xB1` | 7 | Unresolved remainder |

The command object supplies an envelope binding identity; the command-sheet
ID is not separately inserted as an opcode or scalar ID. The serializer
starts after name and command object, preserving the remaining arguments.
Signed32 integral numbers use tag `00` plus four big-endian bytes; nil uses `05`;
control references use `06` plus a binding reference; item references carry
binding reference, slot and package through tags `07` or `08`. Consecutive
items with the same reference can coalesce without changing order. Optional
`09` metadata is serializer-generated, followed by terminator `0F`.
Zero padding is not nil. Numeric zero encodes `00 00 00 00 00`, whereas
nil encodes `05`. Currency IDs and amounts have no special encoding branch.
The native manifest owns the complete field, reference, metadata and send-gate
definitions. This is conditional construction, not evidence of an observed
or accepted Bazaar request.

For a single item the exact tuple is `07 R:u32be S:u16be P:u8`, where `R`
is the resolved binding reference, `S` the slot and `P` the package. A
non-item target is `06 R:u32be`. Quantity and price remain ordinary numeric
operands, not fields embedded in the item tuple. Integral operands use the
four-byte tag-`00` encoding above; nonintegral Lua numbers select tag `01`
and float32 bits. The manifest's `serializer.item` and `luaBridge.numbers`
own the native branch and range qualifications. Native item lookup subtracts
one from each Lua package and slot number. The tuple uses native indices;
Lua Bazaar package `8` is native package code `7`. The native record owns
the conversion locators and the c2s `0x0131` package-request layout.

## Wanted-item and materia-service issuers

Request kind `20` is the wanted-item editor path. `BazaarEditWidget`
mode `2` sets its window title from UI row `3127`, then assigns command
operand `20` when Done is processed. The English row is "Seek Item" in
`xivl-client-data:csv/xtx__text_ui.csv` and "Purchase Item" in the separate
`xtx__text_ui(2).csv` member. This consumer/text join establishes the
wanted-item role without inferring it from neighboring kind numbers.
Canonical Lua: `lua/scripts/widget/bazaareditwidget.lua:1039-1052,2435-2453`.
The two text members are pinned by `xivl-client-data:manifests/tables.json`:
SHA-256 `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`
and `e33205165bda559ed69bb63664514f0e12b7c29fc219d13ae17fa740985eca82`.
The text variants do not establish which member a runtime selected.

In the player branch, the editor obtains the requested count from
`CustomControl_NumberInput_ItemSource`. With a numeric reward it passes
`CustomControl_NumberInput_TotalGil` to `setItemDeal`. With an item reward
it resolves the selected reward item and passes its selected reward count
as the sixth helper argument. The connector emits the reward first:

| Kind-20 reward | Nine tail operands after command resolution |
| --- | --- |
| Numeric `R` | `1000001, I, 20, nil, B, R, Q, nil, nil` |
| Item `J` | `J, I, 20, nil, B, RQ, Q, nil, nil` |

Here `I` is the helper's selected item control, `J` the reward item control,
`B` the Bazaar actor, `Q` the requested count and `RQ` the reward count.
Only nil counts default to the corresponding item's stack; numeric zero
is preserved. This fixes operand roles and order, without establishing
server escrow, matching, partial fulfillment or settlement. Sources:
`bazaareditwidget.lua:2435-2610` and
`widget/desktopwidget_connector.lua:18255-18339`. Connector prototype
`0.414`, PCs `17-22` select the reward-first branch, and PCs `37/54`
at `0x26BF9/0x26C3D` issue its numeric/item calls. The wrapper adds the two
trailing nils. A true helper return closes the editor before a named
acknowledgement or changed row is awaited.

For kind `40`, owner confirmation in `Ask/MateriaAttachAskWidget` mode `2`
calls `setMateriaAttachDeal(equipmentIndex,materiaIndex)`. Both controls
come from local-player package `1`. The nine tail operands are
`equipment, materia, 40, nil, player, nil, nil, nil, nil`.
`setMateriaAttachUndeal()` instead resolves command `24216` and preserves
`nil, nil, 40, nil, player, nil, nil, nil, nil`. Closing a confirmation
widget alone does not prove that withdrawal helper ran. Eligibility,
owner confirmation and the distinct crafter command `22016` remain in
[the materia contract](materia-meld-client-contract.md#owner-request-and-cancellation).
The equipment/materia operands do not carry the received modifier block or
an offered price/count scalar. The service cost displayed by the widget
is not an additional operand at this call site.

Kinds `20` and `40` are operands of Deal command `24214`, not network
opcodes. The conditional direct fallback constructs serverbound `0x012D`.
The native record's conditional-layout tables own the offsets, including
same-owner item coalescing. The command helper result establishes neither
socket transmission nor server acceptance.

### Update and completion boundary for kinds 20 and 40

The ordinary Bazaar row consumer enumerates Lua package `8`. It stores
the first `getBazaarItemDealData` result as `bazaarkind`; kind `20` selects
its reward display category. That value comes from the `0xC9` tag's value
byte, not the incoming record's attachment-representation mode byte.
Sources: `widget/bazaarlistwidget.lua:1947-1986` and
`xivl-client-structs:docs/bazaar-native-wire-contract.md#dealing-fields-read-by-lua`.
An updated kind-20 row therefore needs compatible received item/tag state
and package publication. The request does not itself write the row.

The kind-40 crafter widget has a separate consumer: it requests the target's
Lua package `6`, accepts an update only for that actor/package, requires
four items, and reads slots `1-3` for presentation. The command helper
also scans slot `4`. These reads constrain the state consumed by the
crafter UI; they do not prove that a successful kind-40 Deal necessarily
caused a particular package-6 update. See
[the crafter route](materia-meld-client-contract.md#crafter-and-local-meld-routes).

For both kinds, the retained `commandRequest` route conditionally submits
through `_doServerOnCommand` and returns without a Bazaar-specific result
wait. Command completion, incoming item publication, confirmation UI closure
and actual fulfillment are separate boundaries. No route-correlated server
reply, admission result or settlement completion is established for either
kind. The shared Start/PackageStart/item-update/End dependency establishes
how received state becomes publishable, not which response a server sent.

The missing historical specimen must join a known `24214` invocation and
kind `20` or `40` to its complete typed operands, item identities, actor and
per-connection incoming event/item sequence. Kind `20` needs numeric and
item-reward examples with requested/reward counts and resulting package-8
rows and balances. Kind `40` needs owner equipment/materia identities,
the target package-6 publication and resulting equipment/materia state,
plus the distinct `22016` request if claiming fulfillment. Withdrawal needs
its own `24216` request-to-update join. Frame/subevent order, publication
callbacks and final visible state must be retained so receipt is not
mistaken for completion. The frozen corpus does not establish those joins;
new acquisition is unavailable.

### Settlement qualification by request kind

| Kind | Receipt or transition | Closest proven retail fact | Source and locator | Confidence | Remaining gap and finite source boundary |
| --- | --- | --- | --- | --- | --- |
| `20`, wanted item, numeric reward | **UNESTABLISHED**: accepted request, fulfillment, item transfer and currency settlement. | Deal `24214` carries `(1000001,I,20,nil,B,R,Q,nil,nil)`. The package-8 row reads kind from the received `0xC9` tag value. | [Wanted-item issuer](#wanted-item-and-materia-service-issuers), [update boundary](#update-and-completion-boundary-for-kinds-20-and-40); `xivl-client-structs:docs/bazaar-native-wire-contract.md#dealing-fields-read-by-lua`. | High for static operand and row-consumer facts; no completed retail transaction attribution. | Known request/control identities/counts -> per-connection admission/result -> package-8 and physical item changes -> reward/balance changes. The exact issuer/layout/publication contracts and retained command/widget metadata name no correlated settlement record. |
| `20`, wanted item, item reward | **UNESTABLISHED**: accepted exchange, partial/full fulfillment and reward-item transfer. | Deal `24214` carries `(J,I,20,nil,B,RQ,Q,nil,nil)`, preserving both counts and resolved references. | Same issuer and update sections; native record `#kind-20-and-kind-40-application-offsets`. | High for static construction; no completed exchange attribution. | Known requested/reward items and counts -> selected fulfillment request/result -> authoritative item/count and listing changes. Equal serializer references or a published row alone do not identify a successful exchange. The finite metadata and prior transaction ceiling provide no new discriminator. |
| `40`, materia request | **UNESTABLISHED**: accepted listing, service completion, equipment mutation and materia/catalyst/tool/currency settlement. | Owner Deal supplies equipment/materia from package `1`. The crafter separately consumes target package `6` and can issue ready command `22016`. | Same issuer and update sections; [materia settlement](materia-meld-client-contract.md#settlement-qualification); `xivl-decomp:docs/script/materia-command-dispatch.md#target-materia-command-22016`. | High for distinct static issuer/consumer paths; no historical transaction joins. | Owner `24214` -> admission and target package-6 publication -> crafter `22016`/actual category -> selected full result frame -> authoritative state. Generic item handlers, four displayed items and UI close do not close these edges. |
| Withdrawal, `20` or `40` | **UNESTABLISHED**: accepted withdrawal and release/replacement of the associated item or service state. | Separate `24216` helpers exist; kind `40` preserves both leading nils. | [Withdrawal](#widget-callers-withdrawal-and-fulfillment), [owner cancellation](materia-meld-client-contract.md#owner-request-and-cancellation); native record `#command-completion-and-item-locks`. | High for static helper shapes; no withdrawal attribution. | A known `24216` invocation -> its own received removal/replacement and item/balance consequence. Back/Close and the nonblocking return do not prove that occurrence. The retained command/widget metadata supplies no attributable withdrawal sequence. |

This qualification reuses the finite issuer, serializer, package-publication
and target-command studies. The retained Bazaar edit/list/command and materia
ask/connector metadata supplies no new concrete transaction source.
Known payload variants and constructors establish client-compatible shapes,
without observing a server transaction. Binding references, Lua/native
package/slot numbering, typed parameter order, endian qualifications and
callback selection retain their existing boundaries.

## Bazaar inspection and incoming packets

`executeBazaarCommand` saves the current target (or player fallback) and calls
`executePlayerCommandLocal(24215,nil,nil,nil,nil,target)`.
`BazaarCheckCommand.canFire` requires the local living player, a nonnil
alive target, a living target when it is a player, and nonactive player mode.
`processChackBazaar` calls `orderBazaarWidget(1)`;
`processSetupBazaar` and `processSetupRetainerBazaar` call mode `2`.
The method names do not establish the server event that invokes them.
The Check call has four leading nil operands and a target control reference,
with no item, quantity or price. The local wrapper supplies four more trailing
nils. Deal and Undeal each supply seven operands and acquire two trailing nils
from that same wrapper. These positions matter in the conditional typed stream.

The mode-1 route opens `BazaarListWidget`, calls `updateItemPackage(8)` for
another actor, waits for widget creation and updates the Bazaar package.
The existing [market search contract](market-search-bazaar-client-contracts.md)
owns that display boundary. The original `executeBazaarCommand` bytecode is connector
prototype `0.309`, TAILCALL PC `14`, `0x20A5E`.

MapClientbound `0x01DA-0x01DD` do not establish retainer result widgets.
`xivl-opcodes:opcodes.json`, MapClientbound rows for those four values,
records callbacks `0x00DB9090,0x00DB90A0,0x00DB90B0,0x00DB90C0`, each
`RET 0xC` without payload reads or state writes. Its cited native authority
is `xivl-client-structs:manifests/zone_dummy_callback_cluster.json`.
These are ZoneProtoDown callbacks. A separate application dispatcher calls
`FUN_004B6250`, `FUN_004B6270`, `FUN_004B6290` and `FUN_004B62C0` for
`0x01DA` through `0x01DD`, respectively. The authenticated dispatch sites
are `0x004CE307`, `0x004CE316`, `0x004CE325` and `0x004CE334`; see
`xivl-client-structs:manifests/search_recruitment_wire_contract.json`.
Invocation order between the two routes is unproved. These dispatch bindings
do not establish the commerce payload fields or widget-opening semantics.
The independent serverbound uses of the same integers are different routes.
No Bazaar-check reply packet, listing result code, or settlement result
mapping is established by the Lua methods above.

### Seller package updates and reply order

The local command return is a submission result. The Deal widget closes its
edit after a true return from `setItemDeal`; it does not wait there for a
named success packet or a changed dealing row. Undeal similarly returns the
command helper's result. Neither call site selects a server reply opcode.

`DesktopWidget.updateBazaarPackage` requests `updateItemPackage(8)` only for
another actor. It returns immediately when the Bazaar actor is the local
player. Its successful polling interval is 15 server-time units. Check's
mode-1 display route also requests package `8` only for another actor.
Thus package `8` polling is established for inspecting another Bazaar, not
as a seller acknowledgement after Deal or Undeal.

Incoming item updates have an independent presentation route:
`CharaBaseClass._onUpdateItemPackage(package,slots)` forwards the actor,
package and changed-slot collection to
`DesktopWidget.processUpdateItemInformation`. That method calls
`updateBazaarListWidget`, which selects the current Bazaar actor and passes
the update through `updateActorWidget`. Matching actor updates call the
widget's `updateItemList`; local-player updates for a different displayed
actor call `updatePlayerItem`. This establishes incremental UI consumption,
but the Bazaar list has a more specific dependency: `updateItemList` rebuilds
only for package `8`, subject to its update-counter and actor/editor-state
guards (`bazaarlistwidget.lua:5350-5414`). Callback delivery alone does not
guarantee a visible rebuild.

The seller list itself enumerates Bazaar package `8` through
`makeBazaarItemList` and `setItemToXmlLight`
(`bazaarlistwidget.lua:2435-2570,1467-1475,1550-1569`).
`DesktopWidget.getBazaarItem` calls the Bazaar actor's
`_getExtendedTemporaryItem(package,slot)`
(`desktopwidget_connector.lua:13545-13575`), and the row code filters
dealing and attachment state. It does not derive the listing by scanning
physical bag packages. `updatePlayerItem` updates capacity/money without
rebuilding the listing (`bazaarlistwidget.lua:5417-5475`). A seller edit
closed with nil sets `waitupdate` when `chosenOperation == 2`
(`bazaarlistwidget.lua:5489-5500`), without naming a received packet.

The native inventory family is independently catalogued in
`xivl-client-structs:manifests/inventory_subsystem.json`, sections
`inventory_opcodes` and `opcode_dispatch_table`: `0x0146` selects a package,
`0x0148-0x014C` supply item records, `0x014D-0x0151` supply linked-slot
records, `0x0152-0x0156` remove slots, and `0x016D/0x016E` bracket mutation
processing. Its item record carries dealing mode/value/attachment fields and
modifier data. The authenticated native continuation is
`xivl-client-structs:docs/bazaar-native-wire-contract.md`, section
"Incoming package operations and publication": receive handlers queue item
commands, package-start selects the destination, and end-command execution
publishes staged data or defers it. A nonempty changed-slot set reaches
`_onUpdateItemPackage` with Lua indices. Packet receipt and widget refresh
are separate boundaries. These shared handlers do not select a reply subset
by Deal, Undeal or Check ID, or fix event-call ordering against inventory
updates. The `0x0147` dispatch boundary does not establish a required end
acknowledgement.

For each of Deal, Undeal and Check, the exact seller reply sequence remains
unresolved. The missing specimen is a retail 1.23b seller main-connection
trace beginning before opening the seller's Bazaar, including a known
package/slot, listing mode, quantity and price, one successful Deal, one
successful Undeal of that listing, and Check on self. Preserve c2s command
and package requests, s2c event callbacks, all inventory-family records and
the resulting seller display. A synchronized inspector trace for Check on
that seller would distinguish inspector package `8` refreshes from seller
updates. Record TCP connection, direction, frame/subevent and complete typed
arguments for every operation. Include package-8 callback delivery and
resolved listing rows, so an inventory update is not mistaken for a seller
list rebuild. This specifies the missing specimen and evidence ceiling
within the frozen retail corpus; new retail acquisition is unavailable.

### Items with materia

In the inspected ordinary listing route, `setItemDeal` never reads materia
state and always passes the resolved item reference. Its only operand-shape
branch is mode `20/30` and numeric versus item reward. The ordinary Deal
`canFire` branch for modes `11/12/13` checks item identity and liveness,
without a materia-count test. `BazaarEditWidget` reads
`getItemMateriaAttachInfo` to display the attached count and icon, separately
from the listing calls. No separate ordinary listing command for an item
with attached materia is established by these callers.

Mode `40` is the distinct attachment-service request documented in
[Materia meld client contract](materia-meld-client-contract.md), separate from
the ordinary sale of equipment that already has materia.

The native serializer's names `M1/M2` identify two u64 slots in its optional
`09` trailer. Each collected value comes from the first eight-byte field of
a referenced item record, separately from its modifier block. Collection
tests zero sentinels, not materia count. The copy-chain evidence is canonical
in `xivl-client-structs:manifests/player_command_wire_contract.json#serializer.finalizer`,
with Ghidra locators and reproduction in the native record. Treating the
trailer as a materia listing mode would exceed that evidence.

Sources: canonical connector
`lua/scripts/widget/desktopwidget_connector.lua:800-854,5860-6046,6177-6200,6247-6285,6342-6368,14770-14800`,
`lua/scripts/chara/charabaseclass.lua:1276-1324`,
`lua/scripts/widget/bazaareditwidget.lua:537-582,2387-2396`, and
`lua/scripts/command/system/bazaardealcommand.lua:53-154`.
The original LPBs were decoded with `tools/retail_script.py:decode_lpb` and
inspected with the Lua 5.1 reader and instruction decoder in
`tools/build_quest_contracts.py`. Root closure assignments identify connector
prototypes `0.5,0.86,0.91,0.94,0.97,0.309` and CharaBase prototypes
`0.27,0.28`. Connector package `8` CALL is PC `30` at `0x781C`;
the local-actor return is PC `17` at `0x77E8`; item-update forwarding CALL
is PC `9` at `0x10C09`. CharaBase native package-request CALL is PC `9`
at `0x281C`, and update forwarding is PC `7` at `0x2904`.
Deal's exact-mode `40` branch starts at PC `49`, `0x1B7`, in prototype
`0.0`; its attached-count test is PCs `71-76`, `0x20F-0x223`.
These are static observations; no route-specific retail wire reply is
established here.

## Retainer events and local results

The exact widget tuples remain in
[Retainer widget results](retainer-widget-results.md). In particular,
`13` is `(13,package,item)` with no count; `21` has nine values including
bazaar type, reward price/package/item and both counts; `31/32` carry
package/item/count, with package `100` and the appropriate money index in
money-edit mode. These codes have no proven server-operation names.

`PopulaceRetainerManager.eventTalkStep4(a1,a2)` calls
`askRetainerNamingWidget(manager,a1)` and returns its result if it is a
string, otherwise `""`. `RetainerNamingWidget.getAskResult` returns `-3`
when `work.askAnswer == -3`, otherwise the name data or nil. That establishes
a naming interaction, not which server event hires or renames a retainer.
Sources: `chara/npc/populace/populaceretainermanager.lua:711-729` and
`widget/ask/retainernamingwidget.lua:480-520`.
Manager prototype `0.11`, naming CALL PC `4`, `0x162D`.

`OrdinaryRetainer.eventTalkRetainerItemTrade(mode)` and
`eventTalkRetainerItemList(mode)` use `1` to update packages and open their
respective widgets, `2` to update packages and collect a selection, and `3`
to close them. For trade result `31`, the caller resolves the selected item
on the retainer; for `32`, on the player. It validates the object and returns
the code, item object, package and count, followed by catalog/name data.
This resolves the selected owner but does not prove an entrust or withdrawal
transaction or its native response transport. The list method similarly
consumes its nine-value selection and validates referenced items; its returned
data must not be replaced with the widget tuple without tracing that branch.

For the list caller, let `I` be its resolved selected retainer item, `P` the
selected package, `Q` the selected count, `m` the Bazaar type, `RP/RI` the
reward package/slot, `V` the reward price and `RQ` the reward count. These
are caller returns, with `...name` preserving all `_getNameIndex()` results:

| Selection | Caller return prefix before `...name` |
| --- | --- |
| `13` | `(13,I,0,0,I._getPackage(),0,I._countStack(),0,I._getCatalogID())` |
| `21`, `m` is `20` or `30`, `RP == 0` | `(21,currencyItem,m,I,100,P,V,Q,currencyItem._getCatalogID())` |
| `21`, `m` is `20` or `30`, item reward | `(21,rewardItem,m,I,RP,P,RQ,Q,rewardItem._getCatalogID())` |
| `21`, other `m` | `(21,I,m,1000001,P,RP,Q,V,I._getCatalogID())` |

The currency branch scans retainer package `100` for catalog `1000001`.
Nonnumeric `Q` defaults to the selected item's stack, and nonnumeric `RQ`
in the item-reward branch defaults to the reward item's stack. This local
normalization does not identify a server decoder or an accepted mutation.
The final name call uses Lua multiple returns; a fixed arity must not be
inferred from temporary variables printed by the decompiler.

Sources: `chara/npc/retainer/ordinaryretainer.lua:263-415,418-818`;
`widget/desktopwidget_connector.lua:17036-17220`.
Trade prototype `0.6`, selection CALL PC `49`, `0x9B2`, has four results.
List prototype `0.7`, selection CALL PC `58`, `0xD68`, has nine results.
Retainer furniture and meeting-space scripts provide additional event wrappers;
they do not establish a numeric server event or packet binding.

Lobby `0x0017` parsing and retained-record consumers are documented in
`xivl-decomp:docs/net/retainer-lobby-record-consumers.md`. The native trace
establishes dword `+0x04` and byte `+0x08` matching keys, word `+0x0A` flag
uses, and conditional command 0x000F application-buffer construction from
the working snapshot. Its constructor and registration trace binds the paired
dispatcher-lookup calls to a no-op and identifies the carrier getter. Entry
registration also binds a constructed transport route's gate to a constant
true return. Conditional continuation constructs transport-buffer headers and
copies the selected carrier's payload, with one frame dword's value unestablished.
With a null optional callback and returning timing imports, it also stores a
symbolic timestamp and pads where required.
Runtime entry selection, allocation, synchronization and later call results
remain unproved, as detailed in the canonical finding. An independent callback
identity gap bounds the UI connection; server mutation policy remains unproved.

### In-game retainer roster source

`RetainerListWidget.updateRetainerData` reads
`DesktopWidget.countRetainerMember` and `getRetainerMemberInfo`, then passes
the six returned values to its row setters. The connector obtains these
values from `MyPlayer._getGroup(80001)`. This is a positive group-data route;
the matching widget name does not connect the roster to lobby `0x0017`.

| Returned position | Group getter |
| --- | --- |
| 1 | `getMemberWorkCoordinateId` |
| 2 | `getMemberWorkEmploymentState` |
| 3 | `getMemberLocation` |
| 4 | `getMemberRetainerLevel` |
| 5 | `_getMemberLocalizedDisplayName` |
| 6 | `getMemberTown` |

`countRetainerMember` returns nil when the group is absent; the widget turns
that nil into a zero count. `getRetainerMemberInfo` substitutes employment
state `127` for a player member, and the widget omits rows with that state.
The displayed level and location therefore do not establish fields of the
48-byte lobby record. The native implementation and population of this group
are outside this bounded roster trace.

Canonical sources: `widget/retainerlistwidget.lua:173-221,365-399` and
`widget/desktopwidget_connector.lua:17315-17415`. Original bytecode locators:

| Prototype and zero-based PC | Decoded offset | Operation |
| --- | --- | --- |
| RetainerListWidget `0.2`, PC 2 | `0x959` | Calls `countRetainerMember`. |
| RetainerListWidget `0.2`, PC 14 | `0x989` | Calls `getRetainerMemberInfo` with six results. |
| RetainerListWidget `0.2`, PC 15-16, 25 | `0x98D`, `0x991`, `0x9B5` | Skips state 127; otherwise forwards the display index and six values. |
| DesktopWidget `0.384`, PC 4-5, 11 | `0x25105`, `0x25109`, `0x25121` | Loads group 80001, calls `_getGroup`, tail-calls `_countMember`. |
| DesktopWidget `0.385`, PC 10-11 | `0x251CB`, `0x251CF` | Loads group 80001 and calls `_getGroup`. |
| DesktopWidget `0.385`, PC 16, 20, 24, 28, 32, 36 | `0x251E3`, `0x251F3`, `0x25203`, `0x25213`, `0x25223`, `0x25233` | Calls the six getters in table order. |
| DesktopWidget `0.385`, PC 50 | `0x2526B` | Returns six values. |

Root closure bindings identify these methods: RetainerListWidget PC 14-15
at `0x58..0x5C` binds child `0.2` to `updateRetainerData`; DesktopWidget
PC 1281-1284 at `0x1424..0x1430` binds child `0.384` to
`countRetainerMember`, and PC 1285-1288 at `0x1434..0x1440` binds child
`0.385` to `getRetainerMemberInfo`.

## Retainer withdrawal event result

`OrdinaryRetainer.eventTalkRetainerItemList(2)` selects
`Ask/RetainerItemListWidget`, whose code-22 result has four values. Let
`I = self._getItem(package,item)` and `m` be the returned Bazaar type.
The caller rejects a nil item or `_isAlive() == false`, then returns:

`(22,I,m,0,I._getPackage(),0,I._countStack(),A,I._getCatalogID(),...I._getNameIndex())`.

It initially obtains `A` from the third `_getDealingAttached()` result. If
the first result is an `ItemBaseClass`, it replaces `A` with that item's
stack count. Therefore `A` is not always an attached quantity: the native
priced representation supplies `dealingAttached2`, consumed as the sale
price by the [sale-price mode record](bazaar-price-modes.md). An unresolved
or absent attachment can leave `A` nil. The return includes all results of
`_getNameIndex`; the decompiler's temporary-variable list is not its arity.

The selected row has Lua package `8`, but the widget can return its reward
reference instead. The event returns the resolved item's `_getPackage()`,
not an unconditional literal `8` or `7`. The getter's one-based package
interpretation remains `INFERRED` in
`xivl-client-structs:docs/binding-map-native-contract.md`, "Item natives".
That native finding establishes a selected stored dword plus one, with a
separate nil-sentinel branch. This event branch performs no numeric package
conversion and does not call `setItemUndeal` or command `24216`.
The separately documented native package-7 serializer path must not be
assigned to this event result without a transport join.

The Ask widget disables input when it yields code `22` and sets its local
selection delay to `2`. A subsequent selection call invokes
`setAskParameter`, which records server time, resets result/operation/editor
state, redraws, and enables input. The selection handler compares elapsed
server time with that delay. These local steps do not identify a server
acknowledgement. `OrdinaryRetainer.eventReturnResult` handles only `31/32`;
it supplies no code-22 reply payload or success mapping. No required
withdrawal reply, completion event, or accepted mutation is established.

Sources: `chara/npc/retainer/ordinaryretainer.lua:749-818,1024-1051`,
`widget/desktopwidget_connector.lua:17165-17220`, and
`widget/ask/retaineritemlistwidget.lua:4484-4647,6500-6645` below
`lua/scripts/`. OrdinaryRetainer prototype `0.7` selects at PC `58`
(`0xD68`), tests `22` at PC `299` (`0x112C`), reads the attachment at
PC `315` (`0x116C`), and returns at PC `339` (`0x11CC`). The return-result
prototype is `0.9`. Connector `0.380` resolves the Ask widget at PC `12`
(`0x24D51`) and reads nine result positions at PC `25` (`0x24D85`), so the
four-value code-22 result leaves its remaining positions nil.

## Direct retainer repricing boundary

Both retainer item-list variants return false from `operateBazaarSell`
when `chosenPackage == 8`, before opening the price editor. Their buy and
repair editor methods have the same package guard. The ordinary and Ask
sale branches open `BazaarEditWidget` with mode `1` and owner selector `4`
only after that guard. The editor returns listing code `21`; this does
not provide a price-change code for an existing package-8 listing.

The finite literal-caller domain for `BazaarEditWidget` contains those six
retainer openings, three player-item openings, and the Bazaar-list opening.
The player-item sale opening uses owner selector nil; the Bazaar-list
opening uses mode `6`, owner `2`, and the established buyer route. Other
literal occurrences are class declarations, update/lookups or closes.
No direct repricing route for an already listed retainer package-8 item is
established in that domain. Dynamic widget names, a different native UI,
and server policy remain outside this result.

Sources: `widget/retaineritemlistwidget.lua:8080-8226`,
`widget/ask/retaineritemlistwidget.lua:4998-5202`,
`widget/itemlistwidget.lua:4329,4394,4459`, and
`widget/bazaarlistwidget.lua:4766` below `lua/scripts/`.
The sale guards are original prototypes `0.52` and `0.47`, PC `2` at
`0xCE49` and `0x8D1A`; both false returns are PC `5`. The retainer sale
editor calls are PC `22`, `0xCE99` and `0x8D6A`. The editor's retainer
code-21 call is prototype `0.10`, PC `336`, `0x398D`.

## Summoning-bell roster selection

`RetainerFurniture.eventPushStepOpenRetainerMenu` has no arguments after
self. It directly reads `MyPlayer._getGroup(80001)` and returns `0` if
the group is nil or its member count is less than `2`. Otherwise it opens
the retainer list with `(self,true,nil,6501)`. The list uses the
[in-game group roster](#in-game-retainer-roster-source).

After the widget returns a selection, the bell enumerates group member
indices `1..count`. Its separate display ordinal starts at `1` and advances
only when `isPlayerMember(index) == false`. When that ordinal equals the
widget result, it returns the group index. Thus, for members
`[player,retainerA,retainerB]`, displayed selections `1/2` map to group
indices `2/3`. These are group indices, not two possession bits or permanent
owned-slot identifiers. The bell remap itself tests player membership,
not employment state `127`.

The roster initializer stores each one-based UI row index in
`IntData.Value0`, and its Operate handler forwards that value as the answer.
Widget Cancel/Close returns `0`, which the bell preserves. It has no
post-widget nil-to-zero conversion: a nil result remains nil when no
ordinal matches. The later `eventTalkRetainerMenu` argument passed to
dismissal and its final choice-8 enable input do not supply this roster.
The dismissal widget wrapper does not read its additional argument.

The exact bell consumer therefore requires the in-game group snapshot,
including member count and player-member classification. No particular
incoming packet, native group-population field, possession-flag encoding,
or server ownership policy is established by this script join.

Sources: `chara/npc/object/retainerfurniture.lua:84-137,175-297` and
`widget/retainerlistwidget.lua:119-121,225-281,703-710` below `lua/scripts/`.
Furniture prototype `0.3` calls `_getGroup(80001)` at PC `6`, `0x51E`,
checks the count at PC `13`, `0x53A`, opens the list at PC `23`, `0x562`,
and tests `isPlayerMember` at PC `33`, `0x58A`. PCs `36-43`
(`0x596-0x5B2`) remap the ordinal to a group index and return it.
RetainerListWidget initializer `0.0` stores the UI loop index at PC `92`,
`0x57A`, through `IntData.Value0`.

The original-bytecode observations used `tools/retail_script.py:decode_lpb`
and `tools/build_quest_contracts.py:ChunkReader/instruction` with Python
3.12.0. Only the selected script paths and literal caller domain are covered;
no retail execution or authoritative server mutation is claimed.

## Source identity and locators

Extraction: `2012.09.19.0001`, retail 1.23b. Each named decoded Lua member
was checked against its `relativePath` entry in
[`manifests/scripts.json`](../manifests/scripts.json), including size,
SHA-256 and line count. Its installed original LPB and decoded payload were
checked against the `decodedScriptPath` entry and `matched-script`
classification in [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
The coverage entry owns the full LPB path, size and SHA-256.

Instruction locators use the original decoded Lua 5.1 chunk. `0` is the root
prototype, child indices and PCs are zero-based, and offsets are byte offsets
in that chunk. Lua line locators refer to the authenticated canonical member.
Decoded payload SHA-256 values pin the instruction offsets below.

| Decoded member below `lua/scripts/` | Decoded payload SHA-256 |
| --- | --- |
| `widget/desktopwidget_connector.lua` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/retainerlistwidget.lua` | `fe3e8dd4d738b61564443b6c1e06d28804d19ff6293eb49fb01f8e4a6c1d7ce8` |
| `widget/bazaareditwidget.lua` | `083f7cfea5a479cb882d6315cdcc4738996b23de82a161de5c0b55ae03161ac8` |
| `widget/bazaarlistwidget.lua` | `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |
| `chara/player/playerbaseclass.lua` | `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a` |
| `command/system/bazaarcheckcommand.lua` | `794fea44f175104e12e36d31a7e993c281309b68750af5f449f6df67466ae267` |
| `command/system/bazaardealcommand.lua` | `01e86c9adcee297a23c7e887b5c81b470869a58d7f6d49befff7cb6bc078c504` |
| `chara/npc/retainer/ordinaryretainer.lua` | `3b458d8430d91dc358921b5e0ae35e879e6c1e502124a62a1af6a9211861d25a` |
| `chara/npc/populace/populaceretainermanager.lua` | `5f07fe5973489b019a5958d203c9208858351effa83e69a2e328979deac32b09` |
| `widget/ask/retainernamingwidget.lua` | `53546cd0d0702e27ed30fd3c27b2faf92f87b4ed9b011d8b9d3813eb676d1dc3` |
| `chara/charabaseclass.lua` | `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9` |
| `command/commandbaseclass.lua` | `4d9cace900e712997f1a40663144d58f33b1f35f5a4aa521f637eb8c52364f25` |
| `widget/retaineritemlistwidget.lua` | `6409aeac17d051590b7e0f2b15466ed6d5678f146ff11cf867a8a2b313a23301` |
| `widget/ask/retaineritemlistwidget.lua` | `408cf496ed3fcda95c53a6925cc9c8e689c517e37893e6d566e55e0a64aae469` |
| `chara/npc/object/retainerfurniture.lua` | `4a8af6a781c1e364dbdba23eda8824845f4d05b2b755a30402f5b3e18b03cee7` |
| `widget/itemlistwidget.lua` | `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |
