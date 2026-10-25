# To Kill a Raven client quest and Rivenroad mode boundary

The retail Gcl107 resource is shared by all three To Kill a Raven quest
identities. Its 34 methods implement dialogue, player choices, text selection,
and scene presentation. They do not provide the Rivenroad battle state machine.
The client distinguishes Rivenroad and Rivenroad (Hard) in its content UI, but
the inspected encounter classes do not bind Lesser/Normal to those content IDs.

## Identity and method coverage

The three To Kill a Raven IDs 111433, 111633 and 111833 share
`/Quest/Scenario/Gcl/Gcl107`. The canonical ID/title and SAN evidence is
`xivl-client-data:docs/grand-company-quest-identities.md`.
The separate Gcg107 and Gcu107 resources contain initialization only in their
retained quest contracts; their names do not establish separate quest ownership.
Source: `data/quest_contracts.json`, Gcl107 record; original resource
`client/script/tp5rq/r75w9s1v/37y/37yijc.le.lpb`, 17770 bytes,
SHA-256 `c816bd5d08eeee019f4c7bdd93942de143a28bff8f63f8161d5ab14791b90a7e`.
Decoded Lua bytecode SHA-256:
`3b003570fc6d9bf23acf12f2d2333b142bee7fe6c5fc56388702d8f0f717a96b`.
Canonical decoded-source SHA-256:
`98ce0ae86655eccffbc15234091dbbba9acc847c1bbb099ae8f5f64bfdab1345`.
The original LPB, payload, and decoded source match their retained manifests.
The SAN catalog was reproduced in full from the pinned original.

The matrix covers every declared Gcl107 method. Code offsets are byte offsets
in the decoded payload to the first instruction; PCs are zero-based within
the method. Text PCs identify callsites, not executed dialogue or quest order.
The parser is `tools/build_quest_contracts.py:ChunkReader` and `analyze_chunk`.
Ordinary dialogue methods also contain actor talk-turn and scheduler calls;
those supplied actor arguments do not identify server NPC IDs.

| Method | Prototype / code offset | Complete PC range | Text-call PCs / other recovered role |
| --- | --- | --- | --- |
| `initText` | `root/proto0` / `0x59C` | 0-4 | Loads text resource 10496, gcl107, at PC 3 |
| `processEventStartLim` | `root/proto1` / `0x60B` | 0-86 | say 20, 25, 33, 38, 46, 55, 63, 68, 76, 82; showQuestInfomation 48 |
| `processEventStartGri` | `root/proto2` / `0x8B7` | 0-86 | say 20, 25, 33, 38, 46, 55, 63, 68, 76, 82; showQuestInfomation 48 |
| `processEventStartUld` | `root/proto3` / `0xB63` | 0-86 | say 20, 25, 33, 38, 46, 55, 63, 68, 76, 82; showQuestInfomation 48 |
| `processEventGuincum` | `root/proto4` / `0xE21` | 0-27 | say 11, 16, 24 |
| `processEventFulke` | `root/proto5` / `0xF4C` | 0-27 | say 11, 16, 24 |
| `processEventAubrey` | `root/proto6` / `0x1077` | 0-27 | say 11, 16, 24 |
| `processEventKinnison01` | `root/proto7` / `0x11A2` | 0-27 | ask 16; say 11, 23 |
| `processEventMerlwyb1` | `root/proto8` / `0x12D6` | 0-74 | say 13, 18, 23, 31, 36, 44, 49, 57, 66, 71 |
| `processEventSenna01` | `root/proto9` / `0x1517` | 0-77 | say 13, 18, 23, 31, 36, 44, 52, 61, 66, 74 |
| `processEventRaubahn1` | `root/proto10` / `0x175B` | 0-79 | say 13, 18, 23, 31, 36, 44, 49, 57, 63, 71, 76 |
| `processEventEynzahr` | `root/proto11` / `0x19B9` | 0-40 | say 10, 18, 23, 32, 37 |
| `processEventSwethryk` | `root/proto12` / `0x1B2A` | 0-40 | say 10, 18, 23, 32, 37 |
| `processEventEline` | `root/proto13` / `0x1C92` | 0-40 | say 13, 18, 23, 32, 37 |
| `processEventCid01` | `root/proto14` / `0x1E03` | 0-19 | say 11, 16 |
| `processEventKinnison02` | `root/proto15` / `0x1EFC` | 0-27 | ask 16; say 11, 23 |
| `processEventMerlwyb2` | `root/proto16` / `0x2030` | 0-119 | say 13, 32, 40, 45, 50, 58, 63, 68, 76, 81, 86, 94, 105, 111, 116 |
| `processEventSenna02` | `root/proto17` / `0x239B` | 0-114 | say 13, 35, 40, 48, 53, 61, 66, 71, 79, 84, 92, 101, 106, 111 |
| `processEventRaubahn2` | `root/proto18` / `0x26E9` | 0-127 | say 10, 32, 43, 48, 59, 64, 72, 77, 82, 90, 95, 100, 110, 116, 124 |
| `processEventShtola` | `root/proto19` / `0x2ABC` | 0-32 | say 11, 16, 21, 29 |
| `processEventPapalymo` | `root/proto20` / `0x2C04` | 0-40 | say 11, 16, 24, 29, 37 |
| `processEventYda` | `root/proto21` / `0x2D7E` | 0-32 | say 11, 16, 24, 29 |
| `processEventThancred` | `root/proto22` / `0x2EC6` | 0-90 | ask 16; say 11, 26, 31, 36, 44, 57, 62, 67, 75 |
| `processEventCid02` | `root/proto23` / `0x3159` | 0-19 | say 11, 16 |
| `processEventMerlwyb3` | `root/proto24` / `0x3252` | 0-35 | say 13, 18, 27, 32 |
| `processEventSenna03` | `root/proto25` / `0x33AF` | 0-32 | say 13, 18, 24, 29 |
| `processEventRaubahn3` | `root/proto26` / `0x34EE` | 0-35 | say 13, 18, 27, 32 |
| `processEventCid03` | `root/proto27` / `0x364B` | 0-128 | say 11, 16, 21, 29, 35, 40, 48, 59, 69, 77, 92, 97, 105, 111, 117, 125 |
| `processEventStewart` | `root/proto28` / `0x39EA` | 0-155 | askExtendWidget 37; say 23, 51, 59, 74, 83, 92, 101, 114, 122, 131, 142 |
| `getTextIdStewart` | `root/proto29` / `0x3DEA` | 0-50 | Caller-boolean text remapping; see below |
| `processEventCid04` | `root/proto30` / `0x3F82` | 0-82 | say 11, 16, 24, 29, 37, 42, 47, 55, 60, 68, 74, 79 |
| `processEventKinnison03` | `root/proto31` / `0x41F5` | 0-40 | ask 16; say 11, 36; scene gc010750 27 |
| `processEventNq1` | `root/proto32` / `0x43C1` | 0-11 | Scene gc010710 at PC 7 |
| `processEventNq2` | `root/proto33` / `0x448F` | 0-13 | Scene gc010714 at PC 8 |

The root declares Gcl107 with parent ScenarioBaseClass and registers the 34
methods (root PCs 0-109). The full chunk has 35 prototypes and no nested
closure beyond these methods. The retained analysis reports no unresolved
calls, direct actor-class lookups, or explicit quest-work accesses. That does
not establish the behavior of inherited helpers or of external callers.

## Stewart's alternate entry description

`processEventStewart` at code offset `0x39EA` takes four caller arguments after
self. Its fourth argument is passed to `getTextIdStewart`; no content ID or
difficulty enum is decoded from it in this method. The text helper at `0x3DEA`
returns its input unchanged unless the boolean argument equals true. It then
maps 164->321, 165->322, 169->326, 170->327, 171->328, 172->329,
175->330, 178->332 and 179->333 (PCs 0-49); other text IDs remain unchanged.

The caller opens `askExtendWidget` at PC 37 with prompt 165 or 322 and trailing
literal arguments `(3, 1, 1)`. Result 1 presents rows 178/179 or 332/333 and
exits the loop. Result 2 presents entry-description rows and repeats the menu.
Results 3 and -3 exit; the method returns the selected result at PC 154.
When the fourth caller argument equals true, it omits rows 173/174 and 177.
This is client choice processing, not a recovered instance-launch call.

Authenticated `xivl-client-data:csv/gcl107.csv` numeric column 1 (physical CSV cell 3),
SHA-256 `6443eae90fbf3572c553194c85658e54b0689a04aca8b2b5020efc52976cafa1`,
distinguishes the two descriptions:

| Text rows | Direct English-text evidence | Limit |
| --- | --- | --- |
| 171 | Each party member must fulfill entry requirements for one of three To Kill a Raven quests | Text does not implement eligibility |
| 328, reached from 171 when caller boolean is true | Each party member must have completed To Kill a Raven and Living on a Prayer | Does not directly bind the boolean to content 16 |
| 138/170/327 | Byte-equal entry descriptions encode the constant words four/eight and literal level 45 | Fixed description operands, not a selected runtime row or eligibility test |
| 172/329 | Distinct "All assaults on" / "All forays into" wording shares a literal 30-minute number frame and duty-reference control | Description text does not prove the timer or its enforcement |
| 173/174 and 177, omitted when true | Refueling/maintenance explanation and greater rewards for parties representing all three Grand Companies | No reward formula or cooldown recovered |

This is evidence for alternate entry-description text. Calling it the hard-mode
dispatch would require the missing caller-argument-to-content join.

### Embedded entry values

`xivl-decomp:docs/resource/rich-string-entry-counts.md` owns the constructor,
handler and recursive-selection proof for the two count controls. The selected
conditions and list indices are literal, so their static outputs are `four`
and `eight` without a supplied count argument. The standalone level frame is
`02 20 02 2E 03`, whose immediate operand is 45. Rows 172/329 share
`02 20 02 1F 03`, whose immediate operand is 30. The selected number/decimal
path is documented in
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-05/06.

The lossless annotation-to-byte relationship is documented in
`xivl-tools:docs/formats/ssd-sheet.md`, Rich-string control tokens and
Rich-string read and text-export contract.
This interpretation uses the authenticated decoded CSV member, without a fresh
sheet-resource extraction or a historical renderer invocation.

At `processEventStewart` PC 83, the row-170 call supplies worldMaster, the
quest receiver, `getTextIdStewart(quest,170,A4_2)` and `A3_2` unchanged
(decoded Lua lines 2228-2238). The adjacent 171/172 calls pass the same value.
The [WorldMaster message argument contract](worldmaster-message-arguments.md)
traces these values through the shared helpers to the declared native target
`_appendMessagePool_cpp`. The fixed description controls do not establish
A3_2's runtime value/type, the native formatter-vector relationship, the
selected duty reference, caller mode or server admission predicates.

The separate
`xivl-decomp:docs/script/worldmaster-message-pool.md` profile qualifies the
native argument route. If the selected English cell is looked up and A3_2
takes the accepted integer-capture path, its captured dword supplies the row
for that cell's `xtx/raidDungeon` reference, logical field 26. The profile does
not select a historical value, default locale, duty or caller mode.

## Scenes and encounter classes

`processEventKinnison03` asks row 16 at PC 16, then conditionally wraps
`startNQCutScene("gc010750", ...)` at PC 27 in fade helpers.
`processEventNq1` calls gc010710 at PC 7; `processEventNq2` calls gc010714 at
PC 8. See [scene/replay joins](quest-scene-replay-joins.md) for exact replay rows.
Scene presence and callback names do not establish quest stage order.

The original `InstanceRaidLesserWhiteGeneral` has three methods:
`processStartEvent` (`0x153`, PCs 0-5) calls `executeCutScene` with gc010715,
its supplied argument, and true; `processCutSceneEvent` (`0x1B6`, PCs 0-23)
uses caller-supplied scene and weather arguments; `processDummy` (`0x2D3`, PC 0)
returns no values. The [content-director contract](content-director-ui-contracts.md)
owns the precise fade/weather/scene call order.

Original WhiteGeneralBaseClass, WhiteGeneralLesser, WhiteGeneralNormal,
WhiteGeneralAttackWeaponSkill and InstanceRaidNormalWhiteGeneral each contain
only require/class definition and return (root PCs 0-7), with no child methods.
This strengthens the registry's pattern-derived absence into a bounded original
bytecode fact for those five chunks. It does not describe inherited behavior.
The prior [Rivenroad presentation finding](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/rivenroad-presentation.md)
owns WhiteGeneralMeteor's off-ground setting, m091/m917 resource identities,
the Golem/Lentigo identity-only boundary, and arena geometry. Those resources
do not supply meteor/golem counts, movement, spawn policy, or encounter phases.

### WhiteGeneral monster director declarations

The separate `MonsterWhiteGeneralBaseClass`, `MonsterWhiteGeneralLesser`
and `MonsterWhiteGeneralNormal` chunks define director classes. Their original
bytecode supplies no battle logic or initialization fields.

`MonsterWhiteGeneralBaseClass` requires
`/Director/Monster/MonsterDirectorBaseClass`, then calls
`_defineBaseClass("MonsterWhiteGeneralBaseClass", "MonsterDirectorBaseClass")`.
Its root has eight instructions at decoded offset `0x20`: require at PC 2,
class definition at PC 6, and a zero-value return at PC 7. It has no child
prototypes or locally declared methods.

Lesser and Normal each require
`/Director/Monster/WhiteGeneral/MonsterWhiteGeneralBaseClass` and call
`_defineClass` with their own class name and parent
`MonsterWhiteGeneralBaseClass`. Each root has eleven instructions at `0x20`.
The calls are at PCs 2 and 6; PCs 7-9 assign the sole child closure to the
class's `init` field; PC 10 returns no values. Both callsites discard results.

Each `init` is `root/proto0`, at decoded offset `0x113` (275), with one
parameter and no varargs, constants, upvalues or nested prototypes. Its entire
body is PC 0, `RETURN A=0 B=1`: no calls, field writes or returned values.
In particular, Lesser/Normal do not initialize distinct encounter fields in
these chunks. This does not establish how the class-definition helpers or
inherited methods behave.

Sources: `lua/scripts/director/monster/whitegeneral/monsterwhitegeneralbaseclass.lua:1-8`
and `monsterwhitegenerallesser.lua:1-15` / `monsterwhitegeneralnormal.lua:1-15`.
The original LPB, decoded payload and canonical source identities match
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`scripts.json`](../manifests/scripts.json). Exact whole-chunk instruction
checks cover all three roots and both init bodies. These director declarations
do not bind Lesser/Normal to content 15/16 or establish authoritative battle
AI, encounter phases or runtime mode selection.

## Command and animation boundary

The authenticated SAN assigns commands 23596, 23603, 23608, 23616,
23624-23626 and 23645 to WhiteGeneralAttackWeaponSkill. Crucially, commands
23614 and 23615 instead map to `/Command/Game/WeaponSkill/MonsterAttackWeaponSkill`.
The latter original chunk defines only the six getters documented in the
[getter profile](monster-attack-weapon-skill-profiles.md): getCommandInformation,
getFrequency, getRangeWidth, getRangeRotate, getCommandRangeHeight and
getPartsDamageAdjust. Its only member call is getCommandId, once in each
getter. There is no direct animation-bank getter or resource lookup in this
chunk. For 23614, getFrequency returns 6; for 23615 it returns the default 1.
Those values do not independently prove hit count or attack cadence.

The WSS18/19 association with Chaos Thrust/Twisting Vice remains an inference.
As established by `xivl-decomp:docs/actor/garuda-tornado-presentation.md`,
battle-result opcodes 0x0139-0x013c carry independent command and animation IDs.
`xivl-decomp:docs/actor/animation-bank-routing.md` describes the packed bank
selector. Therefore this route needs no command-ID-to-WSS table to present a
result. Closing this specific gap requires a correlated retail command/animation
pair or another authenticated producer connecting 23614/23615 to the packed
m917 bank selectors. The preserved s_awl_on EffectEnd -> RaptureChantSyncClip
mismatch remains as documented in the Rivenroad presentation finding.

## Normal and hard evidence remain separate

| Evidence question | Observed client evidence | Unresolved association |
| --- | --- | --- |
| Content UI identity | Rivenroad is selector 15/native index 14; Rivenroad (Hard) is selector 16/native index 15, as recorded in [timer consumers](myplayer-timer-consumers.md) | No historical captures were inspected here |
| Scenario resource and entry descriptions | Three To Kill a Raven IDs alias Gcl107; alternate entry-description text names Living on a Prayer completion | Stewart's fourth argument is not joined to content 15/16 |
| Instance classes | LesserWhiteGeneral has gc010715 and supplied scene/weather handlers; NormalWhiteGeneral has initialization only | Neither class is bound to a normal/hard content ID by this evidence |
| Command variants and assets | Shared command catalog and presentation resources | No mode-specific dispatch or variant selector authenticated |
| AI and encounter state | No encounter state machine recovered | Phase order, HP, timers, damage, targeting, golem/meteor counts and movement remain unknown for both modes |

## Authenticated original inputs

All paths below are relative to `client/script/`. The LPB and decoded payload
hashes are SHA-256 and match `manifests/retail_lua_coverage.json`; decoded source
hashes also match `manifests/scripts.json`. The selected source members were
read from the archive pinned by `manifests/private_lua_corpus.json`.

| Class resource | Original path | LPB SHA-256 | Payload SHA-256 |
| --- | --- | --- | --- |
| `monsterattackweaponskill.lua` | `7vxx9w6/39x5/n59uvwrz1yy/xvwrq5s9qq97zn59uvwrz1yy.le.lpb` | `8c239de7b4e5b2d924a1d915ae09149fe17bccc49226a6028bbfee5db2711015` | `7727092398c5b36accc1036d988b913b5ec7d3c9cb32a3156c782dec80c5221a` |
| `gcl107.lua` | `tp5rq/r75w9s1v/37y/37yijc.le.lpb` | `c816bd5d08eeee019f4c7bdd93942de143a28bff8f63f8161d5ab14791b90a7e` | `3b003570fc6d9bf23acf12f2d2333b142bee7fe6c5fc56388702d8f0f717a96b` |
| `whitegeneralattackweaponskill.lua` | `7vxx9w6/39x5/n59uvwrz1yy/n21q535w5s9y9qq97zn59uvwrz1yy.le.lpb` | `6c30e201333a48a54ce443f3e44f540585542e4468a57466ef60d7b583313dff` | `6adc82fdd9f38c5411a9f8b0be846294874ded23838ae18987acfb12ea412635` |
| `whitegeneralbaseclass.lua` | `729s9/wu7/xvwrq5s/n21q535w5s9y/n21q535w5s9y89r57y9rr.le.lpb` | `07b315d56323306cca21022bea874bcebbe54b91bc47d8c32097d5e9233b3060` | `eeb6949a1bc7aa9affde9b6a969f6c3a52a14d03d30630a927c1df1fc97902b0` |
| `whitegenerallesser.lua` | `729s9/wu7/xvwrq5s/n21q535w5s9y/n21q535w5s9yy5rr5s.le.lpb` | `42af74915f4959573f7947d70eb6784f71d968fcf627319ad366cc8ee8dafc83` | `242d69a9776f689d2ef807e70638e499fe194ba865632f428e679b8a504e1eb8` |
| `whitegeneralnormal.lua` | `729s9/wu7/xvwrq5s/n21q535w5s9y/n21q535w5s9ywvsx9y.le.lpb` | `ecd1c01b4010683338a3d2b438c8495d14c79cc96815bb9c9a051ba15cf290a1` | `56e775cf30187e3b9008eaeb319f5aff679574e066f0220f91a75a01082f112e` |
| `instanceraidlesserwhitegeneral.lua` | `61s57qvs/1wrq9w75s916/1wrq9w75s916y5rr5sn21q535w5s9y.le.lpb` | `f6e5631947f42562dcb6b865f45c9122c4e50bc002235c28a04846e174e272e7` | `5f5d1b3e8dfe776d208803166eed1b92c987817a43112a26d5ba50c7290433d4` |
| `instanceraidnormalwhitegeneral.lua` | `61s57qvs/1wrq9w75s916/1wrq9w75s916wvsx9yn21q535w5s9y.le.lpb` | `e21b34f19e8a78b82f32660ed8a1b2cffb8e547885aeaaa1cc50eabcefa3ea32` | `9cb91d078304277fd3a8d97e562c64e049d2b241332aafcc0bef633bace769ee` |
| `monsterwhitegeneralbaseclass.lua` | `61s57qvs/xvwrq5s/n21q535w5s9y/xvwrq5sn21q535w5s9y89r57y9rr.le.lpb` | `d843213e32b47cc44cc66f630b4e6d8d723493b560b810a755a800e1e1d0a364` | `2510b9bc678cede76b664ff97be6ba9f727bb6126ba425c8047f4b88bc005985` |
| `monsterwhitegeneralnormal.lua` | `61s57qvs/xvwrq5s/n21q535w5s9y/xvwrq5sn21q535w5s9ywvsx9y.le.lpb` | `10a8e3701844485888e5b31183d7fa2b507d42abe7a3461fc7f9cdf703f5f423` | `e1f8df9c91f24ab2624fcedd3159ef7bb615bbfb8aed7d608b0159b174b13d1e` |
| `monsterwhitegenerallesser.lua` | `61s57qvs/xvwrq5s/n21q535w5s9y/xvwrq5sn21q535w5s9yy5rr5s.le.lpb` | `6fff4fa3a9b4197b99ad2e567bb722b58cc1144950b23dca0bcf8fa6f3138d34` | `d40e9eabc3cb3496f1763ca4d4186dbf4e65c12bdc51668e316bae972ff2385a` |
