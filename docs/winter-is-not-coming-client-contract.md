# Winter Is Not Coming snowman callbacks

The original `Spl0i3` bytecode binds five snowman callbacks. Each calls
`worldMaster:say` once and returns zero Lua values. Only
`processEventSnowManOk` forwards an additional caller-supplied argument into
the text. These local methods present text and supplied data; they do not
calculate a snowman counter, consume an item or return a completion flag.

The [retail quest identity](seasonal-quest-client-contracts.md#retail-quest-identities)
is Winter Is Not Coming, quest 110801, class `/Quest/Scenario/Spl/Spl0i3`.
This finding covers its snowman callbacks, adjacent completion presentation
and two related object initializers, rather than the full quest flow.

## Artifact identity and method

The inputs are the original 1.23b resources below, with paths relative to
`client/script/`. Hashes are SHA-256. The decoded payload starts with the
12-byte Lua 5.1 header; byte offsets below include that header.

| Class / LPB resource | LPB bytes / SHA-256 | Decoded payload bytes / SHA-256 |
| --- | --- | --- |
| `Spl0i3`: `tp5rq/r75w9s1v/ruy/ruyj1g.le.lpb` | 8023 / `4a1867a9cb26c998215ec8fb352c27ac15e956fa8b9ef0ef252fd7be9f944546` | 8010 / `538ca7710c66db39ff09930d05dc720b8bbfbee69be64ebf13adf99dc4a0c357` |
| `ObjectBigSnowMan`: `729s9/wu7/v8057q/v8057q813rwvnx9w.le.lpb` | 301 / `19bf442d306b469c3c1731f8a6512f3397c9af9875a11d93d497564afb447950` | 288 / `f4f012fee4f0f49696d561b81c09a2f5a49ebb608940577f8f6942923b16d8f6` |
| `ObjectSnowThrowBell`: `729s9/wu7/v8057q/v8057qrwvnq2svn85yy.le.lpb` | 304 / `7fe1553bad0ee5a0b01e5ba9c9e654aa54cdf39818adaef0cda0670b1ae92b12` | 291 / `425c05ffa6c654173bd324f75163cc4e95f01f9cd0f4af476874b7ea822e45e6` |

The raw and payload identities matched their resource rows in
[manifests/retail_lua_coverage.json](../manifests/retail_lua_coverage.json),
SHA-256 `46fd1b388a883c0f70fc8a0bae27d08e05a1bfd776ffcac094a6b1ddd4b9d9f4`.
The canonical readable members `quest/scenario/spl/spl0i3.lua`,
`chara/npc/object/objectbigsnowman.lua` and
`chara/npc/object/objectsnowthrowbell.lua` matched
[manifests/scripts.json](../manifests/scripts.json), SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`.
They belong to extraction `2012.09.19.0001`. The canonical `Spl0i3` text hash
is `76e7be2119455dd3e0f36305825fbf3468a62cfd1cbc3fa82f41608d68a720cb`;
it differs from the independent decompile identified in the seasonal summary.

`tools/retail_script.py:decode_lpb` decoded the wrappers in memory.
`tools/build_quest_contracts.py:ChunkReader`, `instruction` and `analyze_chunk`
parsed all three chunks to exact EOF and joined root CLOSURE/SETTABLE
instructions to method prototypes. The tools were inspected at revision
`4ec981f11a1cfa50cdb44bd034bd6394f7408bb0`. A bounded Python instruction
tracer checked 14 synthetic paths, including changed unused parameters and
different P3 values. It invoked no Lua VM, client, server or native function.
Those checks establish static forwarding and return counts, not reachability.

## Snowman argument and return contract

P0-P3 are zero-based fixed Lua parameters, including a receiver if supplied
by the caller. Their runtime types and producer are unresolved. P0 is passed
as the text-context argument. P1 and P2 are unused by these five callbacks.
`SnowManOk` has four fixed parameters; the other four have three. None has
varargs or upvalues.

The table's arguments exclude the `worldMaster` receiver. PCs and child
prototype indices start at zero. All byte offsets in this page are decimal
offsets in the decoded payload, rather than in the LPB wrapper.

| Method under `Spl0i3` | Prototype | Root SETTABLE PC / offset | Explicit `say` arguments | CALL PC / offset / A,B,C | RETURN PC / offset / A,B,C |
| --- | --- | --- | --- | --- | --- |
| `processEventSnowMan` | `root/proto11` | 42 / 200 | P0, 71, 0 | 5 / 6404 / 3,5,1 | 6 / 6408 / 0,1,0 |
| `processEventSnowManOk` | `root/proto12` | 45 / 212 | P0, 72, 0, P3 | 6 / 6520 / 4,6,1 | 7 / 6524 / 0,1,0 |
| `processEventSnowManEvent` | `root/proto13` | 48 / 224 | P0, 68, 0 | 5 / 6632 / 3,5,1 | 6 / 6636 / 0,1,0 |
| `processEventSnowMandefo` | `root/proto15` | 54 / 248 | P0, 70, 0 | 5 / 6993 / 3,5,1 | 6 / 6997 / 0,1,0 |
| `processEventSnowMandefo2` | `root/proto16` | 57 / 260 | P0, 69, 0 | 5 / 7105 / 3,5,1 | 6 / 7109 / 0,1,0 |

Each root CLOSURE immediately precedes its SETTABLE. `CALL B` includes the
function register and all arguments, including the receiver supplied by SELF.
`CALL C=1` retains no results. `RETURN B=1` returns zero Lua values, rather
than a numeric zero or one nil value.

In `SnowManOk`, PC 5 / offset 6516 is `MOVE A=9 B=3 C=0`. The following CALL
passes R5-R9, forwarding P3 unchanged as the last formatting argument. There
is no arithmetic, comparison, normalization or validation of P3 in this body.

`initText`, `root/proto0`, loads text set 5715, `spl0i3`, with CALL PC 3 /
offset 991, A=1 B=4 C=1. Its RETURN at PC 4 / offset 995 has B=1.
The canonical text places the five selected methods at lines 908-1007.

## Text and adjacent completion presentation

Python `csv` read the selected rows from the manifest-pinned decoded CSV
archive, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
The complete `spl0i3.csv` member matched
`xivl-client-data:manifests/tables.json`: 66,075 bytes, SHA-256
`e144471f57ae2d9787d73577e6be6fec111cc50842b8647d7fd8b333e446439d`.
Its English sheet column is 1, counting after the row ID starting at zero.

| Row | English presentation |
| ---: | --- |
| 68 | Target Father Frost and use the Snowball emote or `/snowball`. |
| 69 | Items are needed to make Father Frost grow. |
| 70 | The ice effigy stands silent. |
| 71 | The snowball hit Father Frost. |
| 72 | A formatted quantity and item name are described as remaining. |
| 73 | Father Frost grew slightly. |
| 74 | A present is offered. |

The row-72 template supports interpreting the forwarded P3 as display input
for a remaining-quantity message. It does not establish its runtime type,
range, counter storage or producer. Row 68 supplies player instructions;
it does not prove which command, emote or event dispatcher selects a callback.

The adjacent `processEventClear`, `root/proto14`, has three fixed parameters.
It calls P2:`startCliantTalkTurn(2,P1)` at PC 3 / offset 6736, then
P2:`_runCharaScheduler(354066432)` at PC 6 / offset 6748. P2:`say(P0,73,0)`
and P2:`say(P0,74,0)` occur at PCs 11/16, offsets 6768/6788. It finishes P2
talk at PC 18 / offset 6796 and returns zero values at PC 19 / offset 6800,
`RETURN A=0 B=1 C=0`. The method presents growth and a gift without an item
grant, counter update or quest-state write in its own instructions.

## Object initialization and producer boundary

Both selected object chunks declare a class inheriting `NpcBaseClass` and
only one local method, `initForEvent`, at `root/proto0`. Each initializer
calls P0:`_setGroundOn(false)` and returns zero Lua values:

| Class | CALL PC / offset / A,B,C | RETURN PC / offset / A,B,C |
| --- | --- | --- |
| `ObjectBigSnowMan` | 2 / 230 / 1,3,1 | 3 / 234 / 0,1,0 |
| `ObjectSnowThrowBell` | 2 / 233 / 1,3,1 | 3 / 237 / 0,1,0 |

The only literal references to the five callback names in these three original
chunks are the `Spl0i3` root assignments above. No resolved local CALL targets
one of those names. An exact-identifier search of all 2,671 canonical Lua
members, after checking every member's bytes against the pinned script
manifest, likewise found only their five declarations in `spl0i3.lua`, at
lines 919, 934, 948, 993 and 1007.

Those checks cover literal references and resolved local calls. Inherited,
computed, native, server and other-resource dispatch remain untraced. The
missing edge is the emote/event producer selecting a method and
supplying its arguments, particularly P3. These artifacts do not establish
the actor-class/spawn binding, snowman growth thresholds, item consumption,
gift grant, quest completion or weather activation. The selected object
initializers do not supply those mechanics.
