# Echo pronoun conversion requests

`DesktopWidget.convertPronouns` prepares ordered replacement requests and
returns one value. It directly recognizes a signal pattern under one control
condition. Text substitution is requested through its
[replacement helper](echo-token-replacement.md). The
[parsed-key 107 caller](local-echo-client-request.md#selected-request-and-local-result)
passes its freshly read input to this method and forwards its result to the
saved echo method.

## Input, signal request and result

The original method has two fixed parameters, receiver `D` and input `S`,
with no variadic tail. Missing parameters become nil and extra actual values
are discarded. Exact `S == ""` returns that empty string immediately, before
indexing `D`. Every other value reaches dynamic lookups without a type guard.
In particular, nil, false and numeric zero are not the empty-string case.
The parent alone does not establish a complete accepted-input type domain.

For nonempty input, it reads `D.work.lockUserControl`. Only exact Boolean
false requests `_string.match(S, "<sign[0-7]>")`, retaining one result `M`.
A result other than nil requests `_string.sub(M, 6, 6)`, forwards all of its
results to `tonumber`, retains one numeric-conversion result and adds 1.
It then calls the freshly obtained `D.executePlayerSignal(D, value)`,
discarding every result. It does not loop over signal matches or itself
remove the matched text. Other lock values skip this entire signal request.

If `_string.match` and `_string.sub` have the standard Lua 5.1 string-library
behavior, the unanchored pattern selects the first literal lowercase
`<sign0>` through `<sign7>` anywhere in the input. Adjacent text needs no
separator. The extracted sixth byte selects signal values 1 through 8.
`<SIGN1>`, `<sign8>`, `<sign10>` and incomplete brackets do not match this
pattern. This conditional interpretation follows the
[Lua 5.1 string functions and patterns](https://www.lua.org/manual/5.1/manual.html#5.4),
whose indexing assumes bytes rather than Unicode characters. The actual
`_string`, `tonumber` and signal bindings are not established by this parent.

After the optional signal call, replacement preparation proceeds even when
the input contains no listed token. Each completed `replaceString` call
retains exactly one result as the next input. Missing results become nil,
extra results are discarded, and false, zero or nil do not stop the sequence.
Normal completion returns exactly one final value, including an explicit nil.
There is no protected-call recovery or synthesized false result: a lookup,
call, comparison, arithmetic or concatenation failure can prevent that return.

## Ordered replacement preparation

The method reads global `worldMaster` once, gets `_getMyPlayer` from that
value, calls it with that same value as receiver, and saves one result `P`.
It then performs the following sequence, conditional on each earlier operation
completing normally. `R(token, value)` denotes a fresh method lookup and call
`D.replaceString(D, currentInput, token, value)`, retaining one result. It
denotes a request, not a proved replacement algorithm.

| Order | Prepared request and condition |
| --- | --- |
| 1 | Obtain all results of `D.getPlayerName(D)`, forward them after `D` to `D.deleteChineseName`, and save one result `N`. Request `R("<me>", N)`, then `R("<p0>", N)`. The name helper is called once. |
| 2 | Call `D.getMainTargetCharacter(D)` and retain one result `T`. If `T` is not nil, forward all results of `T._getLocalizedDisplayNameForChat(T)` after `D` to `D.deleteChineseName`, retain one result and request `R("<t>", result)`. |
| 3 | Read `D.work.subTargetName`. If that value differs from `""`, freshly read `D.work.subTargetName` again, pass that second value to `D.deleteChineseName(D, value)`, retain one result and request `R("<lastst>", result)`. Nil, false and zero pass the empty-string comparison. |
| 4 | Call `D._getLastAttacker(D)` and retain one result `A`. If `A` is not nil, forward all results of `D.getActorName(D, A)` after `D` to `D.deleteChineseName`, retain one result and request `R("<lastat>", result)`. |
| 5 | Iterate numeric indices `i = 1` through `8`. Call `D.isPartyMemberActorMe(D, i)`, retaining one result. Only exact false prepares a replacement: forward all results of `D.getPartyMemberDisplayName(D, i)` after `D` to `D.deleteChineseName`, retain one result and request `R("<p" .. tostring(j) .. ">", result)`. Counter `j` starts at 1 and increments only for such replacements. |
| 6 | Call `P.getHP(P)` and `P.getHPMax(P)` independently, forwarding each complete result tail to a separately obtained `tostring` and retaining one string result each. Request `R("<hp>", hpText .. "/" .. maxText)`. |
| 7 | Freshly call `P.getHP(P)` and `P.getHPMax(P)`, retaining one result each. Only `max > 0` requests `R("<hpp>", tostring(_math.floor((hp / max) * 100)) .. "%")`. The floor result tail is forwarded to `tostring`; one string result is retained. |
| 8 | Repeat orders 6 and 7 with `getMP`, `getMPMax`, `<mp>` and `<mpp>`. These are new getter calls, not reused HP or earlier MP values. |
| 9 | Forward all results of `P.getTP(P)` to `tostring`, retain one result and request `R("<tp>", result)`. |
| 10 | Call `D.getStaticWidget(D, 10)`, retain one result `W`, then call `W.getPlayerMapPosition(W, "CustomControl_MiniMap")`, retaining exactly two results `X, Y`. Only when both are at least zero, request `R("<pos>", "( X: " .. tostring(X) .. ", Y: " .. tostring(Y) .. " )")`, with one result from each `tostring`. |

The party token counter is compacted over exact-false tests. For example,
if index 1 is skipped and index 2 qualifies, the request pairs `<p1>` with
the name-helper result for index 2. Nil and other non-false test results
skip the request and leave `j` unchanged. The token construction above uses
the actual dynamic `tostring` result; `<p1>` through `<p8>` assumes its usual
numeric conversion.

All displayed receiver operands are explicit. `P` is saved once and reused
for status getters, while `getPlayerName` and `getActorName` are methods
obtained from `D`. Name-helper result tails preserve nil, false and zero
operands on their way to `deleteChineseName`. Its one-result capture is reused
for `<me>` and `<p0>` only. Later lookups are fresh. Each replacement method
is obtained after its replacement value has been prepared. In contrast, a
`deleteChineseName` method that receives a name-getter tail is captured before
that getter runs. A side effect cannot replace that already captured method.

## Text and actor boundaries

The parent supplies the exact bracketed spellings above. It does not
establish how `replaceString` matches them, how many occurrences it changes,
whether replacements are rescanned, or what it does with case variants,
unknown or malformed tokens, non-string input or replacement values.
It supplies no general delimiter parser, case folding or Unicode rule.
The name `deleteChineseName` supplies no proved normalization semantics.
The [replacement contract](echo-token-replacement.md#guard-frame-and-results)
qualifies the nil-replacement bypass and conditional native request. Actual
converted text still needs the matching library/native frame and helper
values. The name-normalization helper remains a separate source boundary.

The [standard-emote contract](standard-emote-command-contract.md#menu-and-typed-callers)
describes `getCurrentTargetCharacter` and a self-clearing test in its own
caller. This method instead requests `getMainTargetCharacter`; neither that
getter nor the emote caller's self-clearing rule is established here.
`xivl-decomp:docs/net/target-cycle-and-pick.md` describes target-selection
algorithms but does not close this differently named helper edge.

Matching native publications can qualify two requests, under actual binding,
receiver, context and post-preparation frame conditions:

- `xivl-client-structs:docs/desktop-native-call-contract.md`, LuaControl
  returns, owns `_getMyPlayer`'s native control and registry-pool return.
  `xivl-decomp:docs/actor/actor-instantiation-and-self-player.md`, Self player,
  and `xivl-decomp:docs/event/player-profile-work-accessors.md`, Owner join, retain the
  conditional join between the published current-player holder and a later
  getter context. This method proves only the saved Lua result `P`.
- `xivl-client-structs:docs/achievement-target-native-contract.md`, Target
  natives, records `_getLastAttacker` with no explicit arguments, returning
  nil for an unresolved control or zero control byte `+0x5C`, and otherwise
  pushing the control. The last-attacker interpretation remains inferred
  from its name there. This method's nil comparison does not identify an
  actual actor or display name.

Those publications are adopted at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce` and Structs revision
`180ab8aaa49b0157fee8996abe4d27e05b588bda`. Actual helper/native bindings,
getter values, object identity, name values, locale, final echo/log output,
server behavior and historical invocation remain unestablished.

## Source identity and checks

Extraction `2012.09.19.0001` is identified by
[`scripts.json`](../manifests/scripts.json),
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`private_lua_corpus.json`](../manifests/private_lua_corpus.json).
The archive declaration pins source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`.

| Input | Bytes | SHA-256 |
| --- | --- | --- |
| Canonical `lua/scripts/widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| Original `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` |
| Decoded payload | 213474 | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| Retained Lua archive | 14385427 | `0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31` |

The canonical member has 26564 lines. The publication normalization is exact
CRLF-pair-to-LF replacement. The method occupies canonical lines7439-7714.
Original `root/proto128` has 237 instructions, code offset79850, two fixed
parameters, raw vararg0, zero upvalues and no nested prototypes. Root PCs384-386
load `DesktopWidget`, create this closure and assign it with the constant
RK key `convertPronouns`. PCs and offsets below are zero-based.

| Parent behavior | PCs | Decoded-payload offsets |
| --- | --- | --- |
| Empty return, lock test and signal request | 0-24 | 79850-79946 |
| Saved getter result and name/target requests | 25-92 | 79950-80218 |
| Party iteration and compact token counter | 93-123 | 80222-80342 |
| HP and MP preparation and positive-maximum tests | 124-196 | 80346-80634 |
| TP, map-position guard and replacement | 197-234 | 80638-80786 |
| One-value final return | 235 | 80790 |

`tools/retail_script.py` decodes the authenticated original in memory.
`ChunkReader` and `instruction` in `tools/build_quest_contracts.py` expose the
selected header, binding and parent operands. A bounded parent-instruction
check passed 80 authored cases and rejected eleven changes to entry/lock,
signal index, saved-result width, replacement-result width, party bound,
party exact-false test, positive maximum, percentage multiplier, position guard
and final-return width. Cases cover
empty/nil/false/zero input, first signal matches, malformed spellings,
fresh reads, compact party numbering, skipped requests, explicit nil-bearing
tails and missing lookups. Its ASCII string and finite numeric library
models and opaque helper stubs establish only those conditional models.
No helper body or retail client was executed.
