# Aetheryte list widget contract

`AetheryteListWidget` is the ask-widget implementation opened by
`TeleportCommand.eventRegion`. That command calls
`DesktopWidget.selectAetheryteRegion` only after the widget opens successfully.
This connects the widget to the retail teleport-command path; it does not
establish teleport acceptance or server destination policy.

## Widget state and rows

`initAsk` declares temporary `mode` and `regionIndex` fields as `integer8`,
initializes both to zero, and registers selection-change handling for the
region and destination list controls. It also enables cancel and close
conditions and creates the region list.

`setAskParameter` uses mode zero to display the supplied anima value, show the
region list, hide the destination list, and restore the saved region-list focus.
Other mode values build and show the destination list. The widget stores the
mode, but this code does not identify meanings for nonzero values.

The region list has five entries with row indexes 0 through 4 and stored region
IDs 101 through 105. Each `RegionName` uses text ID 5201 with the region ID as
an argument. A sixth row uses text ID 10307 and stores region ID -1. These are
the widget's numeric inputs; this contract does not assign names or world
meanings to them.

The destination builder accepts up to seven `(AetheryteID, Cost)` pairs. A nil
ID skips its row. Each populated row writes the ID and cost properties and
formats `AetheryteName` with text ID 211 and the ID as its argument. ID zero
hides the cost property. If no rows are populated, the widget adds a row with
ID zero, cost zero, and text ID 10304.

## Selection results

Selecting a region stores its zero-based row index in `regionIndex` and sets
the ask result to that index plus one. Selecting a destination resolves the
selected row's property index, reads `AetheryteID`, and sets the result to the
selected row index plus one only when that ID is nonzero. The result is an
index, not the stored region or destination ID. The zero-ID fallback row does
not set a destination result.

Closing the widget sets the base ask result to -1. `getAskResult` converts
that value to nil and otherwise returns the base result unchanged. No client
state mutation, destination eligibility, anima calculation, or server
teleport outcome follows from this widget contract.

## Teleport confirmation result

`TeleportCommand.eventConfirm` waits one second, then obtains a confirmation
result through `worldMaster.ask` or `worldMaster.askMultipleTextMacro`, using
message IDs 34117, 34138, or 34120 according to its inputs. For an accepted
result, it calls `isRiding` on StaticActor 320013 with the supplied actor. If
true, it prompts through `worldMaster.ask` with the ID returned by that static
actor's `getRidingErrorTextId`, passing 26010 as fallback, then replaces the
local result with that answer. If the countdown input is true and the result
remains accepted, it opens `Ask/WaitingCountdownWidget` with
`(1, 15, worldMaster, 34137)` when `A2_2` is true, or
`(1, 15, worldMaster, 34136)` otherwise. A false widget-open result or widget
result 2 changes the local result to 2. The method returns that result and an
optional boolean. It contains no zone-transition call; this method alone does
not establish how a caller uses the return values or what the server does.

## Evidence

The widget's decoded payload is SHA-256
`C43A98FE57C2C23D67D5947F6FAB7F437D5105B67513D7EA83DFD4C4A869547B`, pinned
at `manifests/retail_lua_coverage.json:26494-26505` for
`lua/scripts/widget/ask/aetherytelistwidget.lua`. Its source entry is pinned
at `manifests/scripts.json:14871-14874`.

The caller payload is SHA-256
`9023D10F0B1D0CC8BA7ED9C5DF2BF1099F06852E5EE7B631B6DBCE1A4456DB36`, pinned
at `manifests/retail_lua_coverage.json:23555-23566` for
`lua/scripts/command/system/teleportcommand.lua`. Its source entry is pinned
at `manifests/scripts.json:7629-7632`.

The `eventConfirm` method was decompiled from that caller payload with the
repository-pinned unluac JAR at `tools/vendor/unluac/PROVENANCE.json`, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`. The
source-form entry in `manifests/scripts.json` is a separate representation,
not the byte input used for this decompilation.
