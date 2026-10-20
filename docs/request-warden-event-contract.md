# Request-warden recruitment and end events

`PopulaceRequestWarden` supplies recruitment, cancellation, give-up and end
dialogs. `RequestDirector` retains an externally supplied `requestId` and
declares four synchronized `aimNpcBoss` entries. The selected methods do not
bind either class to normal Behest, company Behest or Guildleve row 1.
Those identities remain separate from these concrete client contracts.

## Source identity

The resources below are relative to retail `client/script/`. Their decoded
paths are `chara/npc/populace/populacerequestwarden.lua` and
`director/guildleve/requestdirector.lua` beneath `lua/scripts/`.
[Registry](../lua/registry.json) entries record the class mappings;
[script](../manifests/scripts.json) and
[coverage](../manifests/retail_lua_coverage.json) manifests pin the artifacts.

| Class / resource | Original LPB SHA-256 | Decoded payload SHA-256 |
| --- | --- | --- |
| `PopulaceRequestWarden`, `729s9/wu7/uvupy975/uvupy975s5tp5rqn9s65w.le.lpb` | `96BFD557B1F384DB943100D8C738AEC68AF1C0354D3D0D163E8817EE58404E32` | `A8D9F05DE7ED37B90B079C36E757A9140EAC2EE34083DDAFB2DF5D8D543436B7` |
| `RequestDirector`, `61s57qvs/3p1y6y5o5/s5tp5rq61s57qvs.le.lpb` | `7988FCE5FD0367F8CE0E3E27A2A0A75E0B0F1E8D2C80FD6B4F654BB300934AB5` | `316B74872A85670F3CACF4E34B3966AB78221A9FA22A45A38022A71ABBF8FF67` |

| Canonical script | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| Warden | 17477 / 858 | `86499EE11D8B31F32E75477DB2472E75EA41EEA6DC60FD11B6CF0530503C4A13` |
| Director | 10347 / 466 | `4EF8CD76D83575FBE6D3657D81A6831BD973224AEBA59757203F5A80200C7927` |

Both canonical decompiles reproduced exactly using
[retail_script.py](../tools/retail_script.py), the
[pinned unluac](../tools/vendor/unluac/PROVENANCE.json), and the documented
CRLF-pair-to-LF normalization. The LPBs contain 7243 and 3529 bytes; their
decoded Lua 5.1 payloads contain 7230 and 3516 bytes respectively.

## Initialization

`initForEvent(self, speechType, townType)` declares two `integer8` temporary
work fields with those names, calls `_setGroundOn(true)`, and stores the
two supplied arguments. It loads text data with `(1355, "populaceRequestWarden")`.
The body returns no values and performs no content lookup.

The selected English bank rows and their matching recruitment/menu keys
are recorded in `xivl-client-data:docs/request-warden-operation-text.md`.
They describe timed culls and operation prompts, without resolving the
helper/native text lookup, normal/company Behest identity or event argument
producers. The retained initializer below supplies one concrete field vector.

`RequestDirector.initAsGuildleve(self, requestId)` calls `initWork` with
an `integer32` temporary `requestId` descriptor and a synchronized
`aimNpcBoss` array descriptor of length 4 and element type `integer8`.
It stores the supplied argument and declares sync tag
`{"infoRequest", 1, {"aimNpcBoss"}}`. The literal 1 belongs to that tag
descriptor. It is not a Guildleve ID assignment. The method returns no values.

These are script descriptors and calls, without a proven native storage or
network layout. The [base Director finding](content-director-ui-contracts.md#guildleve-and-request-directors)
owns the separately established request UI and time-limit helpers.

## Retained Warden initializer

`xivl-captures:studies/request-nmrush-caller-bindings/README.md`, "Warden
creation record", pins `PopulaceRequestWarden` actor `0x44D04940` and the
serialized post-control vector `(1500038,false,false,0,1,"TEST",3,2)`.
Applying the native initializer and class-dispatch conditions gives:

```text
NpcBaseClass._onInit(self,1500038,false,false,0,1,"TEST",3,2)
    actorClassId = 1500038
    fixed superclass gates = false,false
    varargs = (0,1,"TEST",3,2)
    count cursor = 1 -> 2 -> 4
    self:initForEvent(3,2)

PopulaceRequestWarden.initForEvent(self,3,2)
    speechType = 3
    townType = 2
```

The Warden root explicitly passes `NpcBaseClass` as the base of
`PopulaceRequestWarden` to `_defineClass` and assigns child 0 to
`initForEvent`. The inherited initializer stores its first argument as
`npcWork.actorClassId`; the next two fixed arguments go to the superclass.
They are distinct from its variadic count segments.

The first count is 0, so battle-common initialization is skipped and the
cursor advances to 2. The next count is 1. Its common call receives
`initForEventCommon(self,1500038,"TEST",3,2)` through an open `select` suffix;
the call is not truncated to the counted item. The cursor then advances to 4,
past the one counted `TEST` item. Both `initForBattle` and the child
`initForEvent` receive `(3,2)`. The selected inherited event-common method
ignores actorClassId and the entire suffix. It may call `_setGroundOn(false)`
from `_getGrandOnExtraStat()`, so it is not an empty method. `TEST` has no
assigned gameplay meaning here.

The [NPC base contract](map-object-door-client-contract.md#doorstandard-initialization)
owns the NpcBase and event-helper resource identities and generic forwarding
contract. The Warden resource is pinned above. Direct Lua 5.1 operand checks
covered four prototypes: Warden root, NpcBase `_onInit` child 10, event-helper
root and its `initForEventCommon` child 2, totaling 274 instructions / 1,096
code bytes. Whole-resource authentication covered 19,443 original and 19,404
decoded bytes; other methods were skipped structurally. PCs below are
one-based and offsets are decimal decoded-payload offsets.

| Operand | PCs / payload offsets |
| --- | --- |
| Warden base-class declaration and child binding | Root PCs1-7 / 32-56; PCs9-10 / 64-68 |
| NPC actor-class store | PC80 / 2283 |
| Cursor initialization and two advances | PC86 / 2307; PCs100-105 / 2363-2383; PCs119-124 / 2439-2459 |
| Event-common open suffix and call | PCs112-118 / 2411-2435 |
| Child open suffix and call | PCs131-136 / 2487-2507 |
| Event-helper common binding | Root PCs7-9 / 56-64 |
| Common body | PCs1-8 / 874-902; no actorClassId or vararg read |

Open suffixes preserve positional nils and tail count. Each selected method
return is zero-result, not a single nil. The concrete count route, a counted
nil, changed/zero counts, root method, cursor and call/return arity mutations,
and truncated chunks were checked.

This is a conditional formal-argument binding. The native body/application
mapping, guard, non-current-player arm, endian state, mixed-vector retention,
allocation/lifetime and request/lookup conditions remain in
`xivl-decomp:docs/net/guildleve-initializer-route.md`. Its Director-specific
path length and offsets must not be applied to this Warden record. The
capture does not prove historical invocation, assign a place to townType 2,
or identify normal versus company Behest.

## Recruitment and cancellation

`eventTalkRequestJoin(self, A1, A2, A3, A4, A5)` obtains the local player and
calls `startCliantTalkTurn(1, player)`. The client spelling is preserved.
It computes `floor(A1 / 60 + 0.5)`, used below as `minutes`.
The body computes a value from A2 but does not consume it in its subsequent
calls or return; A2 has no established gameplay meaning here.

With `s = getTempWork("speechType")`, the initial scheduler is `354062336`.
The first `self:say` receives `(self, 1+s, 0, townType...)`, forwarding
all results of the final `getTempWork("townType")` call.
For A5 equal to zero, the next say arguments are `(self, 5+s, 0, minutes)`.
Otherwise they are `(self, 143+2*s, 0)` and
`(self, 144+2*s, 0, minutes)`. Both paths then call `worldMaster:say` with
`(self, 157, A3, A4)`. The script does not identify A5 as a normal/company
selector or assign meanings to A3/A4.

Join repeatedly calls `askExtendWidget(self, 111, 3, 1, 1)` while its first
result equals 3. On 3 it runs scheduler `354004992`, says rows `115+s` and
`119+s` with zero, runs scheduler `70799360`, says row `123+s` with
`(0, 8)`, and says row `127+s` with zero before asking again.
Any result unequal to 3 exits and returns exactly that first result.
This body has no `finishCliantTalkTurn` call.

`eventTalkRequestCancel(self, A1)` starts talk in mode 1, computes the same
rounded minutes, runs scheduler `84013056`, and says
`(self, 40+s, 0, minutes)`. Its widget tuple is
`(self, 131, 3, 1, 1)`. It uses the same result-3 retry sequence and returns
exactly the final first widget result, without a talk-finish call in this body.

## Terminal dialogs

| Method | Talk mode / scheduler | Say arguments after receiver | Widget arguments after receiver | Talk finish |
| --- | --- | --- | --- | --- |
| `eventTalkRequestGiveUp(self)` | 2 / `84013056` | `(self, 59+s, 0)` | `(self, 63, 2, 1, 2)` | Always after widget result |
| `eventTalkRequestEnd(self, A1, A2)` | 1 / `84013056` | `(self, 90+s, 0, A1, A2)` | `(self, 94, 3, 1, 1)` | Only when first widget result differs from 1 |

Both return exactly the first widget result. Neither retries on 3.
The result values do not establish server acceptance, cancellation or completion.

## Bytecode locators and limits

Children are zero-based beneath each root. PCs are one-based; offsets are
zero-based decoded-payload offsets. Original LPB offsets are payload offsets
plus 13 before XOR decoding. Root closure assignments bind these children
to the named methods.

| Method | Prototype | Key PCs and payload offsets | Canonical lines |
| --- | --- | --- | --- |
| Warden initialization | `root.0` | Calls 15/18/22/26/30 at `0x3AB/0x3B7/0x3C7/0x3D7/0x3E7`; empty return 31 at `0x3EB` | 11-51 |
| Join | `root.1` | Open-result getter/say 30/31 at `0x52A/0x52E`; ask 78 at `0x5EA`; retry tests 70/80 at `0x5CA/0x5F2`; one-value return 122 at `0x69A` | 56-203 |
| Cancel | `root.8` | Ask 34 at `0xE67`; retry tests 26/36 at `0xE47/0xE6F`; return 78 at `0xF17` | 406-501 |
| Give up | `root.12` | Ask 26 at `0x1395`; finish 29 at `0x13A1`; return 30 at `0x13A5` | 591-630 |
| End | `root.16` | Ask 28 at `0x1859`; equality/branch 30/31 at `0x1861/0x1865`; finish 33 at `0x186D`; return 34 at `0x1871` | 733-776 |
| Director initialization | `root.0` | Calls 19/23/35 at `0x25E/0x26E/0x29E`; empty return 36 at `0x2A2` | 11-57 |

The retained initializer supplies one conditional Warden field binding.
A content-specific caller supplying the Warden event arguments and the
Director's `requestId` remains unresolved. The
[normal/company timer consumers](myplayer-timer-consumers.md#scalar-consumer-map)
and the "Official Behest" title at
`xivl-client-data:derived/guildleve_names.csv`, ID 1, do not supply it.
The selected bodies establish neither encounter progression nor wave,
reward or server policy. Static calls do not establish live behavior.
