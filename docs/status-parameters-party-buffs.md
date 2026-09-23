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

The independently recovered
`tools/outputs/lpb/decomp_further_20260617/lua/status/dotaurumstatus.lua`
has SHA-256
`a27b3c7cd13dec091e1cb585a7b7f29c107ab3bc0567d8c9df22c88105778cc8`.
The matching installed
`client/script/rq9qpr/6vq9pspxrq9qpr.le.lpb` has SHA-256
`7662408d2a5eb007f136e4f0bea13ae3b7651eaaf5cf7b25b8b6abc0e639182d`.
`DotAurumStatus.isRemovedFromDeath` returns false and
`canStartOnDead` returns true. These are class-level client predicates;
the script does not bind the class to status ID 223258 or 223259, identify
an Aurum room or area, or establish a server damage rule.

## Part-break status predicate

The independently recovered
`tools/outputs/lpb/decomp_further_20260617/lua/status/partsbreakstatus.lua`
has SHA-256
`98b6c14d2dab97d1b68e85339d32e33883e7db68552b0ccb25935efda6f9bec2`.
The matching installed
`client/script/rq9qpr/u9sqr8s59zrq9qpr.le.lpb` has SHA-256
`90c2c572c59301d77e3e4cf3077d71a7df154a639f21f7b226d1de26627c8b31`.
`PartsBreakStatus.isBadStatus` returns true. This class-level predicate
does not identify a status ID, monster, part index, breakage bit, damage
threshold, or recovery rule.

## General evidence boundary

The scripts do not define numerical party bonuses, application eligibility,
recast time, persistence, removal policy, server authority, or historical
runtime state. The names `LightPartyEffect` and `FullPartyEffect` are client UI
commands, not proof of a party-size threshold outside the recovered branch.
