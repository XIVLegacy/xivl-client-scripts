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
flags to `askRestrictChoices`. This is a local UI gate; it does not establish
group capacity or server authorization.

`LinkshellListWidget.initAsk` iterates from 1 through 8, forms each
`ListBoxItem_Linkshell_<n>` name, and writes `n` into its
`TextBlock_LinkshellNumber` child. This establishes eight named row slots that
the script addresses, not that native layout creates or displays them.

`LinkshellKickCommand.canFire` obtains the caller's current group of type
`20002`, checks caller and target membership, requires caller rank at least
`7`, and compares caller rank as greater than target rank. This local command
predicate does not establish server authorization or group capacity.

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
