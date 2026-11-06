# Conditional tutorial widget creation frame

The published normal-Ask route supports a conditional positional composition:
the alias position reaches `initCommon.N`, while the controller and infoID
positions reach `init` and then `initAsk`. Applying the original alias or
numeric values to those positions requires the actual dispatch and conversion
conditions below. The publications do not identify a historical invocation,
active form or accepted tutorial progression.

## From the selected opener to native execution

Let `D` be the desktop helper receiver, `t` its stored
`work.tutorialDeviceType`, and `i` exactly numeric 2 or 5. The formal controller
is overwritten. Let `A` be the selected alias: numeric `t == 2` selects the
P spelling, and other values select K. A K alias does not imply `t == 1`.
Let `S` be the literal `"Ask/TutorialWidget"`.

The [complete opener partition](tutorial-widget-opening-contract.md#complete-opener-partition)
selects `openWidgetYield` for both infoIDs. Under its
[creation-wrapper contract](gridania-opening-tutorial-contract.md#selected-widget-calls),
reaching `commandCreateWidget` supplies the following frame. Counts include
the Lua receiver where present.

| Reached boundary | Ordered supplied arguments | Count | Required continuation |
| --- | --- | ---: | --- |
| `commandCreateWidget` | `(D,S,false,D,true,A,12,false,t,i)` | 10 | Wrapper enable, type and occupancy conditions permit the request. |
| Saved function `F` | `(q1,c,false,S,D,true,A,12,false,t,i)` | 11 | The separately looked-up `q2` supplies first command result `c` for low ID 24228. |
| Saved function `G` | `(q1,n,c,S,D,true,A,12,false,t,i)` | 11 | `F` resolves to `commandAboutWidget`, its false-force gates permit execution, and `n` is the first command-name result. |

The [saved-function contract](content-director-ui-contracts.md#commandcreatewidget-forwarding)
owns the first player result `q1`, later independent player result `q2`, and
`F` saved before the second lookup. It does not prove `q1 == q2` or identify
`c`. The [player request contract](player-widget-command-request.md)
owns `G`, the later saved `_executeCommand` lookup, the entry clock and blocker
comparisons, playing rejection, blocker write and one-result return. The
fixed false force argument is consumed by that adapter. It is not another
argument before `S` or in the native Variable tail. Every reached dependency
must complete normally for the following request to occur.

## Conditional native callback and command body

The native [execution contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/command-talk-native-contract.md#execution-natives),
with its Argument cells and list builders section, declares Utf8String,
LuaControl* and Variable after the receiver. Require the unproved typed-frame
premise that the actual `_executeCommand` native frame corresponds to
`(q1,n,c,S,D,true,A,12,false,t,i)` under the accepted receiver convention,
with exactly eight present suffix values after `c`. Actual receiver/context
identity, receiver insertion and the mapping from the source call into that
frame are parts of this premise, not consequences of binding identity.
If this premise holds, `G` is that binding, receiver and prefix conversion
succeed, and every present suffix value has a recognized raw tag and its
selected reader completes normally through the saved top, the eight values
after `c` occupy eight Variable positions. The native copies
cells beginning at index 1, so the callback cell sequence contains the command
control plus those eight values. Its event-slot, binding-reference, package
and control-readiness tests remain required. The
[Variable reader](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/widget-native-call-contract.md#variable-argument-reader)
establishes conditional consumption and cell append counts, without general
value fidelity or arbitrary control-table acceptance. The published
[native callback registration](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/widget-native-call-contract.md#native-callback-registration)
leaves transitive context/frame changes, source-syntax mapping and receiver
insertion unresolved.

The [row 24228 priority declaration](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/command-script-identity.md#widget-open-command-priority-declaration)
is `-1`. Only if the command resolves the published system-command getters
and its sheet read supplies that value does the
[name selector](linkshell-party-command-contracts.md#shared-dispatch-and-wire-representation)
produce `commandRequest`. The row, low ID and class-path mapping do not
identify the actual command, sheet, native descriptor or callback.

Suppose the actual selected descriptor reaches the published CommandNonBlock
path and invokes the published player `_onCommandRequest`. Use new symbols:
`R` for its lookup-derived Lua receiver, `d` for the descriptor's name, and
`c1,s1,p1,b1,a1,j1,h1,t1,i1` for the nine materialized cell values, in that
order. These symbols are not assertions of equality with `q1`, `c`, `S`, `D`,
`true`, `A`, `12`, `false`, `t` or `i`. In particular `d` is not assumed to
equal the caller's `n`.

The native [dispatch spine](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/event/event-base-callback-arguments.md#dispatch-spine),
Record and call arguments, Operator vector and Callback vectors sections
establish the descriptor-name prefix and ordered converted cells. The
[supplied-frame contract](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/delegate-command-producer.md#function-binding-value-and-supplied-frame)
establishes one emitted value per selected descriptor and the registry/binding
conditions. Under those conditions and its runnable fresh-call path, the
callback receives exactly:

```text
(R,d,c1,s1,p1,b1,a1,j1,h1,t1,i1)
```

This is 11 supplied arguments. Null controls, unsupported descriptors, failed
binding/function lookup and prior suspended continuations are not supplied by
that formula. Control values are rematerialized through registry conversion,
not recovered by assuming original Lua object identity. One value per cell
does not prove scalar string, Boolean or small-integer fidelity through the
preceding Lua-to-native read and later emission.

The published [request-hook continuation](materia-meld-client-contract.md#native-and-server-boundary)
tries `command:command(player,...)` before its `fire` and server fallbacks.
If the current `c1.command` lookup actually resolves
`WidgetOpenCommand.command`, the body receives
`(c1,R,s1,p1,b1,a1,j1,h1,t1,i1)`: 10 arguments. The first two fixed arguments
are unused and the third is the path. The descriptor name `d` is consumed by
the player hook and does not become that path. Actual resolution of this
command method remains required, independently of any basename or low ID.

The [command formal-frame contract](widget-open-command-boundary.md#command-formal-frame-and-factory-tail)
then supplies exactly `(nil,B,false,p1,b1,a1,j1,h1,t1,i1)` to its saved factory,
where `B` is the first result of its fresh `_string.gsub(s1,".+/","")` call.
This is 10 arguments: three prefix values and seven payload positions. The
factory global is saved before that fresh `gsub` lookup, after the earlier
`sub` and `require` requests return normally. Only one `gsub` result and one
factory result are retained. The latter is unused before the command's one
true return. That true does not report successful creation. With value fidelity
`s1 == S` and ordinary string behavior, the require operand is
`/Widget/Ask/TutorialWidget` and `B` is `TutorialWidget`. Neither spelling
establishes the factory's actual class binding.

## Creation payload and initializer positions

Require a separate unproved typed-frame premise for the actual `_createActor`
native call: it follows the published Global receiver convention and supplies
`(U,nil,B,false,p1,b1,a1,j1,h1,t1,i1)`, with exactly the seven listed present
payload positions after the nil/B/false prefix. Here `U` denotes that
convention's Global receiver. Its actual identity and insertion are unproved,
and it is not equated with `worldMaster`, either player lookup, `D`, `R` or
`W`. The source factory call and binding identity alone do not establish
this native frame.

Under that premise, suppose the saved factory is the published `_createActor`
binding, prefix reads succeed, every present payload value has a recognized
raw tag and its selected reader completes normally through the saved top,
the class resolves to the selected new WidgetBase creation path, and its
creation and `_onInit` dispatch conditions hold. The
[creation contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/create-actor-native-contract.md#creation)
copies the seven payload cells beginning at internal index 3. The
[widget payload contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/widget-native-call-contract.md#widget-creation-payload)
conditionally emits seven values in order when those cells have only tags
0, 1, 2, 3, 4 or 6, every tag-4 control is nonnull and satisfies its published
binding/registry conversion conditions, and conversion, lookup and invocation
preparation complete normally. Tag 5, null controls and other uninspected
types are outside that formula. Its receiver-first layout remains a supported
inference. This is the new-control path, not a reuse-path initialization claim.

Use `p2,b2,a2,j2,h2,t2,i2` for those newly emitted values and `W` for the
lookup-derived receiver. They are distinct from both the original Lua values
and the command callback values above. Under that layout inference and actual
selection of the shared base `_onInit`, the remaining positions are fixed:

| Reached boundary | Ordered supplied arguments | Consequence |
| --- | --- | --- |
| Shared `_onInit` | `(W,p2,b2,a2,j2,h2,t2,i2)` | Eight supplied arguments. Fixed `P=p2`, `Q=b2`, and `V=(a2,j2,h2,t2,i2)`. |
| Selected `initCommon` | `(W,p2,a2,j2,h2,t2,i2)` | Seven supplied arguments. `Q` is excluded. The five-fixed-parameter target adjusts these to local slots `(W,p2,a2,j2,h2)`, dropping the two excess values. Its third fixed argument `N=a2`. |
| Saved `init`, after ordinary `select(4,V...)` | `(W,t2,i2)` | Three arguments. The first common result must be its ordinary numeric 4. |
| Selected Ask `init` -> current `initAsk` | `(W,t2,i2)` | The complete two-value tail reaches the current Ask tutorial initializer. |

The [shared initialization contract](tutorial-form-name-selection.md#incoming-initialization-frame)
owns exclusion of `Q`, full V forwarding, one common result, the Before/After
command requests, saving `init` before the current `select` call and the later
parent guard. The [Ask base contract](ask-widget-result-state.md#selected-state-and-calls)
owns its preceding declarations/modal requests and full vararg forwarding.
Both method bindings and all preceding normal returns remain conditions.
The parent alive/parenting requests occur after initialization and do not
guard the earlier name request.

No Lua open tail may be collapsed to one temporary. At each published Lua
full-tail boundary an explicit nil, including a trailing nil, occupies its
position. An empty Lua tail contributes no position. Lua scalar first-result
adjustment instead pads no result with nil and discards extras. Native
conversions retain the qualified count conditions above. A missing declared
Variable position is distinct from a present recognized suffix: the native
dispatcher constructs one internal tag-6 placeholder without reading a present
value. For `_createActor`, this is the published `T < 5` case after successful
prefix reads. The selected seven- and eight-value present suffixes above do
not use that missing-position case. A generic emitted-value count is not
evidence that `a2 == A`, `t2 == t` or `i2 == i`.

## Conditional name and lesson result

Under the preceding native frame and binding premises, if value fidelity
through both native boundaries is established for the alias, controller and
infoID, then `N=A`, `init(W,t,i)` and `initAsk(W,t,i)` follow
from the positional composition. For a selected numeric controller 1 or 2
and infoID 2 or 5, this gives the corresponding K2, P2, K5 or P5 initializer
operands. The [normal Ask initializer](normal-tutorial-panel-completion.md#initialization-and-selected-text-branches)
owns those exact controller/infoID comparisons and subsequent requests.

If the actual getter is the published inherited
[one-nil getter](normal-tutorial-panel-completion.md#form-name-and-declaration-boundary),
the current `initCommon` therefore requests `_string.gsub(a2,".+/","")`.
Under the additional alias-fidelity condition and ordinary `gsub`, its first
result is the same `TutorialWidgetK2/P2/K5/P5` spelling. The selected base
`loadFormData` then requests `_setFilename` with that value, followed by
`_loadForm`, discarding their results. Other getters can select a different
non-nil value, including false or zero. Neither the alias computation nor the
default getter alone establishes a form load or its active declaration.
The linked form-name contract owns the subsequent naming/visibility requests,
and the linked normal-panel boundary owns the static form/style limits.

The remaining joins include both unproved actual native frame premises above:
the mapping of each source call into native context/frame positions and the
Global receiver's insertion and identity. Actual dynamic callable/receiver/class
selection, the two native conversion results and their control binding
conditions, and the initializer/getter/library bindings also remain required.
Without them the supported result is the conditional positional frame above,
with transformed values. Native clock domains,
admission and cancellation, readiness, parent/wait behavior, closure and
static declaration/style claims retain the scopes of their canonical contracts.
API true, a supplied argument count, a readiness flag and a finished Ask poll
are separate from successful creation, rendering and accepted progression.

## Evidence and composition checks

This composition adopts the linked publications and their original-source
identities and locators for retail 1.23b extraction `2012.09.19.0001`.
It adds no original-body or runtime observation. Authored positional checks
exercise the selected four alias/controller/infoID combinations, exact frame
widths, fixed-force consumption, trailing nil retention and distinct source,
callback and initialization symbols. Rejecting controls change a path slot,
insert force, truncate a tail, include `Q` in the shared common frame or merge
unproved identities. A separate control rejects collapsing the seven supplied
common arguments into its five fixed slots. These checks validate the
reasoning. Further controls reject deriving native frames from binding
identity, missing or extra present values and projecting the Global receiver
from source syntax. They do not execute retail
bytecode, native bodies or the client.
