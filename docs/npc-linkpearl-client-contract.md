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
