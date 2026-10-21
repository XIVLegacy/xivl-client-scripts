# Request-warden recruitment and end events

`PopulaceRequestWarden` supplies recruitment, cancellation, give-up and end
dialogs. `RequestDirector` retains an externally supplied `requestId` and
declares four synchronized `aimNpcBoss` entries. The selected methods do not
bind either class to normal Behest, company Behest or Guildleve row 1.
Those identities remain separate from these concrete client contracts.

## Binding status

`PROMOTED` identifies an observed client consumer or retained record.
`UNRESOLVED` identifies a missing producer or native semantic join.
`NOT IN CLIENT` applies to the authoritative server decisions, not to a
negative search over every possible native instruction.

| Question | Status | Established contract / remaining boundary |
| --- | --- | --- |
| Join A2-A5 producers, types and ranges | PROMOTED consumers; UNRESOLVED producers/ranges | A2 participates in unused numeric arithmetic; A3/A4 format the place/level message; A5 selects zero versus other. No authenticated content caller or legal server domain was recovered. |
| End A1/A2 and accepted values | PROMOTED formatting use; NOT IN CLIENT server policy | Both are transport-dialog formatting arguments. They are not cancel/complete/withdraw enums. The client returns a separate widget result. |
| `RequestDirector.requestId` | PROMOTED article operand; UNRESOLVED native row/key join | Retained as temp `integer32`, then passed with worldMaster 50090 and an objective selector to article text. That text contains a `request` sheet reference. No authenticated content caller or native expression evaluation was bound. |
| Menu/retry outcomes and acceptance | PROMOTED Lua result handling; UNRESOLVED UI label/result join; NOT IN CLIENT server policy | Join/Cancel consume result 3 as retry; End consumes result 1 as continuation. Widget cancel/default handling is distinct from server admission or refusal. |
| Normal/company timer scalar and units | PROMOTED | Two separate s2c 0x0193 fields produce absolute whole-second availability endpoints consumed by StatusWidget. No join-duration producer is implied. |
| Retained behest session | UNRESOLVED | The complete retained capture query found one Warden creation and no named Warden interaction or RequestDirector creation. |

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

The same decoder and unluac reproduced the inherited work, widget and article
helpers from these original resources. The coverage and script manifests
above pin their payloads and reproduced source hashes. Instruction PCs in
this finding were checked against the decoded Lua 5.1 instruction arrays,
not inferred from the decompiler's temporary-variable names.

| Helper | Resource under `client/script/` | Original LPB SHA-256 |
| --- | --- | --- |
| Guildleve base | `61s57qvs/3p1y6y5o5/3p1y6y5o589r57y9rr.le.lpb` | `73559543D4E2192180C28AC8F8F6F3FB69EBF8BCBB47B2C11A69C837CFE8F303` |
| Director base | `61s57qvs/61s57qvs89r57y9rr.le.lpb` | `7BCA9CCB9F130EA27EA8E43DD94AFDB6BA0ACF9F133F6294564988A281E72D7B` |
| NPC event helper | `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` | `84A5098636FF289F4ECF4E164E84E44890895E8A9005FB102E04929C2BB74BF9` |
| NPC base | `729s9/wu7/wu789r57y9rr.le.lpb` | `3F1DCC3416F7E22DB138A6DCC730B095F81F3D0CEB458A7DED7D5B0D17DF55C9` |
| Desktop connector | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425` |
| Ask widget | `n1635q/9rz/9rzn1635q.le.lpb` | `8541D21030988F4ED5460690156A71A5A0120B68ED38D8DB181676B27A23BFE9` |
| Ask base | `n1635q/9rz/9rz89r57y9rr.le.lpb` | `4C1C98059F5B3663D24A85897D21FF603DFB5C95000C20FDFA4BEFD592AD431D` |
| Execution widget | `n1635q/3p1y6y5o55m57pq1vwn1635q.le.lpb` | `8EED436E9058CBA2BC7EA92603A1A493CF10BE7ACE8B676EA66B5F384326C8CD` |
| WorldMaster event helper | `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb` | `4CED313114AB09753AD0DC82EA8E9CD12C66D31447C967E91883932291CD7459` |
| Desktop widget | `n1635q/65rzqvun1635q.le.lpb` | `BE7B0959BA530027991B22308B1D6A84CE5DB311BDB727F987678B5DBF810E51` |

## Initialization

`initForEvent(self, speechType, townType)` declares two `integer8` temporary
work fields with those names, calls `_setGroundOn(true)`, and stores the
two supplied arguments. It loads text data with `(1355, "populaceRequestWarden")`.
The body returns no values and performs no content lookup.

The selected English bank rows and their matching recruitment/menu keys
are recorded in `xivl-client-data:docs/request-warden-operation-text.md`.
They describe timed culls, menus and transportation prompts. Native text
evaluation, normal/company Behest identity and event argument producers
remain distinct. The retained initializer below supplies one field vector.

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
selector. The matching Warden bank row 157 contains a place-name control
followed by a recommended-level number. A3/A4 are those formatting operands,
without a proven native parameter-domain check or an authenticated producer.

The explicit Warden argument survives the helper chain:
`lua/scripts/world/worldmaster_event.lua:111-124`, `WorldMaster.say`,
`root.4`, PC8 / payload offset `0x4CB`, calls
`desktopWidget:showMessage(worldMaster,40,self,157,A3,A4)`.
`lua/scripts/widget/desktopwidget.lua:369-384`, `showMessage`, `root.14`,
PC9 / `0xF0C`, forwards that suffix to `_appendMessagePool`.
`lua/scripts/widget/desktopwidget_u.lua:3-11` declares its
`_appendMessagePool_cpp` native boundary. The method receiver's name is not
itself proof of bank ownership. The loaded Warden bank and its matching
row 157 supply the static association; native bank resolution and rendering
remain unresolved.

For the retained initializer's `speechType=3`, the matching bank keys are
greeting 4 followed by 8 when A5 equals numeric zero, or 149 and 150
otherwise. The selected text finding above establishes no normal/company
label for either branch. Capturing speechType does not select the A5 branch
or identify its producer.

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

## Widget result production

`NpcBaseClass.askExtendWidget`,
`lua/scripts/chara/npc/npcbaseclass_event.lua:418-493`, `root.11`, receives
`(self,textOwner,promptId,answerCount,flags,defaultIndex,...)`. It builds
`answers[i] = promptId+i` at PC6 / payload offset `0xE0E`. The Warden calls
therefore bind the following values, including the explicit text-owner
argument after the colon-call receiver.

| Method | Answer text rows in index order | Default index | Paging / cancel |
| --- | --- | ---: | --- |
| Join | 112, 113, 114 | 1 | false / true |
| Cancel | 132, 133, 134 | 1 | false / true |
| GiveUp | 64, 65 | 2 | false / true |
| End | 95, 96, 97 | 1 | false / true |

All four use flag 1, which calls the connector at PC39 / `0xE92`.
The data finding records Yes/No/objectives, No/Yes/objectives, Yes/No, and
Yes/Remain here/Cancel respectively. These are answer slots and authored
labels. The result producer below does not prove a native UI event's
association with one of those slots.

`DesktopWidget.askForEventMode`,
`lua/scripts/widget/desktopwidget_connector.lua:11997-12090`, `root.237`,
opens `Ask/AskWidget` at PC16 / `0x1C0BD`, forwards the question, answer
table, default index and flags to `ask` at PC28, then waits for selection
at PC32. It reads `getAskResult` only after selection equals true at PC36
and returns its local result at PC41 / `0x1C121`. That local starts at 0,
so missing-widget or unsuccessful-selection paths return 0.

`AskWidget.ask`, `lua/scripts/widget/ask/askwidget.lua:108-248`, installs
each answer row in `Item_Answers` plus its one-based index and stores the
paging/cancel flags. `processUICommandEvent` at `:387-482`, `root.4`,
produces the stored result as follows:

| UI command | Result and original operand observation |
| --- | --- |
| Operate `TemplateButton_Answer` | Calls `parseWidgetString(eventString,2,"Answers")`, applies `tonumber`, and stores the number at PC16 / `0xD11`. |
| Cancel | Stores -3 at PC27 / `0xD3D` only when `canCancel` is true. |
| PagePrevious / PageNext | Stores -2 / -1 when `askPaging` is true. Otherwise changes pages without completing the ask. |

`parseWidgetString` is Lua, not a native numeric decoder:
`desktopwidget_connector.lua:8059-8089`, `root.141`, splits the UI event
string using `"Answers"` at PC12 / `0x1488C` and returns token 2 at PC21 /
`0x148B0`. The originating UI event string is not present in a retained
Warden transaction. No one-to-one label/result join is claimed here.
`AskBaseClass`, `lua/scripts/widget/ask/askbaseclass.lua:79-86,115-139`,
resets its stored result to 0 (`root.8`, PC9 / `0x583`) and reads it back
unchanged (`root.9`, PC2 / `0x608`).

Join and Cancel treat numeric result 3 as the retry/objective-dialog branch.
End keeps talk open for numeric result 1 and finishes talk for other results.
GiveUp always finishes talk. Each returns the first widget result unchanged.
The server controls admission, refusal, withdrawal and completion. Neither a
positive result nor a Lua boolean is evidence of server acceptance. In
particular, the three-choice End dialog's third label is Cancel, whereas
Join/Cancel's third labels describe objectives.

## Incoming argument boundary

The Warden methods are event consumers. `rg -n` over the 2,671 `.lua` members
of the authenticated [decoded archive](../manifests/private_lua_corpus.json)
found only their four method-name assignments, with no literal caller of
Join, Cancel, GiveUp or End. This is a finite Lua result, not proof that
native or server code never invokes them. The generic server-to-client named
event route is described by the [event delivery contract](keyed-treasure-box-registration.md#conditions-event-delivery-and-key-question).

| Input | Original consumer and observation | Type / legal range established |
| --- | --- | --- |
| Join A2 | Warden `lua/scripts/chara/npc/populace/populacerequestwarden.lua:56-203`, `root.1`, PCs14-17: computes `A2+10`, or 10 when A2 equals 1; never uses the computed local | Numeric arithmetic is expected. No integer width, content meaning or allowed interval is established. |
| Join A3/A4 | Same source `:132-139`, `root.1`, PCs66-69: forwards them after owner and 157 to `worldMaster:say` | Place-name and level formatting operands by static bank association. No validated place-key set, level bound or wire type is established. |
| Join A5 | Same method, PC32 / `0x532`, zero-equality branch before the say calls | Exactly numeric zero selects one path. Other values take the other path. This does not prove a boolean or normal/company enum. |
| End A1/A2 | Same source `:733-776`, `root.16`, PCs19-21: moves both into `say(self,90+s,0,A1,A2)` and never tests either | Formatting values, with no Lua arithmetic, type check or legal range. Rows 90-93 offer transportation and retain nested aetheryte/place-name and conditional suffix controls. Native evaluation remains unresolved. |

The Join A1 division by 60 and the authored minute text are compatible with
a supplied seconds count. They do not produce that value or connect it to
the separate normal/company availability endpoints below. End's result-1
test applies to the widget return, not to End A1. No client body here defines
which inputs a server must accept or when a behest completes.

## Request article consumer

`RequestDirector.getArticleDataOnGuildleveInfo`,
`lua/scripts/director/guildleve/requestdirector.lua:300-381`, `root.5`, reads
temp `requestId` only in these guarded branches:

| Article index | Guard | Returned five-value article tail |
| --- | --- | --- |
| 4 | `getUiStateOf(4) > 0` | `"smash", worldMaster, 50090, requestId, 8+state-1` |
| 8 | `aimNpcBoss[index-4] > 0` | `"smash", worldMaster, 50090, requestId, 8+aimNpcBoss[index-4]-1` |

The getter calls are at one-based PCs 31/65, payload offsets `0x9EF/0xA77`.
`GuildleveBaseClass.getArticleFullDataOnGuildleveInfo`,
`lua/scripts/director/guildleve/guildlevebaseclass.lua:916-971`, rearranges
those five values into this ten-value return for the branches above:
`(state,type,condition,param1,param2,param3,owner,textId,requestId,selector)`.
The RequestDirector values occupy positions 2 and 7-10.
`GuildleveExecutionWidget.updateArticle`,
`lua/scripts/widget/guildleveexecutionwidget.lua:175-214`, `root.3`, calls
that method at PC3 / `0x6D1` and forwards returns 7-10 to `setArticleState` at
PC19 / `0x711`. Thus `requestId` is an article formatting operand, not merely
the literal in the `infoRequest` tag. The same widget's `setArticleState`,
`:637-786`, `root.9`, forwards `(worldMaster,50090,requestId,selector)` to
the Text property at its open `_setProperty` call, PC121 / `0x133F`.
The native boundary is `_setProperty_cpp`, as declared by
`lua/scripts/widget/widgetbaseclass_u.lua:44-51`. The default init loop
visits indices 1 through 7; it does not itself exercise index 8.

The data finding's "Request article text" section pins worldMaster row
50090 and its nested `xtx/displayName` / `request` sheet control with two
operand expressions. This is evidence for the intended request-sheet text
association. Native expression evaluation and a concrete supplied requestId
have not been authenticated together. It does not establish an encounter
instance ID, an opaque token allocation policy or a binding to Guildleve 1.
All four literal `requestId` matches in the Lua corpus are in RequestDirector:
the descriptor, setter and these two getters.

## Normal and company availability clocks

These are the independently named StatusWidget consumers in the
[scalar consumer map](myplayer-timer-consumers.md#scalar-consumer-map).
Fresh reproduction of `lua/scripts/widget/statuswidget.lua:3363-3554`,
`setContentsListItem`, `root.62`, establishes the following operand route.
PCs in this table are one-based, as elsewhere in this document.

| Selector | Read | Native terminal field / publication |
| --- | --- | --- |
| -2 | `_getNormalBehestTime`, PC33 / `0x6D92` | Getter `0x007054D0` -> `0x0075D220`, terminal +0x10; s2c 0x0193 subopcode 0x10 -> writer `0x0075D210` |
| -3 | `_getCompanyBehestTime`, PC42 / `0x6DB6` | Getter `0x00705510` -> `0x0075D240`, terminal +0x14; subopcode 0x11 -> writer `0x0075D230` |

The authenticated retail PE is `ffxivgame.exe`, 15,996,808 bytes, SHA-256
`9341F2B4567440B310A4D494F5CC5599CA334BA51C8042247317FF466492F2E9`.
Direct PE section reads with pefile 2024.8.26 and Capstone 5.0.7 x86-32
reproduced the following instruction observations. The promoted route is
also recorded in `xivl-decomp:docs/net/s2c-0193-native-state.md`.

| Binary locator | Observation |
| --- | --- |
| `0x004DD36F..0x004DD37D` | Passes game-header +8 clock, +0x14 value and +0x10 subopcode to `0x00578C90`. Relative to the 8-byte application body, subopcode/value are +0/+4. |
| `0x00578CC4..0x00578CD4`, jump table `0x00578FDC` | Value `0xFFFFFFFF` becomes zero; otherwise adds header clock to value as uint32. Subopcode 0x10 dispatches to `0x00578D0A`; 0x11 to `0x00578D1E`. |
| `0x00578D14 / 0x00578D28` | Calls the normal/company writers above with that computed endpoint. |
| `0x007079A0..0x007079B7`, `0x006E3AA0`, `0x0075BD80` | WorldMaster server-time read uses cached +0x60, refreshed from NetworkModule +0x30C. The native clock model below establishes whole seconds. |

`xivl-decomp:docs/actor/cast-timing-clock.md`, "Native clock model", binds
NetworkModule +0x30C to whole seconds and +0x310 to milliseconds, including
the `_time64` initializer and packet-clock updates. StatusWidget requires
a positive endpoint, reads `_getServerTime` at PC98 / `0x6E96`, compares
endpoint <= now at PC113, and otherwise subtracts now at PC121 / `0x6EF2`.
It divides the difference by 86400, 3600 and 60 at PCs125/137/149 to format
days, hours and minutes. These are absolute whole-second endpoints, with
the wire scalar interpreted as a relative seconds offset unless it is the
clear sentinel. This establishes display behavior, not a server recurrence
interval or the duration of an active behest.

The StatusWidget LPB `n1635q/rq9qprn1635q.le.lpb` has SHA-256
`2809EAF420CED30DA99C28786A2FE5AB798050B9D654103CBA7B3059926016D4`;
decoded payload SHA-256
`9668B0BC032DFCACC3F19F285BB5BD5673AD72C3DA8D0FC68E893D087B27BB90`.
The same pinned decoder/unluac path reproduced source SHA-256
`29A01E8DADAE3A9DD57A42D453F21338BCF33AEC436FE509F6E565F263151385`.

## Retained interaction census

The full retained set pinned by
`xivl-captures:sources/pcap-1.23b/manifest.yaml` contained 54 captures.
`xivl-captures:config/retail_inputs.json` pinned its archive identity.
The source archive SHA-256 was
`20A78B9F40FF2393037C9A160C957783CF590B4F01797493D22FCD2039E9CBFF`.
After authenticating every member, the capture tools' `validate_framing`,
`extract_streams.reconstruct_lanes`, `parse_outer_frames` and `maybe_inflate`
at revision `82F1783F98FD03DB656D193A6394439A3E1B32F5` reconstructed 84
admitted connections and 19,760 complete outer frames. All decoded bodies
consumed exactly. TLS/54994 traffic and incomplete tails were excluded.

The query checked 831 s2c 0x00CC class fields, 200 s2c 0x0130 function fields
and complete 64-byte parameter spans, and 126 c2s 0x012D owner fields. It
searched complete bodies in both directions for `PopulaceRequestWarden`,
`RequestDirector`, `eventTalkRequest*` and `Behest`, keeping capture,
connection and direction separate and joining EventStart owners only within
the same capture. There was one Warden class record, zero RequestDirector
records, zero matching event functions and zero Warden-owner EventStarts.
The two raw text hits were the Warden class/path in that same creation.

The positive record above was in `teleport_to_camp_tranquil.pcapng`, SHA-256
`488318351CDEDB2E2B650DC68C55014B160FBBC26753C200922402C1BA6C4DD7`:
connection 0/main/s2c, outer frame 61, subevent 14, stream offset 13107,
inflated-body offset 1272, capture packet 230 at
`2012-12-31T01:32:08.379688Z`. Packet numbering is one-based; frame/subevent
ordinals are zero-based. Frame completion was assigned by the packet-span
method in `extract_login_0002_appearance_order` and
`extract_0193_clock_contract`. The existing creation study owns its decoded
initializer vector; this census does not witness Join, End or a menu answer.

All nine retained s2c 0x0193 records had subopcode 0x12 once or 0x14 eight
times. None published the normal/company 0x10/0x11 fields. The retained
clock observations are recorded in
`xivl-captures:studies/map-0193-clock-contract/README.md`. No retained session
authenticated the six requested content bindings together.

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
Director's `requestId` remains unresolved. The "Official Behest" title at
`xivl-client-data:derived/guildleve_names.csv`, ID 1, does not supply it.
The selected bodies establish neither encounter progression nor wave,
reward or server policy. Static calls do not establish live behavior.
The remaining discriminator is a retained Warden transaction containing
the named Join/End argument vectors, widget answer/continuation and a
RequestDirector initialized with its requestId. UI answer production and
text-expression evaluation would additionally settle the UI result and
request-sheet key joins without importing server policy.
