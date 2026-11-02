# AddressListSubWidget local interaction contract

The AddressListSubWidget contract records the local interaction recovered from
one authenticated retail Lua 5.1 resource. It covers the root bindings, all 13 declared own
methods, and their contained code. It does not establish form implementation,
native effects, social mutation, server acceptance, persistence, rendering, or
object lifetime.

## Identity and source proof

- Resource coordinate: `n1635q/966s5rry1rqrp8n1635q.le.lpb` under the
  installed `client/script` tree.
- Original LPB: 5,379 bytes, SHA-256
  `E725869B2344821433231E4B56A55CC27946CFA2B57649638532AAD69DBD2763`.
- Decoded Lua 5.1 payload: 5,366 bytes, SHA-256
  `A71DB0AF74EB5C0176B1DA17304E73C8271BF7B7C9582D53C6B56EE7413E46FA`.
- Canonical LF decompile:
  `xivl-client-scripts:lua/scripts/widget/addresslistsubwidget.lua`, 13,942
  bytes, 645 LF lines, SHA-256
  `B7539F838EA073200D3092EDB84915D97260AC5399E505EE2146EA7DA9864DF4`.
- The canonical path, size, hash, and line count are pinned by
  `xivl-client-scripts:manifests/scripts.json:14853-14856`; the matching LPB
  and payload are pinned by
  `xivl-client-scripts:manifests/retail_lua_coverage.json:26006-26010`.
- Decoder/product route:
  `xivl-client-scripts:tools/retail_script.py`, SHA-256
  `765327CF3DA90AACF8E36B185CE53AA0615F7705E9F9CCDC3A7243E3B6C0C391`.
  Decompiler:
  `xivl-client-scripts:tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256
  bytes, SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
- Static Lua 5.1 instruction parsing used
  `xivl-client-scripts:tools/build_quest_contracts.py`, pinned at SHA-256
  `A24FED11BEE2E52B45513E49F37F3118226CD561227A8F44CAF7F0A7D8CB9956`.

The selected call sidecar identifies class `AddressListSubWidget` and the
three recovered API names at
`xivl-client-scripts:lua/scripts/widget/addresslistsubwidget.calls.json:1-19`.
The registry row records the same class and 13-method list at
`xivl-client-scripts:lua/registry.json:38384-38409`.

## Root bindings

The root prototype starts at decoded offset 32 and contains 47 instructions.
At PC 2 / offset 40, `CALL A=0 B=2 C=1` has raw word `0x0100401c` and calls
`require` with `/Widget/WidgetBaseClass`, discarding results. At PC 6 / offset
56, `CALL A=0 B=3 C=1` has raw word `0x0180401c` and calls `_defineClass` with
`AddressListSubWidget` and `WidgetBaseClass`, discarding results.

Each binding below is a separate `GETGLOBAL AddressListSubWidget`,
`CLOSURE`, and `SETTABLE` sequence. `B` on `SETTABLE` selects the literal
method key; the closure child index is the method's prototype.

| child | method | CLOSURE PC / offset / word | SETTABLE PC / offset / word | key |
|---:|---|---|---|---|
| 0 | `init` | 8 / 64 / `0x00000064` | 9 / 68 / `0x82804009` | `K5=init` |
| 1 | `setMode` | 11 / 76 / `0x00004064` | 12 / 80 / `0x83004009` | `K6=setMode` |
| 2 | `setPartyEnable` | 14 / 88 / `0x00008064` | 15 / 92 / `0x83804009` | `K7=setPartyEnable` |
| 3 | `setFocus` | 17 / 100 / `0x0000c064` | 18 / 104 / `0x84004009` | `K8=setFocus` |
| 4 | `processBeforeShow` | 20 / 112 / `0x00010064` | 21 / 116 / `0x84804009` | `K9=processBeforeShow` |
| 5 | `processUICommandCancel` | 23 / 124 / `0x00014064` | 24 / 128 / `0x85004009` | `K10=processUICommandCancel` |
| 6 | `processUICommandOperate` | 26 / 136 / `0x00018064` | 27 / 140 / `0x85804009` | `K11=processUICommandOperate` |
| 7 | `openPartyDialog` | 29 / 148 / `0x0001c064` | 30 / 152 / `0x86004009` | `K12=openPartyDialog` |
| 8 | `openDeleteDialog` | 32 / 160 / `0x00020064` | 33 / 164 / `0x86804009` | `K13=openDeleteDialog` |
| 9 | `sendTellFormat` | 35 / 172 / `0x00024064` | 36 / 176 / `0x87004009` | `K14=sendTellFormat` |
| 10 | `setSubWindowOperation` | 38 / 184 / `0x00028064` | 39 / 188 / `0x87804009` | `K15=setSubWindowOperation` |
| 11 | `ignoreFamilyName` | 41 / 196 / `0x0002c064` | 42 / 200 / `0x88004009` | `K16=ignoreFamilyName` |
| 12 | `setParentBorder` | 44 / 208 / `0x00030064` | 45 / 212 / `0x88804009` | `K17=setParentBorder` |

## Own-method and original-word coverage

`source LF` is the canonical decompile window. `debug span` is the original
prototype line span and is kept separate from source line numbering. Code
offsets and instruction counts are absolute decoded-chunk facts.

| method | source LF | prototype | debug span | arity | stack | code offset | instructions | direct-call PCs |
|---|---:|---|---:|---:|---:|---:|---:|---|
| `init` | 11-81 | `root/proto0` | 53-82 | 5 | 12 | 625 | 52 | 19,22,25,28,31,34,38,44,47,50 |
| `setMode` | 84-306 | `root/proto1` | 93-180 | 5 | 20 | 1160 | 197 | 14,24,28,32,36,48,52,56,61,68,72,76,78,86,90,94,105,109,113,120,124,131,135,140,144,148,155,159,167,169,191,195 |
| `setPartyEnable` | 309-368 | `root/proto2` | 188-210 | 2 | 6 | 2398 | 49 | 7,12,16,21,25,34,41 |
| `setFocus` | 371-391 | `root/proto3` | 218-225 | 2 | 5 | 2871 | 16 | 6,9,14 |
| `processBeforeShow` | 394-414 | `root/proto4` | 237-245 | 2 | 5 | 3084 | 16 | 7,11 |
| `processUICommandCancel` | 417-429 | `root/proto5` | 256-259 | 5 | 8 | 3274 | 8 | 1,5 |
| `processUICommandOperate` | 432-469 | `root/proto6` | 270-299 | 5 | 8 | 3409 | 32 | 2,6,15,20,25,29 |
| `openPartyDialog` | 472-509 | `root/proto7` | 310-325 | 1 | 10 | 3808 | 34 | 1,3,17,27,31 |
| `openDeleteDialog` | 512-553 | `root/proto8` | 336-355 | 1 | 11 | 4209 | 38 | 7,9,23,31,35 |
| `sendTellFormat` | 556-571 | `root/proto9` | 363-368 | 1 | 6 | 4625 | 10 | 1,3,7 |
| `setSubWindowOperation` | 574-611 | `root/proto10` | 377-389 | 3 | 8 | 4786 | 27 | 1,7,13,17,19,21,25 |
| `ignoreFamilyName` | 614-629 | `root/proto11` | 397-404 | 1 | 4 | 5117 | 11 | 1,5 |
| `setParentBorder` | 632-645 | `root/proto12` | 411-416 | 1 | 5 | 5255 | 8 | 1,6 |

Each direct-call PC above maps to decoded offset `code offset + 4*PC` in the
named prototype. The 86 selected words include every CALL and TAILCALL in the
13 own-method windows; direct opcodes, raw words, A/B/C fields, and fixed or
open widths are reproduced with the disassembly command below. No contained
closure is present in these own-method windows.

Lua 5.1 uses `B=argument count+1` and `C=result count+1`; `B=0` or `C=0`
means an open width. `setMode` requests two `getAddressName` results (`C=3`),
while dialogs and `sendTellFormat` request one name result (`C=2`).
`_getParentWidget` is a one-result request (`C=2`), `openChildWidget` is a
fixed one-result request (`C=2`), `C=1` requests zero results, and
`closeWidgetDirect` and `setTellAddress` are open tails (`C=0`) at the
forwarding sites. `setSubWindowOperation` PC 25 instead issues
`closeWidgetDirect` as `CALL C=1`, requesting it while discarding its results.

## Local behavior

The parent contract remains the accepted source for opening this child and for
the parent list's mode and party-enable inputs:
`xivl-client-scripts:docs/address-list-widget-contract.md:90,106-107`.
The contract adds only the child's own local requests and state transitions.

### Initialization and mode

`init(self, mode, index, parent, partyEnable)` creates
`work._temp = { {"mode", "integer8"}, {"error", "boolean"},
{"party", "integer8"} }`, sets `work.error=false`, registers local cancel and
the Tell, Letter, Party, Delete, and Close confirmation controls, sets the
Close content id to 1230, delegates the supplied four values to `setMode`,
then requests modal and drag state true. It has zero explicit results.

`setMode` stores a non-nil mode or zero, requests `Margin="0,0,0,0"`, and
branches on exact mode 1. Mode 1 sets `work.party=0`, hides Tell, Letter, and
Party, and uses top/left offsets 20 and 40. Other modes set `work.party=2`,
show Tell and Party, hide Letter, and use offsets 0 and 80. It reads the
parent's captured `getAddressName` result. A nil, zero, or empty first result
marks `work.error=true` and disables the applicable Tell, Party, and Delete
controls; otherwise Delete is enabled. In non-mode-1 paths, a nil or zero
second result disables Tell and Party while retaining Delete. The two returned
values are captured from this call and reused by the branch; no fresh parent
name call is made within the branch. The `parent` parameter is the supplied A3
object for this method and is not assumed equal to a later
`self:_getParentWidget()` result. A non-nil party-enable input is delegated to
`setPartyEnable`. `work.error` is sticky after this method marks it true:
later valid `setMode` calls do not clear it, so a subsequent before-show can
still request this widget's close.

When an index is supplied, `setMode` reads the parent's window position and
both desktop and child window sizes, evaluates its fixed offset/threshold
tests, and requests `Top` and `Left`. For a concrete original-word case with
parent position `(180,100)`, index `1`, mode `2`, child size `300x500`, and
desktop size `800x600`, the requested values are exactly `Left=600` and
`Top=100`; these are fixed calculations, not generic child-size centering or
adjustment. These are local property requests; no rendered position is claimed.

`setPartyEnable(nil)` sets party to zero and hides Party. The guard is exact:
only nil and Boolean false take the disabled path; numeric zero is truthy and
enables Party. A false value shows
Party, moves focus from Party to Delete when needed, disables Party, requests
`(desktopWidget.closeChildWidget, desktopWidget, "AddressListNamingWidget",
self)` when the prior local party value exceeds two, and stores party 1. A true
value enables Party and raises a local party value below two to 2.

### Focus, commands, dialogs, and close paths

`setFocus` ignores nil and empty controls. Otherwise it requests
`setLogicalFocus(control)`, reads the full raw tuple
`(desktopWidget._getKeyboardFocusedWidget, desktopWidget)`,
and requests `setKeyboardFocusedControl(control)` only when Lua equality holds
between the returned object and this receiver. A metatable `__eq` effect is
possible under Lua equality but is not established by this source.

`processBeforeShow` tests exact Boolean true. On a non-true input with
`work.error=true`, it requests `setParentBorder` and open-tail forwards
`(desktopWidget.closeWidgetDirect, desktopWidget, self)`. Otherwise it returns
one local true.
`processUICommandCancel` always requests `setParentBorder`, then open-tail
forwards `(desktopWidget.closeWidgetDirect, desktopWidget, self)`.

`processUICommandOperate` first requests `setFocus(command)`. Exact commands
tail-forward Tell to `sendTellFormat`, return nil for Letter, tail-forward
Party to `openPartyDialog`, tail-forward Delete to `openDeleteDialog`, and set
the parent border before open-tail forwarding Close to
`(desktopWidget.closeWidgetDirect, desktopWidget, self)`. Other command values
have no explicit result.

`openPartyDialog` obtains the parent name and, for a value not equal to false,
the empty string, or zero, requests the full raw tuple
`(desktopWidget.openChildWidget, desktopWidget,
"AddressListNamingWidget", self, true, 4, name)`. Nil is not rejected by
these exact Lua comparisons. A non-nil child result stores local party 3 and
returns that result; a nil child result returns zero values. The name argument
is the captured result from the one parent call, not a fresh parent read. The
invalid-name path marks error, sets the parent border, and open-tail forwards
`(desktopWidget.closeWidgetDirect, desktopWidget, self)`; its close results
are returned unchanged.

`openDeleteDialog` chooses naming mode 2 for local mode zero and 3 otherwise.
It makes the same name guard and requests the full raw tuple
`(desktopWidget.openChildWidget, desktopWidget,
"AddressListNamingWidget", self, true, namingMode, name)`. A non-nil result is
returned and a nil child result produces zero results; the name is the
captured result from the one parent call. Invalid input sets error, sets the
parent border, and open-tail forwards the full close tuple above, preserving
its result tail.

`sendTellFormat` forwards the parent's `getAddressName` result to the full raw
tuple `(desktopWidget.setTellAddress, desktopWidget, name)` as an open tail;
it forwards the captured name from that call without refreshing the parent
and preserves every result in the Tell tail. `setSubWindowOperation`
forwards supplied operation values to the parent when present. For exact 21 it
disables Tell and Delete and hides this widget; it then sets the parent border
and requests this widget's close for every operation value. `ignoreFamilyName` returns
the parent's result when a parent exists and literal zero otherwise.
`setParentBorder` requests parent `setBorder(-1)` when a parent exists and has
no explicit result; the raw request is
`(parent.setBorder, parent, -1)`.

These are local request/result boundaries. A `desktopWidget` or parent
callable returning a value does not establish what a native consumer, form,
social store, server, or lifetime manager did with it.

## Finite original-word execution

A bounded finite check executed the original decoded words with actual frame
objects, raw argument-zero receivers, callable owners, and callable identities
for own methods; parent, desktop, and base methods were typed mocks. The 34
cases cover initialization, both mode families, party-enable nil/false/true/
numeric-zero, focus match/empty, show error/no-error, sticky error reuse,
cancel, Tell/Letter/Close commands, party and delete dialog paths, nil child
results, invalid-name close tails, captured-name forwarding, supplied/native
parent mismatch, fixed coordinate calculations, both sub-window operations,
parent/no-parent family-name results, parent border, and zero/nil/multiple
Tell and close tails.

The passing run visited 411 of 498 own-method instructions (82.5 percent) and
visited every own method. It did not claim branch-complete execution. Static
only or unvisited cases include the valid mode-1 name path, nil/empty
non-mode-1 names, the alternate party threshold, focus nil and keyboard-widget
mismatch, dispatcher Party/Delete branches, alternate dialog modes, and
parent-absence paths for sub-window and border operations. Eleven negative
controls rejected a mutated decoded payload hash, a mutated direct-call width,
a same-label wrong raw desktop receiver, an `openChildWidget` callable clone
with the same owner/name, an outgoing child naming-mode operand of 99, name
Eve, both Boolean/numeric swaps, malformed Boolean arithmetic, unsupported
numeric-string index coercion, and Tell-tail truncation.

The finite check distinguished the child receiver, the parent receiver, and
the global `desktopWidget` receiver, retained raw receiver/callable objects
through assertions, and preserved zero-result calls, explicit nil results,
multi-result tails, and open-tail results. Its bounded arithmetic accepts only
typed integer/float operands; Lua 5.1 numeric-string coercion such as index
`"1"` is unsupported and rejected rather than generalized.
No live client, native body, form body, server, social state, or persistence
was used.

## Remaining evidence boundaries

The admitted source proves only the local requests, guards, captures, typed
results, zero-result calls, and open tails described above. It does not prove
name acceptance, friend/ignore/party mutation, Tell delivery, dialog rendering,
native storage, server acceptance, callback settlement, or lifetime. The
`desktopWidget` open-child, Tell, and close calls, plus parent sub-window and
border calls, remain local request boundaries until an independently selected
consumer joins them.

## Reproduction

After authenticating the LPB and retaining outputs in a task scratch folder,
the public decoder route is:

```powershell
python tools/retail_script.py --input <client>/client/script/n1635q/966s5rry1rqrp8n1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/addresslistsubwidget.luac --script-out <scratch>/addresslistsubwidget.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/addresslistsubwidget.disassembly.txt <scratch>/addresslistsubwidget.luac
```

Inspect `root/proto0` through `root/proto12`, the root binding PCs listed above,
and each direct-call PC in the method table. For every selected word, the
decoded offset is the prototype code offset plus four times its PC; Lua 5.1
uses `B=argument count+1` and `C=result count+1`, with zero denoting an open
width. The finite local check covered 34 typed cases and visited 411 of 498
own-method instructions (82.5 percent); this is not branch-complete coverage.
