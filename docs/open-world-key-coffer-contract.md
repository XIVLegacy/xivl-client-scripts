# Open-world key coffer contract

Retail 1.23b preserves coffer-key item identities, two client confirmation
helpers and chest-related text. The inspected evidence does not bind an
open-world keyed coffer to a placement, opening transaction or respawn
interval. In particular, actor-class row 1200161 and its captured appearance
are associated with a guildleve bonus box, so they cannot supply keyed-coffer
cadence for Zahar'ak, U'Ghamaro or Natalan.

The [keyed treasure-box registration contract](keyed-treasure-box-registration.md)
owns the initializer argument layout, work/publication distinction and named
event-helper delivery boundary for PublicTreasureBox and GimmickTreasureBox.

| Question | Supported observation | Remaining discriminator |
| --- | --- | --- |
| Separate actors at each post, or one actor moving | Class declarations and an appearance row exist. No keyed zone placement or BG/instance identity is bound. | A retained keyed actor registration joined to its zone, instance identity and positions at multiple posts. |
| Open, disappear, refill or relocate | The selected coffer chunks contain no opening/despawn/refill sequence or coffer timer. The retained capture search supplies no keyed opening transaction. | One continuous observation covering the keyed interaction, resulting actor updates/removal and subsequent registration or position at the same and alternate posts. |
| Consume key, award item, refuse interaction | The confirmation is bound. Other chest and generic item/refusal rows are available, without a keyed transaction selecting them. | Event arguments/results, key inventory before/after, reward update and selected message IDs from the same opening attempt. |
| Talk/notice contract | Inherited talk dispatch, range values, marker gates and empty rejection hooks are visible. | The registered event conditions and server response for a particular keyed actor. |

## Original inputs and tools

Decoded paths below are relative to `lua/scripts/`; original LPB paths are
relative to `client/script/`. The seven complete original LPBs, decoded Lua
5.1 chunks and reproduced sources matched
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`scripts.json`](../manifests/scripts.json), extraction `2012.09.19.0001`.
[`retail_script.py`](../tools/retail_script.py) decoded their wrappers.
The pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`,
produced source and instruction disassembly. A Python Lua 5.1 operand parser
checked arguments, branches and return arity. PCs and chunk byte offsets
are zero-based. Source lines address the reproduced canonical source.

| Source | LPB resource / SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- |
| `chara/npc/object/guildlevebonustreasurebox.lua` | `729s9/wu7/v8057q/3p1y6y5o58vwprqs59rps58vm.le.lpb` / `c085065e029ddfc5b9a718593098dcde2656d3e7b5730b8a0d5b7f76082997fd` | `43615425eec0b68496d4a2487fdabc154df14cfd04210123ff14003a87420704` |
| `chara/npc/object/treasurebox/publictreasurebox.lua` | `729s9/wu7/v8057q/qs59rps58vm/up8y17qs59rps58vm.le.lpb` / `72d44e70d3f8a781855ae0813d2e26210b03c80c4f2dfaa7cb471856ff6fbdd6` | `82153dd06660376e02103b7c0558b92d33b92bd2ab494a8c8aac99c97205558d` |
| `chara/npc/object/treasurebox/treasureboxbaseclass.lua` | `729s9/wu7/v8057q/qs59rps58vm/qs59rps58vm89r57y9rr.le.lpb` / `02f8bf9534d70cf79605f5129c278a7614e15d2a108d080443ab84dc59d9bc83` | `a2b4cee27ffd37405e158aa358df9505d0f570ddb72676a80594fc2be15bf0bd` |
| `chara/npc/gimmick/gimmicktreasurebox.lua` | `729s9/wu7/31xx17z/31xx17zqs59rps58vm.le.lpb` / `914edf17071592e7756dc35a0299c60ad6f543aae0d14e083d05836121a30c2f` | `a3090ce88840d6bddde35f1d76c8eb54849c8bc6d85d61a3d50ce251d8466c2c` |
| `chara/npc/gimmick/gimmicknpcbaseclass.lua` | `729s9/wu7/31xx17z/31xx17zwu789r57y9rr.le.lpb` / `d685e404923bf98b945ab2d6dbf92b66d358c45051ab5d37da4d159c00319f87` | `eb1941250950be95a0491d1c0bd4f1657a6b71cc1bcd787a8324e7e788bc84b4` |
| `chara/npc/npcbaseclass.lua` | `729s9/wu7/wu789r57y9rr.le.lpb` / `3f1dcc3416f7e22db138a6dcc730b095f81f3d0ceb458a7ded7d5b0d17df55c9` | `1941c40b64cacd721d271b36e31017a24f908b8ea518f713b44da17bb4e57627` |
| `chara/npc/npcbaseclass_event.lua` | `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` / `84a5098636ff289f4ecf4e164e84e44890895e8a9005fb102e04929c2bb74bf9` | `4a3008dd8d2a91e7eb044e5555d2757468a9097bba5175992fb88f943bd07b6c` |

CSV observations used Python `zipfile` and `csv`, after checking the archive
and each selected member against `xivl-client-data:manifests/private_csv_corpus.json`
and `xivl-client-data:manifests/tables.json`. The archive SHA-256 is
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
Relevant member identities are:

| CSV member | SHA-256 |
| --- | --- |
| `_item.csv` | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `xtx_itemName.csv` | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `actorclass.csv` | `3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984` |
| `actorclass_graphic.csv` | `7da8241400530885e0a28ded04a03acf2771b0580a79c1f49f46ee0861010611` |
| `actorclass_mapObj.csv` | `fed5a31df6a3905ffb074f482c19237826ec84b236c6baf09309729296d79bde` |
| `worldMaster.csv` | `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643` |

## Keys and actor identity

`xtx_itemName.csv`, English title header `5`, and `_item.csv` have the
following rows at physical lines 5796-5810 in both members:

| Zone in item name | ID and key metal, in row order |
| --- | --- |
| Zahar'ak | 10011136 Brass; 10011137 Copper; 10011138 Silver; 10011139 Gold |
| U'Ghamaro | 10011140 Brass; 10011141 Silver; 10011142 Copper; 10011143 Bronze; 10011144 Gold |
| Natalan | 10011145 Brass; 10011146 Copper; 10011147 Silver; 10011148 Steel; 10011149 Mythril; 10011150 Gold |

Each full English title ends in `Coffer Key`. `_item.csv` classifies all
fifteen as `Normal/StandardItem`, with headers `1=1`, `2=true`, `3=true`.
The field interpretation in `xivl-client-data:tools/mappings/items.py`
is max stack 1, rare and exclusive. These rows identify inventory items.
They do not identify which actor consumes them, whether consumption succeeds,
or what it awards.

`actorclass_graphic.csv` row 1200161, physical line 3127, has header `6=20923`,
`7=2` and `33=3072`. The mapping in
`xivl-client-data:tools/mappings/actor_appearance.py` calls these base, size
and body. Thirty rows share base 20923, so that base alone is not a class or
placement identity. `actorclass.csv` row 1200161, physical line 3143, has
display-name header `5=0`. There is no row 1200161 in the selected
`actorclass_mapObj.csv`. No BG, post, zone or instance link is recovered from
these observations. The empty class-path and event-condition values emitted
by `xivl-client-data:tools/mappings/actor_class.py` are mapping placeholders,
not recovered retail script registrations or event-condition fields.

The Lua roots register `PublicTreasureBox` with `TreasureBoxBaseClass`,
`TreasureBoxBaseClass` with `NpcBaseClass`, `GimmickTreasureBox` with
`GimmickNpcBaseClass`, and `GuildleveBonusTreasureBox` with `NpcBaseClass`
(each source lines 2-8, root PCs 0-6). These declarations contain no zone,
placement or actor-class number. `NpcBaseClass._onInit` binds work ID 5001
to `npcWork.actorClassId` (`:110-281`, `root/proto10`, PCs 78-84,
chunk `0x8E7..0x8FF`), and `getActorClassId` reads it (`:37-44`,
`root/proto3`, code `0x560`). This is a class-valued field, not an instance
or placement allocator.

## Confirmation and event contract

The following observations come from the original bytecode and its source
reproduction, rather than absence of N-API calls in a sidecar.

| Class and method | Original locator | Observation |
| --- | --- | --- |
| `PublicTreasureBox.initForEvent` | `publictreasurebox.lua:11-19`, `root/proto0`, PCs 0-2, `0x11D..0x125` | Calls `_setGroundOn(false)`. This method does not call the base initializer. |
| `PublicTreasureBox.askUseKey(self,A1,A2)` | `:22-37`, `root/proto1`, PCs 0-9, `0x167..0x18B` | Calls `askExtendWidget(worldMaster,60023,2,1,1,A1,A2)` and returns its one result unchanged. |
| `TreasureBoxBaseClass.initForEvent` | `treasureboxbaseclass.lua:11-27`, `root/proto0`, code `0x10E` | Declares `treasureBoxWork._temp={{"_assignForChild",64}}` and calls the empty `processInitTreasureBox` hook (`:30-34`, `root/proto1`, `0x1BC`). No opening state or timer is declared here. |
| `GimmickNpcBaseClass.initForEvent` | `gimmicknpcbaseclass.lua:11-45`, `root/proto0`, code `0x149` | Stores supplied talk range in `gimmickNpcWork.talkRange`, declares `_assignForChild` values 60 in `_temp` and 4 in `_sync`, then calls `initForGimmick` with the remaining arguments. |
| `GimmickNpcBaseClass.getLimitedDistanceForTalk` | `:54-61`, `root/proto2`, code `0x284` | Returns that stored range. No coffer-specific numeric range is supplied in these chunks. |
| `GimmickTreasureBox.initForGimmick` | `gimmicktreasurebox.lua:11-30`, `root/proto0`, code `0x146` | Stores the supplied marker boolean in `work.mapMarkerVisible` and calls `_setGroundOn(false)`. Its marker getter returns that field (`:33-40`, `root/proto1`, `0x1F0`). |
| `GimmickTreasureBox.askKeyItemUse(self,A1)` | `:43-71`, `root/proto2`, PCs 0-20, `0x248..0x298` | Calls `desktopWidget:askForEventMode(nil,nil,worldMaster,1,false,true,60023,{60024,60025},A1,1)`. Returns one boolean, true only when the widget result equals 1. |
| `GuildleveBonusTreasureBox` | `guildlevebonustreasurebox.lua:11-31`, `root/proto0..2`, code starts `0x136`, `0x162`, `0x18E` | `initForEvent` and `eventTalkStep0` are empty. The marker gate always returns false. The complete chunk contains no key prompt. |

The inherited `NpcBaseClass_event.askExtendWidget`, source `:418-493`,
`root/proto11`, code `0xDFA`, builds consecutive choices after the supplied
text ID. For the public box's mode 1 it calls
`askForEventMode(self,self,worldMaster,1,false,true,60023,{60024,60025},A1,A2)`.
PC 37 is `VARARG r19,0`, PC 38 is the open-argument `CALL r9,0,2`
(`0xE8E`, `0xE92`), and PC 72 returns one result (`0xF1A`). Both supplied
arguments survive this call. The decompiled temporary assignment alone
obscures this variable-argument behavior. Neither keyed helper installs a
callback or mutates inventory. A confirmed choice is not proof of consumption.

The inherited talk route calls `_callServerOnTalk(A1,A2)` with lock-on
presentation and target cleanup (`npcbaseclass.lua:406-446`,
`root/proto21`, PCs 18-27, `0xFC9..0xFED`). `_onTalkRequest` calls
`_doServerOnTalk(A1,A2)` (`:449-458`, `root/proto22`, code `0x1091`).
`_onTalkRejected`, `_onNoticeRejected` and `_onReaction` are empty hooks
(`:601-623`, `root/proto29`, `31`, `32`, code `0x167D`, `0x16D5`, `0x1701`).
No selected coffer chunk supplies notice conditions or a key/inventory
eligibility predicate. The generic event script returns talk distance 7
(`npcbaseclass_event.lua:4-10`), but the caller enforcing that distance and
the keyed actor's actual range are not bound here.

`NpcBaseClass._onTimer` forwards to the superclass, then calls the empty
`processTimer` hook for work names `work` or `retainerWork`
(`npcbaseclass.lua:284-310`, `root/proto11..12`, code `0xBD9`, `0xCA7`).
The selected classes do not override this with a coffer lifetime. This
bounded absence does not rule out server timers, native presentation or
other scripts. The separate
[raid treasure-box contract](raid-object-client-contracts.md#treasure-box-sheet-structure)
owns the raid drop algorithms and their unbound sheet inputs. It does not
provide open-world keyed placements or loot probabilities.

## Text rows and transaction limits

Python CSV inspection of `worldMaster.csv`, English header `1`, recovered:

| Row / physical line | Text meaning | Binding |
| --- | --- | --- |
| 60021 / 2211 | This chest can only be opened with the supplied item. | Available key-required text. No selecting call in the inspected keyed chunks. It does not itself test possession. |
| 60022 / 2212 | Your inventory is full. | Available refusal text, without a keyed capacity-check or emission binding. |
| 60023 / 2213 | Use the supplied item to open the chest? | Directly selected by both keyed helpers. |
| 60024-60025 / 2214-2215 | Yes; No. | The two ordered choices selected by both helpers. |
| 60026 / 2216 | The chest unlocks! | Available presentation text, without a keyed success/consumption binding. |
| 60027 / 2217 | The chest is empty. | Available presentation text. Its raid caller is separately documented in the raid object contract. |
| 25081 / 196 | You are too far away. | Generic distance text. No keyed-coffer caller is bound. |
| 25022 / 137; 25117 / 232 | You obtain the supplied item. | Generic receipt templates, without a keyed reward selection or grant binding. |
| 40112 / 1472 | You use the supplied item. | Generic use template, without a keyed consumption binding. |

The descriptions paraphrase variable formatting, whose original control-code
tokens remain in the pinned CSV. The presence of these rows establishes text
availability, not the server branch that emits them or an inventory mutation.
No reward item, refusal priority, key loss or successful opening is inferred
from their wording.

## Retained capture coverage and lifecycle boundary

The capture input is `xivl-captures:config/retail_inputs.json`,
`pcap-1.23b-objects.zip`, 2622720 bytes, SHA-256
`20a78b9f40ff2393037c9a160c957783cf590b4f01797493d22fcd2039e9cbff`.
All 54 members and local cache files matched
`xivl-captures:sources/pcap-1.23b/manifest.yaml`.
`xivl-captures:tools/validate_framing.py` reported zero compression flag
mismatches for every capture. The producing stream tools were
`xivl-captures:tools/extractors/extract_streams.py`, specifically
`reconstruct_lanes`, `parse_outer_frames` and `maybe_inflate`, with a Python
subevent walker. Connections and directions remained separate. The search
covered 84 admitted clear port-54992 lanes and 19760 complete outer frames.
It excluded TLS/lobby traffic and incomplete stream tails.

The finite search used four-byte little- and big-endian values for all
fifteen key IDs, class 1200161 and appearance base 20923, plus ASCII
`TreasureBox`, `treasure coffer`, `coffer key`, `Zahar.ak`, `Ghamaro` and
`Natalan`, case-insensitively. The only key-number matches were big-endian
10011136 at subevent byte +57 in c2s `0x00CA` position reports in
`accept_leve.pcapng` (lane 0, frame 16, stream +3056, inflated-body +121)
and `accept_local_leve.pcapng` (lane 0, frame 58, stream +10656,
inflated-body +57). That byte span crosses movement-state/reserved fields
in `xivl-captures:tools/extractors/extract_c2s_00ca_position_report.py`,
not an item-ID field. These are rejected numeric coincidences.

The four base-20923 appearance records and four class-1200161 byte matches
occurred only in `party_battle_leve.pcapng`, SHA-256
`6327e5e1f5cbd51a9baaa9bcbacf53ca51c50a98fe4b66ae3e6bdecd9198089f`.
The exact registration locators are below. Each s2c
`0x00CC` contains `GuildleveBonusTreasureBox` and
`/Chara/Npc/Object/GuildleveBonusTreasureBox`; each paired `0x00D6` has
appearance base 20923 at subevent +32. The four registrations have distinct
inner actor IDs. They are not keyed open-world opening observations.

| Lane 0 s2c frame | Outer stream offset | Inflated-body offset of `0x00CC` | Paired `0x00D6` body offset |
| --- | --- | --- | --- |
| 1018 | 127275 | 1104 | 504 |
| 1449 | 178685 | 1104 | 504 |
| 1763 | 216669 | 1104 | 504 |
| 1957 | 239053 | 2688 | 2088 |

The follow-up searched s2c `0x00CC` records for the four-byte values of all
30 CSV classes sharing base 20923. Only the same four 1200161 matches
appeared. No other searched coffer/zone string appeared. This is a bounded
wire search, not a census of every possible coffer class, encoding or event.
No keyed actor add/open/remove pair was identified, so no open-to-despawn
duration or respawn timer can be measured from it. Repeated guildleve
registrations cannot be repurposed as such a timer.

To decide same-post refill versus relocation, the missing retained
transaction must identify a keyed actor and key, preserve zone/instance and
actor identity across the opening and removal, and observe the same and
alternate posts continuously through the next appearance with trustworthy
elapsed timestamps. Inventory and message updates must accompany the
interaction to distinguish a successful open from cancellation or refusal.
The inspected evidence is silent about original placement policy, reward
odds and respawn timers.
