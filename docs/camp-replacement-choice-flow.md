# Camp replacement-choice result flow

The selected Camp replacement call requests four answers through
`WorldMaster.ask`, `DesktopWidget.askForEventMode` and `Ask/AskWidget`.
The local cancel path becomes nil, answer 4 remains 4, and an opening or
selection failure can return numeric zero. The script does not establish a
runtime result domain restricted to nil and 1-4.

This composes the no-empty-slot branch of the
[Camp favored-destination contract](camp-favored-destination-client-contract.md).
The selected actor remains Manine's recognized destination `1280062`.
The existing page owns actor identity, supplied slots, final confirmation and
the unbound historical caller. The contracts below require the dynamic method
lookups to resolve to these authenticated implementations.

## Ordered call and display requests

Let `N` be the `PopulaceCampMaster.defTalk` receiver, `W` the global
`worldMaster`, `D` the global `desktopWidget`, and `F1..F3` the three supplied
destinations. Function arguments below include each method receiver.

| Boundary | Ordered supplied values |
| --- | --- |
| Camp to `ask` | `W,N,N,53,4,F1,F2,F3` |
| WorldMaster to `askForEventMode` | `D,N,W,N,1,false,true,53,answers,F1,F2,F3` |
| Connector opening request | `D,4,"Ask/AskWidget",nil,nil,false` |
| Connector to the opened widget's `ask` | `widget,W,N,1,false,true,53,answers,F1,F2,F3` |

Here `answers` is a newly constructed table containing rows 54 through 57
at indices 1 through 4. `WorldMaster.ask` builds it from row 53 and answer
count 4. This count is distinct from the connector's literal opening category
4. The path operand names `AskWidget`, not `QuestAskWidget`.

The original open-ended `VARARG` and `CALL` instructions preserve every
formatter argument, including a nil between later values. Both the Camp call
and WorldMaster wrapper retain exactly one result. The connector discards
the widget `ask` call's results.

`AskWidget.ask` calls `initialWidget`, which requests a base-result reset
and initializes its local work fields. The selected call then requests
`askAnswerMax=4`, `askPaging=false`, `canCancel=true` and `askPageMax=1`.
It stores the nonnil default answer 1 without a range comparison, as the
[default-answer contract](ask-widget-answer-focus.md#default-answer-and-focus)
describes. These assignments do not prove native storage or later readback.

For the question, its selected property request has this exact argument tuple:

```text
_setProperty(widget,nil,"TextBlock_Question","Text",N,53,F1,F2,F3)
```

Thus the NPC receiver `N` supplies the text provider alongside row 53.
The separately forwarded WorldMaster value does not replace that provider.
The helper also requests answer content using the constructed answer rows.
Native property interpretation, text lookup, displayed controls and actual
event delivery remain outside this source contract. Initialization and
creation already make opaque calls before the result handlers can run.

Source: `world/worldmaster_event.lua:236-265`,
`widget/desktopwidget_connector.lua:12038-12090`, and
`widget/ask/askwidget.lua:108-248,485-533`, under `lua/scripts/`.

## Local completion, result and cancellation

The connector initializes its saved result to numeric zero. It opens the
widget, and only an exactly nil first opening result skips the remaining
widget operations. Any other first value reaches a dynamic `ask` lookup;
false is not treated as an opening failure sentinel here and can fail at
that lookup.

After a normal `ask` return it requests
`selectWidgetYield(D,widget,true)` and keeps the first selection result.
Only exact Boolean true causes `getAskResult(widget)` to run. That call's
first result replaces the saved zero, even when it is nil, false or zero.
For every non-nil opening result, normal completion of these calls then
requests `closeWidgetDirect(D,widget)`, discards the close results, and
returns exactly one saved value. Nil opening skips the close request.
Errors, suspension or nonreturn can prevent later calls.

The published [selection wait](gridania-opening-tutorial-contract.md#selected-widget-calls)
has no fixed timeout on this route. It distinguishes a finished widget wait
from loss of the widget. The [Ask base contract](ask-widget-result-state.md)
polls whether `askWork.askResult` differs from numeric zero. It does not poll
for acceptance. Conditional on those base methods and applied storage, reset
requests zero, a later nonzero result finishes the poll, and the getter
returns the stored scalar without an acceptance conversion. Nil and false
reads also differ from numeric zero in that predicate.

The selected `AskWidget.processUICommandEvent` has these result paths:

| Delivered command and guard | Local result request |
| --- | --- |
| `UILuaCommands.Operate` with control `TemplateButton_Answer` | Parse component 2 of the supplied widget name using delimiter `Answers`, convert it with `tonumber`, then pass that first conversion result to `setBaseAskResult`. |
| `UILuaCommands.Cancel`, with `work.canCancel == true` | Pass numeric -3 to `setBaseAskResult`. |
| Cancel with any other flag read | No result setter. |
| PagePrevious or PageNext with the selected false paging read | Adjust the local page and request `pageChange`; no result setter. |

The operation handler does not compare the converted suffix with 1 or 4,
does not check `askAnswerMax`, and does not normalize a failed numeric
conversion. `DesktopWidget.parseWidgetString` uses the script `string.split`
helper and returns the requested component. Those helpers add no answer-range
validation. A synthetic delivered `Answers5` name can therefore produce a
request to store 5 through these pinned script bodies. This characterizes
the parser and handler, not a control that the native UI actually delivers.

For the pinned base setter, an exact true input-control flag first requests
input disablement. After its normal return, or when that flag is not true,
the setter assigns the supplied scalar. The setter itself does not close the
widget. The connector's later explicit close remains a separate operation.
The published [direct-close contract](content-director-ui-contracts.md#closewidgetdirect-behavior)
qualifies that request and its liveness lookup. Even a normal true close
result does not prove native cleanup or destruction.

`WorldMaster.ask` maps exactly numeric -3 to nil and returns one value.
Every other first connector result is preserved. In particular:

| Connector outcome | WorldMaster result | Camp's next local branch |
| --- | --- | --- |
| Open returns nil, or selection returns other than exact true | 0 | Continues into old-slot resolution and final confirmation, since 0 is neither nil nor 4. |
| Selected widget result -3 | nil | Returns nil after finishing the talk turn. |
| Selected widget result 4 | 4 | Returns 4 unchanged after finishing the talk turn. |
| Selected widget result 1, 2 or 3 | Same scalar | Resolves the corresponding supplied old destination, then asks for final confirmation. |
| Another selected scalar | Same scalar | No range rejection before the existing old-slot and confirmation path. |

The final confirmation can still replace a saved result with nil, as described
in the Camp contract. No new favored-state writer, charge, registration
acknowledgement or server consumer is established here.

Source: connector `askForEventMode` and `parseWidgetString` at
`widget/desktopwidget_connector.lua:12038-12090,8061-8089`,
`widget/ask/askwidget.lua:387-482`, and `system/string.lua:156-200`.
The Ask base page owns its authenticated setter, getter and polling contract.

## Authenticated inputs and locators

Extraction: retail 1.23b `2012.09.19.0001`. The containing archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json).
Selected canonical source members matched [scripts.json](../manifests/scripts.json)
after replacing CRLF byte pairs with LF only. Original resources and decoded
payloads matched [retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Source paths below are relative to `lua/scripts/`; resource paths are relative
to `client/script/`. Hashes are SHA-256.

| Canonical source | Bytes | SHA-256 |
| --- | ---: | --- |
| `world/worldmaster_event.lua` | 7559 | `744487a7caaa94e1c4d2056cc07686a894c6ba336bbd021bbffeebceef2ad099` |
| `widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/ask/askwidget.lua` | 14551 | `c5032a2d2d1264c4a01165834f6248a01dc1c4bf7b9f791ce8baf511295398af` |
| `system/string.lua` | 4528 | `b1897ec9fb516fb7205c40fb10937ff54dd4a5dee972b45d4d4c37252347225a` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `nvsy6/nvsy6x9rq5s_5o5wq.le.lpb` | 2555 / `4ced313114ab09753ad0dc82ea8e9cd12c66d31447c967e91883932291cd7459` | 2542 / `c7db606357f8e5811809a6232157c2c9ac1daf0055cfcaa01fbbc7051fd68bf5` |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `n1635q/9rz/9rzn1635q.le.lpb` | 5257 / `8541d21030988f4ed5460690156a71a5a0120b68ed38d8db181676b27a23bfe9` | 5244 / `1b0d5e2ca4c39b781305b98320eb597337e0d4c0fc0c9167244553dfc49d14c0` |
| `rlrq5x/rqs1w3.le.lpb` | 1630 / `a85e4c176600de4274a47c4d269b42ce594d74247eded7919e248cec3b1bc885` | 1617 / `739290208fab2aad23470f1bfafb11c5cafe347c5ff16017d7a8b954b6a9886d` |

The Camp source and original resource were also reauthenticated against the
identities retained in its contract. The Ask base source, original resource
and payload were reauthenticated against the pins in the
[base result page](ask-widget-result-state.md#source-identity).

Prototype indices and PCs below are zero-based. Offsets are bytes in the
decoded payload, excluding the LPB wrapper. A PC is at `code start + 4*PC`.
Root binding PCs assign the named closures.

| Method | Root binding PC | Prototype / code start | Selected original evidence |
| --- | ---: | --- | --- |
| Camp `defTalk` | 12 | `root/proto1` / `0x1C8` | PC702 calls global WorldMaster ask with eight arguments and one result. |
| WorldMaster `ask` | 26 | `root/proto8` / `0x7C4` | PCs0-8 construct answer rows. PC18 forwards all varargs; PC19 keeps one result. PC20 compares -3; PC23 returns one value. |
| Connector `askForEventMode` | 713 | `root/proto237` / `0x1C081` | PC15 keeps one open result; PC16 tests nil. PC27 discards ask results. PC31 keeps one selection result; PC32 tests true. PC35 keeps one widget result; PC39 discards close results; PC40 returns one saved value. |
| AskWidget `ask` | 15 | `root/proto2` / `0x583` | PC1 calls initialization. PCs4/6/8/16 request answer-count/paging/cancel/page fields. PC76 forwards the question property and complete formatter tail. |
| AskWidget `initialWidget` | 24 | `root/proto5` / `0xFC4` | PC1 requests result reset; PC40 returns zero values. |
| AskWidget `processUICommandEvent` | 21 | `root/proto4` / `0xCD5` | PCs1/3 test operation/control. PCs11-15 parse, convert and request the result. PCs18/22 guard cancellation; PC26 requests -3. PC83 returns zero values. |
| Connector `parseWidgetString` | 425 | `root/proto141` / `0x14860` | PC11 calls split; PCs12/15 bound the component index; PC20 returns the selected component. |
| String `split` | 17 | `root/proto5` / `0x4CA` | PC8 finds delimiters; PCs21/34 extract components; PCs22/35 append them; PC36 returns the table. |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader`, `instruction` and `states_for`.
Check complete payload consumption, root assignments, CALL widths, branch
targets and RETURN widths before composing the selected bodies. Focused
checks cover exact input order, row construction, nil-preserving forwarding,
zero failure results, exact-true selection, cancellation, unrestricted suffix
conversion and explicit normal-path closure. Inverted selection/cancel tests
and a narrowed result-width mutation must be rejected.

These are static source and original-bytecode contracts. Actual global and
widget identities, class binding, storage, native creation/property effects,
callback names delivered by the UI, wait completion and cleanup acceptance
remain conditional. No native body, client execution, historical dispatcher
or settlement behavior was inspected for this result flow.
