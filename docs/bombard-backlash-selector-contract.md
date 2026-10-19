# Bombard Backlash item selector contract

`Spl102.processEventItemSelection` supplies two complete eight-item arrays to
`Ask/RewardSelectWidget`. Original bytecode establishes both first entries and
the caller's result handling. This is a client presentation and return contract.
The [seasonal quest identities](seasonal-quest-client-contracts.md#retail-quest-identities)
join `Spl102` to Bombard Backlash, quest ID `110860`.

## Original inputs and locators

The extraction is `2012.09.19.0001`. The resource names and byte pins below are
recorded in [retail Lua coverage](../manifests/retail_lua_coverage.json), and the
canonical source pins are recorded in [the script manifest](../manifests/scripts.json).
PCs are zero-based. Byte offsets are decimal offsets in the decoded payload.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `client/script/tp5rq/r75w9s1v/ruy/ruyijh.le.lpb` | 12679 | `cec1ba8009cd51d409d70812eeecc9a5f18c88fb6b323acefd28fffead520fe7` |
| Decoded `Spl102` payload | 12666 | `c8b972de0500c7517c7ca21cd552b24b591364f7b5270d58259d7c480b0d0fc9` |
| Canonical `lua/scripts/quest/scenario/spl/spl102.lua` | 49963 | `94081214ad3e3393af69a676ab5be58f7c2c96aacc65d6a01bb866ee91534e6b` |

The root declaration is PC `21`, byte `116`, assigning `root/proto4` to
`Spl102.processEventItemSelection`. The method has five fixed parameters,
no varargs, and 857 instructions beginning at byte `3912`. Its canonical
source function is lines `521-1498`, with the method assignment at line `1500`.

Only `Spl102` and the existing `RewardSelectWidget` chunk were selected.
The latter's LPB SHA-256 is
`71a3875baac970973bf38d6a2556ff5ba92c9b800b67b703c1338e4fdad87911`,
decoded-payload SHA-256
`49e4efc9b59917ca88ea3ee2af319012d79b0a434c559dda68935d8dff603a5b`,
and canonical-source SHA-256
`ee220caa549be99a3b69b557822fabd64004125f6e33f6d91596fc6347899548`.
The [widget result contract](reward-widget-result-contracts.md) owns its base
ask-result semantics. Original `root/proto25` PCs `39-44`, bytes `11830-11850`,
corroborate its selection result write, and `root/proto23` and `root/proto24`
PCs `0-3`, bytes `11500-11512` and `11587-11599`, corroborate cancel and close.

## Array and argument contract

Parameter registers are described by their use, without assigning unproven
actor classes: `R0` is passed as a dialogue and widget argument, `R1` receives `isMale`
and is passed to the initial talk-turn call, `R2` receives the talk and dialogue
methods, and `R3` selects numeric dialogue variants `0`, `1`, and `2`. `R4` is
not read. The numeric variants do not establish city identities.

The method calls `R2:startCliantTalkTurn(2, R1)` first (PC `3`, byte `3924`).
It retains one `R1:isMale()` result at PC `6`, byte `3936`, and compares it
with Boolean `true` at PC `7`, byte `3940`. This is equality with `true`,
not a general truthiness test. The true branch loads eight constants into
`R7-R14` and stores them with `SETLIST R6 8 1` at PC `18`, byte `3984`.
The other branch does the same at PC `30`, byte `4032`. Each copies the
constructed table to `R5`.

| One-based caller selector | `isMale() == true` item | Other result item | `say` count argument |
| ---: | ---: | ---: | ---: |
| 1 | 8032834 | 8032837 | 1 |
| 2 | 8032835 | 8032838 | 30 |
| 3 | 8032836 | 8032839 | 50 |
| 4 | 8051521 | 8051524 | 1 |
| 5 | 8051522 | 8051525 | 30 |
| 6 | 8051523 | 8051526 | 50 |
| 7 | 8081921 | 8081922 | 5 |
| 8 | 3020613 | 3020613 | 1 |

The outer menu is `R2:askExtendWidget(R0, 18, 3, 1, 1)` at PC `75`,
byte `4212`. Result `1` opens the item selector. That call at PC `122`,
byte `4400`, supplies the receiver and these arguments in order:

`desktopWidget:askEventModeWidgetYield("Ask/RewardSelectWidget", 1, R0, 19, retained, R5[1], R5[2], R5[3], R5[4], R5[5], R5[6], R5[7], R5[8])`

`retained` starts at `0`. The call retains two result slots in `R8` and `R9`.
Its first result is not consumed by this method. PC `123`, byte `4404`,
copies its second result to the retained argument before further processing.
When that second result equals an index `1-8`, the corresponding branch supplies
`R5[index]`, `10011253`, and the table's count as trailing `say` arguments.
The index comparisons are PCs `212`, `276`, `340`, `404`, `468`, `532`,
`596`, and `660`, at bytes `4760`, `5016`, `5272`, `5528`, `5784`, `6040`,
`6296`, and `6552`. These are dialogue substitutions, not exchange recipes.

## Confirmation, retry, and return

The confirmation call is `R2:askExtendWidget(R0, 72, 2, 1, 1)` at PC `714`,
byte `6768`. Its retained result is compared with numeric `1` at PC `715`
and numeric `-3` at PC `719`.

| Caller input condition | Selected method behavior |
| --- | --- |
| Second widget result `i` in `1-8`, confirmation `1` | Adds `10` to `i` and returns one value `i + 10` at PC `801`, byte `7116`. It does not call `finishCliantTalkTurn` on this path. |
| Confirmation `-3` or any other result unequal to `1` | Presents variant-specific dialogue, sets local result `199`, and reopens the item selector. The retained argument is the preceding raw second widget result. No finish call occurs before the retry. |
| Second widget result `-1` | Normalizes the local result to `9`, presents variant-specific dialogue, calls `finishCliantTalkTurn` at PC `167`, byte `4580`, then returns one value `9` at PC `801`. |
| Second widget result `9` | Takes the same finish-and-return path as normalized `-1`. |
| Second widget result `-3` | Presents variant-specific dialogue, calls `finishCliantTalkTurn` at PC `209`, byte `4748`, then assigns `9` and returns one value `9` at PC `801`. |
| Outer menu result `2` | Presents variant-specific dialogue and repeats the outer menu. |
| Outer menu result `3` or `-3` | Calls `finishCliantTalkTurn` at PC `847` or `853`, bytes `7300` or `7324`, then returns that menu result unchanged at PC `848` or `854`, bytes `7304` or `7328`. |

The retry test is PC `798`, byte `7104`. Local `199` branches through
PC `800`, byte `7112`, back to the widget setup at PC `107`, byte `4340`.
The compiler's final `RETURN B=1` at PC `856`, byte `7336`, returns no values
and is outside the method's reachable control flow.

`CALL B` encodes one plus the argument count, and `CALL C` encodes one plus
the retained result count. Counts below describe caller retention, separately from each producer's
actual return arity:

| Call | B | C | Arguments including receiver | Retained results |
| --- | ---: | ---: | ---: | ---: |
| Initial talk turn | 4 | 1 | 3 | 0 |
| `isMale` | 2 | 2 | 1 | 1 |
| Outer menu and confirmation | 7 | 2 | 6 | 1 |
| Reward widget open | 15 | 3 | 14 | 2 |
| `finishCliantTalkTurn` | 2 | 1 | 1 | 0 |

The three explicit value returns each encode `RETURN B=2`, returning one
value. The initial menu's other values repeat that menu. Widget results
outside the explicitly compared values still reach confirmation after the
index tests. This method does not establish the producer's runtime result
domain or enforce that it contains only the named selectors.

Both selected chunks parsed completely to EOF. An offline instruction model
checked the original words with synthetic call results for all eight indices,
the three numeric dialogue variants, Boolean equality, confirmation retry,
cancel normalization, and finish/return ordering. This was static verification,
not Lua VM or retail-client execution.

## Remaining boundaries

The named widget's base result write and this caller's second retained
widget-open result are distinct evidence points. The selected chunks do not
establish the forwarding implementation, actual native producer arity, runtime
result domain, or binding of this method to a historical invocation.

The item IDs and `say` arguments do not establish inventory validation,
currency consumption, grants, eligibility, quest completion, an invoking NPC,
city placement, or calendar availability. Settlement and historical invocation
require their own evidence.
