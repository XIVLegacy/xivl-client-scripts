# Player trade lifecycle

The retail 1.23b Lua corpus separates a player-trade invitation, the trade
window's local edit loop, synchronized trading-item presentation, and the
commands that carry UI replies. The scripts establish client ordering and
arguments. They do not establish server validation, inventory locking,
ownership transfer, persistence, or atomic completion policy.

## Invitation and confirmation

Static system command 24217 is `TradeOfferCommand`, 24218 is
`TradeExecuteCommand`, 24230 is `TradeOfferCancelCommand`, and 24305 is
`ConfirmTradeCommand`. The command identities come from
`xivl-client-data:manifests/staticactor_class_paths.json`.

`TradeOfferCommand.canFire` and `TradeOfferCancelCommand.canFire` have the same
client preconditions: the source is MyPlayer, a target exists and is alive,
both actors are living, and the source is not in active mode. These checks are
UI command availability, not authoritative trade eligibility.

Trade relation group 50002 synchronizes `host` and `variableCommand` through
work bindings 200001 and 200002. A non-host member exposes the synchronized
command variation and host display name through
`PlayerBaseClass.getConfirmTradeCommandVariation`. The console tray displays
that invitation and opens ask-widget mode 4. `ConfirmTradeCommand.canFire`
compares its argument directly with the synchronized variation, with no nil
guard; two nil values also compare equal. Its separate `isEnabled` method
requires the current variation to be in 30000-39999, and its recovered `fire`
method returns false. Therefore this corpus proves the invitation presentation
and comparison, but not the native command dispatch or the server response
that creates or removes the trade relation.

The same console tray exposes command 24230 while a target is in the
during-offer state and command 24217 when the target is offerable. Those target
predicates and the command labels are presentation gates, not proof of a
server-side invitation state machine.

Evidence: `lua/scripts/command/system/tradeoffercommand.lua`,
`lua/scripts/command/system/tradeoffercancelcommand.lua`,
`lua/scripts/command/system/confirmtradecommand.lua`,
`lua/scripts/chara/player/playerbaseclass_cliprog.lua`,
`lua/scripts/group/relationgroup/traderelationgroup.lua`, and
`lua/scripts/widget/consoleicontraywidget.lua`.

## Tray command boundary

`TradeExecuteCommand` cannot be fired as an ordinary client-selected command.
Its named methods instead bridge the native system-command runtime to the
desktop widget:

| Callback | Client effect |
|---|---|
| `processTradeCommandOpenTray` | Opens modal `TradeWidget` in desktop slot 4 and waits for creation. |
| `processUpdateTradeCommandTrayData` | Polls one completed widget operation and decodes the recovered arguments. |
| `processTradeCommandReply` | Converts a reply string into one widget notice code. |
| `processTradeCommandCloseTray` | Requests closure of `TradeWidget`. |

The address-confirmed native route joins static actors 24217 and 24230 to the
generic c2s `0x012D` EventStart path. Preserved captures contain 126 `0x012D`
subpackets of 216 bytes: a 200-byte body, including a 16-byte game-message
prefix and 184-byte application payload. This is a bounded command-start join;
no trade-specific field layout is recovered.

The native event-function route joins static actor 24218 to generic s2c
`0x0130` RunEventFunction. The function name and Lua arguments are selected at
runtime. Preserved captures contain 200 `0x0130` subpackets of 176 bytes, with
a 160-byte body and 144-byte application payload. This directly bounds the
server-to-client callback carrier; no fixed trade payload or sequence is
assigned.

Generic c2s `0x012E` EventUpdate is an address-confirmed event route and appears
200 times in the retained corpus as 120-byte subpackets with a 104-byte body.
No direct evidence maps the widget operations below to `0x012E`, however, so
it remains only a candidate outgoing carrier. The update callback is the last
recovered Lua boundary for an outgoing edit, and the reply callback is the
first recovered Lua boundary for an incoming result.

Evidence: `lua/scripts/command/system/tradeexecutecommand.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`,
`xivl-client-structs:manifests/trade_message_routing.json`,
`xivl-opcodes:opcodes.json`, and
`xivl-captures:derived/observations.json`.

## Local offer editing

`TradeWidget` presents four destination slots 1-4 and four local source slots
5-8. Each slot stores three local UI values in `IntData.Value0..2`.
`TradeEditWidget` supplies item or gil selections, while `TradeWidget` records
the pending operation in temporary work.

The stable `TradeWidget.getAskResult` result map is:

| Operation | UI source | Returned arguments after the operation code |
|---:|---|---|
| 1 | Remove the locally reserved source slot | source slot index 1-4 |
| 2 | Clear all local source slots | 0 |
| 3 | Add an inventory item | source slot index, package, item index, stack |
| 4 | Add gil through temporary package 100 | source slot index, package 100, item index, stack |
| 11 | Cancel trade | none; trailing values are nil |
| 12 | Mark the local offer fixed/ready | none; trailing values are nil |
| 13 | Return to editing | none; trailing values are nil |

Item selection records `chosenPackage`, `chosenItem`, and `chosenStack`, then
copies `chosenSlot` into `reservedSlot`. Gil selection uses the first empty
local source slot and operation 4. The widget rejects another slot edit while
`reservedSlot` is nonzero. This is a local in-flight UI reservation only; it
does not prove that the inventory item or gil is locked by the client or
server.

The retail bytecode preserves the complete operation 3/4 tuple across
`DesktopWidget.checkReplyTradeWidget`. Its ready path returns `true` followed
by all five `TradeWidget.getAskResult` values. The command callback receives
ready, operation, slot, package, item index, and stack. The two-result capture
and three-value return in the canonical decompiled connector are a decompiler
defect. The [retail return-arity finding](#retail-return-arity) establishes this
boundary directly from instructions and registers.

The widget does not immediately install the selected item into its own slot
model. The polling path exposes the full operation at the native command boundary.
A later trading-item callback obtains the synchronized item
with `_getTradingItem` and updates either the local source presentation or the
other player's destination presentation. A nil item clears the displayed
slot. The local callback also clears `reservedSlot` when the corresponding
slot update arrives.

Catalog ID 1000001 is rendered as gil. The widget calculates the displayed gil
totals from synchronized slot items and uses `_isTrading` for the displayed
stack quantity. This presentation does not establish a currency debit or
credit.

Evidence: `lua/scripts/widget/tradewidget.lua`,
`lua/scripts/widget/tradeeditwidget.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`, and
`lua/scripts/command/system/tradeexecutecommand.lua`.

## Retail return arity

The inputs are the retail 1.23b resources identified by the
`decodedScriptPath` rows below in
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
Each original LPB's size and SHA-256, and each decoded payload's size and
SHA-256, matched that row. The ciphered paths also matched the corresponding
[`lua/registry.json`](../lua/registry.json) entries after the documented suffix
conversion. Those records own the exact input identities.

| Decoded script under `lua/scripts/` | Resource under `client/script/` |
|---|---|
| `widget/tradewidget.lua` | `n1635q/qs965n1635q.le.lpb` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` |
| `command/system/tradeexecutecommand.lua` | `7vxx9w6/rlrq5x/qs9655m57pq57vxx9w6.le.lpb` |

Method: decode the LPB wrapper with `tools/retail_script.py`, parse the Lua
5.1 chunk header and prototype arrays, and extract opcode/A/B/C fields from
the little-endian instruction words. Match each method's top-level `SETTABLE`
key to its preceding `CLOSURE` child index. Check the result against the pinned
unluac `--disassemble` output. Prototype indices and registers below are
zero-based, PCs are one-based within each prototype, and byte offsets are
zero-based within the decoded chunk, including its header.

| Method | Root child prototype | Root closure / assignment PCs | Decisive prototype PCs and operands |
|---|---:|---|---|
| `TradeWidget.getAskResult` | 31 | 102 / 103 | 49 and 67: `RETURN A=2 B=6`, five results from R2..R6 for operations 3 and 4. |
| `DesktopWidget.checkReplyTradeWidget` | 216 | 650 / 651 | 17: `CALL A=4 B=2 C=0`; 18: `RETURN A=3 B=0`, all call results after the ready flag. |
| `TradeExecuteCommand.processUpdateTradeCommandTrayData` | 4 | 21 / 22 | 5: `CALL A=3 B=3 C=7`, six results into R3..R8. |

The widget's operation 3 branch places operation, `reservedSlot - 4`,
`chosenPackage`, `chosenItem`, and `chosenStack` in R2..R6 at PCs 41-48.
Operation 4 uses the same positions at PCs 60-66, with package 100 in R4.
Their return instructions are at decoded offsets `0x4C81` and `0x4CC9`.

The connector places `true` in R3 at PC 15, selects `getAskResult` at PC 16,
and calls it at PC 17 (offset `0x1ABE7`). In Lua 5.1, `CALL C=0` keeps all
results and sets the dynamic stack top. PC 18 (offset `0x1ABEB`) uses
`RETURN B=0` to return R3 through that top, yielding six values here. Its
`maxstacksize=6` does not limit the open result count. The early missing-widget
and waiting paths return one nil or false value at PCs 8 and 14.

The command's call at PC 5 (offset `0x57D`) receives ready in R3, operation in
R4, slot in R5, package in R6, item index in R7, and stack in R8. For operation
3, PCs 35-38 use R6/R7 for `_getExtendedTemporaryItem`. PCs 96-103 return
stack and the current package/item values in the callback's final seven-value
result. Operation 4 replaces R6/R7 with the gil lookup's package/item values
before that return.
The interpretation follows Lua 5.1
[`lopcodes.h`, `OP_CALL`/`OP_RETURN`](https://www.lua.org/source/5.1/lopcodes.h.html),
[`lvm.c`, `luaV_execute`](https://www.lua.org/source/5.1/lvm.c.html), and
[`ldo.c`, `luaD_poscall`](https://www.lua.org/source/5.1/ldo.c.html).

The [pinned decompiler](../tools/vendor/unluac/PROVENANCE.json) reproduced all
three canonical script bodies byte-for-byte against
[`manifests/scripts.json`](../manifests/scripts.json), including the connector's
incorrect fixed two-result capture. The canonical corpus remains a reproduction
artifact. Use this finding for its retail return semantics. The owning
[`regression check`](../tools/tests/test_player_trade_lifecycle.py) keeps corpus
fidelity separate from an explicit local LPB arity check, documented in
[tools](../tools/README.md#player-trade-return-arity).

This is static bytecode evidence for these pinned resources under Lua 5.1
instruction semantics. It establishes no live client session, runtime method
replacement, native packet route, server acceptance, or ownership transfer.

## Reply and readiness ordering

The command reply strings map to widget notices as follows:

| Reply | Notice | Client transition |
|---|---:|---|
| `set` | 103 | Clear the reservation and leave selection mode. |
| `back` | 101 | Leave selection mode. |
| `fix` | 112 | Set local `sourceFix`. |
| `targetfix` | 90 | Set remote `destinationFix`. |
| `reedit` | 91 | Clear remote `destinationFix`. |
| `doedit` | 113 | Leave selection mode and clear local `sourceFix`. |
| `noabort` | 211 | No recovered state change. |
| `noreedit` | 213 | No recovered state change. |
| `cantset` | 203 | Clear reservation and selection mode. |
| `cantback` | 201 | Clear reservation and selection mode. |

The unused `nosplit` and `failed` branches produce no widget notice. Notice
204 and 205 leave selection mode; 206 also clears the reservation. Notice 212
has no recovered state change. These notice codes are client callback values,
not packet subopcodes.

Pressing OK yields operation 12 only when no selection or clear is in flight
and the local offer is not already fixed. Reply `fix` then sets `sourceFix`.
The other participant's readiness arrives separately as `targetfix`. The
widget considers the presentation finished only when both `sourceFix` and
`destinationFix` are true; most edit and update handlers then stop processing.
This order proves two-sided readiness presentation. It does not prove that
either readiness flag authorizes an ownership transfer or that both flags are
the server's atomic commit condition.

Pressing Reedit yields operation 13. Reply `doedit` clears local readiness;
reply `reedit` clears remote readiness. A synchronized counterparty item update
also schedules operation 13 automatically when local `sourceFix` is already
true, so the local side requests re-edit after a remote offer change. Pressing
Cancel yields operation 11. The corpus does not show which reply, relation
update, or packet follows a successful cancellation or completion.

Evidence: `lua/scripts/widget/tradewidget.lua` and
`lua/scripts/command/system/tradeexecutecommand.lua`.

## Closure and authority boundary

`processTradeCommandCloseTray` calls `DesktopWidget.closeWidget` for desktop
slot 4 and `TradeWidget`. `TradeRelationGroup._onFinalize` only refreshes the
confirm-trade command variation. The recovered Lua does not explicitly unlock
items, transfer ownership, persist inventory, clear a server transaction, or
distinguish cancellation closure from successful-completion closure.

The strongest supported client order is synchronized invitation variation ->
confirmation presentation -> native open callback -> local operation polling
-> native replies and synchronized item callbacks -> separate local and remote
fixed notices -> native close callback and relation finalization in an
unrecovered order. The native command dispatcher and synchronized-work
producers are the exact missing boundaries.

No claim in this page assigns authoritative policy for distance, capacity,
stacking, uniqueness, tradability, gil limits, disconnects, duplicate
requests, rollback, locking, validation, ownership mutation, atomicity, or
persistence. Those behaviors require direct native, packet, or server
evidence; widget disablement, synchronized presentation, and closure are not
substitutes.
