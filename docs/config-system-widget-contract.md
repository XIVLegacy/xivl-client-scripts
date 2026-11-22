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
