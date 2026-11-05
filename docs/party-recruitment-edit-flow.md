# Recruitment editor outcomes

`PcMatchingEditWidget` can advance local editing, publish signal 3, or notify
30507 and request closure. `processUICommandOperate` does not itself reject a
disabled Operate button. Its enable helper and its actual outcome branches are
separate. These are recovered Lua control and call contracts, not proof of a
server request, recruitment acceptance, or a visible retail session.

The [party matching contract](party-matching-client-contract.md) owns the
purpose and content list inputs. [MyPlayer timer consumers](myplayer-timer-consumers.md)
owns occupancy checks. The [search and recruitment native boundary](search-recruitment-native-boundaries.md)
owns the separate Find result flow and links its wire evidence.

## Button admission and local state

`isOperateButtonEnable` reads `work.view`. Unless it equals 99, the helper
loops from 1 through `work.matchNum`, reads each
`CustomControl_NumberOfPeople_<i>` value, and returns exactly one `false` if
any value equals numeric 0. It then calls
`desktopWidget:getPlayerConfirmGroupCommandVariation()`, retaining three
results but testing only the first. A first result of 10001 or 10002 returns
one `false`; every remaining path returns one `true`. View 99 skips the
number-of-people loop, not the variation check. This helper does not validate
comments, selected classes, rank ordering, or server eligibility.

The selected Operate handler branches on its third parameter, the control
name. For `Button_Operate`, it reads `work.view` and uses the following paths.
The handler does not call the enable helper before choosing a final outcome.
Calls made while moving between steps do recompute the button's enabled
property, as described below.

## Operate in view 99

Before deciding the outcome, the handler obtains a fresh player through
`worldMaster:_getMyPlayer()`. It reads that player's `getStateMainSkill`,
`getMainSkillCategory`, `getStateMainSkillLevel` and `getMainClassOrJob`.
It sets local controls as follows:

| Control | Writes |
| --- | --- |
| `ComboBox_Skill_1` | user-work integer slot 3 = main-skill category; slot 4 = state main skill |
| `ComboBox_Skill_2` | slot 3 = the same category; slot 4 = main class or job |
| `CustomControl_RankFrom_1`, `_2` | maximum and value = state main-skill level + 100 |
| `CustomControl_RankTo_1`, `_2` | maximum and value = 200 |
| `CustomControl_NumberOfPeople_1`, `_2` | value = 1 |
| `CustomControl_NumberOfPeople_3`, `_4` | value = 0 |

Each user-work access above passes an explicit `nil` between its slot and
control name. The handler then obtains three fresh variation results and uses
only their first result:

| Guard, in order | Outcome |
| --- | --- |
| Variation equals 10001 or 10002 | Notify 30507, obtain a fresh parent, update its child status to 0 if the parent is not `nil`, then return all results of direct closure. |
| Otherwise, a fresh `countPartyMember()` result is greater than 1 and a subsequent `isMyPartyLeaderForMyPlayer()` result equals exactly `true` | Notify 30507 and return all results of direct closure. This arm has no explicit parent-status update. |
| Otherwise | Write signal 3, obtain a fresh parent and update its child status to 3 if it is not `nil`. Return no values. |

The party-size read is not reached in the first arm. The leader read is not
reached when the party count fails the strict greater-than-one comparison.
These notification arms remain present even though the enable helper returns
`false` for the two named variation values.

## Operate in other views

The handler reads `work.step` at each step comparison.

| Step | Local outcome |
| ---: | --- |
| 0 | Set step to 1, publish the current step in `Button_Operate` user-work slot 2 with explicit `nil`, recompute its enabled property, call `setGrid` with the current step and focus `ComboBox_Skill_1`. |
| 1 | Set step to 2, publish the step in the same slot, recompute the enabled property, call `setGrid` and focus `TextBox_Comment`. |
| 2 | Normalize selection properties and take the final-outcome branch below. |
| Other | Return no values without one of these step actions. |

At step 2, the handler reads user-work slot 2 with explicit `nil` separately
from `ComboBox_Purpose`, `ComboBox_Place` and `ComboBox_GLName`. For each read
equal to -1, it writes 0 into that control's slot 3. It then loops over all
four `ComboBox_Skill_<i>` controls. A slot-2 value of -1 causes slots 2, 3 and
4 of that skill control to be written as 0. These are local property writes,
not a validation failure or an early return.

After those writes, a fresh variation call retains three results and tests
only the first. Values 10001 and 10002 notify 30507, obtain a fresh parent,
update its child status to 0 if it is not `nil`, and return all results of
direct closure. This arm has no party-size or leader check.

Otherwise the handler reads `work.view` again. If this fresh value equals 30,
it reads `ComboBox_GLName` slot 3 and forwards all returned values as the final
arguments of a slot-3 write to `ComboBox_Purpose`. It then writes 0 to
`ComboBox_GLName` slot 3. Both accesses include explicit `nil`. This transfer
occurs after normalization and only in the non-notification arm. Finally the
handler writes signal 3, obtains a fresh parent, updates child status to 3 if
it is not `nil`, and returns no values.

No selected purpose, place, skill, rank, people count or comment is appended
to the notification call. No notification result is tested here.

## Cancel and Close

Cancel first reads `getKeyboardFocusedControl()` once and compares that
result with `tostring(i)` for integers 0 and 1. A match calls
`setWindowFocus` with the supplied control name and returns no values.
Only when neither comparison matches does Cancel continue:

| Guard, in order | Local outcome |
| --- | --- |
| Supplied control name is `TextBox_Comment`, view is 99 | Focus `ComboBox_Purpose`. |
| Supplied control name is `TextBox_Comment`, other view | Read enabled properties in order: Operate, Minus, Plus. Focus the first truthy one. If all are false or `nil`, do not change focus here. |
| Other supplied control, view is 99, a fresh focused-control read equals `Button_Operate` | Focus `ComboBox_Purpose`. |
| Other supplied control, view is 99, fresh focus differs | Obtain a fresh parent, update child status to 0 if it is not `nil`, and return all results of direct closure. |
| Other supplied control, other view, step is 0 | Obtain a fresh parent, update child status to 0 if it is not `nil`, and return all results of direct closure. |
| Other supplied control, other view, step is 1 and `work.matchNum` is greater than 1 | Decrement `matchNum`, call `setGrid`, reset skill set at the newly read `matchNum + 1`, recompute Operate enable, focus the newly read `ComboBox_Skill_<matchNum>` and return no values. |
| Other supplied control, other view, step is 1 and the count comparison fails | Reset skill set 1, set step to 0, publish step in Operate slot 2, enable Operate with exactly `true`, call `setGrid` and focus `ComboBox_Purpose`. |
| Other supplied control, other view, step is 2 | Set step to 1, publish it in Operate slot 2, recompute Operate enable, call `setGrid` and focus `ComboBox_Skill_<matchNum>`. |
| Other supplied control, other view, other step | Return no values. |

The focus-only and navigation arms return no values. Cancel does not notify
30507 or write signal 3. Its enabled-property tests use Lua truthiness,
whereas Operate's party-leader comparison requires exactly `true`.

`resetSkillSet(i)` sets `ComboBox_Skill_<i>` selection to -1, obtains
`ComboBoxItem_Skill_<i>_1` property `Content` and uses it as the combo text.
It writes 0 into combo user-work slots 2 and 3 with explicit `nil`, calls
`checkRankNumberRange(i, 0, 0)`, then sets both rank values and the people
value to 0. It does not write combo slot 4. In this reached rank-range arm,
the helper obtains a fresh player and forwards all `getStateMainSkill()`
results to `getSkillLevelCap`. It uses that call's first result as both rank
maxima and clamps either old rank value that exceeds it, before the reset
writes both values to 0.

Close reads `work.chosenOperation`. Unless that value equals numeric 0, it
returns no values. With 0, it obtains a fresh parent, updates child status
to 0 if the parent is not `nil`, and returns all direct-closure results.
The selected Close method does not reset `chosenOperation`, selections or
signal. Cancel and Close therefore do not imply submission or acceptance.

## Calls, results and remaining boundary

All three notification sites have the same complete Lua call operands:
`worldMaster:notify(worldMaster, 30507)`. The implicit receiver plus two
explicit arguments make three function arguments. The original instruction
is `CALL B=4 C=1`: zero results are retained. The numeric value is a UI
notification identifier, not an established wire opcode.

Every explicit parent update is
`parent:updateChildWidgetStatus("PcMatchingEditWidget", status)`, with status
0 or 3 as specified above. The parent check is equality against `nil`, not
a general truthiness test. The parent is resolved anew at each reached site.
Its dynamic identity and implementation are outside this contract.

Direct closure is `desktopWidget:closeWidgetDirect(self)`. Each selected
closure site uses `TAILCALL B=3 C=0`, followed by open `RETURN B=0`: the
handler forwards however many values closure returns. It does not force a
single `nil`, `false`, zero, or a success value. Other handler exits use
`RETURN B=1`, meaning zero values.

`setSignal(3)` calls
`setUserWorkInt(3, nil, "Button_Operate", 3)` and retains no results.
The helper skips a write only when its argument equals numeric 0.
`getSignal` tail-calls `getUserWorkInt(3, nil, "Button_Operate")` and forwards
all results. These selected handlers do not poll that signal or wait for a
callback. Delivery of a property change, notification, native control action,
or external response remains outside the inspected methods.

For `Button_Minus`, a `matchNum` greater than 1 is decremented, the grid is
updated, and the skill set at the newly read `matchNum + 1` is reset. For
`Button_Plus`, a `matchNum` less than 4 is incremented and the grid is
updated. Plus then reads and sums the active people controls and calls
`numberOfPeopleRemain`, even when no row was added. That helper makes a fresh
party-count read and returns 7 for count 0, otherwise `8 - count`. The Plus
arm computes `remaining - matchNum + 1` but performs no control write with
that value. Both button arms then recompute Operate enable when the freshly
read step is not 0, or set it to exactly `true` when step is 0. They return
no values. Neither arm notifies, publishes signal 3, or closes.

This finding does not inventory the widget's list builders or infer the
native control machinery, wire serialization, server eligibility, or
settlement from the adjacent Find protocol.

## Evidence and reproduction

The canonical decoded source is
`manifests/scripts.json:15735`,
`lua/scripts/widget/pcmatchingeditwidget.lua`, 118,943 bytes, SHA-256
`6944f874d7d4caa57c8b50d48512041c649d33ba1f27f04a6353c5c2ddb8e07f`.
Canonical decompile method assignments occur at lines 4008 (Close), 4548
(Operate), and 4772 (Cancel). Helper assignments are at 2476
(`checkRankNumberRange`), 2663 (`resetSkillSet`), 3075
(`isOperateButtonEnable`), 3035 (`numberOfPeopleRemain`), 5000 (`setSignal`)
and 5013 (`getSignal`).

`manifests/retail_lua_coverage.json:27543` identifies original resource
`n1635q/u7x9q721w3561qn1635q.le.lpb`, 33,862 bytes, SHA-256
`530d0636d305515ce06a5de639e3527f227358a60ded1af41e8994a381c0ef2d`.
Its XOR-73 wrapper decodes to 33,849 bytes, SHA-256
`86afa854ce49d06eb4acd1da9e6e46706fce4ef401759fb1ad2191fffc9b262b`.
The following locators use one-based PCs in that decoded Lua 5.1 payload.
Prototype names use the reader's zero-based child indices.

| Method | Prototype; code byte offset; words | Distinguishing instruction locations |
| --- | --- | --- |
| Operate | `root/proto35`; 27869; 425 | View test 5; variation tests 100/102 and 287/289; party count test 125; exact-true leader test 130; notify 108/136/295; parent updates 116/152/303/339; closure 120/140/307; selection normalization 214..283; GL transfer 311..328 |
| Cancel | `root/proto36`; 30862; 188 | Initial focus loop 1..16; comment branch 17..53; view-99 focus 56..65; closure 77/95; row reset 119/136; step rollback 138/163 |
| Close | `root/proto33`; 27332; 19 | Numeric-zero guard 3..5; parent update 13; closure 17 |
| Enable helper | `root/proto30`; 20838; 34 | View test 4; row loop 10..22; numeric-zero comparison 18; three-result variation call 25; one-boolean returns 21/31/33 |
| Skill reset | `root/proto25`; 18005; 75 | Combo slots 2/3 writes 35/45; rank helper 50; zero values 58/66/74 |
| Remaining people | `root/proto29`; 20686; 11 | Fresh count 3; numeric-zero test 4; return 7 at 7; subtract count from 8 at 9 |
| Reached rank-range arm | `root/proto23`; 16044; 218 | Fresh player 3; category-zero test 5; state-skill call 9; cap call 10; common maxima/clamps 168..217 |
| Signal write/read | `root/proto41`; 33501; 10 / `root/proto42`; 33639; 7 | Numeric-zero guard 1..3 and fixed setter 9 / open getter tail-call 5 |

Authenticate the restricted archive with `manifests/private_lua_corpus.json`,
normalize only CRLF byte pairs in the selected decoded member, and check it
against `manifests/scripts.json`. Decode the separately authenticated LPB
with `tools/retail_script.py:decode_lpb`. The format-aware reader and
instruction decoder in `tools/build_quest_contracts.py` expose the prototype
bindings, predicates, call operands and return arities above without retaining
payloads or a disassembly. The original operands resolve notification arity,
strict comparisons and open tail-call results independently of decompiler
presentation. They do not establish that any branch executed at runtime.
