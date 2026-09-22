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

## Evidence boundary

The scripts do not define numerical party bonuses, application eligibility,
recast time, persistence, removal policy, server authority, or historical
runtime state. The names `LightPartyEffect` and `FullPartyEffect` are client UI
commands, not proof of a party-size threshold outside the recovered branch.
