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

## Man2 city scenario composite scenes

The following installed `client/script/tp5rq/r75w9s1v/x9w/` resources
match the corpus inventory. Each independently recovered Lua body is
identified separately so its decompiler output is not silently treated as
canonical source:

| Script | LPB file / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `Man2g0` | `x9wh3j.le.lpb` / `fc3f5a0bcc7f39dc530da10ef6ef96d11d6081d5b4ea1557df0b011a7df58844` | `861ceddbc33b6c4b381ec9e47fa0446011a0740ce495ffab4ed1288ee436b831` |
| `Man2l0` | `x9whyj.le.lpb` / `b4054e097797215c92ef1096c1c8c055490d08355e4ca8c4ce27caa9bf3b60c0` | `3508e22978b017c4a9bcea9cb48e45b39b3f0c94a9e6f0823b77dfc1e931c0f0` |
| `Man2u0` | `x9whpj.le.lpb` / `deed0213ddd0c57edb09dd9a7ff216769658c3a710142bb036fcb597a9149992` | `9843a8314d1a32a116a2e7192888626b6043c239937f89ad4b5d627118e562ab` |

`Man2g0.processEvent007_2` presents ask row 240, and its recovered
answer-1 branch plays HQ scene `man2g000`; the sibling
`processEvent007_2_2` has the ask and fades but no scene call.
The decompiled return expressions repeat `ask`, so the exact number of
runtime prompts and returned value should not be inferred from this output.

`Man2l0.processEvent020` calls NQ `man2l020` with its fourth method
argument, then HQ `MAN2L030`, then NQ `man2l040`, ending with a post-warp
fade-in. `processEvent081` similarly chains NQ `man2l081`, HQ `MAN2L090`,
NQ `man2l100`, and NQ `man2l110`. `Man2u0.processEvent005` chains NQ
`man2u000`, NQ `man2u010`, and HQ `MAN2U020`; `processEvent085` chains NQ
`man2u085`, HQ `MAN2U090`, NQ `man2u100`, and NQ `man2u110`. These are
client presentation sequences, not evidence of server-side duty state,
combat objectives, scene-trigger ownership, or reward timing.

## SimpleQuestBattle client give-up hook

The recovered `SimpleQuestBattleBaseClass.eventContentGiveUp` returns
`worldMaster:ask(self, worldMaster, 25230, 2, argument)`; its
`getOwnClientQuestId` delegates to `getOwnClientQuestIdAsSimple`.
The base implementation of the latter has no recovered return value.
Three recovered child overrides return exact client quest IDs:

| Child class | `getOwnClientQuestIdAsSimple` return |
| --- | ---: |
| `QuestDirectorCom0l601` | `111406` |
| `QuestDirectorCom0u501` | `111805` |
| `QuestDirectorEtc3g201` | `110736` |

The installed LPBs are under
`client/script/61s57qvs/tp5rq/r1xuy5tp5rq89qqy5/`. Their file
SHA-256 values, followed by the independent recovered-Lua SHA-256, are:

| Class | LPB file | LPB SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- | --- |
| Base | `r1xuy5tp5rq89qqy589r57y9rr.le.lpb` | `cb4981bdeb1ecc4bbad4132896bc90b1eeb31eda35c244550304cfc60ff4e190` | `b4b352644bee4aed8936e0e86b7d17e9c2ab8f80b604f9a7c0058b9e9e3254ec` |
| `Com0l601` | `tp5rq61s57qvs7vxjydji.le.lpb` | `3c2f349d571fb038d12b3b7199f28339bd533e1e4b0eb9d4fd5dd2832fb04b57` | `d5a0faf159fe00851482c08a304fe5cba64437984545d4f682e4496f64333de9` |
| `Com0u501` | `tp5rq61s57qvs7vxjpeji.le.lpb` | `ed295a0c3d308a52003e63d67e36219979541cfafc9ef908f0d1b20ac69f0f4e9fe` | `1666578956a9d3eb8df42adb3a169ffdcb8e8d08d6568b76c84902184d8d74a5` |
| `Etc3g201` | `tp5rq61s57qvs5q7g3hji.le.lpb` | `c88450a2d59bc94c81437a2e4bf149826bcabbfbf8c11f35d0d0765d90a6ad27` | `a563117f80b6cb686c65ff62afce8819fcad2b04e32dbaa03cb4ce05464673b3` |

This authenticates a client ask route and three override constants. It
does not establish a server give-up transaction, cancellation semantics,
battle spawn, kill callback, cleanup, or reward policy. The recovered base
does not define `eventContentCancel`; absence of that method in this file
does not prove there was no other retail cancellation path.

## Man0 opening tutorial boundaries

The installed scenario LPBs under `client/script/tp5rq/r75w9s1v/x9w/`
match the corpus inventory. The exact resource and independent recovered-Lua
SHA-256 identities are:

| Script | LPB file / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `Man0g0` | `x9wj3j.le.lpb` / `0180a8e3c55086b1b0c5cf2c17a7907846ce0b8854fb540bae57298b6f03a8e5` | `ababe7bb21455dbe2be5cd8abdb3e374a5366079b73de5f5829d209dba632836` |
| `Man0l0` | `x9wjyj.le.lpb` / `30352866fca599cd199263e3e8253472c4230509c1e2b8c2755506690563f4ec` | `e28fe6ed28e7c3a8bbce3bae44285b173b5b612d0f0dcaaa1022836e152ee7ac` |
| `Man0u0` | `x9wjpj.le.lpb` / `b954f9735da9ef38401872562074482ffeb510da44441febaa4fba959052f0cc` | `c7c1a3c51df28dac202bc4742349feb85b0d3a60dad376eb433645157dd700c6` |

`Man0l0.processEvent000_2` cancels desktop-widget mode 16, closes the
tutorial widget, and orders mode 16 again; it does not launch a scene.
`processEvent020_9` presents ask row 84 with mode 2 and places a fade-out
only in the recovered answer-1 branch. Its decompiled return expression
repeats `ask`, so the number of runtime prompts and returned value remain
unresolved. `Man0u0.processEvent000_3` delegates to
`_getTutorialJudge():man0u0processEvent000_3`, while
`processEvent020_8` returns the corresponding tutorial-judge method's
result. `Man0g0.processTtrBlkNml002` has an empty recovered body.

These scripts identify presentation and delegation only. They do not
authenticate the contributor server's content spawns, kill counts, return
warps, quest replacement, or reward grants.

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
