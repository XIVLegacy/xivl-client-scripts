# Social widget close and parent boundaries

The social widget contracts establish local close requests and typed result
handling. The published Desktop helper contracts qualify what those requests
mean when dynamic lookup reaches the documented closures. Neither a close
request nor a normal true result establishes completed object destruction,
social mutation, server settlement or lifetime safety.

## Caller and helper composition

| Caller | Owning local request contract |
| --- | --- |
| Ignore list | [Ignore list commands](ignore-list-widget-contract.md#commands-and-paging) records the signal-11 close sequence and the list-count and control branches that select it. |
| Address submenu | [Address submenu](address-list-subwidget-contract.md) records border requests followed by open-tail close forwarding on cancel, Close, and invalid-name paths. |
| Naming dialog | [Naming dialog](address-list-naming-widget-contract.md) distinguishes the direct close that discards results from paths that forward a close result tail, and records cancel/confirmation guards. |

The [published closeWidgetDirect contract](content-director-ui-contracts.md#closewidgetdirect-behavior)
owns its argument, branch and result semantics. Nil widget input returns one
Boolean false. For a non-nil input, only an exact Boolean false first result
from the dynamic `_isAlive` call refuses the later close request. Other normal
first results, including zero results adjusted to nil, reach a fresh
`closeWidgetLocal` lookup. That call's results are discarded; after it returns
normally, `closeWidgetDirect` returns exactly one Boolean true. Ordinary lookup
or call errors propagate and prevent that return.

Therefore a caller that forwards the full close result tail has one Boolean
normal result if this lookup resolves to the documented helper. A caller that
discards close results still discards that Boolean. The widget fixtures also
exercise arbitrary helper result tails to verify caller forwarding widths;
those fixtures do not establish the nominal helper's result arity or an
actual runtime binding.

The [published closeWidgetLocal contract](content-director-ui-contracts.md#closewidgetlocal-cleanup-request)
owns recursive cleanup and owner handling. It requests owner cleanup only
after an exact true first recursive result. A nil owner skips the owner
requests; every non-nil saved owner reaches an explicit-nil setter request
before a late lookup of that saved owner's `close` member. All normal paths
return zero values. Consequently the outer helper can return true even when
recursive or owner cleanup was skipped. This is not a cleanup-success result.
The recursive traversal and conditional `_isAlive` profiles retain their own
receiver, dispatch and lifetime premises on that page.

## Supplied parent and native parent query

The address submenu's `setMode` uses its supplied parent argument to obtain
the name and position. Its contract explicitly keeps that object separate
from a later dynamic `self:_getParentWidget()` result. The naming dialog also
uses a dynamically queried parent for `ignoreFamilyName`. Matching widget
names do not establish that either query returns the supplied opening object.

The [native parent query](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/talk-native-contract.md#parent-and-child-widgets)
resolves a receiver identity, reads widget `+0xD8`, and returns the selected
identity as a control or nil under the documented gates. Interpreting that
field as a parent is inferred from the name and nil branch; its writer remains
untraced. This native contract does not bind a particular social invocation,
prove equality to the supplied parent, or establish a complete owner graph.

## Evidence and remaining boundary

This composition reuses the linked published findings. The Desktop helper
contracts pin connector LPB SHA-256
`0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`;
the social contracts own their separate resource identities, original-word
checks, finite typed fixtures and unvisited paths. No additional original
helper or native body is required to repeat those findings.

The actual dynamic callable, native receiver and field producer, callback
delivery, close/destruction implementation and complete object lifetime remain
unjoined. Reopening those boundaries requires the exact binding, receiver,
writer or callback discriminator, rather than a matching member name or a
local Boolean result.
