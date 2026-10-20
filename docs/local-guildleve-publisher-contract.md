# Local guildleve publisher contract

`PopulacePassiveGLPublisher` uses the local `talkOffer*` / `askOffer*`
callback family. The regional `eventTalk*` contract does not substitute for
these menus. This page distinguishes recovered client consumers from the
server's offer selection and acceptance policy.

Pack reply 6 selects class 34, weaver. Rank replies 1/2/3 select displayed
lower bounds 1/20/40. A card reply selects its original slot among eight
supplied IDs, even when empty slots are hidden. `askOfferQuest` argument 2 is
unused. Welcome's 38 is the displayed allowance count; Decide has no consumed
argument. Exact server refusal triggers and rank-band offer pools remain
separate from these recovered client contracts.

## Evidence and confidence

- **A-Lua:** recovered retail client behavior, conditional on the named method
  receiving its arguments and its helper calls completing as described.
- **A-data:** authenticated static client rows or text, not a server rule.
- **A-wire:** values and direction-local ordering in the retained capture.
- **U:** an unbound producer, policy or historical execution condition.

The client extraction is `2012.09.19.0001`. The publisher's source identity is
owned by `manifests/scripts.json:6477-6480` and
`manifests/retail_lua_coverage.json:7790-7801`:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Original `729s9/wu7/uvupy975/uvupy975u9rr1o53yup8y1r25s.le.lpb` | 5,122 | `ded83220dc9e8a73ecdc6f6bb4e95e35a2fd74c459c49a09d03205d5105781be` |
| Decoded Lua 5.1 payload | 5,109 | `f1463d12d9658ed49cfd15c2766de5982d33fab0502d48311267fe5a8e71539e` |
| Canonical decompile, `chara/npc/populace/populacepassiveglpublisher` | 11,836 | `f4d7ab96f3932e41a9b6afb6d21ea0270fed945fe1dda1211807963ec13265f1` |

The [Lua corpus guide](../lua/README.md#extraction-pipeline) owns extraction
and canonicalization. Method/prototype locators below identify the evidence
distilled in this tracked contract; raw decompiler output is not a public
dependency. `lua/registry.json:13296-13327` identifies the class, its require of
`/Chara/Npc/NpcBaseClass`, and its callback names.

## Offer callbacks and reply meanings

Arguments below exclude `self`. `player` denotes the first explicit argument
of the offer callbacks; the body ignores it where stated. A callback return
is a client result, not proof that the server accepted or persisted a leve.
All method locators in this section refer to the publisher identified above.

| Callback | Client consumer | Reply / service interpretation | Confidence |
|---|---|---|---|
| `askOfferPack(player)` | Calls `desktopWidget:askGuildleveSelectPackNumber(self,true)`; ignores `player`. | Returns the helper's one result unchanged. Use the class lookup below for a positive pack position; nil is a back/close result in the retained capture. | A-Lua for forwarding and lookup; A-wire for reply 6 and nil |
| `askOfferRank(player)` | Ignores `player`; builds question 31 with option rows `32,32,32,33`, formatting levels `1,20,40,0`. | Returns a numeric helper result 1-3 unchanged, otherwise nil. Map 1 -> level 1, 2 -> 20, 3 -> 40. | A-Lua / A-data |
| `askOfferQuest(player,arg2,id1,...,id8)` | Ignores `player` and `arg2`; fills `work.pre_leve_id` in received slot order, then opens the local card selector and detail selector 11. | A positive accepted result selects that offered slot, not a guildleve ID. The detailed result branches are below. | A-Lua / A-wire |
| `talkOfferWelcome(player,allowances)` | Calls `startCliantTalkTurn(2,player)` and chooses a greeting by actor class; forwards `allowances` to its number formatting. | No Lua return values. Observed 38 is the displayed allowance value, not a text ID, pack, rank or refusal code. | A-Lua / A-data / A-wire |
| `talkOfferDecide()` | Chooses an acknowledgement text by actor class. No explicit argument is read. | No Lua return values. The captured nil argument is unused compatibility padding. | A-Lua / A-wire |
| `talkOfferMaxOver()` | Chooses an issuance-limit text by actor class. No count or failure code is accepted or checked. | No Lua return values. The server must choose when to call it. | A-Lua / A-data; U for authoritative trigger |
| `finishTalkTurn()` | Calls inherited `finishCliantTalkTurn()`. | No Lua return values. The capture sends an unused nil argument. | A-Lua / A-wire |

### Pack position and crafting class

`getMaxGuildlevePackNum()` returns 8. `getPreGuildlevePackId(index)` contains
this literal array; no `guildlevePack`, `passiveGL_type` or local-leve sheet
orders these entries in the publisher body:

| Position | Returned class ID | English class name |
|---:|---:|---|
| 1 | 29 | carpenter |
| 2 | 30 | blacksmith |
| 3 | 31 | armorer |
| 4 | 32 | goldsmith |
| 5 | 33 | leatherworker |
| 6 | 34 | weaver |
| 7 | 35 | alchemist |
| 8 | 36 | culinarian |

The same array contains 39, 40, 41 and 42 at positions 9-12, while the
advertised pack count remains 8. An absent array index yields nil. Do not
expose those extra positions merely because the lookup table contains them.
`DesktopWidget.askGuildleveSelectPackNumber` opens
`Ask/GuildleveAreaOrderWidget`, calls `addAreaParameter(i,classId)` for each
position 1-8, then `updateList()`. It reads `getAskResult()` only after a true
selection result and closes the widget. Nil widget or cancellation returns
nil. This population path is a recovered dynamic Lua member assignment, even
though the pattern-recovered registry does not list the helper by name.
With the passive flag true, the area widget uses title text 6108, hides its
second title/column and writes list row `i-1` with text 206 and class ID as
the formatting argument. `processUICommandSelection` stores the selected
zero-based row plus 1. Closing stores -1, which `getAskResult` converts to
nil. Thus the reply is the one-based menu position, not class ID 29-36.

UI text row 206 references `xtx/text_jobName`; it supplies the class label,
not the ordering. Rows 29-36 of `xtx_text_jobName.csv` (physical lines 31-38,
English singular data position 1 after the row ID) give the names above.
The row-206 reference is the same in both authenticated UI text members:

| Member / selected rows | Bytes | SHA-256; manifest locator |
|---|---:|---|
| `xtx__text_ui.csv`, 206 / 6108 / 78605 at CSV lines 8 / 1794 / 3660 | 1,284,564 | `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`; `xivl-client-data:manifests/tables.json:5987-5992` |
| `xtx__text_ui(2).csv`, 206 / 6108 at lines 8 / 1059 | 397,517 | `e33205165bda559ed69bb63664514f0e12b7c29fc219d13ae17fa740985eca82`; `xivl-client-data:manifests/tables.json:5979-5984` |
| `xtx_text_jobName.csv`, 29-36 | 12,555 | `61535798445ddb716cd16e8b68b06d9c6a67f76c321fe0dd5e9840c143de8b57`; `xivl-client-data:manifests/tables.json:6347-6352` |

Text 6108 is the class title. Text 78605 describes a leve's class requirement.
The alternate UI member has no 78605 row. These text joins identify the
labels without proving which UI member was loaded in a historical session.

### Rank positions and class level

The exact `askForEventMode` arguments after its receiver are
`self,self,self,1,false,true,31,{32,32,32,33},0,0,0,0,1,20,40,0`.
Publisher text 31 asks for difficulty, row 32 formats a level number and row
33 is Return. `getMaxRankBand()` returns 3. Bytecode checks the helper result
against both 1 and 3 before returning it, avoiding the canonical decompile's
misstructured nested branch. The three offered labels are always 1, 20 and
40 in this body. It reads no class level, selected class or recommended-level
sheet field. It does not construct a 1/10/20/30/40/50 menu or filter these
three choices for lower-level characters. Any authoritative class-level gate
belongs to an unresolved server producer, not this callback.

The row-32 label ends in a tilde: these are displayed lower bounds. The body
does not supply upper bounds or a rule joining a band to the individual
`recommendedLevel1..4` fields. It therefore does not prove that selecting
band 1 means selecting only native packs whose recommended level equals 1.
For every class code 29-36, the authenticated `passiveGL_craft` rows contain
the distinct recommended-level values `1,5,10,15,20,25,30,35,40,45,50` in
zero-based data positions 16/24/32/40, excluding the row ID. For example, row
120214 stores 5/15/25/40. The mapping and source pin are
`xivl-client-data:tools/mappings/passivegl_craft.py:7-43` and
`xivl-client-data:manifests/tables.json:4099-4104`, SHA-256
`2e2b68515f43ba2898bc3c4bf642332bd924687a4d771ba8d8d9733c539cd0ba`.

The shared `askForEventMode` helper opens `Ask/AskWidget`, forwards the prompt,
choices and formatting values, and returns 0 on nil widget or cancellation.
That numeric 0 becomes the publisher's nil result. Choosing Return (position
4) likewise lies outside 1-3 and returns nil.

### Card arguments, acceptance and cancellation

`initForEvent` creates `work.pre_leve_id` as an eight-element `integer32`
array. `askOfferQuest` clears the current array and copies its varargs into
successive slots. The interoperable retained shape is exactly eight IDs, with
integer zero for unused slots. The vararg copy has no explicit eight-value
limit; that does not establish support for overflowing the native array.

The shared card helper passes the publisher object to
`Ask/GuildleveCardOrderWidget`. The widget reads all eight source slots,
compacts positive IDs into visible buttons, and stores each original slot in
control user-work integer field 4. Selecting a button returns that stored
slot. For example, `[120222,0,120202,0,0,0,0,0]` renders two positive cards,
but its second visible card returns **3**, not 2. Zero-filled tail buttons
carry ask ID 0. The server must resolve the reply against the original offer
snapshot. Card cancellation stores base result -1; the publisher rejects
nil/nonpositive helper results regardless of the inherited result conversion.

Argument 2 is never read. The value 2 in both captured lists therefore cannot
be assigned a remaining-picks, allowance, page or populated-card-count role
from this consumer. It may be retained as the observed placeholder without
driving offer-state decisions.

For a chosen nonzero slot `i`, the client calls
`askJournalDetailWidget(11,offeredIds[i],variation[i])`. The local variation
lookup is `1,2,3,4,1,2,3,4` for slots 1-8. It ignores the selected ID and falls
back to 1 outside that range. The canonical
[journal lifecycle finding](guildleve-journal-lifecycle.md#passive-guildleve-card-selection)
owns this selector contract and its unresolved visual/server meaning.

| Client condition | Lua result | Adapter action |
|---|---|---|
| No nonzero offered ID | `(nil,5)` | No card acceptance. The second result is distinct from accepting slot 5. |
| Card helper returns nil/nonpositive, or the chosen slot contains nil/zero | Zero return values | Return/back without accepting an ID. Do not infer allowance mutation. |
| Selected nonzero ID and detail result exactly true | `i` | Resolve `offeredIds[i]` from the outstanding offer snapshot and retain the slot's variation selector. |
| Selected nonzero ID and any other detail result | `-1` | Detail was not confirmed. Keep it separate from a successful slot selection. |

The retained nil wire response is not proof of which zero-value/nil Lua branch
ran. The source return arities and observed EventUpdate values are separate
facts. Only a positive accepted slot should reach the service's acceptance
transaction.

## Greeting, acknowledgement and refusal texts

`initForEvent` loads `populacePassiveGLPublisher` with bank argument 509.
It selects these rows using `getActorClassId()`:

| Actor class ID | Welcome | Accepted acknowledgement | Issuance-limit explanation |
|---:|---:|---:|---:|
| 1000455 | 1 | 2 | 17 |
| 1000456 | 13 | 14 | 18 |
| 1001372 | 15 | 16 | 19 |

Welcome calls `say(self,row,0,allowances)` after starting the talk turn. The
greeting rows' number control is `022003e80203`; the retained value 38 fills
that allowance field. Decide and MaxOver call `say(self,row,0)` with no count.
Unknown actor class IDs receive no fallback text in these three methods.
Welcome still performs its initial talk-turn call.

The bank's English data column 1 contains acknowledgement text at 2/14/16
and issuance-limit explanations at 17/18/19. The latter do not identify which
authoritative check failed. A server-side no-allowance versus journal-slots
decision cannot be reconstructed from that wording alone. There is no
class-too-low refusal branch in the inspected publisher methods, and the
rank callback does not check level.

`populacePassiveGLPublisher.csv` has rows 1-33. English data column 1 is
physical CSV field index 2 when the row ID is index 0. The member is 18,441
bytes, SHA-256
`d15247491b20bd2fc752cf8a7339210a257c5a3a0c502de61e82c0a17e0060bc`,
pinned by `xivl-client-data:manifests/tables.json:4619-4624`. Its sheet identity
is `0x03A201FD` at `xivl-client-data:manifests/sheet_inventory.csv:576`.
Physical data lines equal the row ID plus 2. Rich text conditionals remain
part of the source; greetings are not fixed strings independent of their
format values.

## Other callback surface

These are available client callbacks, not a claim that every one must appear
in an ordinary acceptance conversation. All are **A-Lua**; the text roles
are **A-data**. Their authoritative server triggers remain **U** where the
capture does not show them. `askExtendWidget` is the inherited helper called
on the publisher, and exact arguments below are after that method's receiver.

| Callback arguments | Direct client call / result | Meaning and boundary |
|---|---|---|
| `confirmOffer(player,questValue)` | `askExtendWidget(self,7,2,1,2,questValue)`; true only for helper result 1, otherwise false | Row 7 asks to activate the selected leve, with 8/9 Yes/No. The player argument is unused. |
| `confirmMaxOffer(player)` | `askExtendWidget(self,20,2,1,2)`; same boolean conversion | Row 20 warns acceptance reaches the current maximum. No slot count or allowance is passed. |
| `askDiscardGuildleve()` | `askExtendWidget(self,25,2,1,2)`; same boolean conversion | Row 25 asks whether to return a held local leve; rows 26/27 are Yes/No. |
| `selectDiscardGuildleve(player)` | `askPassiveGuildleveReleaseWidget()` -> `(ok,ordinal)`; when `ok == true`, scans the player's non-nil local quests | Returns the selected quest object, not a quest ID or raw journal slot. Nil when the gate or ordinal lookup fails. |
| `confirmDiscardGuildleve(player,A2,A3)` | `askExtendWidget(self,28,2,1,2,A2,A3)`; same boolean conversion | Row 28 asks to return a selected leve; rows 29/30 are Yes/No. The publisher forwards both format values without assigning their server meaning. |
| `confirmJournal(A1,selector,A3,A4,A5,A6,A7)` | When A1 exists and selector is 1-4, `askJournalDetailWidget(13,A1,selector,A4,A5,A6,A7)`; returns its result | Skips A3. This is a detail presentation contract, not proof of supply/attempt field producers. |
| `askRetryRegionalleve(A1,A2)` | `worldMaster:ask(self,worldMaster,50144,2,A1,A2)`; result 2 additionally asks 50149 with A1 | Returns `(1,nil)`, `(2,secondResult)` or `(firstResult,nil)`. The callback name is preserved despite belonging to this local publisher class. It does not perform a Retry transaction. |

The Retry/abandon prompts and transport boundary are owned by the
[journal lifecycle](guildleve-journal-lifecycle.md#return-node-retry-and-local-synthesis-prompts)
and [local supplies contract](local-guildleve-supplies-contract.md). No
publisher callback above performs an allowance debit, supplies mutation or
authoritative acceptance check.

## Offer-service adapter

The recovered mapping is `packPosition -> classId` and
`rankPosition -> displayed lower bound`. Keep those menu positions separate
from an offer service's native pack key. If a consumer uses
`(classId << 8) | recommendedLevel`, the low byte still identifies an exact
native recommended level. For example, class 34 / level 5 gives `0x2205`
(8709). This key formula is a consumer convention, not a recovered wire field.
Pack reply 6 / rank reply 1 identifies class 34 and the menu's level-1 band;
it does not alone select every exact native pack or a single recommended-level
value within that band.

The adapter can implement these **A-Lua/A-wire-backed** steps:

1. Accept pack positions 1-8 and translate them through the hardcoded class
   table. Accept rank positions 1-3 and translate them to 1/20/40 labels.
   Nil returns to the preceding menu without accepting a commission.
2. Retain an eight-slot offer snapshot and its service-owned variant identity.
   Send eight integer IDs, zero-fill unused slots, and preserve the source-slot
   mapping even if presentation hides holes. The observed unused argument 2
   can remain 2; do not spend an allowance or remove a card because of it.
3. Resolve a positive card result against that snapshot. The detail decline
   result -1 and back/empty results do not select a commission. Only the
   service's successful acceptance transaction should produce the accepted-row
   journal update and acknowledgement.
4. Supply the actual remaining allowance count to Welcome. Decide, MaxOver
   and Finish consume no explicit arguments; captured nil padding is sufficient
   for the void forms. Confirmation/discard callbacks use the signatures above.

The exact joins from class/band to native pack pools, authoritative class-level
eligibility, zero-allowance versus journal-cap refusal sequencing, and optional
discard flow are **U** as historical server rules. The current capture contains
only a successful offer. The first missing evidence would be a band-keyed
offered-row/variant producer, or an attributable refusal conversation with its
precondition. The client provides the presentation surface; it does not choose
the offer service's acceptance policy.

## Exact consumer locators

The table records the publisher's recovered method assignments. Line ranges
refer to the canonical 622-line decompile pinned above, not a separately
published raw script. Prototypes are direct children of `main`; PCs are
zero-based inclusive and decoded instruction-byte ranges are half-open.
These locators and the original resource pin make the tracked findings
reproducible through the corpus pipeline.

| Method | Canonical lines | Prototype / PCs | Decoded code range |
|---|---|---|---|
| `getMaxGuildlevePackNum` | 11-17 | `main/f0`, 0-2 | `[0x3A2,0x3AE)` |
| `getMaxRankBand` | 20-26 | `main/f1`, 0-2 | `[0x3DF,0x3EB)` |
| `getPassiveGuildleveVariation` | 29-59 | `main/f2`, 0-23 | `[0x41C,0x47C)` |
| `initForEvent` | 62-92 | `main/f3`, 0-20 | `[0x4E7,0x53B)` |
| `getPreGuildlevePackId` | 95-126 | `main/f4`, 0-16 | `[0x5FE,0x642)` |
| `getMaxCardNum` | 129-137 | `main/f5`, 0-4 | `[0x6D6,0x6EA)` |
| `getPreGuildleveId` | 140-148 | `main/f6`, 0-4 | `[0x72D,0x741)` |
| `askOfferPack` | 151-162 | `main/f7`, 0-6 | `[0x784,0x7A0)` |
| `askOfferRank` | 165-213 | `main/f8`, 0-39 | `[0x7FD,0x89D)` |
| `askOfferQuest` | 216-292 | `main/f9`, 0-73 | `[0x940,0xA68)` |
| `confirmOffer` | 295-314 | `main/f10`, 0-14 | `[0xB5B,0xB97)` |
| `confirmMaxOffer` | 317-335 | `main/f11`, 0-13 | `[0xBEF,0xC27)` |
| `talkOfferWelcome` | 338-386 | `main/f12`, 0-38 | `[0xC7F,0xD1B)` |
| `talkOfferDecide` | 389-429 | `main/f13`, 0-31 | `[0xDC2,0xE42)` |
| `talkOfferMaxOver` | 432-472 | `main/f14`, 0-31 | `[0xEC7,0xF47)` |
| `finishTalkTurn` | 475-482 | `main/f15`, 0-2 | `[0xFCC,0xFD8)` |
| `selectDiscardGuildleve` | 485-516 | `main/f16`, 0-26 | `[0x101A,0x1086)` |
| `confirmJournal` | 519-541 | `main/f17`, 0-19 | `[0x1130,0x1180)` |
| `askDiscardGuildleve` | 544-562 | `main/f18`, 0-13 | `[0x11F3,0x122B)` |
| `confirmDiscardGuildleve` | 565-585 | `main/f19`, 0-15 | `[0x1283,0x12C3)` |
| `askRetryRegionalleve` | 588-622 | `main/f20`, 0-30 | `[0x131B,0x1397)` |

For `askOfferRank`, PCs 29-37 at `0x871-0x891` apply the two bounds and set
nil on either failing comparison. PC 38 returns exactly one value. For
`askOfferQuest`, PCs 37-39 return two values on the empty-list branch,
PC 49 returns zero values on card cancellation, PC 69 returns the accepted
slot, and PC 72 returns `-1`. These return branches are bytecode facts rather
than a reconstruction of the server's continuation.

### Shared widgets

The following additional resource pins are owned by
`manifests/retail_lua_coverage.json`; canonical decompile identities are owned
by `manifests/scripts.json`. All were authenticated before consumer inspection:

| Resource; manifest locators | LPB bytes / SHA-256 | Decoded bytes / SHA-256 |
|---|---|---|
| Connector `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`; coverage 25443-25455, scripts 15399-15402 | 213,487 / `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213,474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| Area `n1635q/9rz/3p1y6y5o59s59vs65sn1635q.le.lpb`; coverage 25293-25305, scripts 14937-14940 | 1,880 / `633eaf3f3fd31dd5c94d9eca3f5eb48a3a090e46ac6313e5efff692aed301802` | 1,867 / `a281ce05244a3cc47dfb63ddf1738d0358c418c301b106c2ae746a53a8e1a442` |
| Card `n1635q/9rz/3p1y6y5o579s6vs65sn1635q.le.lpb`; coverage 26328-26340, scripts 14943-14946 | 4,575 / `ef5877c28b1a57f68e78b16d66b96433616f60e900178cec1c34082c766a7208` | 4,562 / `b2cbde8432e8534c065cd64166397a1eb4fac89a4ce4d5402acb5107ab5925f7` |

Canonical SHA-256 values are connector
`9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01`,
area `eeff3579f0e169c108195e96af614245f00415a0acfd711f53f2a49fa07e4625`,
and card `52e90297119de26fb867692124ebb4a84957f3b28503f2d06914c8b10f39e24d`.
The chunk paths below are decoded paths under `lua/scripts/`. Code ranges
use decimal decoded offsets, half-open, within the respective chunk:

| Chunk / method | Canonical lines | Prototype / PCs | Code range |
|---|---|---|---|
| `widget/desktopwidget_connector`, `askGuildleveSelectPackNumber` | 16646-16697 | `main/f366`, 0-38 | `[147272,147428)` |
| Same, `askGuildleveSelectCard` | 16701-16746 | `main/f367`, 0-34 | `[147701,147841)` |
| Same, `askForEventMode` | 12038-12090 | `main/f237`, 0-41 | `[114817,114985)` |
| `widget/ask/guildleveareaorderwidget`, `initAsk` | 11-86 | `main/f0`, 0-59 | `[400,640)` |
| Same, `addAreaParameter` | 89-130 | `main/f1`, 0-33 | `[1050,1186)` |
| Same, `updateList` | 133-150 | `main/f2`, 0-10 | `[1390,1434)` |
| Same, `processUICommandSelection` | 153-161 | `main/f3`, 0-3 | `[1598,1614)` |
| Same, `processUICommandClose` | 164-172 | `main/f4`, 0-3 | `[1685,1701)` |
| Same, `getAskResult` | 175-187 | `main/f5`, 0-7 | `[1772,1804)` |
| `widget/ask/guildlevecardorderwidget`, `initAsk` | 11-154 | `main/f0`, 0-116 | `[610,1078)` |
| Same, `processUICommandOperate` | 157-188 | `main/f1`, 0-24 | `[1635,1735)` |
| Same, `processUICommandCancel` | 191-199 | `main/f2`, 0-3 | `[1896,1912)` |
| Same, `setUserWorkAskID` | 506-520 | `main/f9`, 0-9 | `[4276,4316)` |
| Same, `getUserWorkAskID` | 523-536 | `main/f10`, 0-9 | `[4423,4463)` |

## Retained local acceptance witness

**A-wire.** The source is `accept_local_leve.pcapng`, 50,676 bytes, SHA-256
`3b4b071d88742a5d3c94a1e29ca6a4074cb6b9a9a60207118302fe22f932bd7c`.
`xivl-captures:studies/regional-guildleve-publisher-contract/derived/timeline.csv:27-46`
owns these selected rows. Its
[verdict](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/regional-guildleve-publisher-contract/derived/verdicts.md#local-comparison)
owns the bounded local acceptance conclusion.

The main-lane s2c `0x0130` calls have wire owner `0x44D80009`. The player actor
value is `0x029B2941`. Replies use c2s `0x012E`. Frame/subevent indexes are
zero-based and completing capture packet indexes one-based:

| Callback and supplied values | s2c frame/subevent; packet | Reply; c2s frame/subevent; packet |
|---|---|---|
| `talkOfferWelcome(player,38)` | 5/0; 38 | nil; 10/1; 44 |
| `askOfferPack(player)` | 9/0; 48 | integer 6; 18/1; 68 |
| `askOfferRank(player)` | 15/0; 72 | integer 1; 24/2; 83 |
| `askOfferQuest(player,2,120222,120202,0,0,0,0,0,0)` | 20/0; 88 | integer 2; 38/2; 122 |
| `talkOfferDecide(nil)` | 30/1; 126 | nil; 43/1; 136 |
| `askOfferQuest(player,2,120222,0,0,0,0,0,0,0)` | 34/1; 139 | nil; 54/1; 164 |
| `askOfferRank(player)` | 42/0; 166 | nil; 59/1; 178 |
| `askOfferPack(player)` | 46/0; 181 | nil; 64/1; 207 |
| `finishTalkTurn(nil)` | 50/0; 210 | nil; 66/1; 213 |

At s2c frame 31/0, packet 126, `0x0137` publishes
`work.guildleveId[8]=202`. This is an accepted-row journal publication.
The capture does not identify an allowance debit, durable persistence,
refusal branch or rank-lock policy. Capture completion order does not establish
cross-direction server causality.
