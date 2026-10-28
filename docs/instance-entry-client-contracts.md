# Instance entry client contracts

The retail 1.23b sources recover quest identities, entry descriptions and
selector returns. None of the selected routes joins a positive answer to
instance allocation, an entry NPC instance ID, or a destination transform.
The distinctions below preserve original, repeatable and Hard requests.

## Variant identities and unresolved admission fields

| Requested variant | Supported quest/content identity | Director or content class | Concrete entry NPC/object ID | Destination zone | Actual entry position |
| --- | --- | --- | --- | --- | --- |
| Toto-Rak | `xtx_raidDungeon.csv` row 1 names the duty. Imperial Devices quest IDs 111410/111610/111810 map to `Com5l0`/`Com5g0`/`Com5u0`. | These are scenario classes; no duty-1-to-instance-Director binding is established. | Not established. `Com5*0` methods receive an actor argument; neither that parameter nor a named dialogue actor identifies a numeric instance. | Static place 2123 has `_zoneParam.csv` row 159 and `_layout.csv` row 313 (`fst0Dungeon03`). This identifies the static zone context, not a selected admission target. | Not established: missing accepted-entry destination transform, including X/Y/Z and facing. |
| Rivenroad, original To Kill a Raven | Quest IDs 111433/111633/111833 share `Gcl107`; duty vocabulary row 15 is Rivenroad. | `Gcl107` is a scenario class. `InstanceRaidLesserWhiteGeneral` and `InstanceRaidNormalWhiteGeneral` are not bound to duty 15/16 by the recovered evidence. | Not established. `processEventStewart` receives actor A2; its name supplies no numeric NPC instance binding. | Rivenroad place 4073 is shared by zone rows 257, 267 and 268. No original-entry discriminator selects one. | Not established: the answer-to-zone/transform producer is missing. |
| Rivenroad, repeatable ordinary battle | Duty vocabulary row 15 remains distinct from row 16. No distinct repeatable quest/caller is selected. `Gcl107`'s alternate description remains unassigned to a runtime mode. | No repeatable-instance Director or mode-specific dispatch is established. | Not established: no retained caller joins Stewart's supplied actor to a numeric instance. | The same three place-4073 zone candidates remain unselected. | Not established: no admission continuation or destination transform is joined. |
| Requested Rivenroad Hard / The Raven, Nevermore | Quest 110870 is `The Raven, Nevermore` and maps to `Sum6w0`. Duty vocabulary row 16 names Rivenroad (Hard). The quest-to-duty-16 runtime binding is not established. | `Sum6w0` is the recovered quest scenario class. Its methods do not select an instance Director; Lesser/Normal filenames do not supply that association. | Not established. `processEventTrisselle` supplies a method name and actor A2, without a numeric NPC instance ID or binding. | Place 4073 and zone rows 257/267/268 do not select a Hard instance. | Not established: no accepted answer-to-entry transform is recovered. |
| Ifrit Hard | Duty row 3 names the Bowl of Embers (Hard), distinct from ordinary row 4 and Extreme row 14. Quest 110627 maps to `Sum6a0`; its exit prompt supplies literal content value 3. | `Sum6a0` is a scenario class. No entry binding selects `InstanceRaidLesserIfrit`, `InstanceRaidNormalIfrit` or `InstanceRaidHyperIfrit`. | Not established. `sum6a0.csv` rows 47/48/54/57 describe a beastman aetheryte in a cave southwest of Camp Broken Water; no numeric object instance is supplied. | Bowl of Embers place 3038 is shared by `_zoneParam.csv` rows 240 and 265. No Hard-entry discriminator selects a zone row. | Not established: prose directions and an exit selector do not supply an accepted-entry X/Y/Z/facing transform. |

Identity sources: `xivl-client-data:manifests/staticactor_class_paths.json`,
records 110627, 110869, 110870, 111410/111610/111810 and
111433/111633/111833; `xivl-client-data:csv/xtx_quest.csv` English field 2, those same row
keys; `xivl-client-data:csv/xtx_raidDungeon.csv` English field 26, rows 1, 3, 4, 14, 15
and 16. These row keys are separate namespaces, not interchangeable zone,
NPC or Director IDs.

The static destination associations are direct selected-row observations:
`xivl-client-data:csv/xtx_placeName.csv`, English field 1, rows 2123,
3038 and 4073; `xivl-client-data:csv/_zoneParam.csv`, field 0; and `xivl-client-data:csv/_layout.csv`,
field 3. The unique Toto-Rak layout/zone association is also documented in
`xivl-client-data:docs/dungeon-map-identities.md`, layout row 313. A shared
place label does not discriminate the Rivenroad or Bowl of Embers copies.
Authored scene placements and inn `cutReplay` rows do not establish entry
positions.

## Exact client event and result boundaries

Here A0 denotes the method receiver. A1, A2 and later symbols are ordered
formal parameters after it; their roles follow the selected calls and do
not identify historical objects. All listed methods have fixed formal
parameters and are non-vararg. A returned selector is a client result,
without an inferred server acceptance meaning.
PCs are zero-based. Code and instruction offsets are byte offsets in the
decoded Lua 5.1 payload.

| Route and complete formal parameters | Exact selected call | Return and branch boundary | Useful source and original-bytecode locator |
| --- | --- | --- | --- |
| Generic `InstanceRaidGuideBaseClass.askEnterInstanceRaid(A0,A1)` | `desktopWidget:askForEventMode(nil,nil,worldMaster,1,false,true,52045,{52046,52047},A1)` | Retains one answer. Returns exactly one boolean, true only when the answer equals numeric 1, false otherwise. No duty-specific literal or admission continuation. | `lua/scripts/chara/npc/populace/instanceraidguide/instanceraidguidebaseclass.lua:31`; `root/proto2`, code 492, call PC15/552, return PC19/568. |
| Toto-Rak-related `Com5g0.processEvent_010_1(A0,A1,A2)` | `A2:startCliantTalkTurn(0,A1)`; `A2:say(A0,73,0)`; `A2:ask(A0,28,2)` | Returns the one saved answer. Numeric 1 reaches the return immediately; every other answer says row 31 and finishes talk before returning. No launch call. | `docs/grand-company-selector-paths.md`, Imperial Devices follow-up prompts; `root/proto4`, code 2434, ask PC13, return PC24/2530. |
| Toto-Rak-related `Com5l0.processEvent_010_01(A0,A1,A2)` | `A2:startCliantTalkTurn(2,A1)`; `A2:say(A0,79,0)`; `A2:ask(A0,43,2)` | Same one-answer return; the alternative branch says row 46 and finishes talk. | Same finding; `root/proto6`, code 3942, ask PC13, return PC24/4038. |
| Toto-Rak-related `Com5u0.processEvent_010_01(A0,A1,A2)` | `A2:startCliantTalkTurn(2,A1)`; `A2:say(A0,68,0)`; `A2:ask(A0,35,2)` | Same one-answer return; the alternative branch schedules 70795264, says row 72 and finishes talk. | Same finding; `root/proto6`, code 3605, ask PC13, return PC27/3713. |
| Rivenroad `Gcl107.processEventStewart(A0,A1,A2,A3,A4)` | `A2:askExtendWidget(A0,A0:getTextIdStewart(165,A4),3,1,1)` | Retains and eventually returns exactly one saved answer. Result 1 presents rows 178/179 or 332/333 and exits; 2 presents the description and repeats; 3/-3 exit. A4 selects text remapping only when exactly true. No caller binds A4 to original/repeatable/Hard. A3 is forwarded unchanged to description rows, without a recovered duty value. | `lua/scripts/quest/scenario/gcl/gcl107.lua:2139`; `root/proto28`, code 14826, ask PC37/14974, return PC154/15442. `getTextIdStewart`: source 2326, `root/proto29`, code 15850. |
| The Raven, Nevermore `Sum6w0.processEventStart(A0,A1,A2)` | `A0:showQuestInfomation()` | Retains one result, compares it with numeric 1 for dialogue, and returns that result unchanged. This is quest-offer presentation. | `lua/scripts/quest/scenario/sum/sum6w0.lua:23`; `root/proto1`, code 483, call PC10/523, return PC26/587. |
| The Raven, Nevermore `Sum6w0.processEventTrisselle(A0,A1,A2,A3)` | `A2:askExtendWidget(A0,12,3,1,1)` | One answer is saved. Result 1 says row 21 and exits; 2 presents rows 16-20/37 and repeats; 3/-3 exit. Finish-talk runs before exactly one saved answer is returned. A3 is forwarded unchanged to `worldMaster:say(A0,row,A3)` for rows 17-20/37. No literal duty value is supplied. | `lua/scripts/quest/scenario/sum/sum6w0.lua:63`; `root/proto2`, code 765, ask PC31/889, return PC96/1149. |
| The Raven, Nevermore `Sum6w0.processEventClearAfter(A0,A1,A2,A3)` | `A2:askExtendWidget(A0,5,3,1,1,A3)` | Same one-answer loop and return. Description branch forwards A3 to `worldMaster:say(A0,row,A3)` for rows 33-36/38. The extra ask argument and row-reference text do not select A3's runtime value or a duty variant. | `lua/scripts/quest/scenario/sum/sum6w0.lua:207`; `root/proto4`, code 1746, ask PC32/1874, return PC97/2134. |
| Repeatability-related information `Etc304.processAfterQuestRewardWidget(A0,A1,A2)` | `desktopWidget:openEventModeWidgetYield("ExtraBossInfomationWidget")`; only when its first result is exactly true, `worldMaster:say(A0,158)` and `desktopWidget:closeEventModeWidget("ExtraBossInfomationWidget")` | Waits 5 first, and 4 before the conditional message. Returns zero values. The information widget/message does not allocate content or establish a later entry invocation. | `lua/scripts/quest/scenario/etc/etc304.lua:587`; `root/proto8`, code 4470, open PC6/4494, equality PC7/4498, say PC16/4534, return PC21/4554. |
| Ifrit quest offer `Sum6a0.processEventLOUISOIXStart(A0,A1,A2,A3,A4)` and `processEventLOUISOIX2ndStart(A0,A1,A2,A3,A4)` | `A0:showQuestInfomation()` | Each retains and returns exactly one quest-information result, with a numeric-1 dialogue branch. Neither is an instance-entry call. | `lua/scripts/quest/scenario/sum/sum6a0.lua:23` and `:227`; `root/proto1`, code 604, call PC133/1136, return PC160/1244; `root/proto2`, code 1697, call PC63/1949, return PC90/2057. |
| Ifrit quest item dialogue `Sum6a0.processEvent_005(A0,A1,A2)` / `processEvent_005_2(A0,A1,A2)` | `A2:ask(A0,42,2)` | Both retain one ask answer and branch on numeric 1. `_005` returns that saved answer; `_005_2` returns zero values. Their fades, scheduler calls and dialogue do not establish entry or item settlement. | `lua/scripts/quest/scenario/sum/sum6a0.lua:345` / `:446`; `root/proto3`, code 2384, ask PC16/2448, return PC75/2684; `root/proto4`, code 2997, ask PC16/3061, return PC56/3221. |
| Ifrit Hard exit prompt `Sum6a0.processEventContentExit(A0,A1,A2,A3)` | `worldMaster:ask(A2,worldMaster,52042,2,3)` | Returns exactly one boolean: true for ask answer numeric 1, false otherwise. The full call includes literal 3, which the referenced duty text names Hard. This is an exit question; it supplies no entry callback or transition. | `lua/scripts/quest/scenario/sum/sum6a0.lua:590`; `root/proto7`, code 4002, ask PC7/4030, returns PC11/4046 and PC14/4058. |

The preserved spelling `Infomation`, `Cliant` and `BasaClass` belongs to the
source identifiers. The separate common helper
`QuestBaseClass.contentsJoinAskInBasaClass` forwards all results of
`getQuestId()` to `actor:ask(worldMaster,25015,2,...)` and returns one
answer. Its variable argument behavior and inherited widget continuation
are recorded in `docs/duty-confirmation-client-contract.md`, Prompt and
argument forwarding and Selection and continuation. No selected concrete
entry invocation is established by availability of that inherited helper.

## What the descriptions establish

`gcl107.csv` rows 170/171/172 describe a party, To Kill a Raven entry
requirements and a visit limit. When Stewart's A4 is exactly true, rows
327/328/329 replace them; row 328 names completion of To Kill a Raven and
Living on a Prayer. `docs/to-kill-a-raven-client-contract.md`, Stewart's
alternate entry description, owns the original rich-string/static-count
interpretation and its missing caller-to-content join. The false/true text
paths are not authenticated original/Hard dispatch values.

`sum6w0.csv` rows 12-15 are the boarding menu, and rows 5-8 are the later
attempt menu. Rows 17-20/37 and 33-36/38 describe boarding requirements,
Living on a Prayer, visit duration, cooldown presentation and recast reset.
The latter rows reference `xtx/raidDungeon` through their supplied argument.
These are shipped descriptions; neither the menu result nor the supplied
formatter value implements or proves the described server rule.

`etc304.csv` row 158 says that The Raven, Nevermore can be initiated from
Gridania's airship landing. `Etc304` is Living on a Prayer, quest 110869.
This gives a named source location and a conditional message method, not a
numeric Trisselle/Stewart instance, a Hard-mode selector, or an entry
position. `sum6a0.csv` row 57 similarly describes a beastman aetheryte
granting access to the Bowl of Embers without a numeric object binding.

`worldMaster.csv` English field 1, rows 52042-52047, separates the
end-duty question and Yes/No from the begin-duty question and Yes/No.
When the Sum6a0 call resolves to shipped `WorldMaster.ask`, its complete
argument tail is forwarded to the desktop helper. On this route that is
`desktopWidget:askForEventMode(A2,worldMaster,worldMaster,1,false,true,52042,{52043,52044},3)`.
`world/worldmaster_event.lua:236`, `root/proto8`, code 1988, uses
`VARARG B0` at PC18/2060 and `CALL B0 C2` at PC19/2064, retaining one
answer. It maps answer -3 to nil and returns one value at PC23/2080.
Thus the literal 3 is the static Hard-duty text-reference argument on
this inspected helper path. This does not establish historical helper
resolution, exit execution, or admission.

## Search and evidence limits

The existing authenticated full-corpus exact-name search in
`docs/primal-entry-client-contract.md`, Search boundary and missing join,
found only the definitions of `askEnterInstanceRaid` and
`contentsJoinAskInBasaClass`. It is not repeated here. Dynamic dispatch,
inherited invocation and external event producers remain outside that
negative. The selected Sum6w0 and Sum6a0 original chunks contain dialogue,
selector, presentation and fade calls; they supply no direct instance launch
or destination transform. Gcl107's complete retained analysis and original
boundary are recorded in `docs/to-kill-a-raven-client-contract.md`.

The next evidence needed for every unresolved entry is one concrete event
binding containing the actor instance and selected method, complete supplied
arguments, returned answer, accepted continuation, selected content/Director
and destination transform. Rivenroad additionally needs the original versus
repeatable versus Hard discriminator; Ifrit needs an entry-side link selecting
Hard rather than ordinary or Extreme. No class-name inference closes either
gap.

Retained web and video manifests provide qualified leads only. The
`xivl-captures:studies/elemen-instanced-content-entry-rules/manifest.yaml`
assigns web-tables; `xivl-captures:studies/se-forum-rivenroad-hard-51632/manifest.yaml`
assigns historical-research; and
`xivl-captures:sources/side-quest-rivenroad-hard-video-breakdown/manifest.yaml` preserves
the recording provenance without an exact recording-patch identity. Those
sources do not supply the retail 1.23b numeric admission bindings above.

## Source identity and reproduction

The selected canonical sources are extraction `2012.09.19.0001`. Their complete
member sizes and SHA-256 values matched [scripts.json](../manifests/scripts.json)
inside the archive declared by
[private_lua_corpus.json](../manifests/private_lua_corpus.json).
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) maps each named
source to its original LPB and decoded-payload identities. Each selected original
matched both pins. `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` supplied the decoded instruction
observations above. No decompiler regeneration was required for those operands.

The selected CSV members matched `xivl-client-data:manifests/tables.json` inside
the archive declared by `xivl-client-data:manifests/private_csv_corpus.json`.
Reproduction selects the exact source members, prototypes, rows and numeric
fields above, preserving argument order, return arity and duplicate zone rows.
