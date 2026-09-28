# Hamlet supply and score UI contract

The recovered client has separate Hamlet supply dialogue, supply ranking,
and defense score routes. Their LPBs matched the recovered LUACs
byte-for-byte; these calls describe client presentation, not a server-side
supply, ranking, or reward policy.

`Noc002` defines captain and supply menu methods, including supply errors
and item-selection dialogue (`noc002.lua:189-849`). Its
`processSupplyAskWhatA04` runs a character scheduler, says text row 62,
then calls `desktopWidget:askHamletDefenseRankingWidget` with five supplied
arguments (`noc002.lua:781-785`). This is a direct ranking-widget opener;
the script does not identify the historical NPC actor or prove the values
of the arguments that a server supplied.

`HamletDefenseRankingWidget.setRankingList` obtains the current area master,
calls `_countHamletSupplyRanking`, and iterates that many
`_getHamletSupplyRanking` rows. It derives a linkshell icon when the row's
linkshell field is nonnull and passes the row to `setRankingListItem`
(`hamletdefenserankingwidget.lua:188-215`; bytecode
`0x0009D0-0x000A40`). `HamletDefenseScoreWidget.initAsk` instead gets the
local player, iterates `_countHamletDefenseScore` and
`_getHamletDefenseScore`, and reads `_getHamletDefenseScoreAll` for totals
(`hamletdefensescorewidget.lua:3-49`; bytecode `0x00011F-0x00013B`
and following). Neither widget's Lua calls alone decode the raw native
ranking or score receiver fields or validate particular row values.

`PopulaceHamletSupply` provides separate item and materia delivery-menu
methods (`populacehamletsupply.lua:7-78`). Its item getters return a
craft-list count of 8 and gather-list count of 3. For actor class IDs
1500433, 1500320, and 1500434 respectively, the craft sheet base keys are
12001, 11001, and 13001; the gather bases are 12009, 11009, and 13009.
Each getter reads `itemHamletSupplySheet` at `base + requestedIndex - 1`
and returns columns 0 and 2 (`populacehamletsupply.lua:79-173`; craft
bytecode `0x0009A2-0x000A3A`). The selected item IDs and quantities in the
pinned table are cataloged in
`xivl-client-data:docs/hamlet-supply-rows.md`. These are conditional
client-sheet lookups, not proof that those actor IDs spawned with this class
or accepted the listed items historically. The zero-base fallback for other
actor IDs is not a verified supply association.

Decoded LUAC SHA256 values: `Noc002`
`1DA67252A10403AFF3C6391B2B6BFB1AF5B30EC9B29942690676B28F7B58C988`;
ranking widget
`E1293DA98F699955D5C5935EFDF7E1A52D25B6A88717A7DAEFF78C53B3413054`;
score widget
`54779D0E785A52CFF64B7136A34C168C3B10A1A99089B7789EB9A199AE98AD7E`;
`PopulaceHamletSupply`
`E9CC7C69A6B0409BD6FD5D63AC42B243CC2BC526F72E243B54E02C83AECF8FD1`.
Recovered-source identities are in
`manifests/scripts.json:6434-6439,12716-12721,14960-14971`.
