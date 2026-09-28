# Quest selector consumers

The stable client-side finding is a presentation contract, not an acceptance
contract. Each initial job-unlock script formats a level 30 base class and a
level 15 secondary class in worldMaster message 51130. All 42 job-quest scripts
also format the required active class or job in messages 51131 and 51132. The
recovered request path returns approval or refusal without selector arguments,
and no retained retail capture proves the authoritative server check.

The machine-readable census is
[`manifests/quest_selector_consumers.json`](../manifests/quest_selector_consumers.json).
It pins `xivl-client-data:csv/quest.csv`, `xtx_quest.csv`, and
`worldMaster.csv`, plus this repository's script manifest, registry, and N-API
index.

## Affected rows

| Family | Rows | Unlock requirement shown by 51130 | Later primary selector |
|---|---:|---|---|
| Warrior | 111201-111206 | Marauder 30 + Gladiator 15 | Warrior (17) |
| Monk | 111221-111226 | Pugilist 30 + Lancer 15 | Monk (15) |
| White Mage | 111241-111246 | Conjurer 30 + Gladiator 15 | White Mage (27) |
| Black Mage | 111261-111266 | Thaumaturge 30 + Pugilist 15 | Black Mage (26) |
| Paladin | 111281-111286 | Gladiator 30 + Conjurer 15 | Paladin (16) |
| Bard | 111301-111306 | Archer 30 + Conjurer 15 | Bard (18) |
| Dragoon | 111321-111326 | Lancer 30 + Pugilist 15 | Dragoon (19) |

The client-data census contains 735 rows including row 0: 42 named rows with
both selectors, no named primary-only or secondary-only rows, 126 discipline
selectors, 66 explicit `All` rows, and 501 other or placeholder rows. Useful
controls are 110627 (War or Magic), 110813 (Land), 110814 (Hand excluding
Culinarian), and 110001 (`All`).

## Behavior matrix

| Case | Client presentation evidence | Request evidence | Server acceptance |
|---|---|---|---|
| Unlock, both listed classes at the shown levels | 51130 formats both requirements | Approval is result 1 | Not established |
| Unlock, primary only | 51130 still displays the missing secondary level 15 requirement | No selector arguments | Not established |
| Unlock, secondary only | 51130 still displays the missing primary level 30 requirement | No selector arguments | Not established |
| Unlock, neither | 51130 displays both requirements | No selector arguments | Not established |
| Active class differs from required primary | 51131 says the required class/job must be active to accept; 51132 says it must be active to advance | No selector arguments | Error-event selection is not recovered |
| Family rows 2-6 | 51131/51132 use the job overlay selector, while localized eligibility retains the secondary class | No selector arguments | Secondary enforcement is not established |
| `All` row | Quest detail presents `All`; there is no named selector | No named selector argument | Not established by these consumers |

## Consumer chain and boundary

Job scripts call `worldMaster.say`. `lua/scripts/world/worldmaster_event.lua`
forwards type 40 to `DesktopWidget.showMessage`, and
`lua/scripts/widget/desktopwidget.lua` appends it through
`DesktopWidget._appendMessagePool` (BCS-Y-0492 in `lua/napi_index.json`). This
chain establishes display behavior only.

Quest detail reads the eligibility fields in
`lua/scripts/widget/ask/questdetailwidget.lua`. `QuestInfoAsk` in
`lua/scripts/gamedata/cutscene_common.lua` returns only approval result 1 or
refusal result 2. It does not submit a primary or secondary selector. The
recovered client scripts also do not select which job-quest error event the
server sends.

One shipped anomaly is preserved: the 51132 callsite in
`lua/scripts/quest/scenario/drg/drg0j4.lua` passes quest ID 111304 while using
Dragoon selector 19. The expected family row would be 111324; this report does
not silently correct retail script arguments.

## Supported downstream use

For the seven initial unlock rows, the secondary threshold is no longer
unresolved: the exact 51130 consumers show level 15, matching the independent
job-requirement table at
`xivl-captures:studies/lodestone-manual/derived/tables/jobs.csv`. Bahamut can
therefore preserve each listed `secondaryClassId` with threshold 15
as client presentation evidence.

That does not justify claiming that the retail server enforced both selectors.
`BahamutXIV/bahamut:scripts/globals/interaction/quest.lua` currently discards
`secondaryClassId` and fails closed for named rows. The client evidence does not
establish an implementation policy until an authoritative retail acceptance or
rejection capture establishes enforcement.
The 35 later family rows retain a secondary class in localized text, but no
recovered 51130 consumer supplies an independent numeric threshold for them.
