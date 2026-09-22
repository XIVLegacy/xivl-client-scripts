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

## Man1 city scenario cutscene calls

Three installed scenario LPBs match the corpus resource inventory. The
independently recovered Lua bodies have these SHA-256 identities and direct
cutscene calls:

| Script | Installed `client/script/` resource SHA-256 | Recovered Lua SHA-256 | Direct call boundary |
| --- | --- | --- | --- |
| `Man1g0` | `tp5rq/r75w9s1v/x9w/x9wi3j.le.lpb` / `4c95deb83f772036b0900487a8cf87ac7a50e07f583091d97b1de18e5647ecde` | `c0eb238c1f5130bf79a199422bffec5d2d03776e8b7c641c33ed8d9f08ef5eaf` | `processEventMiounneStart` calls `man1g000`; `processEvent010` through `100` call the corresponding `man1g010` through `man1g100` scenes. |
| `Man1l0` | `tp5rq/r75w9s1v/x9w/x9wiyj.le.lpb` / `f24c0974a756ec03519531fae4d73d54c2d691386bf37a137365b06ce791d228` | `3059770f183722e6a07b9b1f3d1d455cf425a41ac32728340b34d8c70ce183c1` | `processEvent200/210/215/400/410/420/600/610` call matching `man1l` scenes; `processEvent2000/2001/2002` call `man2l000/001/002`. |
| `Man1u0` | `tp5rq/r75w9s1v/x9w/x9wipj.le.lpb` / `98f0094d3f32c1535c500db24330dd488be4a77b006e2e197ab9cc01294ebe51` | `62598c9ea22c8dec54d581e4d35d50ec6c89d97cd72bcf6937b50b0ec4f62b79` | `processEventMomodiStart` calls `man1u000`; `processEvent010/020/021/030/040/050/060/070/080/090` call matching `man1u` scenes. `processEvent100` is dialogue-only in the recovered body. |

In `Man1l0`, `processEvent610` passes its fourth method argument to
`startNQCutScene("man1l610", 1, true, arg)`. `processEvent2000` instead
passes the literal `11000002` to `startNQCutScene("man2l000", 1, 0,
11000002)`. The `man2l` names here are calls from the `Man1l0` client
script; they do not transfer quest ownership or establish a server sequence.
Likewise, scene-call presence does not identify the invoking actor, private
area, progression gate, reward, or historical retail activation path.

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
