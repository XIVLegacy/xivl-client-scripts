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

The decompiled `NpcBaseClass.delegateEvent` and
`DirectorBaseClass.delegateEvent` bodies pass the method name, player, self,
and first trailing value to `questActor:_callFunction`. They materialize
`...` into one local before the call. This establishes forwarding of the
text ID; forwarding of later supplied arguments needs bytecode confirmation.
`NpcBaseClass.say` passes the quest actor and text ID to
`DesktopWidget.showMessage`, which forwards them to `_appendMessagePool`.
None of these methods selects a `passiveGL_craft` source column.

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

### Lua and text-control coverage

A literal-name search across the authenticated 2,671-script corpus finds
`passiveGL_craft` only in `AreaBaseClass` sheet preparation:
`lua/scripts/area/areabaseclass_layout.lua:30-33`, SHA-256
`AB17A0177B7F7777887997A5DEC3CD29A56C4F7D4CA32AE27743F65821B27ADD`
(`manifests/scripts.json:33-36`). Preparation does not read a field.

The decoded CSV controls also reference the sheet without a Lua `_getData`
call. Searching the complete CSV corpus for the hex encoding of the literal
`passiveGL_craft` finds these rows:

| Source | Rows |
|---|---|
| `xivl-client-data:csv/xtx__text_ui.csv` | 4225-4231 |
| `xivl-client-data:csv/xtx__text_ui(2).csv` | 4225-4231 |
| `xivl-client-data:csv/worldMaster.csv` | 64050-64057 |

The source identities are pinned in `xivl-client-data:manifests/tables.json`.
Reading each matching control's column expression, including all four arms
of its nested switch, yields columns
`0,1,2,6,7,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43`.
None selects columns 8-11. This is a bounded observation about literal sheet
references in the decoded CSV corpus, not an absence claim about computed
native references or other client resources.

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

These adapters establish the bank identity, parameter decoding, and supplied
text route. They do not reveal a caller selecting source columns 8-11.

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
the terminal completion marker and counts. This result identifies no native
sheet accessor. It excludes neither undefined strings nor computed, indirect,
dynamic, or unanalyzed references.

Producing tool SHA-256 pins in `xivl-client-structs`:

| Tool | SHA-256 |
|---|---|
| `ghidra/VerifyProgramFileBytes.java` | `0277d0f837006579432673172d827a9340b74a55b15fb1c15137cebf320e64bb` |
| `ghidra/FindReferences.java` | `6c33f04980b6ebae1e577857c94afd99c90176e31a2f190573351bb1e3afee6b` |
| `tools/verify_reference_export.py` | `5084624101d82baf8e24f9e21bee7c0eb014ac18e768d38f3f9a920c77bd7f49` |

## Unresolved evidence

Columns 8-11 remain `unk1`-`unk4` in
`xivl-client-data:tools/mappings/passivegl_craft.py`. The first missing edge
is a concrete read of one of these source positions that supplies the
`processPgEvent` text ID. The `pgConv` bank, explicit event arguments, and
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
