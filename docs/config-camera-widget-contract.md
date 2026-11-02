# ConfigCameraWidget contract

`ConfigCameraWidget` is a local camera-configuration editor recovered from the
retail Lua chunk for `widget/configcamerawidget`. Its nine own methods install
camera control conditions, map controls to work slots, reset those slots,
request camera defaults, forward toggle and slider changes, and initialize
control values. This contract describes those local requests and continuations.
It does not claim that a native request succeeds, that a store changed, that a
camera changed, that a value persisted, or that a widget was rendered or
destroyed.

## Evidence and reproduction

The logical resource is `widget/configcamerawidget`; its ciphered source is
`n1635q/7vw41379x5s9n1635q.lua` and its LPB is
`n1635q/7vw41379x5s9n1635q.le.lpb`. The LPB is 3,583 bytes with SHA-256
`ce49334014b3462d812bcab62487b53898e7f2dd2d4c97dd7622dd268568e795`. Its
decoded Lua 5.1 payload is 3,570 bytes with SHA-256
`5b288396a1d0a2477cfa829175c37fd425c9cfcc1b1d7e6b97f3fa3fa0e4d0d1`.

The canonical LF decompile is 8,532 bytes and 393 LF lines with SHA-256
`babe7210e8e4ca4c520964899586293947ec4da8052c103019dbed89cd4e3983`. The
scripts source metadata revision is
`65a5cefa6d7a130b4242723ae1707b5773867b74`. Decoding used
`tools/retail_script.py` (3,555 bytes, SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`) and
`tools/vendor/unluac/unluac_2025_12_23.jar` (796,256 bytes, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`). The
bounded Lua 5.1 parser and instruction decoder use
`tools/build_quest_contracts.py` (SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`).

Public bytecode reproduction uses the repository decoder and pinned unluac
disassembler. Replace `<retail-client-script-root>` with the local retail
`client/script` directory and `<scratch>` with a separate writable directory
outside the public tree:

```text
python tools/retail_script.py --input <retail-client-script-root>/n1635q/7vw41379x5s9n1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/configcamerawidget.luac --script-out <scratch>/configcamerawidget.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/configcamerawidget.disasm <scratch>/configcamerawidget.luac
```

Compare the generated payload and LF source with the identities above, then
use the exact prototype, PC, byte and word locators below. The LPB, payload and
decompiled body are reproduction inputs, not public fixture bytes.

## Root binding

The root has 35 words at byte offset 32. Its direct requests are:

| PC | Byte | Word | ABC | Width | Request and literal arguments |
|---:|---:|---|---|---|---|
| 2 | 40 | `0x0100401C` | `(0,2,1)` | `(1,0)` | `require("/Widget/WidgetBaseClass")` |
| 6 | 56 | `0x0180401C` | `(0,3,1)` | `(2,0)` | `_defineClass("ConfigCameraWidget", "WidgetBaseClass")` |

The root then attempts these nine global table assignments. A binding attempt
does not prove that class publication or a runtime widget owner completed.

| Method | Source assignment | Closure PC/byte/word | Prototype | SETTABLE PC/byte/word |
|---|---:|---|---|---|
| `init` | 139 | 8 / 64 / `0x00000064` | `root/proto0` | 9 / 68 / `0x82804009` |
| `reset` | 199 | 11 / 76 / `0x00004064` | `root/proto1` | 12 / 80 / `0x83004009` |
| `initControls` | 242 | 14 / 88 / `0x00008064` | `root/proto2` | 15 / 92 / `0x83804009` |
| `processUICommandOperate` | 286 | 17 / 100 / `0x0000C064` | `root/proto3` | 18 / 104 / `0x84004009` |
| `processUICommandToggleButton` | 304 | 20 / 112 / `0x00010064` | `root/proto4` | 21 / 116 / `0x84804009` |
| `processUICommandSliderChange` | 332 | 23 / 124 / `0x00014064` | `root/proto5` | 24 / 128 / `0x85004009` |
| `processAskResult` | 344 | 26 / 136 / `0x00018064` | `root/proto6` | 27 / 140 / `0x85804009` |
| `initSliderBar` | 372 | 29 / 148 / `0x0001C064` | `root/proto7` | 30 / 152 / `0x86004009` |
| `initToggleButton` | 393 | 32 / 160 / `0x00020064` | `root/proto8` | 33 / 164 / `0x86804009` |

## Method windows and direct calls

Each source range is inclusive. Each call is written as
`PC/byte/word; ABC; width -> target`. Width is `(argument count, result
count)`. A zero raw width is written `open`; it forwards a variable tail. All
60 direct calls are `CALL`; this envelope contains no `TAILCALL`. Every method
ends with raw `RETURN` word `0x0080001E`.

| Method | Source; prototype; arity | Direct calls |
|---|---|---|
| `init` | `configcamerawidget.lua:11-139`; `root/proto0`; 1 | `2/512/0x0180405C; (1,3,1); (2,0) -> setModal`; `6/528/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `10/544/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `14/560/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `18/576/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `22/592/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `26/608/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `30/624/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `34/640/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `38/656/0x0200405C; (1,4,1); (3,0) -> setControlCommandCondition`; `41/668/0x0180405C; (1,3,1); (2,0) -> setConfirmCondition`; `44/680/0x0180405C; (1,3,1); (2,0) -> setConfirmCondition`; `47/692/0x0180405C; (1,3,1); (2,0) -> setConfirmCondition`; `49/700/0x0100405C; (1,2,1); (1,0) -> setCancelCondition`; `51/708/0x0100405C; (1,2,1); (1,0) -> setCloseCondition`; `56/728/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `61/748/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `66/768/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `71/788/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `76/808/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `81/828/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `86/848/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `91/868/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `96/888/0x0280405C; (1,5,1); (4,0) -> setControlUserWorkInt`; `98/896/0x0100405C; (1,2,1); (1,0) -> initControls` |
| `reset` | `configcamerawidget.lua:142-199`; `root/proto1`; 1 | `3/1555/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `7/1571/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `11/1587/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `15/1603/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `19/1619/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `23/1635/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `27/1651/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `31/1667/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `35/1683/0x0180405C; (1,3,1); (2,0) -> desktopWidget.resetConfigWork`; `37/1691/0x0100405C; (1,2,1); (1,0) -> initControls`; `41/1707/0x0180405C; (1,3,1); (2,0) -> desktopWidget.setDefaultCamera` |
| `initControls` | `configcamerawidget.lua:202-242`; `root/proto2`; 1 | `2/1924/0x0180405C; (1,3,1); (2,0) -> initToggleButton`; `5/1936/0x0180405C; (1,3,1); (2,0) -> initToggleButton`; `8/1948/0x0180405C; (1,3,1); (2,0) -> initToggleButton`; `11/1960/0x0180405C; (1,3,1); (2,0) -> initToggleButton`; `14/1972/0x0180405C; (1,3,1); (2,0) -> initToggleButton`; `17/1984/0x0180405C; (1,3,1); (2,0) -> initSliderBar`; `20/1996/0x0180405C; (1,3,1); (2,0) -> initSliderBar`; `23/2008/0x0180405C; (1,3,1); (2,0) -> initSliderBar`; `26/2020/0x0180405C; (1,3,1); (2,0) -> initSliderBar` |
| `processUICommandOperate` | `configcamerawidget.lua:245-286`; `root/proto3`; 5 | `6/2353/0x0180419C; (6,3,1); (2,0) -> desktopWidget.setDefaultCamera`; `14/2385/0x0180419C; (6,3,1); (2,0) -> desktopWidget.setDefaultCamera`; `29/2445/0x0500419C; (6,10,1); (9,0) -> desktopWidget.openChildWidget` |
| `processUICommandToggleButton` | `configcamerawidget.lua:289-304`; `root/proto4`; 6 | `3/2692/0x0200819C; (6,4,2); (3,1) -> self.getControlUserWorkInt`; `8/2712/0x020041DC; (7,4,1); (3,0) -> desktopWidget.setConfigFlag` |
| `processUICommandSliderChange` | `configcamerawidget.lua:307-332`; `root/proto5`; 6 | `3/2846/0x0200819C; (6,4,2); (3,1) -> self.getControlUserWorkInt`; `10/2874/0x018081DC; (7,3,2); (2,1) -> desktopWidget.getConfigWork`; `17/2902/0x0200421C; (8,4,1); (3,0) -> desktopWidget.setConfigWork` |
| `processAskResult` | `configcamerawidget.lua:335-344`; `root/proto6`; 2 | `3/3087/0x0100409C; (2,2,1); (1,0) -> self.reset` |
| `initSliderBar` | `configcamerawidget.lua:347-372`; `root/proto7`; 2 | `3/3167/0x0200809C; (2,4,2); (3,1) -> self.getControlUserWorkInt`; `7/3183/0x018080DC; (3,3,2); (2,1) -> desktopWidget.getConfigWork`; `17/3223/0x0200411C; (4,4,1); (3,0) -> self.setValue` |
| `initToggleButton` | `configcamerawidget.lua:375-393`; `root/proto8`; 2 | `3/3412/0x0200809C; (2,4,2); (3,1) -> self.getControlUserWorkInt`; `9/3436/0x0180019C; (6,3,0); (2,open) -> desktopWidget.getConfigFlag`; `10/3440/0x000040DC; (3,0,1); (open,0) -> captured self.setChecked` |

## Local control contract

`init` first calls `self:setModal(true)`. It installs toggle conditions for
`ToggleButton_Camera1` through `ToggleButton_Camera5`, slider conditions for
`Slider_CameraView`, `Slider_CameraOffset`, `Slider_CameraTurn` and
`Slider_LockOn`, confirm conditions for `Button_AllClear`, `Button_Save` and
`Button_Reset`, and base cancel and close conditions. It then installs the
following slot/group mappings and calls `initControls`:

| Control | Slot/group | Work index | Lua group/key | Registered record; range; default |
|---|---:|---:|---:|---|
| `ToggleButton_Camera1` | 1 | 20 | 3 / 1 | `cam_fp_vertical`; 0..1; 1 |
| `ToggleButton_Camera2` | 1 | 21 | 3 / 2 | `cam_fp_horizontal`; 0..1; 1 |
| `ToggleButton_Camera3` | 1 | 22 | 3 / 3 | `cam_tp_vertical`; 0..1; 1 |
| `ToggleButton_Camera4` | 1 | 23 | 3 / 4 | `cam_tp_horizontal`; 0..1; 1 |
| `ToggleButton_Camera5` | 1 | 5 | 1 / 5 | `npc_lock`; 0..1; 1 |
| `Slider_CameraView` | 1 | 24 | 3 / 5 | `cam_tp_fov`; 12..28; 18 |
| `Slider_CameraOffset` | 1 | 28 | 3 / 12 | `cam_tp_offset`; 0..12; 4 |
| `Slider_CameraTurn` | 1 | 36 | 3 / 24 | `cam_tp_turn`; 50..200; 100 |
| `Slider_LockOn` | 1 | 70 | 7 / 1 | `cam_tplock_limit`; 0..100; 0 |

The work-index to Lua group/key map is recorded in
`xivl-decomp:docs/script/desktop-user-config-reads.md:43-61`. The registered
records, ranges and defaults are recorded in
`xivl-client-structs:docs/user-config-store-contract.md:105-132,177-212,291-299`.
Those references identify request operands and registration defaults. They do
not prove that this widget changed a native record or that camera output
changed.

`reset` calls `desktopWidget:resetConfigWork` in this exact order:
`20, 21, 22, 23, 5, 24, 28, 36, 70`. It then calls `initControls` and
`desktopWidget:setDefaultCamera(false)`. `initControls` calls
`initToggleButton` for the five toggle controls in numeric order, then
`initSliderBar` for `Slider_CameraView`, `Slider_CameraOffset`,
`Slider_CameraTurn` and `Slider_LockOn`.
Each `desktopWidget` expression is a fresh global lookup. The sequence only
continues while each preceding lookup and native call returns normally; a
failure at a reset request leaves the failing request as the final observed
request and does not reach later reset IDs, `initControls` or
`setDefaultCamera`.

`processUICommandOperate` compares its control argument with three literals:

- `Button_AllClear` requests `desktopWidget:setDefaultCamera(false)`.
- `Button_Save` requests `desktopWidget:setDefaultCamera(true)`.
- `Button_Reset` requests
  `desktopWidget:openChildWidget("CommonAskWidget", self, true, nil, 1347,
  2, 1348, 1349)`. The raw `B=10` call has nine Lua arguments including its
  `desktopWidget` receiver, so eight explicit arguments follow the receiver;
  its fixed width is `(9,0)`.

Other control values take the empty branch. The widget does not itself prove
the ask widget's implementation or any completed reset/save operation.

`processUICommandToggleButton` resolves
`self:getControlUserWorkInt(1, control)` and requests
`desktopWidget:setConfigFlag(resolvedWorkIndex, value)`. It has no own result.

`processUICommandSliderChange` resolves the same slot. For the exact control
`Slider_CameraView`, it adds 18 to the supplied value. It reads
`desktopWidget:getConfigWork(resolvedWorkIndex)` and requests
`desktopWidget:setConfigWork(resolvedWorkIndex, value)` only when the adjusted
value is not equal to the read value. Other slider controls forward the value
unchanged. The source has no own return value.

`processAskResult` uses Lua equality with numeric `1`. Only numeric one calls
`reset(self)`; Boolean `true`, numeric zero, nil and other values do not.

`initSliderBar` resolves the work index and reads its config value. For the
exact `Slider_CameraView`, it subtracts 18 and clamps negative values to zero,
then calls `self:setValue(control, value)`. Other slider controls forward the
read value.

`initToggleButton` resolves the work index, captures the current
`self.setChecked` callable and its receiver, then requests
`desktopWidget:getConfigFlag(workIndex)` with open result width `(2,open)`. It
forwards the complete result tail to the captured callable with open argument
width `(open,0)`, preserving zero results and an explicit nil as distinct
finite inputs. A replacement of `self.setChecked` made during the getter does
not replace the captured callable used by this sequence.

There is no own apply, cancel, close or save method. Apply and close behavior
is bounded to the base conditions installed by `init`, the reset ask request,
and the numeric-one `processAskResult` continuation. The widget source does
not establish native storage, effective camera behavior, persistence, server
behavior or object lifetime. The existing camera consumer study likewise
leaves the upstream widget-to-camera producer unresolved
(`xivl-decomp:docs/actor/camera-input-chain.md:356-361,418-434`).

Configuration work edges:

- `init` writes slot/group 1 work indexes 20, 21, 22, 23, 5, 24, 28,
  36 and 70 at `root/proto0` PCs 56, 61, 66, 71, 76, 81, 86, 91 and 96.
  `processUICommandToggleButton` reads `(1, control)` at PC 3 and passes the
  result to `desktopWidget.setConfigFlag` at PC 8. Slider change reads the
  same slot at `root/proto5` PC 3, reads `desktopWidget.getConfigWork` at PC
  10, and conditionally requests `setConfigWork` at PC 17. Initialization
  reads the same slot before `getConfigWork`/`setValue` or
  `getConfigFlag`/captured `setChecked`. These are exact Lua request edges;
  They do not identify native storage or a camera consumer.

Default-camera request and reset edges:

- `Button_AllClear` and `Button_Save` reach
  `desktopWidget.setDefaultCamera(false)` and `(true)` at
  `root/proto3` PCs 6 and 14. `Button_Reset` reaches the full
  `openChildWidget` tuple at PC 29. A numeric-one ask result reaches
  `reset(self)` at `root/proto6` PC 3, whose reset sequence ends in
  `setDefaultCamera(false)` at `root/proto1` PC 41. These are request and
  continuation boundaries only; setter success, readback, apply and save are
  not joined to a completed native or disk outcome.

## Finite verification and limits

The bounded instruction-driven checks ran 29 typed cases: 25 ordinary cases
and 4 expected failures. They checked 287 raw call events, 291 typed literal
expectations and 116 receiver/callable identity controls. All nine own methods
were exercised through direct or nested calls. The cases covered the complete
initialization condition and work mapping, every reset ID and order, all three
operate branches plus no-op, numeric-one versus Boolean-true ask results,
toggle requests, view-slider addition and equal-value suppression, ordinary
slider writes, view initialization subtraction and zero clamp, numeric-string
addition, Boolean and nil arithmetic failures, zero-result and explicit-nil
toggle tails, a multi-result open tail, and replacement of `setChecked` after
capture. The checks also compared all nine `initControls` nested request
tuples, every getter request tuple and raw native callable owner, exact error
prefixes with no later requests, a reset-time global replacement, and the
save branch's exact one-request sequence. Twenty-one targeted corruptions were
rejected, including changed initialization and reset IDs, a Camera2-to-Camera1
request, group `1` to `999` getter substitutions, a foreign same-label
receiver, Boolean-to-number substitution, altered default-camera and slider
values, fresh or wrong-owner `setChecked` callables, injected save/reset
requests and an injected request after a reset failure.

The finite arithmetic model treats numeric values as numbers, accepts the
tested lexical numeric string `"5"` for the view-slider addition, and rejects
Booleans, nil and nonnumeric strings. This is a bounded test-model boundary,
not a universal Lua coercion or metamethod claim. Untested branches,
metamethod behavior, base-widget dispatch, connector behavior, native effects,
storage, persistence, rendering, server effects and complete lifetime remain
opaque.
