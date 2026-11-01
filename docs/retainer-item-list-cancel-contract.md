# Ask RetainerItemListWidget cancel and focus contract

The Ask resource `lua/scripts/widget/ask/retaineritemlistwidget.lua` contains a
local cancel/close/focus continuation after its item-selection path. The
contract below is limited to recovered Lua instructions from the retail
1.23b extraction. It does not assign server, native, rendering, or widget
lifetime behavior.

## Pinned resource

The source identity is anchored by these public manifest records:

- LPB path `n1635q/9rz/s5q91w5s1q5xy1rqn1635q.le.lpb`, 50376 bytes,
  SHA-256 `CF7DA0872C6EB1743C9A2C73C11769022D030BDCE1F67CFA4FE2A8EF9127E81E`:
  `manifests/retail_lua_coverage.json:26642-26655`.
- Decoded payload, 50363 bytes, SHA-256
  `408CF496ED3FCDA95C53A6925CC9C8E689C517E37893E6D566E55E0A64AAE469`:
  `manifests/retail_lua_coverage.json:26642-26655`.
- Canonical LF source, 156026 bytes and 6813 lines, SHA-256
  `854328615DFAC84F08861DA2157300EDFAD67D63010783EBD7F520969C2521E6`:
  `manifests/scripts.json:15140-15144`.
- Class and base metadata:
  `lua/registry.json:39614-39700` and
  `xivl-client-structs:manifests/lua_api_contract.json:152947-153908`.
- The decode path is `tools/retail_script.py`; its pinned unluac artifact is
  `tools/vendor/unluac/unluac_2025_12_23.jar`, 796256 bytes, SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`, as
  recorded in `tools/vendor/unluac/PROVENANCE.json`.

The root source calls `require("/Widget/Ask/AskBaseClass")` at lines 2-4 using
root PCs 0-2 (`GETGLOBAL require`, `LOADK path`, `CALL B2 C1`) and
`_defineClass("RetainerItemListWidget","AskBaseClass")` at lines 5-8 using
root PCs 3-6 (`GETGLOBAL _defineClass`, two `LOADK` operands, `CALL B3 C1`).
The later `RetainerItemListWidget` member assignments for the four selected
names are source-level `SETTABLE` attempts at lines 1108, 4285, 4439, and
4481 (root PCs 36, 120, 126, and 129); they do not prove class installation
or runtime readback. The selected method source bounds are exactly:

Formal arities include the receiver. Local compositions require the selected pinned closures and normal completion of intervening accesses and calls.

| Method | Source lines | Declared arity |
| --- | ---: | ---: |
| `setWindowFocus` | 1088-1108 | 2 |
| `previousSequence` | 4261-4285 | 1 |
| `processUICommandCancel` | 4362-4439 | 5 |
| `processUICommandClose` | 4442-4481 | 5 |

## Local behavior

`setWindowFocus(self, name)` returns no values. It does nothing for exact nil
or the empty string. Otherwise it requests `setLogicalFocus(self,name)`, calls
`_getKeyboardFocusedWidget(desktopWidget)` for one result, and requests
`setKeyboardFocusedControl(self,name)` only when Lua `==` compares the returned
value equal to `self`. The five focus fixtures use ordinary mock tables with no
`__eq` metamethod; they do not establish a universal identity or native
comparison guarantee. A request is not evidence that focus was applied or
rendered.

`previousSequence(self)` first reads `self.work.sorttype`, then requests
`getConfigWork(desktopWidget,9)` and compares that first result with the initial
sort value. If they differ by Lua `==`, it independently reads
`self.work.sorttype` again and requests
`setConfigWorkWithSave(desktopWidget,9,<fresh sorttype>)`. Thus an ordinary
fixture whose getter changes `sorttype` from 3 to 4 and returns 4 reaches the
setter with 4, not the initial 3. It then performs independent `self.work`
lookups before the `editWidgetOpen = -1` and `chosenOperation = 1`
`SETTABLE` attempts, returning no values. Table `__index`/`__newindex` behavior
could redirect or drop those accesses; the setter request and writes do not
prove storage, persistence, or readback.

`processUICommandCancel(self, A1, command, A3, A4)` evaluates its leading
guard in short-circuit order. It reads `work.error` first; when `error == true`,
it does not call `isValidRetainer(desktopWidget)` and directly requests `saveSortType(self)`
then tailcalls `closeWidgetDirect(desktopWidget,self)`. Only when
`error ~= true` does it call `isValidRetainer(desktopWidget)` for one result; an exact false result takes the
same save-and-tailcall path, while every other result continues. The
tailcall preserves the dynamic callee's result width. On the valid path,
`checkKeyboardFocused(desktopWidget,self)` requests one result. Exact false
reaches the original `RETURN B1` and returns zero values. Six later guards run in source
order: `editWidgetOpen ~= 0`, `resultForAsk ~= 0`, `0 < updatecount`,
`0 < updatecountbaz`, `submenu == true`, and `inputok == false`. The first two
reject any value not Lua-equal to numeric zero, including nil, false, and the
empty string; each of these six guards returns one literal `false` when it
rejects. Exact `command == "Button_ListClose"`
requests `closeMateriaList(self)` and returns no values. Other commands invoke
`previousSequence(self)` and return no values.

`processUICommandClose` has the same short-circuit error/validity order and
save-and-tailcall path. Its valid path returns one literal `false` for exact
true `submenu` or exact false `inputok`; otherwise it invokes
`previousSequence(self)` and returns no values.

The counter tests assume normal Lua table indexing, calls, and comparisons. At
PC 37, `0 < work.updatecount`, and PC 43, `0 < work.updatecountbaz`, a nil
value that reaches the comparison raises the ordinary Lua numeric comparison
failure; ordinary false, true, and other non-numeric values have the same
boundary. These are not converted to a local false result. Metamethod
comparison behavior was not
executed. Zero and negative numeric values continue past these positive-counter
guards.

These tests preserve the distinction between nil, false, zero, empty strings,
and exact true values. They also preserve zero results versus one result
`false`. Dynamic calls outside the four methods remain opaque.

## Relationship to the Ask result

The existing Ask selection contract remains separate from these local
continuations. `OrdinaryRetainer.eventTalkRetainerItemList(2)` selects the Ask
widget and consumes its four-value code-22 UI result; the widget disables input
and uses a local selection delay of 2 before `setAskParameter` resets local
state and re-enables input. These are local UI facts and do not establish a
server acknowledgement or accepted mutation. See
`xivl-client-scripts:docs/bazaar-retainer-client-contracts.md:565-608`.

The code-22 tuple is `(22, package, item, bazaartype)`, with the published
reward-reference selection rule and Ask `resultPackage/resultItem` distinction;
it has no quantity or price. See
`xivl-client-scripts:docs/retainer-widget-results.md:20-24,34-43`.
The existing code-22 issuer and repricing boundaries remain at
`xivl-client-scripts:docs/retainer-widget-results.md:53-69` and
`xivl-client-scripts:docs/bazaar-retainer-client-contracts.md:610-635`.

Nothing here establishes native registration, first values, request
application, achieved focus, rendering, child creation or destruction,
historical actor/ward/roster state, transaction acceptance, inventory or
currency mutation, settlement, or a withdrawal reply.
