# NMRush guide and director client contracts

`PopulaceNMRushGuide` passes a supplied talk argument through and returns the
first customization result after finishing talk. `QuestDirectorNMRush01/02`
starts content information on states 1 or 2 only when its timer flag is
exactly Boolean false. State 3 always requests cancel without resetting the
flag. These are client call contracts, without an established admission,
encounter progression or reward producer.

## Source identity

The resources below are relative to retail `client/script/`. Decoded paths
are beneath `lua/scripts/`. Class mappings are in the
[registry](../lua/registry.json); original and canonical identities are in
the [coverage](../manifests/retail_lua_coverage.json) and
[script](../manifests/scripts.json) manifests.

| Artifact | Guide | Director01 |
| --- | --- | --- |
| Resource | `729s9/wu7/uvupy975/uvupy975wxspr23p165.le.lpb` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2ji.le.lpb` |
| Original bytes | 3193 | 1936 |
| Original SHA-256 | `681C5C462DE0268B4E54EBCB90A1E0FCFEFF061CC4282FCC1ED7E21269B09C56` | `5A0B0B7524E0A6B0B9FA1DADB5FB1D7A0708DC8864AA1FE1BE9AB9248437D04E` |
| Payload bytes | 3180 | 1923 |
| Payload SHA-256 | `63DCA3ED3F761E491484A8551E85877E3FE5E308D0DCCE343B5EB72209FC73B5` | `E271622889764302C94C94878C2370356256B24F9480DDF72138F61F5BB319D2` |
| Decoded path | `chara/npc/populace/populacenmrushguide.lua` | `director/quest/questdirectornmrush01.lua` |
| Canonical bytes / lines | 6605 / 355 | 3569 / 197 |
| Canonical SHA-256 | `0540EAEF9635883C898D1DCA2B7286301A324C64AA02E6CC81ADB23422FEDB13` | `E73ABD30092591D113B0EF002A77417D5DFAAEF13B4A0C106FACFC16864AE24E` |

Reproduction with [retail_script.py](../tools/retail_script.py), the
[pinned unluac](../tools/vendor/unluac/PROVENANCE.json), and the documented
CRLF-pair-to-LF normalization matched both canonical manifests exactly.
The observations below use raw Lua 5.1 operands, independently of decompiler
control-flow presentation.

## Guide arguments and results

`initForEvent(self)` loads text data with
`(10608, "populaceNMRushGuide")`, calls `_setGroundOn(false)`, and returns
no values. Each selected event method takes `(self, A1)` and passes A1
unchanged to `self:startCliantTalkTurn(mode, A1)`. The methods do not resolve
A1 through `_getMyPlayer` or establish its native type.

| Method | Talk mode | Scheduler | Ordered `self:say(self, id, 0)` IDs | Customization call |
| --- | ---: | ---: | --- | --- |
| `processWarpAsk` | 2 | `354066432` | 19, 20 | `self:askForCustomizeOption(self, 1, false, true, 21, {22,23,24})` |
| `processBattleAsk` | 2 | `354103296` | 29, 30, 31 | `self:askForCustomizeOption(self, 1, false, true, 32, {33,34,35})` |
| `processContentEndAsk` | 1 | `69165056` | 46, 47 | `self:askForCustomizeOption(self, 2, false, true, 48, {49,50})` |
| `processBattleEnd` | 1 | `70828032` | 44 | None |

The order is talk start, scheduler, the listed `self:say` calls, customization
where present, then `self:finishCliantTalkTurn()`. Warp additionally calls
`worldMaster:say(self, 3, 45, 4)` and `worldMaster:say(self, 51)` between
its self messages and customization. Those calls have different receivers.
The numeric text arguments alone do not establish those cells' meanings.

The matching English bank keys are recorded in
`xivl-client-data:docs/nmrush-skirmish-text.md`. They explicitly name Skirmish
and provide participation/commencement labels. This static association leaves
helper/native text resolution, rendered labels and a live guide, site or
instance unresolved. The [shared helper contract](#shared-talk-and-choice-helpers)
supplies the conditional choice-index mapping.

The three ask methods retain exactly one customization result and return
exactly that one value after finishing talk. Extra results are discarded;
an absent result becomes nil in the single returned position. No branch
interprets it as an admission or end decision. `processBattleEnd` returns
zero values. Presentation helper results are discarded.

## Shared talk and choice helpers

The Guide root requires `/Chara/Npc/NpcBaseClass` and declares
`PopulaceNMRushGuide` with base `NpcBaseClass`. The NPC main root requires
`/Chara/Npc/NpcBaseClass_event`; that event root binds
`startCliantTalkTurn`, `finishCliantTalkTurn` and `askForCustomizeOption`.
These declarations establish the helper path subject to normal require/class
resolution, method lookup and no later replacement.

Let G be the Guide and P its supplied talk argument. The start helper has six
fixed parameters `(G,mode,P,x,y,z)` and no varargs. For the Guide's modes 1
and 2, it calls `P:_getPos()` and retains exactly three results, then calls
`G:_getDir()` and `G:_getOrientation(x,y,z)`, retaining one result from each.
It passes P unchanged to `G:_lookAtCharacter(P,1)`. Mode 2 additionally calls
`G:_lookAtCharacter(P,0.25)`. Mode 1 calls
`G:_turnDir(savedDir+orientation)` and `G:_waitForTurning()` only when the
orientation result is strictly outside `[-1.047,1.047]`.

Thus P must support the position lookup/call and be acceptable to the Guide's
look-at method. The helper does not select P through `_getMyPlayer` or prove
P's native type or historical identity. Extra position results are discarded
and missing results become nil; their acceptability to the native orientation
method is unproved. The optional fixed x/y/z arguments are unused for these
two modes. Start returns zero values. Finish calls `G:_turnBack()` and
`G:_cancelLookAt()`, discards their results and returns zero values. These
are observed calls, without established native effects or event completion.

The customize helper forwards all six explicit arguments plus its open
varargs to `desktopWidget:askForEventMode`, with two extra G values before
them. Substituting the Guide's calls gives this explicit desktop tuple:

```text
(G, G, G, M, false, true, questionKey, optionKeys)
```

The [desktop and AskWidget contract](duty-confirmation-client-contract.md#prompt-and-argument-forwarding)
omits the first owner argument and calls
`widget:ask(G,G,M,false,true,questionKey,optionKeys)`. G supplies both the
talker and text-provider positions. P is absent from this tuple. M is the
default answer index, false is `askPaging` and true is `canCancel`.
The NPC helper retains exactly one desktop result and returns exactly that
one value; an absent callee result becomes one nil, and extra results are
discarded. Its open varargs preserve positional and trailing nils.

The [selection contract](duty-confirmation-client-contract.md#selection-and-continuation)
preserves ordinary answer-control indices through the stored ask-result field.
Conditional on that widget path and an ordinary first-answer selection:

| Guide method | Supplied default answer index | First supplied text key / authored label | Returned first-answer value |
| --- | ---: | --- | ---: |
| `processWarpAsk` | 1 | 22 / "No." | 1 |
| `processBattleAsk` | 1 | 33 / "Commence Skirmish." | 1 |
| `processContentEndAsk` | 2 | 49 / "Yes." | 1 |

The text-key/label associations belong to the client-data finding above.
Text keys 22, 33 and 49 are presentation inputs, not returned answer values.
The content-end default index 2 is distinct from its first answer, Yes at
index 1. With `canCancel=true`, the widget's cancel branch stores `-3`.
With `askPaging=false`, the `-1/-2` paging-result branches do not apply.
The desktop fallback is numeric `0` after a failed open or a selection
continuation unequal to Boolean true. It is separate from selected No and
from cancellation. No completion/status prefix is inserted.

The Guide finishes talk and returns its one retained result without choosing
a content action. The [generic callback result path](passivegl-dialogue-producer.md#native-callback-result-and-eventupdate)
can collect and serialize the result for c2s `0x012E` on normal completion.
That does not identify a Skirmish invocation, outer adapter, actual reply or
server continuation. Text resolution, successful display and native/widget
state remain conditions of applying the client result mapping.

The NPC main and event-helper resource identities are in the
[NPC base finding](map-object-door-client-contract.md#doorstandard-initialization)
and the [resource manifest](../manifests/retail_lua_coverage.json):
`729s9/wu7/wu789r57y9rr.le.lpb` and
`729s9/wu7/wu789r57y9rr_5o5wq.le.lpb`. The Guide resource is pinned above.
Direct Lua 5.1 operand checks covered the three roots plus three event methods,
375 instructions / 1,500 code bytes, including the root revisits. Whole-file
authentication covered 15,393 original and 15,354 decoded bytes. Other
prototype bodies were skipped structurally. Deeper widget and native result
evidence is reused from the cited contracts.

PCs here are one-based; offsets are decimal decoded-payload offsets. The duty
contract uses zero-based PCs, so its PC numbers differ while offsets agree.

| Operand | Prototype / PCs / payload offsets |
| --- | --- |
| Guide base declaration | Guide root PCs1-7 / 32-56 |
| NPC event-helper require | NPC root PCs1-3 / 32-40 |
| Three helper bindings | Event root PCs12/21/39 / 76/112/184 |
| P position call, three retained results | Event child 3, PCs9-13 / 1022-1038 |
| Initial look-at calls | Child 3, PCs61-69 / 1230-1262 |
| Mode-1 turn test and calls | Child 3, PCs100-114 / 1386-1442 |
| Mode-2 second look-at call | Child 3, PCs115-120 / 1446-1466 |
| Finish calls and zero-result return | Event child 6, PCs1-5 / 2286-2302 |
| Customize open arguments, one-result call/return | Event child 12, PCs3-13 / 3998-4038 |

Focused instruction replay with substituted method results checked Guide-mode
branches, threshold equality, argument order, nil preservation and return
arity. Eight operand/arity mutations were rejected. These checks do not
execute the client or establish native-method behavior.

## Director01 state branches

`processUIUpdate(self, A1)` reads `self.work.directNumber` once; A1 is unused.
Its state comparisons use numeric 0, 1, 2 and 3. The timer comparisons use
the Boolean constant false, rather than Lua falsiness.

| State | Timer precondition | Client action and explicit write |
| --- | --- | --- |
| 0 | Unused | No widget call or timer access/write |
| 1 or 2 | Exactly Boolean false | `desktopWidget:processUpdateContentsInformation(self, "start")`, then `self.work.timer=true` |
| 1 or 2 | Any other value | No call or write |
| 3 | Unused | `desktopWidget:processUpdateContentsInformation(self, "cancel")`; timer unchanged |
| Other values | Unused | No call or write |

Every branch returns zero values, without falling through to another state's
action. The start flag is written after the call returns. Repeated state-1/2
updates therefore start once while the flag remains true; every state-3
update requests cancel. Nil and numeric zero do not satisfy the exact-false
test. Uninspected callees may have additional effects.

The [quest Director finding](content-director-ui-contracts.md#quest-content-information-directors)
owns Director01's separate initialization, title and finalization evidence.

## Director02 original state and time contract

The separately authenticated Director02 resource establishes the same update
state/flag behavior as the table above. This comparison reuses Director01's
published proof; it does not infer Director02's branches from the class name.

| Director02 artifact | Identity |
| --- | --- |
| Resource under `client/script/` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2jh.le.lpb` |
| Original bytes / SHA-256 | 1936 / `C65739DA2CB6817C6333B9D5D69A4DB3B7118649304D0F461E8319BC9DAB3491` |
| Decoded payload bytes / SHA-256 | 1923 / `6EF7C7C7D55D01DD311BE32DDACBE6020C59E0E3BDDAE0BC2571B11C9E9C6374` |
| Canonical Lua under `lua/scripts/` | `director/quest/questdirectornmrush02.lua`, 3569 bytes / 197 lines |
| Canonical Lua SHA-256 | `8753C016DF079227ADB24F55538095EF63164953BFCE5F051E9107127071C083` |

Original root closure assignments bind the four selected methods at PCs 9,
12, 15 and 30. The fixed Lua 5.1 reader consumed the payload exactly to EOF.
The following offsets are decoded-payload code-array offsets and PCs are
zero-based; original source-line metadata is distinct from canonical
decompiled line numbering.

| Method | Prototype / code offset | Original source lines / instruction words |
| --- | --- | --- |
| `initAsQuestDirector` | `root/proto0`, `0x249` | 891-914 / 41 |
| `processUIUpdate` | `root/proto1`, `0x3B6` | 923-948 / 46 |
| `processUIFinalize` | `root/proto2`, `0x535` | 956-958 / 6 |
| `getTimeDataOnGuildleveInfo` | `root/proto7`, `0x6CB` | 1020-1026 / 7 |

Initialization declares local `timer:boolean`, synchronized
`directNumber:integer8` and `limitTime:integer32`, sets `timer=false` at PC 21,
and associates tags `direct` and `time` with those two synchronized fields.
It returns zero values.

Update reads `directNumber` at PCs 0-1 and does not use the argument after
`self`. Numeric 0 jumps to return at PC 45. Numeric 1 selects the exact-false
timer test at PC 10, calls `processUpdateContentsInformation(self, "start")`
at PC 16, then writes `timer=true` at PC 18. Numeric 2 takes the separate
exact-false test at PC 25, start call at PC 31 and write at PC 33. Each start
branch returns directly; it does not fall through into cancellation. Nil,
numeric zero and true timer values do not satisfy either Boolean-false test.
Numeric 3 always calls `processUpdateContentsInformation(self, "cancel")`
at PC 42 without resetting the flag. Other direct numbers return without a
widget call. All three CALLs discard results and update returns zero values.

Finalization unconditionally requests cancel at PC 4, discards its results,
and returns zero values without a timer write. The time getter reads
`limitTime` once, subtracts constant 60 at PC 2 and returns exactly
`(limitTime, limitTime - 60)` at PC 5. It applies no clamp or unit conversion;
those operands alone do not establish the unit or timer-expiry policy.

The four bodies total 100 instruction words / 400 bytes. Focused static
instruction replay checked initialization, 40 direct-number/timer cases,
repeated start/cancel, finalization and getter return arity. Inverting either
exact-false comparison rejected a supported start case. This is conditional
client UI behavior, without a runtime reproduction, historical instance
assignment, wave/encounter transition, admission decision or reward rule.
The [content-information adapter](content-director-ui-contracts.md#quest-content-information-directors)
owns the existing kind-1 route to `GuildleveExecutionWidget`.

## Bytecode locators and evidence boundary

Children are zero-based beneath each root. PCs are one-based, with zero-based
decoded-payload offsets. Original LPB offsets are payload offsets plus 13
before XOR decoding. Root closure assignments bind the named child methods.

| Method | Child / canonical lines | Key CALL or RETURN PCs and payload offsets |
| --- | --- | --- |
| Guide initialization | 0 / 11-22 | Load 4 at `0x1DB`; ground 7 at `0x1E7`; empty return 8 at `0x1EB` |
| Warp ask | 1 / 27-84 | Option 42 at `0x30D`; finish 44 at `0x315`; one-value return 45 at `0x319` |
| Battle ask | 3 / 134-183 | Option 35 at `0x62D`; finish 37 at `0x635`; one-value return 38 at `0x639` |
| Content end ask | 6 / 287-328 | Option 29 at `0xA9C`; finish 31 at `0xAA4`; one-value return 32 at `0xAA8` |
| Battle end | 7 / 333-353 | Finish 14 at `0xBCC`; empty return 15 at `0xBD0` |
| Director01 update | 1 / 67-118 | Start calls 17/32 at `0x3F6/0x432`; flag writes 19/34 at `0x3FE/0x43A`; cancel call 43 at `0x45E`; empty return 46 at `0x46A` |

Director timer equality tests are PCs 11/26 at `0x3DE/0x41A`; unequal
values jump to PC46 through PCs 12/27. The cancel-state equality test is
PC37 at `0x446`, with unmatched values jumping to PC46 through PC38.
The three option CALLs use `A=3 B=8 C=2`; their operative RETURNs use
`A=3 B=2`. Director start/cancel calls use `A=3 B=4 C=1`.

The [Skirmish timer consumer](myplayer-timer-consumers.md#scalar-consumer-map)
connects the NMRush timer API to the displayed status label. It does not
identify an actual guide NPC, site, instance or event dispatcher. The selected
bodies leave unresolved the caller supplying A1, the content-specific consumer of the returned
option value, and the producer of synchronized `directNumber`/`limitTime`.
No server policy or live encounter follows from the static UI contract.

## Incoming caller positions

The conditional native frame is established in
`xivl-decomp:docs/script/delegate-command-producer.md`, "Function, binding
value and supplied frame" and "Delegate and callback positions". It distinguishes
two possible caller forms; neither is an observed Skirmish call here.
Let O be the selected binding's Lua value and D0, D1, ... the explicitly
materialized typed parameters.

| Selected call form | Guide self | Guide A1 |
| --- | --- | --- |
| Incoming function directly resolves a Guide event method | O | D0 |
| Incoming function resolves `PlayerBaseClass.delegateCommand`, D0 is the Guide and D1 resolves its event method | D0 | O |

The direct form supplies `(O,D0,D1,...)`; the reflective form calls the inner
method with `(D0,O,D2,...)`. In the latter form D1 is consumed as the method
key. The native bridge does not independently insert the raw trigger key as
the Guide's A1. An explicit actor-reference token also requires resolution
before it becomes a Lua value. Selecting between these forms requires an
actual requested outer function, typed parameters and resolved binding.

The six-capture comparison at
`xivl-captures:studies/request-nmrush-caller-bindings/README.md` found no Guide
or NMRush Director class field and no selected Guide method call. That result
does not identify A1 or the returned option consumer, and does not establish
absence from the rest of the retained corpus.
