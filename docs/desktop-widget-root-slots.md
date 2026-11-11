# Desktop root widget slots

`DesktopWidget.work.rootWidget` holds one widget per opener kind. The
connector tests a slot for occupancy, the WidgetBase creation callback fills
an empty slot, and the finalization callback or an abort sweep clears it.
These are recovered Lua contracts. The native widget-command entry, the
deletion trigger and object liveness are not established here.

The [desktop widget admission and close contracts](content-director-ui-contracts.md#desktop-widget-admission-and-close)
own `openWidgetYield`, `openWidget`, `openWidgetLocal`,
`commandCreateWidget`, `getWidget`, `closeWidgetDirect` and
`WidgetBaseClass.close`. The
[shared initialization frame](tutorial-form-name-selection.md#incoming-initialization-frame)
owns `_onInit` up to the `initialized` write. This page covers the slot
reads and writes around them.

## Occupancy test and root opener

`isWidgetExec(D,k)` (`root/proto531`) reads `D.work.rootWidget[k]` and
returns one `true` when it is nonnil and one `false` when it is nil (PCs
0-8). It makes no `_isAlive` call, so a slot that still holds a dead widget
reads as occupied.

`openRootWidget(D,k,name,parent,p4,...)` (`root/proto535`) begins with a
literal nil-versus-true test whose false return at PCs 2-3 is unreachable.
It then requests `isWidgetExec(D,k)` and keeps one result (PCs 4-6). An exact
`true` returns one `false` (PCs 7-10). Every other result reaches the
tailcall

```text
openWidget(D,k,name,nil,parent,p4,...)
```

at PCs 11-18. The VARARG at PC17 has B=0 and the TAILCALL has B=0, C=0, so
the complete extra-argument tail and every `openWidget` result are
forwarded. The window-name slot is always nil on this route.

## Creation callback

`WidgetBaseClass._onInit` (`widget/widgetbaseclass.lua`, `root/proto0`)
receives `(W,P,Q,V1,...,Vn)` as on the shared initialization page. After
`initialized` is set true (PC110), the rest of the body runs as follows:

1. A truthy `_isInstanceOf(W,"DesktopWidget")` result, saved at PCs 67-74,
   returns at PC133 with no callback (PCs 111-112).
2. A truthy `desktopWidget:isInitializing()` result also returns without a
   callback (PCs 113-117).
3. Otherwise F is `true` for a nil P, else `not P:isInitializing()`
   (PCs 118-125).
4. The body requests `desktopWidget:processWidgetCreated(W,F,Q,V1,...,Vn)`
   with the complete variadic tail and discards its results (PCs 126-132).

`isInitializing` (`root/proto2`) returns `not widgetWork.initialized`.

`processWidgetCreated` (`desktopwidget_connector.lua`, `root/proto532`) has
seven fixed slots `(D,W,F,Q,V1,V2,V3)` and makes these requests in order:

| PCs | Condition | Request or result |
| --- | --- | --- |
| 0-8 | F equals true and `W:_getParentWidget()` differs from D | `parent:setInputEnable(Q)` |
| 9-16 | `W:isCreateCancel()` equals true | `D:closeWidgetDirect(W)`, then return |
| 17-19 | F is false or nil | Return |
| 20-27 | `D.work.rootWidget[V2]` is nil | Store W in `D.work.rootWidget[V2]` |
| 28-35 | `D.work.widgetEnableFlag[W:getWidgetType()]` equals false | Return |
| 36-40 | `W:getVisibleFlag()` equals false | Return |
| 41-58 | Each child i from 1 to `W:_countChildWidgets()` | `child:show()` when `child:getVisibleFlag()` equals true |
| 59-60 | Reached end | `W:show()` |

The slot store does not replace an occupied slot, and it precedes the enable
and visibility returns. A widget can therefore occupy its slot without a
show request. The shared `initCommon` (`widget/widgetbaseclass_common.lua`,
`root/proto0`) stores its fourth fixed argument in
`widgetWork.common.widgetIndex` at PC61. With the shared frame's call
`initCommon(W,P,V1,...)`, that argument is the same V2 that keys the slot
store, conditional on applied work storage and no later write.

Under the positional reading of the
[conditional creation frame](tutorial-widget-creation-frame.md#creation-payload-and-initializer-positions),
V1 is the window name, V2 is the opener kind and V3 is the shown flag. The
selected Gridania tutorial tuple would then store the widget under kind 12.
That reading carries the native frame premises of the linked page.

## Selection show pass

`selectWidgetYield(D,W,flag)` (`root/proto539`) also begins with an
unreachable literal test (PCs 0-3). When flag equals true exactly, it repeats
the child show pass of `processWidgetCreated` and then requests `W:show()`
(PCs 4-23). It then requests `selectWidgetTimerYield(D,W,nil)` with `C=3`
and returns only the first result (PCs 24-28). The
[selection wait](gridania-opening-tutorial-contract.md#selected-widget-calls)
owns the timer helper.

## Abort sweep and deletion

`processWidgetCreateAborted(D)` (`root/proto533`) visits slots 1 to 17. A
nonnil slot whose `_isAlive()` result equals false is set to nil (PCs 0-19).
Live slots, and slots above 17, are left unchanged.

`processWidgetDeleted(D,W)` (`root/proto534`) reads the slot key from
`W:getWidgetIndex()`, which returns `widgetWork.common.widgetIndex`
(`widgetbaseclass_common.lua`, `root/proto5`). A nil slot returns. When the
slot's `_isAlive()` result equals true, the slot is cleared only if it holds
W. Any other liveness result clears the slot regardless of its occupant
(PCs 0-26).

`WidgetBaseClass._onFinalize` (`widgetbaseclass.lua`, `root/proto4`) first
requests the superclass `_onFinalize`. When `_isInstanceOf(W,"DesktopWidget")`
and `W:isInitializing()` are both falsy, it requests
`desktopWidget:processWidgetDeleted(W)` (PCs 9-16). It always ends with
`processFinalize()` (PCs 17-18).

The shared `WidgetBaseClass.close` requests `setInputEnable(false)`,
`processClosing()` and `_delete()` in that order (`root/proto38`, PCs 0-6).
It does not touch the slot. The base `processUICommandClose`
(`root/proto17`) requests `desktopWidget:closeWidgetDirect(W)` and discards
its results, and the base `processUICommandCancel` (`root/proto16`)
forwards its four arguments to the dynamically resolved
`processUICommandClose` (PCs 0-5).

Consequences under these bodies:

- `openRootWidget` refuses a kind while its slot is nonnil, including a slot
  that holds a closed widget whose `_onFinalize` has not run.
- `openWidget` and the `openWidgetYield` precheck test the slot only when
  their parent argument is nil, as their published contracts state.
- A slot is emptied by `processWidgetDeleted`, by the abort sweep for a dead
  occupant, or by the published `getWidget` branch for an exact-false
  `_isAlive` result.

The following remain NOT TRACED: when the native side raises `_onFinalize`
relative to the `_delete` request, when `_isAlive` starts to return false
for a deleted widget, the caller of `processWidgetCreateAborted`, and the
lifetime of the native widget-command entry that `isCreateWidgetCommandPlaying`
observes. `xivl-client-structs:docs/fade-actor-group-native-contract.md`,
"Widget delete override", owns the `+0x70` delete entry.

## Source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
Original resources and decoded payloads matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `widget/desktopwidget_connector.lua` | 660617 / 26564 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/widgetbaseclass.lua` | 8518 / 421 | `737a53b0472b510440735cf19a1d0a11fd100e69df7f3eab1178969a3d57b95c` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `n1635q/n1635q89r57y9rr.le.lpb` | 4080 / `aad807a42296e93301582defc8f15e4003b8093af672794282cd54950cc556ad` | 4067 / `11e5bab509c4dbbd7e2767d35cdf132a59b5c510c32c2e215f83cac713115140` |
| `n1635q/n1635q89r57y9rr_7vxxvw.le.lpb` | 32996 / `c549f746370366f9827570ee22201516e07a05d91829ca643a2e2ec0c73bcf3c` | 32983 / `7c45426b1a9f168557d84e420c5767c6fdea4abf90b976b276546af4e6a5de5f` |

Prototype indices and PCs are zero-based, and code starts are decoded-payload
offsets with PC n at start plus 4n.

| Method | Canonical lines | Root binding PC | Prototype / code start |
| --- | --- | ---: | --- |
| Connector `isWidgetExec` | `desktopwidget_connector.lua:25438-25453` | 1872 | `root/proto531` / `0x3259C` |
| Connector `processWidgetCreated` | `desktopwidget_connector.lua:25455-25533` | 1876 | `root/proto532` / `0x32607` |
| Connector `processWidgetCreateAborted` | `desktopwidget_connector.lua:25535-25562` | 1880 | `root/proto533` / `0x32818` |
| Connector `processWidgetDeleted` | `desktopwidget_connector.lua:25564-25598` | 1884 | `root/proto534` / `0x328D1` |
| Connector `openRootWidget` | `desktopwidget_connector.lua:25600-25627` | 1888 | `root/proto535` / `0x329A4` |
| Connector `selectWidgetYield` | `desktopwidget_connector.lua:25692-25733` | 1904 | `root/proto539` / `0x32BE7` |
| WidgetBase `_onInit` | `widgetbaseclass.lua:7-170` | 5 | `root/proto0` / `0x33C` |
| WidgetBase `isInitializing` | `widgetbaseclass.lua:179-187` | 11 | `root/proto2` / `0x822` |
| WidgetBase `_onFinalize` | `widgetbaseclass.lua:204-231` | 17 | `root/proto4` / `0x8E0` |
| Common `initCommon` | `widgetbaseclass_common.lua:4-111` | 2 | `root/proto0` / `0x19FA` |
| Common `getWidgetIndex` | `widgetbaseclass_common.lua:238-246` | 17 | `root/proto5` / `0x21D0` |
| Common `processUICommandCancel` | `widgetbaseclass_common.lua:642-653` | 50 | `root/proto16` / `0x2FF3` |
| Common `processUICommandClose` | `widgetbaseclass_common.lua:656-665` | 53 | `root/proto17` / `0x3052` |
| Common `close` | `widgetbaseclass_common.lua:844-858` | 116 | `root/proto38` / `0x35ED` |

Reproduction uses `tools/retail_script.py:decode_lpb` and the
`ChunkReader` and `instruction` definitions in
`tools/build_quest_contracts.py`. Check the root closure assignments, the EQ
and TEST operands and jump targets named above, the open VARARG and CALL
widths, and the slot SETTABLE operands. The connector root binds each method
through `GETGLOBAL DesktopWidget`, `LOADK` of the name, `CLOSURE` and
`SETTABLE`.
