# Command and NPC event operands

These contracts distinguish a value read by client Lua from a legal producer
domain or a completed server transaction. Original instruction checks support
the specific operands identified below. Other branch descriptions retain the
recovered-decompile evidence class from extraction `2012.09.19.0001`.

| Subject | Meaning and supported values | Evidence locator | Confidence and unresolved part |
| --- | --- | --- | --- |
| Place-driven variation and judge callback | Variation 30003 maps to ready command 22004, the Fishing UI command. Callback operands 20006 and numeric 15 have no established formal meaning or accepted domain. | [Place-driven judge-command mapping](gathering-marker-fishing-ui.md#place-driven-judge-command-mapping), `mapJudgeCommand`, original `root/proto0` PCs 34/36/38. | Original mapping confirmed. The separate `commandJudgeMode` signature, operand producers and correlated result remain unresolved. |
| Teleport confirmation 138824 | In `eventConfirm(self,player,A2,A3,A4,A5,A6)`, 138824 at A5 is bypassed when A2 is false. A5 is only an untyped formatter in the alternate row-34138 arm. | [Confirmation formatting argument](aetheryte-list-widget-contract.md#confirmation-formatting-argument), original `root/proto1` PCs 32/35/48. | Original branch confirmed. No destination, item or text-key identity or accepted A5 domain is established. |
| Regional guildleve publisher inputs | Twelve inputs after self govern opening speech, choice controls, numeric thresholds, menu continuation and formatting. The table below records uses rather than a universal accepted-value list. | [Publisher inputs](#regional-publisher-inputs), `populaceguildlevepublisher.lua:164-752`, original `root/proto1` CALL PCs 75/92/151. | Fixed arity and three calls confirmed in original instructions. Remaining branches are recovered-source evidence; producer ranges and server eligibility remain unresolved. |
| Request-warden town and Join inputs | The retained class-1500038 vector routes to `speechType=3,townType=2`. Join A2 is computed but unused, A3/A4 format place/level, and numeric zero A5 selects one presentation arm. | [Retained Warden initializer](request-warden-event-contract.md#retained-warden-initializer) and [Incoming argument boundary](request-warden-event-contract.md#incoming-argument-boundary). | Original operands and retained record confirmed at their stated boundary. Actual town/instance binding and Join A2-A5 producers/ranges remain unresolved. |
| Public coffer key question and opening | `askUseKey(A1,A2)` requires the coffer method receiver, uses worldMaster text, forwards both formatters and returns one widget result unchanged. | [Conditions, event delivery and key question](keyed-treasure-box-registration.md#conditions-event-delivery-and-key-question), Public `root/proto1` PCs 8/9 and inherited widget PCs 37/38/72. | Original call/return confirmed. Key operand domains, historical trigger/owner pairing and the subsequent opening transaction's ownership remain unresolved. |
| Kinnison default talk | A3/A4 select row 554 when either is at least zero, otherwise row 240, after row 239. No named quest-state enum is established. | [Kinnison numeric predicates](quest-event-client-contracts.md#kinnison-numeric-predicates), `DftFst` original `root/proto119` PCs 12-15/20/26. | Original predicates and zero-result return confirmed. Numeric producers, legal intervals and named states remain unresolved. |
| Direct equipped-gear repair 24244 | `RepairEquipmentWidget` issues `executePlayerCommand(24244,S,nil,nil,nil,T)`. S is an authored equipment-slot integer or bulk selector 27; T is a target player control. | `xivl-client-structs:docs/direct-gear-repair-fulfillment.md`, Ordered operands and identity domains; Source identity and original instruction checks. | Original issuer, nine-position forwarding and empty result method confirmed. Runtime descriptor selection, reply dispatch and authoritative settlement remain unresolved. |

## Place-driven variation and callback values

The [mapping contract](gathering-marker-fishing-ui.md#place-driven-judge-command-mapping)
owns the complete variation lookup. Its input 20006 maps to 22007, while
30003 maps to 22004. Neither relationship names the fifth argument of a
different `commandJudgeMode` callback. No authenticated formal consumer or
correlated reply here assigns that callback's fifth value `0x4E26=20006`
or eighth value `0x0F=15` a meaning or legal range.

The integer 15 also differs from typed-stream END tag `0F`. In the established
command serializer, an ordinary integral Lua 15 has tag `00` and the
four-byte big-endian payload `00 00 00 0F`; the terminator is a separate
single-byte tag. Source:
`xivl-client-structs:docs/player-command-wire-contract.md`, Dispatch and
construction; Values and references. This framing distinction does not bind
the callback to that transport or establish callback semantics.

## Teleport confirmation argument

Substituting `(false,false,1,138824,false)` into A2-A6 selects
`worldMaster:ask(self,worldMaster,34120,2)`. That arm does not read A5.
In the alternate arm, A5 precedes A4 and literal 1 after the row-34138
formatter flags. The value's source-domain identity remains unresolved;
the false-A2 call cannot identify 138824 as a destination. The
[canonical confirmation contract](aetheryte-list-widget-contract.md#confirmation-formatting-argument)
owns the source/payload identities and original branch locators.

## Regional publisher inputs

`PopulaceGuildlevePublisher.eventTalkType` has the fixed frame
`(self,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12)`, without varargs.
The receiver is the publisher instance. These incoming positions differ
from the method's outgoing menu results.

| Input | Recovered use and source lines | Supported values or type ceiling |
| --- | --- | --- |
| A1 | Compared with thresholds 10, 25, 35 and 45 while constructing the row-69 submenu (`349-389`). | Numeric ordering is required on those paths. The thresholds do not prove a level producer, integer-only input or legal interval. |
| A2 | A truthy value starts talk in mode 2 and enables opening speech (`170-251`). | Lua truthiness is tested, without an explicit Boolean type check. |
| A3 | Fifth choice-control value after row 59 (`308-315`). | Forwarded unchanged. No mask width or producer domain is established. |
| A4 | Sixth choice-control value after row 59 (`308-315`). | Forwarded unchanged. No mask width or producer domain is established. |
| A5 | Seventh choice-control value after row 59 (`308-315`). | Forwarded unchanged. No mask width or producer domain is established. |
| A6 | Sixth choice-control value after row 4 (`260-268`). | Forwarded unchanged. No Boolean or numeric-mask domain is established by this call. |
| A7 | Compared with numeric zero before the `work.omenTalk` speech cycle (`176-240`). | Zero versus other is the observed test, without a Boolean or enum declaration. |
| A8 | Nil opens the main menu. The tests `40 <= A8 < 53`, `20 <= A8 < 30` and `A8 == 5` select internal branches 4, 2 and 5 (`253-276`). It is also compared with individual continuation values and may be reset to nil (`301-342,459`). | Nil or numeric comparisons are consumed. The intervals are not an integer-only accepted-value list; the recovered individual continuation branches are not all independently proved from original control flow. |
| A9 | Formatter after zero in the opening `say(self,3,0,A9)` (`244-250`). | Forwarded unchanged. No allowance, balance or count domain is proved by this call. |
| A10 | Used with A1 at least 45: the submenu-selection branches compare `0 <= A10`, `2 <= A10` or `1 <= A10` (`385`). | Numeric thresholds, not an enum restricted to 0/1/2. |
| A11 | Equality with the internal submenu selection enables an extra row-69 choice; later result mapping distinguishes 1 and 2 (`390-394,443-448`). | Selection equality is observed. No faction membership or eligibility producer is established. |
| A12 | Appended to the row-69 formatting list when that equality holds (`393`). | Forwarded unchanged, without a type/range check. |

The two choice-control tails are exactly
`row4: (true,true,false,true,true,A6,true,true)` and
`row59: (true,true,true,true,A3,A4,A5)`. They establish argument order,
not numeric bit-mask semantics for A3-A6. The selected opening speech call
is `say(self,3,0,A9)`.

The recovered row-59 submenu arm returns three values: the selected internal
value plus 40, a second constructed value, and A8 (`462-466`). Other arms
can return one value or nil. The canonical
[Regional publisher result values](guildleve-journal-lifecycle.md#regional-publisher-result-values)
section owns the named Information/Tutorial, Fieldcraft and evaluation results.
An outgoing result code does not define the incoming A1-A12 schema.

Source: `lua/scripts/chara/npc/populace/populaceguildlevepublisher.lua:164-752`,
SHA-256 `578e390f7c9ea2eb9941560df9319d7e3987ceba3abe0fd0105f93c9786ceeb1`,
pinned by [scripts.json](../manifests/scripts.json). The
[call index](../lua/scripts/chara/npc/populace/populaceguildlevepublisher.calls.json)
records the class and native-call locations; it does not expose these script
helper calls. The original member is
`729s9/wu7/uvupy975/uvupy9753p1y6y5o5up8y1r25s.le.lpb`, SHA-256
`7b05c7f7508c7883fcedf5c576d3e865408db04c79fc4fdc67627e864c1050d5`;
decoded Lua 5.1 payload SHA-256
`fb2f2cf01f6de72c526f0c21af88d4cec35b82b1dc78c1b0a82f07a66c9e1b75`,
pinned by [retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Original `root/proto1` establishes 13 fixed parameters including self and
no varargs, CALL PC 75 for speech row 3 with A9, PC 92 for row 4 with A6,
and PC 151 for row 59 with A3-A5. PCs are zero-based. The readers were
`tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. These selected
checks do not independently establish the entire complex method's original
control flow. The threshold and continuation descriptions above follow
the authenticated recovered source. No authenticated producer supplies a
complete legal domain or server eligibility policy for the twelve inputs.

## Request-warden binding and Join arguments

The initializer declares `speechType` and `townType` as `integer8`
temporary work fields. The retained actor key `0x44D04940`, actor-class
value 1500038 and `townType=2` are separate identities. The
[retained initializer](request-warden-event-contract.md#retained-warden-initializer)
conditionally routes that vector to `(3,2)`. It does not identify the actual
town, a placement/instance, other actor-class-to-town mappings or historical
invocation. The declaration's type name does not establish a town enum.

| Join input | Consumer contract | Accepted-value boundary |
| --- | --- | --- |
| A2 | Computes `A2+10`, or 10 when A2 equals 1, then never consumes the computed local. | Numeric arithmetic is expected; no integer width, meaning or legal interval is established. |
| A3 | First row-157 formatter, associated with the place-name control. | No authenticated place-key producer or validated key set. |
| A4 | Second row-157 formatter, associated with the recommended-level number. | No authenticated level producer or validated bound. |
| A5 | Numeric zero chooses one speech sequence; every other value chooses the alternate sequence. | No Boolean or normal/company domain is established. |

The [Incoming argument boundary](request-warden-event-contract.md#incoming-argument-boundary)
owns these original operands and the finite caller-search limit. Its
retained-interaction finding supplies no named Warden interaction that could
resolve the producers. The consumed Join A1 duration and separate player
availability clocks do not supply A2-A5 or a town binding.

## Public coffer ownership

The coffer instance must be the receiver for `askUseKey`; worldMaster is its
text owner. Public A1/A2 survive the inherited widget call unchanged, and
the method returns one raw widget result. Gimmick's separate helper returns
a Boolean instead. The
[event delivery contract](keyed-treasure-box-registration.md#conditions-event-delivery-and-key-question)
owns both original call shapes and the conditional incoming function route.

These facts do not choose the event envelope's trigger/owner pairing,
validate a particular key ID/count or establish ownership of a later open
request. They also do not bind confirmation to key consumption, inventory
updates or a successful opening. The missing observation must join the
same coffer's registration, enabled condition, prompt, answer and opening
outcome within one actor lifetime. The
[open-world coffer finding](open-world-key-coffer-contract.md#retained-capture-coverage-and-lifecycle-boundary)
owns the retained capture limit and transaction discriminator.

## Kinnison numeric branches

The frame is `(self,player,npc,A3,A4)`. Both numeric inputs are compared
with zero, and the selected predicate is an OR:

| A3 | A4 | Rows said in order |
| ---: | ---: | --- |
| -1 | -1 | 239, 240 |
| 0 | -1 | 239, 554 |
| -1 | 0 | 239, 554 |
| 0 | 0 | 239, 554 |

The same rule applies to other comparable numbers: both negative values
select 240; either nonnegative value selects 554. These four substitutions
illustrate the original predicate, without asserting retail initial values
or a producer domain. Both arms close talk and return zero values. The
[canonical Kinnison contract](quest-event-client-contracts.md#kinnison-numeric-predicates)
owns original source, payload and PC identities. Named quest states,
particular quest IDs and finite accepted ranges remain unresolved.

## Direct repair issuer and settlement

The canonical contract is
`xivl-client-structs:docs/direct-gear-repair-fulfillment.md`, Ordered operands
and identity domains; Admission and local result; Conditional transport and
completion boundary. The issuer's exact call is
`executePlayerCommand(24244,S,nil,nil,nil,T)`. Its connector expands the
values after the command actor to `(S,nil,nil,nil,T,nil,nil,nil,nil)`.
T occupies position 5 and is a player control, not a numeric actor ID.

The individual submitting buttons select S from
`1,2,9,11,13,14,15,16,17,18,20,22,23`; RepairAll selects 27 for target
repair type 1, 2 or 3. Those UI values differ from `canFire`'s broader
numeric check: type `number` and no value below 1, without an upper bound
or integral-value check. The canonical contract also preserves the
explicitly refused mapped slots and the source/target predicates.

`RepairEquipmentsCommand.processResultRepair` is empty, with a zero-result
original RETURN. That does not establish a server dispatch to it. Local true
and the generic equipment refresh do not prove durability, material, reward
or refusal settlement. The selected runtime command descriptor and a repair
reply or demonstrated alternative completion route remain unbound. Command
24243's [equipment-request mode](repair-request-client-contract.md#equipment-request-mode-24243)
and CraftCommand 22013 self-repair in
`xivl-client-structs:docs/repair-contract.md` remain separate contracts.
