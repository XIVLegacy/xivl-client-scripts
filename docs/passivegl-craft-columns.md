# Local guildleve titles and passiveGL_craft columns

Local guildleve journal titles come from `xtx/quest`, keyed by the local
guildleve ID. The title route does not read `passiveGL_craft` columns 8-11.
Those four column meanings and their consumers remain unresolved.

This finding describes static client Lua and text controls from extraction
`2012.09.19.0001`. It does not establish server availability, difficulty
selection, or runtime text evaluation.

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

| Source column | Current mapping field | Consumer function | Indexed sheet | Meaning | Confidence |
|---:|---|---|---|---|---|
| 8 | `unk1` | Unresolved | Unresolved | Unresolved | Unverified |
| 9 | `unk2` | Unresolved | Unresolved | Unresolved | Unverified |
| 10 | `unk3` | Unresolved | Unresolved | Unresolved | Unverified |
| 11 | `unk4` | Unresolved | Unresolved | Unresolved | Unverified |

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
is a concrete read of one of these source positions and its downstream
consumer. No recovered Lua or literal text-control route above establishes
the sheet indexed by their small integer values. Naming them as text IDs or
difficulty variants would exceed this evidence.

Resolving each column requires a native, script, or other identified client
resource locator that reads that exact column, then follows the returned
value into a named sheet or presentation operation. Establishing a relation
to selector values 1-4 additionally requires the selection edge between that
consumer and the corresponding column. Similar value ranges or the card
slot order do not provide those edges. Local display names are resolved
independently by the journal title route above.
