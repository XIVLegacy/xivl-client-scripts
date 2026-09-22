# Monster map-marker selection

The 1.23b client Lua maps four negative `potencial` values to four notorious
monster ranks. `DepictionJudge` then uses two of those ranks while selecting a
monster's local map marker.

The retained
[`monster_map_marker_selection.json`](../manifests/monster_map_marker_selection.json)
pins the decoded bytecode, canonical decompiler output, tool identity, source
locators, and exact branch table. Re-running the repository's pinned unluac
tool over both decoded chunks reproduces their canonical `scripts.json` hashes.

## Potential and rank map

For a non-player actor, `CharaBaseClass.calcPotencial` reads monster-base field
132 first. Numeric values 1 through 4 return potential values -1 through -4.
A truthy non-number returns -1. Other values fall back to monster-base field
87 and the level interpolation path. `CharaBaseClass.getPotencial` reads the
stored value from `charaWork.battleSave.potencial`.

`CharaBaseClass.isNotoriousMonster` maps the stored values as follows:

| Potential | Is notorious | Rank |
|---:|---|---:|
| -1 | true | 11 |
| -2 | true | 12 |
| -3 | true | 13 |
| -4 | true | 14 |
| other | false | 0 |

The recovered name is spelled `potencial` in the client script and is retained
as an identifier rather than corrected.

## Depiction branch

In the non-player monster branch, `DepictionJudge.judgeNameplate` obtains
`getHateType` and both return values from `isNotoriousMonster`.

| Condition | Initial marker |
|---|---:|
| Hate type 1 or 2, rank 13 | 8 |
| Hate type 1 or 2, other rank | 5 |
| Other hate type, occupancy-party member, rank 13 | 9 |
| Other hate type, occupancy-party member, other rank | 4 |
| Other hate type, not an occupancy-party member, rank 13 | 8 |
| Other hate type, not an occupancy-party member, other rank | 5 |

Rank 12 then overrides the selected marker with 7. Finally,
`isMapMarkerVisibleForTalkable` can replace the marker with `nil` before the
script calls `_setMapMarker`. Ranks 11 and 14 have no special case in this
branch and therefore retain the applicable non-rank-13 default.

## Evidence boundary

This finding concerns the actor depiction script's local `_setMapMarker`
selection. It does not name marker artwork, map marker packet fields, actor
class IDs, a specific notorious monster, or a full-map group marker. It is
separate from `SetActorIcon` and from the s2c `0x018D` full-map consumer.

The branch establishes client presentation after the named methods return. It
does not establish how a server chooses monster-base fields 87 or 132, how the
stored potential value arrives at the client, or whether a given historical
actor instance took the branch.
