# Duty confirmation client contract

`QuestBaseClass.contentsJoinAskInBasaClass` requests the common duty prompt
with world-master question row 25015 and returns one answer. When the supplied
actor's `ask` resolves to `NpcBaseClass.ask`, the path opens `Ask/AskWidget`
with choices 25016 and 25017, default answer 1, `askPaging=false` and
`canCancel=false`. The helper contains no content allocation or duty transition.

This is a static 1.23b contract. It does not identify a historical trigger,
actor binding, quest invocation or server admission rule. A visually similar
Yes/No dialog does not establish this route or its client version.

## Artifact identities and reproduction

The extraction is `2012.09.19.0001`. Resource paths below are relative to
`client/script/`. The complete LPB and decoded payload identities match
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
Canonical source paths and hashes belong to
[`scripts.json`](../manifests/scripts.json).

| Decoded script | LPB resource | LPB SHA-256 | Decoded payload SHA-256 |
| --- | --- | --- | --- |
| `quest/questbaseclass_common.lua` | `tp5rq/tp5rq89r57y9rr_7vxxvw.le.lpb` | `ecc3f7c6fb49df196431494aa5aece95ede1c24ca1325af11ddc993a3836322d` | `9379ee6832bdfa542273c7f43f065d7a15f9a730d9ef244be9a565a1faa53504` |
| `chara/npc/npcbaseclass_event.lua` | `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` | `84a5098636ff289f4ecf4e164e84e44890895e8a9005fb102e04929c2bb74bf9` | `4a3008dd8d2a91e7eb044e5555d2757468a9097bba5175992fb88f943bd07b6c` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/ask/askwidget.lua` | `n1635q/9rz/9rzn1635q.le.lpb` | `8541d21030988f4ed5460690156a71a5a0120b68ed38d8db181676b27a23bfe9` | `1b0d5e2ca4c39b781305b98320eb597337e0d4c0fc0c9167244553dfc49d14c0` |
| `widget/ask/askbaseclass.lua` | `n1635q/9rz/9rz89r57y9rr.le.lpb` | `4c1c98059f5b3663d24a85897d21ff603dfb5c95000c20fdfa4befd592ad431d` | `a1d4129ca5779c3b2598da418909f057bd9b6c6733701855fd70bf2a9dcb1230` |

Decode each resource with `decode_lpb` in
[`retail_script.py`](../tools/retail_script.py), parse its complete Lua 5.1
payload with `ChunkReader` in
[`build_quest_contracts.py`](../tools/build_quest_contracts.py), and decode
the instruction operands at the locators below. PCs are zero-based and offsets
are zero-based within the decoded payload. For `CALL`, `B` includes the
function slot and `C` is one greater than the requested result count.
`B=0` uses the variable argument top and `C=0` requests all results.
The canonical decompile is useful for names and line locators, but its
apparent fixed vararg assignments do not establish bytecode arity.

## Prompt and argument forwarding

Let `P0` be the common helper's quest receiver, `P1` its unused event argument
and `P2` its supplied actor. Let `Q=(q1,...,qn)` be all results from
`P0:getQuestId()`. The selected bodies preserve `Q`; they do not establish
its count, types or runtime values.

| Method and source locator under `lua/scripts/` | Original instruction locator | Observation |
| --- | --- | --- |
| `quest/questbaseclass_common.lua:562`, `contentsJoinAskInBasaClass` | `root/proto18`, PC 5 / offset 5454, `CALL A8 B2 C0`; PC 6 / 5458, `CALL A3 B0 C2`; PC 7 / 5462, `RETURN A3 B2` | Calls `P2:ask(worldMaster,25015,2,Q...)`, retains one answer and returns exactly one value. The apparent two `getQuestId` results in source line 571 are not a fixed two-result contract. |
| `chara/npc/npcbaseclass_event.lua:389`, `NpcBaseClass.ask` | `root/proto10`, PC 18 / 3473, `VARARG A16 B0`; PC 19 / 3477, `CALL A6 B0 C2`; PC 20 / 3481, `RETURN A6 B2` | Builds numeric choices `{25016,25017}`. Calls `desktopWidget:askForEventMode(P2,P2,worldMaster,1,false,false,25015,choices,Q...)`, retaining and returning one answer. This hop depends on `P2.ask` resolving to this method. |
| `widget/desktopwidget_connector.lua:12038`, `DesktopWidget.askForEventMode` | `root/proto237`, PC 15 / 114877, `CALL A11 B7 C2`; PC 26 / 114921, `VARARG A21 B0`; PC 27 / 114925, `CALL A12 B0 C1` | Opens `openWidgetYield(4,"Ask/AskWidget",nil,nil,false)` and retains one widget. On a non-nil widget, calls `widget:ask(P2,worldMaster,1,false,false,25015,choices,Q...)` and discards that call's results. The first owner argument is not forwarded to `widget.ask`. |

The numeric `1` passed to `widget.ask` is its default answer index. It is
not a requested result count. The two boolean `false` values set `askPaging`
and `canCancel`. Their result branches are described below. Numeric zero is
not substituted for either boolean.

The NPC delegation frame is already recorded in
[Winter snowman delegation](winter-is-not-coming-client-contract.md#emote-entry-and-conditional-callback-frame).
Conditionally on that recovered adapter, reflective lookup and incoming
binding, materialized `(D0,D1,D2,...)` supplies callback receiver `D1`, event
argument `D0`, actor `O`, then `D3...`, consuming `D2` as the method key.
Selecting `contentsJoinAskInBasaClass` therefore still requires an actual
invocation and the appropriate actor binding. Its availability on a class
does not identify a historical caller.

## Text and native property input

`AskWidget.ask` (`widget/ask/askwidget.lua:108`, `root/proto2`) stores
`askAnswerMax=2`, `askPaging=false` and `canCancel=false` on this route.
With a non-nil text provider `worldMaster`, its native question call has
these arguments, including the receiver:

```text
(widget, nil, "TextBlock_Question", "Text", worldMaster, 25015, Q...)
```

PC 75 / offset 1711 is `VARARG A19 B0`. PC 76 / 1715 is
`CALL A12 B0 C1` to `_setProperty`, so every element of `Q` reaches that
native entry and no result is retained.

The answer loop supplies rows `25015+i` for `i=1,2`. It computes
`k=max(n-2,0)` and forwards the complete suffix from `select(k+i,Q...)`,
with this fixed prefix:

```text
(widget, "Item_Answers"..i, "TemplateButton_Answer", "Content",
 worldMaster, 25015+i)
```

PC 94 / offset 1787 is `VARARG A25 B0`, PC 95 / 1791 is
`CALL A23 B0 C0` to `select`, and PC 96 / 1795 is `CALL A16 B0 C1`
to `_setProperty`. The suffix is not restricted to one value. The method
itself returns zero values at PC 123 / offset 1903, `RETURN B1`.

`xivl-client-data:manifests/tables.json`, `worldMaster.csv`, pins the
1,851,138-byte sheet to SHA-256
`2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`.
English sheet field `1`, rows 25015-25017 at physical lines 130-132, contains
the duty-proceed question and Yes/No answers. The question includes the
`xtx/quest` sheet control `02280fff0a7874782f7175657374e8020303`.
This identifies shipped text and the supplied formatting path. Native text
evaluation and a successful visible display remain separate observations.

The quest title sheet is independently pinned by the same manifest:
`xtx_quest.csv`, 2,953,504 bytes, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`.
English field `2` identifies row 110009 as Flowers for All and row 110080 as
All Bark and No Bite, at physical lines 12 and 29. A title match does not
join either quest to a particular prompt invocation.

## Selection and continuation

`AskWidget.processUICommandEvent` (`widget/ask/askwidget.lua:387`,
`root/proto4`) parses the numbered answer control and calls
`setBaseAskResult(index)` at PC 15 / offset 3345, `CALL B3 C1`.
The cancel branch writes `-3` only when `canCancel==true` at PC 22,
with the setter call at PC 26 / offset 3389. This route supplies `false`.
The paging-result branches that write `-2` or `-1` require
`askPaging==true`, also false here. With false, page controls instead update
the widget's internal page and call `pageChange`.
These branches do not establish every way a native widget can stop.

The original class declarations at each root's PC 6 / offset 56 establish
`AskWidget -> AskBaseClass -> WidgetBaseClass`. In
`widget/ask/askbaseclass.lua:98`, `setBaseAskResult` stores its argument
unchanged in `askWork.askResult` (`root/proto7`, PC 8 / offset 1259) and
returns zero values at PC 9 / 1263, `RETURN B1`.
`getBaseAskResult` at source line 132 returns that field as exactly one
value (`root/proto9`, PC 2 / 1548, `RETURN A1 B2`). `getAskResult` at
source line 79 tail-calls this getter (`root/proto5`, PC 1 / 1066,
`TAILCALL A1 B2 C0`). Thus ordinary answer indices 1 and 2 are returned
unchanged through the inherited helpers, without a status prefix.

The separate `isAskFinish` predicate (`askbaseclass.lua:142`,
`root/proto10`) compares the field with zero at PC 2 / offset 1632 and
returns one boolean at PCs 5/7, offsets 1644/1652. Its completion predicate
is not the selected answer value. These declarations and stores do not
observe a runtime binding or exclude later field mutation.

The desktop helper saves an answer initialized to numeric `0`. It calls
`selectWidgetYield(widget,true)` at PC 31 / offset 114941, `CALL B4 C2`.
Only an exact boolean `true` result takes `getAskResult` at PC 35 / 114957,
`CALL B2 C2`, retaining one result. It then calls `closeWidgetDirect` at
PC 39 / 114973, `CALL B3 C1`, and returns exactly one answer at PC 40 /
114977. A failed open or non-true selection continuation leaves answer `0`.
That fallback differs from selected No and from the conditional `-3` cancel
branch. No completion prefix is inserted by the common, NPC or desktop
methods.

The generic native callback collection and c2s `0x012E` EventUpdate route
are already documented in
[Native callback result and EventUpdate](passivegl-dialogue-producer.md#native-callback-result-and-eventupdate).
Those mechanisms do not select the server's next quest or content action.
The outer adapter, native result conversion and actual invocation remain
separate from the one answer retained by this helper.

## Evidence boundary

This route distinguishes an NPC choice prompt from multiple `say` calls,
`WidgetOpenCommand` 24228 and an instance director's start lifecycle. Reuse
the [widget-open boundary](widget-open-command-boundary.md) and
[content director contracts](content-director-ui-contracts.md) for those
different owners.

The client method does not request allocation, choose a duty destination,
check eligibility or settle rewards. A complete historical producer join
requires the selecting event/actor, outer function, resolved receiver and
method, and complete typed argument vector. An observed reply must be
correlated with that invocation before assigning its server continuation.
