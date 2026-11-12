# Aetheryte list widget contract

`AetheryteListWidget` is the ask-widget implementation opened by
`TeleportCommand.eventRegion`. That command calls
`DesktopWidget.selectAetheryteRegion` only after the widget opens successfully.
This connects the widget to the retail teleport-command path; it does not
establish teleport acceptance or server destination policy.

## Widget state and rows

`initAsk` declares temporary `mode` and `regionIndex` fields as `integer8`,
initializes both to zero, and registers selection-change handling for the
region and destination list controls. It also enables cancel and close
conditions and creates the region list.

`setAskParameter` uses mode zero to display the supplied anima value, show the
region list, hide the destination list, and restore the saved region-list focus.
Other mode values build and show the destination list. The widget stores the
mode, but this code does not identify meanings for nonzero values.

The region list has five entries with row indexes 0 through 4 and stored region
IDs 101 through 105. Each `RegionName` uses text ID 5201 with the region ID as
an argument. A sixth row uses text ID 10307 and stores region ID -1. These are
the widget's numeric inputs; this contract does not assign names or world
meanings to them.

The destination builder accepts up to seven `(AetheryteID, Cost)` pairs. A nil
ID skips its row. Each populated row writes the ID and cost properties and
formats `AetheryteName` with text ID 211 and the ID as its argument. ID zero
hides the cost property. If no rows are populated, the widget adds a row with
ID zero, cost zero, and text ID 10304.

## Selection results

Selecting a region stores its zero-based row index in `regionIndex` and sets
the ask result to that index plus one. Selecting a destination resolves the
selected row's property index, reads `AetheryteID`, and sets the result to the
selected row index plus one only when that ID is nonzero. The result is an
index, not the stored region or destination ID. The zero-ID fallback row does
not set a destination result.

Closing the widget sets the base ask result to -1. `getAskResult` converts
that value to nil and otherwise returns the base result unchanged. No client
state mutation, destination eligibility, anima calculation, or server
teleport outcome follows from this widget contract.

## Destination-slot restoration

`TeleportCommand.eventRegion` and `TeleportCommand.eventAetheryte` are separate
event methods. The former opens the ask widget and calls
`DesktopWidget.selectAetheryteRegion`, which selects mode zero and returns the
region row result. The latter accepts a region selector and builds the
destination inputs. The script does not directly call the destination method
from the region method.

`DesktopWidget.selectAetheryteList` selects mode one, forwards the supplied
ID/cost operands and returns the ask result unchanged. Both wrappers request
two results from `selectEventModeWidgetYield` and return its second result.
On success, that helper returns `true` followed by the widget's `getAskResult`.

The destination method restores original slot identity. For region selectors
1-5, it reads six supplied costs. Their fixed-ID domains contain 6, 5, 6, 6
and 2 slots respectively. The mapping examples keep unused tail costs zero;
they do not establish arbitrary nonzero costs with absent fixed IDs as valid
server input. For selector 6, it reads three costs followed by three
destination IDs. Each branch omits a slot whose supplied cost equals
numeric zero. For every retained slot, it appends the destination ID and cost
to compacted arrays and records the original one-based slot at the compacted
one-based ordinal. It passes six ID/cost pairs to the widget, receives the
visible ordinal, closes the widget, and returns the recorded original slot.
The widget's seven-pair capacity is larger than this caller's argument list.

For example, the following synthetic costs illustrate leading and interior
omissions. `C` means a nonzero supplied cost; all retained IDs are nonnil.

| Supplied costs | Original slot | Visible row | Widget/wrapper result | Command return |
| --- | --- | --- | --- | --- |
| `[C,C,C,C,C,C]` | 1 | 0 | 1 | 1 |
| `[0,C,C,C,C,C]` | 2 | 0 | 1 | 2 |
| `[C,0,C,C,C,C]` | 3 | 1 | 2 | 3 |
| `[0,C,0,C,0,C]` | 2 | 0 | 1 | 2 |
| Same | 4 | 1 | 2 | 4 |
| Same | 6 | 2 | 3 | 6 |

The result at the widget and wrapper is a one-based visible ordinal. The
destination method's result is the original cost-slot number, not an
`AetheryteID`, a region ID, or an established wire selection field.

The two filters have different conditions. The command omits numeric-zero
supplied costs; the widget omits nil IDs. The original-slot map remains aligned
when each cost-retained entry has a nonnil ID. A nonzero-cost entry with nil ID
can enter the command's map and then disappear in the widget, and neither
wrapper repairs that additional compaction. The selected script does not
establish that such a tuple is a valid server input. A nil cost is not numeric
zero, so nil must not be substituted for the command's exclusion value by
analogy. Later code can also set a retained display cost to zero after the
compaction, so a displayed zero does not imply omission.

If all IDs are omitted, the widget supplies its zero-ID fallback row, which
does not set a destination result. Closing produces nil, and the destination
method's map lookup also returns nil. This establishes client result handling;
it does not identify how attunement determines supplied arguments or how the
server interprets the returned slot.

### Original-bytecode evidence

The wrapper source is pinned at `manifests/scripts.json:15399` for
`lua/scripts/widget/desktopwidget_connector.lua`. Its LPB and decoded payload
are pinned at `manifests/retail_lua_coverage.json:25444`, with payload SHA-256
`685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`.
The original `selectAetheryteRegion` prototype `root/proto452`, PCs 4-5
(decoded offsets 168439 and 168443), selects mode zero and returns the second
helper result. `selectAetheryteList`, `root/proto453`, PCs 4-5 (168577 and
168581), selects mode one and returns the second helper result.

In the previously pinned teleport payload, `eventAetheryte` is `root/proto3`.
Its zero-cost tests are PCs 76, 126, 171, 221, 271 and 301. The corresponding
original-slot map writes are PCs 114, 159, 209, 259, 289 and 327. PC 388
(decoded offset 3017) calls the destination wrapper with six pairs. PC 393
(3037) indexes the map with the returned ordinal, and PC 394 (3041) returns
that original slot. Canonical source locators are
`lua/scripts/command/system/teleportcommand.lua:558` and `:577`.

These observations use authenticated original LPBs and separately
manifest-matched canonical source. Synthetic execution of the selected
instructions checks leading/interior omissions, all supported zero-cost masks,
nil-ID compaction, zero-ID suppression and cancel handling. It does not claim
retail-runtime or server validation.

The producing readers were `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`, using Python 3.12.0.
Prototype indices and PCs are zero-based. Decoded offsets above are decimal
byte offsets in the authenticated Lua 5.1 payload.

## Teleport confirmation result

`TeleportCommand.eventConfirm` waits one second, then obtains a confirmation
result through `worldMaster.ask` or `worldMaster.askMultipleTextMacro`, using
message IDs 34117, 34138, or 34120 according to its inputs. For an accepted
result, it calls `isRiding` on StaticActor 320013 with the supplied actor. If
true, it prompts through `worldMaster.ask` with the ID returned by that static
actor's `getRidingErrorTextId`, passing 26010 as fallback, then replaces the
local result with that answer. If the countdown input is true and the result
remains accepted, it opens `Ask/WaitingCountdownWidget` with
`(1, 15, worldMaster, 34137)` when `A2_2` is true, or
`(1, 15, worldMaster, 34136)` otherwise. A false widget-open result or widget
result 2 changes the local result to 2. The method returns that result and an
optional boolean. It contains no zone-transition call; this method alone does
not establish how a caller uses the return values or what the server does.

### Waiting countdown widget

In original `TeleportCommand.eventConfirm` root/proto1, PCs 71-74
require exact Boolean true in A3 and numeric result 1. PCs 76-88 use
A2 to select the text row and open `Ask/WaitingCountdownWidget`.
The first argument after the widget name is the requested result count,
one. The child receives `(15, worldMaster, row)`. PCs 89-96 return 2
when the helper status is exact false or its widget result is numeric 2.
Otherwise they retain the accepted result and the separately computed
optional boolean.

`WaitingCountdownWidget.initAsk` proto0 PCs 0-7 register three priority-5
conditions through `WidgetBaseClass` common proto56, proto58 and proto54:
`Button_Cancel` for `UILuaCommands.Operate`, `_widget` for
`UILuaCommands.Cancel`, and `_widget` for
`UILuaCommand.CountDownCompleted`. The completion name has singular
`Command`. PCs 8-13 set `TextBlock_Text` from the supplied owner and
row. PCs 14-21 set `ProgressBar_CountDown.Maximum`, then its `Value`,
both to seconds times 60. For this caller both writes supply 900.
The installed English WorldMaster rows 34136 and 34137 have plain
logical field 1 text. Sheet `0x03A20027` references data
`0x03A200BC`, enable `0x03A200BD` and offsets `0x03A200BE`.
The row byte ranges in the data member are `[119144,119193)` and
`[119193,119249)`.

The standard form merges `common/WINBasis.tpl` and the widget template.
It declares `TextBlock_Text` at line 20, the outer
`ProgressBar_CountDown` with `ControlTemplate_ProgressBar` at line 21
and `Button_Cancel` with `UILuaCommands.Operate` at line 23.
The template declares `ProgressBar_Anime` with `Maximum` bound to
the templated parent. Its `ValueChanged` EventTrigger selects the
templated parent's name as source (line 5). Its single BeginStoryboard
has a DoubleAnimation from the templated parent's `Value` to 0,
with `Velocity=60` and target `ProgressBar_Anime.Value` (lines 6-8).
The Storyboard's `CompletedCommand` is
`UILuaCommand.CountDownCompleted`. The event source and the animated
bar are distinct controls. The form declares `IsHitTestVisible=False`
on the Grid at line 13. The cancel command routes below do not establish
pointer admission through that Grid.

An admitted changed ProgressBar value stores the bounded snapshot before
raising the routed event, at `0x00966E4B` and `0x00966EA1`. See
[xivl-decomp:docs/resource/sqwt-range-value-changed.md](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-range-value-changed.md).
For this trigger and its resolved bindings, the
[Velocity setup](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-double-animation-velocity.md)
computes a 15000 ms span from 900 to 0 at 60 units per second.
DoubleAnimation calls the Duration writer at `0x009B4A36` and
the timeline reset at `0x009B4A48`. Reset `0x009AD020` reads
`+0x48/+0x4C` at `0x009AD10B..0x009AD111` and stores the
span at `+0xF8/+0xFC` at `0x009AD131..0x009AD157`.
The forward evaluator reads that span at `0x009ACA81..0x009ACA87`.
Group setup `0x009CAB40` takes the maximum child span from
`0x009AC360`, writes it as its own Duration at `0x009CABE1`,
and calls the same reset at `0x009CABF0`. With this sole child
and the template's default nonrepeating clock, the final sample
requests zero and Storyboard completion dispatches the retained command
at `0x009A64C9`. See the
[bounded forward completion path](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-double-animation-clock.md#bounded-nonrepeat-samples-and-completion).
These are static paths conditional on property, trigger and timeline
admission. Native instance attachment and successful live delivery are open.

The widget accepts `Operate` on exact `Button_Cancel` (proto1
PCs 0-8) or the Cancel callback (proto2 PCs 0-6) while
`isAskFinish()` is exactly false. Both write base ask result 2.
The Default callback requires that same unfinished guard and the
exact completion command, then writes result 1 (proto3 PCs 0-8).
`AskBaseClass.processWaitCallFunction` proto1 PCs 0-1 checks
`isAskFinish`, whose proto10 tests base result against zero.
The wait checks the result field. The timer producer is the Storyboard.

The Desktop connector's `askEventModeWidgetYield` proto541
PCs 0-5 selects category 4. `askWidgetYield` proto542 PCs 2-8
opens with nil parent and forwards the child arguments. For a nonnil
child, PCs 11-16 wait via `selectWidgetYield(child,true)`. Exact
true collects `getAskResult` at PCs 17-22. PCs 23-25 request
`closeWidgetDirect` for that same child on either normal wait
outcome. PCs 26-36 return one false on failure or true and the
requested result on success. The child callbacks set the result.
The wrapper owns the
[close request](content-director-ui-contracts.md#closewidgetdirect-behavior).
This does not establish final detach timing for this form.

The four retained `delegateCommand` messages with inner method
`eventConfirm` carry false in D3, the formal A3. D2 and D3 are at
offsets 19 and 20 in the 64-byte parameter field. The
[delegate ABI](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/script/delegate-command-producer.md#typed-values-and-bounds)
maps them to A2 and A3. The original members are pinned by the
[1.23b capture manifest](https://github.com/XIVLegacy/xivl-captures/blob/9c827fd1d84e12f7a462e6cd5234d874c0e886c9/sources/pcap-1.23b/manifest.yaml).
Replay clear main lane 0, server to client, opcode `0x0130`. After
the actor and method prefix, D3 is tag `0x04` and the typed sequence
ends at offset 32 in each case. Frame and subevent indices are zero-based.

| Capture member | Frame | Subevent | D2 / A2 | D3 / A3 |
| --- | --- | --- | --- | --- |
| `return_to_inn.pcapng` | 6 | 1 | true | false |
| `teleport_to_camp_nine_ivies.pcapng` | 42 | 2 | false | false |
| `teleport_to_camp_tranquil.pcapng` | 20 | 2 | false | false |
| `teleport_to_gridania.pcapng` | 24 | 2 | false | false |

An A3=true fixture exercises a bytecode branch beyond these observed
inputs. The result contract stops at the local confirmation callback.

The installed widget LPB is
`client/script/n1635q/9rz/n91q1w37vpwq6vnwn1635q.le.lpb`.
Its stored and decoded identities are pinned by
`manifests/retail_lua_coverage.json:26536-26550`. The original
widget prototype starts are `0x15A`, `0x2CC`, `0x361` and
`0x3DB` respectively. Inspect with the LPB reader above. Decode
the following SQWT files with their basename Blowfish key and remove
the eight-byte wrapper. The PE identity and method are in the
[clock trace](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-double-animation-clock.md#identity-and-method).

| Client-relative asset | Stored bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `client/sqwt/widget/WaitingCountdownWidget.form` | 1898, `9a8c1a236e3c3007c152f7151ef0173755818675b590a787ca4d4896473c4d71` | 1890, `e375a58a1c965b518b2f05a9cc9ebd558709a5b662cf14ec113f829a2ac29c06` |
| `client/sqwt/widget/WaitingCountdownWidget.tpl` | 1002, `5935232e3be7c9370c8ea373729b70444c72262841ae778bb33e86040ae19071` | 994, `ce9a8fb39454cb3830c67b9a1aba567ef6c5fd9da5702ba4a9c98097f9be83d6` |
| `client/sqwt/common/default.style` | 353783, `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` | 353775, `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |
| `client/sqwt/common/default.skin` | 141967, `6788f2986d9cc8aeab83fcdbcf7a9115d3576ecfabf40529cc861f41f0df5640` | 141959, `929e65e9d5f191292d9b044e3e659ba115f18f6b3d8a82894046a7c75cbcad5a` |

#### Countdown track and indicator

The standard form selects `common/default.style`. Its outer
`ProgressBar_CountDown` declares `PRB_parameter_tpMiddleH` and
`ControlTemplate_ProgressBar` on line 21. The selected template
root `ProgressBar_Anime` omits a local style and Template (line 3).
With the declared outer template installed, initialization
`0x00937190` skips that owner's default-template constructor.
The admitted template attachment transfers the style to the inner
bar, whose null Template allows the default track and indicator
constructor. See the
[native template selection and style inheritance](https://github.com/XIVLegacy/xivl-decomp/blob/7e453c250cef200b6694714647e65afe43de2cbb/docs/resource/sqwt-progress-template-style.md).
The outer owns the value-change trigger. The inner owns the default
track and indicator.

In `common/default.style` lines 5491-5494, the ProgressBar style
resolves `HorizontalBackground` to the Window style
`PRB_parameter_middle_bgH` and `HorizontalIndicator` to
`PRB_parameter_tpMiddleH`. The Window styles at lines 375 and 315 select those skins through
their Frame parts for Normal, Hover, Active, Disabled and Focused.
All listed cells in `common/default.skin` select atlas
`common/default.dds`.

| Role | Skin declaration | DrawMode |
| --- | --- | --- |
| Track | `PRB_parameter_middle_bgH` line 617, three cells, border thickness `6,1,6,1` | Stretch |
| Indicator first layer | `PRB_parameter_tpMiddle_uvAnimeH` line 2434, referencing `PRB_parameter_tpMiddle_bgH` line 643 | Tiling |
| Indicator second layer | `PRB_parameter_tpMiddle_uvAnime2H` line 2470, referencing `PRB_parameter_tpMiddle_bg2H` line 857 | Tiling |
| Indicator frame | `PRB_parameter_tpMiddle_frameH` line 632, three cells | Stretch |

The indicator's merged skin at line 2186 names those three layers
in that order. The two animation references set `IsMinimumSize=False`.
Their sequences declare horizontal Scroll parameters `30,0` and
`-20,0` respectively. The frame is part of the indicator. The
scroll parameters describe the texture sequences, while the inner
Value drives the indicator's arranged width.

The admitted float `ValueChanged` event (ID `0x30`) reaches ProgressBar
input slot 13 at `0x0107E8E0 -> 0x00966B20`. The receiver's primary
`+0x120` slot at `0x0107EAF4` calls `0x009B6330 -> 0x009B60A0`
before the template trigger pass at `0x00966B58`.
The sizing helper requires the default-template pointer at `+0x378`,
which is initialized to null at `0x009B6713` and assigned on default
template creation at `0x009B64F8`. The default-template helper
computes `(Value-Minimum)/(Maximum-Minimum)` from its owner's values.
The RangeBase constructor supplies Minimum zero at
`0x009678E8..0x00967906`. For the default horizontal branch,
the track Border arranges the indicator to the fraction of its inner
width at `0x009B627A`. For an admitted finite range 0 to 900, Value
450 requests half the available width, and Value 0 requests indicator
Visibility 0 (Collapsed) at `0x009B60E7`. These are static layout
and property requests. Exact pixels, animated texture sampling and
live retail frame timing remain unverified.

## Evidence

The widget's decoded payload is SHA-256
`C43A98FE57C2C23D67D5947F6FAB7F437D5105B67513D7EA83DFD4C4A869547B`, pinned
at `manifests/retail_lua_coverage.json:26494-26505` for
`lua/scripts/widget/ask/aetherytelistwidget.lua`. Its source entry is pinned
at `manifests/scripts.json:14871-14874`.

The caller payload is SHA-256
`9023D10F0B1D0CC8BA7ED9C5DF2BF1099F06852E5EE7B631B6DBCE1A4456DB36`, pinned
at `manifests/retail_lua_coverage.json:23555-23566` for
`lua/scripts/command/system/teleportcommand.lua`. Its source entry is pinned
at `manifests/scripts.json:7629-7632`.

The `eventConfirm` method was decompiled from that caller payload with the
repository-pinned unluac JAR at `tools/vendor/unluac/PROVENANCE.json`, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`. The
source-form entry in `manifests/scripts.json` is a separate representation,
not the byte input used for this decompilation.

## Confirmation formatting argument

The fixed formals of `TeleportCommand.eventConfirm` are
`(self,player,A2,A3,A4,A5,A6)`. A5 is read only in the row-34138
`askMultipleTextMacro` arm: it precedes A4 and literal 1 after the formatting
flags. With false A2, the method asks row 34120 in mode 2 and does not forward
A5. The method does not identify A5 as a destination, item or text-row key.

The canonical source is `lua/scripts/command/system/teleportcommand.lua:44-98`,
SHA-256 `468377e42ad3c05eae7f24d84a00fe89b66ad3cc478de36349e554fd7b326bcd`,
pinned by `manifests/scripts.json`. The original LPB member
`7vxx9w6/rlrq5x/q5y5uvsq7vxx9w6.le.lpb` is identified by the coverage
manifest's entry for that source; its SHA-256 is
`04b99f3c9672fea0bf1317ead1aebbf29683ce021417bb7f42598f45fc6e1039`.
The decoded payload identity is recorded in Evidence above. In original
`root/proto1`, A5 is moved at PC 32; the row-34138 call is PC 35
(decoded offset `0x291`) and the row-34120 call is PC 48 (`0x2C5`).
The read-only instruction reader was
`tools/build_quest_contracts.py:ChunkReader/instruction`, with zero-based PCs.
