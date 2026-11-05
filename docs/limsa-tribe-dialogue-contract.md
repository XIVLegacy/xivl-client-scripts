# Limsa tribe and dialogue operands

The two [Limsa normal tutorial methods](limsa-normal-tutorial-flow.md#dialogue-argument-and-final-movement-lesson)
transform one `A1:getTribe()` result and pass it as the sole extra operand
for dialogue row 91. Conditional on A1 using `PlayerBaseClass.getTribe`,
the input is its stored `playerWork.tribe` value. For each static tribe
row ID 0-15, the local transformation equals `tribe.csv` column 1.
This establishes a conditional numeric correspondence, without proving
that a runtime field contains one of those row IDs.

The selected `man0l0.csv` row 91 contains different control expressions
across its logical columns. Its five-alternative switches occur in columns
0 and 4. Columns 1 and 2 use a different parameter expression. The source
name, row number and extra operand therefore do not establish a rendered
race-specific English line.

## Getter and finite numeric correspondence

`PlayerBaseClass.getTribe` reads `self.playerWork.tribe` and returns exactly
one value. Its reachable body contains no call, store or local conversion.
It does not populate the field, coerce its type or enforce a finite domain.
The selected normal methods call `getTribe` on their supplied A1, whose
actual class and method binding remain unproved.

The published MyPlayer initialization declares `tribe` in `playerWork._sync`
with type `integer8` and a native descriptor width of eight bits
(`xivl-client-structs:docs/work-binder-native-contract.md`, Declared work of
a MyPlayer / playerWork and Member widths). This does not establish that the
supplied A1 uses that declaration or that its value is a static row ID 0-15.
The same native contract's An object without storage section records that a
declared member without installed instance storage reads nil. The actual
layout, storage and value for this caller remain unproved.

The [normal-flow mapping](limsa-normal-tutorial-flow.md#dialogue-argument-and-final-movement-lesson)
owns the ordered inclusive comparisons and unmatched-value rule. Applying
those actual instructions to all 16 static row IDs gives the exact value
in `tribe.csv` column 1, including zero for row 0. This is a checked
correspondence over that static input set, rather than a sheet lookup in
the selected Lua methods. Unmatched numeric values retain their original
value. No behavior for an unobserved nonnumeric field value is established.

`xivl-client-data:docs/tribe-row-domains.md`, the row table and separate
numeric domains, owns the labels, column values and race-name-key warning.
Its exact row-ID join to `xtx_tribe.csv` column 4 supplies the English
labels. In that grouping column, the Miqo'te-labeled rows group at 4 and
the Roegadyn-labeled rows at 5. The paired `xtx_text_raceName` keys are a
separate domain and cannot replace the grouping values. The correspondence
adds no player-race wire field, complete appearance dictionary, creation
selection rule or historical availability claim.

## Dialogue forwarding and source initializer

The call at the end of each selected transformation is
`A0:sayFreeDisplayName(1600150,A0,91,v)`. The authenticated
`QuestBaseClass.sayFreeDisplayName` helper has four fixed formals and a
variadic tail. Under that helper binding, those operands forward to
`DesktopWidget.showMessage` with these roles:

| Forwarded role | Value |
| --- | --- |
| Desktop receiver | Global `desktopWidget` |
| Speaker operand | `1600150` |
| Message mode | `38` |
| Text-provider operand | The helper receiver A0 |
| Row operand | `91` |
| Variadic tail | The one supplied value v |

The helper's fixed third formal is not used in this forwarding. Its text
provider is its own receiver, rather than a substitution of that formal.
It performs no local branch or conversion, preserves the open variadic
tail, discards the message result and returns no values. The existing
[desktop message forwarding contract](wandering-minstrel-client-contract.md#inherited-message-path)
owns `showMessage` forwarding to `_appendMessagePool`. These are Lua
operand roles, without authenticated runtime speaker or actor identities.

`Man0l0.initText` separately calls
`_loadTextDataPermanently(self,21,"man0l0")`, retains no result and returns
no values. The native arithmetic in
`xivl-client-structs:docs/boot-native-call-contract.md`, Text data loading,
adds `0x03A20000` to an accepted integer input. For literal 21, that gives
`0x03A20015`. The same contract records the name test and possible wait.
This initializer supplies an attributable source-name lead. The name and
adjusted number alone do not authenticate a `man0l0` definition/data
association, a successful load, a selected locale or the later provider's
identity and lifetime.

## Selected row 91 declarations

Logical columns exclude the CSV row ID. `man0l0.csv` declares five `str`
fields, and row 91 has a nonempty cell in each. Parsing only that row's
lossless control markers gives:

| Logical columns | Static declaration |
| --- | --- |
| 0 and 4 | A `switch` with unary expression `E8(1)` and five string alternatives. |
| 1 and 2 | An `if` with unary expression `E9(4)` and two string alternatives. |
| 3 | Non-breaking-space controls, without a parameter conditional. |

The expression grammar is owned by
`xivl-tools:docs/formats/ssd-sheet.md`, Rich-string read and text-export
contract. Here `E8(1)` denotes a unary node with code `E8` and integer
operand 1. This syntax does not establish the node's runtime source or
meaning, its relationship to v or a formatter argument, a selected string
alternative or an active language.

Columns 1 and 2 do not declare that `E8(1)` switch. Their `E9(4)` expression
is kept distinct without assigning its runtime source or meaning. There
is no demonstrated binding from the selected numeric-speaker, mode-38
message path to this table, a chosen field or the formatter's actual
argument vector. The separately published WorldMaster message path does
not establish that binding for this speaker operand. Row-number equality
and the initializer's matching name remain a static association.

## Input identity and original locators

The extraction is retail 1.23b `2012.09.19.0001`. Selected canonical members
matched [scripts.json](../manifests/scripts.json), their archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json), and installed
LPBs and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
The [Limsa source identity](limsa-opening-tutorial-contract.md#input-identity-and-locators)
owns the Man0l0 triple. The additional selected sources are:

| Member under `lua/scripts/` | Source bytes | Source SHA-256 |
| --- | ---: | --- |
| `chara/player/playerbaseclass.lua` | 66466 | `6226B3FA15DFDBAD279B7DBA453F8A3B76FCB8B68BAD6E14F5403D52987F76E4` |
| `quest/questbaseclass_common.lua` | 35511 | `CF61A5687DBC7B6ACCD26C8CD3A138DECC0372FB72518AC6F2054F125BC1465E` |

Their exact original resource and payload identities are the entries for
those decoded paths in `retail_lua_coverage.json`. All selected chunks
parsed completely, with no trailing bytes. Child indices are zero-based,
PCs one-based, and code offsets address the decoded payload without its
LPB wrapper. PC p starts at `codeStart + 4*(p-1)`.

| Method | Canonical assignment line | Root closure / assignment PCs | Prototype / codeStart | Decisive PC |
| --- | ---: | --- | --- | --- |
| `PlayerBaseClass.getTribe` | 50 | 20 / 21 | Child 2 / `0x0CD7` | 3 returns the one field value. |
| `Man0l0.initText` | 20 | 9 / 10 | Child 0 / `0x06F6` | 4 calls the loader. |
| `QuestBaseClass.sayFreeDisplayName` | 962 | 89 / 90 | Child 29 / `0x213D` | 8 forwards the message and open tail. |
| `Man0l0.processTtrNomal001withHQ` | See normal-flow locators | See normal-flow locators | Child 30 / `0x20FE` | 158 reads the getter; 193 sends row 91. |
| `Man0l0.processTtrNomal001` | See normal-flow locators | See normal-flow locators | Child 31 / `0x28AC` | 159 reads the getter; 194 sends row 91. |

The selected CSV members matched
`xivl-client-data:manifests/tables.json` before parsing. Their archive
identity is owned by `xivl-client-data:manifests/private_csv_corpus.json`.
Only these members were read in memory, without hydrating a corpus:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `tribe.csv` | 156 | `D484FD5FE29A9F618C09242BCB33FFB6A77369FA2086FB44E2C8415720CEF5A3` |
| `xtx_tribe.csv` | 1550 | `D460C1C404A96B0B2E0C73D002F265EACE5159B59F63E1302F68CF7C8D4FA2ED` |
| `man0l0.csv` | 49319 | `925CDAA267EF298CF9885CF6163D86D910FCF037E11639A0CF821D351BEAEBE7` |

## Verification and remaining boundary

`tools/retail_script.py:decode_lpb` and the Lua 5.1 reader in
`tools/build_quest_contracts.py` supplied decoding and complete chunk
parsing. Root closure assignments authenticated the selected methods.
Checks covered the getter's reachable result, initializer tuple, dialogue
helper's fixed roles and open tail, both local numeric mappings against
all 16 static row IDs, and the selected row's distinct control expressions.
Controls rejected a changed getter field, loader number, message mode,
range polarity, switch unary operand and confused numeric column. These checks
did not execute a retail tutorial or reproduce the whole corpus.

The conditional workflow stops at actual method invocation and helper
binding, A1's getter binding, field population and domain enforcement, source initialization
and provider lifetime, the Man0l0 definition/data association, mode-38
native dispatch, formatter type conversion and argument selection, locale
selection and rendered dialogue. No historical actor selection or accepted
fresh-character progression is established.
