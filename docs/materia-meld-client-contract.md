# Materia meld client contract

The client exposes an owner-side meld request through Bazaar mode `40` and
a crafter-side target contract widget. Its Lua distinguishes the request,
local melding, rate lookup, and melding another player's equipment. It does
not bind those stages to a complete server request/reply sequence.

The static sheets are exported as `xivl-client-data:derived/materia.csv`
and `xivl-client-data:derived/materia_book.csv`; their contract is
`xivl-client-data:docs/materia.md`. The 52-row `materiaBook` prose sheet has
no established key join to the 66-row `materia` sheet. Removal is separate:
[Materia removal client UI](materia-removal-client-ui.md).

## Owner request and cancellation

`Ask/MateriaAttachAskWidget` mode `2` reads the equipment and materia
indices from `ItemListWidget`. Install calls
`DesktopWidget.setMateriaAttachDeal(equipmentIndex,materiaIndex)`, sets the
item-list order time and closes the related selection UI. The connector
resolves both items in the local player's package `1`, then calls:

```text
executePlayerCommandLocal(24214,equipment,materia,40,nil,player)
```

`ItemListWidget.operateMateriaAbort` calls `setMateriaAttachUndeal()`, which calls
`executePlayerCommandLocal(24216,nil,nil,40,nil,player)`. This is a separate
helper; closing or backing out of the ask widget does not by itself prove
that this helper ran. Source: `widget/itemlistwidget.lua:5242-5250`.

Command `24214` maps to `/Command/System/BazaarDealCommand`, and `24216`
to `/Command/System/BazaarUndealCommand` in
`xivl-client-data:manifests/staticactor_class_paths.json`. For exact mode
`40`, the deal command checks that the first item is equipment with a
nonzero materia free index and no attached materia, and that the second item
is enchant materia. Those are client `canFire` checks, not server admission.

Canonical sources: `lua/scripts/widget/ask/materiaattachaskwidget.lua:754-827`,
`lua/scripts/widget/desktopwidget_connector.lua:18400-18449`, and
`lua/scripts/command/system/bazaardealcommand.lua:11-154`.
Bytecode: connector `setMateriaAttachDeal` prototype `0.416`, TAILCALL PC
`18` at `0x26F1C`; `setMateriaAttachUndeal` prototype `0.417`, TAILCALL PC
`9` at `0x26FDF`. The former passes command ID plus five operands; the
latter retains both leading nil item positions.

## Crafter and local-meld routes

`MainMenuWidget` selection `22016` and `ConsoleIconTrayWidget` control
`Button_Conditions_9` call `DesktopWidget.openMateriaAttachContractWidget()`.
Sources: `widget/mainmenuwidget.lua:2170-2174` and
`widget/consoleicontraywidget.lua:402-406`. The helper obtains the main target,
requires another player, refuses while static widget `17` is shown, and
opens the root widget as:

```text
openRootWidget(3,"Ask/MateriaAttachAskWidget",nil,false,100,nil,3,target)
```

Mode `3` stores the target actor, asks it to `updateItemPackage(6)`, and
sets common timer `5`. The update path reads that actor's package `6`.
Install requires item `2001002` or `2001003` in package `101`, the required
class to equal the player's main skill, and the required level not to exceed
the player's main-skill level. Refusals alert `40232`, `40234`, or `40235`.
It then calls `executeTargetMateriaJoinCommand(target)` and closes itself.
This widget does not offer an accept/decline result tuple carrying the
equipment and materia; it invokes the command helper directly.

The mode-3 update accepts only the stored target and package `6`, requires
exactly four package items, then supplies slots `1,2,3` to `setInitialData`.
An item-count mismatch closes the widget. The target helper scans slots
`1-4` of target package `6` for equipment,
enchant materia and catalog `1000001`. A second scan requires an item whose
catalog matches the materia's `getItemRepairItem()`. Missing any required
object returns `false`. It passes the equipment, materia and target to ready
command `22016`; the located currency and repair-item objects are checked
but are not separate operands at this call site.

| Connector helper | Exact ready-command call |
| --- | --- |
| `executePlayerMateriaJoinCommand(equipmentIndex,materiaIndex)` | `(22014,equipment,materia,nil,player)` using local package `1` |
| `executePlayerMateriaJoinRateGetCommand(equipmentIndex,materiaIndex)` | `(22015,equipment,materia,nil,player)` using local package `1` |
| `executeTargetMateriaJoinCommand(target)` | `(22016,equipment,materia,nil,target,nil)` using target package `6` |

`22014`, `22015` and `22016` map to `/Command/Game/CraftCommand` in the
static actor map. They are command IDs, not numeric network opcodes.
`executePlayerReadyCommand` resolves the ready-command index and command
object, returns `false` for unavailable indices, and replaces a nil third
operand with the ready-command variation. Thus the literal nil in this
table is not necessarily a nil at the eventual native command call.

Canonical sources: `desktopwidget_connector.lua:13737-13797,14120-14160,18674-18831`;
`materiaattachaskwidget.lua:411-604,624-674,829-918`.
Bytecode: connector target-widget prototype `0.285`, TAILCALL PC `27` at
`0x1F822`; local-meld prototype `0.425`, TAILCALL PC `27` at `0x27761`;
target-meld prototype `0.426`, TAILCALL PC `65` at `0x278FB`;
rate prototype `0.427`, TAILCALL PC `27` at `0x27A46`.
The ask-widget mode-3 package update is prototype `0.6`, count comparison
PC `19` at `0x1459` and data CALL PC `34` at `0x1495`. Its initialization
has one package-update CALL PC `145` at `0xFDA` in prototype `0.4`.

## Widget result and rate presentation

Mode `1` is the local confirmation path. Install with `rate < 100` opens
`MateriaAttachCautionWidget` with text rows `3544,3545,3546`; the other
branch closes the selection widget and sets base ask result `1`.
`processAskResult(1)` also closes `MateriaAttachWidget` and sets result `1`.
Back/Close sets `-1`; `getAskResult` translates `-1` to `nil` and otherwise
returns the base result. These are local confirmation values, not an
authoritative success result.

Mode `2` presents cost from the equipment's `getAttachMateriaAmount()` and
compares it with money on hand. Mode `3` displays the target package data.
The widget stores supplied rate as `work.rate`; zero disables Install.
Nothing here establishes the rate formula, a random roll, item consumption,
gil settlement, or successful equipment mutation.
Source: `materiaattachaskwidget.lua:89-234,411-604,754-976`.

## Sheet getters

`DesktopWidget` uses a materia type row and a quality argument `q` in
`lua/scripts/widget/desktopwidget_materia.lua:208-294`:

| Consumer | Sheet positions after the row ID | Bytecode |
| --- | --- | --- |
| `getMateriaCatalogID(type,q)` | `floor(q/4)` | Prototype `0.7`, floor CALL PC `3` at `0x9CF`, data CALL PC `8` at `0x9E3` |
| `getMateriaIcon(type,q)` | `38,39,40,41` for `q` in `0-3,4-7,8-11,12-15` | Prototype `0.6`, data CALL PC `28` at `0x8E5` |
| `getMateriaProperty(type,q)` | Four ordered values: `4`, `5+q`, `21`, `22+q` | Prototype `0.5`, data CALL PCs `8,14,20,26` at `0x798,0x7B0,0x7C8,0x7E0`; four-value RETURN PC `32`, `0x7F8` |

The two value pairs from `getMateriaProperty` feed `getItemParamString` and
the materia parameter labels. These consumers establish catalog, icon and
display-parameter uses. They do not make the quality argument a server grade
encoding or make any other sheet column a catalyst or success-rate field.

## Native and server boundary

The Bazaar request helpers share the conditional command transport described
in [Bazaar and retainer client contracts](bazaar-retainer-client-contracts.md)
and `xivl-client-structs:manifests/player_command_wire_contract.json`.
That manifest proves the native direct fallback builds serverbound `0x012D`;
the retained definitions and conditional constructors are recorded in
`xivl-client-structs:manifests/command_descriptor_registration.json`. Neither
proves which runtime descriptor a later invocation selected, that it took
the fallback, passed its send gates, or reached a server.

The ready-command routes additionally depend on runtime command availability,
variation and `CraftCommand` dispatch. Conversion is separate system command
`24240`, mapped to `ItemMaterializeCommand`; its `showResult` creates a
virtual item and displays `Ask/MateriaInformWidget`. That presentation does
not supply the two-player meld request. Source:
`lua/scripts/command/system/itemmaterializecommand.lua:30-76`.
This contract establishes no numeric
serverbound or clientbound opcode for the completed two-player meld,
no server opener for mode `2`, no counterpart notification ordering, and
no result packet or status that proves success or failure. The owner and
crafter flows above are separate client paths, not a captured interaction.

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
| `widget/ask/materiaattachaskwidget.lua` | `b5cdbfac344c7c966b08edad0ac48a22c8dcfdfcd8cd012e50ea13364efc6fd6` |
| `widget/desktopwidget_connector.lua` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/desktopwidget_materia.lua` | `834e5180a20668add24bafe7d94baa430dce855a13797d3038eab31a26392fb0` |
| `widget/itemlistwidget.lua` | `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |
| `widget/mainmenuwidget.lua` | `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2` |
| `widget/consoleicontraywidget.lua` | `498b25c7365180cd1ecff32d099ebc3e38fae0c6b6cd9d1f6e3a0953a33e3a7e` |
| `command/system/itemmaterializecommand.lua` | `c4e9b0572601b84436cf35bce6b3920d165f41ae73181075cc75f99b4ebe2450` |
