# ShopSellWidget local contract

## Resource identity

This contract is for the exact retail resource
`client/script/n1635q/9rz/r2vur5yyn1635q.le.lpb`.

- LPB: 26,203 bytes, SHA-256
  `C4024FC41C6C53D0E3C91FED17DC646F06F0138A580FA3724FFA9EA4B59BABF1`.
- Decoded Lua payload: 26,190 bytes, SHA-256
  `834E9B5C09AA5DF6FE9D34031DC68B11BF0B05E0C14E87E6CADA728930AA5AED`.
- Canonical LF source: 66,135 bytes, 3,161 lines, CRLF count 0, SHA-256
  `DE0B1BD6BF32ADAFD2F6FE8ED71C64E7753DCFFE3BF709E3661FD069C4EB5766`.
- Unluac JAR: 796,256 bytes, SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.

The pinned decode route is `xivl-client-scripts/tools/retail_script.py` with
`xivl-client-scripts/tools/vendor/unluac/unluac_2025_12_23.jar`.

The public manifest identifies the decoded resource and coverage window at
`xivl-client-scripts:manifests/scripts.json:15165-15168` and
`xivl-client-scripts:manifests/retail_lua_coverage.json:26613-26625`. The
registry identifies class `ShopSellWidget`, base
`/Widget/Ask/AskBaseClass`, and 55 methods at
`xivl-client-scripts:lua/registry.json:39831-39896`. Method arities and
canonical LF source windows are recorded at
`xivl-client-structs:manifests/lua_api_contract.json:155145-155798`.

The table below gives canonical LF source lines and zero-based decoded-chunk
prototype offsets. `protoN@offset+words` means root child prototype N, its
zero-based code offset, and its code-word count. Lua 5.1 `CALL` widths are
`B-1` fixed arguments and `C-1` fixed results when B/C are nonzero; B=0 or
C=0 is dynamic. A nonzero `RETURN B` returns B-1 values. Every result width
and dynamic boundary below follows those original operands. A `pcN/M` locator
means instruction PC N at decoded byte offset M.

The root code starts at offset 32 and has 173 words. Its `pc2/offset40`
CALL supplies `"/Widget/Ask/AskBaseClass"` to the resolved `require`
(`B=2,C=1`). Its `pc6/offset56` CALL supplies `"ShopSellWidget"` and
`"AskBaseClass"` to the resolved `_defineClass` (`B=3,C=1`). All results
are discarded. Fresh global `ShopSellWidget` reads precede the 55 closure
assignment attempts, with SETTABLE PCs 9,12,...,171. Root
`RETURN pc172/offset720` returns zero values. These are emitted operations,
without proof of class creation or method installation.

`tools/build_quest_contracts.py:ChunkReader,instruction` parsed the original
instruction vectors for the byte offsets and PCs below.

## Contract boundary and work state

This is a local behavior contract under supplied values. The
[selected sale flow](shop-sell-selection-flow.md) owns its conditional opener,
rearming, result-to-item adaptation and explicit close. Actual NPC, shop
assignment, server request, inventory removal, currency mutation, completed
sale and settlement remain unbound. UI and child calls record requested
handoffs and returned helper values; they do not prove rendering, widget
creation, widget destruction, native persistence, or transaction effects.
The ShopBuy opening tuple and `shopItem.csv` buy-price field are not sell
inputs (`xivl-client-data:docs/shop-family-audit.md:42-45`,
`xivl-client-scripts:docs/gil-shop-widget-opening.md:1-6,41-66`).

`initAsk` creates a `_temp` declaration operand on `self.work`; its
`SETTABLE` writes are Lua assignment operands. The published work-member
boundary says that `_temp` declarations and field writes do not prove native
table backing, initial-value conversion, preservation, or durable readback
(`xivl-decomp:docs/script/widget-work-members.md:1-4,116-174,293-324`).
Each subsequent `GETTABLE` read of `self.work` is a fresh Lua read of the
current receiver member at that point; it is a runtime read at the Lua
receiver boundary, not evidence that a native registry or first value exists.
Fresh calls through `worldMaster`, player items, catalog/name helpers, and
desktop helpers retain their original call operands and remain binding
dependent.

The 37 `_temp` declaration fields and declared types are:

`chosenItem:integer32`, `chosenPackage:integer32`,
`chosenOperation:integer32`, `mode:integer16`, `index:integer16`,
`focus:integer16`, `selected:integer16`, `prevIndex:integer16`,
`prevFocus:integer16`, `prevCount:integer16`, `indexChange:boolean`,
`focusChange:boolean`, `listbox:integer8`, `page:integer8`,
`bonus1:boolean`, `bonus2:boolean`, `bonus3:boolean`, `itemlife:boolean`,
`bazaar:boolean`, `editWidgetOpen:integer8`, `submenu:boolean`,
`initialized:boolean`, `waitForPrice:boolean`, `waitNext:boolean`,
`waitupdate:boolean`, `shopid:integer32`, `updatecount:integer32`,
`buycount:integer32`, `price:integer32`, `closeok:boolean`,
`demandSync:boolean`, `sorttype:integer8`, `lastsub:integer8`,
`sdsize:boolean`, `lastcommandtime:integer32`, `askstatus:boolean`, and
`isMateriaList:boolean`.

The explicit assignment operands in `initAsk` set
`chosenOperation=0`, `editWidgetOpen=0`, `initialized=false`, `index=0`,
`listbox=0`, `bonus1=false`, `bonus2=false`, `bonus3=false`,
`itemlife=false`, `bazaar=false`, `waitNext=false`, `waitForPrice=false`,
`waitupdate=false`, `focus=0`, `closeok=false`, `demandSync=false`,
`submenu=false`, `lastsub=10`, and `askstatus=true`; `sorttype` receives the
one-result `desktopWidget.getConfigWork(9)` call. These operands are in
`proto1@2088+293`, with the source declaration window LF 20-246. The first
descriptor `SETTABLE` at decoded offset 2692 is the `_temp` assignment
operand; the later SETTABLEs through 2872 are separate work-field assignment
operands, not one native descriptor write.

## Complete 55-method contract

Every row describes the named pinned local prototype under supplied values.
All compositions through self, global, inherited, desktop, item, parent or
child helpers require the relevant actual function selection and normal
completion, with relevant values preserved until their reads. This applies
to fixed-width and open calls alike. Lookup/assignment/equality metamethods
and callable objects retain their own effects. Tuples list explicit Lua
arguments, including receivers; an object's `__call` can add an implicit
argument. Assignment descriptions are Lua operands and requests, not proof
of native application, persistence or matching later reads.


| # | Method / arity | LF source; prototype | Behavior, branches, calls, and result width |
|---:|---|---|---|
| 1 | `getFormName(self)` | 11-17; `proto0@2016+3` | Loads and returns `ItemListWidget`; nonzero result `RETURN pc1/offset2020`, width 1. The following zero-result epilogue is unreachable from the result path. |
| 2 | `initAsk(self)` | 20-412; `proto1@2088+293` | Declares `_temp`, performs the assignment operands above, calls `getConfigWork(9)` (`pc189/offset2844`, B=3,C=2, 2 args/1 result), configures title/text/visibility/commands/lists/help, and calls `setInitialData`; loop branches are `pc213/offset2940` and `pc222/offset2976`; `RETURN pc292/offset3256`, width 0. |
| 3 | `setInitialData(self)` | 415-462; `proto2@4669+34` | Calls `setModal(true)`, `resetListBox` for 1,2,3,4,5, `makeListFromPackage`, `changeList`, `updateWindowDisplay(true)`, and `setText("TextBlock_Title",3207)` at offsets 4677-4797; assigns modal/initialized/listbox operands; `RETURN pc33/offset4801`, width 0. |
| 4 | `processBeforeShow(self, flag)` | 465-496; `proto3@5073+25` | If `flag ~= true`, returns true. Otherwise calls `getChildWidgetByWindowName("ShopEditWidget")`; a nonnil child calls `closeShopEdit(true)`, while a nil child calls `updateWindowDisplay(true)` unless `work.submenu == true`. Branches `pc0/5073`, `pc8/5105`, `pc16/5137`; calls/returns `pc12/5121`, `pc21/5157`, `pc3/5085`, and `pc23/5165`, width 1. |
| 5 | `getListPropertyName(self, list)` | 499-525; `proto4@5335+35` | Branches list 1-5 to `TabItem_1_Maker`..`TabItem_5_Maker`, 8 to `SlotItem_Maker`, 9 to `HelpCache_Maker`; matched returns width 1 and unmatched fallthrough has no value. |
| 6 | `updateWindowDisplay(self, full)` | 528-575; `proto5@5724+37` | Calls `setGridVisibility(3)`. Truthy `isMateriaList` enables `Grid_MateriaEquipList` and disables `Grid_TabList`; listbox 1 enables `Button_SortStatus` and calls `displaySortType(sorttype)`, otherwise disables the button; only `full == true` at `pc32/5852` calls `updateListFocus`; materia/list branches are `pc5/5744` and `pc17/5792`; no result, width 0. |
| 7 | `updateListFocus(self)` | 578-683; `proto6@6140+87` | If `updatecount ~= 0`, returns false width 1. Otherwise reads list/focus properties, handles empty/list visibility, clamps focus, calls `focusToIndex`, writes focus, and calls help/focus refresh; normal fallthrough width 0. |
| 8 | `setGridVisibility(self, mode)` | 686-764; `proto7@6917+82` | Sends `Grid_ActorName=false`, `Grid_Help=(mode==2)`, `Grid_TabList=(mode==1 or mode==2 or mode==3)`, `Grid_BackpackAndGil=true`, `Grid_ItemNameBase=(mode==1 or mode==3 or mode==4 or mode==5)`, details 1/2 from `bonus1/bonus2`, detail 3 from `bonus3 or itemlife or bazaar`, labels/life/bazaar from their work fields, and `Grid_MateriaAttachBazaarInformation=false`; calls begin `pc3/6929`, `pc10/6957`, `pc21/7001`, and end `pc80/7237`; no result, width 0. Mode 0 still supplies backpack/gil true and materia-bazaar false; detail 3 receives the selected Lua value without boolean normalization. |
| 9 | `setWindowFocus(self, window)` | 767-787; `proto8@7702+16` | For nonnil and nonempty `window`, requests logical focus, reads keyboard focus, and conditionally requests keyboard focus; no result, width 0. |
| 10 | `displayBagcapacityAndMoney(self)` | 790-822; `proto9@7915+23` | Freshly calls player money, package-1 capacity, and package-1 free-space; requests `TextBlock_Gil` text 3263 and `TextBlock_ItemStack_2` text 3551; no result, width 0. |
| 11 | `isExistItem(self, a1, a2, type)` | 825-861; `proto10@8247+34` | For type nil/1, fresh-reads player item and returns `item ~= nil`; for type 2, calls `desktopWidget.getBazaarItem` and returns its nonnil test; tested returns width 1, unknown type has no value. |
| 12 | `getSelectedTab(self)` | 864-874; `proto11@8529+6` | Reads `TabControl_ItemList` selected index, adds 1, and returns width 1. |
| 13 | `getListBoxName(self, list)` | 877-900; `proto12@8649+28` | Maps 1-5 to `ListBox_TabItem_1`..`ListBox_TabItem_5`; otherwise returns empty string, width 1. |
| 14 | `getListBoxItemNum(self, list)` | 903-914; `proto13@8967+7` | `CALL pc3/offset8979 B=3,C=0` calls `getListPropertyName(self,list)` with dynamic results; `TAILCALL pc4/offset8983 B=0,C=0` calls `getListPropertyCount` with `self` plus all returned values, preserving dynamic arguments/results. |
| 15 | `getListBoxFocusNum(self, list)` | 917-953; `proto14@9086+30` | Calls list count/name and `getControlProperty("FilteredCount")`; only item count `== 0` branches at `pc6/9110` to `(0,0,0,0)`. Otherwise it saves a first current `work.focus` read F1, compares filtered count K to a second fresh focus read F2 at `pc21/9170`, and replaces F1 with K-1 only if K<F2. It returns `(K,K-1,0,F1)` after that conditional replacement, width 4, at `pc28/9198`; empty return is `pc12/9134`. Thus item count 1/K3/F1=3/F2=3 returns `(3,2,0,3)`, and F1=6/F2=2 returns `(3,2,0,6)`. |
| 16 | `focusToIndex(self, list, focus)` | 956-984; `proto15@9376+24` | Calls list name/focus helpers. Conditions `pc6/9400` and `pc8/9408` select one `-1` RETURN at `pc11/9420` when the first focus-count result K is zero or supplied focus>=K. There is no lower-bound guard; negative focus proceeds when K is positive. Otherwise requests `FilteredIndex=focus`, then `TAILCALL pc21/9460 B=4,C=0` supplies `(self,listProperty,"Index")` to `getControlProperty` and forwards its dynamic results. |
| 17 | `indexToFocus(self, list, index)` | 987-1019; `proto16@9657+24` | Calls `getListBoxItemNum` at `pc6/9681` but ignores that result; calls focus at `pc9/9693` and tests only whether its first result is greater than zero at `pc10/9697`, then writes `Index`, reads `FilteredIndex`, and returns it (initial -1 otherwise), width 1. |
| 18 | `initListBox(self, list)` | 1022-1092; `proto17@9961+55` | If the resolved list name is empty (`pc3/9973`), no-op; otherwise writes `IntData.Value0`, command conditions for mouse/anchor/selection/previous/next, cancel, visibility, empty label, and `IsTabStop`; no result, width 0. |
| 19 | `resetListBox(self, list)` | 1095-1126; `proto18@10571+24` | If count is zero (`pc6/10595`), returns; otherwise loops deleting rows and calls `updateListProperty`; no result, width 0. |
| 20 | `getPackageFromList(self, list)` | 1129-1146; `proto19@10821+22` | Branches list 1->1, 2->100, 3->8, 4->5, 5->100 at offsets 10825, 10841, 10857, 10873, 10889; default remains 1; return width 1. |
| 21 | `setItemToXmlLight(self, list, row, package, item, extra)` | 1149-1256; `proto20@11012+91` | Requires positive package/item; fresh-reads item, catalog, icon, stackability, count, and name. Missing item returns false; otherwise the emitted `setItemToXml` arguments after the desktop receiver are `self,listProperty,row,item,"TBL_null",catalog,icon,stackable,count,name,sortMode,true,false,submode,package,item,extra,false`, with sortMode `work.sorttype` or 11 and submode 7 or 8; returns true width 1. Pending updates can set focusChange. |
| 22 | `getMoneyListIndex(self, currency)` | 1259-1391; `proto21@11813+129` | Exact accepted mapping is `1000001->1`, `1000102->2`, `1000101->3`, `1000103->4`, `1000107->5`, `1000106->6`, `1000111->11`, `1000110->12`, `1000113->14`, through `1000123->24`. IDs `1000104`, `1000108`, `1000109`, `1000105`, `1000112`, and unknown values return -1; every branch result width 1. |
| 23 | `setSortType(self, list, row)` | 1394-1420; `proto22@12603+20` | Freshly reads package-1 item at `row+1`; its nonnil branch is `pc7/12631`, then `pc18/12675` calls the selected desktop helper with explicit tuple `(desktopWidget,self,list,row,work.sorttype,item)`. No result, width 0. |
| 24 | `updateSortType(self)` | 1423-1448; `proto23@12842+18` | Iterates list-1 rows, calls `setSortType`, then updates the list property; no result, width 0. |
| 25 | `makeListFromPackage(self, package, item)` | 1451-1667; `proto24@13052+185` | With nil item, package 1 builds only package 1 through capacity-freeSpace, package 100 builds only package 100 through capacity, nil package builds both, and unsupported package builds neither. Each full-build row loop stops on a helper result not exactly true. With a supplied item, package outside 1/100 returns before the bag/money call; 1/100 adds/deletes the corresponding row. The common continuation requests bag/money display; no result, width 0. |
| 26 | `displayHelp(self, value)` | 1670-1679; `proto25@14248+5` | Requests help text on `TextBlock_Help` with the supplied value; no result, width 0. |
| 27 | `displayFocusedItemHelp(self)` | 1682-1867; `proto26@14341+176` | Returns one false for `updatecount>0`, no focus, or past list end (`pc2/14349`, `pc10/14381`, `pc36/14485`); updatecount -1 does not take the first rejection. Literal local selector 1 uses player `_getItem`. After `setItemDetail`, exactly true from `isEquipment` enables the point scan 1..27 (`pc102/14749` through `pc124/14837`), retaining at most four points whose `isFitForEquipPoint` result is exactly true. It queries player `_getEquippingItem` for those points in order until nonnil, calls `setItemDetailEquip` (C=5, four requested results), then `updateWindowDisplay(false)`. Normal fallthrough returns zero values. |
| 28 | `previousSequence(self)` | 1870-1881; `proto27@15675+6` | Calls the dynamically selected `saveSortType`, then `setBaseAskResult(self,-1)`; both results are discarded. No setter effect is inferred; zero values returned. |
| 29 | `processUICommandOperate(self, a1, command, a3, a4)` | 1884-1929; `proto28@15788+36` | Handles only `Button_SortStatus` (`pc1/15792`), calls `changeSortType`, `updateSortType`, remaps index/focus with `indexToFocus`/`focusToIndex`, then calls `displaySortType`; no result, width 0. |
| 30 | `processUICommandCancel(self, a1, command, a3, a4)` | 1932-1958; `proto29@16169+21` | Returns false width 1 when editWidgetOpen is nonzero (`pc2/16177`), waitNext is true (`pc8/16201`), or `isAskFinish` returns true (`pc14/16225`); otherwise calls `previousSequence` and falls through width 0. |
| 31 | `processUICommandClose(self, a1, command, a3, a4)` | 1961-1968; `proto30@16387+3` | Calls `previousSequence` at `pc1/16391`; no result, width 0. |
| 32 | `processUICommandSelection(self, a1, command, focus, list)` | 1971-2108; `proto31@16461+120` | Only when current `editWidgetOpen~=0` does it look up the child (`pc2/16469`, `pc7/16489`): a nonnil child returns one false; a nil child with fresh time minus `lastcommandtime>2` (`pc15/16521`) calls `closeShopEdit(true)`, while a false strict comparison returns one false at pc22. Exact-true waitNext or isAskFinish returns one false. Exact-false keyboard check returns zero values; nil proceeds. Remaining paths handle empty/stale focus, exact-true waitupdate, package-1 exact-false isEnabled, and package 100 selection. Normal selection writes focus/listbox/chosenPackage/chosenItem (`index+1`) and calls operateSell. Locators include `pc28/16573`, `pc34/16597`, `pc41/16625`; `TAILCALL pc54/16677` and `pc65/16721` forward the selected display/focus results dynamically. Normal fallthrough width 0. |
| 33 | `processUICommandDefault(self, a1, command, event, focus, list)` | 2111-2198; `proto32@17570+84` | Only when `editWidgetOpen~=0` does it look up the child (`pc2/17578`, `pc7/17598`): nonnil returns one false; nil plus fresh time-minus-lastcommandtime>2 (`pc15/17630`) calls closeShopEdit(true), a false strict comparison returns one false at pc22. Exact-true waitNext/isAskFinish also returns one false. Exact-false keyboard check (`pc39/17726`) reaches zero-value RETURN `pc41/17734`; nil proceeds. MouseEnteredItem/AnchoredItem requires nonnil list and nonnegative focus, assigns listbox/focus and calls setCommonTimer(0.2). TabChanged reads selected tab and calls changeList; Previous/Next calls catalogSkip(-1/1). Normal fallthrough width 0. |
| 34 | `processTimer(self)` | 2201-2225; `proto33@18478+18` | Calls `focusToIndex`; only the index assignment is guarded by result `>= 0` at `pc6/18502`. It always sets page 0 at `pc11/18522`, calls `updateWindowDisplay(true)` at `pc14/18534`, and calls `selectedBorder` at `pc16/18542`, including an index result of -1; no result, width 0. |
| 35 | `catalogSkip(self, delta)` | 2228-2331; `proto34@18717+96` | Subtracts one from the first `getListBoxFocusNum` result and returns at `pc7/18745` when that value is -1; this is an empty-count guard, not a missing-index test. Remaining list 1/page and sorted `getItemSortKey` paths (`pc13/18769`, `pc20/18797`) bound movement, write focus, and refresh when changed; no result, width 0. |
| 36 | `selectedBorder(self, item, visible)` | 2334-2390; `proto35@19376+50` | A nonnil item is only a gate for the single-row path; exact-false visible selects Collapsed, while nil or 0 selects Visible. It passes one fresh work.index as the setListProperty row operand, then assigns work.selected from a second fresh work.index read then calls updateListProperty. Neither a work.index write nor equality of those two reads follows. With nil item, current selected==-1 and nil visible returns before row writes/update; otherwise it requests Collapsed for all rows and assigns selected=-1. Branches `pc4/19392`, `pc7/19404`, `pc24/19472`, `pc26/19480`; no result, width 0. |
| 37 | `changeList(self)` | 2393-2419; `proto36@19806+21` | Builds `TabItem_` + tostring(listbox) and reads `Header`; `CALL pc10/19846 B=4,C=0` has 3 fixed args/dynamic results, then `CALL pc11/19850 B=0,C=1` preserves the prefix `(self,"TextBlock_Title",<all Header results>)` with dynamic total width. It resets index/focus, then `TAILCALL pc18/19878 B=3,C=0` forwards `updateWindowDisplay(true)` results; no fixed result. |
| 38 | `operateSell(self)` | 2422-2442; `proto37@20107+15` | Calls selected setBaseAskResult(self,1), assigns waitForPrice=true and lastsub=8, then assigns the fresh _getServerTime result to work.lastcommandtime. Returns one true at `pc13/20159`; these assignments do not establish native state application. |
| 39 | `updatePlayerItem(self, type, item)` | 2445-2540; `proto38@20348+85` | Exact numeric type 0 assigns the supplied update count and clears change flags. Every value with type~=0, including nil and false, reaches chosen-item matching and the continuation; only exact types 1/100 rebuild their lists. Decrement requires a fresh positive updatecount; a later zero read controls refresh/close, then waitupdate=false is assigned. Numeric comparisons and selected calls must complete normally. Branches type 0/1/100 are `pc1/20352`, `pc11/20392`, `pc19/20424`; zero values returned. |
| 40 | `setShopEditData(self, operation, count)` | 2543-2551; `proto39@21094+5` | Assigns chosenOperation and buycount from arguments; no result, width 0. |
| 41 | `closeShopEdit(self, optional)` | 2554-2623; `proto40@21199+57` | Only nil optional enters operation dispatch (`pc0/21199`): chosenOperation==1 calls setBaseAskResult(self,1), setInputEnable(false), then assigns waitNext=true; another operation assigns editWidgetOpen=0, calls selectedBorder(self,nil,false) at `pc20/21279`, then setInputEnable(true). Nonnil optional, including false, skips both. Common continuation calls closeMateriaList only for truthy isMateriaList, assigns chosenOperation=0, looks up ShopEditWidget, and only for a nonnil result calls closeChildWidget(desktopWidget,"ShopEditWidget",self) at `pc41/21363 B=4,C=2`, requesting one result that is discarded. It assigns editWidgetOpen=0 and the fresh server-time result to work.lastcommandtime, redraws only for nil optional (`pc49/21395`), then returns one true. Calls are attempts, without proved closure or selected-border effect. |
| 42 | `checkChosenItem(self, item, package, row)` | 2626-2684; `proto41@21832+52` | Checks optional package/item against chosen work, current list package, and `index+1`, then fresh-reads `_getItem` and compares with Lua `==` at `pc44/22008`, which may invoke `__eq`; it is not a raw identity proof. Each terminal branch returns bool width 1. |
| 43 | `getItemContent(self, selector, content, extra)` | 2687-2778; `proto42@22232+82` | With nil selector, `TAILCALL pc5/22252 B=4,C=0` forwards getControlProperty(self,content,extra) results dynamically. Otherwise it freshly gets I through player._getItem using current chosenPackage/chosenItem. For content="isEquipping" and nonnil I, exact-true I._isEquipping(I) returns one `1`, otherwise one `0`; nil I instead falls through to the list-property tailcall. Both getItemMateriaAttachInfo calls use the fixed tuple `(desktopWidget,I)` at `pc37/22380` and `pc49/22428`, with B=3,C=3 requesting two results. Content="materianumber" returns one first requested result, or one `0` for nil I. Content="materiapermission" returns one second requested result, or one false for nil I. Content="polish" returns one boolean: nonnil I, truthy isEquipment (including numeric `0`) and exact fitness equal to `10000` yield true, otherwise false. Remaining content, including isEquipping with nil I, calls getListPropertyName(self,current listbox) for one result P, then `TAILCALL pc79/22548 B=6,C=0` supplies five explicit arguments `(self,P,current work.index,content,extra)` to getListProperty and forwards all results. |
| 44 | `getAskResult(self)` | 2781-2820; `proto43@22999+35` | Calls `getBaseAskResult` at `pc1/23003`; base -1 returns `(0,0,0,0)` at `pc8/23031`; otherwise assigns askstatus=false, and only `waitForPrice == true` at `pc14/23055` returns `(chosenPackage,chosenItem,1,1)` at `pc22/23087`. A value such as 0 takes the other path, assigns waitupdate=true, and returns `(chosenPackage,chosenItem,buycount,nil)` at `pc33/23131`. All explicit returns width 4. |
| 45 | `setAskParameter(self)` | 2823-2842; `proto44@23340+14` | Calls `updateWindowDisplay(true)`, assigns askstatus=true, conditionally calls `selectedBorder` when editWidgetOpen=0 (`pc7/23368`), assigns waitNext=false, and returns width 0. |
| 46 | `setPrice(self, package, item, price)` | 2845-2961; `proto45@23553+99` | A chosen item/package mismatch assigns waitForPrice=false and returns zero. A matching pair assigns price before package dispatch; unsupported package returns at `pc19/23629` without clearing waitForPrice. Packages 1/100 freshly read item/catalog/name and call openChildWidget at `pc53/23765 B=0,C=2` with prefix `(desktopWidget,"ShopEditWidget",self,true,11,price,nil,nil,nil,self,<all item._getCatalogID(item) results>)` and dynamic total width. Only exact-true child result (`pc54/23769`) takes success order: selectedBorder(self,work.chosenItem-1,true) at `pc61/23797`, waitForPrice=false at `pc63/23805`, editWidgetOpen=11 at `pc65/23813`, input false at `pc68/23825`, server-time CALL `pc72/23841` then assignment to work.lastcommandtime `pc73/23845`. Truthy isEquipment followed by attached count>0 calls showMateriaList; then one true RETURN `pc87/23901`. Other child results assign editWidgetOpen=0 at `pc90/23913` and fresh time to lastcommandtime at `pc95/23933`, then waitForPrice=false at `pc97/23941` and zero return. These are request/assignment operands, without proved child creation. |
| 47 | `updatePrice(self, catalog, name, price)` | 2964-3009; `proto46@24479+36` | Iterates one-based item index i and calls selected checkCatalogQuality(self,package,i,catalog,name); exact true requests setListText on zero-based list row i-1, property price, text ID `3201` and supplied price. Then updates the list; zero values returned. |
| 48 | `checkCatalogQuality(self, package, item, catalog, name)` | 3012-3040; `proto47@24855+21` | Calls player._getItem(package,item) and indexes its returned I for _getCatalogID without a nil guard. Catalog mismatch (`pc9/24891`) returns one false before _getNameIndex lookup. Matching catalog permits the name lookup; matching name returns one true, otherwise one false. Nil I can fail on indexing, so it does not establish a false return. |
| 49 | `syncItemWork(self, value)` | 3043-3049; `proto48@25066+3` | Assigns demandSync=false; no result, width 0. |
| 50 | `getAskWaitStatus(self)` | 3052-3059; `proto49@25146+4` | GETTABLE-reads current work askstatus and returns it, width 1. |
| 51 | `showMateriaList(self)` | 3062-3100; `proto50@25227+29` | Freshly reads the chosen item and calls the selected helper with explicit tuple setMateriaListItems(desktopWidget,self,item), three arguments. Requests Grid_MateriaEquipList=true, Grid_TabList=false and Button_ListClose=false, then assigns isMateriaList=true. Zero values returned; no item or materia mutation is established. |
| 52 | `closeMateriaList(self)` | 3103-3119; `proto51@25628+11` | Requests `Grid_MateriaEquipList=false` and `Grid_TabList=true`, assigns isMateriaList=false; no result, width 0. |
| 53 | `displaySortType(self, sort)` | 3122-3133; `proto52@25807+7` | Calls `desktopWidget.displaySortType(desktopWidget,sort,self,"Button_SortStatus")` with `pc5/offset25827` original fixed operands; no result, width 0. |
| 54 | `changeSortType(self)` | 3136-3148; `proto53@25938+8` | GETTABLE-reads work sorttype, calls desktop sort change, and stores the one-result readback; no result, width 0. |
| 55 | `saveSortType(self)` | 3151-3161; `proto54@26073+6` | GETTABLE-reads work sorttype and calls `desktopWidget.saveSortType`; no result, width 0. |

## Exact local mappings and literals

List selectors map to properties `TabItem_1_Maker` through
`TabItem_5_Maker`, `SlotItem_Maker` for 8, and `HelpCache_Maker` for 9;
list-box names are `ListBox_TabItem_1` through `ListBox_TabItem_5`.
Package mapping is 1->1, 2->100, 3->8, 4->5, 5->100. Initialization uses
title `@` + tostring(3408), `Button_SortStatus`,
`TabControl_ItemList`, `UILuaCommands.TabChanged`, text IDs 214/10091 and
214/10093, title 3402, hidden `TabItem_3` through `TabItem_6`, and help
parameters `TabItem_1,1,71911` and `TabItem_2,1,71912`. `setInitialData`
uses title 3207. Bag/money uses text IDs 3263 and 3551; price uses 3201;
focused-item help uses 3140.

`getMoneyListIndex` starts at index 1. Its exact accepted mapping is:

`1000001->1`, `1000102->2`, `1000101->3`, `1000103->4`, `1000107->5`,
`1000106->6`, `1000111->11`, `1000110->12`,
`1000113->14`, `1000114->15`, `1000115->16`, `1000116->17`,
`1000117->18`, `1000118->19`, `1000119->20`, `1000120->21`,
`1000121->22`, `1000122->23`, `1000123->24`.
The explicit rejected IDs `1000104`, `1000108`, `1000109`, `1000105`, and
`1000112`, and every unknown ID, return -1.

The original `proto21@11813+129` path starts with `LOADK pc0/offset11813`
(`R2=1`) and follows the ordered EQ/JMP/ADD chain. Accepted IDs take true
edges at `pc1/11817`, `pc6/11837`, `pc11/11857`, `pc16/11877`,
`pc21/11897`, `pc26/11917`, `pc55/12033`, `pc60/12053`, and
`pc71/12097` through `pc121/12297` to the indexed width-1 returns. Rejected
IDs take true edges at `pc31/11937`, `pc37/11961`, `pc43/11985`,
`pc49/12009`, or `pc65/12073`, then load -1 and return width 1. Unknown
input follows every EQ false edge and reaches `JMP pc122/12301`, `ADD
pc125/12313`, `LOADK pc126/12317`, and `RETURN pc127/12321` with -1.

Selection and default command paths compare the fresh server-time result minus
`lastcommandtime` to the literal 2; no seconds, clock domain, or rate is
inferred. `processUICommandDefault` passes literal `0.2` to
`setCommonTimer`; this is preserved as an operand, not interpreted as a
duration unit. `processTimer` conditionally writes the mapped index but always
writes page 0 and requests redraw and selected-border update, including a
negative mapped index.

## Binding and width limits

The 55 child prototypes have seven tailcalls, 309 reachable CALL/TAILCALL
instructions, 138 RETURN instructions, and no VARARG. The root adds two CALLs
and one RETURN, so the whole chunk has 311 CALL/TAILCALL and 139 RETURN
instructions under the same finite CFG rule. Dynamic operands are retained at
the following original locations:

- `getListBoxItemNum`: `CALL pc3/8979 B=3,C=0`, then `TAILCALL pc4/8983
  B=0,C=0`.
- `focusToIndex`: `TAILCALL pc21/9460 B=4,C=0`.
- `processUICommandSelection`: `TAILCALL pc54/16677 B=3,C=0` and `pc65/16721
  B=2,C=0`.
- `changeList`: `CALL pc10/19846 B=4,C=0`, `CALL pc11/19850 B=0,C=1`, and
  `TAILCALL pc18/19878 B=3,C=0`.
- `getItemContent`: `TAILCALL pc5/22252 B=4,C=0` and
  `pc79/22548 B=6,C=0`.
- `setPrice`: `_getCatalogID CALL pc52/23761 B=2,C=0`, followed by
  `openChildWidget CALL pc53/23765 B=0,C=2`.

The call and composition qualifications preceding the method matrix apply
to every fixed or open call, including selectedBorder and previousSequence.
Zero B/C operands retain their dynamic widths and known fixed prefixes.
Child helper values are tested or discarded as the original operands specify.
Property, focus, item, catalog, money, time and materia helper effects require
their actual bindings and are not established by their names.

The resource establishes assignment operands, current reads, predicates,
call arguments and result widths. Opener/NPC identity, server protocol,
inventory/currency mutation, rendered output, child lifecycle and completed
sale require their separate evidence.
