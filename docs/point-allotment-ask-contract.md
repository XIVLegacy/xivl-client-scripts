# Point allotment Ask contract

`BonusPointCommand.operateUI` opens the Ask resource
`Ask/BonusPointAssignWidget` and turns its answer into six attribute totals.
This page records that command, the Ask widget's conditions, operations and
result, the installed form it drives, and the `WidgetBaseClass` Boolean
helper its enable test reads through. The normal, non-Ask
`BonusPointAssignWidget` is a separate resource with its own
[contract](bonus-point-assign-widget-contract.md).

## Command

`BonusPointCommand` (`command/game/bonuspointcommand.lua`) defines
`operateUI(self, a1, a2, a3, a4, a5, a6, a7, a8, a9)` (`:29-85`). It computes
`a2 - (a4 + a5 + a6 + a7 + a8 + a9)` and calls
`desktopWidget:askEventModeWidgetYield("Ask/BonusPointAssignWidget", 7,
remaining, a3, a4, a5, a6, a7, a8, a9)`. It returns the first answer and six
totals: for each of the six answers after the first two, `a4` to `a9` plus
that answer when the answer is not nil and at least 0, else `a4` to `a9`
unchanged. `a1` is not read.

## Ask widget

`BonusPointAssignWidget` in `widget/ask/bonuspointassignwidget.lua` derives
from `AskBaseClass`.

| Method | Lines | Behavior |
| --- | --- | --- |
| `initAsk` | `:11-488` | Stores its first argument as `totalRemainingBonusDefault` and `totalRemainingBonus`, its third to eighth as the six `CumulateAddBonus` values, and the second argument less each cumulative value as the six `AddBonusLimit` values. It calls `setConfirmCondition` for `Button_PointMinus_STR` to `_PIE`, `Button_PointPlus_STR` to `_PIE`, `Button_Redo`, `Button_Complete` and `Button_Cancel` (`:231-290`). |
| `initWindowDisplay` | `:491-559` | Zeroes the six `AddBonus` values, disables Redo and Complete and calls `setWindowFocus("Button_PointPlus_STR")`. |
| `setWindowFocus` | `:1462-1482` | Calls `setLogicalFocus` with the name, and `setKeyboardFocusedControl` when the widget holds the keyboard focus. |
| `execBonusPointPlusButton` | `:1261-1367` | Adds one to the Button's `AddBonus` while it is below its `AddBonusLimit` and `totalRemainingBonus` is above 0, and takes one from `totalRemainingBonus`. |
| `execBonusPointMinusButton` | `:1370-1459` | Takes one from the Button's `AddBonus` while it is above 0 and adds one to `totalRemainingBonus`. |
| `processUICommandOperate` | `:1485-1581` | For `Button_Redo`, when `getEnable("Button_Redo")` is exactly true, runs `initWindowDisplay` and `updateWindowDisplay` and returns. A PointMinus or PointPlus name runs the matching handler. `Button_Complete` stores the ask result 1 and `Button_Cancel` -1 through `setBaseAskResult` and return. Otherwise it enables Redo and Complete when the six `AddBonus` values sum above 0, disables them otherwise, and runs `updateWindowDisplay`. |
| `getAskResult` | `:1584-1611` | Returns false for the ask result -1 and true otherwise, then the six `AddBonus` values. |

INFERRED. `askEventModeWidgetYield` passes the eight values after the literal
7 to `initAsk`, so the first is the points left, the second the per-attribute
cap and the rest the points already spent. `getAskResult` supplies the
answers `operateUI` reads after its first two.

## WidgetBaseClass Boolean read

`WidgetBaseClass.getEnable(control)` returns
`getBoolean(getControlProperty(control, "IsEnabled"))`
(`widget/widgetbaseclass_common.lua:1644-1657`). `getBoolean` returns true
only when its argument equals the text `"True"` and false for any other value
(`:3351-3361`).

## Installed form

The form `client/sqwt/widget/BonusPointAssignWidget.form` (17320 stored
bytes, SHA256
`6F30C2B95A3879F24B995A29E89359B92BDBCD0423B8CAD17CA65CC377892943`, 17312
decoded bytes, SHA256
`DB5F384DE3BA603ED50FBD372974618AA169D0ECCB2A54EAFEB3F35B0398B6CC`) has the
root `Window_BonusPointAssignWidget` and declares 15 Buttons in this document
order: `Button_Redo` (`@6905`), then `Button_PointMinus_X` and
`Button_PointPlus_X` for STR, VIT, DEX, INT, MND and PIE, then
`Button_Complete` (`@6903`) and `Button_Cancel` (`@6904`). Every one declares
`Command="UILuaCommands.Operate"` and no `CommandParameter` or
`CommandTarget`. The twelve point Buttons declare no `Width`, `Height` or
`Content` and take the styles `BTN_basis_pointMinus` and
`BTN_basis_pointPlus`.

In `client/sqwt/common/default.style` (353783 stored bytes, SHA256
`632B314CB2257FCBEE42D4B002989A58DFEB42E64AF864C1F5356336DC233DC0`, 353775
decoded bytes, SHA256
`33BB178C3B172C62EEB65E8BCAF94F701A0EC3921564E27A619516900896D9F6`) the
`Frame` part of `BTN_basis_pointPlus` (decoded line 1469) draws
`BTN_basis_pointPlus_N` for `SkinNormal` and `SkinDisabled`,
`BTN_basis_pointPlus_H` for `SkinHover`, `SkinActive` (offset `1,1`),
`SkinAnchored` and `SkinReserved`, and `NULL` for `SkinFocused` and
`SkinDroppable`. `BTN_basis_pointMinus` (decoded line 1481) has the same
shape with the `pointMinus` skins.

INFERRED. A click on any of the 15 Buttons raises `UILuaCommands.Operate`
with no markup parameter, and the confirm conditions of `initAsk` admit it
to `processUICommandOperate`. The size a point Button arranges to is not set
by markup, and the native rule that sizes it is not established here.

## Source identity

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule, and
the original resources matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `widget/ask/bonuspointassignwidget.lua` | 35622 / 1611 | `56C32C14E99D7871D60E0EDBDD1B7EAF059EA73127A3712335CBE072683EAEBF` |
| `command/game/bonuspointcommand.lua` | 1922 / 85 | `1D5291268D165302FA646E5BD85283F550E90E9036D20667566BF15348B30A0B` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/9rz/8vwpruv1wq9rr13wn1635q.le.lpb` | 13987 / `AC1C71F341F9A916BF9A37480D592CB42F5F55462F3FA8BF7BADE62C5AA2ABC3` | 13974 / `3F4BC4BE586F7EBE92EAD3C74984AF693EBF5DD1C1B7F154E2634D3424A67035` |
| `7vxx9w6/39x5/8vwpruv1wq7vxx9w6.le.lpb` | 812 / `994FF794818919429B5463DC46CCB5585F450F13A2748F2D2D1AE4359460B781` | 799 / `C6BA7C57D22E5272F94574985C5788AC93C9A63E26C08B22B8E0FEEF44C7162A` |

Decode each resource with `tools/retail_script.py` and the pinned unluac JAR,
and read the methods at the lines above. Decode the form and style with
`xivl extract-resource` and read the Button and `SqwtStyle` elements.
