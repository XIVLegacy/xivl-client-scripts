# Standard emote command target contract

The standard emote menu and typed-emote wrappers preserve a selected other
player in the fifth argument after the command object. Original bytecode
resolves the shared menu branch that the decompiled Lua renders as an empty
arm. These are static client input and dispatch facts, not an observed
request/reply exchange or successful playback.

## Menu and typed callers

`EmoteListWidget.processUICommandDefault` reads the selected row's `EmoteID`
and calls `executePlayerSystemCommand(24102, E, 1)` for an ordinary emote.
In `DesktopWidget.executePlayerSystemCommand`, comparison with 24102 takes
the jump to the shared current-target branch. Its eligibility and command
calls preserve this ordered tail after the resolved command object:

| Position | Value |
| --- | --- |
| 1 | Selected emote ID `E`. |
| 2 | Display flag 1. |
| 3-4 | nil, nil. |
| 5 | Current target character `T`, or nil when no character is selected. |
| 6-9 | nil, nil, nil, nil. |

The target getter forwards the current cursor result to `_getTargetCharacter`.
It does not replace another selected player with the local player.

For the typed Bow path, `emote.csv` row 105, column 3, carries text-command
key 247. `xtx__textCommand.csv` row 247 contains `/bow` in its English
command cells. The exact parsed-key-247 branch of `executeTextCommandLocal`
calls `emoteCommand(105, subcommand)`. A missing subcommand keeps its display
flag true. `executePlayerEmote` converts that flag to numeric 1 and obtains
the current target when no explicit target was supplied. It clears that
target only when it equals the local player, then calls
`executePlayerCommandLocal(24102, E, flag, nil, nil, T)`.

The fixed helper formals pad omitted later positions with nil. The desktop
`command` helper and player request callback use open vararg CALL operands,
preserving the complete nine-position tail. A decompiler's single displayed
vararg expression does not establish truncated forwarding. The native slash
parser's acceptance of an actual submitted line remains a separate
observation from the static sheet and parsed-key branch.

## Conditional server fallback

`command.csv` row 24102, column 29, is signed -1. `getPriority` reads that
column, and `CharaBaseClass.getCommandName` consequently selects
`commandRequest` for this system command. `CommandBase.isDesktopCommandMode`
returns false; neither selected derived class overrides it.

`PlayerBaseClass.canCommand` skips `_canExecuteCommand` for that name and
calls command `canFire`. `EmoteStandardCommand.canFire` checks living state
and the specific salute/seasonal conditions. It has no selected-player
refusal. Its `fire` handles an `NpcBaseClass` target locally; other targets
return false. The request callback therefore reaches `_doServerOnCommand`
when the inherited command method and `fire` both return false and the
remaining native transport gates pass.

The conditional native envelope, descriptor lookup and argument serializer
remain owned by
`xivl-client-structs:docs/player-command-wire-contract.md` and
`manifests/player_command_wire_contract.json`. A successfully resolved target
control uses tag `06` and its binding reference in position five. Explicit
nils retain their positions. The runtime command-control reference, executing
player and selected target are separate identities; static command ID 24102
does not identify the runtime command object.

The `0x00E1` consumer separately accepts a packed presentation selector,
target key and route-control halfword. Its source actor comes from dispatch
context (`xivl-decomp:docs/actor/action-queue.md`, compact producer).
Neither emote ID 105 nor the text-command key is an authenticated Bow
presentation selector. The existing Dance/Kneel witnesses and Bow's unproved
selector join remain in
`xivl-decomp:docs/actor/emote-animation-ids.md`. No selected-player Bow
request/reply pair or historical target policy follows from these callers.

## Original-bytecode locators

All paths below are under `lua/scripts/`; PCs are zero-based. Extraction
`2012.09.19.0001`, canonical sources and original LPB/payload identities are
pinned in [`scripts.json`](../manifests/scripts.json) and
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).

| Script and method | Prototype / PCs | Decoded offsets |
| --- | --- | --- |
| `widget/emotelistwidget.lua`, `processUICommandDefault` | `root/proto1`, 16-20, 38, 40-45 | `0x077B`-`0x078B`, `0x07D3`, `0x07DB`-`0x07EF` |
| `widget/desktopwidget_connector.lua`, `executePlayerSystemCommand` | `root/proto280`, 54, 56, 65-69; 141-148, 156-163 | `0x1EFBB`, `0x1EFC3`, `0x1EFE7`-`0x1EFF7`; `0x1F117`-`0x1F133`, `0x1F153`-`0x1F16F` |
| Same, `getCurrentTargetCharacter` | `root/proto33`, 0-3 | `0x91CA`-`0x91D6` |
| Same, `executeTextCommandLocal` | `root/proto463`, 1531-1539 | `0x2B956`-`0x2B976` |
| Same, `emoteCommand` | `root/proto472`, 0-15 | `0x2E4B2`-`0x2E4EE` |
| Same, `executePlayerEmote` | `root/proto286`, 0-10, 15-21 | `0x1F8F9`-`0x1F921`, `0x1F935`-`0x1F94D` |
| Same, `executePlayerCommandLocal`, `executeCommand`, `command` | `root/proto273`, 0-14; `root/proto271`, 27-39; `root/proto272`, 0-9 | `0x1E640`-`0x1E678`; `0x1E4D5`-`0x1E505`; `0x1E5C9`-`0x1E5ED` |
| `chara/player/playerbaseclass.lua`, `command`, `_onCommandRequest` | `root/proto44`, 35-47; `root/proto43`, 0-16 | `0x42EE`-`0x431E`; `0x41C3`-`0x4203` |
| `command/system/emotestandardcommand.lua`, `fire` | `root/proto1`, 16-31 | `0x02B6`-`0x02F2` |

The connector LPB is `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, 213,487
bytes, SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`.
Its decoded payload SHA-256 is
`685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`;
canonical connector Lua SHA-256 is
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`.
The selected source members and six original chunks were authenticated
against those manifests. `tools/retail_script.py` reproduces the decoded
chunks; `ChunkReader` and `instruction` in `tools/build_quest_contracts.py`
expose the original branch and CALL operands.
