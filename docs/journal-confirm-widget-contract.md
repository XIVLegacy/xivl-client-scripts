# JournalConfirmWidget client interaction contract

`JournalConfirmWidget` is a static client Lua widget recovered from the
retail 1.23b extraction. This page records its presentation and interaction
contract. It does not establish native transport, rendered success,
authoritative Guildleve mutation, or object destruction after a close request.

## Identity

The registry identifies class `JournalConfirmWidget`, base path
`/Widget/WidgetBaseClass`, and exactly these methods:

| Method | Prototype | Parameters | Returns | Original code offset and PCs |
|---|---|---:|---:|---|
| `getFormName` | `root/proto0` | 1 | 1 | `0x020B`, 0-2 |
| `init` | `root/proto1` | 3 | 0 | `0x024E`, 0-71 |
| `ask` | `root/proto2` | 2 | 0 | `0x059B`, 0-188 |
| `processUICommandEvent` | `root/proto3` | 6 | 0 | `0x0A53`, 0-185 |
| `initialWidget` | `root/proto4` | 1 | 0 | `0x0EE3`, 0-33 |
| `setContentsID` | `root/proto5` | 2 | 0 | `0x105E`, 0-2 |
| `getContentsID` | `root/proto6` | 1 | 1 | `0x10AC`, 0-3 |
| `setViewType` | `root/proto7` | 2 | 0 | `0x10FE`, 0-2 |
| `getViewType` | `root/proto8` | 1 | 1 | `0x114A`, 0-3 |
| `setAnswerText` | `root/proto9` | 3 | 0 or 1 | `0x119A`, 0-28 |
| `convertTextID` | `root/proto10` | 10 | 1 | `0x12C6`, 0-112 |

`params` includes `self`. `setAnswerText` returns one value only for its
rejected-input path and no values after a successful property update. The
resource has `init`, not a separate `initAsk` method.

The decoded script is `lua/scripts/widget/journalconfirmwidget.lua`. Its
manifest identity is 14,842 bytes, SHA-256
`503D63377723872A74072EEB2E054FA909FFF1C364827379405F84A5665932B7`.
The matched retail resource is
`n1635q/0vpsw9y7vw41sxn1635q.le.lpb`, 5,343 bytes, SHA-256
`6B6B85DFF8EE661F20CAFB50B7442CEF548A340CAA1F693E577198C637938153`; its
decoded payload is 5,330 bytes with SHA-256
`4E27E15DB6AAA33617E655307F9D42AE6A9AB99FCD44826EE1C120AAD8684A56`.

Sources: `xivl-client-scripts:lua/scripts/widget/journalconfirmwidget.lua`,
`xivl-client-scripts:lua/registry.json:42122-42143`,
`xivl-client-scripts:manifests/scripts.json:15561-15564`, and
`xivl-client-scripts:manifests/retail_lua_coverage.json:25038-25050`.

## Initialization

`init(self, viewType, contentsID)` declares `_temp` fields `viewType` and
`askAnswer` as `integer8`, `askAnswerMax` as `integer8`, and `contentsID` as
`integer32`. It stores `viewType`, stores `contentsID` only when non-nil, and
sets `Window_JournalConfirmWidget.IsModal` to true.

It registers these raw UI requests:

- `_setUICommandCondition("_widget", "UILuaCommands.Cancel", 3)`
- `_setUICommandTemplateCondition("ControlTemplate_ListBoxItem",`
  `"TemplateButton_Answer", "UILuaCommands.Operate", 5)`

It adds `Item_Answers1` through `Item_Answers24` to `ListBox_Answers` using
`ControlTemplate_ListBoxItem` and sets each item's `Focusable` property false.
It then calls `ask(self, contentsID)`. The third initializer input is thus both
the optional stored contents ID and the raw argument forwarded to `ask`.

`initialWidget` resets `work.askAnswer` and `work.askAnswerMax` to zero,
clears `Label_Question.Content`, clears each answer's content, and collapses
answer visibility for items 1 through 24. `ask` calls this reset first and
collapses `Grid_Button.Visibility`.

The sidecar records the property, condition, parent lookup, and item calls at
`xivl-client-scripts:lua/scripts/widget/journalconfirmwidget.calls.json:1-42`.
Those records identify requested calls, not native property or UI semantics.

## Presentation branches

The view-type groups below are resolved from the original EQ/JMP branch
operands. `A1` is the second formal of `ask`; the raw `Content` argument tail
is shown where the body passes arguments directly to `_setProperty`.

| `viewType` | Question `Content` request | Answer text IDs by displayed index |
|---|---|---|
| 5, 7, 8 | raw tail `worldMaster, 33601, A1` | 1 -> 4203; 2 -> 100212 |
| 9, 10 | raw tail `worldMaster, 33601, A1` | 1 -> 5013; 2 -> 5014 |
| 11 | `convertTextID(4219, A1)` result | 1 -> 5013; 2 -> 5014 |
| 6 | `convertTextID(5020)` result | 1 -> 5015; 2 -> 5016; 3 -> 5017 |
| 12 | `convertTextID(5001, A1)` result | 1 -> 5018; 2 -> 5019 |

Each answer text is produced through `convertTextID` and applied through
`setAnswerText`. Other view types receive only the reset and grid-collapse
requests. `ask` returns no values and does not update `askAnswer` or
`askAnswerMax` after the reset.

## Operate result and parent requests

`processUICommandEvent(self, widgetString, controlTemplate, command, A4, A5)`
uses only the first three event inputs. It proceeds only for the exact pair
`controlTemplate == "TemplateButton_Answer"` and
`command == "UILuaCommands.Operate"`.

The original `CALL A9 B5 C0` invokes
`desktopWidget:parseWidgetString(widgetString, 2, "Answers")` with four
arguments and requests all actual parser results with dynamic Lua stack-top
arity. The following `CALL A8 B0 C2` forwards all actual parser results from
the range beginning at R9 through the current stack top to `tonumber` and
stores one conversion result. The decompiler's named R9 through R13 locals do
not cap runtime result or argument count and do not prove nil padding. The
body does not assign meaning to the forwarded parser results, a numeric base,
or their nilness. The table is therefore conditional on the normal conversion
result matching the listed value.

The handler first reads `getViewType()` to select the result calculation.
Only when gate `L7 == 1` reaches callback dispatch does a later fresh read
choose the parent callback method. The table's callback rows assume both reads
return its listed view type and the dynamic methods resolve to these
implementations. Close rows depend only on the first read and skip the later
one. Initialization does not freeze either read. In `root/proto3`, zero-based
CALL PCs 16 and 142 are at decoded
offsets `0x0A93` and `0x0C8B` (canonical source lines 356 and 483).
A first read of 6, conversion result 2 and later read of 5 instead request
`setConfirmResult(-3)`. The [selected caller contract](journal-confirm-caller-contract.md#conditional-child-to-parent-continuation)
records that split-read consequence for the non-Ask journal parent.

| `viewType` | Conversion result | Internal result | Gate | Requested action |
|---|---:|---|---:|---|
| 5 | 1 | 1 | 1 | `_getParentWidget():setConfirmResult(1)` |
| 7, 8 | 1 | -3 | 1 | `_getParentWidget():setConfirmResult(-3)` |
| 9, 10, 11, 12 | 1 | `getContentsID()` | 1 | `_getParentWidget():setConfirmResult(contentsID)` |
| 6 | 1 | `getContentsID()` | 0 | `desktopWidget:closeWidgetDirect(self)` |
| 6 | 2 | -3 | 1 | `_getParentWidget():setSelectedIndex2(-3)` |
| 6 | 3 | -4 | 1 | `_getParentWidget():setSelectedIndex2(-4)` |
| 5, 7, 8, 9, 10, 11, 12 | 2 | -2 | 0 | `desktopWidget:closeWidgetDirect(self)` |
| Handled view types above | other normal conversion result | unchanged | 0 | `desktopWidget:closeWidgetDirect(self)` |
| Other view types | any normal conversion result | unchanged | 0 | `desktopWidget:closeWidgetDirect(self)` |

The gate is `L7 == 1`. Parent calls return no value to this widget. The body
does not nil-check `_getParentWidget()` before calling either parent method.
Successful parent notification does not issue a close request.

## Helpers and cancel boundary

`setContentsID` and `setViewType` assign their second input directly to
`work.contentsID` and `work.viewType`. Their getters return those stored
values. No validation is recovered for either setter.

`setAnswerText(self, index, text)` returns false when `index` is nil, `""`,
below zero, or above 24. If those comparisons complete without rejecting, it
requests the item's content and visible state using `Item_Answers` plus
`tostring(index)`. A nonempty string or boolean index reaches the less-than
comparison and may raise before any property request. Index 0 is permitted by
the guard even though initialization creates only items 1 through 24.

`convertTextID(self, textID, i2, ..., i9)` starts with `"@" .. tostring(textID)`.
For each later input, nil, true, or false returns the current string; another
value appends `/i` and its `tostring` value. It performs no text lookup.

The Cancel condition is registered during `init`, but the event method has no
Cancel branch. An event reaching this method without the exact Operate guard
is a no-op in this body; framework-level cancel handling is outside this
resource.

## Caller and lifetime boundary

The [non-Ask JournalListWidget caller](journal-confirm-caller-contract.md)
has an attributable child request and a conditional selected-result join.
Its source keeps the opening guard, fresh view argument, child event-time
reads and dynamic parent lookup separate. Native creation/initializer
dispatch and actual parent identity remain unproved. `getFormName` returns
`AskWidget`, but that string does not prove how a factory maps the class.

The only close operation recovered here is the requested
`desktopWidget:closeWidgetDirect(self)` on the failed selection gate. The
resource contains no destructor, ownership transfer, retained-handle, or
close-to-destruction proof. Object lifetime after a close request remains
unresolved. This contract also makes no claim about authoritative Guildleve
state or a rendered success state.
