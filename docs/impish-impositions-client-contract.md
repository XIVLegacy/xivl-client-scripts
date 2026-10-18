# Impish Impositions client contract

Impish Impositions is quest 110800, class `/Quest/Scenario/Spl/Spl0i2`.
The client preserves Limsa dialogue, pumpkinhead exchange presentation and
an imp question/answer callback. It does not preserve the corresponding
server settlement or seasonal population policy.

## Artifact identity

These are canonical decoded Lua members from extraction `2012.09.19.0001`,
game version 1.23b. Their bytes matched [manifests/scripts.json](../manifests/scripts.json),
SHA-256 `86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`.
[lua/registry.json](../lua/registry.json) supplies decoded/ciphered joins.
Method locators below refer to this canonical decompile, whose text hashes
differ from the independent decompile in
[Seasonal quest client contracts](seasonal-quest-client-contracts.md).
Decompiled control flow is not an independently verified bytecode result.

| Decoded member under `lua/scripts/` | SHA-256 |
| --- | --- |
| `quest/scenario/spl/spl0i2.lua` | `afcde8d49165281d75e8e4e20164ae41ceacab78c14ae55fa467983e8004097d` |
| `chara/npc/populace/populacehalloweentrans.lua` | `67846b7c23581c39968792679806f12c43a34cb32161d2dc9f8aed0aa7d62bdf` |
| `director/halloweendirector.lua` | `1ee351e9b6b69ec9fc4aa0a4fdc99619896da4ce91d7d386bfc5d9b9455ef14a` |

The title/class and text/item joins use `xivl-client-data` revision
`9ca24cf5aecd33c4f2753c0d75887ac6e96516cc`:
`manifests/staticactor_class_paths.json`, record 110800, and the CSV members
identified by `manifests/tables.json`, SHA-256
`239cb63fb00de5f434b92924696c043cb80ddcd9abc7f334075afb6b28d5626d`.
Selected members were read with Python `csv` from the manifest-pinned decoded
archive, whose SHA-256 is
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
CSV column numbers below are sheet columns after the row ID, starting at zero.

## Limsa runner and exchange presentation

`xivl-client-data:csv/xtx_quest.csv`, row 110800 column 2, supplies the title.
`Spl0i2.processEventHWLStart`, lines 24-172, presents Limsa dialogue,
calls `showQuestInfomation` and returns its result after finishing the talk.
Text set `spl0i2`, row 16, explicitly names Limsa. This does not establish
the calling NPC, server acceptance or a quest-state mutation.

`processEventSUMFES001`, lines 507-911, presents a menu followed by
`Ask/RewardSelectWidget`. Lines 579-591 supply four item IDs. Row-23
`worldMaster:say` arguments at lines 669-710 pair each with Pumpkin Cookie
3010417 and these displayed counts:

| Item ID | English name | Displayed cookie count |
| --- | --- | ---: |
| 8013301 | Pumpkin Head | 3 |
| 8013302 | Unripened Pumpkin Head | 10 |
| 8013303 | White Pumpkin Head | 50 |
| 8013304 | Ripened Pumpkin Head | 99 |

Names join through `xivl-client-data:csv/xtx_itemName.csv`, column 5.
The row-24 confirmation follows at lines 711-721. Decompiled branches test
selected indices 1-4 and add 10 after confirmation. Values 11-14 are therefore
candidate callback results, not a proven server exchange protocol. Cancel,
exit and loop structure also remains a decompile interpretation.
`processEventSUMFES002/003/004/005` presents insufficient-cookie,
success/first-success and duplicate-prize text. None of those calls debits
cookies, grants prizes, proves entitlement rules or completes a server quest.

`xivl-client-data:csv/xtx_journalxtxRoc.csv`, rows 10-11, describes continued
exchanges after objective completion. Japanese, German and French columns
0/2/3 state 19:00-05:00 Eorzea time for imp appearance. English column 1
says nighttime. This is shipped availability text, not a recovered scheduler
or exact boundary comparison.

## Imp question and consolation presentation

`PopulaceHalloweenTrans.initForEvent`, lines 11-24, selects text set 7696,
`populaceHalloweenTrans`. Its `firstTalkAskEvent`, lines 67-144, takes a
caller-supplied question A2, three choices A3-A5 and expected answer A6.
It compares the widget result to A6. The matching branch passes nine to
text row 15 and returns zero. The other branch passes five to row 18,
which describes a consolation prize, and returns one. Text rows 13-19
distinguish correct and wrong answers.

Those literals establish the recovered presentation and return branches.
They do not establish server answer validation, actual cookie grants, the
question producer or basket creation. The same class presents busy text
rows 20-21 and inventory-full text rows 22-23. `getSweets`, lines 184-188,
is empty and supplies no collection contract. `HalloweenDirector` contains
only its require/class declaration, with no recovered event lifecycle.

## Actor and server boundary

`xivl-client-data:csv/actorclass.csv`, row 1001789 column 5, joins display-name
1300189, Ursielle, in `xtx_displayName.csv` column 1. Basket actor class
1200254 similarly joins display-name 4010012, treat basket. These identities
do not provide city placement or script binding. The staticactor catalog
contains script actors and does not supply these NPC class bindings.

The client artifacts above do not establish the event's calendar, imp spawn
locations, disguise-to-imp binding, question selection, basket quantity,
per-player sharing or expiry. Actual grants and first-trade completion also
remain server-owned unknowns. Decoration weather and population are distinct
controls; the recovered quest methods do not activate a city decoration set.
