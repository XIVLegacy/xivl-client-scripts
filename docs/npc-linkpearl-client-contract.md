# NPC Linkpearl client route

Three decoded Lua 5.1 chunks matched the LPBs byte-for-byte
after their 13-byte `rle` wrappers were decoded (payload XOR `0x73`).
The shared DesktopWidget connector and MainMenuWidget identities are pinned
in [Parley target gate](parley-target-gate.md). Recovered method names and
line numbers below locate Lua decompiler output, not native executable code.

| Recovered class | LPB beneath `client/script/` | LPB SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- | --- |
| `widget/consoleicontraywidget` | `n1635q/7vwrvy517vwqs9ln1635q.le.lpb` | `892ac23eb20269dc847572c7a9877f31fb7766137d76b32f1a7e6ca671bd2af5` | `498b25c7365180cd1ecff32d099ebc3e38fae0c6b6cd9d1f6e3a0953a33e3a7e` |
| `widget/npclinkshelllistwidget` | `n1635q/wu7y1wzr25yyy1rqn1635q.le.lpb` | `587178c19d85620750d2adbbc52f62f94ec705f7e5f4bc5f7f9b1364ad2e8a16` | `0021720833324e4d8a0bfc2aa8fbd25c863051c585028be754de13f4df354468` |
| `command/system/npclinkshellchatcommand` | `7vxx9w6/rlrq5x/wu7y1wzr25yy729q7vxx9w6.le.lpb` | `edf5467434dbf67d0cd1ba69098fe1b333977cfad3b0db1a43670214d827be4b` | `54863f52d5d3a2e1b7cd934544b0f65a848ab3d3d74385736274424945699275` |

`ConsoleIconTrayWidget.processUICommandOperate` sends
`UILuaCommands.ShortCutActionQuestLSMenu` when `Button_QuestLinkPearl`
is operated (recovered lines 209-212). The DesktopWidget connector handles
that shortcut by opening `NpcLinkshellListWidget` (lines 1692-1695 and
1985-1988). `MainMenuWidget` has a separate list-opening path (lines
208-211).

`NpcLinkshellListWidget.init` adds a row for each `hasNpcLinkshell(id)`
result, stores that ID in `IntData.Value0`, and uses text ID 3482 with
the same ID for the row label (lines 30-49). In
`processUICommandSelectionChanged`, it retrieves the stored ID and calls
`desktopWidget:executePlayerNPCLinkshellChat(id)` (lines 94-110).
The DesktopWidget connector maps that method to
`executePlayerCommandLocal(24213, id)` (lines 7981-7985).
`NpcLinkshellChatCommand.canFire` returns
`player:isNpcLinkshellChatCalling(id)` (its recovered method body).
These calls establish the local UI-to-command route and a client guard,
not server handling or quest advancement.

The recovered tray updater compares `getLinkpearlStatus()` with -1, 0,
1, and 2 and selects hidden icon 293, visible icon 293, visible icon 292,
and animated icon 291 respectively (lines 906-944). The recovered list
updater likewise contains icon IDs 291, 292, and 293, but repeats the same
`isNpcLinkshellChatCalling(id)` condition in two adjacent branches (lines
132-146). The DesktopWidget status producer has the same duplicated-looking
predicate. That decompiler ambiguity prevents assigning a second underlying
flag or a historical calling/extra state to each icon from these bodies
alone. No Man206-specific NPC LS ID, message pack, sequence transition,
or successful retail call follows from this UI code.

## Linkshell management UI and local command checks

`PopulaceLinkshellManager.eventTalkStep22` sets the second of five choice
flags to `false` when `countCommunityGroup(20002) >= 8`, before passing the
flags to `askRestrictChoices`. Its actor-class branches select keys 128 for
1001183, 122 for 1001182, and 116 on the shared residual path; the selected
key is passed to `askRestrictChoices` (`root/proto7`, selection PCs 6-20,
offsets `0x1151`-`0x1189`, and call PCs 35-43, `0x11C5`-`0x11E5`). The
1000078 comparison also uses that residual key. These are local UI facts;
they do not establish text meanings, group capacity, or server authorization.

`LinkshellListWidget.initAsk` iterates from 1 through 8, forms each
`ListBoxItem_Linkshell_<n>` name, and writes `n` into its
`TextBlock_LinkshellNumber` child. This establishes eight named row slots that
the script addresses, not that native layout creates or displays them.

`LinkshellKickCommand.canFire` requires a non-nil alive caller for which
`isPlayer()` is true and a string group ID in argument 2. With target actor
argument 6 present, that actor must also be alive and pass `isPlayer()`;
otherwise it uses argument 3 to find a matching member unique identifier in
the group. It obtains the caller's current group of type `20002`, matches its
unique ID to argument 2, checks caller and target membership, requires the
caller's raw member rank to be at least `7`, and returns false unless that
rank is greater than the target's raw rank
(`root/proto0`, PCs 0-135, offsets `0xF6`-`0x312`; caller `isPlayer` PCs
12-14 or 35-38, offsets `0x126`-`0x12E` or `0x182`-`0x18E`; target
`_isAlive` PCs 29-32, `0x16A`-`0x176`, and target `isPlayer` PCs 39-42,
`0x192`-`0x19E`). These local command predicates do not establish server
authorization or group capacity.

`PopulaceLinkshellManager.checkLinkshellName` marks its local result false
when the string length is outside `3`-`31`, `_string.match` finds
`[^a-zA-Z0-9 ]` or `[^a-zA-Z0-9][^a-zA-Z0-9]`, or the string begins or ends
with a space. These are the visible checks in this method; they do not define
the accepted-name policy.

`PopulaceLinkshellManager.eventTalkStep2` has visible return triples with
first values `3`, `4`, and `5`. The `3` branch returns the values from the
name and icon steps; the `4` branch returns the first then second result from
`eventTalkStep24`; and the `5` branch returns the `eventTalkStep25` result
and literal `0`. Other exits return accumulated local values, including the
visible first value `10`, or `-1` with those values. These are method-level
tuple shapes; they are not assigned create, change, disband, or
server-operation meanings.

Lua 5.1 instruction PCs cross-check the tuple order: `eventTalkStep2`
(`root/proto5`) returns status 3 at PC 149, status 4 at PC 169 after copying
the first and second `eventTalkStep24` results into that order, status 5 with
the `eventTalkStep25` result and zero at PC 184, and status 10 or -1 with the
current two values at PCs 202 and 214. The payload identity is pinned in the
table below.

The decoded script and retail resource identities are pinned here:

| Script and method | Decoded source | LPB and payload identity |
| --- | --- | --- |
| `lua/scripts/chara/npc/populace/populacelinkshellmanager.lua` (`eventTalkStep2`, `eventTalkStep22`, `checkLinkshellName`) | `manifests/scripts.json:6453-6456` | `manifests/retail_lua_coverage.json:7849-7861` |
| `lua/scripts/widget/ask/linkshelllistwidget.lua` (`LinkshellListWidget.initAsk`) | `manifests/scripts.json:15021-15024` | `manifests/retail_lua_coverage.json:26973-26985` |
| `lua/scripts/command/system/linkshellkickcommand.lua` (`LinkshellKickCommand.canFire`) | `manifests/scripts.json:7491-7494` | `manifests/retail_lua_coverage.json:23974-23986` |

## Additional linkshell client routes

The following observations are from pinned retail 1.23b Lua 5.1 payloads.
Prototype paths use the root as `root` and number direct children from zero;
PCs are zero-based, and each byte-offset pair locates the first and last
instruction starts in the displayed PC span. These methods show
client control flow and presentation. They do not establish enum names,
dialog wording, server policy, or successful runtime execution.

### Manager text and widget handoffs

`PopulaceLinkshellManager.initForEvent` calls
`_loadTextDataPermanently(2221, "populaceLinkshellManager")`
(`root/proto0`, PCs 0-3, offsets `0x0387`-`0x0393`).
`eventTalkStep1` obtains the player, calls `startCliantTalkTurn(2, player)`
when non-nil, then dispatches among `eventTalkStep11`, `eventTalkStep12`, and
`eventTalkStep13(true)` based on local boolean and branch results
(`root/proto1`, PCs 3-46, offsets `0x0414`-`0x04C0`). The returned numeric
values remain unlabeled.

`eventTalkStep11` compares actor class IDs `1001183`, `1001182`, and
`1000078`. It selects text keys 78/79 and ask key 82 for the first match,
40/41 and 44 for the second, and 2/3 and 6 on the residual path
(`root/proto2`, PCs 5-44, offsets `0x0610`-`0x06AC`). The residual path is
shared with the `1000078` comparison; it is not exclusive to that ID.
`eventTalkStep12` selects keys 80/81/82, 42/43/44, or 4/5/6 for those same
branches (`root/proto3`, PCs 5-36, offsets `0x0788`-`0x0804`); only the first
two keys are passed to `say`.

`eventTalkStep13` selects `say` keys 85/86/87, 47/48/49, or 9/10/11 by the
same actor comparisons, and conditionally makes a fourth text call with key
88, 50, or 12 (`root/proto4`, PCs 0-80, offsets `0x08CB`-`0x0A0B`). These
are raw actor-class and text-key comparisons;
they do not identify an actor, location, or text meaning. The residual text
branch also serves the `1000078` comparison and is not exclusive to it.

`eventTalkStep21` selects ask key 89 for actor class 1001183, key 51 for
1001182, and key 13 on the residual path; the comparison with 1000078 does
not change that fallback. It calls `ask` with mode 2 and returns that call's
result (`root/proto6`, selection PCs 3-16, offsets `0x104B`-`0x107F`, and
ask/return PCs 19-25, offsets `0x108B`-`0x10A3`).
`eventTalkStep231` selects keys 97, 59, and 21 for those respective actor
branches, passes the selected key to `say`, then calls
`askLinkshellNamingWidget` for three results and returns the third only when
result 1 is true and result 2 equals 1; otherwise it returns an empty string
(`root/proto8`, key selection and `say` PCs 3-22, offsets `0x132E`-`0x137A`,
and widget result PCs 23-33, `0x137E`-`0x13A6`). `eventTalkStep232` selects
keys 98, 60, or 22 and passes the selected key to `say` before it calls
`askLinkshellSelectIconWidget(1, nil)`; it returns result 3 for `(true, 1)`,
0 for `(true, 2)`, or -1 otherwise (`root/proto9`, key selection and `say`
PCs 3-22, offsets `0x1481`-`0x14CD`, and widget result PCs 23-42,
`0x14D1`-`0x151D`). `eventTalkStep233` loads key pairs 100/101, 62/63, or
24/25; it passes the first key to `say`, while the second key is not consumed
later in the method. It then calls `askLinkshellConfirmWidget(1, name, icon)`
and returns result 2 for `(true, 1)`, 0 for `(true, 2)`, or -1 otherwise
(`root/proto10`, pair selection PCs 4-21, `0x160C`-`0x1650`, `say` PCs
22-26, `0x1654`-`0x1664`, and widget result PCs 29-50, `0x1670`-`0x16C4`).
These raw keys and result values do not assign text meanings or create,
modify, cancel, or server-operation semantics.

`eventTalkStep24` first selects keys 99, 61, or 23 for the respective actor
branches and passes the selected key to `say` (`root/proto11`, PCs 13-32,
offsets `0x17F3`-`0x183F`). It then asks `LinkshellListWidget` in mode 2,
checks the selected group and its alive state, reads its unique ID and crest
icon, then asks `LinkshellSelectIconWidget` in mode 2 and returns the ID with
the selected icon, 0, or -1 (`root/proto11`, PCs 33-101, offsets
`0x1843`-`0x1953`).
`eventTalkStep25` first selects keys 111, 73, or 35 for the respective actor
branches and passes the selected key to `say`; keys 112, 74, or 36 are also
loaded but not consumed later in the method (`root/proto12`, PCs 12-34,
offsets `0x1AFD`-`0x1B55`). The subsequent path asks the list in mode 3,
reads the selected group's unique ID and crest icon, passes those values to
`askLinkshellConfirmWidget(3, ...)`, then calls
`askExtendWidget(actor, textID, 2, 0, 2)`. A later text branch selects keys
115, 77, or 39 and passes the selected key to `say` (`root/proto12`, PCs
97-118, offsets `0x1C51`-`0x1CA5`). When the post-dialog result branch
retains the group getter result, that value is returned; the other paths load
the literal empty string. The getter result type is not established
(`root/proto12`, PCs 35-124, offsets `0x1B59`-`0x1CBD`; getter result at
PCs 55-58, `0x1BA9`-`0x1BB5`, return at PC 123, `0x1CB9`, and empty-string
loads at PCs 95, 120, and 122). The widget modes and result tuples do not
identify a server-side crest or group operation.

`checkLinkshellNameChinese` rejects strings with length below 3 or above 31
and strings with a leading or trailing ASCII space
(`root/proto18`, PCs 2-29, offsets `0x2396`-`0x2402`). This method shows no
character-set whitelist; it remains separate from `checkLinkshellName` and
does not define the complete accepted-name policy.

`eventTalkStepMakeupDone`, `eventTalkStepModifyDone`, and
`eventTalkStepBreakDone` call `updateGroupMemberRank` and
`finishCliantTalkTurn`; the first two also select and call a `say` text.
`eventTalkStepMakeupDone` uses keys 104 for actor class 1001183, 66 for
1001182, and 28 on the residual path. `eventTalkStepModifyDone` uses 109,
71, and 33 on those same respective paths. In both methods the comparison
with 1000078 shares the residual branch, so that key is not exclusive to that
ID (`root/proto13`, selection PCs 8-22, offsets `0x1E9B`-`0x1ED3`, `say`
PCs 23-27, `0x1ED7`-`0x1EE7`; `root/proto14`, selection PCs 8-22,
`0x1FF4`-`0x202C`, `say` PCs 23-27, `0x2030`-`0x2040`). Their method names
do not prove how they are registered or what operation result invokes them.
The text-key branches in `eventTalkStep22`, `eventTalkStep231`-
`eventTalkStep25`, `eventTalkStepMakeupDone`, and
`eventTalkStepModifyDone` compare actor classes 1001183 and 1001182, then
use the third key on the shared residual path; comparisons with 1000078 do
not make that fallback exclusive to that ID.
`updateGroupMemberRank` loops group
indices for type 20002 and calls `updateMemberInformation` and
`updateRankInGroup` for each non-nil alive group (`root/proto19`, PCs 3-24,
offsets `0x248C`-`0x24E0`).

### Desktop command bridge and local command checks

The DesktopWidget current-group wrapper returns false before command 24236
when a supplied non-nil group has no unique ID; a nil group takes the
separate nil-ID command path (`root/proto319`, PCs 0-9, offsets
`0x21165`-`0x21189`). It then makes one local command 24236 call with
`(uniqueID-or-nil, nil, 1)` at PC 15. On a true result with a
non-nil group, it refreshes member information, then returns the saved result
at PC 23 (`root/proto319`, PCs 0-24, offsets `0x21165`-`0x211C5`; command
call offset `0x211A1`, refresh PCs 20-22, return offset `0x211C1`). The
in-order wrapper selects the first type
20002 group when no current group exists, otherwise the next indexed group;
it passes nil when the current group is last and does not wrap
(`root/proto320`, PCs 0-54, offsets `0x2126D`-`0x21345`).

The invite wrappers call local command 24232: actor invite returns false
before the command when `checkActor(target)` or the resolved unique ID is
nil, otherwise passing `(uniqueID, nil, nil, nil, targetActor)`; the
current-target wrapper first checks `isInviteCurrnetLinkshellByTarget`, and
name invite returns false unless `type(name) == "string"` and the resolved
unique ID is non-nil, otherwise passing `(uniqueID, name)`
(`root/proto321`, PCs 0-13, offsets `0x2145F`-`0x21493`, and call PCs 14-21,
`0x21497`-`0x214B3`; `root/proto322`, PCs 0-19, offsets `0x2153A`-`0x21586`;
`root/proto323`, PCs 0-13, offsets `0x21665`-`0x21699`, and call PCs 14-20,
`0x2169D`-`0x216B5`). Actor and name cancellation wrappers call local
command 24233 with
`(nil, nil, nil, targetActor)` or `(name)`; the current-target wrapper
delegates with the current target actor. The actor wrapper returns false when
`checkActor(target)` is nil, and the name wrapper returns false unless
`type(name) == "string"` (`root/proto324`, guard PCs 0-6, offsets
`0x21742`-`0x2175A`, and full span PCs 0-13, `0x21742`-`0x21776`;
`root/proto325`, guard PCs 0-6, offsets `0x217DB`-`0x217F3`, and full span
PCs 0-12, `0x217DB`-`0x2180B`; `root/proto326`, PCs 0-6, offsets
`0x21875`-`0x2188D`).

The resign wrapper returns false for a missing checked current-group actor,
an owner result of true, or a nil unique ID, before calling local command
24235 with `(uniqueID)` (`root/proto327`, guard PCs 9-29, offsets
`0x21924`-`0x21974`; PCs 16-22 are the owner check). The kick wrapper
resolves a supplied group or falls back to the current
type-20002 group; it returns false when that fallback is absent or when the
group's unique ID is nil (`root/proto328`, PCs 0-20, offsets
`0x21A6C`-`0x21ABC`). It then gets the localized member name. A nil or empty
name refreshes member information and returns false without command 24234.
If the group/ID and name checks pass, it calls command 24234 once with
`(uniqueID, name)`, refreshes member information on success, and returns the
stored call result (`root/proto328`, name check PCs 21-32,
`0x21AC0`-`0x21AEC`, and full span PCs 0-44, `0x21A6C`-`0x21B1C`). The
appoint wrapper uses the same provided-group/current-group and unique-ID
gates (`root/proto329`, PCs 0-20, offsets `0x21C2F`-`0x21C7F`). A nil or
empty localized member name refreshes member information and returns false
without command 24231. If the earlier checks and name check pass, it calls
command 24231 once with `(uniqueID, name, rank)` and refreshes rank
information on success (`root/proto329`, name check PCs 21-32,
`0x21C83`-`0x21CAF`, and full span PCs 0-45, `0x21C2F`-`0x21CE3`).

DesktopWidget helper methods show these additional local contracts:

- `getLinkshellUniqueIdentifier` falls back to the current type 20002 group,
  checks the group actor's alive state, and returns its unique ID
  (`root/proto430`, PCs 0-19, offsets `0x27BF2`-`0x27C3E`). The paired
  member helper applies the same group, actor, and identifier checks; it
  returns false when the resulting identifier is nil and otherwise returns
  `(true, uniqueID, actor-or-nil)`. It calls client-membership only after
  world-membership and looks up the actor only when both predicates pass
  (`root/proto431`, PCs 0-43, offsets `0x27CDE`-`0x27D8A`).
- The member refresh helper calls `updateMemberInformation` and
  `updateRankInGroup`; the rank-only helper calls only `updateRankInGroup`
  (`root/proto432`, PCs 0-22, offsets `0x27E81`-`0x27ED9`;
  `root/proto433`, PCs 0-20, offsets `0x27F94`-`0x27FE4`).
- `getLinkshellIconID` maps 0 to 0 and other inputs to `input + 40001 - 1`;
  `getLinkshellBaseIconID` first computes `(base - 1) * 10 + 1`
  (`root/proto434`, PCs 0-7, offsets `0x28082`-`0x2809E`;
  `root/proto435`, PCs 0-6, offsets `0x280E5`-`0x280FD`).
- Current-group validity checks `checkActor` on group type 20002;
  `isMyCurrnetLinkshell` then calls `isOwner(player)` on that group
  (`root/proto436`, PCs 0-14, offsets `0x28153`-`0x2818B`;
  `root/proto437`, PCs 0-16, offsets `0x28212`-`0x28252`). The owner-name
  helper returns nil for an invalid current group; otherwise it scans for raw
  rank 10 and returns the localized name or an empty string. The icon helper
  applies the icon conversion to the current crest
  (`root/proto438`, PCs 0-32, offsets `0x282E6`-`0x28366`;
  `root/proto439`, PCs 0-18, offsets `0x2844E`-`0x28496`).
- The current-group invite predicate returns true for raw rank 7 or 10. The
  current-target predicate rejects a nil target, self, non-player, or a target
  for which the player reports relation group 50001 before delegating to that
  predicate. The invite-offer helper requires a non-nil different player
  target, requires relation group 50001, and returns whether that relation
  group's command variation is raw 10002
  (`root/proto440`, PCs 0-27, offsets `0x28550`-`0x285BC`;
  `root/proto441`, PCs 0-30, offsets `0x28668`-`0x286E0`;
  `root/proto442`, PCs 0-44, offsets `0x2879E`-`0x2884E`).
- Member-list creation supplies row index, member ID, localized name, raw
  rank, and three local flags to `setListItem`; the flags come from self,
  world/client membership, and a rank-zero check (`root/proto443`, PCs 0-66,
  offsets `0x2892F`-`0x28A37`). Member-name lookup returns nil for an invalid
  group or an ID greater than the member count (`root/proto444`, PCs 0-22,
  offsets `0x28B73`-`0x28BCB`). The online count loops over world-member
  checks, and the rank-icon helper maps raw 7 to 384, 10 to 383, and other
  values to 0 (`root/proto445`, PCs 0-31, offsets `0x28C88`-`0x28D04`;
  `root/proto446`, PCs 0-14, offsets `0x28DCC`-`0x28E04`).
- The current-community-group update method updates static widget 2's title
  for update type 1 and updates open `Ask/LinkshellListWidget` and
  `LinkshellMembersListWidget` instances (`root/proto447`, PCs 0-32, offsets
  `0x28E5D`-`0x28EDD`). Four ask wrappers open Naming mode 2, SelectIcon mode
  2, Confirm mode 1, and List mode 1 (`root/proto448`, PCs 0-5, offsets
  `0x28FB8`-`0x28FCC`; `root/proto449`, PCs 0-7, offsets `0x2903D`-
  `0x29059`; `root/proto450`, PCs 0-8, offsets `0x290CE`-`0x290EE`;
  `root/proto451`, PCs 0-6, offsets `0x29160`-`0x29178`).

The `canFire` methods for linkshell change, resign, invite, invite cancel,
and appoint check that argument 1 is non-nil, alive, and passes `isPlayer()`.
Change returns true when argument 4 is nil after those player checks. When
argument 4 equals 1, it also requires argument 2 to be nil or a string;
other argument-4 values return false (`root/proto0`, PCs 0-41, offsets
`0xF8`-`0x19C`; `isPlayer` PCs 10-12, `0x120`-`0x128`; argument-4 nil
branch PCs 16-22, `0x138`-`0x150`; argument-4 and argument-2 checks PCs
23-38, `0x154`-`0x190`). Resign requires a string in argument 2
(`root/proto0`, PCs 0-25, offsets `0xF8`-`0x15C`; `isPlayer` PCs 10-12,
`0x120`-`0x128`). Invite requires argument 2 to be a string; when actor
argument 6 is absent, argument 3 must be a string, and when it is present,
that target must be alive and pass `isPlayer()` (`root/proto0`, PCs 0-61,
offsets `0xF8`-`0x1EC`; caller `isPlayer` PCs 12-14, `0x128`-`0x130`,
and actor-path caller `isPlayer` PCs 42-45, `0x1A0`-`0x1AC`; target
`_isAlive` PCs 36-39, `0x188`-`0x194`, and target `isPlayer` PCs 46-49,
`0x1B0`-`0x1BC`). Invite cancel uses the same
name/actor split without requiring argument 2: when actor argument 6 is
present it must be alive and pass `isPlayer()`, otherwise argument 2 must be
a string (`root/proto0`, PCs 0-54, offsets `0xFE`-`0x1D6`; caller
`isPlayer` PCs 12-14, `0x12E`-`0x136`, and actor-path caller `isPlayer`
PCs 42-45, `0x1A6`-`0x1B2`; target `_isAlive` PCs 36-39,
`0x18E`-`0x19A`, and target `isPlayer` PCs 46-49, `0x1B6`-`0x1C2`).

Appoint requires a string group ID in argument 2 and compares argument 4
against numeric bounds 1 and 10, returning false for values outside that
inclusive range. With actor argument 6 present, the target must be
alive and pass `isPlayer()`; otherwise argument 3 must be a string. It checks
the current alive type-20002 group and its unique ID, requires the caller to
be a member with raw rank at least 7, requires the target to be a member, and
returns false unless the caller's raw rank is greater than the target's
(`root/proto0`, PCs 0-161, offsets `0xF9`-`0x37D`; caller `isPlayer` PCs
12-14 and 55-58, `0x129`-`0x131` and `0x1D5`-`0x1E1`; target actor alive
check PCs 49-52, `0x1BD`-`0x1C9`, and target `isPlayer` PCs 59-62,
`0x1E5`-`0x1F1`; argument-3 type check on the no-actor branch PCs 25-31,
`0x15D`-`0x175`; membership/rank checks PCs 97-110 and 131-158,
`0x27D`-`0x2B1` and `0x305`-`0x371`). These are client command guards, not
server authorization rules.

### Linkshell widgets and member rows

`LinkshellMenuSubWidget.init` stores raw ask type, ranks, member ID, and
login state; it hides Button_3, gates Buttons 1 and 2 on login, enables both
rank flags for raw my-rank 10, and enables only the Button_5 rank flag for
raw my-rank 7 with target rank 4. Those flags are combined with login for
Buttons 4 and 5 (`root/proto0`, PCs 0-104, offsets `0x238`-`0x3D8`). Its
operate handler routes Button_1 to member-name lookup and
`setTellAddress`, Button_2 to dialog type 3, Button_4 to type 1, Button_5 to
type 2, and Button_6 to call `setParentBorder` (`root/proto3`, PCs 0-45,
offsets `0x685`-`0x739`). The dialog builder uses text ID 1259 for type 1
when stored rank is 7 and 1258 otherwise, text ID 1260 for type 2, and text
ID 3725 for type 3. Type 1 also includes raw parameter 100007; type 3 uses
raw mode 3 (`root/proto5`, PCs 0-60, offsets `0x8DC`-`0x9CC`). The result
handler proceeds only for result 1, routes type 1 to
appoint with raw rank 7 changed to 4 and other ranks changed to 7, routes
type 2 to kick after a valid-current-group check, and routes type 3 to
name-based party invite after its local predicate (`root/proto6`, PCs 0-66,
offsets `0xAF3`-`0xBFB`). Its party predicate checks login, member name,
existing party membership, `isRestrictedByContents(1)`, raw command
variation values 10001/10002, party count, and leader state (`root/proto8`,
PCs 0-68, offsets `0xE19`-`0xF29`). After those gates, a party count at most
1 passes; for a larger party, it passes only when the leader check succeeds
and the count is not 8. It rejects when the first returned command-variation
value is 10001 or 10002.

Before choosing the dialog arguments, `openCommonDialogWidget` calls
`DesktopWidget.getCurrnetLinkshellMemberName(work.memberID)` and returns
immediately when that result is nil. The return precedes storing `askType`
and opening `CommonDialogWidget` (`root/proto5`, PCs 0-7, offsets
`0x8DC`-`0x8F8`). This is a local early-return condition; it does not establish
why the name lookup may return nil.

`LinkshellNamingWidget.initAsk` sets Next's raw command parameter to 1 and
Quit's to -1 and initially disables Next. On the non-Chinese path it calls
`setAcceptChars` with `"Space"`; on the other path it sets MaxLength to
`"30b"`, IsReplaceUnaccept to `"True"`, IME input to true, and
`SqwtInputAllowedChars` to `"Alphabet|Number"` before setting accepted
characters from `getUserWorkString` (`root/proto0`, PCs 0-100, offsets
`0x198`-`0x328`). The default handler enables Next when `LEN(text) >= 3`
on the non-Chinese path, or when `getZenHanLength(text)` is 3-20 inclusive
and `IsValidFirst` is not false on the other path (`root/proto3`, PCs 0-91,
offsets `0x7AC`-`0x918`). These assignments do not define a full accepted
character set or final name policy. `initAsk` also calls
`setControlCommandCondition` for `TextBox_LinkshellName` with the raw tags
`ApplicationCommands.Operate` and `UILuaCommands.TextChanged`
(`root/proto0`, PCs 24-31, offsets `0x1F8`-`0x214`). These registrations do
not prove a dispatch link from either tag to `processUICommandDefault`.

The default handler's `TabNext` route focuses enabled Next or Quit when the
current control is `TextBox_LinkshellName`; Next focuses Quit; Quit returns
to the text box (`root/proto3`, PCs 33-61, offsets `0x830`-`0x8A0`). Its
`TabPrevious` route moves from the text box to Quit, from Next to the text
box, and from Quit to enabled Next or the text box (PCs 62-90, offsets
`0x8A4`-`0x914`). These are explicit focus calls in the handler, not a claim
about any other tab-order behavior.

`LinkshellConfirmWidget.initAsk` configures Making result 1 and Back result
2; Quit result -1 is configured only in mode 1 and is hidden in the other
branch (`root/proto0`, PCs 0-85, offsets `0x131`-`0x285`). Its text IDs do
not establish prompt meanings. The emblem path passes its icon argument to
`getLinkshellIconID` and then `IconControl_Emblem` (`root/proto0`, PCs 67-73,
offsets `0x23D`-`0x255`).

`LinkshellSelectIconWidget.initAsk` configures named Button_Icon controls
1-58; it does not create those controls. It declares `_temp` fields
`iconBaseID`, `selectBaseID`, and `oldIconID` as `integer32`, and `iconColor`
as `integer8` (`root/proto0`, PCs 0-19, offsets `0x1AC`-`0x1F8`). A nil old
icon selects base/color 1/1; otherwise base is
`floor((oldIconID - 1) / 10) + 1` and color is
`((oldIconID - 1) % 10) + 1`
(`root/proto0`, PCs 34-57 and 122-143, offsets `0x234`-`0x290` and
`0x394`-`0x3E8`). In both cases it initializes the child
`LinkshellIconListWidget` with `false` (`root/proto0`, PCs 146-149, offsets
`0x3F4`-`0x400`). Its operate handler routes base buttons to the parent and
other parameters to the child icon list (`root/proto1`, PCs 0-26, offsets
`0x6D4`-`0x73C`). `getIconID` returns
`getLinkshellBaseIconID(base) + color - 1` (`root/proto5`, PCs 0-6, offsets
`0xA05`-`0xA1D`); `getAskResult` converts that value to
`iconID - 40001 + 1` and uses raw result 2 when it equals a nonnegative old
icon (`root/proto3`, PCs 0-21, offsets `0x88F`-`0x8E3`).
The child list uses 7 entries for base 1 and hides buttons 8-10; other bases
use 10 entries with each icon value computed as the base icon minus one plus
the color index (`LinkshellIconListWidget.setIconBaseID`, root/proto3, PCs
0-46, offsets `0x373`-`0x42B`). The icon-list initializer binds
`Button_Icon_1` through `Button_Icon_10` to command parameters 1 through 10
(`LinkshellIconListWidget.init`, root/proto0, PCs 12-15, offsets
`0x180`-`0x18C`). When its operate handler receives a non-nil parameter, it
passes that value to the parent `setIconColor`, hides itself, and returns
(`root/proto1`, PCs 7-16, offsets `0x298`-`0x2BC`).
`LinkshellSelectIconWidget.setIconColor` calls
`setSelectedIcon(work.selectBaseID, color)` (`root/proto4`, PCs 0-5, offsets
`0x994`-`0x9A8`); `setSelectedIcon` stores the base and color, computes the
icon ID, then calls `setIcon` for `IconControl_SampleEmblem`
(`root/proto6`, PCs 0-12, offsets `0xA85`-`0xAB5`). These routes do not
identify icon art or why base 1 has fewer entries.

`Ask/LinkshellListWidget.update` calls `createList` (`root/proto4`, PCs 0-2,
offsets `0x0B7D`-`0x0B85`). `Ask/LinkshellListWidget.createList`
(`root/proto3`, PCs 0-138, offsets
`0x665`-`0x88D`) reads the count of type-20002 community groups and builds
rows from the indexed groups. It passes text ID 33626 and each group to
`setTextWorldMaster`; the online-count text uses ID 228, the result of
`getLinkshellOnlineMemberCount(group)`, and the returns of
`group:_countMember()`. It gets the rank icon for `IconControl_Reader` and
passes the `getCrestIcon` result through
`DesktopWidget.getLinkshellIconID` before writing `IconControl_Emblem`. It
toggles `IconControl_Current` for the current group,
hides unused row slots through 8, and switches the empty and list controls
when the count is not positive. The rank-help IDs are 79246 for raw rank 7
and 79203 for raw rank 10. The helper's icon mapping is documented above;
text, rank, and icon meanings remain unassigned.

`Ask/LinkshellListWidget.processUICommandSelectionChanged`
(`root/proto2`, PCs 0-26, offsets `0x520`-`0x588`) opens
`LinkshellListSubWidget` at the parent position plus `(240,60)` when
`work.mode == 1`, setting its border to `selectedIndex + 1` only after a
successful open. Other modes call `setBaseAskResult(selectedIndex + 1)`.
`processUICommandClose` (`root/proto1`, PCs 0-12, offsets `0x45E`-`0x48E`)
closes directly in mode 1 and otherwise calls `setBaseAskResult(-1)`. These
methods do not establish the list control's index convention outside their
own calls or later ask-framework effects.

`LinkshellListSubWidget.init` (`root/proto0`, PCs 0-82, offsets
`0x18E`-`0x2D6`) compares the selected group with the current group. It
sets `work._temp` to an `index` field of type `integer8`, stores the raw
selected index in `work.index`, sets modal state and position, and confirms
Button_6 in both cases. For the current group it confirms Buttons
1, 2, 4, and hides Button_3; it confirms Button_5 only when
`isMyCurrnetLinkshell()` is false. For another group it confirms Button_3
and hides Buttons 1, 2, 4, and 5. The button labels are not recovered here.
In `processUICommandOperate` (`root/proto3`, PCs 0-103, offsets
`0x59D`-`0x739`), Button_1 requires a valid current group, then calls static
widget 2's `setChatMode(5)` and focuses it; Button_2 requires a valid
current group and opens `LinkshellMembersListWidget`; Button_3 obtains the
selected group and calls `executePlayerSetCurrentLinkshell(group)` once,
then clears the parent border and closes only on a true result. Button_4
calls the same helper without a group and closes only on a true result.
Button_5 is offered only for the selected current group when the player is
not its owner; its operate branch requires a valid current group and opens
`CommonDialogWidget` with `(nil,1213,2,2)`. Its result-1 handler calls
`executePlayerLinkshellResign()` only if the group is still valid and the
player is not the owner, but it clears the parent border and closes on every
result-1 path. Button_6 calls `setParentBorder()` and closes directly. The
helper calls the parent `setBorder(-1)` only when a parent exists
(`root/proto5`, PCs 0-7, offsets `0xA75`-`0xA91`). The numeric dialog and
chat arguments and button labels are not assigned meanings.

`LinkshellMembersListWidget.init` (`root/proto0`, PCs 0-46, offsets
`0x224`-`0x2DC`) sets modal state and configures the back/list display
conditions. With a valid current group it sets the group title with text ID
33626 and the current crest icon; otherwise it hides the emblem icon. It then
calls `createMemberList`. Its operate handler closes directly
(`root/proto1`, PCs 0-4, offsets `0x527`-`0x537`). Its default handler calls
`updateLinkshellMemberInformation()` only for the raw command
`UILuaCommands.Shown` (`root/proto3`, PCs 0-9, offsets `0x81A`-`0x83E`).
`createMemberList` clears all `ListBox` properties before updating the list.
`updateMemberList` delegates row population to
`createCurrnetLinkshellMemberList`, updates the property list, then calls
`updateMemberInformation`; that method counts rows whose `StatusIcon == 385`
and calls `setText("TextBlock_OnlineMember",228,count,listPropertyCount)`
(`root/proto4`, PCs 0-13, offsets `0x8BC`-`0x8F0`; `root/proto5`, PCs 0-9,
offsets `0x986`-`0x9AA`; `root/proto6`, PCs 0-23, offsets `0xA51`-`0xAAD`).
The connector emits members by indices 1 through `_countMember()` in that
sequence; it does not establish native actor sorting or order semantics
(`root/proto443`, PCs 0-66, offsets `0x2892F`-`0x28A37`).

`LinkshellMembersListWidget.setListItem` stores its arguments as MemberID,
MemberRank, IsPlayer, IsClient, and IsLogin, then sets Selected to
`"Collapsed"` (`root/proto7`, PCs 0-112, offsets `0xB72`-`0xD32`). It also
sets RankIcon from the rank-icon helper, RankIconVisibility to `"Hidden"`
only when that icon is 0, MemberName using text ID 230, and RankIconHelp to
79247 for raw rank 7 or 79218 for raw rank 10. StatusIcon, StatusIconHelp,
and ItemColor default to `385`, `79217`, and `"1"`; when input IsLogin is
false they become `386`, `79221`, and `"0.5"`. The helper's rank-icon
mapping is documented above. These assignments do not assign rank titles,
icon art, help text, color meaning, or online policy.

`LinkshellMembersListWidget.processUICommandSelectionChanged`
(`root/proto2`, PCs 0-65, offsets `0x58D`-`0x691`) returns for an invalid
current group, raw IsLogin false, or raw IsPlayer equal to 1. It reads
IsClient but does not branch on it. Otherwise it opens
`LinkshellMenuSubWidget(myRank, memberID, targetRank, IsLogin)` and sets the
border only when the child opens. The connector sets IsLogin from
`_isExistInWorldMember`, sets IsClient only inside that world-member branch,
sets IsPlayer when the member actor equals the current player, and clears
IsClient for rank zero. This population path does not emit an IsLogin-false,
IsClient-true row; no broader login or membership meaning follows from these
local fields.

`NpcLinkshellListWidget.searchFirstCall` scans UI ordinals in order, calls
`isNpcLinkshellChatCalling(index)` once per row, and keeps both returned
values. It returns the earliest row where both values are true; if there is
none, it returns the earliest row with the first value true; otherwise it
returns literal 1 (`root/proto8`, PCs 0-46, offsets `0xDEE`-`0xEA6`). The
method does not name either returned value's meaning.

### Linkshell icon event state

`CharaBaseClass.initEventSyncWork` declares `eventTemp.linkshellIcon` as
four `integer16` elements and maps the `linkshellIcon` sync entry
(`root/proto6`, PCs 15-21 and 65-73, offsets `0x7B1`-`0x7C9` and
`0x879`-`0x895`). `getLinkshellIconId` returns the four values for player or
retainer game parameters and four zeroes otherwise (`root/proto5`, PCs
17-33, offsets `0x65D`-`0x69D`). The DesktopWidget character-parameter
update handler treats key `linkshellIcon` by updating static widget 2's
title and refreshing an open `Ask/LinkshellListWidget` (`root/proto78`, PCs
378-392, offsets `0xF7F3`-`0xF82B`). The field order and meanings, event
producer, and server-side source of these values remain unknown.

### Additional pinned source identities

LPB SHA-256 values are pins in the coverage manifest; the corresponding
retained decoded `.luac` SHA-256 values match its `decodedPayloadSha256`.
Manifest locators refer to `manifests/retail_lua_coverage.json`.

| Script | Manifest locator | LPB SHA-256 | Payload SHA-256 |
|---|---|---|---|
| `chara/charabaseclass_event.lua` | 5880 | `00212FC3146E5DB067FBF48436B16B50CBBCEB23618C69C1F4015079D60BBE66` | `5D5B10D8F36B08C01894D101679E19DC150AF33D6B18B1A84EA5F29E5AC468AF` |
| `chara/npc/populace/populacelinkshellmanager.lua` | 7860 | `C5ECAFC5F14E716A4692C66486BF44419226A5B6C36E2CB36756B834157D6C5E` | `24CD6CE5AC4C20B2F09B872D7BDBE0BA9BB81EA978B9E935BAD44D076B0BF565` |
| `widget/desktopwidget_connector.lua` | 25454 | `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425` | `685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621` |
| `command/system/linkshellchangecommand.lua` | 23940 | `D37CC54E1FFEE41296B6DF528EF145E0F200EF8C3FF939CD7FB6DC1B8C0783A1` | `306BD136D083AC6B57314C0AC6BDDD0267D8A108A1813EB2DCBB1406CCEC3394` |
| `command/system/linkshellresigncommand.lua` | 23970 | `3B5CD195995B565496175707BACEA746D9E4B45FD6DAF91B74FA4AEF71046EB6` | `7A6972F9F091DE177E688B329403667B40DBE7F8AD5FAAADF1C81628684F9388` |
| `command/system/linkshellinvitecommand.lua` | 23925 | `5C51D6EE2BA9E050C6ED5196A8DC25E2F699E2D10E7DA933F70FEFE87F0D72E8` | `4D918167FC36DEEB4715AB504F6328DE53705F57145F5EA935DAF2E24FAAC00C` |
| `command/system/linkshellinvitecancelcommand.lua` | 23910 | `91A5253A78530CE8C8CEF0B533F0A5BAF0D3D2E937F2F565EDA81527A520C8BC` | `FB6D7F7973B7A59FF066769113028E4FDECD73D7592D421C76E7849BDDB5CF6F` |
| `command/system/linkshellappointcommand.lua` | 23955 | `FD15F648C719B10DE33A67B061AD96433768C362BCD8B05731979C9B05C88363` | `7428C51FB4BFFF9A65F875DFFB4107E8064CE39FC63576C569D8ABCE6D0827E3` |
| `command/system/linkshellkickcommand.lua` | 23985 | `38E0602D26D343C9FCA64629EB6A5A392792C7AF033E5EFDEFE53E3C8A65FF99` | `7695F875032873DF409B48CE864AD634CABC4F0863964A28E9DFAC1B5C35D496` |
| `widget/ask/linkshellconfirmwidget.lua` | 26939 | `C77C26A0F457EC00C11D76F364A7E01E22EE8B9F053555577A7165DE19D41D25` | `3475D292A86380C46E3BB0B793320B68BE2729B4469C65FE91D9CE6F78CF705F` |
| `widget/ask/linkshellselecticonwidget.lua` | 26954 | `2E6B806B20215812546910D054E19F7087518192ED0DC832A2C1A82AB23AAF1A` | `FA031958FE041FAB7DAB969E43FF9AED4FBA0CBEEF740582479A3DF0F13F341F` |
| `widget/ask/linkshellnamingwidget.lua` | 26969 | `7887717AE56C891C81D9B67F25AABAD8285324EB8BA7D737C34E50D337692F1D` | `298BBD90663303B87679867FEF424D9C06670C1E0A43968F2043A119A8806D05` |
| `widget/ask/linkshelllistwidget.lua` | 26984 | `12E80352377EDB49A0B4B00AA2558B5F0C1633143852C3E11D7A6C1C57A22A7F` | `A5D3987DCBB9602592EA77BE5F67E2ECFBA77B3E67CDCD1C940132D41AD0BB2B` |
| `widget/npclinkshelllistwidget.lua` | 27794 | `587178C19D85620750D2ADBBC52F62F94EC705F7E5F4BC5F7F9B1364AD2E8A16` | `0021720833324E4D8A0BFC2AA8FBD25C863051C585028BE754DE13F4DF354468` |
| `widget/linkshelliconlistwidget.lua` | 27914 | `8ADB6128D72426B1CD780A18DA77F368E71B5432398347F22BBB4F6AC0AE07C5` | `4C606E192010A9387A23FF39188DBDBEAB10016A268E84D15BEE6E82E0C885B9` |
| `widget/linkshellmenusubwidget.lua` | 27944 | `A3CFEBE12F68A68018329E7F3996EA743E6A0AB57691D7CB3CCF458BB4DD7399` | `DC30DCFA5243196DA3AE2BD93E9A8D6DB98CB7AC9F4AFA3BDBA1328EE3328FCF` |
| `widget/linkshellmemberslistwidget.lua` | 27959 | `641DEBD065530ED86852C6CC39258A36B7D54B1134154E9B96CC0D9F729DDE42` | `3F3EA163C1CDDC2860E8FBDB447581476AD108708B9E0709997F5F3FCFBA8374` |
| `widget/linkshelllistsubwidget.lua` | 27989 | `D52FF28F40B63656E3CA9AE3F20D6F7AF79B7C9F75EC2C0593F87AEAF7B9EF99` | `0CF67CE8C56FA8274EEDF3A8B4114773079E26DFA4E8833AA5865953EDF37758` |
