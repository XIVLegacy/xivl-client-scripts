# Foundation Day presentation and salute contract

The nine selected `Spl000` methods establish a conditional three-company
presentation contract. Each starts a talk turn, retains one `doSalute` result,
branches on equality with numeric zero and presents dialogue. On normal
completion it finishes the talk turn and returns zero values. The three leader methods also compare a fourth
fixed caller argument against numeric thresholds and select further presentation.

The company grouping follows
`xivl-decomp:docs/event/spring-foundation-actor-scripts.md`, Foundation Day
section, lines 20-47. It is decoded presentation context. It does not identify
the historical invoking NPC, city placement, or dispatch path.

## Evidence identity and coordinates

The original resource is
`client/script/tp5rq/r75w9s1v/ruy/ruyjjj.le.lpb`, 8,559 bytes, SHA-256
`ffa8b4b30c9e8444c8f7fc251aafdc7f2b9c62f87807a942eead2d3c5b6edd5f`.
Its decoded Lua 5.1 payload is 8,546 bytes, SHA-256
`cd7b529d6db29ddcbde80c15e2057c6aea78962d4d5c48ce891475d84118ea58`.
The bounded decoder consumes exactly one complete chunk through byte 8,546.
The [retail resource coverage](../manifests/retail_lua_coverage.json) record
for `lua/scripts/quest/scenario/spl/spl000.lua` supplies the resource join.

The separately pinned canonical text is archive member
`quest/scenario/spl/spl000.lua`, 21,200 bytes, SHA-256
`9491f7e3724d6fa0bc5f0c17a079c3dc758c6ce2107e154cbbb5c3362c4804b3`.
The decoded-Lua archive has SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Its matching [source manifest](../manifests/scripts.json) has SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`.
Canonical source lines locate the recovered presentation. Original instructions
establish the argument, branch, and result contract below.

PCs and decoded byte offsets are zero-based. A method's instruction at PC `n`
is at its code offset plus `4*n`. Canonical source lines are one-based and
refer to the pinned member. Source ranges include the method assignment.
The declaration column identifies the root `SETTABLE` assigning the closure.

| Method suffix after `processEvent` | Prototype | Fixed parameters / instructions | Code offset | Root declaration PC / byte | Canonical lines | Return PC / byte |
| --- | --- | --- | ---: | --- | --- | --- |
| `LINDLEADER` | `root/proto10` | 4 / 44 | 5362 | 39 / 188 | 693-747 | 43 / 5534 |
| `BRIELLE` | `root/proto11` | 3 / 30 | 5794 | 42 / 200 | 750-790 | 29 / 5910 |
| `GILLARD` | `root/proto12` | 3 / 25 | 6126 | 45 / 212 | 793-827 | 24 / 6222 |
| `ELNAURE` | `root/proto13` | 4 / 44 | 6429 | 48 / 224 | 830-884 | 43 / 6601 |
| `ARISMONT` | `root/proto14` | 3 / 30 | 6861 | 51 / 236 | 887-927 | 29 / 6977 |
| `MERLIE` | `root/proto15` | 3 / 25 | 7184 | 54 / 248 | 930-964 | 24 / 7280 |
| `SOMBER` | `root/proto16` | 4 / 44 | 7478 | 57 / 260 | 967-1021 | 43 / 7650 |
| `MIMIO` | `root/proto17` | 3 / 30 | 7919 | 60 / 272 | 1024-1064 | 29 / 8035 |
| `SISIMUZA` | `root/proto18` | 3 / 25 | 8251 | 63 / 284 | 1067-1101 | 24 / 8347 |

All nine are nonvariadic. `p0`, `p1`, `p2`, and `p3` below mean the fixed
caller parameters at registers 0, 1, 2, and 3. Their names do not assign
historical meanings to the caller inputs. `p3` exists only in the leaders.

## Common call and salute behavior

All nine execute `p2:startCliantTalkTurn(2, p1)` at PC 3, then
`p2:doSalute(firstLiteral, secondLiteral)` at PC 7, using the literal pairs
in the company table below. The latter call retains exactly its
first result. Extra results are discarded. An absent first result is padded
with nil.

PC 8 is `EQ A=0` comparing that retained register against numeric `0`.
Equality skips the following jump and executes
`p2:_runCharaScheduler(353959936)` at PC 12. Inequality takes the PC 9 jump
to PC 14 and executes `p0:_wait(2)` at PC 16. The PC 13 jump makes these
paths mutually exclusive. Both paths join at PC 17 and execute the first
`p2:say(p0, row, 0)` at PC 21.

This is numeric equality, not a Boolean or truthiness test. Nil, false, true,
and the string `"0"` do not equal numeric zero. No historical result domain
or meaning of zero is established. The scheduler and wait effects remain
opaque beyond these calls and their arguments.

| Call | PC | Encoded B / C | VM arguments including receiver | Explicit arguments / retained results |
| --- | ---: | --- | ---: | --- |
| `startCliantTalkTurn` | 3 | 4 / 1 | 3 | 2 / 0 |
| `doSalute` | 7 | 4 / 2 | 3 | 2 / 1 |
| First `_runCharaScheduler` | 12 | 3 / 1 | 2 | 1 / 0 |
| Alternative `_wait` | 16 | 3 / 1 | 2 | 1 / 0 |
| Each `say` | 21, and role-specific sites below | 5 / 1 | 4 | 3 / 0 |
| Leader second `_runCharaScheduler` | 26 | 3 / 1 | 2 | 1 / 0 |
| `finishCliantTalkTurn` | Role-specific site below | 2 / 1 | 1 | 0 / 0 |

Lua 5.1 fixed `CALL` encodes argument count as `B-1` and retained result
count as `C-1`. The implicit receiver counts as a VM argument. For the
leaders, the PC 3/7 call base register A is 4 and all later call bases are 5.
For the other methods those bases are 3 and 4 respectively. No selected
`CALL` uses an open argument or result count.

## Company and role differences

| Company context | Leader: suffix; salute arguments; dialogue rows; item argument | Second method: suffix; salute arguments; dialogue rows | Third method: suffix; salute arguments; dialogue row |
| --- | --- | --- | --- |
| Maelstrom | `LINDLEADER`; `(1,31)`; `55 / 56 / 57`; `3020614` | `BRIELLE`; `(1,21)`; `58,59` | `GILLARD`; `(1,13)`; `60` |
| Twin Adder | `ELNAURE`; `(2,31)`; `61 / 62 / 63`; `3020615` | `ARISMONT`; `(2,21)`; `64,65` | `MERLIE`; `(2,13)`; `66` |
| Immortal Flames | `SOMBER`; `(3,31)`; `67 / 68 / 57`; `3020616` | `MIMIO`; `(3,21)`; `70,71` | `SISIMUZA`; `(3,13)`; `72` |

The leader row triple means first `p2:say`, second `p2:say`, and
`worldMaster:say`, respectively. SOMBER's last row is exactly `57`.

After the first dialogue, each leader tests `2 <= p3` at PC 22 (`LE A=0`).
If true, it skips PC 23's jump, calls
`p2:_runCharaScheduler(354066432)` at PC 26, then
`p2:say(p0, secondRow, 0)` at PC 31. PC 32 jumps to PC 41.
If false, PC 23 jumps to PC 33, which tests `1 <= p3` (`LE A=0`).
If that test is true, it skips PC 34's jump and calls
`worldMaster:say(p0, worldRow, itemArgument)` at PC 40. Otherwise PC 34
jumps to PC 41. Thus supported numeric values below 1 add no further
dialogue, values in `[1,2)` select the worldMaster call, and values at least
2 select the second scheduler and dialogue. The caller domain is unknown:
the instructions do not establish that `p3` is an integer count. Ordering
errors or metamethod behavior for other input types are outside this contract.

Leaders then call `p2:finishCliantTalkTurn()` at PC 42 and execute
`RETURN A=0 B=1 C=0` at PC 43. The second methods unconditionally execute
their second `p2:say(p0, row, 0)` at PC 26, finish at PC 28, and return at
PC 29. The third methods finish at PC 23 after their one dialogue, then
return at PC 24. Every return has zero values. The retained salute result
is consumed locally and is not returned. All other call results are discarded.

Useful canonical expression locators for the salute calls are lines
701/758/801, 838/895/938, and 975/1032/1075, in company order.
The leader threshold presentation expressions are 724/728/736,
861/865/873, and 998/1002/1010. These source expressions corroborate the
presentation identities; the original PCs determine their control flow.

## Verification and limits

A focused offline decoder checks the wrapper and payload hashes, canonical
archive/member/manifest identities, exact EOF, selected declarations, and all
nine methods. An independent expected-call model checks 480 cases with opaque
callees. It exercises absent and extra salute results, nil, Booleans, numeric
zero and nonzero values, string `"0"`, leader numeric thresholds including
`1.5`, discarded results from the other calls, exact call tuples and order,
finish calls, and zero-value returns. This checks original-instruction
behavior under the modeled inputs, not retail execution or native effects.

Only these nine prototypes and their root declarations support this finding.
Native callees were not inspected. Their internal effects, actual producer
result domains, historical actor/city dispatch, player-work and shop
availability, event-mode-11 effects, grants, calendars, quest progression,
and weather control remain separate questions. In particular, an item ID
passed to `say` establishes a presentation argument, not a grant or
entitlement. The prior company grouping does not close those bindings.
