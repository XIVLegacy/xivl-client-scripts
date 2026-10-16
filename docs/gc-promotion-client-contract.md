# Grand Company promotion client contract

`PopulaceCompanyOfficer` exposes a promotion choice, separate rank-up
presentation, and a completion presentation. The choice returns a local
selection. It does not change rank or debit seals. The server-side trigger,
approval producer, and event-to-packet binding remain unresolved.

The static rank rows and positional names are exported in
`xivl-client-data:derived/gc_rank.csv`; its field contract is
`xivl-client-data:docs/gc-rank.md`. The officer and status widget supply the
specific consumers below. The wider company event paths are documented in
[Job and Grand Company event contracts](job-grand-company-event-contracts.md).

## Officer methods and dialogue

`initForEvent` loads text sheet `6797`, `populaceCompanyOfficer`, declares
`work.townNumber` and `work.companyRank` as `integer8`, and initializes
`companyRank` to literal `33`. Actor classes `1500199`, `1500200`, and
`1500198` set `townNumber` to `1`, `2`, and `3`, respectively. This rank is
the officer's salute input, not the player's current rank.
Source: `lua/scripts/chara/npc/populace/populacecompanyofficer.lua:11-69`.

The following row groups follow that actor-class order. They are text-sheet
row IDs, not globally unique message IDs.

| Method | Dialogue rows for the three officer classes | Local behavior |
| --- | --- | --- |
| `eventTalkJoined(a1,a2,a3,a4)` | `27 / 28 / 29` | Starts a talk turn, salutes with officer work values, then presents macro `66` with `a4` as an input |
| `eventInformationRankUp(a1,a2)` | `45,46,48 / 49,50,52 / 53,54,56` | Says the first row with `a2,a1`, then the remaining rows |
| `eventRankUpChoice(a1,a2,a3)` | prompt `30 / 31 / 32`; refusal `39 / 40 / 41`; other answer `42 / 43 / 44` | Presents macro `70` using `a1`, current seals and belonging company |
| `eventDoRankUp(a1,a2)` | `33,34 / 35,36 / 37,38` | Presents `a2`, rank-up scheduler, join effect and status UI |
| `eventRankUpDone(a1,a2)` | No dialogue row | Sets displayed join status to `a1`, displayed points to `a2`, plays the player salute and closes the status UI |

`eventTalkJoined` treats menu result `1` as `eventRankUpChoice(a1,a2,a3)`.
It returns `1` only when that helper returns boolean `true`. Result `2`
runs the information helper and repeats the menu. Other results return `0`.
The choice helper accepts only macro result `1` together with `a3 == true`.
Otherwise it speaks its refusal or other-answer row and returns `false`.
The value `a2` is not read by this helper. Neither the helper nor the caller
computes the approval flag from rank, seals, or quests.

The menu call is exactly
`askMultipleTextMacro(officer,officer,3,66,3,0,a4,true,true)`.
The choice call is
`askMultipleTextMacro(officer,officer,2,70,2,1,true,true,0,a1,seals,company,0,0)`.
The company comes from `player._getBelongGrandCompany()` and seals from
`player.getGrandCompanySealCount(company)`.

Canonical lines: `populacecompanyofficer.lua:348-619,622-771`.
Bytecode: `eventTalkJoined` prototype `0.6`, menu CALL PC `54` at `0xE68`,
choice CALL PC `62` at `0xE88`; `eventRankUpChoice` prototype `0.8`, seal
CALL PC `44` at `0x1301`, choice CALL PC `61` at `0x1345`, true RETURN PC
`67` at `0x135D`, false RETURN PC `87` at `0x13AD`.

`eventDoRankUp` uses scheduler `84090880`, `84094976`, or `84099072`
for the respective officer classes. It opens the join effect with
`(work.townNumber,a2)`, waits `4.7`, opens the company status widget with
`work.townNumber`, sets displayed join status to `a1`, then waits `2.7`.
`eventRankUpDone` sets displayed points to `a2`, waits `2`, runs and waits
for the player scheduler, finishes the talk turn and closes the widget.
These methods do not call one another.
Bytecode: prototypes `0.9` and `0.10`, effect/status CALL PCs `55,63,67`
at `0x160A,0x162A,0x163A`, and completion status/point/close CALL PCs
`25,29,43` at `0x1897,0x18A7,0x18DF`.

## Player state and sheet consumers

`PlayerBaseClass.getGrandCompanyRank(company)` calls native
`_getGrandCompanyRank(company)`. Raw `127` returns `(0,true)`; raw values
at most `0` or greater than `100` return `(0,false)`; other values return
`(raw,false)`. This is a native getter result, not a Lua `playerWork`
field established here.

`getGrandCompanySealCount(company)` selects catalog `1000201`, `1000202`,
or `1000203` for company `1`, `2`, or `3`. It scans player package `100`,
matches the catalog ID and returns that item's `_countStack()`. It returns
`0` if no matching stack is found. Source: `playerbaseclass.lua:264-385,2857-2914`.
Bytecode: rank prototype `0.12`, native CALL PC `2` at `0x13BF`;
seal-count prototype `0.70`, item CALL PC `43` at `0x60D3` and stack
TAILCALL PC `45` at `0x60DB`.

Columns are zero-based sheet positions after the CSV row ID.

| `gcRank` position | Proven consumer meaning | Bytecode locator |
| --- | --- | --- |
| `0` | `getGrandCompanyRankLinear` result for the native rank row, after its sentinel checks | Player prototype `0.13`, CALL PC `25`, `0x14C8` |
| `1` | `getGrandCompanySealMax` result for the native rank row; status UI point maximum | Player prototype `0.14`, column LOADK PC `11`, `0x159D`; CALL PC `12`, `0x15A1` |
| `2` | `getGrandCompanyNeedSealNextRank` result for the native rank row | Player prototype `0.15`, column LOADK PC `11`, `0x165C`; CALL PC `12`, `0x1660` |
| `6,7,8` | Status icon for company `1,2,3`, at the supplied rank row | Status prototype `0.8`, column arithmetic PCs `8-9`, `0x10CA-0x10CE`; CALL PC `10`, `0x10D2` |

Sources: `lua/scripts/chara/player/playerbaseclass.lua:304-385` and
`lua/scripts/widget/grandcompanystatuswidget.lua:204-403,492-510,616-737`.
The status widget sends `8079 + company` with rank and gender to the rank
name text renderer. This establishes company-dependent text macro selection,
but does not directly join company IDs to the three `xtx/gcRank` text
positions. The export's name variants must remain positional until that
renderer join is established. The getter names also do not prove an actual
promotion debit or the server's availability and admission rules.

## Unresolved event boundary

No retained caller here binds a packet or server event ID to these officer
methods, identifies the producer of their method arguments, or proves their
historical invocation. The native rank getter's storage and network update
route are outside this contract. No server rank mutation, seal debit,
promotion requirement, or promotion ladder availability follows from these
presentation methods or static rows.

## Source identity and locators

Extraction: `2012.09.19.0001`, retail 1.23b. Each named decoded Lua member
was checked against its `relativePath` entry in
[`manifests/scripts.json`](../manifests/scripts.json), including size,
SHA-256 and line count. Its installed original LPB and decoded payload were
checked against the `decodedScriptPath` entry and `matched-script`
classification in [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
The coverage entry owns the full LPB path, size and SHA-256.

Instruction locators use the original decoded Lua 5.1 chunk. `0` is the root
prototype, child indices and PCs are zero-based, and offsets are byte offsets
in that chunk. Lua line locators refer to the authenticated canonical member.
Decoded payload SHA-256 values pin the instruction offsets below.

| Decoded member below `lua/scripts/` | Decoded payload SHA-256 |
| --- | --- |
| `chara/npc/populace/populacecompanyofficer.lua` | `ba827b063fd9747cbab293e97d07ccf039768299342e3891abafbdaff0837e95` |
| `chara/player/playerbaseclass.lua` | `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a` |
| `widget/grandcompanystatuswidget.lua` | `c28038e3c596621b0e87d7a9fd5d2857274a836fedaabd6a83ffaf4729e5b070` |
