# MyPlayer timer consumers

The retail Lua corpus has 22 direct calls to the five MyPlayer timer callbacks
mapped to s2c `0x0193`: 17 occupancy calls, one normal-behest call, one
company-behest call, one warp-recast call, and two NM-rush calls. Five
`PlayerBaseClass` receiver declarations, five registry `_inl` method records,
the call sidecars, and `lua/napi_index.json` agree with that count. No other
exact callback string or resource reference occurs in the 2,671 scripts.

The generated [`myplayer_timer_consumers.json`](../manifests/myplayer_timer_consumers.json)
is the complete callsite ledger. `python tools/myplayer_timer_consumers.py
--check` re-enumerates the corpus, sidecars, declarations, registry metadata,
and N-API index and rejects semantic-pattern drift.

## Occupancy argument and index map

The native wrapper subtracts one from its Lua argument before indexing the
16-entry vector. The corpus passes every integer from 1 through 16 and no
other value to the occupancy callback. `StatusWidget.updateContents` calls
`setContentsListItem` with four negative scalar selectors and all 16 positive
occupancy selectors. Therefore the dynamic-looking direct call inside
`setContentsListItem` has a complete deterministic corpus domain.

The title column is the exact English client vocabulary reached by the status
widget's `_text_ui` row 10051 lookup into `raidDungeon`; it is presentation
vocabulary, not a packet-field or server-state name.

| Lua argument | Native index | Other caller context | Status title |
|---:|---:|---|---|
| 1 | 0 | `PcMatchingEditWidget.makeGuildleveList` | the Thousand Maws of Toto-Rak |
| 2 | 1 | `PcMatchingEditWidget.makeGuildleveList` | Dzemael Darkhold |
| 3 | 2 | `PcMatchingEditWidget.makeRaidList` | the Bowl of Embers (Hard) |
| 4 | 3 | `PcMatchingEditWidget.makeRaidList` | the Bowl of Embers |
| 5 | 4 | `PcMatchingEditWidget.makeRaidList` | Thornmarch |
| 6 | 5 | `PcMatchingEditWidget.makeGuildleveList` | Aurum Vale |
| 7 | 6 | `PcMatchingEditWidget.makeGuildleveList` | Cutter's Cry |
| 8 | 7 | `PcMatchingEditWidget.makeBanzokuList` | the Battle for Aleport |
| 9 | 8 | `PcMatchingEditWidget.makeBanzokuList` | the Battle for Hyrstmill |
| 10 | 9 | `PcMatchingEditWidget.makeBanzokuList` | the Battle for the Golden Bazaar |
| 11 | 10 | `PcMatchingEditWidget.makeRaidList` | the Howling Eye (Hard) |
| 12 | 11 | `PcMatchingEditWidget.makeRaidList` | the Howling Eye |
| 13 | 12 | `PcMatchingEditWidget.makeGuildleveList` | Castrum Novum Transmission Tower |
| 14 | 13 | `PcMatchingEditWidget.makeRaidList` | the Bowl of Embers (Extreme) |
| 15 | 14 | `PcMatchingEditWidget.makeRaidList` | Rivenroad |
| 16 | 15 | `PcMatchingEditWidget.makeRaidList` | Rivenroad (Hard) |

Every `PcMatchingEditWidget` call compares the returned value with zero. A
positive result adds or retains the corresponding selection row; the value is
not formatted or subtracted there. The status path instead treats the value as
an endpoint: it hides a non-positive row, compares a positive value with
`WorldMaster._getServerTime`, subtracts that server time while the endpoint is
still ahead, divides the difference by 86400, 3600, and 60 for presentation,
and writes the title and status text into `ListBox_Contents`.

Arguments 8, 9, and 10 have one additional status-only transformation. The
widget maps them to Hamlet slots 2, 1, and 3. If the corresponding defense
window has not begun and the callback endpoint is positive, it replaces that
endpoint with `getHamletDefenceBeginTime` and changes the status format to the
exact English text `Hamlet defense available in` (text ID 10058). This is a
local presentation substitution; it does not change the native vector map.
`setGLComboBoxData` independently adds one to its selection-slot argument when
choosing the concrete combo-box row.

Evidence: `lua/scripts/widget/pcmatchingeditwidget.lua`,
`lua/scripts/widget/statuswidget.lua`,
`xivl-client-data:csv/xtx_raidDungeon.csv`, and
`xivl-client-data:csv/xtx__text_ui.csv`.

## Scalar consumer map

| Callback | Direct consumer | Deterministic downstream use | Exact presentation vocabulary |
|---|---|---|---|
| `_getNormalBehestTime` | `StatusWidget.setContentsListItem` | Selector -2 chooses the callback, then uses the shared endpoint comparison, subtraction, formatting, and row-visibility path. | Behests; Available in; Available |
| `_getCompanyBehestTime` | `StatusWidget.setContentsListItem` | Selector -3 chooses the callback, then uses the shared endpoint comparison, subtraction, formatting, and row-visibility path. | Company Behests; Available in; Available |
| `_getWarpRecastTime` | `PlayerBaseClass.getWarpRecastTime` | Subtracts `WorldMaster._getServerTime` and clamps at zero. `TeleportCommand.canFire` rejects a living-player command attempt while the result is positive. `MainMenuWidget.getButtonMask` disables its sixth returned mask under the recovered conditions, and `setDezionTimer` writes the positive result to `MainMenu` item 15 timer properties or collapses that timer. | Return. The recovered method name is `setDezionTimer`. |
| `_getNMRushUpdateTime` | `StatusWidget.setContentsListItem`; `DesktopWidget.isNMRushEnable` | Selector -4 uses the shared status endpoint path. The desktop connector independently returns only whether the raw value is positive; no exact Lua caller of `isNMRushEnable` was recovered. | Skirmish; Available in; Available |

`PlayerBaseClass.getWarpRecastTime` has exactly three recovered callers: the
teleport command check and the two main-menu methods above.
Main-menu item 15 uses `DataTemplate_ListBoxItem_Return` and `_text_ui` row
2112, whose exact English title is `Return`.
`StatusWidget.setContentsListItem` has exactly 20 recovered callers, all in
`StatusWidget.updateContents`: -1 through -4 and 1 through 16.
`PcMatchingEditWidget` reaches its fixed occupancy calls through its named list
builders when the matching view branches are selected.

Evidence: `lua/scripts/chara/player/playerbaseclass.lua`,
`lua/scripts/command/system/teleportcommand.lua`,
`lua/scripts/widget/mainmenuwidget.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`, and
`lua/scripts/widget/statuswidget.lua`.

## Evidence boundary

The callback-to-subopcode mapping and native one-before-index transform come
from `xivl-decomp:config/s2c_0193_native_state.json`. The Lua corpus proves how
the recovered scripts consume the values; the English strings come from the
public client-data sheets named above.

No occupancy call with zero, a negative argument, or an argument above 16 was
recovered. The four negative `StatusWidget` selectors do not reach occupancy.
An invocation from outside the recovered corpus remains outside this bounded
negative result.

This finding does not infer a native timer unit, rename widget titles as server
packet nouns, establish authoritative eligibility, describe setup or teardown,
or assign server policy. The divisions used by the UI are presentation facts;
they do not independently type the native fields.
