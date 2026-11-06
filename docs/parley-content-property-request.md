# Parley Content property requests

`WidgetBaseClass.setContent(W,N,K,...)` requests
`setTextProperty(W,nil,N,"Content",K,...)`. It preserves the entire format
tail, including empty, explicit nil and trailing nil positions, discards
every result and returns exactly zero values. Its body supplies no guard,
default, conversion, success test or separate `setItemContent` request.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
The adapter establishes a property request, without proving native delivery,
part resolution, applied Content, a selected label or rendered output.

## Supplied frame and call order

The helper has three fixed parameters and raw vararg flag 3. W is its
receiver, N is the part-name operand and K is its key/value operand.
Missing fixed positions become nil. The format tail begins after K and
retains all remaining positions and its exact count.

The body first captures `setTextProperty` from W, retaining W as the call's
receiver. It supplies a literal nil as the first name, N unchanged as the
second name, the literal property `"Content"`, K unchanged and the complete
incoming tail. Nil, false and numeric zero N/K values receive no local type
check or replacement. A one-nil tail is distinct from an empty tail, and
values after nil remain supplied.

All normally returned values are discarded. No result, one nil, false,
zero and multiple results produce the same zero-value helper return.
Lookup or call errors propagate and prevent normal return. The body does
not catch errors, retry, resolve a global receiver, read work or perform a
direct assignment. The actual method binding and any implicit indexing
behavior remain conditions.

The [Parley initializer](parley-initial-state-request.md#ordered-control-requests)
already owns `setContent(W,"Button_Ability",7107)`. If its dynamic method
resolves to this adapter, the reached request is
`setTextProperty(W,nil,"Button_Ability","Content",7107)`, with an empty Lua
format tail. This identifies an adapter frame, without resolving row 7107
or a displayed button label.

The [ability-list initializer](parley-ability-list-initialization.md#ordered-initializer-requests),
revision `e81ad360db72c58df104e6682e0eac642af2eb4e`, owns
`setContent(W,"Button_CloseWindow",7109)`. Under the same adapter binding,
this requests `setTextProperty(W,nil,"Button_CloseWindow","Content",7109)`.
The raw Button declaration and selected English row are owned by
`xivl-client-data:docs/parley-ability-text-labels.md`. They qualify a static
provider/label candidate under the conditions below, without establishing
an actual applied button value.

## Conditional numeric Content route

Adopt only the numeric `setTextProperty` path from
[CommonAsk's numeric projection](common-ask-answer-list.md#numeric-named-context-projection).
Write that wrapper's frame as `(W,C,P,Q,K,...)`. Under its actual binding,
normal prerequisite completion and a reached `type(K)` result exactly
`"number"`, it freshly captures W's `_setTextProperty` after that type call
and forwards every supplied position unchanged. Applied here, the request
is `_setTextProperty(W,nil,N,"Content",K,...)`. Alternate type reports
leave that studied path. This adapter supplies no type result itself.

The leading nil is part of the request. It is distinct from CommonAsk's
nonnil item-context name and template part. Adopting the numeric wrapper
does not replace this frame with that named-context example.

The adopted native contracts are
`xivl-client-structs:docs/widget-native-call-contract.md`, Property access,
and `xivl-client-structs:docs/global-native-contract.md`, Native frame,
revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`. Actual binding,
marshalling and preparation must preserve the matching typed frame and
values. The declared reader has three string names, an integer identifier
and eight integer/string alternatives. The first name's Nil admission
through the actual marshaller remains a condition.

On that admitted non-Nil identifier path, the native serializer begins
`@K`. Supported integer and string format cells append `/i` or `/s` with
their value. The first Nil scan cell terminates serialization. An empty Lua
tail alone does not prove zero native arguments: the first actual prepared
format scan cell must be Nil to establish the plain `@K` spelling. A supplied
Lua value's type and position do not establish an admitted native cell type
or preservation through preparation.

The adopted native/provider source is
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-01..03,
SQTP-07, Default table and named language fields, and Concrete lookup and
loaded-schema condition, revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`. The leading-Nil handler route
joins `FUN_006F4910 -> FUN_006E9AC0 -> FUN_0075B810` and the selected
property setter. SQTP-07 conditionally identifies Button.Content or
Label.Content with ContentControl descriptor `0x01358F94`, index zero,
callback `FUN_00936320` and common text preprocessing. This is a
registration/lookup inference for the selected Button or Label receiver,
not an inferred property route for every control type.

Application requires successful form record and part lookup, the visibility
gate, selected Content info/descriptor and permitted owner interception.
Property flags, TLS, interface/table selection, preliminary-helper effects
including aliased-input changes, preprocessing admission and normal helper
completion remain conditions. The source of the shared setter route is also
`xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter and
Setter, at that Decomp revision. A Content key retains its own property name
on the selected path.

On the admitted reference path the published constructor retains TextModule
and defaults to `xtx/_text_ui`. A pending table override can replace that
default. Language input chooses the outer logical field; this helper supplies
no language selector. The published static English definition maps logical
field 1 to physical string column 0. Actual schema loading, row readiness,
mapped type 10, supported argument parsing/copying and successful formatting
remain required. This wrapper study decodes no row and establishes no
ability identity, eligibility, gameplay rule or historical invocation.

## Source identity and original locators

The canonical member is `lua/scripts/widget/widgetbaseclass_common.lua`,
69,077 bytes and 3,361 lines, SHA-256
`2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f`.
[scripts.json](../manifests/scripts.json) owns this pin. The containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

The original beneath `client/script/` is
`n1635q/n1635q89r57y9rr_7vxxvw.le.lpb`, 32,996 bytes, SHA-256
`c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c`.
Its decoded Lua 5.1 payload is 32,983 bytes, SHA-256
`7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns those
identities. The manifests and adopted common/Parley Script publications
are pinned at revision `1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`.

Canonical lines 1749-1761 contain the selected adapter and binding. Original
root closure PC256 and assignment PC257 bind `WidgetBaseClass.setContent`
to `root/proto85`: code offset 20915, eight instructions, three fixed
parameters, raw vararg flag 3, zero upvalues and no children. Prototype
indices and PCs are zero-based; offsets exclude the LPB wrapper.

| Operation | Original locator |
| --- | --- |
| Capture `setTextProperty` and W | SELF PC0. |
| Literal nil, N, Content and K | PCs 1-4. |
| Entire incoming tail | VARARG PC5, B=0. |
| Open-argument call, discarded results | CALL PC6, B=0,C=1. |
| Zero-value return | RETURN PC7, B=1. |

The canonical display materializes the varargs in one local and supplies
that local. The original open VARARG/CALL pair owns the complete-tail
contract. The displayed local neither truncates the original tail nor pads
an empty original tail with a nil position.

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Archive, member,
original/payload identities, non-reparse paths, complete parsing and the
selected header/binding were checked. Original-instruction evaluation
matched an independent request oracle across names, keys, nil/false/zero,
missing fixed positions, empty/nil-bearing/long tails, discarded results and
lookup/call errors. Canonical evaluation retained the known one-local display
projection rather than asserting full argument agreement. Rejecting controls
changed receiver/name/key/property slots, tail/call widths and return width.
No other helper body, native body, form or row was interpreted by this
adapter study, and no raw body, listing, payload or vector is retained.
