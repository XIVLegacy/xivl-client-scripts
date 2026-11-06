# Hamlet supply and score UI contract

The recovered client has separate Hamlet supply dialogue, supply ranking,
and defense score routes. Their LPBs matched the recovered LUACs
byte-for-byte; these calls describe client presentation, not a server-side
supply, ranking, or reward policy.

The [delivery-selection flow](hamlet-delivery-selection-flow.md) qualifies
the item/materia menu results, selected price updates and separate close.

`Noc002` defines captain and supply menu methods, including supply errors
and item-selection dialogue (`noc002.lua:189-849`). Its
`processSupplyAskWhatA04` runs a character scheduler, says text row 62,
then calls `desktopWidget:askHamletDefenseRankingWidget` with five supplied
arguments (`noc002.lua:781-785`). This is a direct ranking-widget opener;
the script does not identify the historical NPC actor or prove the values
of the arguments that a server supplied.

`HamletDefenseRankingWidget.setRankingList` obtains the current area master,
calls `_countHamletSupplyRanking`, and iterates that many
`_getHamletSupplyRanking` rows. It derives a linkshell icon when the row's
linkshell field is nonnull and passes the row to `setRankingListItem`
(`widget/ask/hamletdefenserankingwidget.lua:setRankingList`; bytecode
`0x0009D0-0x000A40`). `HamletDefenseScoreWidget.initAsk` instead gets the
local player, iterates `_countHamletDefenseScore` and
`_getHamletDefenseScore`, and reads `_getHamletDefenseScoreAll` for totals
(`widget/ask/hamletdefensescorewidget.lua:initAsk`; bytecode
`0x00011F-0x00013B` and following). The native receiver copies, cache writes,
getter order and wire-field joins are recorded in
`xivl-client-structs:manifests/hamlet_wire_contract.json`.
The score totals getter consumes and clears its cache; neither receiver
directly opens a widget. Client display arithmetic does not validate server
ranking, bonus or reward policy.

## Score widget requests and total-read order

`HamletDefenseScoreWidget.initAsk` has two fixed parameters: the widget
receiver and a supplied value used in the title request. The original
`root/proto0` contains 83 instructions starting at decoded offset `0x00010B`.
The matching canonical span is
`widget/ask/hamletdefensescorewidget.lua:11-117`, SHA-256
`7C6ECF986F0DAA8CB9555B7FBE19F1C63C9EE86620443F1BDE29A27362282B78`.
Its original instructions and canonical source agree on the requests below.
The [script sidecar](../lua/scripts/widget/ask/hamletdefensescorewidget.calls.json)
records the named getter references.

All calls use the indicated object as their receiver. First the widget calls
`setCancelCondition()` and `setConfirmCondition("Button_Confirm")`. It then
reads global `worldMaster`, calls its `_getMyPlayer()` once, retains the first
result as `player`, and calls `player:_countHamletDefenseScore()` once,
retaining the first result as the loop limit. Neither the player nor the
count has an explicit validity guard.

For each numeric-loop index `i`, starting at 1 with step 1 through the captured
limit, the method makes these calls in order:

| Receiver | Method | Ordered explicit arguments | Results retained |
|---|---|---|---|
| `player` | `_getHamletDefenseScore` | `i` | First three: `points`, `category`, `factor` |
| widget | `setListText` | `"DataMaker_ListBox", i - 1, "bonus", 13019, category, factor` | None |
| widget | `setListProperty` | `"DataMaker_ListBox", i - 1, "point", points` | None |

After the loop, including when it ran no iterations, the widget calls
`updateListProperty("DataMaker_ListBox")`. Only after that call returns does
the method replace a nil second parameter with the literal `9` and call
`player:_getHamletDefenseScoreAll()`, retaining its first five results as
`t1` through `t5`. The title fallback tests nil specifically: supplied
`false` and `0` remain unchanged. The meaning of `9` is not established here.
The totals call is at decoded offset `0x0001AB`, after the list update call
at `0x000193` and before the first total text call at `0x0001D7`.

The remaining calls occur in this order. Here `titleValue` is the supplied
second parameter after the nil-only fallback.

| Receiver | Method | Ordered explicit arguments |
|---|---|---|
| widget | `setText` | `"TextBlock_ContentsTitle", 13012, titleValue, t2` |
| widget | `setText` | `"TextBlock_PointTotalValue", 225, t1` |
| widget | `setText` | `"TextBlock_CorrectionLevelValue", 3189, t2` |
| widget | `setText` | `"TextBlock_PointAfterCorrectionValue", 225, t3` |
| widget | `setText` | `"TextBlock_ClearTimeValue", 225, t4` |
| widget | `setText` | `"TextBlock_TotalPointsValue", 225, t5` |
| widget | `setContent` | `"Label_TotalPointsValue", 225, t5` |

Extra getter results are discarded and missing results are padded with nil
to the stated widths. Row and total values, including nil, false and zero,
are forwarded without a value guard. All presentation-call results are
discarded, and `initAsk` returns no values on completion. Each method is
looked up again on its retained receiver at its call site, including row
getters on later iterations, the totals getter after the list update, and
each `setText`. The global and player lookup are not repeated.

The only explicit arithmetic in this method is the list index `i - 1` and
numeric-loop progression. It neither multiplies row points by `factor` nor
recomputes or checks the five totals. For example, authored getter results
`(points, category, factor) = (17, 23, 4)` request point value `17`, not `68`.
Totals `(19, 3, 7, 11, -5)` are forwarded unchanged even though they do not
satisfy a correction formula. A nil title parameter with fourth total `27`
still requests title arguments `(13012, 9, t2)`.

The published getter contract in
`xivl-client-structs:manifests/hamlet_wire_contract.json`, opcode `0x01a8`,
at revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`, identifies the native
totals tuple as `(sum, signed correction, sum * correction, additive,
sum * correction + additive)`. Conditional on the retained player using
that binding and cache, the totals read consumes its score state before
any of the seven total/title presentation requests. An earlier row or list
update error prevents this method from reaching that read. A later control
error has no local recovery or rollback of a completed read.

These are requests to uninspected presentation helpers, not proof of rendered
text or control behavior. Text rows `13019`, `13012`, `225` and `3189` are
literal operands; this method establishes no text bank or provider binding.
The source fixtures do not execute the retail client or establish actual
scores, cache lifetime across other callers, a Hamlet variant, server score
production, a historical clear, or reward delivery.

`PopulaceHamletSupply` provides separate item and materia delivery-menu
methods (`populacehamletsupply.lua:7-78`). Its item getters return a
craft-list count of 8 and gather-list count of 3. For actor class IDs
1500433, 1500320, and 1500434 respectively, the craft sheet base keys are
12001, 11001, and 13001; the gather bases are 12009, 11009, and 13009.
Each getter reads `itemHamletSupplySheet` at `base + requestedIndex - 1`
and returns columns 0 and 2 (`populacehamletsupply.lua:79-173`; craft
bytecode `0x0009A2-0x000A3A`). The selected item IDs and quantities in the
pinned table are cataloged in
`xivl-client-data:docs/hamlet-supply-rows.md`. These are conditional
client-sheet lookups, not proof that those actor IDs spawned with this class
or accepted the listed items historically. The zero-base fallback for other
actor IDs is not a verified supply association.

Decoded LUAC SHA256 values: `Noc002`
`1DA67252A10403AFF3C6391B2B6BFB1AF5B30EC9B29942690676B28F7B58C988`;
ranking widget
`E1293DA98F699955D5C5935EFDF7E1A52D25B6A88717A7DAEFF78C53B3413054`;
score widget
`54779D0E785A52CFF64B7136A34C168C3B10A1A99089B7789EB9A199AE98AD7E`;
`PopulaceHamletSupply`
`E9CC7C69A6B0409BD6FD5D63AC42B243CC2BC526F72E243B54E02C83AECF8FD1`.
Recovered-source identities are in
`manifests/scripts.json:6434-6439,12716-12721,14960-14971`.
