# Echo token replacement request

`DesktopWidget.replaceString` returns the supplied input unchanged when its
replacement value is nil. Otherwise it tail-calls plain global
`_replaceMacroCodeString` with exactly the input, token and replacement,
returning that call's complete result tail. This is the helper used by the
[ordered echo conversion requests](echo-pronoun-conversion.md#ordered-replacement-preparation).

## Guard, frame and results

The original method has four fixed parameters `(D, S, K, V)` and no variadic
tail. Missing positions become nil; extra actual values are discarded. The
receiver `D` is unused by this body, which performs no receiver lookup.

Exact `V == nil` returns exactly one value, `S`, including an explicit nil.
That path neither reads nor calls the native global. False, numeric zero and
the empty string are non-nil replacements and take the other path. There is
no guard on the supplied input or token and no string conversion in this
helper.

The non-nil path freshly reads global `_replaceMacroCodeString` and tail-calls
it with exactly `(S, K, V)`. It passes no widget receiver. Normal completion
forwards zero, one or multiple results without truncation or padding. Errors
have no protected-call recovery. These statements do not establish an
accepted native input domain or the actual global binding.

The parent converter retains one result from each completed helper call.
Consequently, its next intermediate text receives `S` unchanged on this
helper's nil-replacement path, or the native call's first result on the other
path, nil when there is no native result. Further native results are discarded
by that parent. The helper itself does not search for a token, skip absent
tokens or prove substitution semantics.

## Existing native contract

`xivl-client-structs:docs/global-native-contract.md`, Receiverless call
convention, Native frame, Contracts, and String natives, supplies the matching
published global contract. `_replaceMacroCodeString` is registration order15,
registrar `0x00753860`, caller `0x00758426`, callback `0x006FF600`, with wrapper
`0x00726E00`. It declares three `Utf8String` arguments, one `Utf8String` result
and no yield.

Under the matching actual global forwarder, receiver and post-preparation
frame, the existing publication records a text, pattern and replacement read.
Its replacement tag6 case pushes the text unchanged; that internal tag test
is separate from this Lua helper's nil test. For text without a byte below
`0x20`, it records replacement of every pattern occurrence through
`0x0067AC00`. For text containing such a byte, it records the selected
`0x02`/`0x03` span loop and a first-span position anomaly: a hit inside the
first span is replaced. Several-span behavior was not executed there.
The inline-macro interpretation of those delimiters remains inferred.

Those are adopted publication facts. This finding does not independently
establish the routines' complete matching rules, overlapping-hit or empty-token
behavior, byte/Unicode rules, replacement rescanning, live binding or actual
converted text. It does not replace that recorded span limitation with a
claim that all encoded spans are protected. No new native body was inspected.

The global convention's entry request is `global[name](global, ...)`; its
actual argument-cell projection still requires the expected layout after
native preparation. The widget-free Lua frame above does not independently
prove an actual `ExecuteParameters` vector or conversion of false/zero/nil
values into the declared string arguments.

The adopted Structs revision is
`180ab8aaa49b0157fee8996abe4d27e05b588bda`. Its
`docs/global-native-contract.md` and
`manifests/global_native_call_contract.json` own the native evidence and
frame limits. Actual replacement/name values, actor identity, rendered echo
output, server behavior and historical invocation remain separate.

## Source identity and checks

The [converter source identity](echo-pronoun-conversion.md#source-identity-and-checks)
pins the retained archive, canonical connector, original LPB and decoded
payload at private-source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`, extraction `2012.09.19.0001`.
Canonical `widget/desktopwidget_connector.lua` lines7273-7285 supply this
method. Original `root/proto125` has ten instructions, code offset78670,
four fixed parameters, raw vararg0, zero upvalues and no nested prototypes.
Root PCs375-377 obtain `DesktopWidget`, create the closure at PC376 and assign
the constant RK key `replaceString` at PC377. PCs and payload offsets are
zero-based.

| Behavior | PCs | Decoded-payload offsets |
| --- | --- | --- |
| Exact-nil comparison and one-value unchanged return | 0-2 | 78670-78678 |
| Plain global lookup and fixed three-argument preparation | 3-6 | 78682-78694 |
| Complete-result tailcall | 7 | 78698 |

The ten-word code range has SHA-256
`c04c05320e3ff9cc6d4dd85712bbc425db67371d89adc7323b9d09c9fb3a4441`.
`tools/retail_script.py` and `ChunkReader`/`instruction` in
`tools/build_quest_contracts.py` expose the authenticated original in memory.
A bounded check passed 27 authored cases for nil versus non-nil replacements,
unchanged nil/false/zero input, fixed-parameter padding/truncation, receiver-free
arguments and zero/nil-bearing/multiple result tails. Seven changed guard,
argument and result-width controls were rejected. Opaque native stubs prove
only the source frame and result adjustment; no native body or retail runtime
was executed.
