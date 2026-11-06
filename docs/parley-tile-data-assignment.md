# Parley tile-data assignment

`NegotiationWidget.negotiationWidgetSetData(W,S,K,I,V)` assigns three supplied
operands. When S equals numeric N in 1 through 12, it assigns K to
`W.work.keyN`, I to `W.work.iconN` and V to `W.work.valueN`, in that order.
Each assignment reads `W.work` afresh. An unmatched selector performs no
receiver access or assignment. Every normal path returns exactly zero values.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
Direct Lua assignments establish the local writer and operand mapping.
They do not prove native storage installation, conversion, successful
readback, an actual caller's input values or gameplay effects.

## Supplied frame and selector

The original has five fixed parameters, no varargs, no captured upvalues and
no nested prototypes. W is the receiver. S selects the member suffix, and
K, I and V are the three assignment sources. Missing positions become nil.
Extra arguments are unused. The body does not obtain a missing S from
`work.select` or obtain a missing assignment operand from an existing member.

The method compares S with numeric literals 1 through 12, in ascending
order, using Lua equality. Numeric N and numeric N.0 select the same branch.
Numeric zero, nil, false, true and strings, including `"1"` through `"12"`,
match none of those numeric literals. There is no coercion, range clamp,
truthiness test or alternate selector.

| Reached condition | Ordered operations | Normal result |
| --- | --- | --- |
| S equals numeric N, for N in 1-12 | Read W's `work` and assign its `keyN` from K; read W's `work` again and assign its `iconN` from I; read W's `work` again and assign its `valueN` from V. | Zero values. |
| No comparison matched | No work lookup or assignment. W, K, I and V are unused. | Zero values. |

K, I and V undergo no local type test, conversion, fallback or range check.
Nil, false and zero are supplied unchanged to their reached assignments.
For a matching S with all three operands omitted, the body still attempts
three assignments, each with nil. This is distinct from skipping those
members or substituting numeric zero. Under ordinary Lua-table assignment,
nil removes a member and false/zero remain values. The actual work object's
assignment behavior requires its own binding and storage evidence.

The result is neither a Boolean success flag nor the three assigned values.
This body does not read the written members back or validate any storage
effect before returning. An unmatched call can return normally even with
nil W because it never indexes W.

## Fresh receivers and assignment failures

Every outer lookup uses the same supplied W. The body resolves no global
receiver and retains no single work object across the three assignments.
The second and third `W.work` lookups can yield different objects from the
first. Assignment behavior can also affect later lookups. The sequence is
not an atomic update or a promise that one storage object receives all
three operands.

The next lookup and assignment are reached only after the preceding
operation completes normally. Invalid receiver/work indexing or an
assignment error propagates. The body has no error handler, rollback,
retry or fallback after a match. For example, an error assigning `iconN`
prevents the `valueN` lookup and assignment. An earlier completed `keyN`
assignment is not undone by this body. Failure of the second work lookup
likewise occurs after the first assignment and before the second.

There is no explicit helper/native call, global/upvalue write or other
member assignment. In particular, this body does not assign `work.select`,
declare work, assign a result, or request a text/icon/control update.
Implicit behavior of actual object indexing and assignment remains separate
from those explicit operations.

## Declaration and getter composition

The [initializer's declaration and storage boundary](parley-initial-state-request.md#work-declaration-and-direct-assignments)
owns the declaration-table request. The
[getter's selected declarations](parley-topic-data-values.md#selected-declarations-and-storage-boundary)
identify `key1` through `key12` as requested `integer16`, `icon1` through
`icon12` as `integer24`, and `value1` through `value12` as `integer8`, each
without an explicit default in its declaration pair. Those requested types
do not establish installed storage, conversion, signedness or actual Lua
readback types. This setter performs none of that declaration work.

The [getter contract](parley-topic-data-values.md#selector-and-result-contract)
returns fresh `keyN`, `iconN` and `valueN` reads in that order for matching
numeric N. Its returned values equal this setter's K, I and V only if the
actual setter/getter bindings, supplied selectors, receiver/work objects,
assignment behavior and preservation through each later read support that
relationship. A completed setter call alone proves none of those joins.
Its zero-value return must not be mistaken for the getter's three-value
result or unmatched three-zero fallback.

The [published Parley widget boundary](parley-target-gate.md#negotiation-widget-boundary)
owns other tile-update and copying observations. This setter study does not
establish a matching call from that code or identify this method's actual
S, K, I or V. The field names and declared widths supply no row, icon
resource, topic-count, item, actor, timer, scoring or server-policy meaning.
Actual stored values, referenced rows, rendered output and historical
invocation remain unestablished.

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
identities. The manifests and adopted initializer publication are pinned at
repository revision `6d0a026a1e6d8bc2f8f41f187a7dbf18606c2ac8`.
The linked getter page owns its independently authenticated original
selector/read/result contract.

Canonical lines 1665-1792 contain this setter and binding. Original root
closure PC35 and assignment PC36 bind it to `root/proto9`: code offset
12225, 123 instructions, five fixed parameters, raw vararg flag 0, zero
upvalues and no children. Prototype indices and PCs are zero-based. Offsets
exclude the LPB wrapper; setter PC n is at `12225+4*n`.

| Consequential operation | Original locator |
| --- | --- |
| Saved selector | MOVE PC0, from fixed parameter register 1. |
| Numeric selector N equality | PC `1+10*(N-1)`, N=1-12. |
| Fresh work reads before key/icon/value assignments | PCs `3+10*(N-1)`, `5+10*(N-1)` and `7+10*(N-1)`. |
| keyN=K, iconN=I, valueN=V assignments | SETTABLE PCs `4+10*(N-1)`, `6+10*(N-1)` and `8+10*(N-1)`, using fixed parameter registers 2, 3 and 4 respectively. |
| Shared zero-value return | RETURN PC122, B=1. |

Verification used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Archive, member,
original and decoded payload identities, complete parsing, selected original
root binding and prototype were checked. Original-instruction and selected
canonical evaluation agreed on selectors, operand slots, assignment order,
fresh work reads, omitted/excess arguments, nil/false/zero, zero-value
returns and errors with retained earlier assignments. Synthetic changing
work objects distinguished fresh reads from caching. A synthetic object
that discarded assignments confirmed the absence of local readback or a
storage-success check. Rejecting controls changed selector type/value,
guard, receiver/source slots, target field, order and return width.
No other body or declaration table was interpreted. No raw retail body,
listing, payload or complete vector was retained, and no native or runtime
execution was performed.
