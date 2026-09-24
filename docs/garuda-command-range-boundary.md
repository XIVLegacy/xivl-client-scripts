# Garuda command range boundary

The shipped `BattleCommandBaseClass.getCommandRangeCode` and
`getRangeAngle` methods each contain a single Lua 5.1 `RETURN` with no
values or constants. They are empty overrides, not numeric range or
angle selectors. The ancestor `GameCommandBaseClass.getRangeAngle`
returns 120, but that default does not supply a Garuda-specific cone
angle through these overridden methods.

`GameCommandBaseClass.getCommandRangeShape` delegates to range-code,
angle, rotation, and effect-range getters. Its
`getCommandRangeLength` returns range and minimum range separately
for the non-weapon branch. Neither wrapper is a geometric
intersection test. `GarudaAttackWeaponSkill` has no own method closure
and inherits `WeaponSkillBaseClass` then `BattleCommandBaseClass`;
`GarudaOthers` likewise has no own closure and inherits
`BattleCommandBaseClass`. These class bodies supply no additional
Garuda angle override.

The five relevant `.le.lpb` files were decoded with
`xivl-client-structs/tools/decode_lpb.py`. Their encoded paths, raw hashes,
and decoded-chunk hashes are recorded at
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json)
(source rows 21690, 21855, 21870, 22335, and 22410). The canonical
source identities are in [`scripts.json`](../manifests/scripts.json)
(rows 6867, 6903, 6981, 7251, and 7299):

| Decoded script | Decoded SHA-256 |
| --- | --- |
| `command/game/gamecommandbaseclass` | `1b3ba520dc0efb2f1941d2b8206d33f7a2e1a8ee52a6012092563395f853a6f7` |
| `command/game/battlecommandbaseclass` | `95d29680ba473e0090a3a90573d38e7ce13a9ca63759c7f846bc8a9e5fa83eb0` |
| `command/game/weaponskill/weaponskillbaseclass` | `eae69c37113f42d62bd6031d8869dff880c4d389da1eae43ca6864f8f23b86c1` |
| `command/game/weaponskill/garudaattackweaponskill` | `c7a1782af189b59dbad096290e944783a0a47dd94d0b7858bf179c1dc5f12eaf` |
| `command/game/basic/garudaothers` | `d4dc1af5445c6c56b39ce6c578db993709a2c3327df5889d3b47a8776872f3f2` |

The empty methods are at decoded bytecode offsets `0x52E` and `0x55A`
in `battlecommandbaseclass`, respectively. The contributor's
bytecode pass supplied the instruction offsets and class-method census;
the pinned LPBs and canonical scripts above identify the inspected inputs.
These are script facts, not a command-ID-to-class
binding or proof of the client/server hit evaluator. The active range
selector, angle unit, radius/diameter convention, and retail damaging
geometry remain unresolved.
