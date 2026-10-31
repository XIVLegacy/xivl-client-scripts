# Skirmish and Behest client contract

The retail 1.23b client establishes dialog operands, initializer forwarding
and UI timer consumers. Historical admission, encounter progression and reward
authority require additional evidence. The four questions below distinguish
those boundaries. Announcements and named wiki content belong to
`xivl-captures:docs/skirmish-behest-content-evidence.md`.

| Question | Supported client contract and evidence | Confidence | Unresolved edge |
| --- | --- | --- | --- |
| Q1. Which Skirmish Guide, caller and answer owner? | `PopulaceNMRushGuide` loads bank 10608 and exposes seven dialogs. Its ask methods return one customization result. The [binding and answer contract](#guide-binding-and-results) distinguishes direct and delegated calls. `xivl-client-data:docs/nmrush-skirmish-text.md`, "Actor label and admission instructions", joins actor class 1002087 to display name 1600350, Storm Captain Loetahlsyn, and separately zone 230 to place 1051, Limsa Lominsa. | Confirmed static consumers and label joins. | These joins do not connect that actor class to the Guide script or zone. An attributable actor lifetime, outer function, typed parameters, actual answer and same-transaction server event owner remain required. |
| Q2. What starts and ends Skirmish, and which timer applies? | [Director state](#director-state-and-availability) distinguishes numeric `directNumber`, Boolean `timer`, synchronized `limitTime` and the separate native `0x0193/0x16` availability scalar. | Confirmed static state branches and native storage. | No encounter assignment, admission decision, phase/wave producer, terminal outcome or reward settlement follows from those UI fields. The retained scalar census contains no `0x16` publication. |
| Q3. What does Warden signup/entry require? | [Warden initialization and event operands](#warden-initialization-and-event-operands) establishes two count segments before child `(speechType,townType)`, one retained conditional `(3,2)` binding, and Join/Cancel/GiveUp/End result consumers. [RequestDirector initialization](#requestdirector-initialization) retains a separately supplied `requestId`. | Confirmed static forwarding and consumers. One retained creation, conditional on native initialization. | The full retained Warden census has no named interaction, Warden-owner EventStart or RequestDirector creation. Signup confirmation, executed transport, private-area identity and the admission-to-Director chain remain unbound. |
| Q4. What are the per-Behest phases, spawns and rewards? | [RequestDirector UI](content-director-ui-contracts.md#guildleve-and-request-directors) supplies time-limit literal 20 and objective presentation. `xivl-client-data:docs/request-warden-operation-text.md`, "Menu and retry text", supplies objective, reward-promise and transport labels. Named wiki associations and announced waits are qualified in the content-evidence record above. | Confirmed client presentation. Historical content retains its own source tier. | No exact 1.23b per-Behest `requestId`, wave order/counts, spawn positions, outcome/reward quantities or settlement schedule is established. A UI time limit, reward promise or monster drop string does not supply that policy. |

## Guide binding and results

The [Guide contract](nmrush-guide-director-contract.md#incoming-caller-positions)
owns the conditional caller matrix. Let O be the selected binding's Lua value,
and D0, D1, ... the materialized incoming typed values.

| Requested call | Guide self | Guide A1 | Remaining adaptation |
| --- | --- | --- | --- |
| Outer function directly resolves the Guide method | O | D0 | Supplied frame `(O,D0,D1,...)` |
| Outer function resolves `PlayerBaseClass.delegateCommand`, with D0 the Guide and D1 its method key | D0 | O | Inner frame `(D0,O,D2,...)`; D1 is consumed |

O comes from the selected native binding. It is distinct from the raw trigger
key, and is not automatically the local player. Guide talk modes 1/2 require
A1 to support position lookup and the Guide's look-at call. The incoming
record, binding selection and conversion guards are canonical in
`xivl-decomp:docs/script/delegate-command-producer.md`, "Incoming record and
receiver", "Typed values and bounds" and "Function, binding value and supplied
frame".

The `0x0130` application contains trigger `+0x00`, owner `+0x04`, event type
`+0x08`, event name `+0x09`, outer function `+0x29` and the copied 64-byte
typed span at `+0x49`. Supported token conversions are:

| Tag | Encoded operand | Materialized Lua value |
| --- | --- | --- |
| `00` | Four-byte signed integer | Number |
| `01` | Four-byte float | Number |
| `02` | NUL-terminated string | String |
| `03` / `04` | No additional bytes | True / false |
| `05` | No additional bytes | Explicit positional nil |
| `06` | Four-byte actor key | Resolved binding value, subject to lookup/readiness |
| `0F` | Terminator | No value |

The native endian selector, unknown tags and malformed-input bounds remain
subject to the cited native contract. A raw actor token does not prove a
resolved historical actor. The decoder's success result does not prove complete
input consumption or execution.

Under the established helper/widget path, ordinary first-answer selection
returns numeric 1: WarpAsk's first label is No, BattleAsk's is Commence
Skirmish, and ContentEndAsk's is Yes. ContentEndAsk defaults to index 2.
Widget cancellation returns -3; failed open or unsuccessful selection returns
0. These are separate results. No status/completion prefix is inserted.
The Guide finishes talk and returns its one retained value without choosing
a content action. The [shared helper contract](nmrush-guide-director-contract.md#shared-talk-and-choice-helpers)
owns these conditions and the additional dialogs' option lists.

Normal native completion can serialize that result to c2s `0x012E`, but its
numeric variant's precise integer/float encoding still depends on operator
selection. `xivl-decomp:docs/script/delegate-command-producer.md`, "Completion
reply serializer", owns that boundary.
`xivl-client-structs:structs/network/event-update.md`, "Builder and copied
extent" and "Context dword provenance and correlation", owns the reply fields
and CRC32. Its first dword derives from the trigger's resolved context; the
incoming owner key is not passed to that builder. Neither that dword nor the
cached dword at `+0x04` independently identifies the server event owner or a
fresh invocation. Establish answer ownership with one complete event
transaction and its continuation.

## Director state and availability

The [NMRush Director contract](nmrush-guide-director-contract.md#director01-state-branches)
and [Director02 proof](nmrush-guide-director-contract.md#director02-original-state-and-time-contract)
establish numeric states 1/2 starting content information only when local
`timer` equals Boolean false, followed by `timer=true`. State 3 and
finalization request cancel without resetting that flag. State 0 and other
states make no update widget call. Director02 declares synchronized
`directNumber:integer8` and `limitTime:integer32`, with tags `direct` and
`time`. Its getter returns exactly `(limitTime,limitTime-60)`, without a clamp
or unit conversion. The [content-information route](content-director-ui-contracts.md#quest-content-information-directors)
uses kind 1, maximum article index 0, titles 51143/51144 and instruction 51145.

Separately, `0x0193/0x16` writes native timer state `S+0x1C`: value
`0xFFFFFFFF` stores zero; otherwise it stores `(headerClock+value) mod 2^32`.
The clock is game-message header `+0x08`, and the scalar is message `+0x14`.
Reader `0x0075D280` returns the word unchanged through MyPlayer wrapper
`_getNMRushUpdateTime` at `0x00706A00`. StatusWidget selector -4 presents
Skirmish availability. Sources:

- [Native update scalar](nmrush-guide-director-contract.md#native-update-scalar).
- [Scalar UI consumers](myplayer-timer-consumers.md#scalar-consumer-map).
- `xivl-decomp:docs/net/s2c-0193-native-state.md`, "Timer readers" and "Handler arguments and stored words".
- `xivl-client-structs:docs/player-misc-native-contract.md`, "Timers and replay state".

This availability endpoint has no established join to Director `limitTime`,
battle duration or an encounter reset. The complete retained scalar census,
`xivl-captures:studies/map-0193-clock-contract/README.md` and
`derived/occurrences.csv`, contains nine records: eight `0x14`, one `0x12`.
There is no retained `0x10`, `0x11` or `0x16` publication in that scope.

## Warden initialization and event operands

The [retained Warden initializer](request-warden-event-contract.md#retained-warden-initializer)
owns actor `0x44D04940`, class 1500038 and this post-control vector:

```text
NpcBaseClass._onInit(self,1500038,false,false,0,1,"TEST",3,2)
    fixed superclass gates = false,false
    variadic count segments = 0 ; 1,"TEST"
    child suffix = 3,2
    self:initForEvent(3,2)
```

The two counts advance the variadic cursor by `count+1` each. With both
counts zero, the corresponding caller shape is
`(actorClassId,gate1,gate2,0,0,speechType,townType)`. The gates and both
counts precede the child fields. A caller must preserve those positions and
the complete child suffix. A value placed in the second count position is
consumed as that count, rather than becoming `townType`. Common calls use
open suffixes, so a positive count is not a truncation bound on their supplied
arguments. The [NpcBase forwarding contract](map-object-door-client-contract.md#doorstandard-initialization)
owns the general cursor and superclass behavior.

Warden `initForEvent(self,speechType,townType)` declares/stores two temporary
`integer8` fields, loads `(1355,"populaceRequestWarden")` and calls
`_setGroundOn(true)`. The retained conditional suffix is `(3,2)`. It does not
assign a geographic meaning to townType 2, select a Behest variant or prove a
completed historical initializer.

The [event contract](request-warden-event-contract.md#incoming-argument-boundary)
owns the following operand limits:

| Method/input | Established consumer |
| --- | --- |
| Join A1 | Formats `floor(A1/60+0.5)` as minutes. No producer joins it to an availability clock. |
| Join A2 | Numeric arithmetic whose computed local is unused. No gameplay meaning or legal range established. |
| Join A3/A4 | Place/level formatting through `worldMaster:say(self,157,A3,A4)`. No authenticated wire types/ranges. |
| Join A5 | Numeric zero versus other branch. No normal/company enum established. |
| End A1/A2 | Transport-dialog formatting values. No outcome enums, arithmetic or legal range established. |

[Widget result production](request-warden-event-contract.md#widget-result-production)
separately establishes Join/Cancel result 3 as the retry/objective branch,
End result 1 as continuing talk, and GiveUp always finishing talk. Each
returns the first widget result. Widget cancellation -3 and fallback 0 remain
distinct from answer slots and server acceptance. The [normal/company clocks](request-warden-event-contract.md#normal-and-company-availability-clocks)
use separate `0x0193/0x10` and `/0x11` absolute whole-second availability
endpoints at native `+0x10` and `+0x14`. Neither supplies Join's countdown or
an active battle duration.

## RequestDirector initialization

The [Director initializer chain](guildleve-initializer-arguments.md) separates
`directorId` from Guildleve ID, location and extra marker X/Y/Z, then forwards
the remaining suffix to `initAsGuildleve`. The
[RequestDirector hook](request-warden-event-contract.md#initialization)
requires its supplied `requestId`, retained as temporary `integer32`, and
declares synchronized `aimNpcBoss[4]:integer8`. Its `{"infoRequest",1,...}`
descriptor does not assign Guildleve ID 1. Caller conformance therefore
requires the inherited positional prefix and the child `requestId` suffix,
with each identity supplied independently.

[Request article consumers](request-warden-event-contract.md#request-article-consumer)
forward `requestId` with worldMaster text 50090 and an objective selector into
the Text property. The nested `request` sheet expression is identified in
`xivl-client-data:docs/request-warden-operation-text.md`, "Request article
text". Its native key evaluation and a concrete encounter/request row remain
unbound. Literal UI timeLimit 20 does not prove a server battle budget.

The [full retained Warden census](request-warden-event-contract.md#retained-interaction-census)
already covers all 54 source captures for Warden/RequestDirector/event names
and matching EventStart owners. Its single creation supplies no signup,
transport, private-area or Director chain. Closing those edges requires one
attributable Warden event with typed inputs, observed answer and reply,
participant confirmation, destination/private-area identity, and initialized
Director/requestId over the same actor/event lifetimes. Static caller
conformance can be checked independently of that missing runtime sequence.
