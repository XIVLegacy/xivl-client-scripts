# Parley cancel-confirmation request

`NegotiationWidget.processUICommandCancel` requests a `CommonAskWidget` child
through the current global desktop receiver. The selected child adapter gets
the widget index from the supplied parent, then forwards the complete extra
tail to `openWidget`. Conditional on the published creation and initialization
contracts receiving the matching frame, 7124 is the question key, 2 is the
default-answer operand, and 7125 and 7126 are the two ordered answer keys.

`NegotiationWidget.processAskResult` requests base result -1 only for numeric
child result 1. These are static retail 1.23b request contracts from extraction
`2012.09.19.0001`. They establish neither an actual dialog nor an accepted
gameplay quit.

## Cancellation caller and selected receiver

Write the caller's five fixed parameters as `(W,A1,A2,A3,A4)`. It has no
varargs. Missing positions become nil, excess positions are unavailable to
this body, and A1-A4 are unused.

The body reads global `desktopWidget` as D, captures D's `openChildWidget`
function and D as receiver, and supplies exactly nine arguments:

```text
openChildWidget(D,"CommonAskWidget",W,true,nil,7124,2,7125,7126)
```

The supplied parent is W. D is the method receiver; the caller does not look
up `openChildWidget` on W. The nil before 7124 is a present argument, not an
omitted operand. Every call result is discarded and the caller returns zero
values after normal completion. Nil, false, zero, multiple results or no
results from a different opener do not select another local branch.

There is no local child-presence check, parent validation, success test,
result write, explicit wait, close or timer request. Lookup and call errors
propagate. A call that suspends or fails to return prevents the normal return.
There is no protected cleanup or rollback.

## Child adapter and complete projection

If the selected function is `DesktopWidget.openChildWidget`, its fixed frame
is `(D,N,P,F,...)`, with four fixed parameters and raw vararg flag 3. Missing
fixed positions become nil. It performs these operations in order:

1. Look up `getWidgetIndex` on P and request exactly `(P)`. Keep its first
   result I. An empty result becomes nil; extra results are discarded.
2. After that call returns, capture `openWidget` on the original D and D as
   receiver. Tailcall the captured function with exactly
   `(D,I,N,nil,P,F,...)`, preserving every position in the original extra tail.

The index receiver is P, not D. The getter can change which `D.openWidget`
function is captured next. The adapter does not reload global `desktopWidget`
after the getter, replace P with I, or look up an existing child by N.
The nil after N is a separate fixed alias-position operand.

I, N, P and F are not tested or converted locally. Nil, false and zero index
results all reach the next lookup. An empty tail contributes no extra
position. Explicit nils, entries after nil and trailing nils retain their
count and order. Every normally returned result of `openWidget` propagates,
including zero results, false and nil positions. The cancellation caller
discards that entire sequence. Errors propagate in order, so an index lookup
or call failure prevents the later opener lookup and call.

For the selected cancellation request, P=W, N=`"CommonAskWidget"`, F=true
and the tail is exactly `(nil,7124,2,7125,7126)`. Its reached request is:

```text
openWidget(D,I,"CommonAskWidget",nil,W,true,nil,7124,2,7125,7126)
```

This is eleven supplied arguments, including D. It is a request frame,
without an observed index value or actual desktop/parent identity.

## Conditional creation and initialization

The published [openWidget contract](content-director-ui-contracts.md#openwidget-inputs-and-results)
has six fixed slots. Under that actual binding, the frame above gives it
index I, path `CommonAskWidget`, nil alias, parent W, flag true and the same
five-value tail. Its type and enable checks must permit the request. For
nonnil W, its root-occupancy check is bypassed. Its reached local call is:

```text
openWidgetLocal(D,"CommonAskWidget",nil,W,I,true,nil,7124,2,7125,7126)
```

Under the published [local creator](content-director-ui-contracts.md#openwidgetlocal-creation-request),
the nil alias defaults to `"CommonAskWidget"`. With nonnil W, the parent
remains W. Let B be that helper's saved input value: it starts true, but its
conditional parent show/input queries can replace it with their first result.
If its liveness gate permits creation, it requests:

```text
commandCreateWidget(D,"CommonAskWidget",false,W,B,"CommonAskWidget",I,true,nil,7124,2,7125,7126)
```

The command helper and subsequent player adapter retain their published
[saved lookup and forwarding](content-director-ui-contracts.md#commandcreatewidget-forwarding)
and [command request](player-widget-command-request.md) conditions.
The [generic creation composition](tutorial-widget-creation-frame.md)
distinguishes source calls, native frames, converted values and delivered
initialization. It does not establish these Parley values crossing those
boundaries. Actual command/factory selection, typed frames, receiver insertion,
conversion, class selection and delivery are required independently.

To express the initializer condition without assuming value identity, suppose
the actual child resolves the published shared `_onInit` and receives:

```text
(C,P2,B2,A2,I2,F2,U2,Q2,D2,V1,V2)
```

C is the child receiver. P2 and B2 are the shared caller's second and third
fixed arguments. The eight-value variadic sequence begins at A2. These are
delivered values, not assertions of equality with W, B, the alias, index,
flag or original tail. Under the published
[shared initialization contract](tutorial-form-name-selection.md#incoming-initialization-frame),
the selected `initCommon` returning its ordinary first result 4, ordinary
`select`, and the saved `init` resolving to CommonAsk's initializer, the call
is exactly:

```text
init(C,U2,Q2,D2,V1,V2)
```

Thus if the delivered tail preserves the corresponding requested values,
U2=nil, Q2=7124, D2=2, V1=7125 and V2=7126. The
[CommonAsk initializer](common-ask-text-request.md#original-initializer-contract)
then receives `(C,nil,7124,2,7125,7126)`. Its unused P position is nil,
question Q is 7124, default D is 2, and its complete answer tail has exactly
two entries. It requests `askDefaultAnswer=2`; its nil-only fallback to 1
does not apply. This positional result assigns no mode meaning to 2.

Under the separately selected
[answer-list helper](common-ask-answer-list.md#selected-helper-contract),
those two entries request count 2 and the ordered `Content` writes for
`Item_Answers1` / `TemplateButton_Answer` with key 7125, then
`Item_Answers2` / `TemplateButton_Answer` with key 7126. Their numeric named
property route retains that publication's native frame, context, part,
provider, schema and locale conditions. No localized row, wording, rendered
choice, actual default focus or selected answer follows from these requests.

## Child result and confirmed-cancel continuation

The [published CommonAsk callback](confirm-prompt-client-contracts.md#answers-and-command-submission)
maps numbered answer items to numeric results and UI cancel to 0, invokes the
parent's `processAskResult` through `setAskResult`, and requests closure.
Applying it requires the actual CommonAsk binding, delivered UI event and
parent resolution. The opening request alone does not identify that parent
with the original W or demonstrate callback delivery.

For `NegotiationWidget.processAskResult`, write the two fixed arguments as
`(R,X)`. Missing X becomes nil and excess arguments are unavailable. It
compares X with numeric 1 using Lua equality. Only equality requests
`setBaseAskResult(R,-1)`, discarding all results. Every normal path returns
zero values. Numeric 1.0 also compares equal to 1; nil, false, true, zero,
2, -1 and string `"1"` do not. A nonmatching result performs no receiver
lookup in this body. It neither clears nor replaces an earlier result.

If CommonAsk's first answer callback actually reaches this function on the
intended parent, it therefore requests -1. Answer 2 and UI cancel 0 request
no base-result change through this callback. This does not prove that their
dialog remains open, that an earlier parent result was zero, or that no other
callback or writer acts.

Under the selected [base-result contract](ask-widget-result-state.md#selected-state-and-calls),
the -1 request first requests input disablement only when the read flag is
exactly true, then assigns -1 after normal call completion. A later read of
that stored -1 would make the published zero-comparison poll return true.
Storage, readback, same-instance identity and actual method bindings remain
conditions. This callback has no local close, timer or gameplay request, and
a finished poll is separate from authoritative cancellation or settlement.

## Original sources and verification

[scripts.json](../manifests/scripts.json) owns canonical identities and
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns original
resource and decoded-payload identities. The containing archive is pinned by
[private_lua_corpus.json](../manifests/private_lua_corpus.json), private-source
revision `40006d5d716583d78690a6f3ef50ca1bc41dddee`, 14,385,427 bytes and SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical parent | `lua/scripts/widget/ask/negotiationwidget.lua`, 2110 lines | 48254 | `68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3` |
| Original parent LPB under `client/script/` | `n1635q/9rz/w53vq19q1vwn1635q.le.lpb` | 15618 | `dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1` |
| Parent decoded payload | XOR-0x73 Lua 5.1 chunk | 15605 | `33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd` |
| Canonical connector | `lua/scripts/widget/desktopwidget_connector.lua`, 26564 lines | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| Original connector LPB under `client/script/` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` |
| Connector decoded payload | XOR-0x73 Lua 5.1 chunk | 213474 | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |

Canonical identity uses the [published LF convention](../lua/README.md#canonical-form).
PCs and prototype indices below are zero-based. Offsets are decoded-payload
bytes, excluding the LPB wrapper. All three prototypes have zero upvalues
and no child prototypes.

| Method | Canonical definition/binding | Root closure/assignment PCs | Prototype / start / words / fixed / raw vararg |
| --- | --- | --- | --- |
| `NegotiationWidget.processUICommandCancel` | 784-800 | 17/18 | `root/proto3` / 5900 / 12 / 5 / 0 |
| `NegotiationWidget.processAskResult` | 2100-2110 | 44/45 | `root/proto12` / 15509 / 6 / 2 / 0 |
| `DesktopWidget.openChildWidget` | 25631-25647; name literal 25629 | 1891/1892 | `root/proto536` / 207429 / 12 / 4 / 3 |

| Consequential operation | Original locator |
| --- | --- |
| Cancel desktop capture and opener call | GETGLOBAL PC0; SELF PC1; CALL PC10, offset 5940, B=10,C=1; RETURN PC11, B=1. |
| Child-result comparison and setter | EQ PC0, offset 15509, X/numeric 1; SELF PC2; CALL PC4, offset 15525, B=3,C=1; RETURN PC5, B=1. |
| Parent index request | SELF PC0 on fixed P; CALL PC1, offset 207433, B=2,C=2. |
| Desktop opener capture and complete tail | SELF PC2; VARARG PC8, B=0; TAILCALL PC9, offset 207465, B=0,C=0; open RETURN PC10, B=0. |

The canonical desktop body displays ellipsis through one local and supplies
that local once. This loses multi-value tails and supplies one nil for an
empty tail. Original open `VARARG`/`TAILCALL` operands govern the complete-tail
contract above. No such qualification is needed for the two parent bodies.

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`, with complete payload
consumption and root owner/key/closure checks. In-memory replay checks the
original operations against authored request expectations, exact numeric
comparison, missing operands, nil/false/zero values, first-result adjustment,
full tails, returned results, late opener replacement and propagated failures.
Canonical evaluation checks both parent bodies and the desktop body with the
explicit tail-display qualification; separate checks retain its unqualified
empty/multiple-tail discrepancy. Changed literals, receivers, argument sources,
comparison polarity, call/tail widths and return widths are rejected.
Authored positional checks validate only the conditional published-contract
composition. They execute no creation helper, native body or client.

The linked publications and source manifests are adopted at Scripts revision
`994d6a356f2de4cac8756040bdca78cf007da6ec`. No further helper body, raw form,
template, localized row or native implementation was interpreted. Actual
class/binding/frame selection, delivery and conversion, storage and readback,
focus, timer effects, rendered state and server acceptance remain unproved.
