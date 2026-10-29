# Cast gauge property and command flow

This finding supplements `cast-gauge-lifecycle.md` with direct Lua 5.1 bytecode inspection of ActionGaugeWidget. It establishes conditional script calls and their literal arguments, rather than native lookup acceptance or display behavior.

## Source identity

The identified retail input is `client/script/n1635q/97q1vw39p35n1635q.le.lpb`, 2208 bytes, SHA-256 `dad3335de111491aab5fdc7fc50fac741931f2b10379e1fb2ef2f4d7ac4cae48`. The published wrapper decoder in `tools/retail_script.py` yields a 2195-byte Lua 5.1 chunk with SHA-256 `4046233a972c1a709f9295be3e618ca198ef1271124a7eb1860248245ced08a8`.

Pinned unluac `unluac_2025_12_23.jar`, 796256 bytes, SHA-256 `98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`, followed by CRLF-pair replacement with LF, reproduces the canonical `lua/scripts/widget/actiongaugewidget.lua` identity: 4058 bytes, SHA-256 `4269a53c9be52759d49289364fdbd16e7fef350c5866bdca5c5aae5eba746aff`. The decompilation guides navigation. The observations below were checked independently against constants and instruction flow. Restricted input, bytecode and decompiled bodies are not distributed here.

Program counters below are one-based within each child prototype. Byte offsets are zero-based in the decoded chunk. Add 13 for the corresponding raw LPB offset. Main CLOSURE and SETTABLE pairs identify child 2 as startCastGauge, child 3 as stopCastGauge, child 4 as deleteCastGauge, child 5 as startCastGaugeAnimation, child 6 as stopCastGaugeAnimation, child 7 as showWidget and child 8 as hideWidget.

## Start flow

`startCastGauge`, child 2, reads getCommandID from its command argument and getPlayerActionCommandData with the same argument and literal 36. A command result of -1 or nil data replaces both results with zero. PC16-24 writes the icon and text controls. PC25-28 calls showWidget and then startCastGaugeAnimation. This does not establish the image pixels or translated text.

`startCastGaugeAnimation`, child 5, PC2-9 reads `getCastEndTime` from `worldMaster:_getMyPlayer()` and reads `worldMaster:_getServerTime()`. PC10 subtracts server time from the deadline. PC11-13 replace the remainder with 1 only when it is <=0. PC14 divides 1 by that remainder. In particular, this is not a general clamp of positive fractional remainders to at least 1. The operand domain is not established by this LPB alone.

The conditional instructions are SUB at byte offset 1230, LE against numeric zero at 1234, JMP +1 at 1238, LOADK numeric one at 1242 and DIV at 1246.

The same method then makes these calls, all targeting literal `ProgressBar_MagicCast_Main`:

| PCs | Call byte offset | Method | Arguments after target |
| --- | ---: | --- | --- |
| 15-20 | 1270 | _setProperty | Maximum, 1 |
| 21-26 | 1294 | _setProperty | Value, 0 |
| 27-32 | 1318 | _setProperty | FloatData.Value0, reciprocal remainder |
| 33-36 | 1334 | setVisibility | true |
| 37-41 | 1354 | _sendStoryboardCommand | UILuaCommands.StartCastGauge |

The _setProperty and _sendStoryboardCommand calls pass nil between self and the target name. The script establishes no native interpretation of that argument. It does not write Minimum.

## Stop, delete and visibility

`stopCastGauge`, child 3, PC1-4 calls stopCastGaugeAnimation and then hideWidget. In child 6, PC1-5 sends `UILuaCommands.PauseCastGauge` to the main progress owner at call offset 1688. PC6-9 sets that owner visibility false at call offset 1704.

`deleteCastGauge`, child 4, PC1-2 only calls hideWidget at offset 1130. It does not directly pause the gauge, call stopCastGaugeAnimation or set progress visibility false.

`showWidget`, child 7, PC1-8 sets visibility true on IconControl_MainCommand and TextBlock_MainCommand. PC9-10 calls self show. It has no direct progress visibility write.

`hideWidget`, child 8, PC1-2 calls self hide. PC3-6 sets icon visibility false and PC7-10 sets text visibility false. The call offsets are 2038, 2054 and 2070. It has no direct progress range, value, visibility, pause, stop or native-destroy call. A method name alone does not establish native destruction.

These branches do not establish invocation cadence, clock conversion, native property acceptance, native event delivery, the display frame applying a change, animation scheduling, or actual rendered or live behavior. The progress owner and template part declarations are separate client-asset evidence.
