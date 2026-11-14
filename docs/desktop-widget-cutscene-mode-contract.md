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

## Limits

- The per-widget flags that the later arms of `setDesktopModeDetail` write
  for each mode are not mapped here.
- Mode 64 has a level and counts as a cut scene mode, but the constants
  of `setDesktopModeDetail` do not include 64, so no arm of it names that
  mode.
- The native storage behind `work` and the caller identity of each method
  are not established by these bodies.
