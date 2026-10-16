# Bazaar and retainer client contracts

The client routes Bazaar listing, withdrawal and fulfillment through system
commands. Their operands are item/control references, numbers and explicit
nil positions. The native direct fallback conditionally serializes these in
serverbound `0x012D`; a dedicated fixed Bazaar packet layout and a complete
server result contract are not established.

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
`_callServerOnCommand` / `_doServerOnCommand` fallbacks. The runtime descriptor
record selecting the callback class for `commandRequest` remains unresolved.
A Lua descriptor name alone does not select that class.

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

`BazaarEditWidget.processUICommand` initializes its local mode operand to
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

`executeBazaarBuy(package,slot,count,extra)` resolves the Bazaar item and
calls `(24227,I,count,nil,nil,B,extra,catalog,nameIndex1,nameIndex2)`.
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

## Bazaar inspection and incoming packets

`checkBazaar` saves the current target (or player fallback) and calls
`executePlayerCommandLocal(24215,nil,nil,nil,nil,target)`.
`BazaarCheckCommand.canFire` requires the local living player, a nonnil
alive target, a living target when it is a player, and nonactive player mode.
`processChackBazaar` calls `orderBazaarWidget(1)`;
`processSetupBazaar` and `processSetupRetainerBazaar` call mode `2`.
The method names do not establish the server event that invokes them.

The mode-1 route opens `BazaarListWidget`, calls `updateItemPackage(8)` for
another actor, waits for widget creation and updates the Bazaar package.
The existing [market search contract](market-search-bazaar-client-contracts.md)
owns that display boundary. The original `checkBazaar` bytecode is connector
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

Lobby `0x0017` reaches `FUN_00DA4D80` with application data, as recorded in
`xivl-client-structs:manifests/symbols.json#BCS-Y-0022`. Direct disassembly
confirms the following bounded parser contract:

| Application offset | Native use and instruction locator |
| --- | --- |
| `+0x08`, u8 | Mask `0xfe` controls clearing the accumulator at `0x00DA4D8E`; inverse low bit supplies the return at `0x00DA4F18..0x00DA4F20`. |
| `+0x09`, u8 | Number of records iterated, at `0x00DA4DE4` and `0x00DA4F0B`. |
| `+0x10`, u16 | Zero-extended into operation `+0x200` when clearing, at `0x00DA4DD8..0x00DA4DDC`. |
| `+0x1c`, stride `0x30` | Record array, at `0x00DA4DF4..0x00DA4DFF`. |

A zero record dword `+0x04` skips that record. Otherwise the parser copies
all 48 bytes, appends to the operation accumulator, matches record `+0x04`
against character-slot `+0x04`, and upserts into the matched slot's vector
at `+0x2d0` (`0x00DA4E1A`, `0x00DA4E23`, `0x00DA4E95..0x00DA4EA0`,
`0x00DA4EF9`). `FUN_00DA94C0` rejects a zero record byte `+0x08` and uses
that byte as the upsert key (`0x00DA94C5`, `0x00DA9505..0x00DA950B`).
It replaces a matching 48-byte record or appends a new one.

`xivl-client-structs:manifests/structs.json#BCS-S-0004` owns the existing
record layout, including its ID and 32-byte name labels. The parser's bulk
copy does not independently prove those labels, class, level, location, or
listing count. The first unresolved field-semantic boundary in this trace is
the downstream consumer of the copied `RetainerListRecord`; a 496-byte catalog
packet label alone does not resolve it. Hiring/renaming event dispatch,
retainer result serialization, persistent mutations and settlement responses
also remain unestablished.

Native identity: retail `ffxivgame.exe`, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`, image
base `0x00400000`. Capstone 5.0.7 x86-32 disassembly of original PE bytes:
`0x00DA4D80`, 425 bytes, SHA-256
`ee7bdba9a54e7d742abd6d87416ef1ed3751f5bbfd26195647512d027c563c2e`;
`0x00DA94C0`, 131 bytes, SHA-256
`6b00ba1f92b0d39979074c48abcb9ed4a87cf3d1551304abd776546a68d451b6`.

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
| `widget/bazaareditwidget.lua` | `083f7cfea5a479cb882d6315cdcc4738996b23de82a161de5c0b55ae03161ac8` |
| `widget/bazaarlistwidget.lua` | `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |
| `chara/player/playerbaseclass.lua` | `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a` |
| `command/system/bazaarcheckcommand.lua` | `794fea44f175104e12e36d31a7e993c281309b68750af5f449f6df67466ae267` |
| `chara/npc/retainer/ordinaryretainer.lua` | `3b458d8430d91dc358921b5e0ae35e879e6c1e502124a62a1af6a9211861d25a` |
| `chara/npc/populace/populaceretainermanager.lua` | `5f07fe5973489b019a5958d203c9208858351effa83e69a2e328979deac32b09` |
| `widget/ask/retainernamingwidget.lua` | `53546cd0d0702e27ed30fd3c27b2faf92f87b4ed9b011d8b9d3813eb676d1dc3` |
| `chara/charabaseclass.lua` | `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9` |
| `command/commandbaseclass.lua` | `4d9cace900e712997f1a40663144d58f33b1f35f5a4aa521f637eb8c52364f25` |
