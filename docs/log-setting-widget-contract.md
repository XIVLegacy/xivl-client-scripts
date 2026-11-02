# LogSettingWidget contract

## Contract

LogSettingWidget is a local settings editor. Its own Lua body initializes
controls, reads native configuration values into controls, sends native
configuration requests for control changes, builds a category list, and
refreshes one of two static log widgets. Native storage, persistence timing,
server effects, application effects, and object lifetime remain opaque.

This contract covers the root binding and all 25 own-method windows.
It does not infer behavior from callers, sibling widgets, native
implementations, wire code, or an initializer census. Root assignments are
binding attempts represented by the bytecode; runtime class publication is not
established here.

## Evidence and pins

The canonical decompiled source is
`lua/scripts/widget/logsettingwidget.lua`, 1,307 LF lines and 28,702 bytes,
SHA-256
`0E390F3D579294AB7ED6F0B732373F70F537F5FABC2AD08560504E7370AA461C`.
The public manifest records this path and identity at
`manifests/scripts.json:15621-15624`; the retail coverage record maps the
resource at `manifests/retail_lua_coverage.json:28049-28050`.

The matching resource is `n1635q/yv3r5qq1w3n1635q.le.lpb`, 12,114 bytes,
SHA-256
`2109638556BFB2013133C80AD86B96F62F28F12C65430D24DC6A0DE5C12FE02B`.
Its `xor-73` wrapper has a 16-byte header and a 12,101-byte decoded payload,
SHA-256
`D9D6DB86D21E8C91302A4B293026905BE25A15A50743505ED51C3A363921EF74`.
The repository decode adapter is `tools/retail_script.py`; its pinned unluac
product is `tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes,
SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
The resource, payload, and source identities agree.

## Root binding ledger

The root prototype has 83 words at byte offset 32, exclusive end 364, max
stack 3, and instruction-word SHA-256
`96B6895FE83676BA499E8862F926BABC3DA6C878756B90C333075ABDDA23448A`.
It requests `require("/Widget/WidgetBaseClass")` at PC 2, byte 40, word
`0x0100401C`, ABC `0,2,1`, and requests
`_defineClass("LogSettingWidget", "WidgetBaseClass")` at PC 6, byte 56,
word `0x0180401C`, ABC `0,3,1`. Both have fixed result width zero (`C=1`).

The 25 closure and assignment rows are:

| Method | Closure PC/byte/word | SETTABLE PC/byte/word | Child | Method constant |
| --- | --- | --- | ---: | ---: |
| `init` | 8 / 64 / `0x00000064` | 9 / 68 / `0x82804009` | 0 | 5 |
| `update` | 11 / 76 / `0x00004064` | 12 / 80 / `0x83004009` | 1 | 6 |
| `processClosing` | 14 / 88 / `0x00008064` | 15 / 92 / `0x83804009` | 2 | 7 |
| `processUICommandOperate` | 17 / 100 / `0x0000C064` | 18 / 104 / `0x84004009` | 3 | 8 |
| `processUICommandSelection` | 20 / 112 / `0x00010064` | 21 / 116 / `0x84804009` | 4 | 9 |
| `processUICommandToggleButton` | 23 / 124 / `0x00014064` | 24 / 128 / `0x85004009` | 5 | 10 |
| `processUICommandSliderChange` | 26 / 136 / `0x00018064` | 27 / 140 / `0x85804009` | 6 | 11 |
| `processUICommandDefault` | 29 / 148 / `0x0001C064` | 30 / 152 / `0x86004009` | 7 | 12 |
| `processUICommandClose` | 32 / 160 / `0x00020064` | 33 / 164 / `0x86804009` | 8 | 13 |
| `processAskResult` | 35 / 172 / `0x00024064` | 36 / 176 / `0x87004009` | 9 | 14 |
| `initLogDisplayDataForUserConfig` | 38 / 184 / `0x00028064` | 39 / 188 / `0x87804009` | 10 | 15 |
| `updateLogDisplayContent` | 41 / 196 / `0x0002C064` | 42 / 200 / `0x88004009` | 11 | 16 |
| `setLogDisplayTitleForUserConfig` | 44 / 208 / `0x00030064` | 45 / 212 / `0x88804009` | 12 | 17 |
| `setLogDisplayContentForUserConfig` | 47 / 220 / `0x00034064` | 48 / 224 / `0x89004009` | 13 | 18 |
| `updateLogWidget` | 50 / 232 / `0x00038064` | 51 / 236 / `0x89804009` | 14 | 19 |
| `setAllFilter` | 53 / 244 / `0x0003C064` | 54 / 248 / `0x8A004009` | 15 | 20 |
| `setButtonStyle` | 56 / 256 / `0x00040064` | 57 / 260 / `0x8A804009` | 16 | 21 |
| `updateControlEnable` | 59 / 268 / `0x00044064` | 60 / 272 / `0x8B004009` | 17 | 22 |
| `setListItem` | 62 / 280 / `0x00048064` | 63 / 284 / `0x8B804009` | 18 | 23 |
| `createFilterList` | 65 / 292 / `0x0004C064` | 66 / 296 / `0x8C004009` | 19 | 24 |
| `addListItem` | 68 / 304 / `0x00050064` | 69 / 308 / `0x8C804009` | 20 | 25 |
| `setTabTitleButton` | 71 / 316 / `0x00054064` | 72 / 320 / `0x8D004009` | 21 | 26 |
| `setSelectedButton` | 74 / 328 / `0x00058064` | 75 / 332 / `0x8D804009` | 22 | 27 |
| `setTabTitleTextBox` | 77 / 340 / `0x0005C064` | 78 / 344 / `0x8E004009` | 23 | 28 |
| `initSliderBar` | 80 / 352 / `0x00060064` | 81 / 356 / `0x8E804009` | 24 | 29 |

## Method source/debug/word ledger

`Source` is the canonical LF window, inclusive. `Source-window SHA-256` hashes
those exact canonical LF bytes. `Debug` is the Lua prototype line-defined
range. `Offset` is the code byte offset. `Words` is instruction count. The
first and last words are the raw word starts of each selected window, while
the instruction-word hash covers every little-endian instruction word.

| Method | Source | Source-window SHA-256 | Debug | Arity | Stack | Offset | Words | First word | Last word | Instruction-word SHA-256 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `init` | 11-239 | `5FA4421718F03193EA0E75BFCBDAA824256C51518FD1D01189771C8970CFFDF4` | 57-165 | 1 | 16 | 1114 | 182 | `0x00400046` | `0x0080001E` | `D2C6B22364E40603C0C39AC95360F3C1003BA32E7E2A94FBDE7C1F4417B1E102` |
| `update` | 242-302 | `B0AD0365275A7000BE1F5AD653D88AB593D074DC17BDB940E2CCB8CE84D6D2B7` | 172-180 | 1 | 7 | 3066 | 51 | `0x0040004B` | `0x0080001E` | `031F93776067C6E363DF66DFB42E8E67515C930C6026E5AF456D4D4A9CF49634` |
| `processClosing` | 305-314 | `A4553D53574B87A1B8E28BD18AF7DD29ECBD2EDD3AA588317475FB49633687C1` | 187-190 | 1 | 4 | 3640 | 5 | `0x00000045` | `0x0080001E` | `FB4634B021819068D928A23E527BBF254E913AB492A70E6CF0CBB500823754E4` |
| `processUICommandOperate` | 317-356 | `16AACF90D0C1EC2870821581E77DBDDC798393F078B747AA11F0DCFC6B74D584` | 202-228 | 5 | 16 | 3745 | 32 | `0x01000140` | `0x0080001E` | `7077CC7346215BE3634B00AF2B0E6032938BC70B8335719F003400ADB0CC2DF1` |
| `processUICommandSelection` | 359-402 | `3E6E12D93B7C967AFBE7A81F6BF170E73F9D7268285B1BC0E979596EBC42614A` | 239-258 | 5 | 10 | 4086 | 34 | `0x01000140` | `0x0080001E` | `E156C141FAB1E6E8B0642DB54DC3E1DC6DA4CD6C115B228053ABDB8A4031E3CD` |
| `processUICommandToggleButton` | 405-495 | `8D57676E7E7789786BF3AA18FF02D7D4B79601648F00C6618F0D93BF3EC1914F` | 270-308 | 6 | 14 | 4488 | 83 | `0x01400017` | `0x0080001E` | `8308714C48CCD4D3865222D19EADFF15BE2978E40441387464E49670AA472065` |
| `processUICommandSliderChange` | 498-535 | `CE1A0A20E9AD5F89A548577BB48CB58A3B1EADAF6B3BAE3199F2EFE6753E8B14` | 320-337 | 6 | 11 | 5363 | 31 | `0x0040018B` | `0x0080001E` | `87CDB0261F331FDC172CCAD1B4E92BF43293043C6EC8A23E3523B204262995DF` |
| `processUICommandDefault` | 538-575 | `674EFFDE1F5551E9C3075FF32B05859C8E986316A45CBBC14BF1F3B24F38D481` | 349-374 | 6 | 12 | 5757 | 29 | `0x01800180` | `0x0080001E` | `918885E66BC884CAF6BDA1C06B4912AE582B2143DC3F39B019FE1878A481E273` |
| `processUICommandClose` | 578-593 | `47E80D4D4D9C11CBCB53950679EDC93C3A9C5AA35DC5A17E4108FB791EDFF149` | 385-392 | 5 | 8 | 6117 | 9 | `0x0040014B` | `0x0080001E` | `503D66C502A72206C2DFE88C4104B50DEC4650FF31438F7B448464D4D9ABCF09` |
| `processAskResult` | 596-605 | `E2808EEFD42311EEDE8E75E2F86BB9828F7FA84EBF9BD62B043C1A78200066AB` | 401-405 | 2 | 4 | 6311 | 5 | `0x00C00017` | `0x0080001E` | `DDB8E56238844725E3393CBDF8379BA932B82F2592584BF917E5DC099DC11F29` |
| `initLogDisplayDataForUserConfig` | 608-781 | `EECD80B0C8550EBF628B5A3464A0C26DB3DC0C88FFFEECC01F817E16B9724F24` | 433-486 | 1 | 14 | 6417 | 143 | `0x00000041` | `0x0080001E` | `B65C2C14B1221660DD9202DBC4A97AC3FCAFF020B22CA12E54BE84A4CAB51BFC` |
| `updateLogDisplayContent` | 784-853 | `FE6C7E37AD466FAE1973C5CDCFCCD470597677A585A36511EABA74D940513718` | 497-537 | 3 | 14 | 7779 | 58 | `0x004000C6` | `0x0080001E` | `A64E44DF0C82BCB3930308B47547A8AB6AEA9435926E06420041A77530A65882` |
| `setLogDisplayTitleForUserConfig` | 856-884 | `769E04A7D5371B682937653F2F504894C0347CAADFF95F721289A8E8C172FDB3` | 546-563 | 1 | 9 | 8411 | 21 | `0x00400046` | `0x0080001E` | `B76618C5BE5F7583C06E9BB643B7F80C6D76D9FBD7141740512ED73C018887E6` |
| `setLogDisplayContentForUserConfig` | 887-937 | `5C94DCBB863214B4F510E265DD79BB9AA31DF4298E7E3228A07830CB505AE50F` | 572-596 | 1 | 13 | 8706 | 42 | `0x00400046` | `0x0080001E` | `40549EB868E1052A85F24F201FB63D2B05AC66F172B3B180DA918E0EEC708C66` |
| `updateLogWidget` | 940-956 | `1B490B5281842CE63D03C6DA6CFB2773B4EEB7F9D425A04909D433BE7BF2DD7F` | 603-613 | 2 | 6 | 9164 | 11 | `0x00000081` | `0x0080001E` | `F1C5F2069EA3710F498FC9DFF162F7BBD829E816A07D408D80DC1E58804F64F8` |
| `setAllFilter` | 959-982 | `A435FA6E4D75981164C1F5550390751716E3989B788EC7B69E9225745E5DD4C0` | 620-628 | 2 | 10 | 9345 | 17 | `0x00000081` | `0x0080001E` | `E6B33C6A497E3D12DD41B52421A68DCB3E6F34DA6B597C0EBB3BDB0B7D254D0A` |
| `setButtonStyle` | 985-998 | `EE7F76DF15F737ABDE8B0DB0C8B9A0676588BC2D7811B0DCA7CEF7CA2AEE34E8` | 636-644 | 3 | 8 | 9595 | 9 | `0x000000C1` | `0x0080001E` | `A1A4165900C62219D685DEC6B26D1377BE2E4DD0DCB9B2A2D2FD7E475F19B0DB` |
| `updateControlEnable` | 1001-1025 | `E5CF8D451E0D6F8370BECC5BA78743E4FE1FF13E30CE5BD37B3C9BC8427DF23A` | 650-657 | 2 | 6 | 9728 | 17 | `0x0040008B` | `0x0080001E` | `91F083FAB60DA9FF1D0C7819C813C09325E53DEA2E6FE3697C8CA44298014A4C` |
| `setListItem` | 1028-1074 | `287000055A04351DE34504BE908D2CB81EC7B140CB7A6AD4877F460D474C0694` | 665-690 | 3 | 12 | 9938 | 39 | `0x000000C1` | `0x0080001E` | `8E89AFB63C503F974AFD33CD50D693BDDA7A85FF643BA8BBE2E3E1A0FFE9DE5C` |
| `createFilterList` | 1077-1163 | `55A7B753878C6CA1930936254CD3665972EE95D2999525C47BEB7DD90F5953CE` | 704-762 | 1 | 8 | 10322 | 65 | `0x00000041` | `0x0080001E` | `65B4F3ACB27365442D689F96FF343A2E5B4C7BC03C3FDE8143E3DD708FA3885C` |
| `addListItem` | 1166-1198 | `FBB547BCA1BDF7A77B9877368E64BB07D451FEF47CCAA638C0E02BA10464A973` | 769-777 | 2 | 10 | 10847 | 26 | `0x00400086` | `0x0080001E` | `EA61E1C18604C4EE3C02913523FE34403A330714CC8B42E25BF5E1BE9D456DDA` |
| `setTabTitleButton` | 1201-1239 | `7A7164DBD44ABB5A4DC2E7723EA5E8EED226CD48F68D63D15811F9D2137B98EB` | 786-800 | 3 | 11 | 11140 | 30 | `0x000000C5` | `0x0080001E` | `89381004C19EE42A2B8D54B75EE546ADA5B399BF2BDB16C597CC50EA69E2AE3A` |
| `setSelectedButton` | 1242-1265 | `A4E1B25A78B3CD5697FCF0BC45F530C36D446CAEEA3A007C5B1760AB7F48BA3C` | 809-815 | 4 | 10 | 11466 | 18 | `0x00000105` | `0x0080001E` | `6D631B09F91009A057DDB4EFD0D04B0A620C5DC31284AE0F6C5A52A5B5606453` |
| `setTabTitleTextBox` | 1268-1285 | `9A42222CBED6D58EA463551251F38458C7C1B023F40521901220DDA6E6CDBBA0` | 824-828 | 2 | 7 | 11709 | 12 | `0x00000085` | `0x0080001E` | `47190CEF76B76E5794B7A9E5991E9590B96E2FCC1C6A2FAAFBFC1D2F401002D9` |
| `initSliderBar` | 1288-1307 | `48D3199EAAA266EB914371B9DDF8179217E3DCEB8DBD51435BB0E0787DA2EA4A` | 835-841 | 2 | 8 | 11929 | 13 | `0x0040008B` | `0x0080001E` | `A561E31F370CCA2BCFE0C4C49A3670217766E35618F0AD5BA9E8CE60475E9B52` |

## Local interaction contract

All 25 methods return no explicit values. Local composition requires the
actual frame receiver and the pinned callable identity; a function's origin
does not establish its receiver. Native names below describe requests or reads,
not storage or application semantics.

### Lifecycle and command routes

- `init` (11-239) declares `_temp` entries `logDisplayCount`,
  `logDisplayWindow`, and `logDisplayTab` as `integer8`; installs confirm,
  control-command, cancel, and close conditions; maps slider control work keys
  6, 7, 17, and 18; disables log auto-hide; initializes work to window 1,
  tab 1, count 0; sets modal true; creates the filter list; registers four
  window/tab buttons; loads display content for 1/1; selects button 1; writes
  labels 1 and 2; initializes four sliders; and calls `update`.
- `update` (242-302) reads work keys 39 and 40 into the two font combo boxes,
  flag 38 into the arriving-SE toggle, work keys 12 and 16 as nonzero
  undisplay toggles, and flag 19 into the weapon-skill toggle.
- `processClosing` (305-314) requests `desktopWidget.setLogAutoHideEnable(true)`.
- `processUICommandOperate` (317-356) opens `CommonAskWidget` for
  `Button_AllClear` with actual frame receiver, `true`, nil, 1347, 2, 1348,
  and 1349. `Button_AllOn` and `Button_AllOff` call `setAllFilter(true)` and
  `setAllFilter(false)`.
- `processUICommandSelection` (359-402) handles the filter list by calling
  `setListItem(A3, nil)`, refreshing the list, and rebuilding selected content.
  Font selections write native work keys 39 and 40.
- `processUICommandToggleButton` (405-495) handles tab enable, flag 38,
  work 12, work 16, and flag 19. Tab enable writes `(window, tab, A5)`,
  updates controls, derives the button index, changes style, and updates the
  selected log widget. It captures the work window/tab before the native enable
  request and reuses those values for later local/native requests. Undisplay
  writes 60 for truthy A5 and 0 otherwise.
  Weapon-skill writes flag 19 and rebuilds selected content.
- `processUICommandSliderChange` (498-535) resolves a slider work key, writes
  A5 to native work, and refreshes transparency only for the two `_2` sliders.
  The base log/text sliders have no extra refresh.
- `processUICommandDefault` (538-575) handles `OperateTab` by deselecting the
  current tab, loading A4/A5, and selecting the new tab. It handles
  `LostFocusTitle` by saving the title.
- `processUICommandClose` (578-593) saves title, saves selected content, and
  requests `desktopWidget.closeWidgetDirect(actual frame receiver)`.
- `processAskResult` (596-605) restores only when A1 is numeric integer 1.
  Boolean true is not equal to numeric 1 in Lua. The own body has no separate
  cancel method or cancel branch: `init` registers a base-widget cancel
  condition, while rollback and cancellation behavior remain outside scope.

### Read, restore, apply, and refresh

- `initLogDisplayDataForUserConfig` (608-781) clears titles and initializes
  native log data for all four window/tab pairs, refreshes tab buttons and
  widgets, resets work keys 6, 7, 17, and 18, requests both transparency
  refreshes, initializes four sliders, requests `resetConfigWork(38)` and
  `resetConfigWork(19)`, restores the flag-38 control, requests
  `resetConfigWork(12)` and `resetConfigWork(16)`, restores those work controls,
  then reads flag 19 and restores its control. It next
  requests `resetConfigWork(39)` and `resetConfigWork(40)` and restores both
  combo boxes, then freshly reads work window/tab at GETTABLE PCs138/140 and
  reloads that current pair. These are exact native requests;
  flag persistence and application remain opaque.
- `updateLogDisplayContent` (784-853) captures active window/tab before native
  reads, stores them, reads native enable state, and for primary 1/1 disables
  the tab-setting control while forcing only the local control value to true;
  it does not request `setConfigLogEnable`. Other pairs enable the tab-setting
  control, then the method updates the tab toggle and title, reads the native
  flag table, maps each list row's `CategoryID`, and refreshes the list.
- `setLogDisplayTitleForUserConfig` (856-884) captures window/tab before
  `getText`, then writes native title, refreshes its tab button, and updates
  the active widget using the captured pair. A reentrant text read changing
  work does not replace those captured operands.
- `setLogDisplayContentForUserConfig` (887-937) captures window/tab before row
  reads, collects category IDs whose `Checked` property is exactly true, writes
  that ordered list to native log data for the captured pair, and calls
  `updateLogWidget(1)` then `updateLogWidget(2)`. Those helpers select native
  static-widget indices 2 then 3, respectively.
- `updateLogWidget` (940-956) selects static widget 2 only for numeric 1;
  every other A1, including boolean true, selects static widget 3, then calls
  `updateLogCategoryDisplay` on the actual static-widget result receiver.

### Filter, list, tab, and slider helpers

- `setAllFilter` (959-982) composes the pinned `setListItem` helper for every
  row, then refreshes the list and rebuilds selected content. A nil A1 is not a
  direct nil write: each selected row enters `setListItem`'s read-and-invert
  branch. Likewise, a missing key in `updateLogDisplayContent`'s flag table
  passes nil to that same helper and follows the inversion branch.
- `setButtonStyle` (985-998) chooses `BTN_basis` only for exact false; nil,
  zero, and true retain `BTN_basis_cmdRunning`.
- `updateControlEnable` (1001-1025) applies A1 to the title box, all-on,
  all-off, and filter list controls.
- `setListItem` (1028-1074) captures its row index before native row writes and
  treats omitted or nil A2 as a read-and-invert request, inverting only exact
  true. It writes `Checked`, uses message 2226 and `TBL_parameterMinus` only
  for exact false, otherwise uses 2225 and `TBL_parameterPlus`, and writes
  both status fields.
- `createFilterList` (1077-1163) adds IDs 1..12, 27, 25, 22, 23, 24, 26,
  80..109, 66, 70, 71, 72, 73, 68, 69, 32, and 33, then refreshes the list.
  `addListItem` (1166-1198) captures count at GETTABLE PC1 and uses that row
  for all three native writes, including after callbacks. It writes message
  2254, category ID and help expression `(74801 + A1) - 1`, then freshly
  accesses work at PC22 and assigns the captured count plus one. A callback
  changing count 0 to 99 therefore leaves the later row operands 0 and final
  assigned count 1.
- `setTabTitleButton` (1201-1239) derives `Button_<index+1>` from native log
  index, reads its title and enable state, writes macro content, and delegates
  style selection.
- `setSelectedButton` (1242-1265) derives the same button name and writes its
  selected-effect visibility to A3.
- `setTabTitleTextBox` (1268-1285) reads the active native title and writes it
  to `TextBox_TabName`; declared A1 is not consumed.
- `initSliderBar` (1288-1307) resolves a slider work key, reads native work,
  and writes the value to the slider.

## Complete direct CALL/TAILCALL ledger

The following 189 rows are the complete root-inclusive direct-call
enumeration: 187 own-method rows plus 2 root rows. Raw A/B/C, word, byte
offset, target, argument operands, and result width are inline. Fixed B means
B-1 arguments and fixed C means C-1 results. B=0 and C=0 are open tails and
remain distinct from explicit nil, zero, or no arguments. No result-width
normalization was applied.

Member expressions marked `captured(...)` denote evaluated values retained
in registers, not fresh reads at CALL. Capture notes identify method-local
read points; not every row uses every noted value. The final restore call
has separate fresh work reads after earlier callbacks, as noted in its row.

| Method | PC | Byte | Word | Op | ABC | Target | Raw arguments | Results | Open-argument provenance | Capture/fresh-read qualification |
| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| `root` | 2 | 40 | `0x0100401C` | CALL | 0,2,1 | `require` | ['/Widget/WidgetBaseClass'] (1) | 0 | - | - |
| `root` | 6 | 56 | `0x0180401C` | CALL | 0,3,1 | `_defineClass` | ['LogSettingWidget', 'WidgetBaseClass'] (2) | 0 | - | - |
| `init` | 18 | 1186 | `0x0180405C` | CALL | 1,3,1 | `setConfirmCondition` | [arg0, 'Button_AllClear'] (2) | 0 | - | - |
| `init` | 21 | 1198 | `0x0180405C` | CALL | 1,3,1 | `setConfirmCondition` | [arg0, 'Button_AllOn'] (2) | 0 | - | - |
| `init` | 24 | 1210 | `0x0180405C` | CALL | 1,3,1 | `setConfirmCondition` | [arg0, 'Button_AllOff'] (2) | 0 | - | - |
| `init` | 28 | 1226 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'TextBox_TabName', 'UILuaCommands.LostFocusTitle'] (3) | 0 | - | - |
| `init` | 32 | 1242 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ToggleButton_TabSetting', 'UILuaCommands.ToggleButton'] (3) | 0 | - | - |
| `init` | 36 | 1258 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ToggleButton_TellArrivingSE', 'UILuaCommands.ToggleButton'] (3) | 0 | - | - |
| `init` | 40 | 1274 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ToggleButton_Undisplay', 'UILuaCommands.ToggleButton'] (3) | 0 | - | - |
| `init` | 44 | 1290 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ToggleButton_Undisplay_2', 'UILuaCommands.ToggleButton'] (3) | 0 | - | - |
| `init` | 48 | 1306 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ToggleButton_WeaponSkillLog', 'UILuaCommands.ToggleButton'] (3) | 0 | - | - |
| `init` | 52 | 1322 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'Slider_LogOptical', 'UILuaCommands.SliderValueChanged'] (3) | 0 | - | - |
| `init` | 56 | 1338 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'Slider_LogOptical_2', 'UILuaCommands.SliderValueChanged'] (3) | 0 | - | - |
| `init` | 60 | 1354 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'Slider_TextOptical', 'UILuaCommands.SliderValueChanged'] (3) | 0 | - | - |
| `init` | 64 | 1370 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'Slider_TextOptical_2', 'UILuaCommands.SliderValueChanged'] (3) | 0 | - | - |
| `init` | 69 | 1390 | `0x0280405C` | CALL | 1,5,1 | `setControlUserWorkInt` | [arg0, 1, 'Slider_LogOptical', 6] (4) | 0 | - | - |
| `init` | 74 | 1410 | `0x0280405C` | CALL | 1,5,1 | `setControlUserWorkInt` | [arg0, 1, 'Slider_LogOptical_2', 7] (4) | 0 | - | - |
| `init` | 79 | 1430 | `0x0280405C` | CALL | 1,5,1 | `setControlUserWorkInt` | [arg0, 1, 'Slider_TextOptical', 17] (4) | 0 | - | - |
| `init` | 84 | 1450 | `0x0280405C` | CALL | 1,5,1 | `setControlUserWorkInt` | [arg0, 1, 'Slider_TextOptical_2', 18] (4) | 0 | - | - |
| `init` | 86 | 1458 | `0x0100405C` | CALL | 1,2,1 | `setCancelCondition` | [arg0] (1) | 0 | - | - |
| `init` | 88 | 1466 | `0x0100405C` | CALL | 1,2,1 | `setCloseCondition` | [arg0] (1) | 0 | - | - |
| `init` | 92 | 1482 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ListBox_LogSettingItems', 'UILuaCommands.Selection'] (3) | 0 | - | - |
| `init` | 96 | 1498 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ComboBox_Font_Win1', 'UILuaCommands.Selection'] (3) | 0 | - | - |
| `init` | 100 | 1514 | `0x0200405C` | CALL | 1,4,1 | `setControlCommandCondition` | [arg0, 'ComboBox_Font_Win2', 'UILuaCommands.Selection'] (3) | 0 | - | - |
| `init` | 104 | 1530 | `0x0180405C` | CALL | 1,3,1 | `setLogAutoHideEnable` | [global:desktopWidget, false] (2) | 0 | - | - |
| `init` | 113 | 1566 | `0x0180405C` | CALL | 1,3,1 | `setModal` | [arg0, true] (2) | 0 | - | - |
| `init` | 115 | 1574 | `0x0100405C` | CALL | 1,2,1 | `createFilterList` | [arg0] (1) | 0 | - | - |
| `init` | 128 | 1626 | `0x0200825C` | CALL | 9,4,2 | `getConfigLogIndex` | [global:desktopWidget, control-flow-or-computed-value, control-flow-or-computed-value] (3) | 1 | - | - |
| `init` | 133 | 1646 | `0x010082DC` | CALL | 11,2,2 | `tostring` | [control-flow-or-computed-value] (1) | 1 | - | - |
| `init` | 139 | 1670 | `0x028042DC` | CALL | 11,5,1 | `setCommandParameter` | [arg0, control-flow-or-computed-value, control-flow-or-computed-value, control-flow-or-computed-value] (4) | 0 | - | - |
| `init` | 143 | 1686 | `0x020042DC` | CALL | 11,4,1 | `setControlCommandCondition` | [arg0, control-flow-or-computed-value, 'UILuaCommands.OperateTab'] (3) | 0 | - | - |
| `init` | 147 | 1702 | `0x020042DC` | CALL | 11,4,1 | `setTabTitleButton` | [arg0, control-flow-or-computed-value, control-flow-or-computed-value] (3) | 0 | - | - |
| `init` | 153 | 1726 | `0x0200405C` | CALL | 1,4,1 | `updateLogDisplayContent` | [arg0, 1, 1] (3) | 0 | - | - |
| `init` | 158 | 1746 | `0x0280405C` | CALL | 1,5,1 | `setSelectedButton` | [arg0, 1, 1, true] (4) | 0 | - | - |
| `init` | 162 | 1762 | `0x0200405C` | CALL | 1,4,1 | `setText` | [arg0, 'TextBlock_1', '1'] (3) | 0 | - | - |
| `init` | 166 | 1778 | `0x0200405C` | CALL | 1,4,1 | `setText` | [arg0, 'TextBlock_2', '2'] (3) | 0 | - | - |
| `init` | 169 | 1790 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_LogOptical'] (2) | 0 | - | - |
| `init` | 172 | 1802 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_LogOptical_2'] (2) | 0 | - | - |
| `init` | 175 | 1814 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_TextOptical'] (2) | 0 | - | - |
| `init` | 178 | 1826 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_TextOptical_2'] (2) | 0 | - | - |
| `init` | 180 | 1834 | `0x0100405C` | CALL | 1,2,1 | `update` | [arg0] (1) | 0 | - | - |
| `update` | 5 | 3086 | `0x0180011C` | CALL | 4,3,0 | `getConfigWork` | [global:desktopWidget, 39] (2) | open | - | - |
| `update` | 6 | 3090 | `0x0000405C` | CALL | 1,0,1 | `setSelectedIndex` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ComboBox_Font_Win1']; tail from update PC 5 `getConfigWork` (C=0/open result tail) | - |
| `update` | 12 | 3114 | `0x0180011C` | CALL | 4,3,0 | `getConfigWork` | [global:desktopWidget, 40] (2) | open | - | - |
| `update` | 13 | 3118 | `0x0000405C` | CALL | 1,0,1 | `setSelectedIndex` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ComboBox_Font_Win2']; tail from update PC 12 `getConfigWork` (C=0/open result tail) | - |
| `update` | 19 | 3142 | `0x0180011C` | CALL | 4,3,0 | `getConfigFlag` | [global:desktopWidget, 38] (2) | open | - | - |
| `update` | 20 | 3146 | `0x0000405C` | CALL | 1,0,1 | `setChecked` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ToggleButton_TellArrivingSE']; tail from update PC 19 `getConfigFlag` (C=0/open result tail) | - |
| `update` | 26 | 3170 | `0x0180811C` | CALL | 4,3,2 | `getConfigWork` | [global:desktopWidget, 12] (2) | 1 | - | - |
| `update` | 31 | 3190 | `0x0200405C` | CALL | 1,4,1 | `setChecked` | [arg0, 'ToggleButton_Undisplay', control-flow-or-computed-value] (3) | 0 | - | - |
| `update` | 37 | 3214 | `0x0180811C` | CALL | 4,3,2 | `getConfigWork` | [global:desktopWidget, 16] (2) | 1 | - | - |
| `update` | 42 | 3234 | `0x0200405C` | CALL | 1,4,1 | `setChecked` | [arg0, 'ToggleButton_Undisplay_2', control-flow-or-computed-value] (3) | 0 | - | - |
| `update` | 48 | 3258 | `0x0180011C` | CALL | 4,3,0 | `getConfigFlag` | [global:desktopWidget, 19] (2) | open | - | - |
| `update` | 49 | 3262 | `0x0000405C` | CALL | 1,0,1 | `setChecked` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ToggleButton_WeaponSkillLog']; tail from update PC 48 `getConfigFlag` (C=0/open result tail) | - |
| `processClosing` | 3 | 3652 | `0x0180405C` | CALL | 1,3,1 | `setLogAutoHideEnable` | [global:desktopWidget, true] (2) | 0 | - | - |
| `processUICommandOperate` | 13 | 3797 | `0x0500419C` | CALL | 6,10,1 | `openChildWidget` | [global:desktopWidget, 'CommonAskWidget', arg0, true, nil, 1347, 2, 1348, 1349] (9) | 0 | - | - |
| `processUICommandOperate` | 20 | 3825 | `0x0180419C` | CALL | 6,3,1 | `setAllFilter` | [arg0, true] (2) | 0 | - | - |
| `processUICommandOperate` | 27 | 3853 | `0x0180419C` | CALL | 6,3,1 | `setAllFilter` | [arg0, false] (2) | 0 | - | - |
| `processUICommandSelection` | 6 | 4110 | `0x0200419C` | CALL | 6,4,1 | `setListItem` | [arg0, arg3, nil] (3) | 0 | - | - |
| `processUICommandSelection` | 9 | 4122 | `0x0180419C` | CALL | 6,3,1 | `updateListProperty` | [arg0, 'ListBox'] (2) | 0 | - | - |
| `processUICommandSelection` | 11 | 4130 | `0x0100419C` | CALL | 6,2,1 | `setLogDisplayContentForUserConfig` | [arg0] (1) | 0 | - | - |
| `processUICommandSelection` | 20 | 4166 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 39, arg3] (3) | 0 | - | - |
| `processUICommandSelection` | 29 | 4202 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 40, arg3] (3) | 0 | - | - |
| `processUICommandToggleButton` | 11 | 4532 | `0x0280421C` | CALL | 8,5,1 | `setConfigLogEnable` | [global:desktopWidget, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab), arg5] (4) | 0 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 14 | 4544 | `0x0180421C` | CALL | 8,3,1 | `updateControlEnable` | [arg0, arg5] (2) | 0 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 19 | 4564 | `0x0200821C` | CALL | 8,4,2 | `getConfigLogIndex` | [global:desktopWidget, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab)] (3) | 1 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 25 | 4588 | `0x0100831C` | CALL | 12,2,2 | `tostring` | [control-flow-or-computed-value] (1) | 1 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 28 | 4600 | `0x0200425C` | CALL | 9,4,1 | `setButtonStyle` | [arg0, control-flow-or-computed-value, arg5] (3) | 0 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 31 | 4612 | `0x0180425C` | CALL | 9,3,1 | `updateLogWidget` | [arg0, captured(arg0.work.logDisplayWindow)] (2) | 0 | - | tab-setting branch only: window/tab captured at GETTABLE PCs3/5 before its callbacks |
| `processUICommandToggleButton` | 39 | 4644 | `0x0200419C` | CALL | 6,4,1 | `setConfigFlag` | [global:desktopWidget, 38, arg5] (3) | 0 | - | - |
| `processUICommandToggleButton` | 49 | 4684 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 12, 60] (3) | 0 | - | - |
| `processUICommandToggleButton` | 55 | 4708 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 12, 0] (3) | 0 | - | - |
| `processUICommandToggleButton` | 65 | 4748 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 16, 60] (3) | 0 | - | - |
| `processUICommandToggleButton` | 71 | 4772 | `0x0200419C` | CALL | 6,4,1 | `setConfigWork` | [global:desktopWidget, 16, 0] (3) | 0 | - | - |
| `processUICommandToggleButton` | 79 | 4804 | `0x0200419C` | CALL | 6,4,1 | `setConfigFlag` | [global:desktopWidget, 19, arg5] (3) | 0 | - | - |
| `processUICommandToggleButton` | 81 | 4812 | `0x0100419C` | CALL | 6,2,1 | `setLogDisplayContentForUserConfig` | [arg0] (1) | 0 | - | - |
| `processUICommandSliderChange` | 3 | 5375 | `0x0200819C` | CALL | 6,4,2 | `getControlUserWorkInt` | [arg0, 1, arg2] (3) | 1 | - | - |
| `processUICommandSliderChange` | 8 | 5395 | `0x020041DC` | CALL | 7,4,1 | `setConfigWork` | [global:desktopWidget, result(pc=3,r=0), arg5] (3) | 0 | - | - |
| `processUICommandSliderChange` | 17 | 5431 | `0x0100421C` | CALL | 8,2,1 | `updateLogTransparency` | [global:desktopWidget] (1) | 0 | - | - |
| `processUICommandSliderChange` | 27 | 5471 | `0x0100421C` | CALL | 8,2,1 | `updateLogTextTransparency` | [global:desktopWidget] (1) | 0 | - | - |
| `processUICommandDefault` | 9 | 5793 | `0x028041DC` | CALL | 7,5,1 | `setSelectedButton` | [arg0, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab), false] (4) | 0 | - | - |
| `processUICommandDefault` | 13 | 5809 | `0x020041DC` | CALL | 7,4,1 | `updateLogDisplayContent` | [arg0, arg4, arg5] (3) | 0 | - | - |
| `processUICommandDefault` | 18 | 5829 | `0x028041DC` | CALL | 7,5,1 | `setSelectedButton` | [arg0, arg4, arg5, true] (4) | 0 | - | - |
| `processUICommandDefault` | 24 | 5853 | `0x010041DC` | CALL | 7,2,1 | `setLogDisplayTitleForUserConfig` | [arg0] (1) | 0 | - | - |
| `processUICommandClose` | 1 | 6121 | `0x0100415C` | CALL | 5,2,1 | `setLogDisplayTitleForUserConfig` | [arg0] (1) | 0 | - | - |
| `processUICommandClose` | 3 | 6129 | `0x0100415C` | CALL | 5,2,1 | `setLogDisplayContentForUserConfig` | [arg0] (1) | 0 | - | - |
| `processUICommandClose` | 7 | 6145 | `0x0180415C` | CALL | 5,3,1 | `closeWidgetDirect` | [global:desktopWidget, arg0] (2) | 0 | - | - |
| `processAskResult` | 3 | 6323 | `0x0100409C` | CALL | 2,2,1 | `initLogDisplayDataForUserConfig` | [arg0] (1) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 13 | 6469 | `0x0280425C` | CALL | 9,5,1 | `setConfigLogTitle` | [global:desktopWidget, control-flow-or-computed-value, control-flow-or-computed-value, nil] (4) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 18 | 6489 | `0x0200425C` | CALL | 9,4,1 | `initConfigLogData` | [global:desktopWidget, control-flow-or-computed-value, control-flow-or-computed-value] (3) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 22 | 6505 | `0x0200425C` | CALL | 9,4,1 | `setTabTitleButton` | [arg0, control-flow-or-computed-value, control-flow-or-computed-value] (3) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 26 | 6521 | `0x0180415C` | CALL | 5,3,1 | `updateLogWidget` | [arg0, control-flow-or-computed-value] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 31 | 6541 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 6] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 35 | 6557 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 7] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 39 | 6573 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 17] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 43 | 6589 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 18] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 46 | 6601 | `0x0100405C` | CALL | 1,2,1 | `updateLogTransparency` | [global:desktopWidget] (1) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 49 | 6613 | `0x0100405C` | CALL | 1,2,1 | `updateLogTextTransparency` | [global:desktopWidget] (1) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 52 | 6625 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_LogOptical'] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 55 | 6637 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_LogOptical_2'] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 58 | 6649 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_TextOptical'] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 61 | 6661 | `0x0180405C` | CALL | 1,3,1 | `initSliderBar` | [arg0, 'Slider_TextOptical_2'] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 65 | 6677 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 38] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 69 | 6693 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 19] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 75 | 6717 | `0x0180011C` | CALL | 4,3,0 | `getConfigFlag` | [global:desktopWidget, 38] (2) | open | - | - |
| `initLogDisplayDataForUserConfig` | 76 | 6721 | `0x0000405C` | CALL | 1,0,1 | `setChecked` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ToggleButton_TellArrivingSE']; tail from initLogDisplayDataForUserConfig PC 75 `getConfigFlag` (C=0/open result tail) | - |
| `initLogDisplayDataForUserConfig` | 80 | 6737 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 12] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 84 | 6753 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 16] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 90 | 6777 | `0x0180811C` | CALL | 4,3,2 | `getConfigWork` | [global:desktopWidget, 12] (2) | 1 | - | - |
| `initLogDisplayDataForUserConfig` | 95 | 6797 | `0x0200405C` | CALL | 1,4,1 | `setChecked` | [arg0, 'ToggleButton_Undisplay', control-flow-or-computed-value] (3) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 101 | 6821 | `0x0180811C` | CALL | 4,3,2 | `getConfigWork` | [global:desktopWidget, 16] (2) | 1 | - | - |
| `initLogDisplayDataForUserConfig` | 106 | 6841 | `0x0200405C` | CALL | 1,4,1 | `setChecked` | [arg0, 'ToggleButton_Undisplay_2', control-flow-or-computed-value] (3) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 112 | 6865 | `0x0180011C` | CALL | 4,3,0 | `getConfigFlag` | [global:desktopWidget, 19] (2) | open | - | - |
| `initLogDisplayDataForUserConfig` | 113 | 6869 | `0x0000405C` | CALL | 1,0,1 | `setChecked` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ToggleButton_WeaponSkillLog']; tail from initLogDisplayDataForUserConfig PC 112 `getConfigFlag` (C=0/open result tail) | - |
| `initLogDisplayDataForUserConfig` | 117 | 6885 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 39] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 121 | 6901 | `0x0180405C` | CALL | 1,3,1 | `resetConfigWork` | [global:desktopWidget, 40] (2) | 0 | - | - |
| `initLogDisplayDataForUserConfig` | 127 | 6925 | `0x0180011C` | CALL | 4,3,0 | `getConfigWork` | [global:desktopWidget, 39] (2) | open | - | - |
| `initLogDisplayDataForUserConfig` | 128 | 6929 | `0x0000405C` | CALL | 1,0,1 | `setSelectedIndex` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ComboBox_Font_Win1']; tail from initLogDisplayDataForUserConfig PC 127 `getConfigWork` (C=0/open result tail) | - |
| `initLogDisplayDataForUserConfig` | 134 | 6953 | `0x0180011C` | CALL | 4,3,0 | `getConfigWork` | [global:desktopWidget, 40] (2) | open | - | - |
| `initLogDisplayDataForUserConfig` | 135 | 6957 | `0x0000405C` | CALL | 1,0,1 | `setSelectedIndex` | [] (open) | 0 | fixed prefix ['actual frame receiver', 'ComboBox_Font_Win2']; tail from initLogDisplayDataForUserConfig PC 134 `getConfigWork` (C=0/open result tail) | - |
| `initLogDisplayDataForUserConfig` | 141 | 6981 | `0x0200405C` | CALL | 1,4,1 | `updateLogDisplayContent` | [arg0, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab)] (3) | 0 | - | fresh work window/tab reads at GETTABLE PCs138/140 after earlier restore callbacks |
| `updateLogDisplayContent` | 8 | 7811 | `0x020080DC` | CALL | 3,4,2 | `getConfigLogEnable` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `updateLogDisplayContent` | 16 | 7843 | `0x0200411C` | CALL | 4,4,1 | `setEnable` | [arg0, 'ToggleButton_TabSetting', false] (3) | 0 | - | - |
| `updateLogDisplayContent` | 22 | 7867 | `0x0200411C` | CALL | 4,4,1 | `setEnable` | [arg0, 'ToggleButton_TabSetting', true] (3) | 0 | - | - |
| `updateLogDisplayContent` | 26 | 7883 | `0x0200411C` | CALL | 4,4,1 | `setChecked` | [arg0, 'ToggleButton_TabSetting', control-flow-or-computed-value] (3) | 0 | - | - |
| `updateLogDisplayContent` | 29 | 7895 | `0x0180411C` | CALL | 4,3,1 | `updateControlEnable` | [arg0, control-flow-or-computed-value] (2) | 0 | - | - |
| `updateLogDisplayContent` | 32 | 7907 | `0x0180411C` | CALL | 4,3,1 | `setTabTitleTextBox` | [arg0, control-flow-or-computed-value] (2) | 0 | - | - |
| `updateLogDisplayContent` | 37 | 7927 | `0x0200811C` | CALL | 4,4,2 | `getConfigLogFlagTable` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `updateLogDisplayContent` | 48 | 7971 | `0x0280825C` | CALL | 9,5,2 | `getListProperty` | [arg0, 'ListBox', control-flow-or-computed-value, 'CategoryID'] (4) | 1 | - | - |
| `updateLogDisplayContent` | 52 | 7987 | `0x0200429C` | CALL | 10,4,1 | `setListItem` | [arg0, control-flow-or-computed-value, control-flow-or-computed-value] (3) | 0 | - | - |
| `updateLogDisplayContent` | 56 | 8003 | `0x0180415C` | CALL | 5,3,1 | `updateListProperty` | [arg0, 'ListBox'] (2) | 0 | - | - |
| `setLogDisplayTitleForUserConfig` | 6 | 8435 | `0x018080DC` | CALL | 3,3,2 | `getText` | [arg0, 'TextBox_TabName'] (2) | 1 | - | window/tab captured at GETTABLE PCs1/3 before getText; later calls use that pair |
| `setLogDisplayTitleForUserConfig` | 12 | 8459 | `0x0280411C` | CALL | 4,5,1 | `setConfigLogTitle` | [global:desktopWidget, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab), result(pc=6,r=0)] (4) | 0 | - | window/tab captured at GETTABLE PCs1/3 before getText; later calls use that pair |
| `setLogDisplayTitleForUserConfig` | 16 | 8475 | `0x0200411C` | CALL | 4,4,1 | `setTabTitleButton` | [arg0, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab)] (3) | 0 | - | window/tab captured at GETTABLE PCs1/3 before getText; later calls use that pair |
| `setLogDisplayTitleForUserConfig` | 19 | 8487 | `0x0180411C` | CALL | 4,3,1 | `updateLogWidget` | [arg0, captured(arg0.work.logDisplayWindow)] (2) | 0 | - | window/tab captured at GETTABLE PCs1/3 before getText; later calls use that pair |
| `setLogDisplayContentForUserConfig` | 15 | 8766 | `0x0280821C` | CALL | 8,5,2 | `getListProperty` | [arg0, 'ListBox', control-flow-or-computed-value, 'Checked'] (4) | 1 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `setLogDisplayContentForUserConfig` | 22 | 8794 | `0x0280821C` | CALL | 8,5,2 | `getListProperty` | [arg0, 'ListBox', control-flow-or-computed-value, 'CategoryID'] (4) | 1 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `setLogDisplayContentForUserConfig` | 27 | 8814 | `0x0180425C` | CALL | 9,3,1 | `insert` | [control-flow-or-computed-value, result(pc=22,r=0)] (2) | 0 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `setLogDisplayContentForUserConfig` | 34 | 8842 | `0x0280411C` | CALL | 4,5,1 | `setConfigLogData` | [global:desktopWidget, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab), control-flow-or-computed-value] (4) | 0 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `setLogDisplayContentForUserConfig` | 37 | 8854 | `0x0180411C` | CALL | 4,3,1 | `updateLogWidget` | [arg0, 1] (2) | 0 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `setLogDisplayContentForUserConfig` | 40 | 8866 | `0x0180411C` | CALL | 4,3,1 | `updateLogWidget` | [arg0, 2] (2) | 0 | - | window/tab captured at PCs1/3, count at PC7 before row callbacks |
| `updateLogWidget` | 7 | 9192 | `0x018080DC` | CALL | 3,3,2 | `getStaticWidget` | [global:desktopWidget, control-flow-or-computed-value] (2) | 1 | - | - |
| `updateLogWidget` | 9 | 9200 | `0x0100411C` | CALL | 4,2,1 | `updateLogCategoryDisplay` | [result(pc=7,r=0)] (1) | 0 | - | - |
| `setAllFilter` | 9 | 9381 | `0x0200419C` | CALL | 6,4,1 | `setListItem` | [arg0, control-flow-or-computed-value, arg1] (3) | 0 | - | - |
| `setAllFilter` | 13 | 9397 | `0x0180409C` | CALL | 2,3,1 | `updateListProperty` | [arg0, 'ListBox'] (2) | 0 | - | - |
| `setAllFilter` | 15 | 9405 | `0x0100409C` | CALL | 2,2,1 | `setLogDisplayContentForUserConfig` | [arg0] (1) | 0 | - | - |
| `setButtonStyle` | 7 | 9623 | `0x0200411C` | CALL | 4,4,1 | `setStyle` | [arg0, arg1, control-flow-or-computed-value] (3) | 0 | - | - |
| `updateControlEnable` | 3 | 9740 | `0x0200409C` | CALL | 2,4,1 | `setEnable` | [arg0, 'TextBox_TabName', arg1] (3) | 0 | - | - |
| `updateControlEnable` | 7 | 9756 | `0x0200409C` | CALL | 2,4,1 | `setEnable` | [arg0, 'Button_AllOn', arg1] (3) | 0 | - | - |
| `updateControlEnable` | 11 | 9772 | `0x0200409C` | CALL | 2,4,1 | `setEnable` | [arg0, 'Button_AllOff', arg1] (3) | 0 | - | - |
| `updateControlEnable` | 15 | 9788 | `0x0200409C` | CALL | 2,4,1 | `setEnable` | [arg0, 'ListBox_LogSettingItems', arg1] (3) | 0 | - | - |
| `setListItem` | 7 | 9966 | `0x0280811C` | CALL | 4,5,2 | `getListProperty` | [arg0, 'ListBox', arg1, 'Checked'] (4) | 1 | - | - |
| `setListItem` | 19 | 10014 | `0x0300411C` | CALL | 4,6,1 | `setListProperty` | [arg0, 'ListBox', arg1, 'Checked', control-flow-or-computed-value] (5) | 0 | - | - |
| `setListItem` | 31 | 10062 | `0x0300419C` | CALL | 6,6,1 | `setListText` | [arg0, 'ListBox', arg1, 'StatusName', control-flow-or-computed-value] (5) | 0 | - | - |
| `setListItem` | 37 | 10086 | `0x0300419C` | CALL | 6,6,1 | `setListProperty` | [arg0, 'ListBox', arg1, 'StatusStyle', control-flow-or-computed-value] (5) | 0 | - | - |
| `createFilterList` | 6 | 10346 | `0x0180415C` | CALL | 5,3,1 | `addListItem` | [arg0, control-flow-or-computed-value] (2) | 0 | - | - |
| `createFilterList` | 10 | 10362 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 27] (2) | 0 | - | - |
| `createFilterList` | 13 | 10374 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 25] (2) | 0 | - | - |
| `createFilterList` | 16 | 10386 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 22] (2) | 0 | - | - |
| `createFilterList` | 19 | 10398 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 23] (2) | 0 | - | - |
| `createFilterList` | 22 | 10410 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 24] (2) | 0 | - | - |
| `createFilterList` | 25 | 10422 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 26] (2) | 0 | - | - |
| `createFilterList` | 32 | 10450 | `0x0180415C` | CALL | 5,3,1 | `addListItem` | [arg0, control-flow-or-computed-value] (2) | 0 | - | - |
| `createFilterList` | 36 | 10466 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 66] (2) | 0 | - | - |
| `createFilterList` | 39 | 10478 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 70] (2) | 0 | - | - |
| `createFilterList` | 42 | 10490 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 71] (2) | 0 | - | - |
| `createFilterList` | 45 | 10502 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 72] (2) | 0 | - | - |
| `createFilterList` | 48 | 10514 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 73] (2) | 0 | - | - |
| `createFilterList` | 51 | 10526 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 68] (2) | 0 | - | - |
| `createFilterList` | 54 | 10538 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 69] (2) | 0 | - | - |
| `createFilterList` | 57 | 10550 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 32] (2) | 0 | - | - |
| `createFilterList` | 60 | 10562 | `0x0180405C` | CALL | 1,3,1 | `addListItem` | [arg0, 33] (2) | 0 | - | - |
| `createFilterList` | 63 | 10574 | `0x0180405C` | CALL | 1,3,1 | `updateListProperty` | [arg0, 'ListBox'] (2) | 0 | - | - |
| `addListItem` | 8 | 10879 | `0x038040DC` | CALL | 3,7,1 | `setListText` | [arg0, 'ListBox', captured(arg0.work.logDisplayCount), 'ItemName', 2254, arg1] (6) | 0 | - | row/count captured at GETTABLE PC1; final work target reread at PC22 and receives captured count+1 |
| `addListItem` | 14 | 10903 | `0x030040DC` | CALL | 3,6,1 | `setListProperty` | [arg0, 'ListBox', captured(arg0.work.logDisplayCount), 'CategoryID', arg1] (5) | 0 | - | row/count captured at GETTABLE PC1; final work target reread at PC22 and receives captured count+1 |
| `addListItem` | 21 | 10931 | `0x030040DC` | CALL | 3,6,1 | `setListProperty` | [arg0, 'ListBox', captured(arg0.work.logDisplayCount), 'Help', control-flow-or-computed-value] (5) | 0 | - | row/count captured at GETTABLE PC1; final work target reread at PC22 and receives captured count+1 |
| `setTabTitleButton` | 4 | 11156 | `0x020080DC` | CALL | 3,4,2 | `getConfigLogIndex` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `setTabTitleButton` | 9 | 11176 | `0x0100815C` | CALL | 5,2,2 | `tostring` | [control-flow-or-computed-value] (1) | 1 | - | - |
| `setTabTitleButton` | 15 | 11200 | `0x0200815C` | CALL | 5,4,2 | `getConfigLogTitle` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `setTabTitleButton` | 19 | 11216 | `0x0200419C` | CALL | 6,4,1 | `setMacroContent` | [arg0, control-flow-or-computed-value, result(pc=15,r=0)] (3) | 0 | - | - |
| `setTabTitleButton` | 24 | 11236 | `0x0200819C` | CALL | 6,4,2 | `getConfigLogEnable` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `setTabTitleButton` | 28 | 11252 | `0x020041DC` | CALL | 7,4,1 | `setButtonStyle` | [arg0, control-flow-or-computed-value, result(pc=24,r=0)] (3) | 0 | - | - |
| `setSelectedButton` | 4 | 11482 | `0x0200811C` | CALL | 4,4,2 | `getConfigLogIndex` | [global:desktopWidget, arg1, arg2] (3) | 1 | - | - |
| `setSelectedButton` | 9 | 11502 | `0x0100819C` | CALL | 6,2,2 | `tostring` | [control-flow-or-computed-value] (1) | 1 | - | - |
| `setSelectedButton` | 16 | 11530 | `0x0200419C` | CALL | 6,4,1 | `setVisibility` | [arg0, control-flow-or-computed-value, arg3] (3) | 0 | - | - |
| `setTabTitleTextBox` | 6 | 11733 | `0x0200809C` | CALL | 2,4,2 | `getConfigLogTitle` | [global:desktopWidget, captured(arg0.work.logDisplayWindow), captured(arg0.work.logDisplayTab)] (3) | 1 | - | - |
| `setTabTitleTextBox` | 10 | 11749 | `0x020040DC` | CALL | 3,4,1 | `setMacroText` | [arg0, 'TextBox_TabName', result(pc=6,r=0)] (3) | 0 | - | - |
| `initSliderBar` | 3 | 11941 | `0x0200809C` | CALL | 2,4,2 | `getControlUserWorkInt` | [arg0, 1, arg1] (3) | 1 | - | - |
| `initSliderBar` | 7 | 11957 | `0x018080DC` | CALL | 3,3,2 | `getConfigWork` | [global:desktopWidget, result(pc=3,r=0)] (2) | 1 | - | - |
| `initSliderBar` | 11 | 11973 | `0x0200411C` | CALL | 4,4,1 | `setValue` | [arg0, arg1, result(pc=7,r=0)] (3) | 0 | - | - |

## Original-word execution coverage

Coverage tiers are exact: ordinary declarations 25/25 methods and 25/25 root
binding attempts; static source/word inspection 25/25 methods and 189/189
direct-call rows; instruction-driven execution 18/25 methods.

The finite instruction-driven checks executed 13 selected cases
against the selected Lua words with pure mocks. 12 cases completed
successfully and one unsupported string category produced the expected
numeric-operand failure; all 187 observed call events matched their
admitted raw words, targets, and A/B/C widths. Independently authored typed
arguments/results cover only the retained demonstrated claims, not every
literal argument or native result (19 typed expectation rows were
checked). Raw receiver and closure identity controls ran before diagnostic
serialization. The checked native results remain requests/reads, not storage
or application observations.

Executed method coverage was 18/25:
`addListItem, initLogDisplayDataForUserConfig, initSliderBar, processAskResult, processUICommandClose, processUICommandSliderChange, processUICommandToggleButton, setAllFilter, setButtonStyle, setListItem, setLogDisplayContentForUserConfig, setLogDisplayTitleForUserConfig, setTabTitleButton, setTabTitleTextBox, update, updateControlEnable, updateLogDisplayContent, updateLogWidget`.
The 7 remaining methods are static-only: `createFilterList, init, processClosing, processUICommandDefault, processUICommandOperate, processUICommandSelection, setSelectedButton`.

The selected execution cases cover restore numeric-1 versus boolean-true,
close ordering, style false versus nil, Lua zero truthiness in a toggle,
float slider forwarding, open-tail result-to-argument forwarding with each
fixed prefix and producer tail recorded in the call ledger, explicit nil list
inversion, nil set-all-filter composition, a missing flag-table key, a zero
category, actual frame and desktop receivers, fixed/open widths, and one typed
failure. This is partial execution coverage, not universal runtime coverage.
The remaining methods and branches retain static source/word coverage only. No
live client, native storage, application, server, or wire effect was executed.

## Limits

The body establishes local control flow and native request operands. It does
not establish what native configuration APIs store, when they persist, which
UI/application lifetime owns them, or whether a request reaches a server. It
does not establish the meaning of message IDs, help IDs, or native key numbers
beyond their literal use here. Native, coercion, metamethod, and helper
boundaries remain explicit.
