# Parley literal count text request

Under ordinary `tostring`, ordinary global `type` and the selected shared
wrapper bindings, Parley
update code 27's count string reaches `_setProperty` as a direct value. It
does not take the numeric `_setTextProperty` request that serializes a text
identifier. This is recovered retail 1.23b Lua from extraction
`2012.09.19.0001`, without proof of applied properties or rendered text.

## Selected property request

Write `WidgetBaseClass.setTextProperty`'s frame as `(W,C,P,Q,K,...)`:
receiver, first name, second name, property, value and complete trailing
sequence. Its five fixed parameters pad missing positions with nil.
The selected original operations distinguish these cases:

| Reached condition | Request |
| --- | --- |
| K is nil, including an omitted fixed position | `_setProperty(W,C,P,Q,"")`, without calling `type`. |
| K is nonnil and the current `type(K)` reports a value other than exactly `"number"` | `_setProperty(W,C,P,Q,K)`. |
| `type(K)` reports exactly `"number"` | The [published numeric projection](common-ask-answer-list.md#numeric-named-context-projection), adopted without another interpretation of its body. |

With ordinary `type`, strings, including `"7103"` and the empty string,
take the direct-value request unchanged. False also remains false on that
route. Numeric zero takes the numeric route. There is no string-to-number
coercion or `tostring` request inside the studied direct-value path.
The actual global `type` binding matters: a replacement reporting
`"number"` for a string would select the published numeric path instead.
Only the first `type` result is retained; missing results become nil.

Both direct-value calls supply exactly W plus C, P, Q and one value. They
discard the entire variadic tail, including explicit and trailing nil
positions, false and zero. The names and property remain unchanged, even
when nil, false or zero. This forwarding does not validate their native
types. All call results are discarded, and normal completion returns
exactly zero values.

For a nonnil K, the `_setProperty` method and W receiver are captured after
`type` returns. The nil path captures them without that call. Each uses
the saved method and receiver for its request. A type, lookup or method
error propagates and prevents normal return. There is no error handler or
retry. A suspended or nonreturning call likewise blocks continuation.

## Conditional code 27 composition

The [code 27 contract](parley-update-code-27-request.md#ordered-slot-requests)
owns `setText(W,path,T)`, where
`path="Button_ItemIcon_"..i..":TextBlock_NumberOfTopics"` and T is the one
retained result of dynamic `tostring(E)`. Its
[storage qualification](parley-update-code-27-request.md#conditional-storage-conversion)
keeps E separate from a conditional stored scalar.

Adopt the [shared wrapper projection](parley-topic-text-provider.md#request-and-wrapper-projection):
the selected `setText` requests `setItemText(W,nil,path,T)`, which requests
`setTextProperty(W,nil,path,"Text",T)`. These wrappers preserve the full
tail, which is empty here, discard results and return zero values. With
ordinary `tostring` producing a string and ordinary `type` reporting
`"string"`, the selected branch requests exactly
`_setProperty(W,nil,path,"Text",T)`. It supplies the retained string,
without another work read or any formatting operand. The Lua wrapper adds
no `@` identifier prefix or numeric-reference serialization to that value.

The adopted [native Property access contract](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/widget-native-call-contract.md#property-access)
matches this `_setProperty` request and its leading-Nil name route. Actual
method bindings, marshalling and preparation must produce its typed native
frame. Successful part lookup, value pickup and property application remain
conditions. This study supplies no active form, selected part, formatter
result, applied Text value, rendering, stored count or gameplay rule.

## Source identity and original locators

The source manifests and adopted Script publications are pinned at Scripts
revision `47eb1dddc6e523356e5fa50d47b3051462ed9e30`. The common-module
identities are:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `lua/scripts/widget/widgetbaseclass_common.lua` | 69077 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| Original `client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 | `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` |
| Decoded Lua 5.1 payload | 32983 | `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |

[scripts.json](../manifests/scripts.json) owns the canonical pin and its
3361-line count. [retail_lua_coverage.json](../manifests/retail_lua_coverage.json)
owns the original and payload pins. The containing archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json): 14385427
bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

Root closure PC547 and assignment PC548 bind `setTextProperty` to
`root/proto182`, code offset 32430, 29 words, five fixed parameters, raw
vararg flag 3, zero upvalues and no children. Canonical definition/binding
lines 3276-3311 agree with the selected original paths. PCs are zero-based;
PC n is at decoded offset `32430+4*n`, excluding the LPB wrapper.

| Operation | Original locator |
| --- | --- |
| Exact-nil entry and alternative | EQ/JMP PCs 0-1; nil target PC22. |
| Dynamic type request and exact-number comparison | GETGLOBAL PC2; CALL PC4 B=2,C=2; comparison/jump PCs 5-6. |
| Nonnumeric method/receiver capture and request | SELF PC15; CALL PC20 B=6,C=1; jump PC21 to PC28. |
| Nil alternative capture and empty-value request | SELF PC22; empty string PC26; CALL PC27 B=6,C=1. |
| Shared zero-value return | RETURN PC28 B=1. |

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Archive, canonical,
original and payload identities, non-reparse paths, complete parsing, header
and root binding were checked. A bounded original-instruction evaluator,
separate request oracle and in-memory canonical evaluation agreed on the
selected values, nil alternative, discarded tails/results and lookup order.
Controls rejected changed method, receiver, value, type guard, empty value,
tail width and call/return result widths. Numeric PCs7-14 stopped before
interpretation and retain their published contract. No other helper or
native body, form, template or row was studied. No retail body, payload,
listing, AST or complete instruction vector was retained or executed in a
client.
