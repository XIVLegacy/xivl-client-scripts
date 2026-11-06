# Conditional Parley topic text provider

The selected Parley topic request conditionally addresses row 7103 in
`xtx/_text_ui`. Its Lua wrappers forward exactly one format operand, the opaque
first result R1 of `negotiationWidgetGetData`. The published TextBlock route
and default provider supply a static candidate, subject to native frame,
part, preprocessing, provider and locale conditions.

## Request and wrapper projection

The [parameter contract](parley-parameter-request.md#ordinary-request-order)
owns the ordinary-path requests `W:negotiationWidgetGetData(S)` and
`W:setText("TextBlock_TopicItem",7103,R1)`. The first retains exactly three
results, padding absent results with nil and discarding extras. Only R1 is
supplied to this text call. It has no established type, value or domain.
The helper and control names do not identify an item, actor or name value.

Adopt the shared wrappers from the
[selected text-property contract](normal-tutorial-panel-completion.md#selected-text-property-request)
and the original numeric path from the
[numeric projection](common-ask-answer-list.md#numeric-named-context-projection).
Under the selected bindings and normal completion, they request, in order:

1. `setItemText(W,nil,"TextBlock_TopicItem",7103,R1)`.
2. `setTextProperty(W,nil,"TextBlock_TopicItem","Text",7103,R1)`.
3. `_setTextProperty(W,nil,"TextBlock_TopicItem","Text",7103,R1)`.

Each wrapper discards its call results and returns zero values. The first
two preserve the complete format tail, including its count, order and nil
positions. Here that tail contains one position even when R1 is nil. False
and zero are forwarded unchanged. No local conversion or fallback supplies
an integer or string interpretation for R1.

The last projection requires the reached `type(7103)` call to report exactly
`"number"`. The native method and W receiver are captured after that call.
Other type reports leave the studied numeric path. Alternate property paths
are outside this contract. A lookup, argument-producing call or method error
propagates and can prevent the following requests.

This is the leading-Nil `Text` route. The answer-list publication's nonnil
item-context name, template part and `Content` property use a distinct named
route. They are not substitutions for this frame.

## Supplied topic declaration

The supplied retail `client/sqwt/widget/NegotiationWidget.form` contains one
element named `TextBlock_TopicItem`, of expanded type
`{http://namespace.square-enix.com/sqwt}TextBlock`. It starts at decoded
byte 2808, line 41. Its ancestor types, from the root, are
Window / Grid / Grid / Label / Grid / Grid / Label / Grid. The root is named
`Window_NegotiationWidget`; the two named ancestor grids are
`Grid_ItemSelection` and `Grid_TopicText`. All those expanded types use the
same Sqwt namespace.

The input is 9254 bytes, SHA-256
`0328f3b103658af4b91bd0f3a47112db8ceb2042acde5c970c9d5f8bf77f836d`.
Its decoded XML is 9246 bytes, SHA-256
`ab6eadae80c17253b3f98aeec8ac740e3f8e2e77ea24be2620a87847680715ce`.
The complete SQEX signature, basename-key Blowfish decode, strict UTF-8/XML
and exact re-encryption were checked using
`xivl-tools:tools/blowfish.py`, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.
Only the selected Name/type/namespace and ancestor context were interpreted.
Other attributes, styles and templates supply no evidence here. This matching
declaration does not establish the actual selected form or native part.

## Conditional native provider

The adopted [Property access contract](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/widget-native-call-contract.md#property-access)
owns `_setTextProperty` identity, leading-Nil routing and serialization. Its
declared reader has three string names, an integer identifier and eight
integer/string alternatives. Application requires the actual binding,
marshalling and preparation to produce the matching typed native frame.
The [Native frame contract](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/global-native-contract.md#native-frame)
retains post-preparation layout and value preservation as conditions.

With identifier 7103, the serializer begins `@7103`. A first Nil format cell
ends the scan without a suffix. An admitted integer cell appends `/i` and its
value, including `/i0` for integer zero. An admitted string appends `/s` and
its value. The Lua forwarding proof establishes none of those native types
for R1, including false. A non-Nil R1 yields exactly one serialized argument
only when the following native scan cell is Nil. The complete prepared frame
must establish that termination as well as the supplied cell's type and value.
The
[restricted reference grammar](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-01-restricted-descriptor-subset)
qualifies canonical signed 32-bit integer payloads and printable ASCII string
payloads excluding `/`. Other strings and conversions retain their boundaries.

The [tutorial provider composition](tutorial-text-reference-provider.md)
adopts SQTP-03's same-handler connection from a non-Nil identifier and
leading-Nil name through `FUN_006E9AC0` and `FUN_0075B810` to property processing.
Successful part lookup and its visibility gate must reach the selected
TextBlock.Text info, owner interception must permit dispatch, and preprocessing
must admit the wrapper. Property flags, TLS, selected interface/tables and the
preliminary helper's possible effects, including aliased-input changes, remain
conditions. The static declaration alone settles none of them.

On that admitted reference path, the published constructor retains TextModule
and defaults to `xtx/_text_ui`. A pending table override can replace that
default. Language input chooses the logical field; this Lua request supplies
no language selector. The published static `lang="en"`, `mode="client"`
definition at sheet ordinal 1 maps logical field 1 to physical `str` column 0.
Actual schema loading, row readiness and mapped native type 10 remain required.
SQTP-02 preserves supported argument types and order into the formatter under
its copy, allocation and iterator conditions.

The [selected English row contract](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/parley-topic-text-arguments.md)
owns row 7103's original/canonical structure and conditional argument use.
It selects no actual R1, loaded locale, referenced field value, formatter
result, applied Text value or rendered topic. These requests establish no
server rule or historical Parley outcome.

## Sources and verification

The Parley caller and adopted Script publications are pinned at
`6d0a026a1e6d8bc2f8f41f187a7dbf18606c2ac8`. The common-module original and
canonical identities are owned by
[CommonAsk's source identity](common-ask-answer-list.md#source-identity-and-verification).
The selected wrappers are common root/proto89, code offset 21514, seven words,
three fixed parameters/raw vararg 3; root/proto91, offset 21697, eight words,
four fixed/raw vararg 3; and numeric root/proto182, offset 32430, PCs 0-14 and
shared return PC28, five fixed/raw vararg 3. Their closure/assignment PCs are
268/269, 274/275 and 547/548. Canonical definition/binding envelopes are
1833-1844, 1859-1871 and 3276-3311 in
`lua/scripts/widget/widgetbaseclass_common.lua`. PCs are zero-based and
offsets exclude the LPB wrapper.

Authenticated archive/member/LPB/payload identities, complete parsing, selected
bindings and bounded original-instruction checks confirmed the one-value
projection, nil/false/zero and complete-tail preservation, result widths and
lookup after `type`. Rejecting controls changed call/return/tail widths and
selected declaration name, type, namespace or multiplicity. Native/provider
claims adopt the cited Structs revision and Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, SQTP-01..04, Default table and
named language fields, Concrete lookup and loaded-schema condition, and Static
English definition. No new native body or runtime invocation was studied.
