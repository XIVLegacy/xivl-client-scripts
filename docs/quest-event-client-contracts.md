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

`Alc200` has two separate scene wrappers that branch on their fourth method
argument. If it equals numeric 3, they pass 1 as the final scene argument;
otherwise they pass 2. Both use NQ mode 1 and a literal `true` before that
selected value:

| Method | Scene | Final fade-in |
| --- | --- | --- |
| `processEvent020` | `alc20020` | after-warp |
| `processEvent030` | `alc20030` | default |

The installed `client/script/tp5rq/r75w9s1v/9y7/9y7hjj.le.lpb` decodes
byte-for-byte to the recovered `Alc200` chunk (SHA-256
`cd2c07c7d4aa6e3a289a26aff300ee48c197d3a8199d3c820d28a150eede2313`).
The method locators are in `lua/scripts/quest/scenario/alc/alc200.lua`, with
the ciphered path in its `.calls.json` sidecar. The separate static replay
rows for these scene keys are recorded in
`xivl-client-data:docs/quest-replay-rows.md`. Neither the scene call nor the
replay rows identify the producer of the fourth argument, a quest objective,
or the historical event dispatcher.

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

## Man200 scenario presentation lead

The installed `client/script/tp5rq/r75w9s1v/x9w/x9whjj.le.lpb` has SHA-256
`dfb750ed666d1100b5940751c9d658c4537b3f6d51e44cbc153660c4500ffeaf`.
Decoding its 13-byte `rle` wrapper and XOR `0x73` payload matches the
recovered `quest/scenario/man/man200.luac` byte-for-byte (SHA-256
`8b9d472804dbbff2a2fa4397cd91d9514593a991febccaf259e6fdbdf9101ca3`).
The recovered `Man200.pE00` at
`quest/scenario/man/man200.lua:6-15` calls SNPC NQ scene `man20100`
between a default fade-out and an after-warp fade-in. `pE25` at lines
236-250 shows an ask-gated `man20130` scene path, but its repeated `ask`
in the decompiled return is not a verified second prompt. These client
presentation leads do not identify the historical event caller or server
progression.

`Man200.processSnpcSelect` at recovered lines 329-470 maps ask row 77
choices 1-5 to offsets 1, 17, 33, 49, and 65, adds 1070000, and passes
the resulting base ID to `getSnpcCandidacyNumber`. The resulting bases
are 1070001, 1070017, 1070033, 1070049, and 1070065. Other answers
return `(-1, -1)` in the recovered method. Its decompiled scene-choice
branch repeats `startNQCutScene("man20140", ...)`, so that text does not
establish a repeated playback count or the exact candidate-selection
algorithm. These IDs are client selection inputs, not proof of spawning,
persistence, or a server-side class/personality mapping.

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
The installed `Man2g0` LPB decodes byte-for-byte to the recovered chunk
(SHA-256 `b51e16fd99459eed9271d9f02396b3a2ec307b6d0a0846dd0d5219812c991645`).
The bytecode calls `ask` once in each method (`0x0D83` and `0x0EFB`),
branches on the saved answer, and returns it (`0x0DBF` and `0x0F27`).
The repeated `ask` in the decompiled return expressions is a rendering
artifact, not a second prompt.

The same recovered `Man2g0` body has these later direct presentation calls:
`processEvent010` fades out, plays NQ `man2g010`, then uses the post-warp
fade-in; `processEvent020` plays NQ `man2g020` between default fades;
`processEvent070` plays NQ `man2g070` with a post-warp fade-in; and
`processEvent080` chains NQ `man2g080`, HQ `MAN2G090`, NQ `man2g095`,
and NQ `man2g100` before a post-warp fade-in. These calls are at recovered
`quest/scenario/man/man2g0.lua` lines 55-69 and 316-337, under the
installed LPB and recovered-Lua identities above. They do not identify the
server event caller, prove which scene followed a retail combat result,
or establish an instance or zone transition.

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
only in the answer-1 branch. The installed `Man0l0` LPB decodes byte-for-byte
to the recovered chunk (SHA-256
`19a7ef9877a314ed296a918aea709c57b2cf89b6f46a543c17d51a8e29df17a1`).
Its bytecode calls `ask` once at `0x1AF2`, branches on that saved result at
`0x1AFE`, and returns it at `0x1B56`. The repeated `ask` in the decompiled
return expression is a rendering artifact. `Man0u0.processEvent000_3`
delegates to `_getTutorialJudge():man0u0processEvent000_3`, while
`processEvent020_8` returns the corresponding tutorial-judge method's
result. `Man0g0.processTtrBlkNml002` has an empty recovered body.

These scripts identify presentation and delegation only. They do not
authenticate the contributor server's content spawns, kill counts, return
warps, quest replacement, or reward grants.

## Com0 instanced cutscene calls

The installed LPBs under `client/script/tp5rq/r75w9s1v/7vx/` match the
corpus inventory. Their resource SHA-256 values and the separately recovered
Lua SHA-256 values identify the six bodies used here:

| Script | LPB file / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `Com0l5` | `7vxjye.le.lpb` / `faebd6c76c4a01f50322d90f3f44e2ba05a7485e91893824a5f5bc7de88e558a` | `3be06e417323cbea89d1b42ec9ddcbb0e8c0fb02c6c258852d9d71b484e3552b` |
| `Com0u5` | `7vxjpe.le.lpb` / `6b8b7b874c10f25703706a34a927d528c538cdeeecee06d1182b7bc09293ac86` | `f6b925d3230fa4731b2664b754f01c8e44ffc8284207ce1eeef7c184fa17c3ff` |
| `Com0g6` | `7vxj3d.le.lpb` / `3400a351ec43fc8bbcb7b2c936a072b53db056858f12815cd820326d80307b45` | `e6cccde10118dffdf15cfe30a49650fd84e611e3a71b09f9b6f21b564692ed7c` |
| `Com0l6` | `7vxjyd.le.lpb` / `59e7af49138f282a8764f8282ddf65169e39872c54c610679a8ca4b0435cc301` | `f8bd6cacdac222e0889867f83049fb2852dd5909783391ff2f8a856924789d32` |
| `Com0u6` | `7vxjpd.le.lpb` / `52efcfcd3a8bb1c949654052efe00307ace4945a2d1de662e14367fba64881dd` | `ab508f6688aea592f236a1a1be4031c8a0f0c35a449bdaec51cfb25e738a5958` |
| `Com0g4` | `7vxj3f.le.lpb` / `7d6af2a009754c16d5916a1e9eaaea5dfcf3b858ba6ac3837ce2d64cb3620a77` | `926430d8e0fa3e41bf541b1939b7266bccee7e2b389c0f37270904fb3cf17715` |

`Com0l5.processEvent_010` calls NQ `COM0l110` and a post-warp fade-in.
Its `processEvent_elevator_nq1` presents ask row 79, mode 2; the
recovered answer-1 branch calls NQ `elv0l110` then `com0l610` and fades
in after warp. The sibling `processEvent_elevator_nq2` calls only
`elv0l110` in that branch. `processEventExit` asks world-master row
51036, mode 2. Both elevator return expressions repeat `ask`. The
installed `Com0l5` LPB decodes byte-for-byte to the recovered chunk
(SHA-256 `aa2b2d66bb19ddcb881644506580c7f6becedc18a0d448fcd8a23e42ceaaa4d1`).
The bytecode calls `ask` once in each elevator method (`0x14F8` and
`0x16D8`), branches on that saved answer, and returns it (`0x1564` and
`0x1730`). The repeated decompiled return expression is not a second
prompt.

`Com0u5.processEvent025` calls NQ `com0u610` with a post-warp fade-in.
`Com0g6.processEventNq` calls NQ `COM0G510` with default fade-out and
fade-in.
`Com0l6.processEvent_010` passes its fourth method argument into NQ
`com0l510` as the fourth scene argument. `Com0u6.processEvent_005_03`
does the same for NQ `com0u510` and then fades in after warp.
`Com0g4.processEventClear` calls NQ `com0g410` only when its fourth
and fifth method arguments are both zero; the other recovered branch
is dialogue. These direct calls do not identify the server-side event
owner, instance start, quest sequence, clear condition, or reward.

## Man0l1 cutscene preview gap

The installed
`client/script/tp5rq/r75w9s1v/x9w/x9wjyi.le.lpb` has SHA-256
`0e6c6fd091123137d8b37dcb42f7f36b66de8acc73019cd6ac2c17884cedbe8a`.
The independently recovered
`tools/outputs/lpb/decomp_more_20260617/lua/quest/scenario/man/man0l1.lua`
has SHA-256
`24f486e6c9249e90397caad137665548e7219df9590344a6240d51a9140efeeb`.
In `Man0l1.processEventTalkMenuManCutPreview`, the recovered selection-7
branch calls `startNQCutScene("man0l420", 1)` between default fade-out
and fade-in calls.

The installed `client/cut/` tree has 690 immediate scene directories,
including other `man0l*` scenes but no `man0l420` directory. The freshly
extracted canonical `cutReplay.csv` (SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`)
also has no `man0l420` text match. These are bounded installed-asset and
replay-table absences. They do not prove that the menu branch was reachable
in retail, that another asset source was unavailable at runtime, or that a
replacement scene should be invented.

The independently generated
`tools/outputs/lpb/quest_cutscene_bridge_contract_20260619/quest_scene_key_gap_contract.csv`
(SHA-256
`4368f51e2e1e44d0ec71b6c7177b637e2bfa0ac7db79278fd33d4824ebfb5a91`)
lists 31 direct-scene keys without a `cutReplay` row. A fresh text-match
check against the canonical CSV found none of those keys; an installed
`client/cut/` directory check found 30 matching scene directories and
the one missing `man0l420` directory above. The 31 keys are:

`bsm40020`, `bsm40030`, `bsm40040`, `bsm40045`, `bsm40050`,
`cul40010`, `cul40020`, `cul40025`, `cul40030`, `elv0l01a`,
`elv0l02a`, `elv0l110`, `elv0u01a`, `elv0u02a`, `fsh40010`,
`fsh40020`, `fsh40030`, `fsh40040`, `fsh40050`, `fsh40060`,
`man0g225`, `man0g230`, `man0l420`, `man0l640`, `man0l650`,
`man0u235`, `man0u240`, `man20140`, `man20155`, `man40645`,
and `wpn0f010`.

This list is a bounded replay-table gap, not a claim that direct playback
fails, that retail offered replay for those scenes, or that adding rows is
safe without the original replay metadata.

## Man206 scene and return branches

The installed `client/script/tp5rq/r75w9s1v/x9w/x9whjd.le.lpb` has SHA-256
`1f84e4a0948599dad65b06efca478b92ce9c62d8e3074dbd6cf3f7ec7b9552f9`.
Its 13-byte wrapper and XOR `0x73` payload decode byte-for-byte to recovered
`quest/scenario/man/man206.luac` (SHA-256
`0461fc2def0f392fa0e952a4557ab1421ba96302d1192f1ae4456ac929c9af71`);
the recovered Lua rendering at `quest/scenario/man/man206.lua` has SHA-256
`787e91bbb985c045682848151b70c20448f31f2601dd8814a6dbf0295ff5d067`.

| Method / recovered-source lines | Direct client operation |
| --- | --- |
| `processEventUdowntownrectStart`, 6-10 | Calls NQ `man20600` in mode 1 and fades in after warp. |
| `processEvent001`, 58-66 | Calls NQ `man20601` in mode 2; result 1 selects after-warp fade-in, other results default fade-in. The bytecode has one scene call at `0x0E7B`, then returns its saved result at `0x0EA3`. |
| `pE12`, 133-138 | Converts its second scene payload through `getSnpcActorClassID`, calls SNPC NQ `man20602` in mode 1, then uses default fade-in. |
| `pE13`, 173-183 | Converts its second scene payload, calls SNPC NQ `man20603` in mode 2; result 1 selects after-warp fade-in, other results default fade-in. The bytecode has one scene call at `0x1E0B` and returns its saved result at `0x1E23` or `0x1E37`. |
| `processEvent016`, 184-188 | Calls HQ `MAN20610` in mode 1, then uses default fade-in. |
| `pE20`, 204-209; `pE30`, 215-220 | Convert the second scene payload and call SNPC NQ `man20620` and `man20630` respectively in mode 1. `pE20` uses default fade-in; `pE30` uses after-warp fade-in. |
| `processEvent040`, 262-266 | Calls NQ `man20640` in mode 1 and fades in after warp. |

The decompiled return expressions in `processEvent001` and `pE13` repeat
their cutscene calls, but the underlying Lua 5.1 instructions call each scene
only once. The extracted canonical `cutReplay.csv` rows `11001401` through
`11001408` name `man20600`, `man20601`, `man20602`, `man20603`, lowercase
`man20610`, `man20620`, `man20630`, and `man20640` respectively
(`xivl-client-data:manifests/tables.json`, `csv/cutReplay.csv`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`).
The script's uppercase `MAN20610` key and replay row's lowercase key must
not be silently normalized into a proven runtime alias. These methods and
rows do not establish the invoking actors, duty lifecycle, quest sequences,
server rewards, or historical scene playback.

## Man300 SNPC cutscene arguments

The installed
`client/script/tp5rq/r75w9s1v/x9w/x9wgjj.le.lpb` has SHA-256
`43f4e01434a77290ada4ccda6c259afe669af0ae39063a983e85c264e31e4d9b`.
The independently recovered
`tools/outputs/lpb/decomp_more_20260617/lua/quest/scenario/man/man300.lua`
has SHA-256
`5a82d35f669314e3e10631d01221561cc9bb007b5ab864a633d0f4deb373b608`.
After its 13-byte wrapper and XOR `0x73` payload decoding, the installed LPB
matches the recovered Lua 5.1 chunk byte-for-byte (decoded SHA-256
`ccf8cd853c3aa6568e05ddfe702b42ac97a041783d5ec3b549203c7b6d7cf95f`).
`processEvent000` calls NQ `man30000` with mode 1 between default fade-out
and after-warp fade-in (recovered source lines 6-10; bytecode offsets
`0x0866..0x088E`). `processEvent010` has the same shape for NQ `man30010`
(source lines 102-106; offsets `0x1518..0x1540`). The extracted canonical
`cutReplay.csv` rows `11001501` through `11001507` name `man30000` through
`man30060` in order; row `11001506` carries literal `10` in its replay
payload (`xivl-client-data:manifests/tables.json`, `csv/cutReplay.csv`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`).
Replay-row order and method bodies do not establish the historical server
event owners, invocation order, or zone-change lifetime.
The `Man300` class defines five `pE*` wrappers for SNPC NQ cutscenes:

| Wrapper | Scene | Additional visible branch |
| --- | --- | --- |
| `pE20` | `man30020` | After-warp fade-in |
| `pE30` | `man30030` | Sixth method payload selects default fade-in when true, otherwise after-warp |
| `pE40` | `man30040` | Default fade-in |
| `pE50` | `man30050` | Sixth method payload is forwarded to the scene call; after-warp fade-in |
| `pE60` | `man30060` | After-warp fade-in |

Each wrapper converts its second method payload through
`getSnpcActorClassID` before forwarding it as the second scene payload.
All five scene calls forward five method payloads, with `pE50` forwarding
one more. Those are argument shapes, not recovered values or meanings for
the other slots. The contributor's proposed nickname, skin, personality,
coordinate, and town tuple is a server-side candidate; this client body
does not establish that tuple or an actor owner for any wrapper.

## Man304, Man308, Man402, and Man406 scene wrappers

The installed LPBs for these four scenario classes were decoded through their
13-byte `rle` wrappers (XOR `0x73` payload); each decoded byte matched the
corresponding recovered Lua 5.1 chunk. A bytecode trace executes scenario
instructions against inert API result fixtures, not a retail runtime.

| Class | Installed LPB beneath `client/script/` | LPB SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- | --- |
| `Man304` | `tp5rq/r75w9s1v/x9w/x9wgjf.le.lpb` | `193f30b822c5beb9bf1652f38f29583da3e3a4e2551563f7874825e947c749a8` | `c8a0fbc6eeeafa1b1e148c73139f290e883ca86c2a413900d38cf4a9cd7d8280` |
| `Man308` | `tp5rq/r75w9s1v/x9w/x9wgjb.le.lpb` | `1a2128960ac57b68c5030e6f98666fbd5347d1f1233b0912cb48dd89366c6730` | `3ccdc300df451ab52e45618cc2444ecdad0e0fd39062bcc1af82977929729e43` |
| `Man402` | `tp5rq/r75w9s1v/x9w/x9wfjh.le.lpb` | `c3e31e692dbf988ed2937a6f2d6e3bba49f47b13c212c53a5ac6caf01a3c971d` | `8794fa034cb6b5e61f1af9ca387d55af88296b3231db748d230eec142f50f76b` |
| `Man406` | `tp5rq/r75w9s1v/x9w/x9wfjd.le.lpb` | `a2ea85d17545a44a097145489dc80f164acf6b8c6e8644f19fcffe84d4dda289` | `c6415866f54ae206230f1d245b20c65b0146cae1ab3be99c37b2d1e314a129ad` |

The installed scenario bodies make these additional selected `say` calls:

| Method group | Literal text row IDs passed to `say` |
| --- | --- |
| `processEvent000_2..processEvent000_13` | `469..480` |
| `processEvent001_2` | `304` |
| `processEvent001_3..processEvent001_6` | `481..488` (two consecutive IDs per method) |
| `processEvent005_1`, `processEvent005_2` | `505`, `504`, respectively |
| `processEvent010_2..processEvent010_8` | `459..468` |

In `Man308`, `pE00` passes rows `357..383` to `say`. The separate
`processEvent090` method calls `startNQCutScene("man30890", 1)`;
`processEvent090_1..processEvent090_14` pass rows `600..622` to `say`.
In `Man402`, the methods `processEvent000_1`, `processEvent000_2`, and
`pE03` pass rows `108..113`; `processEvent000_4..processEvent000_6`
pass `114..119`; `processEvent020_1`, `processEvent020_2`, and `pE23`
pass `120..125`; and `processEvent020_4..processEvent020_6` pass
`126..131`. `processEvent000_7` separately passes row `250`.

These are literal client method calls in the pinned chunks above. Their
presence does not establish that a server route invokes them, that the rows
are reachable in a historical quest, or what localized text was displayed.
The 1.23b `cutReplay.csv` values for Hamlet are cataloged in
`xivl-client-data:docs/quest-replay-rows.md`; the Hamlet item and quantity
rows are cataloged in `xivl-client-data:docs/hamlet-supply-rows.md`.

Verification: the three LPBs above were decoded with
`xivl-client-structs:tools/decode_lpb.py`; each decoded chunk SHA-256 matched
the hash in the table. The source view was produced with the bundled
`unluac_2025_12_23.jar` (`tools/vendor/unluac/PROVENANCE.json`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`).

The independently decoded `quest/questbaseclass_common.luac` also matched
installed `client/script/tp5rq/tp5rq89r57y9rr_7vxxvw.le.lpb`
(`sha256=ecc3f7c6fb49df196431494aa5aece95ede1c24ca1325af11ddc993a3836322d`)
byte-for-byte after wrapper decoding and has SHA-256
`9379ee6832bdfa542273c7f43f065d7a15f9a730d9ef244be9a565a1faa53504`.
Its `getSnpcActorClassID` bytecode adds `1070000` to the input at offset
`0x1195`; its `startSnpcNQCutScene` forwards the scene's second payload
through to `startNQCutScene` at offset `0x0CAD` without that conversion.
These are client-side argument operations, not a server payload definition.

| Wrapper and bytecode locator | Direct client operation |
| --- | --- |
| `Man304.pES`, offsets `0x05A3..0x0697` | Converts its second payload, fades out twice, maps personality values 1-9 to `1,1,2,2,3,3,4,5,1`, calls SNPC NQ `man30400` in mode 2 with literal extra values 5 and 10, fades in, and returns the saved scene result. The two literals have no established gameplay meaning. |
| `Man308.pE50`, `0x1862..0x18EA`; `pE80`, `0x1AED..0x1B5D` | The former calls SNPC HQ `man40640` before SNPC NQ `man30850`; the latter calls SNPC NQ `man30880` before `man30890`. A scene key crossing quest-name families is not an error to normalize away. |
| `Man308.pE90`, `0x24D9..0x2515` | Calls SNPC NQ `man30900` and forwards incoming R4 to the scene's second payload without calling `getSnpcActorClassID`, then fades in after warp. An already-converted actor class is required if that scene slot is intended to hold one. |
| `Man402.pES`, `0x0352..0x03FA` | A numeric offer result of 1 calls SNPC NQ `man40200` and returns the saved scene result; the decline branch returns the offer result. Both paths return before the trailing `finishCliantTalkTurn` instructions. The scene's second payload is forwarded without class conversion. |
| `Man402.pE10`, `0x052C..0x0580` | Converts incoming R4 through `getSnpcActorClassID` and forwards incoming R8 twice at the end of the `man40210` scene call. |
| `Man402.pE20`, `0x0636..0x0682`; `pE30`, `0x0738..0x0784` | Both convert incoming R4 through `getSnpcActorClassID` and call SNPC NQ in mode 1 with incoming R3/R5/R6/R7 otherwise forwarded. `pE20` calls `man40220` and uses default fade-in; `pE30` calls `man40230` and uses after-warp fade-in. |
| `Man406.pES`, `0x066B..0x06D3` | Converts incoming R4 through `getSnpcActorClassID` and calls SNPC NQ `man40600` once in mode 2. Saved scene result 1 selects after-warp fade; other results select default fade. It returns the saved scene result, not a second playback. |
| `Man406.pE30`, `0x1D44..0x1DC4` | Calls SNPC NQ `man40630`, SNPC HQ `man40635`, and plain NQ `man40645` in that order before after-warp fade-in. |
| `Man406.pE50`, `0x2231..0x2281`; `pE60`, `0x25AC..0x25F8` | `pE50` forwards incoming R7 twice to `man40650`. `pE60` calls `getSnpcSexualityToSkin` on incoming R5, forwards R4 unchanged to `man40660`, and then fades in after warp; it does not call the class-conversion helper. |

The locators are decoded-chunk instruction offsets, not PE VAs. The direct
wrappers establish scene keys, call order, conditional returns, and payload
provenance only. The sampled trace domain does not establish original server
owners, quest sequence, battle orchestration, reward rules, or visible playback.

## DftSrt travel scene wrapper

The installed
`client/script/tp5rq/r75w9s1v/6549pyqq9yz/64qrsq.le.lpb` has
SHA-256
`989d8f897dbe769090ef7d90eb35fbe4b061ef2314bba24be23d85c4bea729b6`.
The independently recovered
`tools/outputs/lpb/decomp_more_20260617/lua/quest/scenario/defaulttalk/dftsrt.lua`
has SHA-256
`9607626c04f19ad4be53ee433872b43adf3ee0f52789a94d83dac4db30cbaa0a`;
its decoded bytecode has SHA-256
`72762bfbe567a34af198bcf342f42581e2ce83abb65a46a034a5472fe35a17e7`.
The `eventDeparture` bytecode confirms this order: fade out the local
player; call `startNQCutScene` on the method's fourth argument with mode
1; call it again on the fifth argument only when that argument is nonnull;
then fade in after warp. The method does not hardcode either installed
`vsl*` scene key, a route, destination, or server event owner. Its optional
second scene argument is not proof of an arrival movie or of historical
two-scene ferry playback.

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

The separate common `QuestBaseClass.snpcPreviw` method selects a scene for
client quest ID `110020`: its preview-index-1 branch and fallback both load
`man50250` (decoded bytecode offsets `0x1D94..0x1DAC`). It converts the second
scene payload with `getSnpcActorClassID`, then dispatches this key through
`startSnpcHQCutScene` (offsets `0x1E0C..0x1E14`). The recovered method is at
`quest/questbaseclass_common.lua:397-480`; its installed LPB and decoded-chunk
identities are given above. This is a common client preview route, not a
`Man502` event method or proof of quest progression. It supplies no `Man504`
preview route.

## Man0u1 scene and talk calls

`Man0u1.processEvent035` fades out, calls `startNQCutScene("man0u135", 1)`,
then fades in after warp (`quest/scenario/man/man0u1.lua:242-246`; decoded
bytecode offsets `0x3033..0x305B`, scene-key load `0x3043`, call `0x304B`).
The installed `client/script/tp5rq/r75w9s1v/x9w/x9wjpi.le.lpb` has SHA-256
`1b049927bc315982ab85edecf763a26f0242398de3986ad8252d26242a732bc4`;
after its 13-byte wrapper and XOR `0x73` payload decoding, it matches the
recovered chunk byte-for-byte (SHA-256
`955e51d95f942c1763a5e34c7d111380891ade2c7f34c2e7a50a68f47697a83d`).
The extracted `cutReplay.csv` row `11001005` also names `man0u135`
(`xivl-client-data:manifests/tables.json`, `csv/cutReplay.csv`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`).
That replay row and this method do not establish a post-fight trigger,
invoking actor, server event owner, or historical execution of the scene.

The same recovered `Man0u1` body has separate `processEvent075` and
`processEvent080` wrappers for NQ `man0u175` and `man0u180`. Each uses a
default fade-out and post-warp fade-in around its scene call
(`quest/scenario/man/man0u1.lua:474-483`). `processEvent080_2` through
`processEvent080_12` are separate talk methods, not part of the `080`
scene wrapper: they say rows `160-163`, `358-364`, and `377`
(`man0u1.lua:484-537`). `processEvent090` then calls NQ `man0u190`,
another default fade-out, NQ `man0u200`, and a post-warp fade-in
(`man0u1.lua:538-544`). The recovered Lua SHA-256 is
`db6e32d8c4ff849d02ea2ccdc12b14b24b8bdf40c50af5f75d8511f106603cec`;
the installed LPB identity and decoded-chunk match are given above. These
methods do not prove the retail caller, quest sequence, escort completion
rule, historical private-area transfer, or timing of either scene.

## Evidence boundary

The decoded chunks and the pinned decompiler establish the recovered client
scripts listed in the manifest. They do not establish server templates,
authoritative routing, objective completion, rewards, or seasonal variants.
Those claims require separate evidence and remain unresolved here.
