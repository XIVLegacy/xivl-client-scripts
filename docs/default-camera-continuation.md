# DesktopWidget default-camera continuation

`DesktopWidget.setDefaultCamera` requests one desktop command and returns no Lua
values locally. A strict Boolean `true` requests
`RaptureCommands.TPSCameraMemorize`; every other tested value requests
`RaptureCommands.TPSCameraInitialize`.

## Local request contract

The closure is the direct child `root/proto483` of the registered
`widget/desktopwidget_connector` resource. Its code starts at decoded offset
191873, contains 10 words through exclusive offset 191913, and has code SHA-256
`a572156428467f9af8a6cf607297c3b546882061e2c06eb3a54cd1f22efec0fd`. The
canonical LF binding window is
`widget/desktopwidget_connector.lua:23419-23437`; the function body is at
lines 23422-23435. These are canonical decompile line locators, not the
bytecode debug line-defined values.

| PC | Instruction | Local contract |
| ---: | --- | --- |
| 0 | `EQ R1, K0(true)` | Strictly selects the memorize branch only for Boolean `true`. |
| 1 | `JMP -> 6` | Routes all other values to initialization. |
| 2 | `SELF R2, R0, K1("sendDesktopCommand")` | Performs a fresh receiver lookup and captures the callable in `R2`; `R3` receives the same receiver. |
| 3 | `LOADK R4, K2("RaptureCommands.TPSCameraMemorize")` | Loads the true-branch command. |
| 4 | `CALL R2, B=3, C=1` | Calls with two Lua arguments, receiver then command, and observes zero results. |
| 5 | `JMP -> 9` | Skips the initialization branch after a normal memorize request. |
| 6 | `SELF R2, R0, K1("sendDesktopCommand")` | Performs the corresponding fresh lookup for the other branch. |
| 7 | `LOADK R4, K3("RaptureCommands.TPSCameraInitialize")` | Loads the other-branch command. |
| 8 | `CALL R2, B=3, C=1` | Calls with two Lua arguments, receiver then command, and observes zero results. |
| 9 | `RETURN B=1` | Returns zero Lua values. |

The selected branch performs exactly one `sendDesktopCommand` lookup and one
call when the lookup succeeds. The `SELF` result is captured before the call;
a replacement of the receiver member after lookup does not replace the
captured callable. The call and return widths have fixed, closed tails: there
is no open result tail and no explicit returned `nil`.

## sendDesktopCommand request boundary

The root bytecode contains a `WidgetBaseClass.sendDesktopCommand` binding
attempt for the logical `widget/widgetbaseclass_common` script. This root
assignment does not establish that a runtime receiver lookup executes the
closure or that the lookup succeeds. The installed connector input is
`client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb`, 32996 bytes with SHA-256
`c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c`. Its
decoded Lua 5.1 payload is 32983 bytes with SHA-256
`7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f`; the
canonical LF decompile is 69077 bytes, 3361 lines, with SHA-256
`2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f`.

The root registration witnesses are GETGLOBAL pc 153 at offset 644,
CLOSURE pc 154 at offset 648 for child 51, and SETTABLE pc 155 at offset 652
with the literal key `sendDesktopCommand`. The selected child is
`root/proto51`, code offset 16642 through exclusive offset 16666, six words
and 24 bytes, with code SHA-256
`f009526a598433a49f91f381668c6b6bef7007aaa75084f8ab81bf19468bb9a5`. The
canonical binding window is `widget/widgetbaseclass_common.lua:1240-1252`,
with the function body at lines 1242-1250.

Its bounded local request is:

| PC | Instruction | Request contract |
| ---: | --- | --- |
| 0 | `SELF R2, R0, K0("_sendStoryboardCommand")` | Looks up the helper on the receiver and captures the callable; `R3` receives the same receiver. |
| 1 | `LOADNIL R4` | Supplies an explicit nil second argument. |
| 2 | `LOADK R5, K1("")` | Supplies an empty string third argument. |
| 3 | `MOVE R6, R1` | Forwards the method's caller argument as the fourth argument. |
| 4 | `CALL R2, B=5, C=1` | Calls with four arguments, including self, and observes zero results. |
| 5 | `RETURN B=1` | Returns zero Lua values. |

Therefore the earlier `setDefaultCamera` result can join this wrapper only if
proto483's `sendDesktopCommand` `SELF` lookup completes normally and resolves
to the admitted `root/proto51` closure. Proto483 then attempts its separate
two-argument `CALL` `(self, command)`; its continuation and zero-result return
require that call to complete normally. The admitted proto51 closure separately
performs its `_sendStoryboardCommand` `SELF` lookup. Only after that inner
lookup returns normally does proto51 attempt the four-argument `CALL`
`(self, nil, "", command)`; actual helper invocation requires a callable
result, and the outer zero-result return likewise requires normal inner
completion. The helper body, runtime lookup success, native delivery, effective
camera or store changes, readback, disk completion, server behavior, and object
lifetime remain unproved.

The closest published native route says `_sendStoryboardCommand` jumps through
receiver vftable slot `+0x94` to `0x006EBF30` for both `WidgetBase` and
`DesktopWidget`; its documented pickup selection depends on the argument
types, and unsupported combinations send nothing
([xivl-client-structs:docs/boot-native-call-contract.md:160-166](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/boot-native-call-contract.md#L160-L166)). A separate input-boundaries
analysis describes the native wrapper's cells and downstream calls, but
explicitly leaves the `_sendStoryboardCommand_cpp` registration to
`0x006EBF30` unproved
([xivl-client-structs:docs/native-input-ui-boundaries.md:1926-1950](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/native-input-ui-boundaries.md#L1926-L1950)). These facts do not prove that the Lua member lookup resolves to that native callback. The closest published camera facts remain the
`RaptureCommands` handling and conditional `TPSCameraInitialize` writes/events
([xivl-decomp:docs/actor/camera-input-chain.md:203-216](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/camera-input-chain.md#L203-L216)); they do not close the Lua-to-native bridge.

The tested typed inputs were Boolean `true`, Boolean `false`, numeric `1`,
numeric `0`, explicit `nil`, and the string `"true"`. Only Boolean `true` took
the memorize path. In the bounded Lua 5.1 path, a missing table member leaves
`SELF`'s callable as nil when a plain table has no member and no
fallback; the reachable `CALL` then raises the nil-call error before the later
jump or return. A metatable or `__index` fallback could resolve a callable and
is outside this bounded proof. A helper failure after the reachable `CALL`
preserved the lookup and call prefix and did not reach the later jump or
return.

## Caller boundary and limits

The camera widget requests `setDefaultCamera(false)` for All Clear and
`setDefaultCamera(true)` for Save; reset reaches the false request after its
reset sequence. These are local request boundaries only
([xivl-client-scripts:docs/config-camera-widget-contract.md:120-143](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/docs/config-camera-widget-contract.md#L120-L143)).
The widget contract does not establish native success, camera application,
readback, persistence, server behavior, rendering, or object lifetime
([xivl-client-scripts:docs/config-camera-widget-contract.md:172-201](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/docs/config-camera-widget-contract.md#L172-L201)).

The registered resource identity and logical source path are recorded in the
tracked registry
([xivl-client-scripts:lua/registry.json:40893-41156](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/lua/registry.json#L40893-L41156)).

The connector LPB is
`n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, 213487 bytes with SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`. Its
decoded Lua 5.1 payload is 213474 bytes with SHA-256
`685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`; the
canonical LF decompile is 660617 bytes with SHA-256
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`.
The decoder is pinned to `tools/retail_script.py` SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391` and
`tools/vendor/unluac/unluac_2025_12_23.jar` SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
The structural parser is `tools/build_quest_contracts.py` SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`.
The caller widget has a different LPB identity; its evidence cannot pin this
connector resource.

The root registration identifies a Lua binding attempt. Runtime continuation is
conditional on the receiver lookup resolving this closure; the
`sendDesktopCommand` edge is a source/helper lookup, not native attribution.

## Reproduction

Use the pinned public decoder and decompiler with caller-selected paths:

```text
python tools/retail_script.py --input <retail-lpb> --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <decoded.lua51> --script-out <canonical.lua>
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <disassembly.txt> <decoded.lua51>
```

The finite typed executions and identity/corruption controls are separate local
evidence. They do not form part of the public reproduction command and do not
expand the native, storage, or persistence boundary.
