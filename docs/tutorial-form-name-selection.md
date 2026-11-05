# Tutorial form-name selection

`WidgetBaseClass.initCommon` requests a form name from the receiver's current
`getFormName` method. Only an exact nil first result selects a fallback call
using the third fixed `initCommon` argument. It then supplies the selected
value as the explicit name argument to the receiver's current `loadFormData`
method. This establishes a conditional request frame, without identifying an
active tutorial form.

The [tutorial opener](tutorial-widget-opening-contract.md#complete-opener-partition)
owns selection of `Ask/TutorialWidget`, and the
[controller vocabulary](tutorial-widget-vocabularies.md) owns its K/P aliases.
The shared [initialization sequence](gil-shop-widget-opening.md#item-list-initialization)
places `initCommon` before widget `init`. The original shared caller below
maps its incoming variadic sequence to that name argument.

## Incoming initialization frame

If `_onInit` resolves to the base implementation, write its incoming frame as
`(W,P,Q,V1,...,Vn)`: W, P and Q are its three fixed arguments, followed by
its complete variadic sequence V. It looks up `initCommon` on W and calls
that function with exactly `(W,P,V1,...,Vn)`. Q is excluded from this call.
The original open `VARARG` and open-argument call preserve every supplied V
value, its type and position, including false, zero and trailing nils.

With the selected five-fixed-parameter `initCommon`, this frame adjusts to
`(W,P,V1,V2,V3)`. Missing positions become nil and excess positions are ignored
by that target. Thus N is V1. With an empty V, the caller supplies only W and
P and the target pads N with nil. With an explicit nil V1, that third operand
is present as nil. These different call widths give the same local N but are
not the same incoming frame. No `_getName` request or property read produces N
on this route.

The normal entry jumps to original PC30. After preceding initialization
operations complete, both truth branches of `_isInstanceOf(W,"DesktopWidget")`
converge at the selected `initCommon` lookup. The predicate keeps one result
and uses Lua truth, so only false and nil skip its optional work. Neither
branch refuses the shared call. Other initialization remains opaque here.

The caller keeps exactly the first `initCommon` result I, with missing results
padded nil. It then requests
`sendCommand(W,"UIOperatorCommands.BeforeLuaInit")`, discarding all results.
After that returns, it looks up `init` on W and saves that function and W.
It reads the current global `select` and calls it with `(I,V1,...,Vn)`, using
the complete original variadic sequence again. Every `select` result becomes
an argument after W to the saved `init` function. There is no fixed result
width or extra nil padding between `select` and `init`. The `init` results are
discarded, followed by a fresh `sendCommand` lookup requesting
`(W,"UIOperatorCommands.AfterLuaInit")`, also discarding results.

The generic `initCommon` below returns I=4. If the current `select` is ordinary
Lua `select`, `init` therefore receives `(W,V4,...,Vn)`, including any trailing
nils, or just W when that suffix is empty. This is a conditional positional
contract. It does not authenticate `select`, the invoked widget initializer
or the actual controller/infoID values. A change of W's `init` property during
`select` does not replace the function already saved before that call.

Only after those calls, an exactly nil P skips the parent requests. Otherwise
the caller looks up `_isAlive` on the original P and calls it with `(P)`,
keeping one result. A false or nil result returns zero values immediately.
Any Lua-truthy result, including zero, permits a fresh `_setParentWidget`
lookup on W and request `(W,P)`, whose results are discarded. The reached
continuation freshly reads `W.widgetWork` and sets its `initialized` field
true. The later parent guard cannot prevent the earlier name/load request,
and that flag does not establish successful native loading. Remaining
callbacks are outside this contract. Every normal `_onInit` return has zero
values.

The [WidgetOpenCommand contract](widget-open-command-boundary.md) owns its
original `_createActor` argument forwarding. The published native
[creation contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/create-actor-native-contract.md#creation)
owns conversion and `_onInit` dispatch conditions. Neither publication supplies
this tutorial's actual typed incoming frame, selected shared implementation
or successful initialization. Those remain the first external dependencies.

## Name producer and request

Let W be the first fixed argument, used as receiver, and N the third fixed
argument, counting W as the first. The method has five fixed parameters and
no varargs. Omitted fixed arguments become nil and excess arguments are not
available to this body. N remains that supplied value through name selection;
it is not read from the widget's stored `widgetName` property.

After the preceding initialization operations return normally:

1. Look up `getFormName` on W, call the returned function with exactly `(W)`,
   and keep exactly its first result G. No result becomes nil and additional
   results are discarded.
2. If G is exactly nil, read the current global `_string`, then its `gsub`
   member. Call that function with exactly `(N,".+/","")`, with no implicit
   library receiver, and keep exactly its first result F. Otherwise use G.
3. Look up `loadFormData` on W after that selection and call the returned
   function with exactly `(W,F)`, where F denotes either selected value.
   Discard all results.

The fallback is an exact-nil test, not a truth test. False, numeric zero and
an empty string returned first by a different getter are forwarded unchanged.
There is no string conversion, type check or second nil guard before the
load request. A fallback returning no values therefore supplies an explicit
nil name operand. Neither call uses open result forwarding. A second `gsub`
result, such as a replacement count, never enters the load frame.

The pattern and replacement are literal call operands. Reading `_string.gsub`
does not authenticate the ordinary Lua string library or its runtime result.
This body does not substitute N directly, read an alias property, use another
fixed argument, append `.form`, or inspect controller/infoID to select F.
For the shared caller above, N is its first incoming variadic value. Its
actual value and meaning, and the dynamic method/library bindings, remain
unbound. In particular, the opener's alias alone does not prove that N
received that alias.

The inherited [common getter and base load wrapper](normal-tutorial-panel-completion.md#form-name-and-declaration-boundary)
establish the conditional normal-Ask composition: with those actual bindings,
the getter supplies nil, so this selector requests `_string.gsub(N,".+/","")`
and supplies its first result unchanged to the wrapper's native-named
filename/load requests. The supplied form declarations remain owned by that
linked contract. This composition does not bind N to a tutorial alias or
establish an active form.

## Following local naming requests

After `loadFormData(W,F)` returns normally, the body freshly reads
`W.widgetWork`, then its `common`, and writes that object's `widgetName` to
`"Window_" .. F`. The work objects are read after the load call, so earlier
objects cannot be substituted if the call changed those properties. The load
results do not guard this store. The concatenation follows Lua's operand
rules and can fail for an unsuitable selected value after the load request.

If F compares equal to `"Desktop"`, the following rename and visibility calls
are skipped. Otherwise, if F compares unequal to N, the body freshly looks up
`setWindowName` on W and requests `(W,"Window_" .. N)`. It then freshly looks
up `setProperty` on W and requests `(W,"Visibility","Hidden")`, including
when F equals N. Both calls discard all results. The comparisons use Lua
equality, including applicable equality metamethods.

These operations follow the name request and never replace its earlier F
operand. They establish neither a form root's actual name nor successful
native renaming or hiding. Remaining initialization is outside this name
contract. On normal completion the method returns one numeric 4; it does
not return F or a load-success result.

## Original source and reproduction

The source is extraction `2012.09.19.0001`, retail client 1.23b. Authenticate
the retained archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json), both selected
members against [scripts.json](../manifests/scripts.json), and its original
resource and decoded payload against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Canonical `lua/scripts/widget/widgetbaseclass.lua` | 8518 | `737a53b0472b510440735cf19a1d0a11fd100e69df7f3eab1178969a3d57b95c` |
| Original `client/script/n1635q/n1635q89r57y9rr.le.lpb` | 4080 | `aad807a42296e93301582defc8f15e4003b8093af672794282cd54950cc556ad` |
| Base decoded payload | 4067 | `11e5bab509c4dbbd7e2767d35cdf132a59b5c510c32c2e215f83cac713115140` |
| Canonical `lua/scripts/widget/widgetbaseclass_common.lua` | 69077 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| Original `client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 | `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` |
| Common decoded payload | 32983 | `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |

Use `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` and `instruction`, checking complete
payload consumption. Root closure/assignment PCs 1/2 bind `root/proto0` to
`WidgetBaseClass.initCommon`. Its instruction start is `0x19FA`, with 86
words, five fixed parameters and no varargs. PCs here are zero-based and
payload offsets exclude the LPB wrapper. Canonical source 4-109 contains the
function and line 111 its assignment. Original debug lines 57-129 are a
separate coordinate system.

The base `_onInit` is canonical `widget/widgetbaseclass.lua:7-170`, including
its assignment. Root closure/assignment PCs 4/5 bind base `root/proto0`, code
start `0x33C`, 134 words, three fixed parameters and raw variadic flag 3.
Its original debug range is 57-193. The selected `initCommon` reference is
PC83 and its call is PC86 at payload offset `0x494`.

| Shared caller dependency | Canonical source lines | Original PCs |
| --- | --- | --- |
| Normal-entry jump and instance-predicate convergence | 7-114 | 0 -> 30; 68-73, both arms reach 83 |
| Current common method, P and full incoming tail | 114-118 | 83-86; `VARARG B=0`, `CALL B=0,C=2` |
| Before command, saved init, select and full results | 119-129 | 87-95; select `CALL B=0,C=0`, init `CALL B=0,C=1` |
| After command, parent guard and fresh initialized write | 130-147 | 96-110; alive `CALL B=2,C=2`, parent `CALL B=3,C=1` |
| Zero-value returns | 42,139 and implicit final return | 29,105,133; all `RETURN B=1` |

| Dependency | Canonical source lines | Original PCs |
| --- | --- | --- |
| Current getter and one-result adjustment | 42-44 | 26-27, `CALL B=2,C=2` |
| Exact-nil selection and fallback frame | 45-52 | 28-36, fallback `CALL B=4,C=2` |
| Current load method and explicit selected name | 54-57 | 37-39, `CALL B=3,C=1` |
| Fresh work reads and stored part name | 58-63 | 40-45 |
| Desktop/name comparisons, rename and hidden requests | 64-79 | 46-58 |
| Normal final result | 108 | 83-84, `RETURN B=2` |

Focused checks authenticate the inputs and original binding, then check the
selected predicates, call operands and result widths. Synthetic replies
exercise nil/missing-result fallback, non-nil false and zero, discarded extra
results, changed post-load work objects and the three naming continuations.
Changed name sources, lookup receivers, predicate polarity, pattern, explicit
name operand and fixed result widths must be rejected. These checks establish
the local original-instruction contract, not actual runtime binding or a full
corpus reproduction. Caller checks separately preserve missing versus explicit
nil tail positions, trailing nils, full argument and select-result sequences,
first common/alive results, saved initializer lookup and post-init parent
guards. Changed fixed sources, variadic widths, call/result widths and guard
operands must be rejected.

The published native
[form path resolver](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-form-locale-resolution.md#lua-entry)
owns the conditional filename-store/load and locale lookup behavior. Applying
it still requires the actual native binding and state. The contract stops at
external argument/property writers, unknown method/library implementations,
actual widget/class/form identity, load acceptance, locale/root selection and
further template/style resolution. No client execution or delivered tutorial
input is established.
