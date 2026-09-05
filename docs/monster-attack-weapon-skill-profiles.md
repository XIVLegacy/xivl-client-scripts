# MonsterAttackWeaponSkill getter profile

[`manifests/monster_attack_weapon_skill_profiles.json`](../manifests/monster_attack_weapon_skill_profiles.json)
records the six constant getter rules defined by
`/Command/Game/WeaponSkill/MonsterAttackWeaponSkill`. The producer reads only
the exact decoded source file and stores compact defaults with grouped sparse
command-id overrides. It does not require a command catalog or copy decoded
Lua into this repository.

The source is the 1.23b extraction `2012.09.19.0001` script
`lua/scripts/command/game/weaponskill/monsterattackweaponskill.lua`, pinned by
SHA-256 `d5b8e884aad2ca2cfe5cfa96cf5e029d975a32bb0bc1742873ded2f3a78b668e`
and by its retained row in `manifests/scripts.json`. The declared parent is
`/Command/Game/WeaponSkill/WeaponSkillBaseClass`.
The producer cross-checks that row's path, hash, byte count, and line count
when rebuilding or checking the retained profile.

Run the producer against a hydrated decoded corpus:

```text
python tools/monster_attack_weapon_skill_profiles.py --scripts-root <path>
```

Check the retained manifest without supplying decoded bytes:

```text
python tools/monster_attack_weapon_skill_profiles.py --check
```

The profile preserves the recovered boundary that `getCommandInformation`
returns a value only for selector 8. The pair returned by
`getPartsDamageAdjust` is retained as two values; its consumer and combination
rule remain unresolved.
