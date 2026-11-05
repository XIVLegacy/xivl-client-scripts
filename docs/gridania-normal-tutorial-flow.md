# Gridania normal tutorial flow

`Man0g0.processTtrNomal001withHQ` requests HQ scene `MAN0G000` and then
NQ scene `man0g005`. `processTtrNomal001` requests only the NQ scene. Both
select a tutorial device through a repeated sampling loop, request camera
lesson 1, wait for the camera tutorial, request success presentation and
then request main-menu lesson 5. Each returns one value: the last local
result of the device selector, without testing a tutorial acceptance result.

These are separately callable local contracts. Their names establish neither
which method a historical event selected nor a continuation to the
[battle tutorial methods](gridania-opening-tutorial-contract.md).

## Inputs and operand roles

The extraction is `2012.09.19.0001`, retail version `1.23b`. Selected source
members were authenticated against [scripts.json](../manifests/scripts.json),
the containing archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json), and original
resources and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Canonical normalization replaces CRLF byte pairs with LF only. The
[Gridania input table](gridania-opening-tutorial-contract.md#input-identity-and-method)
owns the exact Man0g0 and desktop connector identities. This is selected-input
verification, without a new full-corpus validation or regeneration.

A0 is the scenario receiver, A1 the supplied player-like receiver and A2 an
unused third formal in both methods. D denotes global `desktopWidget` and W
global `worldMaster`. These are operand roles, without authenticated runtime
actor identities or an assertion that a player fetched through W equals A1.
Source ranges are `man0g0.lua:354-576` for withHQ and `:579-802` for normal.

## Initial tutorial state and device selection

Both first call `A1:_lockCameraControl()`. WithHQ then calls
`D:orderTutorialMode()` unconditionally. Normal calls `D:isTutorialMode()`
and orders tutorial mode only when its first result is exactly false.
Nil, zero and true skip that order call in normal.

The reached connector getter returns `D.work.tutorialFlag` directly.
`orderTutorialMode` stores true in that field, fetches a player through W,
requests its lockon-control lock, sets mask `(true,true,true,true,true,4)`
and orders desktop mode 120. It does not first test the old flag. Thus the
withHQ call is not established to be idempotent by its name or by a previously
true flag. The
[shared mask contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup)
owns stored-flag comparisons and their control effects.

After that conditional difference, both order desktop mode 62, explicitly
set mask `(true,true,true,true,true,4)`, call
`A1:_fadeInNowLoadingForNoticeEventJustInArea()`, call
`A0:startFadeOut(A1,0)` and wait 1 on A0.

The device loop then follows this exact sampling rule:

1. Read one result s from `W:_isKeyboardOnlyTutorial()`.
2. Save one result t from `D:askTutorialDeviceType()`, then wait 3 on A0.
3. Read a fresh result r from `W:_isKeyboardOnlyTutorial()`. If `r == s`,
   leave the loop. Otherwise read that predicate again, replace s with this
   new result, and repeat from step 2.

The first predicate does not suppress the selector when true. The comparison
is equality between separate reads, not equality with false or a cached
Boolean test. Nil equals nil, while false and numeric zero differ. A stable
pair performs two predicate calls and one selector call. A mismatch performs
a third predicate read before the next selector. There is no local retry limit
or timeout, and the mismatch-refresh value can differ from both earlier reads.

The [device selector contract](tutorial-widget-vocabularies.md) owns its
initial value 1, mode-selector buttons, stored `tutorialDeviceType` and
returned value. Its widget nil test and selection result are distinct:
an exactly nil open result skips selection, and only selection result exactly
true causes an ask-result read. A read ask result is stored and returned
without a local 1/2 validation. In particular, nil, false and zero are not
rewritten to 1 after a successful selection-result test. Each loop iteration
replaces local t with the selector's first result.

## Scene and camera lesson order

On normal return from the device loop, withHQ calls
`A0:startHQCutScene("MAN0G000",3)` followed by
`A0:startNQCutScene("man0g005",3)`. Normal calls only that NQ starter.
These are sequential requests in withHQ, without an HQ/NQ result branch or
an alternate-scene predicate. Both discard scene results. The
[quest scene wrapper contract](quest-event-client-contracts.md#man304-man308-man402-and-man406-scene-wrappers)
describes the HQ wrapper's forwarding and result boundary. No completion,
skip result, rendered playback or server progression is inferred here.

Both then execute this conditional normal-return sequence:

1. Call `A1:_waitForMapLoaded(nil)`, preserving the explicit nil operand,
   call `A1:_fadeIn(5)`, and wait 4 on A0.
2. Cancel desktop mode 61, request
   `D:openPublicInformDialogWidget(A0,94)`, call `A1:_waitForFading()` and
   wait 2 on A0. The inform request's results are discarded. Its
   [public helper contract](job-grand-company-event-contracts.md#dont-hate-the-messenger-selector-paths)
   owns the actor check and forwarded show results.
3. Order desktop mode 16, call
   `A0:sayFreeDisplayName(2300120,A0,72)`, wait 0.5 on A0 and cancel mode 16.
4. Call `D:openTutorialWidget(t,1)`, then
   `A1:_unlockCameraControl()`, then `D:_waitForCameraTutorial()` with no
   data operand and no retained result.
5. After the camera wait resumes, call `D:closeTutorialWidget()`, request
   `D:openTutorialSuccessWidget(9005,true)` and wait 3 on A0.

InfoID 1 is Moving the Camera. The
[shared opener](tutorial-widget-opening-contract.md#complete-opener-partition)
replaces formal t with `D.work.tutorialDeviceType`, opens
`Ask/TutorialWidget` through its creation/selection wait branch and returns
no values. The scenario does not read its ask result. Camera unlock and the
native tutorial wait follow the opener's normal return, including its nil-open
path. The local t is therefore not proof of the device value later reread by
the opener, successful widget creation or acceptance.

The camera wait and its yielding checker are owned by
`xivl-client-structs:docs/tutorial-control-native-contract.md`, section
"Waits". The completion producer is owned by
`xivl-client-structs:docs/tutorial-camera-input-contract.md`, sections
"Installation and completion" and "Selected input writer and remaining edge".
Those publications establish the selected completion-bit observation and
phase sequence. They leave the actual camera payload's float producer,
physical input, instance and scheduling unresolved. This Lua flow adds the
call order, without assigning a keyboard, mouse or gamepad gesture to the wait.

The close is a slot-12 close request whose result is ignored, as described in
the [shared cleanup contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup).
The success helper obtains static widget 22 and calls its
`setData(9005,true)` without a nil test, wait or returned value. Its
[shared implementation](gridania-battle-tutorial-branches.md#btl003-and-btl004)
does not establish native presentation or closure completion.

## Final target request and cleanup

After the success delay, both lock A1's camera control again, order mode 16,
call `W:_aimCameraTutorial(2300120)`, then
`A0:sayFreeDisplayName(2300120,A0,74)`. Both call
`D:_setTargetCharacter(1,nil)`, with an explicit nil final operand. This is
not a target tutorial wait, and no target result is consumed. The separate
published `_waitForTargetTutorial` contract in
`xivl-client-structs:docs/tutorial-control-native-contract.md`, section
"Target wait and unchanged selection", supplies no additional completion
condition for this method because neither selected body calls that wait.

Both then cancel mode 16, call `D:openTutorialWidget(t,5)`, set mask
`(true,true,true,true,true,1)`, unlock A1's camera control, call
`W:_cancelAimCameraTutorial(2300120)` and return exactly one value, t.
InfoID 5 is The Main Menu and uses the same creation/selection wait group as
infoID 1. Its result is discarded. There is no subsequent local slot-12 close,
`cancelTutorialMode`, clearing of `tutorialFlag` or lockon-control unlock.
The final all-true mask is not an all-unlocked cleanup request. These calls
do not establish balanced native control counters.

The returned t is the last selector result, not a camera result, scene result,
lesson answer or success flag. A nil t is still one returned Lua value.
Neither body invokes the other body or any battle tutorial method.

## Original-bytecode locators and verification

Child indices below are zero-based. PCs are one-based within their prototype.
Offsets are decoded-payload offsets excluding the LPB wrapper. An instruction
at PC p starts at `codeStart + 4*(p-1)`.

| Method | Root closure -> assignment PCs | Child / codeStart | Decisive PCs |
| --- | --- | --- | --- |
| withHQ | 48 -> 49 | 13 / `0xF98` | 5 orders tutorial mode; 37/49/54 read the predicate; 38/50 test loop flag/equality; 42 selects device; 63 then 67 request HQ then NQ scenes. |
| normal | 51 -> 52 | 14 / `0x15C7` | 5 reads tutorial mode, 6 compares exact false, 10 conditionally orders it; 42/54/59 read the predicate; 43/55 test loop flag/equality; 47 selects device; 68 requests NQ. |
| withHQ continuation | Same | Same | 70 map wait `B=3`; 111 lesson 1; 113 unlock; 116 camera wait `B=2,C=1`; 119 close; 124 success; 147 target `B=4`; 162 lesson 5; 171 mask; 173 unlock; 177 cancel aim; 178 `RETURN B=2`. |
| normal continuation | Same | Same | 71 map wait `B=3`; 112 lesson 1; 114 unlock; 117 camera wait `B=2,C=1`; 120 close; 125 success; 148 target `B=4`; 163 lesson 5; 172 mask; 174 unlock; 178 cancel aim; 179 `RETURN B=2`. |
| Connector orderTutorialMode | 458 -> 459 | 152 / `0x161AE` | 2 stores true; 5 fetches player; 7 locks lockon control; 15 sets mask; 18 orders mode 120. |
| Connector isTutorialMode | 467 -> 468 | 155 / `0x1669B` | 3 returns stored tutorialFlag, `RETURN B=2`. |

Use `tools/retail_script.py:decode_lpb` and the fixed Lua 5.1 reader,
instruction decoder and closure-state analysis in
`tools/build_quest_contracts.py`. Authenticate source, resource and payload
identities, check complete payload consumption and bind methods through the
root assignments before following the selected calls and jumps.

Branch-sensitive interpretation of the original instructions checked exact
false versus nil/zero, stable and changing predicate reads, device values,
sequential scenes, explicit nil arity, camera wait/close/success ordering,
final masks and cleanup, discarded call results and one-value local returns.
Mock API results were explicit inputs to these checks, without runtime
authority. Mutations to mode and device comparisons, the wait callback,
lesson value, target arity, selector-result adjustment, final cancellation
and return arity were rejected. No retail bodies, payloads or listings are
required in the retained contract.

The contract stops at actual method invocation and actor binding, player
properties, stored-device changes outside these calls, native input identity,
widget creation and acceptance, callback delivery, wait scheduling and
external event selection. It does not establish accepted fresh-character
progression or a historical successor event.
