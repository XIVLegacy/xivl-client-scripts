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

## Destination-slot restoration

`TeleportCommand.eventRegion` and `TeleportCommand.eventAetheryte` are separate
event methods. The former opens the ask widget and calls
`DesktopWidget.selectAetheryteRegion`, which selects mode zero and returns the
region row result. The latter accepts a region selector and builds the
destination inputs. The script does not directly call the destination method
from the region method.

`DesktopWidget.selectAetheryteList` selects mode one, forwards the supplied
ID/cost operands and returns the ask result unchanged. Both wrappers request
two results from `selectEventModeWidgetYield` and return its second result.
On success, that helper returns `true` followed by the widget's `getAskResult`.

The destination method restores original slot identity. For region selectors
1-5, it reads six supplied costs. Their fixed-ID domains contain 6, 5, 6, 6
and 2 slots respectively. The mapping examples keep unused tail costs zero;
they do not establish arbitrary nonzero costs with absent fixed IDs as valid
server input. For selector 6, it reads three costs followed by three
destination IDs. Each branch omits a slot whose supplied cost equals
numeric zero. For every retained slot, it appends the destination ID and cost
to compacted arrays and records the original one-based slot at the compacted
one-based ordinal. It passes six ID/cost pairs to the widget, receives the
visible ordinal, closes the widget, and returns the recorded original slot.
The widget's seven-pair capacity is larger than this caller's argument list.

For example, the following synthetic costs illustrate leading and interior
omissions. `C` means a nonzero supplied cost; all retained IDs are nonnil.

| Supplied costs | Original slot | Visible row | Widget/wrapper result | Command return |
| --- | --- | --- | --- | --- |
| `[C,C,C,C,C,C]` | 1 | 0 | 1 | 1 |
| `[0,C,C,C,C,C]` | 2 | 0 | 1 | 2 |
| `[C,0,C,C,C,C]` | 3 | 1 | 2 | 3 |
| `[0,C,0,C,0,C]` | 2 | 0 | 1 | 2 |
| Same | 4 | 1 | 2 | 4 |
| Same | 6 | 2 | 3 | 6 |

The result at the widget and wrapper is a one-based visible ordinal. The
destination method's result is the original cost-slot number, not an
`AetheryteID`, a region ID, or an established wire selection field.

The two filters have different conditions. The command omits numeric-zero
supplied costs; the widget omits nil IDs. The original-slot map remains aligned
when each cost-retained entry has a nonnil ID. A nonzero-cost entry with nil ID
can enter the command's map and then disappear in the widget, and neither
wrapper repairs that additional compaction. The selected script does not
establish that such a tuple is a valid server input. A nil cost is not numeric
zero, so nil must not be substituted for the command's exclusion value by
analogy. Later code can also set a retained display cost to zero after the
compaction, so a displayed zero does not imply omission.

If all IDs are omitted, the widget supplies its zero-ID fallback row, which
does not set a destination result. Closing produces nil, and the destination
method's map lookup also returns nil. This establishes client result handling;
it does not identify how attunement determines supplied arguments or how the
server interprets the returned slot.

### Original-bytecode evidence

The wrapper source is pinned at `manifests/scripts.json:15399` for
`lua/scripts/widget/desktopwidget_connector.lua`. Its LPB and decoded payload
are pinned at `manifests/retail_lua_coverage.json:25444`, with payload SHA-256
`685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`.
The original `selectAetheryteRegion` prototype `root/proto452`, PCs 4-5
(decoded offsets 168439 and 168443), selects mode zero and returns the second
helper result. `selectAetheryteList`, `root/proto453`, PCs 4-5 (168577 and
168581), selects mode one and returns the second helper result.

In the previously pinned teleport payload, `eventAetheryte` is `root/proto3`.
Its zero-cost tests are PCs 76, 126, 171, 221, 271 and 301. The corresponding
original-slot map writes are PCs 114, 159, 209, 259, 289 and 327. PC 388
(decoded offset 3017) calls the destination wrapper with six pairs. PC 393
(3037) indexes the map with the returned ordinal, and PC 394 (3041) returns
that original slot. Canonical source locators are
`lua/scripts/command/system/teleportcommand.lua:558` and `:577`.

These observations use authenticated original LPBs and separately
manifest-matched canonical source. Synthetic execution of the selected
instructions checks leading/interior omissions, all supported zero-cost masks,
nil-ID compaction, zero-ID suppression and cancel handling. It does not claim
retail-runtime or server validation.

The producing readers were `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`, using Python 3.12.0.
Prototype indices and PCs are zero-based. Decoded offsets above are decimal
byte offsets in the authenticated Lua 5.1 payload.

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
