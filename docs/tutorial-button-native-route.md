# Normal tutorial Button-to-Operate route

The published native Button path can conditionally supply the Operate command
consumed by the selected Getting Around and The Main Menu panels. If that
delivery invokes the published Lua methods on the selected tutorial receiver W,
the exact command comparison reaches `processUICommandOperate` and requests
base ask result 1. The supplied form declarations and registration request do
not establish an actual Button click or complete the instance binding.

This adopts existing static findings. The [panel completion contract](normal-tutorial-panel-completion.md#selected-operate-event-route)
owns the Lua continuation and its result, wait and closure boundaries. The
[module and opener contract](tutorial-widget-opening-contract.md#static-module-and-creation-relationships)
keeps `Ask/TutorialWidget` distinct from `widget/tutorialwidget.lua`.

## Selected declaration and registration

`xivl-client-data:docs/tutorial-normal-form-declarations.md`,
[Selected declarations](https://github.com/XIVLegacy/xivl-client-data/blob/b79709ec0abbc9ab323b47354cef79021ae46dff/docs/tutorial-normal-form-declarations.md#selected-declarations),
records exactly one `Button_OK` of type `Button` in each supplied
`TutorialWidgetK2/P2/K5/P5` form, with `Command="UILuaCommands.Operate"`
and `Content="@9095"`. Its scoped absence findings and the
[selected style declarations](https://github.com/XIVLegacy/xivl-client-data/blob/b79709ec0abbc9ab323b47354cef79021ae46dff/docs/tutorial-normal-style-declarations.md#local-property-scope-and-remaining-resolution)
establish no current focus, enabled, visibility or hit-test value.
`SkinFocused` and `SkinDisabled` remain raw condition strings. Neither
publication establishes the Button's stored CommandParameter record kind.

The selected Lua [button requests](normal-tutorial-panel-completion.md#button-requests-and-operation)
reach `setConfirmCondition(W,"Button_OK")`, whose published implementation
requests `W:_setUICommandCondition("Button_OK","UILuaCommands.Operate",5)`.
The native [UI command conditions](https://github.com/XIVLegacy/xivl-client-structs/blob/a4ab1843a64c5d5262dd6be1de20f55c1edcad55/docs/desktop-native-call-contract.md#ui-command-conditions)
marshal two strings and an int and resolve a receiver before registration.
The native consumer's [subscription gate](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#subscription-gate)
and [script entry](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#script-entry)
identify the number's low byte as event priority. Under that publication's
constant-byte inference, numeric 5 selects the Event form with priority 5.
It is not an event enum, a CommandParameter kind or a delivered event.

Registration must actually resolve the intended form and named control and
install a matching subscription. A plain registration uses the form root name
as template key. Delivery looks up the exact template, sender control and
command triple. A name in a raw form is not a native element identity, and a
registration request is not proof that this triple exists.
Template lookup outside a template and template-map expansion retain the
native publication's INFERRED status.

## Conditional native producer

The canonical native fact home is
`xivl-decomp:docs/resource/sqwt-command-parameter-consumer.md`. Its complete
contract and qualifications apply to this composition:

1. [Button mouse source](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#button-mouse-source)
   starts at delivered preview mouse events on a concrete native Button E,
   with interface I=E+0xB4. Base handlers run before the handled and current
   IsHitTestVisible gates. The down branch requires current ClickMode 1.
   The up branch requires current ClickMode 2 and the prior pressed-bit
   snapshot, with the published packed-state update gates. Constructor writes
   of ClickMode 2 and the hit-test value bit do not establish current values.
2. Click invokes a nonnull Command's slot 2 with the stored record at
   `[E+0x380]`, the conditionally selected target and Click arguments. There
   is no per-Click text formatting on this path. The target may differ from
   E or be null. The [destruction notification](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#click-destruction-notification)
   can stop later generic Click forwarding and supplies no universal
   surviving-object guarantee. An installed Click trigger is not required
   evidence for the default Command call and is not established here.
3. [Command name resolution](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#command-name-resolution)
   conditionally stores the name-selected command under holder metadata gates.
   Initializer `0x00F0F250` names `UILuaCommands.Operate` at `0x00FA8674`
   and constructs static object `0x0133B798` with table `0x0106A78C`, whose
   slot 2 is `0x00927FA0`. This supports the RoutedCommand join if lookup
   selects that object, or if fresh RoutedCommand construction succeeds.
   An arbitrary same-name lookup hit has no established implementation family.
4. [Executed event delivery](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#executed-event-delivery)
   raises PreviewExecuted, then Executed only if preview remains unhandled.
   Target, parent route, stop/handled bytes, actual store and handler attachment
   constrain delivery. Concrete Button forwarding to the base store is
   established. The wildcard form handler still requires its entry/form gates
   and exact subscription lookup. For the selected static Operate object,
   the published six-object per-frame debounce also applies.
5. A supported [record kind](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#kind-switch)
   selects the native parameter class. The installed actor/holder, supplied
   context eligibility, callback resolution and event admission must reach
   `_onUICommandEvent`. A subscription without a number selects
   `_onUICommandRequest` instead and does not supply this Event join.

These are conditional static edges. The complete native publication owns
target fallback, metadata and entry gates, handler ordering, priority admission,
[supplied-context eligibility](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#supplied-context-eligibility),
[event release and pending replay](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#event-release-and-pending-replay)
and [upstream control slot 4](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-command-parameter-consumer.md#upstream-control-slot-4).
Accepted native event parameters can still fail callback invocation. Active and
pending slots, matching release callbacks and a gated pump do not guarantee
eventual Lua delivery or a fixed frame interval. The context predicates are
not an ordinary widget lifetime or owner-liveness proof.

## Event operands and Lua continuation

Under the native parameter-class and successful callback conditions above,
counting W as position 0, the native script-entry push sequence gives:

| Lua operand | Supported role |
| --- | --- |
| A1 | Template name, or nil for an empty first string. A matching plain root-template registration takes the root variant and supplies nil. |
| A2 | Sender element's control name, with the root-name substitution `_widget`. It is `Button_OK` only when that named sender's subscription is the one dispatched, not merely because the original Click source was a Button. |
| A3 | Subscription command string matching the incoming command name. The selected join requires exactly `UILuaCommands.Operate`. |
| A4, A5 | Parameter-class values as below, without a tutorial-operation meaning. |

Kind 0 supplies no additional values. Kind 1 supplies its first stored signed
32-bit integer as A4. Kinds 2 and 3 supply their first and second stored signed
32-bit integers as A4 and A5; kind 3 drops its third stored integer. These are
field positions, not numeric value constants. Kind 8 supplies a string argument as
A4, without an arbitrary byte-preservation claim. Missing fixed Lua arguments
adjust to nil. Kinds 4-7 and above 8 supply
no call. The selected Button record is unresolved, so none of these cases
is selected here. Missing CommandParameter evidence is not an empty parsed
string or proof of kind 0.

`xivl-client-structs:docs/autotranslate-selection-contract.md`, AT-LUA-004,
and its [structured scriptEventForwardingTrace](https://github.com/XIVLegacy/xivl-client-structs/blob/a4ab1843a64c5d5262dd6be1de20f55c1edcad55/manifests/autotranslate_wire_format_study.json)
own the generic `_onUICommandEvent` forwarding of A1-A5 unchanged and its
surrounding thread-owner requests. These requests do not prove actual owner
state. The [selected Lua dispatch](normal-tutorial-panel-completion.md#selected-operate-event-route)
tests only exact A3 equality on this branch, then calls
`processUICommandOperate(W,A1,A2,A4,A5)`, omitting A3 and discarding results.
It does not test A2 against `Button_OK` or inspect A4/A5. If W resolves the
published tutorial handler and calls return normally, that handler makes the
published result-1 request regardless of the supported parameter variant.

The native form/actor relationship remains conditional, including the generic
consumer's inferred LuaActorImpl receiver. This composition does not identify
the actual Lua W, prove its inherited or override bindings, equate it with E
or authenticate its ownership/context. A supplied Operate callback on the
correct W can reach the Lua result request without proving its physical source.

## Evidence ceiling and source receipts

The remaining selected dependencies are the actual loaded form and Button E;
property application and current input state; selected Command implementation
and stored record kind; route/handler/subscription attachment and exact keys;
installed actor, supplied context and callback binding to W; and admission,
normal returns and scheduling. OS/hardware arrival, complete hit testing,
capture, focus and actual input acceptance remain outside this mouse scope.
Result storage/readback, widget closure and accepted tutorial progression remain
the separate [Ask poll and desktop wait boundary](normal-tutorial-panel-completion.md#composition-with-the-ask-poll-and-desktop-wait).

This adoption uses the following published source revisions and locators:

| Repository revision | Published contract and locator |
| --- | --- |
| `xivl-client-scripts` `1e63bfab1fcbd4499511dcf162d780942ed55ab7` | `docs/normal-tutorial-panel-completion.md`, Button requests and operation, Selected Operate event route, Input identities and original locators; `docs/tutorial-widget-opening-contract.md`, Static module and creation relationships. |
| `xivl-client-data` `b79709ec0abbc9ab323b47354cef79021ae46dff` | `docs/tutorial-normal-form-declarations.md`, Source identities and decoding, Selected declarations; `docs/tutorial-normal-style-declarations.md`, Local property scope and remaining resolution. |
| `xivl-client-structs` `a4ab1843a64c5d5262dd6be1de20f55c1edcad55` | `docs/desktop-native-call-contract.md`, UI command conditions; `docs/autotranslate-selection-contract.md` and `manifests/autotranslate_wire_format_study.json`, AT-LUA-004 / scriptEventForwardingTrace. |
| `xivl-decomp` `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce` | `docs/resource/sqwt-command-parameter-consumer.md`, Input and method and the linked producer, delivery and eligibility sections. |

The native source pins retail `ffxivgame.exe`, build `2012.09.19.0001`,
15996808 bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Addresses above are VAs at image base `0x00400000`. Form, style, Lua source,
LPB and decoded-payload identities remain in their cited canonical contracts.
The result is an existing-finding composition, with no new binary, resource,
source-body or live-client reproduction.
