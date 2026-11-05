# Ul'dah normal tutorial flow

`Man0u0.processTtrNomal001withHQ` requests `MAN0U000` and then
`man0u005`. `processTtrNomal001` requests only `man0u005`. Both select a
device through repeated sampling, request camera lesson 1, wait for the
camera tutorial, request success presentation and then request movement
lesson 2. Each returns exactly one value, the last device-selector result.
Neither method selects or invokes the other or a battle tutorial method.

These are separately callable local contracts. Their names establish no
historical event selection or continuation to the
[Ul'dah battle and Judge contracts](uldah-opening-tutorial-contract.md).

## Inputs and roles

The inputs are extraction `2012.09.19.0001`, retail version `1.23b`.
The [Ul'dah input table](uldah-opening-tutorial-contract.md#input-identity)
owns the exact Man0u0 source, LPB and decoded-payload identities. Selected
members were authenticated against [scripts.json](../manifests/scripts.json),
the archive against [private_lua_corpus.json](../manifests/private_lua_corpus.json),
and resources and decoded payloads against
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Canonical normalization replaces CRLF byte pairs with LF only. This is
selected-input verification, without a new full-corpus validation.

A0 is the scenario receiver, A1 the supplied player-like receiver and A2 an
unused third formal. D denotes global `desktopWidget`, W global
`worldMaster`. These are operand roles, without authenticated runtime actor
identities or equality between A1 and a player fetched by a helper. Canonical
source ranges are `quest/scenario/man/man0u0.lua:666-933` for withHQ and
`:936-1204` for normal, relative to `lua/scripts/`.

## Entry and device loop

Both first call `A1:_lockCameraControl()`. WithHQ then unconditionally calls
`D:orderTutorialMode()`. Normal calls `D:isTutorialMode()` and orders tutorial
mode only when its first result is exactly false. Nil, zero and true skip
that order call. The getter returns the stored `tutorialFlag` directly.
The [tutorial-state contract](gridania-normal-tutorial-flow.md#initial-tutorial-state-and-device-selection)
owns the reached order helper's flag store, fetched player, lockon request,
mask and mode 120 request. Its name does not establish idempotence.

Both then order desktop mode 62, set mask `(true,true,true,true,true,4)`,
call `A1:_fadeInNowLoadingForNoticeEventJustInArea()`, call
`A0:startFadeOut(A1,0)` and wait 1 on A0. Their device loop is:

1. Read one result s from `W:_isKeyboardOnlyTutorial()`.
2. Save one result t from `D:askTutorialDeviceType()`, then wait 3 on A0.
3. Read a fresh result r from `W:_isKeyboardOnlyTutorial()`. If `r == s`,
   leave the loop. Otherwise read the predicate again, replace s with that
   new result, and repeat from step 2.

The first predicate does not suppress selection when true. A stable pair
performs two predicate calls and one selector call. A mismatch performs a
third predicate read before selecting again. Nil equals nil, while false
differs from numeric zero. There is no local retry limit or timeout.
Each selection replaces t, which is returned without a local 1/2 check.
A nil t remains one returned Lua value.

The [device-selector contract](tutorial-widget-vocabularies.md) owns its
default, buttons, stored value and returned result. Selection result exactly
true permits the ask-result read; an open result exactly nil skips selection.
Those comparisons do not validate the subsequently stored value.

## Scenes, dialogue and camera wait

WithHQ calls `A0:startHQCutScene("MAN0U000",3)` followed by
`A0:startNQCutScene("man0u005",3)`. Normal calls only that NQ starter.
The requests are sequential in withHQ, without an HQ/NQ alternative branch.
Both discard scene results. The
[scene-wrapper contract](quest-event-client-contracts.md#man304-man308-man402-and-man406-scene-wrappers)
owns forwarding and result boundaries. Playback, skip handling and server
progression are not established by these calls.

Both then follow this conditional normal-return order:

1. Call `A1:_waitForMapLoaded(nil)` with an explicit nil operand,
   call `A1:_fadeIn(5)` and wait 4 on A0.
2. Cancel desktop mode 61, request
   `D:openPublicInformDialogWidget(A0,118)`, call `A1:_waitForFading()` and
   wait 2 on A0. The request discards all helper results. The
   [public inform helper](job-grand-company-event-contracts.md#dont-hate-the-messenger-selector-paths)
   owns the actor check and result forwarding.
3. Order mode 16. Call `W:_runCharaSchedulerTutorial(1100003,353972224)`
   and then `W:_runCharaSchedulerTutorial(1100003,403087360)`.
   Call `A0:sayFreeDisplayName(1100003,A0,96)`, then
   `W:_waitForCharaSchedulerTutorialFinished(1100003,353972224)`.
   After that wait resumes, wait 0.5 on A0 and cancel mode 16.
4. Call `D:openTutorialWidget(t,1)`, then
   `A1:_unlockCameraControl()`, then `D:_waitForCameraTutorial()` with no
   data operand and no retained result.
5. After the camera wait resumes, close the tutorial widget, request
   `D:openTutorialSuccessWidget(9005,true)` and wait 3 on A0.

The scheduler wait is only for the first scheduler operand of the first
pair. These integers are call operands, without an authenticated actor,
animation or scheduler-entry identity. The yielding scheduler and camera
waits are owned by `xivl-client-structs:docs/tutorial-control-native-contract.md`,
section "Waits". The camera completion producer and its float-input boundary
are owned by `xivl-client-structs:docs/tutorial-camera-input-contract.md`,
sections "Installation and completion" and "Selected input writer and
remaining edge". Those contracts do not assign a physical control gesture
or establish actual instance invocation and scheduling for this flow.

InfoID 1 is Moving the Camera. The
[shared opener](tutorial-widget-opening-contract.md#complete-opener-partition)
replaces t with stored `tutorialDeviceType`, selects `Ask/TutorialWidget`
and uses the creation/selection wait branch for both selected lessons 1/2.
It returns no values and reads no tutorial answer. Camera unlock and wait
follow its normal return, including its nil-open path. Local t therefore
does not prove the stored value later used, widget creation or acceptance.
The [close contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup)
owns the slot-12 close request. The
[success helper](gridania-battle-tutorial-branches.md#btl003-and-btl004)
owns the static-widget-22 `setData` call. Neither request proves native
presentation or closure completion.

## Final movement lesson and cleanup

Both lock A1's camera control again, order mode 16 and call
`W:_aimCameraTutorial(1100003)`. They then call
`W:_lookAtPlayerTutorial(1100003)` and `W:_lookAtPlayerTutorial(1000347)`,
repeat the two scheduler starts above in the same order, and call
`A0:sayFreeDisplayName(1100003,A0,98)`. There is no scheduler wait after
this second pair.

Both call `D:_setTargetCharacter(1,nil)` with an explicit nil final operand,
order mode 16 again and then cancel mode 16. Neither calls a target tutorial
wait or consumes a target result. They call `D:openTutorialWidget(t,2)`,
set mask `(false,true,true,true,true,4)`, unlock A1's camera control, call
`W:_cancelAimCameraTutorial(1100003)` and return exactly one value, t.
InfoID 2 is Getting Around, as recorded in the
[lesson vocabulary](tutorial-widget-vocabularies.md).

There is no later local tutorial close, `cancelTutorialMode`, clearing of
`tutorialFlag`, explicit lockon unlock or `_cancelLookAtPlayerTutorial`.
The [mask contract](gridania-opening-tutorial-contract.md#scenario-order-and-cleanup)
owns stored-flag comparisons and control requests. The final mask and aim
cancellation do not establish balanced native counters or accepted input.
The return is the last selector result, without a camera, scene, lesson
answer or success-result dependency.

## Differences from Gridania normal

The [Gridania normal contract](gridania-normal-tutorial-flow.md) has the same
entry distinction, fresh-read device loop, explicit nil map/target operands,
camera lesson/wait/close/success ordering and one-value device return.
The selected original Ul'dah bodies establish these differences:

| Operation | Gridania | Ul'dah |
| --- | --- | --- |
| Scene keys | HQ `MAN0G000`, NQ `man0g005` | HQ `MAN0U000`, NQ `man0u005` |
| Inform and dialogue | Inform 94; operand 2300120, rows 72/74 | Inform 118; operand 1100003, rows 96/98 |
| First dialogue | No scheduler start/wait calls | Two scheduler starts, then one scheduler wait |
| After success delay | Aim and dialogue | Aim, two look-at calls, two scheduler starts and dialogue |
| After target request | Cancel mode 16 | Order mode 16 again, then cancel mode 16 |
| Final lesson and mask | Main Menu 5; `(true,true,true,true,true,1)` | Getting Around 2; `(false,true,true,true,true,4)` |

These are local callable differences, without a historical city dispatcher,
fresh-character property value or continuation to either city's battle flow.

## Original-bytecode locators and verification

Child indices are zero-based, PCs one-based, and code starts refer to the
decoded payload without its LPB wrapper. PC p starts at `codeStart+4*(p-1)`.

| Method | Root closure -> assignment PCs | Child / codeStart | Decisive PCs |
| --- | --- | --- | --- |
| withHQ | 84 -> 85 | 25 / `0x1BE0` | 5 orders tutorial mode; 37/49/54 read the predicate; 42 selects; 50 compares samples; 63/67 request HQ/NQ. |
| normal | 87 -> 88 | 26 / `0x2325` | 5 reads mode; 6 compares exact false; 10 conditionally orders; 42/54/59 read predicate; 47 selects; 55 compares samples; 68 requests NQ. |
| withHQ continuation | Same | Same | 70 map wait `B=3`; 99/104 scheduler starts; 114 scheduler wait; 126 lesson 1; 131 camera wait `B=2,C=1`; 134 close; 139 success; 156/160 look-at; 165/170 scheduler starts; 180 target `B=4`; 184 extra order; 193 lesson 2; 208 mask; 214 cancel aim; 215 `RETURN B=2`. |
| normal continuation | Same | Same | Corresponding continuation PCs are each one greater than withHQ, from map wait 71 through `RETURN B=2` at 216. |

Use `tools/retail_script.py:decode_lpb` and the fixed Lua 5.1 reader,
instruction decoder and closure-state analysis in `tools/build_quest_contracts.py`.
Authenticate the source, resource and payload identities, check complete
payload consumption and bind methods through root assignments before
following comparisons and jumps. The final zero-value compiler epilogue
after each explicit one-value return is not a second reachable return path.

Original-instruction interpretation checked mode false/nil/zero, stable and
changing predicate reads, unvalidated device values, sequential scenes,
receiver roles, explicit nil arity, scheduler/camera ordering, final masks,
discarded call results and cleanup. Mock API results were explicit check
inputs, without runtime authority. Mutations of these comparisons, predicate
refresh, callback names, scheduler/look-at operands, scenes, lesson, target
arity, mode order, final mask, cancellation and return arity were rejected.

The boundary remains actual method invocation, supplied actor identity,
player properties, stored-device changes outside these calls, scene and
widget acceptance, native input, wait/callback delivery and scheduling,
and historical server selection or successor events. No accepted
fresh-character progression was observed.
