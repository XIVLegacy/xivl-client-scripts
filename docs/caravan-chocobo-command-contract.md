# Caravan chocobo command client contract

`ChocoboCaravanGuard.chocoboCommand` forwards one supplied operand into a
restricted-choice menu. Only a first result equal to numeric 2 opens its
second question. After normal talk cleanup it returns exactly two values,
including an explicit nil second value when that question was skipped.
It does not enforce a Boolean input or validate either returned choice.

The containing class's separate `initForEvent` requests text bank 7680 with
provider identifier `chocoboCaravanGuard`. The command method itself makes
no text-bank load request. This refines the
[Caravan UI summary](content-director-ui-contracts.md#caravan-escort-director).
The selected sources establish client requests, not historical NPC placement,
an external event's typed invocation or an authoritative gameplay effect.

## Fixed frame and ordered requests

Write the frame as `chocoboCommand(N,A1,A2,A3,A4,A5,A6,A7)`, where N is the
method receiver. It has eight fixed parameters, no varargs, no upvalues and
no nested prototypes. Missing arguments occupy nil parameter slots. Values
beyond A7 are ignored. The method uses A1 through A4 only:

| Operand | Exact local use |
| --- | --- |
| A1 | Forwarded unchanged as the third operand in the first menu's trailing sequence `true,true,A1,true`. |
| A2, A3, A4 | Forwarded in this order as three formatting operands to the conditional second question. |
| A5, A6, A7 | Unused. |

All tuples below include their method receiver. W means the value of global
`worldMaster` at that particular lookup, and P is the first player-getter
result. Q and R name the first result of each question.

1. Resolve W and its `_getMyPlayer`, call `(W)` and retain one result P.
2. Resolve N's `startCliantTalkTurn` and call `(N,2,P)`, discarding results.
3. Resolve W afresh and its `askRestrictChoices`, then call
   `(W,N,N,1,true,true,A1,true)`. Retain exactly one result Q.
4. Initialize R to nil. Only `Q == 2` resolves W again and its `ask`, calls
   `(W,N,N,6,4,A2,A3,A4)` and replaces R with that call's first result.
5. Resolve N's `finishCliantTalkTurn`, call `(N)` and discard results.
6. Return exactly `(Q,R)`.

Each global lookup resolves the current value. A change made during the getter,
talk-start or first question can therefore change the WorldMaster receiver
of a later request. Each method lookup is also made at its own call site.
Neither a WorldMaster object nor one of its method values is cached across
these requests. Within a colon call, the looked-up object supplies both the
method lookup and its receiver argument. N is passed twice to each question,
separately from W.

The comparison uses numeric 2. Nil, false, numeric 0, numeric -3, Boolean
true and string `"2"` do not select the second question when supplied directly
as Q. The caller neither retries nor converts those results. When either
question returns no values, its fixed one-result request supplies nil to
the saved slot. Additional callee results are discarded. These local caller
fixtures do not prove that the published helpers or the native UI can
produce every directly supplied value.

## Restricted flags and formatting boundary

The following composition requires the dynamic first-question member to
resolve to the published
[restricted-choice helper](aetheryte-restricted-choice-flow.md#caller-and-prefix-scan-arity).
That helper consumes a Boolean prefix, includes original slots whose values
are exactly true, and preserves the first non-Boolean value and remaining
values as a formatting tail. The command supplies the exact finite sequence
`true,true,A1,true`. It does not coerce A1 or append a separate terminator.

| A1 type/value | Boolean prefix | Conditional answer rows | Formatting tail |
| --- | --- | --- | --- |
| Boolean true | `true,true,true,true` | `2,3,4,5` | No values |
| Boolean false | `true,true,false,true` | `2,3,5` | No values |
| Any non-Boolean, including nil or numeric 0 | `true,true` | `2,3` | Exactly `A1,true`, including one explicit nil when A1 is nil |

Rows are `1 + original slot number` in a newly constructed dense answer
table. A false A1 omits row 4 rather than creating a disabled placeholder.
A non-Boolean A1 ends the restriction prefix, so the final literal true is
part of the formatting tail rather than another displayed answer flag.
Numeric zero is therefore different from Boolean false here.

For a Boolean A1, the four Boolean operands exhaust the original helper's
open `select` result at its prefix probe. The following open call is
`type()`, with zero arguments, rather than `type(nil)`. Under retained base
`select` and standard Lua `type`, that is a missing-argument error at helper
PC25 before a connector or widget is reached. The caller has already started
talk and has no handler that requests its later finish on that error.

The published helper page adopts the authenticated
[native arity contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/lua-base-library-arity.md#lge-override):
the installed LGE `type` override distinguishes missing input from explicit
nil and selects its diagnostic path for no input. Actual global bindings,
diagnostic protection and propagation at this command invocation remain
unbound. Thus the all-Boolean tuples do not establish an observed retail
menu failure or guarantee a normal helper result. Their downstream rows
above require normal prefix-scan completion with the stated interpretation.

A non-Boolean A1 instead supplies a two-value tail `A1,true`; the prefix
boundary and the helper's lookahead have supplied values. The published
helper contract's nil/true formatting-tail fixture preserves both values.
This differs from appending one nil after an otherwise exhausted Boolean
sequence, which can leave the helper's second probe without an argument.
No missing argument is silently padded inside an open `select`/`type` call.

Conditional on a normal helper return for an integer compact answer within
the requested answer count, the result is an original slot number:

| Compact answer | A1 true | A1 false | A1 non-Boolean |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 |
| 3 | 3 | 4 | Outside requested count |
| 4 | 4 | Outside requested count | Outside requested count |

Consequently compact answer 2 selects the conditional second question in
each normally completed variant. This mapping is not proof that an actual
UI opened or delivered that answer. The helper's result scan has no
answer-count or end-of-varargs rejection. An out-of-range positive result
therefore has no general safe-result guarantee. The published scan boundary
must not be replaced with an invented validation or cancellation rule.

## Conditional Ask and result composition

Write D for the global `desktopWidget` resolved by a matching WorldMaster
helper. Let `answers` be the first menu's dense table above and `tail` its
complete formatting tail. The shared
[Camp question flow](camp-replacement-choice-flow.md#ordered-call-and-display-requests)
owns the connector and Ask behavior adopted here.

| Reached boundary | Exact ordered tuple |
| --- | --- |
| Restricted helper to `askForEventMode` | `(D,N,W,N,1,false,true,1,answers,tail...)` |
| Second `WorldMaster.ask` to `askForEventMode` | `(D,N,W,N,1,false,true,6,{7,8,9,10},A2,A3,A4)` |
| Each connector opening request | `(D,4,"Ask/AskWidget",nil,nil,false)` |
| First opened widget's `ask` | `(widget,W,N,1,false,true,1,answers,tail...)` |
| Second opened widget's `ask` | `(widget,W,N,1,false,true,6,{7,8,9,10},A2,A3,A4)` |

Here `{7,8,9,10}` denotes a dense table indexed from 1. Each route requests
default compact answer 1, paging false and cancellation true. The first
answer count is the constructed table's length. The second answer count is
4. Neither count is inferred from the opening category, which is separately
literal 4. Applied work storage and its default-range reads remain premises.

The selected question property request uses provider N and row 1 with the
complete first formatting tail, or provider N and row 6 with exactly
`A2,A3,A4`. For example the latter tuple is
`_setProperty(widget,nil,"TextBlock_Question","Text",N,6,A2,A3,A4)`.
The extra W operand does not replace N as text provider. No selected text
cell, localized label, native renderer or delivered control-name binding
has been inspected for these rows.

The connector initializes its result to numeric 0. Exactly nil opening
skips widget operations and close. A non-nil opening proceeds to the widget
method lookup; false can fail there. After a normal widget ask, only exact
true selection requests `getAskResult`. Normal completion for a non-nil
opening then requests `closeWidgetDirect` and discards its results. Errors,
suspension or nonreturn can prevent later requests. This close request does
not prove native destruction, and the wait has no fixed timeout on this route.

The first helper adapts the reached connector result before the caller
compares Q. The second helper is ordinary `WorldMaster.ask`, whose separate
scalar passthrough is documented by the Camp flow:

| Reached connector result | First helper / Q | Second helper / R, if asked |
| --- | --- | --- |
| Numeric -3 | One nil | One nil |
| Numeric 0 | One numeric 0 | One numeric 0 |
| Other nonpositive number | One numeric 0 | Same number |
| Nil or Boolean | Numeric comparison error before a first-helper return | Same scalar |
| Integer compact answer in requested range | Original slot number above | Same scalar |

For the first menu, an opening failure or non-true selection therefore
normally produces Q=0, while cancellation normally produces Q=nil. Both
skip the second question and, after normal talk finish, return two values:
`(0,nil)` or `(nil,nil)`. Neither outcome selects original slot 1.
When Q=2, a second cancellation returns `(2,nil)` and a second numeric-zero
failure returns `(2,0)`. A false second result remains `(2,false)`.
The caller adds no acceptance conversion.

The pinned Ask operation handler parses a delivered answer-name suffix and
adds no answer-range guard. Cancellation requests -3 only with exact true
`canCancel`. Those source paths do not establish which names the native UI
can deliver. A later first-helper comparison error follows any close request
already made by a normally completed connector; a prefix-probe error instead
precedes connector entry. Neither error produces a normal two-value caller
return or reaches the caller's talk-finish request.

## Original widths and source identity

The extraction is retail 1.23b `2012.09.19.0001`. PCs are zero-based and
offsets are bytes in the decoded payload. Only the command and its separate
text initializer were interpreted. The complete canonical member matched
[scripts.json](../manifests/scripts.json), exact key
`lua/scripts/chara/npc/monster/chocobo/chocobocaravanguard.lua`, inside the
archive declared by [private_lua_corpus.json](../manifests/private_lua_corpus.json).
The original resource and payload matched the same key in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Representation | Bytes | SHA-256 |
| --- | ---: | --- |
| Canonical member | 1624 | `b3bb82478514322df268336d8d90a6a2cd66af3ed133923802c3181bdf37bb7e` |
| Original LPB | 844 | `1230331709ed7ac9deaba4705b802d905f72a8db7943e0cf2e880fe4bbce9c18` |
| Decoded payload | 831 | `e1e8c253a8a20c9a1479772f53541ef1b471874a4b514710d04acae6655ddc27` |

The resource is
`729s9/wu7/xvwrq5s/72v7v8v/72v7v8v79s9o9w3p9s6.le.lpb`, relative to
retail `client/script/`. Canonical locators are command lines 32-77 and
initializer lines 20-29. Root CLOSURE/SETTABLE PCs14/15 bind root/proto2 to
`chocoboCommand`; PCs11/12 bind root/proto1 to `initForEvent`.

The command starts at payload `0x1F0`, has 37 words and the fixed frame
described above. All of its calls and returns use fixed widths:

| Site | Arguments / requested results |
| --- | --- |
| `_getMyPlayer`, PC2 / `0x1F8` | 1 / 1 |
| `startCliantTalkTurn`, PC6 / `0x208` | 3 / 0 |
| `askRestrictChoices`, PC16 / `0x230` | 8 / 1 |
| Numeric-2 comparison, PC18 / `0x238` | Exact equality, not truthiness |
| Conditional `ask`, PC29 / `0x264` | 8 / 1 |
| `finishCliantTalkTurn`, PC32 / `0x270` | 1 / 0 |
| RETURN PC35 / `0x27C` | Exactly 2 results |
| Trailing RETURN PC36 / `0x280` | Zero results; unreachable in local control flow |

The initializer starts at `0x174`, has five words, one fixed parameter and
no varargs, upvalues or children. Its sole call is
`N._loadTextDataPermanently(N,7680,"chocoboCaravanGuard")`, PC3 / `0x180`,
with three arguments and zero requested results. RETURN PC4 / `0x184`
returns zero values. The initializer's existence does not prove it ran on
the object used by a particular command invocation.

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader,instruction`. Authenticate the
complete inputs and payload consumption, verify the root bindings, then
interpret only these 42 words. Focused original-VM executions and literal
canonical evaluations in memory agreed with an independent authored caller
oracle on 117 cases. They covered typed inputs, missing and extra arguments,
zero/one/multiple callee results, conditional questions, fresh global lookup,
errors and normal cleanup. Eleven rejecting controls changed original
operands or canonical predicates/return widths. The initializer's provider,
tuple and zero-result return also agreed. No discrepancy was found in these
selected original and canonical methods.

The canonical fixture used Lua 5.4.8 for this fixed-width caller, with opaque
authored callees. Helper composition checks projected the already published
contracts; they did not reopen helper, connector or native bodies. No retail
body, complete instruction vector or decoded payload was retained. These
checks establish the selected static contract, not live retail execution.

The method has no protected call, argument validation, result-range guard
or compensating cleanup. Actual actor identity, external argument producers,
runtime bindings, text rendering, wait completion and accepted cleanup remain
unproved. No selected request establishes feeding, material debit, health,
cargo, timing, reward or actual movement effects.
