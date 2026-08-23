# Guildleve journal state and commands

The retail 1.23b Lua corpus distinguishes the state of a retained guildleve
journal entry from the requests to retry or remove it. These scripts establish
client presentation and command arguments. They do not establish the server's
authoritative state changes.

## Journal state

`JournalDetailWidget.checkGuildleveProcess` returns `checked`, `done`, and
`failed`, where `failed = done and not checked`. The list widget uses the same
two stored bits to select its active, failed, and completed presentations. A
nonzero journal ID is required before either widget reaches this state logic.

| done | checked | Client presentation |
|---|---|---|
| false | false | Retained entry without an active, failed, or completed flag |
| false | true | Active |
| true | false | Failed |
| true | true | Completed |

For journal mode 1, regional type 1 and local type 2 entries expose Retry and
Break controls. Retry is enabled only for a failed entry when the supplied
`offerLimit` is positive. This is a client-side precondition, not evidence of
where or when an allowance is decremented.

Evidence: `lua/scripts/widget/ask/journaldetailwidget.lua`,
`lua/scripts/widget/ask/journallistwidget.lua`,
`lua/scripts/chara/player/player_work.lua`, and
`lua/scripts/chara/player/playerbaseclass_work.lua`.

## Command mapping

After confirmation, the detail widget passes the journal type, journal ID, and
selected subindex to `DesktopWidget.executeJournalCommand`.

| Journal type | Subindex | Request |
|---|---:|---|
| 1, regional guildleve | 2 | Break |
| 2, local guildleve | 3 | Break |
| 1, regional guildleve | 4 | Retry |
| 2, local guildleve | 5 | Retry |
| 3, quest | 1 | Break |

Direct Lua 5.1 bytecode control flow establishes that valid journal types 1,
2, and 3 call system command 24241 as
`command(24241, journalID, subindex, nil, nil)`. The journal type validates the
route but is not forwarded. Invalid types and a missing command object return
false. The caller closes the detail widget only when the forwarded result is
exactly true; that result is not proof that a server mutation completed.

Evidence: `lua/scripts/widget/ask/journaldetailwidget.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`, and
`lua/scripts/chara/player/playerbaseclass.lua`. The published decompile
misstructures the type 1 and 2 branches in `executeJournalCommand`; the command
argument claim is therefore bounded to the decoded bytecode control flow.

## Ownership boundary

The command 24241 registration and player-facing text belong to
`xivl-client-data`. Native guildleve execution retirement and director object
finalization belong to `xivl-client-structs:manifests/guildleve_lifecycle.json`.
Neither owner currently maps subindices 2-5 to an outgoing packet or proves
Break and Retry server mutations. This page does not infer those behaviors from
widget closure or native director teardown.
