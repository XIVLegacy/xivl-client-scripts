# Gathering marker and fishing UI

Decoded bytecode for `MiningPoint` and `FishingInputWidget` reproduces the
canonical 1.23b corpus exactly. The retained
[`gathering_marker_fishing_ui.json`](../manifests/gathering_marker_fishing_ui.json)
pins both inputs and their canonical outputs.

## Mining-point markers

`MiningPoint.getMapMarkerTypeForTalkable` maps actor class IDs directly:

| Actor class ID | Marker type |
|---:|---:|
| 1200053 | 10 |
| 1200055 | 11 |
| 1200057 | 12 |
| other | 6 |

`isMapMarkerVisibleForTalkable` returns true only for actor class 1200057 in
the recovered body; 1200053, 1200055, and other classes reach false.
`initForEvent` disables ground placement with `_setGroundOn(false)`.

This is a direct actor-class mapping, but it covers only the generic mining
point script. It does not assign names, coordinates, gathering tables, yields,
or probabilities to those class IDs.

## Fishing input presentation

`FishingInputWidget` initializes its HP progress bar to the range 0 through
100 and its phase-A slider to 50. The angle-gauge route issues
`Start_PowerGauge`, then `Stop_PowerGauge` and reads the resulting
`RenderTransform.AngleZ` value. In phase 1, `getAskResult` returns the chosen
command followed by the phase-A slider value. Other phases return the chosen
command and the stored current angle.

`updateHP` accepts only values from 0 through 100 and writes the accepted value
to the HP progress bar. `setAskParameter` selects and enables the applicable
slider or angle controls, updates display effects, retains a supplied HP value,
and refreshes bait presentation.

These are input and display contracts. They do not establish bite selection,
fish identity, yield, fatigue, sweet-spot probability, success chance, or
server validation.

## HarvestJudge widget calls

The recovered HarvestJudge uses these fixed formal argument lists. A1 is the
actor tested with `isPlayer`; A2 is unused in all four bodies below.

| Method | Recovered client call and return |
| --- | --- |
| `loadTextData(self,A1,A2)` | Empty body, returning no values. Its separate `initText(self)` loads `(1308,"harvestJudge")`. |
| `openInputWidget(self,A1,A2,A3,A4)` | For `A1:isPlayer()==true`, command A3 selects MiningInputWidget 22002, FellingInputWidget 22003 or FishingInputWidget 22004. It forwards A4 to `openEventModeWidgetYield` and returns the first result, with false as its local default. |
| `orderInputWidget(self,A1,A2,A3,A4,A5)` | Under the same actor predicate, A5 selects the same widget and the method forwards A3/A4 to `updateEventModeWidget`. It returns the first result, with false as its local default. |
| `askInputWidget(self,A1,A2,A3,A4,A5,A6,A7,A8,A9)` | A3 selects the widget. It receives three results from `selectEventModeWidgetYield`, retains the first as the selection flag, and returns the second, third and first in that order. An exactly-false flag zeroes the first two returned values. |

The Mining/Felling ask argument tails are
`(primary,secondary,extra,quit,nil,A4,nil,A9)`. Phase A4 equal to 1 selects
primary commands 22701/22704; the other branch selects 22703/22705.
The quit commands are 22702/22706, and extra is 22710 when A5 differs from
zero, otherwise nil. These are extracted input and result routes, without
an established server success calculation or a complete wire sequence.

Source: `lua/scripts/judge/harvest/harvestjudge.lua:11-26,69-265`,
9,902 bytes, SHA-256
`E097DE09274574430D14FCAFE02CE520CCA1BA14CCF8CC42C57413D5CD9CA814`,
pinned by `manifests/scripts.json`. Branch descriptions here follow the
recovered decompile; original instruction operands were not independently
replayed for this finding. Retained wire observations remain a separate
evidence class.

## Selected HarvestJudge text

The loaded bank is `harvestJudge`, extrasheet resource `0x03A2051C`.
`xivl-client-data:csv/harvestJudge.csv`, English column 1, row 20
(physical line 22) is "You failed to obtain anything." The following
rows provide related guidance or failure/end messages. Their content does
not identify which server condition selected a row.

| Row | English meaning |
| ---: | --- |
| 10-11 | Unsuitable force or angle yields no item from the deposit or tree. |
| 16 | Each action reduces Remainder; reaching zero fails the attempt. |
| 21-23 | The mining, logging or fishing attempt has ended, respectively. |
| 28 | No bait or lure is equipped. |
| 29, 31 | Gathering ceased or finished. |
| 30 | Agitated fish cause the player to put away the rod and observe. |
| 32 | Nothing was found. |
| 33-35 | Unable to hook a fish, nothing bites, or the fish escaped. |
| 39, 42 | No bites or nothing promising was felt. |
| 43 | The action moved farther from the mark. |
| 46-48 | Close to an item, but unable to extract, cut or reel it in. |
| 52 | The tired fish still cannot be reeled in. |
| 54 | Unable to obtain anything. |
| 55-57 | A strike or chop damaged the formatted item, or it was lost while fishing. |
| 58-59 | Bait ran out or the lure was lost. |

Physical source lines are row ID plus two for these selected rows.
The complete member identity is pinned by
`xivl-client-data:manifests/tables.json`; the resource ID is in
`xivl-client-data:manifests/sheet_inventory.csv`.
