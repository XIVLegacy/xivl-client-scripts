# Cut scene caption script route

The native caption clip ends in `_onShowUIClip` at its start and
`_onHideUIClip` at its end, both with the tag `Caption` and the clip's
actor-class word. This page records how the shipped scripts turn those two
callbacks into writes of the `TextBlock_Caption` block of static widget 9.
The native route, the clip timing and the widget markup are in
`xivl-decomp:docs/resource/cut-caption-actor-bindings.md`. Rendering, text
resolution and live behavior are outside this page.

## Source identity

The inputs are three installed resources of client extraction
`2012.09.19.0001`, authenticated against the
[coverage manifest](../manifests/retail_lua_coverage.json).

| Decoded path under `lua/scripts/` | Installed resource under `client/script/` | Wrapper bytes | Decoded bytes / SHA-256 |
| --- | --- | ---: | --- |
| `gamedata/cutscene_common.lua` | `39x569q9/7pqr75w5_7vxxvw.le.lpb` | 9125 | 9112 / `7ef33408c579f2d1ede120d9751851bd39b77dd1b6ca6a0aa821b413fe11b4fd` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/captionwidget.lua` | `n1635q/79uq1vwn1635q.le.lpb` | 819 | 806 / `3d7c3d94a7de07ac7e0ff303a4061cae4482255a7f992e76f4fa1ead6916f9d6` |

`tools/retail_script.py` decoded each LPB. `ChunkReader` and `instruction`
from `tools/build_quest_contracts.py` read the prototypes. Prototype IDs and
PCs are zero-based, a code start is the byte offset of the first instruction
in the decoded payload, and operand counts include the receiver.

| Method | Prototype / code start / PCs |
| --- | --- |
| `CutScene._onShowUIClip` | `root/proto3` / `0x0CBE` / 303, variadic after three fixed operands |
| `CutScene._onHideUIClip` | `root/proto4` / `0x1333` / 14 |
| `DesktopWidget.setDefaultWidgetLocation` | `root/proto142` / `0x14908` / 181 |
| `DesktopWidget.showCaption` | `root/proto197` / `0x19BA8` / 16, variadic after four fixed operands |
| `DesktopWidget.hideCaption` | `root/proto198` / `0x19C50` / 8 |
| `CaptionWidget.setCaptionText` | `root/proto1` / `0x019B` / 6, variadic after three fixed operands |
| `CaptionWidget.removeCaptionText` | `root/proto2` / `0x01EB` / 3 |
| `CaptionWidget.setCaption` | `root/proto3` / `0x0232` / 9, variadic after three fixed operands |
| `CaptionWidget.removeCaption` | `root/proto4` / `0x02B1` / 7 |

## Show

The operands of `_onShowUIClip` after the receiver are the tag `A1`, the
actor-class word `A2` and the variadic tail. PCs 0-3 take the caption branch
when `A1` equals `Caption` or `CaptionClip`. PCs 4-7 replace `A2` with
`self:getNameByActorClass(A2)`. PCs 8-11 take the first tail value through
`select(1, ...)`. PCs 12-22 call

```text
desktopWidget:showCaption(name, self.work.textOwner, first, select(2, ...))
```

`showCaption` jumps over an unreachable `RETURN` at PCs 0-1. PCs 2-9 return
when `self:getStaticWidget(9):isShow()` equals false. PCs 10-14 call
`setCaptionText(A2, A3, ...)` on that widget, so the resolved name in `A1` is
not passed on.

`setCaptionText` calls `self:setCaption(A1, A2, ...)` (PCs 0-4), and
`setCaption` calls

```text
self:_setProperty(nil, "TextBlock_Caption", "Text", textOwner, textOperand, ...)
```

at PCs 0-7.

## Hide

`_onHideUIClip` takes the tag `A1` and the actor-class word `A2`. PCs 0-3 take
the caption branch for `Caption` or `CaptionClip`, and PCs 4-6 call
`desktopWidget:hideCaption()`. The `PlaneMap` branch at PCs 8-12 calls
`closeMapForCutScene`. The actor-class word is not read.

`hideCaption` skips the same unreachable `RETURN` and calls
`self:getStaticWidget(9):removeCaptionText()` at PCs 2-6.
`removeCaptionText` calls `self:removeCaption()`, and `removeCaption` calls
`self:_setProperty(nil, "TextBlock_Caption", "Text", "")` at PCs 0-5.

## Static widget 9

`setDefaultWidgetLocation` PCs 82-88 call
`self:createStaticWidget(9, "CaptionWidget", nil, 1, true)`.

## Reproduction

Decode each resource with `tools/retail_script.py`, read the root prototype
with `ChunkReader`, map each `CLOSURE` to the constant key of the `SETTABLE`
that stores it, and list the selected child prototype's instructions with
`instruction`.
