# QuestDetailWidget answer contract

`QuestDetailWidget` is an `AskBaseClass` widget with a journal mode and an
offer mode. In the offer mode `Button_Undertake` requests base result 1 and
`Button_Refuse` requests -1. Its `getAskResult` returns `true` exactly for a
base result of 1. Close in a mode other than 1 also requests -1. These are
recovered Lua request contracts. They do not establish quest acceptance,
server acknowledgement or a rendered dialog.

The [quest-offer reward display](quest-offer-reward-display.md) owns the
widget's reward and condition rows. The
[journal lifecycle](guildleve-journal-lifecycle.md#detail-selectors-and-map-navigation)
owns `askQuestDetailWidget` and its quest callers. The
[Ask base contract](ask-widget-result-state.md) owns the result setter,
getter and completion poll.

## Initialization and mode branches

`initAsk(W,mode,questID)` (`root/proto0`) replaces `work._temp` with
`mode` as `integer8` and `questID` as `integer32` (PCs 0-11). It requests
`setCancelCondition(W)`, `setCloseCondition(W)` and
`setUICommandCondition(W,"UILuaCommands.Shown")` (PCs 12-18), then writes
both work fields from its formals (PCs 19-22). Visibility, text, icon, help,
condition and reward requests follow (PCs 23-109).

The title and client text requests pass the quest key to `setText`.
`getGrandCompany(questID)` selects the title target. A zero result requests
text key 5025 on `TextBlock_Title` (PCs 41-42 load the name and key). A
nonzero result requests the same key on `TextBlock_GrandCompany` (PC 86 loads
the key). Both paths then request key 5028 on `TextBlock_ClientName`
(PCs 99-100).

`setConditionData` (`root/proto5`, lines 454-579) receives the quest key and
reads quest field 53. A zero field requests key 5030 on `TextBlock_Condition`
with the quest key (PCs 22-23). A nonzero field requests a key computed from
5056 on `TextBlock_Condition` (PC 63 loads the name) and key 5030 on
`TextBlock_RequiredLevel` (PC 82 loads the key).

PC113 compares `work.mode` with 1. A mode other than 1 jumps to the offer
branch at PC174:

| PCs | Offer-branch request |
| --- | --- |
| 174-179 | `setConfirmCondition` for `Button_Undertake`, then `Button_Refuse` |
| 180-195 | `Grid_Bottom_Order` visible, `Grid_Bottom_Progress` and `Grid_QuestHystory` hidden, `Label_Number` visible |
| 196-198 | `desktopWidget:getQuestCount()`, keeping two results C1 and C2 |
| 199-203 | `setText(W,"TextBlock_Explain",5050,questID)` |
| 204-209 | `setText(W,"TextBlock_Number",228,C1,C2)` |
| 210-212 | `setLogicalFocus(W,"Button_Undertake")` |

Mode 1 instead takes PCs 115-173. That branch hides `Button_Destruction` for
quest IDs 110001-110059, 111200-111339 and 110869, and registers it as a
confirm control otherwise. It registers `Button_OpenMap` and `Button_Close`,
disables `Button_OpenMap`, hides `Grid_Bottom_Order`, shows the progress grid
and history, hides `Label_Number` and focuses `Button_Close`.

Both branches continue at PC213 with visibility requests for
`Border_QuestItem`, `Border_QuestItem_Head`,
`TextBlock_QuestItemTitle` and `TextBlock_QuestItem`, whose flag is true after
the mode 1 branch and false after the offer branch (PCs 110, 172 and 213-228).

## Ordinary Journal detail request

For the active quest row path described in
[JournalListWidget modes and row arguments](guildleve-journal-lifecycle.md#journallistwidget-modes-and-row-arguments),
the local `Ask/QuestDetailWidget` child opens with mode 1 and the row's
`JournalID` as `questID`.

The installed `widget/QuestDetailWidget.form` names the root
`Window_QuestDetailWidget` at line 1, imports `common/WINBasis.tpl` at
line 5 and selects its `ControlTemplate_Window_WINBasis` at line 11.
That template's `Shown` trigger at line 9 starts `OpeningAnimation`
at lines 12-19. Its storyboard declares
`CompletedCommand="UILuaCommands.Shown"` at line 13. The three
animations use a 0.2-second duration. The
[native Anime path](https://github.com/XIVLegacy/xivl-decomp/blob/5dc5699/docs/resource/sqwt-anime-property.md#window-handler)
raises the Window's `Shown` event. The Lua command follows storyboard
completion under the
[animation clock](https://github.com/XIVLegacy/xivl-decomp/blob/5dc5699/docs/resource/sqwt-double-animation-clock.md#bounded-nonrepeat-samples-and-completion).

The shared [setUICommandCondition wrapper](action-menu-page-controls.md#event-registration-and-page-dispatch)
used by `initAsk` registers the plain `_widget` command with numeric
priority 5. In `processUICommandDefault` (`root/proto3`), PCs 0-6
compare the command with `UILuaCommands.Shown` and `work.mode` with
integer 1. PCs 7-12 call
`desktopWidget:executeCommandJournalDetailInfo(3,work.questID)`.
An exactly false result opens failure widget 4311 and returns
(PCs 13-20). Other modes skip this request.

The connector's type-3 branch (`root/proto188`, PCs 24-36) reads
`player:getSystemCommand(24211)` and calls
`player:command(command,questID,nil,nil,nil,nil)` if it finds a
command. The fourth formal of the connector is absent at the Shown
call site. The
[command's local guard](guildleve-journal-lifecycle.md#command-mapping)
delegates to
[`canRequestInformation`](player-command-event-routes.md#information-request-guard-and-record-state).
The
[journal capture comparison](https://github.com/XIVLegacy/xivl-captures/blob/a8e89429b1fe4aaa5adef435f886db58126eb60a/studies/quest-journal-map-wire/derived/evidence-map.md)
records command 24211 with quest ID 110658 and eight nils, then a
`qtdata` delivery. The receiver routes that tag to the
[open detail widgets](quest-event-client-contracts.md#quest-journal-and-reward-presentation-widgets).
The static command and capture identify the route and its arguments.
Whether a given local attempt passes the request guard depends on the
current player state.

| Installed SQWT resource | Container bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `widget/QuestDetailWidget.form` | 17212 / `27517dfe9c2577efdb28c037a235c1fdb2bf559346ee29eecc2e4864dfc8d04d` | 17204 / `0a7203b9f1948ab117f8b3c13f6c143acc712978cdbda30b77ff16cdb11c9a00` |
| `common/WINBasis.tpl` | 6278 / `27d03aca012d1554a3cf8ecd1b5e8da22cc7c815c6f92a1d6d0557dad3bcc5aa` | 6270 / `d3227d9200d301ba715250e393d8e09c0ca2d39080754e1ed517692fa7d50700` |

Reproduce the SQWT locators with the basename-keyed Blowfish decoder in
`xivl-tools:tools/research/census_sqwt.py`. Hash the complete decoded
payload before XML parsing.

## Local results

`processUICommandOperate(W,a,control,b,c)` (`root/proto1`) compares its
third argument with control names:

| Control | PCs | Request |
| --- | --- | --- |
| `Button_Undertake` | 1-5 | `setBaseAskResult(W,1)` |
| `Button_Refuse` | 8-12 | `setBaseAskResult(W,-1)` |
| `Button_OpenMap` | 15-26 | `desktopWidget:openChildWidget("MapNavigationWidget",W,true,1,nil,work.questID)` |
| `Button_Destruction` | 29-45 | `desktopWidget:openChildWidget("CommonAskWidget",W,true,nil,packTextParameter(W,5049,work.questID),2,1348,1349)` |
| `Button_Close` | 48-53 | `desktopWidget:closeWidgetDirect(W)` |
| Any other name | 57 | No request |

`processUICommandClose` (`root/proto2`) requests
`desktopWidget:closeWidgetDirect(W)` when `work.mode` equals 1 (PCs 2-7) and
`setBaseAskResult(W,-1)` otherwise (PCs 9-11). The widget defines no
`processUICommandCancel`, so a Cancel delivered to the shared handler reaches
the base method, which forwards to this `processUICommandClose`, as the
[root slot contract](desktop-widget-root-slots.md#abort-sweep-and-deletion)
describes.

`getAskResult` (`root/proto4`) reads one result from `getBaseAskResult`
(PCs 0-1). PC2 compares it with numeric 1. Equality returns one `true` (PCs
4-5), and every other value, including -1, 0 and nil, returns one `false`
(PCs 6-7).

## Offer route composition

`askQuestDetailWidget` passes `("Ask/QuestDetailWidget",1,3,questID)` to
`askEventModeWidgetYield`, which inserts kind 4 and tailcalls
`askWidgetYield` (`root/proto541`). With result count 1, `askWidgetYield`
(`root/proto542`) requests
`openWidgetYield(D,4,"Ask/QuestDetailWidget",nil,nil,false,3,questID)`,
waits through `selectWidgetYield(D,W,true)` and, on an exact `true`, reads
all `getAskResult` results into a table before closing the widget. It
returns `true` with `unpack(results,1,1)`, or one `false` when the opening
is nil or the wait is not exactly true (PCs 0-36). `askQuestDetailWidget`
returns the second value after an exact `true`, otherwise nil.

If the trailing `3,questID` reach `initAsk` as its two formals, the widget
is in the offer branch and its local outcomes compose as follows:

| Local event | Base result | Helper result | `showQuestInfomation` |
| --- | ---: | --- | ---: |
| Operate on `Button_Undertake` | 1 | `true` | 1 |
| Operate on `Button_Refuse` | -1 | `false` | 2 |
| Close or Cancel | -1 | `false` | 2 |
| Operate on `Button_Close` | none | nil, if the wait then observes the widget as not alive | 2 |
| Opening returns nil | none | nil | 2 |

The `showQuestInfomation` column applies the journal lifecycle page's
exact-true test. The offer branch requests no confirm condition for
`Button_Close`, so the `Button_Close` row assumes a delivery that this
branch does not subscribe. Under the positional reading of the
[conditional creation frame](tutorial-widget-creation-frame.md#creation-payload-and-initializer-positions),
`init` would receive `(W,3,questID)`, which the Ask base forwards to
`initAsk`. That native mapping of the opener's trailing values to the
initializer formals is NOT TRACED here. The
[requested-quest opening contract](craft-requested-quest-selection.md#selected-opening-and-result-tuple)
states the same limit for this opener. The `Button_Destruction` CommonAsk
result handler, `processAskResult` (`root/proto8`), is NOT TRACED here.

## Source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
Original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `widget/ask/questdetailwidget.lua` | 23972 / 1072 | `0d1474c6b43cce61d90a75ba0fe32e2b1d77504fd396024ee32a8876ebc8c8ce` |
| `widget/desktopwidget_connector.lua` | 660617 / 26564 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/9rz/tp5rq65q91yn1635q.le.lpb` | 8553 / `f65d63b3a2e6588eb924ad4d521b00a817a51528307a68d401ca58d726cdbc27` | 8540 / `47fda35f2a462b17f7ca8f0ff751e7ac4f3341052cd1ffcfae5d4400f1a0d9ca` |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |

The root defines `QuestDetailWidget` over `AskBaseClass` after requiring
`/Widget/Ask/AskBaseClass`, and binds 14 child prototypes. Prototype indices
and PCs are zero-based, and code starts are decoded-payload offsets with PC
n at start plus 4n.

| Method | Canonical lines | Root binding PC | Prototype / code start |
| --- | --- | ---: | --- |
| `initAsk` | `questdetailwidget.lua:11-277` | 9 | `root/proto0` / `0x2AA` |
| `processUICommandOperate` | `questdetailwidget.lua:280-348` | 12 | `root/proto1` / `0xACB` |
| `processUICommandClose` | `questdetailwidget.lua:351-369` | 15 | `root/proto2` / `0xD29` |
| `processUICommandDefault` | `questdetailwidget.lua:372-435` | 18 | `root/proto3` / `0xDEB` |
| `getAskResult` | `questdetailwidget.lua:438-451` | 21 | `root/proto4` / `0x1038` |
| Connector `askQuestDetailWidget` | `desktopwidget_connector.lua:10078-10094` | 560 | `root/proto186` / `0x18239` |
| Connector `executeCommandJournalDetailInfo` | `desktopwidget_connector.lua:10267-10322` | 566 | `root/proto188` / `0x1870C` |
| Connector `askEventModeWidgetYield` | `desktopwidget_connector.lua:25790-25801` | 1912 | `root/proto541` / `0x32E39` |
| Connector `askWidgetYield` | `desktopwidget_connector.lua:25805-25856` | 1916 | `root/proto542` / `0x32E9E` |

Reproduction uses `tools/retail_script.py:decode_lpb` and the
`ChunkReader` and `instruction` definitions in
`tools/build_quest_contracts.py`. Check the EQ constants and jump targets at
`processUICommandOperate` PCs 1, 8, 15, 29 and 48, `processUICommandClose`
PC2, `getAskResult` PC2 and `initAsk` PC113, and the LOADK operands 1 and -1
at PCs 4 and 11 of the operate handler.
