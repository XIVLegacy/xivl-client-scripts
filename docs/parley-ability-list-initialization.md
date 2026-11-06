# Parley ability-list initialization

`NegotiationAbilityListWidget.initAsk(W,F1,F2,F3,F4,F5)` forwards all five
supplied values unchanged to `abilityUseCheck` and later to five numbered
button-visibility requests. It has no local value guard or Boolean
conversion. It passes exactly the first `abilityUseCheck` result to
`abilityHelpDisp` and returns zero values after its ordered requests.

Under the selected helper bindings, the first Lua-truthy F value selects an
index 1-5. Numeric zero and an empty string qualify. Only indices 1-4 request
help text; index 5 and a missing result request none. These are static
retail 1.23b Lua contracts from extraction `2012.09.19.0001`, without a proof
of actual ability eligibility, native control state or gameplay effects.

## Supplied initializer frame

The initializer has six fixed parameters, no varargs, no captured upvalues
and no nested prototypes. W is the receiver. Missing F positions become
nil, and extra arguments are unused. All five F positions are used without
a local type test, fallback or range check. Nil, false, zero and other
values retain their supplied types and positions.

The [Ask base initializer](ask-widget-result-state.md#selected-state-and-calls)
forwards its complete variadic sequence to dynamic `initAsk`, discards its
results and returns zero values. If that dispatch resolves to this body on
the intended W, fixed-parameter adjustment applies as above. Actual
inheritance, creation delivery and selected method/frame remain conditions.
The Ask base's separate work/result writes are not operations of this body.

## Ordered initializer requests

The first operation reads `W.work` and assigns its `_temp` member a fresh
empty table. This is a direct assignment, without any declaration pairs or
explicit call to `defineWork`. It establishes no work defaults, successful
registration, storage installation or conversion.

The following requests are sequential. Each dynamically resolves its named
method on W and supplies W as the first argument. Continuation requires all
preceding operations to complete normally. Every call discards its results
except the one-result capture stated in step 2.

| Order | Request |
| ---: | --- |
| 1 | `setText(W,"TextBlock_AbilityTitle",7108)`. |
| 2 | `abilityUseCheck(W,F1,F2,F3,F4,F5)`, retaining exactly one result R. Missing results pad R with nil; extra results are discarded. |
| 3 | `abilityHelpDisp(W,R)`. This call supplies one operand after W even when R is nil. |
| 4 | Four `setText` requests in the numbered order shown below. |
| 5 | `setContent(W,"Button_CloseWindow",7109)`. |
| 6 | For n=1 through 5 in order, `setVisibility(W,"Button_AbilityCommand_"..n,Fn)`. These are five separate requests, forwarding each original F value unchanged. |
| 7 | `setModal(W,true)`. |
| 8 | Separate `setConfirmCondition(W,name)` requests for `Button_AbilityCommand_1` through `Button_AbilityCommand_5`, then `Button_CloseWindow`. |
| 9 | Separate `setControlCommandCondition(W,name,"UILuaCommands.Hover")` requests for those same six names in the same order. The command operand is a literal string. |
| 10 | `setCancelCondition(W)`, without an optional operand. |

The numbered button text requests are:

| Control | Literal request key |
| --- | ---: |
| `Button_AbilityCommand_1:TextBlock_Ability` | 7110 |
| `Button_AbilityCommand_2:TextBlock_Ability` | 7111 |
| `Button_AbilityCommand_3:TextBlock_Ability` | 7112 |
| `Button_AbilityCommand_4:TextBlock_Ability` | 7113 |

This initializer has no text request for button 5. It still makes that
button's visibility, confirm and hover requests. All five confirm and hover
requests occur regardless of F values. There is no `setEnable`, focus,
timer, show or result-setting request in this body.

The initializer makes 27 explicit calls and returns exactly zero values.
It never tests a request's returned true, false, zero or nil as a success
condition. R is used only as the help-call operand. Its capture does not
replace, convert or default any F value before the later visibility calls.

Each repeated method lookup is fresh, including repeated `setText`,
`setVisibility` and condition requests. The help method is resolved after
the check call returns, and the later text/visibility methods are resolved
after the help call returns. No one method binding is cached across these
requests. All outer method lookups use the supplied W.

## First truthy supplied value

The selected `abilityUseCheck(W,F1,F2,F3,F4,F5)` has six fixed parameters,
no varargs, no captured upvalues and no children. It tests F1 through F5
in ascending order using Lua truthiness, returning immediately on the first
truthy value. It does not access W, call a method, read a work member or
write any state.

| Supplied values | Result |
| --- | --- |
| The first truthy value is Fn | Exactly one numeric value, n. |
| All five values are nil or false | Exactly zero values. |

Numeric zero, an empty string and Boolean true are truthy. This is neither
an exact-true test nor a comparison against numeric one. Missing positions
are nil and excess positions are unused. The no-match result is not numeric
zero, false or one explicit nil. The initializer's one-result capture turns
that zero-value return into a local nil R.

The result identifies the first truthy supplied position. The method name
does not establish that its corresponding ability is owned, usable,
enabled or accepted by the client or server.

## Selected help request

The selected `abilityHelpDisp(W,S)` has two fixed parameters, no varargs,
no captured upvalues and no children. It compares S with numeric literals
1 through 5 in ascending order. For 1-4 it requests:

| Numeric S | First request | Second request |
| ---: | --- | --- |
| 1 | `setText(W,"TextBlock_AbilityHelp",7114)` | `setVisibility(W,"TextBlock_AbilityHelp",true)` |
| 2 | `setText(W,"TextBlock_AbilityHelp",7115)` | `setVisibility(W,"TextBlock_AbilityHelp",true)` |
| 3 | `setText(W,"TextBlock_AbilityHelp",7116)` | `setVisibility(W,"TextBlock_AbilityHelp",true)` |
| 4 | `setText(W,"TextBlock_AbilityHelp",7117)` | `setVisibility(W,"TextBlock_AbilityHelp",true)` |

Numeric 5 has a comparison branch but makes no request. Every other S also
makes no request. In particular, nil, false, true, zero and string `"1"`
through `"5"` do not request help. Numeric 1.0 matches numeric 1. The method
does not coerce S, substitute a default or request help clearing/hiding on
the paths without requests. Those paths do not access W, so they can return
normally with nil W. Every normal path returns exactly zero values.

On a matched request path, the text method is resolved and called first.
Only after that call returns normally does the visibility method lookup
occur. Both use the supplied W and discard every result. A false, nil or
zero text-call result does not suppress the second request.

Composing the three selected bodies requires actual matching dynamic
bindings and normally completed preceding operations. With those premises,
the initializer's first truthy F position controls its initial help key for
positions 1-4. First-truthy position 5, or all nil/false values, produces no
help text/visibility request from the selected helper. The initializer
still calls that helper and continues its other requests. The five button
visibility operands remain the original F1-F5 rather than a Boolean
projection or the selected index.

## Errors and remaining boundaries

None of these bodies catches errors. Invalid receiver/work indexing,
assignment, method lookup or a reached call error prevents subsequent
operations and normal return. A suspended or nonreturning call also blocks
continuation. Earlier completed assignments and requests are not rolled
back by these bodies. The initializer's empty `_temp` assignment precedes
every request, so a later request error does not undo it locally.

The [published Parley result boundary](parley-target-gate.md#negotiation-widget-results)
reports the parent `Button_Ability` opening request with five stored
ability values and the child's numbered button/result correspondences:
buttons 1-5 lead to local parent results 15-19 under that callback contract.
Those are adopted observations, not a new parent or callback-body study.
Actual child selection/frame delivery, stored values, method bindings,
callback delivery and state preservation remain conditions. This
initializer and its helpers produce none of those result values.

The numeric operands above are text/content request keys. No form,
provider, locale, row, label or ability identity is established here.
Visibility, modal and condition requests do not demonstrate applied native
state, actual input acceptance, focus, timer effects, eligibility, scoring,
server policy, rendered output or historical invocation.

## Source identity and original locators

The canonical member is
`lua/scripts/widget/ask/negotiationabilitylistwidget.lua`, 8,904 bytes and
408 lines, SHA-256
`38955fa9c9ccc151711ce7f038f14b662c75bd4667577088e90cb66bf9f42528`.
[scripts.json](../manifests/scripts.json) owns that pin. The containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF byte pairs with LF only.

The original beneath `client/script/` is
`n1635q/9rz/w53vq19q1vw981y1qly1rqn1635q.le.lpb`, 3,727 bytes, SHA-256
`dc365626983d6fd751f2a98b8075933fd52f442af5ba2c1ee27be07580fe2cce`.
The decoded Lua 5.1 payload is 3,714 bytes, SHA-256
`bc6e6ec2a4afdadf1b18435f9cb4aa79efa6dc4849da2aa29ac5f113dc26736a`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns those
identities. The manifests and adopted Ask/Parley publications are pinned at
repository revision `1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`.

| Method | Canonical definition/binding | Original prototype / code offset / words | Root closure/assignment PCs |
| --- | --- | --- | --- |
| `initAsk` | Lines 11-146 | `root/proto0` / 455 / 105 | 8 / 9 |
| `abilityUseCheck` | Lines 283-303 | `root/proto4` / 2775 / 25 | 20 / 21 |
| `abilityHelpDisp` | Lines 306-373 | `root/proto5` / 2960 / 55 | 23 / 24 |

Prototype indices and PCs are zero-based. Offsets exclude the LPB wrapper;
instruction PC n is at `code offset+4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Initializer work read, new empty table and `_temp` assignment | PCs 0-2. |
| Title, one-result check and help calls | CALL PCs 6, 13 and 16. PC13 has B=7,C=2; PC16 has B=3,C=1. |
| Four numbered text calls and CloseWindow content | CALL PCs 20,24,28,32 and 36. |
| Five supplied visibility calls and modal true | CALL PCs 40,44,48,52,56 and 59. |
| Six confirm calls, six hover calls and cancel | CALL PCs 62,65,68,71,74,77; 81,85,89,93,97,101; and 103. Cancel has B=2. |
| Initializer zero-value return | RETURN PC104, B=1. All calls except PC13 have C=1. |
| First-truthy helper tests and index returns | TEST PCs 0,5,10,15,20; one-value RETURN PCs 3,8,13,18,23. Zero-value fallback is RETURN PC24, B=1. |
| Help numeric comparisons | EQ PCs 1,13,25,37,49 for numeric 1-5. |
| Help text/visibility pairs and zero-value return | CALL PCs 6/10,18/22,30/34,42/46, all B=4,C=1; RETURN PC54, B=1. |

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Archive, member,
original and decoded payload identities, complete parsing and the three
selected original root bindings/prototypes were checked. Original and
canonical evaluation checked the fixed frames, empty assignment, ordered
requests, fresh lookups, result widths, nil/false/zero and error prefixes.
Finite supplied-value combinations checked first-truthy priority and its
zero-value fallback. Synthetic nested execution checked the initializer's
one-result projection into the selected help body. Rejecting controls
changed guards, sources, keys, receiver/argument/result widths, request
order and command operands. No parent, callback, other helper, native body,
form or row was interpreted, and no raw retail body, listing, payload or
complete vector was retained. No native or runtime execution was performed.
