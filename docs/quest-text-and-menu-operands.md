# Quest text and menu operands

These retail 1.23b findings separate text lookup keys, ordered formatting
arguments, and actual event producers. Formatting arguments below are numbered
from one. A source row or callable helper establishes its own contract, without
establishing which external event invoked it.

| Subject | Meaning | Values or domain | Evidence locator | Confidence and remaining limit |
| --- | --- | --- | --- | --- |
| Rivenroad menu keys | Duty-name keys passed to the generic raid-entry question. | `xtx_raidDungeon` key 15 is Rivenroad; key 16 is Rivenroad (Hard). | [Instance entry identities](instance-entry-client-contracts.md#variant-identities-and-unresolved-admission-fields), rows for Rivenroad; generic helper in Exact client event and result boundaries. | Confirmed static names and original helper operands. The NPC instance, admission dispatcher, Director and destination remain unresolved. |
| Task Board guild argument | `Noc000.pETaskBoardGuild` forwards one job-name formatting key to row 66. | Selected `xtx/text_jobName` keys 29-36 and 39-41. Row 67 takes level, item, quality and quantity in that order. | [Task Board speech operands](quest-event-client-contracts.md#task-board-speech-operands); `xivl-client-data:docs/message-operand-rows.md`, noc000 66/67 and selected job-name keys. | Confirmed original forwarding and selected static expressions. Arbitrary integer acceptance, every class-ID equivalence and server guild eligibility remain unproved. |
| Man2u0 messages 176-178 | Proximity refusal, ineffective item use on a target, and effect expiration for Niellefresne's Gold Dust. | Item 11000081 is embedded in all three rows. Row 177 takes its target display-name key from formatting argument 1. | `xivl-client-data:docs/message-operand-rows.md`, man2u0 176-178; [Man2 source boundary](#man2u0-fixed-item-messages). | Confirmed static expression layout and canonical source identity. The actual producer of rows 176-178 remains unresolved. |
| Their Finest Hour: Earthbreaker objective and disposal | Generic item-use objective text can describe an item and target. | Candidate `worldMaster` row 51075 uses item argument 1, display-name argument 2 and group/singular selector argument 3. The actual Earthbreaker tuple and disposal row are unresolved. | `xivl-client-data:docs/message-operand-rows.md`, worldMaster 51075; [objective template boundary](#earthbreaker-objective-and-disposal). | Confirmed generic static template. Its use by this duty is unverified. No disposal-row or item-removal producer is authenticated. |
| Burning Man: post-battle docks | `Com0u5.processEvent025` presents scene `com0u610` and fades in after warp. | No post-battle private-area class, numeric type, instance key or zone is established. | [Com0 instanced cutscene calls](quest-event-client-contracts.md#com0-instanced-cutscene-calls); [area initialization](area-base-client-initialization.md). | Confirmed recovered scene call and generic base initialization. The post-victory area binding remains unresolved. |

## Rivenroad menu names and result

The names belong to the `xtx_raidDungeon.csv` namespace, English field 26,
rows 15 and 16. They are not zone, NPC, quest or Director IDs. The
[instance entry contract](instance-entry-client-contracts.md) owns the selected
static joins and the unresolved original, repeatable and Hard admission routes.

`InstanceRaidGuideBaseClass.askEnterInstanceRaid(self,dutyKey)` passes
`dutyKey` as the formatting tail of desktop question row 52045, using answer
rows 52046 and 52047. Its original `root/proto2`, call PC 15 and return PC 19,
establish exactly one Boolean result: true only for answer 1. This question and
result do not bind either duty key to an entry NPC or accepted transition.
The complete original identity and reproduction are in the canonical contract.

## Task Board formatter positions

`Noc000` owns text bank `(5923,"noc000")`. The
[canonical speech contract](quest-event-client-contracts.md#task-board-speech-operands)
records the complete method arguments and original call operands. The
`TaskBoard` object member itself supplies `initForEvent`, rather than these
speech methods.

| Text row | Formatting position | Role and evidence ceiling |
| --- | ---: | --- |
| noc000 66 | 1 | Job-name lookup key. Japanese and German expressions use `xtx/text_jobName`; English omits the label. |
| noc000 67 | 1 | Level presentation. No level eligibility range follows from this position. |
| noc000 67 | 2 | Item lookup key. |
| noc000 67 | 3 | Quality selector. The selected expression contains the empty, +1, +2 and +3 text alternatives. This does not establish a server acceptance rule. |
| noc000 67 | 4 | Quantity presentation and item-name formatting quantity. |

The selected key-to-name mapping is canonical in
`xivl-client-data:docs/message-operand-rows.md`: 29-36 name carpenter,
blacksmith, armorer, goldsmith, leatherworker, weaver, alchemist and culinarian;
39-41 name miner, botanist and fisher. These selected values establish the
formatter's job-name domain. No separate guild enumeration or universal
guild-to-class conversion is established by these expressions.

`Noc001` is a separate text route: its selected speech methods use rows 20
and 21 rather than noc000 rows 66 and 67
(`lua/scripts/quest/scenario/noc/noc001.lua:23-53`). Those row numbers must
retain their own text owner. The noc000 expression layout above does not
authenticate the noc001 row layout.

## Man2u0 fixed-item messages

The canonical `Man2u0.initText` loads `(1367,"man2u0")`
(`lua/scripts/quest/scenario/man/man2u0.lua:11-19`). The static expressions
belong to `xivl-client-data:docs/message-operand-rows.md`, man2u0 176-178,
with source identities in `xivl-client-data:manifests/tables.json`.

| Row | Meaning | Fixed lookup | Dynamic formatting dependency |
| --- | --- | --- | --- |
| 176 | Proximity refusal. | Item 11000081. | No item or target key is supplied by a formatting argument in the selected expression. |
| 177 | The item has no effect on the named target. | Item 11000081. | Argument 1 selects `xtx/displayName`. |
| 178 | The item's effect expires. | Item 11000081. | No item or target key is supplied by a formatting argument in the selected expression. |

Item 11000081 is Niellefresne's Gold Dust. Row 177 therefore requires the
target display-name key in the first formatting position. A tail ordered
`(itemId,nameId)` would use `itemId` as the target-name key. The row does not
consume a supplied item key before the name.

The named `processEventSystemMessage` method at canonical lines 604-623
selects rows 179 and 180 from its supplied value. That method is not a
producer proof for rows 176-178. Neither the static wording nor the item
reference proves the corresponding combat effect, item consumption, or
external event invocation.

The canonical member and the separately recovered composite-scene artifact
have distinct decoded identities:

| Artifact | SHA-256 | Identity locator |
| --- | --- | --- |
| Canonical `quest/scenario/man/man2u0.lua` | `7eb43e5b29acc9e9b76164c568a5eab3049599f93fcbab2a45f67c9f6859dee7` | [scripts.json](../manifests/scripts.json), `lua/scripts/quest/scenario/man/man2u0.lua`. |
| Canonical decoded LPB payload | `51ac82341b6fa0a2ccd6df8f61cf32cc9793904fe44f1f4aed1e92a3f2a88228` | [retail_lua_coverage.json](../manifests/retail_lua_coverage.json), original `tp5rq/r75w9s1v/x9w/x9whpj.le.lpb`. |
| Separately recovered composite-scene Lua | `9843a8314d1a32a116a2e7192888626b6043c239937f89ad4b5d627118e562ab` | [Man2 city scenario composite scenes](quest-event-client-contracts.md#man2-city-scenario-composite-scenes), Man2u0 identity row. |

The original LPB identity is
`deed0213ddd0c57edb09dd9a7ff216769658c3a710142bb036fcb597a9149992`.
The composite-scene artifact supports its documented presentation sequences.
Its identity does not independently authenticate an emitter for rows 176-178.

## Earthbreaker objective and disposal

`worldMaster.csv` English field 1, row 51075, is a generic item-use defeat
objective. Its selected layout is canonical in
`xivl-client-data:docs/message-operand-rows.md`.

| Candidate row | Formatting argument 1 | Formatting argument 2 | Formatting argument 3 |
| --- | --- | --- | --- |
| worldMaster 51075 | Item key. | Display-name key. | Group/singular selector. |
| worldMaster 51003 | Display-name key. | Group/singular selector. | No third dependency in the selected expression. |

Row 51003 has no item lookup, so it cannot reproduce the item-specific
wording of row 51075. This comparison identifies text layouts, not the
Earthbreaker duty's actual row or emitted tuple. Source identity for both
rows belongs to `xivl-client-data:manifests/tables.json`, `worldMaster.csv`.

The exact Earthbreaker objective producer, third-selector value, disposal
message row and disposal arguments remain unresolved. A matching generic
template does not establish item removal, credit for each participant or
the return transition. The selected quest presentation and Director evidence
in [quest event contracts](quest-event-client-contracts.md) does not close
those joins. A direct emitter or observed complete message tuple is needed
to assign the objective and disposal rows.

## Post-battle docks area

The [Com0 scene contract](quest-event-client-contracts.md#com0-instanced-cutscene-calls)
records `Com0u5.processEvent025` presenting `com0u610`, followed by a
post-warp fade-in. A scene identifier supplies no area initialization record
or proof that this method followed a particular victory.

The [private-area base contract](area-base-client-initialization.md) records
superclass argument forwarding and `init(_getZoneName())`.
`PrivateAreaMasterPast` inherits that base and has an empty own `init`
(`lua/scripts/area/privatearea/privateareamasterpast.lua:1-14`, source
SHA-256 `0cf88fb0e965f9b157a40afc58913c8dd792a396dac199d3aa6d1e319e0818f7`).
Its class name does not bind it to the docks or a numeric private-area type.

The post-battle docks class, instance key, private-area type, zone and runtime
owner remain unresolved. A static docks resource or matching scene name
does not supply that binding. An area-bearing initialization or runtime record
tied to the post-victory lifetime is needed to establish it.

## Evidence scope

Canonical Lua identities use extraction `2012.09.19.0001` and the
[script manifest](../manifests/scripts.json). Selected source claims above
retain their decompiled-source boundary. Original instruction claims are
limited to the existing authenticated helper and speech contracts linked
above. Static row layouts retain the client-data evidence tier. No live
rendered message, actual admission, objective transaction or post-battle
area transition is established by these findings.
