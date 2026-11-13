# ConfigSoundWidget contract

`ConfigSoundWidget` is a local sound-configuration editor recovered from the
retail Lua chunk for `widget/configsoundwidget`. The body requests seven
control user-work slot/group 1 assignments for ids 50 through 56. Later
getter results supply the ids forwarded through `desktopWidget`; the setter
requests do not establish those results. The published desktop map associates
those ids with keys 1 through 7 in Lua config group 4. Applying that map to
an invocation requires both the corresponding getter result and the dynamic
helper lookup reaching the documented connector/map. The widget uses
`CommonAskWidget` for reset confirmation. This contract covers the root
binding and all nine own methods. It does not claim effective audio output,
native store success, application timing, completed save or persistence,
server behavior, or object lifetime.

## Evidence and reproduction

The logical resource is `widget/configsoundwidget`; its ciphered source is
`n1635q/7vw413rvpw6n1635q.lua` and its LPB is
`n1635q/7vw413rvpw6n1635q.le.lpb`. The LPB is 2,972 bytes with SHA-256
`7d55428a0a5a5dbe5abfd9a8988179ac2e36931118334643089fedb3b7fbcfb6`. Its
decoded Lua 5.1 payload is 2,959 bytes with SHA-256
`d7a83e29863f9b8745b0f2e1d13056b2c0f59a20b31d567c2f28066fe8b271ff`.

The canonical LF decompile is 6,784 bytes and 320 LF lines with SHA-256
`12405b2e3a6626124cfafaa081e7969c32062147e4867662a39de6c0408606a6`.
The pinned scripts revision is `65a5cefa6d7a130b4242723ae1707b5773867b74`.
Decoding used `tools/retail_script.py` (3,555 bytes, SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`) and
`tools/vendor/unluac/unluac_2025_12_23.jar` (796,256 bytes, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`). The
bounded Lua parser and typed executor use the pinned host helper
`tools/build_quest_contracts.py` (SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`) only
for Lua 5.1 chunk parsing and instruction decoding.

Public bytecode reproduction uses the repository decoder and pinned unluac
disassembler. Replace `<retail-client-script-root>` with the local retail
`client/script` directory and `<scratch>` with a separate writable directory
outside the public tree:

```text
python tools/retail_script.py --input <retail-client-script-root>/n1635q/7vw413rvpw6n1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/configsoundwidget.luac --script-out <scratch>/configsoundwidget.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/configsoundwidget.disasm <scratch>/configsoundwidget.luac
```

Compare the decoded payload and canonical source with the pinned identities
above, then use the exact root, prototype, PC, byte and word locators in this
contract. Finite typed checks are summarized below but do not depend on a
public harness path. All source reads were bounded to this resource; no
connector, form, native, store or server body is part of this contract.

## Root binding

The root has 35 words at byte offset 32. Its two direct requests are
`require("/Widget/WidgetBaseClass")` at root PC 2, byte 40, word
`0x0100401C`, ABC `(0,2,1)`, fixed width 1 argument/zero results, and
`_defineClass("ConfigSoundWidget", "WidgetBaseClass")` at root PC 6, byte 56,
word `0x0180401C`, ABC `(0,3,1)`, fixed width 2 arguments/zero results.
The root then attempts nine closure assignments to the global
`ConfigSoundWidget` table:

| Method | Source assignment | Closure | SETTABLE |
| --- | ---: | --- | --- |
| `init` | 109 | root PC 8, byte 64, `0x00000064`; child `root/proto0` | root PC 9, byte 68, `0x82804009` |
| `reset` | 154 | root PC 11, byte 76, `0x00004064`; child `root/proto1` | root PC 12, byte 80, `0x83004009` |
| `initControls` | 189 | root PC 14, byte 88, `0x00008064`; child `root/proto2` | root PC 15, byte 92, `0x83804009` |
| `processUICommandOperate` | 215 | root PC 17, byte 100, `0x0000C064`; child `root/proto3` | root PC 18, byte 104, `0x84004009` |
| `processAskResult` | 227 | root PC 20, byte 112, `0x00010064`; child `root/proto4` | root PC 21, byte 116, `0x84804009` |
| `processUICommandToggleButton` | 245 | root PC 23, byte 124, `0x00014064`; child `root/proto5` | root PC 24, byte 128, `0x85004009` |
| `processUICommandSliderChange` | 270 | root PC 26, byte 136, `0x00018064`; child `root/proto6` | root PC 27, byte 140, `0x85804009` |
| `initToggleButton` | 291 | root PC 29, byte 148, `0x0001C064`; child `root/proto7` | root PC 30, byte 152, `0x86004009` |
| `initSliderBar` | 320 | root PC 32, byte 160, `0x00020064`; child `root/proto8` | root PC 33, byte 164, `0x86804009` |

These are binding attempts represented by the bytecode. They do not prove that
the native class publication or a runtime widget owner completed.

## Method windows and direct calls

Each method's source window is inclusive. `CALL` entries below give
`prototype PC/byte word ABC width`, where width is `(argument count, result
count)`. `C=0` is an open result tail; `B=0` is an open argument tail. There
are no `TAILCALL` instructions. Every method ends with raw `RETURN` word
`0x0080001E` (zero explicit results).

| Method | Source; prototype; arity | Direct CALL words and targets |
| --- | --- | --- |
| `init` | `configsoundwidget.lua:11-109`; `root/proto0`; 1 | `pc3/515 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc7/531 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc11/547 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc15/563 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc19/579 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc23/595 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc27/611 0x0200405C (1,4,1) w(3,0) -> setControlCommandCondition`; `pc30/623 0x0180405C (1,3,1) w(2,0) -> setConfirmCondition`; `pc32/631 0x0100405C (1,2,1) w(1,0) -> setCancelCondition`; `pc34/639 0x0100405C (1,2,1) w(1,0) -> setCloseCondition`; `pc37/651 0x0180405C (1,3,1) w(2,0) -> setModal`; `pc42/671 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc47/691 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc52/711 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc57/731 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc62/751 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc67/771 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc72/791 0x0280405C (1,5,1) w(4,0) -> setControlUserWorkInt`; `pc74/799 0x0100405C (1,2,1) w(1,0) -> initControls` |
| `reset` | `configsoundwidget.lua:112-154`; `root/proto1`; 1 | `pc3/1318 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc7/1334 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc11/1350 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc15/1366 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc19/1382 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc23/1398 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc27/1414 0x0180405C (1,3,1) w(2,0) -> desktopWidget.resetConfigWork`; `pc29/1422 0x0100405C (1,2,1) w(1,0) -> initControls` |
| `initControls` | `configsoundwidget.lua:157-189`; `root/proto2`; 1 | `pc2/1599 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc5/1611 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc8/1623 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc11/1635 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc14/1647 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc17/1659 0x0180405C (1,3,1) w(2,0) -> initSliderBar`; `pc20/1671 0x0180405C (1,3,1) w(2,0) -> initToggleButton` |
| `processUICommandOperate` | `configsoundwidget.lua:192-215`; `root/proto3`; 5 | `pc13/1948 0x0500419C (6,10,1) w(9,0) -> desktopWidget.openChildWidget` |
| `processAskResult` | `configsoundwidget.lua:218-227`; `root/proto4`; 2 | `pc3/2135 0x0100409C (2,2,1) w(1,0) -> reset` |
| `processUICommandToggleButton` | `configsoundwidget.lua:230-245`; `root/proto5`; 6 | `pc3/2215 0x0200819C (6,4,2) w(3,1) -> getControlUserWorkInt`; `pc8/2235 0x020041DC (7,4,1) w(3,0) -> desktopWidget.setConfigFlag` |
| `processUICommandSliderChange` | `configsoundwidget.lua:248-270`; `root/proto6`; 6 | `pc3/2369 0x0200819C (6,4,2) w(3,1) -> getControlUserWorkInt`; `pc8/2389 0x018081DC (7,3,2) w(2,1) -> getMaximum`; `pc14/2413 0x020041DC (7,4,1) w(3,0) -> desktopWidget.setConfigWork` |
| `initToggleButton` | `configsoundwidget.lua:273-291`; `root/proto7`; 2 | `pc3/2572 0x0200809C (2,4,2) w(3,1) -> getControlUserWorkInt`; `pc9/2596 0x0180019C (6,3,0) w(2,open) -> desktopWidget.getConfigFlag`; `pc10/2600 0x000040DC (3,0,1) w(open,0) -> setChecked` |
| `initSliderBar` | `configsoundwidget.lua:294-320`; `root/proto8`; 2 | `pc3/2750 0x0200809C (2,4,2) w(3,1) -> getControlUserWorkInt`; `pc7/2766 0x018080DC (3,3,2) w(2,1) -> desktopWidget.getConfigWork`; `pc12/2786 0x0180811C (4,3,2) w(2,1) -> getMaximum`; `pc17/2806 0x0200411C (4,4,1) w(3,0) -> setValue` |

## Local contract

`init` installs slider-change conditions for `Slider_BGM`,
`Slider_SystemSE`, `Slider_SE`, `Slider_Voice`, `Slider_EnvSound` and
`Slider_SoundPos`, and a toggle condition for `ToggleButton_DOLBY`. It sets
the confirm control to `Button_Reset`, installs base cancel and close
conditions, sets modal true, requests work group 1 assignments, and calls
`initControls`.

`initControls` calls `initSliderBar` for the six sliders and
`initToggleButton` for `ToggleButton_DOLBY`. `reset` requests
`desktopWidget.resetConfigWork` in order for 50, 51, 52, 54, 55, 56 and 53,
then reinitializes controls. `processUICommandOperate` opens
`CommonAskWidget` only for `Button_Reset`. Its raw `CALL A=6 B=10 C=1`
passes nine ordered arguments after the function register:
`(desktopWidget, "CommonAskWidget", self, true, nil, 1347, 2, 1348, 1349)`.
The first item is the method receiver; the eight explicit
`openChildWidget` arguments are `("CommonAskWidget", self, true, nil, 1347,
2, 1348, 1349)`. Other operate values take the empty branch.
`processAskResult` calls `reset(self)` only when the result is the numeric
value 1. Lua boolean `true` is not equal to numeric 1, so it does not restore.

`processUICommandToggleButton` resolves the control name with
`self:getControlUserWorkInt(1, control)` and requests
`desktopWidget:setConfigFlag(resolvedId, value)`. `processUICommandSliderChange`
uses the same lookup and requests
`desktopWidget:setConfigWork(resolvedId, value)`. When the resolved id is 56,
it first reads `self:getMaximum(control)` and writes
`maximum - value`; other ids forward the value unchanged.

`initToggleButton` resolves the id, captures `self.setChecked` and its receiver,
then calls `desktopWidget:getConfigFlag(id)` with open results. It forwards the
complete result tail to that captured callable with an open argument tail; a
getter that replaces `self.setChecked` after capture does not replace the
callable used by this bytecode. Zero results and an explicit nil are distinct
and remain distinct in the finite checks. `initSliderBar` resolves the id, reads
`desktopWidget:getConfigWork(id)`, applies the same id-56 inversion using
`self:getMaximum(control)`, and calls `self:setValue(control, value)`.

The finite arithmetic model treats Lua numeric values as numbers and accepts a
lexical numeric string such as `"25"` for id-56 subtraction. It rejects
Booleans, nil and nonnumeric strings; these are modeled failure boundaries, not
a claim about every Lua coercion or metamethod.

The established work-index map places 50 through 56 in Lua group 4 at keys 1
through 7 (`xivl-decomp:docs/script/desktop-user-config-reads.md:43-56`).
The table records requested control assignments. Its Lua group/key and record
columns describe the published map's meaning for the requested index. Applying
that meaning to an invocation requires both a later getter returning that
index and the dynamic helper lookup reaching the documented connector/map.
A different getter result is forwarded instead; the actual helper binding
remains unproved. Direct literal reset operands do not depend on a control
getter, while their helper binding and effects remain unproved.

| Control | Requested slot/group | Requested work index | Lua group/key for that index | Registered record for that index; default |
| --- | ---: | ---: | ---: | --- |
| `Slider_BGM` | 1 | 50 | 4 / 1 | `music_volume`; 100 |
| `Slider_SystemSE` | 1 | 51 | 4 / 2 | `sys_volume`; 100 |
| `Slider_SE` | 1 | 52 | 4 / 3 | `se_volume`; 100 |
| `ToggleButton_DOLBY` | 1 | 53 | 4 / 4 | `dolby_iiz`; 0 |
| `Slider_Voice` | 1 | 54 | 4 / 5 | `voice_volume`; 100 |
| `Slider_EnvSound` | 1 | 55 | 4 / 6 | `env_sound_volume`; 100 |
| `Slider_SoundPos` | 1 | 56 | 4 / 7 | `listener_position_scale`; 0 |

The registered names, ranges and defaults are recorded at
`xivl-client-structs:docs/user-config-store-contract.md:215-227`.
This identifies the requested category operands. It does not prove that a
widget request changed a native record, that `getMaximum` equals a store range,
or that audio output changed.

There is no own apply, cancel, close, or save method. Apply/restore behavior is
bounded to the base conditions installed by `init`, the reset ask request and
the numeric-one continuation above. Native storage, readback completion,
application, file writes and persistence remain outside this source envelope.

## Inherited sound-control dispatch

The installed WidgetBase common LPB is
`client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb`, 32996 bytes with
SHA-256 `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c`.
Its decoded Lua 5.1 payload is 32983 bytes with SHA-256
`7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f`.
The decoder, unluac disassembly and ChunkReader method above apply to
this carrier as well. PCs are zero based within `root/proto13`.

| Command branch | Read of sender A2 | Callback, arguments after self |
| --- | --- | --- |
| `UILuaCommands.ToggleButton`, PC137 | Calls `getChecked(self, A2)` for one result at PC141 | `processUICommandToggleButton(A1, A2, A4, A5, checked)` at PC148 |
| `UILuaCommands.SliderValueChanged`, PC151 | Calls `getValue(self, A2)` with open results at PC157 and passes them to `_math.floor` at PC158 for one result | `processUICommandSliderChange(A1, A2, A4, A5, flooredValue)` at PC165 |

The Slider branch resolves the floor callable before the value read. It
derives the config value from that read, while A4 and A5 remain the
separate command inputs passed to the callback. The
[standard selected Style](https://github.com/XIVLegacy/xivl-decomp/blob/d7fdab17b8155a2515f2e1ea8b6947a7dcde77c5/docs/resource/sqwt-track-rectangle-requests.md#float-slider-and-its-sound-configuration-styles)
declares the Slider command without a parameter. Native event delivery and
effective property readback remain conditions on reaching the branch.

## Finite checks and limits

The instruction-driven executor ran 22 typed cases: 18 ordinary cases and 4
expected failures. It checked 164 raw call events, 32 typed expectations, 88
raw receiver/callable identity controls, and 7 corruption controls. Cases cover
initialization and reset order, every reset id, reset confirmation and no-op
command, numeric 1 versus boolean true, toggle and slider requests, id-56
inversion with numeric-string and Boolean boundaries, one-result/multi-result/
explicit-nil/zero-result open tails, and reentrant replacement of
`self.setChecked` after capture. The corruption controls reject a same-label
nested reset receiver, a foreign same-label `openChildWidget` child-self
argument, numeric 1 for Boolean true at both the toggle and exact child-open
callsites, initialization `Slider_BGM` id 50 for 99, reset id 99 for 50, and a
fresh `setChecked` callable. The executor
used the actual frame receiver, desktop receiver and pinned local closures. It
is not a live client run and its supplied helper callables are typed stubs;
the checks therefore establish only the bounded Lua
control flow and raw call shape.

All nine own methods were parsed and exercised through direct or nested calls;
there are no contained child closures. Branches not selected by a finite case,
metamethod behavior, base-widget dispatch, connector behavior, native effects,
file content, persistence, server effects and complete lifetime remain
unvisited or opaque.
