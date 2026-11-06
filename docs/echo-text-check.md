# Echo text admission check

`DesktopWidget.checkText` returns one false value for nil or the exact empty
string. It returns one true value for every other supplied value. The
[echo output helper](echo-text-log-request.md#checker-request-and-result)
uses that result as its exact-false gate before requesting the log call.

## Predicate and composition

The original method has two fixed parameters `(D, S)` and no variadic tail.
Missing arguments become nil and extra actual values are discarded. The
receiver `D` is unused. The body compares `S` first with nil, then with `""`.
Each matching case returns exactly one literal false; the remaining case
returns exactly one literal true. There are no helper calls, global reads,
string conversion or receiver accesses in this body.

False, numeric zero, strings containing spaces, tabs or newlines, and
non-string values differ from both rejected operands. This predicate therefore
does not trim whitespace or validate a native string domain, byte encoding,
length, markup, permissions or chat policy. A true return is its Boolean
predicate result, with no assertion that the subsequent native accepts or
displays the supplied value.

If the echo helper's dynamically obtained `W.checkText` is this original
method, nil and the exact empty string take the helper's zero-result early
return. Other supplied values reach its later `worldMaster._printLog` request
unchanged. Both normal helper paths still return zero values. This static
composition requires that actual checker binding; it does not identify the
converter output, world/native receiver, post-preparation frame, live log sink
or historical invocation.

## Source identity and checks

The [echo caller source identity](local-echo-client-request.md#source-identity-and-reproduction)
pins the retained Lua archive, canonical connector, original LPB and decoded
payload at private-source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`, extraction `2012.09.19.0001`.
Canonical `widget/desktopwidget_connector.lua` lines874-888 supply this method.
Original `root/proto7` has eleven instructions, code offset31139, two fixed
parameters, raw vararg0, zero upvalues and no nested prototypes. Root PCs21-23
obtain `DesktopWidget`, create the closure at PC22 and assign the constant RK
key `checkText` at PC23. PCs and payload offsets are zero-based.

| Behavior | PCs | Decoded-payload offsets |
| --- | --- | --- |
| Nil comparison and one-false return | 0-3 | 31139-31151 |
| Exact empty-string comparison and one-false return | 4-7 | 31155-31167 |
| One-true return | 8-9 | 31171-31175 |

The eleven-word code range has SHA-256
`598bf26369ff84cce8438e6b9e56dc68f4ec81a371ac46ddbd9b3be7c2e29d92`.
`tools/retail_script.py` and `ChunkReader`/`instruction` in
`tools/build_quest_contracts.py` expose the authenticated original in memory.
A bounded type-preserving check passed thirteen authored cases for missing,
nil, empty, false, zero, whitespace and other supplied values, unused receiver,
extra actuals and one-Boolean returns. Seven changed predicate, Boolean-value
and return-width controls were rejected. These finite source checks executed
no helper body or retail runtime.
