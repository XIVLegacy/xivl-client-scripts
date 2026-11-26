# Tutorial mode control locks, menu lesson release and cancel routes

`DesktopWidget.setTutorialMask` holds the player-control lock that tutorial
mode takes. A mask whose first flag changes to `true` calls
`_lockPlayerControl`, and only a later mask whose first flag changes calls
`_unlockPlayerControl`. After the
[Gridania normal tutorial](gridania-normal-tutorial-flow.md#final-target-request-and-cleanup),
whose final mask is all `true` with menu type 1, three widget callbacks
advance a menu lesson that releases that lock when the main menu closes.
`cancelTutorialMode` releases it as part of leaving tutorial mode.

These are recovered Lua call contracts. They do not establish a historical
server message, callback delivery, native lock counters or accepted input.

## Stored tutorial state

`DesktopWidget.init` stores `tutorialFlag=false`, `tutorialMenuType=0`,
`tutorialMenuStatus=0`, `tutorialDeviceType=1` and `false` in each of the
five `tutorialLockFlag` elements.

`setTutorialMask(f1,f2,f3,f4,f5,type)` (`root/proto154`) fetches a player
through `worldMaster:_getMyPlayer()`. A nil operand leaves its element
alone. It does not read `tutorialFlag`.

| Operand | PCs | Action when the operand differs from the stored value |
| --- | --- | --- |
| f1 | 4-20 | Store it. Exactly `true` calls the fetched player's `_lockPlayerControl`, and any other value calls `_unlockPlayerControl`. |
| f2 | 21-37 | Store it. Exactly `true` calls `_lockTargetCursorControl` on the desktop, and any other value calls `_unlockTargetCursorControl`. |
| f3 | 38-42 | Stored whenever non-nil, without a comparison or a call. |
| f4 | 43-53 | Store it and request the final static-15 button mask update. |
| f5 | 54-68 | Store it and call `updateButtonMask` on static widget 7. |
| type | 69-82 | Store `tutorialMenuType`, call `updateButtonMask` on static widget 1 and request the static-15 update. |

PCs 83-89 call `updateButtonMask` on static widget 15 when f4 or the type
changed. Repeating a mask with f1 `true` therefore issues no second player
lock. Starting from the initial `false`, `orderTutorialMode` reaches the one
`_lockPlayerControl` call through its all-`true` mask. While the stored f1
stays `true`, a later all-`true` mask issues none. After a mask has stored
`false`, the next `true` f1 calls `_lockPlayerControl` again. The lock effect
of an all-`true` mask, such as those in `Man0g1.processEventTu_001`,
therefore depends on the stored value.

`orderTutorialMode` (`root/proto152`) sets `tutorialFlag=true`, calls
`_lockLockonControl`, requests mask `(true,true,true,true,true,4)` and orders
desktop mode 120. `cancelTutorialMode` (`root/proto153`) calls
`_unlockLockonControl`, requests mask `(false,false,false,false,false,0)`,
cancels desktop mode 120 and sets `tutorialFlag=false`. Its mask releases the
player and target-cursor locks only for elements stored as `true`. Neither
method writes `tutorialMenuStatus`.

While `tutorialFlag` is `false`, `getTutorialMenuType` and
`getTutorialMenuStatus` return 0 and `setTutorialMenuStatus` writes nothing
(`root/proto157` to `root/proto159`).

## Main menu lesson release

All three callbacks require `getTutorialMenuType() == 1` and one status.
Lesson numbers are the infoIDs in
[Tutorial controller and Ask widget values](tutorial-widget-vocabularies.md).

| Status | Callback | Ordered requests on the matching arm | New status |
| ---: | --- | --- | ---: |
| 0 | `MainMenuWidget.processBeforeShow` | `closeTutorialWidget()`, then `openTutorialWidget(nil,16)` | 1 |
| 1 | `QuestDetailWidget.processUICommandDefault` for `UILuaCommands.Shown` | `closeTutorialWidget()` | 2 |
| 2 | `MainMenuWidget.processUICommandClose` | Initial-town branch below | 3 |

`MainMenuWidget.processBeforeShow` (`root/proto4`) reaches the test at PCs
30-51 after `updateMainMenu`, then returns `true`. The test does not read the
method's formal.

The `QuestDetailWidget` arm (`root/proto3`, PCs 31-47) follows the
[`Shown` handling](quest-detail-widget-contract.md#ordinary-journal-detail-request).
It is not limited to mode 1. In mode 1, an exactly false detail request
returns before it.

`MainMenuWidget.processUICommandClose` (`root/proto2`) fetches the player
through the world master and compares the first result of `getInitialTown`
with 2 (PCs 10-15):

| First `getInitialTown` result | Lesson | Mask | PCs |
| --- | ---: | --- | --- |
| Equals 2 | 17 | `(false,true,true,true,true,4)` | 17-30 |
| Any other value | 14 | `(false,false,false,true,false,3)` | 32-45 |

Both masks pass `false` first, so a stored `true` produces one
`_unlockPlayerControl`. The lockon-control lock is not touched, and
`tutorialFlag` stays set. Type 4 also satisfies
[`isTutorialMainMenuMask`](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/script/main-menu-command-route.md),
which makes `processCommandMainMenu` return early. Whether or not any
tutorial test matched, the method then stores `mainMenuIndex` and calls
`hide` (PCs 50-56).

## Numeric data-packet route

`PlayerBaseClass._onReceiveDataPacket(self,key,...)` first calls the
superclass method. Keys `requestedData` and `attention` take their own arms.
For any other key whose `type` is `number`, it calls
`desktopWidget:processUpdateGeneralNotificationDialog(key,v1,v2,v3,...)`,
where v1 to v3 are the first three variable operands and the rest follow
from the fourth (`root/proto31`, PCs 32-48).

`processUpdateGeneralNotificationDialog(code,a2,a3,a4,...)`
(`root/proto99`) dispatches on the code:

| Code | Request |
| ---: | --- |
| 10 | `openPublicInformLongDialogWidget(a2,a4,...)` |
| 1 | `openCautionInformDialogWidget(a2,a4,...)` |
| 3 | `openPublicEffectWidget(a4)` |
| 2 | `openTutorialSuccessWidget(a4,true)` |
| 4 | `openTutorialWidget(a4,v)`, where v is the first further operand |
| 5 | `closeTutorialWidget()` |
| 7 | When `isTutorialMode()` is exactly `true`, `closeTutorialWidget()` then `cancelTutorialMode()` (PCs 56-64) |
| 8 | `closeRaidDungeonExecutionWidget()` |
| 9 | When `isTutorialMode()` is exactly `false`, `orderTutorialMode()`. Then mask `(false,false,false,true,true,3)` (PCs 75-95) |

Other codes make no request. Code 7 is thus a data-packet cancel route that
needs no quest scene method. Which message, sender or game event supplies a
numeric key is outside these Lua bodies.

## Other cancel consumers

`Man0g1.processEvent110` (`root/proto11`), `Man0l1.processEvent020`
(`root/proto9`) and `Man0u1.processEvent010` (`root/proto12`) share one
guarded sequence at PCs 0-15. When `isTutorialMode()` is exactly `true`,
they cancel desktop mode 16, call `cancelTutorialMode()` and order desktop
mode 16 again.

A search of the 2671 decoded payloads for the NUL-terminated constant
`cancelTutorialMode` finds it in the desktop connector, these three scenario
scripts and `commanddebugger/commanddebuggertest.lua`.
`setTutorialMenuStatus` and `getTutorialMenuStatus` occur in the connector
and the two widgets above. `processUpdateGeneralNotificationDialog` occurs
in the connector, `PlayerBaseClass` and the two raid directors whose code 3
call is in the
[content director contracts](content-director-ui-contracts.md). A constant
search does not cover a method name computed at run time.

## Source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. Each installed resource
matched [retail_lua_coverage.json](../manifests/retail_lua_coverage.json),
and each member regenerated from it with `tools/retail_script.py` and the
pinned unluac matched [scripts.json](../manifests/scripts.json). Prototype
indices and PCs are zero-based positions in the `unluac --disassemble`
listing.

| Canonical source | Bytes | SHA-256 |
| --- | ---: | --- |
| `widget/desktopwidget_connector.lua` | 660617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/mainmenuwidget.lua` | 58470 | `7DFD161C2852A56FD598F47469CC2D7597BA9F0E4B228555A09274674B2B4E41` |
| `widget/ask/questdetailwidget.lua` | 23972 | `0D1474C6B43CCE61D90A75BA0FE32E2B1D77504FD396024EE32A8876EBC8C8CE` |
| `chara/player/playerbaseclass.lua` | 66466 | `6226B3FA15DFDBAD279B7DBA453F8A3B76FCB8B68BAD6E14F5403D52987F76E4` |
| `quest/scenario/man/man0g1.lua` | 41724 | `8B0988C285974162A150638156826605B75E093C9F6EB8F33B99B6D139A195B8` |
| `quest/scenario/man/man0l1.lua` | 56179 | `FEA9C9359AC610737BE1B5910D473D98F5174512DDF01F0B730F9E0F608F8C67` |
| `quest/scenario/man/man0u1.lua` | 53155 | `31FC9EBF234B4945F3CBBE6B7C5F1493C659A2A584D508C778F9351089FEB10A` |

The contract does not establish which actor the world master returns, the
native effect or balance of the lock calls, when the three widget callbacks
are delivered, or the order in which a session reaches them.
