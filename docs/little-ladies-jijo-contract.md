# Little Ladies' Day JIJO menu and result contract

The three named city `JIJO` methods in `Spl000` each ask row `10` once,
retain one result, and compare it with numeric `1`. Equality selects the
city's longer presentation sequence. Every other retained value skips that
sequence. Both paths finish the talk and return zero values.

The city associations are the existing Limsa Lominsa, Gridania and Ul'dah
presentation associations in
[Little Ladies' Day and Foundation actor scripts](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/event/spring-foundation-actor-scripts.md#little-ladies-day),
`xivl-decomp:docs/event/spring-foundation-actor-scripts.md:7-16`.
The menu/result contract does not establish an NPC-to-method dispatch binding.

## Sources and locators

The single original resource is
`client/script/tp5rq/r75w9s1v/ruy/ruyjjj.le.lpb`, identified as
`quest/scenario/spl/spl000.lua` by
[the retail coverage manifest](../manifests/retail_lua_coverage.json).
An independent fixed-header Lua 5.1 reader parsed its decoded chunk through
EOF. PCs start at zero. Byte offsets start at the decoded payload's first byte.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Original LPB | 8559 | `ffa8b4b30c9e8444c8f7fc251aafdc7f2b9c62f87807a942eead2d3c5b6edd5f` |
| Decoded payload | 8546 | `cd7b529d6db29ddcbde80c15e2057c6aea78962d4d5c48ce891475d84118ea58` |
| Canonical `quest/scenario/spl/spl000.lua` | 21200 | `9491f7e3724d6fa0bc5f0c17a079c3dc758c6ce2107e154cbbb5c3362c4804b3` |

The canonical member matches
[the source manifest](../manifests/scripts.json), SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`,
and the retained corpus archive, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The canonical text corroborates the selected original instructions.

All selected methods have three fixed parameters, no varargs and no upvalues.
Name the parameters `p0`, `p1`, and `p2` in register order. Their caller
identities and actual supplied values remain unresolved. Abbreviate
`processEvent_PRINCESSDAY_LIM_JIJO`,
`processEvent_PRINCESSDAY_GRI_JIJO`, and
`processEvent_PRINCESSDAY_UL_JIJO` as LIM, GRI and UL below.

| Method | Prototype | Instructions / first byte | Root assignment PC / byte | Canonical body / assignment lines |
| --- | --- | --- | --- | --- |
| LIM | `root/proto3` | 83 / 1874 | 18 / 104 | 139-242 / 244 |
| GRI | `root/proto6` | 83 / 3331 | 27 / 140 | 371-474 / 476 |
| UL | `root/proto9` | 80 / 4717 | 36 / 176 | 589-688 / 690 |

Each root assignment takes the closure created immediately before it.
These locators identify declarations, not historical callers.

## Common prefix and menu result

Every call below uses receiver `p2`. Explicit arguments exclude that receiver.
The dialogue helper notation `say(row)` means `p2:say(p0, row, 0)`.
The notation `scheduler(id)` means `p2:_runCharaScheduler(id)`.

| Call, in order | PC | Decoded byte, LIM / GRI / UL |
| --- | ---: | --- |
| `p2:startCliantTalkTurn(2, p1)` | 3 | 1886 / 3343 / 4729 |
| `scheduler(opening)` | 6 | 1898 / 3355 / 4741 |
| `say(firstRow)` | 11 | 1918 / 3375 / 4761 |
| `p2:_waitForCharaSchedulerFinished(opening)` | 14 | 1930 / 3387 / 4773 |
| `p2:askExtendWidget(p0, 10, 2, 1, 1)` | 21 | 1958 / 3415 / 4801 |

| Argument | LIM | GRI | UL |
| --- | ---: | ---: | ---: |
| `opening` scheduler and wait argument | 354054144 | 354054144 | 353980416 |
| `firstRow` | 46 | 29 | 9 |

The menu instruction is `CALL A=3, B=7, C=2`: six Lua arguments including
the receiver, one requested result retained in `R3`. Fixed-result adjustment
keeps the first producer value, discards extra producer values, or supplies nil
if the producer returns no values. This request does not establish the native
producer's actual returned arity or result domain.

PC 22 / bytes 1962, 3419 and 4805 executes `EQ A=0` between `R3` and
numeric constant `1`. Equality skips PC 23 and enters PC 24. Inequality
executes the PC 23 jump at bytes 1966, 3423 or 4809 to PC 80, 80 or 77.
Those targets prepare the finish call.

This is numeric equality, with no truthiness test or conversion to boolean.
Boolean `true`, boolean `false`, numeric `0`, numeric `2`, string `"1"`,
empty string and nil are unequal to numeric `1`. The canonical ask/result
and comparison lines are 167-168, 399-400 and 617-618 respectively.

## Numeric-1 branch

The cells below give `call; PC / decoded byte` in execution order. All
`say` calls retain the common `(p0, row, 0)` explicit arguments.

| Order | LIM | GRI | UL |
| ---: | --- | --- | --- |
| 1 | `scheduler(353959936)`; 26 / 1978 | `scheduler(353976320)`; 26 / 3435 | `scheduler(353968128)`; 26 / 4821 |
| 2 | `say(47)`; 31 / 1998 | `say(30)`; 31 / 3455 | `say(13)`; 31 / 4841 |
| 3 | `scheduler(353972224)`; 34 / 2010 | `say(31)`; 36 / 3475 | `say(14)`; 36 / 4861 |
| 4 | `say(48)`; 39 / 2030 | `scheduler(353972224)`; 39 / 3487 | `scheduler(354086912)`; 39 / 4873 |
| 5 | `say(49)`; 44 / 2050 | `say(32)`; 44 / 3507 | `say(15)`; 44 / 4893 |
| 6 | `say(50)`; 49 / 2070 | `say(33)`; 49 / 3527 | `say(16)`; 49 / 4913 |
| 7 | `scheduler(353964032)`; 52 / 2082 | `scheduler(353968128)`; 52 / 3539 | `scheduler(353980416)`; 52 / 4925 |
| 8 | `say(51)`; 57 / 2102 | `say(34)`; 57 / 3559 | `say(17)`; 57 / 4945 |
| 9 | `say(52)`; 62 / 2122 | `say(35)`; 62 / 3579 | `say(18)`; 62 / 4965 |
| 10 | `scheduler(353984512)`; 65 / 2134 | `scheduler(353980416)`; 65 / 3591 | `scheduler(353968128)`; 65 / 4977 |
| 11 | `say(53)`; 70 / 2154 | `say(36)`; 70 / 3611 | `say(19)`; 70 / 4997 |
| 12 | `scheduler(354054144)`; 73 / 2166 | `scheduler(354054144)`; 73 / 3623 | `say(20)`; 75 / 5017 |
| 13 | `say(54)`; 78 / 2186 | `say(37)`; 78 / 3643 | - |

These are all presentation argument and order differences in the three
selected methods. LIM schedules between its first two branch dialogue calls.
GRI and UL issue both dialogue calls before their next scheduler. UL has no
scheduler between its final two dialogue calls. There is no explicit wait in
this branch. The opening scheduler wait is before the menu.

## Finish, return and limits

The numeric-1 branch ends with a zero-displacement `JMP` at PC 79 / byte
2190, PC 79 / byte 3647 or PC 76 / byte 5021. It proceeds to the same
finish preparation as the unequal path.

| Instruction | LIM PC / byte | GRI PC / byte | UL PC / byte |
| --- | --- | --- | --- |
| `p2:finishCliantTalkTurn()` | 81 / 2198 | 81 / 3655 | 78 / 5029 |
| `RETURN A=0, B=1, C=0` | 82 / 2202 | 82 / 3659 | 79 / 5033 |

The return has zero values. It does not return one nil or the retained menu
result. Canonical finish calls are at lines 241, 473 and 687, followed by
function end without an explicit source return.

Every call except the menu uses `C=1`, requesting zero results. `B` is one
plus the Lua argument count, including the receiver: start-talk uses `B=4`,
scheduler and scheduler-wait use `B=3`, dialogue uses `B=5`, and finish
uses `B=2`. The common-prefix calls use `A=3`. Calls after the menu use
`A=4` and leave `R3` unchanged until the zero-value return.

There is one menu call, one numeric comparison and no local retry,
acknowledgement test, cancel normalization or forwarding of a call result.
If a producer supplies a cancellation value unequal to numeric `1`, it follows
the unequal path. The actual cancel sentinel is unknown. Dialogue and scheduler
results are discarded. These selected methods contain no Boolean `TEST`.

Focused offline Python checks verified the full chunk framing and pins,
all selected method tuples, encoded argument/result fields, both paths and
finish/return order. They modeled 72 cases covering zero producer values,
one nil, numeric/Boolean/string distinctions, extra menu results, and discarded
opaque results from other calls. The checks executed neither Lua nor the client.

Call order and literal arguments do not establish native scheduler or wait
effects, elapsed time, menu completion, or a producer's complete domain.
Normal-path finish and return assume preceding calls complete normally. There
is no protected cleanup path here. Historical NPC dispatch and placement,
event calendar, eligibility, grants, progression and weather effects remain
outside this contract.
