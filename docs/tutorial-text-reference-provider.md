# Conditional tutorial TextBlock text provider

The selected Getting Around text request has a published native route to
TextModule using the interface's default table, `xtx/_text_ui`. This qualifies a static provider
candidate for text keys 9008 and 9009. Actual native binding, selected part,
preprocessing state, loaded table, locale and row result remain conditions.

## Selected request and native property route

The [selected text-property contract](normal-tutorial-panel-completion.md#selected-text-property-request)
owns the request
`_setTextProperty(W,nil,"TextBlock_Text_1","Text",key,R1,R2,R3)`, with key
9008 for Pad or 9009 for Keyboard. It also owns the conditional native
`@id/i.../s...` encoding and first-Nil termination. The
[supplied form declarations](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/tutorial-normal-form-declarations.md)
identify a unique `TextBlock_Text_1` of raw type `TextBlock` in each selected
form. A matching declaration does not identify the native part used by a call.

The native
[TextBlock route](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-03-conditional-native-textblock-route)
explicitly connects a non-Nil identifier and leading-Nil handler argument
through the same `_setTextProperty` handler to generic property processing.
With successful part lookup, its visibility gate, selected TextBlock.Text
info and owner interception result, that path reaches the Text descriptor's
preprocessing callback. Property flags, TLS, interface selection, mutable
tables and the preliminary helper's effects remain part of that contract.
The handler-level match does not prove admission of this Lua call through
the actual native argument marshaller.

## Default table, fields and remaining values

On the admitted reference path using the published constructor, and when no
pending table override replaces the default, the
[provider construction](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#default-table-and-named-language-fields)
retains TextModule and uses the literal `xtx/_text_ui`. Thus an admitted
9008 or 9009 reference requests that row in this table. The provider constructor
selects the field from its language input. The selected Lua request supplies
no explicit language selector.

The [restricted parameterized reference contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-01-restricted-descriptor-subset)
and [pending-node argument contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-02-pending-node-argument-identity)
preserve the supported integer/string argument types and order into the
selected formatter. They do not assign a town, NPC, grammatical or count
meaning to the tutorial's three operands.

The [loaded-schema condition](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#concrete-lookup-and-loaded-schema-condition)
requires the selected table, ready row and mapped string field/type 10.
The [static English definition](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#static-english-definition)
demonstrates one such schema input, mapping logical field 1 to physical
ordinal 0. It selects neither a running locale nor an actual loaded schema.
This composition supplies no row contents, encoded-token interpretation,
formatter result, applied Text value or rendered lesson.

The linked findings own the exact retail 1.23b input identities and native
locators. The conditional provider route adds no historical invocation or
same-instance readback to the original Lua request.
