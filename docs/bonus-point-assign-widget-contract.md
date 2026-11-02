# BonusPointAssignWidget local interaction contract

This page records the bounded local behavior recovered from the normal
`BonusPointAssignWidget` resource. It covers the root setup,
all 26 direct methods, and their own dynamic helper calls. It excludes the
same-named Ask resource, `BonusPointReductionWidget`, `WidgetBaseClass`,
callers, native bodies, other resources, runtime behavior, and service or wire
effects.

## Evidence and authentication

The original resource is
`client/script/n1635q/8vwpruv1wq9rr13wn1635q.le.lpb`, 16,038 bytes, SHA-256
`25184BD72F7F44425ED8223204201BE9D65E368090D7FC330F1B6DE107B601A3`.
The decoded payload is 16,025 bytes, SHA-256
`5015FA7B4B3F3AC323093329D0E7EB90EC638CB87270D1BAE89B53FFBEF99D65`.
The canonical LF source is
`lua/scripts/widget/bonuspointassignwidget.lua`, 42,304 bytes, 1,778 lines,
SHA-256
`55E33BCD0547A31A3AE37980E5385129845DBFBA5003E8F5E7980D70EC037978`.
The source identity is indexed by `manifests/scripts.json:15206-15211`.
The LPB and decoded identity are indexed by
`manifests/retail_lua_coverage.json:25938-25950`, and the normal class,
methods, and require path are indexed by `lua/registry.json:40130-40168`.

The pinned decompiler is
`tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
Reproduction uses `tools/retail_script.py` and the pinned unluac JAR above;
the source and payload identities are the hashes recorded here and in the
repository metadata locators.

The root prototype starts at decoded payload byte 32. It calls
`require("/Widget/WidgetBaseClass")` with `B=2,C=1` (zero result slots), then calls
`_defineClass("BonusPointAssignWidget","WidgetBaseClass")` with `B=3,C=1`.
It creates and attempts to bind exactly these 26 closures in registry order;
the root `GETGLOBAL`, closure, and `SETTABLE` operands are retained in the
instruction audit. A binding is an attempt and does not prove class
table identity or later dispatch.

## Method ledger

PC spans are zero-based instruction indices within each child prototype.
Byte spans are the first and last four-byte instruction words in the decoded
payload. `Debug` stores the original reader debug-line values; it is not a
zero-based source-line numbering claim. `Source` is the canonical source line
range. `Calls` counts direct `CALL` instruction sites in the method's original
words, not proven runtime reachability or calls made by a helper.

| # | Method | Source | Proto | Debug | Params/stack | PC span | Byte span | Words | Calls | Bounded result and behavior |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `init` | 11-349 | 0 | 54-149 | 1/33 | 0-246 | 1118-2102 | 247 | 35 | Returns zero values. Declares 28 integer16 work members, requests modal/tab/drag and command conditions, requests parameter title text, then calls `initParameter`. |
| 2 | `checkParameterUpdate` | 354-487 | 1 | 158-180 | 1/7 | 0-116 | 3835-4299 | 117 | 15 | Returns one false only when every fresh stock and parameter comparison is Lua-equal; every failed equality jump in the original chain returns one exact true. A final bare return word is present after the chain but is not reached by ordinary equality results. |
| 3 | `resetWork` | 492-624 | 2 | 187-226 | 1/7 | 0-115 | 4824-5284 | 116 | 15 | Returns zero values. Captures each `self.work` destination before its stock or parameter helper, writes the helper result to that captured table, then freshly reads `self.work` and Base stock fields for Assigning-stock attempts; a work replacement can leave the new physical Assigning stock nil. It attempts all twelve Assigning parameters as numeric zero. |
| 4 | `isAssigning` | 629-684 | 3 | 233-251 | 1/3 | 0-51 | 6096-6300 | 52 | 0 | Returns exactly one boolean: false only if all twelve Assigning members are Lua-equal to numeric zero; otherwise true. |
| 5 | `updateAssignButton` | 689-717 | 4 | 258-266 | 1/5 | 0-21 | 6589-6673 | 22 | 5 | Returns zero values. Exact true from `isAssigning` enables Complete and Redo; every other result disables both. |
| 6 | `updateRetakeButton` | 722-738 | 5 | 273-279 | 1/8 | 0-11 | 6789-6833 | 12 | 3 | Returns zero values. Gets the player and calls `player.isPassedBonusPointRetakeTime()` retaining two results; exact false requests Shake disabled, otherwise no UI request. |
| 7 | `updateDisplay` | 743-907 | 6 | 286-340 | 1/8 | 0-136 | 6981-7525 | 137 | 38 | Returns zero values. Requests physical stock display, six physical current-value operations, element stock display, then six element current-value operations in source order. |
| 8 | `getPhysicalBonusedParameter` | 912-929 | 7 | 350-356 | 3/10 | 0-12 | 8524-8572 | 13 | 3 | Gets the player, reads parameter `A1`, adds `A2`, and returns the one result of `player.processInitParameterFromBonusPoint(A1, sum)`. |
| 9 | `updateDisplayStockForPhysical` | 934-946 | 8 | 363-365 | 1/8 | 0-9 | 8729-8765 | 10 | 2 | Returns zero values. Converts the Assigning physical stock with open `tostring` results and requests Remaining_Status text. |
| 10 | `canAssignBonusPoint` | 951-972 | 9 | 375-384 | 3/7 | 0-16 | 8924-8988 | 17 | 3 | Returns exactly one boolean: for ordinary numeric operands it is true when the candidate is below the fresh maximum, and ordinary strings use lexical `<`; other operands may use a Lua `__lt` metamethod, while coercion and error behavior remain opaque here. |
| 11 | `updateDisplayStr` | 977-1002 | 10 | 391-397 | 1/9 | 0-20 | 9135-9215 | 21 | 4 | Returns zero values. Requests the calculated STR value and the string form of `strAssigning`. |
| 12 | `updateDisplayVit` | 1007-1032 | 11 | 404-410 | 1/9 | 0-20 | 9432-9512 | 21 | 4 | Returns zero values. Requests the calculated VIT value and the string form of `vitAssigning`. |
| 13 | `updateDisplayDex` | 1037-1062 | 12 | 417-423 | 1/9 | 0-20 | 9729-9809 | 21 | 4 | Returns zero values. Requests the calculated DEX value and the string form of `dexAssigning`. |
| 14 | `updateDisplayInt` | 1067-1092 | 13 | 430-436 | 1/9 | 0-20 | 10026-10106 | 21 | 4 | Returns zero values. Requests the calculated INT value and the string form of `intAssigning`. |
| 15 | `updateDisplayMnd` | 1097-1122 | 14 | 443-449 | 1/9 | 0-20 | 10323-10403 | 21 | 4 | Returns zero values. Requests the calculated MND value and the string form of `mndAssigning`. |
| 16 | `updateDisplayPie` | 1127-1152 | 15 | 456-462 | 1/9 | 0-20 | 10620-10700 | 21 | 4 | Returns zero values. Requests the calculated PIE value and the string form of `pieAssigning`. |
| 17 | `updateDisplayStockForElement` | 1157-1169 | 16 | 469-471 | 1/8 | 0-9 | 10917-10953 | 10 | 2 | Returns zero values. Converts the Assigning element stock with open `tostring` results and requests Remaining_Attribute text. |
| 18 | `updateDisplayFire` | 1174-1199 | 17 | 479-485 | 1/9 | 0-20 | 11114-11194 | 21 | 4 | Returns zero values. Requests the calculated FIRE value and the string form of `fireAssigning`. |
| 19 | `updateDisplayIce` | 1204-1229 | 18 | 492-498 | 1/9 | 0-20 | 11414-11494 | 21 | 4 | Returns zero values. Requests the calculated ICE value and the string form of `iceAssigning`. |
| 20 | `updateDisplayWind` | 1234-1259 | 19 | 505-511 | 1/9 | 0-20 | 11711-11791 | 21 | 4 | Returns zero values. Requests the calculated WIND value and the string form of `windAssigning`. |
| 21 | `updateDisplayEarth` | 1264-1289 | 20 | 518-524 | 1/9 | 0-20 | 12011-12091 | 21 | 4 | Returns zero values. Requests the calculated EARTH value and the string form of `earthAssigning`. |
| 22 | `updateDisplayThunder` | 1294-1319 | 21 | 531-537 | 1/9 | 0-20 | 12314-12394 | 21 | 4 | Returns zero values. Requests the calculated THUNDER value and the string form of `thunderAssigning`. |
| 23 | `updateDisplayWater` | 1324-1349 | 22 | 545-551 | 1/9 | 0-20 | 12623-12703 | 21 | 4 | Returns zero values. Requests the calculated WATER value and the string form of `waterAssigning`. |
| 24 | `processUICommandOperate` | 1354-1742 | 23 | 563-725 | 5/24 | 0-341 | 12926-14290 | 342 | 45 | Returns zero values. Cancel requests `closeWidgetDirect` and returns immediately; Shake requests `openChildWidget`; Redo requests `initParameter`; Complete requests `executePlayerBonusPointAssign` with twelve computed values plus four zero padding arguments, then requests `closeWidgetDirect`; PointPlus commands independently gate, attempt local increments, request display operations, and attempt local stock decrements before the final button request. |
| 25 | `initParameter` | 1747-1761 | 24 | 732-737 | 1/3 | 0-8 | 15760-15792 | 9 | 4 | Returns zero values and calls `resetWork`, `updateDisplay`, `updateAssignButton`, `updateRetakeButton` in that order. |
| 26 | `updateParameter` | 1766-1776 | 25 | 744-748 | 1/3 | 0-6 | 15918-15942 | 7 | 2 | Returns zero values. Exact true from `checkParameterUpdate` requests `initParameter`; every other result does nothing. |

## Direct call matrix

Each entry gives the actual dynamic receiver and explicit arguments. `->0`
means `C=1` requests zero result slots, `->1` means `C=2` requests one
retained result, `->2` means `C=3` requests two retained results, and `->open`
means `C=0` preserves the called function's result width. No `->0` call first
obtains a result tuple. The enclosing method's return width is stated in the
ledger and is separate from helper call width.
All repeated calls below are independent source call sites in the indicated
order; no native implementation is inferred.

In this matrix, `self.f(args)`, `player.f(args)`, `worldMaster.f(args)`, and
`desktopWidget.f(args)` abbreviate the actual call `f(receiver,args)`, with
the receiver occupying the first Lua argument slot (an empty `args` list means
the receiver is the sole argument). A global `tostring(x)`
has no implicit receiver. Unquoted control, property, and command tokens in
call tuples are literal strings exactly as spelled in the source.
Every `work` member and global read described here occurs at its original
operand or call point; the contract does not cache, coalesce, or normalize
independent reads. Compositions require the selected pinned closures and
normal completion of each intervening access and call.

`T(x)` below means the complete open result tuple from the immediately
preceding global `tostring(x)` call; it is the actual final argument sequence,
not a forced one-result conversion or a new field read. Thus an invocation written with `T(x)`
has `B=0,C=1` and forwards every result returned by that `tostring` call.
Each `T(x)` site captures its `_setProperty` function and receiver by the
original `SELF` instruction immediately before `tostring(x)`. This applies to
stock display (proto 8), current display (proto 6), and parameter display
(proto 10); a setter, global `tostring`, work-table, or helper replacement
during conversion does not replace the captured call.
In the Complete row, `G1` through `G12` mean the single retained results of
the explicitly listed `player.getBonusPointAtPhysicalParameter(1)` through
`(12)` calls at that same source site; they are computed values, not omitted
arguments. The Complete `desktopWidget` receiver and each local
`work.<field>Assigning` value are captured before that field's getter/add pair;
the later `closeWidgetDirect` reloads `desktopWidget` at its own global lookup.

| Method | Complete direct calls, in source order |
|---|---|
| `init` | `self.setModal(true) ->0`; `self.setProperty(IsHitTestVisible,true) ->0`; `self.setProperty(IsTabStop,true) ->0`; `self.setProperty(DragMode,"CanDrag") ->0`; `self.setCancelCondition() ->0`; `self.setConfirmCondition(Button_Cancel) ->0`; `self.setConfirmCondition(Button_Redo) ->0`; `self.setConfirmCondition(Button_Shake) ->0`; `self.setConfirmCondition(Button_Complete) ->0`; `self.setCloseCondition(Button_Close) ->0`; `self.setConfirmCondition(Button_PointPlus_STR) ->0`; `self.setConfirmCondition(Button_PointPlus_VIT) ->0`; `self.setConfirmCondition(Button_PointPlus_DEX) ->0`; `self.setConfirmCondition(Button_PointPlus_INT) ->0`; `self.setConfirmCondition(Button_PointPlus_MND) ->0`; `self.setConfirmCondition(Button_PointPlus_PIE) ->0`; `self.setConfirmCondition(Button_PointPlus_FIRE) ->0`; `self.setConfirmCondition(Button_PointPlus_ICE) ->0`; `self.setConfirmCondition(Button_PointPlus_WIND) ->0`; `self.setConfirmCondition(Button_PointPlus_EARTH) ->0`; `self.setConfirmCondition(Button_PointPlus_THUNDER) ->0`; `self.setConfirmCondition(Button_PointPlus_WATER) ->0`; `self.setText(TextBlock_ParameterTitle_STR,6911,1) ->0`; `self.setText(TextBlock_ParameterTitle_VIT,6911,2) ->0`; `self.setText(TextBlock_ParameterTitle_DEX,6911,3) ->0`; `self.setText(TextBlock_ParameterTitle_MND,6911,5) ->0`; `self.setText(TextBlock_ParameterTitle_INT,6911,4) ->0`; `self.setText(TextBlock_ParameterTitle_PIE,6911,6) ->0`; `self.setText(TextBlock_ParameterTitle_FIRE,6911,7) ->0`; `self.setText(TextBlock_ParameterTitle_WATER,6911,12) ->0`; `self.setText(TextBlock_ParameterTitle_THUNDER,6911,11) ->0`; `self.setText(TextBlock_ParameterTitle_WIND,6911,9) ->0`; `self.setText(TextBlock_ParameterTitle_EARTH,6911,10) ->0`; `self.setText(TextBlock_ParameterTitle_ICE,6911,8) ->0`; `self.initParameter() ->0`. |
| `checkParameterUpdate` | `worldMaster._getMyPlayer() ->1`; `player.getBonusPointStockForPhysical() ->1`; if equal, `player.getBonusPointStockForElement() ->1`; if that is equal, `self.getPhysicalBonusedParameter(1,0) ->1`; `self.getPhysicalBonusedParameter(2,0) ->1`; `self.getPhysicalBonusedParameter(3,0) ->1`; `self.getPhysicalBonusedParameter(4,0) ->1`; `self.getPhysicalBonusedParameter(5,0) ->1`; `self.getPhysicalBonusedParameter(6,0) ->1`; `self.getPhysicalBonusedParameter(7,0) ->1`; `self.getPhysicalBonusedParameter(8,0) ->1`; `self.getPhysicalBonusedParameter(9,0) ->1`; `self.getPhysicalBonusedParameter(10,0) ->1`; `self.getPhysicalBonusedParameter(11,0) ->1`; `self.getPhysicalBonusedParameter(12,0) ->1`, each independently reached only while preceding comparisons are equal. |
| `resetWork` | `worldMaster._getMyPlayer() ->1`; captures a destination `self.work` immediately before each stock or parameter helper, including the stock p2 PCs 3-6 and parameter p2 PCs 11/15-16 target/write pairs, then writes that helper result to the captured table; the later Assigning-stock writes freshly read `self.work` as both destination and Base source. Thus a helper can write physical stock 7 to an old table while a replacement table has no physical Assigning stock. It attempts all twelve Assigning parameters as numeric zero. |
| `isAssigning` | No direct calls. |
| `updateAssignButton` | `self.isAssigning() ->1`; on exact true, `self.setEnable(Button_Complete,true) ->0` and `self.setEnable(Button_Redo,true) ->0`; otherwise the same two calls use literal false. |
| `updateRetakeButton` | `worldMaster._getMyPlayer() ->1`; `player.isPassedBonusPointRetakeTime() ->2`; exact false then `self.setEnable(Button_Shake,false) ->0`. |
| `updateDisplay` | `self.updateDisplayStockForPhysical() ->0`; `tostring(work.strBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_STR,Text,T(work.strBase)) ->0`; `self.updateDisplayStr() ->0`; `tostring(work.vitBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_VIT,Text,T(work.vitBase)) ->0`; `self.updateDisplayVit() ->0`; `tostring(work.dexBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_DEX,Text,T(work.dexBase)) ->0`; `self.updateDisplayDex() ->0`; `tostring(work.intBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_INT,Text,T(work.intBase)) ->0`; `self.updateDisplayInt() ->0`; `tostring(work.mndBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_MND,Text,T(work.mndBase)) ->0`; `self.updateDisplayMnd() ->0`; `tostring(work.pieBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_PIE,Text,T(work.pieBase)) ->0`; `self.updateDisplayPie() ->0`; `self.updateDisplayStockForElement() ->0`; `tostring(work.fireBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_FIRE,Text,T(work.fireBase)) ->0`; `self.updateDisplayFire() ->0`; `tostring(work.iceBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_ICE,Text,T(work.iceBase)) ->0`; `self.updateDisplayIce() ->0`; `tostring(work.windBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_WIND,Text,T(work.windBase)) ->0`; `self.updateDisplayWind() ->0`; `tostring(work.earthBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_EARTH,Text,T(work.earthBase)) ->0`; `self.updateDisplayEarth() ->0`; `tostring(work.thunderBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_THUNDER,Text,T(work.thunderBase)) ->0`; `self.updateDisplayThunder() ->0`; `tostring(work.waterBase) ->open`, then `self._setProperty(nil,TextBlock_CurrentValue_WATER,Text,T(work.waterBase)) ->0`; `self.updateDisplayWater() ->0`. Every `_setProperty` uses `B=0,C=1`. |
| `getPhysicalBonusedParameter` | `worldMaster._getMyPlayer() ->1`; `player.getBonusPointAtPhysicalParameter(A1) ->1`; `player.processInitParameterFromBonusPoint(A1,current+A2) ->1`. |
| `updateDisplayStockForPhysical` | `tostring(work.stockForPhysicalAssigning) ->open`; `self._setProperty(nil,TextBlock_Remaining_Status,Text,T(work.stockForPhysicalAssigning)) ->0` with `B=0,C=1`. |
| `canAssignBonusPoint` | `self.getPhysicalBonusedParameter(A1,A2) ->1`; `worldMaster._getMyPlayer() ->1`; `player.getParameterMaxFromBonusPoint() ->1`. |
| `updateDisplayStr` | `self.getPhysicalBonusedParameter(1,work.strAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_STR,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.strAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_STR,Text,T(work.strAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayVit` | `self.getPhysicalBonusedParameter(2,work.vitAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_VIT,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.vitAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_VIT,Text,T(work.vitAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayDex` | `self.getPhysicalBonusedParameter(3,work.dexAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_DEX,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.dexAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_DEX,Text,T(work.dexAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayInt` | `self.getPhysicalBonusedParameter(4,work.intAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_INT,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.intAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_INT,Text,T(work.intAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayMnd` | `self.getPhysicalBonusedParameter(5,work.mndAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_MND,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.mndAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_MND,Text,T(work.mndAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayPie` | `self.getPhysicalBonusedParameter(6,work.pieAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_PIE,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.pieAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_PIE,Text,T(work.pieAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayStockForElement` | `tostring(work.stockForElementAssigning) ->open`; `self._setProperty(nil,TextBlock_Remaining_Attribute,Text,T(work.stockForElementAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayFire` | `self.getPhysicalBonusedParameter(7,work.fireAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_FIRE,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.fireAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_FIRE,Text,T(work.fireAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayIce` | `self.getPhysicalBonusedParameter(8,work.iceAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_ICE,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.iceAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_ICE,Text,T(work.iceAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayWind` | `self.getPhysicalBonusedParameter(9,work.windAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_WIND,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.windAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_WIND,Text,T(work.windAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayEarth` | `self.getPhysicalBonusedParameter(10,work.earthAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_EARTH,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.earthAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_EARTH,Text,T(work.earthAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayThunder` | `self.getPhysicalBonusedParameter(11,work.thunderAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_THUNDER,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.thunderAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_THUNDER,Text,T(work.thunderAssigning)) ->0` with `B=0,C=1`. |
| `updateDisplayWater` | `self.getPhysicalBonusedParameter(12,work.waterAssigning) ->1`; `self._setProperty(nil,TextBlock_AfterUseValue_WATER,Text,the single result from that call) ->0` with `B=6,C=1`; `tostring(work.waterAssigning) ->open`; `self._setProperty(nil,TextBlock_UsePoint_WATER,Text,T(work.waterAssigning)) ->0` with `B=0,C=1`. |
| `processUICommandOperate` | `desktopWidget.closeWidgetDirect(self) ->0` on Cancel and again after Complete; `desktopWidget.openChildWidget("BonusPointReductionWidget",self,true) ->0` on Shake; `self.initParameter() ->0` on Redo; Complete first calls `worldMaster._getMyPlayer() ->1`, then captures the `desktopWidget` receiver and `executePlayerBonusPointAssign` function before the twelve field-before-getter/add pairs, independently calls `player.getBonusPointAtPhysicalParameter(1) ->1`, `player.getBonusPointAtPhysicalParameter(2) ->1`, `player.getBonusPointAtPhysicalParameter(3) ->1`, `player.getBonusPointAtPhysicalParameter(4) ->1`, `player.getBonusPointAtPhysicalParameter(5) ->1`, `player.getBonusPointAtPhysicalParameter(6) ->1`, `player.getBonusPointAtPhysicalParameter(7) ->1`, `player.getBonusPointAtPhysicalParameter(8) ->1`, `player.getBonusPointAtPhysicalParameter(9) ->1`, `player.getBonusPointAtPhysicalParameter(10) ->1`, `player.getBonusPointAtPhysicalParameter(11) ->1`, and `player.getBonusPointAtPhysicalParameter(12) ->1`, invokes the captured function with its receiver and twelve computed values plus four zero padding arguments, then reloads `desktopWidget` for `closeWidgetDirect(self) ->0`; each physical PointPlus arm calls `self.canAssignBonusPoint(1,work.strAssigning) ->1`, `self.canAssignBonusPoint(2,work.vitAssigning) ->1`, `self.canAssignBonusPoint(3,work.dexAssigning) ->1`, `self.canAssignBonusPoint(4,work.intAssigning) ->1`, `self.canAssignBonusPoint(5,work.mndAssigning) ->1`, and `self.canAssignBonusPoint(6,work.pieAssigning) ->1` independently, and an exact true result increments its member and calls the matching display method (`updateDisplayStr`, `updateDisplayVit`, `updateDisplayDex`, `updateDisplayInt`, `updateDisplayMnd`, `updateDisplayPie`) `->0`; if any physical arm succeeded, `self.updateDisplayStockForPhysical() ->0` follows the stock decrement; the element arms call `self.canAssignBonusPoint(7,work.fireAssigning) ->1`, `self.canAssignBonusPoint(8,work.iceAssigning) ->1`, `self.canAssignBonusPoint(9,work.windAssigning) ->1`, `self.canAssignBonusPoint(10,work.earthAssigning) ->1`, `self.canAssignBonusPoint(11,work.thunderAssigning) ->1`, and `self.canAssignBonusPoint(12,work.waterAssigning) ->1` independently, exact true increments and calls the matching Fire/Ice/Wind/Earth/Thunder/Water display `->0`, and any success calls `self.updateDisplayStockForElement() ->0`; each stock block is skipped when its stock is zero; all non-Cancel paths finish with `self.updateAssignButton() ->0`. |
| `initParameter` | `self.resetWork() ->0`; `self.updateDisplay() ->0`; `self.updateAssignButton() ->0`; `self.updateRetakeButton() ->0`. |
| `updateParameter` | `self.checkParameterUpdate() ->1`; exact true then `self.initParameter() ->0`. |

The matrix uses `T(x)` only to denote the open-result tuple forwarded by the
immediately preceding `tostring(x)` call; these are `B=0,C=1` calls, not
forced one-result conversions. The `processUICommandOperate` matrix lists all
twelve getter sites and all twelve guard sites by explicit index, preserving
direct receiver and argument order. Branches that are not taken do not make
their listed calls.

## Local work state and branch contract

`init` attempts a `_temp` declaration table with exactly these 28
`integer16` names, in order: `stockForPhysicalBase`,
`stockForElementBase`, `strBase`, `vitBase`, `dexBase`, `intBase`, `mndBase`,
`pieBase`, `fireBase`, `iceBase`, `windBase`, `earthBase`, `thunderBase`,
`waterBase`, `stockForPhysicalAssigning`, `stockForElementAssigning`,
`strAssigning`, `vitAssigning`, `dexAssigning`, `intAssigning`, `mndAssigning`,
`pieAssigning`, `fireAssigning`, `iceAssigning`, `windAssigning`,
`earthAssigning`, `thunderAssigning`, `waterAssigning`.

`resetWork` captures each `self.work` destination before its stock or parameter
helper call, including the stock p2 PCs 3-6 and parameter p2 PCs 11/15-16
target/write pairs, then later reads `self.work` and its Base stock fields
afresh for the Assigning-stock attempts. It sets all Assigning parameters to numeric zero.
The Base parameter order is
STR=1, VIT=2, DEX=3, INT=4, MND=5, PIE=6, FIRE=7, ICE=8, WIND=9, EARTH=10,
THUNDER=11, WATER=12. `getPhysicalBonusedParameter` uses the fresh current
player value plus the supplied increment before the processing helper.

`processUICommandOperate(A0,A1,A2,A3,A4)` uses only `A2` as its selector;
`A1`, `A3`, and `A4` are unused by this body. It compares `A2` with the full
literal controls `Button_Cancel`, `Button_Shake`, `Button_Redo`,
`Button_Complete`, and the twelve `Button_PointPlus_*` strings. Cancel requests
`desktopWidget.closeWidgetDirect(A0)` and returns before any later guard.
Shake requests `desktopWidget.openChildWidget("BonusPointReductionWidget",A0,true)`;
Redo requests `A0.initParameter()` and then, after the independent stock
blocks, the final `A0.updateAssignButton()` request; neither branch returns
early. Complete first gets `worldMaster._getMyPlayer()`, then captures one fresh
`desktopWidget` receiver and its `executePlayerBonusPointAssign` function.
It independently captures each local Assigning field immediately before its
player getter/add pair for parameters 1 through 12, computes the twelve local
sums, and requests
`desktopWidget.executePlayerBonusPointAssign` with those twelve values followed
by four literal zeros (`B=18,C=1`), then performs a fresh global
`desktopWidget` lookup for `closeWidgetDirect(A0)`.

After those selector branches, the physical block first reads
`A0.work.stockForPhysicalAssigning` and continues only when `0 <` that value;
the physical counter is initialized to numeric zero at PC111. At PC121, an
exact successful selector sets it to numeric one before the fresh target/source
reads, store, and display calls. Each physical control
has an independent exact `A2` comparison. Its
`A0.canAssignBonusPoint(index,A0.work.<field>Assigning)` call retains one
result, and only exact true sets the local counter to numeric one before a
fresh target-work read, source-field read, addition, Assigning store attempt,
and matching display request. If the counter is greater than zero, a fresh
stock read attempts subtraction by that counter and the stock-display request
follows. The element block then independently reads
`A0.work.stockForElementAssigning`, applies the same `0 <` predicate and
counter sequence to indices 7 through 12, and requests the element stock
display only after a successful counter. Unknown `A2` controls fall through
both blocks and still reach the final `A0.updateAssignButton()` request. The
normal widths are the matrix widths; only Cancel omits that final request.

The guard is Lua `<`: two numeric operands use strict numeric order, and two
strings use lexical order. Other operands may invoke `__lt`; unsupported
metamethod, coercion, and error behavior remains opaque here. A candidate equal
to a numeric maximum is rejected. `isAssigning` uses
exact Lua equality to numeric zero; nil, false, and nonzero values are not
numeric zero.
The update and check methods preserve Lua's zero-result versus one-result
distinction. `checkParameterUpdate` has a statically present bare return word
after its conditional chain, but each ordinary failed equality jump reaches
the one-true return; the focused original-word fixtures exercise the false
all-equal and true mismatch vectors.

## Boundaries and fixture receipt

The source and decoded words establish local declaration attempts, reads,
Lua work assignment attempts, helper calls, UI requests, branch order, fixed call widths, open
returns, and the four zero padding arguments. They do not establish native
storage, actual UI rendering, focus, allocation lifetime, authoritative stat
mutation, reset eligibility, caller construction, historical invocation,
server acceptance, transaction settlement, or any behavior of opaque helper
bodies. Dynamic helper lookup, metamethods, callable objects, coercion, and
errors can stop a method before its normal result.

The focused original-word fixture check executes the authenticated words
through a bounded Lua-aware interpreter and asserts all 26 prototype spans,
direct call counts, all 28 declaration cells, recursively typed dictionary
keys and values, distinct Table identity, raw reset destinations including a
same-label redirect, typed reset and PointPlus write vectors, captured setter
and Complete function/receiver/self identities, valid float-equivalent getter
indices, the full getter-to-execute-to-close-to-button trace, exact boolean
versus numeric values, the all-equal false and first/later mismatch true
vectors, strict retake and assignment gates, zero-stock STR and FIRE skips,
Cancel, Shake, Redo, PointPlus success/failure, Complete's 17 operands, and
the init/update callback order. In-memory negative controls reject
declaration, recursive type, write, getter, padding, callback-order,
stock-gate, table-identity, and lookup-replacement corruption. It uses
explicit helper returns and ordinary tables; it does not model native
implementations, metamethods, callable objects, general coercion, dynamic
class binding, UI/render/focus/lifetime, caller behavior, server or settlement
behavior, or all possible error paths.
