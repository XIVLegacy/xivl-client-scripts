# Aetheryte restricted-choice result flow

The first `AetheryteParent.eventAetheryteParentSelect` menu has an argument
arity boundary before its Ask widget can open. Its six Boolean restriction
arguments exhaust an open-ended `select` call, whose zero results become
zero arguments to `type`. The authenticated native contract distinguishes
this missing argument from explicit nil in both base `type` and the installed
LGE override. The override selects a diagnostic path. This does not establish
which globals this menu resolves or an observed retail failure.

Conditional on normal completion of that prefix scan, the helper filters
answer rows in Lua and translates a compact answer index back to the
original slot number. It does not forward six disabled-button flags to Ask.
Only an exactly Boolean true first caller argument includes original slot 2.
False, nil and numeric zero all omit that slot.

This composes the first row-117 menu in the
[Aetheryte object contract](aetheryte-object-event-contracts.md#parent-selection).
That page owns the other object methods and nested menu. The
[Camp choice flow](camp-replacement-choice-flow.md) owns the shared connector
and Ask operation/cancel behavior. The selected methods below require their
dynamic lookups to resolve to the authenticated implementations.

## Caller and prefix-scan arity

Let `N` be the Aetheryte method receiver, `W` the global `worldMaster`, `D`
the global `desktopWidget`, and `A1` the first argument after `N`.
The tuples below include each method receiver.

| Boundary | Ordered values |
| --- | --- |
| Parent to `askRestrictChoices`, `A1 == true` | `W,N,N,117,true,true,true,true,true,true` |
| Parent to `askRestrictChoices`, every other `A1` | `W,N,N,117,true,false,true,true,true,true` |

Neither call supplies a non-Boolean formatter or terminator after its six
flags. In the original helper, `select` at PC24 has `CALL C=0`, preserving
all results. The following `type` at PC25 has `CALL B=0`, forwarding exactly
those results. Once the six flags have been consumed, standard `select`
returns zero values. This is `type()`, not `type(nil)`.

The separate standard Lua 5.1 fixture uses `luaB_type`, which calls
`luaL_checkany` for argument 1. That guard
rejects an absent value while accepting explicit nil. Its `luaB_select`
returns no values for an exhausted suffix. These are the standard-library
premises in the [base library](https://lua.org/source/5.1/lbaselib.c.html)
and [auxiliary library](https://lua.org/source/5.1/lauxlib.c.html).
Under those premises, all four selected A1 cases (true, false, nil and zero)
stop at helper PC25 before any connector, opening or close call.

The helper also has a second open `select`/`type` pair at PCs35-36. Appending
only one synthetic nil after the six flags moves the missing-argument error
to PC36. Appending two explicit nils satisfies both probes and permits the
downstream path under standard globals. That is a synthetic helper fixture;
the original parent supplies neither value.

### Adopted native arity contract

The retained native
[`xivl-client-structs:docs/lua-base-library-arity.md`](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/lua-base-library-arity.md#lge-override),
"Retained base functions", "LGE override" and "Script boundary", records
exhausted base `select` returning zero values. It also records `0x00CD8990`
installing LGE `type` function `0x00D09240` into globals. The base registration
table alone therefore does not identify the later `type` binding.

The installed override returns one `"nil"` for an explicit nil. A zero-argument
call instead enters its diagnostic/error-dispatch chain. Conditional on this
menu resolving the retained base `select` and that override, the call at
helper PC25 selects this diagnostic path before any connector call. The
native contract leaves the actual diagnostic-state identity, error protection
and propagation unbound. It does not establish an observed menu error or
whether the invocation later reaches a connector.

Actual global values, script environment and later rebinding at this menu
invocation remain unproved. The strict standard-library replay above is a
conditional fixture, not authority for the installed override's behavior.
Both the native and fixture contracts preserve the missing-versus-nil
distinction. Downstream behavior still requires normal prefix-scan completion.

## Conditional rows and default

The following tuples, row/default requests and result mapping require the
prefix scan to complete normally with the shown restriction interpretation.
For the original no-tail call, that requires global behavior compatible with
the scan, including both exhausted `type` calls. Downstream checks instead
use standard globals with two explicit synthetic nil terminators. In that
fixture, two nil formatter values are appended to the `askForEventMode` and
widget `ask` tuples below. They do not change the answer rows or default.

| Boundary after a normal prefix scan | Ordered values for the original no-tail call |
| --- | --- |
| WorldMaster to `askForEventMode` | `D,N,W,N,1,false,true,117,answers` |
| Opening request | `D,4,"Ask/AskWidget",nil,nil,false` |
| Opened widget's `ask` | `widget,W,N,1,false,true,117,answers` |

The six Boolean values describe original slots 1 through 6. The helper
includes a slot only when its value is exactly true. It constructs a new
dense answer table from row 117 plus the original slot number:

| Caller predicate | `answers`, indexed from 1 |
| --- | --- |
| `A1 == true` | `118,119,120,121,122,123` |
| Every other `A1` | `118,120,121,122,123` |

The actual receiver of the helper is `W`, while `N` is supplied twice.
The selected question property request consequently uses provider `N` and
row 117. The forwarded `W` does not replace that provider. The numeric rows
do not establish labels, destinations or action meanings.

The helper's downstream literal default is compact answer 1, corresponding
to row 118 in both tables. Through the pinned Ask method, this requests answer count
6 or 5, paging false, cancellation true and one page. The default request
still depends on the Ask work-field range checks and applied storage.
The connector's opening category 4 is distinct from either answer count.
No original slot-2 placeholder is retained in the five-answer table, and
these selected calls supply no separate disabled-control request.

The helper uses `type(select(...))` to delimit the Boolean restriction
operands, including the lookahead described above. A numeric zero is not a
Boolean false. A non-Boolean begins the formatter tail rather than adding
another restriction. Original open-ended `VARARG` and `CALL` operands preserve
that tail, including nil values. The parent and helper each request exactly
one callee result. If reached, the connector discards the widget `ask` results.

Source: `chara/npc/object/aetheryte/aetheryteparent.lua:32-194`,
`world/worldmaster_event.lua:159-233`,
`widget/desktopwidget_connector.lua:12038-12090`, and
`widget/ask/askwidget.lua:108-248`, under `lua/scripts/`.

## Conditional result adaptation and caller branches

After a reached connector returns normally, `askRestrictChoices` scans the
original restriction values, counting only exact true values, until it has counted
the requested number of answers. For an integer answer in the requested
range, it returns the original slot number of that answer. The result is
therefore an original slot number rather than a compact displayed index.

| Compact answer | Original slot, `A1 == true` | Original slot, other `A1` |
| ---: | ---: | ---: |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 3 | 4 |
| 4 | 4 | 5 |
| 5 | 5 | 6 |
| 6 | 6 | Outside the requested range |

After a normal helper return, the parent consumes that one adapted result
as follows. These branches do not establish that the prefix scan succeeded:

| Adapted original slot | Parent's selected local continuation |
| ---: | --- |
| 1 | Returns exactly one nil. |
| 2 | On the true-gate path, enters the separate branch leading to the row-7 menu. Its further processing is owned by the object contract. |
| 3 | Returns exactly one numeric -1. |
| 4 | Shows row 328, then asks with row 329. Exactly answer 1 returns one numeric -2; every other first confirmation result returns one nil. |
| 5 | Returns exactly one numeric -3. |
| 6 | Calls `N:showAetheryteTips()`, discards its results, then returns zero values. |

After reaching the connector, cancellation and failure remain distinct from
these slot numbers. The earlier missing-argument error returns no such scalar:

| First connector result | Helper result or boundary | Parent behavior after a normal helper return |
| --- | --- | --- |
| Numeric -3 | Exactly one nil | No slot branch matches; returns zero values. |
| Numeric 0 | Exactly one numeric 0 | No slot branch matches; returns zero values. |
| Other nonpositive number | Exactly one numeric 0 | No slot branch matches; returns zero values. |
| Nil or Boolean false | Numeric comparison error before a helper return | No subsequent parent branch is established. |
| Positive number beyond the number of true flags | The scan has no end-of-varargs or answer-count rejection | No normal helper return is established. |

The last row describes the script boundary, not a delivered native answer.
With the selected finite flags and the standard `select` behavior, exhausted
varargs supply no further true values and the scan cannot satisfy its count.
The pinned Ask operation handler converts the delivered answer-name suffix
with `tonumber` and adds no answer-range guard. A failed conversion can
supply nil; a synthetic out-of-range suffix can supply an excessive number.
This does not establish that the native UI can deliver either name.

The adaptation is not the generic `WorldMaster.ask` scalar passthrough.
In particular, its numeric comparison occurs before its exact -3-to-nil
conversion. Nil, false and zero must not be collapsed into one failure value.
Neither cancellation nor an opening failure selects original slot 1.

## Conditional wait and explicit close boundary

If the prefix scan reaches it, the
[shared connector contract](camp-replacement-choice-flow.md#local-completion-result-and-cancellation)
initializes its saved result to numeric zero. Exactly nil opening skips the
widget operations and close request. Every other opening value reaches the
widget method lookup, so Boolean false can fail there. After a normal `ask`
return, only an exactly true selection result causes `getAskResult` to run.
Its first result replaces the saved zero without normalization. Other
selection results leave zero.

For a non-nil opening and normal completion of those calls, the connector
then requests `closeWidgetDirect(D,widget)`, discards its results and returns
one saved value. This conditional close precedes the restriction helper's
numeric comparison and index adaptation. A later helper error or excessive
result scan does not undo a close request already made. The strict standard
missing-argument failure at PC25 instead occurs before any opening and close.
Errors, suspension or nonreturn within a reached connector can also prevent
its later close request.

The [Ask base predicate](ask-widget-result-state.md#selected-state-and-calls)
tests whether the stored result differs from numeric zero, rather than
whether it represents acceptance. The selected cancellation command requests
numeric -3 when `canCancel` reads exactly true. The base setter does not
close the widget. The [selection wait](gridania-opening-tutorial-contract.md#selected-widget-calls)
has no fixed timeout on this route, and the
[direct-close contract](content-director-ui-contracts.md#closewidgetdirect-behavior)
qualifies its liveness lookup and cleanup request. A normal close return
does not prove native cleanup or destruction.

## Authenticated inputs and reproduction

Extraction: retail 1.23b `2012.09.19.0001`. The containing archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). Canonical
members matched [scripts.json](../manifests/scripts.json) after CRLF-pair-to-LF
normalization only. Original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Hashes below are SHA-256. Resource paths are relative to `client/script/`.

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Parent canonical source | `lua/scripts/chara/npc/object/aetheryte/aetheryteparent.lua` | 39937 | `aa4897a10fa0f024fdcb609d556751627b858eb9d20817069baf42509359c3fa` |
| Parent original LPB | `729s9/wu7/v8057q/95q25slq5/95q25slq5u9s5wq.le.lpb` | 9809 | `6ba7d090271b658e523d416820cfb5d45e57227d4f22aaff8bfae1637c11f8ff` |
| Parent decoded payload | XOR-0x73 LPB payload | 9796 | `4824c5921d56b262d47b40b82bc8366a795860b4dd9944ecdb41ac7fee4e33e3` |
| WorldMaster canonical source | `lua/scripts/world/worldmaster_event.lua` | 7559 | `744487a7caaa94e1c4d2056cc07686a894c6ba336bbd021bbffeebceef2ad099` |
| WorldMaster original LPB | `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb` | 2555 | `4ced313114ab09753ad0dc82ea8e9cd12c66d31447c967e91883932291cd7459` |
| WorldMaster decoded payload | XOR-0x73 LPB payload | 2542 | `c7db606357f8e5811809a6232157c2c9ac1daf0055cfcaa01fbbc7051fd68bf5` |

The connector, AskWidget, AskBaseClass and `system/string.lua` canonical
members, original resources and payloads were also reauthenticated against
the identities retained in the [Camp flow](camp-replacement-choice-flow.md#authenticated-inputs-and-locators)
and [Ask base page](ask-widget-result-state.md#source-identity).

Prototype indices and PCs below are zero-based. Code starts are byte offsets
in the decoded payload, excluding the LPB wrapper. A PC is at `code start +
4*PC`. Root binding PCs assign the named closures.

| Method | Root binding PC | Prototype / code start | Selected original evidence |
| --- | ---: | --- | --- |
| Parent `eventAetheryteParentSelect` | 15 | `root/proto2` / `0x2F5` | PC39 compares A1 with Boolean true. PCs52/112 call global WorldMaster with ten arguments and retain one result. PC154 returns zero values after tips or an unmatched result. |
| WorldMaster `askRestrictChoices` | 23 | `root/proto7` / `0x612` | Four named parameters plus varargs. PC13 tests exact true; PCs15-16 construct compact rows. PC24 preserves all select results and PC25 forwards them to type; PCs35-36 repeat the open select/type probe. PCs26/37 test Boolean type. If reached, PC44 supplies default 1 and PCs51-53 forward the open tail and retain one connector result. PCs55/60/61 scan the original flags; PC67 tests -3; PC70 returns one value. |
| Connector `askForEventMode` | 713 | `root/proto237` / `0x1C081` | PC15 retains one opening result; PC16 tests nil. PC27 discards ask results. PC32 tests exact true selection. PC35 retains one widget result; PC39 discards close results; PC40 returns one saved value. |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader`, `instruction` and `states_for`.
Check complete payload consumption, root assignments, original argument and
return widths, exact Boolean predicates, compact row construction and the
result scan before composing the selected route. Focused original-instruction
checks distinguish true, false, nil and zero at the actual caller and require
the standard-type failure at PC25 before connector entry. They distinguish
missing arguments from explicit nil, with a one-nil control failing at PC36.
Conditional downstream checks use two synthetic nil terminators and cover all
requested compact indices, cancellation, numeric-zero failure and formatter
forwarding. Caller branch checks directly supply helper results. Inverted
caller/type/remapping tests, altered result widths and silent missing-to-nil
padding must be rejected for their intended differences.

This is a static script contract. Actual object identity, class binding,
global `type`/`select` bindings, work storage, native creation and property
effects, rendering, delivered callback names, wait completion and accepted
cleanup remain conditional.
No label lookup, native body, runtime execution, external event dispatcher,
server action or persistent travel state is established by this flow.
