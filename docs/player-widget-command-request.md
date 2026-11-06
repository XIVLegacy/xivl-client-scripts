# Player widget-command request

Original `PlayerBaseClass.commandAboutWidget` conditionally requests
`_executeCommand` with the resolved command name, supplied command operand and
complete extra tail. It keeps only the first result, writes its saved entry
time to the widget blocker, and returns that one result. A truthy force operand
also requests cancellation before execution and information-request recording
after the blocker write. These are local Lua requests, not evidence of native
command admission or accepted widget creation.

## Inputs and ordered local behavior

The original has three fixed slots `(P,C,f)`, including receiver `P`, followed
by `...`. Missing fixed arguments become nil. `C` is the supplied command
operand and `f` is tested with Lua truthiness: only nil and false are falsey.
Numeric zero, an empty string and other truthy values take the forced path.
The adapter does not normalize or validate these operands.

On normal completion of each reached lookup and call:

1. Resolve global `worldMaster` and request its `_getServerTime` method with
   that receiver. Keep only first result `t`. Read `P.playerWork`, then that
   object's `widgetCommandBurstBlocker` as `b`.
2. If `b ~= 0`, evaluate the Lua comparison `t < b`. When both comparisons
   hold and `f` is falsey, return exactly one false. No command-name lookup,
   playing query, cancellation, execution or store follows this rejection.
3. Otherwise request `P:getCommandName(C)` and keep only first result `n`.
   For falsey `f`, request `P:_isCommandPlaying(n)` and keep its first result.
   A truthy result returns exactly one false before execution or stores.
   For truthy `f`, skip that query and request `P:_cancelCommand(n)`, discarding
   all cancellation results.
4. Resolve `P._executeCommand` as saved function `G`, saving `P` as its
   receiver. Request exactly `G(P,n,C,...)`, preserving the complete incoming
   extra tail. Keep only its first result `r`.
5. Read `P.playerWork` afresh and write `t` to that result's
   `widgetCommandBurstBlocker`. If `f` is truthy, request
   `P:recordRequestInformation()` and discard all its results. Return exactly
   one value `r`.

The force test in step 2 follows both blocker comparisons. Truthy force does
not bypass the time call, blocker reads or a reached comparison. In particular,
nil, false or a string blocker is not converted to numeric zero. The comparisons
retain Lua's type rules and any applicable metamethod behavior. A numeric
blocker equal to `t` does not reject, and exact numeric zero skips the ordering
comparison even if `t` is negative. Neither rejected path writes the blocker.

The name, time and execution calls each retain one result: zero results become
nil and extra results are discarded. Nil or false `n` is passed onward without
a guard. A false, nil or zero execution result still precedes the blocker write
and, for truthy force, the recording request. The final return does not convert
`r` to Boolean or return the cancellation/recording result. The blocker store
uses the entry sample `t`, with no added interval and no second time call in
this adapter. Its fresh `playerWork` read need not return the object read by
the initial gate.

The request preserves zero extras, explicit nils, false, zero and trailing nil
positions. With no extras, `_executeCommand` receives exactly three arguments
including its receiver. One explicit nil extra adds a fourth position. The
fixed force slot is consumed locally and is not inserted into that tail.
Canonical source line 2611 assigns ellipsis to only one local; that
rendering does not express the original full-tail forwarding.

The published [information-request record contract](player-command-event-routes.md#information-request-guard-and-record-state)
owns the nominal recording helper and its separate `requestBurstBlocker`
state. Its application here requires the dynamically resolved method to be
that implementation and to complete normally. This adapter does not check
`canRequestInformation` or consume a recording success flag. The published
[clock qualification](player-command-event-routes.md#clock-qualification)
owns the conditional native clock domain. Neither contract establishes an
accepted request, a request rate or a monotonic clock.

There is no loop, explicit wait, protected call, error handler or rollback in
the adapter. The first opaque call is the time request. Errors, supported
suspension or nonreturn in reached dynamic lookups, comparisons, calls or the
store can prevent later work. In particular, cancellation must return normally
before execution; execution must return normally before the blocker store;
and a forced recording failure can occur after that store and prevent the
final return. A saved function and receiver do not freeze their referenced
objects or establish their runtime identities.

## Conditional composition with widget creation

The existing [commandCreateWidget forwarding contract](content-director-ui-contracts.md#commandcreatewidget-forwarding)
owns its two separate player lookups, saved function `F` and final request:

```text
F(q1,c,p3,p2,...)
```

If that saved `F` is this adapter, its fixed slots are `(q1,c,p3)` and its
complete extra tail is `(p2,...)`. If its local gates and dependencies reach
execution, it requests exactly:

```text
G(q1,n,c,p2,...)
```

Here `n` is the first result of `q1:getCommandName(c)`, and `G` is the later
saved `q1._executeCommand` function. The originating wrapper forwards this
adapter's one normal return, including a rejection false or a nil execution
result. The original wrapper's `q1` and `q2` remain separate lookup results;
the source does not establish their equality.

The [tutorial opener](tutorial-widget-opening-contract.md#static-module-and-creation-relationships)
selects `Ask/TutorialWidget` for the path operand. This conditional composition
extends its local request route. It does not identify the actual callable `F`
or `G`, native receiver or typed conversion, runtime class of `c`, selected
native callback, or the frame received by `WidgetOpenCommand`. The
[WidgetOpenCommand contract](widget-open-command-boundary.md) remains a separate
conditional body contract. An actual command dispatch, `_createActor` suffix,
factory class selection, initialization and accepted creation are still
unestablished by these Lua adapters.

## Source identity and reproduction

This is static evidence from extraction `2012.09.19.0001`, retail client
1.23b. Authenticate the archive using
[private_lua_corpus.json](../manifests/private_lua_corpus.json), canonical member
using [scripts.json](../manifests/scripts.json), and original resource and
decoded payload using [retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
The archive is 14385427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.

The canonical member `lua/scripts/chara/player/playerbaseclass.lua` is
66466 bytes, 3020 lines, SHA-256
`6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4`.
The selected declaration, function end and class binding are lines
2576, 2621 and 2623. Its `_executeCommand` reference is line 2608.
The original resource `client/script/729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`
is 25846 bytes, SHA-256
`32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e`.
The 25833-byte decoded payload has SHA-256
`1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`.

Use `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader`, `instruction` and `successors`
at revision `2fe7f00be3d989b5843a4139da99777491c545ae`. Check complete payload
consumption and the root class/name assignment. Root CLOSURE/SETTABLE PCs
196/197 bind child61 to `PlayerBaseClass.commandAboutWidget`.
The full `root/proto61` body is 42 words/168 bytes at
`[0x580D,0x58B5)`, PCs 0-41, three fixed parameters, raw vararg flag 3,
zero upvalues and no child prototypes. Its original debug lines 8030-8075
are distinct from canonical source lines. PCs are zero-based and payload
intervals are half-open.

| Operation | Original PCs | Adjustment or decision |
| --- | --- | --- |
| Entry time and blocker reads | 0-4 | Time CALL2 keeps one result. |
| Blocker gate | 5,7,9 | Numeric-zero equality, strict time/blocker ordering, force truthiness. RETURN12 returns one false. |
| Command-name request | 13-15 | CALL15 keeps first result `n`. |
| Playing or forced cancellation | 16-28 | CALL20 keeps one playing result. Truth test21 can reach one-false RETURN24. CALL28 discards cancellation results. |
| Execution request | 29-33 | SELF29 at `0x5881`; VARARG32 has `A=11,B=0`; CALL33 at `0x5891` has `A=7,B=0,C=2`. |
| Blocker write and forced recording | 34-39 | Fresh `playerWork` read34, saved-time store35, force truth test36, zero-result CALL39. |
| Final return | 40 | One-result RETURN `A=7,B=2`. Empty RETURN41 has no normal reachable path. |

Focused original-instruction replay checked 250 synthetic local paths with
opaque dependency replies. It checked force/playing truthiness, blocker zero
and strict equality boundaries, comparison-before-force behavior, original
command and saved-name operands, full nil-bearing tails, one-result
adjustments, fresh blocker-write target and interruption order. Fifteen
gate, operand, argument/result-width and saved-time mutations were rejected.
These checks characterize the admitted Lua instructions. They do not execute
the client or establish helper/native semantics or a historical invocation.
