# Joining the Spirit objective boundary

Quest 110813, Joining the Spirit, instructs the player to obtain any one of
three catalysts using Fingerprints of the Gods. Its journal explicitly
includes calcified matter obtained through fishing. The recovered client
script does not establish the server condition that advances sequence 0.

## Identity and instruction

The quest class is `/Quest/Scenario/Etc/Etc103`, with level 18 and Disciples
of the Land eligibility. Wil journal row 435 names the miner Kokosamu and
introduces his catalyst lesson. Row 436 lists carbonized matter from mining,
germinated matter from harvesting, and calcified matter from fishing, and
tasks the player with procuring any one using the newly learned ability.
Row 446 says a catalyst was obtained and directs the player back to Kokosamu.
`xtx_quest` row 110813's English journal field contains conditional
references to rows 436 and 446. The selected text does not establish the
producer of the condition parameter.

Sources: `xivl-client-data:csv/xtx_quest.csv`, row 110813, columns 2,14,41,46-50;
`csv/quest.csv`, row 110813, column 51;
`manifests/staticactor_class_paths.json`, entry 110813;
`csv/xtx_journalxtxWil.csv`, rows 435,436,446, English column 1; and
`csv/etc103.csv`, rows 10,13-17,19,22,23, English column 1.
Columns are zero-based and exclude the row key.

## Client methods and progress limit

`Etc103.initText` loads text resource 7424,"etc103".
`processEventKokosamuStart` presents the lesson and returns the
`showQuestInfomation` result. Equality to 1 selects the accepted-offer
dialogue. `processEventKokosamuYet` presents the eligibility reminder.
`processEvent_000` presents row 16, which asks the player to try the ability.
`processEvent_005` presents rows 17/18, including praise for obtaining a
catalyst. The latter three methods return zero values.

The complete five-method payload contains presentation, scheduler and
talk-turn calls. It reads no inventory item, compares no acquisition result,
writes no quest work and tests no catalyst or gathering outcome. The
`_000`/`_005` method suffixes and completion narration do not identify a
server sequence transition or its cause.

Canonical source: `lua/scripts/quest/scenario/etc/etc103.lua:11-308`.
Original Lua 5.1 sites: root/proto1 offer CALL PC51/0x2B2,
comparison PC52/0x2B6 and one-result RETURN PC148/0x436;
root/proto3 reminder CALL PC14/0x6E9 and zero-result RETURN PC17/0x6F5;
root/proto4 praise CALL PC14/0x7E5 and zero-result RETURN PC25/0x811.
PCs and prototype indices are zero-based. Offsets are in the decoded payload.

The intended objective therefore admits a fished catalyst. The actual
sequence-0 trigger remains **UNESTABLISHED**: fresh acquisition, current
possession, a particular item/count, ability activation, and gathering versus
fishing causality are not distinguished by these methods. An exact selector
producer or attributable retained acquisition-to-quest-state transition is
needed to establish that rule.

## Source identity

Extraction 2012.09.19.0001, retail 1.23b. The decoded Lua and CSV archives
matched the owning private-corpus manifests, and selected members matched
`manifests/scripts.json` and `xivl-client-data:manifests/tables.json`.
Etc103 canonical Lua SHA-256 is
`949413fa68918aae021563bc813bb9b3e123876f96b92b056ac93ec067299b89`.
Its exact LPB resource is `tp5rq/r75w9s1v/5q7/5q7ijg.le.lpb`,
SHA-256 `36dbeb967ec5c818771c7e225f8bd9f79fa9e7c8a38a58867edb8c93a10afcc2`.
Decoded payload SHA-256 is
`68c453457905c8d0c12c5f0559cf84feecb4c81d0d8b604b09bb682665375232`,
as pinned by `manifests/retail_lua_coverage.json`.
The selected original instructions were checked with
`tools/retail_script.py:decode_lpb` and the Lua 5.1 reader in
`tools/build_quest_contracts.py`.
