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
search success and observed pixels remain unverified. The native scroll surface
and its conditional wheel command are described below.

The form identity is in Selected original inputs below. The template carrier
is 9428 bytes, SHA-256
`3f00ec92eaad78105bb946d76b3a9f920721f3258eb3822783789048d66b096d`.
Its decoded markup is 9420 bytes, SHA-256
`14bbe467d89e0ed28477a7c00bee25e991795fdfe24a709b968cbd94c98aa87c`.
Both inputs were decoded with basename-keyed Blowfish, re-encrypted
byte-for-byte and inspected as namespace-aware XML. Direct-child and
descendant counts were checked independently of visual rendering.

### Search result scroll surface

MEASURED. The two selected Search ListBoxes described above each use SqwtStyle
`LIB_basis`. The 628 by 280 `ListBox_SearchResult` owns its generated results.
The 628 by 40 `ListBox_PlayerInformation` has a distinct maker and item host.
Both Lists use the constructed viewer. The result Button declares Height
40. Its final arranged extent and visible row count remain layout-dependent.

STATIC. ListBox constructor `0x0096D980` supplies a separate panel at `+0x4B0`
and viewer at `+0x7E0`, named `PART_ListBox_ScrollViewer`. The viewer owns a
ScrollContentPresenter with ClipToBounds enabled and publishes its arranged
viewport to the panel. Its vertical bar is Auto, in the constructed Grid's
right Auto column, and its inherited horizontal bar is Disabled. The native
vertical part is `PART_VerticalScrollBar` (`0x00970B63`, name `0x010730AC`),
with `PART_UpButton`, `PART_DownButton`, `PART_Track` and `PART_Thumb` as
recorded in the [ScrollViewer part table](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-tab-scroll-text-parts.md#part-keys-set-by-the-constructors). `LIB_basis`
selects `SCB_basis` for the vertical part. The
[constructed item viewport](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-listbox-constructed-parts.md#constructed-item-viewport)
owns constructor, style, clipping and geometry locators. The trigger-only
Search outer template does not replace those parts.

STATIC. Base ScrollViewer constructor `0x00973190`, specifically
`0x009734EC..0x00973514`, constructs one MouseBinding at complete viewer
`+0xB88`. Its command is `ScrollViewer.LineUpCommand`, descriptor `0x0135C0B0`,
its explicit target is that viewer's input interface at `+0xB4`, and its
initial parameter kind is 0. Primary virtual `+0x28 -> 0x00971A40` adds this
binding through the viewer's collection interface at `+0xE0` at
`0x00971EAD..0x00971EBB`. The binding's shared MouseGesture at `0x012E47C8`
has action byte `+0x18 = 7`, modifier mask `+0x1C = 0`, and zero repeat and
release bytes at `+0x20/+0x21` in the PE data.

The admitted MouseWheel descriptor has id `0x1E`. Dispatcher `0x0091D320`
subtracts 1 from that id and uses byte `0x0091D835 = 0x1B`, table cell
`0x0091D7CC -> 0x0091D367`, then input virtual `+0x74`. The viewer table
`0x01071E4C + 0x74` selects `0x0091F270`. That worker visits a returned
provider binding collection, when nonempty, then its own collection through
`0x009212A0`. The walker rejects an already handled event unless the binding
allows it, and requires a nonnull stored target to pass input `+0x5C`.
A gesture match and command virtual `+4` success are required before command
virtual `+8` executes with the stored target. The actual live pointer route
remains conditional.

MouseGesture match `0x0094D8E0` requires the exact current modifier mask.
Its `0x0094DAB5..0x0094DAD2` arm accepts MouseWheel id `0x1E` only for action
7 and a nonzero device virtual `+8` wheel value. `0x0094DB20` puts that signed
value in integer 2 of a kind-3 parameter record (`+0x60`), converting the two
pointer coordinates into integers 0 and 1. Executed event construction copies
integer 2 to event `+0x84`. The
[mouse provider](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/input/sqwt-rapture-mouse-device.md)
and [numeric mouse callback](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/input/sqex-mouse-numeric-callback.md)
own the signed wheel quotient and routed input producer. The
[command event contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-command-parameter-consumer.md#executed-event-delivery)
owns record copying and PreviewExecuted before Executed.

| Native command consumer | Verified vertical effect |
| --- | --- |
| `0x0097144F..0x009714E8`, LineUpCommand | With integer 2 positive, repeat up that many times. With it negative, repeat down its negation. With zero, take one up step after applying the repeat flag from integer 7. |
| `0x009714F0..0x00971524`, LineDownCommand `0x0135BC08` | Apply the repeat flag from integer 7, then take one down step. |
| `0x009713ED..0x0097144C`, PageUpCommand `0x0135C210` and PageDownCommand `0x0135BD10` | Require complete viewer byte `+0x3AE` exactly 2, then subtract or add current viewport height. The meaning and current value of that byte are not established here. |

All those consumers call the base Executed handler first and run only if its
handled pointer still reads zero. Accepted branches mark event `+0x19`.
Viewer primary `+0x12C/+0x120` reaches panel interface `+0x40/+0x34`,
`0x009B7E60/0x009B7DA0`. Each step calls `0x009B7B60`, subtracts or adds
the step to vertical offset, then clears the interface's `+0x2C` mask 4.
With that mask clear, the step helper sets 24.0 layout units from
`0x0107F56C`. With it set, it multiplies the retained step by the double at
`0x01073260` and caps it at 48.0 from `0x0107F574`. Thus an ordinary wheel
step from a clear repeat flag moves the vertical offset by 24 layout units.
The page methods `0x009B7B00/0x009B7AA0` subtract or add interface `+0x20`,
the current viewport height.

The common vertical setter `0x009B7D00` clamps an ordinary finite offset to
the available extent and publishes only a changed value. ScrollChanged then
sets the presenter's vertical translation to the negative offset inside the
clip. The constructed-parts page also records the conditional visible-range
optimization and its retained mask. Its use by the live Search style
remains untraced.

INFERRED. A current admitted result viewer can apply this local scroll route
to its own viewport.
A Search-specific physical hit, active modal/capture selection, intervening
handled event, effective viewport after layout, scrollbar thumb gesture and
repeat cadence remain UNKNOWN. No original client execution or observed
Search scroll is claimed. A bounded wheel consumer needs the current owner,
visible clipped surface, zero modifiers and routed-command admission.

### Search checkbox presentation

MEASURED. The standard form declares one ToggleButton,
`ToggleButton_JobCheck`, at line 74 inside Grid_SearchSetting's class-filter
area. It declares IsChecked False, Command `UICommands.Operate`,
SqwtStyle `TOG_basis_checkBox`, Width and Height 16, Margin `0,2,3,0`,
and left/top alignment. It has no children, Content, explicit Template,
local Style, IsEnabled or Visibility declaration. The adjacent
sibling TextBlock_JobCheck uses `@11067` (line 75). The form and its
selected templates contain one ToggleButton in total.

The form names `common/default.style`. Its ToggleButton style
`TOG_basis_checkBox` has two referenced parts (lines 3464-3467):
CheckedButton uses Button style `CHB_basis_checked`, and UncheckedButton
uses Button style `CHB_basis_unChecked`. Each referenced Button style has
one Frame part (lines 1409-1432).

| Frame condition | Checked skin | Unchecked skin |
| --- | --- | --- |
| SkinNormal, SkinDisabled | `CHB_basis_checked_N` | `CHB_basis_unChecked_N` |
| SkinHover, SkinActive, SkinAnchored, SkinReserved | `CHB_basis_checked_H` | `CHB_basis_unChecked_H` |
| SkinFocused, SkinDroppable | `NULL` | `NULL` |

The four selected skins are one-by-one CellSkins with one Stretch Cell,
HitMargin 2 and a 20-by-20 source rectangle in the declared
`common/default.dds` sheet (`common/default.skin` lines 439-450).
This source extent is separate from the form's declared 16-by-16 control
and the effective arranged or physical pixel extent.

STATIC. The [native Toggle skin profile](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/action-menu-timer-icon-style.md#conditional-initial-toggle-skin)
orders the own-key groups UncheckedButton then CheckedButton, independent
of their order in this style XML. With the constructor seeds retained,
group 0 and condition 0 select UncheckedButton Frame SkinNormal.
The [checked callback](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/input/game-controller-startup.md#checked-state-callback-changes-the-image-part-index)
requests image-part index 1 or 0 under its mutation guards. These published
paths select the retail Frame from the effective checked state. Physical
input acceptance remains unverified.

The native operator can restore the checked state. In the identified PE, routine
`0x00691F30` resolves the `ToggleButton_JobCheck` name at
`0x00692253..0x0069227E` and retains its result at receiver `+0x78`.
At `0x006930E7..0x006930F6` it loads the byte at `0x01342BF8`, loads
that retained toggle as ECX, and requests the published IsChecked setter
`0x0095D440(value,0,1)`. This setup can replace the form's declared False.

The same setup routine resolves Button_Reset and stores it at `+0x74`
(`0x0069220B..0x00692236`). Handler `0x00693650` compares its control
argument with that retained value at `0x00693729..0x0069372C`.
After the matched branch's preceding calls return, it zeroes the cached
byte and requests `0x0095D440(0,0,1)` on receiver `+0x78`
(`0x0069378B..0x0069379B`). Runtime delivery, mutation and a Reset click
remain unverified.
Ghidra supplied leads, and LLVM disassembly of the identified PE
corroborated the control offsets, arguments and callsites.

The default style and skin identities are pinned in the
[numeric presentation input table](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/damage-plate-numeric-presentation.md#identity-and-method).
Their installed carriers were decoded, re-encrypted byte-for-byte and
parsed as XML. The selected number-input template
`common/LABBasisNumberInputBox.tpl` is 1059 bytes, SHA-256
`91c6aec1f2c3445faad6570d934eb4392afcd0aabdff36ae8cfbc69a48d269af`.
Its decoded 1051-byte XML has SHA-256
`546672a02cb526a810bbe191a574832499b3208ff294df5940c184fb3e729922`.
Form and other selected template identities are recorded on this page.
Other cached-state producers, ordinary toggle click routing, job-filter
semantics, result changes and first live pixels remain outside this paint
contract.

### Fresh native Search message setup

STATIC. The stock setup request is `UIOperatorCommands.AfterLuaInit`.
`WidgetBaseClass._onInit` sends BeforeLuaInit, calls the selected `init`,
then sends AfterLuaInit (`widget/widgetbaseclass`, `main/f0` PCs 87-98).
Initializer `0x00F14755..0x00F14774` registers AfterLuaInit with command
id 25. Its RoutedCommand constructor `0x00928D90` retains that id at
command `+0x78`.

The [form gate](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/sqwt-command-parameter-consumer.md#form-gate-object)
factory selects PcSearchWidgetOperator for Window_PcSearchWidget. An active
gate receives Executed before the Lua subscription lookup. Its table
`0x00FC8424` slot 42 selects `0x00695C20`. That dispatcher requires
operator `+0x1C` bit `0x40000000` clear and the root Window's
`+0x3E0` bit `0x20` set (`0x00695C20..0x00695C39`). The latter is the
published [SqwtIsEnableInput bit](https://github.com/XIVLegacy/xivl-client-structs/blob/e8061eda875c38a3816eeafb81476df6dfbba8b4/docs/sqwt-window-input-property.md).
The switch subtracts 1 from the command id. For id 25, table cell
`0x00695F28` selects `0x00695E57`, whose call at `0x00695E66` invokes
virtual `+0x74`. PcSearch table cell `0x00FC8498` selects setup
`0x00691F30`. The guarded command delivery starts this setup.

PcSearch `init` with no argument writes `mode_widget` to
`XmlDataMaker_Data` row 0 attribute `string_command_line` (`main/f0`
PCs 24-29). It makes no list Update request. Common `setListProperty`,
`main/f169` PCs 0-5, only forwards to `_setListProperty`. The
[native maker contract](https://github.com/XIVLegacy/xivl-client-structs/blob/e8061eda875c38a3816eeafb81476df6dfbba8b4/docs/stub-overload-native-contract.md#lists)
separates SetAttr's XML attribute store from Update's recount and filtered
view rebuild. The native setup reads the stored string through
`0x009452C0` at `0x00692765` before any Update.
The later class-information `update` sends `UIOperatorCommands.Reply` with
1. Reply is command id 23 and selects virtual `+0x6C` through
`0x00695E27..0x00695E36`, a different callback from this setup.

Setup resolves TextBlock_NoContents to operator `+0x68` at
`0x00692567..0x00692592` and TextBlock_MaximumOver to `+0x6C` at
`0x006925AF..0x006925DA`. After its earlier helper call at `0x00693199`,
the normal continuation requests these changes in order:

| Control and property | Requested value | Instruction range |
| --- | --- | --- |
| `TextBlock_NoContents.Text` | `@11064` | `0x0069319E..0x006931CB` |
| `TextBlock_NoContents.Visibility` | 2, Visible | `0x006931D0..0x006931E0` |
| `TextBlock_MaximumOver.Visibility` | 0, Collapsed | `0x006931E5..0x006931F5` |

The Text request uses `0x009557D0`, which supplies descriptor
`0x0135A300`. The Visibility requests use `0x0093C2A0` and the
[published 0/2 encoding](https://github.com/XIVLegacy/xivl-decomp/blob/4802bdfe22b04413a283695c301a67239128b19f/docs/resource/damage-plate-numeric-presentation.md#numeric-branch-and-reused-roles).
The property gates govern these setter requests. The initial NoContents
request replaces the form's `@11058` reference with `@11064`.

Fresh constructor `0x00693500` clears operator byte `+0x24` at
`0x0069355F`. Setup compares the stored command-line text with
`mode_widget` at `0x0069277E..0x00692793`. Helper `0x00445E00` returns
zero for equal bytes through the first NUL and nonzero for unequal bytes.
Only unequal text sets `+0x24` to 1. The final setup branch at
`0x0069321C..0x00693225` calls `0x00690360(0)` only for nonzero `+0x24`.
Thus equal default text on a fresh operator skips that automatic query.
The message requests above precede this branch and require no result packet.
Retained operators or different command-line text have different premises.

TextBlock_HitCount has no literal Text in the form. This setup establishes
no initial count-text or Visibility request for it. Result projection
`0x00693B50` is separate: it requires its final flag zero and operator
`+0xF5` nonzero, then formats `@228/i<count>/i200` and sets the hit-count
text at `0x00693D92..0x00693DE4`. Fresh construction clears `+0xF5`
at `0x00693585`. The completed-query helper's zero-count and
equality-to-200 branches belong to result projection.

Ghidra output supplied leads. LLVM disassembly, section-mapped PE reads,
command literals, switch cells and vtable cells corroborated these claims
against the executable identified above. The selected LPB operands were
checked with `unluac --disassemble`. Actual gate installation and lifetime,
property admission, dispatch scheduling, reused controls, result retrieval
and live rendering remain unverified.

### Native setup restores selector captions

STATIC. During the admitted AfterLuaInit setup `0x00691F30`, the normal
continuation restores cached selector captions without a click. After the
numeric and job-checkbox writes, the loop at `0x006930FB..0x00693139`
walks caption records `[0x013431D8,0x01343498)` with stride 0x58. It
makes eight interface calls. Each passes that record's string and byte
`+0x54` to embedded selector interface virtual `+0x18` at `0x00693121`,
while temporarily setting operator current-selector `+0x8C` to the slot.
The preceding selector index is restored on every iteration.

The selected body `0x00690760` supports indices 0 through 4 and returns
without a caption write for indices 5 through 7. Its five supported arms
request Text on each retained TextBlock_ButtonText and Visibility on the
corresponding TextBlock_ThreePoint. A zero flag requests Collapsed and a
nonzero flag requests Visible (`0x00690778..0x006908DE`). The named
owners, default caption references and interface cell are in the
[Reset contract](#search-reset-button-and-retained-first-reply-byte).
First-use `0x00691EE0` supplies those defaults before the restore loop.
A normal reopen restores the saved strings and flags, including a
retained Class choice.

This loop precedes readiness presentation `0x00691AE0` at `0x00693199`,
the initial NoContents requests at `0x0069319E..0x006931F5`, and the
optional nondefault-mode query at `0x0069321C..0x00693225`. This is part of
AfterLuaInit. Successful named-control lookup,
property writes and text resolution remain conditions on rendered captions.
LLVM disassembly and the identified PE's interface cells corroborated the
loop and setter ordering. No original client ran.

### Begin Search activation and first-use filters

MEASURED. The standard form's `Button_Search` declares
`Command=UILuaCommands.Operate`, Content `@11033`, `SqwtStyle=BTN_basis`,
MinWidth 180 and Help value 0 `@79609` (decoded line 134). It is in
Grid_SearchSetting's third row, beside Button_Reset. It has no local
CommandTarget, CommandParameter, ClickMode, Template, Visibility or
IsEnabled declaration. The selected form and template identities are below.

STATIC. The [ordinary Button command path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-command-parameter-consumer.md#button-mouse-source)
qualifies eligible delivered press/release and default ClickMode 2. Its
Click uses the Button as source and original source, then invokes its
stored Command. The omitted parameter retains the shared kind-0 record.
The [Window target fallback](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-command-parameter-consumer.md#actionmenu-arrow-target-fallback)
and keyboard-focus alternative remain conditional. This markup does not
prove the physical OS recipient, capture or initial keyboard focus.

The Operate literal at `0x00FA8674` is registered as native command id 1
by `0x00F0F279..0x00F0F29B`. The active PcSearch form gate sees Executed
before Lua lookup. Its existing operator/input guards are documented above.
For id 1, switch cell `0x00695EC8` selects `0x00695C5B`, which calls
operator virtual `+0x20` at `0x00695C6A`. PcSearch table cell `0x00FC8444`
selects `0x00693650`. The gate passes the routed source as that method's
control argument. This native path does not require a new Lua Operate
subscription or call `processUIOperatorCommandRequest`.

Setup resolves literal `Button_Search` at `0x00FC7B80` and retains its
control at operator `+0x70` (`0x006921C4..0x006921EF`). The search arm
requires its supplied control to equal that value at `0x006937AB`, then
requires nonzero `0x00874590(operator+0x28)` at
`0x006937B4..0x006937BE`. The reader returns contractor byte `+0x14`.
The contractor constructor sets it to 1 at `0x0087454A`. A different sender
or zero readiness byte skips the search arm before query construction.
Matching the command string alone is insufficient.

#### First-use state and query

STATIC. Equal `mode_widget` text on a fresh operator skips command-line
parsing and the automatic query, as documented in the setup section.
There is also a separate retained first-use byte at `0x01342BF9`.
When it is zero, setup calls `0x00691E80`, calls `0x00691EE0`, then writes
1 to it (`0x00692797..0x006927BA`). The latter helper resets the five
search selector vectors, writes lower 1 at `0x01342BF4`, upper 50 at
`0x01342BF0`, and checkbox 0 at `0x01342BF8`
(`0x00691EE6..0x00691F12`). Reopening a Window with the first-use byte
already set does not establish these defaults.

For selector indices 0 through 4, reset `0x00691DC0` calls `0x00870530`
at `0x00691E1F`. It rebuilds the vector from the records selected by
`0x0086FD50`, with stride `0x14`. The row copy at `0x0068FB00` preserves
all `0x14` bytes. These constant source tables have no row whose byte
`+0x11` equals 1:

| Selector | Table VA | Records |
| --- | --- | ---: |
| Status | `0x0104DF20` | 4 |
| Class | `0x0104DFB0` | 22 |
| Region | `0x0104E168` | 5 |
| GrandCompany | `0x0104E1D0` | 5 |
| Location | `0x0104E238` | 46 |

MEASURED. The form declares `CustomControl_LevelFrom` and
`CustomControl_LevelTo` with Type NumberInputBox and Width 64 (lines 92
and 96). STATIC. Setup resolves those literals at `0x00FC7D58` and
`0x00FC7D70`, retaining the lower control at operator `+0x7C` and upper
at `+0x80` (`0x006925F7..0x00692622`, `0x0069263E..0x00692669`).
It sets both controls' minimum to 1 and maximum
to 50, then requests the cached lower and upper values
(`0x00693086..0x006930E2`). It requests the cached checkbox through
`0x0095D440` at `0x006930E7..0x006930F6`. `0x006958B0` writes the decimal
`%d` value through the named property object `0x01345510`.
Initializer `0x00F148C0..0x00F148CA` names that object `Value`.
The query's `0x00695950` reads that same property and converts its string
with `atol` (`0x00695994..0x006959B1`). Successful control construction,
property application and no intervening input remain premises.
Begin Search reads the controls directly. The
[level-editing and title-close paths](#search-level-editing-and-title-close-cache)
separately establish opposite-bound correction and a cache-save boundary.
The [first class-info Reply](#first-class-info-reply-level-range) can replace
these setup values before the first query.

The Search arm tests selector row `+0x11 == 1` and value `+0x0C != -1`
before serializing it. It tests the checkbox's effective checked bit and
serializes both levels only when both are positive. The
[wire request](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-requests)
owns the tag widths and record. With the first-use defaults above retained,
no selector or checkbox tag is emitted. The only filter is tag 2, lower 1,
upper 50. The used tail length is 3. Application dword `+0x00`, word
`+0x06` and unused tail bytes are zero. This is a conditional first-use
query, not a rule to replace current filters with defaults on each click.

Before sending, the native arm clears its cached results, sets operator
`+0x108` to -1, clears the result maker and publishes Update
(`0x00693A59..0x00693AAA`). It passes the `0x104`-byte query to
`0x008746E0` at `0x00693AD2`. That method checks readiness again and calls
emitter `0x004C7300`. Only emitter success clears contractor `+0x14`,
requests the pending presentation with `0x00691AE0(0)`, and returns
success (`0x008746E3..0x0087473A`). The caller then sets operator `+0xF5`
to 1. Failure instead requests NoContents text `@11065` and Visible
(`0x00693ADB..0x00693B22`). Query acceptance is not an empty-result reply.

The bounded ordinary action is an eligible activation of the exact current
Button_Search routed to its initialized current PcSearch operator, with
readiness and current filters preserved. A stock empty-search check also
needs the [result/completion stream](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-results-and-completion):
a latched nonzero token, zero returned rows and matching completion through
`0x01E0`, then the native completion callback. A send, timeout, zero rows
without completion, or the setup's no-query message is insufficient.
Result rendering and historical empty-search traffic are outside this trace.

The executable is the identified 15996808-byte `ffxivgame.exe`, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`,
image base `0x00400000`. Ghidra CLI supplied focused leads. LLVM
disassembly and section-mapped PE reads corroborated command and vtable
cells, branch operands, source tables and property names. SQWT decryption,
re-encryption and namespace-aware XML checks authenticated the selected
button declaration. No original client ran.

### Search level editing and title-close cache

MEASURED. The two controls named above have no local Value, Minimum,
Maximum or Style declaration. Their containing Labels select
`ControlTemplate_Label_NumberInputBox` from the imported
`common/LABBasisNumberInputBox.tpl` (form lines 10, 91-96).
That template's ValueChanged trigger has SourceType Slider and executes
`NumberInputBox.ValueChanged` with one Int read from PropertyName1 Value,
without an explicit target (template lines 2-10).
The [constructed numeric control](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-number-input-box.md)
and [short arrow press](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-number-input-pointer-edit.md)
contracts apply to this exact selected Type NumberInputBox. SmallChange is
1, the rebuilt ones digit is selected, and an eligible short arrow press
requests the selected decimal-place delta through the same bounded Value.
The [digit editor](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-number-input-digit-grid.md)
is a separate embedded editor. These contracts do not establish initial
OS focus or successful physical input delivery for Search.

STATIC. Initializer `0x00F14557..0x00F14576` registers the literal at
`0x00FC902C`, NumberInputBox.ValueChanged, with native command id 16.
Dispatcher switch cell `0x00695F04` selects `0x00695DF7`, which calls
virtual `+0x64` at `0x00695E06`. PcSearch cell `0x00FC8488` selects
`0x00690470`. Under the existing active operator and Window input guards,
it reads current lower and upper Values through `0x00695950`. If lower
exceeds upper and the routed source is exactly the retained lower control,
it writes upper to lower. For the exact upper source, it writes lower to
upper (`0x00690474..0x006904BD`). Otherwise there is no opposite-bound
write. This callback changes the controls, not the two global bound caches.
No new Lua ValueChanged subscription is required by this native path.

The ordinary native WidgetClose arm has a distinct cache boundary. Id 3
selects `0x00695C8B`, then PcSearch virtual `+0x28`, cell `0x00FC844C`,
body `0x00695F40`. It immediately calls `0x006959F0`. That helper invokes
virtual `+0x1C` at `0x00695A20`, before setting operator `+0x1C` bit
`0x40000000` at `0x00695A22` and requesting UIOperatorCommands.Close on
its retained root (`0x00695A42..0x00695A6B`). The save body `0x006917F0`
reads the two current Values and writes lower `0x01342BF4`, upper
`0x01342BF0` (`0x0069180F..0x00691831`). Later normal setup restores
those caches. This proves a save before the admitted native title-close
request, not a save on every edit, arbitrary Lua close, hide or teardown.
The [Cancel source test](#search-cancel-source-and-numeric-restore) below
has a numeric restore arm before this close request.

### Search Cancel source and numeric restore

STATIC. UILuaCommands.Cancel literal `0x00FA868C` is registered with
native id 2 at `0x00F0F2F9..0x00F0F31B`. Switch cell `0x00695ECC`
selects `0x00695C73`, which calls virtual `+0x24` at `0x00695C82`.
PcSearch cell `0x00FC8448` selects `0x00691730`. The existing operator
and Window input guards still apply. This handler uses the routed source
passed by that dispatcher, not an independent editor-active flag.

Let C be a retained lower or upper NumberInputBox and D its selected
NumberLabel. Accessor `0x0069C090` returns C+0x3B84, D, while
`0x0069C080` returns the embedded TextBox at C+0x11D0. D is not proof
of an active text editor. The
[digit rebuild](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-number-input-digit-grid.md#digit-controls-and-value-binding)
already selects ones and retains the generated ContentLabel child at
D+0x340 when its constructor's Content cast succeeds.

The lower arm consumes only when D is nonnull and the routed source
matches D+0x340 or the lower embedded TextBox
(`0x00691733..0x00691756`). Otherwise it tries the upper arm. That arm
requires upper D nonnull and source equal to upper D+0x340, or to the
**lower** embedded TextBox (`0x0069178B..0x006917AC`). The lower lookup
in the upper fallback is the actual load at `0x006917A2`, not a symmetric
upper-editor rule. A matched arm calls `0x0069C0A0` on the matched box,
requests that box's input virtual `+0x38`, then returns without calling
the native root-close arm (`0x00691758..0x0069177A`,
`0x006917AE..0x006917D6`).

`0x0069C0A0` requests typed Value from C+0x3B80 through `0x00967090`
with arguments 0,1 (`0x0069C0A0..0x0069C0AB`). The NumberInputBox
constructor registers `0x0069C230` for descriptor `0x01359468` at
`0x0069DBCF..0x0069DBF1`. Initializer `0x00F227E0..0x00F227F6`
names it IsKeyboardFocusWithinChanged, event id 0x2B, strategy 1.
That handler copies current effective Value C+0x35C into C+0x3B80 only
when the current IsKeyboardFocusWithin bit C+0x15D bit 5 is set
(`0x0069C230..0x0069C23F`). The restore request is not the Search
bound-cache save and does not itself call the text-editor opening path.

The [qualified short-arrow route](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-number-input-pointer-edit.md#focus-before-the-quantity-step)
can focus C before digit selection and the release step. Its MouseDown
handler selects D at C+0x3B84. Those operations do not call the separate
`0x0069C020` text-editor opener. If the later Cancel's actual routed
source is C, it matches neither numeric content nor embedded TextBox.
Both unmatched arms fall through to virtual `+0x28` at `0x006917E6`,
then the shared save and root-close request described above. If source
is one of the matched inner controls, the numeric restore arm applies.
The [Layout0 Escape bindings](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/main-menu-command-route.md#key-bindings)
request Cancel and separately MoveFocus 10. Their actual route membership,
first source, preview handling and post-command focus remain conditions.
This static branch does not make every physical Escape a root close or
an editor cancel. LLVM instructions and section-mapped reads of the
identified PE corroborated the accessors, source comparisons and calls.
No original client ran.

### First class-info Reply level range

STATIC. The installed PcSearchWidget `processAfterShow` calls
`desktopWidget:demandPlayerExpInfomation()` and calls its own update only
when the return is exactly false (`main/f1`, zero-based PCs 0-7).
The desktop method calls the self player's updateGameParameters with
`"exp"` (`desktopwidget_connector`, `main/f390` PCs 0-5). Its later
processCharacterParameterUpdated branch requires isPlayer and isMyPlayer,
then category `"exp"`, looks up current category-3 PcSearchWidget, and
calls update only when that lookup is nonnil (`main/f78` PCs 108-115,
262-263, 322-330). This is the stock immediate-or-callback publication
path, not evidence that every show already has class information.

PcSearchWidget.update writes row 0 value_current_skill in
XmlDataMaker_Data from desktopWidget:getPlayerMainSkillNumber
(`main/f3` PCs 0-7). That getter reads the self player's getStateMainSkill
and replaces nil with 0 (connector `main/f386` PCs 0-8). Update writes
value_skill and value_skill_level for selectors 1 through 44, then a -1
selector at row 44, and sends UIOperatorCommands.Reply Int 1
(`main/f3` PCs 8-40). The level getter uses getSkillLevel. For a job it
first requires hasJobStone, returning 0 when absent, and otherwise applies
convertSkillId before getSkillLevel (connector `main/f387` PCs 0-22).
Update does not publish a maker Update action before Reply.

Native Reply id 23 calls virtual `+0x6C`, cell `0x00FC8490`, body
`0x00691540`. It reads value_current_skill from maker `+0x98`, row 0,
and stores it in the current profile at `0x013430F8 +0xBC` through
`0x0086F730` (`0x00691594..0x006915DE`). It then reads value_skill and
value_skill_level from rows 0 through 42, exactly 43 rows, and writes
that profile's sparse level map through `0x0086FA70`
(`0x006915E3..0x00691687`). This is not a 44-row native loop.

At `0x006916AD..0x006916C3` it sets operator `+0xF4` to 1 and, only
when byte `0x01342BFA` is zero, calls `0x006902D0` and sets that byte
to 1. The helper requires nonzero `+0xF4`, reads the profile's current
selector through `0x0086F720`, then its corresponding level L through
`0x0086FA40`. It writes cached lower=max(L-5,1) and upper=min(L+5,50),
then requests those Values on the current lower and upper controls, in
that order (`0x006902D3..0x00690336`). It writes both caches and requests
both current control Values. The controls' own 1..50 bounds remain a
separate rule.
The first-use default helper `0x00691EE0` clears this first-Reply byte
at `0x00691F12`. It is distinct from the Button_Reset arm below.
The ordinary retained reopen does not by itself clear it.

Reply's first-range branch is not restricted to Int 1. A kind-1 record
with `Int[0] == 2` changes a local flag used by the later nondefault
command-line automatic-query arm, but does not skip the preceding profile
reads or first-range branch (`0x0069157B..0x00691589`,
`0x006916C9..0x006916D4`). The supported stock update above supplies
Reply 1 and complete attributes. Missing or malformed attributes,
nondefault command-line setup, editor focus routing and historical live
input timing remain outside this contract. LLVM instruction and PE table
reads corroborated the native branches. Authenticated original bytecode
and selected SQWT inputs corroborated the named producers. No original
client ran.

### Search Reset button and retained first-Reply byte

MEASURED. The standard form's Button_Reset declares
Command UILuaCommands.Operate, Content `@11062`, SqwtStyle BTN_basis,
MinWidth 180 and Help value 0 `@79610` (line 135). It has no explicit
CommandTarget, CommandParameter, ClickMode or local event trigger.
The [ordinary Button release path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-command-parameter-consumer.md#button-mouse-source)
and [Operate gate](#begin-search-activation-and-first-use-filters) apply
conditionally. The source must reach the current operator as its exact
retained Button_Reset, resolved at `0x0069220B..0x00692236` into `+0x74`.
The matched branch is `0x00693729..0x0069379B` in `0x00693650`.

STATIC. The branch resets selector indices 0 through 4 in order through
`0x00691DC0` (`0x0069372E..0x00693780`). That helper erases the current
selector vector and refills it through `0x00870530` from the constant
table selected by `0x0086FD50`. Every source row's `+0x11` byte is 0
in the five [first-use tables](#first-use-state-and-query). It also
restores that selector's caption reference and clears its retained
caption flag (`0x00691E24..0x00691E62`). The caller
requests each restored caption through the embedded interface at
operator `+0x20`, virtual `+0x18` (`0x00693754..0x00693768`).
Constructor `0x00693558` installs table `0x00FC83FC` for that interface,
and cell `0x00FC8414` selects `0x00690760`.

The caption reference producer `0x00690530` selects these values. Setup
retains the named TextBlock_ButtonText and TextBlock_ThreePoint children
under the corresponding Label (`0x0069229B..0x0069254B`).

| Selector | Label owner | Restored caption |
| --- | --- | --- |
| 0 | Label_Status | `@11001` |
| 1 | Label_Class | `@11006` |
| 2 | Label_Region | `@11016` |
| 3 | Label_GrandCompany | `@11011` |
| 4 | Label_Location | `@11021` |

`0x00690760` requests each caption's Text through `0x0068E840` and
requests Visibility 0, Collapsed, on its ThreePoint child when passed
the cleared byte (`0x00690778..0x006908DE`). The loop preserves the
operator's preceding current-selector index around each update.

After all five selectors, the branch directly calls `0x006902D0` at
`0x00693786`, then writes cached checkbox byte `0x01342BF8` to 0 and
requests IsChecked false on retained `ToggleButton_JobCheck` at `+0x78`
(`0x0069378B..0x0069379B`). After an admitted class-info Reply has set
`+0xF4`, the direct call immediately writes both numeric caches and
requests both current controls using the current profile's class level
and the [published range rule](#first-class-info-reply-level-range).
It does not wait for another Reply.

This Button_Reset arm does not call `0x00691EE0` or write first-Reply
byte `0x01342BFA`. If that byte is already 1, the next Reply updates the
profile but skips its first-range call. Before the first class-info
Reply, `+0xF4` is zero and the direct range helper returns without
changing the numbers. The still-zero first-Reply byte can then admit
the later Reply's range call. An ordinary Reset also does not enter the
separate Search-source arm when the two retained Buttons are distinct.
Actual pointer acceptance, callback reentry, nondefault command-line
setup and historical query results remain outside this static contract.
The identified PE's instructions, interface cells and constant tables,
and the authenticated form corroborate these facts. No original client ran.

### Search job checkbox gesture and query

MEASURED. The selected ToggleButton_JobCheck declaration and checked art
are documented [above](#search-checkbox-presentation). It names
UICommands.Operate, has no explicit CommandParameter, CommandTarget or
ClickMode, and has no local trigger or binding that saves its checked
state. The initial False and later native setup restoration are distinct.

STATIC. On the [qualified ToggleButton release path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#arrow-release-and-checked-state-binding),
Click calls primary slot 71 at `0x0097ED20` before it checks the stored
Command at `0x0097ED22`. ToggleButton cell `0x0106F3D0` selects
`0x0095D2B0`, whose call at `0x0095D2BB` reaches slot 75, cell
`0x0106F3E0`, body `0x0095D470`. Under the property guards it complements
the effective IsChecked bit at `+0x3B4`, mask 0x20, stores it at
`0x0095D4D6` and invokes the checked callback at `0x0095D4D8`.
The callback and toggle's base Click handling return before the stored
Command is routed. Thus the gesture's checked mutation precedes that
Operate dispatch. A refused property mutation is not a successful toggle.

UICommands.Operate literal `0x00FC91CC` is registered with native id 1
at `0x00F14205..0x00F14224`. The current PcSearch Operate method
`0x00693650` compares the routed source with the five selector Buttons,
Button_Reset and Button_Search. It has no ToggleButton_JobCheck `+0x78`
arm. With those retained controls distinct, an Operate from the job toggle
does not enter Reset or Search. Its checked mutation is the ToggleButton
behavior above, not a separate Lua or operator toggle callback.

The shared close-save body `0x006917F0` reads the current toggle at
operator `+0x78`, extracts its effective checked bit and writes cached
byte `0x01342BF8` (`0x006917F3..0x00691806`). Both admitted native title
Close and the unmatched Cancel fallthrough reach this save before the
root-close request. The matched numeric Cancel restore arm does not.
Later normal setup requests that cached Boolean on the new current toggle
at `0x006930E7..0x006930F6`. The ordinary click has no checked-cache arm
in `0x00693650`. Reset instead clears both the cached byte and the current
checked property, as [documented above](#search-reset-button-and-retained-first-reply-byte).
Direct Lua close, arbitrary teardown and nondefault command-line setup are
outside these persistence claims.

The Search arm reads the **current control bit**, not that cached byte,
at `0x006938B5..0x006938BF`. When set, it calls `0x004B5940` with tag 3,
width 1 and value 1 (`0x006938C1..0x006938CE`). The
[wire helper](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-requests)
emits `03 01`. This branch follows the Class-row loop and does not require
that loop to emit a Class tag. An unchecked control emits no tag 3.
Tag 7 belongs to selected Status rows, independently. These client bytes
do not establish the server's interpretation of the job-only request.
Original PE instructions, table cells and authenticated markup corroborate
the paths. Physical hit, press/release admission, route membership,
callback reentry and historical search results remain unverified. No
original client ran.

### Search Class selector child

MEASURED. The standard parent selects
Label_Class:Button_SearchSetting through its selected Label template.
The qualified short Button release uses UILuaCommands.Operate with no
explicit parameter or target. Setup retains this exact Button at operator
`+0x30` (`0x006920A5..0x006920D0`). Under the existing Operate guards,
its source match at `0x00693699` sets current selector `+0x8C` to 1,
registers the embedded callback at operator `+0x20` through `0x0086F180`,
and requests native child-name index 3 through `0x00695AD0`
(`0x00693699..0x006936B8`). The callback pointer is retained globally at
`0x0134F550`. Initializer `0x00F1CD29..0x00F1CD33` names child index 3
PcSearchSelectWidget. The request issues UIOperatorCommands.OpenChild
on the retained parent. The [shared child-open path](#main-menu-root-open-and-close)
passes that name to openChildWidget(name,self,true), preserving the current
parent and category index. This is a native request, not a new Lua Class
selection callback.

STATIC. The selected child operator constructor is `0x0086F290`, table
`0x0104D184`. It initializes TreeView at child `+0x24` from the registered
parent callback. The callback's `+0` method `0x00690510` returns the Class
vector at `0x01343088`, while `+8` method `0x00690520` supplies tree mode
0. The constructor resolves ListBox_TreeView and
XmlDataMaker_TreeView_Key (`0x0086F317..0x0086F327`, `0x0086F510`,
`0x006955B0`). The form declares maker Name XmlDataMaker_TreeView,
XPath `/XmlDataMaker_TreeView_XPath`, and binds ListBox_TreeView to it
with DataTemplate_TreeView (lines 5, 28). The ListBox declares MaxHeight
440, MinWidth 400, IsTabStop False and IsHitTestVisible False. The latter
is a [local hit flag](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-command-parameter-consumer.md#local-hit-flags-and-child-first-query),
not a rule to prune every child hit.

The Class vector is copied from the 22 records at `0x0104DFB0`, stride
0x14 by the parent's first-use or Reset path. Each group header has
level 0 and query selector -1. Each leaf has level 1 and the listed
positive selector. Catalog expand byte `+0x10` is 1 and checked byte
`+0x11` is 0 for every record. Opening a child uses the retained current
vector and does not clear its checks back to these defaults. Text formatting
`0x008724E0` produces the header reference below, or `@206/i<selector>`
for a leaf.

| Header row | Header text | Following leaf selectors in row order |
| ---: | --- | --- |
| 0 | `@11007` | 3, 2, 4, 8, 7 |
| 6 | `@11008` | 23, 22 |
| 9 | `@11009` | 39, 40, 41 |
| 13 | `@11010` | 29, 30, 31, 32, 33, 34, 35, 36 |

Tree build `0x00873560` clears the maker, writes each original row in
order through `0x008725E0`, finalizes the hierarchy through `0x00873220`
and publishes Update. The row writer supplies list_index, user_id, level,
text, expand_flag, checked_flag, and role values
control_index_toggle_expand=0 and control_index_toggle_checked=1.
It writes visibility_icon Collapsed, visibility_indent1 Visible for
level >=1, visibility_indent2 Visible for level >=2, otherwise Collapsed.
The literal indenter names come from pointer cells `0x012D4DA4` and
`0x012D4DA8`. The selected template binds those exact names to
Border_Blank_1 and Border_Blank_2 Visibility at lines 14-15.
Hierarchy finalization writes row `visibility`, sets no_child on leaves and, in mode 0, requests
Hidden for a leaf's expand control. The first leaf is original row 1,
selector 3, text `@206/i3`. The mode-0 initial build does not write
visibility_checked. The selected binding therefore reads empty text for
that absent attribute. On the admitted ordinary
[Visibility string path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-xpath-data-sources.md#conditional-visibility-write),
empty text requests Visible, not Collapsed. Constructor title publication
uses `@11028` from parent callback `0x00690650` for
TextBlock_SettingTitle.

#### Class row setter operands

STATIC. In `0x00873560`, the row writer's user_id argument comes from
original record `+0x0C`, the query selector. Its text operand separately
comes from `+0x04/+0x08` through `0x008724E0`. Thus header user_id is -1,
while row 1 has list_index 1 and user_id 3. Begin Search reads the class
selector directly from the retained record.

For the ordinary empty working string created by `0x00945CE0`, Boolean
formatter `0x00989060` emits exact `True` or `False`
(`0x00945DA0..0x00945DB7`, `0x00989196..0x009891AE`). Those are the
text values of expand_flag, checked_flag, no_child and row visibility.
Catalog defaults initially supply expand_flag True and checked_flag False.
Reopening instead copies their current retained bytes. The row writer sets
no_child False before hierarchy finalization. Finalization sets it True on
leaves and leaves headers False. For the initially expanded catalog, every
row's visibility is True (`0x00873220 -> 0x004EC390 -> 0x00945CE0`).

Visibility-valued attributes use `0x00945F40 -> 0x00914630`, which emits
`Collapsed`, `Hidden` or `Visible` for values 0, 1 or other, respectively
(`0x00914630..0x0091465F`). In the mode-0 initial hierarchy pass,
headers with children take `0x008734AE..0x008734B0` to the return at
`0x0087350C` before the visibility_expand setter. Leaves write Hidden.
Mode 0 also omits visibility_checked.
The selected at-sign binding and ordinary Visibility conversion described
above supply Visible from the absent attribute's empty text. These claims
require admitted maker rows and ordinary attribute writes.

MEASURED. The selected template's ToggleButton_TreeViewChecked binds
IsChecked OneWay to checked_flag, IntData.Value0 to list_index and
IntData.Value1 to control_index_toggle_checked. Its Command is
UICommands.Operate, with no explicit parameter. Thus the row and role
come from source properties, not a Lua selected-index argument. After the
[Toggle checked mutation](#search-job-checkbox-gesture-and-query), the
native child Operate method `0x0086F450` forwards to TreeView
`0x00873760`. That method accepts the exact source names
ToggleButton_TreeViewExpand and ToggleButton_TreeViewChecked, reads the
two IntData values, and handles checked role 1. Mode 0 negates the maker's
checked_flag, applies it to descendants, recomputes the parent check and
publishes Update (`0x00873A6A..0x00873CFB`). For the single initial
row-1 leaf gesture, checked_flag becomes true while the other leaves
remain false. The OneWay binding is not a reverse write from the earlier
Toggle mutation. Keyboard traversal, expansion gestures and other tree
modes remain outside this representative leaf route.

#### Selected tree toggle bindings and frames

MEASURED. In the authenticated selected TreeView template, line 16 declares
ToggleButton_TreeViewExpand with Command UICommands.Operate, style
TOG_basis_tree, Width and Height 16, and no explicit CommandParameter or
CommandTarget. Every binding in this table is XPath with Mode OneWay.

| Expand property | Row attribute |
| --- | --- |
| IsChecked | `@expand_flag` |
| Visibility | `@visibility_expand` |
| IntData.Value0 | `@list_index` |
| IntData.Value1 | `@control_index_toggle_expand` |

The adjacent ToggleButton_TreeViewChecked at line 17 selects
TOG_basis_checkBox. Its [checked and unchecked Frame parts](#search-checkbox-presentation)
are the same CHB_basis_checked and CHB_basis_unChecked parts already
recorded for the parent job toggle. The native row writer's expand and
checked role values remain 0 and 1, respectively.

In authenticated common/default.style, TOG_basis_tree lines 3472-3475
redirect CheckedButton to Button style TOG_basis_treeMinus and
UncheckedButton to TOG_basis_treePlus. Each Button style has one Frame
part (lines 1913-1936), with these selected keys.

| Frame condition | Checked expand | Unchecked expand |
| --- | --- | --- |
| SkinNormal, SkinDisabled | `TOG_basis_treeMinus_N` | `TOG_basis_treePlus_N` |
| SkinHover, SkinActive, SkinAnchored, SkinReserved | `TOG_basis_treeMinus_H` | `TOG_basis_treePlus_H` |
| SkinFocused, SkinDroppable | `NULL` | `NULL` |

The four tree skins are 1-by-1 CellSkins, each with one Stretch Cell and
a 16-by-16 source rectangle in common/default.dds (default.skin lines
1850-1861). The common style/skin identities are pinned in the
[numeric presentation input table](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/damage-plate-numeric-presentation.md#identity-and-method).
Both carriers were decrypted, re-encrypted byte-for-byte and parsed as XML.
These are the selected declarations and skin keys. Actual animation,
style resolution, hit acceptance and rendered pixels remain conditional.

STATIC. Child Cancel selects virtual `+0x24`, cell `0x0104D1A8`, body
`0x0086F190`, which only jumps to virtual `+0x28`. The declared
Button_Close sends UILuaCommands.WidgetClose and reaches that same
`0x00695F40` close request. Both call the shared pre-close save, whose
child virtual `+0x1C`, cell `0x0104D1A0`, is `0x0086F1A0`.
It calls `0x008736A0 -> 0x00872AE0` to copy maker expand_flag and
checked_flag into the current Class vector's record bytes `+0x10/+0x11`.
It derives the caption, calls the parent's caption updater and clears
`0x0134F550` (`0x0086F1F4..0x0086F253`). Neither Cancel nor Close rolls
back the maker checks or returns a Lua selection result. With only row 1
checked, the parent caption becomes `@206/i3`, without a ThreePoint
marker. The later guarded root Search loop emits Class tag 1, width 1,
value 3 (`0x00693881..0x006938A2`), producing `01 03` independently
of the job checkbox. Header selector -1 is skipped.

The bounded path requires the current parent's callback to remain registered
and unchanged while its child builds and closes. Concurrent selectors,
stale owners, arbitrary deletion, physical focus, hit geometry and server
filter interpretation are not established here. The public wire contract
owns request framing. Original LPB/form identities are listed below.
The selected template carrier has 2321 bytes, SHA-256
`25d58df2898d0a3e52f07dde503191da7b6ca5555fb5a1d6be0f4729bedcdde3`.
Its decoded 2313-byte XML has SHA-256
`916e68dd06c580f3ae4988752416ac834da1a632c29ba23f463b40cf40ef5cec`.
It was decrypted, re-encrypted byte-for-byte and parsed as XML. Native
instructions, vtable cells and original Class records corroborated the
consumer joins. No original client ran.

### Search result maker identity

MEASURED. The standard `widget/PcSearchWidget.form` declares a
SqwtXmlDataMaker with Name `XmlDataMaker_PcSearchList`, resource key
`XmlDataMaker_PcSearchList_Key` and XPath `/XmlDataMaker_PcSearchList_XPath`
(decoded line 5). ListBox_SearchResult selects that key and XPath as its
OneWay ItemsSource (line 152). This is distinct from the PlayerInformation
maker and XmlDataMaker_Data declared on lines 6-7.

STATIC. Setup `0x00691F30` resolves the result resource key literal at
`0x00FC7A6C` through `0x006950A0`, then retains it at operator `+0x90`
(`0x00691F7C..0x00691FA8`). Query construction passes that same maker to
clear `0x00942FA0` and Update `0x00943980` at
`0x00693A8F..0x00693AAA`. Result projection loads `+0x90` at
`0x00693D58` and calls Update at `0x00693D5E`. Thus these published clear
and Update requests name `XmlDataMaker_PcSearchList`, not the result
ListBox or either other maker. The selected form identity is pinned below.

### Pending Search and empty completion

STATIC. This path continues the admitted `Button_Search` send above and
the [matching-token stream](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-results-and-completion).
It concerns normal `mode_widget`, zero cached rows and successful terminal
state 3. Populated rows, comment construction, other command-line modes,
error presentation and observed historical traffic are outside this case.
The identified executable and method are recorded above.

#### Pending requests

On emitter success, `0x008746E0` first clears contractor readiness
`+0x14` and its projected-row cursor `+0x18`, then requests
`0x00691AE0(0)` on the registered PcSearch operator
(`0x00874710..0x00874731`). The caller sets operator `+0xF5` to 1 only
after that call returns. The readiness predicate in the Search arm refuses
a further query while the byte is zero.

`0x00691AE0(0)` requests the following changes in order. The retained
operator `+0x68/+0x6C` controls are NoContents and MaximumOver, as pinned
in setup above. The named button lookups resolve `Button_Search`.

| Control and property | Requested value | Instruction range |
| --- | --- | --- |
| `TextBlock_NoContents.Visibility` | 1, Hidden | `0x00691CEE..0x00691CFF` |
| `Button_Search.SqwtStyle` | `BTN_basis_disabled` | `0x00691D0A..0x00691D37` |
| `TextBlock_MaximumOver.Text` | `@11066` | `0x00691D50..0x00691D78` |
| `TextBlock_MaximumOver.SqwtStyle` | `TBL_null` | `0x00691D7D..0x00691D88` |
| `TextBlock_MaximumOver.Visibility` | 2, Visible | `0x00691D8D..0x00691D9E` |

Text uses `0x009557D0`, Visibility uses `0x0093C2A0`, and the named style
helper is `0x004EC650`. Visibility 1 is
[Hidden](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-anime-property.md#visibility-and-anime).
This body makes no HitCount Text or Visibility request and no IsEnabled
write. Its disabled Button style is separate from the native readiness
gate. It requests no new widget or modal setting. The enclosing Search
root's modal initialization is already documented, and this presentation
path establishes no additional modal, overlay or input capture.

#### Zero rows and terminal completion

PcSearchContractor table cell `0x0104ED84` selects ordinary callback
`0x00874610`. It obtains the current row count through `0x004C3980(4)`,
truncates it to u16 and passes the previous cursor, new count and contractor
byte `+0x0C` to `0x00693B50` when the registry lookup for operator kind 2
succeeds (`0x0087461A..0x00874645`). Projection requires that final byte
be zero and operator `+0xF5` be nonzero (`0x00693B8B..0x00693BAD`).
Ordinary `0x008746E0` success clears contractor `+0x0C` at `0x00874736`.
These predicates are not proof of a particular widget generation.

For old cursor 0, count 0 and the cleared cache from query construction,
the row and comment loops execute no iterations. The normal continuation
publishes result-maker Update at `0x00693D58..0x00693D5E`, then writes
`TextBlock_HitCount.Text` as `@228/i0/i200` and its SqwtStyle as `TBL_null`
(`0x00693D92..0x00693E30`). The format is `@%d/i%d/i%d` at `0x00FC83EC`.
There is no HitCount Visibility request in this body. An intermediate
zero-row callback can already publish this count. It does not itself
finish the query.

After projection, `0x00874610` updates contractor cursor `+0x18`, then
tests terminal predicates through `0x004BBE60` with selectors 1, 2 and 3
(`0x0087464A..0x00874672`). `0x004B65E0` maps them to request states 3,
4 and 5 and also requires nonnull request `+0x24`. Nonterminal state 2
returns without restoring readiness. The successful empty case takes
state 3. It writes readiness 1 at `0x00874674`, then requests
`0x00691AE0(1)` when operator kind 2 is still registered
(`0x00874678..0x00874698`). Readiness is restored before these UI requests.

With operator `+0xF5` still set and its cached row count zero,
`0x00691AE0(1)` requests the following ordered continuation:

| Control and property | Requested value | Instruction range |
| --- | --- | --- |
| `TextBlock_NoContents.Text` | `@11058` | `0x00691B52..0x00691B7A` |
| `TextBlock_NoContents.Visibility` | 2, Visible | `0x00691B7F..0x00691B90` |
| `TextBlock_MaximumOver.Visibility` | 0, Collapsed | `0x00691B95..0x00691BA6` |
| `Button_Search.SqwtStyle` | `BTN_basis` | `0x00691BB1..0x00691BDE` |

It then clears operator `+0xF5` at `0x00691BFB`. Normal `mode_widget`
retains `+0x24 == 0`, so the following non-widget enable helper is skipped.
The pending MaximumOver text may remain stored while that control is
Collapsed. Completion does not require clearing its Text or setting
HitCount Visibility.

#### Completion and stale-input boundaries

Clientbound `0x01E0` requires active opcode `0x01DD`, a request state other
than 3, 4 or 5, a retained nonzero token and exact incoming token equality
(`0x004C78A3..0x004C78E4`). Its error mask 4 takes state 4 before copying.
Its completion mask 2 requests state 3 after parsing. The linked wire
contract owns the initial `0x01DF` token latch and zero-row premise.
Wrong tokens, wrong active opcode and already terminated records therefore
do not establish this successful empty continuation.

State notification `0x004B5DF0` invokes a callback only from prior states
1 or 2 with a nonnull callback pointer and an admitted reentry counter
(`0x004B5DF9..0x004B5E46`). State 4 selects callback slot 2, whose cell
`0x0104ED88` is `0x008746B0`. That callback restores readiness and requests
the ready helper but does not invoke `0x00693B50` to project HitCount.
Readiness alone is therefore not proof of successful empty completion.
State 5 and timeout behavior remain outside this case. The shared ready
tail below also qualifies the error callback's presentation requests.

Projection's final-byte and pending-flag guards, request token/state checks
and current registry lookup are distinct. They do not establish a lifecycle
generation check when the root has been replaced or reopened. A bounded
empty-result observation needs the same admitted request and current root,
matching-token successful completion, count projection and ready UI requests.
Callback reentry, property refusal, overlapping roots and late callbacks
against replacements remain unobserved. No original client ran.

Ghidra CLI supplied focused leads. LLVM disassembly of `0x00691AE0`,
`0x00693B50`, `0x00874610`, `0x008746B0`, `0x004B5DF0`, `0x004B65E0`
and the `0x01E0` ingress corroborated branches, call arguments and order.
Section-mapped PE reads checked the callback cells and named style/format
literals. The authenticated standard form supplies the control identities.

#### Shared ready tail for current Search

STATIC. In `0x00691AE0(1)`, restoring `Button_Search.SqwtStyle` to
`BTN_basis` at `0x00691BAB..0x00691BDE` and clearing operator `+0xF5`
at `0x00691BFB` are common tail requests. They do not require a successful
empty result. Entry with `+0xF5 == 0` jumps directly to that tail at
`0x00691B1A..0x00691B21`, without NoContents or MaximumOver requests.

With `+0xF5 != 0`, cached count zero selects NoContents Text `@11058`
and Visible before collapsing MaximumOver. Count 1 through 199 instead
takes `0x00691C44 -> 0x00691B95`, requests MaximumOver Collapsed and
reaches the same Button tail. It requests neither NoContents Text nor
Visibility, leaving its pending Hidden state intact. The exact-200 arm
also rejoins the Button tail after its separate warning requests. These
are style and notice requests, not IsEnabled writes.

Error callback slot 2 (`0x008746B0`) writes contractor readiness 1 before
looking up operator kind 2. A nonnull lookup tail-calls `0x00691AE0(1)`
(`0x008746B0..0x008746D0`). Thus this current error callback restores
Search art through the common tail even though it does not project
HitCount through `0x00693B50`. If the pending flag remains set and the
cache count is zero, the ready helper also requests the zero-count
NoContents notice on this error path. That notice is not proof of a
successful empty stream. A null operator lookup skips the UI request.

These branches describe an admitted callback and current operator.
Wrong-token packets suppressed at ingress produce no such callback.
The ready helper contains no request-token or widget-generation check.
A retained callback reaching a replacement operator, or a transport error
that never invokes this callback, remains outside the proven route.
LLVM disassembly corroborated these common and conditional branches.

#### Exact-200 ready warning

STATIC. With ready argument 1 and operator `+0xF5` nonzero,
`0x00691AE0` compares the cached profile count with exactly 200 at
`0x00691C3F`. Equality requests these writes in order:

| Control and property | Requested value | Callsite |
| --- | --- | --- |
| `TextBlock_MaximumOver.Text` | `@11059` | `0x00691C72` |
| `TextBlock_MaximumOver.SqwtStyle` | `TBL_parameterDanger` | `0x00691C82` |
| `TextBlock_MaximumOver.Visibility` | 2, Visible | `0x00691C98` |
| `TextBlock_HitCount.SqwtStyle` | `TBL_parameterDanger` | `0x00691CD0` |

The arm then jumps to the shared Button_Search `BTN_basis` restore and
pending-flag clear (`0x00691CE9 -> 0x00691BAB`). It makes no NoContents
write and does not replace HitCount Text. With a positive count unequal
to 200, including greater than 200, `0x00691C44` instead branches to
`0x00691B95`, which requests MaximumOver Collapsed before the same tail.
With `+0xF5 == 0`, all these notice writes are skipped. This equality
branch does not establish that historical streams exceeded 200 or admit
malformed result records. LLVM disassembly and the two literal reads at
`0x00FC7E3C/0x00FC7E50` corroborated the common danger style.

### Ordinary Search row publication

STATIC. This path uses the result maker above and the matching-token ordinary
callback already documented. In `0x00693B50`, each newly admitted row index
first obtains the cached wire row through `0x004C39B0(6,index)`, decodes it
with `0x0086FA90`, appends its native profile to the operator cache and
calls `0x00690900(profile,maker,index)` (`0x00693BD0..0x00693C15`).
The row writer does not request a maker Update for each attribute. After
the row loop and any available comment writes, `0x00693D58..0x00693D5E`
publishes Update on `XmlDataMaker_PcSearchList`, then updates HitCount.
A one-row continuation from cursor 0 writes maker row 0 before that Update.

MEASURED. The selected `DataTemplate_PcSearchList` (template lines 33-95)
has 23 distinct row-attribute bindings. Its Button_SearchResult is Height
40. TextBlock_PlayerName binds `text_textblock_player_name` (line 58).
Four fixed IconControls bind only their opacities, with IconDatas 878, 879,
880 and 881 for invitation, party, AFK and online (lines 53-56). The
current and desired class groups, company icon and region labels use the
bindings below. This is presentation evidence, not a result-row activation
or focus contract.

The writer helpers serialize values into XML attribute text before
`0x009425B0`. `0x00944ED0` copies a Sqwt string through `0x00914C70`.
`0x00944DA0` formats its integer through `0x00988A90`, whose empty-format
branch uses `%d` at `0x01077268`. `0x00945F40` uses `0x00914630`, which
prints 0 as Collapsed, 1 as Hidden and other values as Visible.
`0x00946070` copies a C string through `0x00915670`. These are attribute
strings, not live control property writes or an Update per setter.

| Attribute or group | Producer and conversion | Native locator |
| --- | --- | --- |
| `text_textblock_player_name` | Profile name string, without a numeric or reference format | `0x0069095C..0x0069097A` |
| `visualopacity_iconcontrol_invite_party` | `1.0` for effective status 3, otherwise `0.0` | `0x00690994..0x006909E3` |
| `visualopacity_iconcontrol_party` | `1.0` for status 2, otherwise `0.0` | `0x00690A3D` |
| `visualopacity_iconcontrol_afk` | `1.0` for status 4, otherwise `0.0` | `0x00690A97` |
| `visualopacity_iconcontrol_online` | `1.0` for status 1, otherwise `0.0` | `0x00690AF1` |
| `visibility_grid_desired_class` | Visible only for status 3 and nonzero desired class, otherwise Hidden | `0x00690B06..0x00690B8D` |
| `visibility_grid_current_class` | Hidden for class 0, otherwise Visible | `0x00690D31..0x00690DA2` |
| `icondatas_iconcontrol_desired_class`, `icondatas_iconcontrol_current_class` | Class icon lookup `0x00870210`, serialized as decimal integer | `0x00690BE5`, `0x00690DF9` |
| `text_textblock_desired_class`, `text_textblock_current_class` | Corresponding class's level from `0x0086FA40`, restricted to its low byte, then decimal integer | `0x00690C3A`, `0x00690E0E..0x00690E4E` |
| `visibility_iconcontrol_grand_company` | Hidden for company 0, otherwise Visible | `0x00691001..0x006910C0` |
| `icondatas_iconcontrol_grand_company` | Company icon lookup `0x00870510`, serialized as decimal integer | `0x0069104C` |
| `text_textblock_location` | Positive mapped location uses `@11023/i<key>`, otherwise the initialized empty string | `0x00690F5D..0x00690FEA` |

The effective status getter `0x0086F6E0` returns 2 when profile byte
`+0xDC` is set, otherwise profile dword `+0xA8`. The wire decoder's
status-2 special case and sparse class/level inputs are owned by the
[wire contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-results-and-completion).
The opacity objects are initialized from literal strings `1.0`, `0.2`
and `0.0` at `0x00F13A00..0x00F13A70`. Status icons use 1.0 or 0.0.
Region labels use 1.0 or 0.2.

For either visible class group, the writer maps that class through
`0x0086F600` to a possible job and tests the job's level. A positive level
writes `icondatas_iconcontrol_jobchange_1` or `_2` and Visible. Otherwise
it writes `visibility_iconcontrol_jobchange_1` or `_2` as Collapsed
(`0x00690D1A`, `0x00690F31`). The suffix 1
belongs to the desired group and 2 to the current group. A Hidden class
group does not establish writes to its children's icon or level attributes.

The four `visualopacity_textblock_region1` through `region4` attributes
sample `0x0086F750` with bit indices 0, 1, 3 and 2, respectively
(`0x006910D5..0x00691232`). The getter tests profile byte `+0xD0`.
The decoder combines primary Region and additional Region flags, as pinned
in the wire contract. The displayed suffix is not always bit index plus 1.

#### Bounded lookup examples and receipt

The seeded class-icon map contains class 3 -> icon 203 and class 16 ->
icon 939 (`0x00870227..0x0087023D`, `0x00870456..0x00870463`). The
class-to-job switch maps 3 -> 16 in `0x0086F600`. Native catalog setup
`0x008705A0` also seeds company 1 -> 51, 2 -> 52 and 3 -> 54
(`0x00870604..0x00870656`). This does not identify every supported class,
job or company by localized name.

Location setup inserts 42 records from `0x0104DA88`, stride `0x1C`,
into map `0x0134FF80` (`0x008705D8..0x008705F8`). Each key is followed
by a negative-terminated list of location ids. Lookup `0x0086FF30` returns
the key for a matching nonnegative entry or 0 when none matches. No list
contains location 0. Location 133 occurs only under key 101. The empty
fallback object at `0x01343758` is initialized from an empty literal at
`0x00FC7926` (`0x00F13B40..0x00F13B50`). General location mappings and
localized text output are outside these examples.

AUTHORED fixture. A single accepted row can use status 1, current class 3
with an admitted sparse level, no job-16 membership, company 0, primary
Region 0 with no additional flags, and location 133. The traced conversion
then requests the supplied name, online opacity 1.0 with the other status
opacities 0.0, a Hidden desired-class group, current icon 203 with its
numeric level, Collapsed jobchange-2, Hidden company icon, location token
`@11023/i101` and Region opacities `1.0,0.2,0.2,0.2`. These are derived
outputs for declared test inputs, not an observed historical player row.

The comment attribute `text_textblock_comment` is written separately by
`0x00691270`. `0x00693B50` stops its comment loop when a cached comment
pointer is null (`0x00693C51..0x00693C66`). The row's first publication
therefore need not include that attribute. Nonempty comment transformation,
a missing binding's effective Text, result-row selection and populated
server behavior remain unverified here.

A successful one-row completion formats HitCount as `@228/i1/i200`.
The ready helper's count-between-1-and-199 branch collapses MaximumOver
and restores Button_Search without changing the pending Hidden
NoContents (`0x00691C16..0x00691C44` -> `0x00691B95`). It is separate
from one row's first publication and has the existing request, callback,
property and current-root gates. Ghidra supplied leads. LLVM disassembly
and PE reads corroborated the branches, literal operands, serializers,
lookup examples and Update ordering. Namespace-aware XML checks compared
the producer names with all 23 selected template binding attributes. No
original client ran.

### Search row lookup seeds and empty comment

STATIC. In the pinned location table, selector 155 occurs only in record
index 13 at `0x0104DBF4`, whose key is 201. The setup and lookup above
therefore produce `text_textblock_location` as `@11023/i201`. This is a
numeric selector-to-key finding. A server's choice to use 155 for a
particular zone is interoperability input, not a retail zone-name claim.

The guarded class-icon seed in `0x00870210` writes the following exact
selector/icon pairs to map `0x0134FF8C`. LLVM disassembly checked each key
operand and following icon store in `0x00870227..0x008704EF`. The icons
are serialized as decimal strings by the already documented row writer.
The table assigns no localized class or job names and establishes no
unlisted selector's output.

| Selector | IconDatas | Selector | IconDatas |
| ---: | ---: | ---: | ---: |
| 2 | 206 | 3 | 203 |
| 4 | 204 | 7 | 207 |
| 8 | 205 | 10 | 208 |
| 15 | 940 | 16 | 939 |
| 17 | 941 | 18 | 943 |
| 19 | 942 | 22 | 233 |
| 23 | 234 | 26 | 945 |
| 27 | 944 | 29 | 212 |
| 30 | 209 | 31 | 216 |
| 32 | 213 | 33 | 211 |
| 34 | 210 | 35 | 215 |
| 36 | 214 | 39 | 217 |
| 40 | 218 | 41 | 219 |

A valid `0x01E0` comment entry with length 1 contains only its terminal
NUL. The [stream contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#player-search-results-and-completion)
requires a matching nonzero token, an admitted row index and the framing
bounds. Native `0x004C79FC..0x004C7A15` reads the big-endian length and
checks the terminal NUL. `0x004C7A21..0x004C7A2F` installs a nonnull
pointer to that NUL at cached row `+0x5C` and advances by 4 for this entry.
An explicitly empty string is therefore distinct from an absent entry.

With that pointer admitted by the comment loop, `0x00691270` copies the
empty profile comment, takes its optional text-filter path when enabled,
and searches the separator from position 0. The zero-length search
returns 0 (`0x004465BD..0x004465CC`), then substring length 0 constructs
an empty Sqwt string (`0x00447A87..0x00447ABB`). The store at
`0x00691383` writes `text_textblock_comment` as the explicit empty string
before the shared maker Update. Attribute store `0x009425B0` creates
a missing XmlAttr or uses the existing one. Its value slot at
`0x0106C8D8` selects `0x00942500`, which copies the supplied string
without an empty-value removal branch. The optional filter preserves empty
input. Its zero-character worker skips the edit loop at
`0x0045813B..0x0045813F`, and the separate type-3 check reads a temporary
copy (`0x00458100..0x0045811C`). The narrow-copy helper `0x00457920`
retains the terminal NUL for that empty output.

When the cached pointer is null, `0x00693C64..0x00693C66` instead exits
the comment loop without calling the writer. It does not synthesize an
empty comment attribute. In the selected template, TextBlock_Comment's
Text is the OneWay `@text_textblock_comment` XPath binding (line 90).
It declares no literal fallback Text or binding fallback. The effective
Text after an absent attribute remains unproved. A retained prior value
must not be described as an explicit empty-string publication.

PE identity, selected SQWT hashes and projection gates are pinned above.
The selector lists and template bindings were checked with direct PE reads
and authenticated XML. Ghidra supplied leads, and LLVM disassembly checked
the entry framing, empty-string branches and final attribute store. These
static joins establish neither observed retail traffic nor live pixels.

### Search class and job level lookup

STATIC. The row writer's class-to-job helper `0x0086F600` has exactly
these positive mappings. Its byte selector table at `0x0086F678` and
jump table at `0x0086F658` select the return constants at
`0x0086F61D..0x0086F64D`.

| Class selector | Derived job selector |
| ---: | ---: |
| 2 | 15 |
| 3 | 16 |
| 4 | 17 |
| 7 | 18 |
| 8 | 19 |
| 22 | 26 |
| 23 | 27 |

Every other input retains `0xFFFFFFFF`, interpreted as signed -1
(`0x0086F604..0x0086F616`, `0x0086F652`). In particular, a job selector
is not mapped to itself. This table is separate from the icon table.

Decoder `0x0086FA90` materializes level-map keys 1 through 43 at profile
`+0xC0` (`0x0086FBBD..0x0086FBC2`, `0x0086FC3F..0x0086FC5A`).
The classification table at `0x0086FD29 + selector`, reached only for
selectors 15 through 27, selects the membership branch for
15, 16, 17, 18, 19, 26 and 27. The other keys use ordinary level pairs.
This includes keys for which the published icon seed has no entry.

For an ordinary key, the decoder searches the 20 fixed two-byte pairs at
wire row `+0x2C`. Equality reads the following unsigned level byte
(`0x0086FC20..0x0086FC26`, `0x0086FC8C..0x0086FC97`). A greater key
ends that lookup with 0. A smaller key advances to the next pair, up to
40 bytes (`0x0086FC28..0x0086FC32`). There is no zero-key terminator.
Zero keys are skipped, and a first matching level 0 is stored as 0.
A later duplicate does not replace the first match. The decoder does not
sort or generally discard unrecognized keys. A higher key before a later
matching pair can hide that match. A wire key above 43 is never itself
queried, but it can still stop a lower-key search.

For a membership key, the decoder instead searches the eight bytes at
row `+0x54`, with the same equality/greater/advance ordering
(`0x0086FBDE..0x0086FBF9`). Equality writes 1 and no match writes 0
(`0x0086FBFB..0x0086FC17`). Zero entries are skipped rather than ending
the list. Duplicates do not accumulate a value. A job-key level pair in
`+0x2C` is not read for this branch. The membership-derived 1 is not an
ordinary numeric job level.

Getter `0x0086FA40` returns 0 immediately for a negative selector
(`0x0086FA40..0x0086FA49`). For the materialized nonnegative keys it
returns the map value at profile `+0xC0` (`0x0086FA4C..0x0086FA5C`).
The writer's derived-job test therefore requires a mapped job selector
and positive membership-derived value before showing its secondary job
icon (`0x00690C4A..0x00690D1A`, `0x00690E63..0x00690F31`). A positive
base-class level alone is insufficient. This does not infer an active job
from a class/icon id or replace the ordinary class level with 1.

AUTHORED distinguishing inputs. For current class 3, an ordinary pair
`(3,7)` with no job-16 membership supplies level 7 but no secondary job
icon. Adding job selector 16 to the membership bytes supplies value 1 for
that job and admits its icon. An ordinary `(16,99)` pair alone cannot do
so. Ordinary `(0,0),(3,0),(3,7)` pairs yield level 0 for key 3 because
zero is not a terminator and the first match wins. These are static
consequences for declared test inputs, not observed retail rows.

The pinned PE and wire-row identities are recorded above. Ghidra supplied
leads. LLVM disassembly and direct PE switch-table reads corroborated the
key domains, unsigned comparisons, fixed extents, constants and stores.
Unlisted icon outputs, lookup keys outside 1 through 43, malformed framing
and historical ordering of actual server rows remain outside this finding.
No original client ran.

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
above. The [Class selector path](#search-class-selector-child) identifies its native
open request and current-check retention on both child close commands.

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
