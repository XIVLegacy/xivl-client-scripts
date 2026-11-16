# NPC map-marker selection

`DepictionJudge.judgeNameplate` selects the local map marker of every actor
it judges. The [monster page](monster-map-marker-selection.md) records the
monster branch. This page records the retainer and talkable branches of a
non-player actor and the `NpcBaseClass` defaults they read.

## Branches

In `judge/depictionjudge.lua` (`judgeNameplate`, `:11-814`), an actor that
`isDeadMode` reports dead takes `_setMapMarker(nil)` unless it is a player
(`:343-363`). A living non-player that is a member of the local player's
party, the `getPlayerParty()` group read at `:16-19`, takes
`_setMapMarker(1)` (`:450-466`). For any other living non-player for which
`isPropertyEnabled(3)` is false (`:469-472`), the branch runs these arms in
order (`:684-806`):

| Condition | Nameplate colour call | Marker call |
| --- | --- | --- |
| `isRetainer()`, system flag 1 true | by group 80001 membership | `_setMapMarker(4)` |
| `isRetainer()`, system flag 1 not true | by group 80001 membership | `_setMapMarker(6)` |
| `_isTalkable()` true, `isMapMarkerVisibleForTalkable()` exactly true | `(1, 0.5, 1, 0.5, 1)` | `_setMapMarker(getMapMarkerTypeForTalkable())` |
| `_isTalkable()` true, otherwise | `(1, 0.5, 1, 0.5, 1)` | `_setMapMarker(nil)` |
| not talkable, `getMapMarkerRange()` not nil | `(1, 0, 0, 0, 0)` | `_setMapMarker(nil, getMapMarkerRange())` |
| not talkable, otherwise | `(1, 0.5, 0.5, 0.5, 1)` | `_setMapMarker(nil)` |

The retainer arm reads `_getSystemFlag(1)` and sets the nameplate colour
`(1, 0.7, 0.5, 1, 1)` for a member of group 80001 and `(1, 0.5, 0.5, 1, 1)`
otherwise.

## NpcBaseClass defaults

`chara/npc/npcbaseclass_event.lua` defines
`NpcBaseClass.isMapMarkerVisibleForTalkable`, which returns true (`:821-827`),
and `NpcBaseClass.getMapMarkerTypeForTalkable`, which returns 6 (`:830-836`).
Subclasses may override either. They are not enumerated here.

`chara/npc/npcbaseclass_u.lua` binds `_isTalkable_inl(self, a)` with one
declared parameter after `self` to `"self", "_isTalkable_cpp"` (`:64-71`).
`judgeNameplate` calls `_isTalkable()` with no argument (`:744-746`).

INFERRED. A talkable NPC that keeps the defaults takes marker number 6. How
the native binding reads the argument the call omits is not established
here. The native filter callback is in
`xivl-client-structs:docs/chara-desktop-native-contract.md`, "NpcBase filter
natives".

## Evidence boundary

This finding is local script selection. It does not establish when the
client runs `judgeNameplate` for a given actor, which subclasses override
the defaults, or how the marker number reaches a map. The native use of the
stored number is in `xivl-decomp:docs/resource/minimap-marker-entries.md`,
"Actor entries".

## Source identity

The extraction is retail 1.23b `2012.09.19.0001`. Canonical sources matched
[scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule, and
the original resources matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Canonical source | Bytes / lines | SHA-256 |
| --- | ---: | --- |
| `judge/depictionjudge.lua` | 22540 / 814 | `8DB4D613D72DDF1921E3C9C4A961714371D2EAC38FCC3B0211023105CB41A3E1` |
| `chara/npc/npcbaseclass_event.lua` | 20675 / 921 | `5417B1BDF762162CAD240A84715D0FC85958DBE0181B653348A66C02EE4D7C80` |
| `chara/npc/npcbaseclass_u.lua` | 4131 / 237 | `74A54C805173F12C5513C2746C4EA65846F024438B0CF44116E77270DA3FAA0C` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `0p635/65u17q1vw0p635.le.lpb` | 4142 / `9EB9B7054434CD5281CB52C89A2D5B43A40913DC47AB4D11CC18FDDA4ADE6E76` | 4129 / `756FA626BF9703AFB5F97A36EB5BC3643EAF216CC602137DDE5F034F678B9F19` |
| `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` | 6262 / `84A5098636FF289F4ECF4E164E84E44890895E8A9005FB102E04929C2BB74BF9` | 6249 / `4A3008DD8D2A91E7EB044E5555D2757468A9097BBA5175992FB88F943BD07B6C` |
| `729s9/wu7/wu789r57y9rr_p.le.lpb` | 3160 / `1400E76A2735A079726A9920596F1B124C5F9BC912D0AF6FF9635348F9CAD6F8` | 3147 / `26FF1EB8502D975CF8A23C34B211D49265E434998966762BD4BF0D0FCCBF38FF` |

Decode each resource with `tools/retail_script.py` and the pinned unluac JAR
and read the methods at the lines above.
