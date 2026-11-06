# CaravanManager entry and question contracts

`PopulaceCaravanManager.caravanGuardEntry` returns one local choice value.
Its result 3 can be synthesized from ask-16 result 2, while a result from the
conditional ask 23 is returned directly. `caravanGuardQuestion` repeats its
menu after results 1 and 2, otherwise finishes the talk turn and returns no
values. Neither method establishes historical registration, accepted caravan admission or a
server result.

## Evidence and notation

The selected decoded path is
`chara/npc/populace/populacecaravanmanager.lua`, extraction
`2012.09.19.0001`. Canonical source locators below refer to its authenticated
archive member. Original PCs are zero-based within the named prototype;
offsets are within the decoded Lua payload. The selection interprets the two
methods below and the 16-instruction `NpcBaseClass.isUpperRank` helper. The
initializer, other inherited helpers, ask implementation, dynamic getters,
callbacks and other methods are outside this selection.

`M` means the supplied `self`, `W` means the global `worldMaster`, and `P`
means the first result freshly obtained from `W._getMyPlayer(W)`. Call tuples
include every immediate argument, including receivers and repeated `M`
values. The callable is named separately. `H` means that a particular call to
`M.isUpperRank(M,A5,25)` returns exactly Boolean `true`. Each occurrence is a
new call, rather than a saved rank decision. A false, nil, 0 or 1 result takes
the other branch.

## Incoming values

| Method / source / original prototype | Fixed incoming frame |
| --- | --- |
| `caravanGuardEntry`, 33-232; root/proto1, code `0x2E1`, 175 instructions | `(M,A1,A2,A3,A4,A5,A6,A7)` |
| `caravanGuardQuestion`, 235-494; root/proto2, code `0x712`, 222 instructions | `(M,A1,A2,A3,A4,A5)` |

Both prototypes have no varargs, upvalues or children. Missing fixed arguments
become nil; extra supplied arguments are not consumed. No incoming value is
proved to be an actor, a character level, accepted membership or an
authoritative rank snapshot.

| Entry input | Exact local use |
| --- | --- |
| A1 | Compared with A5; formatted in several rows; added to A3. |
| A2 | Only `A2 == false` enables the second ask after first result 1. Nil and 0 do not enable it. |
| A3 | Compared with numeric 0; added to A1; participates in `40 <= A4 and A3 == 0`. |
| A4 | Compared with 40. It is not the rank value supplied to `isUpperRank`. |
| A5 | Second argument in `(M,A5,25)` for every rank-helper call; compared with A1; formatted in rows 21/41. |
| A6, A7 | Only forwarded to W's row 65, in order `(A7,A6)`. |

| Question input | Exact local use |
| --- | --- |
| A1 | Supplied to `doSalute`, compared with A5, formatted, and added to A2. |
| A2 | Only added to A1. It is not the entry method's Boolean-tested A2. |
| A3 | Forwarded to rows 11/43 or 32/44. |
| A4 | Only exact Boolean true enables an additional opening row. |
| A5 | Second argument to the rank helper, compared with A1, and formatted in rows 61/62. |

## Entry ordering and result

Write `S = A1+A3` and `G = (40 <= A4 and A3 == 0)`. The comparison with
A4 is evaluated first, including when A3 is not 0. The method obtains P and
calls `M.startCliantTalkTurn(M,2,P)` before any of these tests.

1. If A1 differs from A5, call the rank helper and say row 63 for H,
   otherwise 64. Both receive `(M,M,row,0,A1)`.
2. If G, make another rank-helper call. H selects row 47 with A1 then row 49;
   the other branch selects row 48 with A1 then row 50. If G is false,
   another rank-helper call instead selects row 15 for H or 37 otherwise,
   with `(M,M,row,0,A1,S)`.
3. Call W's `say` with `(W,M,65,D,A7,A6)`, where D is A1 when A3 equals 0,
   otherwise S. This is a different receiver and argument layout from M's
   `say`; there is no inserted zero argument after 65.
4. Call `M.askExtendWidget(M,M,16,2,1,1,S)` once and save its first result Q.
5. When Q equals 1 and A2 is exactly false, make another rank-helper call,
   say row 22 for H or 38 otherwise with `(M,M,row,0)`, then call
   `M.askExtendWidget(M,M,23,2,1,2)` once. Return that second ask's first
   result. It does not enter the Q-equals-2 branch, even if it equals 2.
6. Otherwise, when Q equals 2, G runs
   `M._runCharaScheduler(M,70795264)` and changes the returned value to 3.
   With G false, another rank-helper call selects row 21 for H or 41
   otherwise, using `(M,M,row,0,A5)`, and the returned value remains 2.
7. Every other path returns Q unchanged. In particular, Q equal to 1 with
   A2 nil, 0 or true returns 1. An unrecognized result, including -1, 0,
   false or nil, is neither normalized nor retried.

This method returns exactly one value, including one nil when the selected
ask result is nil. There is no `finishCliantTalkTurn` call in this method,
and no scheduler wait is requested here. Result 3 therefore does not uniquely
identify the original answer: it can be an original Q of 3 or the synthesized
G/Q-equals-2 result. A second-ask result 2 remains distinct from that latter
path. The native meaning of the ask arguments and cancellation delivery is
uninspected; numeric result handling does not establish labeled choices.

## Question ordering and repeat behavior

Here write `T = A1+A2`. Obtain P, start the talk turn with `(M,2,P)`, then
call `M.doSalute(M,A1,25)`. The original call requests one result but never
uses it. It is neither the rank-helper result nor an admission decision.

If A4 is exactly true, a rank-helper call selects opening row 60 for H or 42
otherwise with `(M,M,row,0,A1)`. Independently, a new rank-helper call selects
row 3 for H or 28 otherwise with `(M,M,row,0,A1,T)`.

The menu calls `M.askExtendWidget(M,M,4,3,1,3)` and retains its first result.
For every result 1 or 2, it makes a fresh rank-helper call and runs the
following presentation sequence before asking again. `sched(x)` means
`M._runCharaScheduler(M,x)` with no result requested or scheduler wait.
Every `say` below uses M's `(M,M,row,0,...)` layout.

| Menu result / helper branch | Ordered presentation calls |
| --- | --- |
| 1 / H | sched(353964032); say 8(T); say 9(); sched(354103296); say 10(A1) |
| 1 / other | sched(353964032); say 29(T); say 30(); sched(354103296); say 31(A1) |
| 2 / H | sched(354099200); say 11(A3); say 43(A3); say 12(T); sched(353980416); say 13(); say 45(); then say 61(A5) only if A1 differs from A5 |
| 2 / other | sched(354099200); say 32(A3); say 44(A3); say 33(T); sched(353980416); say 34(); say 46(); then say 62(A5) only if A1 differs from A5 |

Results 1 and 2 repeat the menu after their presentation. Numeric result 3
exits directly. Every other value, including nil, false, 0 and -1, is replaced
locally with 3 and then exits without a choice-specific presentation
(PC214-218). There is no local repeat limit or separate cancellation test.
On exit, call
`M.finishCliantTalkTurn(M)` and return zero values. This is different from
returning one nil. The menu result, salute result and all rank results are
absent from the outgoing frame.

## Immediate call and return widths

Widths count arguments after the callable, including the receiver shown above.
All calls have fixed widths. No selected call or return uses an open top-of-
stack argument/result range.

| Original site | Argument width / requested results |
| --- | --- |
| Both methods, PC2 `_getMyPlayer` | 1 / 1 |
| Both methods, PC6 `startCliantTalkTurn` | 3 / 0 |
| Entry rank helper PCs12,35,65,118,156 | 3 / 1 |
| Entry say PCs20,27,43,55,164,171 | 5 / 0 |
| Entry say PCs48,60,125,131 | 4 / 0 |
| Entry say PCs74,82 and W-say PCs92,101 | 6 / 0 |
| Entry ask16 PC109, `0x495` | 7 / 1 |
| Entry ask23 PC138, `0x509` | 6 / 1 |
| Entry scheduler PC150 | 2 / 0 |
| Entry RETURN PC173, `0x595` | One result; trailing PC174 zero-result return is unreachable in local control flow. |
| Question doSalute PC10 | 3 / 1; saved then unused |
| Question rank helper PCs16,35,69,125 | 3 / 1 |
| Question say PCs24,31,80,94,104,118,136,142,148,169,179,185,191,212 | 5 / 0 |
| Question say PCs44,52 | 6 / 0 |
| Question say PCs85,109,156,161,199,204 | 4 / 0 |
| Question ask4 PC62, `0x80A` | 6 / 1 per loop iteration |
| Question schedulers PCs74,88,98,112,130,151,173,194 | 2 / 0 |
| Question finish PC220 | 1 / 0 |
| Question RETURN PC221, `0xA86` | Zero results |

The selected canonical call widths, saved results, branch effects and return
widths agree with the original instructions. The one-result `doSalute` call
remains explicit despite its unused value. This agreement is limited to these
two methods and does not resolve the separately documented cancel-method
decompiler discrepancy.

## Shared rank gate

The [published shop lifecycle](grand-company-shop-lifecycle.md#lifecycle-and-state-ordering)
identifies `NpcBaseClass.isUpperRank` as a comparison of a requested threshold
with the local player's company rank, with raw rank 127 normalized to zero.
The selected original helper now fixes the comparison direction and exact
frame beyond that published summary. `isUpperRank(M,C,R)` has three fixed
parameters and no varargs, upvalues or children (root/proto18, code `0x1732`,
16 instructions; canonical `npcbaseclass_event.lua:883-904`). M is unused.

1. Call `W._getMyPlayer(W)`, requesting one result P2 (PC2, `0x173A`).
2. Call `P2._getGrandCompanyRank(P2,C)`, requesting one result K
   (PC5, `0x1746`). This is the supplied C, not a company obtained locally
   by this helper. The dynamic getter body and native value domain remain
   uninspected.
3. Replace K with numeric 0 only when K equals numeric 127 (PC6-8).
4. Compare `K <= R` (PC9, `0x1756`). Return exactly one Boolean true or false
   (RETURN PCs12/14, `0x1762`/`0x176A`). The trailing PC15 zero-result return
   is unreachable in local control flow.

If M's dynamic `isUpperRank` member resolves this helper, the caller frame
`(M,A5,25)` therefore compares the normalized getter value for company-selector
A5 numerically **at most 25**. Below/equal/above probes at 24/25/26 return
true/true/false. Raw 127 becomes 0 and returns true at threshold 25. That is
a numeric comparison, not an independently assigned rank name or an ordering
of named military ranks. It is not an A4 character-level check, a supplied
rank snapshot or a check against an incoming player object.

Each helper invocation obtains P2 afresh, independently of the caller's P
used to start the talk turn. The helper neither dereferences M nor validates
C. It forwards nil, false or 0 in C unchanged if supplied. A nil, Boolean or
string K reaches the comparison without normalization unless equal to numeric
127, and raises an ordinary type error against numeric R=25. A missing R
also reaches that comparison and can error. No helper error is converted into
false, and neither caller catches it. Actual getter delivery, dynamic method
registration and the server's company/rank authority remain unproved.

Even a matching helper's true result only selects dialogue here: neither
method rejects entry for a false result, and both helper branches converge on
the same ask layout. Rank results can differ between successive calls. No
selected caller caches one result as a stable eligibility or authorization
decision.

## Historical admission boundary

The [broader caravan UI summary](content-director-ui-contracts.md#caravan-escort-director)
owns the director/widget evidence. The
[reward guide contract](caravan-reward-client-contract.md#reward-and-completion-boundary)
owns the separate reward, return-to-camp and settlement limits. This selection
does not bind a numeric NPC class or historical placement, reconstruct an
external event's full typed invocation, prove historical entry requirements or
accepted admission, identify a route, establish entitlement or grant a reward.
No text-row meaning or rank-name variant is inferred from these numeric rows.

The callers have no argument validation, protected call or error recovery.
Missing A4 reaches the entry comparison after talk startup and any preceding
A1/A5 dialogue. Missing operands can fail the additions when their branches
are reached. Provider/helper failures propagate. Such failures do not create a
normal return, cleanup or authoritative rejection result. The argument frames
above describe local consumers, not a proved valid external invocation domain.

## Source identity and reproduction

The full member is 16,550 bytes, SHA-256
`273917c5d3f51c47c74bf6a22fd33b5cf371bd76c970dc2cd6d432b5f4ce462e`.
It matches [scripts.json](../manifests/scripts.json), exact decoded-script key,
inside the archive pinned by
[private_lua_corpus.json](../manifests/private_lua_corpus.json). The original
resource and decoded payload match
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json), the same key:
5,215 bytes, SHA-256
`7885754b8648a4079c5f04c78fb96e048a34294a301df5b4f98acb2acaa30a6d`,
and 5,202 decoded bytes, SHA-256
`2f553cd0595dbf6f38527b72ba3916416581cae16e35bf036ab1ce10c175fdaa`.

`tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader,instruction` reproduce the selected
original checks. Root CLOSURE/SETTABLE PCs11/12 bind proto1 to
`caravanGuardEntry`; PCs14/15 bind proto2 to `caravanGuardQuestion`. Focused
in-memory instruction probes and isolated canonical executions with authored
helper stubs check tuple widths, exact Boolean comparisons, changing helper
results, choice order and nil/false/0 distinctions. They do not execute the
retail client or the uninspected callees and retain no retail bodies or
instruction listings.

The separate `chara/npc/npcbaseclass_event.lua` member is 20,675 bytes,
SHA-256 `5417b1bdf762162cad240a84715d0fc85958dbe0181b653348a66c02ee4d7c80`.
Its same-manifest original resource is 6,262 bytes, SHA-256
`84a5098636ff289f4ecf4e164ee84e44890895e8a9005fb102e04929c2bb74bf9`,
and its decoded payload is 6,249 bytes, SHA-256
`4a3008dd8d2a91e7eb044e5555d2757468a9097bba5175992fb88f943bd07b6c`.
Only root/proto18 is interpreted; root CLOSURE/SETTABLE PCs55/56 bind it to
`isUpperRank`. Focused original/canonical probes agree on its fresh getter
frames, normalization, comparison direction and one-Boolean result width.
