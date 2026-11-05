# CommonAsk text requests

`CommonAskWidget.init` forwards its question to `setText` and its complete
variadic answer tail to `setListBoxItem`. These are dynamically selected Lua
helpers. The selected initializer does not establish their implementations,
native property requests or text provider, so its numeric answer keys cannot
yet be joined to a particular localized table through this body.

## Original initializer contract

The authenticated `widget/commonaskwidget.lua:11-57` corresponds to original
`root/proto0`, code offset `0x13F`, 37 instructions. Root closure PC8 and
assignment PC9 bind it as `init`. The prototype has four fixed parameters and
raw vararg flag 3. Write its frame as `(W,P,Q,D,...)`, where W is the receiver,
Q is the question operand and D is the default-answer operand. P is unused by
this body. Missing fixed operands become nil. The variadic tail begins after D.

Assuming the selected method calls return normally, the initializer performs
these requests in order. Each method is looked up on W and receives W as its
first argument. Every call discards all results (`CALL C=1`).

| Request | Original call locator | Argument width |
| --- | --- | --- |
| `setModal(W,true)` | PC10, `0x167` | `B=3` |
| `setCancelCondition(W)` | PC12, `0x16F` | `B=2`; no optional operand supplied |
| `_setUICommandTemplateCondition(W,"ControlTemplate_ListBoxItem","TemplateButton_Answer","UILuaCommands.Operate",5)` | PC18, `0x187` | `B=6` |
| `setText(W,"TextBlock_Question",Q)` | PC22, `0x197` | `B=4`; Q is one value, including nil |
| `setListBoxItem(W,"ListBox_Answers","Item_Answers","TemplateButton_Answer",...)` | PC28, `0x1AF` | `B=0`; open argument width |

`VARARG B=0` immediately before the final call supplies the entire answer
tail. An empty tail supplies no answers. Explicit nil entries, entries after
nil and trailing nil entries keep their positions and count in this Lua call.
The initializer does not inspect their types, convert keys to strings or stop
at the first nil. It does not unpack Q into separate question parameters.
These facts describe the helper requests, not the helpers' interpretation.

Before these calls, the initializer replaces `W.work._temp` with a fresh table
whose first entry is the pair `("askDefaultAnswer","integer8")` (PC0-7,
`0x13F-0x15B`). After the answer call, it tests D against nil (PC29,
`0x1B3`). It freshly reads `W.work` on the selected branch and stores D in
`askDefaultAnswer` when D is nonnil, or 1 when D is nil (PC31-35,
`0x1BB-0x1CB`). False, zero and other nonnil values are not replaced by 1.
The type-name string is a declaration in this table, not proof of native
conversion or range enforcement. The final `RETURN B=1` at PC36, `0x1CF`,
returns no values. There is no local result-dependent branch around the text
requests. Effects or failures inside the selected methods remain outside this
initializer's contract.

## Provider boundary

The [tutorial provider finding](tutorial-text-reference-provider.md#selected-request-and-native-property-route)
starts from a different, explicit request:
`_setTextProperty(W,nil,part,"Text",numericKey,...)`. Its native composition
depends on the leading Nil, identifier, selected property, preprocessing and
provider conditions. The published
[native TextBlock route](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-03-conditional-native-textblock-route)
and
[Content route](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-07-conditional-native-route-to-contentcontrolcontent)
do not identify CommonAsk's `setText` or `setListBoxItem` implementation.

In particular, `TemplateButton_Answer` does not prove a Button.Content write,
and numeric keys do not identify `xtx/_text_ui`. The first missing edge for
the answers is the implementation or binding of the selected
`W.setListBoxItem`. That helper would need to establish the argument-to-item
and property adaptation before a native route could be composed. Actual
receiver, part, marshalling, preprocessing, table override, loaded schema,
language and row result would remain conditions of the published native route.
No localized answer row or rendered label is established here.

## Answer 3 and caller behavior

The [confirm-prompt contract](confirm-prompt-client-contracts.md#pending-work-and-prompt-presentation)
owns the ordered answer keys: Warp uses 1131, 1132, 1136 and Raise uses 1128,
1129, 1136, with default answer 1. Its
[answer contract](confirm-prompt-client-contracts.md#answers-and-command-submission)
owns button results 1, 2, 3 and cancel result 0. MainMenuWidget submits every
result except 3, then clears its casting-system-command field. The tray
forwards result 3 along with its other results for the matching ask type.
This caller distinction assigns neither an expiry meaning to answer 3 nor a
timeout, renewal, authoritative acceptance or server policy.

## Source identity and verification

The source identities are recorded in `manifests/scripts.json`, row
`lua/scripts/widget/commonaskwidget.lua`, and
`manifests/retail_lua_coverage.json`, resource
`n1635q/7vxxvw9rzn1635q.le.lpb`. The canonical member is 2851 bytes and 133
lines, SHA-256
`d304094ae53cd9fa82c59166495941f310161ce1fac62c37025bfdb5da3cd8e5`.
The original LPB is 1559 bytes, SHA-256
`cad77ceafd51dfc6b59da750b7beb01d2d25f3641ba2e52ded2d198964c56b9c`.
Its decoded payload is 1546 bytes, SHA-256
`1a023c9f9d0b995d1640fd6e7c211b823d6eae0dd1970a615adc18e79d1c041b`.
The restricted archive identity is owned by `manifests/private_lua_corpus.json`.
Canonical source identity uses the [published LF convention](../lua/README.md#canonical-form),
separately from the original LPB and decoded-payload identities. Instruction
offsets above are decoded-payload offsets, and PCs are zero-based.

Original instructions, root binding and the selected canonical span agreed.
A bounded instruction evaluator checked missing/nil and nonnil defaults,
question operands, empty/full answer tails and nil positions. Rejecting
controls changed the question operand, tail width, result width, optional
cancel width, nil comparison, answer item and helper identities. No other
CommonAsk method body or localized row was studied. The confirm-prompt
publication was adopted at revision
`297a21a9bfa87f71bd033294fc92b087fd553e40`; the tutorial-provider publication
was adopted at `b4d0e96b02a9bac3b0a62941c0e18493f2b2713f`.
