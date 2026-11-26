# Named script log lines

This page counts the static call sites that put a line into the chat log from a
shipped script, with the source operand and the category of each. A count is a
static call site, not an execution. A caller that builds a method name at run
time is outside the count.

`DesktopWidget.showLog` in `widget/desktopwidget.lua` forwards its source,
category, owner and row operands and the remaining tail to `_appendLogPool`.
`QuestBaseClass.tellByNpcLinkshellChat(source, owner, row, ...)` in
`quest/questbaseclass.lua` calls
`desktopWidget:showLog(source, 39, owner, row, ...)`. How a category selects a
text row is in `xivl-decomp:docs/resource/logcontrol-line-format.md`, LF-04,
and the four installed named rows are in
`xivl-client-data:docs/named-log-line-rows.md`.

## Quest linkshell lines

Thirty sites call `tellByNpcLinkshellChat` with a numeric source operand. Each
passes its scenario receiver as the owner.

| Script under `quest/scenario/man/` | Sites | Source operand | Method: rows |
|---|---:|---:|---|
| `man0g1.lua` | 8 | 1300018 | `processEvent013`: 266 to 270. `processEvent013_2`: 266, 267, 335 |
| `man0u1.lua` | 8 | 1500014 | `processEvent013`: 242 to 246. `processEvent013_2`: 242, 243, 322 |
| `man0l1.lua` | 14 | 1000015 | `processEvent025`: 298 to 302. `processEvent025_2`: 298, 299, 319. `processEvent625`: 131, 132. `processEvent637`: 161 to 164 |

One more site, `showEventBeforeNpsLS` in
`quest/questbaseclass_common.lua`, passes a caller operand as the source,
`worldMaster` as the owner and row 51035.

## Direct calls with a named source

| Script, method | Sites | Category | Source operand |
|---|---:|---:|---|
| `gamedata/cutscene_common.lua`, `_onShowUIClip` | 3 | 38 | A name string. The method takes it from its operands or an actor class lookup, with the literal fallbacks `SnpcNoName` and `???` on different arms |
| `chara/npc/populace/populacecompanywarp.lua`, `eventAskMainMenu` | 2 | 38 | The receiver |
| `quest/scenario/noc/noc001.lua`, `eventShowPrizeMessage` | 1 | 38 | A supplied character operand |
| `director/instanceraid/instanceraidhamletdefense.lua`, `printNPCSay` | 1 | 35 | A display name number picked by `work.hamletID` from 1600146, 1200220 and 1000062 |

## Calls with `worldMaster` as the source or from the world master

| Script, method | Sites | Category |
|---|---:|---:|
| `world/worldmaster_event.lua`, `notify` and `alert` | 1 each | 32 and 33. The receiver is the world master and the source is a caller operand, as in [WorldMaster message arguments](worldmaster-message-arguments.md) |
| `quest/scenario/noc/noc001.lua`, `showSupplyLimit` and `pELimitErr` | 1 each | 40, source `worldMaster` |
| `chara/player/playerbaseclass.lua`, `_onReceiveLimitAddicted` | 5 | 68, through `_appendLogPool` with source `worldMaster` |

The only other `_appendLogPool` site is the `showLog` wrapper. `_printLog`
sites are a different method and are not counted here.

## Source identity and reproduction

The extraction is retail 1.23b `2012.09.19.0001`. Every one of the 2671
installed script resources of
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) was decoded
with `decode_lpb` of `tools/retail_script.py`. Chunks whose constants hold
`showLog`, `_appendLogPool`, `_printLog`, `tellByNpcLinkshellChat` or
`sayFreeDisplayName` were decompiled with the pinned unluac, and the
decompiled members named on this page match
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
Operands were read from the decompiled call sites.

The site counts agree with the original bytecode. With `ChunkReader`,
`instruction` and `walk` of `tools/build_quest_contracts.py`, count each `SELF`
instruction whose key constant is `showLog`, `_appendLogPool` or
`tellByNpcLinkshellChat` in every prototype. Over all decoded chunks that hold
one of the three names, that yields the counts above and no other site.
