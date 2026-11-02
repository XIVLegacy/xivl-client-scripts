# IgnoreListWidget local list contract

This contract records local behavior recovered from one authenticated retail
Lua 5.1 resource. It covers the root bindings, the 15 declared own methods,
and contained code. Base, parent, form, native, callback, social-state,
server, persistence, rendering, and object-lifetime behavior remain outside
the contract.

## Source identity

- Logical resource: `widget/ignorelistwidget.lua`.
- Retail coordinate: `n1635q/13wvs5y1rqn1635q.le.lpb`.
- Original LPB: 7,736 bytes, SHA-256
  `1d3d02837de9875795b247d9a497821d0e933089e58ab4c7fbd76b71664ad935`.
- Decoded Lua 5.1 payload: 7,723 bytes, SHA-256
  `e193b638bf79594851d9d3ae5d33f687bfb36898c427652a4090fee4c6617ddf`.
- Canonical LF decompile: 21,543 bytes, 968 lines, SHA-256
  `0058da65b87bf3635a3f5c031939c68e95f829dfac3b98d6d2b35ef26e5c6a4e`.
- Decoder: `tools/retail_script.py`, SHA-256
  `765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`.
- Decompiler: `tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes,
  SHA-256
  `98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.

The decoded payload and canonical source were reproduced from the pinned LPB
with the pinned decoder and decompiler. The canonical source hash matches the
script manifest. The LPB coordinate and decoded-payload association belong to
retail Lua coverage metadata; that metadata has no canonical-source hash.

## Root binding ledger

The root prototype starts at decoded offset 32 and contains 53 instructions.
PC 2 is `CALL A=0 B=2 C=1`, word `0x0100401c`, for `require` with
`/Widget/WidgetBaseClass`. PC 6 is `CALL A=0 B=3 C=1`, word
`0x0180401c`, for `_defineClass("IgnoreListWidget", "WidgetBaseClass")`.
Each method uses a fresh `GETGLOBAL IgnoreListWidget`, `CLOSURE`, and
`SETTABLE` attempt. For method index `i`, the closure is at root PC `8+3i`
and the table write is at PC `9+3i`; the table key is the method name.
These writes are binding attempts and do not prove class installation or
dispatch.

| method | closure PC | SETTABLE PC | key constant |
| --- | ---: | ---: | --- |
| `init` | 8 | 9 | `init` |
| `setFocus` | 11 | 12 | `setFocus` |
| `processUICommandEvent` | 14 | 15 | `processUICommandEvent` |
| `pageSe` | 17 | 18 | `pageSe` |
| `makeThisPage` | 20 | 21 | `makeThisPage` |
| `getAddressListMax` | 23 | 24 | `getAddressListMax` |
| `setSignal` | 26 | 27 | `setSignal` |
| `getSignal` | 29 | 30 | `getSignal` |
| `ignoreFamilyName` | 32 | 33 | `ignoreFamilyName` |
| `setSubWindowOperation` | 35 | 36 | `setSubWindowOperation` |
| `deleteRequest` | 38 | 39 | `deleteRequest` |
| `addRequest` | 41 | 42 | `addRequest` |
| `getAddressName` | 44 | 45 | `getAddressName` |
| `makeTestList` | 47 | 48 | `makeTestList` |
| `setBorder` | 50 | 51 | `setBorder` |

## Prototype and method windows

The source line range is the canonical LF decompile range. The prototype
offset is the absolute decoded-chunk offset of its first instruction; each
instruction is four bytes, so `offset + 4*PC` locates a word.

| method | source LF | prototype | offset | words |
| --- | ---: | --- | ---: | ---: |
| `init` | 11-205 | `root/proto0` | 646 | 160 |
| `setFocus` | 210-230 | `root/proto1` | 2292 | 16 |
| `processUICommandEvent` | 233-474 | `root/proto2` | 2505 | 225 |
| `pageSe` | 479-488 | `root/proto3` | 4256 | 5 |
| `makeThisPage` | 491-759 | `root/proto4` | 4371 | 239 |
| `getAddressListMax` | 762-771 | `root/proto5` | 5848 | 6 |
| `setSignal` | 774-787 | `root/proto6` | 5966 | 9 |
| `getSignal` | 790-799 | `root/proto7` | 6111 | 6 |
| `ignoreFamilyName` | 802-811 | `root/proto8` | 6235 | 6 |
| `setSubWindowOperation` | 814-832 | `root/proto9` | 6359 | 19 |
| `deleteRequest` | 835-861 | `root/proto10` | 6562 | 19 |
| `addRequest` | 864-881 | `root/proto11` | 6847 | 14 |
| `getAddressName` | 884-901 | `root/proto12` | 7037 | 13 |
| `makeTestList` | 904-932 | `root/proto13` | 7214 | 23 |
| `setBorder` | 935-968 | `root/proto14` | 7462 | 28 |

The authenticated original words contain 128 direct CALL/TAILCALL sites, 144
EQ/LT/LE/JMP guard words, and 44 RETURN words. The complete PC, decoded offset,
opcode, A/B/C, argument/result widths, target name, and raw word matrix is
retained with the evidence for this contract.

Representative request words are:

| prototype PC | word | request |
| --- | --- | --- |
| `root/proto2:46` | `0x0180019d` | tail-call `desktopWidget.closeWidgetDirect(self)` |
| `root/proto2:62` | `0x0180019d` | tail-call `desktopWidget.closeWidgetDirect(self)` |
| `root/proto2:76` | `0x0180019d` | tail-call `desktopWidget.closeWidgetDirect(self)` |
| `root/proto2:134` | `0x0000819c` | call `desktopWidget.openChildWidget`, open argument tail, one result |
| `root/proto2:194` | `0x0180819c` | call `getChildWidgetByWindowName("AddressListSubWidget")` |
| `root/proto2:204` | `0x028041dc` | call child `setMode(1, A4, self)` |
| `root/proto2:206` | `0x010041dc` | call child `show()` |
| `root/proto2:216` | `0x040081dc` | call `desktopWidget.openChildWidget`, seven arguments, one result |
| `root/proto6:7` | `0x0280409c` | call `setControlProperty("Button_Add", "IntData.Value2", A1)` |
| `root/proto9:9` | `0x018000dd` | tail-call own `deleteRequest(work.listindex)` |
| `root/proto9:16` | `0x018000dd` | tail-call own `addRequest(A2)` |

## Local state and requests

All methods receive the widget as `A0`. The evaluator and the word matrix
preserve Lua 5.1 widths: `B=0` and `C=0` are open argument/result tails,
`C=1` discards results, and `C=2` keeps one result. Lua numeric equality
treats `1` and `1.0` as the same numeric value; Boolean `true` is distinct.

### Initialization and focus

`init` creates a fresh `work._temp` table containing ordered descriptor pairs
for `chosenOperation` (`integer8`), `page` (`integer8`), `listindex`
(`integer16`), and `iteminpage` (`integer8`).
It sets `chosenOperation=0`, `listindex=-1`, and chooses a row height of 20,
or 24 only when `desktopWidget.getWindowSize()` returns exactly 640 by 480.
It computes `iteminpage` from `ListBox_Address.Height / row height`, installs
cancel, close, confirm, command-condition, template-confirm, modal and drag
requests, creates `Address_1` through `Address_iteminpage`, hides each row and
status icon, assigns row command parameters, disables Previous and Next,
writes text IDs 3720 and 3703, sets `page=0`, and calls `setSignal(1)`.
The method returns no values.

`setFocus(control)` ignores only nil and the empty string. Otherwise it calls
`setLogicalFocus(control)`, reads the current desktop keyboard-focused widget,
and calls `setKeyboardFocusedControl(control)` only when Lua equality says it
is the actual widget receiver. The identity and equality behavior of a native
metamethod remains outside this contract.

### Commands and paging

`processUICommandEvent` first handles `PropertyChanged`. One fresh `getSignal`
result equal to 2, 22, or 32 calls `makeThisPage` and tail-calls
`setSignal(10)`. A result equal to 3, 23, or 33 tail-calls `setSignal(10)`.
Outside that branch it performs one fresh signal query. Exact 21 returns before
the second query; otherwise it performs a second fresh query, and exact 31
returns after that query. Thus the first 21 path does not perform the second
signal or any later request.

`WidgetClose` sets signal 11 and tail-calls
`desktopWidget.closeWidgetDirect(self)`. `Cancel` on `ListBox_Address` reads
the list count: exact 200 follows the same signal-11 close path; other counts
tail-call `setFocus("Button_Add")`. Other Cancel controls use the close path.
Previous and Next require the corresponding `getEnable` result to be exactly
Boolean `true`; they adjust `work.page`, call `pageSe`, and tail-call
`makeThisPage`. Add tail-calls `setFocus("Button_Add")`.

Operate on Button_Add focuses the button, then calls
`desktopWidget.openChildWidget("AddressListNamingWidget", self, true, 1, nil,
...)`, forwarding the open result of `ignoreFamilyName` as the final open
arguments. A non-nil first child result is returned immediately, including
Boolean false. Operate on Previous or Next changes page, calls `pageSe`, and
tail-calls `makeThisPage` without an enable guard. A positive row parameter
sets `work.listindex=page*iteminpage+A4`, checks the count, and either
tail-calls `makeThisPage` when the index is too large or focuses
`Address_A4`. A non-nil AddressListSubWidget result is treated as an existing
child: the widget itself receives `setBorder(A4)`, then the child receives
`setMode(1,A4,self)` and `show()`. A nil result instead opens
`desktopWidget.openChildWidget("AddressListSubWidget", self, true, 1, A4,
self)`. For a nil lookup, a first result exactly equal to Boolean true triggers
the first widget border request in that path and returns true; a false result
does not issue that request. Because the existing-child guard is `~= nil`, a
false child value enters that path and can error after the widget's own border
request. These local requests encode no server settlement or social mutation
outcome.

`pageSe` calls `sendControlCommand("TextBlock_Total", "Page")` and returns no
values.

### Page construction

`makeThisPage` reads the count. For exact zero it clears and hides the total,
shows the empty-list message, hides every row, disables Previous and Next,
enables and focuses Add, and returns one Boolean false. For a nonzero count it
hides the message, reads `AnchoredIndex`, computes
`floor((count-1)/iteminpage)`, and clamps page in source order: the upper clamp
runs first and the lower clamp runs only in the other branch. It reads
`getKeyboardFocusedControl` for Previous first; it issues the second focus read
only when that first result is not exactly `Button_Previous`. It then updates
the paging enables and total
text ID 3745, fills visible rows using `getAddressName`, and hides stale rows.
When a prior navigation control was focused it chooses a new control focus;
otherwise no focus request is required for a full page. Add is disabled only
for exact count 200. Nonempty paths return no values.

### List and signal helpers

`getAddressListMax` tail-calls
`getControlProperty("Address_Maker", "Count")` with an open result tail.
`setSignal(0)` returns without a request; any other value writes
`Button_Add.IntData.Value2`. `getSignal` and `ignoreFamilyName` tail-call the
corresponding `Button_Add.IntData.Value2` and `Value3` property reads with open
result tails.

`setSubWindowOperation(0)` returns. Operation 21 tail-calls
`deleteRequest(work.listindex)` and operation 31 tail-calls
`addRequest(A2)`; other operation values return no values.

`deleteRequest(index)` reads the count and returns when `index > count`; nil or
unsupported numeric input reaches the original comparison and can error. For
an admitted index it reads `Address_Maker[index-1].name`, writes
`Button_Add.StringData.Value2`, and sets signal 21. `addRequest(name)` returns
for the exact empty string or nil; otherwise it writes the same StringData
property and sets signal 31.

`getAddressName(index)` uses the supplied index when non-nil and otherwise
uses `work.listindex`, then reads `Address_Maker[index-1].name`. It returns
exactly the first property result: a zero-result helper supplies one nil and
extra helper results are discarded by the fixed one-result call width. This is
a raw local property result and does not prove a name-acceptance decision.

`makeTestList(count)` uses 25 when count is nil, writes rows 0 through count
inclusive as `name0`, `name1`, and so on, and calls `updateListProperty`.
`setBorder(index)` hides every `Address_i:Border_ItemSelected` for a negative
index; otherwise it emits one visibility-true request for the selected row.
The nonnegative path does not hide other rows or establish exclusive rendering.

## Local requests and external boundaries

The exact helper requests earned by this source are local UI edges only:

- `root/proto2:134`, `CALL A=6 B=0 C=2`,
  `desktopWidget.openChildWidget("AddressListNamingWidget", self, true, 1,
  nil, ignoreFamilyName results)`. The open argument tail and one-result
  width are recovered; child construction, callback ownership, name
  acceptance, and server ignore-state mutation are not.
- `root/proto2:194`, `CALL A=6 B=3 C=2`,
  `getChildWidgetByWindowName("AddressListSubWidget")`, followed on the
  supplied child by `root/proto2:204`, `CALL A=7 B=5 C=1`,
  `setMode(1,A4,self)`, and `root/proto2:206`, `CALL A=7 B=2 C=1`, `show()`.
  These are local child requests with supplied callable and receiver identity.
- `root/proto2:216`, `CALL A=7 B=8 C=2`,
  `desktopWidget.openChildWidget("AddressListSubWidget", self, true, 1, A4,
  self)`. A Boolean true local result selects the border path; it does not
  establish social acceptance or callback settlement.
- `root/proto2:46`, `:62`, and `:76`, each `TAILCALL A=6 B=3 C=0`,
  `desktopWidget.closeWidgetDirect(self)`. A returned tail is local and does
  not prove destruction or lifetime completion.

No native implementation, callback producer, owner destructor, wire request,
or accepted ignore-state transition was opened or attributed. These calls
therefore establish only local request tuples and typed local branches; they do
not establish native callback settlement, owner lifetime completion, or server
ignore state.

## Verification and limits

Static checks parsed the authenticated payload and checked all root binding
attempts, all 15 method windows, all 128 direct CALL/TAILCALL words and widths,
all 144 guard/JMP words and destinations, and all 44 RETURN words. A finite
instruction-driven replay covered 44 typed cases and visited 666 of 788 own
method instructions. It included initialization, empty and nonempty pages,
stale-row hiding, anchored focus, Previous/Next enable-true paths, count-200
Add disable, selection, add and delete request prefixes, operation 21/31,
Previous/Next refresh, out-of-range row refresh, cancel, close, refusal,
default/error prefixes, explicit nil and open tails, fresh signal/focus reads,
child present/absent paths, and every own method.

Each corruption control had a passing baseline before mutation. The controls
rejected a CALL-width mutation, guard mutation, root-binding mutation, outgoing
request-argument change with the original callable and receiver, a cloned
receiver carrying the original callable, callable replacement, open-tail
truncation with the original callable and arguments, Boolean/numeric guard
swap, zero-result versus explicit-nil change with identical calls, a selection
state-write and list-index mutations, five independent and one suppress-all
init-write suppressions, a type-preserving `_temp` descriptor corruption, and
a nonterminal helper failure that retained its original error prefix while
incorrectly reaching the real close.

The replay is finite, not a universal Lua interpreter. It intentionally does
not model arbitrary coercion, metamethods, native rendering, persistence,
server settlement, or object destruction. Concrete replay cases cover
`make-page-stale-anchored` (stale rows and anchored focus),
`make-page-prev-enabled`, `make-page-next-enabled`, and
`make-page-add-disabled` (the enable and count-200 branches), plus
`process-next-refresh` and `process-operate-row-out-of-range`. Remaining
static-only or unvisited behavior includes alternate 640x480 initialization,
the six `makeThisPage` prior-navigation focus-choice calls at `root/proto4`
PCs 197, 203, 207, 215, 221, and 225, full test-list generation, unsupported
command families, and additional error/coercion combinations. A local helper
return proves only the local
branch and tuple; it does not prove any native or server outcome.

## Reproduction

With a retail client root and a plain scratch directory, reproduce the public
decoder and disassembly artifacts with:

```powershell
python tools/retail_script.py --input <client>/client/script/n1635q/13wvs5y1rqn1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/ignorelistwidget.decoded.luac --script-out <scratch>/ignorelistwidget.reproduced.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/ignorelistwidget.disassemble.txt <scratch>/ignorelistwidget.decoded.luac
```

Inspect `root/proto0` through `root/proto14`, the root binding PCs above, and
the corresponding CALL, guard, and RETURN words in the disassembly. Unluac
prints the root as `main` and `root/protoN` as `main/fN`; the text gives
mnemonics and operands, while a raw word is read from the decoded chunk at
`offset + 4*PC` for zero-based PC. The source line table and bytecode offsets
are independent locators; the metadata identity does not itself establish
local control-flow or request semantics. These commands reproduce the source
and disassembly artifacts only. The bounded behavioral claims remain limited
to the listed source words and local request tuples.
