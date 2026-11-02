# AddressListWidget local interaction contract

This contract records the local behavior recovered from one authenticated retail Lua 5.1 resource. It covers only root bindings, the 20 declared own-method windows, and contained code. Local compositions require the pinned callable, supplied receiver, and normal completion of intervening accesses and calls. Base/native and other-resource helper implementations, callers, native storage, social state, UI rendering, object lifetime, wire/server effects, persistence, and runtime invocation remain outside this contract.

## Identity, authentication, and source proof

- Resource coordinate: `n1635q/966s5rry1rqn1635q.le.lpb` under the installed `client/script` tree.
- Original LPB: 9,211 bytes, SHA-256 `C005B2AB245CE6D4B9873BF29882BA9015E0F43538645D782A0C6EDD0EE37B97`.
- Wrapper: `rle\x0c` xor-0x73, 16-byte header; decoded payload: 9,198 bytes, SHA-256 `5B9674F41D431D550BBF893B399859776D37D1BA5FF603F5E4AF4E0ECD93C3BC`.
- Canonical LF decompile: 25,334 bytes, 1,139 LF lines, SHA-256 `66C9D343C1DC16983410ACB43129B221A8B198F42B8AB1D21B11C5498C2F6DF7`, matching the source pin.
- Decoder/product route: `xivl-client-scripts:tools/retail_script.py`; its SHA-256 was `765327CF3DA90AACF8E36B185CE53AA0615F7705E9F9CCDC3A7243E3B6C0C391` at 3,555 bytes.
- Decompiler: `xivl-client-scripts:tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes, SHA-256 `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
- The pinned decoder and decompiler reproduced the decoded and canonical identities above.

Canonical source coordinate: `xivl-client-scripts:lua/scripts/widget/addresslistwidget.lua`. The path, byte size, SHA-256, and coverage classification are pinned by `xivl-client-scripts:manifests/scripts.json:14859-14862` and `xivl-client-scripts:manifests/retail_lua_coverage.json:25994-25995`; those metadata rows do not establish control flow or request operands.

## Root binding ledger

The root has 68 instructions at decoded offset 32. At PC 2/offset 40, `CALL A=0 B=2 C=1` invokes `require` with one literal `/Widget/WidgetBaseClass` and discards all results. At PC 6/offset 56, `CALL A=0 B=3 C=1` invokes `_defineClass` with exactly two literal strings, `"AddressListWidget"` and `"WidgetBaseClass"`, and discards all results. PCs 7-66 repeat `GETGLOBAL AddressListWidget`, `CLOSURE child=0..19`, and `SETTABLE A=0 B=261..280 C=1` for the 20 method-name constants. These are table-assignment attempts; they do not prove class installation or dispatch.

| root word | value |
|---|---|
| PC 0 / offset 32 | `0x00000005 GETGLOBAL A=0 Bx=0` (`require`) |
| PC 1 / offset 36 | `0x00004041 LOADK A=1 Bx=1` (`/Widget/WidgetBaseClass`) |
| PC 2 / offset 40 | `0x0100401c CALL A=0 B=2 C=1` |
| PC 3 / offset 44 | `0x00008005 GETGLOBAL A=0 Bx=2` (`_defineClass`) |
| PC 4 / offset 48 | `0x0000c041 LOADK A=1 Bx=3` (`AddressListWidget`) |
| PC 5 / offset 52 | `0x00010081 LOADK A=2 Bx=4` (`WidgetBaseClass`) |
| PC 6 / offset 56 | `0x0180401c CALL A=0 B=3 C=1` |
| PCs 7-66 | 20 repeated `GETGLOBAL/CLOSURE/SETTABLE` method binding triplets; the complete words are listed in the root binding ledger below. |

The root uses fresh `GETGLOBAL AddressListWidget`, `CLOSURE`, and `SETTABLE` words for each method. `B=261..280` selects the method-name constants K5..K24.

| child | method | GETGLOBAL pc/offset/word | CLOSURE pc/offset/word | SETTABLE pc/offset/word | key |
|---:|---|---|---|---|---|
| 0 | `init` | pc=7 off=60 word=0x0000c005 | pc=8 off=64 word=0x00000064 | pc=9 off=68 word=0x82804009 | `K5=init` |
| 1 | `setFocus` | pc=10 off=72 word=0x0000c005 | pc=11 off=76 word=0x00004064 | pc=12 off=80 word=0x83004009 | `K6=setFocus` |
| 2 | `processUICommandEvent` | pc=13 off=84 word=0x0000c005 | pc=14 off=88 word=0x00008064 | pc=15 off=92 word=0x83804009 | `K7=processUICommandEvent` |
| 3 | `pageSe` | pc=16 off=96 word=0x0000c005 | pc=17 off=100 word=0x0000c064 | pc=18 off=104 word=0x84004009 | `K8=pageSe` |
| 4 | `makeThisPage` | pc=19 off=108 word=0x0000c005 | pc=20 off=112 word=0x00010064 | pc=21 off=116 word=0x84804009 | `K9=makeThisPage` |
| 5 | `getAddressListMax` | pc=22 off=120 word=0x0000c005 | pc=23 off=124 word=0x00014064 | pc=24 off=128 word=0x85004009 | `K10=getAddressListMax` |
| 6 | `setSignal` | pc=25 off=132 word=0x0000c005 | pc=26 off=136 word=0x00018064 | pc=27 off=140 word=0x85804009 | `K11=setSignal` |
| 7 | `getSignal` | pc=28 off=144 word=0x0000c005 | pc=29 off=148 word=0x0001c064 | pc=30 off=152 word=0x86004009 | `K12=getSignal` |
| 8 | `ignoreFamilyName` | pc=31 off=156 word=0x0000c005 | pc=32 off=160 word=0x00020064 | pc=33 off=164 word=0x86804009 | `K13=ignoreFamilyName` |
| 9 | `setSubWindowOperation` | pc=34 off=168 word=0x0000c005 | pc=35 off=172 word=0x00024064 | pc=36 off=176 word=0x87004009 | `K14=setSubWindowOperation` |
| 10 | `deleteRequest` | pc=37 off=180 word=0x0000c005 | pc=38 off=184 word=0x00028064 | pc=39 off=188 word=0x87804009 | `K15=deleteRequest` |
| 11 | `addRequest` | pc=40 off=192 word=0x0000c005 | pc=41 off=196 word=0x0002c064 | pc=42 off=200 word=0x88004009 | `K16=addRequest` |
| 12 | `getAddressName` | pc=43 off=204 word=0x0000c005 | pc=44 off=208 word=0x00030064 | pc=45 off=212 word=0x88804009 | `K17=getAddressName` |
| 13 | `makeTestList` | pc=46 off=216 word=0x0000c005 | pc=47 off=220 word=0x00034064 | pc=48 off=224 word=0x89004009 | `K18=makeTestList` |
| 14 | `isPartyEnable` | pc=49 off=228 word=0x0000c005 | pc=50 off=232 word=0x00038064 | pc=51 off=236 word=0x89804009 | `K19=isPartyEnable` |
| 15 | `isPartyMember` | pc=52 off=240 word=0x0000c005 | pc=53 off=244 word=0x0003c064 | pc=54 off=248 word=0x8a004009 | `K20=isPartyMember` |
| 16 | `update` | pc=55 off=252 word=0x0000c005 | pc=56 off=256 word=0x00040064 | pc=57 off=260 word=0x8a804009 | `K21=update` |
| 17 | `updateVariation` | pc=58 off=264 word=0x0000c005 | pc=59 off=268 word=0x00044064 | pc=60 off=272 word=0x8b004009 | `K22=updateVariation` |
| 18 | `updateSubWidgetPartyCommand` | pc=61 off=276 word=0x0000c005 | pc=62 off=280 word=0x00048064 | pc=63 off=284 word=0x8b804009 | `K23=updateSubWidgetPartyCommand` |
| 19 | `setBorder` | pc=64 off=288 word=0x0000c005 | pc=65 off=292 word=0x0004c064 | pc=66 off=296 word=0x8c004009 | `K24=setBorder` |

## Full 20-method source/debug/word ledger

`source LF` is the declared canonical decompile window. `unluac debug span` is the prototype line span and is intentionally kept separate. `code offset` and instruction offsets are absolute decoded-chunk offsets. The source-window digest includes the trailing LF.

| child | method | source LF | unluac debug span | arity | stack | code offset | instructions | first word | last word | code-word SHA-256 | source-window SHA-256 |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 0 | `init` | 11-211 | 53-138 | 2 | 19 | 811 | 162 | `0x00400086` | `0x0080001e` | `4CBBF6050A2108D8961F0A49E5B77266C38B63CE29D13CB691DFB26ED28FFC9B` | `A11E9D3A00EB0282C874D3ED895F7BA4A57E3BC292AEAEC2807BF8FF94E94CD0` |
| 1 | `setFocus` | 214-234 | 146-153 | 2 | 5 | 2496 | 16 | `0x00c00057` | `0x0080001e` | `F9070D658F92B4761F3CE4A287AC129E806C3E9E9B01A82866CE956C6D6104D3` | `10CB1BE8671504F9E4DA729BF7F9B0D1CD7DDA77F835F197D9E93D5A62AD2427` |
| 2 | `processUICommandEvent` | 237-486 | 167-279 | 6 | 17 | 2709 | 229 | `0x01c00017` | `0x0080001e` | `DEDED46CCA955B218C549D81BFA595FC21D0CC20036C7E8EEB0368DB82347009` | `C37C89CEA564B8FAED2106AC68BBFB4F469A60CAD47BB1918A15214EE730C55A` |
| 3 | `pageSe` | 489-498 | 286-288 | 1 | 5 | 4495 | 5 | `0x0040004b` | `0x0080001e` | `F1043042FCA10026C87860EA2EF62E2EDF9587D0FE6CCE75CF0791E8B4430AFD` | `8FD642CA3B314B9F8E701DA40526F00592D4A901F2BEE5026F7647D8D3508390` |
| 4 | `makeThisPage` | 501-780 | 296-415 | 1 | 22 | 4610 | 249 | `0x0040004b` | `0x0080001e` | `98CF0262492B518919CA5B0E18C5608218B8BFEC54CE19C1808B76C3584AFBE6` | `AE2479DA67D34F146DE88A612E0D632DB8A8B30FC63FC1BE5663E39F58FC7B5E` |
| 5 | `getAddressListMax` | 783-792 | 423-425 | 1 | 5 | 6183 | 6 | `0x0040004b` | `0x0080001e` | `6E3CE44DC7A139FE71A32BB5F82A05B2D2818BEF2FB4E5E367D66EA1E34A8942` | `62C3E0EB63F035EC094910D723E2AA6A00E5796D3C9646EBAF17061BE62E5D79` |
| 6 | `setSignal` | 795-808 | 433-438 | 2 | 7 | 6301 | 9 | `0x00c00017` | `0x0080001e` | `979775C6FF4181BDE5DB0DB606AB1F50FBA1C1F237A632ED72C232DE3281A6EA` | `E4CD4D668F08EA24BBF7E691A5F1635F8CF1F9D5178453D5F381FD3CB7188A7D` |
| 7 | `getSignal` | 811-820 | 446-448 | 1 | 5 | 6446 | 6 | `0x0040004b` | `0x0080001e` | `6E3CE44DC7A139FE71A32BB5F82A05B2D2818BEF2FB4E5E367D66EA1E34A8942` | `7A193BF4E8726C9553920B2EF09E80C1212341D9DEAA83FBBF1C04D0786DCD45` |
| 8 | `ignoreFamilyName` | 823-832 | 456-458 | 1 | 5 | 6570 | 6 | `0x0040004b` | `0x0080001e` | `6E3CE44DC7A139FE71A32BB5F82A05B2D2818BEF2FB4E5E367D66EA1E34A8942` | `F63848E62388088B54FF15CE6F05D28A7F71C8AF674CFBB6098094CC0165AD41` |
| 9 | `setSubWindowOperation` | 835-853 | 469-477 | 3 | 6 | 6694 | 19 | `0x00c00017` | `0x0080001e` | `23DDBBF382BCBF6E06174A96462E814DBB215DC56965E455F70588E659721CF0` | `D86E2F0EF636BE2AE890DDF06BF461872FD8022826FBD8D1B4EFE25D2362EC87` |
| 10 | `deleteRequest` | 856-882 | 485-494 | 2 | 8 | 6897 | 19 | `0x0040008b` | `0x0080001e` | `278D1BB7BC3AA4A9D1E3CBAE0E8A004AEC7AC0AC708291A885A373689348FD80` | `B8B9E7C2B2659A33255BDBD59BE9C47128E8E6BD73F193F598774EECDF1A0FC4` |
| 11 | `addRequest` | 885-902 | 502-509 | 2 | 7 | 7182 | 14 | `0x00c00057` | `0x0080001e` | `7F60B605EE739A4A41BCEFABCFC021FCF339236F9EBB627D063F9BD4BC5DCB10` | `39B36070AD0519104BBD7D74D231D8E29383F0D8E07ABA33A2404EEBA2FF3152` |
| 12 | `getAddressName` | 905-935 | 519-532 | 2 | 9 | 7372 | 25 | `0x00c00057` | `0x0080001e` | `DF669278873F577101BECE6BEDB539EF3CC0869A47455AFADE0F47A191364578` | `FFC4EF4DFC275ABE0C5D967563077FAFAE5F775C0D4B76C164C6E51A33F287E6` |
| 13 | `makeTestList` | 938-973 | 541-552 | 2 | 15 | 7624 | 29 | `0x00000081` | `0x0080001e` | `A8174366B395573B0906C6E4765F86342309793956B92852E3F3551206D6AE90` | `2E0BF6DEF2E67C3425950B16FEA755C78EF359D59AC8B893EDADB7C49D988302` |
| 14 | `isPartyEnable` | 976-1033 | 560-592 | 1 | 9 | 7917 | 50 | `0x0040004b` | `0x0080001e` | `773A848E44544AD05681164A70E0678D28288F9FC76DCDE1A1C88265AE9607F9` | `9F61AAE401812F6749479ECD23245D38488EC9CBE2BFFFADD256FA24233FBEEF` |
| 15 | `isPartyMember` | 1036-1060 | 601-610 | 2 | 10 | 8361 | 19 | `0x00000085` | `0x0080001e` | `4DB51988867FFA55F19EB8F2E44C6858146CD7179985C66DD37C0F6A91D8785F` | `2728D15788A0FDFE3451208FE7D931ABE90F9ECB6F4A6876ED3D7C2F999B14C2` |
| 16 | `update` | 1063-1073 | 619-621 | 2 | 6 | 8558 | 5 | `0x0040008b` | `0x0080001e` | `4032739D3A065209CD8509BF7C462846BDCD694A3D8E9ACA4DA6F2165BBB82AD` | `3C097A4B13AC15AFABB024E030FC5A9B56C5100058AA214D0B3B7ED4DF35CBB2` |
| 17 | `updateVariation` | 1076-1086 | 629-631 | 1 | 5 | 8670 | 5 | `0x0040004b` | `0x0080001e` | `62F973589BDD561071B8DA74CCD636191B108B8F77E8D11DB62A4C95694E90FB` | `D858CD1B6A9A416C0B2FAFDCE7EF4965BDE3578D7D45E35F83B37412237BF48F` |
| 18 | `updateSubWidgetPartyCommand` | 1089-1103 | 639-644 | 2 | 6 | 8782 | 9 | `0x0040008b` | `0x0080001e` | `BDDF603DD9B104CE3527425A55967429834BEDFEB3BB0BAA651D4241D11B3DA2` | `0E5FE963843680709C5FE0A8CEAC8A6C948EBEB89A6F91B948DA0D5DB9027114` |
| 19 | `setBorder` | 1106-1139 | 653-661 | 2 | 11 | 8937 | 28 | `0x00c00018` | `0x0080001e` | `E7A422E7CE9A30C895E7CE35888E9676A705F6A963B952CD530B6282D4AE94C5` | `6DE83678CD4F3650BF34B4DA959857B3289A0BD22AE78FDA07D9161092D0025C` |

## Local behavior contract

| child | method | source LF | recovered local behavior |
|---:|---|---:|---|
| 0 | `init` | 11-211 | Creates work._temp descriptors for chosenOperation integer8, page integer8, listindex integer16, and iteminpage integer8; initializes chosenOperation=0, listindex=-1, computes iteminpage from ListBox_Address Height divided by 20 (or 24 only for exact desktop size 640x480), installs local cancel/close/confirm and command-condition requests, builds Address_1..Address_iteminpage controls, initializes button/text/modal/drag state, sets page=0 and setSignal(1). No explicit result. |
| 1 | `setFocus` | 214-234 | For non-nil, non-empty A1, requests setLogicalFocus(A1), reads desktopWidget._getKeyboardFocusedWidget(), and only on Lua equality with the actual receiver requests setKeyboardFocusedControl(A1). No explicit result; equality/metamethod behavior remains conditional. |
| 2 | `processUICommandEvent` | 237-486 | Dispatches exact command strings. PropertyChanged captures one getSignal result: 2/22/32 calls makeThisPage with discarded results then tail-forwards setSignal(10); 3/23/33 directly tail-forwards setSignal(10). Otherwise two separate fresh getSignal calls reject exact 21 and then exact 31 with zero results; first31/second0 continues. WidgetClose and Cancel outside A2=ListBox_Address setSignal(11) then tail-forward desktop closeWidgetDirect. List Cancel captures getAddressListMax: exact200 uses that close path; otherwise it tail-forwards setFocus(Button_Add). Previous/Next requires the corresponding getEnable result exacttrue, adjusts page by -1/+1, calls pageSe and tail-forwards makeThisPage. Add tail-forwards setFocus(Button_Add). Operate Button_Add calls setLogicalFocus and opens AddressListNamingWidget with the complete ignoreFamilyName result tail; its first result exacttrue returns one true immediately without setBorder, otherwise execution continues. Operate Button_Previous/Button_Next adjusts page and tail-forwards makeThisPage without an enable test. Remaining Operate returns zero for nil A4; positive A4 writes listindex=page*iteminpage+A4 and tail-forwards makeThisPage if that index exceeds max. Otherwise it focuses Address_A4, then either sets the border and requests the existing subwidget's setMode/show, or opens AddressListSubWidget. A captured child result exacttrue sets the border and returns one true. The remaining normal fallthroughs return zero values. Every described tail forwards the actual callee results, including makeThisPage's false empty-list result; local composition requires the pinned callable and receiver. |
| 3 | `pageSe` | 489-498 | Requests sendControlCommand(self, TextBlock_Total, Page). No explicit result. |
| 4 | `makeThisPage` | 501-780 | Reads max. For exact zero, clears/hides total, shows the message, hides all rows, disables Previous/Next, enables and focuses Add, and returns false. Otherwise computes lastPage=floor((max-1)/iteminpage), then applies ordered if/elseif clamps: if lastPage < page, page=lastPage, elseif page < 0, page=0. Thus max=-1,iteminpage=2,page=0 leaves page=-1; the lower clamp is not applied after the upper branch. It updates paging controls and total text, fills each visible row from getAddressName with icon 385 only for exact online==1 (otherwise 386), hides stale rows and repairs focus, then conditionally chooses a keyboard focus target; a full page with no focus target can make no setFocus request. Add is disabled only for exact max==200. No explicit result on nonzero paths. |
| 5 | `getAddressListMax` | 783-792 | Tail-forwards getControlProperty(self, Address_Maker, Count) with open result width. |
| 6 | `setSignal` | 795-808 | Exact A1==0 returns; otherwise requests Button_Add IntData.Value2=A1. No explicit result. |
| 7 | `getSignal` | 811-820 | Tail-forwards getControlProperty(self, Button_Add, IntData.Value2) with open result width. |
| 8 | `ignoreFamilyName` | 823-832 | Tail-forwards getControlProperty(self, Button_Add, IntData.Value3) with open result width. |
| 9 | `setSubWindowOperation` | 835-853 | Exact A1==0 returns. Exact 21 tail-forwards deleteRequest(work.listindex); exact 31 tail-forwards addRequest(A2); all other values fall through with no result. |
| 10 | `deleteRequest` | 856-882 | Reads max and returns when A1>max. Otherwise reads Address_Maker row A1-1 name, writes Button_Add StringData.Value2, and sets signal 21. Nil/non-numeric A1 reaches the ordinary numeric comparison and is not silently accepted. |
| 11 | `addRequest` | 885-902 | Exact empty string or nil returns. Otherwise writes Button_Add StringData.Value2=A1 and sets signal 31. No explicit result. |
| 12 | `getAddressName` | 905-935 | Uses A1 when non-nil, otherwise work.listindex. If index<1 returns the explicit pair empty string, 0. Otherwise returns the two Address_Maker properties name and online for index-1. |
| 13 | `makeTestList` | 938-973 | Uses count 25 unless A1 is non-nil, then loops inclusively from 0 through count, writing name=name..tostring(i) and online=i%2 for each Address_Maker row, then calls updateListProperty. No explicit result. |
| 14 | `isPartyEnable` | 976-1033 | Captures name/online from getAddressName and returns false immediately for exact online==0, before any isPartyMember request. Otherwise it calls dynamically looked-up isPartyMember(name) and rejects only exact true; composition with the local helper requires its pinned callable and actual frame receiver. It next rejects exact variation 10001/10002. Otherwise countPartyMember<=1 enables; larger parties require isMyPartyLeaderForMyPlayer()!=false and a second count not exactly 8. Returns one literal Boolean on normal completion. |
| 15 | `isPartyMember` | 1036-1060 | Loops i=1..desktopWidget.countPartyMember() and returns true on the first exact equality between getPartyMemberDisplayName(i) and A1; otherwise returns false. Numeric loop inputs are ordinary numeric boundaries. |
| 16 | `update` | 1063-1073 | Calls updateSubWidgetPartyCommand with all results of isPartyEnable on the actual receiver. No explicit result. |
| 17 | `updateVariation` | 1076-1086 | Calls updateSubWidgetPartyCommand with all results of isPartyEnable on the actual receiver. No explicit result. |
| 18 | `updateSubWidgetPartyCommand` | 1089-1103 | Gets AddressListSubWidget. If non-nil, calls its setPartyEnable(A1); otherwise does nothing. No explicit result. |
| 19 | `setBorder` | 1106-1139 | For A1<0, loops 1..work.iteminpage and hides each Address_i:Border_ItemSelected. Otherwise shows exactly Address_A1:Border_ItemSelected. No explicit result; ordinary numeric comparison applies. |

The direct call matrix below retains every CALL and TAILCALL occurrence, including open argument/result widths. `B=0` and `C=0` are open tails; fixed widths are not widened by decompiler presentation. Register operands are frame operands, and RK constants are shown only when statically resolvable. The full raw word, PC, decoded offset, A/B/C, argument width, result width, and raw operands are in the matrix.

## Direct CALL/TAILCALL matrix

Lua 5.1 uses B = argument count + 1 and C = result count + 1; B=0/C=0 are open widths. `raw_args` records RK values where statically resolvable; register values are frame operands, not inferred runtime values.

| child/method | PC | byte offset | word | op | A | B | C | arg width | result width | raw argument operands |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|
| 0/init | 27 | 919 | `0x0100c0dc` | CALL | 3 | 2 | 3 | 1 | 2 | `R[4]` |
| 0/init | 36 | 955 | `0x0200815c` | CALL | 5 | 4 | 2 | 3 | 1 | `R[6], R[7], R[8]` |
| 0/init | 41 | 975 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 0/init | 43 | 983 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 0/init | 46 | 995 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 49 | 1007 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 52 | 1019 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 56 | 1035 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 59 | 1047 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 62 | 1059 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 66 | 1075 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 70 | 1091 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 74 | 1107 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 79 | 1127 | `0x0280419c` | CALL | 6 | 5 | 1 | 4 | 0 | `R[7], R[8], R[9], R[10]` |
| 0/init | 83 | 1143 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 92 | 1179 | `0x010082dc` | CALL | 11 | 2 | 2 | 1 | 1 | `R[12]` |
| 0/init | 99 | 1207 | `0x030042dc` | CALL | 11 | 6 | 1 | 5 | 0 | `R[12], R[13], R[14], R[15], R[16]` |
| 0/init | 103 | 1223 | `0x020042dc` | CALL | 11 | 4 | 1 | 3 | 0 | `R[12], R[13], R[14]` |
| 0/init | 108 | 1243 | `0x028042dc` | CALL | 11 | 5 | 1 | 4 | 0 | `R[12], R[13], R[14], R[15]` |
| 0/init | 115 | 1271 | `0x028042dc` | CALL | 11 | 5 | 1 | 4 | 0 | `R[12], R[13], R[14], R[15]` |
| 0/init | 123 | 1303 | `0x040042dc` | CALL | 11 | 8 | 1 | 7 | 0 | `R[12], R[13], R[14], R[15], R[16], R[17], R[18]` |
| 0/init | 128 | 1323 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 132 | 1339 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 137 | 1359 | `0x0280419c` | CALL | 6 | 5 | 1 | 4 | 0 | `R[7], R[8], R[9], R[10]` |
| 0/init | 141 | 1375 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 147 | 1399 | `0x0100829c` | CALL | 10 | 2 | 2 | 1 | 1 | `R[11]` |
| 0/init | 149 | 1407 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 0/init | 152 | 1419 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 155 | 1431 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 0/init | 160 | 1451 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 1/setFocus | 6 | 2520 | `0x0180409c` | CALL | 2 | 3 | 1 | 2 | 0 | `R[3], R[4]` |
| 1/setFocus | 9 | 2532 | `0x0100809c` | CALL | 2 | 2 | 2 | 1 | 1 | `R[3]` |
| 1/setFocus | 14 | 2552 | `0x0180409c` | CALL | 2 | 3 | 1 | 2 | 0 | `R[3], R[4]` |
| 2/processUICommandEvent | 3 | 2721 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 2/processUICommandEvent | 11 | 2753 | `0x010041dc` | CALL | 7 | 2 | 1 | 1 | 0 | `R[8]` |
| 2/processUICommandEvent | 14 | 2765 | `0x018001dd` | TAILCALL | 7 | 3 | 0 | 2 | open | `R[8], R[9]` |
| 2/processUICommandEvent | 25 | 2809 | `0x018001dd` | TAILCALL | 7 | 3 | 0 | 2 | open | `R[8], R[9]` |
| 2/processUICommandEvent | 28 | 2821 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 2/processUICommandEvent | 34 | 2845 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 2/processUICommandEvent | 42 | 2877 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 2/processUICommandEvent | 46 | 2893 | `0x0180019d` | TAILCALL | 6 | 3 | 0 | 2 | open | `R[7], R[8]` |
| 2/processUICommandEvent | 53 | 2921 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 2/processUICommandEvent | 58 | 2941 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 2/processUICommandEvent | 62 | 2957 | `0x0180019d` | TAILCALL | 6 | 3 | 0 | 2 | open | `R[7], R[8]` |
| 2/processUICommandEvent | 67 | 2977 | `0x0180019d` | TAILCALL | 6 | 3 | 0 | 2 | open | `R[7], R[8]` |
| 2/processUICommandEvent | 72 | 2997 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 2/processUICommandEvent | 76 | 3013 | `0x0180019d` | TAILCALL | 6 | 3 | 0 | 2 | open | `R[7], R[8]` |
| 2/processUICommandEvent | 82 | 3037 | `0x0180819c` | CALL | 6 | 3 | 2 | 2 | 1 | `R[7], R[8]` |
| 2/processUICommandEvent | 91 | 3073 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 2/processUICommandEvent | 93 | 3081 | `0x0100019d` | TAILCALL | 6 | 2 | 0 | 1 | open | `R[7]` |
| 2/processUICommandEvent | 99 | 3105 | `0x0180819c` | CALL | 6 | 3 | 2 | 2 | 1 | `R[7], R[8]` |
| 2/processUICommandEvent | 108 | 3141 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 2/processUICommandEvent | 110 | 3149 | `0x0100019d` | TAILCALL | 6 | 2 | 0 | 1 | open | `R[7]` |
| 2/processUICommandEvent | 116 | 3173 | `0x0180019d` | TAILCALL | 6 | 3 | 0 | 2 | open | `R[7], R[8]` |
| 2/processUICommandEvent | 124 | 3205 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 2/processUICommandEvent | 133 | 3241 | `0x0100035c` | CALL | 13 | 2 | 0 | 1 | open | `R[14]` |
| 2/processUICommandEvent | 134 | 3245 | `0x0000819c` | CALL | 6 | 0 | 2 | open | 1 | `` |
| 2/processUICommandEvent | 146 | 3293 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 2/processUICommandEvent | 148 | 3301 | `0x0100019d` | TAILCALL | 6 | 2 | 0 | 1 | open | `R[7]` |
| 2/processUICommandEvent | 158 | 3341 | `0x0100419c` | CALL | 6 | 2 | 1 | 1 | 0 | `R[7]` |
| 2/processUICommandEvent | 160 | 3349 | `0x0100019d` | TAILCALL | 6 | 2 | 0 | 1 | open | `R[7]` |
| 2/processUICommandEvent | 179 | 3425 | `0x010081dc` | CALL | 7 | 2 | 2 | 1 | 1 | `R[8]` |
| 2/processUICommandEvent | 183 | 3441 | `0x0100019d` | TAILCALL | 6 | 2 | 0 | 1 | open | `R[7]` |
| 2/processUICommandEvent | 189 | 3465 | `0x0100825c` | CALL | 9 | 2 | 2 | 1 | 1 | `R[10]` |
| 2/processUICommandEvent | 191 | 3473 | `0x0180419c` | CALL | 6 | 3 | 1 | 2 | 0 | `R[7], R[8]` |
| 2/processUICommandEvent | 194 | 3485 | `0x0180819c` | CALL | 6 | 3 | 2 | 2 | 1 | `R[7], R[8]` |
| 2/processUICommandEvent | 199 | 3505 | `0x018041dc` | CALL | 7 | 3 | 1 | 2 | 0 | `R[8], R[9]` |
| 2/processUICommandEvent | 205 | 3529 | `0x0100031c` | CALL | 12 | 2 | 0 | 1 | open | `R[13]` |
| 2/processUICommandEvent | 206 | 3533 | `0x000041dc` | CALL | 7 | 0 | 1 | open | 0 | `` |
| 2/processUICommandEvent | 208 | 3541 | `0x010041dc` | CALL | 7 | 2 | 1 | 1 | 0 | `R[8]` |
| 2/processUICommandEvent | 219 | 3585 | `0x010003dc` | CALL | 15 | 2 | 0 | 1 | open | `R[16]` |
| 2/processUICommandEvent | 220 | 3589 | `0x000081dc` | CALL | 7 | 0 | 2 | open | 1 | `` |
| 2/processUICommandEvent | 226 | 3613 | `0x018041dc` | CALL | 7 | 3 | 1 | 2 | 0 | `R[8], R[9]` |
| 3/pageSe | 3 | 4507 | `0x0200405c` | CALL | 1 | 4 | 1 | 3 | 0 | `R[2], R[3], R[4]` |
| 4/makeThisPage | 1 | 4614 | `0x0100805c` | CALL | 1 | 2 | 2 | 1 | 1 | `R[2]` |
| 4/makeThisPage | 10 | 4650 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 13 | 4662 | `0x0180415c` | CALL | 5 | 3 | 1 | 2 | 0 | `R[6], R[7]` |
| 4/makeThisPage | 17 | 4678 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 26 | 4714 | `0x0100829c` | CALL | 10 | 2 | 2 | 1 | 1 | `R[11]` |
| 4/makeThisPage | 31 | 4734 | `0x0200429c` | CALL | 10 | 4 | 1 | 3 | 0 | `R[11], R[12], R[13]` |
| 4/makeThisPage | 36 | 4754 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 40 | 4770 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 44 | 4786 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 47 | 4798 | `0x0180415c` | CALL | 5 | 3 | 1 | 2 | 0 | `R[6], R[7]` |
| 4/makeThisPage | 54 | 4826 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 58 | 4842 | `0x0200815c` | CALL | 5 | 4 | 2 | 3 | 1 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 66 | 4874 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 4/makeThisPage | 81 | 4934 | `0x010081dc` | CALL | 7 | 2 | 2 | 1 | 1 | `R[8]` |
| 4/makeThisPage | 87 | 4958 | `0x010081dc` | CALL | 7 | 2 | 2 | 1 | 1 | `R[8]` |
| 4/makeThisPage | 98 | 5002 | `0x020041dc` | CALL | 7 | 4 | 1 | 3 | 0 | `R[8], R[9], R[10]` |
| 4/makeThisPage | 104 | 5026 | `0x020041dc` | CALL | 7 | 4 | 1 | 3 | 0 | `R[8], R[9], R[10]` |
| 4/makeThisPage | 113 | 5062 | `0x020041dc` | CALL | 7 | 4 | 1 | 3 | 0 | `R[8], R[9], R[10]` |
| 4/makeThisPage | 119 | 5086 | `0x020041dc` | CALL | 7 | 4 | 1 | 3 | 0 | `R[8], R[9], R[10]` |
| 4/makeThisPage | 140 | 5170 | `0x0380425c` | CALL | 9 | 7 | 1 | 6 | 0 | `R[10], R[11], R[12], R[13], R[14], R[15]` |
| 4/makeThisPage | 144 | 5186 | `0x0200425c` | CALL | 9 | 4 | 1 | 3 | 0 | `R[10], R[11], R[12]` |
| 4/makeThisPage | 153 | 5222 | `0x0100839c` | CALL | 14 | 2 | 2 | 1 | 1 | `R[15]` |
| 4/makeThisPage | 162 | 5258 | `0x020043dc` | CALL | 15 | 4 | 1 | 3 | 0 | `R[16], R[17], R[18]` |
| 4/makeThisPage | 165 | 5270 | `0x0180c3dc` | CALL | 15 | 3 | 3 | 2 | 2 | `R[16], R[17]` |
| 4/makeThisPage | 172 | 5298 | `0x0280445c` | CALL | 17 | 5 | 1 | 4 | 0 | `R[18], R[19], R[20], R[21]` |
| 4/makeThisPage | 182 | 5338 | `0x0200449c` | CALL | 18 | 4 | 1 | 3 | 0 | `R[19], R[20], R[21]` |
| 4/makeThisPage | 193 | 5382 | `0x0100849c` | CALL | 18 | 2 | 2 | 1 | 1 | `R[19]` |
| 4/makeThisPage | 195 | 5390 | `0x018043dc` | CALL | 15 | 3 | 1 | 2 | 0 | `R[16], R[17]` |
| 4/makeThisPage | 199 | 5406 | `0x020043dc` | CALL | 15 | 4 | 1 | 3 | 0 | `R[16], R[17], R[18]` |
| 4/makeThisPage | 207 | 5438 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 213 | 5462 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 217 | 5478 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 225 | 5510 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 231 | 5534 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 235 | 5550 | `0x0180425c` | CALL | 9 | 3 | 1 | 2 | 0 | `R[10], R[11]` |
| 4/makeThisPage | 241 | 5574 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 4/makeThisPage | 246 | 5594 | `0x0200415c` | CALL | 5 | 4 | 1 | 3 | 0 | `R[6], R[7], R[8]` |
| 5/getAddressListMax | 3 | 6195 | `0x0200005d` | TAILCALL | 1 | 4 | 0 | 3 | open | `R[2], R[3], R[4]` |
| 6/setSignal | 7 | 6329 | `0x0280409c` | CALL | 2 | 5 | 1 | 4 | 0 | `R[3], R[4], R[5], R[6]` |
| 7/getSignal | 3 | 6458 | `0x0200005d` | TAILCALL | 1 | 4 | 0 | 3 | open | `R[2], R[3], R[4]` |
| 8/ignoreFamilyName | 3 | 6582 | `0x0200005d` | TAILCALL | 1 | 4 | 0 | 3 | open | `R[2], R[3], R[4]` |
| 9/setSubWindowOperation | 9 | 6730 | `0x018000dd` | TAILCALL | 3 | 3 | 0 | 2 | open | `R[4], R[5]` |
| 9/setSubWindowOperation | 16 | 6758 | `0x018000dd` | TAILCALL | 3 | 3 | 0 | 2 | open | `R[4], R[5]` |
| 10/deleteRequest | 1 | 6901 | `0x0100809c` | CALL | 2 | 2 | 2 | 1 | 1 | `R[3]` |
| 10/deleteRequest | 9 | 6933 | `0x0280809c` | CALL | 2 | 5 | 2 | 4 | 1 | `R[3], R[4], R[5], R[6]` |
| 10/deleteRequest | 14 | 6953 | `0x028040dc` | CALL | 3 | 5 | 1 | 4 | 0 | `R[4], R[5], R[6], R[7]` |
| 10/deleteRequest | 17 | 6965 | `0x018040dc` | CALL | 3 | 3 | 1 | 2 | 0 | `R[4], R[5]` |
| 11/addRequest | 9 | 7218 | `0x0280409c` | CALL | 2 | 5 | 1 | 4 | 0 | `R[3], R[4], R[5], R[6]` |
| 11/addRequest | 12 | 7230 | `0x0180409c` | CALL | 2 | 3 | 1 | 2 | 0 | `R[3], R[4]` |
| 12/getAddressName | 15 | 7432 | `0x028080dc` | CALL | 3 | 5 | 2 | 4 | 1 | `R[4], R[5], R[6], R[7]` |
| 12/getAddressName | 20 | 7452 | `0x0280811c` | CALL | 4 | 5 | 2 | 4 | 1 | `R[5], R[6], R[7], R[8]` |
| 13/makeTestList | 15 | 7684 | `0x0100835c` | CALL | 13 | 2 | 2 | 1 | 1 | `R[14]` |
| 13/makeTestList | 17 | 7692 | `0x030041dc` | CALL | 7 | 6 | 1 | 5 | 0 | `R[8], R[9], R[10], R[11], R[12]` |
| 13/makeTestList | 23 | 7716 | `0x030041dc` | CALL | 7 | 6 | 1 | 5 | 0 | `R[8], R[9], R[10], R[11], R[12]` |
| 13/makeTestList | 27 | 7732 | `0x018040dc` | CALL | 3 | 3 | 1 | 2 | 0 | `R[4], R[5]` |
| 14/isPartyEnable | 1 | 7921 | `0x0100c05c` | CALL | 1 | 2 | 3 | 1 | 2 | `R[2]` |
| 14/isPartyEnable | 8 | 7949 | `0x018080dc` | CALL | 3 | 3 | 2 | 2 | 1 | `R[4], R[5]` |
| 14/isPartyEnable | 15 | 7977 | `0x010100dc` | CALL | 3 | 2 | 4 | 1 | 3 | `R[4]` |
| 14/isPartyEnable | 25 | 8017 | `0x0100819c` | CALL | 6 | 2 | 2 | 1 | 1 | `R[7]` |
| 14/isPartyEnable | 33 | 8049 | `0x010081dc` | CALL | 7 | 2 | 2 | 1 | 1 | `R[8]` |
| 14/isPartyEnable | 41 | 8081 | `0x010081dc` | CALL | 7 | 2 | 2 | 1 | 1 | `R[8]` |
| 15/isPartyMember | 2 | 8369 | `0x0100809c` | CALL | 2 | 2 | 2 | 1 | 1 | `R[3]` |
| 15/isPartyMember | 10 | 8401 | `0x018081dc` | CALL | 7 | 3 | 2 | 2 | 1 | `R[8], R[9]` |
| 16/update | 2 | 8566 | `0x0100011c` | CALL | 4 | 2 | 0 | 1 | open | `R[5]` |
| 16/update | 3 | 8570 | `0x0000409c` | CALL | 2 | 0 | 1 | open | 0 | `` |
| 17/updateVariation | 2 | 8678 | `0x010000dc` | CALL | 3 | 2 | 0 | 1 | open | `R[4]` |
| 17/updateVariation | 3 | 8682 | `0x0000405c` | CALL | 1 | 0 | 1 | open | 0 | `` |
| 18/updateSubWidgetPartyCommand | 2 | 8790 | `0x0180809c` | CALL | 2 | 3 | 2 | 2 | 1 | `R[3], R[4]` |
| 18/updateSubWidgetPartyCommand | 7 | 8810 | `0x018040dc` | CALL | 3 | 3 | 1 | 2 | 0 | `R[4], R[5]` |
| 19/setBorder | 11 | 8981 | `0x0100825c` | CALL | 9 | 2 | 2 | 1 | 1 | `R[10]` |
| 19/setBorder | 15 | 8997 | `0x0200419c` | CALL | 6 | 4 | 1 | 3 | 0 | `R[7], R[8], R[9]` |
| 19/setBorder | 22 | 9025 | `0x0100815c` | CALL | 5 | 2 | 2 | 1 | 1 | `R[6]` |
| 19/setBorder | 26 | 9041 | `0x0200409c` | CALL | 2 | 4 | 1 | 3 | 0 | `R[3], R[4], R[5]` |

## Original-word evaluator fixtures

The evaluator parsed and executed the pinned original decoded words, with no source reimplementation. It used actual frame receivers and exact per-table callable identities for own methods, while native/base calls were typed mocks. Equality distinguishes booleans from numbers and uses object identity for tables; zero remains Lua-truthy. Ordinary numeric, metamethod, and coercion boundaries were not silently accepted. No live client, native, server, or social state was used.

The independent expected values and exact call tuples are literal evaluator expectations. The 33 cases are: `init-640x480-one-row`, `setSignal-zero-no-call`, `setSignal-value-writes-property`, `getSignal-typed-value`, `ignoreFamilyName-typed-value`, `setSubWindowOperation-zero`, `getAddressListMax-count`, `deleteRequest-valid`, `addRequest-empty`, `addRequest-value`, `getAddressName-work-index`, `getAddressName-invalid-zero`, `makeTestList-small-original-loop`, `isPartyMember-match`, `isPartyMember-no-match`, `isPartyEnable-party-count-one`, `isPartyEnable-disabled-variation`, `updateSubWidgetPartyCommand-child`, `setBorder-negative-clears-page`, `setFocus-keyboard-identity`, `pageSe-fixed-command`, `makeThisPage-empty-list`, `processUICommandEvent-widget-close`, `processUICommandEvent-cancel-list-max`, `process-propertychanged-signal2-open-tail`, `process-operate-naming-true-no-border`, `makeThisPage-negative-count-ordered-clamp`, `makeThisPage-full-row-no-focus`, `isPartyEnable-exact-party-member`, `update-party-enable-no-child`, `updateVariation-party-enable-no-child`, `isPartyEnable-zero-online-before-member`, `process-operate-new-subwidget-returns-true`. 7 targeted negative controls reject demonstrated Boolean/numeric ordering, fresh callable substitution, string self impersonation, and Boolean/numeric assertion confusion; these controls are corruption guards, not exhaustive model coverage.

The focused run covered all 20 methods, visited 669 of 910 child-prototype instructions (73.5 percent), and had exact call-chronology assertions on 23 of 33 cases. It did not claim branch-complete coverage: unvisited branches include the nonzero/page-fill parts of `makeThisPage`, most command variants in `processUICommandEvent`, alternate party-enable outcomes, and the 640x480/non-640x480 initializer split beyond the selected row. Every positive fixture completed without an unexpected ordinary error; unsupported metamethod/coercion behavior remains explicitly unknown.

## Findings and remaining source gates

- Local list construction is explicit: `makeThisPage` fills row text/icon requests from `getAddressName`, `init` creates the row controls, and `makeTestList` writes deterministic name/online fields. These are local request/state attempts, not proof of native UI rendering or persistent address storage.
- Signal values are local control-property values. 0 is a no-op for `setSignal`; 21/31 are sub-window delete/add gates; 10/11 are command-event transitions. Their external effects remain opaque.
- Add/remove/detail paths are bounded to `addRequest`, `deleteRequest`, `getAddressName`, and the `AddressListNamingWidget` / `AddressListSubWidget` open/request calls in `processUICommandEvent`. Name acceptance, deletion outcome, detail rendering, party/social mutation, server acceptance, and lifetime remain outside the admitted body.
- `isPartyEnable` and `isPartyMember` prove only local exact comparisons and count/leader gates. They do not prove party membership storage, social permissions, or native variation meanings.
- Remaining gates are callers/open tuples, helper/native implementations, initializer census, wire/server outcome, persistence, live runtime observation, and any R4 native social transition/source evidence. No external body was opened.

## Verification and coverage

The authenticated resource yielded 20 own methods, 147 direct call records, and 33 original-word evaluator cases across all 20 methods. Exact call-chronology assertions covered 23 cases; 669 of 910 child-prototype instructions were visited. The 7 negative controls are corruption guards. This finite selection is not branch-complete, and ordinary errors, metamethods, coercions, native behavior, and server outcomes remain outside the source proof.
