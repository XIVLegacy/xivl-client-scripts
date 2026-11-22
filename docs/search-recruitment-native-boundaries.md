# Search and recruitment native boundaries

Player-search rows and comments reach a native widget consumer. Recruitment
results reach `PcMatchingFindWidget` through native property updates. The
[wire contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md)
and its
[evidence manifest](https://github.com/XIVLegacy/xivl-client-structs/blob/main/manifests/search_recruitment_wire_contract.json)
own packet offsets, PE identity, instruction authentication and the complete
Lua/LPB identities. The purpose selectors remain documented in the
[party matching contract](party-matching-client-contract.md).

## Player search

`PcSearchWidget.init` configures operator request and child-widget conditions
and writes `XmlDataMaker_Data.string_command_line`, using `mode_widget` when
no argument is supplied. `processAfterShow` asks the desktop widget for player
experience information. Its `update` method writes current-skill information,
class/level rows and a terminating class value -1, then sends
`UIOperatorCommands.Reply` value 1. `processUIOperatorCommandRequest` supports
Tell, party invitation by name and the request-to-join-party status toggle.

These Lua methods do not construct the search filter record or consume a
wire-row argument list. The native `PcSearchWidgetOperator` builds the
serverbound `0x01DD` filter request. The application dispatcher consumes
clientbound `0x01DF` and `0x01E0`. `PcSearchContractor` callback slot 1 at
`0x00874610` calls `FUN_00693B50` to project cached native records and comment
pointers into the widget. This is a native callback slot, not a
LuaActorImpl receiver slot.

Evidence: `lua/scripts/widget/pcsearchwidget.lua:11-53,58-73,121-179,205-255`.
The original Lua 5.1 payload identifies `processAfterShow` as prototype `0.1`,
PC 1..11, code offset `0x359`; `update` as `0.3`, PC 1..42, code offset
`0x52A`; and `processUIOperatorCommandRequest` as `0.5`, PC 1..35, code offset
`0x7D1`. The decoded script SHA-256 is
`80cb01f52b28bd3273aa8cd69d7906b5bf21eb54bc8cfd6f6a81511b2c45cd5f`.
The original LPB payload SHA-256 is
`e25be2fa13ce9e9b66c1c658076493d632722226080aa93574590acdb024a122`.

### Selected Search list templates

MEASURED. The standard `widget/PcSearchWidget.form` declares exactly two
ListBoxes. Both select `ControlTemplate_ListBox` explicitly and use
`DataTemplate_PcSearchList` as ItemTemplate. Both have IsTabStop false,
IsHitTestVisible false, Width 628 and no inline children. Their ItemsSource
bindings use StaticResource makers and Mode OneWay.

| ListBox | Form line | Height | Maker key | XPath |
| --- | ---: | ---: | --- | --- |
| `ListBox_PlayerInformation` | 30 | 40 | `XmlDataMaker_PcSearchListPlayer_Key` | `/XmlDataMaker_PcSearchListPlayer_XPath` |
| `ListBox_SearchResult` | 152 | 280 | `XmlDataMaker_PcSearchList_Key` | `/XmlDataMaker_PcSearchList_XPath` |

`widget/PcSearchWidget.tpl` defines `ControlTemplate_ListBox` with TargetType
ListBox at lines 2-14. Its only direct child is ControlTemplate.Triggers.
It has no visual root, Setter or ContentPresenter. Its three EventTriggers
are Selection -> `UICommands.Selection`, MouseEnteredItem ->
`UICommands.EnterSelectorMouseFocus`, and AnchoredItem ->
`UICommands.EnterSelectorKeyboardFocus` (lines 4-12).

The separate `DataTemplate_PcSearchList` at lines 33-95 sets IsTabStop false
and contains one Grid visual root. Its Button_SearchResult has height 40,
Command `UILuaCommands.Operate`, and a Grid with two Auto rows and five Auto
columns. Descendant text, icon, visibility and opacity bindings read row
attributes such as `text_textblock_player_name`, `text_textblock_comment`
and `text_textblock_location`. This DataTemplate has no ContentPresenter or
nested ListBox. Each maker supplies the count and data of its rows.

The headings and empty/result controls are siblings outside the lists.
The form declares `TextBlock_PlayerInformation` with `@11025` (line 25),
`TextBlock_SearchSetting` with `@11026` (line 41), and
`TextBlock_SearchResult` with `@11034` (line 147). Grid_SearchResult explicitly
declares Visible (line 139). `TextBlock_NoContents` uses `@11058` alongside
the result ListBox (line 153). TextBlock_MaximumOver uses `@11059` and
TextBlock_HitCount has no literal Text (lines 161-162). Those three controls
have no explicit Visibility declaration here. The markup alone does not
choose their effective visibility or supply a hit count.

STATIC. Native ListBox construction supplies an embedded items panel and
viewer, inserts the viewer as a visual and logical child independently of
the outer Template, and gives that viewer its own presenter template. The
[constructed item viewport](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/sqwt-listbox-constructed-parts.md#constructed-item-viewport)
records the exact constructors, attachments and conditional composition.
The same page records the bare outer presenter selected by ItemListWidget.

INFERRED. The constructed item host remains available under this selected
Search template. The outer template contributes the triggers. The two
makers and separate ItemTemplate provide the generated rows. An empty
maker supplies zero row visuals. This contract covers the measured
trigger-only shape. Native initial maker contents, later visibility writes,
search success, scrolling and observed pixels remain unverified.

The form identity is in Selected original inputs below. The template carrier
is 9428 bytes, SHA-256
`3f00ec92eaad78105bb946d76b3a9f920721f3258eb3822783789048d66b096d`.
Its decoded markup is 9420 bytes, SHA-256
`14bbe467d89e0ed28477a7c00bee25e991795fdfe24a709b968cbd94c98aa87c`.
Both inputs were decoded with basename-keyed Blowfish, re-encrypted
byte-for-byte and inspected as namespace-aware XML. Direct-child and
descendant counts were checked independently of visual rendering.

### Main Menu root open and close

STATIC. Main Menu row 7 requests
`desktopWidget:openMainMenuRootWidget("PcSearchWidget", self)`, with no extra
mode argument (`widget/mainmenuwidget`, `main/f1` PCs 70-76, zero-based).
The [Main Menu route](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/script/main-menu-command-route.md#selection)
owns row 7's text id 2130 and Help id 75739. Connector `main/f538`
PCs 0-15 refuses when static widget 17 is shown with exact true, otherwise
tail-forwards `openRootWidget(3,name,parent,true,...)`. The latter refuses
an occupied root index before opening. The existing
[root lifecycle](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/script/main-menu-command-route.md#community-menu-close)
qualifies creation, close requests and finalization for that shared index.

PcSearch `init`, `main/f0` PCs 0-12, installs Cancel, WidgetClose,
operator Close, OpenChild and Request conditions, then sets modal true.
The shared helpers register the following commands on `_widget`, with
numeric condition 5. PcSearch defines no close-handler override.

| Command | `widgetbaseclass_common` helper and PCs | Shared receiver path |
| --- | --- | --- |
| `UILuaCommands.Cancel` | `main/f58` PCs 0-7 | `main/f13` PCs 21-28 -> `processUICommandCancel`, `main/f16` PCs 0-5 -> `processUICommandClose` |
| `UILuaCommands.WidgetClose` | `main/f59` PCs 0-4 | `main/f13` PCs 31-38 -> `processUICommandClose` |
| `UIOperatorCommands.Close` | `main/f63` PCs 0-4 | `main/f13` PCs 168-171 -> `processUIOperatorCommandClose` |

The common `processUICommandClose` (`main/f17` PCs 0-3) and
`processUIOperatorCommandClose` (`main/f29` PCs 0-3) both request
`desktopWidget:closeWidgetDirect(self)` and discard its results. Neither
compares a control name, mode, selected search row or keyboard-focus result.
The [subscription gate](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/sqwt-command-parameter-consumer.md#subscription-gate)
and actual routed delivery still qualify entry to these Lua handlers.

MEASURED. Standard `widget/PcSearchWidget.form` names
`Window_PcSearchWidget`, uses title `@11024` and directional navigation
Cycle (line 1), merges `common/WINBasisWithTitle.tpl` (line 8), and selects
`ControlTemplate_Window_WINBasisWithTitle` (lines 14-16). That shared
template's `Button_Close` has Command `UILuaCommands.WidgetClose` and
`Focusable=False` (line 11). Its source-named Click trigger plays sound
only (lines 71-73). Its Cancel trigger also plays sound only (lines 80-82).
Delivery of the registered command requests the Lua close.
The Closing storyboard's completion command is separately
`ApplicationCommands.DestroyWindow` (lines 31-44).

The [Layout0 key declarations](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/script/main-menu-command-route.md#key-bindings)
give Escape row 20 `UILuaCommands.Cancel` without a parameter. Thus an
Escape delivered to this admitted widget takes the same close request as
the title button. Modal true does not alone prove the first physical Escape
recipient. PcSearch's Lua does not choose an initial focused control or
request parent focus restoration on close.

STATIC. The close helper rejects nil and exact-false widget liveness before
recursive cleanup. The shared UI callback sets the thread owner to self,
and recursive cleanup postpones that owner's own close until the local
caller clears the thread owner. The root lifecycle link above owns these
branches and the native-delete boundary. Finalization first calls the
superclass, then requests `processWidgetDeleted(self)` for a non-Desktop
widget whose `isInitializing()` is false or nil (`widgetbaseclass`,
`main/f4` PCs 0-16). Connector `main/f534` PCs 0-25 gets the deleted
widget's index. It clears a nonnil root entry when that entry is the same
widget or its liveness result is not exactly true. A different live root
at index 3 survives. A close request's true return alone proves no release.

Operator OpenChild forwards its supplied name to
`desktopWidget:openChildWidget(name,self,true)` (common `main/f13`
PCs 174-178 and `main/f30` PCs 0-5). Connector `main/f536` PCs 0-9 uses
the parent's widget index and passes that parent to `openWidget`.
`PcSearchSelectWidget.init`, `main/f0`, installs Cancel, WidgetClose,
operator Close and OpenChild conditions and sets modal true. It supplies no
close override. Its standard form's `Button_Close` directly declares
`UILuaCommands.WidgetClose` (line 38). When this child has index 3,
finalizing it preserves a different live PcSearch root under the guard
above. Which native operation requests this particular child name remains
untraced here.

The bounded installed test is an admitted row-7 open with root index 3 free,
completed widget initialization and the registered current widget as command
recipient. Deliver title WidgetClose or Escape Cancel, complete finalization,
then check that index 3 is free and the same row can open a fresh root.
An optional child-close test must preserve a different live root. This fixture checks command delivery and root lifetime. Search filtering,
results, network success, native child selection,
exact focus restoration and deletion timing remain outside this close path.

#### Selected original inputs

The PcSearch LPB is `client/script/n1635q/u7r59s72n1635q.le.lpb`, 2403 bytes,
SHA-256 `0f9fa18847d72b5fed5948ef6f9c176a33e8cf81eeddafec71828c4e9418eded`.
Its decoded payload identity is above. PcSearchSelect's LPB is
`client/script/n1635q/u7r59s72r5y57qn1635q.le.lpb`, 577 bytes, SHA-256
`5e086d8cf04cad26ae006655d3908aa086fe5870466407eb4b3a19870bec58b9`.
Its decoded 564-byte payload has SHA-256
`9a5a1fec103e82e82154ccbe5e8e0ad3abb1d3d5d70048e2c043d06ded3dedc2`.
These agree with `manifests/retail_lua_coverage.json`. Bytecode PCs were
checked with `unluac --disassemble` after LPB decoding. The shared class,
common and connector identities are pinned in the root lifecycle evidence.

The following standard installed SQWT inputs were decoded with basename-keyed
Blowfish, re-encrypted byte-for-byte and parsed as namespace-aware XML.

| Path below `client/sqwt` | Carrier bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `widget/PcSearchWidget.form` | 12840, `b15fa2735d3c07d2cf817f3ca25018b262b171e4a24e0a2dcfe9c6bbbfc3f35d` | 12832, `e8bcd312c8eee13f4b8c8a0e57bab7b293966d87560cccdce6b1319e2285b1c4` |
| `common/WINBasisWithTitle.tpl` | 7175, `636d5dd7dbdb0b9d12b08cea875ee0bde729a1e9de9c1cd58eea2d7f66d06daa` | 7167, `93c745038827c5608f09f4aeb2b4186c06138f8f7f7d45c0a2a2483faf11f88b` |
| `widget/PcSearchSelectWidget.form` | 2860, `bf86242d0e924d908ff667edf6eb10208f9547a9f6f118ae9e410c9b15a3fda5` | 2852, `0e656a15f4de4294f2209ee7ec41f3f50047f346bad262b85ab322cc290eeb50` |

## Recruitment results

`PcMatchingFindWidget` uses the native `Result_Maker` control as its result
source. Native `FUN_004B5F50` consumes clientbound `0x01C7`, fills the
recruitment cache and sets operation state 10. `FUN_004BD170` writes the
result properties, publishes an Update action and sets
`Button_Operate.IntData.Value2` to 4.

The Lua `processUICommandDefault` handles `UILuaCommands.PropertyChanged`.
When `getSignal()` returns 4, it updates the grid, sets signal 2 and calls
`updateList`. `getSignal` and `setSignal` read and write user-work integer
slot 3 on `Button_Operate`. `updateList` obtains the count from
`TextBlock_ResultMessage` and reads each `Result_Maker` row's `name`,
`purposeInt`, `placeInt`, `socialInt`, `skillInt`, `currentInt` and
`demandInt`. It formats the display strings and updates the list control.
The -1 count branch displays text 2939 with value 30 and renders 30 rows.
The zero branch displays text 2940. A positive count uses text 2938.

This provides a native wire-to-cache-to-property-to-Lua route for the list.
There is no recovered Lua receiver that directly deserializes `0x01C7`, and
no LuaActorImpl slot is needed for this observed route.

Evidence: `lua/scripts/widget/pcmatchingfindwidget.lua:1805-1837,2106-2329,2481-2508`.
The original payload identifies `processUICommandDefault` as prototype
`0.17`, PC 1..256, code offset `0x3315`; `updateList` as `0.18`, PC 1..231,
code offset `0x3A80`; `setSignal` as `0.24`, PC 1..10, code offset `0x4721`;
and `getSignal` as `0.25`, PC 1..7, code offset `0x47AB`.
The decoded script SHA-256 is
`972e7bbd07c221af78243631c6d88e801a7a5ecd856f3c9f2672a858461c0b8c`.
The original LPB payload SHA-256 is
`c3eb7cde349381d70d70ea5a6d299af412de07645ce7e128e15e6d96e234586a`.

## Acceptance boundary

Serverbound `0x01C6` carries selected cached-row key components. The actual
clientbound answer is also `0x01C6`, consumed by `FUN_004C9D60` through the
application dispatcher. The consumer stores its first application byte, emits
text `0x0B8D` for zero and sets operation state 12.
`FUN_004BF4F0` then branches on answer value 1 while updating the widget.
The static route establishes neither server eligibility nor a successful
retail acceptance session.

The clientbound `0x01C7` list and `0x01C6` answer therefore have substantive
application consumers even though their separate interface callbacks return
without reading payloads. The application dispatcher is `FUN_004CE190`, reached
through `0x004E221D` and `0x004DC715`. A no-op callback in another route does
not negate these direct consumers.
