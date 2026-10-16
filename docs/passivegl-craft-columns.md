# Local guildleve titles and passiveGL_craft columns

Local guildleve journal titles come from `xtx/quest`, keyed by the local
guildleve ID. The title route does not read `passiveGL_craft` columns 8-11.
Columns 8-11 match `pgConv` dialogue IDs across all 169 rows. Retained retail
calls corroborate three values for leve 120202, but the source-column selector
and uniform per-column meanings remain unresolved.

This finding combines client Lua, data and native instructions from build
`2012.09.19.0001` with retained retail event calls. It does not establish
server availability or difficulty selection.

## Local title route

In the type-2 branch of `JournalDetailWidget.setDetailData`, the widget calls
`setText("TextBlock_Title",4219,work.journalID)` at
`lua/scripts/widget/ask/journaldetailwidget.lua:1364-1370`. The branch starts
at lines 1294-1300. UI text row 4219 contains these exact controls:

| Locale | `xtx__text_ui.csv` field | Control |
|---|---:|---|
| Japanese | 0 | `[@sheet:02280fff0a7874782f7175657374e8020203]` |
| English | 1 | `[@sheet:02280fff0a7874782f7175657374e8020303]` |

Each control carries the string `xtx/quest`, row expression `e8 02`, and a
column expression: `02` for Japanese field 1 or `03` for English field 2.
The supplied journal ID is the sole formatting argument. Compact integer
expressions encode their value plus one. This supports the same-ID join to
`xtx_quest.csv` fields 1 and 2. For example, local guildleve 120005 has English
title `Baderon's New Sword` in field 2, and 120001 has `The Collector`.

The journal list uses the same title controls. In
`JournalListWidget.addPassiveGuildleveList`, `getQuestId()` supplies the ID
at lines 1067-1069, and `setListItem` receives type 2, that ID, and text key
5001 at lines 1085-1093. `setListItem` forwards its text key and journal ID
to the `Name` property through `setListText` at lines 1313-1322. UI row 5001
has the same Japanese and English control bytes as row 4219.

Script identities, verified against [the script manifest](../manifests/scripts.json):

| Script | SHA-256 | Manifest locator |
|---|---|---|
| `widget/ask/journaldetailwidget.lua` | `21B9F1B4900BBD3BD9826F852F6DD82BEAB914951A053CBC5A003ADA2B38B32D` | `scripts.json:15003-15006` |
| `widget/ask/journallistwidget.lua` | `C103432E8671EE20493B4060D5D0958F608C967F211C2F73BEE8AEC6AF96DE87` | `scripts.json:15009-15012` |

Text evidence: `xivl-client-data:csv/xtx__text_ui.csv` rows 4219 and 5001,
physical lines 1629 and 1685, SHA-256
`23762A422118D99C4144A48B3495C52511B1B1B865E4FC50FDC61A973E3C6ECE`;
`xivl-client-data:csv/xtx_quest.csv` rows 120001 and 120005, fields 1 and 2,
SHA-256 `938640466B314242916F1F8877A90154C4F4DB7AA63DE6223E6AF4AA194E6719`.
Expression decoding uses `xivl-tools:src/formats/src/richstring.rs`,
`parse_expression` and `decode_integer`, and its
`docs/formats/ssd-sheet.md` rich-string grammar at revision
`75fe7414bf3f1ecd779825083d477adc4ed5f319`. That grammar preserves expressions;
it does not execute the native text renderer.

The reproducible title product is
`xivl-client-data:derived/local_guildleve_names.csv`. Its builder,
`tools/build_local_guildleve_names.py`, joins every `passiveGL_craft` row ID
to `xtx_quest`, preserving English and Japanese text verbatim. All 169 driver
rows match, including test and dummy rows. Source hashes, title controls,
column mappings, and product identity are pinned by
`xivl-client-data:manifests/local_guildleve_names.json`.

## Columns 8-11

The sheet identity is `passiveGL_craft`, resource `0x01030068`
(`xivl-client-data:manifests/sheet_inventory.csv:512`). Positions below are
zero-based source CSV header indices, not output SQL positions.

| Source column | Current mapping field | Observed value at row 120202 | Candidate sheet | Meaning | Confidence |
|---:|---|---|---|---|---|
| 8 | `unk1` | 365, also sent to `processPgEvent` | `pgConv` | Dialogue reference candidate | Corroborated value; source read unverified |
| 9 | `unk2` | 366, also sent to `processPgEvent` | `pgConv` | Dialogue reference candidate | Corroborated value; source read unverified |
| 10 | `unk3` | 367, absent from the three captured calls | `pgConv` | Dialogue reference candidate | Data correspondence; source read unverified |
| 11 | `unk4` | 368, also sent to `processPgEvent` | `pgConv` | Dialogue reference candidate | Corroborated value; source read unverified |

### Dialogue bank and column order

All 676 cells in source columns 8-11 join to `pgConv` rows. They contain
120 distinct IDs in 31 ordered four-value tuples. The input identities are
`xivl-client-data:csv/passiveGL_craft.csv`, 26,972 bytes, SHA-256
`2e2b68515f43ba2898bc3c4bf642332bd924687a4d771ba8d8d9733c539cd0ba`,
and `xivl-client-data:csv/pgConv.csv`, 196,131 bytes, SHA-256
`2c1ed71fe8c9344a674b1cd8135081195b8dca78fbeb1adbb4887bf1610f2818`.
Their owning identities are recorded in `xivl-client-data:manifests/tables.json`.
The join reads driver fields 8-11 by the numbered source header, excluding
the row-ID cell, and compares each value to the `pgConv` row-ID column.

The raw `passiveGL_craft` schema declares 33 signed 32-bit fields in 44
logical positions. Logical columns 8-11 occupy physical row offsets
`0x14,0x18,0x1C,0x20`. All 676 cells agree with the raw little-endian values.
The byte pins below identify the source resources used for that check:

| Resource | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| `0x01030068` | Schema and logical column order | 1,833 | `59cf9e402af39d847cf573da54c2994dda6a7264043036b9fd6e34cf9ae9e28d` |
| `0x01030069` | Row data | 22,308 | `638e964229f9681e83941930756ea92e80878352ed812fcf4cca6ef28bc21652` |
| `0x0103006B` | Row offsets, block beginning 120000 | 4,100 | `a57bb6b662d9155a41797c349156297af9971ac36bd540b4820aeb50fed57536` |
| `0x03A20147` | `pgConv` locale schema | 1,664 | `1489106e1efc7f105a9e1b4f78cb519cf2db3f6d23644582751068b3ec81bd32` |

These are the named `data/` resources from the same retail build. Schema
decoding follows `xivl-tools:tools/research/census_sheet_stack.py:109-128`,
`decode_document`, at revision `75fe7414bf3f1ecd779825083d477adc4ed5f319`.
Row offsets follow `xivl-tools:src/formats/src/sheet.rs:117-128,152-187`:
entry `rowId - block.begin` is the unsigned little-endian end offset and
the preceding entry is the start, with zero used for the first row.
The `pgConv` schema maps Japanese to source field 0 and
English to field 1. It supplies no foreign-key declaration for the four
`passiveGL_craft` columns.

Dialogue content contradicts uniform phase names. Leve 120005, recommended
class 30, has tuple `361,362,363,364`; text 364 in source column 11 accepts
finished work. Leve 120035, also class 30, has `105,107,108,106`; text 108
in column 10 accepts finished work, while text 106 in column 11 supplies
materials. The same text can also occupy different columns: leve 120001
uses `185,186,187,188`, while leve 120229 uses `185,187,188,186`.
These are content comparisons, not observations of phase selection.

### Supplied dialogue consumer

`PgConv` inherits `PassiveGuildleveBaseClass` and loads
`_loadTextDataPermanently(327,"pgConv")` in `initText`. The native binding
adds `0x03A20000` to 327, selecting resource `0x03A20147` as described
below. Its inherited `processPgEvent(self,player,npc,textId,scheduler)`
optionally runs the supplied NPC scheduler and calls `npc:say(self,textId,0)`.
The descriptive parameter names here follow positional flow; they do not
rename the generated API manifest.

Raw Lua 5.1 bytecode establishes that both `NpcBaseClass.delegateEvent` and
`DirectorBaseClass.delegateEvent` call
`questActor:_callFunction(method,player,self,...)`, forwarding every trailing
argument. Their decompiled `L10 = ...` assignment understates this behavior.
Both eight-instruction bodies use `VARARG r10,B0`, `TAILCALL r5,B0`, then
`RETURN r5,B0` at PCs 5-7: the open argument extent is preserved.
`NpcBaseClass.say` passes the quest actor and text ID to
`DesktopWidget.showMessage`, which forwards them to `_appendMessagePool`.
None of these methods selects a `passiveGL_craft` source column.

The bytecode locators below use one-based PCs and zero-based decoded chunk
offsets. `main/f27` and `main/f13` identify the NPC and Director delegate
prototypes, with original source lines 4039-4047 and 2163-2171 respectively.

| Adapter | PC 5: `VARARG`, word `0x000002A5` | PC 6: `TAILCALL`, word `0x0000015D` | PC 7: `RETURN`, word `0x0000015E` |
|---|---|---|---|
| NPC | `0x13E3` | `0x13E7` | `0x13EB` |
| Director | `0x0A66` | `0x0A6A` | `0x0A6E` |

`PassiveGuildleveBaseClass.processPgEvent`, prototype `main/f1`, original
lines 1121-1128, has five parameters and eleven instructions. PCs 1-5 test
formal `r4` against nil and, when non-nil, pass it to
`r2:_runCharaScheduler(r4)`. PCs 6-10 call `r2:say(r0,r3,0)`. Thus the first
supplied integer occupies the text-ID position and the next occupies the
scheduler position. This establishes positional use, not scheduler execution
or native `_callFunction` invocation policy.

The raw resources are relative to retail `client/script/`. Their decoded
payload identities are also pinned in
[the resource census](../manifests/retail_lua_coverage.json):

| Resource | Decoded bytes | Decoded SHA-256 |
|---|---:|---|
| `729s9/wu7/wu789r57y9rr.le.lpb` | 5,925 | `1941c40b64cacd721d271b36e31017a24f908b8ea518f713b44da17bb4e57627` |
| `61s57qvs/61s57qvs89r57y9rr.le.lpb` | 3,854 | `b63cd23139dc84b4e3c9d713c01278ee1d83f45a3658ba7587eec66af81ba93b` |
| `tp5rq/u9rr1o53p1y6y5o5/u9rr1o53p1y6y5o589r57y9rr.le.lpb` | 774 | `ac1de2b6208166e8ec616ee9c0a075ab7cfb91e19051e03041e93020bbea1455` |

Decoding uses `xivl-client-structs:tools/decode_lpb.py`; disassembly uses
`unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`,
as pinned by [unluac provenance](../tools/vendor/unluac/PROVENANCE.json).
The raw instruction fields confirm the open argument counts; `VARARG B2`
would retain only the first trailing value.

The canonical Lua locators and SHA-256 identities are:

| Script under `lua/scripts/` | Method and lines | SHA-256 |
|---|---|---|
| `quest/passiveguildleve/craft/pgconv.lua` | Inheritance 1-8; `initText` 11-17 | `47712E4B02BEBFEC652DA19EC6E3CC104D1D347FE8FA6E2BA5E4438A347A7A2C` |
| `quest/passiveguildleve/passiveguildlevebaseclass.lua` | `processPgEvent` 23-37 | `75F0454B943EB6D808C83FFBC269E817A702B2B9A723BF4A64BFD1F2FADDD3F0` |
| `chara/npc/npcbaseclass.lua` | `delegateEvent` 564-574 | `F18C6C3198DB0402431CA6AA683B601AFBF5A0DC5C22481B3C1DA1DEABEF0DC2` |
| `director/directorbaseclass.lua` | `delegateEvent` 249-259 | `45C87F548A82E81681433D6AD89C6DE6FC62F313CEAD66E72BF8B8CF7AA55A82` |
| `chara/npc/npcbaseclass_event.lua` | `say` 247-310 | `5417B1BDF762162CAD240A84715D0FC85958DBE0181B653348A66C02EE4D7C80` |
| `widget/desktopwidget.lua` | `showMessage` 369-382 | `5D3BFABF2E8A55EE2E64F607BDADA5F04046C9528E9E9ACA858E9AD9E232070A` |

### Retained event calls

`xivl-captures:studies/local-guildleve-dialogue/README.md` owns the capture
extraction, typed argument observations, and reproduction procedure.
The source is `local_leve_complete.pcapng`, 358,296 bytes, SHA-256
`4f0793f354140478725bf2c30642a3458a854460f47fb11a7af635c8881d95cd`.
Three server-to-client `0x0130` calls on main connection 0 invoke
`delegateEvent` with actors `0x029B2941` and `0xA0F1D58A`, method
`processPgEvent`, a text ID, a second integer, and two nil values:

| Capture packet | Frame | Subevent | Text ID | Second integer | Matching column of row 120202 |
|---:|---:|---:|---:|---|---:|
| 38 | 14 | 0 | 365 | `0x151A9000` | 8 |
| 79 | 25 | 0 | 366 | `0x04136000` | 9 |
| 1734 | 497 | 0 | 368 | `0x04140000` | 11 |

The native `_getStaticActorID` mask gives
`0xA0F1D58A & 0x000FFFFF = 120202`.
`xivl-client-data:manifests/staticactor_class_paths.json`, ID 120202,
maps that row to `/Quest/PassiveGuildleve/Craft/PgConv`.
The SAN record begins at decoded byte `0x1622C` of
`client/script/rq9q1797qvs.san`, 108,911 bytes, SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`.
Reparsing it with `xivl-client-data:tools/extract_staticactor_san.py`,
`parse_san`, reproduces all 2,812 tracked records.
`passiveGL_craft` row 120202 has tuple `365,366,367,368` and
`deliveryDisplayName` 1300085, Manine. Its title is `A Mother's Frippery`.
The four raw values begin at resource `0x01030069` offsets
`0x242C,0x2430,0x2434,0x2438`; the corresponding `pgConv` texts are rows
365-368, physical CSV lines 367-370.
The same tuple is shared by rows 120201-120208, so text values alone would
not identify this leve.

The capture establishes explicit incoming text IDs for the matching actor.
Together with the script route, it corroborates the dialogue-bank candidate.
It does not record a sheet read, establish why the sender chose a value,
or show source column 10 being used. A captured call is also not proof that
the client displayed or acknowledged its message.

[The producer boundary](passivegl-dialogue-producer.md) traces the surrounding
requests, quest-choice results, and native conversion of callback results
into EventUpdate replies. The sender's text-ID selection remains unresolved.

The card selector is established separately in
[the journal lifecycle finding](guildleve-journal-lifecycle.md#passive-guildleve-card-selection).
`PopulacePassiveGLPublisher.getPassiveGuildleveVariation` returns slot
selectors `1,2,3,4,1,2,3,4`, and `askOfferQuest` passes the result to the
detail opener. Neither method reads these sheet columns. Their script
SHA-256 is
`F4D7AB96F3932E41A9B6AFB6D21EA0270FED945FE1DDA1211807963EC13265F1`,
with source locators `11-59,216-290` and the bytecode qualification retained
in that finding. This selector is not evidence that columns 8-11 represent
difficulty variants.

### Lua accessor coverage

A literal-name search across the authenticated 2,671-script corpus finds
`passiveGL_craft` only in `AreaBaseClass` sheet preparation:
`lua/scripts/area/areabaseclass_layout.lua:30-33`, SHA-256
`AB17A0177B7F7777887997A5DEC3CD29A56C4F7D4CA32AE27743F65821B27ADD`
(`manifests/scripts.json:33-36`). Preparation does not read a field.

`AreaBaseClass.prepareSpreadSheet`, `area/areabaseclass.lua:380-426`, computes
the default actor name `passiveGLCraftSheet` through
`system/string.lua:4-54`. It returns an existing actor or calls
`_createActor(name,"SpreadSheet",name~=nil,sheetName)`.
`gamedata/spreadsheet.lua:4-13` passes that initialization name to
`_setFilename`; `spreadsheet_u.lua:4-21` supplies the native bindings.
Their identities are pinned by `manifests/scripts.json` and
`manifests/retail_lua_coverage.json`. The preparation caller discards its
result. No raw constant names the computed actor alias elsewhere.

The raw named-accessor census covers 16,821 prototypes in all 2,671 pinned LPB
chunks. It finds 296 `SELF` references to `_getData` and three `LOADK`
references. The 296 direct sites agree with the decompiled
corpus across 52 scripts. Of these, 272 use other fixed sheet globals,
21 use callback or helper parameters, two debug sites construct `_zone`,
and one uses `CutScene.work.actorclassSheet`. The parameter-receiver sites
select fields outside 8-11: `PopulaceMonsterGrandma.getDisplayName`,
`AchievementPopupWidget.processSpreadSheetDataAsync`,
`ActionSettingWidget.processSpreadSheetDataAsync`,
`GuildleveHistoryWidget.processSpreadSheetDataAsync`, and the two
`MapNavigationWidget` piece-menu and map-data helpers.

The three name loads occur in
`commanddebugger/commanddebuggerdev.lua:15032,15106,15144`,
raw `main/f5` PCs 6853, 6924, and 6959. They call an indexed `_getData`
method with caller-selected row and column, then format the cell as debug
text. They can inspect arbitrary cells, but identify no dialogue selector.
This accounting resolves literal `_getData` uses, not arbitrary computed
names. The corpus also contains 1,541 register-index table accesses in
73 scripts, many ordinary array accesses, and caller-supplied `loadstring`
at `command/debuginputcommand.lua:121`. Their dynamic inputs and native
callbacks remain outside the named-accessor claim.

The census method parses each decoded Lua 5.1 prototype, resolves constant
operands of `SELF` and name-loading instructions, then inspects their
receiver flow in the corresponding script. Raw and decoded hashes match the
resource census; decompiled hashes match the script manifest. A separate
unluac disassembly agrees with every prototype's opcode sequence in the
17 selected chunks used for delegate, preparation, and callback analysis.

### Text-control coverage

Recursive expression decoding of all 803 CSVs pinned in
`xivl-client-data:manifests/tables.json` finds 58,691 recognized sheet/noun
nodes, using macros `0x28,0x31,0x32,0x33`. Every bank-name operand is literal;
none names `pgConv`. All nested strings and conditional arms are traversed
using the rich-string grammar cited above. No expression or framing failure
remains in this bound. The 154 `passiveGL_craft` nodes occupy 103 cells:

| Source | Rows |
|---|---|
| `xivl-client-data:csv/xtx__text_ui.csv` | 4225-4231 |
| `xivl-client-data:csv/xtx__text_ui(2).csv` | 4225-4231 |
| `xivl-client-data:csv/worldMaster.csv` | 64050-64057 |

Their row operands are formatting argument 1. Column operands are literals or
a switch on formatting argument 2 with four literal arms. Their union is
`0,1,2,6,7,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43`.
No explicit operand or switch arm selects columns 8-11. All 103 cells and
154 selector tokens agree with their raw retail resources after the
documented length-prefix and XOR-73 decoding. The main UI schema is
`0x0B450082`; the separate `(2)` export uses `0x27950007`, named
`xtx/_text_ui` by master `0x27950000`. Matching names do not imply identical
resource bytes.

The schema and master identities for that distinction are:

| Resource | Bytes | SHA-256 |
|---|---:|---|
| `0x0B450082` | 3,099 | `27e50caf3d258e8eed2d9e70bc8355e2ab67f54f2dc8bf54e6cfcdf604e5e492` |
| `0x27950007` | 2,292 | `411007becbf7915ea5938036511d21806dadad0c06d582ac5f2f5907b61f1f6b` |
| `0x27950000` | 293 | `246c4af86271f0d90475c8f73d67aaed5eae0cc6915995624e96aca2f9ba9251` |

This claim covers recognized sheet/noun expressions, not arbitrary runtime
strings, native registration, or switch behavior outside the explicit arms.
Fourteen unnamed macro `0x26` nodes remain in eleven `worldMaster` source-5
cells, including rows 25009 and 50078. Their first operands are parameters;
their behavior is unresolved, and none contains a static sheet name.

For example, `JournalDetailWidget.setDetailData:1460-1468` uses UI key 4230
for `Item_OfficerText`. Its English control is
`[@sheet:02282dff107874782f646973706c61794e616d65ff19022815ff1070617373697665474c5f6372616674e80208030203]`.
The nested `08` expression selects source column 7, the existing
`deliveryDisplayName` mapping. It does not select column 8. Keys 4227, 4229,
and 4231 instead select the later per-variant data blocks. The type-2 Lua
branch forwards its first formal after self as the extra formatting argument
for these keys (`1294-1300,1434-1449,1475-1493`); it does not expose the
four unknown values.

### Native bindings and event decoding

The native observations below use the same pinned `ffxivgame.exe` identified
in the reference check that follows. Addresses are virtual addresses at image
base `0x00400000`. Instruction bytes were read from the PE's file-backed
sections with pefile 2024.8.26 and decoded as x86-32 with Capstone 5.0.7.
The selected instruction bodies agree byte-for-byte with the retail file;
symbol names are descriptive labels, not recovered source names.

| Route | Native locator | Observation |
|---|---|---|
| `_loadTextDataPermanently` registration | `0x0072E387`, `0x0072E439` | Binds implementation `0x006E7500` to name string `0x00FD660C` |
| Text resource selection | `0x006E7558-0x006E7568`, `0x006E7594-0x006E75BA` | Converts argument 0, adds `0x03A20000`, and forwards the result plus argument 1's name to `0x00767230` |
| Generic `_getData` | `0x0070A758`, `0x0070A78E`, `0x0070A7B1`, `0x0070A7DF` | Converts two supplied integers and uses them for nested lookups; these sites contain no fixed column 8-11 selection |
| `_appendMessagePool` adapter | `0x006ECF5B`, `0x006E8440-0x006E8448` | Calls `0x006E8360` and converts argument 3 to the integer retained in EBP for message construction |
| `RunEventFunction` payload | `0x0076C28E`, `0x0076C2DA-0x0076C2DF` | Reads method at application payload `+0x29` and supplies 64 parameter bytes at `+0x49` |
| `_getStaticActorID` registration | `0x00749927`, `0x007499D9` | Binds `0x006F9690` to name string `0x00FD7A88` |
| Static actor key | `0x006F9694-0x006F9697` | Reads argument-block `+0x0C` and applies mask `0x000FFFFF` |

The prepared sheet name also has a native construction and cache path:

| Route | Native locator | Observation |
|---|---|---|
| `_setFilename` binding | `0x00746EA7`, `0x00746F59` | Registers implementation `0x006EB530` with string `0x00FD6D90` |
| Filename request | `0x006EB566-0x006EB58F` | Converts argument 0, stores it at `this+0x60`, calls manager virtual `+0x04` with that name, and stores the result at `this+0xB4` |
| `SpreadSheet` construction | `0x00760EA7-0x00760ED3`, `0x006F67F7` | Factory selects `SpreadSheet`, allocates `0xDC` bytes, calls `0x006F67C0`, and installs vtable `0x00FD7744` |
| Bulk row loading | `0x006F8A03-0x006F8A42` | Loader `0x006F8880` enumerates columns using sheet virtual slots `+0x44`, `+0x40`, and `+0x08` |
| Signed integer loading | `0x006F8B44-0x006F8B52`, `0x0078E320` | Type 6 reads the current column through a row accessor, then inserts the scalar through `0x00745E30` and `0x00727C90` |
| Row/column lookup | `0x0070A7B1`, `0x0070A7DF` | `_getData` uses argument 0 to find the row in `this+0xC4`, then argument 1 to find its column |
| Cached return | `0x0070A806-0x0070A823` | Supplies the column node's storage pointer at `+0x14` and type at `+0x18` to `0x007584B0`; the integer scalar resides at `+0x10` |

The filename reaches a handle request; the manager virtual target and a
successful runtime binding remain unobserved. Generic loading can copy all
available columns, including 8-11. Callback loader `0x00747FB0` likewise
handles requested columns or enumerates all when its column list is empty.
Neither copying those cells nor returning a caller-selected cell identifies
the caller choosing a dialogue ID.

The static-key getter's complete 38-byte range, `0x006F9690-0x006F96B5`,
has SHA-256
`7181a178468add274ff51d4f2839e0644e66a2d0457a9afa585bd9b3f207e349`.
This is a decoded byte range, without an assumed enclosing function boundary.

The typed parameter walker at `0x007906C0` dispatches through the table at
`0x007909E0` using tag plus one. Tags used by the three captured calls are:

| Tag | Handler | Interpretation |
|---:|---|---|
| 0 | `0x00790757` | Integer, four big-endian bytes after the tag |
| 2 | `0x007907A1` | NUL-terminated string |
| 5 | `0x0079081E` | Nil |
| 6 | `0x0079084B` | Actor reference, four big-endian bytes after the tag |
| 15 | `0x007909B6` | End of parameters |

The DWORD reader at `0x00791CF0` skips the tag, reverses the following four
bytes on its default little-endian host path, and advances by five bytes.
Checker vtable `0x01057438`, slot `+0x14`, points to `0x008A2710`, whose
calls at `0x008A2742` and `0x008A2775` wrap the decoded ID and look up its
actor. This anchors tag 6's actor interpretation. The checker bounds its
input to payload `+0x49`, length 64, at `0x0089E361-0x0089E37E`.
In each selected call the text-ID tag is at parameter offset 26 and its
big-endian value begins at offset 27.

The incoming integer also has a native materialization path. Receiver
`0x0089EDB0:0x0089EE70-0x0089EE9A` retains the supplied parameter span;
`0x0089E260` passes it through `0x006E1140` to `0x00896F70`. On its successful
path, calls at `0x00897053` and `0x0089706F` pass the span to decoder
`0x00790AA0`. Its constructor `0x00793190` installs vtable `0x00FE1178`.
The tag-0 callback at slot `+0x08`, `0x00793430`, passes the decoded integer
through `0x00748E00` and `0x00584F70` to `0x00583D90`.
Instructions `0x00583DF6-0x00583DFC` copy that supplied DWORD into typed
storage; `0x00583E06-0x00583E09` set its pointer and type 0. The manager
passes the resulting argument pack and supplied method to `0x00CD0940` at
`0x00897199`. This path preserves an incoming value rather than deriving it
from a sheet column. It does not prove downstream invocation or rendering.

These adapters establish the bank identity, parameter decoding, and supplied
text route. The sender's value selection remains unidentified.

### Native reference boundary

The static native check used Ghidra 12.1.3, read-only, on `ffxivgame.exe`
from build `2012.09.19.0001`: 15,996,808 bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`,
image base `0x00400000`, language `x86:LE:32:default`, compiler spec
`windows`. `xivl-client-structs:ghidra/VerifyProgramFileBytes.java` completed
`program-file-bytes-v1`: retained original and modified file bytes matched
the input; the verified loaded file-backed ranges also matched. Excluded
non-file-backed ranges are outside that authentication.

The exact-string query `passiveGL_craft` through
`xivl-client-structs:tools/ghidra/export-references.ps1` and
`ghidra/FindReferences.java` scanned 28,414 defined strings and completed with
zero matches and zero references. `tools/verify_reference_export.py` accepted
the terminal completion marker and counts. This exact-string result identifies
no native literal sheet reference. It excludes neither undefined strings nor
computed, indirect, dynamic, or unanalyzed references.

A separate completed address query records 20 references across seven targets:
`0x006EB530,0x0070A720,0x006F8880,0x00747FB0,0x00FD7744,0x0071CAC0,0x00CA73F0`.
The filename and getter implementations have registrar references; the two
loaders have vtable references. The eight recorded callers of row helper
`0x0071CAC0` cover availability, row scheduling/removal, loading, and
`_getData`. The four callers of inner helper `0x00CA73F0` comprise `_getData`
and three generic map routines with no established sheet identity. None of
these reviewed paths carries a selected column into a dialogue operation.
The query covers Ghidra-recorded references only. Construction and cache
decompilation used `xivl-client-structs:ghidra/DumpVAs.java`, SHA-256
`01b64442746c9652cdc9ef1387d0367af481d68a484c48f0096538a5ecb5c344`,
read-only without analysis or saving. Thirty-three selected native bodies or
ranges for that path, and fifteen for the incoming argument path, were
authenticated against the pinned PE and completely decoded.

Producing tool SHA-256 pins in `xivl-client-structs`:

| Tool | SHA-256 |
|---|---|
| `ghidra/VerifyProgramFileBytes.java` | `0277d0f837006579432673172d827a9340b74a55b15fb1c15137cebf320e64bb` |
| `ghidra/FindReferences.java` | `6c33f04980b6ebae1e577857c94afd99c90176e31a2f190573351bb1e3afee6b` |
| `tools/verify_reference_export.py` | `5084624101d82baf8e24f9e21bee7c0eb014ac18e768d38f3f9a920c77bd7f49` |

## Unresolved evidence

Columns 8-11 remain `unk1`-`unk4` in
`xivl-client-data:tools/mappings/passivegl_craft.py`. The first missing edge
is a caller that selects one of these source positions and supplies its value
as the `processPgEvent` text ID. Bulk loading can read all four positions
without making that choice. The `pgConv` bank, explicit event arguments, and
value correspondence are established separately; they do not establish
that selection edge. Generic `pgConvTextId1`-`pgConvTextId4` names would
still promote a candidate relationship into a column contract.

Resolving each column requires a native, script, or other identified client
resource locator that reads that exact column, then follows the returned
value into the presentation operation. Phase-specific names must also
explain the differing tuple orders. Establishing a relation to card selector
values 1-4 requires a separate selection edge; neither the card slot order
nor the four-message groups supplies it. The complete Lua resource census
in [retail Lua coverage](retail-lua-coverage.md) provides no identified
missing chunk to recover for this caller. Local display names are resolved
independently by the journal title route above.
