# Search and recruitment native boundaries

Player-search rows and comments reach a native widget consumer. Recruitment
results reach `PcMatchingFindWidget` through native property updates. The
[wire contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md)
and its
[evidence manifest](https://github.com/XIVLegacy/xivl-client-structs/blob/main/manifests/search_recruitment_wire_contract.json)
own packet offsets, PE identity, instruction authentication and the complete
Lua/LPB identities. The purpose selectors remain documented in the
[party matching contract](party-matching-client-contract.md).

## Player search

`PcSearchWidget.init` configures operator request and child-widget conditions
and writes `XmlDataMaker_Data.string_command_line`, using `mode_widget` when
no argument is supplied. `processAfterShow` asks the desktop widget for player
experience information. Its `update` method writes current-skill information,
class/level rows and a terminating class value -1, then sends
`UIOperatorCommands.Reply` value 1. `processUIOperatorCommandRequest` supports
Tell, party invitation by name and the request-to-join-party status toggle.

These Lua methods do not construct the search filter record or consume a
wire-row argument list. The native `PcSearchWidgetOperator` builds the
serverbound `0x01DD` filter request. The application dispatcher consumes
clientbound `0x01DF` and `0x01E0`. `PcSearchContractor` callback slot 1 at
`0x00874610` calls `FUN_00693B50` to project cached native records and comment
pointers into the widget. This is a native callback slot, not a
LuaActorImpl receiver slot.

Evidence: `lua/scripts/widget/pcsearchwidget.lua:11-53,58-73,121-179,205-255`.
The original Lua 5.1 payload identifies `processAfterShow` as prototype `0.1`,
PC 1..11, code offset `0x359`; `update` as `0.3`, PC 1..42, code offset
`0x52A`; and `processUIOperatorCommandRequest` as `0.5`, PC 1..35, code offset
`0x7D1`. The decoded script SHA-256 is
`80cb01f52b28bd3273aa8cd69d7906b5bf21eb54bc8cfd6f6a81511b2c45cd5f`.
The original LPB payload SHA-256 is
`e25be2fa13ce9e9b66c1c658076493d632722226080aa93574590acdb024a122`.

## Recruitment results

`PcMatchingFindWidget` uses the native `Result_Maker` control as its result
source. Native `FUN_004B5F50` consumes clientbound `0x01C7`, fills the
recruitment cache and sets operation state 10. `FUN_004BD170` writes the
result properties, publishes an Update action and sets
`Button_Operate.IntData.Value2` to 4.

The Lua `processUICommandDefault` handles `UILuaCommands.PropertyChanged`.
When `getSignal()` returns 4, it updates the grid, sets signal 2 and calls
`updateList`. `getSignal` and `setSignal` read and write user-work integer
slot 3 on `Button_Operate`. `updateList` obtains the count from
`TextBlock_ResultMessage` and reads each `Result_Maker` row's `name`,
`purposeInt`, `placeInt`, `socialInt`, `skillInt`, `currentInt` and
`demandInt`. It formats the display strings and updates the list control.
The -1 count branch displays text 2939 with value 30 and renders 30 rows.
The zero branch displays text 2940. A positive count uses text 2938.

This provides a native wire-to-cache-to-property-to-Lua route for the list.
There is no recovered Lua receiver that directly deserializes `0x01C7`, and
no LuaActorImpl slot is needed for this observed route.

Evidence: `lua/scripts/widget/pcmatchingfindwidget.lua:1805-1837,2106-2329,2481-2508`.
The original payload identifies `processUICommandDefault` as prototype
`0.17`, PC 1..256, code offset `0x3315`; `updateList` as `0.18`, PC 1..231,
code offset `0x3A80`; `setSignal` as `0.24`, PC 1..10, code offset `0x4721`;
and `getSignal` as `0.25`, PC 1..7, code offset `0x47AB`.
The decoded script SHA-256 is
`972e7bbd07c221af78243631c6d88e801a7a5ecd856f3c9f2672a858461c0b8c`.
The original LPB payload SHA-256 is
`c3eb7cde349381d70d70ea5a6d299af412de07645ce7e128e15e6d96e234586a`.

## Acceptance boundary

Serverbound `0x01C6` carries selected cached-row key components. The actual
clientbound answer is also `0x01C6`, consumed by `FUN_004C9D60` through the
application dispatcher. The consumer stores its first application byte, emits
text `0x0B8D` for zero and sets operation state 12.
`FUN_004BF4F0` then branches on answer value 1 while updating the widget.
The static route establishes neither server eligibility nor a successful
retail acceptance session.

The clientbound `0x01C7` list and `0x01C6` answer therefore have substantive
application consumers even though their separate interface callbacks return
without reading payloads. The application dispatcher is `FUN_004CE190`, reached
through `0x004E221D` and `0x004DC715`. A no-op callback in another route does
not negate these direct consumers.
