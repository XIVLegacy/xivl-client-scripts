# Parley topic-data values

`NegotiationWidget.negotiationWidgetGetData(W,S)` selects three stored
operands. For numeric S equal to N in 1 through 12, it returns the values
read from `W.work.keyN`, `W.work.iconN` and `W.work.valueN`, in that order.
Each operand reads `W.work` afresh. Every other selector returns exactly
three numeric zeros without reading W.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
The getter establishes neither the actual stored values nor their Lua types.
It performs no call, direct field/global/upvalue write, conversion or row
lookup.

## Selector and result contract

The original has two fixed parameters, no varargs, no captured upvalues and
no nested prototypes. W is the receiver and S is its one supplied operand.
Omitted positions become nil. Excess arguments are unused. The method does
not read `work.select` itself or substitute it for a missing S.

The method compares S with numeric literals 1 through 12, in ascending
order, using Lua equality. There is no numeric coercion, range clamp or
truthiness test. Numeric 1 and numeric 1.0 select the same branch. String
`"1"`, nil, false, true and numeric zero do not select that branch, and no
string spelling selects any of the twelve branches.

| Reached condition | Ordered reads | Normal result |
| --- | --- | --- |
| S equals numeric N, for N in 1-12 | Read W's `work`, then `keyN`; read W's `work` again, then `iconN`; read W's `work` again, then `valueN`. | Exactly three values: the respective read results. |
| No numeric comparison matched | None. W is unused. | Exactly `0,0,0`. |

Matched reads replace all three local scratch zeros. A nil, false or zero
member result is preserved rather than replaced with a default. For
example, three nil member results return three positions `(nil,nil,nil)`,
and a nil third result remains the third position. These cases differ from
returning zero values. A missing ordinary Lua-table member yields nil under
ordinary table indexing, but the getter does not establish that the actual
work object uses that representation or those lookup semantics.

The unmatched path can return normally even when W is nil because it never
indexes W. A matched path must complete its reached lookups. Invalid
receiver/work indexing or a lookup error propagates. There is no error
handler or fallback after a matched read fails, and no normal result before
all three reads complete.

Every work/member lookup occurs when reached. The second and third work
objects need not be identical to the first. Even when they are identical,
the reads do not form an atomic snapshot. The body uses the same supplied W
for each outer lookup, without resolving a global receiver or caching one
work object for all three results.

## Selected declarations and storage boundary

The [initializer contract](parley-initial-state-request.md#work-declaration-and-direct-assignments)
owns the assignment of a declaration table to `W.work._temp` and its storage
qualifications. The selected entries used by this getter request:

| Returned member family | Requested type | Explicit default in its declaration pair |
| --- | --- | --- |
| `key1` through `key12` | `integer16` | None. |
| `icon1` through `icon12` | `integer24` | None. |
| `value1` through `value12` | `integer8` | None. |

Each selected pair has exactly its field name and type string. A declared
width does not establish installed storage, signedness, conversion, default
value, successful registration or actual Lua readback type. In particular,
`integer16` does not prove that R1 reaches a native formatter as an integer.
The getter does not install these declarations or initialize these members.
Writers and actual readback values require separate evidence.

## Conditional topic-request composition

The [parameter request](parley-parameter-request.md#ordinary-request-order)
reads its own W's `work.select` as S, requests the dynamically resolved
`W:negotiationWidgetGetData(S)` and retains exactly three results R1, R2 and
R3. If that method resolves to this getter on the same W and completes
normally, numeric N selects the fresh `keyN`, `iconN` and `valueN` reads
above. A nonmatching S yields the getter's three numeric zeros. That caller
passes R1 unchanged to `setText("TextBlock_TopicItem",7103,R1)`, R2 unchanged
to `setIcon("IconControl_TopicItem",R2)`, and does not use R3.

The [topic-text provider](parley-topic-text-provider.md) and the
[English row's argument contract](https://github.com/XIVLegacy/xivl-client-data/blob/5a5e027409731251abcb5391cb4d5738a9ec4ce2/docs/parley-topic-text-arguments.md#argument-structure-and-conditional-interpretation)
own the conditional projection into row 7103 of `xtx/_text_ui`. On their
admitted integer-argument path, its `0xE8`/index-1 expression uses R1 as a row
selector in `xtx/negotiationItem`, logical field 4. This getter identifies
R1's stored-member source for a matched S. It supplies no actual row value,
native integer tag, referenced schema, locale or resolved field value.

The `iconN` and `valueN` names do not establish an icon resource, topic
count, gameplay quantity or accepted domain. The published callback uses
are owned by the [Parley widget boundary](parley-target-gate.md#negotiation-widget-boundary).
They do not prove that another invocation receives the same selector,
receiver, work objects or stored values. No timer, scoring, server result,
historical invocation or rendered output is established here.

## Source identity and original locators

The canonical member is `lua/scripts/widget/ask/negotiationwidget.lua`,
48,254 bytes and 2,110 lines, SHA-256
`68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3`.
[scripts.json](../manifests/scripts.json) owns that pin. The containing
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
identities. The manifests and adopted Script publications are pinned at
repository revision `1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`.
The linked Data argument publication is pinned at
`5a5e027409731251abcb5391cb4d5738a9ec4ce2`.

Canonical lines 1795-1929 contain the getter and binding. Original root
closure PC38 and assignment PC39 bind it to `root/proto10`: code offset
13280, 130 instructions, two fixed parameters, raw vararg flag 0, zero
upvalues and no children. Prototype indices and PCs are zero-based. Offsets
exclude the LPB wrapper; getter PC n is at `13280+4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Three numeric scratch zeros and saved selector | PCs 0-3. |
| Numeric selector N equality | PC `4+10*(N-1)`, N=1-12. |
| Three fresh work/member read pairs for matched N | PCs `6+10*(N-1)` through `11+10*(N-1)`, in key/icon/value order. |
| Shared result copies and three-position return | PCs 125-128; RETURN PC128 has B=4. |
| Selected declaration pairs in `initAsk`, `root/proto0`, code offset 681 | Name LOADK PCs `3+4*(N-1)` for keyN, `51+4*(N-1)` for iconN and `99+4*(N-1)` for valueN. Each following LOADK supplies its type, followed by SETLIST with B=2. |

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. The archive, member,
original and decoded payload identities, complete parsing, selected original
root binding and prototype were checked. The selected canonical body agreed
with original-instruction evaluation for selector, ordered fresh reads,
nil/false/zero, omitted/excess arguments, result widths and lookup failure
cases. Synthetic changing work objects distinguished fresh reads from
caching. Rejecting controls changed selectors, guards, receiver/member
sources, result order/width, fallback and selected declared type. Only the
selected declaration entries were verified. No raw retail body, listing,
payload or complete declaration vector was retained, and no native or
runtime execution was performed.
