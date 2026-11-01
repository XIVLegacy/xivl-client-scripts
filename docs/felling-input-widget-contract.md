# FellingInputWidget local interaction contract

This bounded contract describes the local Lua behavior recovered from the one
retail `FellingInputWidget` resource. It covers the receiver's work-table
inputs, phase and gauge requests, command-result values, and owner-message and
sweetspot continuations. Calls are requests to selected local or native
helpers; they do not prove storage, rendering, focus ownership, widget
lifetime, gathering acceptance, inventory or currency mutation, server policy,
or transaction completion.

Named self-method compositions below require the selected pinned local closure
and normal completion of each nested call. Inherited, desktop, native, and
other helper bindings remain conditional dependencies. The notation
`self.f(x)` abbreviates the actual Lua argument tuple `f(self,x)`; global calls
such as `tostring(x)` and `_math.floor(x)` have no implicit receiver.

## Reproducibility and public identity

The authenticated resource and generated source identity are:

- LPB: `client/script/n1635q/9rz/45yy1w31wupqn1635q.le.lpb`, 9497 bytes,
  SHA-256
  `DDF14ABD25CB93F23D920D99F16743B8E397FC8DA8A5EAF5654F7D90E26A2240`.
- Decoded Lua 5.1 payload: 9484 bytes, SHA-256
  `578C4CF2E43A1ABD5136459C91438FF056B06E9D3815B68980B31ABB656409F4`.
- Canonical LF source:
  `lua/scripts/widget/ask/fellinginputwidget.lua`, 23717 bytes, 1061 lines,
  SHA-256
  `4A2AEBEDCF71F0FA37386490ED91AA6369FB0F18031F1A395BCD854579C86B81`.
- Decoder route: `xivl-client-scripts:tools/retail_script.py`.
- Pinned unluac JAR:
  `xivl-client-scripts:tools/vendor/unluac/unluac_2025_12_23.jar`, 796256
  bytes, SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.

The manifest records the canonical source at
`xivl-client-scripts:manifests/scripts.json:14912-14917`. The retail resource
and decoded payload pins are at
`xivl-client-scripts:manifests/retail_lua_coverage.json:26417-26431`. The
registry records class, method order, required base path, and 1061-line source
at `xivl-client-scripts:lua/registry.json:38616-38647`.

The root makes one `require("/Widget/Ask/AskBaseClass")` call with
`B=2,C=1`, then one `_defineClass("FellingInputWidget","AskBaseClass")`
call with `B=3,C=1`. It makes 20 method-name `SETTABLE` attempts in the
registry order below. Those assignments are attempts only; they do not prove
class registration, binding, inherited implementation, or construction.

## Complete method matrix

The receiver is `self` in every row. Formal names are Lua argument slots and
are not native type claims. `proto` is the direct child prototype index. Byte
spans are instruction-word offsets in the decoded Lua payload and are derived
from the reader's actual code offset and word count. A bare return is zero
values, not one nil.

| # | method | source LF | proto / debug lines | byte span | local behavior and decisive predicates | local result |
|---:|---|---:|---:|---:|---|---|
| 1 | `initAsk` | 11-204 | 0 / 45-107 | 868-1476 (153 words) | Declares `_temp` entries `focus:integer8`, `hp:integer8`, `commands:integer8`, `currentAngle:integer8`, `previousAngle:integer8`, `chosenItem:integer8`, `chosenCommand:integer16`, `focusedCommand:integer32`, `phase:integer8`, `goodmin:integer8`, and `goodmax:integer8`. Requests drag, cancel, operate, template-confirm, five command-row additions, row properties, selector events, HP controls, slider value 50, and input flag false. The loop concatenates the numeric loop index directly into `"ListBoxItem_Command_"..i`; it does not call global `tostring`. Performs local assignments `work.hp=100`, `currentAngle=0`, `previousAngle=0`, `phase=0`, and `focus=0`; the later Maximum and Value requests freshly read `work.hp`. If `A1 ~= nil`, requests `setText("TextBlock_Grade",3051,A1)`. | 0 values |
| 2 | `setWindowFocus` | 209-227 | 1 / 117-124 | 2450-2510 (16 words) | If `A1 ~= nil` and `A1 ~= ""`, requests `setLogicalFocus(A1)`, then reads `desktopWidget._getKeyboardFocusedWidget(desktopWidget)`. Only Lua-equal-to-`self` requests `setKeyboardFocusedControl(A1)`. Nil or empty-string input is a no-op. | 0 values |
| 3 | `setControlFocusable` | 232-240 | 2 / 133-135 | 2663-2683 (6 words) | Requests `setControlProperty(A1,"Focusable",A2)`. | 0 values |
| 4 | `processUICommandEvent` | 245-406 | 3 / 148-227 | 2766-3338 (144 words) | Exact `isAskFinish()==true` returns immediately. `A3=="UILuaCommands.Cancel"` handles phase 1: a non-slider keyboard control requests `setWindowFocus("Slider_PhaseA")` and `displayHelp()`, while the slider requests `focusFirstCommand(true)`. `A3=="ApplicationCommands.Operate"` requests the first-command helper only when phase 1 and the keyboard control is the slider. `A3=="UILuaCommands.Operate"` with `A2=="TemplateButton_Power"` calls `stopAngleGauge()` only at `focus==2`; only its exact true result requests base result 1 and gauge-focus false, then PC57 attempts `focus=0` inside that focus-2 arm, so focus 1 skips the reset. The other operate arm requires `A4 ~= nil` and `focus ~= 2`, attempts `chosenItem=A4`, captures `work` for the `chosenCommand` assignment before `getCommandId`, then uses fresh `self.work` reads for the collapse argument, help argument, phase, and gauge gate after that call. If `getCommandId` replaces `self.work`, the captured table still receives `chosenCommand`, while those later reads use the replacement. A fresh `phase==1` read requests `setControlFocusable("Slider_PhaseA",false)`, `setEnable("Slider_PhaseA",false)`, and `setBaseAskResult(1)` in that order. In another phase, only exact `isUseGauge(chosenCommand)==true` attempts `focus=2` and requests gauge start; otherwise it requests base result 1. Selector mouse-enter and anchored events return one false only on the rejection guard `focus~=1 or A4<0` at PC124; a valid selector reads `getCommandId(A4+1)`, captures the pre-call `work` table for its PC129 `focusedCommand` assignment, then PC130-137 fresh-read `self.work.focusedCommand` for the nil gate and help argument, and reaches PC138 `RETURN A=0,B=1` with zero results. Slider-focused events request `displayHelp()`. Other commands fall through. | 0 values on normal branches and valid selectors; one false only on selector rejection |
| 5 | `displayHelp` | 411-427 | 4 / 236-242 | 4019-4067 (13 words) | Nil `A1` requests `setText("TextBlock_CommandHelp",3069)`. Any nonnil `A1` requests `setText("TextBlock_CommandHelp",1105,A1)`. | 0 values |
| 6 | `setCommandList` | 432-489 | 5 / 252-266 | 4170-4362 (49 words) | Builds `row="ListBoxItem_Command_"..tostring(A1)` and `button=row..":TemplateButton_Command"`. For nonnil `A2`, performs the local `work.commands=work.commands+1` assignment attempt, then requests content 3043 and style `BTN_basis_listboxSelect` on `button`, and requests row `IntData.Value0=A2` plus row visibility true. For nil `A2`, requests empty content on `button`, row `IntData.Value0=0`, and row visibility false. | 0 values |
| 7 | `getCommandId` | 494-505 | 6 / 275-277 | 4656-4692 (10 words) | Builds the row name with `tostring(A1)` and tail-calls `getControlProperty(self,row,"IntData.Value0")` with an open result sequence. | All selected callee results, including zero results or one nil |
| 8 | `collapseCommandList` | 510-538 | 7 / 285-294 | 4820-4916 (25 words) | Iterates i=1..5, builds each row button path, and when `i==A1` requests style `BTN_basis_listboxSelect_cmdRunning` on that row's `:TemplateButton_Command`. After the loop it requests `setEnable("ListBox_CommandList",false)`. | 0 values |
| 9 | `focusFirstCommand` | 543-601 | 8 / 303-329 | 5166-5366 (51 words) | Scans i=1..5 and treats every value satisfying Lua `command ~= 0`, including nil, as a match. With nil `A1`, the first match requests `setWindowFocus(row)` before attempting `focusedCommand=command`, requests `displayHelp(command)`, and returns that index. With nonnil `A1`, the scan records the last matching index; after the loop it freshly re-reads that command, then requests focus, attempts the assignment, requests help, and returns the index. No match returns one 0. | One selected index, or one 0 |
| 10 | `isUseGauge` | 606-615 | 9 / 338-345 | 5563-5591 (8 words) | Returns true only when `A1 == 22705`; every other value returns false. | One true or one false |
| 11 | `setAngleGaugeFocusable` | 620-657 | 10 / 353-363 | 5644-5760 (30 words) | Exact `A1==true` requests `setControlFocusable("Label_Power",true)`, `IsHitTestVisible=true`, and `setEnable("Label_Power:TemplateButton_Power",true)`. All other values request false for all three. | 0 values |
| 12 | `startAngleGauge` | 662-679 | 11 / 371-376 | 5947-5995 (13 words) | Attempts `currentAngle=0`, then requests `setAngleGaugeFocusable(true)`, `setWindowFocus("Label_Power:TemplateButton_Power")`, and `sendControlCommand("Label_Power","Start_PowerGauge")` in that order. | 0 values |
| 13 | `stopAngleGauge` | 684-738 | 12 / 384-398 | 6225-6425 (51 words) | Requests `sendControlCommand("Label_Power","Stop_PowerGauge")`, reads `RenderTransform.AngleZ`, forwards the complete open result sequence to `tonumber` with no implicit receiver, and tests `0 < angle` before requesting `_math.floor(angle+0.5)` or `angle < 0` before requesting `_math.floor(angle-0.5)`. A normal numeric zero takes neither body assignment branch; a value for which both tests are false receives no body angle assignment, while other nonnumeric/coercive cases remain opaque or may fail. When a floor request returns normally, its selected result is the attempted `currentAngle` assignment. The body then freshly reads `currentAngle`, `goodmin`, and `goodmax`; the inclusive comparisons request `"Se_Good"` or otherwise `"Se_Normal"`. No native floor or persisted-storage effect is claimed. | One true after normal completion |
| 14 | `setAskParameter` | 743-905 | 13 / 420-483 | 6756-7304 (138 words) | Attempts `commands=0`, calls `setCommandList(1,A1)` through `(5,A5)` in order, requests command-list enabled, and attempts `currentAngle=0`. A fresh post-callback `work.commands==0` read returns false. Otherwise the body attempts `focus=1` and requests gauge-focus false. With `A6==1`, it requests title 3059/help 76615, freshly checks `phase==2` before `displayEffect()` and `"SQWTDesignCommands.PhaseBtoA"`, then attempts `phase=1`, requests phase-A visibility/focus/enabled, optionally requests rare effect start only for exact `A8==true` (stop for other nonnil A8), and requests help. With `A6==2`, it requests title 3060/help 76616, freshly checks `phase==1` before `"SQWTDesignCommands.PhaseAtoB"`, freshly checks `phase==2` before `displayEffect()`, then attempts `phase=2`, requests `focusFirstCommand()`, and optionally requests rare gauge start only for exact `A8==true` (stop for other nonnil A8). Other A6 values retain only the preceding local assignments and helper requests and finish normally. | One false for zero commands; otherwise one true |
| 15 | `getAskResult` | 910-930 | 14 / 492-500 | 8137-8205 (18 words) | Phase 1 returns `chosenCommand` followed by the open result sequence from `getControlProperty(self,"Slider_PhaseA","Value")`; zero getter results therefore differ from one nil. Any other phase returns `chosenCommand,currentAngle`. | Open phase-1 sequence, or two values in other phases |
| 16 | `updateHP` | 935-951 | 15 / 510-518 | 8370-8430 (16 words) | Numeric input outside inclusive 0..100 returns false. Valid input attempts `work.hp=A1`, then requests the HP progress value. | One false or one true |
| 17 | `displayEffect` | 956-979 | 16 / 527-536 | 8588-8664 (20 words) | Exact `isUseGauge(work.chosenCommand)==true` requests `sendControlCommand("Label_Power","Start_Effect")`, then attempts `previousAngle=currentAngle` and returns true. Otherwise it returns false. | One true or one false |
| 18 | `updateAskParameter` | 984-995 | 17 / 544-550 | 8851-8879 (8 words) | Forwards A1 to `updateHP`. Exact `A2==true` then requests `displayEffect`, even when the update result was false, provided the update completed. | 0 values |
| 19 | `orderHarvestOwnerMessageDisplay` | 1000-1029 | 18 / 562-570 | 8958-9058 (26 words) | If `A2==nil` or `A1==nil`, requests message text `" "` and `setHidden("Grid_HarvestMessage")`. Otherwise forwards A1..A6 to `setTextByOwner("TextBlock_Message",A1,A2,A3,A4,A5,A6)` and requests grid visibility true. | 0 values |
| 20 | `orderSweetspotDisplay` | 1034-1059 | 19 / 582-613 | 9225-9349 (32 words) | A1=1 selects local control string `"Slider_PhaseA"`; A1=2 selects local control string `"Label_Power"`; there are no UI calls. All other values return false. In phase 2 only, nonnil A2 attempts `goodmin=A2` and nonnil A3 attempts `goodmax=A3`. A4 is tested only for nil or exact false and has no resulting request or assignment. | One false or one true |

## CALL prefix and requested-width matrix

Each entry is `target(actual arguments) @ pc/byte [B,C]` from the original
instruction. `C=1` requests zero result slots, `C=2` requests one result, `C=0` keeps an
open result sequence, and `B=0` supplies an open argument sequence. Loop rows
show the repeated source call once with its loop variables. The receiver is
shown explicitly in every method call.

| # | method | direct CALL prefixes and actual arguments | result width |
|---:|---|---|---|
| 1 | `initAsk` | `self.setDrag(true) @50/1068 [3,1]`; `self.setControlCommandCondition("Slider_PhaseA","UILuaCommands.Cancel") @54/1084 [4,1]`; `self.setControlCommandCondition("ListBox_CommandList","UILuaCommands.Cancel") @58/1100 [4,1]`; `self.setControlCommandCondition("TemplateButton_Power","UILuaCommands.Operate") @62/1116 [4,1]`; `self.setTemplateConfirmCondition("ControlTemplate_Item","TemplateButton_Command","UILuaCommands.Operate") @67/1136 [5,1]`; loop `self._addItem(nil,"ListBox_CommandList","ControlTemplate_Item","ListBoxItem_Command_"..i) @80/1188 [6,1]`; loop row `self.setControlProperty(row,"IsTabStop",false) @85/1208 [5,1]`; loop button `self.setControlProperty(row..":TemplateButton_Command","CommandParameter",i) @92/1236 [5,1]`; `self.setControlCommandCondition("ListBox_CommandList","Selector.MouseEnteredItem") @97/1256 [4,1]`; `self.setControlCommandCondition("ListBox_CommandList","Selector.AnchoredItem") @101/1272 [4,1]`; conditional `self.setText("TextBlock_Grade",3051,A1) @110/1308 [5,1]`; `self.setControlProperty("ProgressBar_HP:TemplateProgressBar_HP","Minimum",0) @115/1328 [5,1]`; `self.setControlProperty("ProgressBar_HP:TemplateProgressBar_HP","Maximum",work.hp) @121/1352 [5,1]`; `self.setControlProperty("ProgressBar_HP:TemplateProgressBar_HP","Value",work.hp) @127/1376 [5,1]`; `self.setControlProperty("Slider_PhaseA","Value",50) @140/1428 [5,1]`; `self.setControlCommandCondition("Slider_PhaseA","UILuaCommands.SliderFocused") @144/1444 [4,1]`; `self.setControlCommandCondition("Slider_PhaseA","ApplicationCommands.Operate") @148/1460 [4,1]`; `self.setInputContorlFlag(false) @151/1472 [3,1]` | All fixed calls request zero results |
| 2 | `setWindowFocus` | `self.setLogicalFocus(A1) @6/2474 [3,1]`; `desktopWidget._getKeyboardFocusedWidget(desktopWidget) @9/2486 [2,2]`; conditional `self.setKeyboardFocusedControl(A1) @14/2506 [3,1]` | Getter requests one; fixed calls discard results |
| 3 | `setControlFocusable` | `self.setControlProperty(A1,"Focusable",A2) @4/2679 [5,1]` | Discarded |
| 4 | `processUICommandEvent` | `self.isAskFinish() @1/2770 [2,2]`; `self.getKeyboardFocusedControl() @12/2814 [2,2]`; `self.setWindowFocus("Slider_PhaseA") @17/2834 [3,1]`; `self.displayHelp() @19/2842 [2,1]`; `self.focusFirstCommand(true) @23/2858 [3,1]`; second `self.getKeyboardFocusedControl() @32/2894 [2,2]`; `self.focusFirstCommand() @36/2910 [2,1]`; `self.stopAngleGauge() @47/2954 [2,2]`; `self.setBaseAskResult(1) @52/2974 [3,1]`; `self.setAngleGaugeFocusable(false) @55/2986 [3,1]`; `self.getCommandId(work.chosenItem) @72/3054 [3,2]`; `self.collapseCommandList(work.chosenItem) @77/3074 [3,1]`; `self.displayHelp(work.chosenCommand) @81/3090 [3,1]`; `self.setControlFocusable("Slider_PhaseA",false) @89/3122 [4,1]`; `self.setEnable("Slider_PhaseA",false) @93/3138 [4,1]`; `self.setBaseAskResult(1) @96/3150 [3,1]`; `self.isUseGauge(work.chosenCommand) @101/3170 [3,2]`; `self.startAngleGauge() @107/3194 [2,1]`; `self.setBaseAskResult(1) @111/3210 [3,1]`; `self.getCommandId(A4+1) @128/3278 [3,2]`; `self.displayHelp(work.focusedCommand) @137/3314 [3,1]`; `self.displayHelp() @142/3334 [2,1]` | Boolean/result helpers request one; selector rejection returns one false at PC124 and valid selectors reach zero-result PC138; all fixed requests discard results |
| 5 | `displayHelp` | `self.setText("TextBlock_CommandHelp",3069) @5/4039 [4,1]`; `self.setText("TextBlock_CommandHelp",1105,A1) @11/4063 [5,1]` | Discarded |
| 6 | `setCommandList` | `tostring(A1) @3/4182 [2,2]`; `self.setContent(button,3043,A2) @19/4246 [5,1]`; `self.setControlProperty(button,"SqwtStyle","BTN_basis_listboxSelect") @24/4266 [5,1]`; `self.setControlProperty(row,"IntData.Value0",A2) @29/4286 [5,1]`; `self.setVisibility(row,true) @33/4302 [4,1]`; nil arm `self.setContent(button,"") @38/4322 [4,1]`; nil arm `self.setControlProperty(row,"IntData.Value0",0) @43/4342 [5,1]`; nil arm `self.setVisibility(row,false) @47/4358 [4,1]` | `tostring` requests one; fixed calls discard results |
| 7 | `getCommandId` | `tostring(A1) @4/4672 [2,2]`; tail `self.getControlProperty(row,"IntData.Value0") @7/4684 [4,0]` | Open tail result sequence |
| 8 | `collapseCommandList` | loop `tostring(i) @7/4848 [2,2]`; conditional `self.setControlProperty(button,"SqwtStyle","BTN_basis_listboxSelect_cmdRunning") @18/4892 [5,1]`; `self.setEnable("ListBox_CommandList",false) @23/4912 [4,1]` | `tostring` requests one; fixed calls discard results |
| 9 | `focusFirstCommand` | loop `self.getCommandId(i) @7/5194 [3,2]`; loop `tostring(i) @16/5230 [2,2]`; conditional `self.setWindowFocus(row) @18/5238 [3,1]`; conditional `self.displayHelp(command) @23/5258 [3,1]`; last-row `self.getCommandId(lastNonzero) @32/5294 [3,2]`; last-row `tostring(lastNonzero) @39/5322 [2,2]`; last-row `self.setWindowFocus(row) @41/5330 [3,1]`; last-row `self.displayHelp(command) @46/5350 [3,1]` | Getters and `tostring` request one; fixed calls discard results |
| 10 | `isUseGauge` | No CALL instructions | Direct boolean result |
| 11 | `setAngleGaugeFocusable` | true arm `self.setControlFocusable("Label_Power",true) @5/5664 [4,1]`; true arm `self.setControlProperty("Label_Power","IsHitTestVisible",true) @10/5684 [5,1]`; true arm `self.setEnable("Label_Power:TemplateButton_Power",true) @14/5700 [4,1]`; false arm has the same three calls with false @19/5720 [4,1], @24/5740 [5,1], @28/5756 [4,1] | Discarded |
| 12 | `startAngleGauge` | `self.setAngleGaugeFocusable(true) @4/5963 [3,1]`; `self.setWindowFocus("Label_Power:TemplateButton_Power") @7/5975 [3,1]`; `self.sendControlCommand("Label_Power","Start_PowerGauge") @11/5991 [4,1]` | Discarded |
| 13 | `stopAngleGauge` | `self.sendControlCommand("Label_Power","Stop_PowerGauge") @3/6237 [4,1]`; `self.getControlProperty("Label_Power:TemplateLabel_Power","RenderTransform.AngleZ") @8/6257 [4,0]`; `tonumber(open getter results) @9/6261 [0,2]`; `_math.floor(angle+0.5) @16/6289 [2,2]`; `_math.floor(angle-0.5) @25/6325 [2,2]`; `self.sendControlCommand("Label_Power","Se_Good") @42/6393 [4,1]`; `self.sendControlCommand("Label_Power","Se_Normal") @47/6413 [4,1]` | Getter is open; `tonumber` and floor request one; command results discarded |
| 14 | `setAskParameter` | five `self.setCommandList(1,A1)`, `self.setCommandList(2,A2)`, `self.setCommandList(3,A3)`, `self.setCommandList(4,A4)`, `self.setCommandList(5,A5) @5/6776`, @9/6792, @13/6808, @17/6824, @21/6840 [4,1]`; `self.setEnable("ListBox_CommandList",true) @25/6856 [4,1]`; `self.setAngleGaugeFocusable(false) @38/6908 [3,1]`; phase-A `self.setText("TextBlock_PhaseTitle",3059) @44/6932 [4,1]`; phase-A `self.setHelpParameter("TextBlock_PhaseTitle",1,76615) @49/6952 [5,1]`; conditional `self.displayEffect() @55/6976 [2,1]`; phase-A transition `self.sendControlCommand("Label_PhaseB","SQWTDesignCommands.PhaseBtoA") @59/6992 [4,1]`; `self.setVisibility("Label_PhaseA",true) @65/7016 [4,1]`; `self.setControlFocusable("Slider_PhaseA",true) @69/7032 [4,1]`; `self.setEnable("Slider_PhaseA",true) @73/7048 [4,1]`; `self.setWindowFocus("Slider_PhaseA") @76/7060 [3,1]`; phase-A rare `self.sendControlCommand("Label_RareCatalystEffect","UILuaCommands.RareEffectStart") @84/7092 [4,1]` or `self.sendControlCommand("Label_RareCatalystEffect","UILuaCommands.RareEffectStop") @89/7112 [4,1]`; `self.displayHelp() @91/7120 [2,1]`; phase-B `self.setText("TextBlock_PhaseTitle",3060) @98/7148 [4,1]`; phase-B `self.setHelpParameter("TextBlock_PhaseTitle",1,76616) @103/7168 [5,1]`; phase-B transition `self.sendControlCommand("Label_PhaseA","SQWTDesignCommands.PhaseAtoB") @111/7200 [4,1]`; phase-B `self.displayEffect() @117/7224 [2,1]`; `self.focusFirstCommand() @121/7240 [2,1]`; phase-B rare `self.sendControlCommand("Label_RareCatalystGaugeEffect","UILuaCommands.RareGaugeEffectStart") @129/7272 [4,1]` or `self.sendControlCommand("Label_RareCatalystGaugeEffect","UILuaCommands.RareGaugeEffectStop") @134/7292 [4,1]` | Every CALL in this row has `C=1` and requests zero result slots; the local helper results are not consumed |
| 15 | `getAskResult` | phase-A `self.getControlProperty("Slider_PhaseA","Value") @9/8173 [4,0]` | Open getter results are appended to chosenCommand; phase-B has no CALL |
| 16 | `updateHP` | valid arm `self.setControlProperty("ProgressBar_HP:TemplateProgressBar_HP","Value",A1) @12/8418 [5,1]` | Discarded |
| 17 | `displayEffect` | `self.isUseGauge(work.chosenCommand) @3/8600 [3,2]`; conditional `self.sendControlCommand("Label_Power","Start_Effect") @9/8624 [4,1]` | Predicate requests one; fixed call discarded |
| 18 | `updateAskParameter` | `self.updateHP(A1) @2/8859 [3,1]`; conditional `self.displayEffect() @6/8875 [2,1]` | Both results discarded |
| 19 | `orderHarvestOwnerMessageDisplay` | hidden arm `self.setText("TextBlock_Message"," ") @7/8986 [4,1]`; hidden arm `self.setHidden("Grid_HarvestMessage") @10/8998 [3,1]`; visible arm `self.setTextByOwner("TextBlock_Message",A1,A2,A3,A4,A5,A6) @20/9038 [9,1]`; visible arm `self.setVisibility("Grid_HarvestMessage",true) @24/9054 [4,1]` | Discarded |
| 20 | `orderSweetspotDisplay` | No CALL instructions | Direct boolean result |

For every fixed-width CALL, Lua writes exactly `C-1` result slots: missing
selected-helper results are padded with nil and extra results are truncated.
The open `getCommandId` TAILCALL and phase-1 `getAskResult` RETURN preserve
the complete selected result sequence. The open getter in `stopAngleGauge`
feeds all of its results through the `B=0` `tonumber` call. Reads of globals,
work fields, controls, and selected helper results occur at their original
instruction points; this contract does not replace independent reads with a
cached value. Exact true, false, nil, and numeric zero predicates remain
distinct.

The source-backed order is material to the local contract: `initAsk` assigns
HP before its fresh Maximum and Value reads; `setAskParameter` assigns the
command count, invokes all five `setCommandList` callbacks, requests
`setEnable("ListBox_CommandList",true)`,
assigns `currentAngle=0`, and only then fresh-reads `commands==0`; each phase
branch performs its own fresh phase comparison around the effect/transition
callbacks before its phase assignment; `startAngleGauge` assigns the current
angle before its three requests, while `initAsk` assigns currentAngle before
previousAngle; `displayEffect` reads current angle before
the previous-angle assignment; and `updateAskParameter` calls `updateHP`
before its exact-true `displayEffect` gate. Each nonnil `setCommandList` call
fresh-reads the current command count before its increment assignment.

The selector arm's rejection `RETURN A=6,B=2` at PC124 is one false value;
valid paths continue through PC138 `RETURN A=0,B=1` and return zero values.
Other exact-true gates remain
independent: `isAskFinish()==true`, `stopAngleGauge()==true`,
`isUseGauge(chosenCommand)==true`, `A1==true` for gauge focusability, `A2==true` for
effect continuation, and `A8==true` for each rare-effect start request.

## Lua and native boundaries

The helper model used for the bounded fixtures supports ordinary numeric
arithmetic and comparison, literal tables, fixed local method bindings, and
the observed `tostring`, `tonumber`, and `_math.floor` returns. It does not
claim string coercion, metamethod dispatch, callable values, native control
storage, or native conversion behavior beyond the concrete helper returns
used for a fixture. Lua equality keeps booleans distinct from numbers and
uses table identity; the typed fixture-vector comparator is separate and
recursive. Unsupported
non-numeric comparison, concatenation, conversion, and missing receiver cases
remain errors or opaque dependencies rather than inferred results.

`_temp` declaration tables, work-table assignment attempts, and fresh work reads establish
Lua operands only. They do not prove initial values supplied by native storage,
successful setter application, readback, registration, or a widget lifetime.
Control, focus, gauge, help, visibility, content, and command strings are
requests. A result true or false is a Lua return value, not a completed UI,
gathering, yield, fatigue, probability, depletion, inventory, currency,
server, or transaction outcome.

The published HarvestJudge22003 route remains caller context only. Selecting
this receiver, constructing it, dispatching its methods, or interpreting a
later gathering result requires evidence outside this one resource and is not
established here.

## Validation

The pinned LPB and JAR passed their exact size and SHA-256 checks. The one
decode/decompile run produced the pinned 9484-byte payload and 23717-byte
canonical source. A reader-backed check passed all 20 prototype parameter,
debug-line, code-offset, word-count, and computed first/last instruction-byte
spans. Typed fixtures passed all 20 method contracts, including the focus
guard, same-widget positive and same-content distinct-widget negative cases,
selector rejection versus valid zero-result returns, selector replacement-table
capture/fresh-read behavior, the focus-1 power reset skip, direct initAsk loop
concatenation, stop-gauge good/normal branches, zero-results versus one-nil
result distinction, nil-command `~=0` selection order, literal call tuples,
local assignment vectors, and result vectors. The fixtures are bounded
observability cases for each method, not an exhaustive branch campaign.
