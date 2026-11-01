# Runtime operand and producer boundaries

The retail 1.23b client establishes the argument uses below. A formatter
position, stored work value or local return does not by itself identify the
server producer, its accepted input domain or a completed transaction.
Arguments exclude `self` unless a signature includes it explicitly.

## Contracts

| Subject | Answer and argument contract | Canonical evidence | Confidence and missing binding |
| --- | --- | --- | --- |
| Action-removal text 30604 | The command-removal announcement looks up `xtx/command`, column 2, using formatter argument 2, `E8(2)`. It renders no action slot. The first argument and the inferred `(slot, commandId)` producer tuple remain unproved. | [Message operand rows](https://github.com/XIVLegacy/xivl-client-data/blob/6254f89b23f8958c53613af57dad5deae61fdaac/docs/message-operand-rows.md), `worldMaster` 30604, English logical column 1; [WorldMaster forwarding](worldmaster-message-arguments.md#generic-argument-route). | High static expression and ordered helper forwarding. The actual removal producer, complete typed vector and runtime rendering are unresolved. |
| Quest-map requested data | `PlayerBaseClass._onReceiveDataPacket` forwards subtype, supplied ID and the remaining tail to `DesktopWidget.processRecievedRequestedDataForWidget(self, subtype, suppliedID, ...)`. The `qtmap` arm ignores `suppliedID` and consumes only the ordered marker varargs, with an existing layer-3 map widget and a nonempty tail. | [Requested-data fixed arguments](content-director-ui-contracts.md#requested-data-fixed-arguments), original PlayerBase prototype 31, PCs 5-17, and desktop prototype 102, PCs 9-65; [selected exchange](https://github.com/XIVLegacy/xivl-captures/blob/a8e89429b1fe4aaa5adef435f886db58126eb60a/studies/quest-journal-map-wire/derived/evidence-map.md#source-and-records), packets 94/96. | High static argument split and selected received list. Server phase selection, historical leaf-class/function dispatch and visible marker rendering remain unresolved. |
| Guildleve signal-dependent marker | The non-self initializer vector is `(D, G, L, X, Y, Z)`: Director ID, Guildleve ID, aetheryte location and extra-marker coordinates. The retained vector is `(20005, 12487, 6, 0, 0, 0)`. Positive `signal` can publish the extra marker; `signal == -1` emits finish and refreshes the marker. | [Initializer arguments](guildleve-initializer-arguments.md#retained-12487-vector); [Guildleve marker consumer](content-director-ui-contracts.md#guildleve-and-request-directors); [native producer limits](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/docs/net/guildleve-initializer-route.md#remaining-unknowns). | High selected vector routing and client uses. The producer and row/key identity of the signal-dependent coordinates are unresolved. Matching a Director ID to a sheet border, or reading a time limit, does not supply that join. |
| Caravan reward guide | `caravanGuardReward(self, A1, A2, A3, A4, A5, A6)` uses A1 for cargo-outcome presentation, leaves A2 unused, compares A3/A4 as company selectors, tests A5 at 40/50 dialogue thresholds and adds A6 to A3 for a destination selector. It returns the answer to the row-33 return-to-camp prompt; result 1 says row 36. | [Six-argument reward consumer](caravan-reward-client-contract.md#six-argument-reward-consumer), original prototype 2, ask PC 105 and return PC 116; [identity and placement](caravan-reward-client-contract.md#identity-and-placement). | High selected method uses and saved return. No numeric guide class, placed actor, event owner, complete historical caller vector or cargo-claim continuation is bound. The travel answer does not prove payout. |
| Place-driven variations | The selected lookup maps `20001` to `22002` Mine; `20002` to `22003` Log; `20003` and `30003` to `22004` Fish; `20004` to `22005` Herd; `20005/20009` to `22006` Quarry; `20006/20010` to `22007` Harvest; and `20007/20011` to `22008` Spearfish. Other inputs return nil. | [Place-driven lookup](gathering-marker-fishing-ui.md#place-driven-judge-command-mapping), original prototype 0, PCs 0-38; [command catalog](https://github.com/XIVLegacy/xivl-client-data/blob/6254f89b23f8958c53613af57dad5deae61fdaac/derived/command_battle_params.csv), exact rows 22002-22008, `name_en`. | High selected lookup and static names. The broader `canFire` interval `20001-20012` adds no mapping for `20008` or `20012`. This does not define another judge callback's operands or prove a gathering transaction. |
| Job unlock and activation | The seven initial job-unlock hints display primary level 30 and secondary level 15, with the class pairs below. Quest approval returns result 1 without selector arguments. Active-job state, stone possession, unlock presentation and activation submission are separate contracts. | [Quest selector consumers](quest-selector-consumers.md#affected-rows), seven initial `51130` consumers; [job-state and acquisition limits](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/docs/actor/job-soulstone-state.md#actions-and-acquisition-boundaries); [Equipment selection limits](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/docs/script/equipment-soulstones.md#widget-masks-and-limits). | High displayed unlock requirements. Whether activation rechecks secondary level 15, and where the retail server enforces each job's requirements, remain unresolved. Stone identities alone do not prove that policy. |

## Selected quest-map reply

The retained map request carries integers `110658, 2` and seven nils.
The incoming list is `requestedData, qtmap, 110658, 11065801`. Under the
verified PlayerBase forwarding contract, `110658` fills the fixed supplied-ID
formal and is excluded from the marker varargs. Only `11065801` enters the
marker list and becomes string `11065801` in both `ssd_marker_data.Row` and
`CustomControl_MapNavigation.QuestMapIndex`.

The [capture finding](https://github.com/XIVLegacy/xivl-captures/blob/a8e89429b1fe4aaa5adef435f886db58126eb60a/studies/quest-journal-map-wire/derived/evidence-map.md#client-argument-and-static-row-join)
owns packet identities and transport/time association. The
[static row crosscheck](https://github.com/XIVLegacy/xivl-client-data/blob/6254f89b23f8958c53613af57dad5deae61fdaac/docs/quest-marker-rows.md#row-11065801)
owns marker 11065801 and the same-key quest title The Penultimate Prank.
These establish one received list and its conditional client argument use.
They do not expose the server's per-quest phase selector or prove the
historical callback lookup and rendered UI. The marker suffix `01` and the
separate journal reply's final numeric input `8` do not identify phases.

## Initial job-unlock presentation

The exact pairs are owned by the
[quest selector report](quest-selector-consumers.md#affected-rows).

| Initial job quest | Primary class and level | Secondary class and level |
| --- | --- | --- |
| Warrior, 111201 | Marauder 30 | Gladiator 15 |
| Monk, 111221 | Pugilist 30 | Lancer 15 |
| White Mage, 111241 | Conjurer 30 | Gladiator 15 |
| Black Mage, 111261 | Thaumaturge 30 | Pugilist 15 |
| Paladin, 111281 | Gladiator 30 | Conjurer 15 |
| Bard, 111301 | Archer 30 | Conjurer 15 |
| Dragoon, 111321 | Lancer 30 | Pugilist 15 |

The [official manual's job table](https://github.com/XIVLegacy/xivl-captures/blob/a8e89429b1fe4aaa5adef435f886db58126eb60a/studies/lodestone-manual/derived/tables/jobs.csv)
independently documents these unlock requirements. Its
[evidence tier](https://github.com/XIVLegacy/xivl-captures/blob/a8e89429b1fe4aaa5adef435f886db58126eb60a/studies/lodestone-manual/README.md#study-contents)
is documented intent, rather than an observed acceptance or rejection.
The 35 later family rows retain a secondary class in localized eligibility
text, but have no independently recovered numeric threshold of 15 in these
consumers. Neither the initial hints nor the manual establishes a secondary
level check on activation after unlock.

## Evidence limits

The linked records preserve their source hashes, original instruction
locators and selected capture coverage. Missing producer and runtime joins
are limited to those records. They do not establish absence elsewhere in
the client or across historical sessions. Static argument forwarding, text
and UI choices remain distinct from authoritative grants and enforcement.
