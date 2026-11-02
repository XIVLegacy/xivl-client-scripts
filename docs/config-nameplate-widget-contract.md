# ConfigNamePlateWidget contract

`ConfigNamePlateWidget` is a bounded local configuration editor recovered from
the retail Lua chunk for `widget/confignameplatewidget`. It installs controls,
maps them to configuration work indexes, forwards local changes, requests a
restore sequence after a numeric ask result of `1`, and initializes control
values.
These requests do not establish rendered nameplate behavior, native success,
effective storage, persistence, server state, or widget lifetime.

## Evidence and reproduction

The source metadata revision is `65a5cefa6d7a130b4242723ae1707b5773867b74`.

| Item | Identity |
| --- | --- |
| Logical resource | `widget/confignameplatewidget` |
| Original LPB | `n1635q/7vw413w9x5uy9q5n1635q.le.lpb` |
| LPB | 4,600 bytes; SHA-256 `78ee61c4e0c405865c6b723335ad8066e11671d2790e34a142f91b32550f1c6e` |
| Decoded Lua 5.1 payload | 4,587 bytes; SHA-256 `a9d24dfb7bff1274355b85a5a4f3add109270d94a26ff4ae70d29829a73cfcb9` |
| Canonical LF decompile | 11,688 bytes; 518 lines; SHA-256 `e64fffd1dfa4e86d6284e15df7b281f22b1cbe332e447b260b150d362edffd56` |
| Decoder | `tools/retail_script.py`; 3,555 bytes; SHA-256 `765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391` |
| Unluac | `tools/vendor/unluac/unluac_2025_12_23.jar`; 796,256 bytes; SHA-256 `98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc` |

Reproduce the payload and canonical source with the repository decoder. The
retail client root and scratch directory are caller-supplied:

```text
python tools/retail_script.py --input <retail-client-script-root>/n1635q/7vw413w9x5uy9q5n1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/confignameplatewidget.luac --script-out <scratch>/confignameplatewidget.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/confignameplatewidget.disasm <scratch>/confignameplatewidget.luac
```

The wrapper authenticates the whole decoded payload by its pinned SHA-256. The
static checker then pins the admitted prototype windows, selected literal CALL
words and widths, RETURN words, and guard destinations. Its finite checks
execute the authenticated payload prototypes with typed native stubs, original
own closures for nested calls, and actual receiver and callable object identity.
The checker is a bounded Lua control-flow oracle, not a universal Lua simulator.

The public reproduction commands above produce the decoded source and unluac
disassembly. The finite checker and its fixtures are separate local evidence;
those public commands do not ship or invoke them.

## Root binding

The root has 41 words at byte offset 32 and 11 child prototypes. Root calls are
`PC 2 / byte 40 / 0x0100401C / width 1,0` for
`require("/Widget/WidgetBaseClass")` and
`PC 6 / byte 56 / 0x0180401C / width 2,0` for
`_defineClass("ConfigNamePlateWidget", "WidgetBaseClass")`.

The following root assignments are binding attempts. They do not prove that a
class table or runtime widget owner completed.

| Method | Closure source line | Prototype | Assignment source line |
| --- | ---: | --- | ---: |
| `init` | 11 | `root/proto0` | 203 |
| `update` | 206 | `root/proto1` | 270 |
| `reset` | 273 | `root/proto2` | 355 |
| `processUICommandOperate` | 358 | `root/proto3` | 381 |
| `processUICommandSelection` | 384 | `root/proto4` | 399 |
| `processUICommandToggleButton` | 402 | `root/proto5` | 417 |
| `processUICommandSliderChange` | 420 | `root/proto6` | 442 |
| `initToggleButton` | 445 | `root/proto7` | 463 |
| `initSliderBar` | 466 | `root/proto8` | 485 |
| `initComboBox` | 488 | `root/proto9` | 506 |
| `processAskResult` | 509 | `root/proto10` | 518 |

## Method windows and original words

The source windows below are inclusive canonical LF source lines. Each row also
gives the prototype code offset and instruction count. A call locator is
`PC / byte / word / args,results`; `open` means the raw B or C width is zero.
For compact repeated rows, every listed PC has the same literal word and
width. Every CALL in the admitted prototypes is a CALL; no TAILCALL occurs.
Every method has exactly one `RETURN` with word `0x0080001E`.

| Method | Source window; prototype | Code offset; instruction count; CALL locators | RETURN |
| --- | --- | --- | --- |
| root | 1-8 plus noncontiguous bindings 11,203,206,270,273,355,358,381,384,399,402,417,420,442,445,463,466,485,488,506,509,518; `root` | 32; 41; 2/40/`0x0100401C`/1,0; 6/56/`0x0180401C`/2,0 | 40/192/`0x0080001E` |
| `init` | 11-201; `root/proto0` | 574; 153; PCs 3,7,11,15,19,23,27,31,35,39,43,47,51,55,59 / words `0x0200405C` / 3,0; PC 62 / `0x0180405C` / 2,0; PCs 64,66 / `0x0100405C` / raw B=2,C=1, zero explicit args; PC 69 / `0x0180405C` / 2,0; PC 151 / `0x0100405C` / raw B=2,C=1; PCs 74,79,84,89,94,99,104,109,114,119,124,129,134,139,144,149 / `0x0280405C` / 4,0. Byte is `574 + 4*PC`. | 152/1182/`0x0080001E` |
| `update` | 206-268; `root/proto1` | 2082; 46; PCs 2,5,8,11,14,17,20,23,26,29,32,35,38,41,44 / `0x0180405C` / 2,0. Byte is `2082 + 4*PC`. | 45/2262/`0x0080001E` |
| `reset` | 273-353; `root/proto2` | 2762; 63; PCs 3,7,11,15,19,23,27,31,35,39,43,47,51,55,59 / `0x0180405C` / 2,0; PC 61 / `0x0100405C` / 1,0. Byte is `2762 + 4*PC`. | 62/3010/`0x0080001E` |
| `processUICommandOperate` | 358-379; `root/proto3` | 3241; 18; PC 13/3293/`0x0500419C`/9,0. | 17/3309/`0x0080001E` |
| `processUICommandSelection` | 384-397; `root/proto4` | 3468; 10; PC 3/3480/`0x0200815C`/3,1; PC 8/3500/`0x0200419C`/3,0. | 9/3504/`0x0080001E` |
| `processUICommandToggleButton` | 402-415; `root/proto5` | 3622; 10; PC 3/3634/`0x0200819C`/3,1; PC 8/3654/`0x020041DC`/3,0. | 9/3658/`0x0080001E` |
| `processUICommandSliderChange` | 420-440; `root/proto6` | 3776; 16; PC 3/3788/`0x0200819C`/3,1; PC 7/3804/`0x018081DC`/2,1; PC 14/3832/`0x0200421C`/3,0. | 15/3836/`0x0080001E` |
| `initToggleButton` | 445-463; `root/proto7` | 3973; 12; PC 3/3985/`0x0200809C`/3,1; PC 9/4009/`0x0180019C`/2,open; PC 10/4013/`0x000040DC`/open,0. | 11/4017/`0x0080001E` |
| `initSliderBar` | 466-485; `root/proto8` | 4151; 13; PC 3/4163/`0x0200809C`/3,1; PC 7/4179/`0x018080DC`/2,1; PC 11/4195/`0x0200411C`/3,0. | 12/4199/`0x0080001E` |
| `initComboBox` | 488-506; `root/proto9` | 4331; 12; PC 3/4343/`0x0200809C`/3,1; PC 9/4367/`0x0180019C`/2,open; PC 10/4371/`0x000040DC`/open,0. | 11/4375/`0x0080001E` |
| `processAskResult` | 509-516; `root/proto10` | 4515; 5; PC 3/4527/`0x0100409C`/1,0. | 4/4531/`0x0080001E` |

The root source has fresh `ConfigNamePlateWidget` lookups at lines
`9,204,271,356,382,400,418,443,464,486,507`; each method assignment freshly
resolves that table before targeting the closure. A later rebind can therefore
change a subsequent assignment target. The closure and assignment source lines
remain the noncontiguous pairs listed in the root binding table above.

The guard words and destinations are exact original words: `root/proto3` PC 1
`EQ 0x02C00017` compares parameter 2 with `"Button_Reset"`; PC 2
`JMP 0x80034016` reaches PC 17 on the false path, and PCs 14, 15 and 16
also reach PC 17. `root/proto6` PC 8 is `EQ 0x0281C057` for the strict
slider inequality and PC 9 `JMP 0x80010016` reaches PC 15 when equal.
`root/proto10` PC 0 is `EQ 0x00C00017` for numeric `1`; PC 1
`JMP 0x80004016` reaches PC 4 for the false path.

## Local control contract

`init` installs `self:setModal(true)`, a confirm condition for
`Button_Reset`, cancel and close condition requests, and
`setHelpParameter("TextBlock_Title", 1, 77418)`. It installs
`UILuaCommands.ToggleButton` for the 14 toggle controls and
`UILuaCommands.SliderValueChanged` for `Slider_NamePlatePos`:

The cancel and close requests are exact zero-argument dynamic calls:
`self:setCancelCondition()` at init PC 64 and `self:setCloseCondition()` at
init PC 66. Each raw CALL has receiver-inclusive `B=2` and discarded-result
`C=1`; these requests do not prove callable or base ownership or handler
effects.

| Control | Work index | Lua group/key | Registered record; range; default |
| --- | ---: | ---: | --- |
| `ToggleButton_NamePlate` | 26 | 3 / 7 | `name_plate`; 0..1; 1 |
| `Slider_NamePlatePos` | 73 | 7 / 4 | `name_plate_offset`; -30..30; 0 |
| `ToggleButton_NameIcon_1` | 74 | 7 / 5 | `name_plate_player_name`; 0..1; 1 |
| `ToggleButton_HPbar_1` | 75 | 7 / 6 | `name_plate_player_hp`; 0..1; 1 |
| `ToggleButton_NameIcon_2` | 76 | 7 / 7 | `name_plate_party_name`; 0..1; 1 |
| `ToggleButton_HPbar_2` | 77 | 7 / 8 | `name_plate_party_hp`; 0..1; 1 |
| `ToggleButton_NameIcon_3` | 78 | 7 / 9 | `name_plate_other_name`; 0..1; 1 |
| `ToggleButton_HPbar_3` | 79 | 7 / 10 | `name_plate_other_hp`; 0..1; 1 |
| `ToggleButton_NameIcon_4` | 80 | 7 / 11 | `name_plate_npc_name`; 0..1; 1 |
| `ToggleButton_NpcHPbar` | 85 | 7 / 16 | `name_plate_npc_hp`; 0..1; 1 |
| `ToggleButton_EnemyName` | 81 | 7 / 12 | `name_plate_enemy_name`; 0..1; 1 |
| `ToggleButton_EnemyHPbar` | 82 | 7 / 13 | `name_plate_enemy_hp`; 0..1; 1 |
| `ToggleButton_ActiveIcon` | 31 | 3 / 16 | `enemy_rank`; 0..1; 1 |
| `ToggleButton_EnemyLevel` | 30 | 3 / 15 | `name_plate_hp_type`; 0..1; 1 |
| `ToggleButton_Hostile` | 35 | 3 / 23 | `hate_info`; 0..1; 1 |

The work-index map is the 68-entry map in
`xivl-decomp:docs/script/desktop-user-config-reads.md:47-58`. The store names,
ranges and constructor defaults are in
`xivl-client-structs:docs/user-config-store-contract.md:181-205,291-313`.
These references identify requested operands and defaults; they
do not prove that a native record changed or that rendering consumed it.

`update` initializes the 14 toggle controls in the table order shown above,
with `ToggleButton_NpcHPbar` before `ToggleButton_EnemyName` and
`ToggleButton_EnemyHPbar`; `Slider_NamePlatePos` is initialized last by
`initSliderBar`.
`initToggleButton` resolves `(slot=1, control)` to a work index, captures the
current raw `self.setChecked` callable and frame receiver, then requests
`desktopWidget:getConfigFlag(workIndex)` with open result width. It forwards
the complete result tail to the captured callable as
`setChecked(control, ...)`, preserving zero results and an explicit nil.
`initSliderBar` requests one fixed result from `getConfigWork`, then loads
`self.setValue` and calls `setValue(control, value)`. `initComboBox` captures
`self.setSelectedIndex` before requesting `getConfigWork` with open result
width, then forwards its complete tail to the captured callable as
`setSelectedIndex(control, ...)`.

`reset` freshly loads global `desktopWidget` for each
`resetConfigWork` request, in this exact order:
`26, 73, 74, 75, 76, 77, 78, 79, 80, 85, 81, 82, 31, 30, 35`, then calls
`update`. An ordinary error at any reset request stops the sequence at that
request and does not reach later IDs or `update`.

`processUICommandOperate` compares its third argument with the exact string
`"Button_Reset"`. A match requests
`desktopWidget:openChildWidget("CommonAskWidget", self, true, nil, 1347, 2,
1348, 1349)`, with raw call width 9,0 including the receiver. Other controls
take the empty branch.

`processUICommandSelection` resolves the work index and requests
`desktopWidget:setConfigWork(workIndex, value)`. With self included as `A0`,
the third positional argument `A2` is the control and the fourth `A3` is the
value forwarded to `setConfigWork`. `processUICommandToggleButton` similarly requests
`desktopWidget:setConfigFlag(workIndex, value)` from its sixth argument.
`processUICommandSliderChange` resolves the work index, reads
`desktopWidget:getConfigWork(workIndex)`, and freshly loads global
`desktopWidget` again for the `setConfigWork` request. It requests that write
only when the supplied sixth argument is not strictly equal to the read value.
The comparison is Lua equality; numeric `0` and string `"0"`, and numeric `1`
and Boolean `true`, remain distinct in the finite checks. Integer and floating
representations of a Lua number share the numeric kind.

`processAskResult` calls `reset(self)` only when its second argument is the
number `1`. Boolean `true`, numeric `0`, nil and other values do not continue.
The reset ask, cancel and close condition requests, setter requests, and getter
requests are local boundaries. The source has no own refusal-result
branch and makes no notification request. It installs cancel and close
condition requests, but their dispatch and effects are opaque. It has no
separate direct apply, save, render, or completion request in these own methods;
downstream effects remain unknown. Reset is the only local restore request, and
it is a request sequence rather than proof of a successful native restore.

## Verification and limits

The independent checker ran 19 typed cases, 11 semantic corruption controls,
and 3 separate static guard mutations (14 controls total). It checked 87
selected original CALL words, 12 RETURN words, 9 guard words and destinations,
all 11 method windows, and 12 prototypes. Finite cases covered initialization
and reset nesting, every reset ID and order, the reset ask request and no-op,
all operate/selection/toggle/slider paths, equal-value suppression,
numeric-string forwarding, zero-result and explicit-nil toggle tails,
multiple-value combo tails, reset and slider global rebinds, toggle capture,
combo capture, slider post-getter callable lookup, raw receiver and callable
identity, and an ordinary error prefix. Each semantic corruption control had
an unchanged passing baseline and rejected a wrong receiver, stale snapshot,
fresh callable, Boolean-versus-numeric slot, altered work index, or altered
reset global. Each static mutation was rejected separately; the whole-payload
SHA check is distinct from these selected word checks.

The bounded execution covers only the typed values and call sequences named above.
Metamethods, arbitrary Lua coercion, base-widget dispatch, native implementation
and result production, control rendering, file contents, persistence, server
effects and complete lifetime remain opaque or unvisited. The store contract's
getter bounds and nil behavior are native reference facts, not additional
claims about this widget's runtime handling.

The decompiler's local register names and source labels are presentation, not
independent semantic identifiers. Original bytecode prototype, PC, word,
width and jump locators are the static authority. In particular, source-level
multiple assignment around `initComboBox` corresponds to an open native result
and an open following call; the finite checks retain zero, nil and multiple
result tails instead of inferring a single scalar.
