# Multiple-text-macro request

`WorldMaster.askMultipleTextMacro` builds a numbered text table, forwards a
request to `desktopWidget.askForEventModeMultiple`, and translates one result
using flags that equal boolean `true`. Its original bytecode preserves the
complete flag tail. The canonical decompile forwards only its first flag and
has additional fixed-width `select` calls. Those are different contracts.

The source locator is `world/worldmaster_event.lua:268-329`, authenticated by
[`manifests/scripts.json`](../manifests/scripts.json), entry
`lua/scripts/world/worldmaster_event.lua`. Exact transport and return widths
below come from original `root/proto9`, code offset 2186, 57 instructions.
Neither representation establishes rendered menus or server behavior.

## Original arguments and preparation

The original has seven fixed parameters, including `self`, and raw vararg
flags 3. It has no upvalues or child prototypes. Root PCs 28-29 create
`root/proto9` and bind it to `askMultipleTextMacro`.

| Position including receiver | Canonical name | Role established here |
| --- | --- | --- |
| 1 | `A0_2` | `self`, forwarded as the third request argument |
| 2 | `A1_2` | Forwarded as the second request argument |
| 3 | `A2_2` | Forwarded as the fourth request argument |
| 4 | `A3_2` | Forwarded as the fifth request argument |
| 5 | `A4_2` | Text-table base, also forwarded unchanged |
| 6 | `A5_2` | Numeric-loop limit, called `count` below |
| 7 | `A6_2` | Arithmetic operand, also forwarded unchanged |
| 8 onward | `...` | Complete ordered flag tail |

There are no explicit parameter defaults or eligibility checks. Omitted
fixed arguments receive Lua's ordinary nil padding. That does not make nil
a valid arithmetic operand. The original uses `select("#",...)` to obtain
the actual tail width, including internal and trailing nil positions.

A fresh plain table receives `table[i] = A4_2 + i` for the numeric loop
`i = 1,count,1`. Every visited index receives an entry, including indices
whose flag is false, nil, zero, or absent. Each iteration calls a freshly
read global `select` with `i` and the complete original tail. Only its first
result is retained. The helper counts flags that equal boolean `true`.
Numeric 1, numeric 0, strings, false and nil do not satisfy that comparison.

Before looking up the request target, the helper evaluates:

```text
actualFlagCount - (count + trueFlagCount * A6_2)
```

This result is unused. The operations still execute and can fail before
the request, including when `A6_2` is false or nil. The table loop and its
additions occur first. There is no custom type check, range check, clamping,
or error handler. Numeric conversion and failure behavior belong to the
ordinary Lua arithmetic and numeric-for rules.

## Original request and reads

At PC 23 the helper reads the current global `desktopWidget`. PC 24 reads
its `askForEventModeMultiple` member and captures that same desktop object
as the method receiver. PC 35 requests one result. The ordered function
arguments, including the receiver, are:

| Position | Value |
| --- | --- |
| 1 | Captured `desktopWidget` |
| 2 | `A1_2` |
| 3 | `self` |
| 4 | `A2_2` |
| 5 | `A3_2` |
| 6 | Boolean `false` |
| 7 | Boolean `true` |
| 8 | `A6_2` |
| 9 | `A4_2` |
| 10 | The fresh text table |
| 11 onward | Every original flag, unchanged and in order |

The width is `10 + actualFlagCount`. Original PCs 34-35 use
`VARARG B=0` and `CALL B=0 C=2`. False, zero and nil are not removed.
Extra flags beyond `count` reach the request even though the two helper
loops do not visit those extra positions. There is no separate final
formatter tail in this helper: all extra arguments occupy the same flag
tail.

The other global is `select`: it is read at PC 0, again on each first-loop
iteration at PC 10, and again on each result-loop iteration at PC 41.
Original PCs 2-3, 12-13 and 43-44 preserve the open tails for these calls,
each retaining one result. No player, rank, company, admission, provider
field, or `self` member is read. The parameters and original tail belong
to this invocation. The table and counters are fresh. There is no captured
upvalue state or global write.

These statements assume ordinary Lua `select`, arithmetic, table access,
and equality. A replaced global or effectful member lookup can fail or
change behavior. The Lua body has no protection around those operations.
The separate [WorldMaster message contract](worldmaster-message-arguments.md)
owns `say`, `notify` and `alert`; their message-pool contracts do not supply
this request's semantics.

## Original result translation

After the request, a fresh counter starts at zero. The helper again visits
`i = 1,count,1` and obtains the first result of `select(i,...)`. Only inside
the boolean-`true` flag arm does it increment the counter, compare that
counter with the retained request result, and return `i` on equality.
Every other flag skips both the increment and the comparison. Original
PCs 45-46 send that non-true path directly to the loop continuation at
PC 51, bypassing the result comparison at PC 48 and return at PC 50.

If no enabled position matches, numeric `-3` becomes nil. Every other
retained result passes through unchanged. There is no validation that an
unmatched result is a valid choice index. For example, with flags
`false,true,true`, results 1 and 2 become 2 and 3, while result 3 remains 3.
An unmatched zero, another negative number, false, nil or a string is also
returned unchanged under ordinary equality rules.

The request's extra results are discarded by `CALL C=2`. Both reachable
returns, PCs 50 and 55, use `RETURN B=2`: exactly one value, including when
that value is nil. The final zero-value return at PC 56 is unreachable.
The result loop can return before visiting its remaining flags. Its fresh
`select` reads occur before the final `-3` comparison. A request error
prevents all result processing. An error during result processing prevents
the final conversion. There is no later eligibility recheck in this body.

## Conditional three-choice profile

The [CompanyBuffer Welcome menu](sanction-company-buffer-contract.md#menu-arguments-and-scalar-results)
supplies the argument frame below. `W` is the method receiver, `N` is the
same supplied object in two positions, and `a` is boolean admission:

```text
askMultipleTextMacro(W,N,N,1,4,3,0,a,true,true)
```

The original makes this 13-argument request:

```text
askForEventModeMultiple(desktopWidget,N,W,N,1,false,true,0,4,
                       {5,6,7},a,true,true)
```

| Admission | Original text table | Request result 1 | Request result 2 | Request result 3 |
| --- | --- | --- | --- | --- |
| `true` | `{5,6,7}` | 1 | 2 | 3 |
| `false` | `{5,6,7}` | 2 | 3 | 3 |

For either mask, request result `-3` becomes one nil. With the false mask,
the recovered original cannot produce numeric 1 under ordinary equality
and library behavior: no enabled original position is 1, and a retained
numeric 1 is translated to 2. Supplying numeric 1 directly as this helper's
return to a caller is a distinct assumption from composing this body with
an underlying request result of numeric 1.

This profile establishes the request operands and local index translation.
It does not assign UI meanings to `false,true`, zero, the table base, or
the flags. In particular, it does not establish disabled-choice clicks,
which row is displayed or focused by default, cancellation behavior of the
underlying widget, or application of Sanction.

## Canonical decompile discrepancy

The canonical source is retained literally. Its fixed assignments pad
missing varargs with nil and truncate excess varargs before the calls:

| Source call | Total arguments | Tail slots after index or fixed request prefix |
| --- | --- | --- |
| Line 273, `select` count | 15 | 14 |
| Line 283, per-table-iteration `select` | 8 | 7 |
| Line 306, request including receiver | 11 | 1 |
| Line 315, per-result-iteration `select` | 6 | 5 |

Consequently its ordinary `select("#",...)` result is always 14. Its
request forwards exactly the first flag, including one nil when no flag
was supplied. For the three-choice frame it forwards 11 arguments and
omits the two trailing true values. The selected result translation agrees
when a common request result is injected into each representation, because
the three visited flags fit both fixed `select` widths. This does not make
the request contracts equivalent. With a true flag at position 6 and no
earlier true flag, original result 1 maps to 6 when `count=6`; the canonical
result loop cannot observe that flag and returns 1.

The original instructions own claims about complete tails, actual flag
count, and exact request width. The canonical source owns the fixed-width
behavior above. Normalizing those source assignments into open varargs
would conceal the discrepancy.

## Identity and verification boundary

The archive is identified by
[`manifests/private_lua_corpus.json`](../manifests/private_lua_corpus.json).
Only its `world/worldmaster_event.lua` member supplies the selected source.
The source member has 7,559 bytes and 329 lines, SHA-256
`744487A7CAAA94E1C4D2056CC07686A894C6BA336BBD021BBFFEEBCEEF2AD099`.
The original resource is `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb`, relative to
`client/script/`, as recorded in
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
Its 2,555 bytes have SHA-256
`4CED313114AB09753AD0DC82EA8E9CD12C66D31447C967E91883932291CD7459`.
The decoded payload has 2,542 bytes, SHA-256
`C7DB606357F8E5811809A6232157C2C9AC1DAF0055CFCAA01FBBC7051FD68BF5`.

In-memory decoding used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` and `instruction`. Focused
original-instruction replay and a separate literal canonical-source
interpreter checked the request, loops, strict flags, nil padding, open
tails, discarded extra results, return widths, and pre-request error order.
Independent expected cases covered both three-choice masks, extra and absent
flags, non-boolean flags, `-3`, unmatched values, and the fixed-width
disagreement. In-memory rejecting controls changed open tails to fixed
tails, request-result retention, strict-true comparison, cancellation and
request boolean literals. These checks do not execute the retail client.

`desktopWidget.askForEventModeMultiple` is the first uninspected application
dependency. Its body, providers, native bindings, UI selection rules,
yielding, rendering, runtime state and server effects remain outside this
contract. No inference here crosses that boundary.
