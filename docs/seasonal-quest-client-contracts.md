# Seasonal quest client contracts

The installed `client/script/tp5rq/r75w9s1v/ruy/` LPBs below decode
byte-for-byte to the independently recovered Lua 5.1 chunks. The recovered
Lua bodies are a separate decompile from the canonical corpus recorded in
`manifests/scripts.json`; their text hashes do not match that manifest. The
claims below therefore cite the installed resource, matching decoded chunk,
and recovered method body, not a supposed match to the canonical Lua text.

| Decoded script | Installed LPB basename / SHA-256 | Recovered Lua SHA-256 |
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

The `lua/registry.json` `quest/scenario/spl/` rows supply the decoded-to-ciphered
name join. The recovered source locators below refer to the independent
decompile of these exact decoded chunks.

| Method | Direct recovered client-script call | Boundary |
| --- | --- | --- |
| `Spl0i1.processEventSUMFES001` | `Ask/RewardSelectWidget` presents `3020604-3020606` and `10012018-10012021`; following `say` arguments pair these with `10012014-10012017` and displayed counts. | Presentation and dialogue arguments, not item ownership, cost deduction, grant, or selector outcome. |
| `Spl0i2.processEventSUMFES001` | `Ask/RewardSelectWidget` presents `8013301-8013304`; `worldMaster:say` arguments pair them with `3010417` and counts `3/10/50/99`. | The decompiler renders selector tests as constants such as `8 == 8`; no selected-index mapping is established. |
| `Spl0i3.processEventStartAfter` | `askExtendWidget(worldMaster, 51109, 2, 1, 1, 1000004)`. | This is an ask call; it does not prove a reward or completion grant. |
| `Spl101.askEgg` | `Ask/EventItemSelectWidget` presents `10012001-10012004`, `10012022`, and `10012024-10012028`. | The meaning of widget return values and any exchange or ring grant are not established by this call. |
| `Spl101` methods in `spl101_quest` | Repeated `askExtendWidget` menus use rows `158` and `164`, including `processEventEASTER_G1Start`. | The recovered body does not identify a corresponding server quest row, selected result, or reward. |
| `Spl102.processEventItemSelection` | `isMale()` selects two eight-item arrays; the stable trailing entries are male `8032835-8032836`, `8051521-8051523`, `8081921`, `3020613`, or female `8032838-8032839`, `8051524-8051526`, `8081922`, `3020613`. `Ask/RewardSelectWidget` consumes that array, while `say` arguments use `10011253` and counts `1/30/50/1/30/50/5/1`. | The decompiler overwrites the first array slot during construction; `8032834`/`8032837` are plausible first-slot values, not proven displayed entries. No exchange mutation or selector result is proven. |
| `Spl0g1`, `Spl0l1`, `Spl0u1` `processEventGirlStart` and `processEvent020` | The city variants present `showQuestInfomation()` dialogue and later a fade-out/fade-in talk sequence. | Method presence does not prove a seasonal schedule, actor binding, eligibility, or completion effect. |
| `Spl0g2`, `Spl0l2`, `Spl0u2` `eventBricotExchange` | Each renders a five-option ask, tests choices 1-4 against four caller-supplied counts, and has a fifth-choice branch. | The decompile repeats `ask` calls and shows a `false == true` comparison; exact return/acceptance behavior and item recipes are not established. |
| `Spl0i4.processEventNQ`, `processEventHin`, `processEventClear` | The first calls `startNQCutScene("spl0i410", 1)`; the hint method branches on two caller arguments, and the clear method presents dialogue and fades. | The client script does not identify the invoking world object, historical trigger, or a server-side reward. |

These are client presentation contracts only. The recovered decompile includes
unstable control-flow and register rendering (including repeated asks and
constant-looking selector comparisons). No historical return values, cancel
semantics, eligibility, server item mutations, or retail activation path are
available from these static scripts. Contributor server quest IDs, SQL reward
rows, and implementation notes are not evidence of a shipped client exchange.
