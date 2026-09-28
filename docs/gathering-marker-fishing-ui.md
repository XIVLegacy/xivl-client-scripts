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
