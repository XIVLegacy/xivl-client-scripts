# Desktop widget mode around a cut scene

`CutScene.startCutScene` orders a desktop widget mode before play and
cancels it after play for some of its selector values. The desktop keeps one
mode per level, stores the applied mode in `work.mode`, and answers
`isCutSceneMode` from that field. This page records those script operands
and branches. Native playback, widget storage, rendering and server
behavior are outside it.

## Source identity

The inputs are three installed resources of client extraction
`2012.09.19.0001`, authenticated against the
[coverage manifest](../manifests/retail_lua_coverage.json).

| Decoded path under `lua/scripts/` | Installed resource under `client/script/` | Wrapper bytes | Decoded bytes / SHA-256 |
| --- | --- | ---: | --- |
| `gamedata/cutscene_common.lua` | `39x569q9/7pqr75w5_7vxxvw.le.lpb` | 9125 | 9112 / `7ef33408c579f2d1ede120d9751851bd39b77dd1b6ca6a0aa821b413fe11b4fd` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/desktopwidget.lua` | `n1635q/65rzqvun1635q.le.lpb` | 4029 | 4016 / `92af6d4fe068c49efcb7f4b1df869e4b5846a86217915bb6cb798fe24c58d14e` |

`tools/retail_script.py` decoded each LPB. Prototype IDs, PCs and code
starts below are zero-based in the decoded payload. A code start is the byte
offset of the prototype's first instruction. Operand counts include the
receiver.

| Method | Prototype / code start / PCs |
| --- | --- |
| `CutScene.startCutScene` | `root/proto8` / `0x1D11` / 289, variadic after four fixed operands |
| `DesktopWidget.orderDesktopWidgetMode` | `root/proto144` / `0x1506B` / 21 |
| `DesktopWidget.cancelDesktopWidgetMode` | `root/proto145` / `0x15149` / 94 |
| `DesktopWidget.getDesktopWidgetMode` | `root/proto146` / `0x153C7` / 7 |
| `DesktopWidget.getModeLevel` | `root/proto147` / `0x15428` / 45 |
| `DesktopWidget.isCutSceneMode` | `root/proto148` / `0x15594` / 20 |
| `DesktopWidget.setDesktopModeDetail` | `root/proto149` / `0x1564A` / 396 |
| `DesktopWidget._onPreCutSceneCancel` | `root/proto11` / `0x0DD7` / 5, in `desktopwidget.lua` |
| `DesktopWidget._onPostCutSceneCancel` | `root/proto12` / `0x0E4B` / 5, in `desktopwidget.lua` |

## Order and cancel in `startCutScene`

The operands after the receiver are the play kind `A1`, the desktop mode
`A2` and the raw selector `A3`. PCs 15-53 set two locals from the raw
selector before PCs 54-84 normalize it, as recorded in the
[replay and skip contract](cutscene-replay-skip-contract.md#skip-actor-binding).

| Raw selector | Order local | Cancel local |
| ---: | --- | --- |
| 1, 2 | false | false |
| 3, 4 | false | true |
| 5, 6 | true | true |
| 7, 8 | true | false |
| any other value | nil | nil |

PCs 88-107 request `desktopWidget:orderDesktopWidgetMode(A2)` when `A1`
equals 1 and the order local is exactly false, so for raw selectors 1 to 4.
The mode compares at PCs 92-103 against 61, 62, 63 and 64 all reach the same
call and do not gate it.

After `_play` or `_replay` returns, PCs 251-264 request
`desktopWidget:cancelDesktopWidgetMode(A2)` when the first result is exactly
true and the cancel local is exactly false, so for raw selectors 1, 2, 7 and
8. This branch does not test `A1`.

## Mode levels

`getModeLevel` returns a level for its one operand:

| Mode | Level |
| --- | ---: |
| 8, 120 | 1 |
| 16, 32 | 2 |
| 61, 62, 63, 64 | 3 |
| 126 | 4 |
| 127 | 5 |
| any other value | 0 |

`orderDesktopWidgetMode` returns for level 0 (PCs 3-8). Otherwise it stores
the mode at `work.desktopMode[level]` (PCs 9-11) and, when `work.modeLevel`
is not above the level, calls `setDesktopModeDetail(mode, level)`
(PCs 12-19).

`cancelDesktopWidgetMode` returns for level 0 (PCs 3-8). For a level above
1 it returns when `work.desktopMode[level]` is already 0, requests
`_unlockPlayerControl` on the local player for mode 126, and stores 0 in the
level slot (PCs 9-26). For level 1 it stores 8 in the slot (PCs 28-30). It
returns when the level is above `work.modeLevel` (PCs 31-34). Its last call,
at PCs 87-92, is `setDesktopModeDetail(work.desktopMode[level], level)` for
the level its scans at PCs 35-86 leave selected.

`_onPreCutSceneCancel` requests `orderDesktopWidgetMode(127)` and
`_onPostCutSceneCancel` requests `cancelDesktopWidgetMode(127)`.

## Applied mode

`setDesktopModeDetail` stores its first operand in `work.mode` (PCs 0-1) and
its second in `work.modeLevel` (PCs 2-3) before any other request. It then
calls `finish(true)` on static widget 17 and `cancelWidgetCommand`
(PCs 4-11) and switches on the fresh `work.mode` read at PCs 12-13. Modes
16, 61, 62, 63, 126 and 127 share the first arm at PCs 31-53: `closeWidget`
for roots 11, 2 and 3, `work.cutsceneMapFlag` false,
`closeCutSceneEffectWidget`, and `hide(true, true)` on static widget 1.

`getDesktopWidgetMode` returns `work.mode` (PCs 3-5). `isCutSceneMode` calls
it and returns true for 61, 62, 63 or 64 and false otherwise (PCs 1-18).

So after an order of mode 61, 62 or 63 that `setDesktopModeDetail` applies,
`work.mode` holds that mode and `isCutSceneMode` answers true until a later
`setDesktopModeDetail` call replaces it.

## Log widgets in the cut scene modes

After the shared first arm, `setDesktopModeDetail` starts a set of local
flags at false and a draw priority local at 0.1, sets some of them in one
arm per mode, and then applies them all in a fixed order. These rows are read
from the decompiled body of the same decoded resource. PCs are not counted
here.

| Mode | Log flag | Log hide flag | Draw priority |
| ---: | --- | --- | ---: |
| 61 | true | true | 0.12 |
| 62 | false | false | 0.1 |
| 63 | true | true | 0.12 |

The apply sequence passes the log flag to `setStaticForceVisible` for static
widgets 2, 3 and 8 and stores it in `work.widgetEnableFlag[7]`. It stores the
log hide flag in `work.logHideFlag` and requests
`setLogEventHide(logHideFlag, true)` and `setLogPriority(false)`. Later in
the same sequence, `getStaticWidget(14)` receives `setDrawPriority` with the
priority local.

`DesktopWidget.setDefaultWidgetLocation` in the same file creates static
widget 2 with `createStaticWidget(2, "LogWidget", nil, 1, true, 1)` and static
widget 3 with `createStaticWidget(3, "LogWidget", "LogWidget2", 1, true, 2)`.

So modes 61 and 63 apply true to `setStaticForceVisible` for both log widgets
and set the log event hide, while mode 62 applies false to both. What
`setStaticForceVisible` and the native side draw for each value is outside
these bodies.

## Log event hide

`DesktopWidget.setLogEventHide(flag, force)` (connector `root/proto138`,
code start `0x145B7`) returns early when `force` is not true and either
static widget 2 answers `isForceHide()` with true or `work.logHideFlag` is
true. Otherwise it calls `setEventHide(flag)` on static widgets 2 and 3.
The cut scene arm passes `force` true, so the guards do not apply there.

`LogWidget.setEventHide(b)` (`widget/logwidget.lua`, `root/proto24`, code
start `0x2A46`) requests `setControlUserWorkInt(4, "Window_LogWidget", v)`
with v 1 for `b == true` and 0 otherwise. In
`widget/widgetbaseclass_common.lua`, `setControlUserWorkInt`
(`root/proto130`) forwards to `setUserWorkInt(index, nil, control, value)`
(`root/proto122`), which calls `setUserWork("IntData.Value", index, ...)`
(`root/proto183`). That method appends `tostring(index - 1)` to the prefix
and requests `_setProperty(nil, control, "IntData.Value3", value)` for
index 4.

The installed `widget/LogWidget.form` merges `widget/LogWidget.tpl` and uses
its `ControlTemplate_Window`. The triggers of that template react to
`IntData.Value3` of the window:

| Condition | Action |
| --- | --- |
| `IntData.Value3` 1, no keyboard focus within | sets `StringData.Value3` to 0 and `IntData.Value3` to 2 |
| `IntData.Value3` 1, keyboard focus within | sets `StringData.Value3` to 10 and `IntData.Value3` to 2 |
| `IntData.Value3` 2, `VisualOpacity` 1, no keyboard focus within | runs `LogWin.FadeOut5sec` |
| `IntData.Value3` 2, `VisualOpacity` 1, keyboard focus within | stops `LogWinFadeOut5sec` |
| `IntData.Value3` 0 and `IntData.Value0` 0 | stops `LogWinFadeOut5sec` and runs `Log.FadeIn` |

`LogWin.FadeOut5sec` starts five 0.2-second `DoubleAnimation`s of
`VisualOpacity` to 0, on the window and four named parts, each with a
`BeginTime` bound to `StringData.Value3`. A `LogChanged` routed event sets
`StringData.Value3` to 10 and runs `LogWin.FadeIn` and `Log.FadeIn`.
`LogWin.FadeIn` stops the fade-out and animates the window opacity to 1.

Read together, an event hide with no keyboard focus in the log fades the
window out after a begin time of 0, and a new log line brings it back with
a begin time of 10 for the next fade. The unit of the bound
`BeginTime` and the native animation clock are outside these files.

| Decoded path under `lua/scripts/` | Installed resource under `client/script/` | Wrapper bytes | Decoded bytes / SHA-256 |
| --- | --- | ---: | --- |
| `widget/logwidget.lua` | `n1635q/yv3n1635q.le.lpb` | 19090 | 19077 / `f40fdae854b956352b045242defcfbedf964944bd2219dc621f9f802600b9a91` |
| `widget/widgetbaseclass_common.lua` | `n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 | 32983 / `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |

| Installed SQWT resource | Container bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `widget/LogWidget.form` | 12323 / `0a5cf3d560a7fa4e32d6363a9a4efffba628ca45ec166af7b95c53243eae29fe` | 12315 / `a7c64d3fd69b4b2bdf5bfeadb6536d6d6052284afcd60f7baf252b1316707f88` |
| `widget/LogWidget.tpl` | 21543 / `1db2198b63cc37f8bbd6131e8029153a5a57bb529803bb865549f9e8a078c112` | 21535 / `508b182fba0991a501b3aa581044d1fdfe8620b2a114d541606bbe9a34d3effc` |

The SQWT files were decoded with the basename-keyed Blowfish cipher of
`xivl-tools:tools/blowfish.py`, as `xivl-tools:tools/research/census_sqwt.py`
does, and hashed before XML parsing.

## Limits

- The other flags that the later arms of `setDesktopModeDetail` write for
  each mode, and static widget 8, are not mapped here.
- Mode 64 has a level and counts as a cut scene mode, but the constants
  of `setDesktopModeDetail` do not include 64, so no arm of it names that
  mode.
- The native storage behind `work` and the caller identity of each method
  are not established by these bodies.
