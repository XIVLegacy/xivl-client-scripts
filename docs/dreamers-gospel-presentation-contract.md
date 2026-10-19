# The Dreamer's Gospel presentation and result contract

The retained `Spl0g1`, `Spl0l1`, and `Spl0u1`
`processEventGirlStart` methods request one result from
`showQuestInfomation()`, compare it with numeric `1`, and return that
retained value after the selected dialogue and talk finish. The selected
`processEvent020` methods issue a straight-line talk, scheduler, wait and
fade sequence, then return zero values.

The [seasonal quest identity table](seasonal-quest-client-contracts.md#retail-quest-identities)
joins these classes to The Dreamer's Gospel in Gridania, Limsa Lominsa, and
Ul'dah respectively. These two methods do not call each other. Their names
and title joins do not establish an event-dispatch or progression relationship.

## Sources and locators

The original resources under `client/script/tp5rq/r75w9s1v/ruy/` match
[the retail coverage manifest](../manifests/retail_lua_coverage.json).
Their wrappers were decoded in memory, and a separate fixed-header Lua 5.1
reader parsed all three complete chunks through EOF. PCs start at zero.
Byte offsets start at the decoded payload's first byte.

| Decoded script / LPB basename | LPB bytes / SHA-256 | Decoded payload bytes / SHA-256 |
| --- | --- | --- |
| `quest/scenario/spl/spl0g1` / `ruyj3i.le.lpb` | 4361 / `c3b050d0a35973ee21b096a51eebf14079f6b250368c67f4eddcabc0a947f493` | 4348 / `875bb9ea1e34420209be0a2f518a357cef234d51df823e2bfba4512eb8bea22a` |
| `quest/scenario/spl/spl0l1` / `ruyjyi.le.lpb` | 4265 / `228598b1f443f63c65d20da536f5e9dc67643b375cd152e330176d4f2e012b52` | 4252 / `13d02038c12ad001565cd80eb57e591df9ea0d78e0240709671ddbe8c41d1bef` |
| `quest/scenario/spl/spl0u1` / `ruyjpi.le.lpb` | 4352 / `df49007989ac4d1da9901af0cdbc1c7d8eaa28aa629249280379a22a1487ff63` | 4339 / `d1cb734d7a7d450a720ea3ae181bd21e7597b40999df892f46f9ba9f8b1c3aa5` |

The canonical source members in [the source manifest](../manifests/scripts.json),
SHA-256 `86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`,
were checked in memory against the retained corpus archive, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
These canonical pins are separate from the independent decompile text pins
in the seasonal overview.

| Canonical member under `lua/scripts/quest/scenario/spl/` | Bytes / SHA-256 | `GirlStart` body / assignment lines | `020` body / assignment lines |
| --- | --- | --- | --- |
| `spl0g1.lua` | 9437 / `ea5d22facebb339764d5608ae41045c6e5f53d7f2d41b6c754f3315441fbbcdb` | 135-214 / 216 | 379-437 / 439 |
| `spl0l1.lua` | 9137 / `4d43be1389207ad915c055d4896c6474cdc03030ca32a68474e4ad89e4f08654` | 135-214 / 216 | 367-425 / 427 |
| `spl0u1.lua` | 9437 / `9fbf24e9eb99960c2d960e7dcdf2061c6ffcecbf2bfa59ec9332afe4879f0842` | 135-214 / 216 | 379-437 / 439 |

Each root assigns closure `root/proto5` to `processEventGirlStart` at
PC 24 / byte 128 and closure `root/proto10` to `processEvent020` at PC 39 /
byte 188. Both prototypes have three fixed parameters and no varargs.
`root/proto5` has 63 instructions starting at byte 1637 in every variant.
`root/proto10` has 45 instructions starting at byte 3348 in `spl0g1`, byte
3281 in `spl0l1`, and byte 3339 in `spl0u1`.

Name the incoming parameters `p0`, `p1`, and `p2` in register order. Their
caller identities and actual supplied arguments remain unresolved. The
canonical source corroborates the selected declarations, arguments,
comparison and returns below. Within these methods, its only differences
are the three variant fields listed in the comparison table.

## `processEventGirlStart`

The common prefix calls the following in order. Every `say` here and in the
branches has receiver `p2` and explicit arguments `(p0, row, 0)`.

| Call | PC / decoded byte |
| --- | --- |
| `p2:startCliantTalkTurn(turn, p1)` | 3 / 1649 |
| `p2:_runCharaScheduler(353964032)` | 6 / 1661 |
| `p2:say(p0, 8, 0)` | 11 / 1681 |
| `p2:say(p0, 9, 0)` | 16 / 1701 |
| `p2:_runCharaScheduler(354103296)` | 19 / 1713 |
| `p2:say(p0, 10, 0)` | 24 / 1733 |
| `p0:showQuestInfomation()` | 26 / 1741 |

At PC 26, `CALL A=3, B=2, C=2` passes only `p0` as the Lua argument,
including the receiver. It requests and retains exactly one value in `R3`.
The producer's actual returned arity is unknown. Fixed-result adjustment
discards extra producer results or supplies nil when it returns no value.

PC 27 / byte 1745 executes `EQ A=0` between `R3` and numeric constant `1`.
Equality skips the jump at PC 28 and enters PC 29. Inequality executes that
jump to PC 51. This is numeric equality, not a truthiness test or a conversion
to boolean. In particular, boolean `true`, numeric `0`, string `"1"`, and nil
are unequal to numeric `1`.

| Retained value | Calls after the comparison, in order |
| --- | --- |
| Equal to numeric `1` | Scheduler `353968128` at PC 31 / byte 1761; `say` row 12 at PC 36 / byte 1781; `say` row 13 at PC 41 / byte 1801; scheduler `354107392` at PC 44 / byte 1813; `say` row 14 at PC 49 / byte 1833. PC 50 / byte 1837 jumps to PC 59. |
| Unequal to numeric `1` | Scheduler `354041856` at PC 53 / byte 1849; `say` row 11 at PC 58 / byte 1869; fall through to PC 59. |

Both paths call `p2:finishCliantTalkTurn()` at PC 60 / byte 1877.
All calls except `showQuestInfomation` request zero results and preserve
`R3`. `RETURN A=3, B=2` at PC 61 / byte 1881 returns exactly one value: the
unchanged retained result. The trailing zero-value return at PC 62 / byte
1885 is unreachable on these normal paths.

There is one `showQuestInfomation` call and no retry. A cancellation value
unequal to `1`, if the producer supplies one, follows the unequal branch and
is returned unchanged. The actual cancel sentinel and complete producer
result domain are not established. Canonical source lines 169-171 identify
the call and numeric comparison, and lines 211-213 identify finish and return.

## `processEvent020`

This method has no conditional branch or retry. The calls below all request
zero results (`CALL C=1`). The notation `g/l/u` orders byte offsets as
`spl0g1`, `spl0l1`, and `spl0u1`.

| Call, in order | PC | Decoded byte, g/l/u |
| --- | ---: | --- |
| `p2:startCliantTalkTurn(2, p1)` | 3 | 3360 / 3293 / 3351 |
| `p2:_runCharaScheduler(353964032)` | 6 | 3372 / 3305 / 3363 |
| `p2:say(p0, firstRow, 0)` | 11 | 3392 / 3325 / 3383 |
| `p2:say(p0, secondRow, 0)` | 16 | 3412 / 3345 / 3403 |
| `p2:_runCharaScheduler(fadeScheduler)` | 19 | 3424 / 3357 / 3415 |
| `p0:_wait(2)` | 22 | 3436 / 3369 / 3427 |
| `p0:startFadeOut(p1, 1)` | 26 | 3452 / 3385 / 3443 |
| `p0:_wait(1)` | 29 | 3464 / 3397 / 3455 |
| `p0:startFadeIn(p1, 1)` | 33 | 3480 / 3413 / 3471 |
| `p2:_runCharaScheduler(354107392)` | 36 | 3492 / 3425 / 3483 |
| `p2:say(p0, finalRow, 0)` | 41 | 3512 / 3445 / 3503 |
| `p2:finishCliantTalkTurn()` | 43 | 3520 / 3453 / 3511 |

Scheduler and wait calls use `CALL B=3`; say calls use `B=5`; the start-talk
and fade calls use `B=4`; finish uses `B=2`. Here `B` is one plus the argument
count, including the receiver.
`RETURN A=0, B=1` at PC 44 / bytes 3524, 3457, and 3515 returns zero values.
It does not return one nil value or forward any engine-call result.

The fades are issued after the two opening dialogue calls and the
`fadeScheduler` call. There is an explicit wait between fade-out and fade-in.
There is no explicit wait between fade-in and the following scheduler.
This establishes call order and literal arguments, not fade completion,
elapsed wall time, or the native scheduler/wait implementations. The source
corroborates waits/fades at lines 407-423 in `spl0g1` and `spl0u1`, and
395-411 in `spl0l1`. Finish is at source lines 435-436 or 423-424 respectively.

## Variant comparison and boundary

| Selected argument | `Spl0g1` | `Spl0l1` | `Spl0u1` |
| --- | ---: | ---: | ---: |
| `GirlStart` initial `turn` | 2 | 1 | 1 |
| `020` dialogue rows, in order | 27, 28, 29 | 25, 26, 27 | 27, 28, 29 |
| `020` scheduler immediately before `_wait(2)` | 69160960 | 69160960 | 68419584 |

These are all argument differences in the six selected methods. The
`GirlStart` branch, retained result and return count agree across variants.
The `020` call order, fade arguments, waits and zero-value return also agree.

The focused Python checks modeled fixed-result adjustment, numeric versus
boolean equality, both dialogue paths, finish/return ordering and the fade
sequence with opaque calls. They covered 189 synthetic cases and rejected
30 mutations of selected result/control-flow facts or complete-chunk framing.
They did not execute Lua or the client. The normal-path finish and return
claims assume that the preceding calls complete normally. The methods do
not provide a protected cleanup path if an intervening call fails.

The selected methods and title joins do not identify the historical NPC,
placement, event calendar, eligibility, item or quest grants, or server
changes. Native call effects, producer result arity/domain, invoking caller,
and a progression relationship between these methods remain unresolved.
