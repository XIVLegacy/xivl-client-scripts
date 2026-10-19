# Scrambled Eggs client require and result contract

The retained `Spl101` main chunk explicitly requires `Spl101_quest` before
adding its own methods to global `Spl101`. The supplemental chunk calls
`_defineClass("Spl101", "ScenarioBaseClass")` and installs
`processEventEASTER_G1Start`. That method requests one result from
`showQuestInfomation`, branches on equality with numeric `1`, and returns the
same retained value after either dialogue path.

The [seasonal quest identities](seasonal-quest-client-contracts.md#retail-quest-identities)
join `Spl101` to Scrambled Eggs, quest ID 110859. The method-name component
`G` is an identifier; it does not establish historical city participation.

## Sources and reproduction

The original resources under `client/script/tp5rq/r75w9s1v/ruy/` match their
records in [the retail coverage manifest](../manifests/retail_lua_coverage.json).
`tools/retail_script.py:decode_lpb` decodes both resources in memory, and
`tools/build_quest_contracts.py:ChunkReader` parses each payload through EOF.
PCs below start at zero; byte offsets start at the decoded payload's first byte.
The decoder and parser were inspected at revision
`ff4663575f86ad21088d3ceb0283f1ba5db89bab`.

| Decoded script / LPB basename | LPB bytes / SHA-256 | Decoded payload bytes / SHA-256 |
| --- | --- | --- |
| `quest/scenario/spl/spl101` / `ruyiji.le.lpb` | 896 / `4000815dc1dedca9b6669530cc3ddfdca8250bca1be189b794102dd1ccc5fc4c` | 883 / `2cb4f8a2b9983fcd9872720e673d727d3c653343b498ad88a9fb240390fc364a` |
| `quest/scenario/spl/spl101_quest` / `ruyiji_tp5rq.le.lpb` | 21644 / `894febbf8c69a13e56e2e417a02b86eb7243bdec36268b4642f946c4adf0f511` | 21631 / `975054e961a38851c8b7261a1b1d582666618c9539c02427b838f3bf9b5542f0` |

The canonical members in [the source manifest](../manifests/scripts.json),
SHA-256 `86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`,
were checked in memory against the retained corpus archive, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The source members are:

- `lua/scripts/quest/scenario/spl/spl101.lua`: 1805 bytes, SHA-256
  `627a74e2b6a96a6a3e4014bb622a4c668457738bd0cc5357ace0b481eaecde72`.
- `lua/scripts/quest/scenario/spl/spl101_quest.lua`: 57241 bytes, SHA-256
  `2d521e780915e26a19b99d48b5d27e857872b0884833c26c63c1ced7bf391afc`.

These canonical member pins are separate from the independent decompile text
pins listed in the seasonal overview. The bytecode and canonical source agree
on the selected require, declaration, argument, equality, and return facts.

## Required supplement and class extension

In `spl101:root`, PC 2 / byte 40 calls
`require("/Quest/Scenario/Spl/Spl101_quest")`. The call retains zero results.
The canonical source agrees at lines 2-4. The root then assigns `initText` at
PC 5 / byte 52 and `askEgg` at PC 8 / byte 64 to global `Spl101`. Their
canonical source assignments are lines 16 and 70. This root does not call
`_defineClass`.

In `spl101_quest:root`, PC 2 / byte 40 requires
`"/Quest/Scenario/ScenarioBaseClass"`, then PC 6 / byte 56 calls
`_defineClass("Spl101", "ScenarioBaseClass")`. Both calls retain zero results.
PC 9 / byte 68 assigns closure `root/proto0` to
`Spl101.processEventEASTER_G1Start`, matching canonical source line 106.

Under successful normal module semantics, an uncached required chunk executes
before the main chunk resumes; a cached `require` need not execute it again.
The roots assign through global `Spl101`, rather than using a returned module
object. This supplies a direct require relationship and a supplemental method
declaration followed by main-class extension. It does not prove the module
loader or `_defineClass` implementation, the runtime cache state, or an event
dispatch into the selected method. Neither root calls that method.

## `processEventEASTER_G1Start`

`spl101_quest:root/proto0` has three fixed parameters, no varargs, and 73
instructions starting at byte 2384. Its canonical body is lines 11-104. Name
the incoming parameters `p0`, `p1`, and `p2` in register order; their caller
identities are unresolved. The method starts with
`p2:startCliantTalkTurn(2, p1)`. Its common dialogue calls are
`p2:say(p0, row, 0)` for rows 2, 3, 4, and 5.

PC 43 / byte 2556 calls `p0:showQuestInfomation()`. `CALL A=3, B=2, C=2`
passes only the receiver as its Lua argument and requests one result. Exactly
one value is retained in `R3`; the producer's actual returned arity remains
unknown. Lua fixed-result adjustment discards extra results or supplies nil
when the producer returns no value.

PC 44 / byte 2560 compares that retained value with numeric `1`:

| Retained value | Calls after comparison |
| --- | --- |
| Equal to `1` | `p2:_runCharaScheduler(83959808)`; `p0:_wait(0.5)`; `p2:say(p0, 7, 0)` at PC 56 / byte 2608 |
| Unequal to `1` | `p2:_runCharaScheduler(84054016)`; `p0:_wait(0.5)`; `p2:say(p0, 6, 0)` at PC 68 / byte 2656 |

Both paths join at PC 69 / byte 2660 and call
`p2:finishCliantTalkTurn()` at PC 70 / byte 2664. The branch and finish calls
request zero results and do not overwrite `R3`. `RETURN A=3, B=2` at PC 71 /
byte 2668 returns exactly one value: the unchanged retained result. The
trailing zero-value return at PC 72 is unreachable on these normal paths.

The method therefore preserves the result rather than converting it to a
boolean. A cancellation value unequal to `1`, if supplied by the producer,
would follow the second branch and be returned unchanged. The actual cancel
sentinel and full result domain are not established. These return statements
assume the intervening calls complete normally.

## Evidence boundary

The result producer, widget implementation, caller/NPC dispatch, historical
event activation, eligibility, rewards, and server changes remain unresolved.
The equality comparison does not prove what the UI presents or what a server
accepts. Other `Spl101` methods and `askEgg` are outside this selected method
contract.

The checks use bytecode parsing and a Python branch model with opaque calls.
Synthetic branch cases verify the retained-result flow and fixed return arity;
they are not Lua VM execution or live client observations.
