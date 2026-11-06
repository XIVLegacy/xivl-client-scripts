# Parley input and result route

`NegotiationJudge.inputNegotiationWidget` returns exactly one value. An
exactly-true player test selects `Ask/NegotiationWidget` and returns the
selection helper's second result. Every other normally returned player-test
value returns numeric zero. Desktop selection failure instead becomes nil:
the caller tests the status but makes no replacement assignment.

This is static retail 1.23b evidence from extraction `2012.09.19.0001`.
It establishes the selected caller and conditionally composes published helper
and callback contracts. It does not establish a turn outcome or server action.

The [separate opener](parley-opening-request.md) owns opening and its requested
initializer tail. The [parameter contract](parley-parameter-request.md) owns
the selected three-value parameter method.

## Supplied frame and result adjustment

Write the six fixed parameters as
`inputNegotiationWidget(self,A1,A2,A3,A4,A5)`. There are no varargs or captured
upvalues. `self` and A2 are unused. A1 supplies the receiver and sole argument
of dynamic `isPlayer()`. Only its first result is retained, with nil padding
for no results. Only Boolean true passes the test. False, nil, numeric zero,
numeric one and other non-true values take the nonplayer path.

The passing path resolves the global `desktopWidget` as D and requests:

```text
selectEventModeWidgetYield(D,"Ask/NegotiationWidget",A3,A4,A5)
```

D is both the method lookup receiver and its first supplied argument. The
actor and Judge receiver are not forwarded. A3, A4 and A5 retain their supplied
values and order, including nil, false and zero. The caller gives them no
local type check, default or gameplay meaning.

Exactly two helper results are retained as status S and value R. Missing
results become nil, and extras are discarded. The caller returns exactly R,
including nil, false, zero or a negative value. Its later `S == false` test
has empty branches: neither status changes R nor is status returned.

| Normal path | Helper adjustment | Caller result |
| --- | --- | --- |
| Player test not exactly true | No desktop call | One numeric 0 |
| Desktop returns only false | S=false, R=nil | One nil |
| Desktop returns true and R | Retains the first two values | One R |
| Substituted helper returns false, R | Retains false and R unchanged | One R |
| Substituted helper returns no values | S=nil, R=nil | One nil |

The pinned generic helper supplies Boolean status on normal completion. The
substituted-helper rows explain this caller's exact adjustment, rather than
claiming those are nominal generic-helper paths. Lookup or call errors do
not become zero or nil results; the selected method has no error handler.
A suspended or nonreturning reached call does not produce a normal return.

## Conditional selector, Ask and callback composition

The following publications own the adopted contracts:

- [ShopSell initialization and result flow](shop-sell-selection-flow.md#opening-and-rearming)
  and [the full generic getter tail](shop-sell-selection-flow.md#four-widget-results-to-five-caller-results).
- [ShopBuy original helper widths](shop-buy-selection-contract.md#original-bytecode-locators).
- [Fishing wait and result widths](fishing-input-flow-contract.md#wait-result-width-and-cleanup).
- [Ask state, setters, getters and completion](ask-widget-result-state.md#selected-state-and-calls).
- [Parley callback results](parley-target-gate.md#negotiation-widget-results).

Under those actual dynamic bindings, event initialization obtains
`getWidget(D,4,"Ask/NegotiationWidget")`. A nil first widget result skips the
initialization calls and yields selection failure. For a nonnil W it requests,
in order, `resetBaseAskResult(W)`, `setAskParameter(W,A3,A4,A5)` and
`show(W,true,true)`, discards their results and returns W. The supplied tail
therefore belongs to `setAskParameter`, not widget creation or `initAsk`.
A normally returned false parameter-helper result does not itself reject W.
The selected Judge method contains no creation or close request.

Selection then calls `selectWidgetYield(D,W)` with its optional show operand
omitted. That path skips its child-show branch and calls
`selectWidgetTimerYield(D,W,nil)`, keeping only its first result. With no
timeout, the timer helper rejects an exactly-false alive result and otherwise
polls for an exactly-true `processWaitCallFunction()` result, requesting
`_wait(0.1)` between incomplete polls. That literal wait operand is not a
Parley timer duration.

A nil initialized W or exactly-false selection result makes the generic
wrapper return one false without reading widget results. Otherwise it returns
literal true followed by the complete open sequence from dynamic
`W:getAskResult()`. The Judge's two-result request keeps only the first getter
value as R. It does not truncate the getter within the generic helper. A
zero-value getter produces caller nil, while a multiple-value getter loses
all but its first value at the Judge boundary.

If that getter resolves to the published Ask base getter and its dynamic
base-result getter resolves as described, the getter contributes one current
`askWork.askResult` read. The published base initialization declares an
`integer16` result and requests zero. The resetter requests zero after its
conditional input-enable request; setter and resetter test the input-control
flag for exact true. The inherited completion predicate finishes for any
read differing from numeric zero, including -1 and nil. A finished poll is
not an acceptance Boolean. The Ask publication owns the conditional native
no-storage case; it does not prove that this selected instance reaches the
wait without storage.

The published Parley callbacks request these local base results:

| Delivered callback path | Requested result |
| --- | --- |
| Tile buttons 1-12 | 1-12 |
| `UILuaCommands.TimerOver` | 13 |
| Ability-child buttons 1-5 | 15-19 on the parent |
| Cancel confirmation child result exactly 1 | -1 |

Cancel first opens a confirmation child; the Cancel command alone does not
supply -1. Ability selection has its published ability-check and child-open
conditions. With the described setter/getter/predicate bindings, the same
widget or parent instance, applied storage, preserved values and later
matching readback, those requested scalars can become the Judge's one result.
They remain separate from desktop failure nil and nonplayer zero. Later work
reads are fresh; a callback request does not establish an atomic snapshot or
native storage effect.

Actual receiver identity, initialization, overrides, native storage, callback
delivery and intervening writes remain conditions. This caller contains no
scoring rule, ability identity, timer-duration inference, Man300 target or
policy, accepted gameplay outcome, subsequent caller or server consumption.
Completion does not close the widget; any closure requires a separate route.

## Source identity and original locators

The selected canonical member is
`lua/scripts/judge/negotiation/negotiationjudge.lua`, 4,512 bytes and 198 lines,
SHA-256 `a617909b7f43c849d11231033dd2714cfbc7b0a33e2e0bc9e03d2a0eef92c0c5`.
Its identity is recorded in [scripts.json](../manifests/scripts.json).
The in-memory archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

The original under `client/script/` is
`0p635/w53vq19q1vw/w53vq19q1vw0p635.le.lpb`, 1,907 bytes, SHA-256
`90823b625d2a41ee5d16b6d55aa9b85f03c178c91c8e9517155d713432c672a9`.
Its decoded payload is 1,894 bytes, SHA-256
`184d55b038ab4e5089af58ecd9037844a39d45b9b28ca01aa7d63fa8168d6ada`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns both pins.
The source manifests and adopted publication versions are pinned at repository
revision `03a4a99f28d79d1a73c28dc57b219a11f778e3d8`.

Canonical lines 110-135 contain the selected function and assignment.
The original root binds `NegotiationJudge.inputNegotiationWidget` through
closure PC17 and assignment PC18 to `root/proto3`, code offset 1192,
20 instructions, six fixed parameters, raw vararg 0, zero upvalues and no
nested prototypes. Prototype indices and PCs are zero-based. Offsets exclude
the wrapper; instruction PC n is at `1192 + 4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Default result numeric zero | PC1 |
| A1 player request and exact-true gate | CALL PC3 B=2,C=2; EQ PC4 |
| Generic selector lookup | SELF PC7, payload offset 1220; canonical line 120 |
| D, path, A3, A4, A5 request; two-result capture | CALL PC12 B=6,C=3, payload offset 1240 |
| Empty exact-false status branch | EQ PC15; JMP PCs 16-17 both reach PC18 |
| Exactly one result | RETURN PC18 B=2 |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Authenticate the
archive, member, original and decoded payload, parse to complete consumption,
then check the selected prototype, root binding and canonical agreement in
memory. Focused synthetic supplied-result cases and rejecting instruction
mutations distinguish the strict player gate, receivers, supplied argument
order, two-slot capture, unchanged failure result and one-value return. These
checks execute neither the retail client nor any helper body.
