# Parley opening request

`NegotiationJudge.openNegotiationWidget` requests the event-mode opening of
`Ask/NegotiationWidget` with nine supplied initializer values. It reaches that
request only after an exactly-true player test. Every normal path returns
zero values, including a normally returned false opening status.

The [input/result caller](parley-input-result-route.md) is a separate method
and incoming frame. This opener does not call it, select an answer, close
the widget or establish a server outcome.

## Incoming values, gate and results

Write the twelve fixed parameters as
`openNegotiationWidget(self,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11)`.
There are no varargs or captured upvalues. Missing parameters become nil;
extra actual values are discarded. `self` and A2 are unused by this body.

It captures `A1.isPlayer`, calls it with exactly A1 and retains one result.
No results become nil and additional results are discarded. Only literal
Boolean true reaches the opening request; every other normally returned
value skips it and returns zero values. The method name supplies no proof
of actual actor identity or native class.

After the test completes, it freshly obtains global `desktopWidget` as D,
captures D's `openEventModeWidgetYield` method and requests exactly:

```text
openEventModeWidgetYield(D,"Ask/NegotiationWidget",A3,A4,A5,A6,A7,A8,A9,A10,A11)
```

D is the lookup receiver and first argument. Neither the Judge receiver nor
A1 is forwarded. The nine values preserve their order, including nil, false
and zero. The fixed call supplies all nine positions even when some incoming
positions were omitted. This body adds no conversion, type check, default or
range check for them. The player call can change the global or its method
before the later lookup.

The opener keeps exactly one helper result and compares it with false.
Both comparison paths converge on the same zero-value return, with no
replacement assignment or extra request. Therefore a false result, nil,
zero, true, no helper results or extra helper results all leave the caller's
normal return width at zero. This does not report opening success or failure.
Lookup and call errors propagate; suspension or nonreturn produces no normal
return and does not reach a later selection method automatically.

## Conditional opening and initializer composition

The [published ShopBuy opening route](gil-shop-widget-opening.md#opening-and-selection-boundaries)
owns the same `openEventModeWidgetYield` method and its creation-completion
path through `openWidgetYield`, slot 4, `openWidgetLocal` and the widget-command
request. It distinguishes that opening wait from the later selection wait.
The recorded `_wait(0.1)` operands are conditional polling requests, without
a fixed opening duration. This adopts that existing helper contract under
the matching dynamic binding; no helper or native body was studied again.

This selected source establishes the Lua request above. The
[initializer contract](parley-initial-state-request.md#supplied-initializer-frame)
owns `NegotiationWidget.initAsk`'s separate nine-value frame. If the requested
nine-value tail reaches that implementation unchanged and in order, it maps
as follows:

| Opening caller value | Initializer position and request |
| --- | --- |
| A3, A4, A5 | Initializer A1, A2, A3, forwarded to the message-child initialization request. |
| A6 | Initializer A4, assigned to `work.time`. |
| A7-A11 | Initializer A5-A9, assigned to `work.ability1` through `work.ability5`. |

The initializer independently requests `work.select=1`. Neither this caller
nor that initializer supplies a fixed time value or establishes a unit,
supported domain, conversion or authoritative duration for it. The three
values used by the separate input method's `setAskParameter` call have their
own roles; equal formal-position names across those methods do not identify
equal runtime values or domains.

Actual command/loader selection, typed native frame, tail delivery, class and
method bindings, creation completion, same-instance identity, storage and
readback remain conditions. This conditional mapping supplies no actual
ability identity, timer behavior,
scoring, accepted result, server consumption or historical invocation.

## Source identity and checks

The [Judge source identity](parley-input-result-route.md#source-identity-and-original-locators)
pins the retained archive, canonical Judge member, original LPB and decoded
payload for extraction `2012.09.19.0001`, private-source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`.
The same inputs are identified by
[`scripts.json`](../manifests/scripts.json),
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`private_lua_corpus.json`](../manifests/private_lua_corpus.json).
The matched published opening route and Judge input contract are adopted at
Scripts revision `cffbad8b4090c485ad260a85f168cf341680c176`.

Canonical `judge/negotiation/negotiationjudge.lua` lines 78-107 contain the
method and assignment. Original `root/proto2` has 24 instructions, code
offset 962, twelve fixed parameters, raw vararg 0, zero upvalues and no nested
prototypes. Root PCs 13-15 obtain `NegotiationJudge`, create the closure at
PC 14 and assign `openNegotiationWidget` at PC 15. PCs and decoded-payload
offsets below are zero-based.

| Behavior | Original locator |
| --- | --- |
| One-result player call and exact-true gate | CALL PC 2, offset 970, B=2,C=2; EQ PC 3. |
| Fresh desktop/method lookup and ordered arguments | PCs 5-16. |
| Eleven arguments including D/path; one result | CALL PC 17, offset 1030, B=12,C=2. |
| Empty exact-false branch and convergence | EQ PC 19; JMP PCs 20/21 both reach PC 22. |
| Zero-value normal return | RETURN PC 22, offset 1050, B=1. |

The 24-word code range has SHA-256
`60d9d0780d7bcbf4a7cc102d2cab976297159adfe0c1977e50e5a5034e6bc241`.
`tools/retail_script.py` and `ChunkReader`/`instruction` in
`tools/build_quest_contracts.py` expose the authenticated original in memory.
A bounded check passed 30 authored cases for player first-result adjustment,
exact Boolean gating, fresh desktop lookup, nine-position padding/truncation,
receiver and value preservation, ignored opening status and zero returns.
Seven changed guard, argument, call-result and return-width controls were
rejected, and two opaque call-error paths propagated. These finite stub
models execute no helper body, native implementation or retail runtime.
