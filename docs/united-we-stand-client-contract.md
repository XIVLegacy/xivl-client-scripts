# United We Stand shared client contract

The retail client binds all three United We Stand quest IDs to
`/Quest/Scenario/Gcl/Gcl106`. The class owns their briefing, map display,
dialogue and returned conversation choices. It does not identify an encounter
director or supply a literal content-13 entry request.

## Quest and text ownership

The canonical title and alias map is
`xivl-client-data:docs/grand-company-quest-identities.md`, rows 111432,
111632 and 111832. Those retail SAN and title-row joins establish the shared
implementation independently of the Lua filenames.

`Gcl106.initText` loads text sheet 10352 with key `gcl106`. Separate resources
Gcg106 and Gcu106 only define initializers loading 10320/`gcg106` and
10384/`gcu106`. Neither has a SAN owner under its own path. Their existence
does not establish three separate quest implementations. The shared Gcl106
contains `initText` and 32 `processEvent` methods.

## Map briefing and returned choices

`processEvent_CommonStart_Jakys_01`, decoded prototype 4 at `0xC43`, opens
`CastrumNovumMapWidget` at PC 50 and closes it at PC 80, surrounding messages 139-142.
Each call receives only the desktop receiver and the widget name. The widget
initializer itself only calls `show()`. No duty or zone argument is carried.

At PC 112 the start handler calls `showQuestInfomation` with the quest receiver.
It compares the one result with 1, displays message 147 for 1 or 146 otherwise,
and returns the unchanged result at PC 128. The follow-up handler, prototype 5
at `0x1037`, asks message 151 with choice argument 2. Only result 1 opens the map,
repeats 139-142, closes it and displays 154. That handler returns no value.

The three city warp handlers also compare their ask result with 1 and return
it unchanged. The Limsa handler, prototype 10 at `0x1B49`, plays
`startNQCutScene("elv0l110",1,0)` at PC 23 for result 1. Gridania prototype 11
at `0x1CE6` and Ul'dah prototype 12 at `0x1DF1` have no local success action.
Their alternative messages are 198 and 203. The client bodies do not establish
the server's interpretation of these returned values.

## Supplied briefing values

`processEvent_CommonInfo_Vevina_01`, prototype 6 at `0x1307`, takes five positional
arguments A0-A4. A0 is its quest receiver, A1 is passed to the talk helper, and
A2 receives NPC dialogue and scheduler calls. `A3 == 2` selects opening message 81
instead of 82. The method name is preserved even though English message 82
introduces Serpent Commander Yarborough.

The method passes A4 unchanged to `worldMaster:say(A0, row, A4)` for
messages 84, 85, 87, 89, 90, 92, at PCs 44, 50, 61, 77, 83, 94. Each uses `CALL B=5, C=1`,
including the receiver. The preceding `MOVE` copies A4 into the last argument
register. The method constructs no parameter table or separate count, level
or duration arguments. The selected English descriptions carry fixed numeric
operands, qualified below; A4 remains an unchanged caller value.

| Message rows | English client instruction |
| --- | --- |
| 83, 138, 145, 148 | Destroy the lunar transmitter in Castrum Novum while the main host diverts the VIIth Legion. |
| 84-85 | The fixed English description specifies four to eight Disciples of War or Magic, level 45 or above, and each member's United We Stand entry requirements. |
| 86-87 | Automated defense triggers after a delay; operatives are extracted. The fixed time-limit description specifies 30 Earth minutes. |
| 88-89, 206 | Further sorties wait for the officers' briefing; the Timers tab reports the remaining wait. |
| 90 | Loot-list items transfer on departure; items that cannot be obtained are lost. |
| 91-92 | Parties representing all three Grand Companies receive greater rewards. |
| 139-142 | The map marks the tower; vanguards defend the stronghold, especially by day. Sector gates are reported to open when imperial sentries patrol. |

These localized instructions do not establish server enforcement or
historical invocation, patrol routes, gate instance bindings, reward values
or combat behavior. Cid and city leader dialogues branch on supplied flags;
they do not compute victory or grant the rewards mentioned in their text.

### Fixed entry-description controls

Row 84's two complete count controls are byte-equal to the selected controls
in `xivl-decomp:docs/resource/rich-string-entry-counts.md`, Exact Gcl107
controls. Under that constructor-qualified native path, their literal
conditions and selectors produce the words `four` and `eight`; neither count
comes from A4. Row 84's `02 20 02 2E 03` number frame carries literal 45.
Row 87's `02 20 02 1F 03` carries literal 30. The selected number/decimal
path is qualified in
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-05/06.

Rows 84, 87, 89 and 90 also share the exact `xtx/raidDungeon` code-28
reference qualified in `xivl-decomp:docs/script/worldmaster-message-pool.md`.
For the same helper/native capture route, an accepted integer A4 supplies
formatter argument 1 and hence that reference's row, with logical field 26
and an empty nested argument vector. This remains conditional on the selected
English cell, source readiness and surviving receiver. It does not select
A4's historical value, a concrete content ID or an invocation.

The [original definition join](gc-text-source-bindings.md#original-definition-joins)
qualifies loader input 10352/name `gcl106` and its conditional definition key
`0x03A22870`. The English definition explicitly names these three original
resources; their association is not inferred from adjacency:

| Resource | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `0x03A22877` | English data | 29581 | `0ef6f86c72282fa043dc348f28c974f9938e5de46de45d8509acd187ffaed77b` |
| `0x03A22878` | Enable ranges | 32 | `09033ee100a25b89ec53054b5695c9ad8e727856a3a51ca66b9b32df5d8cc271` |
| `0x03A22879` | End offsets | 2004 | `969c78fdfaffb77ec7e52d01d4cfff2d3a45722808d4574840ec45955e90bc34` |

It declares one `str` field at logical index 1 and a block with 501 slots.
All 501 original end offsets were monotonic, bounded by the 29,581-byte data
body and ended at its last byte. Four enable ranges selected 212 nonempty row
spans. The six selected rows exactly consumed their individual framed-string
spans and reproduced their own `gcl106.csv` numeric-header-1 cells, physical
CSV cell 3, after lossless control-marker inversion:

| Row | Original half-open data span | Decoded string bytes |
| --- | --- | ---: |
| 84 | `[9870,10200)` | 326 |
| 85 | `[10200,10333)` | 129 |
| 87 | `[10598,10685)` | 83 |
| 89 | `[10845,11112)` | 263 |
| 90 | `[11112,11291)` | 175 |
| 92 | `[11405,11523)` | 114 |

The CSV identity is recorded under [Reproduction and evidence](#reproduction-and-evidence).
The source/row association does not observe loaded fields, actual language or
invocation, nor establish enforcement of the description's rules.

## Content and layout boundary

The separate status timer consumer maps selector 13 to Castrum Novum
Transmission Tower; see [MyPlayer timer consumers](myplayer-timer-consumers.md).
The title is `xivl-client-data:csv/xtx_raidDungeon.csv` row 13, English column 26.
The quest's Castrum briefing and map establish narrative association but do
not supply a concrete director/content dispatch.

`xivl-decomp:docs/resource/transmission-tower-rendering.md` owns content 13,
zones 251/264, layout 511 and its shutter instance 12. Outdoor Castrum Novum's
zone 190/layout 501 doors are separate owners documented in
`xivl-decomp:docs/resource/stronghold-door-owners.md`. The briefing's sentry
statement does not assign a patrol trigger to any one of those instances.

The missing inputs are the historical briefing invocation with its A4 payload
and the associated content 13 director assignment. Historical actor/instance
ordering is also needed to connect sentry patrol state to outdoor gate calls.
The selected client chunks do not define spawning, AI, objective destruction,
clear/failure transitions, rewards, cooldowns or the Tower shutter policy.

## Complete method coverage

The [quest contract](../data/quest_contracts.json), script
`lua/scripts/quest/scenario/gcl/gcl106.lua`, records every call, result
comparison and return. The following locators cover all 33 declared methods.
Prototype numbers mean `root/protoN`; PC ranges include every instruction.
The root has 107 instructions. Four implicit trailing returns are unreachable;
there are no unreachable calls.

| Method | Prototype | Decoded code offset | PCs |
| --- | ---: | --- | --- |
| `initText` | 0 | `0x79C` | 0-4 |
| `processEvent_LimsaHint_Guincum_01` | 1 | `0x80B` | 0-33 |
| `processEvent_GridaniaHint_Fulke_01` | 2 | `0x970` | 0-33 |
| `processEvent_UldahHint_Aubray_01` | 3 | `0xAD5` | 0-33 |
| `processEvent_CommonStart_Jakys_01` | 4 | `0xC43` | 0-129 |
| `processEvent_CommonFollow_Jakys_01` | 5 | `0x1037` | 0-78 |
| `processEvent_CommonInfo_Vevina_01` | 6 | `0x1307` | 0-107 |
| `processEvent_CommonNavi_Rashaht_01` | 7 | `0x161A` | 0-45 |
| `processEvent_CommonNavi_Quinquerol_01` | 8 | `0x17B8` | 0-50 |
| `processEvent_CommonNavi_Jakys_01` | 9 | `0x197C` | 0-50 |
| `processEvent_LimsaWarp_Zanthael_01` | 10 | `0x1B49` | 0-36 |
| `processEvent_GridaniaWarp_Kinnison_01` | 11 | `0x1CE6` | 0-25 |
| `processEvent_UldahWarp_Mumutano_01` | 12 | `0x1DF1` | 0-25 |
| `processEvent_CommonInstance_Cid_01` | 13 | `0x1EFC` | 0-119 |
| `processEvent_CommonInstance_Cid_02` | 14 | `0x2255` | 0-25 |
| `processEvent_LimsaInstance_Merlwyb_01` | 15 | `0x2378` | 0-114 |
| `processEvent_LimsaInstance_Merlwyb_02` | 16 | `0x26B4` | 0-26 |
| `processEvent_LimsaInstance_Reyner_01` | 17 | `0x27DB` | 0-21 |
| `processEvent_LimsaInstance_Reyner_02` | 18 | `0x28C4` | 0-21 |
| `processEvent_LimsaInstance_Eynzahr_01` | 19 | `0x29AD` | 0-23 |
| `processEvent_LimsaInstance_Eynzahr_02` | 20 | `0x2AC0` | 0-44 |
| `processEvent_GridaniaInstance_Shinkan_01` | 21 | `0x2C6C` | 0-112 |
| `processEvent_GridaniaInstance_Shinkan_02` | 22 | `0x2FA0` | 0-26 |
| `processEvent_GridaniaInstance_Pesi_01` | 23 | `0x30C7` | 0-24 |
| `processEvent_GridaniaInstance_Pesi_02` | 24 | `0x31DD` | 0-27 |
| `processEvent_GridaniaInstance_Swethryk_01` | 25 | `0x3308` | 0-23 |
| `processEvent_GridaniaInstance_Swethryk_02` | 26 | `0x341B` | 0-51 |
| `processEvent_UldahInstance_Raubahn_01` | 27 | `0x35E3` | 0-117 |
| `processEvent_UldahInstance_Raubahn_02` | 28 | `0x3934` | 0-26 |
| `processEvent_UldahInstance_Teledji_01` | 29 | `0x3A52` | 0-24 |
| `processEvent_UldahInstance_Teledji_02` | 30 | `0x3B68` | 0-24 |
| `processEvent_UldahInstance_Eline_01` | 31 | `0x3C7E` | 0-16 |
| `processEvent_UldahInstance_Eline_02` | 32 | `0x3D4A` | 0-51 |

## Reproduction and evidence

Build identity is 1.23b, extraction 2012.09.19.0001. The original Gcl106 resource
`client/script/tp5rq/r75w9s1v/37y/37yijd.le.lpb` is 16160 bytes, SHA-256
`4b8d2086529d8783e17b30d47aa3f97b8921110fe0c440b82817670bdc10d692`.
Its decoded chunk is 16147 bytes, SHA-256
`78357a9936c2f8f5c27e110378d4c2402b992a273366477ac22d3fe7d762694c`.
Prototype offsets are within that decoded chunk and PCs are zero-based.

[Retail resource coverage](../manifests/retail_lua_coverage.json) pins the
Gcg106, Gcu106 and CastrumNovumMapWidget originals; the
[script manifest](../manifests/scripts.json) pins decoded sources.
`tools/retail_script.py` decodes the wrappers and
`tools/build_quest_contracts.py` parses the Lua 5.1 instructions. Re-analysis
of the three quest originals reproduces every field of their retained
[quest contracts](../data/quest_contracts.json). All Gcl106 call targets resolve;
only four methods have value-return sites, and no unreachable call is present.

The English messages are `xivl-client-data:csv/gcl106.csv`, numbered column 1,
SHA-256 `bd601a6bb62718b20d8a64bcdc7e920f72f9a6203bbd6703102dfb0164fa883b`.
The separate gcg106/gcu106 sheets contain only an empty row 0 and share SHA-256
`dbac8446a3a793c3094f0f9182cc68d69874abdfb9e3aa6337dcba77e47b72e1`.
The raidDungeon sheet has SHA-256
`24c7e9a071c5a16b8a38254588e350e7e7b043e2dfe4129ecd5363d2f05f6059`.
The client-data table manifest authenticates these decoded CSV members.
