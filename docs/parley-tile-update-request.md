# Parley tile update requests

`NegotiationJudge.updateNegotiationWidget` conditionally requests a desktop
update for `Ask/NegotiationWidget`, forwarding six fixed data positions.
The selected desktop helper looks up that path, forwards its complete
variadic tail to a nonnil result's `updateAskParameter`, and returns one
Boolean. Under matching callback binding and delivery, numeric codes 1-12
request a tile-data assignment, icon/count presentation and a storyboard
command. These are local request contracts, without evidence of actual
native dispatch, applied storage, rendered tiles or gameplay effects.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
The original instructions own the argument widths and control flow below.
The displayed canonical decompile loses the desktop's full tail and damages
the callback's code 1-11 routing.

## Judge request and actor guard

Write the Judge frame as `(J,A,U,N,K,I,V,X,Y)`. It has nine fixed parameters
and no varargs. J and U are unused. Missing positions become nil and excess
positions are unused. The body does not resolve A from a global player or
test actor identity itself.

It looks up `isPlayer` on A, calls the selected function with exactly A,
and keeps one result P. No result becomes one nil position and excess
results are discarded. Only P equal to Boolean true reaches the desktop
request. Nil, false, numeric zero, string `"true"` and other truthy values
skip it. The method's name does not authenticate its actual binding or
establish that A is the local player.

On the admitted branch, the helper reads the current global `desktopWidget`
as D after the predicate returns. It freshly captures D's
`updateEventModeWidget` function and requests exactly
`updateEventModeWidget(D,"Ask/NegotiationWidget",N,K,I,V,X,Y)`.
The six data positions retain their order and count, including explicit,
missing and trailing nils. K, I, V, X and Y undergo no local type, range or
value check. N is not validated here either.

The request keeps one desktop result R, padding an empty return with nil
and discarding extras. Its exact-false comparison has branches that
reconverge without another request or effect. Every normal Judge path
returns exactly zero values. Neither false nor any other normally returned
desktop result becomes the Judge's result or requests a retry.

The fresh global read permits the predicate to affect which desktop and
method are subsequently selected. Lookup and call errors propagate. A
failed predicate operation prevents the desktop lookup; a failed desktop
operation prevents normal return. There is no local error handler or
rollback.

## Desktop lookup and complete tail

The connector's `DesktopWidget.updateEventModeWidget(D,P,...)` has two fixed
parameters and a complete variadic tail. P is passed unchanged, without a
path conversion or default. Missing fixed positions become nil. The helper
first requests `getWidget(D,4,P)` and keeps exactly one result C. No result
becomes nil and extras are discarded.

| First getter result | Reached continuation | Normal result |
| --- | --- | --- |
| Exactly nil | No callback lookup or call. | One Boolean false. |
| Any nonnil value C | Freshly look up `updateAskParameter` on C, then request `updateAskParameter(C,...)` with the complete incoming tail. Discard every callback result. | One Boolean true after normal callback return. |

False and numeric zero are nonnil and attempt the callback lookup. They are
not locally rejected as invalid widgets. Lookup or call failure propagates
instead of producing the normal true result. A normally returned false,
nil or zero from the callback is discarded and does not change that result.

An empty tail supplies only C to the callback. One nil supplies an explicit
second argument. Values after nil and trailing nils preserve their positions
and count. This helper performs no unpacking, suffix truncation or fallback
to another widget. Its supplied D remains the lookup receiver; it does not
read global `desktopWidget` itself.

Composing the Judge with this helper requires its dynamic desktop method to
resolve to the selected implementation and prerequisite operations to
complete normally. The reached lookup is then
`getWidget(D,4,"Ask/NegotiationWidget")`. A nonnil first result C receives
the six-position callback tail `(N,K,I,V,X,Y)`. The desktop's Boolean is
still discarded by the Judge. No lookup hit, callback binding, native
delivery or widget identity is established by this composition alone.

## Selected tile callback

Write the callback frame as `updateAskParameter(C,N,K,I,V,X,Y)`. It has seven
fixed parameters and no varargs. Missing positions become nil and excess
positions are unavailable to this body. Only the prologue, tile routing,
tile requests and their shared normal return are covered here. X and Y are
unused on this selected path.

The original compares N with numeric literals 1 through 12, in ascending
order, using Lua equality. Each matching comparison jumps to the same tile
body. Numeric N and numeric N.0 match the same branch. Nil, false, true,
zero, fractional values and string spellings such as `"1"` do not enter
this body. This is a finite equality selection, without coercion or a
general numeric range test. Behavior after no tile comparison matches is
outside this finding.

For a matched numeric N, the callback makes these requests in order:

1. `negotiationWidgetSetData(C,N,K,I,V)`, discarding all results.
2. `setIcon(C,"Button_ItemIcon_"..N..":IconControl_ItemIcon",I)`,
   discarding all results.
3. `setVisibility(C,"Button_ItemIcon_"..N..":IconControl_ItemIcon",true)`,
   discarding all results.
4. Read the current global `tostring`, call it with exactly V and retain
   one result T. An empty return becomes one nil T and extras are discarded.
5. After that conversion returns, freshly capture `setText` on C and request
   `setText(C,"Button_ItemIcon_"..N..":TextBlock_NumberOfTopics",T)`,
   discarding all results.
6. `setVisibility(C,"Button_ItemIcon_"..N..":TextBlock_NumberOfTopics",true)`,
   discarding all results.
7. `_sendStoryboardCommand(C,nil,"ProgressBar_NegotiationGauge","UILuaCommands.SoundPlayIconSet")`,
   discarding all results.
8. Return exactly zero values.

Each reached method is looked up afresh on the same supplied C. There is
no cached work object, direct work lookup, declaration or member assignment
in this callback path. The selected setter call is the local assignment
boundary described below. The two visibility requests are distinct fresh
lookups, and a preceding helper may affect later method bindings.

The `tostring` call is a request to the actual global function, not proof
that it is the ordinary library implementation. Its result is not locally
required to be a string. A supplied nil, false or zero K/I/V remains
unchanged in the setter and icon positions; V alone goes through the
conversion request for count text. A nil/false/zero T remains one supplied
text position. There is no local positivity, icon-validity, row or count
check. Standard Lua numeric concatenation supplies the matched N's name
suffix; no separate `tostring(N)` call occurs.

Every later operation requires the preceding one to complete normally.
False, nil or zero helper results do not stop the sequence. A lookup,
concatenation, conversion or call error propagates and can prevent later
requests. Earlier requests are not rolled back. The final command spelling
establishes a request, without proving a sound or animation effect.

## Setter, storage and readback composition

The [tile-data assignment contract](parley-tile-data-assignment.md), pinned
at revision `ce64feff79fa4dbb3f8792815cc95da39cc7526f`, owns
`negotiationWidgetSetData(C,N,K,I,V)`. If the callback's captured method
resolves to that implementation, matched numeric N requests assignments
of K to `C.work.keyN`, I to `C.work.iconN` and V to `C.work.valueN`, in that
order. Each assignment reads `C.work` afresh. Its zero-value return does
not prevent the callback's later presentation requests.

The [getter contract](parley-topic-data-values.md), revision
`fda05be9a16163bf853e88ba941dd166e842a754`, owns later fresh reads and their
three-position result. The
[initializer's storage boundary](parley-initial-state-request.md#work-declaration-and-direct-assignments)
and the getter's selected declarations distinguish requested widths from
installed storage, conversion and actual Lua values. These publications are
adopted without another setter, getter or declaration-body study.

The callback establishes a supplied writer request and subsequent icon/text
requests. It does not prove that the same work objects accepted the writes,
that later reads preserve K/I/V, or that any value is a valid row, icon
resource, item or gameplay count. Actual matching Judge/desktop/callback/
setter bindings, complete delivered frame, receiver identity, storage and
readback remain separate premises. The
[coarse widget boundary](parley-target-gate.md#negotiation-widget-boundary)
owns other update codes. Timer behavior, scoring, valid server sequences,
settlement and historical invocation are not established here.

## Sources and original locators

The canonical members matched [scripts.json](../manifests/scripts.json).
The containing archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json): 14,385,427
bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only. Paths in the
following table are relative to `lua/scripts/`.

| Canonical member | Bytes | SHA-256 |
| --- | ---: | --- |
| `judge/negotiation/negotiationjudge.lua` | 4512 | `a617909b7f43c849d11231033dd2714cfbc7b0a33e2e0bc9e03d2a0eef92c0c5` |
| `widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/ask/negotiationwidget.lua` | 48254 | `68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3` |

[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns the
following original and decoded payload identities. Original paths are
relative to `client/script/`.

| Source | Original path | Original bytes | Original SHA-256 |
| --- | --- | ---: | --- |
| Judge | `0p635/w53vq19q1vw/w53vq19q1vw0p635.le.lpb` | 1907 | `90823b625d2a41ee5d16b6d55aa9b85f03c178c91c8e9517155d713432c672a9` |
| Desktop | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` |
| Widget | `n1635q/9rz/w53vq19q1vwn1635q.le.lpb` | 15618 | `dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1` |

| Decoded Lua 5.1 payload | Bytes | SHA-256 |
| --- | ---: | --- |
| Judge | 1894 | `184d55b038ab4e5089af58ecd9037844a39d45b9b28ca01aa7d63fa8168d6ada` |
| Desktop | 213474 | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| Widget | 15605 | `33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd` |

The manifests and decoding/parser tools were checked at revision
`ce64feff79fa4dbb3f8792815cc95da39cc7526f`. Prototype indices and PCs below
are zero-based; code offsets exclude the LPB wrapper. All three selected
prototypes have zero upvalues and no children.

| Method | Canonical definition/binding | Original prototype and code offset | Words | Fixed parameters / raw vararg |
| --- | --- | --- | ---: | --- |
| `NegotiationJudge.updateNegotiationWidget` | 138-164 | `root/proto4`, 1417 | 21 | 9 / 0 |
| `DesktopWidget.updateEventModeWidget` | 26338-26356 | `root/proto557`, 211802 | 13 | 2 / 3 |
| `NegotiationWidget.updateAskParameter` | 1147-1632 | `root/proto7`, 8830 | 449-word envelope | 7 / 0 |

The Judge root closure/assignment PCs are 20/21. The desktop loads its key
at root PC1974, creates the closure at PC1975 and assigns it at PC1976.
The callback root closure/assignment PCs are 29/30.

| Selected operation | Original locator |
| --- | --- |
| Judge actor lookup, predicate result and exact-true guard | SELF PC1; CALL PC2 B=2,C=2; EQ PC3. |
| Fresh desktop method and fixed six-position data tail | GETGLOBAL PC5; SELF PC6; CALL PC14 B=9,C=2. |
| Judge result comparison and zero return | EQ PC16; converging jumps PC17/18; RETURN PC19 B=1. |
| Desktop getter, nil test and initial false | LOADBOOL PC0; CALL PC4 B=4,C=2; EQ PC5. |
| Desktop callback and success result | SELF PC7; VARARG PC8 B=0; CALL PC9 B=0,C=1; LOADBOOL PC10; RETURN PC11 B=2. |
| Tile numeric N comparisons | PCs `7+3*(N-1)`, N=1-12; matches reach PC42. |
| Setter, icon and first visibility calls | PCs 47, 54 and 61, all C=1. |
| Conversion, later text lookup and call | CALL PC64 B=2,C=2; SELF PC66; CALL PC72 B=4,C=1. |
| Second visibility and storyboard calls | PCs 79 and 84, all results discarded. |
| Tile normal continuation | JMP PC85 to shared RETURN PC448 B=1. |

The callback study covers PCs 0-85 and its shared RETURN PC448. Nonmatching
tile routing reaches PC87, where this interpretation stops. The remaining
callback codes and other helper bodies are outside this finding.

The desktop canonical display assigns the varargs to one local and supplies
that local to the callback. Original open `VARARG` and `CALL` preserve the
entire tail, including its empty and nil-bearing cases. The callback's
canonical prefix has empty code 1-11 branches followed by a separate code12
tile block. Original comparison/jump paths put every numeric match from
1 through 12 into the common tile body. The original instructions resolve
both decompiler discrepancies; the display does not impose those losses.

## Verification

Checks used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. They authenticated
archive/member/original/payload identities, non-reparse input paths,
complete parsing and each selected root binding/header. Original-instruction
evaluation matched independent request oracles across actor and selector
types, nil/false/zero, missing/excess positions, full variadic tails, result
widths, dynamic desktop/method changes, ordered requests and reached errors.
The desktop's separate nil/false and nonnil/true results were tested directly.

Canonical evaluation checked the selected prefix and separately identified
shared normal-return suffix, retaining the two known display discrepancies
rather than asserting full agreement. Original execution was bounded before
the excluded callback comparison. Rejecting controls changed actor and
operand slots, exact guards, Boolean return paths, open/fixed widths,
selector type/value, setter/icon/text/conversion/storyboard operands and
normal return widths. The exact-false comparison and discarded-result widths
also received instruction-level checks where changing them had no observable
effect before the converged return. No raw body, listing, payload, AST or
instruction vector is retained. No new native body, row, form, build or
client/runtime execution was used.
