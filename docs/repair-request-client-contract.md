# Repair request client contract

The NPC item-selection menu returns local numeric choices.
RepairOrder 24243 supplies an equipment-request mode. Bazaar repair uses
separate listing, withdrawal and ready-command routes. These client inputs,
work consumers and local returns do not establish server repair settlement.
The NPC/self-repair limits remain canonical in
`xivl-client-structs:docs/repair-contract.md` and its linked manifest.

## Garthrite provider identity

`actorclass.csv` row `1500258`, column 5, contains display key `1100074`;
`xtx_displayName.csv` row `1100074` has English name Garthrite.
`PopulaceItemRepairer.talkWelcome` explicitly recognizes actor class
`1500258`. Its original bytecode joins that comparison to the supplied
fourth method argument's comparison with numeric 20: equality selects speech
row 102, otherwise row 87, with no second speech row. The default branch's
false provider flag is bypassed. This is a specific repair-provider
presentation branch, rather than evidence of a missing generic talk method.

The method's recognized actor class does not prove a particular live actor's
assigned script, position or zone. Those require the corresponding actor
creation/binding and event invocation. The shared repair contract remains
the authority for item selection, confirmation, settlement and evidence
limits. In particular, the six one-gil prompts in
`xivl-captures:studies/retail-repair-contract/` do not establish a global
tariff, a repair-all service or Garthrite-specific settlement.

Source: `xivl-client-data:manifests/tables.json`, `actorclass.csv` and
`xtx_displayName.csv` rows above, columns zero-based after the row key.
The original `PopulaceItemRepairer` LPB
`729s9/wu7/uvupy975/uvupy9751q5xs5u91s5s.le.lpb` has SHA-256
`3d2148a689cbf940bbfc80260fd3d5a540e75d4992cdbd296a36a1e0cf3e1e7d`.
Its decoded payload has SHA-256
`90d9858f42360f5078a0f567d17c3f1651832127f81bd146d293e33ee01889e7`;
the canonical source has SHA-256
`027ac93ef6e805ee4c2197d5fa7353a0ebdff125f6d52f0d6c08bedfb5218ea3`
in `manifests/scripts.json`. `talkWelcome` is `root/proto1`, code offset
`0x0265`; the actor comparison and branch are PCs 76-94
(`0x0395`-`0x03DD`). The default false-flag path is PCs 96-98
(`0x03E5`-`0x03ED`). These are static observations of extraction
`2012.09.19.0001`, not a runtime repair observation.

## NPC item-selection menu

`PopulaceItemRepairer.selectItem(self,A1,A2,A3,A4,A5,A6,A7,A8,A9)`
builds a paged text-choice request and returns three local values. It does
not resolve an inventory item. The original method has ten fixed parameters,
including the receiver, and no varargs. Missing arguments become nil and
extra arguments are ignored. A1 is unused. A2 selects the table below and
participates in result arithmetic. A3 is forwarded as the default answer.
A4-A8 remain supplied formatter values without an established item, catalog,
package or slot domain. Only A9 equal to Boolean false selects the first
table; nil, zero and other values take the second table when A2 is 1.

| Input branch | New answer table, indices 1-5 |
| --- | --- |
| A2 equals numeric 1, A9 equals false | `33,34,35,36,18` |
| A2 equals numeric 1, every other A9 | `13,14,15,16,18` |
| A2 equals numeric 2 | `20,21,23,25,26` |
| Every other A2 | `89,90,92,94,95` |

After constructing that table, the method reads global `desktopWidget`
once, resolves its `askForEventMode` member and calls it with this exact
tuple, including the desktop receiver `D` and NPC receiver `N`:

```text
(D,N,N,N,A3,true,true,88,answers,A2,3,0,0,0,A4,A5,A6,A7,A8)
```

This is its only call. It requests exactly one result, here called R, and
ignores additional results. There is no receiver, type, range or helper
result guard before the call. The member lookup uses the same desktop value
as the call receiver. A later invocation reads the global/member again.
Lookup or call errors prevent result adaptation. Nil supplied values retain
their positions in the fixed call frame, including trailing A4-A8 values.

Conditional on that lookup resolving the published
[Ask connector](camp-replacement-choice-flow.md#ordered-call-and-display-requests),
the opening request is `(D,4,"Ask/AskWidget",nil,nil,false)`. The opened
widget's call is
`(widget,N,N,A3,true,true,88,answers,A2,3,0,0,0,A4,A5,A6,A7,A8)`.
The first N after D is the connector's owner argument and is omitted from
the widget call. The other two N values supply the widget's speaker and
text-provider positions. A3 is a default index, not a requested result count.
The two true values request paging and cancellation. Row 88 and the five
answer numbers are text-request inputs; this method supplies no labels or
item-reference lookup.

The published [Ask result paths](request-warden-event-contract.md#widget-result-production)
associate PageNext/PagePrevious with -1/-2 when paging reads true and Cancel
with -3 when cancellation reads true. These are conditional stored-result
requests, not observed callbacks. The
[connector completion contract](camp-replacement-choice-flow.md#local-completion-result-and-cancellation)
owns the exact-nil opening check, exact-true selection check, first getter
result, wait and explicit normal-path close. In particular, opening nil or
a non-true selection can return numeric zero. Nil or false selected getter
values are preserved. A reached normal close request precedes the following
caller adaptation, even if that adaptation then errors.

Let M be the supplied A2. The method tests R in the order shown and returns
exactly three values on each normal path:

| First helper result and guard | Local return |
| --- | --- |
| R equals -1 | `(nil,next,1)`, where `next=M+1`, replaced by 1 only when `3 < next`. |
| R equals -2 | `(nil,previous,1)`, where `previous=M-1`, replaced by 3 only when `previous < 1`. |
| R equals -3 | `(nil,nil,nil)`. |
| M equals 1 and R equals 1 | `(nil,nil,nil)`. |
| M equals 1 and R equals 2 | `(-1,M,R)`. |
| Every other result | `(5*M+R-7,M,R)`. |

For M=1,2,3, navigation wraps through those three values. It does not apply
a general modulo or reject other supplied M values. The final formula has
no answer-range or integer check. Numeric zero is not cancellation: M=1,
R=0 returns `(-2,1,0)`. With numeric M, nil or false R instead reaches an
arithmetic error. There is no catch, retry or second menu call here.
Omitted M can still return three nils for R=-3, before any arithmetic.

The first return is therefore an arithmetic choice value or a sentinel,
not an authenticated catalog ID, item object, package/slot or inventory
record. Even a plausible positive result does not identify the selected
server item. The actual invocation, supplied value meanings, dynamic
bindings, text evaluation and delivered UI result remain separate inputs.
No command submission, repair confirmation, material check/debit, bulk
service, settlement or durability change occurs in this method.

Source: `lua/scripts/chara/npc/populace/populaceitemrepairer.lua:541-680`,
with the original/canonical identities recorded above. Original Lua 5.1
`root/proto3` starts at decoded offset 3496 and contains 120 instructions,
zero upvalues and no children. Root PCs 17/18 create and bind `selectItem`.
PCs 2/4/27 select the answer tables; 51/52 resolve the desktop/member;
CALL PC 71 has B=20,C=2. Result tests are PCs 74/85/96/100/102/107,
navigation arithmetic/comparisons are 76/77 and 87/88, and the final
multiply/add/subtract is PCs 113-115. RETURN PCs 83/94/99/105/112/118
all have B=4. PCs are zero-based; B includes the function slot for CALL,
and B=4 returns three values for RETURN.

The canonical decompile retains malformed extra `else` tokens at lines
575 and 592. Its byte identity and those structural observations were checked
separately from the original control flow. An exact isolated-method syntax
check with Lua 5.4.8 rejected it; no repaired-source equivalence or retail
execution is claimed. The behavior above follows the authenticated original
instructions, with authored semantic fixtures checking the fixed frames,
guards, arithmetic, errors and result widths. Published helper contracts
were adopted without reopening their bodies. Confirmation, facility and
other repair methods remain outside this method's evidence.

## Equipment request mode 24243

`RepairEquipmentDialogWidget.getDialogResult` constructs its mode from
`CheckBox_Weapon` (+1 when exactly true) and `CheckBox_Armor` (+2) when
`work.mode == 0`; otherwise it returns the stored mode
(`root/proto4`, source 271-299, CALL PCs 8/15, additions 11/18, RETURN
22/23). The UI thus distinguishes weapon-only 1, armor-only 2 and both 3.
Operate forces result 0 when a request mode is already positive. Back and
Close supply -1 to the parent; Cancel does so only for `Button_Back`,
otherwise focusing that button. Checkbox changes update the local
cost/icon preview. The latter do not submit a repair request.

`EquipWidget.setDialogResult(result)` suppresses submission while a macro
plays and uses negative results only to restore/refresh the display. For
nonnegative results it calls `executePlayerCommand(24243,result)`;
zero and nonzero branches forward the same first operand unchanged
(`root/proto140`, source 9730-9800, CALL PCs 44/51). Zero is the dialog's
explicit Operate input when its stored mode is positive. No equipment
reference, package or
slot accompanies this first operand at that call site.

`RepairOrderCommand.canFire` checks `isPlayer`, `isMyPlayer`, and an
`isLiving` result other than exactly false. It requires the operand's Lua
type to be `number` and its value to equal 0,1,2 or 3
(`root/proto0`, source 11-47, PCs 0-36). The predicate does not calculate
commission, select an item or mutate repair condition.

The actual caller uses `executePlayerCommand`, whose existing bridge fills
the remaining command operands and can substitute the current target.
Its final local `player:command` shape for this caller is
`(command24243,mode,nil,nil,nil,currentTarget,nil,nil,nil,nil)`
(`DesktopWidget` connector `root/proto278`, source 13615-13688,
CALL PC 43). The command actor is resolved separately from its numeric ID.
This is not the `executePlayerCommandLocal` helper or a proof of a wire
reply. The shared conditional transport remains owned by
`xivl-client-structs:manifests/player_command_wire_contract.json`.

The equipment caller records `repaircommandtime` and `lastresult` after
submission, and can briefly display that local last result instead of the
work getter. An exactly true `executePlayerCommand` result drives the
preview checks; the equipment caller does not await a
named success packet. The whole 2,671-member authenticated Lua source query
for numeric token `24243` found only the two calls in this method and an
equipment-button alert carrying 24243 as message context.

## Work and icon consumers

`CharaBaseClass.getRepairType` returns
`charaWork.eventSave.repairType` after `hasGameParameter`, otherwise 0
(`chara/charabaseclass_event.lua:106-119`, `root/proto4`, PCs 0-9).
`initEventSyncWork` declares `repairType` as `integer8` and includes the
`eventSave/repairType` pair in the `bazaar` tag group
(source 170-288, `root/proto6`, PCs 9-13 and 56-64). This is a source work
declaration and consumer path, not a field-specific incoming wire witness.

The request icon is distinct from the Bazaar repair-dealer flag
`charaWork.eventTemp.bazaarRepair`. The exact NamePlate category-3
selection and work-update path are canonical in
`xivl-client-structs:docs/bazaar-appearance-contract.md#lua-sign-selection`:
nonzero repair type selects icon 928; otherwise the repair-dealer predicate
can select 380. `EquipWidget` separately sets the visibility of each
`:IconControl_Repair` from the chosen request-mode preview and colors it
gray for absent/full-condition equipment, white otherwise
(`root/proto135`, source 9303-9363). These are presentation choices, not
evidence of item locking or authoritative repair completion.

## Separate Bazaar repair inputs

`ItemListWidget.operateBazaarRepair` opens `BazaarEditWidget` with mode 3
and the chosen package/slot (`root/proto48`, source 4449-4510). The edit
handler maps mode 3 to numeric mode 30 (`root/proto10`, PC 540). Its
local-player calls are `setItemDeal(package,slot,30,rewardValue,stack)`
for numeric reward and
`setItemDeal(package,slot,30,rewardItem,stack,extraCount)` for item reward
(CALL PCs 603/696; source 2672-2824). A true submission updates the parent
operation and closes; a false one closes with operation reset. Those are
local submission outcomes.

The [Bazaar operand contract](bazaar-retainer-client-contracts.md#listing-operands)
owns the reward-first composition. Let `B` be the Bazaar actor, `I` the
resolved repair-listing item, `R` the selected scalar reward, `RI` the
reward item, `Q` the selected stack and `RQ` the reward count. For mode 30,
the nine values after command actor 24214 are:

| Reward branch | Command operands |
| --- | --- |
| Numeric | `(1000001,I,30,nil,B,R,Q,nil,nil)` |
| Item | `(RI,I,30,nil,B,RQ,Q,nil,nil)` |

These are the existing connector's `root/proto414` branches (CALL 37/54).
An omitted `Q` defaults to the listed item's stack; an omitted item `RQ`
defaults to the reward item's stack. Zero remains zero. The scalar reward
is selected UI data, not an authenticated commission tariff.

The numeric mode join is more than a display label: BazaarList's row builder
stores the dealing kind as `bazaarkind` and maps 20/30 to paired row type 4
(`updateBazaarLabel`, source 1930-2005). Its selection handler reads the
preceding row's kind: 20 takes the buy branch; the non-20 branch checks the
item's repair skill against the player's main skill before calling
`operateBazaarRepair` (source 4430-4522). This supports the kind-30 client
repair path without assigning every other non-20 value the same meaning.

`BazaarListWidget.operateBazaarRepair` checks item eligibility and available
repair-material stacks, then calls
`executeRepairBazaarItem(rewardpackage,rewarditem)` (`root/proto53`, CALL
PC 84; source 4840-4944). It returns one true only for an exactly true
helper result (PCs 85-87); a non-true helper result reaches a zero-value
return at PC 88. Earlier refusal branches can return false.

The connector resolves the selected Bazaar item `X`, captures only the first
`X:_getDealingAttached()` result `Y`, and calls
`executePlayerReadyCommand(22012,X,Y,nil,B)` (`root/proto308`, CALL 12,
TAILCALL 23; source 14735-14769). Its second nil guard rechecks `X`, not
`Y`, so this body does not independently reject a missing attachment.
The ready helper replaces the nil third operand with the second
`getReadyCommand` result, the selected category (`root/proto279`, PCs 21-30),
giving local command operands `(X,Y,category,nil,B,nil,nil,nil,nil)` when `B` passes
the target-validity check; otherwise the shared current-target fallback applies.
`xivl-client-structs:docs/bazaar-native-wire-contract.md` owns `Y`'s
item-versus-numeric alternatives. It must not be relabeled a
guaranteed material, currency amount or reward item at this call site.

### Cancel, withdrawal and callback results

The edit widget's Back action reports local operation 1 and closes. Cancel
does so only for `Button_Back`; elsewhere it focuses Back. These actions do
not submit 24216 or 24243. Withdrawing an existing listing is separate:
`ItemListWidget.operateBazaarAbort` takes the selected row's kind or the
paired row's `bazaarkind` and passes it to `setItemUndeal`
(`root/proto49`, source 4517-4608). For supplied kind 30 the existing
connector produces `(W,nil,30,nil,B,stack,attachedCount,nil,nil)` after
command actor 24216, where `W` is the dealing item resolved by that helper.
The trailing UI count arguments on the non-paired caller are outside the
helper's formal parameters; the helper obtains both counts from the item.
The [withdrawal contract](bazaar-retainer-client-contracts.md#widget-callers-withdrawal-and-fulfillment)
owns their exact derivation.

`CraftJudge.startRepair` is an independently callable UI continuation,
not a proven response to 24243 or 22012. Its existing contract is
`xivl-client-structs:manifests/repair_contract.json`, record `REPAIR-C-0004`.
For its player branch it creates the supplied virtual item and calls
`askCraftRepairWidget(0,0,A3,virtualItem,A6,A7,A8)`
(`root/proto20`, CALL PC 34, `B=9,C=5`; source 473-588). It remaps local
modes 1/2 to 5/6, resolves positive temporary indices through package 1,
places ItemBaseClass values before non-items, and returns
`(remappedMode, thirdWidgetResult, unpack(orderedValues))`
(CALL/RETURN PCs 106/107 use open arity). A failed first widget result
sets the remapped mode to nil. The decompiler's apparent fixed return
temporaries do not limit that open result sequence. None of these operations
proves a server-selected callback, debit, material use or durability change.

The [selected repair helper contract](craft-repair-selection-flow.md) owns
the conditional creation/initialization join, getter-result adjustment,
Cancel/failure distinction and explicit close before those results return.

## Evidence boundary

The result is static retail-client evidence. The remaining discriminator is
a transaction joining the selected 24243 mode to its incoming work update,
or a Bazaar repair command to the selected callback and authoritative item,
material and reward changes. A display label or local command return cannot
authenticate commission prices, NPC tariffs, material consumption or a
resulting condition percentage. Player trade's distinct polling/reply
contract remains in [Player trade lifecycle](player-trade-lifecycle.md).

## Source identity and method

Original LPBs and decoded payloads matched `manifests/retail_lua_coverage.json`
by `decodedScriptPath`; canonical LF source matched `manifests/scripts.json`
by size, SHA-256 and line count. Those records own ciphered resource paths
and original size/hash pins. Decoding used `tools/retail_script.py:decode_lpb`
and pinned `unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
Locators above use zero-based root child prototypes and PCs checked against
original Lua 5.1 instructions. Native package/serializer and NPC evidence
were reused from their owning promoted contracts; no new native body or
capture was opened for this request operand.

| Member below `lua/scripts/` | Decoded payload SHA-256 |
| --- | --- |
| `command/system/repairordercommand.lua` | `3c51b5e3062d7c7ffe1cd1395db6fa76d16161f63789eba843a424e1cd4d8255` |
| `widget/desktopwidget_connector.lua` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/equipwidget.lua` | `2672baca238ab5fb4eee096a3f5fba6a6f6fb37ce0ce846a34787a3a65c0815d` |
| `widget/repairequipmentdialogwidget.lua` | `5b1eab72a2d302f08c75a883206fe8df9e1115c54465e094279e74719e67cdfb` |
| `chara/charabaseclass_event.lua` | `5d5b10d8f36b08c01894d101679e19dc150af33d6b18b1a84ea5f29e5ac468af` |
| `judge/depictionjudge.lua` | `756fa626bf9703afb5f97a36eb5bc3643eaf216cc602137dde5f034f678b9f19` |
| `widget/bazaarlistwidget.lua` | `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |
| `widget/bazaareditwidget.lua` | `083f7cfea5a479cb882d6315cdcc4738996b23de82a161de5c0b55ae03161ac8` |
| `widget/itemlistwidget.lua` | `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` |
| `judge/craft/craftjudge.lua` | `0dff8463d2b685ff65a23afcf5e52e451e531e6fac194fd088adba3d05dbd0ff` |
