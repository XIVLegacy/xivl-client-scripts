# Grand Company quest step contracts

Retail FFXIV 1.23b, extraction `2012.09.19.0001`. These contracts describe the six SAN-selected client implementations. They expose callable presentation methods, supplied argument positions, scenes and client returns. The tables do not define an authoritative server quest state machine.

## Reading the tables

`A0..An` are every fixed argument, including the receiver at A0. No selected declaration is variadic. A0 is the scenario/text owner, A1 is commonly forwarded to talk start, and A2 is the supplied speaking actor where used. A3 and later remain supplied values unless a local comparison or formatting use below qualifies them. Numeric NPC instance/class IDs are not established by a named method.

`Q` in the sequence/flag column means: no local `work` read/write was recovered; the external producer must select the method and state. Numeric suffixes are identifiers, not authenticated sequence values. `D` means: no required instance ID or director join is established by this method. The journal and Toto-Rak dialogue identify narrative content, not an instance-launch binding.

Choice expressions include the receiver explicitly: `A2.ask(A2,A0,43,2)` is exactly `A2:ask(A0,43,2)`. A return value such as `r61_0` is result zero of the call at PC 61 in the same prototype. The selected original call at that PC and the canonical metadata own its complete tuple. PCs are zero-based, byte offsets are in the decoded chunk, and source ranges use canonical decoded-source lines. Text-row lists are locators, not a claim that every listed row executes on one invocation.

Return columns report statically reachable RETURN sites from the bounded analysis. They do not assert historical runtime reachability or server acceptance. The precise follow-up and Echo path qualifications below use original operands to distinguish the actual return branches.

## Identity and scope

| Quest ID | English title | SAN class | Source |
| ---: | --- | --- | --- |
| 111427 | Alive | `/Quest/Scenario/Gcl/Gcl102` | `lua/scripts/quest/scenario/gcl/gcl102.lua` |
| 111627 | Two Vans are Better than One | `/Quest/Scenario/Gcg/Gcg102` | `lua/scripts/quest/scenario/gcg/gcg102.lua` |
| 111827 | Like Father, Like Son | `/Quest/Scenario/Gcu/Gcu102` | `lua/scripts/quest/scenario/gcu/gcu102.lua` |
| 111410 | Imperial Devices (Limsa Lominsa) | `/Quest/Scenario/Com/Com5l0` | `lua/scripts/quest/scenario/com/com5l0.lua` |
| 111610 | Imperial Devices (Gridania) | `/Quest/Scenario/Com/Com5g0` | `lua/scripts/quest/scenario/com/com5g0.lua` |
| 111810 | Imperial Devices (Ul'dah) | `/Quest/Scenario/Com/Com5u0` | `lua/scripts/quest/scenario/com/com5u0.lua` |

The six identities each select one listed class. This does not authorize selecting same-numbered Gcg/Gcu resources for SAN IDs owned by another class. The retained singular `questId: null` is not the identity authority.

## Narrative anchors and exact missing producers

| Quest | Client text anchor | Supported step context | First missing producer/join |
| --- | --- | --- | --- |
| Alive 111427 | `xtx_quest` 111427 columns 23-26; Sea 318-320; item-name 11000423 | Crash-site route, imperial confrontation, report to R'ashaht Rhiki; journal describes up to two companions and an interaction-menu Imperial Disruptor. | External dispatch into Gcl102, A1/A2 actor values, battle/director selection, item action/effect and success-to-state transition. |
| Two Vans are Better than One 111627 | `xtx_quest` 111627 columns 23-26; Fst 385-389; item-name 11000422 | Gas-attack aftermath, secure area, Pfrymloef Echo, report at Gridania landing; item is Mist Emitter. | External dispatch into Gcg102, A3 branch value for Quinquerol, actor values, battle/director selection and Mist Emitter effect. |
| Like Father, Like Son 111827 | `xtx_quest` 111827 columns 23-26; Wil 449-452; item-name 11000421 | Garlean fight near the cave northwest of Camp Black Brush, survivor Echo, Ul'dahn landing report. | External dispatch into Gcu102, A3 branch value for processEvent005, actors, encounter/director selection and disruptor effect. |
| Imperial Devices 111410 / 111610 / 111810 | `com5l0` 37 / `com5g0` 22 / `com5u0` 29 | Each briefing formats a supplied maximum Toto-Rak visit length in minutes. | Producer of duration, party bounds and level, numeric guide/NPC binding, follow-up answer consumer and authoritative admission continuation. |

Imperial Disruptor rows 11000421 and 11000423 share an English name but are distinct item IDs. Journal phase order is text, not proof of numeric quest state, runtime scheduling, combat AI, allied health conditions, item ownership, reward grants or historical invocation.

The SAN records describe script actors; their provenance explicitly excludes server-bound NPC actor classes. Consequently the method-name roles below remain useful identifiers without being numeric NPC joins. No direct caller record supplies these A2 objects.

## Alive - 111427

Class `/Quest/Scenario/Gcl/Gcl102`. Source `xivl-client-scripts:lua/scripts/quest/scenario/gcl/gcl102.lua`. `initText` supplies text source `gcl102`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 1020 | None |
| `processEventStart(A0,A1,A2)`; lines 23-156; `root/proto1` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 92 / 1483 [`A0.showQuestInfomation(A0) first result`]; 1 at PC 104 / 1531 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,5,6,7,99,9,10,11,12,8 |
| `processEventStartAfter(A0,A1,A2)`; lines 160-181; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 1958 | say 13 |
| `processEventMyrganmoen(A0,A1,A2)`; lines 185-228; `root/proto3` | A2 speaker; method label Myrganmoen; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 32 / 2250 | say 14,15,16,17 |
| `processEventMyrganmoen2(A0,A1,A2)`; lines 232-253; `root/proto4` | A2 speaker; method label Myrganmoen2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 2506 | say 18 |
| `processEventHidden(A0,A1,A2)`; lines 257-290; `root/proto5` | A2 speaker; method label Hidden; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 24 / 2766 | say 19,100,20 |
| `processEventHidden2(A0,A1,A2)`; lines 294-315; `root/proto6` | A2 speaker; method label Hidden2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 3004 | say 21 |
| `processEventRashaht(A0,A1,A2,A3)`; lines 319-420; `root/proto7` | A2 speaker; method label Rashaht; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 80 / 3488 | say 23,22,24,25,26,102,27,28,29,30 |
| `processEventRashaht2(A0,A1,A2)`; lines 424-445; `root/proto8` | A2 speaker; method label Rashaht2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 3859 | say 31 |
| `processEventNQ(A0,A1,A2)`; lines 449-465; `root/proto9` | A2 supplied speaker; numeric NPC UNJOINED | "gc01l210" -> replay 11142701 | Q; input tests below | D | 0 at PC 10 / 4063 | None |
| `processEventCid(A0,A1,A2)`; lines 469-576; `root/proto10` | A2 speaker; method label Cid; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 84 / 4554 | say 75,76,77,78,96,97,98,82,83,84,86,87 |
| `processEventCid2(A0,A1,A2)`; lines 580-601; `root/proto11` | A2 speaker; method label Cid2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 4909 | say 88 |
| `processEventEbrelnaux(A0,A1,A2)`; lines 605-696; `root/proto12` | A2 speaker; method label Ebrelnaux; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 71 / 5357 | say 66,67,68,69,70,101,71,72,73,74 |
| `processEventEbrelnaux2(A0,A1,A2)`; lines 700-721; `root/proto13` | A2 speaker; method label Ebrelnaux2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 5685 | say 74 |
| `processEventJijina(A0,A1,A2)`; lines 725-774; `root/proto14` | A2 speaker; method label Jijina; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 5997 | say 60,61,62,63,64 |
| `processEventJijina2(A0,A1,A2)`; lines 778-799; `root/proto15` | A2 speaker; method label Jijina2; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 6262 | say 65 |
| `processEventBolaff(A0,A1,A2)`; lines 803-836; `root/proto16` | A2 speaker; method label Bolaff; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 24 / 6522 | say 50,51,52 |
| `processEventSaelbmoht(A0,A1,A2)`; lines 840-889; `root/proto17` | A2 speaker; method label Saelbmoht; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 6852 | say 53,54,55,56,57 |
| `processEventSorezari(A0,A1,A2)`; lines 893-920; `root/proto18` | A2 speaker; method label Sorezari; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 7137 | say 58,59 |
| `processEventHidden3(A0,A1,A2)`; lines 924-951; `root/proto19` | A2 speaker; method label Hidden3; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 7386 | say 91,92 |
| `processEventMyrganmoen3(A0,A1,A2)`; lines 955-982; `root/proto20` | A2 speaker; method label Myrganmoen3; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 7635 | say 89,90 |
| `processEventClear(A0,A1,A2)`; lines 986-1054; `root/proto21` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 50 / 8008 | say 93,94,95 |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 62 / offset 1363 |
| `processEventRashaht` | `A3 == 1`; no authoritative state write is established. | `root/proto7` PC 16 / offset 3232 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Two Vans are Better than One - 111627

Class `/Quest/Scenario/Gcg/Gcg102`. Source `xivl-client-scripts:lua/scripts/quest/scenario/gcg/gcg102.lua`. `initText` supplies text source `gcg102`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 1300 | None |
| `processEventStart(A0,A1,A2)`; lines 23-162; `root/proto1` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 97 / 1783 [`A0.showQuestInfomation(A0) first result`]; 1 at PC 109 / 1831 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,5,6,7,8,9,10,100,11,13,12 |
| `processEventStartAfter(A0,A1,A2)`; lines 166-198; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 23 / 2294 | say 14 |
| `processEventPfrymloef(A0,A1,A2)`; lines 202-211; `root/proto3` | A2 speaker; method label Pfrymloef; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 2521 | say 15 |
| `processEventArthur(A0,A1,A2)`; lines 215-230; `root/proto4` | A2 speaker; method label Arthur; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 10 / 2632 | say 16,17 |
| `processEventTalloak01(A0,A1,A2)`; lines 234-257; `root/proto5` | A2 speaker; method label Talloak01; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 2776 | say 18,19 |
| `processEventVevina01(A0,A1,A2)`; lines 261-284; `root/proto6` | A2 speaker; method label Vevina01; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 2980 | say 20,21 |
| `processEventQuinquerol(A0,A1,A2,A3)`; lines 288-362; `root/proto7` | A2 speaker; method label Quinquerol; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 59 / 3356 | say 25,22,23,24,26,27,103,28,29,30 |
| `processEventArthurNQF(A0,A1,A2)`; lines 366-375; `root/proto8` | A2 speaker; method label ArthurNQF; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 3597 | say 31 |
| `processEventTalloak02(A0,A1,A2)`; lines 379-408; `root/proto9` | A2 speaker; method label Talloak02; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 3752 | say 32,33,34 |
| `processEventVevina02(A0,A1,A2)`; lines 412-421; `root/proto10` | A2 speaker; method label Vevina02; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 3921 | say 35 |
| `processEventQuinquerolNQF(A0,A1,A2)`; lines 425-448; `root/proto11` | A2 speaker; method label QuinquerolNQF; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 4056 | say 36,37 |
| `processEventPfrymloefNQF(A0,A1,A2)`; lines 452-484; `root/proto12` | A2 speaker; method label PfrymloefNQF; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 17 / 4264 [`worldMaster.ask(worldMaster,A0,worldMaster,51030,2) first result`]; 1 at PC 24 / 4292 [`worldMaster.ask(worldMaster,A0,worldMaster,51030,2) first result`] | say 38,39; ask 51030 |
| `processEventPfrymloefNQ(A0,A1,A2)`; lines 488-510; `root/proto13` | A2 speaker; method label PfrymloefNQ; numeric NPC UNJOINED | "gc01g210" -> replay 11162701 | Q; input tests below | D | 0 at PC 15 / 4513 | say 58 |
| `processEventPfrymloefNQA(A0,A1,A2)`; lines 514-523; `root/proto14` | A2 speaker; method label PfrymloefNQA; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 4713 | say 58 |
| `processEventArthurNQA(A0,A1,A2)`; lines 527-536; `root/proto15` | A2 speaker; method label ArthurNQA; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 4804 | say 59 |
| `processEventTalloak03(A0,A1,A2)`; lines 540-569; `root/proto16` | A2 speaker; method label Talloak03; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 4959 | say 60,102,61 |
| `processEventTalloak04(A0,A1,A2)`; lines 573-590; `root/proto17` | A2 speaker; method label Talloak04; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 5152 | say 62 |
| `processEventVevina03(A0,A1,A2)`; lines 594-617; `root/proto18` | A2 speaker; method label Vevina03; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 5347 | say 63,64 |
| `processEventQuinquerolNQA(A0,A1,A2)`; lines 621-688; `root/proto19` | A2 speaker; method label QuinquerolNQA; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 52 / 5695 | say 65,66,67,68,69,70,71 |
| `processEventQuinquerolFragC(A0,A1,A2)`; lines 692-706; `root/proto20` | A2 speaker; method label QuinquerolFragC; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 9 / 5971 | say 71 |
| `processEventLionnellais(A0,A1,A2)`; lines 710-727; `root/proto21` | A2 speaker; method label Lionnellais; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 6120 | say 72 |
| `processEventCid(A0,A1,A2)`; lines 731-748; `root/proto22` | A2 speaker; method label Cid; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 6295 | say 99 |
| `processEventEbrelnaux(A0,A1,A2)`; lines 752-781; `root/proto23` | A2 speaker; method label Ebrelnaux; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 6510 | say 73,74,75 |
| `processEventEbrelnauxAfter(A0,A1,A2)`; lines 785-802; `root/proto24` | A2 speaker; method label EbrelnauxAfter; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 6703 | say 75 |
| `processEventBardo(A0,A1,A2)`; lines 806-835; `root/proto25` | A2 speaker; method label Bardo; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 6918 | say 76,77,78 |
| `processEventBardoAfter(A0,A1,A2)`; lines 839-856; `root/proto26` | A2 speaker; method label BardoAfter; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 7111 | say 79 |
| `processEventClear(A0,A1,A2)`; lines 860-1038; `root/proto27` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 140 / 7802 | say 80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97 |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 85 / offset 1735 |
| `processEventQuinquerol` | `A3 == 1`; no authoritative state write is established. | `root/proto7` PC 4 / offset 3136 |
| `processEventPfrymloefNQF` | `worldMaster.ask(worldMaster,A0,worldMaster,51030,2) first result == 1`; no authoritative state write is established. | `root/proto12` PC 12 / offset 4244 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Like Father, Like Son - 111827

Class `/Quest/Scenario/Gcu/Gcu102`. Source `xivl-client-scripts:lua/scripts/quest/scenario/gcu/gcu102.lua`. `initText` supplies text source `gcu102`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 1087 | None |
| `processEventStart(A0,A1,A2)`; lines 23-112; `root/proto1` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 69 / 1458 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,5,6,7,9,8 |
| `processEvent000_2(A0,A1,A2)`; lines 116-154; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 28 / 1860 | say 10,11 |
| `processEvent000_3(A0,A1,A2)`; lines 158-206; `root/proto3` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 2233 | say 12,13,85,86 |
| `processEvent000_4(A0,A1,A2)`; lines 210-278; `root/proto4` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 53 / 2654 | say 14,15,16,87,88,89 |
| `processEvent000_5(A0,A1,A2)`; lines 282-330; `root/proto5` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 3062 | say 17,18,90,91 |
| `processEvent005(A0,A1,A2,A3)`; lines 334-414; `root/proto6` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 63 / 3523 | say 19,20,21,22,23,24,25,26,27 |
| `processEvent010_2(A0,A1,A2)`; lines 418-451; `root/proto7` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 24 / 3864 | say 28,29,30 |
| `processEvent010_3(A0,A1,A2)`; lines 455-465; `root/proto8` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 6 / 4070 | say 81 |
| `processEvent010_4(A0,A1,A2)`; lines 469-479; `root/proto9` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 6 / 4182 | say 81 |
| `processEvent010_5(A0,A1,A2)`; lines 483-493; `root/proto10` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 6 / 4294 | say 81 |
| `processEvent010(A0,A1,A2)`; lines 497-521; `root/proto11` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 17 / 4450 [`worldMaster.ask(worldMaster,A0,worldMaster,51030,2) first result`]; 0 at PC 18 / 4454 | say 31; ask 51030 |
| `processEvent015(A0,A1,A2)`; lines 525-541; `root/proto12` | A2 supplied speaker; numeric NPC UNJOINED | "gc01u210" -> replay 11182701 | Q; input tests below | D | 0 at PC 10 / 4642 | None |
| `processEvent015_2(A0,A1,A2)`; lines 545-554; `root/proto13` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 5 / 4815 | say 48 |
| `processEvent020(A0,A1,A2)`; lines 558-607; `root/proto14` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 5034 | say 49,50,51,52,53 |
| `processEvent025_2(A0,A1,A2)`; lines 611-638; `root/proto15` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 5310 | say 54,55 |
| `processEvent025_3(A0,A1,A2)`; lines 642-663; `root/proto16` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 5539 | say 56 |
| `processEvent025_4(A0,A1,A2)`; lines 667-694; `root/proto17` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 5779 | say 57,58 |
| `processEvent025_5(A0,A1,A2)`; lines 698-719; `root/proto18` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 6008 | say 78 |
| `processEvent025_6(A0,A1,A2)`; lines 723-744; `root/proto19` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 6228 | say 79 |
| `processEvent025_7(A0,A1,A2)`; lines 748-769; `root/proto20` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 6448 | say 80 |
| `processEvent025_8(A0,A1,A2)`; lines 773-811; `root/proto21` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 28 / 6724 | say 59,60 |
| `processEvent025(A0,A1,A2)`; lines 815-984; `root/proto22` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 134 / 7485 | say 61,62,63,64,65,66,67,68,69,82,70,71,73,83,74,75,76,84 |
| `processEvent_elevator_nq1F(A0,A1,A2)`; lines 988-1006; `root/proto23` | A2 supplied speaker; numeric NPC UNJOINED | "elv0u01a" -> replay no exact row | Q; input tests below | D | 0 at PC 11 / 7919 | None |
| `processEvent_elevator_nq2F(A0,A1,A2)`; lines 1010-1029; `root/proto24` | A2 supplied speaker; numeric NPC UNJOINED | "elv0u02a" -> replay no exact row | Q; input tests below | D | 0 at PC 11 / 8131 | None |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 51 / offset 1386 |
| `processEvent000_3` | `A2.isUpperRank(A2,3,11) first result == true`; no authoritative state write is established. | `root/proto3` PC 12 / offset 2133 |
| `processEvent000_4` | `A2.isUpperRank(A2,3,11) first result == true`; no authoritative state write is established. | `root/proto4` PC 12 / offset 2490 |
| `processEvent000_5` | `A2.isUpperRank(A2,3,11) first result == true`; no authoritative state write is established. | `root/proto5` PC 12 / offset 2962 |
| `processEvent005` | `A3 == 0`; no authoritative state write is established. | `root/proto6` PC 4 / offset 3287 |
| `processEvent010` | `worldMaster.ask(worldMaster,A0,worldMaster,51030,2) first result == 1`; no authoritative state write is established. | `root/proto11` PC 12 / offset 4430 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Imperial Devices (Limsa Lominsa) - 111410

Class `/Quest/Scenario/Com/Com5l0`. Source `xivl-client-scripts:lua/scripts/quest/scenario/com/com5l0.lua`. `initText` supplies text source `com5l0`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 742 | None |
| `processEventGUINCUMStart(A0,A1,A2,A3,A4)`; lines 23-163; `root/proto1` | A2 speaker; method label GUINCUMStart; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 113 / 1289 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,5,6,84,7,8,9,10,12,13,11 |
| `processEvent_000(A0,A1,A2,A3)`; lines 167-220; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 41 / 1824 | say 14,15 |
| `processEvent_005(A0,A1,A2,A3,A4)`; lines 224-336; `root/proto3` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 89 / 2432 | say 16,17,85,18,19,20,21,22,23,24 |
| `processEvent_005_01(A0,A1,A2,A3,A4)`; lines 340-381; `root/proto4` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 32 / 2878 | say 25,26,80 |
| `processEvent_010(A0,A1,A2,A3,A4)`; lines 385-532; `root/proto5` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 118 / 3558 | say 29,30,31,32,33,34,81,35,36,37,38,39,40,82,41,42 |
| `processEvent_010_01(A0,A1,A2)`; lines 536-569; `root/proto6` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 24 / 4038 [`A2.ask(A2,A0,43,2) first result`] | say 79,46; ask 43 |
| `menberCountUnderRange(A0,A1,A2,A3,A4,A5)`; lines 573-623; `root/proto7` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 40 / 4369 | say 29,30,27,28 |
| `processEvent_015(A0,A1,A2,A3)`; lines 627-689; `root/proto8` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 49 / 4782 | say 48,49,50,51,52,53,54,55 |
| `processEvent_015_1(A0,A1,A2)`; lines 693-716; `root/proto9` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 5049 | say 56,57 |
| `processEvent_015_2(A0,A1,A2)`; lines 720-743; `root/proto10` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 16 / 5253 | say 58,59 |
| `processEvent_020(A0,A1,A2,A3,A4)`; lines 747-846; `root/proto11` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 79 / 5709 | say 60,61,62,63,64,65,66,67,86,68 |
| `processEvent_020_2(A0,A1,A2,A3)`; lines 850-880; `root/proto12` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 22 / 6106 | say 87,83 |
| `processEvent_020_1(A0,A1,A2)`; lines 884-911; `root/proto13` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 6364 | say 69,70 |
| `processEvent_025(A0,A1,A2,A3)`; lines 915-1045; `root/proto14` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 103 / 6949 | say 71,72,88,89,90,91,92,93,73,74,75,76,77,78 |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventGUINCUMStart` | `A4 == 1`; no authoritative state write is established. | `root/proto1` PC 48 / offset 1029 |
| `processEventGUINCUMStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 84 / offset 1173 |
| `processEvent_005` | `A4 == 1`; no authoritative state write is established. | `root/proto3` PC 38 / offset 2228 |
| `processEvent_010` | `A3 == 1`; no authoritative state write is established. | `root/proto5` PC 7 / offset 3114 |
| `processEvent_010_01` | `A2.ask(A2,A0,43,2) first result == 1`; no authoritative state write is established. | `root/proto6` PC 14 / offset 3998 |
| `menberCountUnderRange` | `A5 == 1`; no authoritative state write is established. | `root/proto7` PC 5 / offset 4229 |
| `processEvent_015` | `A3 == 1`; no authoritative state write is established. | `root/proto8` PC 9 / offset 4622 |
| `processEvent_020` | `A3 == 1`; no authoritative state write is established. | `root/proto11` PC 23 / offset 5485 |
| `processEvent_020` | `A4 == 1`; no authoritative state write is established. | `root/proto11` PC 64 / offset 5649 |
| `processEvent_020_2` | `A3 == 1`; no authoritative state write is established. | `root/proto12` PC 7 / offset 6046 |
| `processEvent_025` | `A3 == 1`; no authoritative state write is established. | `root/proto14` PC 32 / offset 6665 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Imperial Devices (Gridania) - 111610

Class `/Quest/Scenario/Com/Com5g0`. Source `xivl-client-scripts:lua/scripts/quest/scenario/com/com5g0.lua`. `initText` supplies text source `com5g0`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 725 | None |
| `processEventFULKEStart(A0,A1,A2,A3,A4)`; lines 23-138; `root/proto1` | A2 speaker; method label FULKEStart; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 91 / 1184 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,5,6,7,8,10,11,9 |
| `followEvent_000(A0,A1,A2,A3,A4)`; lines 142-184; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 33 / 1651 | say 12,13,71 |
| `processEvent_010(A0,A1,A2,A3)`; lines 188-289; `root/proto3` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 81 / 2165 | say 14,16,17,18,74,19,20,21,22,23,24,25,26,27 |
| `processEvent_010_1(A0,A1,A2)`; lines 293-326; `root/proto4` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 24 / 2530 [`A2.ask(A2,A0,28,2) first result`] | say 73,31; ask 28 |
| `processEvent_020(A0,A1,A2)`; lines 330-455; `root/proto5` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 98 / 3093 | say 34,35,36,37,38,39,41,42,43,44,45 |
| `followEvent_020(A0,A1,A2)`; lines 459-486; `root/proto6` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 19 / 3519 | say 46,47 |
| `processEvent_030(A0,A1,A2)`; lines 490-525; `root/proto7` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 26 / 3796 | say 48,49,51,52 |
| `processEvent_030_1(A0,A1,A2)`; lines 529-558; `root/proto8` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 4038 | say 50,51,52 |
| `followEvent_030(A0,A1,A2)`; lines 562-579; `root/proto9` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 4231 | say 53 |
| `followEvent_040(A0,A1,A2)`; lines 583-612; `root/proto10` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 4446 | say 54,55,56 |
| `processEvent_050(A0,A1,A2)`; lines 616-665; `root/proto11` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 37 / 4743 | say 57,58,59,60,61 |
| `followEvent_050(A0,A1,A2)`; lines 669-686; `root/proto12` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 4987 | say 76 |
| `processEvent_060(A0,A1,A2)`; lines 690-780; `root/proto13` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 70 / 5389 | say 62,63,64,65,66,67,68,69,70 |
| `menberCountUnderRange(A0,A1,A2,A3,A4)`; lines 784-816; `root/proto14` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 24 / 5791 | say 15,72 |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventFULKEStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 61 / offset 1064 |
| `processEvent_010_1` | `A2.ask(A2,A0,28,2) first result == 1`; no authoritative state write is established. | `root/proto4` PC 14 / offset 2490 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Imperial Devices (Ul'dah) - 111810

Class `/Quest/Scenario/Com/Com5u0`. Source `xivl-client-scripts:lua/scripts/quest/scenario/com/com5u0.lua`. `initText` supplies text source `com5u0`; row ownership follows each call's explicit tuple and the receiver/readiness conditions in `xivl-client-scripts:docs/gc-text-source-bindings.md`.

| Method and full parameters; source/prototype | Supplied NPC role / numeric join | Scene | Sequence / flags | Instance / director | Return arity and locus | Text row locators |
| --- | --- | --- | --- | --- | --- | --- |
| `initText(A0)`; lines 11-19; `root/proto0` | Text loader; no NPC role | No scene call | Q; input tests below | D | 0 at PC 4 / 704 | None |
| `processEventAUBREYStart(A0,A1,A2,A3)`; lines 23-134; `root/proto1` | A2 speaker; method label AUBREYStart; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 88 / 1151 [`A0.showQuestInfomation(A0) first result`] | say 2,3,4,76,5,6,77,7,8,9 |
| `processEvent_000(A0,A1,A2)`; lines 138-176; `root/proto2` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 28 / 1589 | say 10 |
| `processEvent_005(A0,A1,A2,A3,A4,A5)`; lines 180-283; `root/proto3` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 84 / 2177 | say 11,78,79,80,81,12,74,13,14,69,15 |
| `processEvent_005_1(A0,A1,A2,A3,A4,A5)`; lines 287-340; `root/proto4` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 43 / 2638 | say 82,16,70,17 |
| `processEvent_010(A0,A1,A2,A3)`; lines 344-473; `root/proto5` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 104 / 3271 | say 20,21,22,23,24,25,26,27,28,29,30,31,32,75,33,34 |
| `processEvent_010_01(A0,A1,A2)`; lines 477-514; `root/proto6` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 1 at PC 27 / 3713 [`A2.ask(A2,A0,35,2) first result`] | say 68,72; ask 35 |
| `processEvent_015(A0,A1,A2,A3)`; lines 518-604; `root/proto7` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 69 / 4193 | say 73,39,40,41,42,43,44,47,48; notify 25117 |
| `processEvent_015_1(A0,A1,A2)`; lines 608-625; `root/proto8` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 11 / 4569 | say 49 |
| `processEvent_015_2(A0,A1,A2)`; lines 629-658; `root/proto9` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 21 / 4784 | say 50,51,52 |
| `processEvent_020(A0,A1,A2,A3)`; lines 662-761; `root/proto10` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 78 / 5245 | say 53,83,54,84,85,56,57,58 |
| `processEvent_020_1(A0,A1,A2)`; lines 765-786; `root/proto11` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 14 / 5592 | say 59 |
| `processEvent_025(A0,A1,A2,A3)`; lines 790-899; `root/proto12` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 86 / 6100 | say 60,61,62,86,63,64,65,66,67 |
| `menberCountUnderRange(A0,A1,A2,A3,A4)`; lines 903-945; `root/proto13` | A2 supplied speaker; numeric NPC UNJOINED | No scene call | Q; input tests below | D | 0 at PC 32 / 6569 | say 20,18,71 |

### Meaningful supplied inputs and choices

These comparisons qualify local presentation only. Complete static call arguments remain in `xivl-client-scripts:data/quest_contracts.json`, exact `scripts[]` selector above. The method source/prototype locators in the step table identify the corresponding original.

| Method | Local input / returned choice | Original locator |
| --- | --- | --- |
| `processEventAUBREYStart` | `A3 == 1`; no authoritative state write is established. | `root/proto1` PC 31 / offset 923 |
| `processEventAUBREYStart` | `A3 == 1`; no authoritative state write is established. | `root/proto1` PC 52 / offset 1007 |
| `processEventAUBREYStart` | `A0.showQuestInfomation(A0) first result == 1`; no authoritative state write is established. | `root/proto1` PC 67 / offset 1067 |
| `processEvent_005` | `A5 == 1`; no authoritative state write is established. | `root/proto3` PC 13 / offset 1893 |
| `processEvent_005_1` | `A5 == 1`; no authoritative state write is established. | `root/proto4` PC 8 / offset 2498 |
| `processEvent_010_01` | `A2.ask(A2,A0,35,2) first result == 1`; no authoritative state write is established. | `root/proto6` PC 14 / offset 3661 |
| `processEvent_015` | `A3 == 1`; no authoritative state write is established. | `root/proto7` PC 4 / offset 3933 |
| `processEvent_020` | `A3 == 1`; no authoritative state write is established. | `root/proto10` PC 29 / offset 5049 |
| `processEvent_020` | `A3 == 1`; no authoritative state write is established. | `root/proto10` PC 42 / offset 5101 |
| `processEvent_025` | `A3 == 1`; no authoritative state write is established. | `root/proto12` PC 48 / offset 5948 |

`doSalute` result tests choose local animation/wait presentation; they establish no objective flag. Methods absent from this table have no other local comparison in the selected prototype.

## Precise return and presentation qualifications

The three Imperial Devices follow-up prompts retain one `ask` result and return it unchanged. Numeric 1 reaches the return directly, without response or `finishCliantTalkTurn`. Other answers reach the company-specific response and talk finish. Com5u0 additionally runs scheduler 70795264 on that alternative path. Boolean true and string "1" are not numeric 1. Original locators: Com5g0 root/proto4 return PC 24 / offset 2530; Com5l0 root/proto6 PC 24 / 4038; Com5u0 root/proto6 PC 27 / 3713.

Gcg102.processEventPfrymloefNQF returns its saved `ask` result on both branches, after `A0:runCharaSchedulerPastAreaIn(A1)` only for numeric 1. Gcu102.processEvent010 returns its saved `ask` result only for numeric 1, after the same scheduler call; other answers return zero values. The scheduler call does not establish a server progression write.

The three `menberCountUnderRange` bodies return zero values and do not enumerate members, compute range or test level. Limsa selects opening row 29 for A5 == 1 and row 30 otherwise. Gridania forwards A3,A4 to WorldMaster row 72; Limsa and Ul'dah forward A4,A3 to rows 28/71. The tuples below preserve the distinct zero/one literals before these supplied values.

| Member helper | Meaningful parameterized message tuples (receiver explicit) |
| --- | --- |
| Com5g0.menberCountUnderRange(A0,A1,A2,A3,A4) | `A2.say(A2,A0,15,0,0,0,A3,A4)`; `worldMaster.say(worldMaster,A0,72,0,0,A3,A4)` |
| Com5l0.menberCountUnderRange(A0,A1,A2,A3,A4,A5) | `A2.say(A2,A0,29,0)` if A5 == 1, otherwise `A2.say(A2,A0,30,0)`; `A2.say(A2,A0,27,0,0,0,A4)`; `worldMaster.say(worldMaster,A0,28,1,0,A4,A3)` |
| Com5u0.menberCountUnderRange(A0,A1,A2,A3,A4) | `A2.say(A2,A0,20,0)`; `A2.say(A2,A0,18,0,0,0,A4)`; `worldMaster.say(worldMaster,A0,71,1,0,A4,A3)` |

Com5g0.processEvent_010 passes A3 to WorldMaster row 22; Com5l0.processEvent_010 passes A4 to row 37; Com5u0.processEvent_010 passes A3 to row 29. These rows format minutes. The scripts do not supply a fixed duration. Com5g0.followEvent_000 row 71 and member helper row 72 format party bounds and a minimum Disciple of War or Magic level from supplied values. The other company helper text has the corresponding variable admission wording; no numeric bounds can be promoted from these templates.

Com5u0.processEvent_015 calls `desktopWidget:openPublicInformDialogWidget(worldMaster,25117,11000261)` and `worldMaster:notify(worldMaster,25117,11000261)` and waits three seconds. This establishes client presentation only; the absent producer/settlement join is still required before treating that item as granted.

## Source locators and boundaries

Identity: `xivl-client-data:docs/grand-company-quest-identities.md`, six named rows; `xivl-client-data:manifests/staticactor_class_paths.json` records by ID; `xivl-client-data:csv/xtx_quest.csv` numeric column 2. Journal: `xivl-client-data:docs/grand-company-journal-text.md`, exact selected quest/journal/item rows above. Scene/replay: `xivl-client-scripts:docs/quest-scene-replay-joins.md`, gcg102/gcl102/gcu102 rows; exact scene joins are also retained in `data/quest_contracts.json` selected `scripts[].calls`.

Original return and message qualifications:
[Imperial Devices follow-up prompts and member-message helpers](grand-company-selector-paths.md#imperial-devices-follow-up-prompts)
and [briefing arguments](quest-event-client-contracts.md#imperial-devices-briefing-arguments).

The six selected canonical members matched [scripts.json](../manifests/scripts.json)
inside the archive declared by [private_lua_corpus.json](../manifests/private_lua_corpus.json).
Each original LPB and decoded payload matched its exact resource record in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) and
[quest_contracts.json](../data/quest_contracts.json). The selected original
`ChunkReader`/`analyze_chunk` results from `tools/build_quest_contracts.py`
equalled the retained declaration, call, text, scene, result, return and
quest-work records. The selected complete CSV members matched
`xivl-client-data:manifests/tables.json`. These checks establish source identity
and bounded instruction relationships, with the return-path qualifications above.

To implement progression, supply an independently evidenced mapping from authoritative state/event to the exact method and argument tuple, numeric NPC actor binding, any required director/content selector, and the consumer of the client return. Objective/item effects, encounter behavior, admission and reward settlement remain separate missing producer fields.
