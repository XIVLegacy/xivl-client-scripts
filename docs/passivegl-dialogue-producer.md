# Local guildleve dialogue producer boundary

The observed producer of the `processPgEvent` text ID is a server-to-client
event call. The inspected client path consumes that ID and returns callback
results. It does not establish the sender's rule for choosing a
`passiveGL_craft` column or a dialogue value.

[The column finding](passivegl-craft-columns.md) owns the sheet correspondence,
text-bank identity, argument forwarding, and source-column uncertainty.
This finding traces the requests and results around the captured calls.

## Observed requests and supplied values

`xivl-captures:studies/local-guildleve-dialogue/derived/accounting.json`
records a search of all 54 manifest-admitted PCAP members. The only admitted
application payloads containing `processPgEvent` are the three main-lane
server-to-client `0x0130` calls in `local_leve_complete.pcapng`. Their first
integers are 365, 366, and 368. Excluded protocols and discarded trailing
bytes are recorded separately; this is a bound on admitted clear-game data.

The same study's `derived/exchanges.json` retains two `talkDefault`
conversations. Their EventStart payloads and `switchEvent` calls match in
full. Client choice replies contain `0,2` in equal 64-byte parameter blocks,
but their seven-byte trailing fields differ. The following `welcomeTalk`
calls also match in full. Nil replies occur before the server supplies 365
in the first conversation and 368 in the second. These are observations
with separate stream order and packet-completion provenance, not proof of
server execution order or a deterministic response to the matched bytes.
The [native EventUpdate layout](#eventupdate-fields) establishes that the
seven differing bytes are copied from an unwritten stack tail.

Both `welcomeTalk` calls use `delegateEvent`, wire owner `0x44B00005`, player
`0x029B2941`, quest actor `0xA0F1D58A`, method `welcomeTalk`, and four nils.
The verified delegate forwards these to the quest actor. The static actor
key is 120202 and its SAN path is `/Quest/PassiveGuildleve/Craft/PgConv`,
whose script inherits `PassiveGuildleveBaseClass`. The owner need not supply
its own `welcomeTalk` implementation. No captured binding identifies the
owner's client-data actor class.

The capture study owns the exact packet, frame, byte, and source-hash
locators. Matching requests do not identify the server state, a phase rule,
or a source-column number.

## Intervening craft progress

The capture study's `derived/progression.json` records the interval between
the conversations. Three `CraftJudge.askContinueLocalleve` calls for leve
120202 supply current/target counts 1/3, 2/3, and 3/3, with attempts remaining
4, 3, and 2. The last call precedes text 368 in the same main s2c stream.
Player property writes also set `work.guildleveChecked[8] = 1` after text 366,
then `work.guildleveDone[8] = 1` before the second conversation. The recording
does not supply a nonzero `work.guildleveId[8]` baseline, so it does not
directly bind that array slot to leve 120202. The slot index and sheet source
column 8 belong to separate domains.

The count interpretation comes from `lua/scripts/judge/craft/craftjudge.lua`,
`askContinueLocalleve:899-929`. Raw prototype `main/f27`, PCs 18-24 at decoded
offsets `0x21C2-0x21DA`, moves r3-r7 to r20-r24 and uses `CALL A10 B15 C2`.
It forwards all five supplied values to `DesktopWidget.askForEventMode` with
question key 26 and choices 27 and 28. This method contains no comparison of
the counts and no `pgConv` reference.

`CraftJudge.initText:178-187`, raw `main/f11`, loads bank 16 as `craftJudge`.
`xivl-client-data:manifests/tables.json`, entry `craftJudge`, pins its
16,624-byte CSV to SHA-256
`2eb97dc8778c124a794fe5be2d765b4cc0b03ac6eb6781171bbf95f39a681972`.
Row 26, English field 1, explicitly labels the third, fourth, and fifth
formatting values as current count, target count, and attempts remaining.
Their number controls are `022003e80403`, `022003e80503`, and `022003e80603`.
The first two values format the leve title and requested item.

The open vararg adapters preserve those values:
`DesktopWidget.askForEventMode` in `widget/desktopwidget_connector.lua:12038-12090`,
raw `main/f237`, PCs 27-28 at `0x1C0E9-0x1C0ED`, and
`AskWidget.ask` in `widget/ask/askwidget.lua:185-194`, raw `main/f2`, PCs 70-77
at `0x0697-0x06B3`. The latter passes the question key and formatting values
to `TextBlock_Question.Text` through `_setProperty`. This proves supplied
presentation inputs without establishing a historical display.

The observed progress and done-flag changes supply candidate state for the
different dialogue values. They do not establish that the sender tested a
particular count, flag, or source column. Text 367 has no retained call, and
the source-column tuple permutations remain unresolved in the column finding.

## Lua request and return values

Paths below are relative to `lua/scripts/`. PCs are one-based and decoded
chunk offsets are zero-based. The source identities are in
[the script manifest](../manifests/scripts.json); raw LPB and decoded
identities are in [the resource census](../manifests/retail_lua_coverage.json).

| Method | Source and raw locator | Supported flow |
|---|---|---|
| `NpcBaseClass._onTalkEvent` | `chara/npc/npcbaseclass.lua:405-446`; `main/f21`, PCs 19-22, call at `0x0FD5` | Calls `self:_callServerOnTalk(r1,r2)` and discards results; no text ID is added to those arguments |
| `NpcBaseClass.switchEvent` | `chara/npc/npcbaseclass_event.lua:517-801`; `main/f13`, PCs 263-265, return at `0x143E` | `RETURN A15 B3` returns exactly the page/navigation result and UI choice |
| `PassiveGuildleveBaseClass.welcomeTalk` | `quest/passiveguildleve/passiveguildlevebaseclass.lua:11-20`; `main/f0`, PCs 4-5, return at `0x015E` | Calls `npc:startCliantTalkTurn(2,player)`, discards its results, then returns zero values |
| `PassiveGuildleveBaseClass.processPgEvent` | Same script, lines 23-37; `main/f1`, PCs 10-11, return at `0x01D4` | Discards the result of `npc:say(self,textId,0)`, then returns zero values |

For the supplied two-candidate, one-page `switchEvent` input, UI choice 2
returns `(0,2)`. The candidates' static keys are 110541 and 120202, mapped
by `xivl-client-data:manifests/staticactor_class_paths.json` to
`/Quest/Scenario/DefaultTalk/DftFst` and
`/Quest/PassiveGuildleve/Craft/PgConv`. The choice identifies the second
quest candidate. It is not a source-column selector. A bounded interpreter
of the raw instructions also checks choices 0, 1, and 3, yielding `(0,0)`,
`(0,1)`, and `(-1,-3)`, with the external UI answer substituted. This does
not execute the client UI.

`welcomeTalk` and `processPgEvent` end with `RETURN A0 B1`. That means zero
Lua results, rather than one explicit nil. The native conversion below
explains how this can produce a nil wire reply. The delegate's open
`TAILCALL B0` preserves whatever results the native `_callFunction` bridge
returns; it does not itself choose another dialogue value.

The relevant decoded LPB identities, relative to retail `client/script/`, are:

| Resource | Decoded bytes | Decoded SHA-256 |
|---|---:|---|
| `729s9/wu7/wu789r57y9rr.le.lpb` | 5,925 | `1941c40b64cacd721d271b36e31017a24f908b8ea518f713b44da17bb4e57627` |
| `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` | 6,249 | `4a3008dd8d2a91e7eb044e5555d2757468a9097bba5175992fb88f943bd07b6c` |
| `tp5rq/u9rr1o53p1y6y5o5/u9rr1o53p1y6y5o589r57y9rr.le.lpb` | 774 | `ac1de2b6208166e8ec616ee9c0a075ab7cfb91e19051e03041e93020bbea1455` |
| `0p635/7s94q/7s94q0p635.le.lpb` | 10,114 | `0dff8463d2b685ff65a23afcf5e52e451e531e6fac194fd088adba3d05dbd0ff` |
| `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213,474 | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `n1635q/9rz/9rzn1635q.le.lpb` | 5,244 | `1b0d5e2ca4c39b781305b98320eb597337e0d4c0fc0c9167244553dfc49d14c0` |

LPB decoding uses `xivl-client-structs:tools/decode_lpb.py`. Raw instruction
operands and prototype opcode sequences were checked against the pinned
unluac disassembler identified in the column finding. Fixed argument
positions, result-discarding calls, zero-result returns, and the two-result
menu return were checked separately from the decompiled text.

## Native callback result and EventUpdate

The native target is retail `ffxivgame.exe`, build `2012.09.19.0001`,
15,996,808 bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Addresses are virtual addresses at image base `0x00400000`. The incoming
argument path is recorded in the column finding. The following path handles
callback results rather than choosing a new input text ID.

The selected function bodies were read from file-backed PE sections with
pefile 2024.8.26 and decoded as x86-32 with Capstone 5.0.7. All 34 complete
bodies, including the disjoint ranges of `0x00CCF290`, match the pinned file.
Four vtable targets and the nil/integer encoding instructions were checked
directly. Read-only Ghidra exports used
`xivl-client-structs:ghidra/DumpFunctionListing.java` and
`ghidra/VerifyProgramFileBytes.java`; both reported completion, and the latter
authenticated retained file bytes and initialized file-backed mapped ranges.
The report's excluded ranges remain outside that authentication. The listing
tool has SHA-256
`59c1c0a2f0852d5919728acb1dedff3dbec15a8b3c3b0904b27297f6c3e7f465`;
the mapped-byte verifier's identity is recorded in the column finding.

| Step | Native locator | Observation |
|---|---|---|
| Return descriptor | `0x00896F70`, `0x00728AC0` | The event path requests registry entry 9, `StackOperator<Variable>`, with vtable `0x0110E0A0` |
| Collect Lua results | `0x00CCEE30`, `0x00CFAAE0` | Collects results into the thread's vector at `+0xEC` using the requested descriptor |
| Missing result | `0x00CFAAE0`, `0x00583F70:0x00583FD9` | When the expected stack result is absent, constructs a default scalar with internal type 6 |
| Accept default | `0x00CF85D0`, `0x00584EE0` | Descriptor virtual slot `+0x18` accepts the default and the collector appends it |
| Completion listener | `0x00CCE8E0`, `0x00CCD910`, `0x00896090` | Normal completion reaches the player-manager listener and result-send path |
| Result serialization | `0x00894AB0`, `0x00790CE0` | Serializes the typed result vector into a 64-byte buffer |
| Nil encoding | `0x00792B70`, `0x00792470:0x0079248C,0x007924A0` | Internal type 6 writes wire tag `0x05` and terminator `0x0F` |
| EventUpdate send | `0x00894090`, `0x0075E670` | Copies the serialized buffer into c2s `0x012E` and forwards through `0x004D6D30` |

An empty vector would serialize as END alone. The explicit nil comes from
the default value appended during return collection, not from a serializer
that always inserts nil. Integer serialization likewise copies an existing
scalar; it does not read `passiveGL_craft`. These paths support the observed
two-integer menu result and nil callback replies without identifying the
server's next text-ID choice.

The suspended-call continuation at `0x00CCF290` uses the saved descriptors
at thread `+0xFC` and the same `0x00CFAAE0` collector at
`0x00CCF636-0x00CCF64C`, then finishes through `0x00CCE8E0`. This preserves
the result-conversion path after resumption without identifying which
historical callback suspended or completed.

This is static native dataflow. It does not establish that a particular
captured reply completed a particular Lua call, or that the client displayed
the message or ran its scheduler.

## EventUpdate fields

`xivl-client-structs:structs/network/event-update.md` owns the native field
provenance and talk-request route. Normal callback completion supplies a
64-byte span for the CRC32 at application offset `+0x0C`. All 71 such
updates in the retained local-leve capture match that checksum. The seven
bytes at `+0x51-0x57` are unwritten stack bytes included by the forwarder's
copy. Their differing values provide no supported initialized selector.
The other compared application fields and choice parameters match, as
recorded in the capture study. This still leaves the sender's retained state
and its actual selection condition unidentified.

## Remaining producer evidence

The captured text IDs originate in observed server output. The selecting
routine, its state inputs, and any `passiveGL_craft` read remain unidentified.
The client request, callback result, and generic sheet cache paths do not
provide that missing sender-side selection edge. No sender implementation
is part of this evidence set.

Columns 8-11 therefore retain the unresolved contract recorded in the column
finding. Resolving their names requires evidence connecting an actual source
column choice to the outgoing `processPgEvent` text ID; nil results
and repeated menu choices do not supply that connection.
