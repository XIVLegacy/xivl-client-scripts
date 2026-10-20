# Rested experience client contract

The recovered 1.23b Lua chain treats `restBonusExpRate` as a value used to
derive a rested segment of the experience gauge. It is not used here as an
experience award multiplier. The client multiplies it by the current level's
skill point maximum and presents the result as a logout bonus segment beside
the normal skill point gauge.

## Getter to gauge

`PlayerBaseClass.getRestBonusExpRate` is an ordinary one-argument Lua method.
Its body reads `A0_2.playerWork.restBonusExpRate` and returns that value.
The corresponding property hash is
`0xd6917eac`, identified as `playerWork.restBonusExpRate` by
`xivl-client-structs:manifests/gam_hash_names.json`.

The update route is:

```text
PlayerBaseClass._onUpdateWork("playerWork", "expBonus", ...)
  -> DesktopWidget.processUpdateExpBonus(restBonusExpRate)
  -> PlayerProfileWidget.update()
  -> PlayerProfileWidget.updateExp()
  -> PlayerBaseClass.getRestBonusExpRate()
  -> PlayerProfileWidget.setSkill(...)
```

`_onUpdateWork` calls the desktop callback only for the `playerWork` and
`expBonus` pair. `processUpdateExpBonus` receives the rate but does not use
its argument; it obtains static child slot 4, named `PlayerProfileWidget`, and
calls `update`. `PlayerProfileWidget.update` refreshes only when the widget is
shown. Its `processBeforeShow` path also calls `updateExp`.

`updateExp` reads the local player, current skill, class or job, skill level,
current skill points, current-level maximum, next-level maximum, and the rest
rate. Its relevant calculation is equivalent to:

```text
current = getSkillPoint(skill)
currentMax = getSkillPointMax(level)
nextMax = getSkillPointMax(level + 1)
restSegment = currentMax * getRestBonusExpRate()
```

It passes `current`, `restSegment`, `currentMax`, and `nextMax` to `setSkill`.
`setSkill` writes `current` to `ProgressBar_SkillRankEXP.Value` and `currentMax`
to its `Maximum`. When `restSegment` is nonzero, it selects style
`PRB_logoutBonus_blinkH`, shows `IconControl_LogoutBonus`, and places the
current-plus-rest value into the logout bars. If `currentMax` is at least
`current + restSegment`, it writes that sum to
`ProgressBar_LogoutBonus_1.Value` and zero to
`ProgressBar_LogoutBonus_2.Value`. Otherwise it writes zero to the first bar
and `currentMax` to `ProgressBar_LogoutBonus_2.Value`; it does not compute or
write a `current + restSegment - currentMax` overflow amount. The `nextMax`
argument passed to `setSkill` is unused by that method. When the segment is
zero, the logout icon is hidden and both logout bars are reset to zero.

The display has explicit near-cap guards. At level 48, it reduces the segment
when `current + restSegment` exceeds `currentMax + nextMax`. At level 49, it
reduces the segment when that sum exceeds `currentMax`. At level 50, it sets
the segment to zero. These are gauge-display bounds in `updateExp`; they do
not establish server accrual, a pool cap, or an award formula.

The source locators for this chain are:

| Prototype | Bounded source scope | Role |
| --- | --- | --- |
| `PlayerBaseClass.getRestBonusExpRate` | `chara/player/playerbaseclass.lua:1102-1109` | Reads and returns the `playerWork` field. |
| `PlayerBaseClass._onUpdateWork` | `chara/player/playerbaseclass.lua:1303-1426` | Routes `playerWork.expBonus` to the desktop callback. |
| `DesktopWidget.processUpdateExpBonus` | `widget/desktopwidget_connector.lua:6971-6983` | Refreshes the profile child; its rate argument is unused. |
| `PlayerProfileWidget.update` | `widget/playerprofilewidget.lua:69-81` | Refreshes the gauge only while shown. |
| `PlayerProfileWidget.updateExp` | `widget/playerprofilewidget.lua:84-155` | Computes the rested display segment. |
| `PlayerProfileWidget.setSkill` | `widget/playerprofilewidget.lua:177-320` | Writes the normal and logout bonus progress bars. |

The original Lua 5.1 chunks place these methods in bounded prototypes. The
line span is the chunk's `lineDefined` to `lastLineDefined` metadata. Code
offsets are zero-based byte offsets in the decoded payload, and each word is a
four-byte instruction.
The prototype index uses a depth-first walk with the root at index 0;
it is a parser locator, not a method or dispatch ordinal.

| Method | Prototype | Original line span | Code offset; words | Instruction-word SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `PlayerBaseClass.getRestBonusExpRate` | 20 | 6723-6725 | 10293; 4 | `2e677feeb3fc915f3591651020158cbbddae6a8d99189e7cc084f667c0e6ace2` |
| `PlayerBaseClass._onUpdateWork` | 31 | 6911-6952 | 12067; 111 | `596be556ef6c6f4fcfcca6293b8a07610612936aeafa9a3f1199e10a3000bd44` |
| `DesktopWidget.processUpdateExpBonus` | 117 | 5378-5381 | 76733; 7 | `5ff6787b13f7c64d30297e41575120a0b0c4cceb0e43a0b8c329454df79b6974` |
| `PlayerProfileWidget.processBeforeShow` | 2 | 101-104 | 743; 5 | `b33a265362211fc90c4d84b029df074d2ee4e99ac473314778fd20e992c4d652` |
| `PlayerProfileWidget.update` | 5 | 142-146 | 1015; 7 | `5bff3f03a326bfd3e57e32d57da703f1aff0d5c27b26801e25267e942bcbdf03` |
| `PlayerProfileWidget.updateExp` | 6 | 159-194 | 1110; 60 | `afdef45c07cc41e1c1b6046eadb63d81beebd7325cadf9a546afaf3dcfc0b5a9` |
| `PlayerProfileWidget.setSkill` | 8 | 220-259 | 1763; 122 | `e5093e2e0111ea8f6fd8308d1853eb6bbd64d9308714877b3b6cf7adfce1a3f3` |

## Input identities

The original resources below were selected by the registry's `ciphered` paths
and the matching rows in `manifests/retail_lua_coverage.json`. Their decoded
outputs matched the older retained decoded-script coverage in
`manifests/scripts.json` by byte count, line count, and SHA-256. LPB paths are
relative to the retail `client/script` root. The payload is the Lua 5.1 chunk
after the LPB wrapper; the source hash is the canonical decompile output.

| Decoded script | Source bytes; SHA-256 | Original LPB; bytes; SHA-256 | Payload bytes; SHA-256 |
| --- | --- | --- | --- |
| `lua/scripts/chara/player/playerbaseclass.lua` (3020 lines) | 66466; `6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4` | `729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`; 25846; `32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e` | 25833; `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a` |
| `lua/scripts/widget/desktopwidget_connector.lua` (26564 lines) | 660617; `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`; 213487; `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213474; `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `lua/scripts/widget/playerprofilewidget.lua` (376 lines) | 8674; `b734a6424a6236cce0eb00d7a31e1a9f3000837435fff12a859adc33dbc5a796` | `n1635q/uy9l5susv41y5n1635q.le.lpb`; 3228; `93c3d5b44ada9e5db934dac8896b9673c7bde328338c1e90dbea6c5132b86a37` | 3215; `7a6df4da513269e801f1827f4fe245ae73e69d6431f82ca151f3e8ad1b8720ba` |

The three LPBs were decoded with `xivl-client-scripts:tools/retail_script.py`
and the pinned `unluac_2025_12_23.jar`. This is a focused getter-to-gauge
trace, not a claim that every client consumer or native caller has been
recovered. The native methods that supply skill points, level maxima, player
identity, and widget property writes remain outside this Lua contract. The
Lua evidence also does not establish when the server changes the field, how
rest accumulates, the effective award percentage, an offline rule, or any
behavior after level 50.

The independent property-stream catalog records two observations of hash
`0xd6917eac` with parallel float decodings `0.331999987` and `0.33206898`.
Those observations corroborate the field identity and its float-shaped wire
value; they do not establish an accrual rate, an award multiplier, or the
cause of either value. See
`xivl-captures:studies/property-stream-hash-catalog/derived/property-records.csv`.
The exact locators are records 84 and 85, `check_room_map.pcapng`, lane 0,
frames 4 and 20, subevent 0, with bytes `e7fba93e` and `f204aa3e`.
The cited CSV has SHA-256
`244a87a0182c9d3f0b9de253cb7fc454b0f9fd07e2530d6f546b539b7269f437`.

## Documented award policy

The official [Patch 1.21 notes](https://forum.square-enix.com/ffxiv/threads/39024),
2012-03-08, `[dev1301]`, announced a 50% rested EXP increase for combat,
synthesis and gathering, offline accumulation up to an unspecified maximum,
no consumption at level 50, and no application to quest rewards or
levequest-completion EXP. This first-party announcement supports those rules
at documented-intent grade. It does not supply the accrual rate, pool cap,
rounding, or the interaction with other bonuses in retail 1.23b. The gauge
calculation above is separate from the announced award percentage.

Evidence: `lua/registry.json`, `manifests/scripts.json`,
`manifests/retail_lua_coverage.json`, and
`xivl-client-structs:manifests/gam_hash_names.json`.
