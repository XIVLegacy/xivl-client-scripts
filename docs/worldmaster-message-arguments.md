# WorldMaster message arguments

`WorldMaster.say` forwards its receiver, literal 40, a supplied object, a text
row and all variadic arguments through `DesktopWidget.showMessage` to
`DesktopWidget._appendMessagePool`. Both Lua helpers discard results and
return no values. The `_inl` declaration names `_appendMessagePool_cpp`.
This source/helper contract stops at that declaration; the registered native
callback, text lookup and formatter-vector relationship need separate proof.

These are recovered source and original-bytecode contracts for the retail
FFXIV 1.23b extraction `2012.09.19.0001`. They do not establish native
rendering, runtime argument types, display completion or server behavior.

## Generic argument route

`world/worldmaster.lua:2-4` requires `/World/WorldMaster_event`.
`world/worldmaster_event.lua:111-124` defines `say` with parameters
`(A0_2,A1_2,A2_2,...)`, including its receiver. It supplies the following
ordered values to `DesktopWidget.showMessage`:

| Position after function | Supplied value |
| --- | --- |
| 1 | Global `desktopWidget`, the showMessage receiver |
| 2 | say receiver `A0_2` |
| 3 | Literal 40 |
| 4 | say argument `A1_2` |
| 5 | say argument `A2_2` |
| 6 onward | All say variadic arguments, in order |

`widget/desktopwidget.lua:369-384` defines `showMessage` with parameters
`(A0_2,A1_2,A2_2,A3_2,A4_2,...)`. It forwards its receiver, all four named
arguments and all variadic arguments to that receiver's `_appendMessagePool`.
Neither helper constructs a string key, argument table, typed value wrapper
or formatted text in Lua.

The source renders each vararg expansion through a temporary, which alone
does not settle its arity. The original bytecode supplies that proof. The
following tables cover every instruction in both helper prototypes. PCs are
zero-based within each prototype; register names describe the decoded
instructions, not recovered retail source variable names.

`say` is `root/proto4`, with three named parameters and vararg flag set. Its
constants are `desktopWidget`, `showMessage` and 40. The root assigns the
closure to `say` at PC 14.

| PC | Original instruction / effect |
| --- | --- |
| 0 | `GETGLOBAL A=4 Bx=0`: load desktopWidget |
| 1 | `SELF A=4 B=4 C=257`: select showMessage and retain its receiver |
| 2 | `MOVE A=6 B=0`: copy say receiver |
| 3 | `LOADK A=7 Bx=2`: load literal 40 |
| 4 | `MOVE A=8 B=1`: copy first named argument after receiver |
| 5 | `MOVE A=9 B=2`: copy second named argument after receiver |
| 6 | `VARARG A=10 B=0`: place all variadic arguments from register 10 |
| 7 | `CALL A=4 B=0 C=1`: call with arguments through the open stack top; keep no results |
| 8 | `RETURN A=0 B=1`: return no values |

`showMessage` is `root/proto14`, with five named parameters and vararg flag
set. Its sole constant is `_appendMessagePool`. The root assigns the closure
to `showMessage` at PC 56.

| PC | Original instruction / effect |
| --- | --- |
| 0 | `JMP sBx=1`: jump to PC 2 |
| 1 | `RETURN A=0 B=1`: skipped by the initial jump |
| 2 | `SELF A=6 B=0 C=256`: select _appendMessagePool and retain its receiver |
| 3 | `MOVE A=8 B=1`: copy first argument after receiver |
| 4 | `MOVE A=9 B=2`: copy second argument after receiver |
| 5 | `MOVE A=10 B=3`: copy third argument after receiver |
| 6 | `MOVE A=11 B=4`: copy fourth argument after receiver |
| 7 | `VARARG A=12 B=0`: place all variadic arguments from register 12 |
| 8 | `CALL A=6 B=0 C=1`: call with arguments through the open stack top; keep no results |
| 9 | `RETURN A=0 B=1`: return no values |

Both `VARARG B=0` / `CALL B=0` pairs preserve open forwarding. Both `CALL C=1`
instructions discard results, and both reachable terminal `RETURN B=1`
instructions return zero values. These complete helper bodies contain no
Lua wait, yield, loop or display-completion callback. They do not establish
whether a native operation yields or when a message is rendered or dismissed.

The adjacent source helpers provide separate observed literals:
`WorldMaster.notify` at worldmaster_event.lua:127-140 forwards to
`DesktopWidget.showLog` with 32; `WorldMaster.alert` at lines 143-156 forwards
to the same helper with 33. No enum meaning is assigned here to 40, 32 or 33.

## Stewart callsite and text-loading context

Gcl107 `processEventStewart`, `root/proto28` PC 83, supplies this exact tuple:

```text
say(worldMaster, quest, getTextIdStewart(quest, 170, A4_2), A3_2)
showMessage(desktopWidget, worldMaster, 40, quest, selectedRow, A3_2)
_appendMessagePool(desktopWidget, worldMaster, 40, quest, selectedRow, A3_2)
```

Here `quest` denotes the Stewart method receiver `A0_2`. The first function
lookup uses the global worldMaster and also supplies it as say's receiver.
The quest object is the second supplied value. Source lines 2228-2238 retain
both identities explicitly. In original bytecode, PCs 75-76 load worldMaster
and select say; PC 77 copies the quest object into register 10. PCs 78-81 call
`getTextIdStewart` with quest, 170 and A4_2 and keep its single result in
register 11. PC 82 copies A3_2 into register 12. PC 83 is
`CALL A=8 B=5 C=1`: four arguments including say's receiver, with no results
kept. The adjacent row-171/172 calls at PCs 92/101 supply the same A3_2.

`getTextIdStewart`, `root/proto29`, maps 170 to 327 only when A4_2 equals
true; otherwise it retains 170. The [To Kill a Raven contract](to-kill-a-raven-client-contract.md)
owns the full Gcl107 method and alternate-text behavior. This argument route
does not establish A3_2's runtime value or type, or bind A4_2 to a content mode.

Gcl107 `initText` at source lines 11-20 calls
`_loadTextDataPermanently(quest,10496,"gcl107")` at lines 14-17.
WorldMaster's separate `_onInit` at worldmaster.lua:99-115 calls
`_loadTextDataPermanently(worldMaster,39,"worldMaster")` at lines 106-109.
The say route preserves the supplied quest object and selected row; it does
not replace them with these WorldMaster loading arguments. These loading
calls establish the source associations only. The inspected Lua does not
establish how the native leaf interprets the supplied objects as sheet owners
or constructs its lookup key.

## Declared target and native qualification

`widget/desktopwidget_u.lua:4-11` declares `_appendMessagePool_inl` with
parameters `(A0_2,A1_2,A2_2,A3_2,A4_2,...)`. Its original `root/proto0` has four
instructions: PCs 0-1 load the constants `self` and `_appendMessagePool_cpp`
into registers 6 and 7; PC 2 is `RETURN A=6 B=3`, returning those two strings;
PC 3 is a terminal zero-value return. The root assigns this closure to
`_appendMessagePool_inl` at PC 2. This is a declaration of the target name,
not an observed invocation of a resolved native function address.

The promoted N-API snapshot
[`data/vendor/client-structs/lua_api_index.json`](../data/vendor/client-structs/lua_api_index.json),
entry `_appendMessagePool`, records `BCS-Y-0492`, symbol name
`bulk_napi_attribution_via_FUN_00cccad0_callers`, kind `finding`, address
`0x00000000`, confidence `confirmed` and source `notes`. The zero address
does not resolve the native callback. The entry supports the catalog's
API-name attribution only, not the runtime semantics of the declared target.

[`PROVENANCE.json`](../data/vendor/client-structs/PROVENANCE.json) is the
snapshot identity authority. It records source
`XIVLegacy/xivl-client-structs manifests/lua_api_index.json`, source license
CC-BY-4.0, source SHA-256
`25df1fffe1eb17376ce5d09e5f55add76e9a8fe5d1f56a467a68dd0d881daa8c`,
promoted SHA-256
`01fbb75b2d423a958baba4c23d703aee7e3a587b65bf3e85b2387ab70ec62421`,
evidence tier `promoted first-party N-API catalog`, and transformation
`top-level source field omitted from the promoted snapshot`. The promoted
bytes match their pin; this does not independently authenticate the source
snapshot named by the provenance record.

Extending this source route into native behavior requires qualifying the
declared `_appendMessagePool_cpp` name's registered callback and the supplied
object's interpretation, row-key construction, variadic-value conversion,
variant tags and vector indices. The Lua helper bodies alone establish no
join from A3_2 to the duty-reference control.

The separate [native message-pool profile](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/worldmaster-message-pool.md)
qualifies the registered `_appendMessagePool` member, its WorldMaster path and
conditional formatter join. It uses original registration and invocation
evidence, rather than treating the `_cpp` declaration string as a native symbol.

The separate formatter findings in
[`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md)
and
[`xivl-decomp:docs/resource/rich-string-entry-counts.md`](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/rich-string-entry-counts.md)
do not supply this message-pool binding. Fixed text counts, levels and time
operands do not establish A3_2's meaning, a historical argument value or server
admission or enforcement behavior.

## Authenticated input identities

All six selected source members match
[`manifests/scripts.json`](../manifests/scripts.json). Each original LPB and
decoded payload matches
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
Resource paths below are relative to `client/script/`; source paths are
relative to `lua/scripts/`. Hashes are SHA-256. The source members were read
from the archive identified by
[`manifests/private_lua_corpus.json`](../manifests/private_lua_corpus.json).

| Canonical source path | Bytes | Lines | Source SHA-256 |
| --- | --- | --- | --- |
| `world/worldmaster.lua` | 2479 | 135 | `C0A7E0460EF969FE5C10DE5593E3237A279258A5849DF3D2B7F534B08732A4BA` |
| `world/worldmaster_event.lua` | 7559 | 329 | `744487A7CAAA94E1C4D2056CC07686A894C6BA336BBD021BBFFEEBCEEF2AD099` |
| `world/worldmaster_u.lua` | 4102 | 231 | `D562CB7B2DF8AC263460F246BCF6870C00DE6A9AD8E5EB09DBB9652960AA34CF` |
| `widget/desktopwidget.lua` | 7929 | 402 | `5D3BFABF2E8A55EE2E64F607BDADA5F04046C9528E9E9ACA858E9AD9E232070A` |
| `widget/desktopwidget_u.lua` | 8801 | 472 | `D5C6C1CA8EF11D7238F00F46280D3A5D48BC91A3261E9DE407B21347F03A768B` |
| `quest/scenario/gcl/gcl107.lua` | 49757 | 2588 | `98CE0AE86655ECCFFBC15234091DBBBA9ACC847C1BBB099AE8F5F64BFDAB1345` |

| Canonical source path | Original resource path | LPB bytes | LPB SHA-256 |
| --- | --- | --- | --- |
| `world/worldmaster.lua` | `nvsy6/nvsy6x9rq5s.le.lpb` | 1430 | `DA3ADCCEA066061A6289B89AF65BDE92DB13A5EABBDD1F0072565576D5414D20` |
| `world/worldmaster_event.lua` | `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb` | 2555 | `4CED313114AB09753AD0DC82EA8E9CD12C66D31447C967E91883932291CD7459` |
| `world/worldmaster_u.lua` | `nvsy6/nvsy6x9rq5s_p.le.lpb` | 3222 | `14007A1030E2104EF1A29D5DA9135EC7A8CCA8122505F297D322F1CDF89C76C8` |
| `widget/desktopwidget.lua` | `n1635q/65rzqvun1635q.le.lpb` | 4029 | `BE7B0959BA530027991B22308B1D6A84CE5DB311BDB727F987678B5DBF810E51` |
| `widget/desktopwidget_u.lua` | `n1635q/65rzqvun1635q_p.le.lpb` | 6599 | `BA43CD71B0C5A36A74FF947A6BD00C2B7BFE3942BE85B72DEC504FF848FD5B22` |
| `quest/scenario/gcl/gcl107.lua` | `tp5rq/r75w9s1v/37y/37yijc.le.lpb` | 17770 | `C816BD5D08EEEE019F4C7BDD93942DE143A28BFF8F63F8161D5AB14791B90A7E` |

| Canonical source path | Original resource path | Payload bytes | Payload SHA-256 |
| --- | --- | --- | --- |
| `world/worldmaster.lua` | `nvsy6/nvsy6x9rq5s.le.lpb` | 1417 | `6DCA2434550518B09FE58D4878DA3F0F0A77C1124808C231AD399B87089E420D` |
| `world/worldmaster_event.lua` | `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb` | 2542 | `C7DB606357F8E5811809A6232157C2C9AC1DAF0055CFCAA01FBBC7051FD68BF5` |
| `world/worldmaster_u.lua` | `nvsy6/nvsy6x9rq5s_p.le.lpb` | 3209 | `E48ECF96B9D04764367D99711AF5B6F8C7B38914FD9087C4A82ACB12CAF3DEDE` |
| `widget/desktopwidget.lua` | `n1635q/65rzqvun1635q.le.lpb` | 4016 | `92AF6D4FE068C49EFCB7F4B1DF869E4B5846A86217915BB6CB798FE24C58D14E` |
| `widget/desktopwidget_u.lua` | `n1635q/65rzqvun1635q_p.le.lpb` | 6586 | `CE7CBC20EA49771CCCB4066980ED42AFDF4AC088E8BB776F143EF75E6F25CB58` |
| `quest/scenario/gcl/gcl107.lua` | `tp5rq/r75w9s1v/37y/37yijc.le.lpb` | 17757 | `3B003570FC6D9BF23ACF12F2D2333B142BEE7FE6C5FC56388702D8F0F717A96B` |

The original wrapper decoder is `tools/retail_script.py:decode_lpb`; the
fixed Lua 5.1 reader and instruction decoder are
`tools/build_quest_contracts.py:ChunkReader` and `instruction`. Inspection
authenticates the six named resources and checks the complete say,
showMessage and declaration instruction vectors, plus Stewart's PC 83 call
arity. It does not execute retail Lua or invoke the native renderer.
