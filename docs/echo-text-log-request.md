# Echo text log request

`DesktopWidget.echoText` requests `checkText` with its supplied text. Only
literal Boolean false suppresses the following log request. Every other first
result, including nil and numeric zero, requests `worldMaster._printLog` with
that same text. Both normal paths return zero values.

## Checker, request and result

The original method has two fixed parameters, receiver `W` and text `T`,
with no variadic tail. Omitted parameters become nil; extra actual values are
discarded before this body. It obtains `W.checkText`, calls it with exactly
`(W, T)` and retains one result `C`. No results become nil; additional checker
results are discarded. The [separate checker contract](echo-text-check.md#predicate-and-composition)
owns its original predicate. This call site does not establish the actual
checker binding, accepted native types or a transformed string.

When `C` is exactly false, the method returns zero values without reading
global `worldMaster`. Otherwise it freshly reads that global into `M`, obtains
`M._printLog`, calls the captured method with exactly `(M, T)` and discards
every result. It then returns zero values. The checker result is used only
for the exact-false comparison; the log argument is the original fixed text
value `T`, rather than a checker result or a fresh read from the caller's
argument table. A checker side effect can change the global or its method
before the later lookup.

These are normal-completion contracts. Lookup or call errors can stop the
method, with no protected-call recovery. A nil, false or other supplied text
value still reaches the opaque checker; this parent does not prove that the
checker or a later native accepts it.

## Composition with the selected echo caller

The [parsed-key 107 caller](local-echo-client-request.md#selected-request-and-local-result)
captures its echo method before running `convertPronouns`, forwards all
conversion results after the widget receiver, and retains one echo result.
If that captured method is this original `echoText`, its fixed text parameter
receives the conversion's first result, nil when there is no result, and
discards any later results. Whichever normal branch this body takes, the
caller's one-result adjustment receives nil. That value does not report
checker acceptance, log completion, displayed output or server acceptance.

This conditional composition does not establish the actual runtime method
binding, converter behavior, text value or historical invocation.

## Published native boundary

`xivl-client-structs:docs/scheduler-item-native-contract.md`, Registration and
dispatch, Contracts, and Log output, already supplies the `WorldMaster`
`_printLog` native contract. It records registrar `0x0073AD70`, registration
caller `0x00754CCB`, callback `0x006EC230` and wrapper `0x00726CA0`. The declared
argument is one `Utf8String`, with no native return and no yield. This differs
from the separately published `Debug._printLog` registration.

Under the matching actual `WorldMaster` binding, compatible receiver and
post-preparation argument frame, that callback reads its string from internal
cell 0 and requests kind `0x20`, an empty prefix and a zero flag through
`0x0075D4C0`. The published path reaches `0x004D6D90`; it does nothing when
the world object's sink at `+0x660` is null. With a sink, the recorded path
formats the kind, prefix and text and appends an entry and its per-kind queue
id. The semantic name of kind `0x20` remains inferred in that publication.

This method proves the Lua request frame `(M, T)`. The publication does not
make that frame an observed native `ExecuteParameters` vector or prove a
runtime binding, string conversion, live sink, consumed queue entry or visible
line. It supplies no `/echo` network-send result. `_appendLogPool`, `SendLog`
and tab/display behavior are separate contracts and are not inferred from
the shared log terminology.

The adopted Structs revision is
`180ab8aaa49b0157fee8996abe4d27e05b588bda`. Its publication SHA-256 is
`b7f6f4b5f70a2a58706a5bf98fc60dd5fe6e868adc3558ac24118596bbb74381`;
`manifests/scheduler_item_native_call_contract.json` has SHA-256
`794465982d0133a35da2a921963a7cf2bbfdaa4240441673840709516711a73a`.
No new native body was inspected for this adoption.

## Source identity and checks

The [caller source identity](local-echo-client-request.md#source-identity-and-reproduction)
pins extraction `2012.09.19.0001`, the retained Lua archive, canonical connector
and original LPB at private-source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`.
The same inputs are identified by
[`scripts.json`](../manifests/scripts.json),
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`private_lua_corpus.json`](../manifests/private_lua_corpus.json).

Canonical `widget/desktopwidget_connector.lua` lines23177-23193 supply this
method. Original `root/proto476` has eleven instructions, code offset190323,
two fixed parameters, raw vararg0, zero upvalues and no nested prototypes.
Root PCs1649-1652 obtain `DesktopWidget`, load the `echoText` key, create the
closure at PC1651 and assign it at PC1652. PCs and decoded-payload offsets
below are zero-based.

| Behavior | PCs | Decoded-payload offsets |
| --- | --- | --- |
| Capture checker and call with one-result adjustment | 0-2 | 190323-190331 |
| Exact-false guard, branch and zero-value early return | 3-5 | 190335-190343 |
| Fresh global and native-method lookup, two-argument call | 6-9 | 190347-190359 |
| Zero-value final return | 10 | 190363 |

The eleven-word code range has SHA-256
`9a2df26348cd62f25e11c0a1a0f8e0558c2e57493266b3ea84b3f6847b51ec76`.
`tools/retail_script.py` decodes the authenticated LPB in memory;
`ChunkReader` and `instruction` in `tools/build_quest_contracts.py` expose the
selected header, root binding and original operands. A bounded check passed
72 authored cases for fixed-parameter padding/truncation, checker first-result
adjustment, exact false versus nil/zero/true, fresh global lookup after checker
side effects, unchanged text and discarded log results. Eight changed guard,
argument, result-width and return-width controls were rejected. Finite opaque
call stubs and primitive-equality models establish those static distinctions;
no helper body or retail runtime was executed.
