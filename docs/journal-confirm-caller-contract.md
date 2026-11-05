# Journal list confirmation caller contract

The non-Ask `JournalListWidget` requests a `JournalConfirmWidget` child from
its close/cancel handler. Its own `setSelectedIndex2` method can consume the
child's view-6 results: -3 becomes `true, nil`, and -4 becomes `false, nil`
through the parent's result getter. The request does not prove creation,
initializer dispatch, the child's actual parent identity, or automatic cleanup.

The [child interaction contract](journal-confirm-widget-contract.md) owns
the complete child behavior. The
[Guildleve journal lifecycle](guildleve-journal-lifecycle.md#journal-list-entry-points-and-history)
describes the distinct `widget/ask/journallistwidget.lua` implementation.
Matching class names do not join those two parent modules.

## Source identity

The selected parent is `lua/scripts/widget/journallistwidget.lua`, class
`JournalListWidget`, with base require `/Widget/WidgetBaseClass` at source
lines 3-7. Its manifest identity is 63,856 bytes, SHA-256
`D012197B3F59C812AB95F8444D53489513CFFC17DBDA9D6E7C9A3D0CA9176DD8`.
Its only literal `JournalConfirmWidget` reference is source line 272.

The original resource is `n1635q/0vpsw9yy1rqn1635q.le.lpb`, 20,650 bytes,
SHA-256
`3A3834E6E839718D7B5C94779323826C7D23F50C0F738FF9FABA11A81A55622E`.
The decoded Lua 5.1 payload is 20,637 bytes, SHA-256
`AAE90861A1DA854A84A86E6CCB4EC73638765C3D516D9BC57D96468EB9573D6B`.
These identities are pinned by [the script manifest](../manifests/scripts.json),
row `relativePath=lua/scripts/widget/journallistwidget.lua`, and
[retail coverage](../manifests/retail_lua_coverage.json), row
`decodedScriptPath=lua/scripts/widget/journallistwidget.lua`.
The child source/resource identities belong to its
[canonical identity section](journal-confirm-widget-contract.md#identity).

## Selected opening request

`processUICommandEvent(self, A1, A2, A3, A4, A5)` enters the selected block
only when A3 is exactly `UILuaCommands.WidgetClose` or `UILuaCommands.Cancel`.
It reads `ComboBox_Category.IsDropDownOpen`. Only an exact boolean true
requests that property false. In that case Cancel returns immediately,
whereas WidgetClose continues. False, nil, and numeric zero do not satisfy
the exact-true test.

The first `getViewType()` result selects the child-opening branch only when
it equals numeric 6. That branch requests
`desktopWidget:parseWidgetString(A2, 3)` and forwards all actual parser results
to `tonumber`, requesting one conversion result. Its request is then:

`desktopWidget:openChildWidget("JournalConfirmWidget", self, true, freshViewType, conversionResult)`

`freshViewType` comes from a second `getViewType()` call after the parser and
conversion calls. It is neither a literal 6 nor the saved branch-selection
result. The parent's own getter reads `work.viewType`; intervening calls are
not proved unable to change it. No nil guard rejects the conversion result.

The opener receives six raw arguments including its desktop receiver and
requests zero results. The handler's normal continuation returns zero values.
It does not save a child handle, write a selection result, call a waiter, or
issue a close request on this branch.

Source: `lua/scripts/widget/journallistwidget.lua:211-280,897-904`.
Original `root/proto1` has code offset `0x0C4E`: command/dropdown checks at
PCs 3-20, first view read at PC 24, numeric-6 check at PC 54, parser
`CALL A12 B4 C0` at PC 61 (`0x0D42`), conversion `CALL A11 B0 C2` at PC 62
(`0x0D46`), fresh view read at PC 70, and opener `CALL A11 B7 C1` at PC 72
(`0x0D6E`). Open widths preserve actual parser-result count, not a fixed
decompiler-local width. The getter is `root/proto15`, code offset `0x21D6`.

## Conditional child-to-parent continuation

If the request reaches the published child initializer with the tail
`(freshViewType, conversionResult)`, its `init(self, viewType, contentsID)`
consumes those values. This parameter correspondence is conditional: the
selected callsite does not establish how `openChildWidget` dispatches them.
The initializer's second/third formals are not the opener's parent/true pair.

The child's Operate handler first reads `getViewType()` to select the result
calculation. Only a result gate equal to 1 reaches the later fresh read that
selects the callback method. Initialization with view type 6 does not freeze
either read. The table's callback rows assume both event-time reads return
numeric 6 and method lookups resolve to the published child and parent
implementations. Close rows require only the first read. Parent getter results
additionally assume its result-time view type is 6.

| Child conversion result | Child request | Intended parent's local effect | Parent result getter in view 6 |
|---:|---|---|---|
| 1 | `closeWidgetDirect(child)` | No notification from this branch | Unchanged |
| 2 | `_getParentWidget():setSelectedIndex2(-3)` | Stores -3 when the returned object is this parent | `true, nil` |
| 3 | `_getParentWidget():setSelectedIndex2(-4)` | Stores -4 when the returned object is this parent | `false, nil` |
| Other normal conversion result | `closeWidgetDirect(child)` | No notification from this branch | Unchanged |

The child obtains its parent dynamically and does not nil-check that result.
Neither the literal opener name nor the passed `self` proves that the later
lookup returns this Lua receiver. Successful notification issues no child
close request. The child registers Cancel, but its own event body has only
the exact Operate guard, so it supplies no additional Cancel result here.

These are selected applications of
[the child's result and cancel contract](journal-confirm-widget-contract.md#operate-result-and-parent-requests),
source `lua/scripts/widget/journalconfirmwidget.lua:356,483,495-521`,
`root/proto3`, code offset `0x0A53`. The event-time getter calls are zero-based
PCs 16 and 142 (`0x0A93` and `0x0C8B`). With first read 6, conversion result
2, and later read 5, the child instead requests `setConfirmResult(-3)`.
That request does not reach this parent's published `setSelectedIndex2`
implementation or establish a change to its `selectedId`.
These child reads are separate from the parent's fresh opener argument read.
This parent source declares `setSelectedIndex2` but contains no
`setConfirmResult` declaration or reference. That absence does not rule out
an inherited, native, or external implementation.

## Completion, results, and cleanup boundary

The parent initializer writes `work.selectedId = -1` at source line 73
(`root/proto0`, code offset `0x05BD`, PC 43). Its
`processWaitCallFunction` returns one boolean: false only while that field
equals numeric -1, and true otherwise. This is an available completion
predicate, not proof that the selected opener schedules or polls it.

`setSelectedIndex2(self, value)` stores the supplied value directly. In view
6 it makes no further field write and returns zero values.
`getSelectedIndex2` returns exactly two values. Its first value maps -2 to
nil, -3 to true, and -4 to false, preserving other stored values. The second
is nil in view 6. Thus numeric zero, boolean false, and nil remain distinct
stored inputs, even though the -4 mapping also returns false.
`getAskResult` tail-forwards the getter's actual result width.

Source: `lua/scripts/widget/journallistwidget.lua:586-686`.
The completion predicate is `root/proto6`, code offset `0x1844`.
`getAskResult` is `root/proto7`, code offset `0x18B3`, with
`TAILCALL A1 B2 C0` at PC 1. `getSelectedIndex2` is `root/proto8`, code
offset `0x1902`, with two-value `RETURN A3 B3` at PC 38 (`0x199A`).
The setter is `root/proto9`, code offset `0x1A2B`, with the direct field
write at PC 1 (`0x1A2F`).

The selected parent/child bodies establish only local result storage,
completion observation, and requested UI calls. They do not establish a
successful native opening, a callback scheduler, a close after a successful
notification, object destruction, historical invocation, or authoritative
quest/Guildleve mutation.
