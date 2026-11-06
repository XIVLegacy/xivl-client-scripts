# Sanction-scroll local eligibility

For a `CmnGoodStatusItem` receiver whose `_getCatalogID()` first result is
numeric `3020506`, the recovered `canUseForRelation` returns exactly
`(true, false, false)`. Its `canUseDetail` returns exactly `(true, 0)` without
reading any argument. These are local class-method results. They do not
establish successful use or application of Sanction.

`xivl-client-data:docs/sanction-static-rows.md`, "Scroll identity and retained
shop offers", authenticates catalog `3020506` as `scroll of Sanction` with
declared class path `Normal/CmnGoodStatusItem`. That publication is pinned to
revision `6f4def61dcec1c4abe1dd8154be15eb86f742770`. The declared class supplies
the connection to the script below. It does not prove the concrete runtime
object's method resolution or convert the item ID to status `223992`.

## Selected binding and inputs

The source locator is
`xivl-client-scripts:lua/scripts/item/normal/cmngoodstatusitem.lua:1-68`.
The root requests `require("/Item/Normal/NormalItemBaseClass")` at PC 2 and
`_defineClass("CmnGoodStatusItem", "NormalItemBaseClass")` at PC 6, each with
discarded results. Root PCs 8-9 create `root/proto0` and assign
`CmnGoodStatusItem.canUseForRelation`. PCs 11-12 create `root/proto1` and
assign `CmnGoodStatusItem.canUseDetail`.

These assignments establish local definitions under those global/member
bindings. The required base module and `_defineClass` implementation were
not inspected here. Their loading, inheritance, and runtime method lookup
remain inputs, as does any later replacement of a global or method.

| Method | Canonical source window | Original prototype | Fixed parameters including receiver | Code offset / words |
| --- | --- | --- | ---: | --- |
| `canUseForRelation` | 11-58 | `root/proto0` | 1 | 274 / 53 |
| `canUseDetail` | 61-68 | `root/proto1` | 11 | 644 / 4 |

Both prototypes have zero vararg flags, upvalues, and child prototypes.
Offsets are bytes in the decoded payload. PCs below are zero-based within
the named prototype.

## Relation predicate

The method first looks up `_getCatalogID` on its supplied receiver at PC 0.
It then calls that member with exactly the same receiver as its sole
argument at PC 1 (`CALL B=2 C=2`). The call retains exactly one result.
Extra results are discarded, and an empty result supplies nil. No catalog
argument is supplied to the method and no second catalog read occurs.

The retained value is compared with numeric catalog literals. For numeric
`3020506`, the nine earlier visited equality comparisons do not match.
The tenth comparison, PC 36 at payload offset 418, compares the retained
value with literal `3020506`. Equality skips the following jump. PCs 38-40
load boolean `true`, `false`, `false`, and PC 41 at offset 438 returns
exactly those three values (`RETURN B=4`). The corresponding canonical
comparison is at source line 40. No native getter or other helper is called
after the catalog read.

| First getter result | Local relation result | Original return PC |
| --- | --- | ---: |
| Numeric `3020506` | `(true, false, false)` | 41 |
| Nil, false, numeric zero, or string `"3020506"` | `(true, true, false)` | 51 |
| No getter results, padded to nil | `(true, true, false)` | 51 |

The second and third rows are controls for the default arm, rather than
claims about values the native getter actually returns. False, nil and zero
remain different values even though each reaches the same arm here.
Equality does not coerce the numeric string into the numeric literal.
Other catalog cases in this shared class do not identify additional
Sanction items and are not cataloged here.

There is no preliminary nil-receiver, catalog-validity, or getter-result
guard. An unsupported receiver or missing/noncallable member can fail
before a result. A getter error stops before the first comparison. The
body has no error handler, fallback getter, global read, or upvalue read.
These observations assume ordinary Lua 5.1 operations and normal completion
of the dynamic lookup and getter call. They do not establish the native
getter's result, ownership, or side effects.

## Detail predicate

`canUseDetail` reads none of its eleven fixed parameters, including the
receiver. PC 0 loads boolean true, PC 1 loads numeric zero, and PC 2 at
payload offset 652 returns exactly `(true, 0)` (`RETURN B=3`). It makes no
calls or member/global/upvalue reads. Missing arguments are nil-padded and
excess arguments are ignored without affecting this local result.
The final zero-result return at PC 3 is unreachable after the unconditional
two-result return. The relation method likewise returns before its final
zero-result instruction at PC 52.

Under the selected base `canUse` frame documented in
[item-use command flow](item-use-command-flow.md#itemcommand-and-base-item-eligibility),
the detail call is `canUseDetail(item, player, target, 1)` and requests two
results. If that member resolves to this override, the first result is
truthy and the second is numeric zero. This passes that particular detail
check. It does not bypass the earlier use-max, actor-state, target-parts,
or other runtime/native checks described by the base contract.

Neither selected body directly reads a company, rank, status, duration, or
equipment property. This is a statement about these two bodies, not the
absence of rank or company restrictions elsewhere in item use.

## Conditional widget composition

The [ItemUseWidget target-mode mapping](item-use-widget-contract.md#target-mode-mapping)
takes three relation results and separately calls dead-target and live-target
predicates on fresh item reads. If its relation call resolves to this method
and receives numeric catalog `3020506`, it obtains the three booleans above.
If the subsequent predicate calls complete and the dead-target first result
is not exact boolean true, that published mapping selects mode 2. An exact
true dead-target result instead selects mode 8. The live-target result is
read but does not enter that mode decision.

This composition is conditional on the complete published selection frame.
The dead/live method bindings and their bodies are outside this finding,
and the widget's three fresh item reads need not return the same object.
The positional relation flags alone do not establish named target categories
or the actual selected target. In particular, this is not an unconditional
claim that every scroll use selects mode 2 or targets the player.

The [selected item-use flow](item-use-command-flow.md#item-and-actor-operands)
owns the mode-2 package guards, supplied player operand, later fresh item
lookup, ready-command `21007` request, and subsequent target resolution.
Those later lookups and command bindings remain runtime inputs. Neither
the class tuple nor a local submission result proves server acceptance,
consumption, cooldown, inventory mutation, a status grant or duration,
or equipment-stat application. The separate
[CompanyBuffer contract](sanction-company-buffer-contract.md) does not
provide an item-to-status connection for this scroll.

## Source identity and verification

The archive declaration is
[`manifests/private_lua_corpus.json`](../manifests/private_lua_corpus.json).
The selected archive member is `item/normal/cmngoodstatusitem.lua`.
[`manifests/scripts.json`](../manifests/scripts.json) records it under the
`lua/scripts/` prefix. Only this member's header, bindings, and two methods
supply the source behavior described here.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Canonical LF member, 68 lines | 1389 | `c394327594278277509f63e7076a32454f059e0c43aaab70883fa7cd6273d4d1` |
| Original LPB | 714 | `304c54ea1a454f4a7d9fa4bd2812d599dd6f0c396aee7e9624a146a6109670dd` |
| Decoded payload | 701 | `a72ab556988721e97983cfaba204d7fcdd1a01c870248b89fca3654f5f69b318` |

The original resource is
`1q5x/wvsx9y/7xw3vv6rq9qpr1q5x.le.lpb`, relative to `client/script/`, as
recorded in
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
In-memory authentication used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` and `instruction`, including
the complete payload boundary, prototype headers, and root assignments.

Focused original-instruction replay and a separate parser/interpreter of
the literal canonical methods agreed on the exercised scalar cases.
Checks covered the target comparison and branch polarity, supplied receiver,
getter argument/result widths, empty and extra getter results, false/nil/zero
distinctions, exact returned literals and widths, ignored detail arguments,
and lookup/getter error order. In-memory rejecting controls changed the
target literal, branch, receiver, widths, and returned literals.
No original/canonical discrepancy was found for these checks. They are
source checks, not retail execution or a proof of native or server behavior.
