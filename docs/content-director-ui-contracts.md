# Content director UI contracts

The recovered 1.23b Lua corpus preserves client-side director state and UI
contracts for guildleves, request leves, caravan escort, and Hamlet defense.
A reproducible decompile of the decoded chunks matched the canonical corpus
byte-for-byte after CRLF-to-LF normalization. The source identities, hashes,
locators, and claim boundaries are in
[`content_director_ui_contracts.json`](../manifests/content_director_ui_contracts.json).

## Guildleve and request directors

`GuildleveBaseClass` stores the guildleve identifier, start time, aim counts,
UI states, extra marker coordinates, and a time limit. During initialization it
loads the guildleve sheet for the selected identifier and reads column 21 into
the retained `timeLimit` field. Other helpers read the recommended rank and
word text from columns 5 and 19. The class drives guildleve-information UI and
map or minimap marker calls from retained state.

`RequestDirector` derives from `GuildleveBaseClass`, overrides the time limit
with the literal value 20, and supplies request-specific UI initialization,
update, article, state, and parameter methods. These scripts establish client
state layout, sheet consumption, and widget calls. They do not establish
server timers, objectives, acceptance rules, completion, or rewards.

## Caravan escort director

`CaravanGuardDirector` retains `finishTime`, `progressPer`, three chocobo status
values, three chocobo HP status values, and marker coordinates. Its UI methods
return those retained values and update public-effect, minimap, and map
navigation widgets. This authenticates client presentation fields and their
widget routes, not escort movement, enemy waves, failure rules, rewards, or the
server authority that updates the fields.

## Hamlet defense director

`InstanceRaidHamletDefense` derives from `InstanceRaidBaseClass`. It retains a
Hamlet identifier, rank, defense-line status, and goods status, opens the
Hamlet execution widget, and routes timer, defense-line, goods, and boss status
values to that widget. Its local clear path requests the local player's Hamlet
defense score and, when available, opens the score widget for the content ID.

These methods establish client UI consumption only. They do not establish
enemy waves, routes, scoring formulas, victory conditions, server ownership,
or rewards.

## Evidence boundary

No Behest or Skirmish script in this filing proves wave composition, routes,
objectives, timers, or rewards. Those systems, and the server-side behavior
behind the four recovered directors, remain unresolved and must not be filled
from analogy.
