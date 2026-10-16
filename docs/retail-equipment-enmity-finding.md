# Equipment changes while holding enmity

Verdict: a general 1.23b refusal of equipment changes while holding enmity,
and its message ID, are unestablished by the retained evidence below.
The documented restriction on class and job changes is narrower.

## Evidence

The retained official manual's `Classes and Jobs`, sections `Changing Classes`
and `Changing Jobs`, disallows those changes during event scenes, under attack,
or in active mode. It describes changing the main-hand equipment to change
class. It does not equate being under attack with holding any enmity, or extend
that restriction to every equipment slot.
Source: `xivl-captures:sources/lodestone-manual/objects/pages/classes-and-jobs.md`,
SHA-256 `51ec22fa96d93965928b5ada31b1ae9e2eabe23d9286fd0c0d73dd894348f617`.
`xivl-captures:sources/lodestone-manual/manifest.yaml`, member
`pages/classes-and-jobs.md`, owns the retained source identity and
2015-01-08 snapshot. The study class is `web-tables`: documented intent,
not a recorded 1.23b runtime refusal.

The [equipment command contract](equipment-cancel-command-contracts.md#local-refusals)
owns the authenticated command 12007 route. Its own class adds no eligibility
predicate. The inherited actor-state check returns 32509 for dead states,
32501 for seated states, and 32502 for the recognized nonzero states under
`gameCommand.csv` column-37 rule 1. Those are numeric main-state comparisons.
They do not identify the gameplay conditions that assign the states or an
enmity-specific refusal message. The inspected route contains no
command-specific enmity predicate.

The class is `lua/scripts/command/game/changeequipsetcommand.lua:1-26`, source
SHA-256 `53568ae20767c4b0c835018ccc87e0bc67b889a5ce64b33e53c67e15a616a651`,
pinned by [scripts.json](../manifests/scripts.json). The contract's
`Local refusals` and `Input identities` sections identify the inherited
`GameCommandBaseClass` payload and instruction offsets.

## Unestablished boundary

`PlayerBaseClass.canCommand` also calls native `_canExecuteCommand`, and the
admitted command can reach the server fallback. Neither native scheduler
admission nor server refusal is resolved by the Lua class. A local return,
the manual's class-change rule, or raw text ID 32502 cannot establish the
requested held-enmity equipment rule or its displayed message. This finding
does not establish that equipment changes succeed while holding enmity.
