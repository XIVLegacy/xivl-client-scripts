# Craft command and progress contracts

Decoded 1.23b bytecode for `CraftJudge` and `CraftProgressWidget` reproduces
the canonical corpus exactly with the repository's pinned decompiler. The
retained
[`craft_command_progress_contracts.json`](../manifests/craft_command_progress_contracts.json)
pins both chunks and the command tables below.

`CraftJudge` classifies command IDs into system `22501-22549`, standard
`22550-22698`, and gift `29501-29698` bands. It also carries three explicit
16-ID standard-command sets named normal, rapid, and bold. Craft class IDs
29 through 36 select base IDs 22550, 22556, 22562, 22568, 22574, 22580,
22586, and 22592 respectively. Off-hand orders add three before returning the
three consecutive standard commands. Order values 1 or 2 append command
22506.

For a player, `CraftJudge.openCraftProgressWidget` opens
`CraftProgressWidget`; `updateInfo` forwards its supplied values to the
desktop widget update route. `CraftProgressWidget.setInitialData` stores the
provided progress, craft-point, and quality values. It fixes maximum progress
at 100 and substitutes 999 when either supplied craft-point or quality maximum
is zero or nil, then forwards the values to `updateProcess` for display.

These are client classification and UI-routing facts. They do not establish
craft success formulas, quality formulas, durability changes, inventory
mutation, experience rewards, command eligibility, or server validation.
