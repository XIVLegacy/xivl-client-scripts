# Seasonal quest client contracts

The [Impish Impositions contract](impish-impositions-client-contract.md)
separately pins the canonical `Spl0i2` decompile and the retail quest/text joins.
The [Winter Is Not Coming snowman contract](winter-is-not-coming-client-contract.md)
pins the selected `Spl0i3` callbacks and related object initializers against
original bytecode, with their producer and server effects kept separate.

## Retail quest identities

The retail title and class joins below use `xivl-client-data` revision
`9ca24cf5aecd33c4f2753c0d75887ac6e96516cc`:
`csv/xtx_quest.csv`, row ID and column 2; the same IDs in `csv/quest.csv`;
and `manifests/staticactor_class_paths.json`, the record's class path.
CSV sheet columns start at zero after the row ID. Python `csv` checked the
selected rows from the decoded archive, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
The whole members matched `manifests/tables.json`, SHA-256
`239cb63fb00de5f434b92924696c043cb80ddcd9abc7f334075afb6b28d5626d`.
The staticactor class-path manifest has SHA-256
`d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.

| Retail English title | Quest ID | Class under `/Quest/Scenario/Spl/` |
| --- | ---: | --- |
| The Dreamer's Gospel (Gridania) | 110794 | `Spl0g1` |
| The Dreamer's Gospel (Limsa Lominsa) | 110804 | `Spl0l1` |
| The Dreamer's Gospel (Ul'dah) | 110789 | `Spl0u1` |
| The Dreamer's Dilemma (Gridania) | 110795 | `Spl0g2` |
| The Dreamer's Dilemma (Limsa Lominsa) | 110805 | `Spl0l2` |
| The Dreamer's Dilemma (Ul'dah) | 110790 | `Spl0u2` |
| Scrambled Eggs | 110859 | `Spl101` |
| The Heat Is On | 110799 | `Spl0i1` |
| Bombard Backlash | 110860 | `Spl102` |
| Impish Impositions | 110800 | `Spl0i2` |
| Winter Is Not Coming | 110801 | `Spl0i3` |
| Gone with the Snow | 110802 | `Spl0i4` |

Each class joins to the lowercased decoded path in
[lua/registry.json](../lua/registry.json) and the corresponding canonical member
in [manifests/scripts.json](../manifests/scripts.json), SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`.
The [Scrambled Eggs require and start contract](scrambled-eggs-start-contract.md)
owns the original-bytecode relationship between `Spl101` and `spl101_quest`:
the main chunk requires the supplement, which calls the class-definition
helper, before extending the global class. The staticactor record identifies
`Spl101`; these identity and loading joins do not establish event calendars,
NPC placements, event dispatch, rewards or a complete server quest flow.

## Independent decompile inputs

The `client/script/tp5rq/r75w9s1v/ruy/` LPBs below decode
byte-for-byte to the independently recovered Lua 5.1 chunks. The recovered
Lua bodies are a separate decompile from the canonical corpus recorded in
`manifests/scripts.json`; their text hashes do not match that manifest. The
claims below therefore cite the resource, matching decoded chunk,
and recovered method body, not a supposed match to the canonical Lua text.

| Decoded script | LPB basename / SHA-256 | Recovered Lua SHA-256 |
| --- | --- | --- |
| `quest/scenario/spl/spl0i1` | `ruyj1i.le.lpb` / `0e1a9f82c23094e4f5a42506f5ddff47acb7c742c4e4739a9d4d9f426863f34b` | `60fdeb1da8e58debeac792b7d471d5a2929aa02e3b8e24e3dae3cdcf454eeed3` |
| `quest/scenario/spl/spl0i2` | `ruyj1h.le.lpb` / `b30852b309ecb1f954dd220b7549ca5c22ec46f7091b3343e1e60d92a7c2caaa` | `f28563c147c15b2167d53f35c9b0782ddc43e6316c7f4080f2844b61c9f40482` |
| `quest/scenario/spl/spl0i3` | `ruyj1g.le.lpb` / `4a1867a9cb26c998215ec8fb352c27ac15e956fa8b9ef0ef252fd7be9f944546` | `021e73b280067f4281fad80076a39a21d360e813df835599c964a2f699224f1a` |
| `quest/scenario/spl/spl101` | `ruyiji.le.lpb` / `4000815dc1dedca9b6669530cc3ddfdca8250bca1be189b794102dd1ccc5fc4c` | `e8cc2c59e464456073eaf54babdcef0e7da44270bbe006bb124ba739ee57c394` |
| `quest/scenario/spl/spl101_quest` | `ruyiji_tp5rq.le.lpb` / `894febbf8c69a13e56e2e417a02b86eb7243bdec36268b4642f946c4adf0f511` | `1f44d96cadfc73260b7dcfa8eae0a41b07b33b881769ede1aaaade0938d86c76` |
| `quest/scenario/spl/spl102` | `ruyijh.le.lpb` / `cec1ba8009cd51d409d70812eeecc9a5f18c88fb6b323acefd28fffead520fe7` | `8b27941571513f6617bbef26f31b7aa65f1abad8dc58469d8fe5b3479b9d4f86` |
| `quest/scenario/spl/spl0g1` | `ruyj3i.le.lpb` / `c3b050d0a35973ee21b096a51eebf14079f6b250368c67f4eddcabc0a947f493` | `a728ef5c17fc17b517b5092c573586f09f3aa1781faef61cd1db32bf06a0932b` |
| `quest/scenario/spl/spl0g2` | `ruyj3h.le.lpb` / `bd717a5d07a482ac80a7aba47d16e55a456e55283e8df777404c625a11d7ac40` | `6a83d13f2919fee0ca8756e272ccb41151fcdfff3e0ac22e1fa975509d29a7a9` |
| `quest/scenario/spl/spl0l1` | `ruyjyi.le.lpb` / `228598b1f443f63c65d20da536f5e9dc67643b375cd152e330176d4f2e012b52` | `33c1038e2000cb1248ac6b81a803046a619d87fdd552f2b13b03f16c869d8399` |
| `quest/scenario/spl/spl0l2` | `ruyjyh.le.lpb` / `d58c1e5f4e5c5b48863bab9fb68fd986be37b621b4c9f7928ebfbc5c4cf643a7` | `85801e0423a1004ced0ce1ba298f83a02e71a5be2607a8005e34124790e3e22c` |
| `quest/scenario/spl/spl0u1` | `ruyjpi.le.lpb` / `df49007989ac4d1da9901af0cdbc1c7d8eaa28aa629249280379a22a1487ff63` | `da5bfa056b924f1eea4017e99407e58ba1c85ccde2eb24ebde7058e88e2dffed` |
| `quest/scenario/spl/spl0u2` | `ruyjph.le.lpb` / `5dd1748ea28ff472fd3372771b1316f90c49f12ecf5a7942565e10eb918f55f1` | `219b23ed558d762a5e1b101a5ec1f9cca0b59fc4b8622f81119373dccdd3a4a4` |
| `quest/scenario/spl/spl0i4` | `ruyj1f.le.lpb` / `e8b50d891cd63dbc03e394b4da543362ca0e1eeccc6fd09c60e1816b583b0777` | `b0d4014bedd3ef19b269ef252be1b83fe2a994137a10ad8b209404e06533c657` |
| `quest/scenario/spl/spl000` | `ruyjjj.le.lpb` / `ffa8b4b30c9e8444c8f7fc251aafdc7f2b9c62f87807a942eead2d3c5b6edd5f` | `5ef519bf31b09e37a7848c55aa6b69eeb382cd36d060d9a851c9a54370cc7070` |
| `quest/scenario/spl/spl0g3` | `ruyj3g.le.lpb` / `aa39836c95e95a7b3854fd5d75ca3e57d9a3abc3a68438a2f3ed3d76df7bf2c4` | `c8f091916e94fc2d2d523a59041227075a3f1155036ce7872d442c4041778d10` |
| `quest/scenario/spl/spl0g4` | `ruyj3f.le.lpb` / `1c3ebd5e0e149629971ba90f6515fa58d882867ab2009ddc6d8b4454e45dbe66` | `df9091b72c5dffc977f3b74fb7f090b745fa126bb113946366c5183994d17c1c` |
| `quest/scenario/spl/spl0g5` | `ruyj3e.le.lpb` / `dec9fb112267b509ed90b0a09db87a96257a0d6245322329fb08a62073155c47` | `c0c6b4ec4d9f22973400b64d7cfd9e13d00eac4e97362268e5345181cc61a20c` |
| `quest/scenario/spl/spl0i5` | `ruyj1e.le.lpb` / `66acbdc0f5b5b589920f8a633518e6cb684521a9c4c834ddd7cd0908cfacf957` | `0126d74914a30051dc09699a3b9595f62c1673a725cba5b920e14a2c0b1308d6` |
| `quest/scenario/spl/spl0l3` | `ruyjyg.le.lpb` / `5ba70863c9603cd745865c203dcf2dfcb9860ebf6fd7f01f64706995f9be4d33` | `3f68f77e7e3cbfa5caa3a578291dc9aea44bbdb1bea7607d9ec0777bb4342348` |
| `quest/scenario/spl/spl0l4` | `ruyjyf.le.lpb` / `e52d4d2265b7279b873dd672f2b691c11348eb6e1a265fcb8790b73372aaf924` | `7c2f9b0fcd4c694dd893dd1d82d7f93d46afa6bd0776c8e0c3a5bbd693ead951` |
| `quest/scenario/spl/spl0l5` | `ruyjye.le.lpb` / `c39b555489bd9111de6d9f43fa5cbe8f1e1cbb26c1474978135e07f42b5c528a` | `de6fb43f8e20e78f64f365d4fe8208bbf367421f543683fba90c164d64a0d24f` |
| `quest/scenario/spl/spl0u3` | `ruyjpg.le.lpb` / `b700092f5c64e87ad9fe0baaae601ae32a7fdc6ee48453da0570b7170cf8a906` | `6470bc1eb4ba4ee2e4a3e808483201751afc1524eb49bf2da7f351e618f988de` |
| `quest/scenario/spl/spl0u4` | `ruyjpf.le.lpb` / `2a74eaf45d4d594ddcc64e477d8219bd8686385e59a6e16ad40222eca850855a` | `ef7f5aad6fb05b29347569c4848f1e215923cde155f13456a87b80160eb5fa8a` |
| `quest/scenario/spl/spl0u5` | `ruyjpe.le.lpb` / `8c05410b04f80aeb348fdad5b68866abf05cea9cdf37e0f8a87124309af2be8e` | `f9679b51657ef7372a2367d8f979df3cc92534a4e2eff56eed43fd534c61a2a1` |
| `quest/scenario/spl/spl103` | `ruyijg.le.lpb` / `6402129ccf96c34e405b5482d86d206d7c83cd1d1c603ba937cf5e6a882d9d45` | `0fed95ce0eb594dfe16e130a4708a786db0d5f9fd7f25a2bf66170231892c4a3` |

The `lua/registry.json` `quest/scenario/spl/` rows supply the decoded-to-ciphered
name join. The recovered source locators below refer to the independent
decompile of these exact decoded chunks.

| Method | Direct recovered client-script call | Boundary |
| --- | --- | --- |
| `Spl0i1.processEventSUMFES001` | [Original-bytecode selector contract](heat-is-on-selector-contract.md) establishes the seven scalar item arguments, second retained result, confirmation/retry, cancel normalization and both outer-menu result paths. | Caller retention does not establish native arity/domain or forwarding. Local `199` retries on some paths and returns directly on another; presentation IDs/counts do not establish settlement, city binding or historical dispatch. |
| `Spl0i2.processEventSUMFES001` | `Ask/RewardSelectWidget` presents `8013301-8013304`; `worldMaster:say` arguments pair them with `3010417` and counts `3/10/50/99`. | The decompiler renders selector tests as constants such as `8 == 8`; no selected-index mapping is established. |
| `Spl0i3.processEventStartAfter` | `askExtendWidget(worldMaster, 51109, 2, 1, 1, 1000004)`. | This is an ask call; it does not prove a reward or completion grant. |
| `Spl101.askEgg` | [Original-bytecode tuple contract](scrambled-eggs-askegg-contract.md) establishes ten scalar item arguments, twelve retained widget slots, literal-true gates, local numeric mapping and an eight-value return with five unchanged passthrough values. | Native slot meanings/arity/domain and forwarding remain unproved. Local nil, zero and flag distinctions do not establish validation, consumption, a ring or other grant, caller/NPC/city binding or progression. |
| `Spl101` methods in `spl101_quest` | The independent decompile includes `askExtendWidget` menus using rows `158` and `164`. The linked Scrambled Eggs contract separately checks `processEventEASTER_G1Start` against original bytecode. | That selected method retains one `showQuestInfomation` result, branches on equality with numeric 1, then returns the value unchanged. Its actual cancel sentinel, invoking NPC, progression and rewards remain unresolved; the other menu methods retain their separate boundaries. |
| `Spl102.processEventItemSelection` | [Original-bytecode selector contract](bombard-backlash-selector-contract.md) establishes both complete eight-item arrays, the widget-open arguments and second retained result, confirmation/retry, cancel normalization and one-value returns. | The base widget result and caller retention are separate evidence points; forwarding, runtime result domain, settlement and historical invocation remain unproved. Numeric dialogue variants do not establish cities. |
| `Spl0g1`, `Spl0l1`, `Spl0u1` `processEventGirlStart` and `processEvent020` | [Original-bytecode presentation contract](dreamers-gospel-presentation-contract.md) establishes GirlStart's one retained prompt result, numeric-1 comparison and unchanged return, plus 020's talk/fade/wait order, zero-value return and three-city argument differences. | The selected methods do not call each other. Producer arity/domain, historical dispatch, progression, schedule, actor binding and grants remain unproved. |
| `Spl0g2`, `Spl0l2`, `Spl0u2` `eventBricotExchange` | [Original-bytecode exchange contract](dreamers-dilemma-exchange-contract.md) establishes one ask and one retained result per city, numeric operand tests, accepted-choice versus coerced-5 returns, no local retry, and presentation differences. | Native result/operand domains, the meaning of returned 5, item recipes, grants and historical callers remain separate. A fifth-choice branch does not identify a native cancel sentinel. |
| `Spl0i4.processEventNQ`, `processEventHin`, `processEventClear` | The first calls `startNQCutScene("spl0i410", 1)`; the hint method branches on two caller arguments, and the clear method presents dialogue and fades. | The client script does not identify the invoking world object, historical trigger, or a server-side reward. |
| `Spl000.processEvent_PRINCESSDAY_*` | [Original-bytecode JIJO contract](little-ladies-jijo-contract.md) establishes each named city menu's arguments, first-result retention, numeric-1 branch, presentation order and zero-value return. The other dialogue methods retain their separate presentation scope. | No native cancel sentinel, NPC dispatch, historical actor spawn, event availability or progression is established. The selected menu value is not returned. |
| Nine selected `Spl000.processEvent*` Foundation methods | [Original-bytecode presentation contract](foundation-presentation-contract.md) establishes the retained salute result, numeric-zero comparison, four-parameter methods' numeric thresholds, company-specific arguments and zero-value returns. | Company grouping is decoded presentation context. Native effects, caller domains, historical actor/city dispatch, player-work/shop availability, entitlement and grants remain separate. |

The `spl0g3-5`, `spl0l3-5`, `spl0u3-5`, `spl0i5`, and `spl103`
chunks independently recovered as a class declaration with an empty
`initText` method only. The same decoded paths have only `initText` in
`lua/registry.json`. This is a boundary of these specific shipped chunks,
not proof that the historical seasonal event lacked other scripts or flows.

These are client presentation contracts only. The independent decompile
includes unstable control-flow and register rendering, including repeated asks
and constant-looking selector comparisons. The linked original-bytecode
findings establish the selected argument and return contracts within their
stated scopes. They do not establish historical result domains, actual cancel
sentinels, eligibility, server item mutations or a retail activation path.
Contributor server quest IDs, SQL reward rows and implementation notes are not
evidence of a shipped client exchange.
