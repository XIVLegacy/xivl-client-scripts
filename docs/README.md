# Documentation

Guides to the extracted Lua corpus and findings from the Final Fantasy XIV
1.23b client. Each finding distinguishes recovered script behavior from
unverified native or server behavior.

## Start here

- [Lua Script Corpus](../lua/README.md)
- [Tooling](../tools/README.md)
- [XIVLegacy Client Scripts](../README.md)
- [Retail Lua resource coverage](retail-lua-coverage.md)
- [Vendored client-structs input](../data/vendor/client-structs/README.md)

## Commands and character state

- [Content command client route](content-command-client-route.md)
- [Player command event routes](player-command-event-routes.md)
- [TalkCommand client contract](talk-command-client-contract.md)
- [Craft command and progress contracts](craft-command-progress-contracts.md)
- [Equipment parameter formulas](equipment-parameter-formulas.md)
- [General parameter 18 consumers](general-parameter-18-consumers.md)
- [Garuda command range boundary](garuda-command-range-boundary.md)
- [Item compatibility eligibility](item-equipment-compatibility.md)
- [MyPlayer timer consumers](myplayer-timer-consumers.md)
- [Widget-open command boundary](widget-open-command-boundary.md)
- [ActionMenu grid visibility](action-menu-grid-visibility.md)
- [Cast gauge lifecycle](cast-gauge-lifecycle.md)
- [Status parameters and party buffs](status-parameters-party-buffs.md)
- [MonsterAttackWeaponSkill getter profile](monster-attack-weapon-skill-profiles.md)
- [Monster map-marker selection](monster-map-marker-selection.md)

## Quests and events

- [Content director UI contracts](content-director-ui-contracts.md)
- [Guildleve journal lifecycle](guildleve-journal-lifecycle.md)
- [Hamlet supply and score UI](hamlet-supply-ui-contract.md)
- [Raid object client contracts](raid-object-client-contracts.md)
- [Quest event client contracts](quest-event-client-contracts.md)
- [Quest reward Notice helper](notice-helper-contract.md)
- [Quest scene literal and replay-row joins](quest-scene-replay-joins.md)
- [Seasonal quest client contracts](seasonal-quest-client-contracts.md)
- [Seasonal event actor contracts](seasonal-event-actor-contracts.md)
- [Quest selector consumers](quest-selector-consumers.md)

## Travel and world objects

- [Chocobo mount script contracts](chocobo-mount-script-contracts.md)
- [Area-base client initialization](area-base-client-initialization.md)
- [Cutscene replay and skip contract](cutscene-replay-skip-contract.md)
- [Inn bed client hook](inn-bed-client-hook.md)
- [Dungeon exit client contracts](dungeon-exit-client-contracts.md)
- [Aetheryte list widget](aetheryte-list-widget-contract.md)
- [Aetheryte object events](aetheryte-object-event-contracts.md)
- [Map-object door client contract](map-object-door-client-contract.md)
- [Weather director client contract](weather-director-client-contract.md)

## Shops, items, and social UI

- [Gathering marker and fishing UI](gathering-marker-fishing-ui.md)
- [Grand Company shop lifecycle](grand-company-shop-lifecycle.md)
- [Gil-shop widget opening](gil-shop-widget-opening.md)
- [Materia removal client UI](materia-removal-client-ui.md)
- [Item-storage widget contracts](item-storage-widget-contracts.md)
- [Job and Grand Company event contracts](job-grand-company-event-contracts.md)
- [Loot item UI contract](loot-item-ui-contract.md)
- [Party matching client contract](party-matching-client-contract.md)
- [NPC Linkpearl client route](npc-linkpearl-client-contract.md)
- [Parley target gate](parley-target-gate.md)
- [Player trade lifecycle](player-trade-lifecycle.md)
- [Retainer widget results](retainer-widget-results.md)
- [Reward and delivery widget results](reward-widget-result-contracts.md)
- [Market search and bazaar client contracts](market-search-bazaar-client-contracts.md)

## Repository policy

- [Repository style](style-guide.md)
- [AI-assisted contributions](ai_agents/README.md)
- [Comments and prose](ai_agents/comments-and-prose.md)
- [Evidence and claims](ai_agents/evidence-and-claims.md)
- [Retail-input validation](ai_agents/retail-input-validation.md)

`tools/validate_corpus.py` checks that the local Markdown links listed here exist.
