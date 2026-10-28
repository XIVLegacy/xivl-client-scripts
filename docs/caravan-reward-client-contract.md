# Caravan reward guide client contract

`PopulaceCaravanGuide` supplies dialogue and a return-to-camp choice. Its
`caravanGuardReward` result is the answer to that travel prompt. The selected
retail sources do not bind a numeric NPC actor class, historical placement,
reward calculation, payout or authoritative completion to this method.

## Identity and placement

The authenticated `chara/npc/populace/populacecaravanguide.lua` defines
`PopulaceCaravanGuide : NpcBaseClass` and loads text bank 7552,
`populaceCaravanGuide` (`initForEvent`, root/proto0). It calls
`_setGroundOn(true)`. That call supplies no placement coordinate.
The source manifest and retail resource pins are in
`xivl-client-scripts:manifests/scripts.json` and
`manifests/retail_lua_coverage.json`, exact decoded-script key above.

Numeric NPC class and exact placement source are **not established** by this
selection. `xivl-client-data:manifests/staticactor_class_paths.json` explicitly
covers script actors and excludes server-bound NPC classes. Text bank 7552,
the class name, and a destination named in dialogue cannot substitute for a
numeric class or placement record. The discriminator is a retail class-bearing
actor record joined to this path, followed by that actor's placement record.

## Talk methods

Arguments below exclude self. All method locators refer to the identified
guide. `say` rows are in `xivl-client-data:csv/populaceCaravanGuide.csv`.
Prototypes and PCs are zero-based. Source line locators refer to the
authenticated canonical archive member.

| Method / prototype | Supplied argument use | Client return |
| --- | --- | --- |
| `caravanGuardCancel`, proto1, source 27-66 | No arguments. Says 7, asks 8 with `(2,1,2)`, says 11 for result 1. | Saved ask result; RETURN PC28, payload `0x3B1`. |
| `caravanGuardReward`, proto2, source 69-202 | Six arguments, detailed below. | Saved ask-33 result; RETURN PC116, `0x65B`. |
| `caravanGuardNotReward`, proto3, source 205-215 | No arguments. `worldMaster:say(self,46)` presents insufficient contribution. | Zero results. |
| `caravanGuardFailReward`, proto4, source 218-282 | Two arguments. Their sum selects destination in rows 20/29/33. Row 21 receives literal item 3011317. Asks 33 with `(2,1,1,sum)`, says 36 for result 1. | Saved ask result; RETURN PC49, `0x931`. |
| `caravanGuardThanks`, proto5, source 285-343 | Three arguments are display-name selectors in row 4. Says 5/30, asks 8 with `(2,1,2)`, says 11 for result 1. | Saved ask result; RETURN PC44, `0xB1B`. |
| `caravanGuardOffer`, proto6, source 346-381 | Row 1 receives `A1+A2`; row 2 receives `(A3,A1+A2)` for company, sergeant and camp presentation. | Zero results. |
| `caravanGuardAmple`, proto7, source 384-411 | Row 3 receives `A1+A2` as destination selector. | Zero results. |
| `caravanGuardSuccess`, proto8, source 414-440 | No arguments. Says 18. | Zero results. |
| `caravanGuardFailure`, proto9, source 443-470 | Row 22 receives `A1+A2` as destination selector. | Zero results. |
| `caravanGuardIgnore`, proto10, source 473-489 | No arguments. Starts talk mode 2, then finishes. | Zero results. |
| `caravanGuardBonusReward`, proto11, source 492-522 | `A1` unused. `A2 == true` selects row 39, otherwise 40. Scheduler 354107392 is run and awaited. | Zero results. |
| `caravanGuardNotBonusReward`, proto12, source 525-542 | No arguments. Says 41, the inventory-full presentation. | Zero results. |

These names and text describe client presentation. No method above verifies
inventory capacity, computes a contribution score, grants an item or currency,
or sets authoritative completion. The caller chooses which method to invoke.

## Six-argument reward consumer

`caravanGuardReward(self,A1,A2,A3,A4,A5,A6)` has seven fixed parameters and
no varargs (root/proto2, code starts at decoded-payload `0x48B`).

| Argument | Exact use | Supported role / remaining boundary |
| --- | --- | --- |
| A1 | Compares with 9, 0, and `0 < A1 <= 5`; also formats row 31. | Cargo-outcome presentation selector: rows 16/13/14/15 describe all/no/most-lost/some-lost cargo. The argument's unit and producer are unbound. |
| A2 | Unused. | No client role recovered. |
| A3 | Compared with A4; second format value to row 38; added to A6. | Company selector in row 38 and part of a six-destination selector. No independent producer or enum assignment. |
| A4 | Compared with A3; first format value to row 38. | Company selector in localized row 38. No independent producer. |
| A5 | At least 50 selects row 32; 40 through less than 50 selects row 31. | Additional-reward dialogue threshold input. Text mentions beasts/bandits; it does not prove what A5 counts or a payout formula. |
| A6 | Added to A3 for rows 15/16/29/33. | Offset in the destination selector. No independent route/rank meaning. |

The four cargo branches run schedulers 84062208/83927040/84058112/83959808
respectively. After the threshold dialogue, the method says 17, and says 38
with `(A4,A3)` when A3 differs from A4. It runs and awaits scheduler 354107392,
says row 29 with `A3+A6`, then calls
`self:askExtendWidget(self,33,2,1,1,A3+A6)` once. The prompt is "Return to"
the camp selected by its rich-string switch. Result 1 says row 36. It finishes
the talk turn and returns that same result. The bytecode call is PC105 /
`0x62F`, with one requested result, and the return is PC116 / `0x65B`.
The addition feeding the ask is in the retained `0x613..0x65B` region.

Rows 15/16 select Wineport, Quarrymill, the Silver Bazaar, Aleport,
Hyrstmill or the Golden Bazaar. Rows 29/33 select Camp Bloodshore,
Camp Tranquil, Camp Horizon, Camp Skull Valley, Treespeak or Camp Drybone.
These are text alternatives, not an observed placement or travel route.

## Reward and completion boundary

Row 17 announces a reward. The method runs and awaits scheduler 354107392;
the selected evidence does not establish that scheduler's visual meaning.
The script has no settlement API or reward amount argument. Its final ask
concerns returning to camp, so accepting that ask is not evidence of payout.
The fail-reward item literal and bonus/inventory-full text also do not prove
a grant or inventory check.

`xivl-client-scripts:docs/content-director-ui-contracts.md#caravan-escort-director`
owns `CaravanGuardDirector` UI fields: finishTime, progress, chocobo states,
HP states and markers. No selected binding connects those work values to
these six reward arguments or connects a finish presentation to settlement.

The missing producers are the historical NPC class/placement binding,
event dispatch and full typed argument vector, contribution/cargo computation,
reward entitlement and actual grant, and the return-result continuation that
performs travel or completes the event. Each requires an identified retail
producer or a retained transaction joining the call, result and attributable
effect. No exact caravan wire opcode/argument binding is established by these
selected sources.

## Source identity and reproduction

The selected canonical guide member is extraction `2012.09.19.0001`.
Its complete size and SHA-256 matched [scripts.json](../manifests/scripts.json)
inside the archive declared by
[private_lua_corpus.json](../manifests/private_lua_corpus.json).
Its original LPB and decoded payload matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
`tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` supplied the original instruction
checks, including the single ask and saved return in root/proto2.
The complete `populaceCaravanGuide.csv` member matched
`xivl-client-data:manifests/tables.json`. Select its numeric rows above without
treating localized destinations or scheduler literals as actor placements.
