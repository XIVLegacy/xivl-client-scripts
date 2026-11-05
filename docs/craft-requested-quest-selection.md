# Requested Items quest selection

`CraftJudge.selectCraftQuest` converts a completed journal selection into a
current player quest value. It consumes three UI results: completion status,
`JournalIndex`, and a local-guildleve flag. It does not return the visible row
ordinal, the row's `JournalID`, or that flag. A completed Close produces index
0 and therefore one nil result from the judge. A failed UI selection also
produces one nil, through a different branch.

The [local supplies contract](local-guildleve-supplies-contract.md#requested-items-and-recipe-presentation)
owns the Requested Items context and its attributable captured invocation.
That invocation carries no explicit method arguments and does not establish
this adapter's returned value. The contract here comes from authenticated
retail 1.23b scripts and their original Lua 5.1 instructions.

## Selected opening and result tuple

The judge receives `self,A1,A2`. It calls `A1:isPlayer()` and returns zero
values only when that result is exactly false. Nil and numeric zero do not
satisfy that test. A2 is unused. The next call is
`desktopWidget:askPassiveGuildleveSelectWidget()` with no arguments after
the desktop receiver, requesting exactly three results. Missing results are
nil-padded and extras discarded.

The selected helper tailcalls
`askEventModeWidgetYield("Ask/JournalListWidget",2,3)`. Here 2 is the
requested widget-result count and 3 is the journal mode. The event-mode helper
inserts opener mode 4 and tail-forwards to `askWidgetYield`. The resulting
opening request, after the desktop receiver, is exactly:

`openWidgetYield(4,"Ask/JournalListWidget",nil,nil,false,3)`

The raw nil/nil/false positions are preserved. This request does not prove
native creation or that its last argument reaches the named Lua initializer.
The selected journal behavior below is conditional on dispatch to the
published Ask module with mode 3.

| Generic wrapper condition | Results forwarded to the judge | Requests on the normal return path |
| --- | --- | --- |
| Opening returns nil | One false | No selection, result getter, or close call. |
| Opening returns W, selection is not exactly true | One false | `selectWidgetYield(W,true)`, then `closeWidgetDirect(W)`; no result getter. |
| Opening returns W, selection is exactly true | `true,R1,R2` | Select, read all actual `W:getAskResult()` results into a table, request close, then return only result positions 1 and 2 after true. |

The explicit two-result unpack preserves nil in either result position and
discards any later widget results. The wrapper requests one result from
`selectWidgetYield`. Its exact-true test rejects false, nil, and numeric zero.
The [shared selection wait](fishing-input-flow-contract.md#wait-result-width-and-cleanup)
owns the alive/completion polling and nil-timeout behavior. The
[Ask base contract](ask-widget-result-state.md#selected-state-and-calls)
owns completion independently of acceptance. These are dynamic helper calls,
not evidence of a running scheduler or a particular widget instance.

## Mode-3 journal values

The selected module is `widget/ask/journallistwidget.lua`, not the non-Ask
`widget/journallistwidget.lua` described by the
[journal confirmation caller](journal-confirm-caller-contract.md).
The [journal lifecycle](guildleve-journal-lifecycle.md#journallistwidget-modes-and-row-arguments)
owns mode dispatch, ordered list construction, filtering, row fields,
and the actor eligibility call. In mode 3 it builds the scenario list before
the local-guildleve list. The retained `JournalIndex` is the source slot within
the selected kind, rather than the visible row's ordinal in the combined list.

The mode-3 selection handler rejects a row whose `JournalType` is 0. It reads
the row's `JournalID` and `JournalIndex`; for type 2 it writes
`work.guildleveFlag=true`. It then calls `finish(JournalIndex)`. The flag
starts false in `initAsk`. This handler does not reset it to false for another
row type, so the exact result is the later stored flag, not a new Boolean
conversion of the row type.

In mode 3, `finish(value)` stores that value in `work.resultJournalID` when
it is non-nil, or stores numeric zero when it is nil. It then requests
`setBaseAskResult(1)`. `getAskResult()` returns exactly two values:
`work.resultJournalID,work.guildleveFlag`. Despite its field name, the first
result is the selected `JournalIndex` on this path.

`processUICommandClose` calls `finish()` with no value in mode 3. Thus a
normal Close requests base completion 1 and index 0. It does not produce the
generic wrapper's opening/selection failure result false. Neither this finish
branch nor the selected mode-3 handler requests a direct close. The generic
wrapper's explicit close follows the result read. A close request does not
prove close completion or destruction.

## Judge adaptation to the quest value

Let the three requested results be `(S,I,G)`. Only `S == true` reaches either
quest lookup. The comparisons below are exact; in particular, false, nil,
and numeric zero are different flag values.

| Selected conditions | Lookup and result |
| --- | --- |
| S is true, G is true, I is non-nil, `1 <= I`, and `I <= A1:getGuildleveQuestLength()` | Tailcall `A1:getGuildleveQuest(I)`. |
| S is true, G is false, I is non-nil, `1 <= I`, and `I <= A1:getScenarioQuestLength()` | Tailcall `A1:getScenarioQuest(I)`. |
| Any other normal path after the UI call | Exactly one nil. |

The local branch is tested first. A nil or below-1 index skips its length
read. A valid lower bound reaches one fresh length call for the selected
kind, followed by its indexed getter only when the upper bound passes.
No compacted ordinal scan occurs in this adapter. It does not compare a
quest ID, recheck `_isAlive`, or repeat the list's eligibility predicates.
It supplies no separate integer/type validator before these comparisons.

When these dynamic methods resolve to the pinned `PlayerBaseClass` methods,
the length helpers return `#self.playerWork.questGuildleve` and
`#self.playerWork.questScenario`. Their getters return exactly one value,
respectively `self.playerWork.questGuildleve[I]` and
`self.playerWork.questScenario[I]`. Each method reads its current player-work
chain. The length read and the later getter do not freeze one table, one
quest value, or the list-building snapshot. The returned value can therefore
be nil even after the bounds check; false and numeric zero are also forwarded
unchanged if those are the indexed values.

The judge's original calls are open tailcalls. The pinned player getters
return one value, but a different resolved implementation controls its actual
return width. The judge does not narrow that width or convert the value to
a quest ID. The indexed work binding's actual storage and object identity
remain outside this script contract.

Consequently, opening/selection failure and completed UI cancellation both
reach a one-nil judge return. They remain distinct from the initial
exact-false player guard's zero-value return and from a selected dynamic
getter's actual results. No branch here chooses a recipe, grants supplies,
or changes authoritative quest state.

## Source identity

Canonical members were read from the archive identified by
[private_lua_corpus.json](../manifests/private_lua_corpus.json), with only
CRLF-pair-to-LF normalization, and matched the rows below in
[scripts.json](../manifests/scripts.json). Original installed resources and
decoded payloads matched their `decodedScriptPath` rows in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
Paths below are under `lua/scripts/` for source and `client/script/` for LPB.

| Canonical source | Bytes | SHA-256 |
| --- | ---: | --- |
| `judge/craft/craftjudge.lua` | 23,945 | `5019A3E9ACAF99A23210A451E0DF2B0F4A73E5D44F764A480BB3B23953C9076F` |
| `widget/desktopwidget_connector.lua` | 660,617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/ask/journallistwidget.lua` | 37,468 | `C103432E8671EE20493B4060D5D0958F608C967F211C2F73BEE8AEC6AF96DE87` |
| `chara/player/playerbaseclass.lua` | 66,466 | `6226B3FA15DFDBAD279B7DBA453F8A3B76FCB8B68BAD6E14F5403D52987F76E4` |

| Original resource | LPB bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `0p635/7s94q/7s94q0p635.le.lpb` | 10,127 / `FDA277D6626FD0C381100CADD75628CAE7BE508F150BB2558364FE647BA07147` | 10,114 / `0DFF8463D2B685FF65A23AFCF5E52E451E531E6FAC194FD088ADBA3D05DBD0FF` |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213,487 / `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425` | 213,474 / `685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621` |
| `n1635q/9rz/0vpsw9yy1rqn1635q.le.lpb` | 15,297 / `A15C8BF36E8124C5C4F5BE2EF189037894C98342C7C7EEF5889ADE16D975E6F3` | 15,284 / `549BC61FE3C206F1DD080057948A201F2824A785D039FB9F97878D8A31491D33` |
| `729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb` | 25,846 / `32182274F3886D0CDF6329F8A82E6592790C9B3038E00BEBE5B2B38702BBD53E` | 25,833 / `1530DC2B53353888CCC6B47F78920EBD2C2D876335B9968196312153B0DB464A` |

## Original instruction locators and checks

Prototype indices and PCs are zero-based. Code starts are decoded-payload
byte offsets, excluding the LPB wrapper; instruction PC n is at start+4*n.
Canonical line ranges include each named method's binding.

| Method | Canonical lines | Prototype / code start | Decisive PCs |
| --- | --- | --- | --- |
| Judge `selectCraftQuest` | 815-856 | `root/proto24` / `0x1ECA` | 2 exact-false player test; 4 zero-value return; 7 `CALL A3 B2 C4`; 8 exact-true status; 10/25 exact true/false kind; 12-18 and 27-33 index/length gates; 22/37 open tailcalls; 40 one-nil return. |
| Connector `askPassiveGuildleveSelectWidget` | 10035-10045 | `root/proto183` / `0x1807A` | 4 `TAILCALL B5 C0` forwards the name, result count 2 and journal mode 3. |
| Connector `askEventModeWidgetYield` | 25790-25801 | `root/proto541` / `0x32E39` | 4 forwards varargs; 5 open-argument/open-result tailcall inserts opener mode 4. |
| Connector `askWidgetYield` | 25805-25856 | `root/proto542` / `0x32E9E` | 8 open-argument opener, one result; 9 nil gate; 14 select, one result; 15 exact true; 19 `CALL A9 B2 C0`; 20 open `SETLIST`; 25 close, zero results; 29 one-false return; 35 `CALL A9 B4 C0`; 36 open return. |
| Ask journal `initAsk` / `createList` | 11-141 / 810-925 | `root/proto0` / `0x3B9`; `root/proto10` / `0x1D94` | Init PC48 writes result 0 and PC54 writes flag false; mode-3 list PCs 47/51 call the scenario/local builders in order. |
| Ask journal `processUICommandSelection` | 197-332 | `root/proto3` / `0x981` | 9 rejects type 0; 21 reads `JournalIndex`; 109-114 mode-3/type-2 flag write; 120 passes the index to finish. |
| Ask journal `processUICommandClose` | 176-194 | `root/proto2` / `0x900` | 9 calls finish with receiver only on the non-mode-4 path. |
| Ask journal `getAskResult` | 398-450 | `root/proto6` / `0x1105` | 17 mode-3 test; 23 exactly two results. |
| Ask journal `finish` | 453-487 | `root/proto7` / `0x1241` | 17 nil test; 20 supplied value write; 23 zero write; 26 base result 1; 27 zero-value return. |
| Player `getScenarioQuest` / length | 1598-1606 / 1609-1617 | `root/proto34` / `0x393A`; `root/proto35` / `0x3999` | Getter PC2 indexes the current scenario table; length PC2 applies LEN; PC3 returns one value. |
| Player `getGuildleveQuest` / length | 1620-1628 / 1631-1639 | `root/proto36` / `0x39F8`; `root/proto37` / `0x3A58` | Getter PC2 indexes the current local table; length PC2 applies LEN; PC3 returns one value. |

Reproduction uses `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction/states_for`. Complete
payload consumption and original root closure assignments establish the
method identities. Focused original-instruction characterizations checked the
two kind branches, exact Booleans, bounds and call ordering, zero versus one
nil return, dynamic getter return width, opener arguments, nil padding,
completed Close, and the result-read-before-close order. Negative controls
rejected an inverted completion branch, a narrowed three-result caller,
an omitted scenario-getter index, and a narrowed widget-result call.

Those fixtures used ordinary tables and explicit mock method results. They
did not execute native bodies, model native work storage or metamethods,
establish initializer/callback delivery, or recover a historical selection.
Inputs stayed in memory. The first unsupported joins are actual runtime
objects/readback and the authoritative producer or consumer of the returned
quest value. No live client acceptance or quest/supply mutation is established.
