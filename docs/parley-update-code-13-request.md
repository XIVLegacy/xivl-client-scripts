# Parley update code 13 requests

For numeric update code 13, `NegotiationWidget.updateAskParameter` requests
visibility false for a supplied slot's icon and count text. It then requests
one storyboard command selected by an exact numeric-zero comparison on
the second payload position. An exact Boolean true in the fourth payload
position adds an ordered wait/show/wait/hide request sequence for the icon.
Every call discards its results and every normal path returns zero values.

This is recovered retail 1.23b Lua from extraction `2012.09.19.0001`.
The requests establish no applied visibility, sound, timing, animation,
data deletion, accepted move or historical Parley outcome.

## Fixed frame and selected branch

Write the complete callback frame as `(C,N,S,H,U,F,V)`: receiver, update
code and five supplied payload positions. The original has seven fixed
parameters and no varargs. Missing positions become nil and excess positions
are unavailable to the body.

| Position | Selected code 13 use |
| --- | --- |
| C | Same supplied receiver for every method lookup and request. |
| N | Must equal numeric 13 at this branch's guard. |
| S | Concatenated directly into icon and count part-name strings. |
| H | Compared with numeric zero to select a storyboard command. |
| U | Unused. |
| F | Compared with Boolean true to select the optional icon sequence. |
| V | Unused. |

The [published callback prefix](parley-tile-update-request.md#selected-tile-callback)
owns the earlier numeric codes 1-12. After that routing yields to the
selected comparison, numeric 13 and numeric 13.0 enter this body. String
`"13"`, nil, false, true, zero and other unequal values do not. This study
reports their exit from the code 13 branch, without asserting the behavior
of another callback branch.

S has no local type, range, positivity or tile-domain check. Under ordinary
Lua string/number concatenation, numeric 1 produces suffix `1` and string
`"1"` is used as supplied. Zero, negative numbers, 13 and an empty string
also reach name formation without a local 1-12 restriction. The resulting
name does not establish a valid or selected native part. Under ordinary
concatenation, nil or Boolean S cannot complete the name expression. Actual
concatenation/metamethod behavior remains with the running Lua environment.
No separate `tostring(S)` call occurs.

## Ordered requests

Define the requested part names as
`I="Button_ItemIcon_"..S..":IconControl_ItemIcon"` and
`T="Button_ItemIcon_"..S..":TextBlock_NumberOfTopics"`. The body reconstructs
the corresponding name at each request; these abbreviations do not assert
a cached native part.

| Order | Reached condition | Request |
| ---: | --- | --- |
| 1 | Code 13 body entered | `setVisibility(C,I,false)`. |
| 2 | First call returned normally | `setVisibility(C,T,false)`. |
| 3 | H equals numeric zero | `_sendStoryboardCommand(C,nil,"ProgressBar_NegotiationGauge","UILuaCommands.SoundPlayMyOperate")`. |
| 3 | H differs from numeric zero | `_sendStoryboardCommand(C,nil,"ProgressBar_NegotiationGauge","UILuaCommands.SoundPlayEnemyOperate")`. |
| 4 | Selected command returned normally and F equals Boolean true | `_wait(C,0.1)`. |
| 5 | First wait returned normally | `setVisibility(C,I,true)`. |
| 6 | True-visibility call returned normally | `_wait(C,0.1)`. |
| 7 | Second wait returned normally | `setVisibility(C,I,false)`. |

Exactly one order-3 command is requested. Numeric zero, including 0.0,
selects the first spelling. Numeric one, nil, false, true, string `"0"`
and other unequal values select the second. There is no exact-one guard
or local side validation. The command names alone do not establish an
actor identity, side producer or authoritative result.

Only Boolean true F selects orders 4-7. Numeric one, numeric zero, nil,
false and string `"true"` skip that sequence. This is an equality guard,
not Lua truthiness. Skipping it reaches the shared zero-value return after
the storyboard request. When it is taken, the count text receives no later
true-visibility request from this body. The optional sequence addresses
only the icon.

The two `_wait` calls each receive exactly C and literal 0.1. They are
opaque requests here. No helper body, time unit, elapsed duration, yield
condition or scheduling effect is established. Likewise, the storyboard
method receives the literal leading nil, gauge name and command spelling
without an established sound or animation result.

## Lookup, result and error behavior

Every reached method lookup is fresh on the same supplied C. The first
`setVisibility` function and C receiver are captured before the first
concatenation is evaluated. Thus a name-formation error can follow that
lookup and prevent its call. The second visibility lookup occurs only after
the first call returns. The storyboard method is resolved in the selected
H branch after both initial visibility calls.

On the optional path, the first wait method is resolved after the selected
command returns. The next visibility lookup follows that wait. The second
wait and final visibility lookups likewise occur after their preceding
calls. A helper may therefore affect the function selected by a later
lookup. No one visibility or wait method is cached for the entire sequence.

All calls discard every returned value. No result, nil, false, zero and
multiple values select the same next local operation after normal return.
No return value is interpreted as success. Lookup, concatenation and call
errors propagate, prevent later operations and prevent normal return.
Suspended or nonreturning calls also block continuation. Earlier completed
requests are not rolled back by this body.

The selected branch has no direct work lookup, member/global/upvalue write,
data assignment, text-value request or getter call. The
[tile setter](parley-tile-data-assignment.md) and
[getter](parley-topic-data-values.md) own the separate stored key/icon/value
contracts. The
[declaration/storage boundary](parley-initial-state-request.md#work-declaration-and-direct-assignments)
retains their installed-storage, conversion and readback conditions.
Visibility requests here establish no change to those stored values or
successful same-instance readback.

## Conditional five-position example

Consider a supplied frame exactly `(C,13,S,H,nil,true,nil)`. It retains
five payload positions after the update code, including the unused third
and fifth nils. If the selected callback binding receives that full frame
and preceding operations complete normally, it requests both initial
false visibility calls, the H-selected command and all four optional calls
above. With H=0 the command has the `SoundPlayMyOperate` spelling; with H=1
it has the `SoundPlayEnemyOperate` spelling. Neither example chooses an
actual S or H value, identifies a historical side or proves native receipt.

The [Judge and desktop contracts](parley-tile-update-request.md#desktop-lookup-and-complete-tail)
own an upstream conditional request path. The Judge can forward six fixed
positions `(13,S,H,nil,true,nil)` after `"Ask/NegotiationWidget"`. If its
method selects the published desktop helper, a nonnil first getter result
C receives that complete tail through dynamic `updateAskParameter` lookup.
The desktop's normal Boolean result is discarded by the Judge. These
published frames do not prove the actual actor predicate, widget hit,
callback binding, native preparation/delivery or receiver identity.

The example is a supplied-profile interpretation. Actual slot/side/flag
values, native methods and effects, input acceptance, storage, gameplay,
scoring, settlement and historical invocation remain unestablished.

## Source identity and original locators

The canonical member is `lua/scripts/widget/ask/negotiationwidget.lua`,
48,254 bytes and 2,110 lines, SHA-256
`68b0ca9a157b8bdaade66e4e38040a1f6c28b19ef5e0a191ac0f82600b029ec3`.
[scripts.json](../manifests/scripts.json) owns that pin. The containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json):
14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Canonical normalization replaces CRLF pairs with LF only.

The original beneath `client/script/` is
`n1635q/9rz/w53vq19q1vwn1635q.le.lpb`, 15,618 bytes, SHA-256
`dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1`.
Its decoded Lua 5.1 payload is 15,605 bytes, SHA-256
`33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) owns those
identities. The manifests, parser/decoder tools and adopted Script
publications were checked at revision
`31282a5d58fd49b3174d965e5cc1a859c11c53a4`.

Original root closure PC29 and assignment PC30 bind
`NegotiationWidget.updateAskParameter` to `root/proto7`, code offset 8830,
449 instructions, seven fixed parameters, raw vararg flag 0, zero upvalues
and no children. Prototype indices and PCs are zero-based. Offsets exclude
the LPB wrapper; PC n is at `8830+4*n`.

The selected new semantic window is PCs 87-139, with required prologue
PCs 0-6 and shared RETURN PC448. The earlier routing is adopted from the
published prefix. Nonmatching code 13 guard flow exits to PC140, which is
the next branch's metadata boundary. No code 14-29 body is interpreted.

| Consequential operation | Original locator |
| --- | --- |
| Exact numeric 13 comparison and nonmatch exit | EQ PC87; JMP PC88 targets PC140. |
| Initial icon/count visibility requests | SELF PC89/CALL PC95 and SELF PC96/CALL PC102. |
| Exact numeric-zero H comparison | EQ PC103; selected command calls PC109 or PC115. |
| Exact Boolean-true F comparison | EQ PC116; nonmatch JMP PC117 targets PC448. |
| Optional first wait and icon true | SELF PC118/CALL PC120; SELF PC121/CALL PC127. |
| Optional second wait and icon false | SELF PC128/CALL PC130; SELF PC131/CALL PC137. |
| Normal continuation | JMP PC138 to RETURN PC448, B=1. |

All selected CALL instructions have C=1, discarding results. Visibility
calls use B=4, storyboard calls B=5 and wait calls B=3. The canonical code13
branch is lines 1222-1282; its referenced shared normal-return label is at
line 1629. That isolated branch agreed with the original selected behavior.
The full method's canonical definition/binding envelope is lines 1147-1632,
without expanding this study to its other branches.

## Verification

Checks used `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. They authenticated
archive/member/original/payload identities, non-reparse paths, complete
parsing and the selected original root binding/header. Original-instruction
evaluation used only the required prologue, admitted code13 window and
shared return. It stopped before decoding the next branch's body.
Canonical evaluation isolated only the matching code13 branch, required
prologue and referenced normal-return suffix.

An independent request oracle checked numeric/string/Boolean guards,
nil/false/zero, omitted/excess positions, unused payload values, exact name
and command operands, fresh method changes, discarded results and errors
at each reached call/lookup occurrence. Synthetic requests establish those
local contracts, without executing a client, native method or wait helper.
Rejecting controls changed code/side/flag types and guards, slot source,
visibility values, wait literal, command/part strings, argument/result
widths and normal return width. Discarded-result widths also received
instruction-level checks where their alteration had no observable effect
before the shared return. No raw body, listing, payload, AST or complete
instruction vector is retained. No other helper/native body, form, row,
consumer gameplay source, build or runtime case was studied.
