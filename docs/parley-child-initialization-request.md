# Parley child initialization request

`WidgetBaseClass.initChildWidget` requests one `getWidgetIndex` result from its
receiver, then forwards that value, its child-name operand, the original
receiver, its flag operand and its complete variadic tail to
`desktopWidget.openInitialChildWidget`. It tests none of those values,
discards all opener results and returns zero values.

This is a static retail 1.23b contract from extraction `2012.09.19.0001`.
The helper establishes a request frame, without establishing the selected
child class, created object, applied initialization or rendered state.

## Incoming frame and ordered calls

Write the helper frame as `initChildWidget(W,N,F,...)`. The original has three
fixed parameters and raw vararg flag 3. Missing fixed positions become nil.
The variadic tail starts after F. An empty tail remains empty. Explicit nils,
values after nil and trailing nils retain their positions and count.

| Operand | Use in this helper |
| --- | --- |
| W | Receiver of the widget-index request, then a separate original-receiver operand of the opener request. |
| N | Child-name operand passed unchanged to the opener. |
| F | Flag-position operand passed unchanged to the opener. |
| `...` | Entire extra-argument sequence appended after F. |

There is no local type check, nil guard, default, conversion, range test or
comparison with true. False and numeric zero are forwarded as supplied. The
flag's position does not establish that it requests native creation, enables
initialization or reports success.

The reached operations are ordered as follows:

1. Look up `getWidgetIndex` on W and call the selected function with exactly
   W as its only argument. Request exactly one result, I. No result becomes
   one nil value, and excess results are discarded.
2. Read global `desktopWidget` as D after the index call returns. Look up
   `openInitialChildWidget` on D and request
   `openInitialChildWidget(D,I,N,W,F,...)`. This call has five fixed arguments
   before the open tail, including D. It discards every result.
3. Return exactly zero values.

I is not tested. Nil, false and zero results follow the same next request.
The helper does not look up a child by N, inspect F or unpack a table tail.
The global read is fresh after the first call, so that call can affect which
D or opener property is subsequently selected. Each selected function is
obtained before its call. No callee body is needed to establish this adapter
frame.

Lookup or call errors propagate. The subsequent continuation requires the
reached call to return normally. A normally returned nil, false or zero from
the opener is discarded without a success test. There is no
rollback of an earlier request.

## Conditional Parley composition

The [Parley initializer](parley-initial-state-request.md#ordered-control-requests)
requests `initChildWidget(W,"NegotiationMessageWidget",true,A1,A2,A3)` and
discards all results. If that lookup resolves to this common implementation
on the same W, its reached opener request is exactly
`openInitialChildWidget(D,I,"NegotiationMessageWidget",W,true,A1,A2,A3)`.
A1-A3 remain three supplied positions, including any nils. They are not
expanded from a collection or reduced to a nonnil prefix.

I is the first result of the fresh `getWidgetIndex(W)` request. Neither this
composition nor the parent publication supplies the index getter's binding
or semantics. The supplied true remains an untested flag-position value.
Normal helper return lets the parent continue to its next modal request,
without observing a child object or a success result from this helper.

## Desktop continuation and module-path discriminator

If the selected desktop method is the connector's
`DesktopWidget.openInitialChildWidget`, its frame is `(D,I,N,W,F,...)`:
five fixed parameters and the complete tail after F. Omitted fixed operands
become nil. Its only comparison is between literal nil and literal true.
They are unequal, so the early zero-value return is not reached. This test
does not read F or any other supplied value.

The reached path looks up `createWidget` on D and calls
`createWidget(D,N,W,N,I,F,...)`. N is supplied twice: once as the second
fixed argument and again as the first member of the tail received by the
published generic creator. I and F follow that second N, then the entire
incoming tail. There is no input-dependent guard, local conversion, success
test or retained result. Every normally returned result is discarded, and
the desktop helper returns exactly zero values. Lookup or call errors
propagate, without a later normal return or rollback.

For the Parley request, the composed call is therefore
`createWidget(D,"NegotiationMessageWidget",W,"NegotiationMessageWidget",I,true,A1,A2,A3)`.
Applying the published
[generic createWidget contract](tutorial-widget-opening-contract.md#static-module-and-creation-relationships)
requires that dynamic lookup to select its `DesktopWidget.createWidget`
implementation. Its path is `"NegotiationMessageWidget"`, its third fixed
operand is W, and its complete variadic tail is
`("NegotiationMessageWidget",I,true,A1,A2,A3)`.

Under that binding and normal prerequisite returns, the creator requests
`require("/Widget/NegotiationMessageWidget")`, then
`_createActor(nil,"NegotiationMessageWidget",false,W,true,"NegotiationMessageWidget",I,true,A1,A2,A3)`.
These are positional request values, without inferred parent/index/flag or
initializer meanings at the native boundary. The generic creator returns
only its first factory result; the desktop child helper discards it.

The manifest contains both `widget/ask/negotiationmessagewidget.lua` and
`widget/negotiationmessagewidget.lua`. The conditional require request is
unprefixed: it does not request `/Widget/Ask/NegotiationMessageWidget`.
This distinguishes module paths even though the factory basename is the
same. Actual require resolution, factory binding, created runtime class and
initialization delivery remain separate conditions. Neither child module's
initializer behavior follows from that path.

The selected raw declarations are recorded in
`xivl-client-data:docs/parley-message-widget-declarations.md`, Selected roots
and name boundary. Those two forms do not supply a selected root script/class
discriminator. Form selection, template resolution and application remain
unresolved; no referenced template body is established by this request.

## Conditional unprefixed initializer

The unprefixed module's selected body is
`NegotiationMessageWidget.init(C,B1,B2,B3)`, where C denotes the child receiver,
distinct from the parent request's W. It has four fixed parameters and no
varargs. Missing positions become nil and excess positions are unavailable
to this body. These three data positions do not by themselves establish
which values the native factory delivered.

The published
[shared initialization contract](tutorial-form-name-selection.md#incoming-initialization-frame)
supplies a conditional composition. It requires the actual shared `_onInit`
binding and incoming frame, the selected published `initCommon` binding
returning numeric 4 as its first result, ordinary Lua `select`, and the saved
`init` function resolving to this body.

If the actual child `_onInit` variadic sequence is exactly
`("NegotiationMessageWidget",I,true,A1,A2,A3)`, the resulting initializer call
is `init(C,A1,A2,A3)`. Equality of that delivered sequence to the factory
tail is an additional premise. The factory request does not establish a
preserved native frame, delivered sequence, child identity or initialization.

The initializer first reads `C.work` once and assigns its `_temp` member a
fresh empty table. It supplies no declaration pairs or initial field values
in that table. This assignment establishes no native work allocation,
conversion, registration or default.

It then compares B2 with numeric zero, using Lua equality. Numeric zero
selects the first branch; false, nil and string `"0"` do not.

| B2 branch | Ordered requests |
| --- | --- |
| Equal to numeric zero | `setVisibility(C,"IconControl_NegotiationTitle",false)`. Discard all results. |
| Unequal to numeric zero | Read global `worldMaster` as M. Request `_getMyPlayer(M)` and retain one result J. Request `createVirtualItem(J,B2)` and retain one result V. Save C's current `setIcon` function, then request `getItemIcon(V)` with all results. Call the saved setter with C, `"IconControl_NegotiationTitle"` and that entire result sequence. Discard all setter results. |

Both J and V use one-result adjustment: an empty return becomes nil, and
excess results are discarded. There is no local validity or success guard
on either result. The icon getter's result handling is different. An empty
return supplies only C and the control name to the icon setter; one nil
supplies an explicit third argument. Multiple results, values after nil and
trailing nils are all forwarded. The setter function was saved before the
icon getter lookup and call, so a later change to `C.setIcon` does not replace
that saved function. The unequal branch does not request visibility true.

After the selected branch returns normally, the initializer makes these
requests in order. Each `setText` property is looked up afresh on C and all
its results are discarded.

1. `setText(C,"TextBlock_NegotiationTitle",7123,B1)`: B1 is exactly one
   supplied formatting position, including nil, false or zero.
2. `setText(C,"TextBlock_RemainderTurn","1")`: the final operand is the
   literal string `"1"`, not numeric 1.
3. Read the current global `tostring`, call it with exactly B3 and retain
   one result T. Then look up `setText` on C and request
   `setText(C,"TextBlock_AllTurns",T)`. An empty conversion result supplies
   one nil T; extra results are discarded. This body does not authenticate
   ordinary `tostring` or locally require its result to be a string.
4. `setText(C,"TextBlock_TurnText",7122)`, with no formatting operand
   following the numeric key.

The title and turn keys are request operands, without a text-table, item,
turn-count or rendered-output interpretation here. Normally returned false,
nil or zero from any setter does not prevent the following requests. The
initializer returns exactly zero values. Lookup, assignment and call errors
propagate; earlier `_temp` assignment and requests are not rolled back.

The original icon call has an important decompiler distinction: canonical
source displays two assigned getter-result locals and supplies those two
slots to the setter. Original `CALL C=0` followed by `CALL B=0` forwards the
complete sequence. The displayed slots do not impose a two-result limit or
pad an empty original result sequence.

## Source identity and original locators

The canonical member is `lua/scripts/widget/widgetbaseclass_common.lua`,
69,077 bytes and 3,361 lines, SHA-256
`2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f`.
[scripts.json](../manifests/scripts.json) owns this pin. The archive identity
is owned by [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

The original under `client/script/` is
`n1635q/n1635q89r57y9rr_7vxxvw.le.lpb`, 32,996 bytes, SHA-256
`c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c`.
Its XOR-0x73 decoded Lua 5.1 payload is 32,983 bytes, SHA-256
`7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns these
pins. The manifests and adopted parent publication are pinned at revision
`6d0a026a1e6d8bc2f8f41f187a7dbf18606c2ac8`.

Canonical lines 825-841 contain the selected helper and binding. Original
root closure PC112 and assignment PC113 bind `WidgetBaseClass.initChildWidget`
to `root/proto37`, code offset 13654, eleven instructions, three fixed
parameters, raw vararg flag 3, zero upvalues and no nested prototypes.
Prototype indices and PCs are zero-based. PC n is at `13654+4*n`, excluding
the LPB wrapper.

| Consequential operation | Original locator |
| --- | --- |
| Index method lookup and one-result call | SELF PC0; CALL PC1, B=2,C=2. |
| Fresh desktop lookup and opener method lookup | GETGLOBAL PC2; SELF PC3. |
| Complete tail and discarded-result opener call | VARARG PC8, B=0; CALL PC9, B=0,C=1. |
| Zero-value normal return | RETURN PC10, B=1. |

The desktop continuation's canonical member is
`lua/scripts/widget/desktopwidget_connector.lua`, 660,617 bytes and 26,564
lines, SHA-256
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`.
Its original is `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, 213,487 bytes,
SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`.
The XOR-0x73 decoded payload is 213,474 bytes, SHA-256
`685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`.
The same manifests own these pins. The generic creator publication above,
at the same pinned repository revision, owns the subsequent require/factory
adaptation.

Canonical lines 25187-25203 contain the desktop child opener and binding.
Original root PC1842 loads its method key; closure PC1843 and register-key
assignment PC1844 bind `DesktopWidget.openInitialChildWidget` to
`root/proto524`, code offset 204686, twelve instructions, five fixed
parameters, raw vararg flag 3, zero upvalues and no nested prototypes.
PC n is at `204686+4*n`, excluding the LPB wrapper.

| Desktop operation | Original locator |
| --- | --- |
| Literal nil/true comparison and early zero return | EQ PC0, A=0,B=256,C=257: both RK constants, nil/true; JMP PC1; RETURN PC2, B=1. |
| Creator method lookup | SELF PC3. |
| Complete tail and discarded-result creator call | VARARG PC9, B=0; CALL PC10, B=0,C=1. |
| Reached zero-value normal return | RETURN PC11, B=1. |

### Unprefixed child source

The selected canonical member is
`lua/scripts/widget/negotiationmessagewidget.lua`, 1,416 bytes and 65 lines,
SHA-256
`8343aa4ff6f6cd44c036b9f518373326ff6fd5601b077d82e8e205f115cfee91`.
Its original is `n1635q/w53vq19q1vwx5rr935n1635q.le.lpb`, 770 bytes,
SHA-256
`0bd146c48fede507299b78fe737b5cefae8c38e5ece08021d357cd1bb4149da9`.
The XOR-0x73 decoded payload is 757 bytes, SHA-256
`0540f07974e98223d4be4f312ec7fd24664d90572c59977d263ff41f71c3de9c`.
The same pinned manifests own these identities. The shared initialization
publication above is adopted at that repository revision.

Canonical lines 11-65 contain this initializer and binding. Root closure
PC8 and assignment PC9 bind `NegotiationMessageWidget.init` to `root/proto0`,
code offset 225, 42 instructions, four fixed parameters, raw vararg flag 0,
zero upvalues and no nested prototypes. PC n is at `225+4*n`, excluding the
LPB wrapper. This is the unprefixed member, not the separate Ask member.

| Child operation | Original locator |
| --- | --- |
| Fresh empty `_temp` assignment | GETTABLE PC0; NEWTABLE PC1; SETTABLE PC2. |
| B2/numeric-zero comparison | EQ PC3, B=2 with numeric-zero RK operand; jumps PC4/9. |
| Hide request on zero branch | CALL PC8, B=4,C=1. |
| One player and one virtual-item result | CALL PC12, B=2,C=2; PC15, B=3,C=2. |
| Saved icon setter and complete getter results | SELF PC16; getter CALL PC19, B=2,C=0; setter CALL PC20, B=0,C=1. |
| Title and literal remainder text | CALL PC25, B=5,C=1; PC29, B=4,C=1. |
| One conversion result, all-turns text and turn key | CALL PC32, B=2,C=2; PC36/40, B=4,C=1. |
| Zero-value normal return | RETURN PC41, B=1. |

Focused checks authenticate this original binding and verify both numeric-zero
branches, the fresh empty table, fixed supplied positions, saved setter,
complete icon results, one conversion result, literal string operand and
zero-value return. Canonical agreement has exactly the icon-result display
qualification above. Synthetic replies distinguish empty, explicit nil,
false, zero, multiple and trailing-nil results. Rejecting controls change
the guard source/type/polarity, request sources, result widths and return
width. No Ask child body, row, form property, template or native body is
part of this initializer contract.

Reproduction authenticates the archive, canonical member, original and payload,
then uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction` through complete
parsing and the selected root binding. In-memory canonical agreement,
supplied-frame/error probes and rejecting controls check both fixed frames,
open tails, operand identities, the literal comparison and result widths.
The two admitted adapters also compose against an opaque creator mock.
The probes model the admitted instructions without executing the client,
index getter, generic creator or native factory. They retain no raw source,
payload or instruction listing.
