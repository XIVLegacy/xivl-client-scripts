# Passive-mode command state check

The recovered `GameCommandBaseClass` check uses `gameCommand` sheet column 37
as an actor-main-state category. It does not establish a complete list of
battle commands usable in passive mode.

## Source identity

The selected canonical sources belong to client extraction `2012.09.19.0001`.
Their byte identities are recorded in
[`scripts.json`](../manifests/scripts.json):

| Script under `lua/scripts/` | Bytes | SHA-256 |
|---|---|---|
| `command/game/gamecommandbaseclass.lua` | 55102 | `75f366ca597f77a8e4b506fa8d7b214171cfdbb8d913fa12aa685d72a0b3256b` |
| `command/game/battlecommandbaseclass.lua` | 2533 | `0eb0b8c77b05128461d94ca1a9bee9b65bccf397ab8efd60903c448915d1e757` |
| `command/game/activatecommand.lua` | 1197 | `389e5fa09cc272ab6b0c90f2621cb1621ec3f152b68ea19914c06c7326d06c76` |

The original `GameCommandBaseClass` resource is
`7vxx9w6/39x5/39x57vxx9w689r57y9rr.le.lpb`, 24331 bytes, SHA-256
`7272fe8c36c6533819dbe061034fdea8513a2f9bf6144e8bf6cfcdc032973a97`.
Its decoded Lua payload is 24318 bytes, SHA-256
`1b3ba520dc0efb2f1941d2b8206d33f7a2e1a8ee52a6012092563395f853a6f7`.
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json)
pins both identities.

## Base actor-state predicate

`processCanCommandForActorStat` at lines 73-174 reads
`actor:_getActorMainStat()` and `getGameCommandData(37)`. Sheet column 37 is
`CsvRow.values[37]` under the decoded CSV indexing convention.

The check first rejects states 1 and 3 through the dead-command helper unless
`canFireOnDead` allows the command. It then rejects states 11, 13 and 14 with
32501 unless `isAvailableOnSit` allows the command. After those checks,
category 0 passes. The recognized state branches accept these categories:

| Actor main state | Accepted column-37 categories |
|---|---|
| 0 | 0, 1, 2, 5, 6, 7 |
| 2 | 0, 2, 5 |
| 30, 31, 32 | 0, 3, 6 |
| 50, 51 | 0, 4, 7 |
| 70 | 0, 5, 7 |

Other numeric states reach the default success result after the earlier
checks. `BattleCommandBaseClass` does not override this method.
`checkFireImpl` calls it at lines 2344-2351, and
`processCanFireWithoutTarget` calls it at lines 2531-2538. Both return the
failure and its text ID immediately. Other requirements and the
`canFireDetail` hook are separate checks.

Original bytecode corroborates the table. The method is `root/proto5`, with
126 instructions beginning at decoded payload offset `0x14EB`. The error
helper is `root/proto7`, with 45 instructions beginning at `0x1896`. Offline
replay of the selected branch and return operands agreed with the recovered
predicates for actor states 0-70 and category values 0-8, including both
values of the dead and sitting hooks. This is static control-flow evidence,
not recorded game execution.

## Mode identities and command-list limit

`ActivateCommand.canFireDetail` at lines 29-63 accepts command 21001 only
from source state 0 and command 21002 only from source state 2. The decoded
command names identify them as Active Mode and Passive Mode respectively.
The corresponding failure texts require active and passive mode respectively.
Together these sources support state 0 as passive and state 2 as active.

Source: `xivl-client-data:derived/command_battle_params.csv`, rows 21001 and
21002. Their exact imported identities are pinned by that repository's
`manifests/tables.json`.

Category 2 passes this base check in passive state 0. Heavy Swing, command
27190, has category 2. This rules out treating column 37 alone as a complete
passive battle-command eligibility flag. A projection of the base actor-state
predicate is a list of passes through one check. It does not account for all
subclass, native, target, acquisition, cost, or server requirements.

The registry recovers only the base definitions of
`processCanCommandForActorStat` and `getCanCommandErrTextIdForActorStat`.
[Registry fields are pattern-recovered](ai_agents/evidence-and-claims.md#generated-field-limits),
so this is not proof of complete runtime override coverage. A complete usable
passive-command list remains unresolved.

## Refusal text boundary

`getCanCommandErrTextIdForActorStat` at lines 186-213 returns 32503 for
category 2. The exact English cell in `worldMaster.csv`, sheet column 1,
is "That command can only be performed in active mode."

That constant does not establish a generic passive-ineligible battle-command
refusal. Source state 0 passes category 2 in the base check and does not
reach that error. Its populated category rejections are category 3 with
32504 and category 4 with 32505, whose texts require crafting and gathering.

`ActivateCommand` has separate branches. Command 21001 returns 32503 when
its source state is not 0. Command 21002 returns 32502 when its source
state is not 2. Text 32502 says "That command can only be performed in
passive mode."

Source: `xivl-client-data:csv/worldMaster.csv`, English sheet column 1,
rows 32502-32505, physical lines 938-941. The source is 1851138 bytes,
SHA-256 `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`.
Its identity is pinned by `xivl-client-data:manifests/tables.json`.

An observed refusal for a battle command rejected specifically because the
actor was passive, and its producing branch, remain unresolved. These
static findings do not authenticate the patch 1.19 announcement or establish
whether a successful command draws a weapon.
