# Party matching client contract

`PcMatchingEditWidget` constructs local purpose and content-selection rows from
recovered Lua. Its direct literals establish client list inputs and widget
branches; they do not establish server eligibility, duty start, or encounter
ownership. The occupancy callback map and status-title join are in
[MyPlayer timer consumers](myplayer-timer-consumers.md).

## Purpose selector

`makePurposeList` supplies the following widget slot, text ID, and stored
purpose-value triples. The Lua passes zero-based slots to `setPurposeList`,
which increments them for the widget control.

| Widget slot | Text ID | Purpose value |
| ---: | ---: | ---: |
| 1 | 2920 | 0 |
| 2 | 4005 | 1 |
| 3 | 4026 | 2 |
| 4 | 4027 | 3 |
| 5 | 2941 | 15 |
| 6 | 2968 | 16 |
| 7 | 2961 | 17 |
| 8 | 2962 | 19 |
| 9 | 7301 | 34 |
| 10 | 10059 | 20 |
| 11 | 2963 | 18 |
| 12 | 2964 | 32 |
| 13 | 10049 | 35 |
| 14 | 2947 | 31 |
| 15 | 2949 | 33 |
| 16 | 2942 | 99 |

The class disables slot 16 when `countPartyMember()` is greater than one.

## List builders

`makeRaidList`, `makeBanshinList`, and `makeHamletList` add rows only when the
matching `_getOccupancyContentsTime(id)` result is positive. The exact
occupancy IDs and their independent native vector indices are recorded in the
linked timer finding. This is a client-side row condition, not a recovered
server eligibility rule.

In `makeBanshinList`, the client passes place keys to `maskPlaceList` after
adding selected rows: ID 4 masks 3019 and 3038; ID 3 masks 3038; ID 5 masks
1280078; and ID 12 masks 1280099. For ID 15, `_getBelongGrandCompany()` selects
111433, 111633, or 111833 for company values 1, 2, or 3; ID 16 uses 110870.
`setGLComboBoxData` uses text ID 5001 for those four selector values under
purpose value 16 and 10051 otherwise. These IDs are inputs to the display
branches, not proven unlock or quest-state semantics.

`makeChocoboList` passes six pairs to `setGLComboBoxData` under purpose value
34. The second value in each pair is also passed to text ID 2966; with a zero
override, the first value is stored as the row's user-work value.

| Slot | First value | Second value |
| ---: | ---: | ---: |
| 1 | 1280005 | 1031 |
| 2 | 1280003 | 1030 |
| 3 | 1280066 | 2004 |
| 4 | 1280073 | 2003 |
| 5 | 1280034 | 3043 |
| 6 | 1280033 | 3044 |

The function name identifies this as the Chocobo list, but these values alone
do not bind a row to a server route or establish either value's canonical
place-name meaning.

Other direct list inputs are:

- `makeBanzokuList`: 1125, 3521, 4503, and 5009.
- `makeRushList`: 51143 and 51144.
- `makeNMList`: 3107616, 3102012, 3100801, 3104214, 3102720, 3107618, 3104513,
  3103203, 3104323, 3101612, 3106628, 3100311, 3101511, 3110312, 3101513,
  3102806, 3101011, 3106221, 3100515, 3100512, 3105915, 3102611, 3100612,
  3103009, 3100117, 3102311, 3105515, 3100913, 3106312, 3101415, 3106557,
  3100717, 3106209, 3106019, 3106433, and 3101710.
- `makeLevelingList`: `setGLComboBoxData(1, 2965, 0, 102)`.

These are the values used by their named list builders; they do not by
themselves identify server content rows or runtime policy.

## Party controls

`numberOfPeopleRemain` returns 7 when `countPartyMember()` is zero and
otherwise returns `8 - countPartyMember()`. In `processUICommandOperate`, the
`Button_Operate` path notifies with 30507 and closes the widget when the player
confirm-group-command variation is 10001 or 10002. It has a separate matching
branch that also notifies with 30507 and closes the widget when the party has
more than one member and the local player is party leader. These are
widget-side guards, not a complete recruitment or party matching server
contract.

## Evidence boundary

The canonical script entry is
`manifests/scripts.json:15735`: decoded path
`lua/scripts/widget/pcmatchingeditwidget.lua`, 118,943 bytes, SHA-256
`6944f874d7d4caa57c8b50d48512041c649d33ba1f27f04a6353c5c2ddb8e07f`.
`manifests/retail_lua_coverage.json:27554` pins its source resource
`n1635q/u7x9q721w3561qn1635q.le.lpb` at 33,862 bytes, SHA-256
`530d0636d305515ce06a5de639e3527f227358a60ded1af41e8994a381c0ef2d`, and
decoded payload SHA-256
`86afa854ce49d06eb4acd1da9e6e46706fce4ef401759fb1ad2191fffc9b262b`.

The calls and values above describe recovered widget code. They do not prove
that a particular row was visible in a retail session, that a timer value was
positive, or that any server accepted the corresponding selection.
