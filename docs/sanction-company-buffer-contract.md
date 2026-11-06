# Sanction CompanyBuffer client contract

`PopulaceCompanyBuffer` selects dialogue and menu results, requests character
schedulers, and exposes separate effect and talk-cleanup callbacks. Its five
methods do not establish a status grant, status duration, seal payment, or
server eligibility. The Sanction association is established separately by
`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md`,
lines 469-499.

## Source identity and locators

The source is the retail 1.23b extraction `2012.09.19.0001`, decoded script
`chara/npc/populace/populacecompanybuffer.lua`. The
[script manifest](../manifests/scripts.json),
[retail resource census](../manifests/retail_lua_coverage.json), and
[callsite metadata](../lua/scripts/chara/npc/populace/populacecompanybuffer.calls.json)
retain its corpus and resource coordinates. The canonical source is a restricted
local input, as described by the [Lua corpus contract](../lua/README.md).

| Input | Bytes | SHA-256 |
|---|---:|---|
| Canonical script | 6373 | `122a9211b5433f99e896db126fc9eff8e18982ca9f5b6b2f13c0751420cbd0ac` |
| Original LPB | 2454 | `54b86a001a871c087a4d89ff87d2f1df667a1cddead20695aee47cbcc57df96d` |
| Decoded Lua 5.1 payload | 2441 | `5a7239727c3f7cfc7fa7be8d7f38fc0316e0d2fee5afbf57fbea535d34d90c62` |

The original resource is
`729s9/wu7/uvupy975/uvupy9757vxu9wl8p445s.le.lpb`, relative to retail
`client/script`. It uses the XOR-`73` LPB wrapper. The canonical archive named
by [the decoded-corpus manifest](../manifests/private_lua_corpus.json) has
SHA-256 `0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Its member `chara/npc/populace/populacecompanybuffer.lua` matches the canonical
script pin above.

All PCs below are zero-based within the named prototype. A payload instruction
starts at `code offset + 4 * PC`. Each root `CLOSURE` is followed by a
`SETTABLE` binding to the named field of global `PopulaceCompanyBuffer`.

| Method | Prototype | Code offset | Instructions | Root closure / binding PC | Canonical lines |
|---|---|---:|---:|---|---|
| `initForEvent` | `root/proto0` | 374 | 45 | 8 / 9 | 11-67 |
| `eventTalkWelcome` | `root/proto1` | 841 | 170 | 11 / 12 | 70-257 |
| `eventTalkBufEffect` | `root/proto2` | 2014 | 12 | 14 / 15 | 260-278 |
| `eventTalkBufEffectAfter` | `root/proto3` | 2182 | 15 | 17 / 18 | 281-303 |
| `eventTalkStepBreak` | `root/proto4` | 2371 | 3 | 20 / 21 | 306-313 |

The methods have respectively 1, 3, 2, 2, and 1 fixed parameters including
`self`, with no varargs, upvalues, or nested prototypes. In this page `npc`
means supplied `self`, `player` means the supplied second parameter, `flag`
means Welcome's third parameter, and `company` means
`npc.work.grandCompanyNumber`. These are caller-supplied values and dynamic
member lookups. The bodies do not resolve an actor, acquire a fresh player, or
authenticate their caller.

## Initialization requests

`initForEvent` requests the following in order. Calls discard results except
for the actor-class query.

| PC | Request |
|---:|---|
| 3 | `npc:_loadTextDataPermanently(10256, "populaceCompanyBuffer")` |
| 17 | `npc:initWork(nil, schema)` where the schema declares `grandCompanyNumber` and `companyRank`, each as `integer8` |
| 19 | `npc:getActorClassId()`, retaining one result |
| 43 | `npc:_setGroundOn(false)` |

The actor-class comparisons at PCs 20, 26, and 32 assign company 1 for 1500388,
2 for 1500389, and 3 for 1500390 (writes at PCs 23, 29, and 35). No company
write occurs for another result. The initial value supplied by `initWork` is
outside these bodies. PC40 assigns `npc.work.companyRank = 13` on every path.
PC44 returns zero values. The `initWork` call has exactly three arguments
including the receiver. Its middle argument is an explicit nil, not an
omitted argument.

## Welcome selection and rank boundary

Welcome reads `player:_getBelongGrandCompany()` at PC4 and retains one result,
called `belonging` here. It starts with row 2 and menu admission false
(PCs 0-2). PCs 5-35 select the following row and admission boolean.

| Condition, in evaluation order | Selected row | Menu admission | Rank read |
|---|---:|---|---|
| `belonging == 0` | 20 | false | none |
| `belonging ~= company` and `flag == false` | 17 | false | none |
| `belonging ~= company`, flag is not false, rank < 27 | 17 | false | PC19 |
| `belonging ~= company`, flag is not false, rank >= 27 | 18 | true | PC19 |
| `belonging == company`, rank < 27 | 15 | false | PC29 |
| `belonging == company`, rank >= 27 | 2 | true | PC29 |

Both rank reads are exactly
`player:_getGrandCompanyRank(belonging)`, retaining one result. The strict
comparisons are at PCs 20 and 30. The `flag` comparison at PC13 tests equality
with false, not truthiness: nil and numeric zero do not take that rejection
branch. The flag is not examined on the same-company path. Rank 27 takes the
upper branch. A rank value that ordinary Lua cannot compare with 27 raises an
error before the salute request. There is no local type or nil guard.

After selection, PC41 requests `npc:doSalute(company,
npc.work.companyRank)` and retains one result. The rank passed here is the
work field initialized to 13, not the freshly read player rank. Only a result
equal to numeric zero admits the scheduler branch (PC42). If menu admission
is false, that branch requests scheduler 353959936 at PC48. Otherwise it
selects 84090880, 84094976, or 84099072 for company 1, 2, or 3 and requests it
at PC72 (selection PCs 50-69). For another company it selects zero and makes
no scheduler request. A nonzero, false, or nil salute result skips this
initial scheduler branch.

Every normally continuing path then requests, in order:

1. `npc:startCliantTalkTurn(2, player)` at PC76.
2. `npc:_wait(1.5)` at PC79.
3. `npc:say(npc, selectedRow, 0, company)` at PC86.

Each discards all results. Rows 20 and 17 return exactly one numeric zero at
PC92 after these requests (tests PCs 87-90). Row 15 reaches the menu even
though its admission boolean is false.

## Menu arguments and scalar results

At PC105 Welcome requests
`worldMaster:askMultipleTextMacro(npc, npc, 1, 4, 3, 0, admission, true, true)`.
There are exactly ten arguments including the global `worldMaster` receiver,
and exactly one retained result. The numeric positions and booleans are the
caller's operands. The provider's mapping of text rows, enabled choices,
cancel actions, and returned values is outside these five bodies.

| Retained result | Local behavior | PCs |
|---|---|---|
| Its ordinary Lua `type` is not `"number"` | Return one numeric zero | 109-113 |
| Numeric 1 | Return one numeric one | 114-117 |
| Numeric 2 | Make the explanation requests below, then ask again | 119-162, 165-166 back to 94 |
| Any other number | Return one numeric zero | 163-164 |

The caller does not coerce strings or recheck admission after the answer.
Even when admission is false on row 15, a provider result of numeric 1 reaches
PC117 and returns one. This is a conditional client result contract, not
proof that an interactive widget permits that choice. Welcome does not call
either effect callback or apply a status before returning one.

Numeric 2 makes these requests in sequence, with no additional wait:

| PC | Request |
|---:|---|
| 123 | `npc:_runCharaScheduler(353959936)` |
| 130 | `npc:say(npc, 10, 0, company)` |
| 133 | `npc:_runCharaScheduler(353968128)` |
| 140 | `npc:say(npc, 11, 0, company)` |
| 143 | `npc:_runCharaScheduler(353959936)` |
| 150 | `npc:say(npc, 12, 0, company)` |
| 156 | `worldMaster:say(npc, 13, 180)` |
| 161 | `worldMaster:say(npc, 14)` |

All discard results. The last two calls have four and three total arguments,
respectively, including `worldMaster`. The literal 180 is a fixed dialogue
operand. These instructions do not apply a 180-minute status, derive a
duration, or request a payment. Repeating the explanation repeats the menu
with the existing admission value, without repeating the player belonging or
rank queries (PC166 jumps to PC94). Each explanation iteration freshly reads
`npc.work.grandCompanyNumber` at PCs 129, 139, and 149 for the company operands
of rows 10, 11, and 12. A provider that changes this work field can therefore
change those dialogue operands while admission remains unchanged.

## Effect callbacks and cleanup

| Method | Ordered requests | Return |
|---|---|---|
| `eventTalkBufEffect` | PC4 `npc:say(npc, 8, 0)`; PC7 `npc:_runCharaScheduler(68378624)`; PC10 `npc:_wait(2)` | Zero values at PC11 |
| `eventTalkBufEffectAfter` | PC2 `player:_runCharaScheduler(67108924)`; PC5 `npc:_wait(2)`; PC8 `npc:_runCharaScheduler(83906560)`; PC13 `npc:say(npc, 9, 0)` | Zero values at PC14 |
| `eventTalkStepBreak` | PC1 `npc:finishCliantTalkTurn()` | Zero values at PC2 |

Each listed call discards all results. BufEffect does not use its supplied
second parameter. BufEffectAfter uses the supplied second parameter for its
first scheduler request, with no fresh actor lookup. Neither callback checks
company, rank, menu result, or status. There is no local status or seal write.

Welcome has no `finishCliantTalkTurn` call on its ordinary exits. StepBreak
contains only the cleanup request and return. Which event path invokes that
callback, including cancellation, remains outside these bodies. All requests
are direct calls with no protected-call or local exception cleanup. For
example, a failing salute prevents talk start, and a failing initial `say`
occurs after talk start and wait but prevents the menu (Welcome PCs 41, 76,
79, 86, 105). A request error stops the remaining requests in that callback.

## Interpretation and verification limits

The original Lua 5.1 instructions establish branch polarity, supplied
receivers, exact call argument widths, discarded versus retained results,
and zero-value versus scalar returns. The canonical five-method decompile
agrees with focused authored-provider probes for company/rank boundaries,
false versus nil/zero, repeated explanation, scalar choices, scheduler order,
and request-error reachability. The explicit nil in `initWork` and the
different `worldMaster:say` widths are preserved. This agreement is a source
comparison, not retail execution.

These conclusions assume ordinary Lua equality, numeric comparison and
`type`, stable method bindings, and successful earlier requests. Scheduler
completion, wait units and yielding, `initWork` initialization, salute
semantics, text/macro expansion, and talk-turn ownership require their own
provider evidence. Dynamic method replacement, actor binding, and the
invoking event frame remain unresolved.

The five bodies do not establish historical invocation, server-side
acceptance, seals or costs, actual status grant or duration, death or expiry
behavior, or equipment-stat application. The separate effect requests are
presentation requests whose native and server consequences are not recovered
by this contract.
