# RetainerPaymentWidget conditional local contract

The root calls `_defineClass` with `RetainerPaymentWidget` and `WidgetBaseClass`
as its class and base names. Its owned Lua body emits display/property requests
and exposes a conditional
confirmation/result protocol. This contract covers a named receiver and
supplied method values; it does not recover the caller that opened the widget.

## Provenance and method vectors

The pinned retail LPB resource was
`n1635q/s5q91w5su9lx5wqn1635q.le.lpb`, 2748 bytes, SHA-256
`81AE94AE857412F017A03A914FC5CA114A49BA7D3DA8DF1B6742B765120E881E`.
The pinned `xivl-client-scripts:tools/retail_script.py` route with
`xivl-client-scripts:tools/vendor/unluac/unluac_2025_12_23.jar` (SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`)
produced a 2735-byte decoded payload, SHA-256
`9CAC65B9B39892393D11E0F5C57116D7292AE4761A37AF3DA2C118E2D293B043`.
The LF-canonical source is 5209 bytes and 251 lines, SHA-256
`02972D3DF10B8097140EB62206576CAAF50239C3E7B0EE6C02DD15B5FA3FFB98`.
`xivl-client-scripts:tools/build_quest_contracts.py:ChunkReader,instruction`
parsed the original prototypes and operands. Public identity pins are
`xivl-client-scripts:manifests/scripts.json:15843-15846` and
`xivl-client-scripts:manifests/retail_lua_coverage.json:27393-27405`.

| Method signature | Prototype | Arity | Code start | LF source window |
| --- | --- | ---: | ---: | ---: |
| `init(self,A1,A2,A3)` | `root/proto0` | 4 | `0x1E5` | 11-100 |
| `processUICommandEvent(self,A1,A2control,A3command,A4value,A5)` | `root/proto1` | 6 | `0x52A` | 103-132 |
| `processAskResult(self,A1result)` | `root/proto2` | 2 | `0x6CE` | 135-152 |
| `processWaitCallFunction(self)` | `root/proto3` | 1 | `0x779` | 155-167 |
| `getAskResult(self)` | `root/proto4` | 1 | `0x7E7` | 170-183 |
| `setAskResult(self,A1)` | `root/proto5` | 2 | `0x869` | 186-192 |
| `getPayment(self)` | `root/proto6` | 1 | `0x8B6` | 195-202 |
| `setPayment(self,A1)` | `root/proto7` | 2 | `0x905` | 205-218 |
| `setRetainerData(self,A1,A2nickname)` | `root/proto8` | 3 | `0x9A4` | 221-251 |

The API contract independently records these nine methods and arities at
`xivl-client-structs:manifests/lua_api_contract.json:185028-185149`.

The published native work-binding route uses userdata; this LPB does not prove
ordinary table backing. The work-member contract says that `_temp` declares
fields, declared field writes route through native descriptors, undeclared
writes can be dropped, and initial value, conversion, and preservation outcomes
remain open (`xivl-decomp:docs/script/widget-work-members.md:1-4,116-174,293-324`).
The SETTABLE facts below are therefore Lua assignment operands, not
unconditional native stores or durable readbacks. The `_temp` registry
node/factory selection and each field's first value are not proved by this LPB.

## Local state and requests

`init(self,A1,A2,A3)` reads `self.work` and assigns `_temp` a declaration list
for `askAnswer/integer32` and `payment/integer32`. It then executes the Lua
assignment `self.work.askAnswer = -1`. These are declaration and assignment
operands only; this body does not prove a native initial value, conversion,
application, or later readback.

The exact request/call operands emitted by `init` are:

- `_setProperty(nil,"Window_RetainerPaymentWidget","IsModal",A1)`.
- `_setUICommandCondition("Button_Decide","UILuaCommands.Operate",5)` (first
  occurrence).
- `setText("TextBlock_Message",6701)`.
- `setText("TextBlock_NicknameTitle",6401)`.
- `setContent("Button_Decide",6702)`.
- `setContent("Button_Cancel",6703)`.
- `_setUICommandCondition("Button_Decide","UILuaCommands.Operate",5)` (second
  occurrence, after both `setContent` calls).
- `_setUICommandCondition("Button_Cancel","UILuaCommands.WidgetClose",5)`.
- `_setUICommandCondition("_widget","UILuaCommands.Cancel",5)`.
- `_setUICommandCondition("_widget","UILuaCommands.WidgetClose",5)`.
- `_setUICommandCondition("Label_NumberInput","NumberInputBox.ValueChanged",10)`.
- `self:setRetainerData(A2,A3)`.

These are calls/requests only. No modal registration, rendering effect, or
condition dispatch is proved by this LPB. The inherited `setText` and
`setContent` bodies, native property application, and command-condition
dispatcher are outside scope. When the corresponding `self` lookups resolve to
the published native bindings, the shared contracts identify `_setProperty` as
a typed property request with a nil leading name and no Lua result
(`xivl-client-structs:docs/widget-native-call-contract.md:218,235-240`) and
`_setUICommandCondition` as a three-argument condition request with no yield or
result (`xivl-client-structs:docs/desktop-native-call-contract.md:62-70`). A
receiver or self-lookup override can supply different semantics. Regardless of
binding, each source `CALL` has `C=1`, so its result is discarded.

`setRetainerData(self,A1,A2nickname)` ignores its first data argument and, when
the local method is selected by dynamic dispatch, emits in order:

1. `_setProperty(nil,"TextBlock_Nickname","Text",A2nickname)`.
2. `_setProperty(nil,"CustomControl_NumberInput","Minimum",0)`.
3. `_setProperty(nil,"CustomControl_NumberInput","Maximum",999999999)`.
4. `self:setPayment(0)`.

The `init` call is `self:setRetainerData(A2,A3)`: only if that call selects the
local method does init's `A2` become the unused local `A1`, and init's `A3`
become nickname `A2nickname`. Its final `self:setPayment(0)` is a separate
dynamic lookup; only if that lookup selects the local `setPayment` does the
assignment operand `self.work.payment = 0` precede the number-input `Value`
property request. No formatting, rounding, clamping, currency lookup, or
nickname conversion occurs in the owned Lua body.

The local `setPayment(self,A1)` body is general: for any supplied `A1`, it
executes the Lua assignment operand `self.work.payment = A1`, then requests
`_setProperty(nil,"CustomControl_NumberInput","Value",A1)`, and returns no
values. The local `setAskResult(self,A1)` body executes
`self.work.askAnswer = A1` for any supplied `A1` and returns no values. These
are not guarantees that native work state was applied or preserved.

## Event and confirmation protocol

`processUICommandEvent(self,A1,A2control,A3command,A4value,A5)` handles exact
command strings in this order:

1. If `A3command` is exactly `UILuaCommands.Cancel` or
   `UILuaCommands.WidgetClose`, it dynamically calls
   `self:setAskResult(-3)` and returns no values. If the local setter is
   selected, its assignment operand is `self.work.askAnswer = -3`, subject to
   native work application and readback.
2. Otherwise, if `A2control` is exactly `Button_Decide` and `A3command` is
   exactly `UILuaCommands.Operate`, it calls opaque global
    `desktopWidget:openChildWidget` with six data arguments
    `("CommonDialogWidget", self, true, nil, 6704, 2)` and returns no values.
    The explicit `desktopWidget` receiver plus those six data arguments are the
    seven explicit Lua arguments supplied by `CALL A=6 B=8 C=1`; the helper
    result is discarded.
3. Otherwise, if `A3command` is exactly `NumberInputBox.ValueChanged`, it
   executes the assignment operand `self.work.payment = A4value` and returns
   no values. It does not call `setPayment` or `_setProperty` on this path.
4. Any other command is a no-op with no values.

`processAskResult(self,A1result)` takes the exact numeric `1` branch only. It
requests `_setProperty(nil,"Label_NumberInput","IsEnabled",false)` and then
dynamically calls `self:setAskResult(1)`. The owned method does not directly
store `askAnswer`; if the local setter is selected, its assignment operand is
`self.work.askAnswer = 1`, subject to native work application and readback.
Other results, including nil, false, zero, and true, do not enter this branch.

`processWaitCallFunction(self)` reads current `self.work.askAnswer` and tests
the readback with `~= -1`. A readback of nil, false, zero, `1`, `-3`, or any
other unequal value returns true; only a readback equal to numeric `-1`
returns false. `getAskResult(self)` reads the same current field and returns
one `-3` only for readback equal to numeric `-3`; all other readbacks tailcall
the selected `getPayment`. The local `getPayment` returns one current-field value, but
`TAILCALL` with `C=0` forwards the results of whichever getter dynamic
dispatch selects. It does not guarantee the selected getter reads current
payment or returns one value.

The `WidgetClose`/`Cancel` condition-request operands/calls emitted by `init`
do not prove framework dispatch or completed closure; a receiver or self-lookup
override can supply different semantics. The Lua body does not call close,
hide, destroy, or finalize, so these requests are not evidence that window
closure or destruction completed.
Opening `CommonDialogWidget` is not proof of dialog creation, display, a
delivered answer, or parent closure.

## Decisive original operands

The following locators summarize the branch and result evidence.

The root has arity `0` and code offset `0x20`. Root `pc 2/0x28`
(`CALL A=0 B=2 C=1`) calls `require` with `/Widget/WidgetBaseClass`; root PCs
`9/0x44`, `12/0x50`, `15/0x5C`, `18/0x68`, `21/0x74`, `24/0x80`,
`27/0x8C`, `30/0x98`, and `33/0xA4` issue method-binding `SETTABLE`
instructions for `init`,
`processUICommandEvent`, `processAskResult`, `processWaitCallFunction`,
`getAskResult`, `setAskResult`, `getPayment`, `setPayment`, and
`setRetainerData`, and root
`pc 34/0xA8` returns zero values. The decisive `init` assignments are
proto0 `pc 11/0x211 SETTABLE` for `_temp` and `pc 13/0x219 SETTABLE` for
`askAnswer`. Cancellation uses proto1 `pc 6/0x542 CALL A=6 B=3 C=1` to
dynamically call `setAskResult(-3)`.

| Method | Decisive original PC/offset and operand | Local implication |
| --- | --- | --- |
| Root/init | root `pc 6/0x38 CALL A=0 B=3 C=1`; proto0 `pc 19/0x231 CALL A=4 B=6 C=1`; `pc 69/0x2F9 CALL A=4 B=4 C=1`; `pc 70/0x2FD RETURN A=0 B=1 C=0` | Calls `_defineClass` with the class and base names, emits modal-property call operands, dynamically calls `setRetainerData`, returns no values. |
| `processUICommandEvent` | `pc 0/0x52A EQ` Cancel; `pc 2/0x532 EQ` WidgetClose; `pc 6/0x542 CALL A=6 B=3 C=1` cancel setter; `pc 8/0x54A EQ` Button; `pc 10/0x552 EQ` Operate; `pc 20/0x57A CALL A=6 B=8 C=1`; `pc 22/0x582 EQ` ValueChanged; `pc 25/0x58E SETTABLE`; `pc 26/0x592 RETURN A=0 B=1 C=0` | Cancel/close dynamically calls setter, Decide requests child helper with explicit receiver, ValueChanged uses payment assignment operand, no result. |
| `processAskResult` | `pc 0/0x6CE EQ A=0 B=256 C=1`; `pc 7/0x6EA CALL A=2 B=6 C=1`; `pc 10/0x6F6 CALL A=2 B=3 C=1`; `pc 11/0x6FA RETURN A=0 B=1 C=0` | Exact numeric 1 requests disable then dynamically calls setter; no result. |
| `processWaitCallFunction` | `pc 2/0x781 EQ A=1 B=1 C=258`; `pc 5/0x78D RETURN A=1 B=2 C=0`; `pc 7/0x795 RETURN A=1 B=2 C=0` | Compares current askAnswer readback to -1 and returns one boolean. |
| `getAskResult` | `pc 2/0x7EF EQ`; `pc 5/0x7FB RETURN A=1 B=2 C=0`; `pc 7/0x803 TAILCALL A=1 B=2 C=0`; `pc 8/0x807 RETURN A=1 B=0 C=0` | Returns -3 on exact readback, otherwise forwards the selected getter's results; no current-payment or fixed-width guarantee follows from this tailcall. |
| `setAskResult` | `pc 1/0x86D SETTABLE A=2 B=257 C=1`; `pc 2/0x871 RETURN A=0 B=1 C=0` | Assignment operand is `A1`; no result. |
| `getPayment` | `pc 2/0x8BE RETURN A=1 B=2 C=0` | Returns current payment-field readback as one value. |
| `setPayment` | `pc 1/0x909 SETTABLE A=2 B=257 C=1`; `pc 7/0x921 CALL A=2 B=6 C=1`; `pc 8/0x925 RETURN A=0 B=1 C=0` | Assignment operand precedes the UI property request; no result. |
| `setRetainerData` | `pc 5/0x9B8 CALL`; `pc 12/0x9D4 CALL`; `pc 18/0x9EC CALL`; `pc 21/0x9F8 CALL A=4 B=3 C=1`; `pc 22/0x9FC RETURN A=0 B=1 C=0` | Nickname/min/max requests precede dynamic `setPayment(0)`; no result. |

## Boundary of meaning

The body establishes Lua assignment operands, current-field reads, display
request arguments, and exact local branch predicates. It does not establish
who opened the widget, what entity the payment refers to, which currency or
balance is involved, whether the value is a withdrawal or proceeds amount,
any item or currency mutation, a server request, server acceptance, or
settlement. Those questions require an external caller and transaction
evidence and remain unestablished.
