# Craft repair selection flow

`CraftJudge.startRepair` reaches the literal `CraftRepairWidget` through
`DesktopWidget.askCraftRepairWidget`. The helper requests initialization,
selection, result reads and an explicit close before returning four values.
With the recovered widget getter, the third helper result is nil: the helper
requests two operation results, but this widget returns only one. Successful
Cancel is operation 0, distinct from opening or selection failure.

The [repair request contract](repair-request-client-contract.md#cancel-withdrawal-and-callback-results)
owns the caller's virtual-item construction, result adaptation and event
boundary. The [complete CraftRepairWidget contract](craft-repair-widget-contract.md)
owns all widget methods, declarations, child requests and item presentation.
This page supplies their selected helper join. The
[CraftStart selection contract](craft-start-selection-contract.md) describes a
different widget and does not supply this widget's operation-result width or
reset behavior.

Every composition requires the actual dynamic lookups to select the described
bindings and the calls to return normally. The literal class name and returned
object do not prove actual instance identity, constructor dispatch, installed
work storage, native readback, rendering or lifetime.

## Creation and initialization

Write the judge signature as `startRepair(self,A1,A2,A3,A4,A5,A6,A7,A8,A9)`.
Its exactly-true player branch supplies
`askCraftRepairWidget(D,0,0,A3,V,A6,A7,A8)`, where D is the desktop receiver
and V is the first virtual-item construction result. The helper retains one
result W from:

`openWidgetYield(D,4,"CraftRepairWidget",nil,nil,false)`.

The [generic opening contract](content-director-ui-contracts.md#desktop-widget-admission-and-close)
owns the nil-owner precheck, creation request, polling, saved selector and
lookup result. The final false above occupies the sixth fixed slot, rather
than the owner slot. There is no additional initialization tail in this call.
The helper's nil-only W guard returns exactly `(false,0,nil,{})` for nil W,
without initialization, selection or close. False W passes that guard and can
fail at ordinary method indexing.

For nonnil W, the next request is exactly
`setInitialData(W,0,0,A3,V,A6,A7,A8)`, with all seven operands preserved.
It discards every initializer result, including false, before requesting
`selectWidgetYield(D,W,true)`. An initializer error or nonreturn prevents
selection and close. The widget's published initialization contract qualifies
the skill comparison, optional item/life/materia/fitness operands, repeated
child lookups and failure cases. This helper does not call `setInitialItems`
or an operation-reset method.

`init` requests chosenOperation=-1. Neither `setInitialData` nor
`getCraftOperation` locally resets it. Thus an existing object is not proved
ready for a new wait merely because these methods were called.

## Selection, fresh result reads and close

The exact-true show flag makes the nominal `selectWidgetYield` enumerate
children and request `show(child)` only for an exactly-true first
`getVisibleFlag` result, then request `show(W)`. Each show result is discarded.
It next calls `selectWidgetTimerYield(D,W,nil)` and retains only the first
result S. The
[published wait contract](fishing-input-flow-contract.md#wait-result-width-and-cleanup)
owns the exact-false alive refusal, exact-true callback completion and
`_wait(0.1)` polling. No timeout is supplied. Show requests do not establish
actual visibility or callback delivery.

The widget's `processWaitCallFunction` returns false only for a current
chosenOperation equal to numeric -1. Every other value returns true. Under
the published command guards and applied writes, main/sub request operations
1/2 and Cancel requests 0, with input disabled. These are local selection
values, not repair outcomes.

Only S exactly true reads results. The helper requests exactly two values
O and R from `getCraftOperation(W)`, nil-padding missing values and discarding
extras. The pinned getter freshly reads chosenOperation and returns exactly
that one value, without a reset. Consequently R is nil under that binding.
A substituted getter's second result would instead remain observable.

O equal to numeric 0 leaves the local item table T empty. Every other O,
including nil and false, requests `getCraftItems(W,i)` separately for i=1..8,
retaining one result into `T[i]`. The getter obtains three current slot fields
through independent property reads, then selects:

| Current `(Value0,Value1,Value2)` | One getter result |
| --- | --- |
| Value0 differs from numeric 0 | Value1 unchanged, including nil or false |
| Value0 equals 0 and Value2 differs from numeric 0 | 0 |
| Value0 and Value2 equal 0 | -1 |

Nil/false Value0 are not numeric zero, and nil/false Value2 are not numeric
zero. A nil getter result removes that table entry under ordinary Lua table
semantics. The eight requests therefore do not establish a dense table or
stable native slot contents. Completion, operation and each item are separate
reads, rather than a frozen snapshot.

After every normally completed nonnil-W path, including non-true S and
operation-0 Cancel, the helper requests `closeWidgetDirect(D,W)`. It discards
all close results and only then returns exactly `(S,O,R,T)`. Initially S is
false, O is 0, R is nil and T is empty. A non-true S skips both result getters
but preserves that S in the return. There is no protected cleanup: a reached
error or nonreturn prevents later calls and the normal result.

The [direct close contract](content-director-ui-contracts.md#closewidgetdirect-behavior)
and its linked recursive/owner cleanup qualify this explicit request. A
normally returned false close result does not change the selection status,
operation or item table. Normal helper return does not prove destruction or
successful cleanup.

## Conditional judge return

The judge requests exactly four helper results and accepts S only when it is
exactly true. Its published adaptation remaps operations 1/2 to 5/6 and makes
the operation nil for a non-true S. Therefore, under the pinned one-result
widget getter, main/sub give final prefixes `(5,nil)` / `(6,nil)`, successful
Cancel gives `(0,nil)`, and ordinary helper failure gives `(nil,nil)`.

The [caller contract](repair-request-client-contract.md#cancel-withdrawal-and-callback-results)
owns positive temporary-index resolution through package 1, the two fresh
ItemBaseClass classification passes, and the final open `unpack` result tail.
These prefixes do not impose a fixed total result count. That contract and
`xivl-client-structs:manifests/repair_contract.json`, `REPAIR-C-0004`, remain
the authorities for the continuation's scope.

The first unbound edges are actual object creation/selection and dynamic
method/storage application. Nothing here establishes a server-selected
callback, causal 24243/22012 settlement, item identity, grant, debit, material
consumption or condition change.

## Source identity and verification

The extraction is retail 1.23b `2012.09.19.0001`. The selected archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). Selected
members were read in memory with only CRLF pairs normalized to LF, then
matched [scripts.json](../manifests/scripts.json) by bytes, lines and SHA-256.
Original LPBs and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) before complete
Lua 5.1 chunk parsing with `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`.

| Source relative to `lua/scripts/` | Canonical bytes | Canonical SHA-256 |
| --- | ---: | --- |
| `judge/craft/craftjudge.lua` | 23945 | `5019a3e9acaf99a23210a451e0df2b0f4a73e5d44f764a480bb3b23953c9076f` |
| `widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/craftrepairwidget.lua` | 35844 | `4756facc801ec743e43bc4eebf53cb918751901ad533b7b52aa3f6f4ac226d0c` |

Prototype indices, PCs and decoded-payload offsets below are zero-based.
Canonical source ranges include the method binding. The widget's complete
method and source identity publication remains canonical.

| Selected method | Canonical source | Prototype / code offset | Decisive PCs |
| --- | --- | --- | --- |
| Judge `startRepair` | 473-588 | `root/proto20` / 5580 | 34 caller B=9,C=5; 46 exact-true status; 106/107 open unpack/return |
| Desktop `askCraftRepairWidget` | 11225-11287 | `root/proto211` / 108227 | 9 open B=7,C=2; 10 nil guard; 20 init B=9,C=1; 24 selection B=4,C=2; 26 true guard; 29 operation B=2,C=3; 32 zero test; 40 item B=3,C=2; 45 close B=3,C=1; 50 RETURN B=5 |
| Desktop `selectWidgetYield` | 25694-25733 | `root/proto539` / 207847 | 4 show flag; 17 child visibility; 20/23 show; 27 timer B=4,C=3 |
| Widget `init` | 11-298 | `root/proto0` / 1139 | 75 chosenOperation=-1 request |
| Widget wait / operation getter | 1483-1496 / 1499-1506 | `root/proto23` / 12435; `root/proto24` / 12555 | wait 2 compares -1; getter 2 RETURN B=2 |
| Widget item getter | 1509-1526 | `root/proto25` / 12642 | 2 slot call C=4; 3/7 zero tests; 5/10/13 one-value returns |

Bounded original-bytecode fixtures checked the literal open inputs, seven
initialization operands, nil/false distinction, true-only selection, show/wait
ordering, one-versus-two operation result adjustment, absence of a local reset,
fresh slot reads, Cancel/main/sub operations, item-table construction and
explicit close ordering. Negative controls rejected a changed class name,
truncated operation request, inverted selection guard and missing getter
result. These ordinary-table fixtures use mocked normal helpers. They do not
execute native storage, the client, an event callback or a transaction.
