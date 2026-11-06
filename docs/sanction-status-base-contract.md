# Sanction and the status base client contract

The selected `StatusBaseClass` methods expose a static-actor-ID request,
a sheet-data request, a sheet-life calculation and a default death predicate.
Their conditional relationship to Sanction depends on the declared child
class and actual runtime member bindings. They establish neither an applied
duration nor removal of an active status. The canonical sheet-life decompile
also differs from the original bytecode on one fallback path.

## Identity and sheet request

Each selected root binding reads the current global `StatusBaseClass`,
creates its closure and assigns the named member. Those separate reads do
not establish a stable table across the selected assignments, who produced that
global or which runtime object receives the methods. In the frames below,
`s` is the supplied receiver. Argument counts include explicitly passed receivers.

| Method | Exact local behavior | Normal results |
| --- | --- | --- |
| `getStatusId(s)` | Resolve `s._getStaticActorID`, then call it with exactly `(s)`. | Tail-return every result, including zero results. |
| `getStatusData(s, q)` | Read global `statusSheet` once as `sheet` and resolve `sheet._getData`. Resolve and call `s.getStatusId(s)`, retaining its first result as `id`. Call the previously resolved function with exactly `(sheet, id, q)`. | Tail-return every `_getData` result. |
| `getObjectClassId(s)` | No reads or calls. | Exactly one result, numeric `5`. |
| `isRemovedFromDeath(s)` | No reads or calls. | Exactly one result, boolean `true`. |

The ID call in `getStatusData` requests one result: an empty return supplies
nil, and extra results are discarded. The sheet call always has three
arguments, even when `id` or `q` is nil. False, numeric zero and nil are not
converted or guarded. A change to global `statusSheet` during the ID call
does not change the cached sheet or `_getData` function used by that call.
The `_getData` member lookup precedes the `getStatusId` member lookup and call.

These five bodies do not inspect `_getStaticActorID` or `_getData`. Numeric
`5`, the returned static-actor ID, and the supplied sheet operand `q` are
different values with different producer boundaries. These bodies alone do not
define a conversion between them, a native field index, or a bridge from
`q` to a decoded CSV position. The names of the methods do not supply that
missing schema or receiver binding. The qualified published composition below
supplies additional provider evidence.

## Sheet-life inputs and calculation

`getStatusLifeAtSheet(s, u1, u2, u3, u4, u5)` has six fixed parameters,
including `s`. The five explicit inputs retain positional names here because
their domains and units are not established by this body. `u5` is unused.

The original bytecode first calls `s.getStatusData(s, 47)` and retains one
result as `b`. This request occurs before every input guard. It then tests
`u1`, `u3` and `u4`, in that order, for equality with nil. If none is nil,
it calls `u4._isAlive(u4)` and tests its first result for Lua truthiness.
Only nil and false are false in that test. Numeric zero is truthy.

When any of those three inputs is nil, or the alive result is false or nil,
the original returns exactly one result from `b * 1`. This is multiplication,
not an identity return: ordinary Lua coercion and arithmetic behavior still
apply. False or zero inputs pass the non-nil guards. For example, false or
zero in `u4` reaches its `_isAlive` lookup and can fail there.

When the alive result is truthy, the following calls run in order. Every
call in this table requests exactly one result, filling nil for an empty
return and discarding any extra results. PCs are zero-based within the
selected prototype.

| PC | Resolved member | Complete arguments | Retained name |
| ---: | --- | --- | --- |
| 16 | `s.getStatusData` | `(s, 49)` | `k` |
| 21 | `s.getStatusCompatibilityWithAdjust` | `(s, k, u1, u2, u3, u4)` | `m` |
| 30 | `s.getStatusLifeLevelAdjustGrow` | `(s, u1, u2, u3, u4)` | `g` |
| 36 | `s.getStatusLifeAdjustForLowLevelUse` | `(s, u1, u2, u3, u4)` | `l` |
| 42 | `s.getStatusLifeAdjustForHighLevelUse` | `(s, u1, u2, u3, u4)` | `h` |
| 47 | `s.getStatusLevelAdjust` | `(s, b, g, l, h, u1, u2, u3, u4)` | `a` |

The return is exactly one result from `a * m`, in that operand order.
The initial query is at PC 2 and the alive call is at PC 10. `u2` has no
nil guard. Neither query result nor any adjustment result has a local type,
range or truth guard.

Member resolution has observable ordering beyond the calls. The compatibility
member is resolved before the fresh `getStatusData` member lookup for operand
49. The level-adjustment member is resolved before the grow, low and high
members are resolved and called in turn. A helper replacing one of these
already resolved functions does not replace the function used by the pending
call. Conversely, the two sheet-data requests perform separate member reads
and need not resolve to the same function. All supplied receivers and inputs
are the original parameter values, without a fresh actor lookup.

The selected adjustment formulas are recovered below. Their composition
remains conditional on each actual member binding and normal return.
No multiplier range or time unit follows from the helper names.

## Conditional inherited life adjustment

The selected adjustment bodies supply the formula for the truthy-alive path
above. They retain positional inputs because their actual receiver and
provider meanings remain conditional. Each helper returns exactly one value.
The high-level and low-level helpers return numeric `0.7` and `1`,
respectively, without reading any input or calling another function.

`getStatusCompatibilityWithAdjust(s, k, u1, u2, u3, u4)` returns numeric
`1` when `u2` is nil or `k` equals numeric zero. Otherwise it resolves and
calls `s.getStatusCompatibilityByHand(s, u1, u2, u3, u4)`, retains its
first result `c`, and returns `c - (1 - c) * k`. Numeric zero and false
in `u2` pass its nil guard. Nil or false `k` does not take the zero branch.
There is no local clamp or numeric conversion call.

`getStatusLifeLevelAdjustGrow(s, u1, u2, u3, u4)` first calls
`s.getStatusData(s, 48)` and retains its first result `d`. If `d < 0`,
it returns one nil and skips the remaining provider. Otherwise it resolves
and calls `u1.judgeGrowColumn(u1, u4, d)` and returns exactly its first
result `g`. An empty provider return becomes nil. Nil or false `d` reaches
the comparison and can fail there. Numeric zero reaches `judgeGrowColumn`.

`getStatusLevelAdjust(s, b, g, l, h, u1, u2, u3, u4)` returns `b`
directly when `g` is nil, without resolving another member. False and zero
`g` enter its provider path. In order, that path calls:

| Resolved member | Complete arguments | Requested results |
| --- | --- | --- |
| `u2.getCommandLevel` | `(u2)` | One, `C` |
| `u1.getStateMainSkillLevel` | `(u1)` | One, `T` |
| `u2.getCommandLevelAdjustLevelMax` | `(u2)` | Two, `D` and `U` |

Set the effective comparison value `E` initially to `T`. When `T < C`
and `D ~= -1`, resolve the current global `_math` and its `min` member,
call it with exactly `(D, C - T)`, retain one result `z` and set
`E = C - z`. When `C < T` and `U ~= -1`, the corresponding call is
`_math.min(U, T - C)` and `E = C + z`. There is no receiver argument
to either `min` call. Equal values and the selected `-1` sentinel skip
that call. The function named `min` is an actual binding premise.

Next, resolve and call `u1.getGrowData(u1, C, g)` for one result `X`,
then resolve the member afresh and call `u1.getGrowData(u1, E, g)` for
one result `Y`. Compute `R = Y * (b / X)`, preserving that operation
order. The result `a` is `b - (b - R) * l` when `E < C`,
`b + (R - b) * h` when `C < E`, and `b` otherwise. Both grow calls
and the ratio calculation occur even when `E == C`. The sheet-life caller
then returns one `a * m`, with `l = 1` and `h = 0.7` only when those
selected helper bindings supply its values.

All called members are resolved separately at their stated point. Retained
results remain cached values, including the two results from the maximum
provider. Extra provider results are discarded and missing results become
nil. There are no local type/range/zero-divisor guards or protected calls.
An indexing, call, comparison or arithmetic error stops later work. Ordinary
Lua arithmetic can coerce numeric strings, but this is not a separate
conversion request. These ordinary-value checks do not characterize metatables.

The first further body on the compatibility path is
`getStatusCompatibilityByHand`. The grow path stops at `judgeGrowColumn`;
the level path stops at the three level providers, `_math.min` and
`getGrowData`. Their bodies remain uninspected. The selected formulas do
not establish an actual Sanction adjustment value, time units, invocation,
status application or expiry.

## Canonical fallback discrepancy

The canonical method's outer non-nil guard is at line 764, and its nested
alive guard is at line 768. Its fallback assignments at lines 813-814 belong
only to the outer guard's else branch. The nested alive guard has no else
branch. Therefore, with non-nil `u1`, `u3` and `u4` but a false or nil alive
result, multiplier local `L6_2` remains nil before the multiplication at
line 816. With an ordinary numeric initial sheet result, that canonical path
raises an arithmetic error. The original bytecode instead initializes the
fallback multiplier to numeric `1` on this path and returns `b * 1`.

An empty alive return supplies nil and has the same discrepancy. Truthy
alive results, including numeric zero, enter the adjustment path in both
artifacts. The canonical source is not repaired or treated as equivalent to
the original on the false-alive path.

## Published provider composition

The adopted `xivl-decomp:docs/script/sheet-globals.md`, "Sheets created by
the Judge classes," "Readers" and "Timing," records the `statusSheet`
creation request with table path `status`. Its creator/accessor facts are
`OBSERVED`, while parts of initialization ordering remain `INFERRED` or
`NOT TRACED`. Creation does not itself load row data or prove that this
particular runtime global holds the intended initialized sheet.
The publication is at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, 11938 bytes, SHA-256
`2fb50542960b10e9b875ea4eaf5cd2624d127985b32579309db03eda0ddb35dd`.

The adopted `xivl-client-structs:docs/spreadsheet-native-contract.md`,
"Registration and dispatch," "Contracts" and "Cached rows and _getData,"
records the registered `_getData` native's `SpreadSheet` receiver cast,
two integer arguments and cached lookup: the first integer selects the outer
tree and the second selects the found row's cell tree. Their interpretation
as row key and zero-based column is explicitly `INFERRED` from the poll's
key and column-counter writes. It records float column type `9` producing
a float cell, tag `1` pushing that float, and the `Which` return marshalling.
The getter loads nothing and requests no yield. Missing row or cell keys
reach the native invalid-parameter route, rather than a supported nil-cell
fallback. That publication leaves wrapper argument adjustment open. The
selected descriptor and published alias route below qualify this boundary.
This publication is at revision
`180ab8aaa49b0157fee8996abe4d27e05b588bda`, 26820 bytes, SHA-256
`71ab9936873662af20463f2462573ad71986afbb59c9f6bccf2ab35d4affd3cb`.

At the same Structs revision,
`xivl-client-structs:docs/nameplate-group-native-contract.md`, "Registration
and dispatch," "Contracts" and "Actor identity natives," records the
registered `_getStaticActorID` native's `ActorBase` receiver cast, no explicit
arguments and integer result. It masks the supplied receiver identity with
`0xFFFFF`. Calling the low 20 bits a static actor ID is `INFERRED` in that
publication, not a registry lookup performed by this getter. The publication
is 53434 bytes, SHA-256
`087bd2c913271088ee22ac3600ff27d61c36f185824d73b6ddf0c39ce0111119`.
These are adopted published findings, without inspecting new native bodies.

## Sheet descriptor and alias

`SpreadSheet._getData_inl` has three fixed parameters, including its nominal
receiver, and ignores them all. Its original bytecode and canonical source
return exactly two strings, `"self"` and `"_getData_cpp"`. It reads no global
or member and makes no call. A direct descriptor call returns those strings,
not a sheet cell. Its root binding reads the current global `SpreadSheet`
and assigns this closure under `_getData_inl`.

The adopted `xivl-decomp:docs/script/lua-call-function-bridge.md`,
"Descriptor resolution and alias installation" and "Invocation boundary,"
records a conditional registration path that calls an `_inl` descriptor with
zero arguments and two requested results. The first string `self` selects
the original registration table, not the later call's receiver. The second
string supplies the lookup key, searched in that table and, on nil, its
registered parents. With nonempty registration context, the appropriate
`_inl` method name and a resolved Lua type-6 function, the successful path
copies that function under the name with `_inl` removed. For this descriptor,
that is a lookup of `_getData_cpp` and an alias named `_getData`.

Successful alias copying introduces no argument prefix or transformation.
It copies the resolved callable value rather than retaining a live link to
the lookup key. Later changes to the selected table, parent chain or either
member can therefore matter. Lua type 6 alone does not identify the native
implementation. A failed descriptor resolution leaves ordinary registration
available and does not establish this alias or a data query.

The same published bridge separately records the successful forwarding
wrapper `0x00D07F20 -> 0x00D04BF0`: it copies all supplied arguments in order,
including index 1, and does not consume index 2 as a selector. If this wrapper
is present on the actual selected call path, `(sheet, row, column)` remains
that complete argument vector. Alias copying and this forwarding behavior
are distinct facts, conditional on the actual context, table, lookup result,
callable and subsequent mutations. This publication is at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, 16789 bytes, SHA-256
`b717a6372b09a45914fe85c153874fc22cb4694d0cc0a8b01c7fb1ffb7c43a36`.

## Conditional Sanction composition

The adopted `xivl-client-data:docs/sanction-static-rows.md`, sections
"Status identity" and "Declared status class," identifies Sanction row
`223992`, declares `/Status/GrandCompanyStatus`, and authenticates the empty
child module's requests for `/Status/StatusBaseClass` and the class definition
`GrandCompanyStatus`, `StatusBaseClass`. That source is pinned at revision
`0d4c49ceb9ea4fffb3baef6c57c47cde3f867f8c`, 13256 bytes, SHA-256
`7c3d3e1ea8ff6f1beaa1e1e4858b642cb46752bce468059a234d58aa406b787e`.
This adopts the published declaration rather than reinterpreting the child
module, SAN or raw CSV.

If the actual class definition inherits these members without replacement,
the default death predicate returns true. That local predicate does not
remove a status, prove that a caller evaluated it, or establish server death
policy. If the actual receiver's selected ID provider returns `223992` as
its first result and the sheet method resolves as described above, its data
requests pass `(sheet, 223992, 47)` and conditionally `(sheet, 223992, 49)`
to the resolved `_getData` function. Those premises are not established by
the static class declaration alone.

The adopted Data finding preserves raw zero-based CSV column 47 as the
float `10800`. The five script bodies alone do not establish the API-to-CSV
bridge. Under the published native row/column interpretation, this becomes
the queried base life value `b` only if all of these premises hold:

- The actual inherited methods resolve to the selected bodies, and the ID
  provider resolves to the published native with a successful receiver cast
  and receiver identity whose low 20 bits are `223992`.
- The cached `statusSheet` and `_getData` resolve to the intended `status`
  sheet and published native with successful `SpreadSheet` casting and
  integer argument marshalling. The successful descriptor alias selects that
  implementation, and the actual call path retains the published argument
  preservation. The descriptor's strings are not substituted for cell data.
- The selected table/schema and already loaded row/cell cache match the
  published extraction, including row `223992`, zero-based column `47` and
  its float value. The row/column interpretation retains its `INFERRED` tier.

The selected `xivl-client-data:csv/status.csv`, row `223992`, has raw
empty cells at zero-based columns `48` and `49`. Both type-header cells
are also empty. These are blank lexemes, not literal numeric zero or `-1`,
and the headers establish no native type or blank-to-Lua conversion.
The authenticated member has 43499 bytes, SHA-256
`3b09a76123b0fd8aba320dc5513e8182820fef409cf9d40f0b522b10b11d02ec`.
The selected row is CSV record 295, including the two header records.
Its identity is recorded by `xivl-client-data:manifests/tables.json` for
extraction `2012.09.19.0001` and by
`xivl-client-data:manifests/private_csv_corpus.json`. The archive declaration
pins source revision `8b38a02ce8ebf662b931092e46273251b38c58f0`,
`extracted/ffxiv-1.23b/client-data/csv.zip`, 70110686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.

Under the same table, cache, binding and argument premises, query `48`
requests `(sheet, 223992, 48)`. The two raw blanks alone cannot determine
its Lua result `d` or query `49`'s result `k`. If the actual `k` is
numeric zero or `u2` is nil, compatibility returns `1` without calling
`getStatusCompatibilityByHand`. If actual `d < 0`, grow returns nil
without calling `judgeGrowColumn`, and level adjustment returns `b`
without calling any level or grow-data provider. Together those conditions
make the original truthy-alive path return `b * 1`, conditionally
`10800 * 1`. The raw blanks do not establish those conditions. For ordinary
values, nil, false or an empty string in `d` instead fails the comparison.
No default numeric value is inferred from a blank or from a helper's name.

With those premises, the original fallback computes `10800 * 1`. The truthy
alive path instead sends that base value through the selected adjustment
formulas before multiplying their results. This does not assign time units to
the value or establish the actual result of that adjustment path. An applied
duration of 10800 seconds or three hours, expiry scheduling, status grant,
actual death removal and gear bonuses remain outside the recovered contract.
The separate
[CompanyBuffer](sanction-company-buffer-contract.md) and
[scroll](sanction-scroll-local-eligibility.md) contracts retain their own
request and application boundaries.

## Source identity and checks

The evidence class is `client_extraction`. The selected source is
`xivl-client-scripts:lua/scripts/status/statusbaseclass.lua`, authenticated
in memory against `xivl-client-scripts:manifests/scripts.json` and
`xivl-client-scripts:manifests/retail_lua_coverage.json` at revision
`1750b735bf9069323f773c141e0500335ea2af97`. The latter identifies original
resource `rq9qpr/rq9qpr89r57y9rr.le.lpb`, relative to `client/script/`.
The [archive declaration](../manifests/private_lua_corpus.json) identifies
the canonical archive. Its selected members are `status/statusbaseclass.lua`
and `gamedata/spreadsheet_u.lua`. The latter's source identity is recorded by
the same Scripts manifests and revision. Its original resource is
`39x569q9/rus596r255q_p.le.lpb`, relative to `client/script/`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Canonical LF source, 875 lines | 18790 | `132f18c5f22f9958ab5a8c665ba99f8ed1e9ae4e55674cdf46e42bac565abbfa` |
| Original LPB | 8243 | `1f12f23ed6f9e8650ceb27f862ef74fa5289a8387471b1b1d64b72ee23e5fa9a` |
| Decoded payload | 8230 | `ea3a0ff226fc049b540385cc111b38582f48270be1aa6b8f80b670192e6daa2d` |
| Sheet descriptor canonical LF source, 101 lines | 1723 | `aee20170d141ac92ee889caaa53d615914d8bb5b46515b6be85e4060d218e936` |
| Sheet descriptor original LPB | 1358 | `2c6d44d7b4c9adb69352fa295fb61f715fd0806f062d08d818c6a9ff5577fbf2` |
| Sheet descriptor decoded payload | 1345 | `c9b4f2b8eb2b446cae97bfc6f319cb36e116c3632d0a08fc13eb1428d158c064` |

The initial source selection comprises the necessary header/root bindings,
five status methods and one sheet descriptor:

| Method | Canonical lines | Original prototype / code offset / words | Root closure / assignment PCs |
| --- | --- | --- | --- |
| `getStatusId` | 4-11 | `root/proto0` / 1762 / 4 | 1 / 2 |
| `getStatusData` | 14-26 | `root/proto1` / 1841 / 8 | 4 / 5 |
| `isRemovedFromDeath` | 108-114 | `root/proto7` / 2534 / 3 | 22 / 23 |
| `getObjectClassId` | 146-152 | `root/proto11` / 2784 / 3 | 34 / 35 |
| `getStatusLifeAtSheet` | 758-820 | `root/proto37` / 7238 / 55 | 112 / 113 |
| `SpreadSheet._getData_inl` | 14-21 | `root/proto1` / 535 / 4 | 4 / 5 |

All six have zero vararg flags, upvalues and child prototypes. Fixed
parameter counts are respectively 1, 2, 1, 1, 6 and 3. ID and data tail calls
are at PCs 1 and 5. Their subsequent open-result returns at PCs 2 and 6
and final zero-result returns at PCs 3 and 7 are unreachable after normal
tail-call completion. Death and class-ID return one value at PC 1 before
an unreachable zero-result return at PC 2. Sheet life returns one value at
PC 53 before an unreachable zero-result return at PC 54.
The sheet descriptor returns two values at PC 2 before an unreachable
zero-result return at PC 3.

The adjustment selection adds only these five bodies from the same status
member, totaling 90 instruction words:

| Method | Canonical lines | Original prototype / code offset / words | Root closure / assignment PCs | Fixed parameters |
| --- | --- | --- | --- | ---: |
| `getStatusCompatibilityWithAdjust` | 216-234 | `root/proto16` / 3301 / 16 | 49 / 50 | 6 |
| `getStatusLevelAdjust` | 237-295 | `root/proto17` / 3458 / 54 | 52 / 53 | 9 |
| `getStatusLifeAdjustForHighLevelUse` | 334-340 | `root/proto22` / 4089 / 3 | 67 / 68 | 5 |
| `getStatusLifeAdjustForLowLevelUse` | 379-385 | `root/proto27` / 4394 / 3 | 82 / 83 | 5 |
| `getStatusLifeLevelAdjustGrow` | 476-495 | `root/proto32` / 5071 / 14 | 97 / 98 | 5 |

All five have zero vararg flags, upvalues and child prototypes. No further
status/helper body is selected. Their original instructions and a separate
literal canonical parser agree on focused ordinary-value fixtures for the
formula, nil guards, false/zero distinctions, fresh member reads, cached
results, one/two-result calls and error prefixes. Rejecting controls change
the query operand, constants, guard polarity and call/return widths. Separate
composition fixtures adopt the sheet-life caller above and preserve the raw
blank-cell distinction. These checks do not establish a native cell type or
blank conversion.

Authentication uses `xivl-client-scripts:tools/retail_script.py`,
`decode_lpb`, and `xivl-client-scripts:tools/build_quest_contracts.py`,
`ChunkReader` and `instruction`, at the same Scripts revision. Their
identities are respectively 3555 bytes, SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`,
and 34038 bytes, SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`.
A focused
original-instruction interpreter and a separate literal canonical parser
check exact frames, lookup/call order, open returns, scalar truncation,
empty results, nil/false/zero, ignored inputs and thrown-error prefixes.
Literal fixtures distinguish the canonical fallback discrepancy. Rejecting
controls change query operands, guards, truth polarity, class output,
provider namespace, call/result widths and arithmetic. Separate literal
descriptor fixtures check its result order and width, ignored parameters,
registration-table versus call-receiver meaning, successful callable copying
and unchanged argument order. Conditional alias/forwarding fixtures use the
published bridge contract rather than executing native code.

These are source checks, not retail execution. All calls are unprotected:
a lookup or call error stops subsequent work, and no local exception cleanup
is present. A multiplication can fail after the earlier calls have completed.
The ordinary-value fixtures do not characterize provider metatables, helper
side effects, the sheet schema, actual class/receiver resolution or historical
invocation. Those remain the first interpretation and application boundaries.
