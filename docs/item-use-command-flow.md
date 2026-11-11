# Selected item-use command flow

ItemUseWidget supplies package/slot values and a target value to
`DesktopWidget.executeCharacterUseItem`. That helper obtains the local player
again, resolves an item with `_getExtendedTemporaryItem`, and requests ready
command `21007` with the resolved item object and the supplied target. Its
return describes local submission or refusal. It does not establish accepted
item use, consumption, cooldown, effects or inventory mutation.

The [widget contract](item-use-widget-contract.md#target-mode-mapping) owns
mode selection, its fresh item reads and the package/free-space guards.
The [ready-command contract](equipment-cancel-command-contracts.md#callers-and-arguments)
owns ready lookup and common argument forwarding. This page joins those
boundaries to the selected helper and ItemCommand eligibility.

## Item and actor operands

The two widget callers differ in both the target source and result handling:

| Caller | Helper inputs after the desktop receiver | Result consumer |
| --- | --- | --- |
| Mode 2 in `processUICommandEvent` | `usePackage, useItem, player` | Takes exactly one result. Only exact `true` requests `previousSequence`; the window refresh follows. |
| `processSubTargetDecided` | `usePackage, useItem, A1` | With nonnil callback `A1` and the widget guards satisfied, discards every helper result, then refreshes the window. |

These are the existing original-instruction observations at
`widget/itemusewidget.lua:1330-1399,1443-1486`, prototypes `root/proto21`
CALL PC 198 and `root/proto22` CALL PC 31. The callback's nonnil test does
not establish that its value is a valid actor. Zero, false and nil remain
distinct values. The direct caller's player value is an earlier read; it
must not be equated with the helper's later player read.

`executeCharacterUseItem(self, package, slot, target)` performs these local
steps (`widget/desktopwidget_connector.lua:14618-14643`):

1. Takes one result from `worldMaster:_getMyPlayer()` as `P`.
2. Takes one result from `self:getItem(P, package, slot)` as `item`.
3. If `item` is nil, returns one exact `false`.
4. Otherwise tailcalls
   `self:executePlayerReadyCommand(21007, item, nil, nil, target)`, preserving
   that callee's open result sequence.

The item is a resolved object, not the package number, slot number or catalog
ID. It is also a new lookup, separate from the widget's earlier `_getItem`
reads used for display and mode selection. The helper tests only nil at
step 3; a replacement `getItem` returning false or zero would reach the
ready call rather than this refusal branch.

`getItem` and its selected guards are local connector methods:

| Method | Established branch and return |
| --- | --- |
| `checkActor`, lines 857-871 | Nil input or an exact-false `_isAlive()` result returns one nil. Otherwise returns the original input. This is object-validity handling, not a gameplay living/dead-state test. |
| `isValidItemParameter`, lines 13481-13511 | Returns false when `checkActor(player)` is nil, `_hasItemPackage(package)` is exact false, or numeric slot lies outside `1.._getItemPackageCapacity(package)`. Otherwise returns true. There is no local integer/type check. |
| `getItem`, lines 13515-13543 | Only exact false from `isValidItemParameter` exits with nil. Otherwise reads `player:_getExtendedTemporaryItem(package, slot)` as one result, calls `checkActor` on it, returns nil when that check is nil, and otherwise returns the originally read item. |

Nil and false results from the named calls are therefore not interchangeable.
Unsupported receiver shapes or numeric comparisons can fail before a normal
return. The predicates do not prove native result types, storage, ownership
or that this later lookup returns the same object used to choose the mode.

`getReadyCommandIndex` maps 21007 to ready index 6 (connector
`root/proto246`, code start `0x1CA99`, PCs 22-25,
`desktopwidget_connector.lua:12408-12497`). The
[ready-command dispatcher](equipment-cancel-command-contracts.md#callers-and-arguments)
returns one `false` before its command lookup when
`work.commandIndex[6] <= 0` (`root/proto279`, PCs 6-19), so the helper's
tailcall then yields exactly that `false`. A nil entry fails that comparison
under standard Lua rules instead of returning. The writer of
`work.commandIndex` is NOT TRACED here.

The static-actor map assigns `21007` to `/Command/ItemCommand`
(`xivl-client-data:manifests/staticactor_class_paths.json:98-99`). This is a
command ID and class-path mapping, not a network opcode or an observed
command actor. Applying the published ready and common dispatch contracts,
the nine submitted values after a resolved command object are:

```text
(item, nil, readyVariation, nil, resolvedTarget, nil, nil, nil, nil)
```

The ready helper replaces the nil third value with the selected ready
command's returned hand/variation value. Common dispatch retains a usable
explicit target or substitutes the current target for a missing/invalid one.
`resolvedTarget` can still be nil. Ready-slot availability, the actual command
object, current target and player identity at those later reads remain
runtime inputs. The
[shared return contract](equipment-cancel-command-contracts.md#return-and-refusal-handling)
owns local dispatch acceptance and distinguishes it from server completion.
This flow does not assign an ItemCommand event descriptor or wire payload.

## ItemCommand and base item eligibility

`ItemCommand.isBattleCommand` returns one true. Its `canFire` directly calls
the first command operand's `canUse` member. There is no local nil-item or
item-type guard in that method.
Using `V1..V9` for command values, the call is:

```text
V1:canUse(player, V3, V4, V5, V6, V7, V8, V9)
```

`V2` is skipped. The method takes only the first `canUse` result and returns
one boolean using Lua truthiness: nil/false refuse; zero and other truthy
values admit this predicate. A second error value is discarded. A missing
`V1.canUse` binding can fail instead of returning false
(`command/itemcommand.lua:11-42`, `root/proto1`, CALL PC 10).

`ItemBaseClass` explicitly requires `/Item/ItemBaseClass_common`; the latter
binds the inspected base `canUse`. This establishes a local base definition,
not the concrete runtime item's class or overrides. When the call resolves
to that definition, the selected inputs are:

```text
canUse(item, player, readyVariation, nil, resolvedTarget, nil, nil, nil, nil)
```

The positional names below refer to that base method, with `A0=item`.
It defaults nil `A4` to `A1` (player), and nil `A8` and `A9` each to integer
1. `A8` becomes the target-parts argument. The ItemCommand call omits `A9`,
so fixed parameters supply nil before that default. `A9` is not subsequently
consumed by this body. The base body does not inspect the forwarded ready variation.
It then performs these checks in order:

1. `getItemUseMax(item)` returning exact numeric zero yields `(false, 0)`.
   False or nil is not this exact-zero branch.
2. `processCanUseForActorStat(item, player)` supplies two local results.
3. `processCanUseForTargetParts(item, target, 1)` supplies two results.
4. `canUseDetail(item, player, target, 1)` supplies two results.

For checks 2-4, a falsey first result requests
`sendMessageUseErr(item, error, player, target)` and returns `(false, error)`.
The two-result calls nil-pad a missing error and truncate extra results.
If all pass, the base method returns one exact true. A message request does
not establish rendering or a server refusal.

The selected base `getItemUseMax(item)` tailcalls `item:getItemData(43)`.
The base `getItemData(item, field)` takes one fresh result from
`item:_getCatalogID()`, then tailcalls
`itemDataSheet:_getData(catalog, field)`. Both helpers preserve the final
callee's open result sequence. For this call, the field is numeric 43;
the `canUse` caller takes only the first result before its exact-zero test.
An empty result therefore supplies nil, and a first false remains distinct
from numeric zero. This is a field request, without an inventory-count read
in either selected helper. Actual method/global binding, native provider,
physical table, field meaning and value remain unproved.

These original common-module methods are `root/proto69`, decoded code
offset 15743, five words, and `root/proto0`, offset7317, eight words.
Their selected tailcalls are zero-based PC2 and
PC5; the fresh catalog call is PC3 and requests one result.

For the selected parts argument 1, the base target-parts method calls
`canUseWithPartsCheck` and returns `(true, 0)` on either truthy or falsey
results without reaching its target/parts readers. The base `canUseDetail`
also returns `(true, 0)`. Dynamic overrides and the native/property inputs
to the other predicates remain unresolved.

The base actor-state predicate reads `_getActorMainStat(player)` and
`getItemCanUseStatCategory(item)`. Its numeric decisions are:

| Actor main-state code | Passing condition |
| --- | --- |
| 1 or 3 | `canUseOnDead(item)` is Lua-truthy, regardless of the category. |
| 0 | Category 0, 1, 5, 6 or 7. |
| 2 | Category 0, 2 or 5. |
| 30, 31 or 32 | Category 0, 3 or 6. |
| 50 or 51 | Category 0, 4 or 7. |
| 70 | Category 0, 5 or 8. |
| Other state codes | Passes this predicate. |

These comparisons do not name the gameplay conditions that assign those
states or establish the native/property values for a particular item.
The selected base checks are client eligibility, not accepted use.

## Published itemData sheet creator

`xivl-decomp:docs/script/sheet-globals.md`, "Sheets created by the Judge
classes", records `CommonJudge.init` preparing path `itemData` and the derived
global name `itemDataSheet`. Its "prepareSpreadSheet in the Judge classes"
section qualifies publication and `SpreadSheet._onInit` forwarding that path
to `_setFilename`. The existing-name reuse path can return an existing sheet;
this preparation call alone does not authenticate the global's actual object
or its loaded contents.

`xivl-client-data:docs/item-equipment-columns.md`, introduction, identifies
the named `itemData` table as game-schema resource `0x01030129`. Together these
publications provide a static source candidate for the field-43 request.
Applying it requires the actual `itemDataSheet` binding to select that sheet
and its native reader/row. Neither publication supplies field 43's meaning,
the current catalog row/value, an item-use count or an authoritative use rule.

## Evidence and reproduction

Canonical source members were authenticated in memory against
`manifests/scripts.json`. Original retail LPBs and decoded payloads matched
`manifests/retail_lua_coverage.json`. Decoding used
`tools/retail_script.py:decode_lpb`; original Lua 5.1 instructions were read
with `tools/build_quest_contracts.py:ChunkReader` and `instruction`.
Sources use the canonical LF representation. LPB paths below are relative
to retail `client/script/`.

| Member after `lua/scripts/` | Source bytes / lines / SHA-256 |
| --- | --- |
| `widget/desktopwidget_connector.lua` | 660617 / 26564 / `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `command/itemcommand.lua` | 837 / 42 / `3302b9e1d0f1fb763542233666617d04c6f75c468bd4f49df33c69526b0706f6` |
| `item/itembaseclass.lua` | 1391 / 68 / `2a0841c0477019577e9939330eb80f2e3a3d1a2166a3d2278a7e378ee36540c8` |
| `item/itembaseclass_common.lua` | 87762 / 4686 / `7620492917230c3e060ed84d3197bf164c234a3ab73e48a0939bc65107f6b7fa` |

| LPB | Bytes / LPB SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `7vxx9w6/1q5x7vxx9w6.le.lpb` | 432 / `70573e99578745c3b9f0e6f46d19291ac204f086e17c73a9826474067b21a02c` | 419 / `771a29bfc514892d59f9b0b265dfde6d6284947661a347833a6c582a1dc504c9` |
| `1q5x/1q5x89r57y9rr.le.lpb` | 759 / `03331954e7795cd1c820973d74ef975513a4cb1793c3bd78f49568972dc325d7` | 746 / `6a4e865ebcf1f4d2d70bf245e4eeb7b53988e877d5fbebcb71fdf4616697873d` |
| `1q5x/1q5x89r57y9rr_7vxxvw.le.lpb` | 41430 / `50bd1025ad4ad14c12e51f96f9c73894d990f0c452cd756e0d815d684e5c91f0` | 41417 / `55f24303105864b50b37bab4e796f81ad65b889a08ff665e6130be96e62ba4d6` |

PCs are zero-based. Offsets are decoded-payload byte offsets at the start
of the prototype's instruction array; each instruction occupies four bytes.

| Member and method | Canonical source lines | Prototype / offset / words | Selected original instructions |
| --- | --- | --- | --- |
| Connector `checkActor` | 857-871 | `root/proto6` / 31042 / 10 | Nil compare PC 0; alive CALL 3; exact-false compare 4. |
| Connector `isValidItemParameter` | 13481-13511 | `root/proto274` / 124643 / 26 | Actor CALL 2; package CALL 9; capacity CALL 16; range comparisons 17/19. |
| Connector `getItem` | 13515-13543 | `root/proto275` / 124865 / 22 | Validation CALL 4; exact-false compare 5; item CALL 12; actor CALL 15; nil compare 16. |
| Connector `executeCharacterUseItem` | 14618-14643 | `root/proto303` / 132592 / 19 | Player CALL 3; item CALL 6; nil compare 7; false RETURN 10; ready TAILCALL 16. |
| ItemCommand `canFire` | 20-42 | `root/proto1` / 303 / 18 | Item `canUse` CALL 10 takes one result; truth test 11; boolean RETURNs 14/16. |
| Item common `canUse` | 4511-4586 | `root/proto196` / 40275 / 65 | Nil comparisons 0/3/6; defaults 2/5/8; use-max CALL 10; zero compare 11; predicate CALLs 18/32/49; message CALLs 25/41/58; success RETURN 63. |
| Item common actor-state predicate | 3556-3646 | `root/proto157` / 33281 / 109 | State/category CALLs 1/3; dead-use CALL 9; category/state comparisons 4-94. |
| Item common target-parts predicate | 3803-3865 | `root/proto162` / 35229 / 56 | Parts-check CALL 1; selected part-1 compare 9; early RETURN 13. |
| Item common base detail | 3546-3553 | `root/proto156` / 33216 / 4 | Fixed `(true, 0)` RETURN 2. |

Targeted execution of the authenticated original instructions checked item
lookup, exact-false/nil/zero distinctions, receiver and argument positions,
the skipped command operand, nil defaults, short-circuit order, result widths
and actor-state decisions. Seven deliberate instruction mutations were
rejected, including omitted target/final arguments, lost lookup results,
inverted refusal/state branches and changed target defaults. Opaque calls
used controlled return values; these checks do not reproduce native behavior,
concrete runtime item binding or a historical invocation.
