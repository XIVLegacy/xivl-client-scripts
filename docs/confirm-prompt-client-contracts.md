# ConfirmWarp and ConfirmRaise client contracts

ConfirmWarp (`24304`) and ConfirmRaise (`24306`) submit a selected answer
with the current command variation. They do not themselves open a dialog.
The client presents pending work through MainMenuWidget and
ConsoleIconTrayWidget, and opens CommonAskWidget when the user selects the
corresponding entry. These are recovered client contracts, not evidence of a
historical server invitation, teleport or resurrection.

## Pending work and prompt presentation

`PlayerBaseClass` registers `playerWork` listener groups
`confirmWarpCommand` and `confirmRaiseCommand` over these fields
(`chara/player/playerbaseclass.lua:758-814`):

| Prompt | Work fields |
| --- | --- |
| Warp | `variableCommandConfirmWarp`, `variableCommandConfirmWarpSender`, `variableCommandConfirmWarpSenderByID`, `variableCommandConfirmWarpSenderSex`, `variableCommandConfirmWarpPlace` |
| Raise | `variableCommandConfirmRaise`, `variableCommandConfirmRaiseSender`, `variableCommandConfirmRaiseSenderByID`, `variableCommandConfirmRaiseSenderSex` |

`getConfirmWarpCommandVariation` returns `(variation, sender, sex, place)`.
`getConfirmRaiseCommandVariation` returns `(variation, sender, sex)`. A zero
variation returns nil. The sender is `SenderByID` unless that value is zero,
in which case the string `Sender` is used
(`chara/player/playerbaseclass_cliprog.lua:4-53`). The grouped update callback
calls the matching DesktopWidget update method, which refreshes the main menu
(`playerbaseclass.lua:1303-1315`;
`widget/desktopwidget_connector.lua:6928-6940,7011-7023`). This establishes a
work-update trigger. The exact incoming packet, field encoding and server
producer of these work values remain unestablished here.

MainMenuWidget's `executeSystemCommand` and the tray's
`openConfirmTelepoWidget` / `openConfirmRaiseWidget` open the same generic
question with the following ordered text inputs:

| Command | Question | Question parameters | Answer 1 | Answer 2 | Answer 3 |
| --- | ---: | --- | ---: | ---: | ---: |
| 24304 | 1130 | sender, place | 1131 | 1132 | 1136 |
| 24306 | 1127 | sender | 1128 | 1129 | 1136 |

The default answer index is 1. Locators are
`widget/mainmenuwidget.lua:1969-2050` and
`widget/consoleicontraywidget.lua:1975-2000,2030-2054`. These raw text IDs do
not assign a duration or expiry meaning to answer 3.

## Answers and command submission

`CommonAskWidget.processUICommandEvent` parses the numbered answer item and
passes that number to `setAskResult`; UI cancel passes 0. `setAskResult`
invokes the parent's `processAskResult` and closes the widget
(`widget/commonaskwidget.lua:59-94,117-133`). Therefore the first and second
answer buttons yield 1 and 2, the third yields 3, and cancel yields 0.

The main menu submits every result except 3, then clears
`work.castingSystemCommand`. The tray submits its result for ask type 3
(warp) or 5 (raise) without that filter. These are distinct caller contracts
(`widget/mainmenuwidget.lua:916-936`, payload `root/proto6`,
`0x1D36-0x1D72`; `widget/consoleicontraywidget.lua:2082-2137`,
`root/proto30`, warp `0x46C2-0x46DE`, raise `0x4712-0x472E`).

`DesktopWidget.executePlayerSystemCommand` obtains the current variation,
allows explicit nonnil first/second arguments to replace the defaults, calls
`canCommand`, then submits exactly nine values after the command object:

```text
(variation, answer, nil, nil, nil, nil, nil, nil, nil)
```

The nine positions are deliberate. Bytecode at `root/proto280`,
`0x1F153-0x1F16F`, constructs all of them; the canonical decompile is at
`widget/desktopwidget_connector.lua:13899-13978`.

`command.csv` column 29 is -1 for both IDs. `CommandBaseClass.getPriority`
reads that column (`command/commandbaseclass.lua:116-125`), and
`CharaBaseClass.getCommandName` selects `commandRequest` for these system
commands (`chara/charabaseclass.lua:399-496`, `root/proto17`,
`0x12CC-0x1444`). When the native dispatcher delivers `_onCommandRequest`,
the callback calls inherited `command` and then `fire`, both false, before
invoking `_doServerOnCommand`
(`chara/player/playerbaseclass.lua:1884-1908`, `root/proto43`,
`0x41C3-0x4207`). The native direct route and scalar encoding are recorded in
`xivl-client-structs:manifests/player_command_wire_contract.json`.
The runtime name-to-descriptor-class registration is not established by
the Lua event name alone. The block callback `_onCommandEvent` uses
`_callServerOnCommand`; both bridges have the same proven direct fallback.
That fallback uses MapServerbound `0x012D`, the command object's resolved
control reference and the event name `commandRequest`. It does not write a
standalone scalar command ID into the typed tail. For ordinary integral
variation and answer values, the tail is `I(variation) I(answer) N^7 E`,
where `I(v)` is `00` followed by u32be bits, `N` is `05`, and `E` is `0F`.

## Eligibility and expiry boundary

Warp is enabled only for nonnil variations 20000-29999; raise is enabled
only for 40000-49999. Warp requires `isLiving()`, matching variation,
`isActiveMode() == false` and `_getActorMainStat() == 0`. Raise requires
`isLiving() == false` and matching variation. Raise's detail predicate is
true. Both `fire` methods return false. The original chunks resolve the
undefined temporary printed by the decompiler: `canFire` returns the detail
result when the supplied variation matches, otherwise false
(`confirmwarpcommand.lua:14-58`, `root/proto0`, `0x15E-0x1AA`;
`confirmraisecommand.lua:14-58`, `root/proto0`, `0x161-0x1AD`;
`confirmwarpcommand_warp.lua:11-29`, `0xFA-0x132`;
`confirmraisecommand_raise.lua:11-16`, `0xFB-0x103`).

Player command submission also checks the command burst blocker, checks the
sum of the byte lengths of the first two string arguments against 50, and
runs `canCommand` before `_executeCommand`
(`chara/player/playerbaseclass.lua:1911-2023`). None of these inspected
prompt or answer methods starts an invitation deadline, emits a timeout
answer, or waits for a named reply. The tray's `UIFormCommands.TimerFinish`
hides balloon help (`consoleicontraywidget.lua:577-614`), not a pending warp
or raise. A timeout duration, timeout message, authoritative acceptance and
subsequent server state change remain unknown.

## Shared source identity

The restricted decoded Lua archive is pinned by
`manifests/private_lua_corpus.json` at 14,385,427 bytes and SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The authenticated `command.csv` member is 126,638 bytes, SHA-256
`14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848`,
pinned by `xivl-client-data:manifests/tables.json`, row `command.csv`.
Static command-class mappings are in
`xivl-client-data:manifests/staticactor_class_paths.json`, rows 24304 and
24306. Native addresses in the linked wire contract refer to the 1.23b
executable SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.

## Input identities

The decoded members below matched `manifests/scripts.json` by byte count,
line count and SHA-256. Each original resource matched
`manifests/retail_lua_coverage.json`, including its decoded payload hash.
LPB paths are relative to retail `client/script/`. The payloads were decoded
with `tools/retail_script.py:decode_lpb` and parsed as Lua 5.1 instructions.
Instruction offsets on this page are offsets into the decoded payload.

- `lua/scripts/command/system/confirmwarpcommand.lua` (60 lines): source SHA-256
  `eedb485b0738817b31107e0e211ed47e00912df30ca219a69e2a868012f30ee6`.
  LPB `7vxx9w6/rlrq5x/7vw41sxn9su7vxx9w6.le.lpb`, SHA-256
  `694503cfe138f03d63780f92a632cbb8a4e605bfe17e3ce8176b19de30aa6ae4`. Decoded payload SHA-256
  `70b25357ccc6029c17d575702b943e583000dd7da059b5fc2ebb9fd041a33d8c`.
- `lua/scripts/command/system/confirmwarpcommand_warp.lua` (31 lines): source SHA-256
  `454fd1ff4b8b506659180cc1060f24ccbf21d3773fa4fa00efb46c41dc109b09`.
  LPB `7vxx9w6/rlrq5x/7vw41sxn9su7vxx9w6_n9su.le.lpb`, SHA-256
  `82ef8c95701599af544ba539f4e435d10fd409180244e72348f086cec95ba82d`. Decoded payload SHA-256
  `20e9fc470adf38f57426d03766cb23045ddf693270a6ac2fe3fbd807ed5cfda4`.
- `lua/scripts/command/system/confirmraisecommand.lua` (60 lines): source SHA-256
  `bfce70e84f72f564869f9449f54c544c3e0a2c29fabb58f2f6ee44a55ae7ba03`.
  LPB `7vxx9w6/rlrq5x/7vw41sxs91r57vxx9w6.le.lpb`, SHA-256
  `8be07f30584955f769fccb162a75708970d47d3497780a311e4783d367c8b40b`. Decoded payload SHA-256
  `c2b1a66f21f170d48c3fe62d9f32b82e1f31cf60dd0832aedfa7d4cb01f99998`.
- `lua/scripts/command/system/confirmraisecommand_raise.lua` (17 lines): source SHA-256
  `35d66dcfef6ee2b8658e58ea7a3c492e3576247b60942a5b238c93dedad09701`.
  LPB `7vxx9w6/rlrq5x/7vw41sxs91r57vxx9w6_s91r5.le.lpb`, SHA-256
  `350cd3b76b373b4cdae68a2d05127484f693184df5816a2fa9ae9846cd9ce14f`. Decoded payload SHA-256
  `94ea97a5373d788f4ad504a0ec0d9b75bdef923b475f5d263787aa9b533275ac`.
- `lua/scripts/command/commandbaseclass.lua` (246 lines): source SHA-256
  `bf7dd5fa7a6530c0c3b683be16a252b7ffd62492bdc268f36322977dee4d3e31`.
  LPB `7vxx9w6/7vxx9w689r57y9rr.le.lpb`, SHA-256
  `2cb8936f373b25344a115f397da981146ae927c28c91a0c2c3dd2655b0b9d1b1`. Decoded payload SHA-256
  `4d9cace900e712997f1a40663144d58f33b1f35f5a4aa521f637eb8c52364f25`.
- `lua/scripts/command/system/systemcommandbaseclass.lua` (17 lines): source SHA-256
  `4e71e311c9a06dfbef1ea56f9276414099844db7a0dc185557da561bce3b6efe`.
  LPB `7vxx9w6/rlrq5x/rlrq5x7vxx9w689r57y9rr.le.lpb`, SHA-256
  `738a4a4153c9e7bb4cadde005b41ddb35124ef7742dabfd8469af466b5fa84b0`. Decoded payload SHA-256
  `a53bc68e6d917da821ff65b9f408756c0f5906441826b4003e1356ca65b058f5`.
- `lua/scripts/chara/charabaseclass.lua` (1734 lines): source SHA-256
  `f17b3e62a137d8f524ba88d55296e1fb064512dc803f7a85dc980dd4bcbc9625`.
  LPB `729s9/729s989r57y9rr.le.lpb`, SHA-256
  `c7cd1dad84f7d9b723f5a10fb66108da9d9d6ef5d7c15186b48ec55092465238`. Decoded payload SHA-256
  `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9`.
- `lua/scripts/chara/player/playerbaseclass.lua` (3020 lines): source SHA-256
  `6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4`.
  LPB `729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`, SHA-256
  `32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e`. Decoded payload SHA-256
  `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`.
- `lua/scripts/chara/player/playerbaseclass_cliprog.lua` (180 lines): source SHA-256
  `dd7dadf2cee4647068f6dae0b865cfb9f203be7c189e60c63accaf8976ec7cf9`.
  LPB `729s9/uy9l5s/uy9l5s89r57y9rr_7y1usv3.le.lpb`, SHA-256
  `1d41560f5750be6c9a6903c489cb535f05296674a08548afda44437c83b06f53`. Decoded payload SHA-256
  `816eae5a48a7e4ad3c76939ac44aaf9488d4be00bd56a40fb65198edff15ca1d`.
- `lua/scripts/widget/desktopwidget_connector.lua` (26564 lines): source SHA-256
  `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`.
  LPB `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, SHA-256
  `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`. Decoded payload SHA-256
  `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621`.
- `lua/scripts/widget/commonaskwidget.lua` (133 lines): source SHA-256
  `d304094ae53cd9fa82c59166495941f310161ce1fac62c37025bfdb5da3cd8e5`.
  LPB `n1635q/7vxxvw9rzn1635q.le.lpb`, SHA-256
  `cad77ceafd51dfc6b59da750b7beb01d2d25f3641ba2e52ded2d198964c56b9c`. Decoded payload SHA-256
  `1a023c9f9d0b995d1640fd6e7c211b823d6eae0dd1970a615adc18e79d1c041b`.
- `lua/scripts/widget/mainmenuwidget.lua` (2605 lines): source SHA-256
  `7dfd161c2852a56fd598f47469cc2d7597ba9f0e4b228555a09274674b2b4e41`.
  LPB `n1635q/x91wx5wpn1635q.le.lpb`, SHA-256
  `c0e1782a3ca183fcaa520a16320946f62d3fc861c74978cde19ea20fcd064b0a`. Decoded payload SHA-256
  `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2`.
- `lua/scripts/widget/consoleicontraywidget.lua` (2154 lines): source SHA-256
  `c7731790f37eca0ade415e8b42610ed6db84da416d734c27b44341296a081767`.
  LPB `n1635q/7vwrvy517vwqs9ln1635q.le.lpb`, SHA-256
  `892ac23eb20269dc847572c7a9877f31fb7766137d76b32f1a7e6ca671bd2af5`. Decoded payload SHA-256
  `498b25c7365180cd1ecff32d099ebc3e38fae0c6b6cd9d1f6e3a0953a33e3a7e`.
