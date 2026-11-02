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
