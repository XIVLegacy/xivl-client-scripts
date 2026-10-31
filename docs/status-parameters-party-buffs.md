# Status parameters and party buffs

Decoded bytecode for `StatusWidget`, `DesktopWidget`, and
`PartyBuffEffectWidget` reproduces the canonical 1.23b corpus exactly. The
retained
[`status_parameters_party_buffs.json`](../manifests/status_parameters_party_buffs.json)
pins the three chunks and the mappings below.

## Craft and gathering parameters

`StatusWidget.updatePcParameter` obtains six values from the player and passes
each one directly to a display setter. Every setter converts the received value
with `tostring` and writes it to `TextBlock_BaseParameter` under the named
label.

| Player getter | Status setter | UI label |
|---|---|---|
| `getCraftProcessing(1)` | `setCraftProcessing` | `Label_PhysicalProcessing` |
| `getCraftProcessControl(1)` | `setCraftProcessControl` | `Label_AlteredControl` |
| `getCraftMagicProcessing(1)` | `setCraftMagicProcessing` | `Label_MagicProcessing` |
| `getHarvestPotency(1)` | `setHarvestPotency` | `Label_GatheringAbility` |
| `getHarvestLimit(1)` | `setHarvestLimit` | `Label_GatheringResistance` |
| `getHarvestRate(1)` | `setHarvestRate` | `Label_GatheringInspiration` |

This identifies presentation vocabulary and value routing. The widget performs
no numerical bonus calculation in these setters.

## Party-buff identity and effect

`DesktopWidget.getPartyBuffID` accepts only status IDs 223193 and 223194.
When a recognized status is added for the local player, the desktop route
passes that ID to the party widget. If the separate party-buff effect widget is
shown, it calls `startEffect` with true only for status 223194.

`PartyBuffEffectWidget.startEffect(false)` sends
`LightPartyEffect.Start`; `startEffect(true)` sends
`FullPartyEffect.Start`. The IDs therefore select ordering/state in the party
widget and light-versus-full presentation in the effect widget.

The separately maintained [MyPlayer timer consumer](myplayer-timer-consumers.md)
report remains the canonical home for the `StatusWidget` content-timer paths.
This finding does not duplicate those timer claims.

## Aurum status predicates

The canonical `lua/scripts/status/dotaurumstatus.lua:11-26`
has SHA-256
`c0067d845c1b5b5ad53fb594b46de6762ae2fa77860b93185816230cdfe96004`
(`manifests/scripts.json`).
The matching
`client/script/rq9qpr/6vq9pspxrq9qpr.le.lpb` has SHA-256
`7662408d2a5eb007f136e4f0bea13ae3b7651eaaf5cf7b25b8b6abc0e639182d`.
`DotAurumStatus.isRemovedFromDeath` returns false and
`canStartOnDead` returns true. These are class-level client predicates;
the script does not bind the class to status ID 223258 or 223259, identify
an Aurum room or area, or establish a server damage rule.

## Part-break status predicate

The canonical `lua/scripts/status/partsbreakstatus.lua:11-17`
has SHA-256
`8d7691f2946650ab817bd91e111f66785863f50b9995a0e5ed163928e82f9c63`
(`manifests/scripts.json`).
The matching
`client/script/rq9qpr/u9sqr8s59zrq9qpr.le.lpb` has SHA-256
`90c2c572c59301d77e3e4cf3077d71a7df154a639f21f7b226d1de26627c8b31`.
`PartsBreakStatus.isBadStatus` returns true. This class-level predicate
does not identify a status ID, monster, part index, breakage bit, damage
threshold, or recovery rule.

## Main-skill-change status predicates

The canonical decoded status scripts recover a class-level
`isRemovedAtChangeMainSkill` predicate. `StatusBaseClass` returns false;
`BerserkStatus` and `DivineAttackStatus` each override it with literal true.
These three bodies read no sheet column, current class, destination class or
active job.

| Canonical source | Lines | Return | SHA-256 |
| --- | --- | --- | --- |
| `lua/scripts/status/statusbaseclass.lua` | 117-123 | false | `132f18c5f22f9958ab5a8c665ba99f8ed1e9ae4e55674cdf46e42bac565abbfa` |
| `lua/scripts/status/ability/berserkstatus.lua` | 11-17 | true | `12c408bbebd3446c8a8e67a1c105a8a677862b1b889a6d48cd2b0fecb668cb07` |
| `lua/scripts/status/ability/divineattackstatus.lua` | 11-17 | true | `3fa16fe5e80b6810eb4eb4ba92358679cbef136030859bbb794c55ce41923d56` |

The byte identities are recorded in
[`scripts.json`](../manifests/scripts.json). This is a direct reading
of the pinned decoded source, without a separate bytecode or runtime check.

The static-actor map in
`xivl-client-data:manifests/staticactor_class_paths.json` and the exact-name
rows in `xivl-client-data:derived/status_names.csv` join Berserk row 223207 to
`/Status/Ability/BerserkStatus` and Cleric Stance row 223227 to
`/Status/Ability/DivineAttackStatus`. The map's SHA-256 is
`d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
The identically named Berserk rows remain separate: 223160 binds
`/Status/ParameterControlStatus`, and 231004 binds `/Status/DummyStatus`.
The selected recovered bodies define direct subclasses of `StatusBaseClass`
without a main-skill-change override, so they retain the base false predicate.
Their canonical source identities are:

- `lua/scripts/status/parametercontrolstatus.lua:1-112`, SHA-256
  `eef787f210d186a7e459562bf9cc3af5eeec2aaa33ce478dca27753b87311c2c`.
- `lua/scripts/status/dummystatus.lua:1-8`, SHA-256
  `974c1608bbce034994fa0c00719f3aa9089231c972996cef62b870fd1de0dd14`.

This identifies recovered client predicates and exact row bindings. It does
not establish which named status was active in retail, which caller evaluated
the predicate, removal on a main-hand swap, or a server rule. In particular,
the separate main-skill and active-job state described by
`xivl-decomp:docs/actor/job-soulstone-state.md#base-class-active-job-and-stone`
does not make command 12017 soul-stone equip or unequip a main-skill change.
Removal on either job transition and the order of clear packets remain
unresolved.

## General evidence boundary

The scripts do not establish numerical party bonuses, server application
eligibility, applied durations, historical runtime persistence or server
removal policy. The names `LightPartyEffect` and `FullPartyEffect` are client UI
commands, not proof of a party-size threshold outside the recovered branch.
