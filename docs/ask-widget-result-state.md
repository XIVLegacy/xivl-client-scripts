# Ask widget result and wait state

The recovered `AskBaseClass` separates a result value from completion polling.
It declares `askWork.askResult` as `integer16`, requests an initial value of
numeric zero, and considers a later read finished exactly when it differs
from numeric zero. A cancel value such as -1 therefore finishes the same
poll as a positive answer. Completion alone does not identify acceptance.

These are the selected base-method contracts, conditional on a widget
resolving these implementations. The [event item selector](event-item-select-widget-contract.md)
and [QuestAsk](quest-ask-widget-contract.md) have their own result producers
and caller conditions. The [Ask wrapper](materia-meld-client-contract.md#craftjudge-callback-contract)
owns opening, selection and requested result counts.

## Source identity

The extraction is retail 1.23b `2012.09.19.0001`. The selected canonical
member, original LPB and decoded payload matched
[scripts.json](../manifests/scripts.json) and
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
The containing retained archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). Source
normalization replaces CRLF byte pairs with LF only.

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical source | `lua/scripts/widget/ask/askbaseclass.lua`, 154 lines | 2633 | `642F3112D4663004FDC0B79DAF0A5FAF8B7588EAD58D2CD8E6747821BDA54ADB` |
| Retail LPB | `client/script/n1635q/9rz/9rz89r57y9rr.le.lpb` | 1742 | `4C1C98059F5B3663D24A85897D21FF603DFB5C95000C20FDFA4BEFD592AD431D` |
| Decoded Lua 5.1 | XOR-0x73 LPB payload | 1729 | `A1D4129CA5779C3B2598DA418909F057BD9B6C6733701855FD70BF2A9DCB1230` |

## Selected state and calls

`init` declares the temporary fields `askResult: integer16` and
`inputControlFlag: boolean` (canonical lines 16 and 21), requests
`askResult=0` and `inputControlFlag=true`, calls `setModal(true)`, then
forwards its varargs to dynamic `self:initAsk(...)`. It discards that
method's results and returns no values. These calls do not establish
successful storage installation or native modal state.

| Method | Selected local behavior | Result |
| --- | --- | --- |
| `setBaseAskResult(value)` | If the read of `inputControlFlag` equals Boolean true, requests `setInputEnable(false)`. After the normal return of that call, or immediately when the flag is not true, assigns the supplied value to `askWork.askResult`. | Zero values. |
| `resetBaseAskResult()` | If the flag equals Boolean true, requests `setInputEnable(true)`. It then assigns numeric zero to `askWork.askResult`. | Zero values. |
| `getBaseAskResult()` | Reads `askWork.askResult` without a fallback or acceptance conversion. | Exactly one value. |
| `getAskResult()` | Tailcalls dynamic `self:getBaseAskResult()`. | For the pinned base getter, its one value; otherwise the actual resolved target controls the results. |
| `isAskFinish()` | Reads `askWork.askResult`; returns false when the read equals numeric zero, true otherwise. | Exactly one Boolean. |
| `processWaitCallFunction()` | Tailcalls dynamic `self:isAskFinish()`. | For the pinned base predicate, one Boolean. |

The typo in the source method name `setInputContorlFlag` is retained. It
assigns its supplied value to `askWork.inputControlFlag` and returns no
values. The result setter and resetter test exact Boolean true, rather than
general Lua truthiness. Neither helper closes a widget or restores focus.

The native contract at
`xivl-client-structs:docs/work-binder-native-contract.md`, "An object without
storage", says a declared integer member reads nil and drops writes when its
storage pointer is zero. Conditional on that native binding and the pinned
predicate, such a nil read also differs from numeric zero and therefore
returns true from `isAskFinish`. This is a conditional composition, not a
demonstration that a selected widget can reach the wait without storage.
The source predicate supplies no nil or false fallback. It must not be
replaced by a truthiness test: zero is truthy in Lua.

## Selected caller composition

The [event item selector](event-item-select-widget-contract.md#result-tuple)
maps a later base result of exactly -1 to acceptance false. Other base reads
map to true in that producer. Its operate and close branches request 1 and
-1 respectively through `setBaseAskResult`. When those calls resolve to
the pinned base setter, they request input disablement under the exact-true
flag and then assign that scalar to the declared result member. The base
poll regards either scalar as finished if a later read returns it.

This joins the selected setter, read and polling contracts without proving
that a request was applied or that the same widget instance was polled.
Actual storage, overrides, callback delivery, later writes, rendered output
and native creation remain separate conditions. The wrapper's opening-status
Boolean and a widget's acceptance value remain separate result positions.
A finished poll is not an item selection, quest decision, server grant or
completed close.

## Bytecode locators and reproduction

Prototype indices and PCs below are zero-based. Offsets are bytes in the
decoded payload, excluding the LPB wrapper. A PC is at `code start + 4*PC`.
Each binding PC is the root `SETTABLE` assigning the named closure.

| Method | Binding PC | Prototype / code start | Selected operands |
| --- | ---: | --- | --- |
| `init` | 9 | `root/proto0` / `0x228` | PC17 assigns zero; PC19 assigns true; PC25 has `CALL B=0,C=1`; PC26 returns zero values. |
| `processWaitCallFunction` | 12 | `root/proto1` / `0x359` | PC1 tailcalls the predicate with receiver only. |
| `getAskResult` | 24 | `root/proto5` / `0x426` | PC1 tailcalls the base getter with receiver only. |
| `setInputContorlFlag` | 27 | `root/proto6` / `0x474` | PC1 assigns the supplied flag; PC2 returns zero values. |
| `setBaseAskResult` | 30 | `root/proto7` / `0x4CB` | PC2 compares the flag with true; PC6 discards input-call results; PC8 stores the supplied value; PC9 returns zero values. |
| `resetBaseAskResult` | 33 | `root/proto8` / `0x563` | PC2 compares the flag with true; PC6 discards input-call results; PC8 stores zero; PC9 returns zero values. |
| `getBaseAskResult` | 36 | `root/proto9` / `0x604` | PC2 has `RETURN B=2`, returning the member read. |
| `isAskFinish` | 39 | `root/proto10` / `0x658` | PC2 compares the member with zero; PC5/7 return false/true respectively. |

Reproduction uses `decode_lpb` in `tools/retail_script.py` and the complete
fixed-header Lua 5.1 reader and instruction decoder in
`tools/build_quest_contracts.py`. Check the root closure assignments, selected
comparison jumps, field declarations, call operands and return widths against
the authenticated original payload. Read inputs in memory and retain only
identities, assertions and supported contracts.
