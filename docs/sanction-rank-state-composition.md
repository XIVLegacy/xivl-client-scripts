# Sanction rank state composition

The published Grand Company state fields can supply the belonging-company
value and selected signed rank used by `PopulaceCompanyBuffer` Welcome's local
row and menu-admission guard. This composition is conditional on the native
binding, frame and object identities below. It establishes which state inputs
feed that guard, not that a snapshot was delivered or that Sanction was granted.

## Published sources

These authored contracts own the observations and their confidence labels:

- `xivl-client-structs:docs/player-misc-native-contract.md`, `Grand Company
  rank` at line 190, with `Registration` at line 78 and `Contracts` at line 167.
  Revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`, 34335 bytes,
  SHA-256 `219397ae69eea7bc24c6290bca0d80681562740e5a10bc51750806d238561fa0`.
- `xivl-decomp:docs/event/gc-approval-wire-contract.md`, `Allegiance and rank
  publication` at line 112 and `Evidence grades and identity` at line 15.
  Revision `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, 23373 bytes,
  SHA-256 `9111da92a2ee0b9379951d477d6c225ecb77a9c9668f3b36d21bb77b82bf23ba`.
- `xivl-client-scripts:docs/sanction-company-buffer-contract.md`,
  [Welcome selection and rank boundary](sanction-company-buffer-contract.md#welcome-selection-and-rank-boundary)
  at line 74 and [Menu arguments and scalar results](sanction-company-buffer-contract.md#menu-arguments-and-scalar-results)
  at line 117. Revision `9b76f32c64029cf6ed3d350ccef7cd65021eb33f`,
  11225 bytes,
  SHA-256 `1fa780b388a22cfe11d8473e1f93fb0b9d240787077262998f187ba580cbd3eb`.

The native publications identify retail `ffxivgame.exe`, version
`2012.09.19.0001`, PE32 x86, image base `0x00400000`, `15996808` bytes,
SHA-256 `9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Addresses here retain their published VA convention. The Decomp publication
records PE section reads with pefile `2024.8.26` and Capstone `5.0.7` in
x86-32 mode, compared with retained Ghidra assembly. Its `A-native` grade and
Structs' `STATIC` observations remain static evidence. Structs labels the
semantic identification of `+0xED` as company number and `+0xEE/+0xEF/+0xF0`
as company ranks `INFERRED` from native names and argument range. This
composition retains that qualification.

The Scripts publication identifies retail extraction `2012.09.19.0001`,
`chara/npc/populace/populacecompanybuffer.lua`, and its source/resource hashes
under [Source identity and locators](sanction-company-buffer-contract.md#source-identity-and-locators).
Its instruction and authored-provider agreement is a source comparison, not
retail execution. This page combines those published findings without a new
binary observation or runtime claim.

## Native publication and getter conditions

The Decomp contract's s2c Map `0x0194` route is central dispatcher
`0x004DC690`, LuaActorImpl slot 71, adapter `0x0075A400`, receiver constructor
`0x0089CC90`, then `GrandCompanyReceiver` routine `0x0089CD60`.
The adapter and constructor preserve application bytes 0-3 at receiver
`+4/+5/+6/+7`. These are application positions, not whole-packet offsets,
header geometry or an independently specified transport envelope.

The receiver must successfully cast the actor control from `ActorBase` to
`PlayerBase`. It calls through the resulting object's vtable offset `+0xA4`,
virtual slot 41. The selected target must be the published setter:
`PlayerBase` `0x006DEB00`, cell `0x00FD5EA8`, or `MyPlayer` `0x006E2DE0`,
cell `0x00FD7900`. The setter ignores its first stack argument and stores
arguments 2-5 as the following four bytes. An actual derived object's selected
vtable target remains a condition.

| Application byte | Receiver byte | `PlayerBase` field | Getter input |
| --- | --- | --- | --- |
| `+0` | `+4` | `+0xED` | `_getBelongGrandCompany()` |
| `+1` | `+5` | `+0xEE` | `_getGrandCompanyRank(1)` |
| `+2` | `+6` | `+0xEF` | `_getGrandCompanyRank(2)` |
| `+3` | `+7` | `+0xF0` | `_getGrandCompanyRank(3)` |

The setter writes all four fields, so its input is a complete desired
snapshot. The record is not a rank delta, officer-approval boolean, seal balance, Sanction
grant or callback invocation. Preserving the other companies' intended bytes
is part of supplying that snapshot.

The getter read must use the same `PlayerBase` subobject that received those
writes, with those field values still present. The same Lua variable, actor
name or player name does not establish that identity or intervening state.
This page does not establish actor registration, delivery or ordering between
state publication and an event invocation.

`_getGrandCompanyRank` `0x00706CF0` is a direct member under `PlayerBase`,
not one of the published virtual getter thunks that return nothing on a plain
`PlayerBase`. Structs' holder invoke routine `0x0071E7D0` still requires its
successful `LuaControl` to `PlayerBase` cast through `0x009DA6CC`.
The native rank input must be a matching prepared frame: the int reader
`0x005819A0` must successfully read the selector from a present cell with tag
0. Ordinary Lua numeric values alone do not establish that post-preparation
native-cell descriptor or the complete preparation path. The published
wrapper/receiver, descriptor and type conditions must actually match before
applying this composition.

For a successfully read int selector 1, 2 or 3, the getter sign-extends the
corresponding byte and pushes one int through `0x00584F70`. The allegiance
getter `0x00706CC0` similarly sign-extends `+0xED`. A byte `b` yields `b` for
0-127 and `b - 256` for 128-255. Any other successfully read int selector
pushes no value. That is zero native results, not an explicit nil push.

Welcome retains one result from each query. Under ordinary Lua result
adjustment, a zero-result rank getter therefore supplies nil to that caller,
and comparison with 27 raises an error before the salute request. Keep this
distinct from native failure: a mismatched int cell tag reaches
`0x00CCA730`, and a missing input cell reaches the vector-size failure route
`0x009D22B4`. Neither is the validly read, unsupported-selector branch. The
published holder's failed cast returns without calling the callback and is
also a separate cause.

## Conditional Welcome decision

Assume that Welcome is invoked with the intended supplied `npc` and `player`,
stable method bindings, ordinary Lua equality, comparison and `type`, and
successful preceding requests. Its belonging query at PC4 must resolve to the
published allegiance getter under a matching native frame and receiver. Any
rank query at PC19 or PC29 must resolve to the direct rank getter with the
matching prepared int frame above. The publications do not establish that
binding or preparation for an actual invocation merely from method spelling.

Let `company` be `npc.work.grandCompanyNumber`, and let `belonging` be the
one retained signed allegiance result. Welcome chooses:

| Guard in evaluation order | Rank input | Row | Menu admission |
| --- | --- | ---: | --- |
| `belonging == 0` | No rank query | 20 | false |
| `belonging ~= company` and `flag == false` | No rank query | 17 | false |
| Other-company path, flag is not false, rank < 27 | Rank for `belonging` | 17 | false |
| Other-company path, flag is not false, rank >= 27 | Rank for `belonging` | 18 | true |
| Same-company path, rank < 27 | Rank for `belonging` | 15 | false |
| Same-company path, rank >= 27 | Rank for `belonging` | 2 | true |

Belonging 1 selects `+0xEE`, 2 selects `+0xEF`, and 3 selects `+0xF0`.
Selection follows belonging, even on the other-company path. Belonging 0
skips rank entirely. An unsupported nonzero signed belonging reaches a rank
query only if it passes the preceding other-company/false guard. In that case
its successfully prepared int selector returns zero native results as above.
The exact-false test is not truthiness: nil and numeric zero do not bypass the
rank query. The flag is not inspected on the same-company path.

For the decisive same-company profile `company = 1`, application byte 0 is
1 and application byte 1 varies below. Bytes 2-3 retain their independently
desired snapshot values. The following are local selection values only:

| Raw rank byte | Signed getter result | Row | Menu admission |
| ---: | ---: | ---: | --- |
| 26 | 26 | 15 | false |
| 27 | 27 | 2 | true |
| 127 | 127 | 2 | true |
| 128 | -128 | 15 | false |
| 255 | -1 | 15 | false |

Direct Welcome does not normalize raw 127 before comparing with 27. Separate
Lua wrappers own their normalization contracts. The value 127 here describes
this direct guard, not an assertion that 127 is an obtainable or allowed rank.
The table likewise establishes no global rank domain or Sanction benefit.

## Consumer boundary

The consumer can conditionally use the signed allegiance and its selected
signed rank as the published inputs to the local row/admission decision.
Row 15 still reaches the menu with admission false. Normally continuing rows
20 and 17 return numeric zero after their presentation requests. Menu admission is passed to
`askMultipleTextMacro` at PC105. It does not itself establish a permitted
widget choice, a status grant or the final scalar callback result. The
[menu contract](sanction-company-buffer-contract.md#menu-arguments-and-scalar-results)
owns helper/result conditions, and the
[effect callbacks](sanction-company-buffer-contract.md#effect-callbacks-and-cleanup)
remain separately invoked presentation requests.

The composition leaves actual invocation, native preparation, object binding,
applied snapshot and unchanged write/read state conditional. It establishes
no server approval policy, transaction order, free cost, duration, equipment
stat application, status effect or callback delivery. Authored synthetic
byte-order, sign, selector and return-width checks establish publication/model
consistency only. They do not execute the native client or reproduce a retail
state transition.
