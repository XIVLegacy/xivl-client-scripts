# MiningInputWidget local interaction contract

This page records the bounded local behavior recovered from the retail Lua
resource `widget/ask/mininginputwidget`. It describes the original method
words and their direct local requests, not native, server or gathering
completion behavior.

## Evidence and public locators

The canonical decoded script is
`lua/scripts/widget/ask/mininginputwidget.lua`, 23,567 bytes, 1,055 lines,
SHA-256
`AEE357DEC2F3257C36A83B0C879E4561A56A03180459EFF7A8435875EB2D6B83`.
The reproduction row is `manifests/scripts.json:15068-15073`.

The original resource is
`n1635q/9rz/x1w1w31wupqn1635q.le.lpb`, 9,468 bytes, SHA-256
`0EB5D0054BA5C64AE3E7B81A7CFEA014C594C0CA18AA45967CA689D5A17EB3E0`.
Its coverage row is `manifests/retail_lua_coverage.json:26836-26850` and
records the 9,455-byte decoded payload with SHA-256
`A6A7BD9AC1D4660E8A6D853C66BE582A9F780BFFADD07BC52140E542175FBF04`.
The registry row is `lua/registry.json:39319-39354`; it records class
`MiningInputWidget`, its 20 methods and the require path
`/Widget/Ask/AskBaseClass`.

The LPB was decoded and canonicalized with `tools/retail_script.py:37,62`.
The pinned decompiler is
`tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`;
its source and license provenance are recorded in
`tools/vendor/unluac/PROVENANCE.json:2-9`. The canonical LF output has the
script-manifest identity above.

The resource contains one root prototype and exactly 20 direct method
prototypes. The table below gives each method's canonical source lines,
prototype index, original instruction PC span, decoded payload byte span, and
bounded result contract. Byte offsets are the first and last four-byte Lua
instruction words for that method. Result statements assume the dynamically
called helper returns normally; a helper or conversion error can stop the
method before its listed return.

Compositions of local methods require the dynamic lookups to select the
described pinned closures and intervening accesses and calls to complete
normally. Assignment attempts do not prove storage; repeated work-member
lookups may supply different values.

## Twenty-method source and instruction ledger

| # | Method | Source lines | Proto | PC span | Byte span | Result and bounded behavior |
|---:|---|---:|---:|---:|---:|---|
| 1 | `initAsk` | 11-206 | 0 | 0-152 | 867-1475 | Method return width 0. Attempts `_temp` metadata, drag and command conditions, five command slots, HP controls, phase controls, and initial `hp=100`, `currentPower=0`, `previousPower=0`, `phase=0`, `focus=0`; non-nil grade requests text 3051. |
| 2 | `setWindowFocus` | 209-229 | 1 | 0-15 | 2434-2494 | Method return width 0. Empty or nil control skips requests; otherwise requests logical focus, then keyboard focus only when `desktopWidget._getKeyboardFocusedWidget() == self` in Lua. |
| 3 | `setControlFocusable` | 232-242 | 2 | 0-5 | 2647-2667 | Method return width 0. Requests `setControlProperty(control,Focusable,flag)`. |
| 4 | `processUICommandEvent` | 245-408 | 3 | 0-143 | 2750-3322 | Method return width 0 except selector guard false. Exact event guards and work assignments are bounded below; finish is an exact-true early return. |
| 5 | `displayHelp` | 411-429 | 4 | 0-12 | 4003-4051 | Method return width 0. Nil command requests text 3068; non-nil command requests text 1105 and the command. |
| 6 | `setCommandList` | 432-491 | 5 | 0-48 | 4154-4346 | Method return width 0. Nonnil input attempts a commands increment from its current read, then requests content/style/id/visibility. Nil input requests empty content, id 0 and hidden visibility; that branch makes no commands assignment. |
| 7 | `getCommandId` | 494-507 | 6 | 0-9 | 4640-4676 | Open-width tail from `getControlProperty(ListBoxItem_Command_<index>,IntData.Value0)`, preserving zero, nil and additional returned values. |
| 8 | `collapseCommandList` | 510-540 | 7 | 0-24 | 4804-4900 | Method return width 0. Scans slots 1..5, requests style for the Lua-equal selected slot, then requests list enable false. |
| 9 | `focusFirstCommand` | 543-603 | 8 | 0-50 | 5150-5350 | Method return width 1. Tests command ~= 0. Nil argument stops at the first match without refetch; nonnil argument scans all five and refetches the last matching index. Both paths request focus before attempting focusedCommand assignment and help with the retained command. No match returns 0. |
| 10 | `isUsePower` | 606-617 | 9 | 0-7 | 5547-5575 | Method return width 1, exactly one boolean, true only for numeric command 22703. |
| 11 | `setPowerGaugeFocusable` | 620-659 | 10 | 0-29 | 5628-5744 | Method return width 0. Exact true selects literal-true focusability/hit-test/enable requests; every other value selects literal-false requests. |
| 12 | `startPowerGauge` | 662-681 | 11 | 0-12 | 5931-5979 | Method return width 0. Attempts currentPower=0, then requests gauge focusability, window focus and Start_PowerGauge. |
| 13 | `stopPowerGauge` | 684-732 | 12 | 0-40 | 6209-6369 | Method return width 1, exactly one true after stop. The open scale read forwards all results to `tonumber` (B=0,C=2); fresh global `_math.floor` receives one explicit argument (B=2,C=2), with no `_math` receiver, before current-power assignment and sound selection. Low and high tests use separate current-power reads. |
| 14 | `setAskParameter` | 735-901 | 13 | 0-139 | 6700-7256 | Method return width 1. Attempts commands=0, makes five list calls then list-enable, attempts currentPower=0 then previousPower=0, and reads commands afresh. Exact 0 returns false before later calls; commands ~= 0, including nil/false, continues with focus=1 attempt and gauge-disable request. Phase branches are below; other A6 values return true after common setup. |
| 15 | `getAskResult` | 904-926 | 14 | 0-17 | 8108-8176 | Exact phase 1 has open method return width: chosen command plus the open-width slider property tail. Every other phase value, including phase 2 and defaults, has method return width 2: exactly chosen command and current power. |
| 16 | `updateHP` | 929-947 | 15 | 0-15 | 8341-8401 | Method return width 1. Either reject comparison, 100 < A1 or A1 < 0, returns literal false. Otherwise attempts work.hp=A1, requests the HP property using A1, and returns literal true on normal completion. Comparison errors are separate. |
| 17 | `displayEffect` | 950-975 | 16 | 0-19 | 8559-8635 | Method return width 1. Exact true from isUsePower requests Start_Effect, then reads currentPower and attempts previousPower assignment before returning true. Other results return false without a previousPower assignment by this branch; the callback retains its own effects. |
| 18 | `updateAskParameter` | 978-991 | 17 | 0-7 | 8822-8850 | Method return width 0. Requests `updateHP`; exact true effect flag then requests `displayEffect`, regardless of the updateHP return value. |
| 19 | `orderHarvestOwnerMessageDisplay` | 994-1025 | 18 | 0-25 | 8929-9029 | Method return width 0. Nil first or second input requests one-space message text and hidden grid; otherwise forwards all six inputs to owner text and requests grid visibility true. |
| 20 | `orderSweetspotDisplay` | 1028-1055 | 19 | 0-31 | 9196-9320 | Method return width 1, exactly one false for a phase other than 1 or 2; valid phases return true. It only selects a local control string; phase 2 conditionally attempts `work.goodmin=A2` and `work.goodmax=A3` for non-nil bounds, and its final flag branch makes no UI call. |

## Twenty-method call and result matrix

Call notation uses the actual Lua argument list. For a `CALL`, `->0` means
C=1 requested and discarded zero results, `->1` means C=2 requested one
result, and `->open` means C=0 preserves the dynamic result width. The
`method return` text is separate and describes the enclosing method's RETURN
words. These are direct dynamic requests; a request does not prove that a
native implementation accepted or completed it. Named controls, properties,
styles and command tokens denote source string literals, including
`UILuaCommands.*` and `SQWTDesignCommands.*`; receiver and argument variables
retain their operand roles.
For `setCommandList`, `row` is `"ListBoxItem_Command_"..tostring(index)`
and `button` is `row..":TemplateButton_Command"`.

| Method | Fixed receiver and call-prefix order | Result contract |
|---|---|---|
| `initAsk` | `setDrag(self,true) ->0`; `setControlCommandCondition(self,"Slider_PhaseA","UILuaCommands.Cancel") ->0`; `setControlCommandCondition(self,"ListBox_CommandList","UILuaCommands.Cancel") ->0`; `setControlCommandCondition(self,"TemplateButton_Power","UILuaCommands.Operate") ->0`; `setTemplateConfirmCondition(self,TemplateControl_Item,TemplateButton_Command,UILuaCommands.Operate) ->0`; for n 1..5, `_addItem(self,nil,ListBox_CommandList,TemplateControl_Item,ListBoxItem_Command_n) ->0`, item `setControlProperty(self,item,IsTabStop,false) ->0`, button `setControlProperty(self,button,CommandParameter,n) ->0`; selector conditions `setControlCommandCondition(self,ListBox_CommandList,"Selector.MouseEnteredItem") ->0` and `setControlCommandCondition(self,ListBox_CommandList,"Selector.AnchoredItem") ->0`; optional `setText(self,TextBlock_Grade,3051,grade) ->0`; `setControlProperty(self,ProgressBar_HP:TemplateProgressBar_HP,Minimum,0) ->0`, then `setControlProperty(self,ProgressBar_HP:TemplateProgressBar_HP,Maximum,work.hp) ->0` and `setControlProperty(self,ProgressBar_HP:TemplateProgressBar_HP,Value,work.hp) ->0` from separate reads, `setControlProperty(self,Slider_PhaseA,Value,50) ->0`, `setControlCommandCondition(self,Slider_PhaseA,"UILuaCommands.SliderFocused") ->0`, `setControlCommandCondition(self,Slider_PhaseA,"ApplicationCommands.Operate") ->0`; `setInputContorlFlag(self,false) ->0` | Method return ->0. Literal `work.hp=100` precedes the independent reads; A2 and A3 are unused by this body; nil grade omits only grade text. |
| `setWindowFocus` | `setLogicalFocus(self,control) ->0`; `_getKeyboardFocusedWidget(desktopWidget) ->1`; when Lua `==` with self is true, `setKeyboardFocusedControl(self,control) ->0` | Method return ->0. Nil or empty control makes no call. |
| `setControlFocusable` | `setControlProperty(self,control,Focusable,flag) ->0` | Method return ->0. |
| `processUICommandEvent` | `isAskFinish(self) ->1` first; exact true returns zero values. For A3=`UILuaCommands.Cancel`, only phase==1 calls `getKeyboardFocusedControl(self) ->1`: a result Lua-unequal to Slider_PhaseA requests `setWindowFocus(self,Slider_PhaseA) ->0` then `displayHelp(self) ->0`; equality requests `focusFirstCommand(self,true) ->0`. Cancel then returns zero values. A3=`ApplicationCommands.Operate` also reads focus only in phase 1 and requests `focusFirstCommand(self) ->0` only for Slider_PhaseA equality, then returns. For A3=`UILuaCommands.Operate` and A2=TemplateButton_Power, only focus==2 calls `stopPowerGauge(self) ->1`; exact true requests `setBaseAskResult(self,1) ->0` then `setPowerGaugeFocusable(self,false) ->0`; either stop result is followed by a focus=0 attempt. Other operate controls require A4~=nil and focus~=2: attempt chosenItem=A4, request `getCommandId(self,<fresh chosenItem>) ->1` and attempt chosenCommand assignment, then `collapseCommandList(self,<fresh chosenItem>) ->0` and `displayHelp(self,<fresh chosenCommand>) ->0`. A fresh phase==1 selects `setControlFocusable(self,Slider_PhaseA,false) ->0`, `setEnable(self,Slider_PhaseA,false) ->0`, `setBaseAskResult(self,1) ->0`. Otherwise `isUsePower(self,<fresh chosenCommand>) ->1` exact true attempts focus=2 then requests `startPowerGauge(self) ->0`; any other result requests `setBaseAskResult(self,1) ->0`. Selector.MouseEnteredItem/Selector.AnchoredItem first reject focus~=1, then reject A4<0 with one false; otherwise `getCommandId(self,A4+1) ->1` feeds a focusedCommand attempt. A later nonnil focusedCommand read requests `displayHelp(self,<another fresh focusedCommand>) ->0`; normal selector continuation returns zero values. UILuaCommands.SliderFocused requests `displayHelp(self) ->0`. | Method return ->0 except the two selector reject guards, which return one false. Operate power/other-control arms are separate; nil item or focus==2 can skip the latter calls. A1/A5 are unused. Calls/accesses/comparisons retain their error and nonreturn boundaries. |
| `displayHelp` | Nil: `setText(self,TextBlock_CommandHelp,3068) ->0`. Non-nil: `setText(self,TextBlock_CommandHelp,1105,command) ->0` | Method return ->0; nil and non-nil prefixes are distinct. |
| `setCommandList` | Global `tostring(index) ->1`; nonnil path attempts commands=current read+1, then `setContent(self,button,3043,value) ->0`, `setControlProperty(self,button,SqwtStyle,BTN_basis_listboxSelect) ->0`, `setControlProperty(self,row,IntData.Value0,value) ->0`, `setVisibility(self,row,true) ->0`. Nil path requests `setContent(self,button,"") ->0`, `setControlProperty(self,row,IntData.Value0,0) ->0`, `setVisibility(self,row,false) ->0`. | Method return ->0. The nil branch makes no commands assignment; helper effects remain separate. |
| `getCommandId` | Global `tostring(index) ->1`, then open tail `getControlProperty(self,item,IntData.Value0) ->open` | Method return ->open exactly preserves zero returns, nil returns, one value and extra values. |
| `collapseCommandList` | Global `tostring(n) ->1` for n 1..5; selected n requests `setControlProperty(self,button,SqwtStyle,BTN_basis_listboxSelect_cmdRunning) ->0`; final `setEnable(self,ListBox_CommandList,false) ->0` | Method return ->0. Nil or unmatched selection only omits style. |
| `focusFirstCommand` | `getCommandId(self,n) ->1` scans n=1..5 and tests command~=0. With nil A1, the first match calls `tostring(n) ->1`, requests `setWindowFocus(self,row) ->0`, attempts focusedCommand=<retained scan result>, requests `displayHelp(self,<retained scan result>) ->0` and returns n. With nonnil A1, scan all five, retain the last match, then `getCommandId(self,index) ->1` refetches before `tostring(index) ->1`, `setWindowFocus(self,row) ->0`, the focusedCommand attempt and `displayHelp(self,<retained refetch result>) ->0`. | Method return ->1: selected index or 0. Only the nonnil-argument path refetches. Both focus requests precede the assignment attempt; nil getter results satisfy nil~=0. |
| `isUsePower` | No calls | Method return ->1, true only for numeric 22703. |
| `setPowerGaugeFocusable` | In either branch: `setControlFocusable(self,Label_Power,flag) ->0`, `setControlProperty(self,Label_Power,IsHitTestVisible,flag) ->0`, `setEnable(self,Label_Power:TemplateButton_Power,flag) ->0` | Method return ->0. Here flag is literal true when A1 is exactly true and literal false otherwise. |
| `startPowerGauge` | `setPowerGaugeFocusable(self,true) ->0`; `setWindowFocus(self,Label_Power:TemplateButton_Power) ->0`; `sendControlCommand(self,Label_Power,Start_PowerGauge) ->0` | Method return ->0. Current power assignment precedes calls. |
| `stopPowerGauge` | `sendControlCommand(self,Label_Power,Stop_PowerGauge) ->0`; `getControlProperty(self,Label_Power:TemplateLabel_Power,RenderTransform.ScaleX) ->open`; global `tonumber(<all property results>) ->1` (PC9 byte6245, B=0,C=2); field `floor` of freshly read global `_math` receives `(converted*100+0.5) ->1` (PC15 byte6269, B=2,C=2), with no `_math` receiver argument; final `sendControlCommand(self,Label_Power,Se_Good) ->0` or `Se_Normal ->0` | Method return ->1, true on normal completion. `Se_Good` requires `goodmin <=` the first currentPower read and a separate currentPower read `<= goodmax`; otherwise `Se_Normal`. Conversion/helper behavior and arithmetic/comparison errors retain their own boundaries. |
| `setAskParameter` | Attempt commands=0; five `setCommandList(self,i,Ai) ->0` for i=1..5; `setEnable(self,ListBox_CommandList,true) ->0`; attempt currentPower=0 then previousPower=0. Fresh commands==0 returns false before later calls. Commands~=0 attempts focus=1 then `setPowerGaugeFocusable(self,false) ->0`. A6==1: `setText(self,TextBlock_PhaseTitle,3059) ->0`, `setHelpParameter(self,TextBlock_PhaseTitle,1,76605) ->0`; fresh phase==2 requests `displayEffect(self) ->0` then `sendControlCommand(self,Label_PhaseB,SQWTDesignCommands.PhaseBtoA) ->0`; attempt phase=1; `setVisibility(self,Label_PhaseA,true) ->0`, `setControlFocusable(self,Slider_PhaseA,true) ->0`, `setEnable(self,Slider_PhaseA,true) ->0`, `setWindowFocus(self,Slider_PhaseA) ->0`. Nonnil A8 sends `sendControlCommand(self,Label_RareCatalystEffect,UILuaCommands.RareEffectStart) ->0` for exact true or `sendControlCommand(self,Label_RareCatalystEffect,UILuaCommands.RareEffectStop) ->0` otherwise; then `displayHelp(self) ->0`. A6==2: `setText(self,TextBlock_PhaseTitle,3060) ->0`, `setHelpParameter(self,TextBlock_PhaseTitle,1,76606) ->0`; fresh phase==1 requests `sendControlCommand(self,Label_PhaseA,SQWTDesignCommands.PhaseAtoB) ->0`; another fresh phase==2 independently requests `displayEffect(self) ->0`, so both can occur. Attempt phase=2; `focusFirstCommand(self) ->0`; nonnil A8 sends `sendControlCommand(self,Label_RareCatalystGaugeEffect,UILuaCommands.RareGaugeEffectStart) ->0` for exact true or `sendControlCommand(self,Label_RareCatalystGaugeEffect,UILuaCommands.RareGaugeEffectStop) ->0` otherwise. | Method return ->1: false for the fresh commands==0 test, true on other normal continuations. Nil/false command counts satisfy ~=0. Other A6 values make only common setup requests. A7 is unused; nil A8 omits its effect send. |
| `getAskResult` | Exact phase 1: `getControlProperty(self,Slider_PhaseA,Value) ->open` after chosen command. Other phases: no call | Exact phase 1 method return ->open, chosen command plus property tail; all other phases method return ->2, chosen command and current power. |
| `updateHP` | Reject on 100<A1 or A1<0 with no body assignment or request. Otherwise attempt work.hp=A1 then `setControlProperty(self,ProgressBar_HP:TemplateProgressBar_HP,Value,A1) ->0`. | Method return ->1: literal false on either reject; literal true after the property request completes. Ordinary comparison errors are not false results. |
| `displayEffect` | `isUsePower(self,<current chosenCommand>) ->1`; exact true requests `sendControlCommand(self,Label_Power,Start_Effect) ->0`, then reads currentPower and attempts previousPower=<that read>. | Method return ->1 boolean. A non-exact-true result returns false with no subsequent effect request or previousPower assignment by this branch; callback effects are not excluded. |
| `updateAskParameter` | `updateHP(self,hp) ->0` with any returned value discarded; exact effect flag true then `displayEffect(self) ->0` | Method return ->0. Effect request follows the flag, not updateHP's returned value. |
| `orderHarvestOwnerMessageDisplay` | Nil A1 or A2: `setText(self,TextBlock_Message," ") ->0`, `setHidden(self,Grid_HarvestMessage) ->0`. Otherwise `setTextByOwner(self,TextBlock_Message,A1,A2,A3,A4,A5,A6) ->0`, `setVisibility(self,Grid_HarvestMessage,true) ->0` | Method return ->0. A3-A6 are forwarded without local filtering on the value path. |
| `orderSweetspotDisplay` | Invalid A1 has no calls. Phase 1 sets only local control string `Slider_PhaseA`; phase 2 sets only local control string `Label_Power` and independently attempts `work.goodmin=A2` and `work.goodmax=A3` when each is non-nil, including false or 0; no UI calls are made anywhere, including the final flag branch | Method return ->1: false for invalid phase; true for phase 1 or 2. A4 nil, false and true all reach the same no-op tail. |

## Setup and phase requests

The root prototype starts at payload byte 32. Its `require` setup is
`GETGLOBAL require` PC 0 byte 32, `LOADK "/Widget/Ask/AskBaseClass"` PC 1
byte 36, and `CALL` PC 2 byte 40 with requested width 0 (`->0`). Its class declaration
is `GETGLOBAL _defineClass` PC 3 byte 44, class-name and base-name loads at
PC 4 byte 48 and PC 5 byte 52, and `CALL` PC 6 byte 56 with requested width 0
(`->0`).
Before every closure binding, the root performs a fresh `GETGLOBAL
MiningInputWidget`: PCs 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43,
46, 49, 52, 55, 58, 61 and 64 (bytes 60, 72, 84, 96, 108, 120, 132, 144,
156, 168, 180, 192, 204, 216, 228, 240, 252, 264, 276 and 288). The root
then creates each closure and attempts a `SETTABLE` binding at these payload locations: `initAsk` PC 9 byte
68, `setWindowFocus` PC 12 byte 80, `setControlFocusable` PC 15 byte 92,
`processUICommandEvent` PC 18 byte 104, `displayHelp` PC 21 byte 116,
`setCommandList` PC 24 byte 128, `getCommandId` PC 27 byte 140,
`collapseCommandList` PC 30 byte 152, `focusFirstCommand` PC 33 byte 164,
`isUsePower` PC 36 byte 176, `setPowerGaugeFocusable` PC 39 byte 188,
`startPowerGauge` PC 42 byte 200, `stopPowerGauge` PC 45 byte 212,
`setAskParameter` PC 48 byte 224, `getAskResult` PC 51 byte 236,
`updateHP` PC 54 byte 248, `displayEffect` PC 57 byte 260,
`updateAskParameter` PC 60 byte 272, `orderHarvestOwnerMessageDisplay` PC 63
byte 284, and `orderSweetspotDisplay` PC 66 byte 296. Each binding's target is
the fresh global value at its preceding `GETGLOBAL`; a `SETTABLE` metamethod or
global replacement can change later targets, so no one class-table identity is
assumed. These bindings require the selected globals and the preceding calls
and closure creation to complete normally; the operands establish attempts,
not installation or dispatch. The `_math` value used by `stopPowerGauge` is a
fresh global lookup at proto 12 PC 11 byte 6253, followed by its
`floor` field at PC 12 byte 6257.

`initAsk` attempts to create the local `_temp` metadata rows for focus, HP,
command count, current and previous power, chosen item and command, focused
command, phase and sweetspot bounds. It attempts drag mode, command conditions
for phase cancellation, list cancellation, power operation, selector events,
slider focus and slider operation, five item templates, HP minimum 0, HP
maximum and value each read the then-current `work.hp` after the literal
`work.hp=100` attempt, phase slider value 50, and input-control flag false.
The Maximum read is proto 0 PCs 119-120 (bytes 1343-1347), and the Value read
is proto 0 PCs 125-126 (bytes 1367-1371); they are separate operand reads.
These assignments and calls describe operands supplied by the script; they do
not prove native initialization, registration, storage persistence or focus
readback.

`setAskParameter` attempts commands=0 before its five list calls. List enable
precedes the currentPower and previousPower reset attempts and the fresh count
test. Exact zero returns false; Lua commands~=0, including nil or false,
continues with focus=1 and gauge-disable attempts/requests. The phase-2 checks
use separate reads around the transition request and can both pass.

`processUICommandEvent` uses A3 as the command operand. Selector handling first
rejects focus~=1, then tests A4<0; it does not replace that comparison with
an A4>=0 requirement. Missing values, comparison errors or nonreturning calls
can prevent normal returns. Unmatched command tokens fall through after the
finish check without an additional request.

## Qualifications and focused verification

The direct `require` and `_defineClass` operands, work-table assignments and
dynamic method calls are attempts recovered from the resource. They do not
prove installation, dispatch, normal completion, native storage, native
metamethods, render behavior, lifetime, service behavior or helper-to-widget
creation. UI, focus, gauge and close operations are requests. Sweetspot phase
selection is a local string choice; bound assignments are only script attempts
and no UI call occurs. A missing or invalid dynamically supplied value can lead
to an unbounded native or Lua error path, as noted for scale conversion and HP
comparison.

A focused original-word fixture check covered 60 literal result vectors, exact
call tuples and selected PC paths across all 20 methods. Its domain was
ordinary tables and numbers with explicit helper return fixtures. It exercised
SETLIST, loops, concatenation, arithmetic, type-aware equality and ordering,
ordinary same-object table equality for fixtures without an `__eq` hook, Lua
truthiness, callback mutations, independent repeated reads, refetched command
results, HP assignment, and open-width calls. Result vectors and call tuples
use Lua type-aware comparison, so booleans and numbers remain distinct. The
source operation remains Lua `==`; hook dispatch is outside this contract. The
numeric-not-true finish guard has a required continuation PC assertion. It excluded
metamethod dispatch, callable objects, general coercion, native implementations
and dynamic binding behavior. The check supports this bounded contract only.

The published HarvestJudge route in
`docs/gathering-marker-fishing-ui.md:45-77` is related reuse context; it does
not establish runtime creation of this widget or a successful gathering
transaction. No server yield, probability, depletion, fatigue, accepted
transaction or historical invocation claim is made.

