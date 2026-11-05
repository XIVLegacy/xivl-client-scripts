# Debugger raid-selector contract

The DEV debugger supplies a concrete positional selector from its
`raidDungeonSheet` global to `worldMaster._getZoneAt`. The selected row feeds
columns 20, 21 and 22 directly; column 41 contributes an offset into a table
obtained from static actor 320014. This establishes the caller's operands,
without identifying the global's creator, a decoded sheet schema or the
implementations behind the dynamic helper properties.

## DEV row selection and operands

In `lua/scripts/commanddebugger/commanddebuggerdev.lua`, the selected branch
at lines 3433-3453 parses two positive numeric values. Its two-capture pattern
uses an unescaped separator dot; the pattern does not require a literal dot at
that position. The branch requires `isRaidMaster()` to differ from false.

At lines 3465-3488 it invokes `_getAllKey` on the current `raidDungeonSheet`
global with no explicit arguments. It treats adjacent result entries as
inclusive bounds, enumerates their integer values and selects by the first
parsed value's one-based ordinal. The selected integer is row r; zero is
rejected. This is the script's treatment of the result, without proof that an
unattributed runtime handle uses that range encoding.

Each subsequent `_getData` call reloads `raidDungeonSheet` and supplies the
selected row r. Relating their outputs to one sheet requires current handle
and storage continuity across the calls:

| Column | Source lines | Selected consumer role |
|---:|---|---|
| 3 | 3498-3504 | Rejects a second parsed value greater than the returned value |
| 20 | 3512-3518 | First explicit `_getZoneAt` operand |
| 21 | 3519-3525 | Second explicit `_getZoneAt` operand |
| 22 | 3526-3532 | Third explicit `_getZoneAt` operand |
| 41 | 3533-3541 | Additive table-index offset c; zero is replaced by 1 |

At lines 3542-3549, `_getStaticActor(320014)` supplies the receiver for
`getRegionTbl(r,true)`, whose result is T. The script indexes T at
`second+c-1`, rejects a result equal to numeric zero, then invokes the current
`worldMaster._getZoneAt` at line 3570 with four explicit operands:

`(column20,column21,column22,T[second+c-1])`.

The arithmetic is addition and subtraction. These positional roles do not
assign schema names, cell types, physical units, zone IDs or variant meanings.
The dynamic call alone supplies no native registration, execution or network
result.

`xivl-client-data:manifests/staticactor_class_paths.json`, actor 320014,
maps the selected script actor to `/Judge/InstanceRaidGuideJudge`.
Its authenticated `judge/instanceraidguidejudge.lua` initializer at lines
8-10 contains no `getRegionTbl` implementation or `_cpp` declaration.
The class-path relationship does not implement the property invoked by DEV.

## GM diagnostic reader

In `commanddebuggergm.lua`, parsed command 20040 obtains the current
AreaMaster and returns before the selected read if `isInstanceRaid()` equals
false. At lines 3853-3862 it calls that object's dynamic `getInstanceRaidID`
property, then uses the result directly as the row for column 41. A zero
column value is replaced by 1. The branch uses it in display arithmetic and
returns a diagnostic string at line 3891.

The [AreaBaseClass initialization contract](area-base-client-initialization.md)
owns the retained `isInstanceRaid` flag. It does not provide the instance raid
ID producer. The GM result does not bind a historical duty to a zone or prove
that this diagnostic branch supplied a gameplay selection.

## Source and implementation boundary

An exact identifier-reference query over the authenticated extraction found
`raidDungeonSheet` only as reads in the two debugger members, and
`getInstanceRaidID` only as GM's dynamic identifier. It supplied no global
initializer or implementation. The observed name is not an authenticated
sheet filename or resource key. It is not thereby the `xtx/raidDungeon` text
sheet or one of the similarly named extrasheets.

The native key-vector contract in
`xivl-client-structs:docs/spreadsheet-native-contract.md`, `_getAllKey`,
returns a raw vector. DEV's adjacent-pair interpretation does not establish
that vector's format or bind this global to that native without a wrapper.
Actual rows, the handle creator, current receiver implementations and their
results remain separate evidence requirements.

## Source identity and verification

The [reproduction manifest](../manifests/scripts.json) pins the retail
`2012.09.19.0001` canonical Lua sources:

| Member under `lua/scripts/` | Bytes | SHA-256 |
|---|---:|---|
| `commanddebugger/commanddebuggerdev.lua` | 623458 | `9ce79f78f841c964222ec7a72f1a557406d1efa1ad75bc03685a55af8b5ba34a` |
| `commanddebugger/commanddebuggergm.lua` | 281241 | `cdbbf9929a1353399e372dde705d38c577f491587d64b577beb8d43a1aaa0301` |
| `judge/instanceraidguidejudge.lua` | 205 | `da5c9dadfa35629b9a12d4907396f3e6d93b43c3811740b904966674fe99b36e` |

Read-only Python checks authenticated the canonical LF bytes and the selected
receiver, row, column and selector expressions. A deliberately altered column
operand was rejected in memory. Source hashes matched before and after the
check. These are decompiled-source findings; no sheet rows or runtime values
were executed or observed.
