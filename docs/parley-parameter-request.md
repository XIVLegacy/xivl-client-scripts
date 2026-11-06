# Parley parameter requests

`NegotiationWidget.setAskParameter(W,P1,P2,P3)` has three distinct paths.
Exactly-true P3 requests `UILuaCommands.ResumeLimitTimer` and returns.
Otherwise exactly-true P2 returns without a request. The remaining path
uses P1 only in a conditional child-text conversion, then makes the timer,
button, topic and focus requests below. Every normal path returns zero values.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
The method contains no direct field, global or upvalue write. In particular,
it assigns neither `work.time`, `work.select` nor the Ask result. A property
or helper call is a request to its actual resolved implementation, rather
than evidence that storage, timer state, visibility or focus changed.

## Supplied values and guards

The original has four fixed parameters, no varargs and no captured upvalues.
W is the method receiver. Missing supplied positions become nil and extra
arguments are unused. P1, P2 and P3 have no local type validation or fallback.
The Boolean comparisons are exact: nil, false, numeric zero, numeric one and
other non-true values do not pass them.

The [selected Judge and generic initializer](parley-input-result-route.md#conditional-selector-ask-and-callback-composition)
conditionally forward the Judge's A3, A4 and A5 to P1, P2 and P3 respectively.
That initializer requests the base result reset before this method and show
after it, discarding this method's results. Those surrounding requests belong
to the initializer rather than this body.

| Ordered guard | Reached behavior |
| --- | --- |
| P3 equals Boolean true | Requests `W:_sendStoryboardCommand(nil,"ProgressBar_TimeGauge","UILuaCommands.ResumeLimitTimer")`, discards all results, then returns. P2 and P1 are not consumed. |
| P3 did not pass; P2 equals Boolean true | Returns without any method/global lookup or request. P1 is unused. |
| Neither guard passed | Continues through the ordinary requests below. |

The resume path takes priority when P2 and P3 are both true. The local
scratch slots initially contain one false and four numeric zeros. They do
not default supplied values or work fields. Reached calls replace their
respective result slots, including nil padding when results are absent.

## Ordinary request order

The following requests are sequential and conditional on all preceding
reached operations returning normally. Colons below include the named
receiver as the first argument. All method results are discarded except
where a retained width is stated.

| Order | Request or local adaptation |
| ---: | --- |
| 1 | `W:getChildWidgetByWindowName("NegotiationMessageWidget")`, retaining exactly one result C. |
| 2 | Only when C differs from nil, resolve global `tostring` and call it with exactly P1, retaining one result T. Then request `C:setText("TextBlock_RemainderTurn",T)`. The guard is a nil comparison, so false is not a skip value. No conversion or child text lookup is reached for nil C. |
| 3 | Request `W:_setProperty(nil,"ProgressBar_TimeGauge","Maximum",M)`, where M is a fresh `W.work.time` read. |
| 4 | Request `W:_setProperty(nil,"ProgressBar_TimeGauge","Value",V)`, where V is another fresh `W.work.time` read. M and V need not agree. |
| 5 | Request `W:_sendStoryboardCommand(nil,"ProgressBar_TimeGauge","UILuaCommands.StartLimitTimer")`. |
| 6 | For numeric indices 1 through 12, in ascending order, request `W:setEnable("Button_ItemIcon_" .. index,true)`. |
| 7 | Request `W:abilityCheck()`, retaining one result. Only Boolean true requests `W:setEnable("Button_Ability",true)`. Other results produce no ability-button request here. |
| 8 | Request `W:negotiationWidgetGetData(S)`, with S a fresh `W.work.select` read, retaining exactly three results R1, R2 and R3. |
| 9 | Request `W:setText("TextBlock_TopicItem",7103,R1)`, then `W:setVisibility("TextBlock_TopicItem",true)`, `W:setIcon("IconControl_TopicItem",R2)` and `W:setVisibility("IconControl_TopicItem",true)`. R3 is unused. |
| 10 | Resolve global `desktopWidget` as D and request `D:checkKeyboardFocused(W)`, retaining one result F. If F is Lua-truthy, request `W:setKeyboardFocusedControl("Button_ItemIcon_" .. Q)`, with Q another fresh `W.work.select` read. |

P1 is passed unchanged to the dynamic `tostring` target. The method does not
itself establish a string result or a turn-count domain. Standard Lua string
conversion requires the actual standard binding. The literal 7103, control
names and helper names do not identify a text provider, item, ability or actor.
R1 and R2 are passed unchanged, including nil or false. A missing helper
result becomes nil, and results after R3 are discarded. The earlier local
zeros do not replace missing results.

The final focus guard uses Lua truthiness, unlike the exact-true ability
guard: nil and false skip the focus request, while zero is truthy. The
focus-name expression uses Lua concatenation directly. It does not call
`tostring` on Q, validate Q against 1-12, or reuse S. A failed concatenation
or any other reached error propagates.

Method and property lookups occur when reached. In particular, the child
`setText` lookup follows the conversion call. Each property request resolves
its method before reading `W.work.time`. The get-data and final focus methods
are resolved before their respective `W.work.select` reads. Each loop
iteration resolves `setEnable` again. No helper return freezes later work
reads or proves that those reads refer to unchanged storage.

The method has no error handler. A lookup, concatenation or call error does
not become a false result or a zero-value success. A suspended or nonreturning
call prevents the following requests and normal return.

## Related state and remaining boundaries

The [Parley callback and update contracts](parley-target-gate.md#negotiation-widget-boundary)
own other writes and result producers. Their `work.time` and `work.select`
references do not make either field an input assignment in this method.
The [Ask state contract](ask-widget-result-state.md#selected-state-and-calls)
owns result resetting, storage conditions and completion polling. None of
those base operations is called by this selected method.

Actual bindings, helper bodies, work declarations and native storage remain
separate. The command names alone establish no elapsed-time behavior or
authoritative duration. This method supplies no scoring rule, valid input
domain, ability identity, accepted result, Man300 policy or historical
invocation. The requests do not demonstrate rendered output or gameplay
effects.

## Source identity and original locators

The canonical member is `lua/scripts/widget/ask/negotiationwidget.lua`,
48,254 bytes and 2,110 lines, SHA-256
`68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3`.
[scripts.json](../manifests/scripts.json) owns that pin.
The containing archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

The original under `client/script/` is
`n1635q/9rz/w53vq19q1vwn1635q.le.lpb`, 15,618 bytes, SHA-256
`dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1`.
The decoded payload is 15,605 bytes, SHA-256
`33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns those
identities. The source manifests are pinned at repository revision
`c85f5af0ac6bf0e7e0a71f96b6f168a85fd8de45`. The related Judge, Ask and
Parley publications are pinned at `e276b5cd03642ac32e368aca53532c80c44f2e60`.

Canonical lines 1020-1144 contain the function and binding. The root binds
`NegotiationWidget.setAskParameter` through closure PC26 and assignment
PC27 to `root/proto6`, code offset 7748, 105 instructions, zero upvalues and
no nested prototypes. Prototype indices and PCs are zero-based. Offsets
exclude the LPB wrapper; instruction PC n is at `7748 + 4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Scratch defaults | PCs 0-4 |
| P3 exact-true test; resume request and zero-result return | EQ PC5; CALL PC11 B=5,C=1; RETURN PC12 B=1 |
| P2 exact-true test and zero-result return | EQ PC13; RETURN PC15 B=1 |
| Child read, nil guard, conversion and child text | CALL PC18 B=3,C=2; EQ PC20; CALL PC24 B=2,C=2; CALL PC28 B=4,C=1 |
| Fresh time reads and property requests | GETTABLE PCs 34-35 and 41-42; CALL PCs 36/43 B=6,C=1 |
| Start request | CALL PC48 B=5,C=1 |
| Twelve-button loop | Bounds PCs 49-51; FORPREP PC52; CALL PC58 B=4,C=1; FORLOOP PC59 |
| Ability request and exact-true branch | CALL PC61 B=2,C=2; EQ PC62; CALL PC67 B=4,C=1 |
| Fresh selected-data read and three-result request | GETTABLE PCs 69-70; CALL PC71 B=3,C=4 |
| Topic text, visibility, icon, visibility | CALL PC79 B=5,C=1; PCs 83/87/91 B=4,C=1 |
| Desktop focus check and truthy branch | CALL PC95 B=3,C=2; TEST PC96 C=0 |
| Fresh focus index, concatenation, focus request and return | GETTABLE PCs 100-101; CONCAT PC102; CALL PC103 B=3,C=1; RETURN PC104 B=1 |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Authenticate the
archive, member, original and decoded payload, parse to complete consumption,
then check the selected root binding and original/canonical agreement in
memory. Focused synthetic traces distinguish priority, exact Boolean versus
truthy guards, nil-child handling, supplied-value preservation, fresh reads,
loop bounds, request frames, result padding/truncation and propagated errors.
Rejecting operand controls guard those distinctions without executing a
helper body or the retail client. Retain only identities and assertions.
