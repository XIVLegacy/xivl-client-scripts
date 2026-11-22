# ConfigSystemWidget contract

`ConfigSystemWidget` is a bounded local configuration editor recovered from
the retail Lua chunk for `widget/configsystemwidget`. It requests toggle and
frame-rate condition operations, issues literal work-index setter requests,
forwards local changes, requests `CommonAskWidget` with literal arguments, and
has a separately invoked result handler for numeric `1` that performs a fresh
`self.reset` lookup. These requests do not establish the purpose of the child
request, native success, effective storage, persistence, server state, OS
effects, restart requirements, filenames, rendering, or widget lifetime.

## Evidence and reproduction

The source metadata revision is `65a5cefa6d7a130b4242723ae1707b5773867b74`.

| Item | Identity |
| --- | --- |
| Logical resource | `widget/configsystemwidget` |
| Original LPB | `n1635q/7vw413rlrq5xn1635q.le.lpb` |
| LPB | 3,193 bytes; SHA-256 `0fe86210802cac8162f6c44f535e3b8d508fa18700f0fc629a87e2fe3029594a` |
| Decoded Lua 5.1 payload | 3,180 bytes; SHA-256 `b4f8e796e2199efe1a48436b98b21fd2a42d262b04515800675c4b4138c3abc3` |
| Canonical LF decompile | 7,531 bytes; 340 lines; SHA-256 `3a63dc1c480de1add02628a439f7087a653b97853e67533f2ef28084e82a85c0` |
| Unluac disassembly | 15,702 bytes; SHA-256 `61c9126717e59c545d50226926b518fbf93959d3b384ce09635270deb92632fa` |
| Decoder | `tools/retail_script.py`; SHA-256 `765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391` |
| Unluac | `tools/vendor/unluac/unluac_2025_12_23.jar`; SHA-256 `98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc` |
| Static parser | `tools/build_quest_contracts.py`; SHA-256 `a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956` |
| Tool versions | Python 3.12.0; OpenJDK 21.0.12 |

Reproduce the payload and canonical source with the public repository decoder.
The retail client root and scratch directory are caller-supplied:

```text
python tools/retail_script.py --input <retail-client-script-root>/n1635q/7vw413rlrq5xn1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/configsystemwidget.luac --script-out <scratch>/configsystemwidget.lua
java -Djava.io.tmpdir=<scratch>/java-tmp -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/configsystemwidget.dis <scratch>/configsystemwidget.luac
```

The public commands reproduce decode and disassembly when a caller supplies
the original LPB. The finite original-word checker and literal fixtures are
separate local evidence and are not a public runtime simulator. They execute
the authenticated prototypes with typed stubs, original own closures, actual
pre-execution receiver and callable identities, and raw CALL widths. They do
not run the retail client or native implementations.

## Root binding

The root has 32 words at byte offset 32 and eight child prototypes. Root calls
are `PC 2 / byte 40 / 0x0100401C / raw B=2,C=1`, which requests
`require("/Widget/WidgetBaseClass")`, and `PC 6 / byte 56 /
0x0180401C / raw B=3,C=1`, which requests
`_defineClass("ConfigSystemWidget", "WidgetBaseClass")`. The root return is
`PC 31 / byte 156 / 0x0080001E`.

The following assignments are binding attempts. They do not prove that a
class table or runtime widget owner completed.

| Method | Closure source line / PC / byte | Prototype | Assignment source line / PC / byte |
| --- | --- | --- | --- |
| `init` | 11 / 8 / 64 | `root/proto0` | 136 / 9 / 68 |
| `update` | 139 / 11 / 76 | `root/proto1` | 193 / 12 / 80 |
| `reset` | 196 / 14 / 88 | `root/proto2` | 253 / 15 / 92 |
| `processUICommandOperate` | 256 / 17 / 100 | `root/proto3` | 272 / 18 / 104 |
| `processUICommandSelection` | 275 / 20 / 112 | `root/proto4` | 289 / 21 / 116 |
| `processUICommandToggleButton` | 292 / 23 / 124 | `root/proto5` | 307 / 24 / 128 |
| `initToggleButton` | 310 / 26 / 136 | `root/proto6` | 328 / 27 / 140 |
| `processAskResult` | 331 / 29 / 148 | `root/proto7` | 340 / 30 / 152 |

The root has no captured upvalues. No contained closure was present in the
eight source methods.

## Method windows and original words

The source windows below are inclusive canonical LF lines. A call locator is
`PC / byte / word / raw B,C`; `open` means a raw B or C width is zero. Every
CALL below is a CALL; no TAILCALL occurs. Each method has one RETURN with word
`0x0080001E`.

| Method | Source window; prototype | Code offset; words | CALL / TAILCALL matrix | RETURN |
| --- | --- | ---: | --- | --- |
| root | 1-10 and assignments at 136, 193, 253, 272, 289, 307, 328, 340; `root` | 32; 32 | PC 2 / 40 / `0x0100401C` / 2,1; PC 6 / 56 / `0x0180401C` / 3,1 | PC 31 / 156 / `0x0080001E` |
| `init` | 11-136; `root/proto0` | 464; 98 | PCs 3,7,11,15,19,23,27,31,35,39 / `0x0200405C` / 4,1; PC 42 / `0x0180405C` / 3,1; PCs 44,46 / `0x0100405C` / 2,1; PC 49 / `0x0180405C` / 3,1; PCs 54,59,64,69,74,79,84,89,94 / `0x0280405C` / 5,1; PC 96 / `0x0100405C` / 2,1 | PC 97 / 852 / `0x0080001E` |
| `update` | 139-193; `root/proto1` | 1489; 40 | PCs 2,5,8,11,14,17,20,23,26 / `0x0180405C` / 3,1; PC 30 / `0x0180805C` / 3,2; PC 38 / `0x020040DC` / 4,1 | PC 39 / 1645 / `0x0080001E` |
| `reset` | 196-253; `root/proto2` | 2083; 43 | PCs 3,7,11,15,19,23,27,31,35,39 / `0x0180405C` / 3,1; PC 41 / `0x0100405C` / 2,1 | PC 42 / 2251 / `0x0080001E` |
| `processUICommandOperate` | 256-272; `root/proto3` | 2437; 12 | PC 10 / 2477 / `0x0500415C` / 10,1 | PC 11 / 2481 / `0x0080001E` |
| `processUICommandSelection` | 275-289; `root/proto4` | 2622; 10 | PC 8 / 2654 / `0x0200419C` / 4,1 | PC 9 / 2658 / `0x0080001E` |
| `processUICommandToggleButton` | 292-307; `root/proto5` | 2776; 10 | PC 3 / 2788 / `0x0200819C` / 4,2; PC 8 / 2808 / `0x020041DC` / 4,1 | PC 9 / 2812 / `0x0080001E` |
| `initToggleButton` | 310-328; `root/proto6` | 2930; 12 | PC 3 / 2942 / `0x0200809C` / 4,2; PC 9 / 2966 / `0x0180019C` / 3,0; PC 10 / 2970 / `0x000040DC` / 0,1 | PC 11 / 2974 / `0x0080001E` |
| `processAskResult` | 331-340; `root/proto7` | 3108; 5 | PC 3 / 3120 / `0x0100409C` / 2,1 | PC 4 / 3124 / `0x0080001E` |

The selected static facts cover listed calls, guards, jumps, returns, CALL
widths, operands and capture records. Per-instruction words and locators are
separate raw ledger evidence. The public source and disassembly above are the
reproducible source for these facts; no private receipt path is required.

The only conditional instructions are `update` PC 32 (`EQ`, word
`0x00C38017`, result of PC 30 compared with numeric `30`) followed by PC 33
(`JMP`, word `0x80000016`, target PC 35), `processUICommandSelection` PC 1
(`EQ`, word `0x01C04017`, parameter 3 compared with numeric `1`) followed by
PC 2 (`JMP`, word `0x80000016`, target PC 4), and `processAskResult` PC 0
(`EQ`, word `0x00C00017`, parameter 1 compared with numeric `1`) followed by
PC 1 (`JMP`, word `0x80004016`, target PC 4). No other guard, jump or tailcall
occurs in the source windows. The one dynamic capture is
`initToggleButton` PC 4 / byte 2946: `SELF` captures `self.setChecked` and its
frame receiver for the open-argument call at PC 10 / byte 2970.

## Local control contract

### Initialization and update

`init` requests `UILuaCommands.ToggleButton` for the nine toggle controls and
`UILuaCommands.Selection` for `ComboBox_FrameRate`. It requests the
`setConfirmCondition("Button_Reset")` condition operation, cancel and close
condition operations, and `setModal(true)`; the source does not establish the
condition's purpose. No `Button_Reset`-to-operate/form route is proved by these
source windows. It issues the following literal setter requests through
user-work group `1`:

| Control | Group | Requested setter work index |
| --- | ---: | ---: |
| `ToggleButton_ActionBar` | 1 | 1 |
| `ToggleButton_Macrobar` | 1 | 41 |
| `ToggleButton_ActionCancel` | 1 | 15 |
| `ToggleButton_DamagePlate` | 1 | 25 |
| `ToggleButton_Vulgarity` | 1 | 27 |
| `ToggleButton_Shadow` | 1 | 60 |
| `ToggleButton_FootSmoke` | 1 | 61 |
| `ToggleButton_Background` | 1 | 63 |
| `ToggleButton_Physics` | 1 | 62 |

These are setter request operands, not a proved getter map. The later
`getControlUserWorkInt(1, control)` call receives only group and control; its
work result is passed as the `workIndex` argument to `getConfigFlag`. The
passing
`init-normal` fixture requested setter work `1` for `ToggleButton_ActionBar`
but its getter returned `901`, which the next request used. No native meaning
of either value or registered group/key record is established.

`init` then performs a fresh `self.update` lookup. `update` performs fresh
`self.initToggleButton` lookups in the same nine-control order, requests
`desktopWidget:getConfigWork(64)`, and
selects index `1` only when the returned value equals numeric `30`; every
other observed non-30 integer selected index `0`. The finite original-word
cases covered both `30 -> 1` and `60 -> 0`.

`initToggleButton(control)` requests
`self:getControlUserWorkInt(1, control)`, passes that work result to
`desktopWidget:getConfigFlag(workIndex)` with open result width, and forwards
that call's complete result tail to the frame's captured `setChecked` callable
as `setChecked(control, ...)`. The work result is not forwarded to
`setChecked`, and the config-flag result is not used as the work index. The
finite cases retained a zero-result tail, one
Boolean result, and a Boolean plus explicit nil tail. The open widths are
`PC 9 / raw B=3,C=0` and `PC 10 / raw B=0,C=1`; neither proves a fixed result
arity or Boolean coercion.

One passing capture fixture replaced `frame.setChecked` during
`getConfigFlag`. The `SELF` capture before that getter still invoked the
original frame callable with the complete Boolean-plus-nil tail; a separate
fresh-callable mutation was rejected by the pre-execution callable guard.

### Reset and result handling

`reset` freshly loads global `desktopWidget` for each
`resetConfigWork` request, in this exact order:

`1, 41, 15, 25, 27, 60, 61, 63, 62, 64`, then performs a fresh
`self.update` lookup. The passing fixture pins the original own `reset` and
`update` closures for this result-to-reset chain; a replacement at either
fresh lookup can divert it.
The retained failing-prefix fixture raised at `27` and preserved the
preceding events; later IDs and `update` remain structurally reachable when
the helper returns, as shown by the continuation control below.

A passing reentrant fixture changed the global `desktopWidget` after the
first reset request. The first request used the original receiver; every later
reset ID and the `update` getter requests used the replacement receiver,
matching the fresh global loads in the original words. The existing
replacement corruption control still fails when that rebind does not match the
expected event trace.

`processUICommandOperate` always requests
`desktopWidget:openChildWidget("CommonAskWidget", self, true, nil, 1347, 2,
1348, 1349)` in its method body. The receiver-inclusive raw width is
`B=10,C=1`: nine raw values are present, including the desktop receiver and
the eight explicit values. This is a Lua helper request; the body and native
consumer attribution remain opaque, as do the return and dialog semantics.
The source has no own branch or predicate in this method.

`processAskResult` performs a fresh `self.reset` lookup only when its second
positional value is numeric `1`. Numeric `0` was covered as a no-op. Boolean
`true`, nil and other values were not dynamically visited. The source contains no own save,
apply, refusal, server, restart or OS request.
There is no proved child-to-`processAskResult` callback bridge: operate and
the result handler were tested as separate invocations, not as a completed
child opening followed by an automatically delivered result.

### Direct control requests

`processUICommandSelection` requests
`desktopWidget:setConfigWork(64, value)`, with `value=30` when its fourth
positional parameter equals numeric `1`, otherwise `60`. The finite cases
covered both values. `processUICommandToggleButton` resolves the control's
group-1 work index and requests
`desktopWidget:setConfigFlag(workIndex, value)`, forwarding its sixth
positional parameter without a local Boolean conversion. The finite case
covered Boolean `true`; a corruption control changing it to integer `1` was
rejected by the typed raw expectation.

The request operands are local Lua evidence. Native configuration stores,
registered group/key names, coercion, file contents, persistence and any
consumer effects remain the boundaries owned by
`xivl-client-structs:docs/user-config-store-contract.md` and
`xivl-client-structs:docs/desktop-native-call-contract.md`.

## Public contract bounds

| Concept | Current source bound |
| --- | --- |
| Control/work requests | The source emits group `1`, the nine literal control names, and the nine requested setter work indexes through `setControlUserWorkInt`. A work result is passed to `getConfigFlag`; that call's complete result tail is passed to the captured `setChecked` callable. No native consumer body or global work-index map is established by these source windows. |
| Local request ordering | The source contains separate local request shapes: operate requests `CommonAskWidget`; a separately invoked numeric result `1` performs a fresh `self.reset` lookup; the pinned fixture then runs reset requests and a fresh `self.update` lookup. Selection and toggle requests are local setters. No callback bridge, completed child opening, apply success, cancellation effect, save completion or disk persistence is established. |
| Store identity boundary | The source windows expose no character ID, store constructor, resource filename, system-store initialization or file-content edge. `getConfigWork(64)` and `setConfigWork(64, value)` remain opaque operands. |

The static matrix shows all source guards and their destinations. Dynamically
visited cases covered initialization, both frame-rate outcomes, all ten reset
IDs and order, numeric-result reset and no-op, operate, both selection values,
Boolean toggle forwarding, zero/Boolean/nil config-flag tails, the reset-at-27
prefix, the missing-control prefix, fresh own-closure lookup mutations,
same-label alternate receivers, same-label argument identity, and a typed
state-only mutation. Unvisited outcomes include nonnumeric or metamethod
comparisons, missing/foreign native receivers, base-widget dispatch, native
result production, and arbitrary Lua coercion.

## Verification boundary

The original-word executor ran 15 typed cases: 13 successful and 2 expected
error prefixes. It checked 268 raw call events against the 54-row call ledger
and ran 15 isolated corruption controls. Controls changed actual operand,
state, receiver, global lookup or callable objects while preserving each
passing baseline; every corrupted run failed the independent raw assertions.
The state fixtures seeded distinct work/config values before init/reset so a
suppressed setter or reset could not pass by retaining an expected value. A
state-only Boolean-to-integer mutation preserved all request events but was
rejected by the independent `state write mismatch` oracle; argument identity
was checked separately from display labels and rejected with an `argument
identity mismatch` result.

The failing fixture preserves the original error at `27` and validates the
actual preceding prefix. A control mutant suppressed that helper failure,
continued the original later reset IDs and the fresh `self.update` lookup with complete stubs,
retained the original error, and was rejected by an independent guard for its
extra actual requests. This demonstrates the guard without claiming that the
retail helper suppresses errors. Metamethods, native effects, storage application,
persistence, server outcomes, restart/OS effects and complete lifetime remain
unresolved.

## Standard Configuration entry and closed frame-rate selector

MEASURED. The selected standard resources are the following. Decoded SQWT
sizes include the UTF-8 BOM and retain the original CRLF line endings.

| Resource | Carrier bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `widget/ConfigWidget.form` | 2930 / `2029f43c19dd567ad11946553ba09520fe8f4860bfa85c57ae0f00409d972cbf` | 2922 / `6114add8a5e292997ae903575e7c73a044275826ad83cf2275b51f970381ad45` |
| `widget/ConfigSystemWidget.form` | 15103 / `9a53345e2bfa1b790a26837d67f600b0df087cbff6b36c013a20324bf9e02e85` | 15095 / `e5ca55ee2b9fb759d96d6cd9dca356eaafd18bce7ecbb555f21ed13f9d52ff68` |
| `widget/ConfigSystemWidget.tpl` | 3561 / `7968c998152122313cd3e5e2dd001182222122a316745c419d5ff3afa4feca09` | 3553 / `d6f16d532cf59eeb28a79f17a7d465e94c5b02d84db12c790a3b84f4395783e7` |

Decode each SQWT carrier after its eight-byte header using
`xivl-tools:tools/blowfish.py`, with its complete basename as the key. Retain
the decoded line endings when checking these digests. These are declarations
and authenticated static analysis, not an original-client execution.

### System child and shared close

OBSERVED. The Configuration opener is the existing
[ConfigWidget resource](config-sound-widget-contract.md#configuration-menu-opener).
Its `main/f0` PCs 0-2 call `setConfirmCondition("Button_System")`.
The common helper `widgetbaseclass_common` `main/f56` PCs 0-4 registers that
control for `UILuaCommands.Operate` with condition 5. In ConfigWidget
`main/f2` PCs 0-8, the exact sender name `Button_System` selects
`desktopWidget:openChildWidget("ConfigSystemWidget", self, true)`.
The CALL has B=5,C=1. There is no mode argument or additional initializer
operand. The Configuration form's `Button_System` declares that command,
Content `@1360`, style `BTN_basis` and MinWidth 208. It has no local command
target, command parameter, template or click mode.

OBSERVED. Desktop connector `openChildWidget`, `main/f536` PCs 0-9,
reads the supplied parent's widget index and tailcalls
`openWidget(index,"ConfigSystemWidget",nil,parent,true,...)`. For this
no-extra-argument caller, the vararg tail is empty. The
[creation request](content-director-ui-contracts.md#openwidgetlocal-creation-request)
owns the parent liveness, saved input and exact-true creation gates.
The child inherits Configuration's category index. This call does not request
an independent replacement of its live root. Connector `processWidgetCreated`
`main/f532` PCs 20-27 installs the created widget as the root only if that
category's entry is nil. Its enabled/visible branches reach `show()` at
PCs 59-60. Creation success and current parent identity remain prerequisites.

OBSERVED. System init `main/f0` PCs 43-49 calls `setCancelCondition()`,
`setCloseCondition()` and `setModal(true)`, then calls `update()` at PC96.
The standard root is `Window_ConfigSystemWidget`, with margin `318,64,0,0`,
style `WIN_basis_noDecoration` and cyclic directional navigation. It imports
`common/WINBasis.tpl` and the selected System template above. Its childless
footer `Button_Close`, decoded form line 164, declares
`UILuaCommands.WidgetClose`, Content `@1318`, style `BTN_basis`, MinWidth 120
and right alignment. It has no local target, parameter, template or click
mode. It is not a title-template close button.

The inherited Cancel helper registers `_widget` with condition 5
(`widgetbaseclass_common` `main/f58` PCs 0-7). The Close helper does likewise
for WidgetClose (`main/f59` PCs 0-4). Common Cancel forwards to
`processUICommandClose` (`main/f16` PCs 0-5), and that method calls
`desktopWidget:closeWidgetDirect(self)` (`main/f17` PCs 0-3). System's eight
own methods above override neither route. The
[recursive close and finalizer](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/main-menu-command-route.md#community-menu-close)
qualify the native deletion and root cleanup. A different live Configuration
root survives the child finalizer. ConfigWidget alone overrides
`processClosing` to request `_saveUserConfig()` (`main/f3` PCs 0-2).
System does not add a save call on its own close. This is not proof of disk
write completion or immediate native finalization.

Neither selected own initializer makes an explicit named-control focus
request. Modal, input-enable and show requests do not establish the final OS
or native focused element. The ordinary shared command gates still apply.

### Closed frame-rate presentation

MEASURED. System form lines 151-154 declare `ComboBox_FrameRate`, Width 120,
style `COM_basis`, selected `ControlTemplate_ComboBox`, and Text `@2316`.
It owns exactly two childless inline ComboBoxItems, in this order:

| Name | Content | Declared item properties |
| --- | --- | --- |
| `ComboBoxItem_Frame1` | `@2316` | IsTabStop False, FontEdge True, style NULL, IsHitTestVisible False |
| `ComboBoxItem_Frame2` | `@2315` | IsTabStop False, FontEdge True, style NULL, IsHitTestVisible False |

Both select `ControlTemplate_ComboBoxItem`. Neither declares ItemsSource or
an item data template. The selected item template, System template lines
30-35, contains one Button with style `BTN_basis_listboxSelect`, MinHeight 20
and MinWidth 100, and an element-form OneWay Content binding to its templated
parent. These are inline choice contents, not unconditional sibling rows in
the closed form.

MEASURED. The selected ComboBox template's DockPanel contains two toggle
parts bound TwoWay to IsDropDownOpen. `PART_DropDownButton_Text` has style
NULL and contains `PART_Label`, Height 16 and FontSize 13. That label's Text
binds OneWay to its templated parent's Text, with Padding `2,-1,0,0`
(template lines 13-21). `PART_Popup` separately binds IsOpen TwoWay to
IsDropDownOpen and contains `PART_ListBox` (lines 22-28). The template's
Selection trigger declares `UILuaCommands.Selection` and sound 3. Its
Operate trigger declares OpenDropDown and sound 3. The popup Escape binding
and the list's Cancel trigger declare CloseDropDown. These declarations do
not by themselves prove physical input delivery or successful popup layout.

STATIC. In the pinned executable identified by
[xivl-decomp's ComboBox contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#input-and-method),
constructor `0x009695C0` clears object byte `+0x4A8` bits 0-5 at
`0x0096960E`. The two following metadata operations at
`0x00969635..0x0096967D` restore only bits 1 and 0. Thus its IsDropDownOpen
bit `0x20` starts clear. The selected form declares no overriding open
value. Popup hiding, part ownership and changed open/close callbacks remain
owned by that native contract. A closed-only consumer can preserve these two
inline items and show the current parent Text without painting their popup
choices or claiming support for dropdown selection.

MEASURED. The English `xtx/_text_ui` rows 2315 and 2316, field 1, resolve to
`30 fps` and `60 fps`. In data resource `0x0B4502B5` their stored intervals
are `[0x2FF3,0x2FFD)` and `[0x2FFD,0x3007)`, with SHA-256
`5d005cd9bdc3ca544574d760eb81a0acfdf008c84c542530a0448ad3dafea450`
and `5b8c3a298302e1a1ffe2505ae6c268455e711017687173045fdae5da6d48d199`.
The sheet definition, enable and offset resources are identified in
[xivl-decomp's selected English UI text route](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-plain-text-reference-lookup.md#static-english-definition).
The Lua update rule above selects index 0 for value 60 and index 1 for 30.
[Work index 64](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/desktop-user-config-reads.md#work-index-map)
selects Lua GameConfig group 5/key 9. Its registered `draw_frame_rate`
default is 60 in
[xivl-client-structs](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/user-config-store-contract.md#group-4-lua-group-5).
This establishes the unmodified default closed caption. This section does
not establish how a changed selected item replaces Text, popup item hit
geometry, or native frame pacing.

## System Vulgarity toggle gesture and current setting

MEASURED. In the authenticated standard System form above, decoded line 89
names the childless `ToggleButton_Vulgarity`. It declares
`UILuaCommands.ToggleButton`, IsChecked True, style `TOG_config`, Width 120,
right/center alignment and Grid.Column 1. It declares no local Content,
Template, CommandTarget, CommandParameter, ClickMode, Visibility or
IsEnabled. Its parent Grid has Margin `12,2,0,2` and Help type 1/value 0
`@77405`. Neither that parent nor the toggle declares a visibility override.
The adjacent descriptive TextBlock is a separate element, not the command
sender. This scopes the control declaration, not its effective ancestor
visibility, hit footprint or current focus.

The selected `common/default.style` has 353783 carrier bytes, SHA-256
`632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0`,
and 353775 decoded bytes, SHA-256
`33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6`.
Its `TOG_config` style selects CheckedButton `TOG_config_leftOn` and
UncheckedButton `TOG_config_rightOn` (lines 3448-3451). Each referenced
Button style has one Frame (lines 1577-1600). For either prefix, Normal
uses suffix `_N`, Hover/Active/Anchored/Reserved use `_H`, Disabled uses
`_D`, and Focused/Droppable use NULL. These are Toggle image groups and
style references, not two form-declared child Button command senders.
The [native checked callback](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/input/game-controller-startup.md#checked-state-callback-changes-the-image-part-index)
selects image-part index 1 for checked and 0 for unchecked. The
[Toggle group ordering](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/action-menu-timer-icon-style.md#conditional-initial-toggle-skin)
selects UncheckedButton before CheckedButton independently of XML order.

OBSERVED. System init `main/f0` PCs 16-19 requests
`setControlCommandCondition("ToggleButton_Vulgarity",
"UILuaCommands.ToggleButton")`. Common `main/f55` PCs 0-4 passes that
control and command to `_setUICommandCondition` with condition 5. System
PCs 70-74 assign group-1 control user-work 27 to the same named control.
Its update calls `initToggleButton("ToggleButton_Vulgarity")` at
`main/f1` PCs 12-14. The existing `main/f6` getter chain above restores the
current config flag through `setChecked`. Thus a completed update can
replace the form's initial True with the current stored False.

STATIC. The identified native
[Toggle release path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#arrow-release-and-checked-state-binding)
uses default ClickMode 2 and requires its handled, hit and prior pressed
conditions. Click calls primary slot 71 at `0x0097ED20`, reaching
`0x0095D2B0 -> 0x0095D470`, before it tests and routes the stored Command
at `0x0097ED22..0x0097ED73`. The guarded changed branch complements the
effective IsChecked bit `0x20` at object `+0x3B4`, writes it at
`0x0095D4D6` and invokes its callback at `0x0095D4D8`. A refused property
mutation does not establish a complemented value. The later command can
still observe the effective old checked state. These paths establish
ordering after accepted native Click, not arbitrary pointer acceptance or
successful command subscription.

OBSERVED. The inherited command dispatcher supplies the value rather than
requiring a Boolean command parameter. In `widgetbaseclass_common`
`main/f13`, PCs 137-141 match `UILuaCommands.ToggleButton` and read
`self:getChecked(sender)`. PCs 142-148 call
`processUICommandToggleButton(template,sender,extra1,extra2,checked)` using
the first checked result. Common `getChecked`, `main/f103`, requests the
sender's IsChecked through `getControlProperty`. System `main/f5` PCs 0-8
then reads `getControlUserWorkInt(1,sender)` and calls
`desktopWidget:setConfigFlag(workIndex,checked)`. The retained root/control
subscription, current named control and native routing gates qualify this
join. The value is current property readback, not a guessed complement of
a cached config value or an integer command parameter.

OBSERVED. Desktop connector `setConfigFlag`, `main/f490` PCs 0-7, converts
exact Boolean true to integer 1 and every other normally returned value to
0, then calls `setConfigWork`. That helper, `main/f485` PCs 0-24, resolves
the group/key and reads `_getUserConfig`. Missing group or an equal current
value returns false. Otherwise it calls `_setUserConfig(group,key,value)`
at PC19 and `updateConfigWork(workIndex)` at PC22 before returning true.
Its `main/f486` has no work-27 arm. The work-index map's `main/f484`
PCs 139-143 selects Lua GameConfig group 3/key 8 for work 27.
The [native store](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/user-config-store-contract.md#record-model)
places the integer in the current record and then notifies its configured
listener. The registered record is `vulgar`, native group 2/key 7, default 1.
A subsequent successful `getConfigFlag(27)` reads that current integer and
returns true only for 1. The local setting is not deferred until Close.

There is no own update, reset, child close or save request in the toggle
handler. The shared System-close and parent Configuration save boundaries
above remain distinct. The
[Search comment formatter](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/text-word-filter.md#inputs-and-method)
reads the same current config record when it projects a comment. This
setter path does not establish an automatic repaint of previously projected
comments, successful disk persistence or a historical user's saved choice.
Frame-rate interaction and other controls are outside this gesture contract.

## Selected inline frame-rate caption

STATIC. In the identified executable above, ComboBox Text has descriptor
`0x0135B14C`, ordinal 2. Initializer `0x00F242B0..0x00F242C9` joins it to
string `Text` at `0x010707E0`. Descriptor `0x0135AFE4` instead names
SelectionBoxItemTemplate, ordinal 3 (`0x00F242D0..0x00F242F3`, string
`0x010707E8`). These two properties must remain distinct.

The [Selector index callback](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#selector-payload-and-events)
at `0x0096F440` takes its ordinal-0 arm only with nonnull ItemsPanel at
owner `+0x35C`, then calls `0x0096F080` with current SelectedIndex at
`+0x480`. That routine constructs the added/removed index lists and
raises SelectionChanged through `0x0091F1E0` at `0x0096F3E9`.
The ComboBox input interface cell `0x01070AB8` selects `0x0096EA60`.
For event id `0x3C`, its call at `0x0096EA84` reaches primary slot 71.
ComboBox primary cell `0x01070CC8` selects `0x00968C90`. The primary
table has zero-offset COL `0x0117C964` and remains the concrete receiver.

At `0x00968C9E`, this handler requires event source `+8` equal to itself.
It takes the first added index only when that vector is nonempty
(`0x00968CA7..0x00968CE2`), resolves the logical item through
`0x00961420` on its accessor at owner `+0x3A0`, and requires a successful
FrameworkElement cast. Its virtual `+4` call at `0x00968D0B` obtains
that item's text representation. The concrete inline ComboBoxItem's
primary table `0x010807FC`, zero-offset COL `0x01181A98`, has slot 1
`0x00934AD0`. That getter reads Content's text pointer at item `+0x344`,
falling back to the shared empty string when null. The
[Content storage](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-qualified-property-lookup.md#contenttemplate-write-gates-and-fresh-content)
contract distinguishes that pointer from the Content payload and type flags.

The handler passes that text to the owner Text holder at `+0x4AC`, with
Text descriptor `0x0135B14C`, ordinary update mode 0, notify 1 and final helper flag 1
(`0x00968D0D..0x00968D28 -> 0x009BA4E0 -> 0x00983FE0`). The holder's
property guards and string equality still apply. A changed admitted string
reaches notification through `0x00953BA0`. The existing OneWay
TemplatedParent.Text binding on `PART_Label` can therefore reflect the new
current Text, rather than retaining the form's original `@2316` forever.
The later `0x00967B60` call also installs a Content-to-Text binding for the
selected FrameworkElement (`0x00967B8E..0x00967BAE`). General subsequent
Content mutation and template replacement are outside this caption case.

For the two authenticated inline items above, realized selection index 0
uses Frame1 Content `@2316`, and index 1 uses Frame2 Content `@2315`.
The existing English text lookup yields `60 fps` and `30 fps`, respectively.
Thus an initial stored work-64 value 30, followed by the normal System
update's index-1 request with its current ItemsPanel and logical items ready,
can replace the default closed caption with the second item's text. This is
a qualified selected-item path, not a rule that arbitrary indexes or missing
items clear the caption. This trace does not settle replay when index was
set before ItemsPanel became available, failed property mutation, or a
retired/replaced source. Those cases must not be promoted to this success.
Caption synchronization uses SelectionChanged. It does not itself establish
the separate Selection event used by the template below. A Lua index restore
must not be treated as an additional user Selection command.

## Frame-rate selection application boundary

OBSERVED. The selected System ComboBox template declares Selection on
SourceType ComboBox, then `UILuaCommands.Selection` without a parameter.
The shared Lua dispatcher reads `getSelectedIndex(sender)` before calling
`processUICommandSelection(template,sender,index,extra)`
(`widgetbaseclass_common` `main/f13` PCs 41-55). A negative current index
returns without that handler call. System `main/f4`
PCs 0-8 sends `setConfigWork(64,30)` only for numeric index 1, and 60
otherwise. Its registered sender is the current `ComboBox_FrameRate` from
init `main/f0` PCs 36-39. The two valid installed rows provide indexes
0 and 1. These local requests use Lua GameConfig group 5/key 9, not the
separate native SystemConfig store.

The [native selection command path](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#named-left-button-release)
qualifies a named release by its receiver's source-to-index lookup. With a
nonnegative match it requests that receiver's index and raises Selection.
It does not forward an arbitrary nested ListBox selection to the ComboBox.
The System declaration and native source-qualified path are not proof of
an OS hit or a complete popup arrangement. The immediate config setter and
parent Configuration save boundaries above also apply here. There is no
additional System close/save call in this selection handler, and no frame
pacing behavior is established.

## Standard frame-rate popup gestures and inline source lookup

MEASURED. The selected System template above has the same named ComboBox
parts as the [native dropdown join](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#retained-template-parts).
`PART_DropDownButton` is the childless right-docked arrow ToggleButton.
`PART_DropDownButton_Text` holds `PART_Label`. Both toggles declare
Focusable False and TwoWay IsChecked to the current templated parent's
IsDropDownOpen, with no Command or ClickMode. The label separately declares
LeftClick -> ComboBox.OpenDropDown with that parent as explicit target.
The template's Operate trigger also opens the dropdown. `PART_Popup` holds
`PART_ListBox`, and no PART_EditableTextBox is declared. Popup binds IsOpen
TwoWay to the same owner. Its PlacementTarget and MaxHeight binding strings
omit the outer closing brace, as in the selected Journal template. They
are the installed syntax, not balanced replacement declarations.

The current COM_basis style selects DownButton TOG_basis_comboDown,
ListBox LIB_basis_comboList and Background COM_basis_bg. The arrow style
uses BTN_basis_comboDown for both checked states. Its Normal/Disabled,
Hover/Anchored and Active Frames select suffixes `_N`, `_H` and `_A`.
Each selected skin has one Stretch cell, a 20-by-20 source rectangle and
HitMargin 2. These source dimensions do not establish physical hit size.
The list style selects WIN_basis_comboList for its background. Its ordinary
Frame uses WIN_basis_comboList_frame_N, with a 3-by-3 cell grid,
HitMargin 4 and SkinBorderThickness 4. The skin carrier
`common/default.skin` is 141967 bytes, SHA-256
`6788f2986d9cc8aeab83fcdbcf7a9115d3576ecfabf40529cc861f41f0df5640`.
Its decoded 141959 bytes have SHA-256
`929e65e9d5f191292d9b044e3e659ba115f18f6b3d8a82894046a7c75cbcad5a`.
The style carrier is pinned in the Vulgarity section. The two inline choice
objects and their selected Button_XXX template are pinned above. That
Button has no explicit command or parameter in the selected template.

STATIC. An admitted arrow Click uses the existing Toggle mutation before
its command phase. The attached TwoWay binding can reverse-transfer the
new checked value to owner IsDropDownOpen. The owner's changed callback
first notifies property listeners at `0x00968102`, allowing the binding to
request Popup.IsOpen and its Visible/Hidden state, then requests focus on
the retained popup at `0x0096815B` when still open. Explicit OpenDropDown
can make an additional focus request preferring the retained list over the
popup at `0x00968B1B..0x00968B4A`. These are different admitted opening
paths. Neither proves the eventual stored focus. The exact property,
release, binding and focus guards are in the
[arrow and focus contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#arrow-release-and-checked-state-binding).
No settings write is established merely by opening the popup.

### Inline row source to index

STATIC. The no-ItemsSource branch of `0x00960DE0` delegates source lookup
to the current generator at owner `+0x368`, virtual `+0x10`
(`0x00960FC7..0x00960FE1`). The standard System ComboBox declares no
ItemsSource. Constructor `0x009695C0` constructs its embedded generator
at owner `+0x508` at `0x0096972F..0x00969741`, installs vtable
`0x01070A1C`, and passes it to the ItemContainerGenerator setter
`0x009635D0` at `0x009697EF`. The corresponding property descriptor
is `0x0135AC40`. That table's slot 4, cell `0x01070A2C`, selects
`0x009C3A30`.

The lookup returns -1 for a null retained panel at generator `+8` or for a
source outside that panel's recursive child tree
(`0x009C3A34..0x009C3A4B -> 0x00929800`). It then visits current panel
children in order, using the array at panel `+0x2B4/+0x2B8` and
`0x00978B50` at `0x009C3A50..0x009C3A77`. A direct child identity match
or recursive descendant match returns that child's zero-based index
(`0x009C3A7C..0x009C3AA6`). Exhaustion returns -1. The panel itself is
not a child match. Helper `0x00929800` enumerates the receiver's child
collection and recurses, rather than checking names or screen coordinates.
The generator's panel attachment/migration method is `0x009C3BD0`.
This establishes a source predicate on the current retained composition,
not an association with a previous panel, another ComboBox or a same-name
Button outside the current row. The generator/panel and logical-item order
must agree before treating the result as one of the two installed choices.

The shared preview release `0x0096ED00` can call `0x0096EC00(index,0,1)`
only after the event remains unhandled and this receiver's lookup succeeds.
That call requests SelectedIndex, then raises Selection for a requested
index other than -1. An equal index can skip SelectionChanged but still
raise this user Selection event. The selected System trigger and shared Lua
readback above then own the current index-to-work-64 request. Ordinary
ComboBox release `0x00968A20` independently requests closure after its own
successful source lookup. It does not require a changed SelectedIndex.
The [paired release contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-combobox-dropdown.md#named-left-button-release)
owns these branches and their order. A nested ListBox Selection alone is
not a substitute for the qualifying ComboBox source and trigger.

### Close and surviving input boundary

STATIC. Clearing owner IsDropDownOpen can notify Popup.IsOpen and request
Visibility Hidden through the existing binding/callback path. In the closed
owner callback, the explicit focus request at `0x009681C1` is conditional
on retained PART_EditableTextBox at owner `+0x4CC`. The selected System
template has none. This branch supplies no explicit return focus to the
ComboBox, prior row or parent Configuration. Visibility/focus-manager
side effects and the final keyboard-focus recipient remain unqualified.
Popup Escape and the list's Cancel trigger request CloseDropDown as declared
above. They do not declare Selection or a settings write. Their routing and
precedence depend on current focus and unhandled input.

The proven row action begins with delivery of the current row source to the
ComboBox preview/ordinary handlers. Complete OS press/capture ingress,
actual arranged row hit rectangles and the popup's current route back to
that owner were not observed. The inline item declarations have
IsHitTestVisible False. They alone do not identify the effective physical
source in a generated row. ComboBox generator creation `0x00967BF0` is
a further discriminator for that realized container and its inner content. The route builder walks interface parent
`+0x60` at `0x0091E2A6`. Establishing that current ancestor chain across
the realized popup is a remaining discriminator before claiming an
unconditional physical row click. A bounded consumer can retain the exact
arrow/open and current-row predicates above without claiming arbitrary
ListBox forwarding, guaranteed focus restoration or frame pacing.
