# Equipment set and cancel command contracts

ChangeEquipSetCommand (`12007`) and CommandCancelCommand (`21005`, `21006`)
inherit their command checks and execution behavior from GameCommandBaseClass.
Their own methods only disable action-gauge use and action-menu presentation.
The equipment-set wrapper passes an opaque argument to ready command 12007.
The stock action-menu cancel route passes the selected command's
`charaWork.commandCategory` value to 21006. These routes do not establish a
saved-set schema, an equipment-list
reply, or a combat-result reply contract.

## Callers and arguments

`DesktopWidget.executeCharacterEquipItemSet(value)` calls
`executePlayerReadyCommand(12007, value)`
(`widget/desktopwidget_connector.lua:14692-14703`).
`cancelPlayerCastCommand(value)` similarly calls
`executePlayerReadyCommand(21006, value)` (14473-14483).
`ActionMenuWidget.cancelCommand(value)` invokes that cancel helper and, when
the local return is true, immediately resets its casting-command information
for the same value (`widget/actionmenuwidget.lua:1151-1167`). That immediate
UI reset is not a server acknowledgement.

`getReadyCommandIndex` maps 21006 to index 1 and 12007 to index 9
(`desktopwidget_connector.lua:12408-12499`). The ready-command dispatcher
refuses an unmapped ID or nonpositive equipped-slot mapping. It retrieves the
command object and its hand value through `getReadyCommand`, then supplies
that hand when no explicit third command value was given
(13729-13789, payload `root/proto279`, `0x1ED81-0x1EE25`).

`executePlayerCommand` resolves numeric command IDs, refuses a missing or
invalid command actor, and replaces a missing/invalid target with the current
target. It forwards nine command values to `PlayerBaseClass.command`
(13620-13758, `root/proto278`, argument construction at
`0x1EAE2-0x1EB06`). For both one-argument callers above the submitted tuple is:

```text
(value, nil, readyHand, nil, currentTarget, nil, nil, nil, nil)
```

`currentTarget` may be nil. This is the submitted argument vector before
eligibility helpers normalize local copies. The first value's server meaning
is unresolved. Its client-side provenance is established for the action-menu
cancel route below. The equip-set wrapper does not itself enumerate
item-package/slot pairs, and the cancel wrapper does not construct a result
packet. Command 21005 shares the mapped class and sheet settings with 21006,
but no concrete UI caller or argument vector for 21005 is established here.

## First-operand provenance

`ActionMenuWidget.executeGameCommand` obtains three results from
`getPlayerEquippedReadyCommand(slot)` for ready type `1`, or from
`getPlayerEquippedCustomCommand(slot)` for type `2`. It retains the command
object, the second scalar and a validity flag separately. Under config flag
`15`, the current-cast equality and positive cast-time tests lead to
`cancelCommand(secondScalar)`
(`widget/actionmenuwidget.lua:859-949`). `cancelCommand` forwards that scalar
to `cancelPlayerCastCommand`, then uses the same value for its local reset
when submission returns true (`:1152-1168`).

The scalar's source is explicit Lua work, without a native return-value
interpretation:

| Getter | First and second results |
| --- | --- |
| `CharaBaseClass.getReadyCommand(slot)`, `chara/charabaseclass.lua:288-344` | `charaWork.command[slot]`, `charaWork.commandCategory[slot]`, after its special command-22001 exclusions. |
| `CharaBaseClass.getCustomCommand(slot)`, `chara/charabaseclass_cliprog.lua:231-249` | The same two arrays indexed by `charaWork.commandBorder + slot`. |
| Desktop equipped-command wrappers, `widget/desktopwidget_connector.lua:12534-12652` | Preserve those two results and append the command-validity flag after slot/object checks. |

`CharaBaseClass` declares `commandCategory` as an array of 64 `integer8`
values (`chara/charabaseclass.lua:575-583`). On the successful action-menu
cancel route, operand 1 therefore comes from the selected action's category
entry. It is distinct in provenance from the command object/ID and from the
slot used to select that entry. No observed cast-instance identifier is
constructed here. This does not recover the complete numeric category domain
or its server interpretation.

Operand 3 remains the separate category/hand default obtained when the ready
dispatcher resolves the cancel command itself. The two values must not be
conflated merely because both are used in hand-related helpers. The existing
conditional serializer applies to the unchanged tuple.

Original bytecode confirms the multi-return and forwarding chain. PCs below
are zero-based and identify actual `CALL`/`TAILCALL` instructions:

- ActionMenu `main/f13`: ready/custom getters at PCs `21/31`, cancellation at
  PC `83`.
- ActionMenu `main/f16`: desktop cancel call at PC `3`, local reset at PC `8`.
- Connector `main/f297`: `executePlayerReadyCommand(21006, value)` tail call
  at PC `3`.

### Equipment input and 21005 search boundary

A literal-reference search covered every canonical member of the authenticated
decoded Lua corpus: 2,671 manifest-matched scripts. Exact helper-name searches
found `executeCharacterEquipItemSet` only at its connector definition and
`cancelPlayerCastCommand` only at its definition and the ActionMenu caller.
Exact numeric-token searches found no `21005`. `21006` occurred only in the
connector's ready-index mapping and cancel wrapper. The other `12007` hit,
`widget/achievementlistwidget.lua:908-913`, is a `setListText` help-text ID,
not a command submission. Its original LPB independently reproduced that
source. EquipWidget's separate `12017` equipment operations are not callers
of the 12007 wrapper (`widget/equipwidget.lua:8301-8315`).

The pinned `ffxivgame.exe` also contained neither NUL-terminated literal
`executeCharacterEquipItemSet` nor `cancelPlayerCastCommand` in a read-only
exact byte search. Binary identity is size `15996808`, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
This does not exclude constructed names, generic dispatch, or runtime inputs.

The remaining equipment discriminator is a concrete issuer that supplies
12007's first operand. No selected evidence binds it to a class ID, saved-set
number or equipment selector. The 21005 negative covers literal Lua issuers
and these named native literals, not every possible dynamic issuer. Observed
21005 command-slot population is separately recorded in
`xivl-client-structs:manifests/command_slot_context.json`; a populated slot
does not identify a request or its operand vector.

The corpus search authenticated archive size `14385427` and SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`
against `manifests/private_lua_corpus.json`, then every source member against
`manifests/scripts.json` at revision
`39927f86fd8614102d4144cd98fe0eeab01e1e3a`. Only matching locators were
retained. Search output alone was not used to assign semantics.

## Route and native fallback

`command.csv` column 29 is 11 for 12007, 21005 and 21006.
`CommandBaseClass.getPriority` reads that column, and
`CharaBaseClass.getCommandName` selects `commandForced` for game-command
priority 11 (`chara/charabaseclass.lua:399-496`, payload `root/proto17`,
`0x12CC-0x1444`). Column 28 (`needsEquipped`) is true for all three.
The [confirmation contract](confirm-prompt-client-contracts.md#shared-source-identity)
owns the common command-sheet and Lua identities.

`PlayerBaseClass.command` submits the chosen event name and command object
through `_executeCommand` after admission. If dispatch selects the block
descriptor, `_onCommandEvent` calls `_callServerOnCommand`; if it selects the
nonblock descriptor, `_onCommandRequest` calls `command` and `fire`, then
`_doServerOnCommand` when both are false
(`chara/player/playerbaseclass.lua:1820-1908`). The inherited command and fire
methods are false here. The retained `commandForced` definition carries
priority 11 and selector 0, constructing `CommandBlock` if the native selector
global is zero. See `xivl-client-structs:manifests/command_descriptor_registration.json`
for that conditional construction and the unobserved later descriptor selection.

Both native bridges have the same proven direct fallback:
`_callServerOnCommand` at VA `0x006E8B30` calls `0x006E2FB0` at `0x006E8BF9`;
`_doServerOnCommand` at `0x006E8C90` calls it at `0x006E8D59`. The shared
builder writes MapServerbound `0x012D`. See
`xivl-client-structs:manifests/player_command_wire_contract.json` for the
byte-authenticated native chain and serializer. This is a conditional
fallback binding, not an observed socket send.

The envelope carries the chosen event name and command object's resolved
control reference. It does not insert scalar 12007 or 21006 into the tail.
For ordinary integral `value` and `readyHand`, and an ordinary character
reference, the tuple encodes as:

```text
I(value) N I(readyHand) N A(currentTarget) N N N N E
```

`I` is `00` plus u32be bits, `N` is `05`, `A` is `06` plus the resolved
control-reference dword, and `E` is `0F`. A nil target is `N`, not `A(0)`.
Other types of the opaque first value take the serializer's corresponding
branch. The generic serializer cannot establish the server meaning of that
value or supply a valid equipment-set input domain.

## Local refusals

`PlayerBaseClass.canCommand` rejects a nonnil command burst blocker and a
false `_canExecuteCommand(commandForced)`, then calls the command's
`canFire`. Its submission method additionally refuses combined string byte
lengths above 50 in the first two values
(`chara/player/playerbaseclass.lua:1911-2023`). Neither scoped class adds a
custom `canFire` method
(`command/game/changeequipsetcommand.lua:1-26`;
`command/game/commandcancelcommand.lua:1-26`).

Inherited `processCanFire` resolves a missing hand, refuses if no hand can be
chosen, substitutes self for a nil target during its checks, rejects an
invalid supplied target, defaults its last four local check values to zero,
and calls `checkFireImpl`
(`command/game/gamecommandbaseclass.lua:2459-2512`, payload `root/proto113`,
`0x5916-0x59D6`). `checkFireImpl` applies actor-state, skill, recast, HP, MP,
TP and detail checks (2330-2454, `root/proto112`, `0x55CE-0x5792`). The
inherited detail predicate returns `(true, 0)` (`0x14AA-0x14B6`).

`processCanCommandForActorStat` checks dead states 1/3 and seated states
11/13/14 before using `gameCommand.csv` column 37. All three commands
inherit `canFireOnDead == false` and `isAvailableOnSit == false`. The
dead-state refusal text is 32509 and the seated refusal text is 32501. Column 37 is 1 for 12007 and 0 for 21005/21006.
For 12007, the column-1 rule admits main state 0 and refuses the recognized
states 2, 30/31/32, 50/51 and 70 with text 32502. For cancel, column 0
returns true after the dead/seated checks. These are raw main-state comparisons, not a proof of
what gameplay conditions assign those states
(`gamecommandbaseclass.lua:73-175,177-213,546-552,1075-1081`, payload
`root/proto5`, `0x14EB-0x16DF`).

The inspected route contains no command-specific enmity predicate. This does
not prove that an equipment change succeeds while the player holds enmity:
server refusal and the native command scheduler remain separate boundaries.

## Reply boundary and inputs

The inspected wrappers and classes do not wait for or classify equipment
packets, `0x0139-0x013C` combat results, or a command-specific success/error
message. No named server reply, set contents, inventory mutation or cast
interruption is established by their local return values.

The authenticated CSV members are pinned by
`xivl-client-data:manifests/tables.json`, with columns identified by their
numeric header labels, not by counting row fields:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `gameCommand.csv` | 378889 | `775aa8062aebc9f394c97cb634b3a75d687ff03063c849b95333a6bce8032811` |
| `gameCommandBasic.csv` | 230761 | `4d2d75d88e96d56d1b4812b27d1d8cba68919ec9a4d4e2527647f4ae38cf7424` |

The class assignments are
`xivl-client-data:manifests/staticactor_class_paths.json`, rows 12007,
21005 and 21006. The common Lua/LPB identities are recorded in the
[confirmation contract](confirm-prompt-client-contracts.md#input-identities).

## Input identities

The decoded members below matched `manifests/scripts.json` by byte count,
line count and SHA-256. Each original resource matched
`manifests/retail_lua_coverage.json`, including its decoded payload hash.
LPB paths are relative to retail `client/script/`. The payloads were decoded
with `tools/retail_script.py:decode_lpb` and parsed as Lua 5.1 instructions.
Instruction offsets on this page are offsets into the decoded payload.

The first-operand trace additionally authenticated these originals and their
decoded/reproduced identities against the same two manifests at revision
`39927f86fd8614102d4144cd98fe0eeab01e1e3a`. It used
`tools/retail_script.py` and `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
The connector identity remains in the linked shared-source contract.

| Script | LPB path | Original bytes |
| --- | --- | ---: |
| `chara/charabaseclass.lua` | `729s9/729s989r57y9rr.le.lpb` | 13821 |
| `chara/charabaseclass_cliprog.lua` | `729s9/729s989r57y9rr_7y1usv3.le.lpb` | 4508 |
| `widget/equipwidget.lua` | `n1635q/5tp1un1635q.le.lpb` | 85949 |
| `widget/achievementlistwidget.lua` | `n1635q/97215o5x5wqy1rqn1635q.le.lpb` | 11494 |

- `lua/scripts/command/game/changeequipsetcommand.lua` (26 lines): source SHA-256
  `53568ae20767c4b0c835018ccc87e0bc67b889a5ce64b33e53c67e15a616a651`.
  LPB `7vxx9w6/39x5/729w355tp1ur5q7vxx9w6.le.lpb`, SHA-256
  `8657c624acb679ecc97bddd3980557f7a8078e1013ea43577d7e7199749af534`. Decoded payload SHA-256
  `c6d63967db8b184b8d480ec8d72e9a89e64ab75c23d48a6c83bfebd857035e06`.
- `lua/scripts/command/game/commandcancelcommand.lua` (26 lines): source SHA-256
  `0dc50dbfe34484ce2787761b0c5d1b80772a0b742c2ab71d5db7cf1602d3655c`.
  LPB `7vxx9w6/39x5/7vxx9w679w75y7vxx9w6.le.lpb`, SHA-256
  `7fef48a2a7c8f9563acbf38809018987105c460e1b97a235fc53c8b2443805bf`. Decoded payload SHA-256
  `25cc814f1402a1d29122485d0a116e26a09f3b15048d1ea1f081aafdbf231a71`.
- `lua/scripts/command/game/gamecommandbaseclass.lua` (2698 lines): source SHA-256
  `75f366ca597f77a8e4b506fa8d7b214171cfdbb8d913fa12aa685d72a0b3256b`.
  LPB `7vxx9w6/39x5/39x57vxx9w689r57y9rr.le.lpb`, SHA-256
  `7272fe8c36c6533819dbe061034fdea8513a2f9bf6144e8bf6cfcdc032973a97`. Decoded payload SHA-256
  `1b3ba520dc0efb2f1941d2b8206d33f7a2e1a8ee52a6012092563395f853a6f7`.
- `lua/scripts/widget/actionmenuwidget.lua` (2773 lines): source SHA-256
  `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea`.
  LPB `n1635q/97q1vwx5wpn1635q.le.lpb`, SHA-256
  `bceeae7dc8ac024767ba65a7c1ecbf8682f7c4e89b5c4eb55310d4e00e58af31`. Decoded payload SHA-256
  `826b09ef44102a51a34f53276ecafed348744688b8ce987831e82f7833fdcecc`.
