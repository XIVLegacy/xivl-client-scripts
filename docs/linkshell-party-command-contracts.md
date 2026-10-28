# Linkshell and party command contracts

The recovered linkshell and party commands use shared player-command dispatch.
For the scoped
system-command classes that admit a local invocation, the direct native
fallback is MapServerbound `0x012D` with event name `commandRequest`.
`LinkshellChangeCommand` selects the current linkshell. The inspected client
callers do not establish a rename or master-transfer operation. The focused
[master-transfer evidence](linkshell-master-transfer-evidence.md) records
the exhaustive recovered-caller search, member identity relationship, text
and capture findings, and remaining native/backend boundaries.

## Shared dispatch and wire representation

The [confirmation contract](confirm-prompt-client-contracts.md#shared-source-identity)
owns the authenticated common Lua and command-sheet input identities.
`command.csv` column 29 is -1 for IDs 24203-24209, 24230-24236 and 24303.
`CharaBaseClass.getCommandName` consequently returns `commandRequest`
(`chara/charabaseclass.lua:399-496`, payload `root/proto17`,
`0x12CC-0x1444`). The inherited `CommandBaseClass.command` and `fire` return
false for the system classes in the table. When dispatch delivers
`_onCommandRequest`, the player callback therefore reaches
`_doServerOnCommand`
(`chara/player/playerbaseclass.lua:1884-1908`, `root/proto43`,
`0x41C3-0x4207`). The retained `commandRequest` definition and conditional
nonblock constructor are recorded in
`xivl-client-structs:manifests/command_descriptor_registration.json`. The
descriptor selected for a later invocation remains unobserved. The block
callback instead uses `_callServerOnCommand`; both bridges share the same
proven direct fallback. The separate PartyAccept exception is described below.

`xivl-client-structs:manifests/player_command_wire_contract.json` owns the
native binding, envelope and typed serializer evidence. The direct fallback
uses a command-object control reference in the envelope and serializes the
values after the name and command object into its 128-byte tail. A scalar
sheet ID is not an additional tail operand. In normal outbound order:

| Notation | Encoded value |
| --- | --- |
| `I(v)` | `00` followed by four-byte integer bits, big-endian |
| `S(s)` | `02`, string bytes, NUL |
| `N` | `05`, one explicit nil |
| `A(a)` | `06` followed by the actor's resolved control-reference dword, big-endian |
| `E` | `0F`, stream terminator |

`DesktopWidget.executePlayerCommandLocal` forwards nine command values via
`executeCommand`, `command`, `PlayerBaseClass.command` and `_executeCommand`.
Unused positions remain explicit nil, not zero padding
(`widget/desktopwidget_connector.lua:13372-13479`,
`root/proto273`, `0x1E640-0x1E680`;
`chara/player/playerbaseclass.lua:1911-1974`). String byte lengths in the first
two positions must total at most 50. `canCommand` also rejects the player's
command burst blocker before each command's predicate
(`playerbaseclass.lua:1911-2023`).

## Command inputs

Tuples below contain the nine values after the command object. `n^k` means
k explicit nils. `u` is `getLinkshellUniqueIdentifier`'s string; `m` is the
member string supplied by the caller. Actor alternatives put the actor in
position 5. The expressions describe client inputs, not server mutations.
For the system rows with a proven issuer, replace each element using the
encoding table above and append `E` to obtain the typed `0x012D` tail.

| Class and ID | Client input tuple or limit | Caller locator in `widget/desktopwidget_connector.lua` |
| --- | --- | --- |
| LinkshellAppoint 24231 | `(u, m, rank, n^6)` | `executePlayerLinkshellAppoint`, 15376-15432 |
| LinkshellChange 24236 | `(u or nil, nil, 1, n^6)` | `executePlayerSetCurrentLinkshell`, 15018-15048 |
| LinkshellInvite 24232 | `(u, name, n^7)` or `(u, n^3, target, n^4)` | 15118-15147,15182-15207 |
| LinkshellInviteCancel 24233 | `(name, n^8)` or `(n^4, target, n^4)` | 15211-15252 |
| LinkshellKick 24234 | `(u, m, n^7)` | `executePlayerLinkshellKick`, 15319-15372 |
| LinkshellResign 24235 | `(u, n^8)` | `executePlayerLinkshellResign`, 15271-15315 |
| PartyInvite 24203 | `(name, n^8)` or `(n^4, target, n^4)` | 14230-14303 |
| PartyAccept 24209 | No proven local issuer; class declares no methods and inherits `canFire == false`. | `command/system/partyacceptcommand.lua:1-8` |
| PartyJoin 24204 | `(name, n^8)` | `executePlayerPartyJoin`, 17745-17755 |
| PartyKick 24207 | `(name, n^8)` or `(n^4, target, n^4)` | 14326-14366 |
| PartyLeader 24208 | `(name, n^8)` or `(n^4, target, n^4)` through the generic system-command helper | `executePlayerSystemCommand`, 13839-13978 |
| PartyResign 24205 | `(n^9)` | `executePlayerPartyResign`, 14307-14322 |
| PartyBreakup 24206 | `(n^9)` | `executePlayerPartyBreakup`, 14370-14385 |
| PartyTarget 12011 | `(mappedId, mode, 0, nil, target, n^4)` | `executePlayerPartyTarget`, 14523-14565 |

The PartyTarget row is a game command, priority 11, selecting
`commandForced`. It uses the ready-command helper and conditional native
fallback described in the
[equipment and cancel contract](equipment-cancel-command-contracts.md).
It is not a `commandRequest` row. Its input ID must be 1-8 when nonnil;
`mappedId` is 0 for nil, otherwise `id + base` for IDs 4-7 and
`id - 1 + base` for the others, where base is 100 for mode 2 and 1 otherwise.
The ready-command lookup requires a live target and an available equipped
command. Bytecode locator: DesktopWidget `root/proto300`,
`0x2036C-0x20404`.

PartyAccept 24209 has `command.csv` column 26 (`isOnlyServer`) true.
The actual local invitation-answer callers use ConfirmGroup 24303, not the
empty PartyAccept class. An ID/class mapping does not prove a usable request.
For PartyLeader, the generic system-command helper accepts a first-value
name, or a target in its fourth helper argument when the first is nil. Its
bytecode explicitly groups 24208 with 24207 for that target selection
(`root/proto280`, `0x1EF7F-0x1EFA7`). This establishes a callable helper
shape, not a captured leadership transfer.

## Refusals and linkshell operation meaning

Each linkshell command predicate checks that the initiating object exists,
is alive as a client actor, and is a player. The optional target-actor branch
also requires a live player. `_isAlive` here is object validity; it must not
be read as the separate gameplay predicate `isLiving`.

| Predicate | Additional local requirements |
| --- | --- |
| LinkshellChange | Third value equals 1; first value is nil or string. |
| LinkshellInvite | First value is string; without a target actor, second value is string. |
| LinkshellInviteCancel | Without a target actor, first value is string. |
| LinkshellResign | First value is string. The DesktopWidget helper additionally refuses the group's owner. |
| LinkshellKick | First value string, matching live current group of category 20002, local membership, local rank at least 7, selected member present, local rank strictly above selected rank. |
| LinkshellAppoint | The LinkshellKick group/rank checks plus requested rank in 1-10; a string target is required when no actor target is supplied. |
| PartyInvite | Local player is party leader. In the exclusive actor/name alternatives, target is not already in party or relation group 50001. |
| PartyJoin | Own party has at most one member. In the exclusive actor/name alternatives, target is not already in that party. |
| PartyKick / PartyLeader | Local player is party leader, party count is not 1, target is a party member and is not self in the exclusive actor/name alternatives. |
| PartyResign | Party count is not 1. |
| PartyBreakup | Local player is party leader and party count is not 1. |

The party predicates do not generally reject malformed combinations outside
those exclusive alternatives. In particular, passing neither or both a string
and actor is not equivalent to a proven valid server request. The ordinary
party helper additionally refuses `isRestrictedByContents(1)`; invite by name
requires checked text containing a space
(`widget/desktopwidget_connector.lua:14208-14264`).

The per-class predicates occupy `canFire` in the corresponding system Lua
members listed under input identities. Appoint and kick compare the string
branch with `getMemberUniqueIdentifier`, while their DesktopWidget helpers
obtain `m` from `_getMemberLocalizedDisplayName`.
`CompanyGroup.getMemberUniqueIdentifier` bounds-checks its index and returns
`_getMemberDisplayName(index)` (`companygroup.lua:464-479`). The
[focused identity finding](linkshell-master-transfer-evidence.md#caller-and-operand-domains)
records the native same-string branch and its limits.

`executePlayerSetCurrentLinkshell` sends operation 1 with the selected UID
or nil. This is concrete evidence of current-shell selection, not renaming.
`LinkshellMenuSubWidget.processAskResult` changes rank 7 to 4 and other
selected ranks to 7 before calling the appoint helper
(`widget/linkshellmenusubwidget.lua:323-349`). The rank range 1-10 in the
command predicate does not prove master transfer at rank 10. The inspected
issuer establishes rank changes 4 and 7 only.

## NPC naming and master-transfer boundary

The normal management NPC and member widgets did not establish a rename or
master-transfer request. The manager's naming step supplied a standalone name
to a later name/crest return; neither existing-group branch collected a new
name or a target member. This is a bounded client observation, not a claim
that every server-authored event or backend operation was absent.

### Linkshell rename boundary

A rename caller would associate an existing group UID with a replacement
name. The inspected operations preserve different inputs:

| Client path | Established operands | Source locator |
| --- | --- | --- |
| Current-shell selection, 24236 | UID or nil, nil, integer 1, six nils | `executePlayerSetCurrentLinkshell`, 15018-15048 |
| Standalone-name collection | Name, later returned with icon as `(3,name,icon)` | Manager `root/proto8` PCs 23-33 and `root/proto5` PCs 62-149 |
| Icon selection for existing UID | UID and icon, later returned as `(4,UID,icon)` | Manager `root/proto11` PCs 33-101 and `root/proto5` PCs 153-169 |
| Rank appointment, 24231 | UID string, member string, rank, six nils; inspected menu requests 4/7 | `executePlayerLinkshellAppoint`, 15376-15432; submenu 323-346 |

The manager tuples are local method returns, not assigned server operations
or authenticated wire requests. None supplies an existing UID and a new
name together. The complete original-bytecode and authenticated literal
searches below therefore establish no rename caller within those bounds.
They do not exclude the native text-command parser's computed dispatch,
aliases, dynamically formed method/command names, arbitrary server-authored
events, or backend operations. No rename payload, completion receiver,
message row, recipient split or server naming policy is established.

The missing discriminator is a retail existing-UID plus replacement-name
caller followed through its event/command bridge and result consumer, or an
already retained transaction identifying that operation. The naming widget,
current-shell selection, icon selection and rank appointment do not supply
that join.

The [NPC contract](npc-linkpearl-client-contract.md#linkshell-management-ui-and-local-command-checks)
owns the full management method/UI observations and resource identities.
Reproduction from the original LPBs used `tools/retail_script.py:decode_lpb`
and pinned `unluac_2025_12_23.jar` (SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`).
The decoded payload and canonical LF source matched both retail coverage
and source manifests. PCs below are zero-based Lua 5.1 instruction indices.

| Manager boundary | Direct original-bytecode observation |
| --- | --- |
| `eventTalkStep231`, `root/proto8`, PCs 23-33; source 666-675 | Calls `askLinkshellNamingWidget()` with no group UID or old-name argument (CALL 25). Returns the third widget result only when the first two equal `true, 1`; otherwise returns the empty string. |
| `eventTalkStep2`, `root/proto5`, PCs 62-149; source 360-463 | Carries that name through validation, icon selection and confirmation, then returns `(3, name, icon)` at PC 149. The malformed-looking decompiled nesting was checked against the bytecode branches. |
| `eventTalkStep24`, `root/proto11`, PCs 33-101; source 833-905 | Selects a type-20002 group, reads its UID and crest, and calls `askLinkshellSelectIconWidget(2, oldCrest)` at PC 78. Its accepted pair is `(UID, selectedIcon)`; result 2 yields `(UID, 0)`, other unsuccessful widget results `(UID, -1)`. No naming call occurs. |
| `eventTalkStep2`, `root/proto5`, PCs 153-169 | Returns `(4, UID, selectedIcon)` only after a nonempty UID and icon at least 1. |
| `eventTalkStep25`, `root/proto12`, PCs 35-123; source 952-1050 | Selects an existing group's UID/crest, confirms mode 3 (CALL 77), then asks the additional question (CALL 92). Normal cancellation sets the UID to the empty string. It neither requests a member nor reads a replacement name. |
| `eventTalkStep2`, `root/proto5`, PCs 174-184 | A nonempty result from step 25 produces `(5, UID, 0)` at PC 184. |

These are returns to the event caller, not a newly authenticated wire
request. The values `3/4/5` remain local method results; text keys and
`MakeupDone`/`ModifyDone`/`BreakDone` names alone do not assign server
operations or reply semantics. The existing
[completion observations](npc-linkpearl-client-contract.md#manager-text-and-widget-handoffs)
show callable refresh/talk-turn methods, without a transaction proving which
request invoked them.

The naming widget itself returns `(baseAskResult, textBoxText)` from
`getAskResult` (`root/proto5`, source 328-343; base-result CALL PC 1,
text-box `getText` CALL PC 7, RETURN PC 11). Text remains empty unless the
base result equals 1. It does not add a group or
member identity to that result.

The finite original inspection covered all constants and instructions of
`populacelinkshellmanager`, `ask/linkshellnamingwidget`,
`linkshellmemberslistwidget` and `linkshellmenusubwidget`. The member UI's
rank-4/7 issuer remains the separate appoint operation documented above;
the allowed rank-10 predicate is not a demonstrated transfer caller. A
case-sensitive source query across all 2,671 manifest-authenticated Lua
members found `askLinkshellNamingWidget` only at this manager call and the
DesktopWidget wrapper definition. The exact expression
`Linkshell.*(Rename|Master|Transfer)|(Rename|Master|Transfer).*Linkshell`
had no match. This literal query does not exclude aliases or dynamic event
construction.

The missing discriminator is a retail caller associating an existing group
UID with a replacement name, or that UID with a new owner/member, together
with its event/command dispatch and result receiver. No such concrete seed
arose in this scope, so no additional native payload was opened. Backend
capability names cannot fill that request/reply join.

## CompanyGroup rank consumer

`CompanyGroup.getMemberRank` takes a member index or resolves an actor with
`getMemberIndex`. For indices 1 through `#work._memberSave`, it returns
`work._memberSave[index].rank`; an invalid index returns 0
(`group/communitygroup/companygroup.lua:482-515`). Initialization declares
`_memberSave` as an array sized by `_getProperty(0)` with a nested `rank`
field of type `integer8` for each member (100-136).
`getCompanyRank` separately returns `work._globalSave.rank` (22-30).
The latter is not established as the recipient's own member rank.
These Lua fields identify consumers, not their `0x017A` record offsets,
record count, continuation marker or complete synchronization sequence.
The full type-20002 rank consumer inventory and native marker handling are
recorded in `xivl-client-structs:docs/linkshell-rank-work-contract.md`.

## Invitation answers, timing and replies

`PlayerBaseClass.getConfirmGroupCommandVariation` inspects relation group
50001 and returns nil for a missing group or its host. For the non-host it
returns `group:getCommandVariation()`
(`chara/player/playerbaseclass_cliprog.lua:56-81`). Party variation 10001 and
linkshell variation 10002 open CommonAskWidget with these text IDs:

| Variation | Question with sender parameter | Answer text IDs |
| ---: | ---: | --- |
| 10001 | 1121 | 1122,1123,1136 |
| 10002 | 1137 | 1138,1139,1136 |

Both use ConfirmGroup 24303 and the exact tail
`(variation, result, n^7)`. The common answer contract, cancel result 0,
main-menu result-3 filter, and tray forwarding are documented in the
[confirmation contract](confirm-prompt-client-contracts.md#answers-and-command-submission).
The tray bytecode routes both ask types 1 and 2 to 24303
(`root/proto30`, `0x468E-0x46B6`); its decompiled party branch is incomplete.
The direct party-confirm helper sends result 2 only for explicit false and 1
otherwise, after requiring variation 10001
(`desktopwidget_connector.lua:14389-14422`). ConfirmGroup itself admits only
a matching variation and is enabled for 10000-19999
(`command/system/confirmgroupcommand.lua:11-49`).

No inspected party/linkshell prompt method installs an invite deadline or
converts a timer expiry into an answer or message. ConsoleIconTrayWidget's
`UIFormCommands.TimerStart` / `TimerFinish` controls balloon help
(`consoleicontraywidget.lua:577-614,1221-1255`), not the lifetime of group
50001. A numeric invite timeout and its retail expiry message remain
unestablished. A debugger reference to a timeout getter alone cannot establish
runtime expiry behavior.

The synchronous helper return indicates local command admission. The
linkshell appoint/kick helpers call member/rank information refresh methods
on a true return, but they do not await a named success packet or prove that
a rank/member changed. No row above establishes a mandatory group packet,
`0x0143` deletion, chat message or fixed reply sequence for its request.
Those require a receiver/capture join. Backend opcode names `0x1022-0x1032`
do not supply client-facing packet bindings.

## Input identities

The decoded members below matched `manifests/scripts.json` by byte count,
line count and SHA-256. Each original resource matched
`manifests/retail_lua_coverage.json`, including its decoded payload hash.
LPB paths are relative to retail `client/script/`. The payloads were decoded
with `tools/retail_script.py:decode_lpb` and parsed as Lua 5.1 instructions.
Instruction offsets on this page are offsets into the decoded payload.

- `lua/scripts/command/system/linkshellappointcommand.lua` (192 lines): source SHA-256
  `cbfb53f5cd1abe8d322592cd05808e251e7b6b4d3139061e4691f6affd638a60`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yy9uuv1wq7vxx9w6.le.lpb`, SHA-256
  `fd15f648c719b10de33a67b061ad96433768c362bcd8b05731979c9b05c88363`. Decoded payload SHA-256
  `7428c51fb4bfff9a65f875dffb4107e8064ce39fc63576c569d8abce6d0827e3`.
- `lua/scripts/command/system/linkshellchangecommand.lua` (58 lines): source SHA-256
  `5d45980f402fe62e5df4971bcbe47771684750b0fc4dc34020f974844442da99`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yy729w357vxx9w6.le.lpb`, SHA-256
  `d37cc54e1ffee41296b6df528ef145e0f200ef8c3ff939cd7fb6dc1b8c0783a1`. Decoded payload SHA-256
  `306bd136d083ac6b57314c0ac6bddd0267d8a108a1813eb2dcbb1406ccec3394`.
- `lua/scripts/command/system/linkshellinvitecommand.lua` (84 lines): source SHA-256
  `fa49a215ded17fd68eabbc572eb033bfb490669ba388814f962c316ad7010ecc`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yy1wo1q57vxx9w6.le.lpb`, SHA-256
  `5c51d6ee2ba9e050c6ed5196a8dc25e2f699e2d10e7da933f70fefe87f0d72e8`. Decoded payload SHA-256
  `4d918167fc36deeb4715ab504f6328de53705f57145f5ea935daf2e24faac00c`.
- `lua/scripts/command/system/linkshellinvitecancelcommand.lua` (77 lines): source SHA-256
  `b5fbd5e1937d3cc3b846249129d512626c11ae162f7ced94774241237ddb63e1`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yy1wo1q579w75y7vxx9w6.le.lpb`, SHA-256
  `91a5253a78530ce8c8cef0b533f0a5baf0d3d2e937f2f565eda81527a520c8bc`. Decoded payload SHA-256
  `fb6d7f7973b7a59ff066769113028e4fdecd73d7592d421c76e7849bddb5cf6f`.
- `lua/scripts/command/system/linkshellkickcommand.lua` (170 lines): source SHA-256
  `f5960d95ac01b3ce2659caba014354aaaca4ad86a5f90996b0e46e95e53e679d`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yyz17z7vxx9w6.le.lpb`, SHA-256
  `38e0602d26d343c9fca64629eb6a5a392792c7af033e5efdefe53e3c8a65ff99`. Decoded payload SHA-256
  `7695f875032873df409b48ce864ad634cabc4f0863964a28e9dfac1b5c35d496`.
- `lua/scripts/command/system/linkshellresigncommand.lua` (42 lines): source SHA-256
  `2840c690f9f95da1d24e4861f7080f59008518afa770b962b7900e0ce4268a0d`.
  LPB `7vxx9w6/rlrq5x/y1wzr25yys5r13w7vxx9w6.le.lpb`, SHA-256
  `3b5cd195995b565496175707bacea746d9e4b45fd6daf91b74fa4aef71046eb6`. Decoded payload SHA-256
  `7a6972f9f091de177e688b329403667b40dbe7f8ad5faaadf1c81628684f9388`.
- `lua/scripts/command/system/partyinvitecommand.lua` (83 lines): source SHA-256
  `f26340aef9461b13102e9c69579c21d745dc1b3aeda314e428f6565a429d473e`.
  LPB `7vxx9w6/rlrq5x/u9sql1wo1q57vxx9w6.le.lpb`, SHA-256
  `a029b0862bf0384307b04f9beffd15b699f7eceb3ca42b8d7230911fdb2a5b67`. Decoded payload SHA-256
  `da574318fe5107aa7edb0c271de56f38db200bd6054efffad93bf7f7c8b0de04`.
- `lua/scripts/command/system/partyacceptcommand.lua` (8 lines): source SHA-256
  `752da085f1a1c6df0ad059c555dd6a33a36b588708710b6444e8385eeef82734`.
  LPB `7vxx9w6/rlrq5x/u9sql9775uq7vxx9w6.le.lpb`, SHA-256
  `ab0cf95601415fe928e072ebd0980e1d74fbb060ad1048b605c28c0e64b69597`. Decoded payload SHA-256
  `9c7ab3001918e4d02422e6cffcd1083bf1c67488239f59ef6bd9ef59ca83638e`.
- `lua/scripts/command/system/partyjoincommand.lua` (70 lines): source SHA-256
  `68a0a973bae26407ad3425b3d55891ae08a80597aa660c360386d1a51cbbc512`.
  LPB `7vxx9w6/rlrq5x/u9sql0v1w7vxx9w6.le.lpb`, SHA-256
  `6a13f440b3c54a3c22da8cd338875ac1911a824b5561a3f71792fc18fb591456`. Decoded payload SHA-256
  `cf6b0878a625c95084003eb43d7c55da3cbcd6c5144ba28c4bee30348550ec60`.
- `lua/scripts/command/system/partykickcommand.lua` (96 lines): source SHA-256
  `bcae0753dec46a429b2304fd513a16db79e1aa2fc0b2187a0b93b41a4a646b85`.
  LPB `7vxx9w6/rlrq5x/u9sqlz17z7vxx9w6.le.lpb`, SHA-256
  `b67af85288f503e11bf20d5a8740bdc771eeec0b95c98dbe66ca75e3c2991a9d`. Decoded payload SHA-256
  `8e2b8dc3aeff6d059b64aae387e07439e62549d0c9063fe9cbf185b73167a087`.
- `lua/scripts/command/system/partyleadercommand.lua` (96 lines): source SHA-256
  `a329aafceeb37b3e2a2bcbec22461c9f6738af0869dcf0dbf252b828dd4cf5e6`.
  LPB `7vxx9w6/rlrq5x/u9sqly5965s7vxx9w6.le.lpb`, SHA-256
  `6a6f890fedf75b10ea9a9d3467796d45d992be3acff59f81a86d7a07962f5a62`. Decoded payload SHA-256
  `e2011d83b1892e67877ffba674fa3364350e2d72dae5e428cd04940ed3d5bfbc`.
- `lua/scripts/command/system/partyresigncommand.lua` (27 lines): source SHA-256
  `48ab0ede8ca68a647f73b21c22cba6a0d6c288da520a48ac9bdf2f49c44e6937`.
  LPB `7vxx9w6/rlrq5x/u9sqls5r13w7vxx9w6.le.lpb`, SHA-256
  `523bcc7217bb5bea2c40a0390485bec02088f2ce3af838ec52c0b5266e25a26f`. Decoded payload SHA-256
  `079e05d24379e57dfe8f57e4a20a4a78be963578083ab6853def745610da3217`.
- `lua/scripts/command/system/partybreakupcommand.lua` (34 lines): source SHA-256
  `6124d4cde9f43747344b7e8e5c6fe8156b1bb16b5ced2223c95f58202a00f325`.
  LPB `7vxx9w6/rlrq5x/u9sql8s59zpu7vxx9w6.le.lpb`, SHA-256
  `f7a8fb464f995d65775a0ab92138a8de95a8a02146a5d2194bb1d9b0d9a1f618`. Decoded payload SHA-256
  `02b132005b5e96a8a2350105a66d21a07d694e26fcb0112851838aaa3497f8b7`.
- `lua/scripts/command/system/confirmgroupcommand.lua` (45 lines): source SHA-256
  `4594d364f6a347a2fd113625b9583e701b2e8b67883d4eaff587492b412873ce`.
  LPB `7vxx9w6/rlrq5x/7vw41sx3svpu7vxx9w6.le.lpb`, SHA-256
  `74aa2ca19294fc28fcd228b01e31069e29419b6a72aeef3b36c1bd7e564181bc`. Decoded payload SHA-256
  `364a1f10c1de773e49e2e0ebeb3e117164b7b32a5adf9fa87a66c19900476697`.
- `lua/scripts/command/game/partytargetcommand.lua` (84 lines): source SHA-256
  `9cc7e8ba165e6dac4cb3b3db62f48588252b5d67c203bf5a0a9efe61bb4a8b61`.
  LPB `7vxx9w6/39x5/u9sqlq9s35q7vxx9w6.le.lpb`, SHA-256
  `8246c74fda2bc890e9b868002bae2326215bb344f64905c2fbe08971e89ec57d`. Decoded payload SHA-256
  `0c8519eca17663dd07f4801492a799247a9278fcb48e942ff575ef26886094d2`.
- `lua/scripts/widget/linkshellmenusubwidget.lua` (544 lines): source SHA-256
  `339976897789ea6e546ca3b8f066acd375dd9c31d3687bc5d32654f5055dea0a`.
  LPB `n1635q/y1wzr25yyx5wprp8n1635q.le.lpb`, SHA-256
  `a3cfebe12f68a68018329e7f3996ea743e6a0ab57691d7cb3ccf458bb4dd7399`. Decoded payload SHA-256
  `dc30dcfa5243196da3ae2bd93e9a8d6db98cb7ac9f4afa3bdba1328ee3328fcf`.

- `lua/scripts/group/communitygroup/companygroup.lua` (515 lines): source SHA-256
  `c7b931666f80eaf47fdf033a4f749dbfaff4ca88547e274c14cb3d4bb5b54e0e`.
  LPB `3svpu/7vxxpw1ql3svpu/7vxu9wl3svpu.le.lpb`, SHA-256
  `d4a2402ce8e687848e10ccf3dc5d1a1a03daedafab3886f760764173e23b0b4c`. Decoded payload SHA-256
  `5e260e744427ad86bf4f38cfd7d3ead09c3fa5834b022ceac040c9b537323123`.
