# Guildleve party continuity

The retail 1.23b client separates the player party, content-group membership
and guildleve Director presentation. The inspected membership callbacks do
not transfer or retire the Director when a party leader or participant
disappears. That is a statement about those callbacks, not a rule that the
server preserves a running leve.

| Question | Static client result | Remaining discriminator |
| --- | --- | --- |
| Starter/leader leaves the party, zone or connection, or is removed | No departure-specific Director transition is bound. Party leader display and content membership have separate consumers. | A retained transaction identifying the starter, departing actor, cause, remaining recipient and subsequent Director/group/work events. |
| Non-leader disconnects and returns | Generic initialization can present already-running work. Aetherytes expose a generic join question. No dedicated reconnect path is identified in the bounded sources. | A reconnect transaction joining actor reconstruction or group re-registration to the same active Director. Camp interaction is not proved mandatory. |
| Participant set changes | Native group records/callbacks, content-group nameplate/restriction refresh and party roster updates are supported independently. | The exact opcode-to-callback transaction and participant policy for a running leve. |
| Eligibility to join a running leve | Supplied party warnings do not block Begin in the start widget. A separate aetheryte predicate enables journal rows. | The producer of warning/predicate inputs and the admission decision for an active leve. |

## Original inputs and tools

Source paths below are relative to `lua/scripts/`; LPB resource paths are
relative to `client/script/`. All selected original LPBs, complete decoded
chunks and reproduced canonical sources matched
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`scripts.json`](../manifests/scripts.json). The decoder was
[`retail_script.py`](../tools/retail_script.py); the disassembler/decompiler
was the pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
A Python Lua 5.1 operand parser checked prototype boundaries, operands and
return arities. Prototype PCs are zero-based; byte offsets address the
decoded chunk. Bytecode ranges list the first and last instruction offsets.
Source lines address the reproduced canonical source.

| Canonical source | LPB resource / SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- |
| `chara/charabaseclass.lua` | `729s9/729s989r57y9rr.le.lpb` / `c7cd1dad84f7d9b723f5a10fb66108da9d9d6ef5d7c15186b48ec55092465238` | `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9` |
| `chara/npc/object/aetheryte/aetherytebaseclass.lua` | `729s9/wu7/v8057q/95q25slq5/95q25slq589r57y9rr.le.lpb` / `0a6d3f84ffb8fd7881c50e415595d2a3b75384518c1345e13426ef8ca71cd3bb` | `5445e615ecf8b49defc8fb0c5000d6bd42ca901ebf974e7f659a7b273b3a5240` |
| `chara/npc/object/aetheryte/aetherytechild.lua` | `729s9/wu7/v8057q/95q25slq5/95q25slq5721y6.le.lpb` / `272874b6943a09230a4445bcc34743e3e4c89241b81dc19f2a34ff9699cd4845` | `453a18028dbc5d1883954ea33ea1494de1d83947212ee96dddada9db8232d252` |
| `chara/npc/object/aetheryte/aetheryteparent.lua` | `729s9/wu7/v8057q/95q25slq5/95q25slq5u9s5wq.le.lpb` / `6ba7d090271b658e523d416820cfb5d45e57227d4f22aaff8bfae1637c11f8ff` | `4824c5921d56b262d47b40b82bc8366a795860b4dd9944ecdb41ac7fee4e33e3` |
| `director/directorbaseclass.lua` | `61s57qvs/61s57qvs89r57y9rr.le.lpb` / `7bca9ccb9f130ea27ea8e43dd94afdb6ba0acf9f133f6294564988a281e72d7b` | `b63cd23139dc84b4e3c9d713c01278ee1d83f45a3658ba7587eec66af81ba93b` |
| `director/guildleve/guildlevebaseclass.lua` | `61s57qvs/3p1y6y5o5/3p1y6y5o589r57y9rr.le.lpb` / `73559543d4e2192180c28ac8f8f6f3fb69ebf8bcbb47b2c11a69c837cfe8f303` | `bcad3160d16813502529467ce5da17bb3a9bc80c576cd71841708fe7859d7e84` |
| `group/contentgroup/contentgroupbaseclass.lua` | `3svpu/7vwq5wq3svpu/7vwq5wq3svpu89r57y9rr.le.lpb` / `ea328e1a27abda862a1e20588384ae2f8834745b6a3143b89d3ddbd3757433a9` | `c53c41b1036bb8c9a8ed1d0b92b866fdccd2e34099489e3427b8ee97287766b1` |
| `group/contentgroup/guildlevegroup.lua` | `3svpu/7vwq5wq3svpu/3p1y6y5o53svpu.le.lpb` / `67f7be1002b8ae3c26126ee7764e87146088a7019edfca43e0d5656d211625fc` | `ff32bdb4c7e77e33dff41f9bd49ef7e4ee76caca4c776630883d5451a04ac79a` |
| `group/groupbaseclass.lua` | `3svpu/3svpu89r57y9rr.le.lpb` / `59e9ef4b0d50f61e94beb95301b8f1fcb34b6ff16c01f8f7bf66e953aa0aafe6` | `ede6a9819642211a1e08114eab854b2450f00cf3774ae9b015b32b26216066ee` |
| `group/partygroup/partygroupbaseclass.lua` | `3svpu/u9sql3svpu/u9sql3svpu89r57y9rr.le.lpb` / `2bc6f98a00a347fc3104eb31154a983d01754f69ed327951865b959a61a17c13` | `d7635d2a18a75f0d571bcf77a879e6140d77d20cfde79ae5e4b5e8af91b76fde` |
| `group/partygroup/partygroupbaseclass_battle.lua` | `3svpu/u9sql3svpu/u9sql3svpu89r57y9rr_89qqy5.le.lpb` / `f76956c6ac47f60550e4d82e54af67244c005b41410d119eccff3c0eb756ce68` | `e80d7fe8b33ce61b1a155aeb1377530e4cf852582a03321e95e45b6f006cbbf6` |
| `group/partygroup/playerpartygroup.lua` | `3svpu/u9sql3svpu/uy9l5su9sql3svpu.le.lpb` / `15c9c6eedc86eb541cf105622c15a062c16752e7322ac5c5d163f763cecfd851` | `b439d1fa53d5d04c9a42c768c27e8251894fe7c91ac6c85e78aec1066fad0104` |
| `widget/ask/guildlevestartwidget.lua` | `n1635q/9rz/3p1y6y5o5rq9sqn1635q.le.lpb` / `44b396516d7d5bf6558efdb8ebc64f31d104800c24373022f96e761231250d62` | `694dac510e08fc8ad2ad4c84c3bba2f173d76d4e79f105305c38c8dc914aad2d` |
| `widget/ask/journallistwidget.lua` | `n1635q/9rz/0vpsw9yy1rqn1635q.le.lpb` / `a15c8bf36e8124c5c4f5be2ef189037894c98342c7c7eef5889ade16d975e6f3` | `549bc61fe3c206f1dd080057948a201f2824a785d039fb9f97878d8a31491d33` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/partyparameterwidget.lua` | `n1635q/u9sqlu9s9x5q5sn1635q.le.lpb` / `a9acf65df2c4269fc46d742fb11f6b9bb6f547eea1eb6ad66842c88d8cec604c` | `d6b3dd310899ffdeb58c715d7ab9e51b7e581fd87ff55f557becdc236a084cdb` |

Native observations below used original raw-backed PE ranges, `pefile 2024.8.26`
and `Capstone 5.0.7`. The binary was `ffxivgame.exe`, 15996808
bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`,
PE32 image base `0x00400000`. Native addresses are absolute VAs and range
ends are exclusive. No live execution is established by these observations.

## Content group and party are separate state

`GuildleveGroup` is only a class declaration deriving from
`ContentGroupBaseClass` (`group/contentgroup/guildlevegroup.lua:2-8`).
The content base's `init`, `root/proto1`, declares a 32-boolean `property`
array and a nested `_globalTemp.director` of type `member`
(`contentgroupbaseclass.lua:22-85`, PCs 0-46, chunk `0x233..0x2EB`).
There is no starter or party-leader member in this declaration.

`getDirector` returns that member only if non-nil and `_isAlive()` succeeds;
otherwise it returns one nil (`:384-411`, `root/proto7`, PCs 0-18,
chunk `0xD6A..0xDB2`). It does not choose a replacement from the roster.
The director reference is a member-valued work field, not a player-owner
field. No inspected group callback assigns it to a different participant.

The exact content-group callback bodies are:

| Callback | Original locator | Observation |
| --- | --- | --- |
| `_onUpdateMember(self,actor,value)` | `contentgroupbaseclass.lua:184-236`, `root/proto3`, PCs 0-40, `0x70F..0x7AF` | Calls the superclass. If the local player is a member, a supplied `CharaBaseClass` actor gets a nameplate refresh. The restriction refresh additionally requires that supplied actor to be the local player. No Director method is called and the second supplied value is not used after superclass forwarding. |
| `_onUpdateMemberInformation(self,index)` | `:239-284`, `root/proto4`, PCs 0-33, `0x8D0..0x954` | If the local player is a member and that index has a client member of `CharaBaseClass`, refreshes its nameplate. |
| `_onUpdateGroupInformation(self,value)` | `:287-296`, `root/proto5`, PCs 0-4, `0xA69..0xA79` | Only forwards to the superclass. The original `GroupBaseClass` placeholder is empty (`group/groupbaseclass.lua:48-51`). |
| `_onUpdateWork(self,table,tag)` | `:165-181`, `root/proto2`, PCs 0-14, `0x60D..0x645` | Refreshes restrictions for tag `_init`, or table `contentGroupWork` with tag `property`, after superclass forwarding. The `director` tag has no dedicated branch here. |

The restriction helper itself calls only `updateMainMenuWidget`
(`widget/desktopwidget_connector.lua:6125-6135`, `root/proto88`,
PCs 0-4, chunk `0x113DC..0x113EC`). Its name does not prove a join test.

During content-group initialization, local membership plus kind 30001 or
30006 requests world-master row 50011 (`root/proto1`, PCs 47-66).
Finalization refreshes nameplates/restrictions and, under the same membership
and kind condition, requests row 50012 (`root/proto6`, PCs 0-61,
chunk `0xADD..0xBD1`; source `:299-381`). These rows say that the player
is now bound by duty or is no longer bound by duty. The original code does
not identify leader departure as the cause of finalization or guarantee
that local membership remains true when it runs.

`CharaBaseClass.getCurrentContentGroup` separately reads
`charaWork.currentContentGroup`: zero returns nil, otherwise it calls
`_getExtendedTemporaryGroup` with that value
(`chara/charabaseclass.lua:143-159`). It does not equate the content group
with the current player party.

### Party leader and roster presentation

`PartyGroupBaseClass.initForBattle` declares a separate member-valued
`partyGroupWork._globalTemp.owner`, tags it `leader` and binds it through
local work ID 400001 (`group/partygroup/partygroupbaseclass_battle.lua:145-181`,
`root/proto5`, code start `0x524`, 28 instructions). That ID is not proved
to be a wire property hash. `getPartyOwner` returns the field; `getPartyLeader`
additionally requires a live result (`partygroupbaseclass_battle.lua:47-55`,
`root/proto2`; `partygroupbaseclass.lua:14-31`, `root/proto0`). These
methods do not identify the leve starter or elect a replacement leader.

Party `_init` or `partyGroupWork/leader` updates refresh group presentation
for a local member (`partygroupbaseclass.lua:98-125`, `root/proto4`,
23 instructions at `0x41A`). `PlayerPartyGroup` membership, member-info
and group-info callbacks also call `processUpdateGroupInformation` and
refresh relevant nameplates (`playerpartygroup.lua:116-311`,
`root/proto2/3/4`, code starts `0x439/0x5E7/0x7A5`).

The desktop's kind-10001 branch refreshes static widget 6 and party-manager
widgets. It shows that roster for more than one member, otherwise hides it,
then calls `updateAll` (`desktopwidget_connector.lua:5673-5839`,
`root/proto84`, 132-instruction body at `0x106EE`). Static widget 6 is
created as `PartyParameterWidget` at source lines 8158-8166.
Its `updateAll` calls `updateMemberList`; that method uses current count,
supplied membership helper results and `isPartyLeader` for row visibility
and leader marks (`widget/partyparameterwidget.lua:78-87,214-306`,
`root/proto2/10`, code starts `0x821/0xC62`). This is roster presentation.
It neither transfers the guildleve Director nor determines why a member
became unavailable.

## Native group consumers

The distinct native record paths agree with the separate group model in
`xivl-client-structs:manifests/director_group_wire_identity.json`:

| Original range | Direct observation |
| --- | --- |
| `0x006C2F70..0x006C2FDA` | The promoted 0x017F route forwards records at input `+0x10` and a sign-extended byte count at `+0x190`, conditionally through `0x006C1040` and `0x006C19D0`. The branch also tests local flags at object `+0xC`. |
| `0x006C3100..0x006C3144` | The promoted 0x0183 route forwards records at `+0x10` and a sign-extended byte count at `+0x70` to `0x006C1C00`, under its local object gate. |
| `0x006D0350..0x006D03AF` | Two branches invoke `0x007008B0` or `0x00700B70`, carrying a byte from receiver `+0x18`. |
| `0x006D3B20..0x006D3B9C` | Local case values 0/1 call `0x006D0350`; case 2 returns; case 3 selects `0x00700A10` or `0x00700B70`. These are internal cases, not assigned join/leave/disconnect reasons. |
| `0x007008B0..0x00700A01`, `0x00700A10..0x00700B61`, `0x00700B70..0x00700CBE` | Each constructs the literal `_onUpdateMember` callback name and calls dispatcher `0x00CC7A90`, at `0x007009AD`, `0x00700B0D` and `0x00700C6A` respectively. The strings are at `0x00FD48F8`, `0x00FD4908` and `0x00FD4918`. |

No leader, leve-starter, reconnect policy or compulsory camp entry is
identified in these bounded bodies. They establish generic record and
callback mechanisms, not an end-to-end 0x017F/0x0183-to-type-30001 callback
transaction. In particular, the carried byte is not assigned a departure
reason here.

| Native VA range | SHA-256 of original bytes |
| --- | --- |
| `0x006C2F70..0x006C2FDA` | `499ec3e64129655a45247b37f8427e328bc6590c2d811740e3460c05e736a595` |
| `0x006C3100..0x006C3144` | `509e7da4b5acd1994f68d00790d5686a400e996e8300682cde127ef8ac666e02` |
| `0x006D0350..0x006D03AF` | `0ff3494827cf42d02c8a18d39b3245264a3d044f89007ea9c1f3e27f1a0747a4` |
| `0x006D3B20..0x006D3B9C` | `2f2f52cf092818fd241fdee0ed129265d7fb85ae275f2b781960273214f14ed5` |
| `0x007008B0..0x00700A01` | `718f5179ab02b6dd627fedc307884155a535ad490aa7b479c39236ce04374d37` |
| `0x00700A10..0x00700B61` | `fbfe2a578efe78a1cb24750204cd9985db1128d0d25cc94c0bbb650019a627ae` |
| `0x00700B70..0x00700CBE` | `122b347c835bbe7e13ca9f96e2ee93d3e4a04604e446cb33db13c5c052c74dae` |
| `0x00FD48F8..0x00FD4938` | `99b8a649baa784736a308b127dc9f9b3560740e01a5ca54c754dcafb77ebdce2` |

## Director continuation and retirement

The base guildleve initializer stores the supplied leve ID, location and
extra marker coordinates. Its synchronized declarations contain
`startTime`, `signal`, four `aimNum`, `aimNumNow` and `uiState` entries,
and three `markerX/Y/Z` entries (`director/guildleve/guildlevebaseclass.lua:211-456`,
`root/proto17`, 172 instructions at `0xF70`). They contain no declared
party leader, starter, reconnect state or participant roster.

On `_init`, `DirectorBaseClass._onUpdateWork` calls `processUIInit`
and `processUpdateWork` (`director/directorbaseclass.lua:287-363`,
`root/proto16`, code start `0xB7D`). Guildleve `processUIInit` copies current
objective/UI state, then emits content UI `start` when retained start time
is positive and local `uiStep` is zero. It sets `uiStep=1` and refreshes
markers (`guildlevebaseclass.lua:575-622`, `root/proto29`,
38 instructions at `0x18AE`). Thus ordinary initialization can reconstruct
presentation from running work without a reconnect-specific event. This
does not prove that a returning participant receives that initialization.

The existing [Director UI contract](content-director-ui-contracts.md#guildleve-and-request-directors)
owns the `start`, objective update, `signal` and marker consumers.
The lifecycle manifest
`xivl-client-structs:manifests/guildleve_lifecycle.json`, evidence-matrix
questions for EndEvent, DeleteGroup, DirectorBase lifecycle and SyncMemory,
owns these already established boundaries:

| Mechanism | Locator and producing tool | Supported effect |
| --- | --- | --- |
| 0x0137 SyncMemory | `0x0089E550` through `0x00773F10`, retained Ghidra 12.1.3 `DumpVAs.java` recipes | Conditional work application and `_onUpdateWork`; not Director finalization. |
| 0x017A | `0x006C9910 -> 0x006C96B0 -> 0x006C84A0`, same retained tool | Group SharedWork, separate from `guildleveWork`. |
| 0x0131 EndEvent | `0x008A13A0`, same retained tool | Retires/closes event execution state, not a Director destructor. |
| 0x0143 DeleteGroup | `0x006C5DE0 -> 0x006C5150 -> 0x006D6F10`, same retained tool | Queues group breakup; does not establish Director removal or its cause. |
| 0x00CB RemoveActor | Actor lookup and dynamic slot 0; Director slot 0 `0x00721370`, same retained tool | Actor destruction, distinct from Director slot-5 Lua finalization `0x006F6D30 -> 0x006F6900`. |

No new departure sequence is inferred from the manifest's completion sample.
Guildleve `processUIFinalize` clears its minimap marker and sends content UI
`cancel` (`guildlevebaseclass.lua:749-765`, `root/proto31`,
11 instructions at `0x1D87`). The trigger that schedules that finalization
after a participant change remains unbound.

## Entry questions and eligibility

`AetheryteBaseClass.eventGLJoin` delegates to `processGuildleveJoin(self)`
(`chara/npc/object/aetheryte/aetherytebaseclass.lua:338-345`, `root/proto12`,
tail call PC 1 / chunk `0xD3A`). Parent and child implementations ask whether
to join the party leader's levequest and return the one answer unchanged
(`aetheryteparent.lua:1597-1610`, `root/proto8`, CALL PC 6 / `0x25EC`,
RETURN PC 7; `aetherytechild.lua:327-340`, `root/proto5`,
CALL PC 6 / `0x9CB`, RETURN PC 7). The event supplies no reconnect flag,
leve ID or participant identity to that processor. The prompt wording
does not establish that every join, return or reconnect uses this route.

The inherited `eventGLStart` route and five attention inputs are owned by
[the start-event contract](aetheryte-guildleve-events.md#eventglstart-and-widget-argument-reshuffling).
Original base `root/proto6` PC 14 / `0xA84` retains two widget results;
result 2 equal to 1 returns the supplied difficulty, otherwise one nil.
The widget shows warnings for another duty, distance, guild-mark class
eligibility and EXP reduction, but its Begin handler still sets result 1
(`widget/ask/guildlevestartwidget.lua:111-152`, `root/proto0` PCs 93-118,
`root/proto1` PC 4). Neither that widget nor `eventGLStart` evaluates the
party's actual distance, duty, class or accepted leve. These are supplied
presentation values, not proof of authoritative admission checks.

A separate `canUseGuildleve(self,player,id)` tests
`player:isUnusedGuildleveById(id)`, then compares the live aetheryte's
actor class with `guildleveUISheet` column 78 for that ID
(`aetherytebaseclass.lua:133-171`, `root/proto2`, PCs 2,16,18,22-28;
code start `0x746`). The class comparison concerns the aetheryte actor,
not the player's combat class/job. Actual local callers use it for journal
row enablement/data (`widget/ask/journallistwidget.lua:1507-1552` and
`desktopwidget_connector.lua:10163-10185`). It is not called by
`eventGLStart` or `eventGLJoin`. No running-leve admission use is established.
The parent's `getLimitedDistanceForTalk` returns 10
(`aetheryteparent.lua:11-17`, `root/proto0`, PC 1 / `0x244`);
that return alone does not prove a comparison, distance unit or party-wide
join limit.

## Client text and search boundary

The CSV archive and selected members were authenticated against
`xivl-client-data:manifests/private_csv_corpus.json` and
`xivl-client-data:manifests/tables.json`, then read with Python `zipfile`
and `csv` without corpus writes. English column 1 supplied:

| Member / row | Physical line | Observation |
| --- | ---: | --- |
| `worldMaster.csv` 50011/50012 | 1748/1749 | Bound-by-duty / no-longer-bound-by-duty notifications. |
| `aetheryteParent.csv` 18 | 20 | Generic party-leader levequest join question. |
| `aetheryteChild.csv` 7 | 9 | Same question. |
| `xtx__text_ui.csv` 4325 | 1673 | Conditional warning text for supplied duty, distance, class and EXP inputs. |

| CSV member | Bytes | SHA-256 |
| --- | ---: | --- |
| `worldMaster.csv` | 1851138 | `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643` |
| `aetheryteParent.csv` | 156061 | `8b02c6c8f7fefa10d1d90d7ef79b4ae48edc13f79f7fd0920d4d5a2cadf9e27c` |
| `aetheryteChild.csv` | 25098 | `0e4717fc041802bab41f04aab91a9da8eac7d3af7fc7c7b421e552f7a400ab8a` |
| `xtx__text_ui.csv` | 1284564 | `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece` |

The CSV archive was 70110686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
The authenticated 2671-member Lua archive was 14385427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
All source-member size/hash pins matched. The case-insensitive query
`party|group|leader|member|relog|rejoin|reconnect|resume|disconnect|leave`
covered all 34 `director/guildleve/` sources and the selected Director/group
bases. The guildleve sources matched only the presentation key `enemyParty`.
The four aetheryte/start-widget originals have no dedicated reconnect,
rejoin or resume method/constant. Their generic join/start and retry prompts
are distinct local entry points, not an authenticated reconnect protocol.

These finite source and original-bytecode boundaries do not exclude computed
or externally invoked methods, inherited engine behavior or a server choosing
ordinary initialization after reconnect. Static reception and presentation
do not identify which messages a remaining member historically received.
A retained departure/reconnect transaction with stable party/content-group
and Director identities is the precise remaining discriminator.
