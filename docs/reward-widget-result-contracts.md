# Reward and delivery widget results

These recovered Ask widgets return client-side selections or acknowledgements.
Their result values do not prove a server grant, inventory mutation, or reward
authority.

`ContentRewardWidget` sets base ask result `1` for `Button_Confirm` and `-1`
for its cancel command (`contentrewardwidget.lua:344-351`). `RewardSelectWidget`
sets the result to `work.index + 1` for a valid item selection; its cancel and
close commands return `-1` (`rewardselectwidget.lua:520-541`).
`TreasureListWidget` stores the selected row as `A3 + 1`, opens a
`CommonAskWidget`, and copies the stored index into its ask result only when
that child result is `1`; closing the selector sets `-1`
(`treasurelistwidget.lua:34-62`). These are selection/confirmation results,
not item IDs or evidence that the selected reward was granted.

`QuestRewardWidget` sets result `1` for both operate and cancel when its mode is
`1` (`questrewardwidget.lua:64-72`), so that result cannot distinguish those
two UI actions. `QuestDeliveryWidget.getAskResult` returns a seven-value tuple:
chosen package, chosen item slot, chosen count, item name index, catalog ID,
attached materia count, and a final `-1` while waiting for price or `0`
otherwise. A canceled ask or missing item returns seven zeroes
(`questdeliverywidget.lua:1836-1889`). The tuple is a client selection/result;
it does not establish item ownership at the receiver, a server-side delivery,
or a completed quest or Hamlet mutation.

The [Hamlet](hamlet-delivery-selection-flow.md) and
[Company](company-supply-delivery-flow.md) caller flows qualify their
class-specific result adaptation and rearm boundaries.

| Decoded script | Canonical source SHA-256 | Reviewed decompile output SHA-256 | LPB and decoded-payload identity |
| --- | --- | --- | --- |
| `lua/scripts/widget/ask/contentrewardwidget.lua` | `1a8973cb83bb82a9c1695b2aa4561081d5bd3c75d2104cc95443e281bfc0790b` | `d31d283d4b1cf830e15cacdcf4cfcde6def149052b716da5e6ce4e2423968187` | `n1635q/9rz/7vwq5wqs5n9s6n1635q.le.lpb`; LPB SHA-256 `c7e90eddf2671f4aab832f580d1c459fa4a1853cf27b1937c28d1e0ceecede94`; decoded payload SHA-256 `f0f91fbb8dae7a4fcfbe6a0baa8f27bbd2b54275cc2f0aee1dcc49ffe5be95a4` |
| `lua/scripts/widget/ask/rewardselectwidget.lua` | `ee220caa549be99a3b69b557822fabd64004125f6e33f6d91596fc6347899548` | `9e075b9d15cae3e480c085b37fcc592a142aee062907addb75deab9eba61e46f` | `n1635q/9rz/s5n9s6r5y57qn1635q.le.lpb`; LPB SHA-256 `71a3875baac970973bf38d6a2556ff5ba92c9b800b67b703c1338e4fdad87911`; decoded payload SHA-256 `49e4efc9b59917ca88ea3ee2af319012d79b0a434c559dda68935d8dff603a5b` |
| `lua/scripts/widget/ask/treasurelistwidget.lua` | `5ffe819e45ff3b2746af386acaaa43ba94ed9a9dcd256ce12463f6a35a165361` | `382aef7289ede540ffbcc7539e259d1445206e81c2a95028063f0e781750242b` | `n1635q/9rz/qs59rps5y1rqn1635q.le.lpb`; LPB SHA-256 `7c13cab369aa2064bfdd194a2add5827fb9a701870344ce5e4d5cacdaf30510c`; decoded payload SHA-256 `bf59a0cd6ea9b799cdef949785a2527de7c4a1ac6c1c7ed356e0b6bacc5df07e` |
| `lua/scripts/widget/ask/questrewardwidget.lua` | `1f12737ea03fbdd931654e3b47fdd745889e86cef5e0793ef2a6c933b1d9a03d` | `e39c889289ce1dc2b3e92f71e2d49f22da75f2ec5f27e3d0896ce749e096587f` | `n1635q/9rz/tp5rqs5n9s6n1635q.le.lpb`; LPB SHA-256 `bf3921862d3905791a22bfa8d1911c4835e8cae25f68af5b49d8102afbd887e1`; decoded payload SHA-256 `21f32f0fdbbbfcdd39100dfee22067cb6929f60685752f10b2bc7759f667cea4` |
| `lua/scripts/widget/ask/questdeliverywidget.lua` | `ba34706ada144e2f7d2d91c7acf6b4d6f31fcb9f9ec7a95a1a3d00345f35640d` | `b0311ccc3a72564f5e86d5421ec446dc4d3f2229fe8b5135496e9bcf06c416ae` | `n1635q/9rz/tp5rq65y1o5sln1635q.le.lpb`; LPB SHA-256 `224ce2413d952356856d6a58fdaf01ce7985fc751555aeb3b6f384f2db5ace63`; decoded payload SHA-256 `3985b32874a8a105dc464cbd2d703029fd79b48b78198382e2ce72a3a7ad9a08` |

Canonical source hashes are pinned in `manifests/scripts.json`; LPB identities
and decoded payload hashes are pinned in `manifests/retail_lua_coverage.json`.

## RewardSelectWidget opening and keyboard selection

The [Impish Impositions caller](impish-impositions-client-contract.md#runner-menu-and-callback-values)
opens `Ask/RewardSelectWidget` with one requested result. The shared
[Ask wrapper](materia-meld-client-contract.md#craftjudge-callback-contract)
uses category 4 and forwards the remaining operands to `initAsk`. In this
call, `RewardSelectWidget.initAsk(self, actor, 19, remembered, ...)` receives
catalog IDs 8013301, 8013302, 8013303 and 8013304 in positions 4-7 after
self. `initAsk` has 20 fixed parameters including self and reads neither
of the first two operands after self. It calls `setInitialData` with
positions 4-19 (root/proto1 PCs 224-241) and, if `remembered > 0`, stores
`remembered - 1` as both `work.index` and `work.focus` (PCs 257-264).
`setInitialData` (`root/proto2` PCs 0-68) requests up to 16 rows in caller
order, then flushes the first tab through its final `-1` request.
`makeRewardItemList` (`root/proto19`) skips nil item operands and requests
`setItemToXml(1, slot - 1, catalogId)` for each nonnil operand. The row
helper (`root/proto18`) uses `player:createVirtualItem(catalogId, 1)` and
returns false for a nil item. The four caller IDs resolve to `_item`
column 0 `Normal/StandardItem`. Their English `xtx_itemName` column 5
values are Pumpkin Head, Unripened Pumpkin Head, White Pumpkin Head and
Ripened Pumpkin Head in that order.
[xivl-client-data:manifests/tables.json](https://github.com/XIVLegacy/xivl-client-data/blob/e34b3da2cfa4bd023f029eae9af31413ab63dbe8/manifests/tables.json)

`getFormName` (`root/proto0` PCs 0-1) returns `ItemListWidget`. In the
installed standard form, line 65 selects `DataTemplate_ItemList` and
`ControlTemplate_ListBox` for `ListBox_TabItem_1`, bound to the first tab
maker. The selected template's `Selection` event trigger (lines 75-77)
executes `UILuaCommands.Selection` with kind `Int` and properties
`SelectedIndex`, `IntData.Value0`, in that order. The Lua `initListBox`
(`root/proto16` PCs 5-24) assigns the tab number to `IntData.Value0` and
subscribes the list to `UILuaCommands.Selection` and `UILuaCommands.Cancel`.
For this first tab the number is 1. `initAsk` also subscribes `_widget`
to `UILuaCommands.WidgetClose` and `TabItem_1` through `TabItem_5` to
Cancel (`root/proto1` PCs 101-115). The inherited helpers in
`widget/widgetbaseclass_common.lua` use priority 5 in `root/proto55` PC4,
`root/proto58` PC7 and `root/proto59` PC4.
[xivl-decomp:docs/resource/sqwt-xpath-data-sources.md, carrier identities](https://github.com/XIVLegacy/xivl-decomp/blob/c1c7e5fd49af0a26e1ee3543a31c17bdb89ee03b/docs/resource/sqwt-xpath-data-sources.md#carriers-and-script-feed)

STATIC. In the default Layout0 binding table, Enter row 11 is
`ApplicationCommands.Operate` and Escape row 20 is `UILuaCommands.Cancel`.
For the standard ListBox interface table `0x010720EC`, Executed slot 65
is `0x0096ED40`. Its Operate branch (`0x0096ED83..0x0096EE02`) maps the
event source to a row index through `0x00960DE0` and executes
`Selector.SelectIndex` (`0x0135B530`) with kind 1 when the index is
nonnegative. The same slot accepts that command while unhandled, reads
its int at event `+0x7C` and calls `0x0096EC00` at `0x0096EE40`. That
function requests the `SelectedIndex` write at `0x0096EC4E` before
routing `Selection` at `0x0096ECA5` for an index other than -1. The
`Selection` event descriptor is `0x0135B518`, initialized at `0x00F24890`
with ID `0x3B`. These are branches for an admitted row source and command.
[xivl-decomp:docs/script/main-menu-command-route.md, key bindings](https://github.com/XIVLegacy/xivl-decomp/blob/c1c7e5fd49af0a26e1ee3543a31c17bdb89ee03b/docs/script/main-menu-command-route.md#key-bindings)

The inherited dispatcher re-reads `SelectedIndex` using the sender control
name and suppresses a negative read (`widgetbaseclass_common.lua`,
`root/proto13` PCs 41-55). The widget's own Selection handler takes that
index and the tab number as `work.focus` and `work.listbox` (`root/proto25`
PCs 6-9). It returns false if the ask has finished and refreshes without
setting a result when there are no items or focus is at or above the
filtered count (PCs 0-30). Otherwise it refreshes through `updateListFocus`,
which reads source `Index` after writing `FilteredIndex` and updates
`work.index` for a nonnegative mapped value (`root/proto6` PCs 59-68,
`root/proto14` PCs 13-22). It then sets the selected border and requests
base result `work.index + 1` (`root/proto25` PCs 31-44). Thus a successful
second row selection on the four-item caller list supplies local result 2
when the displayed order and source order agree. Cancel and WidgetClose
supply -1. When the base wait completes and the shared wrapper closes the
widget, its two return slots are the completion flag `true` and the local
result. Live focus, rendering, historical invocation and server settlement
remain unmeasured.

PCs are zero-based. Replay the LPBs with `tools/retail_script.py` and
`tools/build_quest_contracts.py:ChunkReader`, and verify the installed
SQWT pair using the linked carrier recipe. The native branches are from
Ghidra 12.1.4 and LLVM 21.0.0 disassembly of the 1.23b `ffxivgame.exe`,
image base `0x00400000`, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
All native addresses are VAs. Command and event initializers identify the
names at `0x01072624` and `0x010726AC` respectively.

### First-tab vertical focus

STATIC. For an eligible Layout0 form, key binding rows 1013 and 1031
request `ApplicationCommands.MoveFocus` with kind 1, directions 2 (Up)
and 4 (Down), and `SqwtShowAnchor=True`. The ListBox `PreviewExecuted`
slot `+0x100` selects `0x009641E0`. Its unhandled, bound-list branch
requires mask 4 at list `+0x47C` and a nonnegative row resolved from the
current anchor recipient through `0x00960DE0`. The directional loops
scan toward smaller or larger filtered row indices and test eligibility
through `0x00961810`. An initial press sets distance 1 (`0x0096426D`),
so an eligible adjacent row is the candidate. An ineligible row can be
skipped. The repeat branch adds a file-backed double zero at `0x0096427D`
and caps the distance at 4.0. A changed eligible index requests
`SqwtFocusedIndex` at `0x0096446F` (Down) or `0x00964546` (Up), then
marks the command handled.
[xivl-decomp:docs/resource/sqwt-listbox-constructed-parts.md, Layout0 vertical keyboard focus](https://github.com/XIVLegacy/xivl-decomp/blob/c1c7e5fd49af0a26e1ee3543a31c17bdb89ee03b/docs/resource/sqwt-listbox-constructed-parts.md#layout0-vertical-keyboard-focus)

The local wrap branch requires at least two rows, a nonrepeat event and
`KeyboardNavigation.DirectionalNavigation` parsed as `Cycle` by
`0x00915570`. `0x009642E2..0x00964338` reads the attached property from
the ListBox's own map (`0x0095F020 -> 0x0095EC10`). With current focus
and anchor indices aligned and no eligible row beyond the current one,
this local route changes no index unless the wrap gate passes
(`0x009643EE..0x00964458`, `0x009644DB..0x00964538`). The standard form
line 62 assigns `Cycle` to ancestor `TabControl_ItemList`; line 65 gives
no such local value to `ListBox_TabItem_1`. An unhandled command can
continue to the parent focus route. Its final target at an edge and the
initial anchor and container state remain unmeasured.

An admitted focus transfer can route `GotAnchor` through `0x0091B890`.
An anchor made visible after the handled key command can also route
`GotAnchor` to the then-current recipient (`0x0091BB76`, `0x0091BBB3`).
ListBox input table `0x010720EC` slot `+0xDC` is `0x0096FAA0`. After the
base handler, an unhandled event with a changed row index and enabled
property holder writes `AnchoredIndex` at list `+0x498` and passes
its descriptor `0x0135B620` to `0x00953BA0` (`0x0096FAC2..0x0096FB16`).
Property ordinal 3 selects `0x0096F440`'s `AnchoredItem` arm, which
routes descriptor `0x0135B500` at `0x0096F592`. These events require
current recipients and delivery through the list.
[xivl-decomp:docs/resource/sqwt-window-trigger-order.md, focus notifications](https://github.com/XIVLegacy/xivl-decomp/blob/c1c7e5fd49af0a26e1ee3543a31c17bdb89ee03b/docs/resource/sqwt-window-trigger-order.md#attachment-and-conditional-focus-notifications)

The selected `ControlTemplate_ListBox` trigger (lines 72-74) requests
`UILuaCommands.AnchoredItem` with `AnchoredIndex` and `IntData.Value0`,
then separately requests `UILuaCommands.EnterSelectorKeyboardFocus` with
the template parent's name. `initListBox` subscribes the first command
on `ListBox_TabItem_1` at priority 5 (`root/proto16` PCs 14-17). The
handler `processUICommandDefault` (`root/proto26` PCs 0-24) checks for a
finished ask, rejects a nil tab and a nil or negative row, then stores
`work.listbox=1` and `work.focus=row` for this first-tab event and requests
`setCommonTimer(0.2)`. This branch writes no ask result. `processTimer`
(`root/proto27` PCs 0-21) maps focus to source index and refreshes the
window. `setWindowFocus` requests logical focus for a nonempty control
name and requests keyboard focus only when the current focused widget
is this receiver (`root/proto8` PCs 0-14).

## ContentRewardWidget caller routes

Each method below calls `askEventModeWidgetYield` for
`Ask/ContentRewardWidget` in mode `1`, passing its own actor instance and a
trailing `1`. These call sites establish a widget open request; they do not
prove that a reward was granted.

| Caller method | Decoded script | LPB resource and pinned identity |
| --- | --- | --- |
| `GuildleveWarpPoint.eventGuildleveReward` | `lua/scripts/chara/npc/object/guildlevewarppoint.lua` | `729s9/wu7/v8057q/3p1y6y5o5n9suuv1wq.le.lpb`; LPB SHA-256 `AAF4816A2542A8365F2738C9958083C07EDD9052ABA4E069CB29C830E63FF7A4`; decoded payload SHA-256 `1C6EEAC00FB31DCA16E9CF6064DC2EE37A64942B9707D8676305CE887D812186` (`retail_lua_coverage.json:8001-8011`) |
| `PopulaceGuildleveTester.eventGuildleveReward` | `lua/scripts/chara/npc/populace/populaceguildlevetester.lua` | `729s9/wu7/uvupy975/uvupy9753p1y6y5o5q5rq5s.le.lpb`; LPB SHA-256 `1682C91087183D0C248681DA9235C667C382ECCAF13EB2452AB771A23EB3194C`; decoded payload SHA-256 `E742FA6CA31E61BFBF647B5FBF4941A72FB7E83B588DF3CE6024052F27190993` (`retail_lua_coverage.json:7056-7066`) |
| `PopulaceCompanyGLPublisher.eventGLReward` | `lua/scripts/chara/npc/populace/populacecompanyglpublisher.lua` | `729s9/wu7/uvupy975/uvupy9757vxu9wl3yup8y1r25s.le.lpb`; LPB SHA-256 `0874F59A069F7A6F87B7A01B93D7D91D8D5DD14F749CFF02B05F7BCBCD15EFDF`; decoded payload SHA-256 `0AE20217500C331EC82F660A0A3762523CBC168B3DBCB37B995D2225934FC43C` (`retail_lua_coverage.json:7371-7381`) |
| `PopulaceFactionGLWorker.eventGuildleveReward` | `lua/scripts/chara/npc/populace/populacefactionglworker.lua` | `729s9/wu7/uvupy975/uvupy975497q1vw3ynvsz5s.le.lpb`; LPB SHA-256 `7B71CEC14520C737F79404B6B15DE7996BED6EEE7BAF0970E5D79F0495455883`; decoded payload SHA-256 `93DC837772665914D81C04993645B1CC90020084BF5F3E687DC49ED7DFB16E2D` (`retail_lua_coverage.json:7221-7231`) |

`GuildleveWarpPoint` also defines `getContentRewardItem` in the same pinned
payload (`root/proto8`). The lookup is gated on `work.glRewardItem > 0`
(PCs `006`-`007`, byte offsets `0xA5E`-`0xA62`). For selector arguments
`R1=1`, `R2=1`, `R3=2`, it loads `work.glRewardItem` through
`itemDataSheet:_getData` with field ID `36` (PCs `016`-`028`, byte offsets
`0xA86`-`0xAB6`). It compares the item ID with numeric constant `1000001` at
PC `031` (`0xAC2`). Equality returns the field-36 result, `nil`, `4405`, and
`work.glRewardNumber` at PC `038` (`0xADE`). Otherwise it returns the field-36
result, `nil`, `4406`, `work.glRewardItem`, and `work.glRewardNumber` at
PC `047` (`0xB02`). This is a client-side getter tuple. The constant's domain
meaning and any server-side grant or inventory effect are not established.

## Guildleve reward difficulty argument

The selected guildleve reward wrappers copy their twelfth argument after
self directly into `difficulty`. They open `Ask/ContentRewardWidget` in
mode 1 with their actor and a trailing 1, then return two widget results.
There is no addition or subtraction between this event argument and its
stored difficulty. `AetheryteBaseClass` uses `aetheryteWork`; the other
selected actors use `work`.

`ContentRewardWidget.initAsk` calls
`actor:getContentRewardItem(grid,row,column)` over ranges 1-3,1-4,1-2.
For selectors (2,2,1), the selected actor getters return
`(nil,nil,4408,difficulty)` under the conditions below. This passes the
stored difficulty unchanged as the reward label's format argument.

| Actor and event | Original difficulty store | Label condition and original return |
| --- | --- | --- |
| GuildleveWarpPoint.eventGuildleveReward | root/proto1 PC23, 0x5CD | difficulty > 1; root/proto8 PC176, 0xD06 |
| PopulaceGuildleveTester.eventGuildleveReward | root/proto8 PC23, 0x991 | difficultyBonus > 0; root/proto14 PC174, 0xFC5 |
| PopulaceFactionGLWorker.eventGuildleveReward | root/proto8 PC23, 0x46BA | difficulty > 1; root/proto15 PC176, 0x5408 |
| PopulaceCompanyGLPublisher.eventGLReward | root/proto13 PC23, 0x16D4 | difficulty > 1; root/proto19 PC176, 0x1D48 |
| AetheryteBaseClass.eventGLReward | root/proto14 PC23, 0xE10 | difficulty > 1; root/proto20 PC174, 0x1468 |

Canonical methods: `chara/npc/object/guildlevewarppoint.lua:124-174,278-539`;
`chara/npc/populace/populaceguildlevetester.lua:246-296,356-549`;
`chara/npc/populace/populacefactionglworker.lua:3223-3273,3614-3875`;
`chara/npc/populace/populacecompanyglpublisher.lua:681-734,797-1058`;
and `chara/npc/object/aetheryte/aetherytebaseclass.lua:355-405,465-716`,
all below `lua/scripts/`. The widget call is root/proto0 PC208/0x46E;
its nested loop setup is PC194/198/202, 0x436/0x446/0x456.
PCs are zero-based and offsets identify decoded payloads.

The ordinary selected getters suppress this bonus slot for both 0 and 1.
The tester instead uses the separate supplied difficultyBonus. The
non-tester getters' separate reward-amount display path subtracts 1 from
difficulty. That calculation does not change the incoming value or rebase
the label argument.

`xivl-client-data:csv/xtx__text_ui.csv`, row 4408, English column 1,
labels the slot Difficulty Bonus and includes a conditional template with
five ordered star strings. The same row in `xtx__text_ui(2).csv` is plain
Difficulty Bonus. These strings do not identify the active sheet or prove
runtime star rendering.

### Retained received value

The retained `party_battle_leve.pcapng` reward call carries 12 typed
integers `(12487,611,542,0,3,0,12,1000001,5121,0,0,1)`, then END.
The final difficulty argument is 1, with integer tag at application offset
0x80, four-byte big-endian value at 0x81, and END at 0x85. No nil or
actor/reference token occurs. This is main connection 0, s2c 0x0130,
frame 3420/subevent 0, completing packet 5384, stream offset 422974.
Source: `xivl-captures:studies/regional-guildleve-publisher-contract/derived/timeline.csv:62`.
Capture member SHA-256:
`6327e5e1f5cbd51a9baaa9bcbacf53ca51c50a98fe4b66ae3e6bdecd9198089f`.
Application SHA-256:
`4cf5349c4cf0f8de5a3f6066131da836549fb5e52ce8656da835b250fad623c9`.

The capture establishes a reward value of 1. The selected client paths
pass it through and use 1 as the ordinary no-difficulty-bonus baseline.
They supply no reward-packet-to-label +1 conversion. A complete producer
range of 1-5 and zero's server meaning remain **UNESTABLISHED**. In
particular, zero suppression in these getters does not prove that zero is
a defined wire sentinel. Start-widget difficulty labels and choices are
separate from this reward argument contract.

The canonical members and original LPB/payloads matched `scripts.json`
and `retail_lua_coverage.json`. Original Lua 5.1 instructions were checked
with `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/states_for/instruction`,
using Python 3.12.0. The named CSV members matched
`xivl-client-data:manifests/tables.json`; the retained capture and archive
matched their owning member/input manifests.

Capture reconstruction used
`xivl-captures:tools/extractors/extract_00da_00e1_comparison.py:_decode_capture`
after `tools/validate_framing.py:check` passed its framing checks. Exact
typed-value decoding agreed between
`tools/extractors/extract_local_guildleve_dialogue.py:decode_parameters`
and `tools/extractors/extract_regional_guildleve_publisher_contract.py:decode_lua_values`.
These are static and retained-wire observations, not runtime reward tests.
