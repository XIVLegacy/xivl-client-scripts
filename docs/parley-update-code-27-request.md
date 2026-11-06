# Parley update code 27 requests

For matched numeric code 27, `NegotiationWidget.updateAskParameter` traverses
slots 1 through 12. At each slot it captures three getter results, multiplies
the third by 2 when its fourth payload value is Lua-truthy and divides it by
2 otherwise. It requests the data setter with the modified tuple, then
converts that local value through dynamic `tostring` and requests count text.
The selected normal path returns zero values.

The branch has no direct work/member, global or upvalue assignment. It does
request `negotiationWidgetSetData`, whose published implementation has direct
work assignments. Direct-write absence here does not establish unchanged
storage. This is recovered retail 1.23b Lua from extraction
`2012.09.19.0001`, without evidence of actual storage, display or gameplay.

## Selected frame and entry

Use the fixed callback frame `updateAskParameter(C,N,K,I,V,X,Y)`. C is the
receiver, N is the update code, and X is the fourth payload position after
the code. This prototype has seven fixed parameters, no varargs, captured
upvalues or nested prototypes. Missing positions become nil and extra
positions are unavailable to the body.

The earlier comparison/jump path rejects numeric codes 1-26 before the
selected comparison. Numeric 27, including numeric 27.0, reaches this branch.
The comparison does not coerce string `"27"`. Nil, false, true and numeric
zero do not match it. Their continuations, and earlier matching update
bodies, are outside this contract. Interpretation stops before the next
unselected comparison rather than assigning a result to the whole method.

K, I, V and Y are unused on this selected path. In particular, the arithmetic
value comes from the getter's third result rather than incoming V. X uses
Lua truthiness, not exact Boolean true:

| X | Selected arithmetic operation |
| --- | --- |
| Nil or Boolean false | `R3 / 2` |
| Any Lua-truthy value, including true, numeric zero or an empty string | `R3 * 2` |

For the supplied tail `(27,nil,nil,nil,true,nil)`, X is true and the
multiplication path is selected. This is a positional consequence of that
profile, not evidence that a particular instance received it. A missing X
selects division. Neither path validates or converts X into a Boolean.

The [published Judge and desktop route](parley-tile-update-request.md#judge-request-and-actor-guard)
owns the conditional six-position update tail and its actor/lookup gates.
Under those actual bindings and complete delivery, it forwards
`(N,K,I,V,X,Y)` unchanged to the selected callback. The desktop's complete
tail preserves nil positions; removing unused payload cells can move X.
Actual receiver, typed frame, callback binding and instance remain conditions.

## Ordered slot requests

The numeric loop has initial value 1, limit 12 and step 1. Each ascending
slot i makes the following operations, conditional on all preceding reached
operations completing normally:

| Order within slot i | Operation |
| ---: | --- |
| 1 | Resolve `negotiationWidgetGetData` on C and request it with exactly `(C,i)`. Retain exactly three results R1, R2 and R3, padding missing positions with nil and discarding extras. |
| 2 | Apply the selected Lua multiplication or division to R3 and numeric 2. Retain the arithmetic result E locally. |
| 3 | Resolve `negotiationWidgetSetData` on C and request exactly `(C,i,R1,R2,E)`. Discard every result. |
| 4 | Resolve current global `tostring`, call it with exactly E and retain one result T. Missing results become nil and extras are discarded. |
| 5 | After conversion returns, resolve `setText` on C and request exactly `(C,"Button_ItemIcon_"..i..":TextBlock_NumberOfTopics",T)`. Discard every result. |

Thus a normally completed traversal makes 48 explicit calls: twelve getter,
twelve setter, twelve conversion and twelve text requests. There is no direct
icon, visibility, storyboard, timer or focus request in this branch. Actual
implementations reached by its dynamic calls can have additional effects.

Each getter, setter and text lookup is fresh on the same supplied C. The
global conversion lookup follows the setter call. The text-method lookup
follows conversion. A setter can therefore affect the later global binding,
and conversion can affect the later text binding. The next iteration also
resolves its getter again. The twelve records are not an atomic snapshot.

R1 and R2 are supplied unchanged to the setter, including nil, false and
zero. The setter's returned nil, false, zero or extra results do not gate
conversion or text. T is likewise supplied unchanged, including one nil,
false or numeric zero position. No local check requires T to be a string,
and no scratch default replaces a missing getter or conversion result.

The text conversion consumes the retained local arithmetic result E. It
does not consume the setter's return or perform another getter read after
the setter. Possible storage conversion is not read back into the text
operand by this body.

The [literal count-text contract](parley-literal-count-text-request.md) owns
the conditional wrapper path for ordinary string conversion results. It
records the fixed direct-property request and discarded formatting tail,
retaining actual binding, native-frame, property-application and rendering
conditions.

## Arithmetic and library conditions

For ordinary Lua numeric operands, multiplication doubles R3 and division
halves it. There is no `math.floor`, integer rounding or integer-division
operation here. For example, ordinary numeric 3 divided by numeric 2 yields
1.5 before any setter/storage conversion. Numeric zero remains zero in both
operations. This is a client-side operand transformation, not an established
server scoring formula or accepted topic quantity.

The getter's third result has no local numeric type check, conversion call
or fallback. Under ordinary nil/Boolean arithmetic without an applicable
metamethod, nil or false R3 causes an error before that slot's setter.
False must not be treated as numeric zero. Lua numeric-string coercion and
applicable arithmetic metamethods require their own actual-value/type
premises. This finding does not select such values or implementations.

The [initializer's declarations](parley-initial-state-request.md#work-declaration-and-direct-assignments)
and [getter's selected member types](parley-topic-data-values.md#selected-declarations-and-storage-boundary)
request `integer8` for `value1` through `value12`. That declaration proves
neither actual Lua numeric values, signedness, installed storage nor what
happens when a fractional E is assigned. No range clamp or rounding occurs
in this branch before its setter request.

The `tostring` target is dynamically resolved. Ordinary library formatting
requires that actual binding and suitable values. Its name alone does not
establish a string result, a decimal spelling or rendered text. The numeric
loop's 1-12 control-name suffix uses Lua concatenation, without a separate
`tostring(i)` request.

## Getter, setter and storage composition

The [getter contract](parley-topic-data-values.md#selector-and-result-contract)
owns `negotiationWidgetGetData(C,i)`. If that lookup resolves to the selected
getter, each numeric i reads the correspondingly numbered key, icon and
value members (`key1` through `key12`, `icon1` through `icon12`, and `value1`
through `value12`). It reads them in that order and freshly reads `C.work`
for each member. The three work objects need not be identical. This branch
retains those three results and uses only the third in arithmetic.

The [setter contract](parley-tile-data-assignment.md#declaration-and-getter-composition)
owns `negotiationWidgetSetData(C,i,R1,R2,E)`. With that selected binding and
normal completion, it assigns R1, R2 and E to the corresponding numbered key,
icon and value members, freshly reading `C.work` for every assignment.
These are conditional direct
Lua assignments in the setter, not proof of native storage installation,
accepted conversion or later readback. The getter and setter can encounter
different work objects and intervening changes.

The branch contains no local storage-success check. Nor does its absence of
direct assignments prove that storage remained unchanged. Setter/helper
overrides, partial assignments and other dynamic effects retain their own
conditions. A later call's value must not be inferred from an earlier text
request or from the declared member width.

## Conditional storage conversion

The [native widget work routing](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/script/widget-work-members.md#read-and-write-routing)
connects a declared member assignment through work userdata `__newindex`
(`0x00D2F000 -> 0x00D175B0`) to `0x00D272D0`. Applying it here requires the
selected setter binding, a `C.work` userdata following that native route,
and a matched declaration registry node and factory that actually select
the `integer8` descriptor for the selected `valueN` member. A declaration
request alone does not establish those selections or installed pool storage.

The [work binder's bind route](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/work-binder-native-contract.md#the-bind-route)
reaches descriptor slot `0x6C` for conversion and storage only with a
nonzero installed storage dword and the shared `_bind` flag clear. A set
flag takes the bind route without storing the value. A zero storage dword
ends the write without a store; the corresponding integer reader yields
nil. These alternatives cannot be treated as successful numeric writes.

The [published value coercion](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/work-binder-native-contract.md#value-coercion)
uses `lua_tonumber` through `0x00CF35C0` for an integer descriptor, then
truncates toward zero through `0x009D6636`. For an ordinary finite fractional
numeric E whose truncated integer fits `integer8`, this qualifies a conditional
stored scalar distinct from E. The publication's qualification that the
exact low-bit store masks were not read byte by byte still applies.

For example, if the selected getter supplies ordinary numeric R3=3 and X
selects division, E is 1.5. Under all the storage premises above, its
`integer8` conversion yields scalar 1. The subsequent conversion request
still receives retained E=1.5, without reading that scalar back. Ordinary
`tostring` spelling requires its actual library binding, and a text request
does not establish rendering. Thus this example cannot justify equating
the text operand with a later work read.

A later getter can be related to the stored scalar only with the matching
getter binding, the same member/storage and descriptor reader at slot
`0x1C`, and preservation until its fresh read. Neither that read nor the
actual registry selection, installed storage or pool construction is proved
here. The native publications' initial-value and lifetime questions remain
open. This is composition of existing published contracts, not a native or
client execution result.

## Failures and source limits

A reached getter, arithmetic operation, lookup, concatenation, conversion or
call error prevents later operations and normal return. There is no local
error handler or rollback. Missing getter results are padded with nil;
they are not replaced with zero before arithmetic. A conversion failure can
occur after the same slot's setter completed, leaving its earlier requests
intact but preventing that slot's text request and later iterations.
A suspended or nonreturning call also blocks continuation.

No actual R1/R2/R3, row, icon resource, topic count, input domain, stored
result or rendered text is established. Timing, eligibility, scoring,
server settlement and historical invocation remain outside the finding.
Other update bodies are not interpreted here.

## Source identity and original locators

The canonical member is `lua/scripts/widget/ask/negotiationwidget.lua`,
48,254 bytes and 2,110 lines, SHA-256
`68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3`.
[scripts.json](../manifests/scripts.json) owns that pin. Its containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF byte pairs with LF only.

The original beneath `client/script/` is
`n1635q/9rz/w53vq19q1vwn1635q.le.lpb`, 15,618 bytes, SHA-256
`dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1`.
The decoded Lua 5.1 payload is 15,605 bytes, SHA-256
`33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns those
identities. The source manifests and adopted publications are pinned at
Scripts revision `e81ad360db72c58df104e6682e0eac642af2eb4e`.

Root closure PC29 and assignment PC30 bind `updateAskParameter` to
`root/proto7`, code offset 8830, with a 449-word prototype envelope. The
selected body window is PCs 392-428, plus the required prologue/comparison
entry dependencies and shared RETURN PC448. The next comparison at PC429
is a stopping boundary. No semantics are inferred for an out-of-scope exit.
Canonical lines 1567-1604 isolate the matching branch within the full
1147-1632 definition/binding envelope. Prototype indices and PCs are
zero-based; offsets exclude the LPB wrapper, so PC n is at `8830+4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Selected numeric-27 comparison and nonmatching exit | EQ PC392; JMP PC393 to PC429. |
| Loop start 1, limit 12, step 1 | LOADK PCs 394-396; FORPREP PC397 to PC426; FORLOOP PC426 to PC398. |
| Fresh getter and exactly three captured results | SELF PC398; CALL PC400, B=3,C=4. |
| Fourth-payload truthiness and local arithmetic | TEST PC404 on fixed parameter register 5; MUL PC406 and DIV PC408, each with right operand numeric 2. |
| Fresh setter and discarded results | SELF PC409; CALL PC414, B=6,C=1. |
| Fresh conversion and one-result capture | GETGLOBAL PC415; CALL PC417, B=2,C=2. |
| Text lookup after conversion and exact text frame | SELF PC419; CALL PC425, B=4,C=1. |
| Selected loop exit and zero-value return | JMP PC427 to shared RETURN PC448, B=1. |

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. It authenticated
archive/member/original/payload identities, non-reparse paths, complete
parsing and the selected root binding/header. Only the admitted branch,
required entry comparisons and shared return were interpreted. Earlier
matched bodies and other exits stopped before interpretation.

An independent request oracle and isolated canonical evaluation agreed with
the original instructions on tuple positions, loop order, Lua truthiness,
primitive numeric operations, nil/false/zero/missing/excess positions,
result widths, fresh dynamic lookups and partial error prefixes. The numeric
oracle rejected Python Boolean coercion and stopped at unmodeled string or
metamethod arithmetic. Conversion targets/results were synthetic, without
pretending to reproduce an actual library binding. Rejecting controls
changed loop bounds, flags, arithmetic, result/argument widths and scope
exits. No new getter/setter/helper/native body, form, row, consumer gameplay
source or runtime was studied. No raw retail body, listing, payload, AST or
complete vector was retained.
