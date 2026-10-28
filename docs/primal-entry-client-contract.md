# Primal entry client boundary

The shipped generic guide can present an entry question for a supplied
content value and return one boolean. The inspected resources do not bind
an ordinary Garuda or Moogle guide instance to that value or join the
answer to admission. The text dictionary names the Howling Eye and
Thornmarch, and the static-actor table identifies the three Garuda quest
titles with `Gcl104`. These are separate, directly observed relationships.

The [selected instance entry contracts](instance-entry-client-contracts.md)
cover Toto-Rak, the separate Rivenroad requests and Ifrit Hard, including
their unresolved actor, admission and destination bindings.

## Original evidence

The scope contains all ten canonical resources under
`chara/npc/populace/instanceraidguide/`,
`judge/instanceraidguidejudge.lua`, and the mapping-selected
`quest/scenario/gcl/gcl104.lua`. Resource paths are relative to
`client/script`; source paths are relative to `lua/scripts`.
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) owns
the exact resource-to-source and decoded-payload identities;
[`scripts.json`](../manifests/scripts.json) owns the canonical source pins.
Every selected LPB, decoded chunk and reproduced source matched those pins.

| Canonical source | LPB resource / SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- |
| `chara/npc/populace/instanceraidguide/aetherytebeastchildguide.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/95q25slq5859rq721y63p165.le.lpb` / `2eb45831bf1e882afe60160f5d5a89d40b6828c37e39b8d0f16886197f589bd9` | `775d341fa2d520d5fedfaada9cb8a8ec8001cdfdf2607eb8c3aa077cb1992490` |
| `chara/npc/populace/instanceraidguide/hasquestguidebaseclass.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/29rtp5rq3p16589r57y9rr.le.lpb` / `8959805b5b0e577036d823203b19f6d367ee1820bf239fbc6384f5d4dccdf628` | `36e082b65402fef87d948819338679d29101552d1c8930093c312d55f3faacaa` |
| `chara/npc/populace/instanceraidguide/inspectableguidebaseclass.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wru57q98y53p16589r57y9rr.le.lpb` / `9601994e1cc9617664be76f6955c61f1efa7b98d628af33038c6858bea981eea` | `d46fe78e838f50c725ad255dc6bd715ad84b87ca274e9d09984e69b1d2f3cc15` |
| `chara/npc/populace/instanceraidguide/inspectableinstanceraidguide.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wru57q98y51wrq9w75s9163p165.le.lpb` / `11d0aa951a9c99e33f6b71291917c1aee2904fee2fc39ddbf71266b87a7c47e5` | `30db6bb876c155f557e55e2ce684794a0da519754ae1917f7b0f9861a80dfc86` |
| `chara/npc/populace/instanceraidguide/instanceraidguide.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p165.le.lpb` / `af88e8a845a9df6c12541b09b49c9c7992359b74a203c6dacd358549c9ea0c62` | `3df3b783a4b58f232b41e683494f47077b0007f27f431d03202e3aa068d98339` |
| `chara/npc/populace/instanceraidguide/instanceraidguideaurumvale.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p1659pspxo9y5.le.lpb` / `f86bad44fca4b253223a639f8806d57ca24582d819a8b20471a1c2be612de1f4` | `80e49a71894d6745e2ae5c63f522c7ac94925f6e0666606ab9a9b4e738c8e1c9` |
| `chara/npc/populace/instanceraidguide/instanceraidguidebaseclass.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p16589r57y9rr.le.lpb` / `b9be2c3b9f3d9e35f6aea60474e054f9690c1c17466c6bf0fb92791eca321894` | `54467e44bd629033695c561e4bc0f2dbbcf898343641ee6dd415a3643020a9a4` |
| `chara/npc/populace/instanceraidguide/instanceraidguidecutterscry.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p1657pqq5sr7sl.le.lpb` / `48f066b5a25749c1d0fc39ac0ad78c93b7d0b099ec73ddb8535dffb11b4b6f1a` | `5e9d5aeff9035c499d7f3f960ae666b97de40289ae5d7b171c46371eac281ee2` |
| `chara/npc/populace/instanceraidguide/instanceraidguidehamlet.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/1wrq9w75s9163p16529xy5q.le.lpb` / `ddd92ab373c1bd9261f23f45bd00d46b0dadba3df711a136a98a8a8e520fc807` | `63b2fa1a56a1e5039b0d830ff65eaf408b13ed8b0b40344a24f7a72661c90741` |
| `chara/npc/populace/instanceraidguide/noquestguidebaseclass.lua` | `729s9/wu7/uvupy975/1wrq9w75s9163p165/wvtp5rq3p16589r57y9rr.le.lpb` / `7856f1aeaeccaddc9962404542d5aa934837b2817a4da3eb910303eb8a771487` | `b2a9c1df037d9cc8af191db06dfd262342407ceda92a092b883106a15c08e788` |
| `judge/instanceraidguidejudge.lua` | `0p635/1wrq9w75s9163p1650p635.le.lpb` / `e4ad597441e0635f304f78ed9400d70ac3f5112fb1152b2c78863e5c5b05e1a6` | `b2c2dd53ae8484a30f27feb6b882c52d591b5fb585cf5fb55a9ad99a91edb3c2` |
| `quest/scenario/gcl/gcl104.lua` | `tp5rq/r75w9s1v/37y/37yijf.le.lpb` / `fc56ae181345397cc8de9102d1733b5a967299a6e4c84e2a57478500765eccee` | `922f5a5599dc228e1078ab6885461bc7087c3396f90ceb54203ec450f5650af0` |

The originals were decoded with
[`retail_script.py`](../tools/retail_script.py) and disassembled/decompiled
with the pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
Prototype names below use the inventory's `root/protoN` convention and
zero-based instruction PCs. Source locators refer to the reproduced
canonical source, not the chunk's retained debug line numbers.

## Generic question and answer

`InstanceRaidGuideBaseClass.askEnterInstanceRaid(self,value)` is at
`chara/npc/populace/instanceraidguide/instanceraidguidebaseclass.lua:31-58`,
`root/proto2`. PCs 1-4 build ordered choices 52046 and 52047. PCs 5-15 call:

```text
desktopWidget:askForEventMode(
    nil, nil, worldMaster, 1, false, true,
    52045, {52046,52047}, value)
```

The supplied value is the second formal parameter, moved unchanged at
PC 14. The call at PC 15 is `CALL A4 B11 C2`: ten explicit arguments,
including the desktop receiver, and exactly one retained answer. It has
no literal ordinary-primal content value. PC 0 initializes the result to
false; PCs 16-18 set it true only when that answer equals numeric 1.
PC 19, `RETURN A2 B2`, returns exactly one boolean. Other answers,
including the desktop helper's zero fallback, return false.

The inherited desktop/widget behavior is owned by
[selection and continuation](duty-confirmation-client-contract.md#selection-and-continuation).
This guide supplies `canCancel=true`, unlike that page's common quest
helper route. It supplies `askPaging=false`. Its boolean result does not
establish a server request, admission, zone movement or instance creation.

### Display identities

The selected CSV members were authenticated inside the pinned archive
without changing or hydrating the corpus. Their canonical size/hash records
are in `xivl-client-data:manifests/tables.json`; the archive identity and
validation boundary are in
`xivl-client-data:docs/ai_agents/retail-input-validation.md#decoded-csv-assertion`.

| CSV member | Bytes | SHA-256 |
| --- | ---: | --- |
| `worldMaster.csv` | 1851138 | `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643` |
| `xtx_raidDungeon.csv` | 2381 | `24c7e9a071c5a16b8a38254588e350e7e7b043e2dfe4129ecd5363d2f05f6059` |
| `xtx_quest.csv` | 2953504 | `938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719` |

In `worldMaster.csv`, English column 1, row 52045 at physical line 2116
asks to begin the duty and includes a sheet token naming
`xtx/raidDungeon`. Rows 52046 and 52047 at lines 2117-2118 are Yes and No.
In `xtx_raidDungeon.csv`, English column 26 gives these display identities:

| Row key | Physical line | English display |
| ---: | ---: | --- |
| 5 | 7 | Thornmarch |
| 11 | 13 | the Howling Eye (Hard) |
| 12 | 14 | the Howling Eye |

These establish distinct text rows. A caller supplying key 5 or 12 is still
needed to identify either ordinary entry invocation. The text keys are not
proved zone IDs, NPC IDs, quest IDs or admission policies. The separate
[party-matching list](party-matching-client-contract.md) does not supply
that guide invocation.

## Guide classes and quest identity

The complete guide-folder resources declare the following chain:

| Class | Base | Chunk-local behavior relevant to the boundary |
| --- | --- | --- |
| `InstanceRaidGuideBaseClass` | `NpcBaseClass` | Clears `instanceRaidGuideWork._temp` and calls `initForInstanceRaidGuide`; owns the generic question above. |
| `HasQuestGuideBaseClass` | `InstanceRaidGuideBaseClass` | Class declaration only. |
| `InspectableGuideBaseClass` | `HasQuestGuideBaseClass` | `isMapMarkerVisibleForTalkable` returns false. |
| `InstanceRaidGuide` | `HasQuestGuideBaseClass` | Overrides initialization only with `_setGroundOn(false)`. |
| `InspectableInstanceRaidGuide` | `InspectableGuideBaseClass` | Same placement override. |
| `AetheryteBeastChildGuide` | `InspectableGuideBaseClass` | Class declaration only. |
| `NoQuestGuideBaseClass` | `InstanceRaidGuideBaseClass` | Explanation-selection delegate, owned by the existing contract below. |
| `InstanceRaidGuideAurumVale` | `NoQuestGuideBaseClass` | Explanation overrides, owned by the existing contract below. |
| `InstanceRaidGuideCuttersCry` | `NoQuestGuideBaseClass` | Explanation overrides, owned by the existing contract below. |
| `InstanceRaidGuideHamlet` | `NoQuestGuideBaseClass` | Initialization only with `_setGroundOn(false)`. |

The simple declarations are at source lines 2-8 of their named resources.
The placement overrides occupy lines 11-19; the inspectable predicate is
lines 11-17. The base's initialization is lines 11-21. The already promoted
[guide and event methods](content-director-ui-contracts.md#instance-raid-guide-and-event-methods)
own the NoQuest/Aurum/Cutter explanation results. Those methods contain
no literal call to `askEnterInstanceRaid`.

`InstanceRaidGuideJudge` derives from `JudgeBaseClass` and declares only an
empty `_onInit` (`judge/instanceraidguidejudge.lua:2-12`, `root/proto0`,
PC 0 `RETURN B1`). The authenticated static-actor SAN maps script actor
320014 to `/Judge/InstanceRaidGuideJudge`.

The same SAN maps the following quest rows to
`/Quest/Scenario/Gcl/Gcl104`:

| Quest ID | `xtx_quest.csv` physical line | English column 2 |
| ---: | ---: | --- |
| 111430 | 455 | In for Garuda Wakening (Limsa Lominsa) |
| 111630 | 489 | In for Garuda Wakening (Gridania) |
| 111830 | 523 | In for Garuda Wakening (Ul'dah) |

The SAN is `client/script/rq9q1797qvs.san`, 108911 bytes, SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`.
XOR-0x73 decoding and `[u32 BE id][NUL-terminated classPath]` parsing
reproduced all 2812 records in
`xivl-client-data:manifests/staticactor_class_paths.json`, SHA-256
`d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
The useful records are IDs 111430/111630/111830 and 320014. This table
covers script actors; it has no guide NPC-instance binding. The title/class
join does not select a duty variant or show a guide invocation.

`Gcl104` was selected from that actual mapping. Its only three selector-like
calls retain one result and compare it with numeric 1:

| Method | Source lines and prototype | Call / return observation |
| --- | --- | --- |
| `processEventStart` | `410-443`, `root/proto4` | `showQuestInfomation()` at PC 122, `CALL A6 B2 C2`; returns that one result at PC 146, `RETURN A6 B2`. |
| `processEventLouisoix01` | `695-789`, `root/proto8` | Supplied NPC's `askExtendWidget(self,205,2,0,1)` at PC 144, `CALL A3 B7 C2`; dialogue branches finish with zero results at PC 216, `RETURN B1`. |
| `processEventZanthael` | `1967-2007`, `root/proto35` | Supplied NPC's `ask(self,279,2)` at PC 16, `CALL A3 B5 C2`; answer 1 selects two cutscene calls; returns the one ask result at PC 43, `RETURN A3 B2`. |

All source lines in that table are in `quest/scenario/gcl/gcl104.lua`.
The complete chunk has no literal `askEnterInstanceRaid` or
`contentsJoinAskInBasaClass` target or duty widget call, and identifies no
selected content value. Quest information, dialogue and cutscene branches
supply no duty admission/result join. Inherited helpers and external callers remain
outside this resource's boundary.

## Search boundary and missing join

A case-sensitive literal query for `askEnterInstanceRaid` and
`contentsJoinAskInBasaClass` covered all 2671 canonical Lua source members
of the authenticated archive. Every member matched its source-manifest
size/hash. The archive was 14385427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The only matches were their definitions: the guide base at line 58 and
`quest/questbaseclass_common.lua:576`. No literal local caller selected a
quest resource for the ordinary entry route. Dynamic names and externally
invoked inherited methods remain outside that negative.

The exact missing edge is a concrete event binding joining a guide NPC or
quest instance to the invoked method and supplied content value, followed
by the returned answer and its admission continuation. The examined SAN,
guide/judge chunks and Garuda title/class mapping do not supply it. No
Moogle entry quest class is established by these relationships. The generic
question's boolean is directly supported; an ordinary Garuda/Moogle
invocation and any server-authored eligibility, selection or admission
policy remain unbound.
