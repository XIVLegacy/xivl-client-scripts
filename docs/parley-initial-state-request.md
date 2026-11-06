# Parley initializer requests

`NegotiationWidget.initAsk` directly assigns its fourth supplied value to
`work.time`, its fifth through ninth values to `work.ability1` through
`work.ability5`, and numeric 1 to `work.select`. It requests temporary work
declarations and an ordered series of UI operations. It supplies no explicit
initial values for `work.selected1` through `work.selected6` and no fixed
duration for `work.time`.

This is static retail 1.23b evidence from extraction `2012.09.19.0001`.
Assignments and method requests establish local intent. Applied native work,
control state, rendering and actual initialization require their own bindings
and runtime conditions.

## Supplied initializer frame

Write the ten fixed parameters as `initAsk(W,A1,A2,A3,A4,A5,A6,A7,A8,A9)`.
There are no varargs, captured upvalues or nested prototypes. Omitted fixed
positions become nil, and excess positions are unavailable to this body.
All nine supplied values are used without a local type test, conversion,
fallback or range check, preserving nil, false and zero as supplied.

| Supplied position after W | Selected use |
| --- | --- |
| A1, A2, A3 | Final three operands of `initChildWidget(W,"NegotiationMessageWidget",true,A1,A2,A3)`. |
| A4 | Direct assignment to a freshly read `W.work` object's `time` member. |
| A5-A9 | Direct assignments, in order, to `ability1` through `ability5`, freshly reading `W.work` for each assignment. |

These initializer positions are distinct from the three values sent to
`setAskParameter` by the [selected Judge input route](parley-input-result-route.md#conditional-selector-ask-and-callback-composition).
That route does not supply this initializer's frame. The
[Ask base initializer](ask-widget-result-state.md#selected-state-and-calls)
forwards its complete variadic sequence to dynamic `initAsk`, discards the
results and returns zero values. If it resolves to this fixed-parameter
implementation, the frame adjusts as above. Actual creation delivery, receiver
identity and selected overrides remain conditions.

## Work declaration and direct assignments

The first operation reads `W.work` and assigns its `_temp` member an ordered
table of 49 declaration pairs. Each pair has exactly a name and type string,
without a third default-value operand. The aggregate types are 12
`integer16`, 18 `integer24`, 14 `integer8` and five `boolean` declarations.
The selected fields used by the published Parley flow are:

| Field | Requested type | Explicit initializer assignment |
| --- | --- | --- |
| `select` | `integer8` | Numeric 1, after the five ability assignments. |
| `selected1` through `selected6` | `integer24` each | None. |
| `time` | `integer8` | A4, after the tile and ability disable requests. |
| `ability1` through `ability5` | `boolean` each | A5 through A9 respectively. |

This is an assignment to `_temp`, not an explicit call to `defineWork` in
this body. The declaration does not by itself establish field defaults,
storage allocation, conversion, successful registration or later readback.
The [Ask work and binder qualifications](ask-widget-result-state.md#selected-state-and-calls)
remain applicable to conditional use of its work/result contracts. In
particular, this page does not turn an omitted explicit initialization of a
selected field into an observed numeric zero.

The five ability writes, `select=1`, and later `time=A4` each read `W.work`
again. A called helper can change that property before a later write. The
body does not retain one work object across the entire sequence or take an
atomic snapshot. A4 is the local source of the time write, not evidence of
its domain, units, accepted storage value or authoritative duration.

## Ordered control requests

Every call below dynamically looks up the named method on W and supplies W
as its first argument. Every reached call discards all results. The sequence
continues after a normally returned false, nil or zero, without testing it.
For each numbered group, ascending numeric order is part of the request order.

| Order | Requests after the declaration assignment |
| --- | --- |
| 1 | For i=1 through 12, request `setVisibility(W,"Button_ItemIcon_"..i..":IconControl_ItemIcon",false)`, then `setVisibility(W,"Button_ItemIcon_"..i..":TextBlock_NumberOfTopics",false)`. |
| 2 | Request `setText(W,"TextBlock_TopicItem","")`, then hide `TextBlock_TopicItem` and `IconControl_TopicItem`, in that order, using `setVisibility` with false. |
| 3 | For i=1 through 6, request `setVisibility(W,"Label_SelectedItem_"..i..":IconControl_SelectedItemIcon",false)`. Then hide `IconControl_Addition_1`, `_2` and `_3`, in order, using `setVisibility` with false. |
| 4 | Assign A5-A9 to the five ability fields and assign `select=1`. |
| 5 | For i=1 through 12, request `setEnable(W,"Button_ItemIcon_"..i,false)`. Then request `setEnable(W,"Button_Ability",false)`. |
| 6 | Assign `time=A4`. Request `setVisibility(W,"Border_ArrowIconLeft",true)`, then `setVisibility(W,"Border_ArrowIconRight",false)`, then `setContent(W,"Button_Ability",7107)`. |
| 7 | Request `initChildWidget(W,"NegotiationMessageWidget",true,A1,A2,A3)`, then `setModal(W,true)`. |
| 8 | Request `setConfirmCondition(W,name)` separately for `Button_ItemIcon_1` through `Button_ItemIcon_12`, then `Button_Ability`. |
| 9 | Request `setControlCommandCondition(W,name,"UILuaCommands.Hover")` separately for the same thirteen names in the same order. The command operand is a literal string. |
| 10 | Request `setUICommandCondition(W,"UILuaCommands.TimerOver")`, `setCancelCondition(W)`, `show(W)`, and `setInputEnable(W,false)`, in that order. The timer command operand is also a literal string. |

The first visibility group, selected-icon group and tile-disable group are
numeric loops with respective bounds 1-12, 1-6 and 1-12, all with step 1.
The thirteen confirm requests and thirteen hover requests are separate calls.
There is no input-dependent branch or early normal return. No optional
operand follows W in `setCancelCondition` or `show`; omitted arguments must
not be replaced with explicit true or false in these request frames.

Each method property is looked up afresh before its arguments are prepared
and its call is reached. The body does not cache one method across a loop or
across repeated requests. No result is used as a success gate. After the
final input-disable call returns normally, `initAsk` returns exactly zero
values. Lookup, concatenation, assignment or call errors are not caught, and
a suspended or nonreturning call does not produce a normal return. Earlier
requests are not rolled back by a later error.

The [published Parley update and callback contracts](parley-target-gate.md#negotiation-widget-boundary)
own later reads of `work.time`, selection changes, tile/ability results and
timer-command requests. Their composition requires the same instance,
matching dynamic bindings, applied storage and preserved values until each
fresh read. An initial assignment is not proof of a later read's value.
This initializer does not establish ability or actor identities, timer
behavior, scoring, accepted outcomes, server consumption or historical
invocation. A field name, declared width or control request supplies no such
authority.

## Source identity and original locators

The canonical member is `lua/scripts/widget/ask/negotiationwidget.lua`,
48,254 bytes and 2,110 lines, SHA-256
`68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3`.
[scripts.json](../manifests/scripts.json) owns this pin. Its containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF byte pairs with LF only.

The original beneath `client/script/` is
`n1635q/9rz/w53vq19q1vwn1635q.le.lpb`, 15,618 bytes, SHA-256
`dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1`.
The XOR-0x73 decoded Lua 5.1 payload is 15,605 bytes, SHA-256
`33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns these
pins. The manifests and adopted publication versions are pinned at repository
revision `e276b5cd03642ac32e368aca53532c80c44f2e60`.

Canonical lines 11-566 contain the selected function and binding. The
original root closure PC8 and assignment PC9 bind `NegotiationWidget.initAsk`
to `root/proto0`: code offset 681, 409 instructions, ten fixed parameters,
raw vararg flag 0, zero upvalues and no nested prototypes. Prototype indices
and PCs are zero-based. Offsets exclude the wrapper; PC n is at `681+4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Declaration table construction and `_temp` assignment | PCs 0-199; assignment PC199. |
| Tile visibility loop | FORPREP PC204, calls PC211/218, FORLOOP PC219. |
| Empty topic text and topic visibility | Calls PC223/227/231. |
| Selected-icon loop and addition visibility | FORPREP PC235, call PC242, FORLOOP PC243; calls PC247/251/255. |
| Five ability writes and `select=1` | Assignments PC257/259/261/263/265 and PC267. |
| Tile-disable loop and ability disable | FORPREP PC271, call PC277, FORLOOP PC278; call PC282. |
| `time=A4`, arrows and content | Assignment PC284; calls PC288/292/296. |
| Child frame and modal request | CALL PC303 B=7,C=1; PC306 B=3,C=1. |
| Confirm and hover requests | Calls PC309-345 at step 3, then PC349-397 at step 4. |
| Timer condition, cancel, show and input disable | Calls PC400/402/404/407, B=3/2/2/3 respectively, all C=1. |
| Zero-value normal return | RETURN PC408 B=1. |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Authenticate the
archive, member, original and payload, parse to complete consumption, and
check the selected root binding and prototype. In-memory canonical agreement
and focused supplied-value, discarded-result, fixed-loop and rejecting
instruction controls check the declaration shape, exact frames, lookup order,
direct writes and return width. They execute neither the retail client nor
any requested helper body and retain no source body or instruction listing.
