# Normal tutorial panel completion

The selected Ask tutorial panels, Getting Around (infoID 2) and The Main Menu
(infoID 5), initialize the same confirmation button. Their operate handler
requests base ask result 1 after hiding the button grid and requesting an
animation. It does not test movement, a menu action or the operation argument.
If the published Ask setter and later poll apply to the same widget and the
result read is 1, that poll reports finished. Neither selected handler closes
the widget, and the desktop opener discards the selection outcome.

These are local contracts of `widget/ask/tutorialwidget.lua`, conditional on
the selected instance resolving the named implementations. The distinct
`widget/tutorialwidget.lua` is not this module. The existing
[module and opener contract](tutorial-widget-opening-contract.md) owns path
selection, stored-controller replacement and creation. The
[normal city comparison](opening-normal-tutorial-city-contracts.md) owns the
final calls: Gridania requests lesson 5, while Limsa and Ul'dah request lesson 2.

## Initialization and selected text branches

Let W be the tutorial receiver, t its supplied controller operand and i its
supplied infoID. `initAsk(W,t,i)`, canonical source lines 11-75, declares
`work.infoID` as `integer8` and `work.autoAnim` as `boolean`, requests
`infoID=i` and `autoAnim=false`, then makes these requests in order:

1. `setModal(W,false)`.
2. `setProperty(W,"IsHitTestVisible",false)`.
3. `setDrag(W,false)`.
4. `setUICommandCondition(W,"UILuaCommands.Shown")`.
5. For t exactly numeric 2, `setTextPad(W,i)`. For t exactly numeric 1,
   `setTextKeyboard(W,i)`. Other values take neither text branch.
6. `setVisibility(W,"TextBlock_Text_2",false)`.

Each call discards its results. The initializer returns zero values. Its
dispatch uses the supplied i directly, rather than reading back the declared
`integer8` field. The declaration and assignments do not prove native storage,
coercion, modal state, focus, hit testing or rendered visibility.

The selected dispatcher branches compare i with numeric 2 and 5. A string
`"2"` or `"5"` does not select either numeric branch. Each selected call
supplies only W and discards all results. The reached text methods are:

| infoID | Pad / Keyboard methods and canonical source | Ordered text prerequisites and requests |
| --- | --- | --- |
| 2 | `setTextPad2`, 419-450; `setTextKeyboard2`, 972-1003 | Fetch one player result from `worldMaster:_getMyPlayer()`, obtain one `getInitialTown()` result from that fetched receiver, then request exactly three results from `W:getTutorial2TownNPC(town)`. Set title key 9006 and `TextBlock_Text_1` key 9008 for Pad or 9009 for Keyboard, forwarding those three results in order. Then call `W:initWidgetWithButton()`. |
| 5 | `setTextPad5`, 527-544; `setTextKeyboard5`, 1080-1097 | Set title key 9021 and `TextBlock_Text_1` key 9023 for Pad or 9024 for Keyboard. Then call `W:initWidgetWithButton()`. |

The text calls discard all results, and these four methods return zero values.
The Getting Around player lookup is fresh in each reached text method. It is
not established to equal a player supplied to a city scenario. Its town and
three helper results are opaque prerequisites here, without a town, NPC,
formatting-domain or rendered-text interpretation. If an earlier call does
not return normally, the later button initialization is not reached.

## Button requests and operation

`initWidgetWithButton`, source 1765-1781, requests `setModal(W,true)`, then
`setProperty(W,"Focusable",true)`, then `enableButtonGrid(W)`. This follows
the initializer's earlier false modal request when the selected text path
reaches the local implementation. It does not assign `autoAnim=true`.

`enableButtonGrid`, source 1801-1819, makes three ordered requests:

1. `setConfirmCondition(W,"Button_OK")`.
2. `setContent(W,"Button_OK",9095)`.
3. `setVisibility(W,"Grid_Button",true)`.

The actual inherited `setConfirmCondition`, in
`widget/widgetbaseclass_common.lua:1312-1322`, forwards the supplied control
name as `W:_setUICommandCondition(control,"UILuaCommands.Operate",5)` and
returns zero values. Thus the selected registration request names
`Button_OK`, `UILuaCommands.Operate` and numeric 5. The static require chain
is Ask tutorial -> `/Widget/Ask/AskBaseClass` -> `/Widget/WidgetBaseClass` ->
`/Widget/WidgetBaseClass_common`. The Ask base declares `WidgetBaseClass`
as its parent. These source relationships and the helper's root closure
binding do not establish runtime method resolution or delivered UI commands.
The native condition request is the boundary of this registration trace.

`disableButtonGrid`, source 1822-1831, requests only
`setVisibility(W,"Grid_Button",false)`. It does not remove the registered
condition or call a button input-enable setter. The helper names alone do
not establish input acceptance or enforcement. Both grid helpers and the
button initializer discard call results and return zero values.

If `processUICommandOperate`, source 78-102, is actually invoked on W and
its calls return normally, it makes these requests in order:

1. `setModal(W,false)`.
2. `disableButtonGrid(W)`, whose local implementation requests the hidden grid.
3. `sendCommand(W,"UILuaCommands.AnimationStart")`.
4. `setProperty(W,"Focusable",false)`.
5. `setBaseAskResult(W,1)`.

It discards every call result and returns zero values. There is no local
comparison of a control name, operation argument, infoID, controller,
visibility, prior result or `autoAnim`. Registration/enabling is therefore
not an internal guard on this handler. Joining Button_OK's registration to
this invocation requires actual command delivery, which is not established
by either method. A repeated invocation has the same local requests.

`processUICommandDefault`, source 105-124, compares its fourth fixed argument
(counting W) with the exact string `UILuaCommands.Shown`. Only for that command
does it read `W.work.autoAnim` afresh. A truthy read requests
`sendCommand(W,"UILuaCommands.AnimationStart")`. False or nil skips that
request; numeric zero is truthy in Lua and takes it. The method discards the
send result and returns zero values on every normal path. It writes no ask
result. With the initializer's false value read back unchanged, Shown alone
does not request animation. Actual storage, later writes and command delivery
remain conditions, and the animation request does not prove animation start
or completion.

Neither selected handler calls close/destroy, writes -1, registers a cancel
condition or waits for an animation result. The default handler takes no
action for `UILuaCommands.Cancel`. These absences describe the selected local
methods, not every inherited or external close/cancel path.

## Composition with the Ask poll and desktop wait

The published [Ask result contract](ask-widget-result-state.md) owns the
setter and poll. Conditional on that implementation, `setBaseAskResult(W,1)`
first requests input disablement only when its fresh `inputControlFlag` read
is exactly Boolean true, then assigns 1 to `askWork.askResult`. A later poll
returns true exactly when its own result read differs from numeric zero.
A successful readback of 1 therefore finishes that poll, without identifying
a physical action, animation completion, close or accepted tutorial outcome.
Nil and false also differ from numeric zero. The published
[native no-storage case](https://github.com/XIVLegacy/xivl-client-structs/blob/c7188343bf5d18984e171f89b63f6adbac66fc63/docs/work-binder-native-contract.md#an-object-without-storage)
can yield nil, so a finished poll alone does not authenticate this setter
request or its storage. Neither base helper closes the widget.

Both selected infoIDs take the opener's
[creation and selection wait branch](tutorial-widget-opening-contract.md#complete-opener-partition).
It replaces the supplied controller with the desktop's stored controller,
requests `Ask/TutorialWidget`, and keeps only the first opening result W.
An exact nil result skips selection and focus restoration. False or zero
would pass the non-nil test without local widget validation.

For a non-nil result, the published
[selection helper](gridania-opening-tutorial-contract.md#selected-widget-calls)
uses a nil timeout. While its widget is alive it polls
`processWaitCallFunction`, ending when that callback returns exactly true.
Otherwise it waits 0.1 and retries. Loss of widget life yields false. There
is no fixed local timeout. Actual life reads, scheduling, callback resolution
and same-widget identity are required to connect this wait to the panel's
result request.

After selection returns normally, the opener discards its outcome and
calls the desktop
[focus helper](tutorial-widget-opening-contract.md#conditional-return-to-desktop-focus-request),
even for a false selection result. The helper's exact-nil and Lua-equality
guards can omit the native-named setter request. The opener
reads no `getAskResult`, closes no widget and returns zero values. Thus the
city method's following final mask and cleanup can follow a nil opening
result or an alive-loss selection outcome as well as a finished Ask poll.
Those outcomes do not prove movement, use of the main menu, native focus,
closure or accepted progression. The three city contracts establish no
additional local close after their final lesson and return the local device
selection result, not a panel answer.

## Input identities and original locators

The extraction is retail 1.23b `2012.09.19.0001`. The retained archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). Selected
canonical members matched [scripts.json](../manifests/scripts.json), and
their original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json). Canonical
source normalization replaces CRLF pairs with LF only. The Ask base's result
methods and shared desktop helpers are adopted from their linked publications.
The base-module inspection covers the static require relationship, the actual
`setConfirmCondition` definition and binding, and the bounded getter/load
contract below.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `lua/scripts/widget/ask/tutorialwidget.lua` | 34132 | `73980DDC53C4DF37A35537020B0DFED620D090F281CA3084BB19CEFB73817D4F` |
| Its LPB, `client/script/n1635q/9rz/qpqvs19yn1635q.le.lpb` | 17472 | `C5B9A018DF9EFA68DF14905A15CF54B88E7158C0A5B6ED822F13AB72B3B3ECEB` |
| Its decoded Lua 5.1 payload | 17459 | `4A86F0F7F6B71F8E6C8C010F9058FB153C7FA1595354EE212B7871FD2EB7E846` |
| `lua/scripts/widget/widgetbaseclass_common.lua` | 69077 | `2057F6A4A94071BF8C9F2FA697BC0571B47DA14A6BC4919A6D5491005417800F` |
| Its LPB, `client/script/n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 | `C549F746370366F9827570EE22201516E07A05D91829CA643A2E2EC0C73BCF3C` |
| Its decoded Lua 5.1 payload | 32983 | `7C45426B1A9F168557D84E420C5767C6FDEA4ABF90B976B276546AF4E6A5DE5F` |

The required-module source pins are
`ask/askbaseclass.lua`: 2633 bytes, SHA-256
`642F3112D4663004FDC0B79DAF0A5FAF8B7588EAD58D2CD8E6747821BDA54ADB`,
and `widgetbaseclass.lua`: 8518 bytes, SHA-256
`737A53B0472B510440735CF19A1D0A11FD100E69DF7F3EAB1178969A3D57B95C`,
both under `lua/scripts/widget/`. Their separate LPB and payload pins remain
in the coverage manifest. Selected authentication is not full-corpus
reproduction or a live tutorial observation.

PCs below are one-based, child indices zero-based, and code starts are decoded
payload byte offsets without the LPB wrapper. Each root binding PC assigns
the named child closure. Source paths are relative to `lua/scripts/`.

| Ask tutorial method | Root binding PC | Child / code start | Decisive PCs |
| --- | ---: | --- | --- |
| `initAsk` | 10 | 0 / `0x7A4` | 14/16 request infoID/false; 19/23/26/29 common calls; 31/38 exact controller comparisons; 35/42 text calls; 49 hides second text; 50 zero-value return. |
| `processUICommandOperate` | 13 | 1 / `0x9B6` | 3/5/8/12/15 modal, grid, animation, focus and result calls; 16 zero-value return. |
| `processUICommandDefault` | 16 | 2 / `0xAB5` | 2 compares fourth argument; 5 reads autoAnim; 6 truthiness test; 10 animation request; 14 zero-value return. |
| `setTextPad` / `setTextKeyboard` | 19 / 22 | 3 / `0xB79`; 4 / `0xF3A` | 8/26 compare 2/5; 11/29 invoke the respective selected text methods with `B=2,C=1`. |
| `setTextPad2` / `setTextKeyboard2` | 28 / 82 | 6 / `0x140D`; 24 / `0x27F1` | 3/5 fresh player/town calls `C=2`; 8 helper call `C=4`; 12/19 text calls; 21 button init; 22 zero-value return. |
| `setTextPad5` / `setTextKeyboard5` | 37 / 91 | 9 / `0x17C1`; 27 / `0x2BA5` | 4/8 text; 10 button init; 11 zero-value return. |
| `initWidgetWithButton` | 157 | 49 / `0x41ED` | 3/7/9 modal/focus/grid calls; 10 zero-value return. |
| `enableButtonGrid` | 163 | 51 / `0x431E` | 3 confirmation; 7 content; 11 visibility; 12 zero-value return. |
| `disableButtonGrid` | 166 | 52 / `0x43DB` | 4 visibility; 5 zero-value return. |

In `widget/widgetbaseclass_common.lua`, root PC171 binds child 56 to
`setConfirmCondition`, code start `0x432F`. PC5 calls the native-named method
with `B=5,C=1`, and PC6 returns zero values. In the Ask base and Widget base,
root PC3 requires the next module named above. The Ask base's root PC7
declares its parent relationship.

Reproduction uses `tools/retail_script.py:decode_lpb` and the fixed Lua 5.1
reader and instruction decoder in `tools/build_quest_contracts.py`. Parse
each payload completely, bind selected root closures, and follow actual
comparisons, jumps, call operands and return widths. Check controller and
infoID equality, fresh player/town reads and three-result adjustment, ordered
button registration/visibility requests, the unguarded operate result 1,
Shown/autoAnim truthiness and zero-value returns. Instruction mutations to
these guards, scalar/visibility operands and call/return widths must be
rejected. Mock helper results qualify local instruction behavior and are
not observed client results. Retain identities and semantic assertions,
without source bodies, payloads or instruction listings.

## Selected Operate event route

For the selected normal panels, the shared Lua dispatch adds an exact command
comparison before the unguarded tutorial operation. It adds no local focus,
work-field or prior-result test on that path. This is a conditional source
join, requiring W to resolve the published `_onUICommandEvent`, shared
`processUICommandEvent` and tutorial `processUICommandOperate`, with preceding
calls returning normally.

Counting W as position 0, let A1 through A5 be the five event operands after
W, with A3 the command.
The published
[AT-LUA-004 forwarding contract](https://github.com/XIVLegacy/xivl-client-structs/blob/8ee5be22e27b63b0442d4a413d584238796a744c/docs/autotranslate-selection-contract.md)
and its
[structured record](https://github.com/XIVLegacy/xivl-client-structs/blob/8ee5be22e27b63b0442d4a413d584238796a744c/manifests/autotranslate_wire_format_study.json)
own `_onUICommandEvent`'s unchanged forwarding of A1 through A5 and surrounding
thread-owner requests. In `widget/widgetbaseclass_common.lua`, canonical
source 395-405, the first dispatch branch compares A3 with the exact string
`UILuaCommands.Operate`. On equality it calls
`processUICommandOperate(W,A1,A2,A4,A5)`: the command is omitted, while the
other four operands retain their order and identity. The call discards all
results and reaches a shared zero-value return. It does not compare an event
operand with `Button_OK`. No semantic meaning is assigned here to A1, A2, A4
or A5. A command mismatch leaves this selected branch; the other branches are
outside this check.

This additional original-bytecode check uses the common-module source, LPB
and payload identities above. Root PC42 binds child 13 to
`processUICommandEvent`, code start `0x26E6`, with six fixed parameters.
Its PC2 command comparison selects the PC9 call with `B=6,C=1`, supplying
five operands including W. PC10 jumps to the shared PC198 return with `B=1`.
The first command-miss target is PC12. These PCs are one-based. Canonical
source locators are separate from original prototype debug-line metadata.
Bounded semantic checks preserve the four operand identities, discard helper
results and stop mismatches at that first target. Mutations to the command,
comparison polarity, forwarded operand, call widths, exit target and return
width are rejected.

This connects a supplied Operate command to the local result-1 request only
under those receiver and normal-return conditions. It does not authenticate
a native event producer, actual receiver or override selection, global object
identity, thread scheduling/state or condition enforcement. The published
[native condition contract](https://github.com/XIVLegacy/xivl-client-structs/blob/8ee5be22e27b63b0442d4a413d584238796a744c/docs/desktop-native-call-contract.md#ui-command-conditions)
owns registration marshalling; numeric 5 remains a registration argument,
without an event-enum interpretation here. Neither the conditional Lua join
nor registration establishes a delivered event, physical click, movement,
menu use, applied native state, widget closure or accepted progression.

## Getting Around format operands

The selected `getTutorial2TownNPC(W,town)` helper returns three values with
these local numeric comparisons:

| `town` input | First result | Second result | Third result |
| --- | ---: | ---: | ---: |
| numeric 1 | 1600150 | 1 | 1 |
| numeric 2 | 2300120 | 2 | 1 |
| numeric 3 | 1100003 | 2 | 1 |
| default path | 0 | nil | nil |

The comparisons are exact Lua numeric equality. String `"1"`, Boolean true
and nil do not select the numeric-1 branch. The default returns three values,
including its two nils. The body makes no call or external field read/write.
These are formatting operands, without a town-name, NPC-identity, grammatical,
quantity or text-rendering interpretation assigned here.

The original helper is `root/proto41`, decoded code offset 15083, 30 words,
with two fixed parameters including W; root zero-based PC132 binds it to
`TutorialWidget.getTutorial2TownNPC`. It uses the same authenticated Ask
tutorial source, LPB and payload as the selected callers above. Both info2
text methods request exactly three helper results and forward them after
text key 9008 for Pad or 9009 for Keyboard. This maps the local values while the
actual fresh town value, receiver/method binding, native/provider state,
formatter meaning, locale and rendered lesson remain unproved.

## Selected text-property request

For the two info2 text calls above, the inherited wrappers request
`_setTextProperty(W,nil,"TextBlock_Text_1","Text",key,R1,R2,R3)`, where key
is 9008 for Pad or 9009 for Keyboard and R1 through R3 are the helper results.
The wrappers preserve all three operands, including nils, and return zero
values. This composition requires the selected method bindings, normal
prerequisite completion and the `type` call reporting `"number"` for the key.
Only that numeric-key branch of `setTextProperty` is included here.

The source methods in `widget/widgetbaseclass_common.lua` are `setText`,
`root/proto89`, decoded code offset 21514, seven words; `setItemText`,
`root/proto91`, offset 21697, eight words; and `setTextProperty`,
`root/proto182`, offset 32430, 29 words. The last method's selected original
path is zero-based PCs 0-14 and shared zero-value return PC 28. Its alternate
property paths at PCs 15-27 were excluded. The same common-module source,
LPB and payload identities used above apply.

The published native contract at
`xivl-client-structs:docs/widget-native-call-contract.md`, `_setTextProperty`,
at revision `8ee5be22e27b63b0442d4a413d584238796a744c`,
owns the declared arguments and encoding: a nonnil identifier starts `@`
and the identifier, integers append `/i` and their values, strings append
`/s` and their values, and the first Nil ends the scan. Given the corresponding
typed native frame, a matched town tuple therefore contributes three integer
format operands; the default tuple contributes integer 0, then stops at its
first nil. This is an adoption of that native contract, not a new native trace.

The selected source request and conditional encoding do not establish the
actual native frame, selected receiver/control or text-data namespace,
physical provider/table, formatter meaning, applied property or rendered text.

## Initial-town getter and declaration

The selected `PlayerBaseClass.getInitialTown(P)` reads
`P.playerWork.initialTown` and returns exactly one value when the lookups
complete normally. The getter has no conversion, default or additional
predicate. Its original definition is `root/proto6`, decoded code offset
3710, four words, in `chara/player/playerbaseclass.lua`.

That canonical source has SHA-256
`6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4`.
Its original LPB is `client/script/729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`,
SHA-256 `32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e`;
decoded-payload SHA-256
`1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`.
These identities matched the same script and retail resource manifests used
above, with the selected archive member and LPB decoded in memory.

The existing native declaration in
`xivl-client-structs:docs/work-binder-native-contract.md`, Declared work of a
MyPlayer / playerWork, at revision
`c7188343bf5d18984e171f89b63f6adbac66fc63`, lists
`playerWork._sync.initialTown` as `integer8`. This adopts the declaration
without establishing that the getter's field uses that layout or storage.
The declaration and getter do not assign
city names to numeric values or establish this player's value. The literal
town-code format table above remains conditional on the actual read and
selected method/helper bindings.

## Form-name and declaration boundary

The declared inherited `WidgetBaseClass.getFormName(W)` returns exactly one
nil. It makes no call, field read or alias transformation. Its canonical
source is `widget/widgetbaseclass_common.lua:182-187`, including the binding.
The original is `root/proto2`, code start `0x2019`, two words, with one fixed
parameter and no varargs. Zero-based root PCs 7/8 create and assign its
closure. Its first instruction returns the initially nil register with
`B=2`; the following zero-value return is unreachable on normal entry.
The common-module source, LPB and decoded-payload identities above apply.

`WidgetBaseClass.loadFormData(W,N)`, in
`widget/widgetbaseclass.lua:190-201`, requests `W:_setFilename(N)`, then
`W:_loadForm()`. It forwards its second fixed argument unchanged, including
nil, false or zero if supplied. It discards both call results and returns
zero values. The original is `root/proto3`, code start `0x87F`, six words,
two fixed parameters and no varargs. Zero-based root PCs 13/14 create and
assign its closure. Calls at child PCs 2/4 have `B=3,C=1` and `B=2,C=1`,
respectively; PC5 returns with `B=1`. These are native-named requests, without
a claim about marshalling, filename storage or successful loading.

The base source identity above applies. Its LPB is
`client/script/n1635q/n1635q89r57y9rr.le.lpb`, 4080 bytes, SHA-256
`aad807a42296e93301582defc8f15e4003b8093af672794282cd54950cc556ad`.
Its decoded payload is 4067 bytes, SHA-256
`11e5bab509c4dbbd7e2767d35cdf132a59b5c510c32c2e215f83cac713115140`.
Both matched the same coverage manifest. Complete parsing, selected source
assertions, root bindings, exact call/return widths and rejecting operand
controls qualify these eight words.

Adopting the declared Ask inheritance and completed opener/alias contract
does not connect `TutorialWidgetK2/P2/K5/P5` to N. The exact missing edge is
the producer/adaptor supplying `loadFormData`'s second argument from the
selected opener alias or another form-name value. The nil getter and the
load wrapper do not supply it. The published resolver at
`xivl-decomp:docs/resource/sqwt-form-locale-resolution.md`, Lua entry and The
opener, applies only after the actual filename argument, loader state and
locale/root are established. No adjacent initializer/helper is included here.

`xivl-client-data:docs/tutorial-normal-form-declarations.md`, Selected
declarations and Template reference and source ceiling, canonically owns the
four supplied files' raw text/control declarations and identities. Their
named controls and button command/content are statically compatible with the
published text/button requests above. Matching declarations establish no active
form, native lookup/cache hit, applied property/binding, delivered Operate
event, rendered text or accepted tutorial outcome. The same page retains the
unread style/provider dependency; no further dependency or native body was
traced.
