# NMRush guide and Director01 client contract

`PopulaceNMRushGuide` passes a supplied talk argument through and returns the
first customization result after finishing talk. `QuestDirectorNMRush01`
starts content information on states 1 or 2 only when its timer flag is
exactly Boolean false. State 3 always requests cancel without resetting the
flag. These are client call contracts, without an established admission,
encounter progression or reward producer.

## Source identity

The resources below are relative to retail `client/script/`. Decoded paths
are beneath `lua/scripts/`. Class mappings are in the
[registry](../lua/registry.json); original and canonical identities are in
the [coverage](../manifests/retail_lua_coverage.json) and
[script](../manifests/scripts.json) manifests.

| Artifact | Guide | Director01 |
| --- | --- | --- |
| Resource | `729s9/wu7/uvupy975/uvupy975wxspr23p165.le.lpb` | `61s57qvs/tp5rq/tp5rq61s57qvswxspr2ji.le.lpb` |
| Original bytes | 3193 | 1936 |
| Original SHA-256 | `681C5C462DE0268B4E54EBCB90A1E0FCFEFF061CC4282FCC1ED7E21269B09C56` | `5A0B0B7524E0A6B0B9FA1DADB5FB1D7A0708DC8864AA1FE1BE9AB9248437D04E` |
| Payload bytes | 3180 | 1923 |
| Payload SHA-256 | `63DCA3ED3F761E491484A8551E85877E3FE5E308D0DCCE343B5EB72209FC73B5` | `E271622889764302C94C94878C2370356256B24F9480DDF72138F61F5BB319D2` |
| Decoded path | `chara/npc/populace/populacenmrushguide.lua` | `director/quest/questdirectornmrush01.lua` |
| Canonical bytes / lines | 6605 / 355 | 3569 / 197 |
| Canonical SHA-256 | `0540EAEF9635883C898D1DCA2B7286301A324C64AA02E6CC81ADB23422FEDB13` | `E73ABD30092591D113B0EF002A77417D5DFAAEF13B4A0C106FACFC16864AE24E` |

Reproduction with [retail_script.py](../tools/retail_script.py), the
[pinned unluac](../tools/vendor/unluac/PROVENANCE.json), and the documented
CRLF-pair-to-LF normalization matched both canonical manifests exactly.
The observations below use raw Lua 5.1 operands, independently of decompiler
control-flow presentation.

## Guide arguments and results

`initForEvent(self)` loads text data with
`(10608, "populaceNMRushGuide")`, calls `_setGroundOn(false)`, and returns
no values. Each selected event method takes `(self, A1)` and passes A1
unchanged to `self:startCliantTalkTurn(mode, A1)`. The methods do not resolve
A1 through `_getMyPlayer` or establish its native type.

| Method | Talk mode | Scheduler | Ordered `self:say(self, id, 0)` IDs | Customization call |
| --- | ---: | ---: | --- | --- |
| `processWarpAsk` | 2 | `354066432` | 19, 20 | `self:askForCustomizeOption(self, 1, false, true, 21, {22,23,24})` |
| `processBattleAsk` | 2 | `354103296` | 29, 30, 31 | `self:askForCustomizeOption(self, 1, false, true, 32, {33,34,35})` |
| `processContentEndAsk` | 1 | `69165056` | 46, 47 | `self:askForCustomizeOption(self, 2, false, true, 48, {49,50})` |
| `processBattleEnd` | 1 | `70828032` | 44 | None |

The order is talk start, scheduler, the listed `self:say` calls, customization
where present, then `self:finishCliantTalkTurn()`. Warp additionally calls
`worldMaster:say(self, 3, 45, 4)` and `worldMaster:say(self, 51)` between
its self messages and customization. Those calls have different receivers.
The text arguments do not establish the uninspected text bodies' meanings.

The three ask methods retain exactly one customization result and return
exactly that one value after finishing talk. Extra results are discarded;
an absent result becomes nil in the single returned position. No branch
interprets it as an admission or end decision. `processBattleEnd` returns
zero values. Presentation helper results are discarded.

## Director01 state branches

`processUIUpdate(self, A1)` reads `self.work.directNumber` once; A1 is unused.
Its state comparisons use numeric 0, 1, 2 and 3. The timer comparisons use
the Boolean constant false, rather than Lua falsiness.

| State | Timer precondition | Client action and explicit write |
| --- | --- | --- |
| 0 | Unused | No widget call or timer access/write |
| 1 or 2 | Exactly Boolean false | `desktopWidget:processUpdateContentsInformation(self, "start")`, then `self.work.timer=true` |
| 1 or 2 | Any other value | No call or write |
| 3 | Unused | `desktopWidget:processUpdateContentsInformation(self, "cancel")`; timer unchanged |
| Other values | Unused | No call or write |

Every branch returns zero values, without falling through to another state's
action. The start flag is written after the call returns. Repeated state-1/2
updates therefore start once while the flag remains true; every state-3
update requests cancel. Nil and numeric zero do not satisfy the exact-false
test. Uninspected callees may have additional effects.

The [quest Director finding](content-director-ui-contracts.md#quest-content-information-directors)
owns the separate initialization, title and finalization evidence. This
bytecode result applies to Director01's update method; Director02's exact
update control flow remains unresolved.

## Bytecode locators and evidence boundary

Children are zero-based beneath each root. PCs are one-based, with zero-based
decoded-payload offsets. Original LPB offsets are payload offsets plus 13
before XOR decoding. Root closure assignments bind the named child methods.

| Method | Child / canonical lines | Key CALL or RETURN PCs and payload offsets |
| --- | --- | --- |
| Guide initialization | 0 / 11-22 | Load 4 at `0x1DB`; ground 7 at `0x1E7`; empty return 8 at `0x1EB` |
| Warp ask | 1 / 27-84 | Option 42 at `0x30D`; finish 44 at `0x315`; one-value return 45 at `0x319` |
| Battle ask | 3 / 134-183 | Option 35 at `0x62D`; finish 37 at `0x635`; one-value return 38 at `0x639` |
| Content end ask | 6 / 287-328 | Option 29 at `0xA9C`; finish 31 at `0xAA4`; one-value return 32 at `0xAA8` |
| Battle end | 7 / 333-353 | Finish 14 at `0xBCC`; empty return 15 at `0xBD0` |
| Director01 update | 1 / 67-118 | Start calls 17/32 at `0x3F6/0x432`; flag writes 19/34 at `0x3FE/0x43A`; cancel call 43 at `0x45E`; empty return 46 at `0x46A` |

Director timer equality tests are PCs 11/26 at `0x3DE/0x41A`; unequal
values jump to PC46 through PCs 12/27. The cancel-state equality test is
PC37 at `0x446`, with unmatched values jumping to PC46 through PC38.
The three option CALLs use `A=3 B=8 C=2`; their operative RETURNs use
`A=3 B=2`. Director start/cancel calls use `A=3 B=4 C=1`.

The [Skirmish timer consumer](myplayer-timer-consumers.md#scalar-consumer-map)
connects the NMRush timer API to the displayed status label. It does not
identify an actual guide NPC, site, instance or event dispatcher. The selected
bodies leave unresolved the caller supplying A1, the consumer of the returned
option value, and the producer of synchronized `directNumber`/`limitTime`.
No server policy or live encounter follows from the static UI contract.
