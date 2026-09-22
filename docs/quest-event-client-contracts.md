# Quest event client contracts

The recovered 1.23b Lua corpus preserves client-side event presentation for a
small set of scenario, class, job, and Grand Company quests. A reproducible
decompile of the decoded chunks matched the canonical corpus byte-for-byte
after CRLF-to-LF normalization. The machine-readable source identities,
hashes, locators, and claim boundaries are in
[`quest_event_client_contracts.json`](../manifests/quest_event_client_contracts.json).

## Scenario and class quest presentation

`Pgl200` contains the client event dispatch for the selected Pugilist scenario.
Its event methods call the recovered cutscene helpers, including the normal
fade-out, NQ cutscene, fade-in, and post-warp fade-in paths. The script also
contains the client ask route used before duty entry. These methods establish
the presentation and local event sequence, but not server eligibility, duty
formation, objective state, or rewards.

`Com0l1`, `Com5l0`, and `Gcl101` similarly preserve direct event, dialog, ask,
and cutscene flows for their selected common and Grand Company scenarios.
`Com5l0` also consumes a member-count value. That consumption does not prove
the server-side membership rule or identify the authoritative source of the
value.

## Job quest presentation

`War0j1`, `Mnk0j6`, `Blm0j3`, and `Whm0j6` define client event and hint
handlers. The recovered bodies include cutscene transitions, public-information
dialogs, clear paths, and, where present, item or artifact presentation. They
authenticate those client UI and event calls only. They do not authenticate
quest eligibility, objective counts, party formation, item ownership, or reward
granting.

## Empty Man scenario boundary

`Man502` and `Man504` define their classes and initialize text. Their paired
`QuestDirectorMan50201` and `QuestDirectorMan50202` scripts only define empty
director classes. This evidence contains no progression, objective, reward, or
scene implementation for those directors. The empty bodies are a negative
boundary, not evidence that the retail server had no corresponding behavior.

## Evidence boundary

The decoded chunks and the pinned decompiler establish the recovered client
scripts listed in the manifest. They do not establish server templates,
authoritative routing, objective completion, rewards, or seasonal variants.
Those claims require separate evidence and remain unresolved here.
