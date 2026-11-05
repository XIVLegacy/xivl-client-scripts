# Guildleve playing choices and local results

The parent and child `processGuildlevePlaying` methods pass `canLeveLink`
unchanged into a Boolean-prefix parser. Conditional on the published
`askRestrictChoices` contract, Boolean true includes original choice 2 and
Boolean false omits it. Numeric zero, numeric one and nil instead terminate
the restriction prefix at that position. They begin the formatter tail and
do not express a disabled or enabled second choice.

The [Guildleve event contract](aetheryte-guildleve-events.md#eventglplay)
owns payload names and client-text meanings. This page composes these two
actual callers with the complete
[restricted-choice helper contract](aetheryte-restricted-choice-flow.md).
The methods' dynamic lookups must resolve to the named implementations.
Neither the supplied server argument types nor a historical invocation of
this menu is established.

## Caller operands and prefix boundary

Let `N` be the method receiver, `W` the looked-up `worldMaster`, `D` the
looked-up `desktopWidget`, and `A1..A9` the explicit payload arguments.
Let `S` be `A7`, except that exactly nil becomes numeric zero. `Q` is parent
row 146 or child row 35. Function tuples include their method receiver.

Both callers first compute `S > 0` and `A8 > 0`. There is no conversion of
`A2` to Boolean and no nil normalization of `A8`. With ordinary numeric
cost and difficulty operands, these comparisons produce Boolean values.
Nil `A8` or Boolean false in either comparison position instead reaches a
comparison-type boundary under ordinary Lua semantics. Zero is preserved
as a number. These are caller predicates, not a supplied argument schema.

| Boundary | Ordered operands |
| --- | --- |
| Playing method to `askRestrictChoices` | `W,N,N,Q,true,A2,(S>0),(A8>0),false,true,A1,S,A6,A8` |
| With six Boolean flags, helper to `askForEventMode` | `D,N,W,N,1,false,true,Q,answers,A1,S,A6,A8` |

The original call at PC31 supplies fourteen operands and retains one result.
The helper interprets the leading Boolean values as restrictions, including
only exactly true values. Its first non-Boolean value starts the formatter
tail. It also probes the following value through an open `select`/`type`
call. The helper publication owns both probes and their missing-argument
behavior.

For Boolean `A2`, non-Boolean `A1`, numeric `S` and numeric `A8`, the prefix
has exactly six flags and the tail has four values. Both probes have a
supplied value, including when `A1` is explicitly nil. This caller therefore
does not inherit the exhausted-argument conclusion of the separate parent
row-117 call, which supplied only six flags and no tail. The adopted
[native arity contract](aetheryte-restricted-choice-flow.md#adopted-native-arity-contract)
still distinguishes missing arguments from explicit nil. It does not prove
the global bindings at either invocation.

The following source-backed fixtures use numeric `A1`, positive numeric `S`
and positive numeric `A8`. They describe conditional helper interpretation,
not observed server payloads:

| Supplied `A2` | Restriction prefix | Formatter boundary |
| --- | --- | --- |
| Boolean true | Six flags. Original slot 2 is included. | Four values, starting at `A1`. |
| Boolean false | Six flags. Original slot 2 is omitted. | Four values, starting at `A1`. |
| Numeric 0, numeric 1, or nil | Only the first flag, true. | Nine values, starting at the unchanged `A2`, followed by the remaining four would-be flags and four format operands. |

Thus numeric zero does not produce the Boolean-false menu. Under these
premises the non-Boolean cases request only original slot 1, and the intended
four formatter positions are shifted. Explicit nil remains a supplied tail
value. Native formatting or rendered text for this shifted tuple is unproved.

`A1` also has no type guard here. If it were Boolean, the parser would consume
it as a seventh restriction and begin the tail at numeric `S`. This synthetic
boundary control prevents treating the positional payload names as type
evidence. The normal six-flag composition requires the stated `A1` premise.

Source: `chara/npc/object/aetheryte/aetheryteparent.lua:1441-1474` and
`chara/npc/object/aetheryte/aetherytechild.lua:171-204`, under `lua/scripts/`.

## Conditional displayed rows and original slots

With the six-flag interpretation above, the helper constructs a dense answer
table from `Q + originalSlot`. It requests compact default answer 1, which
maps to original slot 1 in every case. Parent rows are 147-152 and child rows
are 36-41. The linked event contract owns their text meanings.

| Original slot | Inclusion predicate | Local action |
| ---: | --- | --- |
| 1 | Always true | Continue. |
| 2 | `A2` is Boolean true | Leve-link confirmation. |
| 3 | `S > 0` | Guardian's Aspect confirmation. |
| 4 | `A8 > 0` | Difficulty branch. |
| 5 | Always false | No requested answer row. |
| 6 | Always true | Abandon confirmation. |

For example, Boolean false `A2`, zero `S` and positive `A8` request original
slots `1,4,6`. Compact answer 2 is adapted to original slot 4. The caller's
choice comparisons consume that original slot, not the compact answer index.
There is no disabled placeholder for omitted rows.

The adopted helper maps connector result -3 to one nil, and other nonpositive
numeric results to one numeric zero. Nil and Boolean false connector results
instead encounter its numeric comparison before any normal helper return.
For a positive integer within the requested answer count, its result is the
corresponding original slot. There is no answer-count rejection in its scan.
An excessive result is outside this mapping guarantee. These callers supply
a tail that can itself contain Boolean true, so the no-tail caller's
exhausted-scan consequence cannot simply be transferred here.

The helper's reached connector requests an explicit close before returning
its saved result and before the helper's comparison and adaptation. Exactly
nil opening skips widget operations and close. Other opening values, waits,
getter results, errors and close requests retain the conditions in the
[shared connector contract](camp-replacement-choice-flow.md#local-completion-result-and-cancellation).
A close request does not establish native destruction or cleanup completion.

## Confirmations, retry and caller return widths

After a normal helper return, numeric zero repeats the main menu. Result 1
returns exactly one numeric 1. Nil returns exactly one nil. The caller does
not add a general result-range check: a directly supplied unmatched nonzero
helper result passes through as one value. Synthetic false, 5 and -1 controls
demonstrate that caller boundary. They do not establish normal results from
the adopted helper or answers delivered by the UI.

| Adapted original slot | Calls before completion | Local completion |
| ---: | --- | --- |
| 2 | Parent say 153 / child say 42, optional class warning, then ask 154 / 43 with answer count 2 and format operands `A3,A4,A5,A1`. | Exactly numeric confirmation 1 returns one numeric 2. Every other normally returned first confirmation value retries the main menu. |
| 3 | Parent say 26 / child say 15, then ask 27 / 16 with answer count 2 and format operands `S,A6`. | Exactly numeric confirmation 1 returns one numeric 3. Other first confirmation values retry. |
| 6 | Parent say 158 / child say 47, then ask 159 / 48 with answer count 2. | Exactly numeric confirmation 1 returns one numeric 6. Other first confirmation values retry. |

Each ask retains only its first result. Boolean true is distinct from numeric
1 in these confirmation comparisons. The adopted generic
[`WorldMaster.ask` result contract](camp-replacement-choice-flow.md#local-completion-result-and-cancellation)
maps cancellation -3 to nil and otherwise preserves the first connector
result. Thus cancellation and numeric-zero failure both retry a reached
confirmation, while main-menu cancellation returns nil and main-menu zero
repeats the menu. These observations require normal helper completion.

On each reached leve-link branch, a non-nil, nonzero `A9` causes a fresh
`W:_getMyPlayer()` request. The caller retains one result and supplies it
after `A9` to `W:say(W,50039,A9,playerResult)`. It does not cache that player
across declined confirmations. Nil or numeric-zero `A9` skips these calls.
The player getter and say implementation remain opaque here. A retry calls
the menu helper again rather than reusing its previous result or answer table.

Source: parent `1476-1533,1572-1594` and child `206-263,302-324` in the same
two scripts. The warning is at parent `1483-1495` and child `213-225`.

## Difficulty caller boundary

For adapted slot 4, exactly numeric `A8 == 1` shows parent row 164 or child
row 53 and retries the main menu without calling the selector. Every other
value that reaches this branch shows parent row 162 or child row 51, then
requests:

```text
D:askEventModeWidgetYield("Ask/GuildleveSelectLevelWidget",1,A8-1)
```

The call retains two results, `ok` and `selected`. It returns exactly
`(4,selected)` only when `ok` is Boolean true, `selected` is non-nil, and
numeric comparisons establish `1 <= selected <= 5`. A non-true first result,
nil second result or numeric second result outside those bounds retries the
main menu.

The caller has no integer guard. A synthetic true/2.5 pair returns `(4,2.5)`.
A synthetic true/false pair reaches a comparison-type boundary, whereas a
false first result skips the second-result tests. These controls describe
the caller only. They establish neither values the native selector can emit
nor a supported fractional difficulty. Slot 4 is normally omitted when the
supplied numeric `A8` is nonpositive. The local branch itself does not repeat
that availability check.

The [published event-mode wrapper](craft-requested-quest-selection.md#selected-opening-and-result-tuple)
owns `askEventModeWidgetYield` and its `askWidgetYield` path. Conditional on D
resolving those implementations, 1 is the requested widget-result count.
The opening request after D is
`openWidgetYield(4,"Ask/GuildleveSelectLevelWidget",nil,nil,false,A8-1)`.

On normal helper paths, if opening returns nil, the wrapper returns one false, without selection,
getter or close. Otherwise let H be the non-nil opening result. The wrapper
requests `selectWidgetYield(H,true)` and later `closeWidgetDirect(H)`.
A selection result other than exact true returns one
false without a getter; exact true reads the widget results and returns
`true,R1`, preserving a nil first result and discarding later results. The
playing caller requests two values, so a one-false failure supplies nil to
its second local. The caller has no additional explicit close request.

This adopts the actual event-mode wrapper and retains its opening operands.
Actual widget creation, initializer/getter binding,
native closure, scheduling and accepted difficulty remain unproved. The
selected child widget's own result domain is owned by the
[level-selection widget contract](guildleve-journal-lifecycle.md#level-selection-widget).

Source: parent `1534-1571` and child `264-301`. Original PC114 has four total
operands and requests two results. PCs115-125 establish the result predicates.

## Authenticated evidence and limits

The original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). Canonical
sources matched [scripts.json](../manifests/scripts.json) in the archive pinned
by [private_lua_corpus.json](../manifests/private_lua_corpus.json). Extraction
is retail 1.23b `2012.09.19.0001`. Hashes below are SHA-256. Resource paths are
relative to `client/script/`.

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Parent canonical source | `lua/scripts/chara/npc/object/aetheryte/aetheryteparent.lua` | 39937 | `aa4897a10fa0f024fdcb609d556751627b858eb9d20817069baf42509359c3fa` |
| Parent original LPB | `729s9/wu7/v8057q/95q25slq5/95q25slq5u9s5wq.le.lpb` | 9809 | `6ba7d090271b658e523d416820cfb5d45e57227d4f22aaff8bfae1637c11f8ff` |
| Parent decoded payload | XOR-0x73 payload | 9796 | `4824c5921d56b262d47b40b82bc8366a795860b4dd9944ecdb41ac7fee4e33e3` |
| Child canonical source | `lua/scripts/chara/npc/object/aetheryte/aetherytechild.lua` | 7492 | `b309cd10cbe2759016d8f07735871a118a3957186983af365b1133224674ddd4` |
| Child original LPB | `729s9/wu7/v8057q/95q25slq5/95q25slq5721y6.le.lpb` | 2608 | `272874b6943a09230a4445bcc34743e3e4c89241b81dc19f2a34ff9699cd4845` |
| Child decoded payload | XOR-0x73 payload | 2595 | `453a18028dbc5d1883954ea33ea1494de1d83947212ee96dddada9db8232d252` |

The selected parent closure is `root/proto7`, code start 8707. The child is
`root/proto4`, code start 1506. Each has ten named parameters, no varargs and
155 instruction words. Prototype indices and PCs are zero-based. Code starts
are decoded-payload byte offsets. The root assignments bind the named methods
at parent canonical line 1594 and child line 324.

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader`, `instruction` and `states_for`.
Check complete payload parsing, class assignments, original operands and
result widths before composing the adopted helper contract. Finite caller
fixtures distinguish Boolean, nil and numeric link operands, nil cost
normalization, row predicates, retries, fresh warning reads, confirmation
equality and two-result difficulty handling. Reject altered call/result
widths, inverted confirmation and success predicates, and implicit Boolean
coercion of `A2`. Direct helper-result stubs test caller branches independently
of helper reachability. Prefix fixtures adopt the published helper semantics
and preserve explicit nil and missing-argument cardinality.

Actual event dispatch, actor/class identity, global `type`/`select` and helper
bindings, applied widget storage, formatting, rendering, native creation,
delivered callbacks, wait completion and accepted cleanup remain unproved.
The payload producer and actual operand domain remain unbound. The linked
event contract retains the Guardian's Favor, status, reward and authoritative
leve-link policy limits. These local results do not prove Favor deduction,
status application, difficulty scaling or server acceptance.
