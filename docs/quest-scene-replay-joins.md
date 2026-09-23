# Quest scene literal and replay-row joins

This note records direct `startNQCutScene` calls in an audited set of 49
recovered scenario scripts and their exact-key joins to the static
`cutReplay.csv` table. It records call presence and table matches only; it does
not establish dispatch, invocation, playback, quest ownership, or historical
activation. It is not a full-corpus absence audit.

The canonical Lua source paths, byte counts, and SHA-256 values are pinned in
[`scripts.json`](../manifests/scripts.json); installed resource paths and
decoded-payload identities are in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json). The
source line ranges below locate each key assignment and call in that canonical
Lua source. Each join compares the literal scene key with `cutReplay.csv` sheet
column 0, which is CSV field 1 after the row ID. The table has SHA-256
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

Across these 39 modules, the inventory contains 162 literal calls and 159
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
