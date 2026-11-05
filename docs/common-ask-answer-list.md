# CommonAsk answer-list adaptation

The shared `setListBoxItem` helper requests one `Content` property write for
each supplied answer position. For the published CommonAsk call, the item
names are `Item_Answers1`, `Item_Answers2` and `Item_Answers3`, with
`TemplateButton_Answer` as the second name. The published named-context
native route conditionally connects these numeric `Content` requests to
the default provider, `xtx/_text_ui`. Actual item creation, context and part
lookup, native frame, provider state, locale and rendering remain unproved.

## Selected helper contract

The selected definition is `widget/widgetbaseclass_common.lua:3060-3097`,
including its binding. Its original prototype is `root/proto168`, decoded
code offset `0x78C3`, with 32 instructions, four fixed parameters and raw
vararg flag 3. Zero-based root PCs 505/506 create its closure and assign it
to `WidgetBaseClass.setListBoxItem`.

Write the supplied frame as `(W,L,I,T,V1,...,VN)`: receiver, list name, item
prefix, template name and the complete answer tail. Missing fixed operands
become nil. With the standard Lua `select` implementation, the initial
`select("#",...)` obtains N, including explicit and trailing nil positions.
Only its first result is retained (`CALL B=0,C=2`, PC3).

The helper then makes these requests, assuming preceding operations complete
normally and the selected global functions and methods have the stated
implementations:

1. If L differs from nil, look up and call
   `addListBoxItem(W,L,I,N)`, discarding all results (PC10, `B=5,C=1`).
   This includes N=0. Nil L skips only this call. False and zero are nonnil
   and take it. The implementation of `addListBoxItem` is outside this finding.
2. Iterate numeric i from 1 through N, in ascending unit steps. Form the
   first property name by concatenating I with `tostring(i)`. Only the index
   goes through `tostring`; I is not validated or explicitly converted by a
   call in this body. Nil or Boolean I cannot complete this concatenation
   under standard Lua behavior when an iteration is reached.
3. In each iteration, freshly look up `select` and request `select(i,...)`
   with the complete original answer tail. Keep exactly its first result
   (PC23, `B=0,C=2`), yielding Vi rather than the remaining suffix.
4. After the `tostring` call at PC18 and the `select` call at PC23, freshly
   capture `setTextProperty` and its W receiver at PC24, then call
   `setTextProperty(W,I..tostring(i),T,"Content",Vi)`, discarding all results
   (PC29, `B=6,C=1`). The fixed width supplies exactly one answer operand,
   including nil. The lookup occurs anew in each iteration, after those
   argument-producing calls; PC29 uses the captured method and receiver.
   After the loop, return zero values (PC31, `RETURN B=1`).

The exact-nil list guard is PC4. The numeric loop preparation/back edge is
PC14/30, index string conversion is PC18 and concatenation is PC19.
The open `VARARG` instructions at PCs 2/22 preserve the tail for the count
and each selection. An empty tail performs no property call. Nil answers do
not terminate iteration, and false, zero and strings are forwarded without
a local type test. The helper supplies no formatting operands after Vi.
Results from item creation or property calls do not select a branch or become
the helper's return values. Failures inside those calls can prevent later
requests. This is a request contract, without proof of item creation or writes.

## CommonAsk composition and provider boundary

The [CommonAsk initializer](common-ask-text-request.md#original-initializer-contract)
owns the call
`setListBoxItem(W,"ListBox_Answers","Item_Answers","TemplateButton_Answer",...)`.
Composing it with this helper requires W to resolve the selected shared
implementation and the calls to complete normally. The
[confirm-prompt contract](confirm-prompt-client-contracts.md#pending-work-and-prompt-presentation)
owns Warp's ordered answer keys 1131, 1132, 1136 and Raise's 1128, 1129, 1136.
Thus each supplies N=3 and requests the three item names above in order.
No particular live widget or helper replacement is established by this join.

The [selected tutorial text-property contract](normal-tutorial-panel-completion.md#selected-text-property-request)
owns its specific nil-first-name Text request and the studied `setText` and
`setItemText` wrappers. Those two wrappers are adopted without another trace.
The distinct nonnil-name Content projection is confirmed below from the
selected original numeric path, rather than inferred from that example.

### Numeric named-context projection

`WidgetBaseClass.setTextProperty` has five fixed parameters and raw vararg
flag 3. Write its frame as `(W,C,P,Q,K,...)`: receiver, first name, second
name, property, key and full format tail. On the selected original path, its
`type(K)` call at PC4 keeps exactly one result (`B=2,C=2`). The PC5 comparison
selects this path when that result is exactly `"number"`. Other type results
leave the studied path; their property behavior is outside this finding.

After that call and comparison, PC7 freshly captures W's `_setTextProperty`
method and receiver. The following moves preserve C, P, Q and K unchanged,
including nonnil names. PC12 supplies the complete variadic format tail,
preserving its count, order and explicit/trailing nil positions. PC13 calls
the captured method as `_setTextProperty(W,C,P,Q,K,...)` with `B=0,C=1`,
discarding all results. PC14 reaches the shared zero-value return at PC28.
Thus the wrapper performs its native lookup after `type` completes and uses
that saved method/receiver for the call. Actual global/method bindings and
normal call completion remain conditions.

The original is `root/proto182`, decoded code offset 32430, 29 words, with
root closure/assignment PCs 547/548. Its canonical definition/binding envelope
is `widget/widgetbaseclass_common.lua:3276-3311`. Only original numeric
PCs 0-14 and shared return PC28 were interpreted here; alternate PCs15-27
were excluded. The common-module input identities below apply.

For the selected list call, C is `Item_AnswersN`, P is
`TemplateButton_Answer`, Q is `Content` and K is the supplied numeric answer
key. That call provides an empty format tail, so its native request candidate
is `_setTextProperty(W,itemName,T,"Content",key)` with no formatting operand.

The native
[Property access contract](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/widget-native-call-contract.md#property-access)
distinguishes a Nil first name, routed through `FUN_0075B810`, from a string
first name, routed through `FUN_0075B840`. `_setTextProperty` shares that
name routing through `FUN_006E9AC0`. Its nonnil identifier serialization
therefore supplies `@1131`, for example, with no `/i` or `/s` suffix here.
This encoding requires the matching typed native frame and successful reads.

The published
[named route to the setter](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-anime-property.md#route-to-the-setter)
joins both name-routing entries to builder `FUN_005354D0`. For a nonempty
leading name, it obtains the request/context ID through `FUN_005353E0`;
a negative ID ends the call. Thus `Item_AnswersN` supplies the context name,
`TemplateButton_Answer` the part name and `Content` the property name.
With the selected form, nonnegative ID and string pickup, processor table
`0x00FA0BAC` routes slot `FUN_00542710` to setter `FUN_00537DE0`.
Its [setter contract](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-anime-property.md#setter)
requires the request record and part lookup to succeed, including the
zero-ID/record-field gate. Only an `Anime` name match rewrites the key/value;
`Content` retains its own name and reference string. The receiver/value gate
still applies before generic property engine `FUN_00912850` is called.

The
[SQTP-07 Content route](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-07-conditional-native-route-to-contentcontrolcontent)
starts from that setter and conditionally resolves Button.Content or
Label.Content to ContentControl preprocessing. It supplies the Content info,
descriptor and callback match under its registration/lookup and owner-gate
conditions. The
[SQTP-03 preprocessing conditions](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-03-conditional-native-textblock-route)
and SQTP-07's Content callback then retain their property-flag, TLS,
interface, preliminary-helper and reference-admission conditions.

On that admitted path, the
[default-provider finding](tutorial-text-reference-provider.md#default-table-fields-and-remaining-values)
retains TextModule and uses `xtx/_text_ui` unless a pending table override
replaces it. Its language input selects the logical field; the selected Lua
call supplies no language. The published English schema maps logical field 1
to physical string column 0. This establishes a conditional static provider
candidate for the five answer keys, without selecting an actual locale.

The [static English labels](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/confirm-prompt-answer-labels.md)
own the five selected row contents. A template name alone does not prove a
native Button instance. Normal `addListBoxItem` completion does not prove
item creation, a valid request ID or a selected part. Actual frame preparation,
marshalling, bindings, form/context/record/part selection, property admission,
preprocessing, default-provider preservation, loaded schema, locale, ready row,
formatter completion and rendering remain conditions of this composition.

The [answer-result contract](confirm-prompt-client-contracts.md#answers-and-command-submission)
retains the caller distinction: MainMenuWidget omits result 3 from submission,
while the matching tray route forwards it. Neither that distinction nor these
property requests establish expiry, a timeout, renewal, authoritative
acceptance/refusal or server policy.

## Source identity and verification

The source is retail 1.23b extraction `2012.09.19.0001`.
[scripts.json](../manifests/scripts.json), row
`lua/scripts/widget/widgetbaseclass_common.lua`, pins the canonical member:
69077 bytes, 3361 lines, SHA-256
`2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json), resource
`n1635q/n1635q89r57y9rr_7vxxvw.le.lpb`, pins its original LPB: 32996 bytes,
SHA-256
`c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c`.
The decoded payload is 32983 bytes, SHA-256
`7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f`.
The archive identity is owned by
[private_lua_corpus.json](../manifests/private_lua_corpus.json).
Canonical [CRLF-to-LF normalization](../lua/README.md#canonical-form) is
separate from the original LPB and payload identities. All child PCs above
are zero-based and offsets refer to the decoded payload.

The archive member, original LPB, complete payload parse, root binding,
prototype header and selected canonical span agreed. A bounded evaluator
checked the original helper against synthetic expectations for answer count,
ordered iteration, nil positions, operand identity, exact-nil list admission,
property/selection widths and discarded results. Rejecting controls changed
the guard, property name and count, selection, call or return widths.
The additional numeric-path checks preserved both names, property, key, full
format tail and native lookup after `type`. Controls rejected swapped, dropped
or constant-nil names, changed property/key, dropped tail and changed call/result
or return widths. A separate list-helper control replaced methods during the
argument-producing calls and required the subsequent per-iteration capture to
see those replacements. No alternate numeric-wrapper branch, other original
child body or new native body was studied. The named route
and its STATIC input pins are adopted from
`xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter and
Setter, with `config/sqwt_anime_property.json` and
`tools/verify_sqwt_anime_property.py`, at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`. The same Decomp revision owns
SQTP-03/07, the default provider, loaded-schema and static English contracts.
The CommonAsk publication was adopted at revision
`64278f28975f345303914f30ee60807c6fe42d0a`; the tutorial wrapper example at
`297a21a9bfa87f71bd033294fc92b087fd553e40`; and the tutorial provider
composition at `b4d0e96b02a9bac3b0a62941c0e18493f2b2713f`.
