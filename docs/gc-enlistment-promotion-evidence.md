# Grand Company enlistment and promotion evidence

This page separates the authenticated 1.23b client contract from documented
requirements. The client scripts prove presentation calls and local branches.
They do not prove server acceptance, seal debit, rank mutation, or the event
that supplies a method's arguments.

## Confidence grades

- **A**: authenticated retail artifact fact. An A claim is marked as static
  client data or observed wire evidence where that distinction matters.
- **B**: first-party historical documented intent from the preserved Lodestone
  manual. It is stronger than a community source but is not a runtime capture.
- **U**: unproved boundary or producer. U describes the claim, not a source
  quality judgment.

## Authenticated retail client contract

The source extraction is retail 1.23b (`2012.09.19.0001`). The authenticated
script members are pinned by `xivl-client-scripts:manifests/scripts.json` and
the matching LPB records in `xivl-client-scripts:manifests/retail_lua_coverage.json`.
The source identity table and decoded hashes are also recorded at
`xivl-client-scripts:docs/gc-promotion-client-contract.md:109-128`.

### Official enlistment: `Com0*7`

These are three separate client scenario classes. Each start method makes one
two-result widget request with the company number, then its accepted branch
shows the company join effect at literal rank 11 and updates the status UI.
The end method closes the presentation. The widget result is a local input;
the client source does not establish that it is a server-approved enlistment.

| Retail method | Exact recovered request | Accepted-branch presentation | Source id and grade |
| --- | --- | --- | --- |
| `Com0l7.processEventGuincamStart` | `askEventModeWidgetYield("Ask/GrandCompanyOfficialJoinWidget", 1, 1)`; consume two return values | `openGrandCompanyJoinEffectWidget(1, 11)`, then status-widget update | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:471-495`; member `lua/scripts/quest/scenario/com/com0l7.lua` and `.calls.json`; decoded SHA-256 `7fc28b2420c371d8148b99e2a8513b283adf12375d0ceb419b4b72bdb2373433`; A |
| `Com0g7.processEventFulkeStart` | `askEventModeWidgetYield("Ask/GrandCompanyOfficialJoinWidget", 1, 2)`; consume two return values | `openGrandCompanyJoinEffectWidget(2, 11)`, then status-widget update | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:471-495`; member `lua/scripts/quest/scenario/com/com0g7.lua` and `.calls.json`; decoded SHA-256 `c33194551226d96ad6d1d416b744b2c211fbb3457d4c67f4f2c9ac30b6aa83e8`; A |
| `Com0u7.processEventAubreyStart` | `askEventModeWidgetYield("Ask/GrandCompanyOfficialJoinWidget", 1, 3)`; consume two return values | `openGrandCompanyJoinEffectWidget(3, 11)`, then status-widget update | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:471-495`; member `lua/scripts/quest/scenario/com/com0u7.lua` and `.calls.json`; decoded SHA-256 `241134ea44074bf9855a3cefbd9dda50fd51fd39e5f04c2a533d78c513cfa8f9`; A |

The canonical source summary gives the method lines, bytecode call PCs, and
the explicit client-only boundary at
`xivl-client-scripts:docs/job-grand-company-event-contracts.md:467-495`.
The script registry independently records the three classes and method names
at `xivl-client-scripts:lua/registry.json:23427-23440,23603-23616,23790-23803`.

### Recruit tutorial: `Com0*2`

The recruit tutorial is a different path from official enlistment. Its start
method opens the Grand Company status presentation for its company and sets
the displayed points to zero. The paired end method displays 250 and closes
the widget after a wait. The 250 is a presentation value, not evidence of a
seal grant or a successful transaction.

| Retail method pair | Exact company and displayed values | Source id and grade |
| --- | --- | --- |
| `Com0l2.processEventGUINCUMStart` / `Com0l2.processEventGUINCUMEnd` | open company `1`; start points `0`; end points `250`; close | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:499-520`; member `lua/scripts/quest/scenario/com/com0l2.lua` and `.calls.json`; decoded SHA-256 `e73740a8efeecd5609e9ba47dd1404b58350350585dc0919c79b96c7f48629a1`; A |
| `Com0g2.processEventFulkeStart` / `Com0g2.processEventFulkeEnd` | open company `2`; start points `0`; end points `250`; close | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:499-520`; member `lua/scripts/quest/scenario/com/com0g2.lua` and `.calls.json`; decoded SHA-256 `cd98f56dd6cc8b364537b6125be17ec67cc64f209a24e2520fab3a6a5a84bf57`; A |
| `Com0u2.processEventAUBREYStart` / `Com0u2.processEventAUBREYFinal` | open company `3`; start points `0`; end points `250`; close | `xivl-client-scripts:docs/job-grand-company-event-contracts.md:499-520`; member `lua/scripts/quest/scenario/com/com0u2.lua` and `.calls.json`; decoded SHA-256 `80c320cafa8fc3448dc5d99ab4db6fc889630e5155aa5d18ee260ba0e80371ec`; A |

The bytecode call PCs and decoded hashes are retained at
`xivl-client-scripts:docs/job-grand-company-event-contracts.md:497-517`.
The related client-data notices are literal text rows only and do not prove
offer availability or a transaction:
`xivl-client-data:docs/grand-company-enlistment-notices.md:1-15`.

### Officer promotion methods

`PopulaceCompanyOfficer` has a menu, information, choice, rank-up, and done
method. The officer's `work.townNumber` is set to 1, 2, or 3 by actor class
1500199, 1500200, or 1500198. Its `work.companyRank` starts at literal 33;
that is the officer salute input, not the player's current rank.

| Method and arguments | Exact local behavior | Grade |
| --- | --- | --- |
| `eventTalkJoined(a1,a2,a3,a4)` | Starts the talk, salutes, then calls `askMultipleTextMacro(officer,officer,3,66,3,0,a4,true,true)`. Menu result `1` calls `eventRankUpChoice(a1,a2,a3)`; result `2` calls `eventInformationRankUp(a1,a2)` and repeats; other results return `0`. It returns `1` only when the choice helper returns boolean `true`. | A |
| `eventInformationRankUp(a1,a2)` | Says the first rank-up information row with `a2,a1`, then the remaining company-specific rows. | A |
| `eventRankUpChoice(a1,a2,a3)` | Reads `company = player._getBelongGrandCompany()` and `seals = player.getGrandCompanySealCount(company)`, then calls `askMultipleTextMacro(officer,officer,2,70,2,1,true,true,0,a1,seals,company,0,0)`. It returns `true` exactly when this macro returns `1` and supplied `a3 == true`; otherwise it presents refusal or other-answer text and returns `false`. `a2` is not read here. | A |
| `eventDoRankUp(a1,a2)` | Presents `a2`, runs the officer-class scheduler `84090880`, `84094976`, or `84099072`, opens the join effect with `(work.townNumber,a2)`, waits `4.7`, opens the status widget with `work.townNumber`, sets displayed join status to `a1`, and waits `2.7`. | A |
| `eventRankUpDone(a1,a2)` | Sets displayed join status to `a1`, displayed points to `a2`, plays the player salute, finishes the talk, and closes the status widget. | A |

The exact dialogue rows, calls, bytecode PCs, and wait values are recorded at
`xivl-client-scripts:docs/gc-promotion-client-contract.md:14-64`. The decoded
officer payload is SHA-256
`ba827b063fd9747cbab293e97d07ccf039768299342e3891abafbdaff0837e95`; its
registry methods are at `xivl-client-scripts:lua/registry.json:12694-12722`.
The player getter and status-widget consumers are authenticated at
`xivl-client-scripts:docs/gc-promotion-client-contract.md:66-98`.

The exact `true` approval is therefore a two-input local condition: macro
answer `1` and the supplied Lua boolean `a3`. The officer methods do not
compute `a3` from rank, seals, quest state, or a packet. The producer of
`a1`, `a2`, `a3`, and `a4`, and the caller of `eventDoRankUp` or
`eventRankUpDone`, remain U.

## Packet and event boundary

Within the examined named contracts (`Com0l7`, `Com0g7`, `Com0u7`, `Com0l2`,
`Com0g2`, `Com0u2`, and `PopulaceCompanyOfficer`), no retained retail source
binds an opcode, packet field, or server event ID to the methods below. The
only supported path is the following bounded model; each unbound edge is
labeled rather than filled by analogy.

| Edge | Status | Supported statement |
| --- | --- | --- |
| wire packet or server event -> client event dispatcher for the named contracts | U, unbound | No packet ID, field layout, or dispatcher join is recovered for these GC methods. |
| client event dispatcher -> `Com0*7` start or officer method in the named contracts | U, unbound | The named script method exists and has the calls above; historical invocation is not established. |
| `Com0*7` widget result -> accepted presentation branch | A, conditional | The script consumes two local return values and has an accepted branch; the producer and server meaning of those values are unbound. |
| `eventTalkJoined` menu result `1` -> `eventRankUpChoice`; result `2` -> `eventInformationRankUp`; other -> return `0` | A, conditional | This dispatch is within the recovered officer script. |
| `eventRankUpChoice` result `true` -> `eventTalkJoined` return `1` | A, conditional | The exact condition is macro result `1` plus supplied `a3 == true`. |
| officer choice -> `eventDoRankUp` or `eventRankUpDone` | U, unbound | These methods do not call one another in the recovered script; no caller or server event is retained here. |
| client status display -> authoritative membership, seals, or rank | U, unbound | UI setters and getters do not establish a server mutation or debit. |

Within these named contracts, the bounded model is `unbound event input ->
authenticated client presentation -> unbound server state`. This does not
assert a generic packet envelope. A method name or a local `true` result
cannot close the missing packet boundary.

## Static rank value and cost crosswalk

`xivl-client-data:derived/gc_rank.csv` is a static client-data product with
SHA-256 `b00c28217902142c60efaf1de16479f32f7cb9a39dd1913bf66492e7e42defcd`
(case-insensitive rendering of the manifest digest). It preserves all 22
`gcRank.csv` rows and three positional name variants per row. The field
semantics and unresolved company column are documented at
`xivl-client-data:docs/gc-rank.md:1-39,41-66`. The source sheets are pinned
by `xivl-client-data:manifests/retail_sheet_exports.json:61-79` and use sheet
IDs `gcRank 0x0103057E` and `xtx/gcRank 0x0B450BA8`.

The table below keeps every row. `guide` repeats the Lodestone table index
only where the same linear rank is present (1 through 9); it does not map a
name position to a company. `v0/v1/v2` are export positions, not company IDs.
The values are client getter/display inputs; `next` is
`seals_needed_next_rank`, not proof of a server debit.

| rank id | linear rank | guide | seal maximum | next | name variants v0 / v1 / v2 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 0 | - | 0 | 0 | source text is non-ASCII in all three positions |
| 11 | 1 | 1 | 10000 | 1000 | Storm Private Third Class / Serpent Private Third Class / Flame Private Third Class |
| 13 | 2 | 2 | 15000 | 1500 | Storm Private Second Class / Serpent Private Second Class / Flame Private Second Class |
| 15 | 3 | 3 | 20000 | 2000 | Storm Private First Class / Serpent Private First Class / Flame Private First Class |
| 17 | 4 | 4 | 25000 | 2500 | Storm Corporal / Serpent Corporal / Flame Corporal |
| 21 | 5 | 5 | 30000 | 3000 | Storm Sergeant Third Class / Serpent Sergeant Third Class / Flame Sergeant Third Class |
| 23 | 6 | 6 | 35000 | 3500 | Storm Sergeant Second Class / Serpent Sergeant Second Class / Flame Sergeant Second Class |
| 25 | 7 | 7 | 40000 | 4000 | Storm Sergeant First Class / Serpent Sergeant First Class / Flame Sergeant First Class |
| 27 | 8 | 8 | 45000 | 25000 | Chief Storm Sergeant / Chief Serpent Sergeant / Chief Flame Sergeant |
| 31 | 9 | 9 | 50000 | 50000 | Second Storm Lieutenant / Second Serpent Lieutenant / Second Flame Lieutenant |
| 33 | 10 | - | 50000 | 50000 | First Storm Lieutenant / First Serpent Lieutenant / First Flame Lieutenant |
| 35 | 11 | - | 50000 | 50000 | Storm Captain / Serpent Captain / Flame Captain |
| 41 | 12 | - | 60000 | 60000 | Second Storm Commander / Second Serpent Commander / Second Flame Commander |
| 43 | 13 | - | 60000 | 60000 | First Storm Commander / First Serpent Commander / First Flame Commander |
| 45 | 14 | - | 60000 | 60000 | High Storm Commander / High Serpent Commander / High Flame Commander |
| 51 | 15 | - | 70000 | 70000 | Rear Storm Marshal / Rear Serpent Marshal / Rear Flame Marshal |
| 53 | 16 | - | 70000 | 70000 | Vice Storm Marshal / Vice Serpent Marshal / Vice Flame Marshal |
| 55 | 17 | - | 70000 | 70000 | Storm Marshal / Serpent Marshal / Flame Marshal |
| 57 | 18 | - | 70000 | 0 | Grand Storm Marshal / Grand Serpent Marshal / Grand Flame Marshal |
| 100 | 19 | - | 100000 | 0 | Storm Champion / Serpent Champion / Flame Champion |
| 111 | 111 | - | 0 | 0 | Chief Admiral / Elder Seedseer / Flame General |
| 127 | 127 | - | 10000 | 500 | Storm Recruit / Serpent Recruit / Flame Recruit |

The company field is `unresolved` for all 66 derived records. The status
widget resolves icon columns 6, 7, and 8 for numeric companies 1, 2, and 3,
but no verified consumer joins those company IDs to name positions. Do not
turn the three labels in a row into a company mapping. The raw rank sentinel
`127` is handled by the retail Lua getter as `(0,true)`; this does not identify
a quest, approval producer, or server state.

The eight static current-rank `next` values that have matching guide
destination requirements have the following documented-destination crosswalk:

| Static current rank | A `gcRank` next value | B guide destination index | B guide destination requirement |
| ---: | ---: | ---: | --- |
| 11 | 1000 | 2 | 1,000 company seals |
| 13 | 1500 | 3 | 1,500 company seals |
| 15 | 2000 | 4 | 2,000 company seals |
| 17 | 2500 | 5 | Completion of the Enlistee to Petty Officer duties and 2,500 company seals |
| 21 | 3000 | 6 | 3,000 company seals |
| 23 | 3500 | 7 | 3,500 company seals |
| 25 | 4000 | 8 | 4,000 company seals |
| 27 | 25000 | 9 | Completion of the Petty Officer to Officer duties and 25,000 company seals |

This is numerical corroboration between A static sheet values and B
documented-intent destinations. It does not prove that a server debits the
value, that the destination is available, or that the named duties were
completed. Later static rows have no destination requirement in the preserved
guide.

## First-party documented requirements

The preserved source is the official Lodestone manual page
`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md`.
Its manifest pins the page at SHA-256
`daec7989504db2c4cbf289c8ce496ce417a2eb33ea6c1021ad19be25e52a5b2a` in
`xivl-captures:sources/lodestone-manual/manifest.yaml:1065-1067`. This is
first-party documented intent, grade B; the study explicitly retains a
runtime-versus-intent caveat at
`xivl-captures:studies/lodestone-manual/README.md:17-21`.

For recruit induction, the guide says a player needs one Discipline of War or
Magic at level 22 or higher, then names each prerequisite and acceptance quest
(`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:37-47`):

| Company | Prerequisite mission | Acceptance quest |
| --- | --- | --- |
| Maelstrom | The Price of Integrity | Testing the Waters |
| Order of the Twin Adder | Breaking the Seals | Why Did It Have to Be Snakes |
| Immortal Flames | Career Opportunities | Kindling a Flame |

The guide says recruits are not yet bound to an organization and may use that
period to discover a company and earn all three seal types
(`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:37-39`).

For official enlistment, the guide says a Discipline of War or Magic class at
level 25 or higher, completion of all three named missions, and acceptance of
the company-specific quest
(`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:49-69`):

| Company | Required completed mission | Acceptance quest |
| --- | --- | --- |
| Maelstrom | An Officer and a Wise Man | Till Sea Swallows All |
| Order of the Twin Adder | Their Finest Hour | Serenity, Purity, Sanctity |
| Immortal Flames | Burning Man | By Fire Reborn |

The announced rank table is the following. These requirements are not a
server packet contract and must remain separate from `gcRank.csv` values.

| Guide rank index | Commission | Requirement |
| ---: | --- | --- |
| 1 | Enlistee | Official enlistment |
| 2 | Enlistee | 1,000 company seals |
| 3 | Enlistee | 1,500 company seals |
| 4 | Enlistee | 2,000 company seals |
| 5 | Petty Officer | Completion of the duties below and 2,500 company seals |
| 6 | Petty Officer | 3,000 company seals |
| 7 | Petty Officer | 3,500 company seals |
| 8 | Petty Officer | 4,000 company seals |
| 9 | Officer | Completion of the duties below and 25,000 company seals |

The source table is at
`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:71-105`
and the normalized rows are at
`xivl-captures:studies/lodestone-manual/derived/tables/grand-company-ranks.csv:1-10`.
The guide names these duties for commission advancement
(`xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:99-105`):

| Commission change | Maelstrom | Order of the Twin Adder | Immortal Flames |
| --- | --- | --- | --- |
| Enlistee to Petty Officer | The Weakest Link | You Don't Have the Rite | Gore a Lizard, Hurry |
| Petty Officer to Officer, duty 1 | United We Stand (Limsa Lominsa) | United We Stand (Gridania) | United We Stand (Ul'dah) |
| Petty Officer to Officer, duty 2 | Patrol, Interrupted | Cure for the Common Pox | Mess with the Goat, Get the Horns |

These names are announced duties, not evidence that an officer script received
or completed them.

## Remaining boundary and consumer promotion

The unresolved approval producer is the caller or native/server event that
supplies officer arguments, especially `a3`, and then chooses whether to call
`eventDoRankUp` or `eventRankUpDone`. No retained client script binds that
producer to an opcode or packet. The exact local approval remains
`macro_result == 1 and a3 == true`; seals and company are only macro inputs.

Static `gcRank` values, reward-sheet rows, and enlistment notices remain
separate from a seal debit or balance. The reward sheet records literal rows,
including 250, 700, and 1000 count-shaped values, but does not prove a grant:
`xivl-client-data:docs/grand-company-reward-rows.md:1-25`.

### Consumer promotion

- `xivl-client-scripts:docs/gc-promotion-client-contract.md`: promote the
  exact officer macro condition and getter/display consumers; hold the
  approval producer, packet binding, debit, and availability as unresolved.
- `xivl-client-scripts:docs/job-grand-company-event-contracts.md`: promote
  the separate `Com0*7` and `Com0*2` presentation paths; hold membership and
  seal transactions as unresolved.
- `xivl-client-data:docs/gc-rank.md`: promote all 22 static rows and their
  positional name variants; hold company-to-name mapping and server rank
  rules as unresolved.
- `xivl-client-data:docs/grand-company-enlistment-notices.md`: promote the
  three paired notice rows; hold offer availability, eligibility, membership,
  and transaction state as unresolved.
- `xivl-client-data:docs/grand-company-reward-rows.md`: promote literal seal
  item and count-shaped rows; hold historical grants and acceptance conditions
  as unresolved.
- `xivl-client-data:docs/grand-company-journal-text.md`: promote localized
  campaign text and item lookups; hold server objectives, active state, and
  interaction effects as unresolved.
- `xivl-captures:sources/lodestone-manual/objects/pages/grand-company-guide.md:71-105`:
  promote the B-grade announced costs, named prerequisites, and commission
  duties as documented intent; hold runtime debit, availability, and
  completion as unresolved.
