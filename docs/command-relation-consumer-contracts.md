# Command relation result consumers

The recovered GameCommandBaseClass source has three consumers of
`canAimForRelation`'s ordered returns. For the selected static helpers
`23597-23602/23606-23607`, inherited target-control mode is `0`.
The separate force-target helper distinguishes `23602` by its third
Boolean. These are decoded-source local contracts, without a historical
command invocation or actor/encounter variant assignment.

## Ordered accessor and selected classes

`BattleCommandBaseClass.canAimForRelation`, lines 68-97, uses
`getCommandId(self)` and returns `gameCommandSheet` columns
`137/138/139` in that order. These are header labels, not physical CSV
field indices. The static selected class is
`/Command/Game/Basic/MonsterSubStatOthers`, inheriting BattleCommandBaseClass
and then GameCommandBaseClass.

| Selected command IDs | Ordered return tuple |
| --- | --- |
| `23602` | `true,false,true` |
| `23597/23598/23599/23600/23601/23606/23607` | `true,false,false` |

Sources: `xivl-client-data:manifests/staticactor_class_paths.json`, selected
IDs; `csv/gameCommand.csv`, same IDs and numeric headers 137-139;
`lua/scripts/command/game/battlecommandbaseclass.lua:68-97`;
`command/game/basic/monstersubstatothers.lua:1-8`.
The diagnostic disappearance wording of 23602 does not name a relation
category, numeric model state, scheduler operation or reset.

## Three recovered consumers

Each method loads `self.canAimForRelation` into a temporary, calls it with
`self`, and captures three ordered results. All locators below belong to
`lua/scripts/command/game/gamecommandbaseclass.lua`.

| Method and source span | Ordered-result use and local result |
| --- | --- |
| `aimWithSubTarget:1150-1180`, call 1164-1165 | If both `isMagicCommand` and `isAbilityCommand` are falsey (false or nil), returns false without the accessor call. Otherwise strict Boolean `true,false,false` returns false; another tuple returns true. |
| `getTargetControlMode:1183-1253`, call 1193-1194 | Calls `aimWithSubTarget` first. A falsey result returns numeric 0 at 1188-1190. Only the admitted branch reaches the relation call; in that branch `true,false,true` returns 4 at 1201-1208. |
| `judgeAtForceTarget:2675-2686`, call 2678-2679 | Ignores return 1. If the third explicit argument differs from the first and returns 2/3 are both falsey, replaces the third argument with the first. Returns that third argument at 2683; the second explicit argument is unused. |

Explicit argument positions in this table exclude `self`. Their actor
identities and the eventual caller/application remain unresolved.

The selected class chain does not override these methods or
`isMagicCommand/isAbilityCommand`. The two base predicates at
lines 399-405 and 408-414 return false. Thus all eight selected helpers
inherit `aimWithSubTarget=false` and `getTargetControlMode=0`;
23602's third Boolean does not make its mode 4.

The independent force-target result does distinguish it: 23602 preserves the
third explicit argument. For the other seven, it replaces the third with the
first only when the two compare unequal; otherwise it preserves the third.
It returns the resulting third argument. This comparison does not establish
reference identity, and the local result needs no historical actor-lifetime
match.

## State, collision and invocation boundary

Target-control mode `0` is the return of this helper. It is not a
model/Scene mode, actor main state, status ID, bit/mask or server phase.
The three methods contain no object-field writer or collision/reset request.
Their local argument replacement does not establish a placed target,
activation, cancellation, defeat/wipe/retry/exit operation or restoration.

The relation categories remain unnamed here. Static class/row selection does
not establish invocation on a retail actor or membership in original,
repeatable or Hard Rivenroad. Packed playback selectors, model-qualified
WSS/BID banks and command IDs remain separate domains.

## Source identity and verification

The sources belong to extraction `2012.09.19.0001`. The decoded archive
matched [private_lua_corpus.json](../manifests/private_lua_corpus.json);
all 2,671 members matched [scripts.json](../manifests/scripts.json) before
the distinct case-sensitive identifier/call-use query.

| Canonical member under `lua/scripts/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `command/game/gamecommandbaseclass.lua` | 55102 | `75f366ca597f77a8e4b506fa8d7b214171cfdbb8d913fa12aa685d72a0b3256b` |
| `command/game/battlecommandbaseclass.lua` | 2533 | `0eb0b8c77b05128461d94ca1a9bee9b65bccf397ab8efd60903c448915d1e757` |
| `command/game/basic/monstersubstatothers.lua` | 194 | `11f50240988c54ef7aea2f78324796cd04e060db98d3f80461c3e417574589de` |

Python 3.12 `zipfile/hashlib/json` authenticated inputs. A position-preserving
Lua lexical query excluded strings/comments, distinguished method definitions,
and followed temporary alias calls into the three complete methods.
It found 16 identifier occurrences: 13 definition bindings and these three
executable references. This closes that predicate and corpus, without excluding
dynamic, constructed, native or server-supplied callers.

The consumer branch and arity claims above are qualified to authenticated
decoded source. Their original bytecode has not been verified.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) identifies
`client/script/7vxx9w6/39x5/39x57vxx9w689r57y9rr.le.lpb`, 24,331 bytes,
SHA-256 `7272fe8c36c6533819dbe061034fdea8513a2f9bf6144e8bf6cfcdc032973a97`.
This finding does not reproduce that input or establish original prototype,
PC/offset, branch or closure bindings. Local source predicates and
constant-return consequences are not runtime observations.
