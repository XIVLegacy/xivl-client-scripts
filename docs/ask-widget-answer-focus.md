# AskWidget answer rows, focus and paging

`Ask/AskWidget` precreates 24 answer rows, resets them before each question,
shows the rows of the current page and focuses the default answer's button.
`CommonAskWidget` uses the same focus request. `LogoutCommand.eventConfirm`
is a three-answer caller of this widget through `askForEventMode`. These are
recovered Lua request contracts. Native row creation, focus movement, paging
input and rendered text are not established here.

Neighbouring pages own the adjacent contracts:

- The [camp choice flow](camp-replacement-choice-flow.md#ordered-call-and-display-requests)
  owns `askForEventMode`, its opening request, the `ask` frame and the
  operate and cancel result paths.
- The [duty confirmation contract](duty-confirmation-client-contract.md#text-and-native-property-input)
  owns the question and answer property tuples of `ask`, including the
  provider branch and the formatting suffix calculation.
- `xivl-client-structs:docs/widget-item-consumer-contract.md`, "Ask wrapper
  join", owns the `addListBoxItem` and `addItem` operands, and
  `xivl-client-structs:docs/fade-actor-group-native-contract.md`, "Widget
  item", owns the `_addItem` argument cells.
- The [Ask base contract](ask-widget-result-state.md) owns the result value
  and the completion poll.

## Initialization requests

`AskWidget.initAsk` (`root/proto0`) replaces `work._temp` with six
declarations at PC27: `askDefaultAnswer`, `askAnswerMax`, `askPageMax` and
`askPageNow` as `integer8`, then `askPaging` and `canCancel` as `boolean`.
It then makes these requests, each discarding its results:

| PC | Request |
| ---: | --- |
| 32 | `_setUICommandCondition(W,"Button_Previous","UILuaCommands.PagePrevious",5)` |
| 37 | `_setUICommandCondition(W,"Button_Next","UILuaCommands.PageNext",5)` |
| 39 | `setCancelCondition(W)` with no control operand |
| 45 | `_setUICommandTemplateCondition(W,"ControlTemplate_ListBoxItem","TemplateButton_Answer","UILuaCommands.Operate",5)` |
| 50 | `addListBoxItem(W,"ListBox_Answers","Item_Answers",24)` |
| 52 | `initialWidget(W)` |

The shared `setCancelCondition` (`widget/widgetbaseclass_common.lua`,
`root/proto58`) substitutes `"_widget"` for a nil control at PCs 0-2 and
requests `_setUICommandCondition(W,control,"UILuaCommands.Cancel",5)` at
PC7. The AskWidget call therefore registers Cancel on `_widget`.

After its `_addItem` request, the shared `addItem` (`root/proto166`) also
requests `_setProperty(W,name,name,"Focusable",false)` at PCs 6-11, with the
item name in both name positions. Each precreated row receives this request.

## Row reset

`initialWidget` (`root/proto5`) requests `resetBaseAskResult` at PC1, then
writes `askPageNow=1`, `askPageMax=0`, `askAnswerMax=0`, `askPaging=false`,
`askDefaultAnswer=1` and `canCancel=false` (PCs 2-13). It requests
`setText(W,"TextBlock_Question","")` at PC17. For i from 1 through 24 it
then requests two writes per row, with N the string `"Item_Answers"..i`:

```text
_setProperty(W,N,"TemplateButton_Answer","Content","")   PC32
_setProperty(W,N,N,"Visibility","Collapsed")               PC38
```

The loop bound is the literal 24, independent of the next question's answer
count. `ask` calls this method first (PCs 0-1), so every question starts from
24 collapsed rows with empty content requests.

## Default answer and focus

After the text requests, `ask` (`root/proto2`) tests the default answer
operand X, the third argument after the receiver. PC98 compares X
with nil, and a nonnil X jumps directly to PC106. That path stores X in
`askDefaultAnswer` (PC107), stores the one result of `getPageNum(W,X)` in
`askPageNow` (PCs 109-112) and requests `pageChange(W,askPageNow)` (PC116).
A nonnil X is stored without a range comparison, so 0, 25 or a string reach
that store unchanged.

A nil X falls through to PC100, `LE 1,X`, which compares a number with nil.
Under standard Lua 5.1 comparison rules this raises an error. The PC118
branch that stores 1 and requests `pageChange(W,1)` is reached only from the
comparisons at PCs 100 and 104, so standard semantics reach it with neither a
nil nor a nonnil X.

`processAfterShow` (`root/proto1`) forms
`"Item_Answers"..tostring(work.askDefaultAnswer)` (PCs 0-5), requests
`_setKeyboardFocusedControl(W,name,"TemplateButton_Answer")` (PC9) and
returns one `true` (PC11). `CommonAskWidget.processAfterShow`
(`widget/commonaskwidget.lua`, `root/proto2`) has the same request and
return at the same PCs. Its default answer comes from its own `init`, which
the [CommonAsk initializer contract](common-ask-text-request.md#original-initializer-contract)
owns.

## Paging

`getPageNum(W,i)` (`root/proto7`) iterates p from 1 through
`work.askPageMax` and returns the first p with `i <= 8*p` (PCs 4-9). When no
page qualifies, including `askPageMax=0`, it returns one 0 (PCs 10-11).

`pageChange(W,page)` (`root/proto6`) loops i from 1 through
`work.askAnswerMax`. Each row whose `getPageNum` result equals page requests
`Visibility` `"Visible"`, every other row `"Collapsed"`, again with the row
name in both name positions (PCs 4-25). Rows above `askAnswerMax` keep the
reset request. The button contents start as 1001 for `Button_Previous` and
1002 for `Button_Next` (PCs 26-27). Only when `work.askPaging` equals false
exactly, page 1 replaces the first with 1004 and `askPageNow == askPageMax`
replaces the second with 1003 (PCs 30-43). Both are then requested through
`setContent` (PCs 47 and 51).

`ask` computes `askPageMax` as `_math.ceil(askAnswerMax/8)` (PCs 9-16). It
requests `setVisibility(W,"Grid_Button",true)` only when `askPageMax > 1` or
`askPaging` equals true (PCs 17-28). No request hides `Grid_Button` in these
bodies. Its visibility for a single-page question rests on the form and the
widget's earlier state.

## Logout confirmation caller

`LogoutCommand` is defined over `SystemCommandBaseClass`. Its
`eventConfirm(self,player)` (`command/system/logoutcommand.lua`,
`root/proto1`) makes these requests:

1. `player:_wait(1)`, discarding results (PCs 0-2).
2. Builds `{34129,34130,34131}` (PCs 3-7).
3. `desktopWidget:askForEventMode(self,worldMaster,worldMaster,3,false,true,34123,answers)`
   with `CALL B=10,C=2` (PC18), keeping one result.
4. Returns that one value (PC19).

The method calls the connector directly. `WorldMaster.ask`, whose -3 to nil
mapping is described on the camp page, is not on this route, so a cancel
result of -3 reaches the caller unchanged.

Composed with the camp page's connector contract, the opening request is
`openWidgetYield(desktopWidget,4,"Ask/AskWidget",nil,nil,false)` and the widget receives
`ask(widget,worldMaster,worldMaster,3,false,true,34123,answers)` with no
formatting tail. The duty confirmation page's provider branch then supplies
`(widget,nil,"TextBlock_Question","Text",worldMaster,34123)` for the
question and `(widget,"Item_Answers"..i,"TemplateButton_Answer","Content",worldMaster,R)`
for rows R 34129 to 34131. With an empty tail, k is 0 and each `select(i)`
suffix contributes no values.

Under those pinned bodies the local state requests are `askAnswerMax=3`,
`askPaging=false`, `canCancel=true` and `askPageMax=1`. No `Grid_Button`
request is made. The nonnil default 3 is stored, `getPageNum(3)` is 1, rows
1 to 3 request `Visible`, rows 4 to 24 keep `Collapsed`, `Button_Previous`
requests 1004 and `Button_Next` requests 1003. The later focus request names
`Item_Answers3`. The camp page's result paths give N for an operate on
`Item_AnswersN` and -3 for a cancel while `canCancel` is true. The connector
returns 0 when the opening returns nil or the selection wait does not return
exactly true.

The text of rows 34123 and 34129 to 34131 is NOT TRACED here, including
whether the `worldMaster.csv` sheet pinned by
`xivl-client-data:manifests/tables.json` holds them. No server meaning is
assigned to the ordinals.

## CommonAsk opening from the main menu

`MainMenuWidget.executeCommand` (`widget/mainmenuwidget.lua`,
`root/proto16`) opens `CommonAskWidget` through
`openMainMenuRootWidget(D,"CommonAskWidget",self,nil,Q,1,A1,A2,1136)`
with `CALL B=10,C=1`, where D is `desktopWidget` and Q the packed question.
The calls are at PCs 29 and 46 for command 24303 (one per variation), PC69
for 24304, PC91 for 24305 and PC113 for 24306. The
[confirm-prompt contract](confirm-prompt-client-contracts.md#pending-work-and-prompt-presentation)
owns the 24304 and 24306 text keys.

`xivl-decomp:docs/script/main-menu-command-route.md`, "Selection", owns the
`openMainMenuRootWidget` tailcall `openRootWidget(D,3,name,parent,true,...)`.
The [root opener contract](desktop-widget-root-slots.md#occupancy-test-and-root-opener)
continues it as `openWidget(D,3,name,nil,parent,true,...)`. The published
[openWidget and openWidgetLocal contracts](content-director-ui-contracts.md#openwidget-inputs-and-results)
then give this creation request, with S the saved input value:

```text
commandCreateWidget(D,"CommonAskWidget",false,self,S,"CommonAskWidget",3,true,
                    nil,Q,1,A1,A2,1136)
```

The widget command path is therefore the bare name `CommonAskWidget`, and
the window name defaults to the same string. Under the positional reading of
the [conditional creation frame](tutorial-widget-creation-frame.md#creation-payload-and-initializer-positions),
`init` would receive `(W,nil,Q,1,A1,A2,1136)`, matching the CommonAsk
initializer frame with question Q and default answer 1. That publication
covers a seven-value payload, and this tuple has more values, so the native
join remains conditional.

## Source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
Original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). Paths are
relative to `lua/scripts/` and `client/script/`.

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `widget/ask/askwidget.lua` | 14551 / 615 | `c5032a2d2d1264c4a01165834f6248a01dc1c4bf7b9f791ce8baf511295398af` |
| `widget/commonaskwidget.lua` | 2851 / 133 | `d304094ae53cd9fa82c59166495941f310161ce1fac62c37025bfdb5da3cd8e5` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| `command/system/logoutcommand.lua` | 1627 / 84 | `485450e6e31e5617e23bbf4d5816d3a53971d81e90cf004b5161e74f027e2172` |
| `widget/mainmenuwidget.lua` | 58470 / 2605 | `7dfd161c2852a56fd598f47469cc2d7597ba9f0e4b228555a09274674b2b4e41` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/9rz/9rzn1635q.le.lpb` | 5257 / `8541d21030988f4ed5460690156a71a5a0120b68ed38d8db181676b27a23bfe9` | 5244 / `1b0d5e2ca4c39b781305b98320eb597337e0d4c0fc0c9167244553dfc49d14c0` |
| `n1635q/7vxxvw9rzn1635q.le.lpb` | 1559 / `cad77ceafd51dfc6b59da750b7beb01d2d25f3641ba2e52ded2d198964c56b9c` | 1546 / `1a023c9f9d0b995d1640fd6e7c211b823d6eae0dd1970a615adc18e79d1c041b` |
| `n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 / `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` | 32983 / `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |
| `7vxx9w6/rlrq5x/yv3vpq7vxx9w6.le.lpb` | 980 / `a82225b09637c33e8b09917c51ee2bf85df4df0a186a73d41ede762c1a96305b` | 967 / `11cfcdaefe4072431eca9b732b3e8f0d15f5de23b2a21ce5b81574c251251c3e` |
| `n1635q/x91wx5wpn1635q.le.lpb` | 19491 / `c0e1782a3ca183fcaa520a16320946f62d3fc861c74978cde19ea20fcd064b0a` | 19478 / `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2` |

Prototype indices and PCs are zero-based. Code starts are decoded-payload
offsets, and PC n is at start plus 4n. Canonical windows run from the
definition to its root binding.

| Method | Canonical lines | Root binding PC | Prototype / code start |
| --- | --- | ---: | --- |
| AskWidget `initAsk` | `askwidget.lua:11-85` | 9 | `root/proto0` / `0x1A5` |
| AskWidget `processAfterShow` | `askwidget.lua:88-105` | 12 | `root/proto1` / `0x4AC` |
| AskWidget `ask` | `askwidget.lua:108-248` | 15 | `root/proto2` / `0x583` |
| AskWidget `initialWidget` | `askwidget.lua:485-533` | 24 | `root/proto5` / `0xFC4` |
| AskWidget `pageChange` | `askwidget.lua:536-596` | 27 | `root/proto6` / `0x11D9` |
| AskWidget `getPageNum` | `askwidget.lua:599-615` | 30 | `root/proto7` / `0x13F3` |
| CommonAsk `processAfterShow` | `commonaskwidget.lua:97-114` | 15 | `root/proto2` / `0x495` |
| WidgetBase `setCancelCondition` | `widgetbaseclass_common.lua:1338-1351` | 176 | `root/proto58` / `0x4435` |
| WidgetBase `addItem` | `widgetbaseclass_common.lua:3017-3035` | 500 | `root/proto166` / `0x778F` |
| Logout `eventConfirm` | `logoutcommand.lua:28-56` | 12 | `root/proto1` / `0x1BD` |
| MainMenu `executeCommand` | `mainmenuwidget.lua:1916-2191` | 57 | `root/proto16` / `0x3811` |

Reproduction uses `tools/retail_script.py:decode_lpb` and the
`ChunkReader` and `instruction` definitions in
`tools/build_quest_contracts.py`. Check complete payload consumption, root
closure assignments, the comparison operands and jump targets named above,
and each CALL and RETURN width. The canonical decompile renders the PC98
default-answer test as a joined condition and must not replace the original
jump structure.
