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

## CraftJudge callback contract

The four methods below use the decompiler's zero-based positional names
`A0` through `A8`. Their bodies do not establish a command ID, actor class
or wire-field role for unused positions. In particular, `A0,A1,A2` are
unused by `askJoinMateria`, `displayRate` and `cancelTarget`;
`askJoinResult` uses `A1` only as the `_createVirtualItem` receiver and
does not use `A0,A2`.

| Method and canonical source in `judge/craft/craftjudge.lua` | Consumed arguments and local behavior | Exact Lua return |
| --- | --- | --- |
| `askJoinMateria(A0,A1,A2,A3)`, `994-1019` | Clears the main target, then calls `askEventModeWidgetYield("Ask/MateriaAttachAskWidget",1,A3)`. `A3` becomes the supplied `work.rate`. | One boolean: `false` if the first yielded value equals `false` or the second is not `1`; otherwise `true`. |
| `cancelTarget(A0,A1,A2)`, `1022-1030` | Clears the main target. No argument is consumed and no meld cancellation command is issued in this body. | Zero values. |
| `askJoinResult(A0,A1,A2,A3,A4,A5,A6,A7,A8)`, `1033-1060` | Creates equipment presentation item `E=A1:_createVirtualItem(A4,1,A5)` and materia presentation item `M=A1:_createVirtualItem(A6,1,1)`, then calls `askEventModeWidgetYield("Ask/MateriaInformWidget",1,A3,M,E,A7,A8)`. | Zero values; the yielded acknowledgement is discarded. |
| `displayRate(A0,A1,A2,A3)`, `1071-1087` | Clears the main target, then calls `askEventModeWidgetYield("Ask/MateriaAttachAskWidget",1,A3,true)`. `A3` becomes `work.rate`; the extra argument selects the presentation with Install hidden. | Zero values; the yielded widget result is discarded. |

The `1` after the widget path requests one widget result. It is not the
widget mode. `askEventModeWidgetYield` supplies widget category `4` and
forwards the remaining arguments through `askWidgetYield` and
`AskBaseClass.init` to `initAsk`. Thus the first and second data arguments
reach `MateriaAttachAskWidget.initAsk` as rate and the optional presentation
flag. Its omitted mode defaults to `1`. `setInitialData` tests that flag
against `nil`, hides Install and shows help text `3547` when it is present.
Source: `desktopwidget_connector.lua:25788-25855`,
`widget/ask/askbaseclass.lua:11-48`,
`materiaattachaskwidget.lua:182-245,411-499`.

Modes `1` and `2` share the local selection lookup: `initAsk` obtains
`ItemListWidget`, reads its equipment and materia indices, and calls
`setInitialData(localPlayer,1,equipmentIndex,materiaIndex,nil,flag)`.
A missing item-list widget sets base result `-1`. The equipment detail
consumer forwards the supplied rate to `setItemMateriaInstallRate`, which
formats it using `floor(rate*100)/100`, fractional digits and text row
`3570`. This is rate presentation, not its calculation from item data.
Source: `materiaattachaskwidget.lua:59-85,411-604` and
`widget/desktopwidget_itemdetail.lua:10429-10487`. Bytecode:
ask-widget prototype `0.4`, mode tests PCs `79,82`, shared initialization
CALL PC `109` at `0xF4A`; prototype `0.3`, rate-forwarding CALL PC `6`
at `0x7C5`; prototype `0.1`, detail CALL PC `22` at `0x459`.

The yielded tuple distinguishes completion from the local decision.
`askWidgetYield` returns one `false` when opening or selecting fails. After
completed selection it closes the widget and returns
`true,unpack(widgetResults,1,requestedCount)`. With requested count `1`,
confirmation is `(true,1)` and Back/Close completion is `(true,nil)`.
`askJoinMateria` reduces either failed yielding or a non-`1` decision to
one `false`; it returns neither an item pair nor a rate. The retail
bytecode uses open-arity `getAskResult`, table construction and final
return, despite the decompile's apparent fixed list of temporary values.
Source: `desktopwidget_connector.lua:25804-25855` and
`materiaattachaskwidget.lua:921-946`.

`cancelMainTargetCharacter` calls the local player's
`_setLockonTarget(nil)`, then `_setTargetCharacter(1,nil)` and
`afterTargetChanged(1,nil)` on the desktop widget. These are target-state
operations. Source: `desktopwidget_connector.lua:1612-1634`.

For result presentation, `MateriaInformWidget.initAsk` receives
`(A3,M,E,A7,A8)`. `A3` selects the positive/negative text and styles by
Lua truthiness. With equipment present the text rows are `3592/3593`;
without it they are `3590/3591`. `M` supplies the materia icon and name,
and `E` supplies the equipment icon and name. `A7` is the displayed materia
count, reduced by one only when `A3 == false`; `A8` controls
`IconControl_PolishMAX` visibility. The exact-false branch also presents a
catalyst derived from `M:getItemRepairItem()`. Operate and Cancel both set
the widget acknowledgement to `1`. This describes supplied result data,
not verification of inventory mutation. `A4,A6` are the first native
creation operands for `E,M`; the meaning of creation operand `A5` and the
native creation semantics are not established by these consumers.
Source: `widget/ask/materiainformwidget.lua:11-302`.

| Method | Authenticated retail bytecode |
| --- | --- |
| `askJoinMateria` | Prototype `0.29`, yield CALL PC `8` at `0x23F7`, `B=5,C=3`; comparisons PCs `9,13` at `0x23FB,0x240B`; one-value RETURN PCs `12,16,18` at `0x2407,0x2417,0x241F`, each `B=2`. |
| `cancelTarget` | Prototype `0.30`, target-clear CALL PC `2` at `0x24D1`; zero-value RETURN PC `3` at `0x24D5`, `B=1`. |
| `askJoinResult` | Prototype `0.31`, creation CALL PCs `4,9` at `0x2543,0x2557`, each `B=5,C=2`; presentation CALL PC `19` at `0x257F`, `B=9,C=1`; zero-value RETURN PC `20` at `0x2583`, `B=1`. |
| `displayRate` | Prototype `0.33`, presentation CALL PC `9` at `0x2671`, `B=6,C=1`; zero-value RETURN PC `10` at `0x2675`, `B=1`. |

Supporting anchors: connector `askEventModeWidgetYield` prototype `0.541`,
TAILCALL PC `5` at `0x32E4D`; `askWidgetYield` prototype `0.542`,
`getAskResult` CALL PC `19` at `0x32EEA` with `C=0`, SETLIST PC `20`
at `0x32EEE` with `B=0`, failure RETURN PC `29` at `0x32F12` with `B=2`,
and success RETURN PC `36` at `0x32F2E` with `B=0`.
`AskBaseClass.init` prototype `0.0` forwards varargs at CALL PC `25`,
`0x28C`, with `B=0`. `MateriaInformWidget.initAsk` prototype `0.3`
passes result, materia and equipment to the display helpers at CALL PCs
`4,9,15`, `0x783,0x797,0x7AF`; its equipment helper prototype `0.2`
passes `A8` to visibility at CALL PC `66`, `0x5B2`.

## Local operation binding

| Operation | Established local entry | Callback binding boundary |
| --- | --- | --- |
| Local meld `22014` | `MateriaAttachWidget.attachMateria` calls `executePlayerMateriaJoinCommand` with the selected equipment and materia indices. The connector resolves both in local package `1` and calls the ready-command helper as recorded above. | The `askJoinMateria` boolean and `askJoinResult` presentation contracts are independently recovered. No inspected Lua callsite binds either method to command `22014`. |
| Rate query `22015` | Three failed-requirement branches in `MateriaAttachWidget.attachMateria` call `executePlayerMateriaJoinRateGetCommand` with the same selected-index order, after class, level or repair-item alerts. | `displayRate` consumes a supplied rate and discards its widget result. No inspected Lua callsite binds it to command `22015` or supplies that rate. |

The producer/selector of these four callbacks remains unresolved.
`CraftCommand` supplies only action-gauge and aim overrides; inherited
`GameCommandBaseClass.fire` returns `false`.
The complete decoded corpus contains the four method declarations but no
other exact-name reference to them. Method names and the UI request routes
therefore do not establish a command-to-callback pairing.

Sources: `widget/materiaattachwidget.lua:749-995,1020-1075`,
`desktopwidget_connector.lua:13737-13797,18676-18709,18794-18827`,
`command/game/craftcommand.lua:1-46` and
`command/game/gamecommandbaseclass.lua:2657-2663`.
Bytecode: selection widget prototype `0.8`, local-meld CALL PC `203`
at `0x1CE3` and rate CALL PCs `123,152,184` at
`0x1BA3,0x1C17,0x1C97`, each `B=4,C=2`.
Connector ready helper prototype `0.279` obtains both ready values at
CALL PC `25`, `0x1EDE5`, `C=3`; nil comparison PC `28`, `0x1EDF1`,
and MOVE PC `30`, `0x1EDF9`, select the variation. Its TAILCALL PC `39`,
`0x1EE1D`, passes the command and substituted operands onward.

### Ready variation and command-name selection

The desktop lookup maps `22014` to ready index `15` and `22015` to `17`.
`updateReadyCommand` fills `work.commandIndex` by scanning the player's
ready slots and recording the slot for each recognized command ID. A later
matching slot overwrites an earlier one. The desktop index is therefore
not the ready slot passed to `getReadyCommand`.

Both commands obtain their variation from the second result of
`getReadyCommand(work.commandIndex[readyIndex])` because their supplied third
operand is nil. The getter returns `charaWork.command[index]` and
`charaWork.commandCategory[index]`. The latter is declared as an
`integer8[64]` array, included in local-player synchronization and bound by
`_bindWork(3003,"charaWork","commandCategory")`. This identifies the Lua
field read for variation. It does not recover its native writer or a numeric
value for a particular invocation.

The retained property-stream join in
`xivl-client-structs:manifests/command_slot_context.json`, `commandId` rows
`22014,22015`, records command assignments at property array slots `19,16`
respectively, with empty `categoryObservations` for both. Its SHA-256 is
`6d6141b254a6c33cb1a0ca7c7cfc6a1d4017f64693868a6fb4ade4db6ca02e81`.
Those are qualified static-actor identity joins, not observed Lua ready-slot
state. Category value `1` observed for other commands cannot supply either
materia variation. The catalog also leaves the native property-cache-to-Lua
work-3003 bridge unresolved. Its scope is explained in
`xivl-client-structs:docs/actor/command-slot-context.md`, sections
"Observed loadout writes" and "Category observations".

The authenticated `command.csv` rows select the Lua command name:

| Command row key | Column `29` (`s32`, priority) | Column `32` (`bool`, craft-judge predicate) | Selected name |
| --- | --- | --- | --- |
| `22014` | `6` | `true` | `commandJudgeMode` |
| `22015` | `6` | `true` | `commandJudgeMode` |

Columns use the CSV header labels, excluding the row key. `CraftCommand`
inherits `GameCommandBaseClass` and `CommandBaseClass` without overriding
`getPriority`, `isJudgedAtCraftJudge` or `isDesktopCommandMode`.
`CommandBaseClass.getCommandData` reads `commandSheet` at the command ID and
requested column. `CharaBaseClass.getCommandName` first selects `commandWeak`
for priority `6`, then replaces it with `commandJudgeMode` when the craft
predicate is truthy. The rows and class chain establish this static selection,
not the loaded native descriptor or successful admission.

After `canCommand` returns exactly `true`, `PlayerBaseClass.command` passes
the selected name, command actor and operands to `_executeCommand`. The local
meld and rate routes preserve equipment, materia and the substituted variation
as the first three operands. Neither that name nor the variation selects one
of the four callback methods in the inspected Lua.

Sources: `desktopwidget_connector.lua:12350-12489,13737-13797`,
`chara/charabaseclass.lua:294-341,400-455,569-578,779,948`,
`chara/player/playerbaseclass.lua:1047-1053,1911-1964,1978-2020` and
`command/commandbaseclass.lua:14-21,51-59,123-131,146-149`.
The command rows are `csv/command.csv:40-41`, extraction
`2012.09.19.0001`, authenticated by
`xivl-client-data:manifests/tables.json`, entry `command.csv`, SHA-256
`14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848`.
The class-path mapping remains
`xivl-client-data:manifests/staticactor_class_paths.json`,
`/Command/Game/CraftCommand` range.

Bytecode: `CharaBaseClass.getReadyCommand` prototype `0.14` loads the
command and category at PCs `36-41`, `0x1038-0x104C`, and returns both at
PC `42`, `0x1050`, `B=3`. `getCommandName` prototype `0.17` calls the
craft predicate at PC `40`, `0x136C`, and loads `commandJudgeMode` at PC
`51`, `0x1398`. `CommandBaseClass` prototypes `0.4,0.10` load columns
`32,29` at PCs `1`, `0x474,0x68A`, and tailcall at `0x478,0x68E`.
`PlayerBaseClass.command` prototype `0.44` calls `_executeCommand` at PC
`47`, `0x431E`, `B=13`.

### Incoming delegation boundary

`PlayerBaseClass.delegateCommand(p0,p1,p2,...)` forwards
`p1:_callFunction(p2,p0,...)` and tail-returns the boundary call's complete
result sequence. Here `p0,p1,p2` are positional arguments entering the
delegate. The Lua selects `p1` as the target, forwards `p2` unchanged as the
first explicit operand, then supplies `p0` and every trailing argument.
These positions do not identify packet owner/trigger fields or a particular
CraftJudge receiver.

Source: `chara/player/playerbaseclass.lua:2162-2172`. Original prototype
`0.52` uses VARARG PC `3` at `0x4BE4`, `B=0`, and TAILCALL PC `4` at
`0x4BE8`, `A=4,B=0,C=0`. The open tail is not limited to the decompiler's
single apparent temporary. The two `delegateEvent` adapters and their
different prefix order are recorded in the
[supplied dialogue consumer](passivegl-craft-columns.md#supplied-dialogue-consumer).

`ActorBaseClass._callFunction_inl` returns exactly the descriptor strings
`"self","_callFunction_lua"`; its body does not invoke a callback.
Source: `actorbaseclass_u.lua:24-31`, prototype `0.2`, LOADK PCs `0,1`
at `0x2A6,0x2AA`, RETURN PC `2` at `0x2AE`, `B=3`.
The implementation and conditional native alias installation are recorded in
`xivl-decomp:docs/script/lua-call-function-bridge.md`, sections
"Embedded implementation" and "Class table and installed closure". The embedded Lua
body consumes its name argument by indexing the receiver, then calls the
resolved value with that receiver followed by every trailing argument.
Through the recovered native forwarding closure and successful alias, composing
that body with `delegateCommand` calls the lookup result `p1[p2]` with
supplied arguments `(p1,p0,...)`.
If that lookup selects a CraftJudge callback, its supplied `A0` is `p1`,
`A1` is `p0`, and subsequent positions come from the delegate's trailing
arguments. These are conditional positional relationships. They establish
neither the actor roles of `p0,p1`, the actual function/table used by a
historical invocation, nor a callback selector for command `22014` or `22015`.

The complete admitted capture prefix-string census is recorded in
`xivl-captures:studies/local-guildleve-dialogue/derived/accounting.json`,
`corpus.all_admitted_0x0130_delegate_prefix_string_counts`, with scope and
reproduction in that study's "Delegated prefix-string census" section.
The accounting SHA-256 is
`3c349ec3dacba303d26c9666e487353193b7f662a967587dce52c4fd090dec15`.
Neither its outer function-name census nor its delegated prefix strings
contains the four CraftJudge materia callback names. This is a retained
capture boundary, not a command-to-callback pairing or a complete argument
decoder. The actual selector and callback argument vector for a materia
invocation remain unobserved.

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
variation and the native descriptor selected for `commandJudgeMode`.
The first equal native name match depends on runtime registration records,
their type bytes and the actual player's command vector. The conditional
request bridge and precise selector boundary are recorded in
`xivl-decomp:docs/script/materia-command-dispatch.md`, sections
"Generic command request bridge" and "Unresolved callback selector".
Neither the selected native `commandJudgeMode` descriptor nor a correlated
callback name/argument input was observed for `22014` or `22015`.

To recover the numeric variation, retain the selected ready slot, command
actor and `charaWork.commandCategory` value together. To establish callback
binding, retain that invocation's selected native descriptor and a producer
or correlated dispatch record identifying the CraftJudge receiver, method
and positional arguments. The generic incoming function-name decoder is
only a candidate until such a connection is established. The minimum required
invocation record is specified in
`xivl-decomp:docs/script/materia-command-dispatch.md`, section
"Minimum missing invocation record". It requires a causal producer-to-callback
join; client-side timing alone does not recover a server binding.

The conditional native policy dispatch can call the generic player hooks
`_onCommandEvent` or `_onCommandRequest`, as recorded in
`xivl-decomp:docs/input/chara-selection-producers.md`, section
"Native command construction and policy dispatch". Their Lua continuations
are distinct:

| Hook | Conditional request continuation |
| --- | --- |
| `_onCommandEvent` | For these IDs, calls `_callServerOnCommand(name,command,...)` directly. Its special `fire` check applies to command `24105`. |
| `_onCommandRequest` | Tries `command:command(player,...)`, then `command:fire(player,...)`. If both are falsey, calls `_doServerOnCommand(name,command,...)`. The recovered CraftCommand class chain inherits false-returning implementations of both probes. |

Both request calls forward all incoming varargs. Apparent fixed-length
temporary lists in the decompile do not define their arity. The original
`PlayerBaseClass` prototypes `0.42,0.43` use open VARARG/CALL pairs:
PCs `14/15` at `0x4016/0x401A` and PCs `15/16` at `0x41FF/0x4203`,
respectively, each with `B=0` and the CALL with `C=1`. Sources:
`chara/player/playerbaseclass.lua:1819-1907`,
`command/commandbaseclass.lua:236-247` and
`command/game/gamecommandbaseclass.lua:2657-2663`.
These conditional outgoing continuations do not identify the later
CraftJudge callback or its incoming arguments.

Conversion is separate system command
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
The retained `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader,instruction` reproduce the
chunk parsing and instruction operands without running the client.

| Decoded member below `lua/scripts/` | Decoded payload SHA-256 |
| --- | --- |
| `actorbaseclass_u.lua` | `28d5d3b3fcd26cdb18394b3e9d937b3a5514cf8ff0b3b4c4196efda82d4596b1` |
| `chara/charabaseclass.lua` | `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9` |
| `chara/player/playerbaseclass.lua` | `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a` |
| `command/commandbaseclass.lua` | `4d9cace900e712997f1a40663144d58f33b1f35f5a4aa521f637eb8c52364f25` |
| `judge/craft/craftjudge.lua` | `0dff8463d2b685ff65a23afcf5e52e451e531e6fac194fd088adba3d05dbd0ff` |
| `command/game/craftcommand.lua` | `72a26dc9c62a3b9545e4051f2cb6b92c046e7dfc2a1b52fbb17cd7ebb424cf68` |
| `command/game/gamecommandbaseclass.lua` | `1b3ba520dc0efb2f1941d2b8206d33f7a2e1a8ee52a6012092563395f853a6f7` |
| `widget/ask/askbaseclass.lua` | `a1d4129ca5779c3b2598da418909f057bd9b6c6733701855fd70bf2a9dcb1230` |
| `widget/ask/materiaattachaskwidget.lua` | `b5cdbfac344c7c966b08edad0ac48a22c8dcfdfcd8cd012e50ea13364efc6fd6` |
| `widget/ask/materiainformwidget.lua` | `4bd676e8ea6d61206f88bb81272847545beb5fb3ab90d16a45604381d6559fd6` |
| `widget/desktopwidget_connector.lua` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/desktopwidget_itemdetail.lua` | `dea088111249bdfe99c5dae618a674c112859e1587f60bc1c57917f9b01cc180` |
| `widget/desktopwidget_materia.lua` | `834e5180a20668add24bafe7d94baa430dce855a13797d3038eab31a26392fb0` |
| `widget/materiaattachwidget.lua` | `e549ccae709e4eb8ae1b59d034ec7826e285e8318fea425c4ceecbb1f1ae48c2` |
| `widget/itemlistwidget.lua` | `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |
| `widget/mainmenuwidget.lua` | `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2` |
| `widget/consoleicontraywidget.lua` | `498b25c7365180cd1ecff32d099ebc3e38fae0c6b6cd9d1f6e3a0953a33e3a7e` |
| `command/system/itemmaterializecommand.lua` | `c4e9b0572601b84436cf35bce6b3920d165f41ae73181075cc75f99b4ebe2450` |
