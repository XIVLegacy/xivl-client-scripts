# Quest scene literal and replay-row joins

This note records direct scene-key calls from two bounded audits of 125
recovered scenario scripts and separate HQ-key checks. Exact-key joins to the
static `cutReplay.csv` table are recorded where established. It records call
presence and table matches only; it does not establish dispatch, invocation,
playback, quest ownership, or historical activation. It is not a full-corpus
absence audit.

The canonical Lua source paths, byte counts, and SHA-256 values are pinned in
[`scripts.json`](../manifests/scripts.json); resource paths and
decoded-payload identities are in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json). The
source line ranges below locate each key assignment and call in that canonical
Lua source. Each join compares the literal scene key with `cutReplay.csv` sheet
column 0, which is CSV field 1 after the row ID, using case-sensitive exact
string equality. Similar keys that differ only in letter case are not treated
as matches; the available evidence does not establish runtime aliasing or
normalization. The table has SHA-256
`2553b82e1f983025e0e23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`, pinned
at `xivl-client-data:manifests/tables.json:1123-1127`. The data table and its
row/key convention are described in
`xivl-client-data:docs/quest-replay-rows.md`.

## Module-prefixed scene keys

Each entry is `literal-key @ inclusive-source-lines -> replay-row-ID(s)`.
Hashes identify the canonical decoded source listed in `scripts.json`.
An entry with `and` combines multiple call sites that use the same key.

| Module | Canonical source; SHA-256 | Literal calls and row joins |
| --- | --- | --- |
| `alc300` | `lua/scripts/quest/scenario/alc/alc300.lua`; `3FBC5DA07A7D820CB65569DB718E490F6134107E0CDE1D97903B2091654C174C` | `alc30010` @ 230-233 -> 11042101; `alc30020` @ 277-280 -> 11042102 |
| `alc306` | `lua/scripts/quest/scenario/alc/alc306.lua`; `A8C2BC3CB0B698BF82E2D63BABFD872B5AD25DCF4F17A86E36F3E43E68FD2B4D` | `alc30610` @ 169-172 -> 11042201; `alc30620` @ 174-177 -> 11042202; `alc30630` @ 194-197 -> 11042203 |
| `arc300` | `lua/scripts/quest/scenario/arc/arc300.lua`; `98FC46CBB33469C226033F3E599A970808C443CFB93A03701FEE5BA5120ABD3E` | `arc30010` @ 127-130 -> 11016101; `arc30015` @ 147-150 -> 11016102; `arc30020` @ 167-170 -> 11016103; `arc30025` @ 245-248 -> 11016104; `arc30030` @ 265-268 -> 11016105; `arc30040` @ 316-319 -> 11016106; `arc30050` @ 341-344 -> 11016107 |
| `bsm300` | `lua/scripts/quest/scenario/bsm/bsm300.lua`; `0972B14D5E39BF00972790F25243C834849B4821B0726B457E59A8D897974AE1` | `bsm30010` @ 318-321 -> 11032101; `bsm30020` @ 383-386 -> 11032102; `bsm30030` @ 403-406 -> 11032103 |
| `cnj200` | `lua/scripts/quest/scenario/cnj/cnj200.lua`; `F520D87903068435AB7DF0985D2F2DA427E527F6D2ECD9F0D43E0C1C3955DAAB` | `cnj20010` @ 60-63 -> 11026001; `cnj20020` @ 697-700 -> 11026002; `cnj20030` @ 892-895 -> 11026003 |
| `cnj300` | `lua/scripts/quest/scenario/cnj/cnj300.lua`; `A44C38D7DA66FE8B50241AE04DA58C002527354B63BEDE04C7BA545ED7A8050A` | `cnj30010` @ 389-392 -> 11026101; `cnj30020` @ 469-472 -> 11026102; `cnj30030` @ 598-601 -> 11026103; `cnj30040` @ 819-822 -> 11026104; `cnj30050` @ 989-992 -> 11026105; `cnj30060` @ 1176-1179 -> 11026106; `cnj30070` @ 1196-1199 -> 11026107 |
| `cul200` | `lua/scripts/quest/scenario/cul/cul200.lua`; `338AF8E3EFC0719A59FA7D6A97E237911590267CF5918FF1BB0FEB4F52252012` | `cul20010` @ 270-273 -> 11044001; `cul20020` @ 489-493 -> 11044002, 11044003; `cul20030` @ 633-636 -> 11044004 |
| `cul300` | `lua/scripts/quest/scenario/cul/cul300.lua`; `49C97019160EB335981958AE1B4FD749E839081DE42FBFDDF97471B48B1DC377` | `cul30010` @ 230-233 -> 11044101; `cul30020` @ 535-538 -> 11044102; `cul30030` @ 797-800 -> 11044103 |
| `cul306` | `lua/scripts/quest/scenario/cul/cul306.lua`; `12EB6F1B94B925DB81DBB991228472995DD4A3DC22E452759162B1DD4D279F87` | `cul30610` @ 51-54 -> 11044201; `cul30620` @ 194-197 -> 11044202; `cul30630` @ 219-222 -> 11044203; `cul30640` @ 360-363 -> 11044204; `cul30650` @ 416-419 -> 11044205; `cul30660` @ 609-612 -> 11044206; `cul30665` @ 629-632 -> 11044207; `cul30670` @ 805-808 -> 11044208 |
| `etc3l2` | `lua/scripts/quest/scenario/etc/etc3l2.lua`; `125CE463A3517063D6D19839AFD09088366F8F0B15CD8D0E19379AAA9186794F` | `etc3l210` @ 335-338 -> 11074501 |
| `etc3u2` | `lua/scripts/quest/scenario/etc/etc3u2.lua`; `2286F13B066CDAEB5F656894842CCF5A9EF1F45128A8FA9BFD84866CA4565885` | `etc3u210` @ 235-238 -> 11072701 |
| `etc5g0` | `lua/scripts/quest/scenario/etc/etc5g0.lua`; `74F9F5DCE38D53F19B82135F48B1595C0594B4EAF162E8930A38A32349F2CA0B` | `etc5g010` @ 368-371 -> 11082801 |
| `etc5l0` | `lua/scripts/quest/scenario/etc/etc5l0.lua`; `2160F72B57CB672810B31F48BA8B85AB7E438806401E733CCF0294C0EE26EB27` | `etc5l010` @ 348-351 -> 11083801 |
| `etc5l1` | `lua/scripts/quest/scenario/etc/etc5l1.lua`; `0088A8031C9B2848AD511AA54B8621D4AF9003F8A5F4A3C87003EA36ADC045DB` | `etc5l120` @ 165-170 -> 11083902 |
| `etc5l2` | `lua/scripts/quest/scenario/etc/etc5l2.lua`; `B4F30FB0658AFA79A67E1074FE41CB80425706A51D84579D1E01F1753536728A` | `etc5l210` @ 263-266 -> 11084001 |
| `etc5l3` | `lua/scripts/quest/scenario/etc/etc5l3.lua`; `989BEC5D388322AC93A2819C2E1B718F6A62396F4E551B972BACE986AD6FF2A9` | `etc5l320` @ 141-145 -> 11084104; `etc5l330` @ 244-248 -> 11084105 |
| `etc5u0` | `lua/scripts/quest/scenario/etc/etc5u0.lua`; `37693F54E7B011194FD5D7CA5B90EEE68EA62A318F838A7CBF4B21FFEEF7AEBE` | `etc5u010` @ 175-178 -> 11084801 |
| `exc200` | `lua/scripts/quest/scenario/exc/exc200.lua`; `28618B166241271CA4A12982DF5BAB7F2D173C0467B1D854AE98E593D218045F` | `exc20010` @ 54-57 -> 11010001; `exc20020` @ 160-163 -> 11010002; `exc20030` @ 180-183 -> 11010003; `exc20040` @ 200-203 -> 11010004; `exc20050` @ 220-223 -> 11010005 |
| `exc300` | `lua/scripts/quest/scenario/exc/exc300.lua`; `5F0CDDD8DDBC1AC27E57C32749FE1DB99C6DD5BC3D82098FEF2CB7C7E84D2D8D` | `exc30010` @ 30-33 -> 11010101; `exc30020` @ 58-61 -> 11010102; `exc30030` @ 168-171 -> 11010103 |
| `exc306` | `lua/scripts/quest/scenario/exc/exc306.lua`; `9CA53959191CF4C409C54DBA100DBA960043DD3F720B308C4A58B2842AFC5632` | `exc30610` @ 94-97 -> 11010201; `exc30620` @ 114-117 -> 11010202; `exc30630` @ 134-137 -> 11010203; `exc30640` @ 208-211 -> 11010204; `exc30650` @ 228-231 -> 11010205; `exc30660` @ 255-258 -> 11010206; `exc30670` @ 288-291 -> 11010207 |
| `fsh200` | `lua/scripts/quest/scenario/fsh/fsh200.lua`; `FC7CA4ED65AED15B81986FF7C328626AB07307CE2C69E89ABA0AB8DC0EEB2870` | `fsh20010` @ 135-138 -> 11050001; `fsh20020` @ 155-158 -> 11050002 |
| `fsh300` | `lua/scripts/quest/scenario/fsh/fsh300.lua`; `5F42576DC6DF7B28C0E635DBB6DA514237B890284A86F41591A3A7B44F7185AA` | `fsh30010` @ 102-106 -> 11050101; `fsh30020` @ 348-351 -> 11050102; `fsh30025` @ 395-398 -> 11050103; `fsh30030` @ 823-826 -> 11050104; `fsh30040` @ 870-873 -> 11050105; `fsh30050` @ 890-893 -> 11050106; `fsh30060` @ 1090-1093 -> 11050107; `fsh30070` @ 1119-1122 -> 11050108 |
| `fsh306` | `lua/scripts/quest/scenario/fsh/fsh306.lua`; `0C9E9D5DCCEEF511540E1C39AD8CE721B8C8A8A2EB587C7A2EFD7A20C955C93A` | `fsh30610` @ 187-190 -> 11050201; `fsh30620` @ 537-540 -> 11050202; `fsh30630` @ 788-791 -> 11050203; `fsh30640` @ 821-824 -> 11050204; `fsh30650` @ 865-868 -> 11050205; `fsh30660` @ 930-933 -> 11050206 |
| `gla200` | `lua/scripts/quest/scenario/gla/gla200.lua`; `AC3018F18FB763B9F30797E328382DB8981F678022C8536EB8E24EEAED01E71A` | `gla20010` @ 140-143 -> 11008001; `gla20020` @ 160-163 -> 11008002; `gla20030` @ 180-183 -> 11008003 |
| `gla300` | `lua/scripts/quest/scenario/gla/gla300.lua`; `CBF6D4E26390A5BD7E532FB725F2335D2CCB6E52C6AB9A50B35E52E44EDEFB82` | `gla30010` @ 35-38 -> 11008101; `gla30020` @ 66-69 -> 11008102; `gla30030` @ 129-132 -> 11008103; `gla30040` @ 149-152 -> 11008104; `gla30050` @ 192-195 -> 11008105; `gla30060` @ 242-245 -> 11008106; `gla30070` @ 303-306 -> 11008107; `gla30080` @ 323-326 -> 11008108 |
| `gla306` | `lua/scripts/quest/scenario/gla/gla306.lua`; `B3089EDB8FF203C43F9B86554299641490FAAB51470042F21A2D6AAFCC81DCD4` | `gla30610` @ 161-164 -> 11008201; `gla30620` @ 181-184 -> 11008203; `gla30615` @ 201-204 -> 11008202; `gla30630` @ 321-324 -> 11008204; `gla30640` @ 341-344 -> 11008205; `gla30650` @ 419-422 -> 11008206 |
| `gld300` | `lua/scripts/quest/scenario/gld/gld300.lua`; `64E0AD031DFC9FFE7E3F965F8BD0BAA5DCA64FDE97A4DC7DC9BF1050F8C5761F` | `gld30020` @ 112-117 -> 11036101; `gld30030` @ 134-137 -> 11036102; `gld30040` @ 154-157 -> 11036103; `gld30050` @ 174-177 -> 11036104; `gld30060` @ 264-267 -> 11036105; `gld30080` @ 419-422 -> 11036106 |
| `lnc200` | `lua/scripts/quest/scenario/lnc/lnc200.lua`; `BAFC5F9967E1B40B621D5FDB03222D6A1EA71F2AA3AF4A024BA2D71D38DCBD84` | `lnc20010` @ 130-133 -> 11018001; `lnc20020` @ 150-153 -> 11018002; `lnc20030` @ 170-173 -> 11018003 |
| `lnc300` | `lua/scripts/quest/scenario/lnc/lnc300.lua`; `5E41E548646FC133F7ED279A5146310B782FB43207FE09A7171E6B31C20B3166` | `lnc30010` @ 30-33 -> 11018101; `lnc30020` @ 72-77 -> 11018102; `lnc30030` @ 94-97 -> 11018103; `lnc30040` @ 115-118 -> 11018104; `lnc30050` @ 135-138 -> 11018105; `lnc30060` @ 155-158 -> 11018106; `lnc30065` @ 175-178 -> 11018107; `lnc30070` @ 216-219 -> 11018108 |
| `mnk0j3` | `lua/scripts/quest/scenario/mnk/mnk0j3.lua`; `22EC5BE8B7463F5628F49100A3FA593126A1E64B81A5B8071C4486DA0AA25AB1` | `mnk0j310` @ 468-471 -> 11122301 |
| `pgl300` | `lua/scripts/quest/scenario/pgl/pgl300.lua`; `7D24138D9B8509487E4BFCF3EBC67E4AF84BB06B4823E4CFB71B2A7AFD2FC903` | `pgl30010` @ 30-33 -> 11006101; `pgl30020` @ 51-54 -> 11006102; `pgl30030` @ 86-89 -> 11006103; `pgl30040` @ 106-109 -> 11006104; `pgl30050` @ 126-129 -> 11006105; `pgl30060` @ 177-180 -> 11006106; `pgl30070` @ 228-231 -> 11006107; `pgl30080` @ 279-282 -> 11006108 |
| `pgl306` | `lua/scripts/quest/scenario/pgl/pgl306.lua`; `B5E5C897B0921122270E8221C7213D2AA1340F26C15D7D6BAAC3C8EC87A850F3` | `pgl30610` @ 30-33 -> 11006201; `pgl30620` @ 51-54 -> 11006202; `pgl30630` @ 84-87 and 122-125 -> 11006203; `pgl30640` @ 160-163 and 198-201 -> 11006204; `pgl30650` @ 223-226 -> 11006205; `pgl30660` @ 243-246 -> 11006206; `pgl30670` @ 263-266 -> 11006207; `pgl30680` @ 283-286 -> 11006208 |
| `tan200` | `lua/scripts/quest/scenario/tan/tan200.lua`; `5FA1FA7DE98DD12946E0728077606F89E23DC340EC35551EEAA0D5340C5D4E98` | `tan20010` @ 319-322 -> 11038001; `tan20020` @ 360-363 -> 11038002; `tan20030` @ 611-614 -> 11038003; `tan20040` @ 1087-1090 -> 11038004; `tan20050` @ 1134-1137 -> 11038005 |
| `tan300` | `lua/scripts/quest/scenario/tan/tan300.lua`; `D703F3D3104880BD514CC6EC8FD4866C4BB7561ED7C4DDB052AC24754E811D67` | `tan30010` @ 100-103 -> 11038101; `tan30020` @ 120-123 -> 11038102; `tan30030` @ 167-170 -> 11038103; `tan30040` @ 187-190 -> 11038104; `tan30050` @ 207-210 -> 11038105 |
| `tan306` | `lua/scripts/quest/scenario/tan/tan306.lua`; `A02121F9CC70661BB00A51EBD4E3DAA8682EFD8F224F21FDED2F114312DACAD7` | `tan30610` @ 70-73 -> 11038201; `tan30620` @ 90-93 -> 11038202; `tan30630` @ 179-182 -> 11038203; `tan30640` @ 218-221 -> 11038204; `tan30650` @ 243-246 -> 11038205 |
| `thm200` | `lua/scripts/quest/scenario/thm/thm200.lua`; `50595B3F70416585E4BBD4C3593D06DE41A0CCA461F1E18BC77958E1934F9696` | `thm20010` @ 54-57 -> 11024001; `thm20020` @ 93-96 -> 11024002; `thm20030` @ 113-116 -> 11024003 |
| `thm300` | `lua/scripts/quest/scenario/thm/thm300.lua`; `C9E8F958ECCE4F460A5D23A690D0A57A12A76F7CDC508720B1D6DEACF741D275` | `thm30010` @ 35-38 -> 11024101; `thm30020` @ 63-66 -> 11024102; `thm30030` @ 270-273 and 322-325 -> 11024103; `thm30040` @ 647-650 -> 11024104 |
| `thm306` | `lua/scripts/quest/scenario/thm/thm306.lua`; `2F2402A4530D4CFD54EAE2EEF84AAC7E2AEE24C33EEA6983387D79C6B5D8AD48` | `thm30610` @ 35-38 -> 11024201; `thm30620` @ 63-66 -> 11024202; `thm30630` @ 83-86 -> 11024203; `thm30640` @ 126-129 -> 11024204; `thm30650` @ 146-149 -> 11024205; `thm30660` @ 166-169 -> 11024206 |
| `wdk200` | `lua/scripts/quest/scenario/wdk/wdk200.lua`; `FDBBA22B9736F052CF5B47C231C0CCD52780D5A1935294A6BC5AB1B0A2738FCC` | `wdk20010` @ 115-118 -> 11030001; `wdk20020` @ 135-138 -> 11030002; `wdk20030` @ 196-199 -> 11030003 |
| `wdk300` | `lua/scripts/quest/scenario/wdk/wdk300.lua`; `C619545A31D7D6B39288CC9C3ABC5CD2BE0164A4238EA1DE25F8C32BC40BA90E` | `wdk30010` @ 88-91 -> 11030101; `wdk30020` @ 108-111 -> 11030102; `wdk30030` @ 149-152 -> 11030103; `wdk30040` @ 169-172 -> 11030104; `wdk30050` @ 189-192 -> 11030105; `wdk30060` @ 320-323 -> 11030106 |
| `wdk306` | `lua/scripts/quest/scenario/wdk/wdk306.lua`; `723E60FFD6F22D9962363CA718ECE6C8E6B7DA1B0E56EC7DD3809D21CEAF3EEF` | `wdk30610` @ 123-126 -> 11030201; `wdk30620` @ 143-146 -> 11030202; `wdk30630` @ 243-246 -> 11030203; `wdk30640` @ 263-266 -> 11030204; `wdk30650` @ 283-286 -> 11030205; `wdk30660` @ 303-306 -> 11030206 |

Across these 41 modules, the inventory contains 176 literal calls and 173
unique keys. Every listed key joins at least one row in the pinned table.
Repeated calls and multiple table rows are preserved as observed; they do not
prove repeated playback or shared runtime interpretation.

## Cross-family scene keys

The other ten audited modules also contain literal calls; their keys do not
use their module code as a prefix. These 23 calls join 15 distinct keys to
the static table. The six keys marked `no row` have no exact-key match in the
pinned `cutReplay.csv`.

| Module | Canonical source; SHA-256 | Literal calls and row joins |
| --- | --- | --- |
| `etc106` | `lua/scripts/quest/scenario/etc/etc106.lua`; `6E15C5F1DA729837D360FAA117A7BAFC14BBCA3EEA68C6B0FAB8FA2A9C8A3C10` | `wpn0f010` @ 5524-5529 -> no row |
| `gcg103` | `lua/scripts/quest/scenario/gcg/gcg103.lua`; `69B6366A1620DAF93A2DD356086AFC0CDC12596BDB5DAF4E2B2A381721B0B788` | `gc01g310` @ 426-429 -> 11162901; `gc01g320` @ 453-456 -> 11162902 |
| `gcl103` | `lua/scripts/quest/scenario/gcl/gcl103.lua`; `4136966B4DD5A01382E9EA8BDD4416D0C4A716EFA06FE1C2A432FBF06099BB52` | `gc01l310` @ 394-397 -> 11142901; `gc01l320` @ 421-424 -> 11142902 |
| `gcl104` | `lua/scripts/quest/scenario/gcl/gcl104.lua`; `5D54007D0DBD617F6D1DFE6297151FD01DC3BB52869155DC778D88BBEB0D4F5B` | `elv0l110` @ 1978-1982 -> no row; `gc01l410` @ 1984-1988 -> 11143004; `gc010410` @ 2017-2021 -> 11143001, 11163001, 11183001; `gc01g410` @ 2038-2042 -> 11163004; `gc01u410` @ 2059-2063 -> 11183004 |
| `gcl105` | `lua/scripts/quest/scenario/gcl/gcl105.lua`; `82F3923761541A63D265939D94FFC08E6F7778D5013F02B7D9CB03426D1D5D54` | `elv0l110` @ 3998-4002 -> no row; `gc010620` @ 4085-4090 -> 11143102, 11163102, 11183102; `gc010610` @ 4107-4113 -> 11143101, 11163101, 11183101 |
| `gcl106` | `lua/scripts/quest/scenario/gcl/gcl106.lua`; `505C8F51B325ED997EEDCBE367705252B61C18577B3B43F7C47124BC0BA0447D` | `elv0l110` @ 793-797 -> no row |
| `gcl107` | `lua/scripts/quest/scenario/gcl/gcl107.lua`; `98CE0AE86655ECCFFBC15234091DBBBA9ACC847C1BBB099AE8F5F64BFDAB1345` | `gc010750` @ 2520-2525 -> 11143308, 11163308, 11183308; `gc010710` @ 2554-2558 -> 11143301, 11163301, 11183301; `gc010714` @ 2575-2580 -> 11143302, 11143303, 11163302, 11163303, 11183302, 11183303 |
| `gcu103` | `lua/scripts/quest/scenario/gcu/gcu103.lua`; `850E6B9A903A1BE7F7CD4B918C0EC269DB1A17D82A179C266BA0B1963B523BE5` | `gc01u320` @ 318-321 -> 11182901; `gc01u310` @ 505-508 -> 11182902 |
| `trl0g1` | `lua/scripts/quest/scenario/trl/trl0g1.lua`; `951DB61AC9E8CC07D223CD0C5DFA235C7C55A36F10EC287E2284C12BEE4CB197` | `man0g225` @ 64-67 -> no row; `man0g230` @ 84-87 -> no row |
| `trl0l1` | `lua/scripts/quest/scenario/trl/trl0l1.lua`; `D9B45E1E0241E69BCD8F46F3F66246856323A33550B1C2B62E7F4F9DC6BB80D7` | `man0l640` @ 64-67 -> no row; `man0l650` @ 84-87 -> no row |

The caller and table join alone do not establish why a key crosses module
families, whether any call was reached, or what the corresponding row means
at runtime. No quest ownership, server route, activation condition, or
historical playback conclusion is inferred.

## Additional bounded module selection

A second bounded set adds 74 modules beyond the 51 above. The source files and
line locators below use the same `scripts.json` identities and exact
`cutReplay.csv` field-1 join described above. The 74 files contain 331 direct
literal references; `fsh300` and `fsh306` were rechecked as controls with 14
more references. Across those 76 files there are 345 calls and 289
unique literal keys: 269 keys join one or more rows, while 20 keys have no
exact row. This produces 319 row-bearing call sites, 26 no-row call sites,
and 273 distinct replay-row IDs. Ten case-only spelling differences affect
12 calls; absent runtime alias evidence, those source literals remain
unmatched. Only source-literal calls are recorded below. Two
files, `man304` and `man402`, have no direct `startNQCutScene` field
references; the other 72 contain at least one. This bounded selection is not
a full-corpus absence audit.

Each entry is `literal-key @ inclusive-source-lines -> replay-row-ID(s)`;
`no row` means no exact-key match in the pinned table. Repeated source calls
are preserved.

| Module | Canonical source; SHA-256 | Direct literal calls and row joins |
| --- | --- | --- |
| `alc200` | `lua/scripts/quest/scenario/alc/alc200.lua`; `1DF269E26B25CF240A7D5C0AC6E27E13C60FEB649E62BED2EC31879ADACD08B5` | `alc20010` @ 60-63 -> 11042001; `alc20020` @ 164-169 -> 11042002; `alc20030` @ 191-196 -> 11042003 |
| `arc200` | `lua/scripts/quest/scenario/arc/arc200.lua`; `E72052136CC3A647276D715A9AA9AFAB7D152C538DE06E419287EBCFC3CCD877` | `arc20010` @ 118-121 -> 11016001; `arc20020` @ 138-141 -> 11016002; `arc20030` @ 162-167 -> 11016003; `arc20040` @ 184-187 -> 11016004 |
| `arc306` | `lua/scripts/quest/scenario/arc/arc306.lua`; `E0AFEC8EF21AB82564E68D803AF87677021197A3992FA5A89A1C308430EDBA8E` | `arc30610` @ 100-103 -> 11016201; `arc30620` @ 120-123 -> 11016202; `arc30630` @ 140-143 -> 11016203; `arc30640` @ 160-163 -> 11016204; `arc30650` @ 180-183 -> 11016205 |
| `blm0j1` | `lua/scripts/quest/scenario/blm/blm0j1.lua`; `0BA832CCFD467C31C09EF4B023C0BE3921BD5A4154E4574A9E75902BE8BE82C3` | `blm0j110` @ 386-389 -> 11126101; `blm0j120` @ 526-529 -> 11126102 |
| `blm0j6` | `lua/scripts/quest/scenario/blm/blm0j6.lua`; `AEB8D06AA492D5BF8A597005DA955AEB55DF072067209728210F987FC739BC27` | `blm0j610` @ 827-830 -> 11126601; `blm0j620` @ 854-857 and 874-877 -> 11126602 |
| `brd0j4` | `lua/scripts/quest/scenario/brd/brd0j4.lua`; `26A81B9A83D9299284FAEF28D658A5D33F1C207036DC16572D30778BD6DA04FB` | `brd0j410` @ 287-290 and 314-317 -> 11130401; `brd0j420` @ 334-337 -> 11130402 |
| `brd0j6` | `lua/scripts/quest/scenario/brd/brd0j6.lua`; `99B986C51617C80B22471D35B2AD2BF7DD88587730CC215BD6BDC9F94596C8B3` | `brd0j610` @ 397-400 -> 11130601 |
| `bsm200` | `lua/scripts/quest/scenario/bsm/bsm200.lua`; `AABE5F4A91722C0D8CF36351AF1D9FB8BC551335F199387B288032ED11D8483C` | `bsm20010` @ 196-201 -> 11032001, 11032002; `bsm20020` @ 218-221 -> 11032003 |
| `bsm306` | `lua/scripts/quest/scenario/bsm/bsm306.lua`; `7961DD8E5DCEDEE84FC9B47520A00D5BD4EDE66E3810005B50B2F8A8F82BBB5F` | `bsm30610` @ 263-268 -> 11032201, 11032202; `bsm30620` @ 285-288 -> 11032203; `bsm30630` @ 301-304 -> 11032204; `bsm30640` @ 321-324 -> 11032205 |
| `cnj306` | `lua/scripts/quest/scenario/cnj/cnj306.lua`; `DBF1B35B62117FDBFC90A082DC71472C5ACDDF5347603A8DDB06751A4ADB811A` | `cnj30610` @ 392-395 -> 11026201; `cnj30620` @ 499-502 -> 11026202; `cnj30630` @ 562-565 -> 11026203; `cnj30640` @ 636-639 -> 11026204; `cnj30650` @ 681-684 -> 11026205; `cnj30660` @ 701-704 -> 11026206; `cnj30670` @ 721-724 -> 11026207; `cnj30680` @ 978-981 -> 11026208; `cnj30690` @ 998-1001 and 1018-1021 -> 11026209 |
| `com0g1` | `lua/scripts/quest/scenario/com/com0g1.lua`; `A8F8FFC69BE96E99E16ECED6AC6C8FAE7FD702EA5E4B78CBD99C60980F926AEF` | `COM0G105` @ 292-295 -> no row; `COM0G110` @ 320-325 -> no row |
| `com0g4` | `lua/scripts/quest/scenario/com/com0g4.lua`; `B5FEEE327FBE8B03F474A5DA9DBA303520D28CCAA724FC4463B65438FE910F7E` | `com0g410` @ 551-554 -> 11160401 |
| `com0g5` | `lua/scripts/quest/scenario/com/com0g5.lua`; `7217C217B432346737096FCE288651426C8029462905E9DFAD52FA0F96E9A373` | `com0g610` @ 222-225 -> 11160501 |
| `com0g6` | `lua/scripts/quest/scenario/com/com0g6.lua`; `5378A3764D799F21DE962D0FAFD451A29C5539D26A443D1AFEA63FC573C4A644` | `COM0G510` @ 954-957 -> no row |
| `com0l1` | `lua/scripts/quest/scenario/com/com0l1.lua`; `9074D51B77C895376B0880D12488EE0D1773A2AC611363F4AD7AA02DF8C6EBFE` | `COM0L105` @ 293-296 -> no row; `COM0l110` @ 471-476 -> no row |
| `com0l4` | `lua/scripts/quest/scenario/com/com0l4.lua`; `B986AFF3363BF9C5916AB2E096B2343528278FB91D37265825C36190E35E680D` | `com0l410` @ 619-622 -> 11140401 |
| `com0l5` | `lua/scripts/quest/scenario/com/com0l5.lua`; `D250DE2089F898219B19318D268D24AD1222C8C24577009BE4B782461CBED3D3` | `COM0l110` @ 390-394 -> no row; `elv0l110` @ 676-680 -> no row; `com0l610` @ 682-686 -> 11140501; `elv0l110` @ 733-737 -> no row |
| `com0l6` | `lua/scripts/quest/scenario/com/com0l6.lua`; `B491A913CCB6323FD06F33AD914DBA84EBCDA6C095C2685025CDD62B847BF893` | `com0l510` @ 487-492 -> 11140601; `elv0l01a` @ 1001-1005 -> no row; `elv0l02a` @ 1023-1027 -> no row |
| `com0u1` | `lua/scripts/quest/scenario/com/com0u1.lua`; `4B70ABC5299BC1F2B816AE46B933DFA513EF262A4DD369F4196211B550059CA9` | `COM0U105` @ 263-266 -> no row; `COM0U110` @ 290-295 -> no row |
| `com0u4` | `lua/scripts/quest/scenario/com/com0u4.lua`; `8CE38A9BDEBA006F146F5D281CC21C45B58DEACACA2A508631216BCF45583CBA` | `com0u410` @ 524-527 -> 11180401 |
| `com0u5` | `lua/scripts/quest/scenario/com/com0u5.lua`; `A00382D68B8DC0198E4F244D461F678A2D0B97DCC485CCE113A4D4F1DE91F22E` | `com0u610` @ 681-684 -> 11180501 |
| `com0u6` | `lua/scripts/quest/scenario/com/com0u6.lua`; `C7310059A36EF32D2A5DB013FBD94D41907995CEAC8EF1B71C22A8BAC57F5B7C` | `com0u510` @ 423-428 -> 11180601; `elv0u01a` @ 890-894 -> no row; `elv0u02a` @ 912-916 -> no row |
| `drg0j1` | `lua/scripts/quest/scenario/drg/drg0j1.lua`; `FA02792E6F1EB30FDB0F969EE93D0297277D75765F2E0EF3A4DE649F5B5C869E` | `drg0j110` @ 603-606 -> 11132101 |
| `drg0j4` | `lua/scripts/quest/scenario/drg/drg0j4.lua`; `F704B33562D944A1DD1F1449FAFC14BEA353678E9ED004E6EE8E351AD7A630CF` | `Drg0j410` @ 168-171 -> no row |
| `drg0j6` | `lua/scripts/quest/scenario/drg/drg0j6.lua`; `529D76BBD4830921D4211EF405E08B2881A0B7249BFFDC5EDF6EBA6942972733` | `Drg0j610` @ 159-162 -> no row; `Drg0j620` @ 194-197 and 214-217 -> no row |
| `etc304` | `lua/scripts/quest/scenario/etc/etc304.lua`; `470B87D0ECBAB44CA86F5D073082ED8EF98096A77A9EC3F6A046284F3DEFC03B` | `gc010810` @ 308-313 -> 11086901; `gc010820` @ 381-385 -> 11086902; `gc010830` @ 399-403 -> 11086903; `gc010840` @ 417-421 -> 11086905; `gc010850` @ 435-440 -> 11086904; `gc010860` @ 467-471 -> 11086906 |
| `etc3g2` | `lua/scripts/quest/scenario/etc/etc3g2.lua`; `CB2EDD30C6FFEC1FFF42D34F934CE3158AC27FAC5C2943D7FE010DEDC868364E` | `etc3g210` @ 421-424 -> 11073601 |
| `gcg102` | `lua/scripts/quest/scenario/gcg/gcg102.lua`; `3BB5A88A88D28E7D302DE934836F294F0342C99272D14A4BEB756AB8B7837495` | `gc01g210` @ 495-498 -> 11162701 |
| `gcl102` | `lua/scripts/quest/scenario/gcl/gcl102.lua`; `89DEF899D0E3CD992C6B660D344AC661A0837E5E69745B16576A481F7953CF27` | `gc01l210` @ 456-459 -> 11142701 |
| `gcu102` | `lua/scripts/quest/scenario/gcu/gcu102.lua`; `D89B813B4713021BA5A0EAD4F9AAD90F9D5868168549A57503E6E16B48175E11` | `gc01u210` @ 532-535 -> 11182701; `elv0u01a` @ 995-999 -> no row; `elv0u02a` @ 1017-1021 -> no row |
| `gld200` | `lua/scripts/quest/scenario/gld/gld200.lua`; `497ECDCA1F9A2CE287060183A6254C141ED6D5F7CFC1454F689603FCE3901F33` | `gld20020` @ 184-187 -> 11036001; `gld20030` @ 204-207 -> 11036002; `gld20040` @ 224-227 -> 11036003; `gld20050` @ 287-290 -> 11036004 |
| `gld306` | `lua/scripts/quest/scenario/gld/gld306.lua`; `12376F2B7FE8AAD0E80422D2B91C0620D5A986D5D27FCC0D2DF3F5510357FDB0` | `gld30610` @ 30-33 -> 11036201; `gld30615` @ 111-114 -> 11036202; `gld30620` @ 131-134 -> 11036203; `gld30630` @ 194-197 -> 11036204 |
| `hrv200` | `lua/scripts/quest/scenario/hrv/hrv200.lua`; `8D7C922D5DA254B5D151041F48FA184FBD583E8C3E50A17FF2B3B169F4D3457B` | `hrv20010` @ 128-131 -> 11048001; `hrv20020` @ 148-151 and 168-171 -> 11048002; `hrv20030` @ 188-191 -> 11048003 |
| `hrv300` | `lua/scripts/quest/scenario/hrv/hrv300.lua`; `D6C61E5C5FCD01F5A02DBCE42FED2473E00BB81D256BE665B828E8C98E75949B` | `hrv30010` @ 106-109 -> 11048101; `hrv30020` @ 354-357 -> 11048102; `hrv30030` @ 467-470 -> 11048103; `hrv30040` @ 508-511 -> 11048104 |
| `hrv306` | `lua/scripts/quest/scenario/hrv/hrv306.lua`; `27D5E6360FABE9FFE462D9818F32EB5A4E21B591E6E644103D0A913E330BA090` | `hrv30610` @ 88-91 -> 11048201; `hrv30620` @ 116-119 -> 11048202; `hrv30630` @ 136-140 -> 11048203, 11048204; `hrv30640` @ 314-317 -> 11048205; `hrv30650` @ 385-388 -> 11048206; `hrv30660` @ 405-408 -> 11048207; `hrv30670` @ 425-428 -> 11048208 |
| `lnc306` | `lua/scripts/quest/scenario/lnc/lnc306.lua`; `3DA0281274E9B9700D9700E47EC197736DAB92D39D9585F2CAA39AD3DB03C626` | `lnc30610` @ 82-85 -> 11018201; `lnc30620` @ 102-105 -> 11018202; `lnc30630` @ 122-125 -> 11018203; `lnc30640` @ 182-185 -> 11018204; `lnc30650` @ 202-205 -> 11018205 |
| `man0g1` | `lua/scripts/quest/scenario/man/man0g1.lua`; `8B0988C285974162A150638156826605B75E093C9F6EB8F33B99B6D139A195B8` | `man0g100` @ 30-33 -> 11000601; `man0g110` @ 303-306 -> 11000602; `man0g120` @ 571-574 -> 11000603; `man0g130` @ 697-700 -> 11000604; `man0g135` @ 926-929 and 946-949 -> 11000605; `man0g140` @ 1038-1041 -> 11000606; `man0g150` @ 1415-1418 -> 11000607; `man0g160` @ 1488-1491 -> 11000608; `man0g170` @ 1508-1511 -> 11000609; `man0g180` @ 1528-1531 -> 11000610; `man0g181` @ 1569-1572 -> 11000611; `man0g182` @ 1589-1592 -> 11000612; `man0g185` @ 1636-1639 -> 11000613; `man0g190` @ 1689-1692 -> 11000614; `man0g200` @ 1730-1733 -> 11000615; `man0g210` @ 1918-1921 -> 11000616; `man0g220` @ 1959-1962 -> 11000617 |
| `man0l1` | `lua/scripts/quest/scenario/man/man0l1.lua`; `FEA9C9359AC610737BE1B5910D473D98F5174512DDF01F0B730F9E0F608F8C67` | `man0l110` @ 30-33 and 2740-2743 -> 11000201; `man0l120` @ 253-256 and 2754-2757 -> 11000202; `man0l130` @ 581-584 and 2768-2771 -> 11000203; `man0l140` @ 701-704 and 2782-2785 -> 11000204; `man0l150` @ 748-751 and 2796-2799 -> 11000205; `man0l160` @ 1130-1133 and 1150-1153 -> 11000206; `man0l600` @ 1236-1239 and 2824-2827 -> 11000207; `man0l604` @ 1657-1660 and 2838-2841 -> 11000208; `man0l605` @ 1707-1710 and 2852-2855 -> 11000209; `man0l610` @ 1740-1743 and 2866-2869 -> 11000210; `man0l615` @ 1773-1776 and 2880-2883 -> 11000211; `man0l620` @ 1820-1823 and 2894-2897 -> 11000212; `man0l630` @ 1890-1893 and 2908-2911 -> 11000213; `man0l635` @ 2166-2169 and 2922-2925 -> 11000214; `man0l420` @ 2810-2813 -> no row; `man0l640` @ 2936-2939 -> no row; `man0l650` @ 2950-2953 -> no row |
| `man0u1` | `lua/scripts/quest/scenario/man/man0u1.lua`; `31FC9EBF234B4945F3CBBE6B7C5F1493C659A2A584D508C778F9351089FEB10A` | `man0u100` @ 30-35 -> 11001001; `man0u110` @ 332-335 -> 11001002; `man0u120` @ 666-669 -> 11001003; `man0u130` @ 732-735 -> 11001004; `man0u135` @ 1104-1107 -> 11001005; `man0u140` @ 1124-1127 and 1144-1147 -> 11001006; `man0u150` @ 1209-1212 -> 11001007; `man0u160` @ 1880-1883 -> 11001008; `man0u170` @ 2026-2029 -> 11001009; `man0u175` @ 2046-2049 -> 11001010; `man0u180` @ 2066-2069 -> 11001011; `man0u190` @ 2315-2318 -> 11001012; `man0u200` @ 2324-2327 and 2344-2347 -> 11001013; `man0u205` @ 2391-2394 -> 11001014; `man0u210` @ 2471-2474 -> 11001015; `man0u220` @ 2644-2647 -> 11001016; `man0u230` @ 2664-2667 -> 11001017 |
| `man1g0` | `lua/scripts/quest/scenario/man/man1g0.lua`; `9AD456BE9D6CCA4219EC3DCCB0A9ECA1DA7017BFAF0CE166276CA214AC91E6AA` | `man1g000` @ 30-33 -> 11000701; `man1g010` @ 77-80 -> 11000702; `man1g020` @ 262-265 -> 11000703; `man1g030` @ 345-348 -> 11000704; `man1g040` @ 365-368 -> 11000705; `man1g050` @ 412-415 -> 11000706; `man1g060` @ 459-462 -> 11000707; `man1g070` @ 500-503 -> 11000708; `man1g080` @ 520-523 -> 11000709; `man1g090` @ 582-585 -> 11000710; `man1g100` @ 692-695 -> 11000711 |
| `man1l0` | `lua/scripts/quest/scenario/man/man1l0.lua`; `DB1FAE3A325BF813F8DC872A1985B421657FA85303C07F6633B2ECF1C2D8E131` | `man1l200` @ 30-33 and 1116-1119 -> 11000301; `man1l210` @ 201-204 and 1130-1133 -> 11000302; `man1l215` @ 221-224 -> 11000303; `man1l400` @ 268-271 and 1144-1147 -> 11000304; `man1l410` @ 392-395 and 1158-1161 -> 11000305; `man1l420` @ 492-495 -> 11000306; `man1l600` @ 539-542 and 1172-1175 -> 11000307; `man1l610` @ 605-610 and 1186-1189 -> 11000308; `man2l000` @ 654-659 -> 11000309; `man2l001` @ 943-946 -> 11000310; `man2l002` @ 963-966 -> 11000311 |
| `man1u0` | `lua/scripts/quest/scenario/man/man1u0.lua`; `67233F2A2EF5F81EBCEF30F197950666132DD950BF09265C0765C5ED06A577B6` | `man1u000` @ 30-33 -> 11001101; `man1u010` @ 200-203 -> 11001102; `man1u020` @ 523-526 -> 11001103; `man1u021` @ 690-693 -> 11001104; `man1u030` @ 830-833 -> 11001105; `man1u040` @ 850-853 -> 11001106; `man1u050` @ 897-900 -> 11001107; `man1u060` @ 950-953 -> 11001108; `man1u070` @ 970-973 -> 11001109; `man1u080` @ 1146-1149 -> 11001110; `man1u090` @ 1187-1190 -> 11001111 |
| `min200` | `lua/scripts/quest/scenario/min/min200.lua`; `A8FCFC80E18FA5BD0B6CC257499FA4B09F9A4895ACE3E8138085725E39B5F44D` | `min20010` @ 135-138 -> 11046001; `min20020` @ 302-305 -> 11046002; `min20030` @ 322-325 -> 11046003; `min20035` @ 416-419 -> 11046004 |
| `min300` | `lua/scripts/quest/scenario/min/min300.lua`; `6C655557F1E3528EB7C89E18450BA435C1A2AB8791C37D3E0DFE57529DE906BB` | `min30010` @ 82-85 -> 11046101; `min30020` @ 150-153 -> 11046102; `min30030` @ 197-200 -> 11046103; `min30040` @ 217-220 -> 11046104; `min30050` @ 237-240 -> 11046105; `min30060` @ 270-273 -> 11046106; `min30070` @ 316-319 -> 11046107 |
| `mnk0j1` | `lua/scripts/quest/scenario/mnk/mnk0j1.lua`; `05BD79480BBDDE017B8AB37E4054136046F9814B95E9353DF8744B78F1846779` | `mnk0j110` @ 360-363 -> 11122101 |
| `mnk0j6` | `lua/scripts/quest/scenario/mnk/mnk0j6.lua`; `875D773E291211A91912159BBD2AE5C83004364937A8198D08D8EA15F53100C5` | `mnk0j610` @ 408-411 -> 11122601; `mnk0j620` @ 435-438 -> 11122602 |
| `pgl200` | `lua/scripts/quest/scenario/pgl/pgl200.lua`; `52019BBDE88285ECA89B10C7EF74626536CFFBB772961489BCAD5927AE288BFA` | `pgl20010` @ 121-124 -> 11006001; `pgl20020` @ 153-156 -> 11006002; `pgl20030` @ 178-181 -> 11006003; `pgl20040` @ 224-227 -> 11006004; `pgl20050` @ 255-258 -> 11006005; `pgl20060` @ 275-278 -> 11006006; `pgl20070` @ 295-298 -> 11006007 |
| `pld0j1` | `lua/scripts/quest/scenario/pld/pld0j1.lua`; `6E623C417E2D317606F82A2CF1EBE481E3474C06199EAC106D5EC082AC74EAAF` | `pld0j110` @ 330-333 and 370-373 -> 11128101 |
| `pld0j5` | `lua/scripts/quest/scenario/pld/pld0j5.lua`; `5D51DE1AF192A8A5BEAC939F5186D13BDC0F9C26340E6C372A299DB8117C5107` | `pld0j510` @ 147-150 -> 11128501; `pld0j520` @ 174-177 -> 11128502 |
| `pld0j6` | `lua/scripts/quest/scenario/pld/pld0j6.lua`; `BF21AD4B8303C27F02CCE4BD43ED296C493AC39C22F608D46C9830B09FCBE7F0` | `pld0j610` @ 459-462 -> 11128601; `pld0j620` @ 486-489 and 506-509 -> 11128602 |
| `spl0i4` | `lua/scripts/quest/scenario/spl/spl0i4.lua`; `E7F5417070562D687851EDBC0B873B3DC86EBEA88B4586BC22B4B432DF088FC2` | `spl0i410` @ 251-254 -> 11080201 |
| `war0j3` | `lua/scripts/quest/scenario/war/war0j3.lua`; `B4DDEC6CF017B82B82FA10E85602D79D447A6C4DA6BB903B91FBEE6F2C88525D` | `war0j310` @ 217-222 -> 11120301 |
| `whm0j1` | `lua/scripts/quest/scenario/whm/whm0j1.lua`; `8DCD654151A97E05DA0A502AA78E37D9C4374A5B57A984A5FB093AD2528455CB` | `whm0j110` @ 437-440 -> 11124101 |
| `whm0j2` | `lua/scripts/quest/scenario/whm/whm0j2.lua`; `0706DCB5E5DE02900F5D197348667AEF679E93B3F95EAAACCCAC934DC0740912` | `whm0j210` @ 35-38 -> 11124201 |
| `whm0j4` | `lua/scripts/quest/scenario/whm/whm0j4.lua`; `7A3048873BCAFED7A159FD5811119EFBA5A1EC3C54D8065FDCB225AA8833B9EA` | `whm0j410` @ 379-382 -> 11124401 |
| `whm0j6` | `lua/scripts/quest/scenario/whm/whm0j6.lua`; `894C00C20B7C6AD83CBC79AA44D32A1111C949AD6817A0F71E738D4C867DD959` | `whm0j605` @ 280-283 -> 11124601; `whm0j610` @ 447-450 and 741-744 -> 11124602 |
| `wvr200` | `lua/scripts/quest/scenario/wvr/wvr200.lua`; `386D3E89234978AC21294904094227668A094D09FF1B8904434A981852EC5ACD` | `wvr20010` @ 134-137 -> 11040001; `wvr20020` @ 154-157 -> 11040002; `wvr20030` @ 174-177 -> 11040003 |
| `wvr300` | `lua/scripts/quest/scenario/wvr/wvr300.lua`; `5D762A20B51564D11CACC9A03EF344D3636F7CB51C2E86FCC3CBB0559C67450C` | `wvr30010` @ 30-33 -> 11040101; `wvr30020` @ 300-303 -> 11040102 |
| `wvr306` | `lua/scripts/quest/scenario/wvr/wvr306.lua`; `B7F9F53BB0D868048D652D8F91ED14AFF50927514B9BB1C1AAE8A73F9446F9D0` | `wvr30610` @ 156-159 -> 11040201; `wvr30620` @ 176-179 -> 11040202; `wvr30630` @ 196-199 -> 11040203 |

The remaining 15 modules in this bounded set are listed below. Only direct Lua
literals are recorded, with exact-key joins to the pinned table.

| Module | Canonical source; SHA-256 | Direct source calls and row joins |
| --- | --- | --- |
| `man0g0` | `lua/scripts/quest/scenario/man/man0g0.lua`; `BD367F6606CFF7EB4D43D76B15726B5075B3BF786E53C4B8EBF64D90DD65FD0B` | `MAN0G000` @ 31-33 -> no exact-key row; `man0g005` @ 432-435 and 658-661 -> 11000502 |
| `man0l0` | `lua/scripts/quest/scenario/man/man0l0.lua`; `0F3165390756B2DAF960B978E3C05F094B1FF1A068E3468757A82A6AD3F25F39` | `man0l005` @ 970-973 and 1239-1242 -> 11000102 |
| `man0u0` | `lua/scripts/quest/scenario/man/man0u0.lua`; `0CA29669ACAB5E7F5CCF12A5AE1F692552E51F308D9DC704E2B161E57907A71F` | `man0u005` @ 744-747 and 1015-1018 -> 11000902 |
| `man200` | `lua/scripts/quest/scenario/man/man200.lua`; `42CE1C6D33E093E262A88EE9BECC294C4BF2E9DE40FF945EB4830DC3A598EDB6` | `man20140` @ 1393-1403 and 1542-1552 -> no row |
| `man206` | `lua/scripts/quest/scenario/man/man206.lua`; `C353741B99093F8A3414D2CD3A668FF356C21EF72F2E01F366184E9BDF934256` | `man20600` @ 30-33 -> 11001401; `man20601` @ 254-257 -> 11001402; `man20640` @ 1149-1152 -> 11001408 |
| `man2g0` | `lua/scripts/quest/scenario/man/man2g0.lua`; `52421271441FF2B253C4150EC5154601D0013EAB9ECD1F75200F6FD14F55B90A` | `man1g900` @ 110-113 -> 11000801; `man2g010` @ 238-241 -> 11000803; `man2g020` @ 279-282 -> 11000804; `man2g030` @ 373-376 -> 11000805; `man2g040` @ 567-570 -> 11000806; `man2g050` @ 742-745 -> 11000807; `man2g060` @ 789-792 -> 11000808; `man2g070` @ 1352-1355 -> 11000809; `man2g080` @ 1414-1417 -> 11000810; `man2g095` @ 1424-1427 -> 11000812; `man2g100` @ 1429-1432 -> 11000813 |
| `man2l0` | `lua/scripts/quest/scenario/man/man2l0.lua`; `307F73A32656EB7ED65BF3B6F57184A9AB8CEAFF063C10800D6AE52F3AC67966` | `man2l030` @ 808-811 -> 11000407; `man2l090` @ 906-909 -> 11000414 |
| `man2u0` | `lua/scripts/quest/scenario/man/man2u0.lua`; `7EB43E5B29ACC9E9B76164C568A5EAB3049599F93FCBAB2A45F67C9F6859DEE7` | `man2u000` @ 96-99 -> 11001201; `man2u010` @ 101-104 -> 11001202; `man2u030` @ 258-261 -> 11001204; `man2u040` @ 311-314 -> 11001205; `man2u050` @ 415-418 -> 11001206; `man2u060` @ 456-459 -> 11001207; `man2u070` @ 509-512 -> 11001208; `man2u080` @ 556-559 -> 11001209; `man2u085` @ 576-579 -> 11001210; `man2u100` @ 586-589 -> 11001212; `man2u110` @ 591-594 -> 11001213 |
| `man300` | `lua/scripts/quest/scenario/man/man300.lua`; `965E584C459535E6862F5534ECBEF2B12FAAF6963441DD3F90494D9286FAFECB` | `man30000` @ 30-33 -> 11001501; `man30010` @ 450-453 -> 11001502 |
| `man304` | `lua/scripts/quest/scenario/man/man304.lua`; `1967477F272DFC1E474382C67AAAE2128F61C7D5CCB1BA999DF7B6938B6DBD03` | No direct `startNQCutScene` field references or calls found |
| `man308` | `lua/scripts/quest/scenario/man/man308.lua`; `9A63E78A281C233783C8E18BA280FE88CE664E14DCE01D36125CF36FC6DF7E9B` | `man30890` @ 1030-1033 -> 11001708 |
| `man402` | `lua/scripts/quest/scenario/man/man402.lua`; `8EEC243C2F79A4F3D557963A905FFB0380C3AD3817487DC7F7C386F365ED0FBB` | No direct `startNQCutScene` field references or calls found |
| `man406` | `lua/scripts/quest/scenario/man/man406.lua`; `031BAE3D9927529A89A3540F8F0781F52B5A75FA566C705E42D50B9D6C5E389B` | `man40620` @ 746-749 -> 11001904; `man40645` @ 818-821 -> no row |
| `min306` | `lua/scripts/quest/scenario/min/min306.lua`; `8DBF495BC661232737BE08031396C05DAE1FB0F33376258B9EEA46A57ED48D12` | `min30610` @ 102-105 -> 11046201; `min30620` @ 122-125 -> 11046202; `min30630` @ 142-145 -> 11046203; `min30640` @ 189-192 -> 11046204 |
| `war0j6` | `lua/scripts/quest/scenario/war/war0j6.lua`; `45C1373FB1F69305D7B713B5418D1C5ED72F5EEA9E1ECC80552A91742D6C86F5` | `war0j610` @ 199-202 -> 11120601; `war0j620` @ 244-247 -> 11120602 |

## SNPC launcher and replay-row joins

This supplement records direct Lua 5.1 bytecode calls through `startSnpcNQCutScene`,
`startSnpcHQCutScene`, or `startNQCutScene` whose exact replay-key joins were
established in the decoded scenario chunks. The eight source paths below are
classified `matched-script` in `manifests/retail_lua_coverage.json`. Their
`decodedPayloadSha256` values identify the pinned payloads; the examined Lua
chunks matched those hashes. Each PC tuple is `SELF / LOADK / CALL` within the
named prototype. The `LOADK` contains the literal scene key; `SELF` selects
the launcher method.

| Decoded script path | Decoded payload SHA-256; coverage locator |
| --- | --- |
| `lua/scripts/quest/scenario/man/man200.lua` | `8B9D472804DBBFF2A2FA4397CD91D9514593A991FEBCCAF259E6FDBDF9101CA3`; `retail_lua_coverage.json:39568-39576` |
| `lua/scripts/quest/scenario/man/man206.lua` | `0461FC2DEF0F392FA0E952A4557AB1421BA96302D1192F1AE4456AC929C9AF71`; `retail_lua_coverage.json:39553-39561` |
| `lua/scripts/quest/scenario/man/man2l0.lua` | `F78870ADEED3F85B0C71758DA74EF47BB77B2D2AB99546C5F33C8A5D987BD65F`; `retail_lua_coverage.json:39598-39606` |
| `lua/scripts/quest/scenario/man/man300.lua` | `CCF8CD853C3AA6568E05DDFE702B42AC97A041783D5EC3B549203C7B6D7CF95F`; `retail_lua_coverage.json:39523-39531` |
| `lua/scripts/quest/scenario/man/man304.lua` | `C8A0FBC6EEEAFA1B1E148C73139F290E883CA86C2A413900D38CF4A9CD7D8280`; `retail_lua_coverage.json:39508-39516` |
| `lua/scripts/quest/scenario/man/man308.lua` | `3CCDC300DF451AB52E45618CC2444ECDAD0E0FD39062BCC1AF82977929729E43`; `retail_lua_coverage.json:39493-39501` |
| `lua/scripts/quest/scenario/man/man402.lua` | `8794FA034CB6B5E61F1AF9CA387D55AF88296B3231DB748D230EEC142F50F76B`; `retail_lua_coverage.json:39478-39486` |
| `lua/scripts/quest/scenario/man/man406.lua` | `C6415866F54AE206230F1D245B20C65B0146CAE1AB3BE99C37B2D1E314A129AD`; `retail_lua_coverage.json:39463-39471` |

| Prototype and launcher | `SELF / LOADK / CALL` PCs | Literal key | `cutReplay.csv` row (physical line) |
| --- | --- | --- | --- |
| `man200.pE00`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20100` | `11001301` (141) |
| `man200.pE10`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20110` | `11001302` (142) |
| `man200.pE20`, `startSnpcNQCutScene` | `019 / 020 / 027` | `man20120` | `11001303` (143) |
| `man200.pE25`, `startSnpcNQCutScene` | `019 / 020 / 027` | `man20130` | `11001304` (144) |
| `man200.pE050`, `startSnpcNQCutScene` | `016 / 017 / 024` | `man20150` | `11001305` (145) |
| `man200.pE060`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20160` | `11001306` (146) |
| `man206.pE12`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20602` | `11001403` (149) |
| `man206.pE13`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20603` | `11001404` (150) |
| `man206.pE20`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20620` | `11001406` (152) |
| `man206.pE30`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man20630` | `11001407` (153) |
| `man2l0.processEvent010`, `startNQCutScene` | `003 / 004 / 006` | `man2l010` | `11000401` (34) |
| `man2l0.processEvent010`, `startNQCutScene` | `007 / 008 / 010` | `man2l011` | `11000402` (35) |
| `man2l0.processEvent012`, `startNQCutScene` | `003 / 004 / 006` | `man2l012` | `11000403` (36) |
| `man2l0.processEvent013`, `startNQCutScene` | `003 / 004 / 006` | `man2l013` | `11000404` (37) |
| `man2l0.processEvent020` and `processEventTalkMenuManCutPreview`, `startNQCutScene` | `003 / 004 / 008`; `141 / 142 / 144` | `man2l020` | `11000405` (38), `11000406` (39); call-site-to-row assignment unresolved |
| `man2l0.processEvent020`, `startNQCutScene` | `013 / 014 / 016` | `man2l040` | `11000408` (41) |
| `man2l0.processEvent060`, `startNQCutScene` | `003 / 004 / 006` | `man2l060` | `11000409` (42) |
| `man2l0.processEvent070`, `startNQCutScene` | `003 / 004 / 006` | `man2l070` | `11000410` (43) |
| `man2l0.processEvent075`, `startNQCutScene` | `000 / 001 / 003` | `man2l075` | `11000411` (44) |
| `man2l0.processEvent080`, `startNQCutScene` | `003 / 004 / 006` | `man2l080` | `11000412` (45) |
| `man2l0.processEvent081`, `startNQCutScene` | `003 / 004 / 006` | `man2l081` | `11000413` (46) |
| `man2l0.processEvent081`, `startNQCutScene` | `011 / 012 / 014` | `man2l100` | `11000415` (48) |
| `man2l0.processEvent081`, `startNQCutScene` | `015 / 016 / 018` | `man2l110` | `11000416` (49) |
| `man300.pE20`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30020` | `11001503` (157) |
| `man300.pE30`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30030` | `11001504` (158) |
| `man300.pE40`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30040` | `11001505` (159) |
| `man300.pE50`, `startSnpcNQCutScene` | `007 / 008 / 016` | `man30050` | `11001506` (160) |
| `man300.pE60`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30060` | `11001507` (161) |
| `man304.pES`, `startSnpcNQCutScene` | `046 / 047 / 057` | `man30400` | `11001601` (162) |
| `man304.pE10`, `startSnpcNQCutScene` | `016 / 017 / 024` | `man30410` | `11001602` (163) |
| `man304.pE20`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30420` | `11001603` (164) |
| `man304.pE30`, `startSnpcNQCutScene` | `134 / 135 / 142` | `man30430` | `11001604` (165) |
| `man308.pE01`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30800` | `11001701` (166) |
| `man308.pE10`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30810` | `11001702` (167) |
| `man308.pE30`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30830` | `11001703` (168) |
| `man308.pE50`, `startSnpcHQCutScene` | `007 / 008 / 015` | `man40640` | `11001704` (169) |
| `man308.pE50`, `startSnpcNQCutScene` | `016 / 017 / 024` | `man30850` | `11001705` (170) |
| `man308.pE60`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30860` | `11001706` (171) |
| `man308.pE80`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man30880` | `11001707` (172) |
| `man308.pE90`, `startSnpcNQCutScene` | `003 / 004 / 011` | `man30900` | `11001709` (174) |
| `man402.pES`, `startSnpcNQCutScene` | `019 / 020 / 028` | `man40200` | `11001801` (175) |
| `man402.pE10`, `startSnpcNQCutScene` | `007 / 008 / 017` | `man40210` | `11001802` (176) |
| `man402.pE20`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40220` | `11001803` (177) |
| `man402.pE30`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40230` | `11001804` (178) |
| `man406.pES`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40600` | `11001901` (179) |
| `man406.pE10`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40610` | `11001902` (180) |
| `man406.pE15`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40615` | `11001903` (181) |
| `man406.pE30`, `startSnpcNQCutScene` | `007 / 008 / 015` | `man40630` | `11001906` (184) |
| `man406.pE30`, `startSnpcHQCutScene` | `016 / 017 / 024` | `man40635` | `11001907` (185) |
| `man406.pE50`, `startSnpcNQCutScene` | `007 / 008 / 016` | `man40650` | `11001908` (186) |
| `man406.pE60`, `startSnpcNQCutScene` | `006 / 007 / 015` | `man40660` | `11001909` (187) |

The replay table is pinned at `xivl-client-data:manifests/tables.json:1123-1128`
with SHA-256 `2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`.
Every listed key equals the corresponding replay row's scene key exactly.
This establishes a static call/key/table association only, not invocation, row
selection, unlock, playback, or quest ownership. The two `man2l020` bytecode
calls share the same exact key as both listed rows; the available key equality
does not assign either row to a particular call site.

`man200.processSnpcSelect` (`SELF / LOADK / CALL` PCs `080 / 081 / 090`)
and `man200.processSnpcReselect` (`053 / 054 / 063`) each call the literal
key `man20140`, and `man200.pE055` (`089 / 090 / 098`) calls `man20155`.
Neither key has an exact row in the pinned replay table; no replay ID is
assigned. In `man206.pE13`, the decompiled return expression repeats the
scene call across a condition and two branches, but the pinned bytecode has
one `SELF / LOADK / CALL` sequence for `man20603`.

## HQ replay-key checks

The following inventory covers 23 direct `startHQCutScene` calls with literal
string arguments in eight scenario modules. Each module and decoded Lua payload
is pinned in `manifests/retail_lua_coverage.json`:

| Script module | Canonical decoded path | Decoded payload SHA-256 |
| --- | --- | --- |
| `man0g0` | `lua/scripts/quest/scenario/man/man0g0.lua` | `A6770C85F650B05B0993704E7EEB8BB3456BB59A77A113BA9BA0D6B1DE43D0EF` |
| `man0l0` | `lua/scripts/quest/scenario/man/man0l0.lua` | `19A7EF9877A314ED296A918AEA709C57B2CF89B6F46A543C17D51A8E29DF17A1` |
| `man0u0` | `lua/scripts/quest/scenario/man/man0u0.lua` | `850591E834AB2849DC8B53C949D5DB743E829264EA90CED0EA83C6EBBBFB1A4C` |
| `man206` | `lua/scripts/quest/scenario/man/man206.lua` | `0461FC2DEF0F392FA0E952A4557AB1421BA96302D1192F1AE4456AC929C9AF71` |
| `man2g0` | `lua/scripts/quest/scenario/man/man2g0.lua` | `B51E16FD99459EED9271D9F02396B3A2EC307B6D0A0846DD0D5219812C991645` |
| `man2l0` | `lua/scripts/quest/scenario/man/man2l0.lua` | `F78870ADEED3F85B0C71758DA74EF47BB77B2D2AB99546C5F33C8A5D987BD65F` |
| `man2u0` | `lua/scripts/quest/scenario/man/man2u0.lua` | `51AC82341B6FA0A2CCD6DF8F61CF32CC9793904FE44F1F4AED1E92A3F2A88228` |
| `man406` | `lua/scripts/quest/scenario/man/man406.lua` | `C6415866F54AE206230F1D245B20C65B0146CAE1AB3BE99C37B2D1E314A129AD` |

The decoded payload hashes above match the bytecode payloads used to read the
literal calls. The `cutReplay.csv` bytes are pinned by
`xivl-client-data:manifests/tables.json:1123-1128`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`.
`exact` means the source literal equals the CSV scene key byte for byte;
`case-only` means the literal differs only in letter case.

| `cutReplay.csv` row (physical line) | Scene key | Module | Literal call argument and relation |
| --- | --- | --- | --- |
| `11000101` (3) | `man0l000` | `man0l0` | `man0l000` x2 (exact); `MAN0L000` (case-only) |
| `11000103` (5) | `man0l010` | `man0l0` | `man0l010` x2 (exact); `MAN0L010` (case-only) |
| `11000104` (6) | `man0l020` | `man0l0` | `man0l020` x2 (exact) |
| `11000105` (7) | `man0l030` | `man0l0` | `man0l030` x2 (exact) |
| `11000407` (40) | `man2l030` | `man2l0` | `man2l030` (exact); `MAN2L030` (case-only) |
| `11000414` (47) | `man2l090` | `man2l0` | `man2l090` (exact); `MAN2L090` (case-only) |
| `11000501` (50) | `man0g000` | `man0g0` | `MAN0G000` (case-only) |
| `11000802` (84) | `man2g000` | `man2g0` | `man2g000` (exact) |
| `11000811` (93) | `man2g090` | `man2g0` | `MAN2G090` (case-only) |
| `11000901` (96) | `man0u000` | `man0u0` | `MAN0U000` x2 (case-only) |
| `11001203` (130) | `man2u020` | `man2u0` | `MAN2U020` (case-only) |
| `11001211` (138) | `man2u090` | `man2u0` | `MAN2U090` (case-only) |
| `11001405` (151) | `man20610` | `man206` | `MAN20610` (case-only) |
| `11001905` (183) | `man40625` | `man406` | `MAN40625` (case-only) |

For four rows, the module contains both a lower-case exact call and a separate
upper-case call. The exact lower-case occurrence does not change the spelling
of the upper-case call. In particular, `Man0g0` and `Man2u0` have only the
case-different literals listed above. The generic `startHQCutScene` wrapper
forwards its key unchanged to `worldMaster.createCutScene`
(`quest-event-client-contracts.md`), but the client artifacts do not establish
downstream key comparison or lookup. These calls and rows do not establish
reachability, dispatch, quest ownership, replay eligibility, playback, reward,
or historical runtime behavior.
