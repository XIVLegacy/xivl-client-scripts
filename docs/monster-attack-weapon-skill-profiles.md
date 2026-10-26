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
rule remain unresolved. The [profile schema](../schemas/monster_attack_weapon_skill_profiles.schema.json)
requires exactly two integers for its default and each override result.
The retained-profile check also verifies the canonical getter-rule digest.

## Selected command values

The retained `getPartsDamageAdjust` rule has an ordered default result of
`(1, 1)` and one command-ID override: `23114` returns `(1, 0)`. Each command
below selects the default and returns two separate values.

| Command ID | English display name | First return | Second return |
|---|---|---|---|
| 23604 | Thermionic Burst | 1 | 1 |
| 23605 | Plasma Acoustics | 1 | 1 |
| 23610 | Dalamud Dive | 1 | 1 |
| 23611 | Iron Chariot | 1 | 1 |
| 23612 | Lunar Dynamo | 1 | 1 |
| 23613 | Ravensbeak | 1 | 1 |
| 23614 | Chaos Thrust | 1 | 1 |
| 23615 | Twisting Vice | 1 | 1 |
| 23617 | Aetherial Emission | 1 | 1 |
| 23627 | Lunar Dynamo | 1 | 1 |
| 23631 | Fierce Ravensbeak | 1 | 1 |

These are `gameCommand.csv` row IDs. The public command rows in
`xivl-client-data:derived/command_battle_params.csv`, keyed by the IDs above,
record their English display names and
`/Command/Game/WeaponSkill/MonsterAttackWeaponSkill` class path. The same IDs
identify the class-path records in
`xivl-client-data:manifests/staticactor_class_paths.json`.
`xivl-client-data:docs/command-battle-params.md` defines those fields, and
`xivl-client-data:docs/command-script-identity.md` records the command-ID getter
and sheet-key relationship. Equal display names do not merge command IDs;
`23612` and `23627` remain separate rows.

The two returns do not establish multiplication, additive scaling, a body-part
enumeration or a damage formula. These selected command identities and values
do not establish Nael invocation, difficulty or a complete encounter action set.

## Consumer boundary

The [registry](../lua/registry.json) lists `getPartsDamageAdjust` declarations
for `MonsterSubStatAbility`, `GameCommandBaseClass` and
`MonsterAttackWeaponSkill`. Its `methods` and `requires` fields record
declarations and top-level require paths, as defined by the
[registry schema](../schemas/lua_registry.schema.json); they do not record
return-value consumers.

The [reference scanner](../tools/_corpus.py) accepts only underscore-prefixed
identifiers in its native API whitelist. The per-script `.calls.json` sidecars
and [N-API index](../lua/napi_index.json) therefore do not index ordinary Lua
`getPartsDamageAdjust` references. As the [corpus guide](../lua/README.md#canonical-form)
explains, the references that are indexed can also be accesses, callback
assignments or string literals. An absent getter entry cannot establish that
no Lua or native callback consumer exists.

The pair's consumer and combination rule remain unresolved. Establishing them
requires an actual caller or callback-dispatch locator that selects this
getter, together with its requested return arity and the immediate destination
or forwarding of each returned value.
