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
The original-LPB verification below establishes the selected callback control
flow independently of the decompiler. Canonical source line locators remain
useful for presentation and text joins.

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
The row-24 confirmation follows at lines 711-721. The original bytecode
[establishes its return, exit and retry branches](#runner-menu-and-callback-values).
These client returns do not establish a server exchange protocol.
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

## Original LPB bytecode verification

The original Spl0i2 and PopulaceHalloweenTrans LPBs match the exact resource
records in [manifests/retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
The coverage manifest has SHA-256
`46fd1b388a883c0f70fc8a0bae27d08e05a1bfd776ffcac094a6b1ddd4b9d9f4`.
Both decoded Lua 5.1 chunks parse to exact EOF. Method names are joined to
prototypes by root CLOSURE/SETTABLE instructions. This verifies the contracts
below independently of the canonical decompiler's control-flow rendering.

| Class and original LPB resource | LPB SHA-256 | Decoded payload SHA-256 / bytes |
| --- | --- | --- |
| Spl0i2: tp5rq/r75w9s1v/ruy/ruyj1h.le.lpb | b30852b309ecb1f954dd220b7549ca5c22ec46f7091b3343e1e60d92a7c2caaa | 060506b25c19a40d7c6e194f9c875bf89480296f21992f25645632bc429d8eb8 / 6827 |
| PopulaceHalloweenTrans: 729s9/wu7/uvupy975/uvupy97529yyvn55wqs9wr.le.lpb | 1fee30134a635e42ca12a167c93ceeab70f64147de342d10047f3e8998b9cfbf | 900f1a43967f7afe3269847f5d395d06050a485663d8264719e48afbc006b95d / 1613 |

Prototype child indices and instruction PCs start at zero. Offsets below count
bytes from the decoded payload's first byte, including its 12-byte header.
`tools/retail_script.py:decode_lpb` decodes the wrapper, and
`tools/build_quest_contracts.py:ChunkReader` and `instruction` parse the chunk.
CALL B includes the argument span plus one; C includes the retained result count
plus one. RETURN B includes the returned value count plus one. P0-P6 below are
fixed positional parameters, with P0 the method receiver. Actor types and the
server's invocation arguments are not recovered from those positions.

A bounded Python instruction-path evaluator replaced external calls with
explicit synthetic results and checked 80 menu, retry, start, response and
answer paths. It ran no Lua VM or client code. This checks static branch
interpretation, not runtime widget behavior. The parser and wrapper decoder
were inspected at repository revision
`dce3ed215383eafda4d1cb77de8b4542c7a22833`.

### Runner menu and callback values

Spl0i2 root/proto4 is processEventSUMFES001, bound by root SETTABLE PC21,
offset 0x74. Its body begins at offset 0xd23 and has five fixed parameters.
The method calls P2:startCliantTalkTurn(2,P1). P4 selects dialogue variant 0/1/2. The
comparison of P3 with zero at PCs4-6 has two edges to the same continuation and
causes no change in this chunk.

| Operation | Bytecode contract | Prototype PC / decoded offset |
| --- | --- | --- |
| Main menu | P2:askExtendWidget(P0,18,3,1,1), one result in R5 | proto4 PC50 / 0xdeb, CALL A5/B7/C2 |
| Reward selector | desktopWidget:askEventModeWidgetYield(Ask/RewardSelectWidget,1,P0,19,R6,8013301,8013302,8013303,8013304), two results in R7/R8 | proto4 PC70 / 0xe3b, CALL A7/B11/C3 |
| Remembered selection | Copy second result R8 into R6; first result R7 is unused | proto4 PC71 / 0xe3f |
| Confirmation | P2:askExtendWidget(P0,24,2,1,1), one result in R9 | proto4 PC191 / 0x101f, CALL A9/B7/C2 |
| Confirmed selection | If R9 equals 1, add 10 to R8 and return it as one value | proto4 PCs192/194/260 / 0x1023/0x102b/0x1133, RETURN A8/B2 |

The `1` following `Ask/RewardSelectWidget` is the requested widget result
count, not a widget mode. The Lua CALL retains two return values; this method
uses the second and leaves the first unused. The
[yielded-tuple contract](materia-meld-client-contract.md) describes the shared
helper's completion prefix separately from the widget's requested result.
The actual reward widget's result domain is outside this finding.

Selector result 1/2/3/4 presents row-23 prize/cookie/count arguments
8013301/3010417/3, 8013302/3010417/10, 8013303/3010417/50 and
8013304/3010417/99, respectively. The four say calls are proto4
PC151/162/173/184, offsets 0xf7f/0xfab/0xfd7/0x1003, CALL B7/C1.
With confirmation result 1, the corresponding static callback returns are
therefore exactly 11/12/13/14. These are verified client returns, not a proven
server exchange protocol. These confirmed paths do not call finishCliantTalkTurn
before returning.

The complete menu and list control flow distinguishes exits from retries:

| Input result | Effect in this method | Exact locator |
| --- | --- | --- |
| Main menu 1 | Open reward list | proto4 EQ PC51 / 0xdef |
| Main menu 2 | Present objective text, return to main menu | proto4 EQ PC263 / 0x113f; loop target PC44 / 0xdd3 |
| Main menu 3 | Finish talk, return one value 3 | proto4 finish PC354 / 0x12ab; RETURN PC355 / 0x12af A5/B2 |
| Main menu -3 | Finish talk, return one value -3 | proto4 finish PC360 / 0x12c3; RETURN PC361 / 0x12c7 A5/B2 |
| Other main-menu result | Reopen main menu | proto4 EQ/JMP PCs357-358 / 0x12b7-0x12bb |
| Reward result -1 | Normalize to 8, finish talk, return one value 8 | proto4 PCs72-74 / 0xe43-0xe4b; finish PC106 / 0xecb; RETURN PC260 / 0x1133 |
| Reward result 8 | Finish talk, return one value 8 | proto4 EQ PC75 / 0xe4f; finish PC106 / 0xecb; RETURN PC260 / 0x1133 |
| Reward result -3 | Finish talk, normalize to 8, return one value 8 | proto4 EQ PC108 / 0xed3; finish PC139 / 0xf4f; LOADK PC140 / 0xf53; RETURN PC260 / 0x1133 |
| Confirmation -3 or any result other than 1 | Set internal sentinel 199, reopen reward list with previous result retained in R6 | proto4 PC226 / 0x10ab or PC256 / 0x1123; EQ PC257 / 0x1127; JMP PC259 / 0x112f to PC59 / 0xe0f |

Sentinel 199 is not returned on those retry paths. Runtime meanings and the
complete result domains of the native widgets remain unknown. There is no
explicit 1-4 range guard before confirmation: an otherwise unrecognized list
value can reach confirmation without a price message. The bytecode does not
prove that the actual widget produces such a value or a server accepts it.

### Start and response methods

The root binds the public start methods processEventHWLStart,
processEventHWGStart and processEventHWUStart to proto1/2/3 at PCs12/15/18,
offsets 0x50/0x5c/0x68. Each has four fixed parameters and starts P2 talk with
(2,P1). Each captures one result from P0:showQuestInfomation(), tests it against
1 to select dialogue, finishes P2 talk and returns the original result as one
value. P3 is unused.

| Method | showQuestInfomation CALL B2/C2 | finish call | RETURN A4/B2 |
| --- | --- | --- | --- |
| HWLStart / proto1 | PC49 / 0x347 | PC116 / 0x453 | PC117 / 0x457 |
| HWGStart / proto2 | PC54 / 0x6b5 | PC131 / 0x7e9 | PC132 / 0x7ed |
| HWUStart / proto3 | PC49 / 0xa5b | PC124 / 0xb87 | PC125 / 0xb8b |

The response methods have four fixed parameters. P3 values 0/1/2 select the
following text rows. Other P3 values produce no selected response text. All
finish P2 talk and return zero values, rather than a numeric completion result.

| Method / prototype | P3=0/1/2 text rows and CALL locators | finish / zero-value RETURN |
| --- | --- | --- |
| SUMFES002 / proto5 | 29/62/92 at PCs10/22/34, offsets 0x157e/0x15ae/0x15de | PC38 / 0x15ee; PC39 / 0x15f2, RETURN B1 |
| SUMFES003 / proto6 | 28/61/91 at PCs10/22/34, offsets 0x16c9/0x16f9/0x1729 | PC38 / 0x1739; PC39 / 0x173d, RETURN B1 |
| SUMFES004 / proto7 | 27/68/90 at PCs13/22/31, offsets 0x1829/0x184d/0x1871 | PC35 / 0x1881; PC36 / 0x1885, RETURN B1 |
| SUMFES005 / proto8 | 34/69/97 at PCs14/26/38, offsets 0x1977/0x19a7/0x19d7 | PC42 / 0x19e7; PC43 / 0x19eb, RETURN B1 |

SUMFES004 first runs scheduler 354107392 at proto7 PC2 / 0x17fd and calls
P0:_wait(2.5) at PC5 / 0x1809. SUMFES005 first starts P2 talk with (2,P1)
at proto8 PC3 / 0x194b. These calls do not debit cookies, grant rewards,
validate eligibility or mutate a server quest.

### Imp question arguments and answer returns

PopulaceHalloweenTrans.firstTalkAskEvent is root/proto3, bound by root SETTABLE
PC18 / 0x68. Its body begins at 0x355 and has seven fixed parameters.
P1 is unused. PCs0-4 / 0x355-0x365 create the ordered choice table
{P3,P4,P5}. It calls desktopWidget:askForEventMode(P0,P0,P0,1,false,false,P2,
that_table) at PC15 / 0x391, CALL A9/B10/C2. One result is retained in R9
and moved to R7 at PC16 / 0x395.

EQ PC17 / 0x399 compares R7 directly with P6. A mismatch jumps to PC43 /
0x401; equality enters PC19 / 0x3a1. The two branches are:

| Comparison | Presentation | Return |
| --- | --- | --- |
| Equal to P6 | Rows13/14/15/16; row15 receives 0,9 at PC34 / 0x3dd, CALL A9/B6/C1 | LOADK zero PC40 / 0x3f5, RETURN PC41 / 0x3f9 A9/B2: one value 0 |
| Not equal to P6 | Rows17/18/19; row18 receives 0,5 at PC53 / 0x429, CALL A9/B6/C1 | LOADK one PC59 / 0x441, RETURN PC60 / 0x445 A9/B2: one value 1 |

The non-equal branch has no separate cancellation case. This verifies the
nine-versus-five presentation and zero-versus-one client return, including the
wrong-answer consolation path. It establishes neither actual cookie grants nor
server-side answer validation. The caller's expected-answer producer remains
unknown. getSweets is proto6, a sole zero-value RETURN A0/B1 at PC0 / 0x5f9,
and supplies no basket collection contract.

NPC bindings, seasonal dates and population, actual grants and basket quantity,
sharing and expiry remain outside this static contract.

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
