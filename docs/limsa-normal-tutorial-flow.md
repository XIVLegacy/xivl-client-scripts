# Limsa normal tutorial flow

`Man0l0.processTtrNomal001withHQ` requests HQ scene `MAN0L000` and then
NQ scene `man0l005`; `processTtrNomal001` requests only that NQ scene.
Both request camera lesson 1, wait for the camera tutorial, request success
presentation, then request movement lesson 2. They return exactly one value:
the last local result of the tutorial device selector.

These are independently authenticated local contracts. Neither method name
establishes historical selection, a successful lesson, or a continuation to
another normal or [battle tutorial method](limsa-opening-tutorial-contract.md).

## Inputs and operand roles

The extraction is `2012.09.19.0001`, retail version `1.23b`. The
[Limsa input table](limsa-opening-tutorial-contract.md#input-identity-and-locators)
owns the exact Man0l0 source, LPB and decoded-payload identities. Selected
archive members were authenticated against
[scripts.json](../manifests/scripts.json), the archive against
[private_lua_corpus.json](../manifests/private_lua_corpus.json), and original
resources and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Canonical normalization replaces CRLF byte pairs with LF only. This selected
verification did not regenerate or validate the entire corpus.

Source ranges are `lua/scripts/quest/scenario/man/man0l0.lua:892-1157`
for withHQ and `:1160-1426` for normal. A0 is the scenario receiver, A1 the
supplied player-like receiver and A2 an unused third formal. D denotes global
`desktopWidget` and W global `worldMaster`. These are operand roles, without
authenticated runtime actor identities. A player fetched inside a helper is
not thereby established to equal A1.

## Mode, device and scene requests

Both first call `A1:_lockCameraControl()`. WithHQ then calls
`D:orderTutorialMode()` unconditionally. Normal reads one result from
`D:isTutorialMode()` and orders tutorial mode only when that result is
exactly false. Nil, zero and true skip this order in normal.

The [shared mode contract](gridania-normal-tutorial-flow.md#initial-tutorial-state-and-device-selection)
owns the direct stored-flag getter and unconditional order helper's effects;
the [mask contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup)
owns its stored-flag comparisons and control changes. An already true flag
does not establish that an unconditional order is idempotent or that native
counters are balanced.

Both next order desktop mode 62, explicitly set mask
`(true,true,true,true,true,4)`, call
`A1:_fadeInNowLoadingForNoticeEventJustInArea()`, call
`A0:startFadeOut(A1,0)` and wait 1 on A0. Their device loop then:

1. Reads one result s from `W:_isKeyboardOnlyTutorial()`.
2. Saves one result t from `D:askTutorialDeviceType()` and waits 3 on A0.
3. Reads a fresh result r from `W:_isKeyboardOnlyTutorial()`. Equality
   `r == s` exits. A mismatch reads the predicate again, replaces s with
   that new result and repeats from step 2.

An initial true predicate does not skip the selector. A stable pair uses
two predicate reads and one selector call. A mismatch uses a third fresh
read before the next selector, with no local retry limit or timeout. Nil
equals nil; false and numeric zero differ. Each iteration replaces t.
The [device selector](tutorial-widget-vocabularies.md) owns its default,
widget/result guards, stored device and unvalidated selected result. Thus
t can be nil, false or zero; these methods do not rewrite it to 1.

After the loop, withHQ sequentially requests
`A0:startHQCutScene("MAN0L000",3)` then
`A0:startNQCutScene("man0l005",3)`. Normal requests only the latter.
Both discard scene results. There is no local HQ/NQ alternative-result
branch. The [HQ wrapper contract](quest-event-client-contracts.md#man304-man308-man402-and-man406-scene-wrappers)
owns its forwarding and return boundary; these calls establish no rendered
playback, skip outcome or historical scene-completion policy.

## Camera lesson and success request

On normal return from the preceding calls, both follow this sequence:

1. Call `A1:_waitForMapLoaded(nil)` with an explicit nil operand,
   call `A1:_fadeIn(5)` and wait 4 on A0.
2. Cancel desktop mode 61, request
   `D:openPublicInformDialogWidget(A0,96)`, call
   `A1:_waitForFading()` and wait 2 on A0. The inform result is discarded;
   the [public inform helper](job-grand-company-event-contracts.md#dont-hate-the-messenger-selector-paths)
   owns its actor check and show-result boundary.
3. Order desktop mode 16, request
   `W:_runCharaSchedulerTutorial(1600150,354086912)`, call
   `A0:sayFreeDisplayName(1600150,A0,89)`, wait 0.5 on A0 and cancel mode 16.
4. Call `D:openTutorialWidget(t,1)`, unlock A1's camera control, then call
   `D:_waitForCameraTutorial()` with no data operand and no retained result.
5. After that wait resumes, call `D:closeTutorialWidget()`, request
   `D:openTutorialSuccessWidget(9005,true)` and wait 3 on A0.

InfoID 1 is Moving the Camera. The
[opener contract](tutorial-widget-opening-contract.md#complete-opener-partition)
owns the stored-controller override, Ask module path and creation/selection
wait. It returns no values and reads no tutorial answer. Camera unlock and
the camera wait follow a normal opener return, including a nil-open path.
Local t therefore proves neither the controller later reread from D nor
successful widget creation or acceptance.

The slot-12 close request is owned by the
[shared cleanup contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup).
The [success helper](limsa-opening-tutorial-contract.md#success-and-inform-helpers)
owns the static lookup and setData forwarding without a nil guard, wait or
return value. Neither request proves native completion.

The camera wait's checker and completion-bit observation are owned by
`xivl-client-structs:docs/tutorial-control-native-contract.md`, section
"Waits". The phase sequence and selected float-input boundary are owned by
`xivl-client-structs:docs/tutorial-camera-input-contract.md`, sections
"Installation and completion" and "Selected input writer and remaining edge".
This Lua call order establishes no keyboard, mouse or gamepad gesture,
actual camera instance, callback delivery or wait scheduling.

## Dialogue argument and final movement lesson

After the success delay, both lock A1's camera control again, order desktop
mode 16 and issue these requests on W, in order:
`_aimCameraTutorial(1600150)`, `_lookAtPlayerTutorial(1600150)`,
`_runCharaSchedulerTutorial(1600150,353959936)` and
`_runCharaSchedulerTutorial(1600150,403087360)`. Their results are discarded.
There is no explicit scheduler-completion wait in either selected body.

Both retain one result v from `A1:getTribe()`, then replace that local value
using ordered inclusive numeric range tests:

| Tested range | Replacement |
| --- | ---: |
| 1 through 3 | 1 |
| 4 through 7 | 2 |
| 8 through 11 | 3 |
| 12 through 13 | 4 |
| 14 through 15 | 5 |
| No range matches | Original v |

This is the actual local comparison rule, without a finite tribe enumeration,
an actor-property identity or a localized race-name assignment. They then
call `A0:sayFreeDisplayName(1600150,A0,91,v)` with that local value as an
extra dialogue operand.

Both next call `D:_setTargetCharacter(1,nil)`, preserving the explicit final
nil. They order desktop mode 16 again, cancel mode 16, request
`D:openTutorialWidget(t,2)`, set mask `(false,true,true,true,true,4)`, unlock
A1's camera control, call `W:_cancelAimCameraTutorial(1600150)` and return
exactly one value, t. The extra order before cancellation is present in
both original bodies; it is not removed as a redundant request.

InfoID 2 is Getting Around and uses the opener's creation/selection wait
group. Its results are discarded. The final mask requests flag 1 false
while flags 2-5 stay true and menu type stays 4; the mask helper's stored
flag comparisons govern its control calls. This is not an all-unlocked
cleanup. There is no later local tutorial close, target tutorial wait,
`cancelTutorialMode`, clearing of `tutorialFlag`, explicit lockon unlock
or `_cancelLookAtPlayerTutorial` call. No balanced native-control state
is established. The target request itself is not a target-completion wait.

The returned t is the last selector result, not a scene result, camera
result, lesson answer or success flag. Nil t remains one returned Lua value.
Neither selected method invokes the other or a successor tutorial method.

## Differences from Gridania normal flow

The [Gridania normal contract](gridania-normal-tutorial-flow.md) provides the
comparison. Limsa's mode guard, fresh-read device loop, delays, explicit
nil map/target operands, camera lesson/wait/close/success sequence and
one-value selector return have the same independently checked local rules.
The following differences prevent copying Gridania's full sequence:

| Operation | Limsa | Gridania |
| --- | --- | --- |
| Scene keys | HQ `MAN0L000`, NQ `man0l005` | HQ `MAN0G000`, NQ `man0g005` |
| Public inform row | 96 | 94 |
| Speaker and camera operand | 1600150 | 2300120 |
| Dialogue before camera lesson | Row 89, after scheduler 354086912 | Row 72, without that scheduler request |
| Dialogue after success | Row 91 with transformed getTribe result; preceded by look-at and schedulers 353959936/403087360 | Row 74 without an extra dialogue operand or those requests |
| After target request | Order mode 16 again, then cancel it | Cancel mode 16 |
| Final lesson | 2, Getting Around | 5, The Main Menu |
| Final mask | `(false,true,true,true,true,4)` | `(true,true,true,true,true,1)` |

## Original-bytecode locators and verification

Child indices are zero-based; PCs are one-based. Offsets address the decoded
payload, excluding the LPB wrapper. PC p starts at `codeStart + 4*(p-1)`.

| Method | Root closure -> assignment PCs | Child / codeStart | Decisive PCs |
| --- | --- | --- | --- |
| withHQ | 99 -> 100 | 30 / `0x20FE` | 5 orders tutorial mode; 37/49/54 predicate reads; 38/50 loop tests; 42 selects device; 63/67 request HQ/NQ scenes. |
| normal | 102 -> 103 | 31 / `0x28AC` | 5 reads tutorial mode; 6 tests exact false; 10 conditionally orders it; 42/54/59 predicate reads; 43/55 loop tests; 47 selects device; 68 requests NQ. |
| withHQ continuation | Same | Same | 70 map wait `B=3`; 116 lesson 1; 121 camera wait `B=2,C=1`; 124 close; 129 success; 158 getTribe; 159-188 range mapping; 198 target `B=4`; 202/206 order/cancel 16; 211 lesson 2; 226 mask; 228 unlock; 232 cancel aim; 233 `RETURN B=2`. |
| normal continuation | Same | Same | 71 map wait `B=3`; 117 lesson 1; 122 camera wait `B=2,C=1`; 125 close; 130 success; 159 getTribe; 160-189 range mapping; 199 target `B=4`; 203/207 order/cancel 16; 212 lesson 2; 227 mask; 229 unlock; 233 cancel aim; 234 `RETURN B=2`. |

Authenticate selected source members, original LPBs and decoded payloads,
parse the full Lua 5.1 chunks with `tools/build_quest_contracts.py` and bind
closures through root assignments. `tools/retail_script.py:decode_lpb` owns
wrapper decoding. Check actual comparisons, calls, jumps, explicit nil
operands, result counts and final reachable returns.

Branch-sensitive checks used explicit mock API results to distinguish exact
false from nil/zero, stable and mismatching predicate reads, selector-result
replacement and unvalidated return values, each range boundary and unmatched
numeric values. They checked scene order, lesson IDs, scheduler/look-at
requests, camera wait/close/success order, the extra mode order, final mask,
cleanup and one-value returns. Mutations to the mode/device/tribe comparisons,
camera wait, final lesson, target arity, selector-result count, aim cancellation
and return arity were rejected. These checks interpret original instructions;
they do not execute a retail tutorial.

The contract stops at actual invocation and actor/property binding, external
stored-device changes, native input/scene/widget acceptance, callback and wait
scheduling, external server selection and a historical successor. It does
not establish accepted fresh-character progression.
