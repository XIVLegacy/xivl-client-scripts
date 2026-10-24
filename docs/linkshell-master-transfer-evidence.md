# Linkshell master-transfer evidence

No manual master-transfer issuer was found in the authenticated recovered
1.23b Lua corpus. The member menu appoints or removes a **leader**, using
requested ranks 7 and 4. Its local user must be a master, rank 10. That
requirement is not a request to make the selected member a master.

The command predicate admits a caller-supplied requested rank 10, but no
rank-10 issuer, separate transfer command, transfer-specific completion
receiver or request/reply specimen is established. This is a bounded
negative finding for the recovered scripts and inspected bytecode. It is
not a claim that every native path, computed command or server-authored
event in every 1.x release lacked transfer support.

## Caller and operand domains

All script locators below are relative to `lua/scripts/`. The source revision
and original-resource pins are recorded under [Reproduction](#reproduction).

| Step | Direct observation and locator |
| --- | --- |
| Select member | `widget/linkshellmemberslistwidget.lua:128-162` passes local rank, selected rank, selected member index and login flag to the submenu. Self/offline selections return earlier at 116-126. |
| Construct selection identity | `widget/desktopwidget_connector.lua:19348-19403` iterates one-based group member indices and passes the original index to `setListItem`. `linkshellmemberslistwidget.lua:347-360` stores it as `MemberID`. The visible row counter is a separate zero-based value. |
| Admit appoint UI | `widget/linkshellmenusubwidget.lua:55-123` enables the appoint control only for local rank 10. Button_4 opens ask type 1 at 202-206. |
| Accept confirmation | `linkshellmenusubwidget.lua:323-346` requires answer 1 and ask type 1, then chooses requested rank 4 when the selected existing rank is 7, otherwise 7. The only named appoint-helper call is at 341. |
| Resolve group/member | `desktopwidget_connector.lua:15376-15414` resolves a nil group to the current type-20002 group, obtains its string UID with `getLinkshellUniqueIdentifier`, and reads `_getMemberLocalizedDisplayName(memberIndex)`. |
| Dispatch | `desktopwidget_connector.lua:15416-15422` calls `executePlayerCommandLocal(24231, groupUID, memberText, requestedRank)`. It forwards the supplied rank unchanged. |

The [shared command contract](linkshell-party-command-contracts.md#shared-dispatch-and-wire-representation)
owns the dispatch bridge and serializer. The conditional direct native
fallback is MapServerbound `0x012D`, event `commandRequest`, with a command
object control reference in the envelope. Command sheet ID 24231 (`0x5EA7`)
is not an additional tail operand. The nine values after the command object
are:

```text
(group UID string, member string, requested rank integer, nil x6)
S(groupUID), S(memberText), I(rank), N x6, E
```

`S` is tag `02`, string bytes and NUL. `I` is tag `00` followed by four
big-endian integer bytes. `N` is explicit nil tag `05`, and `E` is terminator
`0F`. This describes the known appoint input, not an observed transfer
payload. Substituting 10 does not establish a supported transfer operation.

The selected UI `MemberID` is a member index. It is replaced by a string
before dispatch. The outgoing member operand is therefore not a numeric
character ID on this caller. The group UID is the selected group's
`getUniqueIdentifier()` string, not its display name or a member identifier
(`desktopwidget_connector.lua:18874-18898`).

`CompanyGroup.getMemberUniqueIdentifier` bounds-checks its member index and
tail-returns `_getMemberDisplayName(index)`
(`group/communitygroup/companygroup.lua:464-479`). The appoint predicate
compares that first result with the supplied member string at
`command/system/linkshellappointcommand.lua:140-145`.
The native relationship is recorded in
`xivl-decomp:docs/event/group-member-name-getters.md`: both getters return
the same stored string through the same result helper when the descriptor's
first dword is `-1`, for the same member and unchanged state. The other
getter branch returns a numeric descriptor value whose semantic ID domain
remains unresolved. The finding does not establish that every linkshell
record selects the string branch. The method name alone must not be read
as a character-ID domain.

## Requested rank 10 and separate-command search

`LinkshellAppointCommand.canFire` rejects requested ranks below 1 or above
10 in both target alternatives (`linkshellappointcommand.lua:46,90`). Its
remaining checks require the matching live current group, local membership,
local rank at least 7 and local existing rank greater than the selected
member's existing rank. It does not cap requested rank below 10 or below
the local existing rank. Thus 10 passes the range test if all other
requirements pass. No live execution or server acceptance was observed.

There is one literal 24231 dispatch and one named helper caller in all
2,671 authenticated sources. The former forwards a variable, while the
latter constructs only 4/7. No recovered UI caller issues 24231 with 10.
No separate master-transfer command was identified by the bounded searches
below.

The inspected text-command route does not add an issuer.
`desktopwidget_connector.lua:21662-21746` handles text-command ID 330 by
selecting the current shell by index/name. Its complete original dispatcher
prototype contains neither an appoint-helper reference nor constant 24231.
The native `_parseTextCommand` implementation, generic GM/debug commands,
computed IDs and dynamically constructed method names are outside this
negative literal-caller result.

## Completion and messages

No transfer-specific completion packet or Lua event was joined to a request.
The appoint helper's synchronous true return only establishes local command
admission. Its subsequent member/rank refresh calls are not evidence of a
server mutation or transaction completion.

The native Group `0x017A` update route, generic `0x0130` function delivery
and `SendLogReceiver` are recorded in
`xivl-decomp:docs/event/group-member-name-getters.md`. None establishes a
master-transfer acknowledgment or mandatory reply order.

The static text finding
`xivl-client-data:docs/linkshell-rank-message-rows.md` identifies
`worldMaster.csv` generic success rows 25168, 25172, 25176 and 25179,
authority refusal 25177 and failure 25178. It preserves the
`xtx/communityMember`, display-name and group-name formatting expressions.
Their runtime parameter banks and transfer-specific delivery bindings are
not established. In particular, there is no supported actor/new-master/
other-members message split or typed transfer-reply tuple. An exact search
for 25168-25179 in every authenticated Lua member found no literal reference.

The static rank labels distinguish member 4, leader 7 and master 10.
UI tooltip IDs 79222/79223 describe changing **leader** privileges, whereas
79203/79218 identify the master. These labels support the role distinction
without adding a transfer request.

## Capture and backend boundaries

`xivl-captures:studies/group-combat-wire-contracts/linkshell-master-transfer.md`
records the authenticated full-corpus search. It identifies no transfer
request/reply specimen: none of the 126 `0x012D` typed windows contains
integer 10, including the 19 `commandRequest` records. The capture finding
owns the exact input pins, predicates, framing checks and group-header limits.
It does not establish feature absence outside the retained corpus.

`xivl-opcodes:opcodes.json` at revision
`5ce6aaec6ce6d122e62211a1b7915cc6f7e56ce7` contains these rows:

| Entry | Catalog state | Supported conclusion |
| --- | --- | --- |
| `0x1026`, `ModifyLinkshellPacket` | `world_map_backend`, direction `backend`, note `map_to_world`, confidence `blocked` | Existing backend label only. No retail payload or client request binding. |
| `0x1032`, `LinkshellRankChangePacket` | Same state | Existing backend label only. No retail rank operand, member identity or transfer semantics. |

Both have null implementation/decompilation anchors, empty observations and
empty payload-length lists. The opcode policy describes backend rows as
server-to-server. These labels do not prove retail linkshell semantics,
what either entry carries, or a relationship to 24231. Their layouts and
manual-transfer relevance remain unresolved.

## Pinned supporting findings

These revisions retain the promoted observations cited above:

| Citation | Revision |
| --- | --- |
| `xivl-client-data:docs/linkshell-rank-message-rows.md` | `492c0e2701747bf63e91cb7ce419e9743f63c3f5` |
| `xivl-decomp:docs/event/group-member-name-getters.md` | `dbc521ee685a2f3af6773dfcd46953cece62bd74` |
| `xivl-captures:studies/group-combat-wire-contracts/linkshell-master-transfer.md` | `0891d86152749863c0e64eb7d09a8f88086307c4` |

## Reproduction

The source baseline is `xivl-client-scripts` revision
`41150d44ffcf98d0ccac65ac2e1f23ad0cb15ba6`.
[scripts.json](../manifests/scripts.json) SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`
pins all 2,671 decoded members. The archive declared by
[private_lua_corpus.json](../manifests/private_lua_corpus.json) has 14,385,427
bytes and SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Every member matched its source-manifest size, line count and SHA-256.

Search the authenticated source bytes case-insensitively with Python `re`
or `rg` using these expressions, then inspect the matching callers:

```text
(?<!\d)24231(?!\d)|0x0*5ea7\b
LinkshellAppoint|linkshellappoint
transfer|setOwner|changeOwner|setMaster|changeMaster|newOwner|newMaster
(linkshell|linkpearl|company|community|group).*(master|owner|transfer|leader|appoint)|(master|owner|transfer|leader|appoint).*(linkshell|linkpearl|company|community|group)
set.*rank|rank.*set|change.*rank|rank.*change
(shell|pearl|company|group).*(give|pass|succ|inherit|chief)|(give|pass|succ|inherit|chief).*(shell|pearl|company|group)
```

The named/literal appoint hits are its class declarations, helper definition,
single helper call and single 24231 dispatch above. The wider expressions
add ownership readers, current-shell selection and unrelated item/retainer
transfer or UI rank methods. They add no alternate transfer issuer. Literal
searches do not exclude computed or dynamically named routes.

The original resources for the connector, submenu, member list and appoint
class matched wrapper and decoded-payload hashes in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json), SHA-256
`46fd1b388a883c0f70fc8a0bae27d08e05a1bfd776ffcac094a6b1ddd4b9d9f4`.
Use `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader` at the source baseline to inspect
these decisive original-bytecode locations. PCs are zero-based Lua 5.1
instruction indices; byte offsets are into the decoded payload.

| Resource/prototype | Original-bytecode observation |
| --- | --- |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, connector `root/proto329`, PCs 33-38, `0x21CB3-0x21CC7` | Loads 24231, moves the supplied rank unchanged and calls `executePlayerCommandLocal`. |
| `n1635q/y1wzr25yyx5wprp8n1635q.le.lpb`, submenu `root/proto6`, PCs 10-14, `0xB1B-0xB2B`; PCs 16-21, `0xB33-0xB47` | Selects rank 4 or 7 and passes it with nil group and the selected member index to the appoint helper. |
| Same submenu, `root/proto0`, PCs 31-44, `0x2B4-0x2E8` | Local rank 10 enables the appoint flag. Local rank 7/selected rank 4 enables only the separate kick flag. |
| `7vxx9w6/rlrq5x/y1wzr25yy9uuv1wq7vxx9w6.le.lpb`, predicate `root/proto0`, PCs 32/34 and 72/74, `0x179/0x181` and `0x219/0x221` | Requested-rank bounds reject only values below 1 or above 10. |
| Connector `root/proto463`, start `0x2A16A`, all 2,147 instructions and constants | Current-shell selection is its only linkshell operation. No appoint reference or 24231 constant occurs. |

This finding establishes what the named sources and finite original
prototypes contain. A whole-client absence claim, a rank-10 transfer request
layout and a causal completion/message contract require an additional retail
caller or receiver join.
