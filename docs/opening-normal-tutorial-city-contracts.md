# Normal opening tutorials across cities

The six selected normal tutorial callables share their mode/device entry and
camera-lesson sequence. Their scene, dialogue, scheduler and final-lesson
requests differ by city. Gridania finishes with Main Menu lesson 5;
Limsa and Ul'dah finish with Getting Around lesson 2 and a different mask.
Consumers can share the established common sequence while preserving the
requests listed for each city below.

The canonical local contracts are [Gridania](gridania-normal-tutorial-flow.md),
[Limsa](limsa-normal-tutorial-flow.md) and
[Ul'dah](uldah-normal-tutorial-flow.md). Each covers that scenario's
`processTtrNomal001withHQ` and `processTtrNomal001`. These names establish
callable contracts, without selecting a historical method or a successor.
The [battle tutorial comparison](opening-tutorial-city-contracts.md) owns
the separate class branches in battle tutorials.

## Shared local sequence

All six first lock the supplied player-like receiver's camera control.
WithHQ unconditionally requests tutorial mode. Normal requests it only when
the stored-mode getter's first result is exactly false; nil, zero and true
skip that order. The
[shared mode contract](gridania-normal-tutorial-flow.md#initial-tutorial-state-and-device-selection)
owns the reached helper's stored flag, fetched player and control requests.
The fetched player is not thereby established to equal the supplied receiver.

All six use the same independently checked device loop: sample the keyboard
only predicate, select one local device result t, wait 3, and compare a fresh
predicate result with the saved sample. A mismatch takes another fresh sample
before selecting again. A true first sample does not skip selection. There
is no local retry limit or 1/2 validation of t. The stored controller later
read by the [tutorial opener](tutorial-widget-opening-contract.md) is a
separate value from that local t.

In every city, withHQ requests its HQ scene and then its NQ scene, discarding
both results. Normal requests only the NQ scene. These are sequential requests,
without a branch that selects a scene from an HQ/NQ result or a proved
playback/skip outcome.

After the first dialogue, all six request camera lesson 1,
unlock camera control and call the native camera tutorial wait. After that
wait resumes, they request a tutorial close, success presentation with
`(9005,true)`, and a wait of 3. The opener's creation/selection wait is
distinct from the following native camera wait. Neither supplies a retained
lesson-acceptance result to these scenario methods.

All six later request `_setTargetCharacter(1,nil)` with its explicit nil
operand. None calls a target tutorial wait. After the final lesson and mask,
each unlocks camera control, cancels its aim request and returns exactly one
value, t. Nil t remains one returned Lua value. The return is independent of
a scene result, camera result or lesson answer.

## Requests by city

Each column refers to the linked city's normal/withHQ contracts. Scheduler,
speaker and camera numbers are call operands, without an authenticated
runtime actor or animation assignment.

| Operation | [Gridania](gridania-normal-tutorial-flow.md) | [Limsa](limsa-normal-tutorial-flow.md) | [Ul'dah](uldah-normal-tutorial-flow.md) |
| --- | --- | --- | --- |
| HQ / NQ scene keys | `MAN0G000` / `man0g005` | `MAN0L000` / `man0l005` | `MAN0U000` / `man0u005` |
| Inform row | 94 | 96 | 118 |
| Main speaker/camera operand; dialogue rows | 2300120; 72/74 | 1600150; 89/91 | 1100003; 96/98 |
| Before first dialogue | No scheduler start request | Start 354086912 | Start 353972224, then 403087360 |
| After first dialogue | No scheduler wait request | No scheduler wait request | Wait for 353972224 on operand 1100003 |
| After success delay | Aim, then dialogue | Aim, look-at, starts 353959936/403087360, then dialogue | Aim, look-at on 1100003 and 1000347, starts 353972224/403087360, then dialogue |
| Extra final dialogue operand | None | One locally transformed getTribe result | None |
| After target request | Cancel mode 16 | Order mode 16 again, then cancel it | Order mode 16 again, then cancel it |
| Final lesson | 5, The Main Menu | 2, Getting Around | 2, Getting Around |
| Final mask | `(true,true,true,true,true,1)` | `(false,true,true,true,true,4)` | `(false,true,true,true,true,4)` |

The second scheduler pairs in Limsa and Ul'dah have no explicit following
scheduler-completion wait in these bodies. Limsa's
[dialogue-argument contract](limsa-normal-tutorial-flow.md#dialogue-argument-and-final-movement-lesson)
owns the inclusive numeric getTribe ranges and unmatched-value behavior.
This comparison assigns no localized race name or native property identity
to that argument.

## Cleanup and evidence boundary

Each method returns after its final opener without another local tutorial
close request, `cancelTutorialMode` call or explicit lockon-control unlock.
Limsa and Ul'dah also issue no explicit look-at cancellation. The final masks
and normal returns do not establish balanced native counters, closed widgets
or accepted input.

The city publications own exact source/LPB/payload identities, root closure
bindings, original branch/call/return locators and semantic checks. They
identify the same `2012.09.19.0001` extraction. This comparison adopts those
contracts without a new original-body, native or capture study.

Actual external method selection, supplied/fetched actor equality, stored
values, native input and scene/widget acceptance, callback scheduling and
historical progression remain unproved. A matching local loop, final lesson
or return value does not establish a same-player city-opening sequence.
