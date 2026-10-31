# Actor and Director initializer operands

The NPC and Director initializers use different argument layouts. The native
creation path and five Boolean controls precede the Lua arguments. A numeric
actor-class value belongs to the NPC Lua vector; it is separate from both the
path and the actor instance identity.

These are static substitutions into identified client consumers. A supplied
example is not evidence of a historical registration or a complete producer
domain. Work descriptors establish field types, not admitted server values.

| Subject | Meaning and supplied values / domain ceiling | Evidence locator | Confidence and unresolved boundary |
| --- | --- | --- | --- |
| `MapObjStandard` and `WolfStandard` | NPC superclass gates, common counts, then child suffix. Map object's `303,10405` are unused extra child arguments. Wolf's count `10` consumes `aggro=0`, `partsName=1` and eight booleans. | [NPC substitutions](#npc-substitutions); [common router](keyed-treasure-box-registration.md#lua-initializer-arguments) | Original instructions establish the common router and MapObj method arity. Wolf ancestry is recovered source. The two MapObj numbers' producer meaning remains unknown. |
| `GarudaNormal`, `GarudaMirageNormal`, `GarudaLesser`, `GarudaFeather` | The first three inherit `GarudaBaseClass`; feather directly inherits `MonsterBaseClass`. All reach the common NPC initializer. No per-class creation values are established. | [Garuda declarations](#garuda-declarations); `lua/registry.json`, exact Garuda members | Authenticated decompiled declarations, without an original operand check. Ancestry supplies no retail per-class defaults or vector differences. |
| `DoorStandard` child `A1/A2` | For actor class `5900001`, `0x141=321` is the layout selector, narrowed to low 16 bits; `0xB79=2937` is the full 32-bit instance selector. Both require native integer tag 0. | [Door selectors](#door-selectors); `xivl-client-structs:docs/door-initialization-native-contract.md`, Reaction-box arguments | Original Lua and promoted native instructions establish conversion and lookup. The exact layout resource, named object and physical placement remain unjoined. |
| `directorWork.directorId` and subclass suffix | `0x4E25=20005` is the Director ID. The Guildleve chain binds `12487,6,0,0,0` to leve ID, location and extra marker coordinates. `QuestDirectorMan0g001` reaches a different initializer whose recovered hook does not use `0,6,0,0,0`. | [Director substitutions](#director-substitutions); [retained Guildleve vector](guildleve-initializer-arguments.md#retained-12487-vector) | Original instructions establish the Guildleve chain. The Quest chain is decompiled-source evidence only. Location 6's place name and producer domains remain unknown. |

## NPC substitutions

The [registration envelope](keyed-treasure-box-registration.md#registration-envelope-and-appearance)
owns the typed path, five native controls and reader bounds. Those controls
are consumed before Lua `_onInit`. The first chooses the native initialization
arm; the other four govern optional native bundles. Their values cannot be
replaced with the two Lua gates below. Lua zero is truthy.

`NpcBaseClass._onInit(self,C,A2,A3,...)` stores `C` as
`npcWork.actorClassId` (`integer32`). Its numeric value is not supplied by the
examples below. `A2/A3` become the superclass game-parameter/event-work and
battle-work gates. The [common router](keyed-treasure-box-registration.md#lua-initializer-arguments)
owns the original instruction and superclass proofs, including count parsing
and open child forwarding. In that router, `b` is the first vararg, the event
count is at `j=2+b`, and the child suffix starts at `k=j+1+e`.

Positions in this table start after `C`, and therefore exclude `self`, the
native prefix and the actor-class value.

| Position after C | Consumer / declared type | MapObjStandard supplied value | WolfStandard supplied value |
| ---: | --- | --- | --- |
| 1 | Superclass `gameParameter` / Lua truthiness gate | `false` | `true` |
| 2 | Superclass battle-work setup / Lua truthiness gate | `false` | `true` |
| 3 | Battle-common count `b` / numeric count used by comparison and `select` | `0` | `10` |
| 4 | MapObj: event-common count `e`; Wolf: `npcWork.battleCommon.aggro`, `integer8` | `0` | `0` |
| 5 | MapObj: child suffix 1; Wolf: `npcWork.battleCommon.partsName`, `integer32` | `303` | `1` |
| 6 | MapObj: child suffix 2; Wolf: `partsExists[1]`, boolean | `10405` | `true` |
| 7 | Wolf `partsExists[2]`, boolean | absent | `false` |
| 8 | Wolf `partsExists[3]`, boolean | absent | `false` |
| 9 | Wolf `partsExists[4]`, boolean | absent | `false` |
| 10 | Wolf `partsExists[5]`, boolean | absent | `false` |
| 11 | Wolf `partsExists[6]`, boolean | absent | `false` |
| 12 | Wolf `partsExists[7]`, boolean | absent | `false` |
| 13 | Wolf `partsExists[8]`, boolean | absent | `false` |
| 14 | Wolf event-common count `e` | absent | `0` |

For MapObj, `b=e=0` gives `k=3`: both child hooks receive `303,10405`.
`MapObjStandard.initForEvent(self)` has one fixed parameter, no varargs and
only calls `_setGroundOn(false)` (source `:11-19`, original `root/proto0`,
zero-based CALL PC 2). The inherited battle hook is empty. Neither consumes
those two numbers. No layout, instance or other semantic name is established
for them on this class.

For Wolf, `b=10` puts `e` at vararg 12 and the child suffix at vararg 13.
The ten common values are exactly two numeric fields and eight booleans;
there is no child suffix. The assignments are in
`lua/scripts/chara/npc/npcbaseclass_battle.lua:13-70` (`aggro` at `:47`,
`partsName` at `:54`, `partsExists` at `:58-66`). `WolfStandard ->
WolfBaseClass -> MonsterBaseClass -> NpcBaseClass` follows the complete
eight-line declarations. These declarations contain no initializer override.
The `integer8` and `integer32` descriptors do not authenticate an aggro
enumeration, a parts-name catalog or a general accepted-value range.

## Garuda declarations

The complete selected decompiled members are eight-line declarations. Each
has only a require and class definition, with no local initializer:

| Class | Parent | Canonical member under `lua/scripts/chara/npc/monster/` |
| --- | --- | --- |
| `GarudaBaseClass` | `MonsterBaseClass` | `garuda/garudabaseclass.lua:1-8` |
| `GarudaNormal` | `GarudaBaseClass` | `garuda/garudanormal.lua:1-8` |
| `GarudaMirageNormal` | `GarudaBaseClass` | `garuda/garudamiragenormal.lua:1-8` |
| `GarudaLesser` | `GarudaBaseClass` | `garuda/garudalesser.lua:1-8` |
| `GarudaFeather` | `MonsterBaseClass` | `garuda/garudafeather.lua:1-8` |

The exact [registry records](../lua/registry.json) and corresponding
`.calls.json` sidecars agree with those declarations. `MonsterBaseClass`
in turn declares `NpcBaseClass` as parent. The common field roles above
therefore apply when such a vector is supplied, but these declarations do
not select a vector or prove a distinction in actual boss, mirage, lesser
or feather creation values. No retail Garuda aggro value, partsName value,
partsExists pattern or special child suffix is authenticated here.

## Door selectors

The [DoorStandard initializer](map-object-door-client-contract.md#doorstandard-initialization)
owns the class-specific routing. For the supplied post-class vector
`false,false,0,0,0x141,0xB79`, the first two values are superclass gates and
the next two are zero common counts. Child `A1=321` and `A2=2937` reach
`_setReactionTriggerBox` only in the `5900001` actor-class branch. They are
not assignments to the similarly named temporary schema fields.

The promoted native contract is
`xivl-client-structs:docs/door-initialization-native-contract.md`,
"Reaction-box arguments", `FUN_006F23F0 -> FUN_0075C7D0 ->
FUN_0058BF60 -> FUN_00590230`. The integer readers require tag 0, reading
four bytes each. `FUN_00590230` zero-extends the layout's low word.
`FUN_0059DF90` resolves that selector against layout entry `+0x58`, with
a child-layout fallback; `FUN_0059F190` retains the full instance selector
at object `+0x2C` for lookup using the resolved layout name. An existing
BG attachment skips creation.

The supported input ceiling is a correctly tagged 32-bit integer pair,
with only 16 bits used for layout selection on this path. This is not a
catalog of valid pairs. No keyed resource row has been joined here to
layout 321 and instance 2937, so their physical object's name and placement
remain unresolved.

## Director substitutions

The [Guildleve initializer contract](guildleve-initializer-arguments.md)
owns original `DirectorBaseClass._onInit` and Guildleve forwarding and the
retained `12487` vector. Its PC convention is one-based, unlike the
zero-based NPC locators above. Director `_onInit` stores its first non-self
argument and forwards the remaining tail to the subclass `init` unchanged.
Here `G` is the selected Guildleve ID; the retained example has `G=12487`.

| Non-self position at `_onInit` | Guildleve chain: supplied value -> field / descriptor | QuestDirectorMan0g001 chain: supplied value -> recovered consumer |
| ---: | --- | --- |
| 1 | `0x4E25=20005` -> `directorWork.directorId`, `integer32` | `0x4E25=20005` -> the same Director ID field |
| 2 | `G` (retained `12487`) -> `guildleveWork.guildleveId`, `integer16` | `0` -> first suffix argument; no named field assignment |
| 3 | `6` -> `guildleveWork.aetheryteLocation`, `integer8` | `6` -> second suffix argument; no named field assignment |
| 4 | `0` -> `guildleveWork.exMarkerX`, `float` | `0` -> third suffix argument; no named field assignment |
| 5 | `0` -> `guildleveWork.exMarkerY`, `float` | `0` -> fourth suffix argument; no named field assignment |
| 6 | `0` -> `guildleveWork.exMarkerZ`, `float` | `0` -> fifth suffix argument; no named field assignment |

The numeric zeros in the Guildleve columns are coordinate values, not NPC
common counts or Boolean gates. The descriptor types are declared at
`lua/scripts/director/directorbaseclass.lua:63-66` and
`director/guildleve/guildlevebaseclass.lua:211-283`. These storage
descriptors do not establish serialized token choices or producer ranges.
The [Guildleve UI contract](content-director-ui-contracts.md#guildleve-and-request-directors)
owns their downstream uses: the leve ID selects sheet/UI data, location 6
selects normal rather than small marker size, and extra coordinates feed
the separate extra-marker path when its signal condition holds. Location 6 has no established
place name. A same-valued static plate-icon use of 20005 does not prove a
universal Director producer rule
(`xivl-decomp:docs/net/guildleve-initializer-route.md`, "Director ID and the sheet's border field").

`QuestDirectorMan0g001 -> QuestDirectorBaseClass -> DirectorBaseClass`
is a separate chain. The complete recovered leaf is a declaration
(`director/quest/questdirectorman0g001.lua:1-8`). The parent's
`init(self,...)` declares only child reserves in `questDirectorWork._temp`
and `_sync`, calls `getOwnClientQuestId`, then forwards the suffix to
`initAsQuestDirector` (`questdirectorbaseclass.lua:11-42`). The inherited
`initAsQuestDirector(self,...)` is empty at `:45-48`; the leaf does not
override it. Thus the recovered code supplies no meaning or type to its
five suffix values. In particular, its 6 is not established as
`aetheryteLocation`, and its zeros are not established as marker coordinates.
The incomplete recovered branches in other Quest methods provide no stronger
runtime or original-bytecode conclusion.

## Source identity and evidence strength

The decoded source members matched their exact
[scripts.json](../manifests/scripts.json) rows in the authenticated corpus
archive, extraction `2012.09.19.0001`, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`
([archive manifest](../manifests/private_lua_corpus.json)). Source hashes below
identify the newly described declarations and Quest methods; they do not
constitute original instruction checks.

| Member basename | Canonical source SHA-256 |
| --- | --- |
| `mapobjstandard` | `e930f06afb942c660d7934e918c0507d8a722bb025857138c2a42b41e9f6c794` |
| `wolfstandard` | `179636d9003724172be35db96b8624ffbee5af162b837a54d591999cc7cbd12a` |
| `wolfbaseclass` | `d87520b72c72410423271e40e24fab791250b038a735c1fe8de1a164b2382fe2` |
| `monsterbaseclass` | `08aff923704ebec221743e1cdfe6d79d3173164dd5eb4de250ce1302e3629a76` |
| `garudabaseclass` | `f841305aabc7c03a5acf819ac25d6036a93481d65fb0c3c54d8a6422dfde1b33` |
| `garudanormal` | `7ecdb63500256880a5cdb965820e0dd53a85fe10c025814d0e76eb74112d9c15` |
| `garudamiragenormal` | `958fa001fd7d4b2dfa35453b4d6772b0e1fd1d4ac29e59650ba41482e92bf447` |
| `garudalesser` | `c3fbebb8d483eb472821d62198f265a4f5a3e5571576115580d4e61d2a230beb` |
| `garudafeather` | `c3e7866b7a4780900ed430f8ace34492e3637d7ac6b918428387c0b544fb7564` |
| `questdirectorman0g001` | `070599dcaf7acb1b8822e6cceb249df3746e71d1903477e3f062c9a0dba53466` |
| `questdirectorbaseclass` | `9e15543ca98e695ff26713a58f5bb8cd8acf77d77e5a4efcb186bd52b32d3929` |

The MapObj arity observation also has a completed original Lua 5.1 operand
check: resource `729s9/wu7/x9uv80/x9uv80rq9w69s6.le.lpb`, original SHA-256
`afa2a9a1427b1f0865515de05556a6cbc695e1266591c2c300255a8994e57bdd`,
decoded payload SHA-256
`a2a140cef245797e71c19ed56873b054495f07b6d837689098c71f778609144e`.
Root closure/assignment identifies `initForEvent`; `root/proto0` has one
fixed self parameter, no vararg and CALL PC 2 as described above. Original
and payload identities are in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
The linked common, Door and Guildleve contracts retain their own original
proofs. No original operand proof is asserted for the Garuda declarations,
Wolf declarations or Quest initializer chain, and no live registration is
established by these static substitutions.
