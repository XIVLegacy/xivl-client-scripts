# CraftEditWidget local interaction contract

This contract describes the bounded local behavior of the pinned retail
`CraftEditWidget`: Lua operands, branches, list-row requests, dynamic parent and
child requests, and local return values. Native implementation, caller
identity, storage, rendering, lifetime, and server behavior remain outside the
contract.

## Reproducibility and public locators

The exact input and the public identity records are:

- LPB resource: `client/script/n1635q/7s94q561qn1635q.le.lpb`, 41578 bytes,
  SHA-256
  `7A992207ACEA14BFBD78154E2E0923D6E7F9EAB04B8F2927C78A4DD691DD80D9`
- Decoded payload: 41565 bytes, SHA-256
  `FA3CC0D608A8C052CAA7AB726A8D30AEAF7257564BD47F1B21F316FA22CC197B`
- Canonical LF source: 117625 bytes, 5376 lines, SHA-256
  `388C81778B4FA9E446239D99A826C794301D410D450A342021F7B86BDE527ACA`
- Pinned decompiler JAR: `tools/vendor/unluac/unluac_2025_12_23.jar`, 796256 bytes,
  SHA-256
  `98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`,
  recorded by `xivl-client-scripts:tools/vendor/unluac/PROVENANCE.json:2-5`

The pinned `xivl-client-scripts:tools/retail_script.py` route decoded the LPB
and drove the decompile; the JAR above is the decompiler stage, not the LPB
decoder.

The canonical source size, hash, and line count are recorded at
`xivl-client-scripts:manifests/scripts.json:15339-15342`. The LPB size, hash,
decoded size/hash, and decoded path are recorded at
`xivl-client-scripts:manifests/retail_lua_coverage.json:25608-25620`. The
registry binds the ciphered resource to `CraftEditWidget` and lists its methods
at `xivl-client-scripts:lua/registry.json:40562-40644`. The API manifest names
the receiver, formal parameters, arities, and LF source windows at
`xivl-client-structs:manifests/lua_api_contract.json:160231-161081`.

The root first requests `require("/Widget/WidgetBaseClass")`, calls
`_defineClass("CraftEditWidget","WidgetBaseClass")`, and then attempts the
72 method-closure bindings. Those root calls and `SETTABLE` operands establish
the script binding attempts only; they do not prove native class registration
or method dispatch. In `init`, the observed startup assignments are the fields
listed in the matrix, including `sorttype` from
`desktopWidget.getConfigWork(9)`; all other `_temp` declarations remain
current-read/unknown until a later write.

The observed `init` writes are `chosenItem=0`, `chosenOperation=0`,
`bonus1/2/3=false`, `itemlife=false`, `bazaar=false`,
`updatenexttime=false`, `closeok=false`, `demandSync=false`, `focus=0`,
`sorttype=desktopWidget.getConfigWork(9)`, and `historyget=false`/
`memoget=false`. These are Lua assignment operands, not native type or
storage proofs.

The decoded root has 72 direct child prototypes and no child prototype beneath
any method. The table below uses zero-based decoded prototype offsets and
zero-based PCs. The formal arity includes the receiver, matching the API
manifest; all 72 prototypes are non-variadic. A bare `return` or fall-through
is written as `0 values`, not as `nil`. No method body here returns a nil
literal; nil can still be a dynamic/native result or an
undeclared work read. `TAILCALL` means the callee's result width is preserved;
an ordinary call followed by a bare return is `0 values`.

## Complete 72-method matrix

| # | method | arity | prototype offset | LF source | behavior and decisive branch | result |
|---:|---|---:|---:|---|---|---|
| 1 | `getFormName` | 1 | `root/proto0 @2584` | 11-17 | Returns the fixed form name. | 1 string, `SubItemListWidget`; the trailing 0-value epilogue is unreachable. |
| 2 | `init` | 3 | `root/proto1 @2659` | 20-459 | Declares 36 `_temp` members, writes the observed initial fields, sources sorttype from `desktopWidget.getConfigWork(9)`, wires controls/list boxes, and calls `setInitialData`. | 0 values. |
| 3 | `setInitialData` | 3 | `root/proto2 @5643` | 462-591 | Requests the modal setter; A2 non-nil selects mode 411/repair, nil selects mode 410/normal; resets lists, configures 3-5, rebuilds packages, and requests dummy rows 0-16. | 0 values. |
| 4 | `setNumberInput` | 5 | `root/proto3 @6527` | 594-614 | Calls `setControlProperty(name,Minimum,A2)`, then distinct `setMaximum(name,A3)` and `setValue(name,A4)`. | 0 values. |
| 5 | `getListPropertyName` | 2 | `root/proto4 @6690` | 617-643 | Maps 1-5 to `TabItem_i_Maker`, 8 to `SlotItem_Maker`, and 9 to `HelpCache_Maker`. | 1 string for supported ids; unsupported fall-through is 0 values. |
| 6 | `setButtonEvents` | 2 | `root/proto5 @7079` | 646-664 | Reads a control's `Command`, installs that command condition, and installs its cancel condition. | 0 values. |
| 7 | `updateWindowDisplay` | 2 | `root/proto6 @7260` | 667-735 | Reads `work.editWidgetMode` freshly at PCs 1, 43 and 52, compared at PCs 2, 44 and 53; the separate `work.mode` read is PC17 and its comparison is PC18. The first read selects the step/edit arm; only a second fresh value equal to 2 writes step 2 and requests grid 7. Step 0 requests grid 4, step 1 reads separate `work.mode` (5 -> grid 9, otherwise grid 4), and step 2 requests grid 5; unsupported steps return. The third fresh edit-mode read gates the A1=true focus refresh. | 0 values. |
| 8 | `updateListFocus` | 1 | `root/proto7 @7747` | 738-1004 | List 8 returns false; a zero first result from the selected `getListBoxFocusNum` selects the display arm that writes step/detail fields and requests help, grid, visibility, and focus before converging on true; only step/edit guards skip work. The populated path passes focus, row-detail, chosen package/item, quantity-bound, and edit-enable operands to its helper requests. | 1 boolean: false only for list 8; empty, skipped, and populated paths return true. |
| 9 | `setGridVisibility` | 2 | `root/proto8 @9677` | 1007-1155 | Requests literal grid predicates; list 1/step 1 requests `Button_SortStatus` true and `displaySortType`, while a non-1 listbox or a non-1 step requests `Button_SortStatus` false; detail grid 3 uses truthy `bonus3`/`itemlife`/`bazaar`, with list 5 requesting detail grids off. | 0 values. |
| 10 | `setWindowFocus` | 2 | `root/proto9 @11003` | 1158-1178 | Ignores nil/empty names; otherwise requests logical focus, calls the dynamic `_getKeyboardFocusedWidget`, and requests keyboard control focus only when that returned value compares equal to self (possibly through Lua `__eq`). This does not prove keyboard ownership. | 0 values. |
| 11 | `displayBagcapacityAndMoney` | 1 | `root/proto10 @11216` | 1181-1213 | Reads money and package-1 capacity/free-space and requests the two text values using content ids 3263 and 3551. | 0 values. |
| 12 | `isExistItem` | 4 | `root/proto11 @11548` | 1216-1238 | For A3 nil or 1, reads player item at A1/A2 and tests non-nil; other A3 skips the lookup. | 1 boolean for A3 nil/1; unsupported A3 is 0 values. |
| 13 | `checkPackageAndIndex` | 5 | `root/proto12 @11723` | 1241-1291 | A4 nil/1 compares a player read, 2 compares bazaar data, and 4 compares retainer data; unsupported A4 skips all paths. | 1 boolean on supported selectors; unsupported A4 is 0 values. |
| 14 | `getSelectedTab` | 1 | `root/proto13 @12095` | 1294-1304 | Calls the dynamic `getSelectedIndex` for `TabControl_ItemList` and executes Lua `ADD` with 1. | 1 value on normal completion; `ADD` may invoke `__add` and return an arbitrary value, so no numeric type or tab-identity guarantee. |
| 15 | `getListBoxName` | 2 | `root/proto14 @12215` | 1307-1330 | Maps ids 1-5 to `ListBox_TabItem_1` through `_5`. | 1 string; unsupported ids return the empty string. |
| 16 | `getListBoxItemNum` | 2 | `root/proto15 @12533` | 1333-1344 | Builds a fixed receiver prefix, appends all results of `getListPropertyName`, and `TAILCALL`s `getListPropertyCount`. | Dynamic callee result width; dynamic argument tail can change the callee's argument count. |
| 17 | `getListBoxFocusNum` | 2 | `root/proto16 @12652` | 1347-1383 | Independent item count N at PC 2 controls the zero arm; when N is nonzero, separate `FilteredCount` K and fresh F1/F2=`work.focus` reads feed the strict K<F2 test, which replaces only local F1 with K-1; there is no `work.focus` write. | 4 values: `0,0,0,0` when N=0, otherwise `(K,K-1,0,F1)` after local replacement; N=3,K=1,F1=6,F2=2 returns `(1,0,0,0)`, while F1=6/F2=2/K=3 returns `(3,2,0,6)` and F1=3/F2=3/K=3 returns `(3,2,0,3)`. |
| 18 | `focusToIndex` | 3 | `root/proto17 @12942` | 1386-1414 | Empty or A2 at/above filtered count returns -1; there is no lower-bound guard, so a negative A2 enters the write path, which then `TAILCALL`s `getControlProperty(Index)`. | 1 value -1 on the guard, otherwise dynamic helper result width. |
| 19 | `indexToFocus` | 3 | `root/proto18 @13223` | 1417-1456 | Starts at -1; when rows exist writes source `Index=A2`, stores the first filtered-index read, then restores `Index=work.index`. | 1 value: -1 or opaque first filtered-index result; not a typed integer guarantee. |
| 20 | `initListBox` | 2 | `root/proto19 @13572` | 1459-1523 | Empty control name is a no-op; otherwise requests `IntData.Value0`, mouse/anchor/selection/previous/next commands, cancel, and visibility. | 0 values. |
| 21 | `resetListBox` | 2 | `root/proto20 @14147` | 1526-1558 | Zero rows return immediately; otherwise requests reverse row deletion and updates the property. | 0 values. |
| 22 | `getPackageFromList` | 2 | `root/proto21 @14401` | 1561-1576 | Maps list 1->1, 2->100, 3->101, 4->8, with default 1. | 1 literal numeric mapping. |
| 23 | `setItemToXml` | 7 | `root/proto22 @14576` | 1579-1864 | Source 5 requests a virtual item from A4; source 6 uses A6 and returns false for nil without an item lookup; source 2 requests bazaar; source 3 requests shop info then requests a virtual item; only the default selector path uses nonnil A6, including false, or looks up the player item when A6 is nil. Nil resolved item branches false; resolved rows pass local owner/equipped/reward operands to desktop row/detail calls. | 1 boolean: false on each nil-source path, true after the normal local call path; a false supplied A6 may fail at later field access. |
| 24 | `setItemToXmlLight` | 6 | `root/proto23 @16316` | 1867-1994 | Non-positive package/index or missing player item branches false; repair mode requests hidden visibility outside 10013001-10013005; list 1/2/3 choose sort operands; updatecount/listbox/focus can set `focusChange`. | 1 boolean: false on rejected lookup, true even when visibility is false. |
| 25 | `getMoneyListIndex` | 2 | `root/proto24 @17285` | 1997-2129 | Applies the literal currency catalog map and fallback. | 1 literal numeric mapping; mapped row or -1. |
| 26 | `setSortType` | 5 | `root/proto25 @18075` | 2132-2157 | Reads player item at package A4 and index A2+1; missing item skips the desktop sort call. | 0 values on both paths. |
| 27 | `updateSortType` | 1 | `root/proto26 @18286` | 2160-2192 | Loops current list-1 rows and calls `setSortType` with current `work.sorttype`, then requests a list update. | 0 values. |
| 28 | `makeListFromPackage` | 3 | `root/proto27 @18568` | 2195-2422 | Nil A2 rebuilds package 1 and/or 100; rebuild loops continue only on exact `true` from `setItemToXmlLight`, so false/nil/0 stop; supplied A2 requests an update or deletion for one list-1/list-2 row, with a missing item deleting the current last row; package 101 and unsupported selectors return before handled refresh. | 0 values. |
| 29 | `makeRecipeList` | 3 | `root/proto28 @19809` | 2425-2453 | A1=0 resets list 5; A1=-1 updates it; otherwise non-nil A2 requests row A1-1 with source 5. | 0 values. |
| 30 | `makeHistoryList` | 4 | `root/proto29 @20071` | 2456-2492 | A1=0 resets the selected list; A1=-1 updates and sets `historyget` for list 3 or `memoget` otherwise; non-nil A2 requests one source-5 row. | 0 values. |
| 31 | `setDummyItem` | 2 | `root/proto30 @20415` | 2495-2809 | Passes fixed slot-row defaults: `name` and `stack` are empty strings; catalog, quality, icon, itemKind, rare, ex, equipment, life, skills, compatibility, ranks, generated bn/bv/bh/bn5 keys, stack/reward/materia counts are literal 0; `nameStyle` is `TBL_null`; visibility values are `polmax/mpvisible/mcvisible="Hidden"` and `mivisible="Collapsed"`. Generated keys are `bn1i/bv1i/bh1i` and `bn3i/bv3i` for i=1..3, and `bn5pi/bn5vi` for i=1..32. | 0 values. |
| 32 | `setReadyItem` | 3 | `root/proto31 @22191` | 2812-2843 | Passes A2 through `createVirtualItem`, requests `setItemToXml(8,A1,0,0,6,virtual,true)`, then requests a list-8 update; calls are attempts, not proof of a created/accepted item. | 0 values; no parent or `setSlotData` call. |
| 33 | `setSlotItem` | 2 | `root/proto32 @22484` | 2846-2956 | Fresh-reads `chosenPackage/chosenItem`, gets package/item/name data, requests `setItemToXml` for list 8 row A1/source 1, then branches only on `_isStackable()==true` exactly (numeric 1 does not match); stackMax forwards all `_getMaxStack` results after its fixed setter prefix. | 0 values. |
| 34 | `findItemSetSlot` | 3 | `root/proto33 @23266` | 2959-3109 | A2=0 takes a bare 0-value return; otherwise PC22 captures exactly three results from `getBagItemDataWithQuality`, compares result 1 to A2 and pass to result 3, and requires operation result exact `true`; matched row/set/stack/parent/update calls must complete before true. The four native outputs are captured inside the bag helper, not here. | 0 values for A2=0; 1 false for no match; 1 true only after normal completion of the matched path; parent request is optional, but a no-parent `getSameItemNum` 0-value result can make later `updateStackPrint` subtraction fail before true. |
| 35 | `getBagItemDataWithQuality` | 2 | `root/proto34 @24247` | 3112-3147 | Captures four `getPlayerItemInPackage` results, tests result 3 for exact false, replaces result 4 with 1 only then, and reads name index. | 3 values: `0,0,0` when item missing, otherwise native result 1, native result 4 (or 1 after exact-false normalization), and name index. |
| 36 | `displayHelp` | 2 | `root/proto35 @24535` | 3150-3164 | Requests `Grid_MateriaEquipList` hidden and `TAILCALL`s `setText(TextBlock_Help,A1)`. | Dynamic `setText` result width. |
| 37 | `displayFocusedItemHelp` | 1 | `root/proto36 @24694` | 3167-3462 | Upper-bound index or edit mode 4 branches false; there is no nonnegative-index guard before item lookup; otherwise detail calls and optional materia requests proceed. | 1 boolean: false on those guards, true only after normal local detail completion. |
| 38 | `previousSequence` | 1 | `root/proto37 @26555` | 3465-3526 | Saves sort; normal/repair step <=1 calls `gotoParent(true)` then returns true; step 2 changes to step 1 and refreshes; mode 415 step <=1 calls `gotoParent()` then returns true. | 1 true on handled transitions; 1 false for normal/repair unsupported step; otherwise 0 values. |
| 39 | `isOperateButtonEnable` | 3 | `root/proto38 @26959` | 3529-3608 | Rejects empty/focusless rows, A2 at/above item count, missing/equipped items, list ids other than 1/8, or equal stack count against the first selected `getSameItemNum` result; no A2<0 guard exists, and equipping uses truthiness while caller acceptance uses exact true. Without a parent, the helper may return zero values, padding the compared result to nil; no parent/count is established. | 1 boolean on normal completion. |
| 40 | `processUICommandOperate` | 5 | `root/proto39 @27553` | 3611-3672 | `recipeopen==true` or chosen-operation nonzero guards take bare return; Back/EditBack route previous or parent; EditCommand removes/sets, clears selection, and returns parent continuation; SortStatus calls `operateSort`. | Guards and sort are 0 values; handled Back/EditBack/EditCommand `TAILCALL` dynamic callee widths. |
| 41 | `processUICommandCancel` | 5 | `root/proto40 @28109` | 3675-3711 | `recipeopen==true`, keyboard focus string `"0"`, or chosen-operation nonzero guards take bare return; mode 2 returns parent; otherwise clears common timer then returns previous sequence. | Guards are 0 values; handled path `TAILCALL`s `gotoParent` or `previousSequence` with dynamic widths. |
| 42 | `processUICommandClose` | 5 | `root/proto41 @28456` | 3714-3723 | Calls `setCommonTimer(nil)` only. | 0 values. |
| 43 | `processUICommandSelection` | 5 | `root/proto42 @28536` | 3726-3814 | Guards exact recipeopen/chosenOperation/keyboard results, stores focus=A3/listbox=A4, requests display without forwarding its result, then non-415 requires exact-true operation before requesting setItem; mode 415 only assigns operation/selection/input when the dynamic parent is non-nil. | Every path is 0 values; this method has no mouse/timer/tab dispatcher. |
| 44 | `processUICommandDefault` | 6 | `root/proto43 @29192` | 3817-3945 | Guards exact recipeopen/chosenOperation/keyboard results; mouse/anchor requires `A5 ~= nil`, `A4 ~= nil`, and `A4 < 0` false before timer .2 (NaN passes the actual LT-false predicate); TabChanged may dereference an unguarded parent for list 4, appends all Header results after setText's fixed prefix, and tailcalls display; ButtonFocused requests both Back properties true; number/previous/next call their helpers. | TabChanged `TAILCALL`s `updateWindowDisplay(true)`; all other branches are 0 values. |
| 45 | `processTimer` | 1 | `root/proto44 @30465` | 3948-4001 | Stores converted index only when `0 <= focusToIndex` result; step exactly 1 refreshes, step exactly 0 sets step 1 and refreshes, while unsupported steps reach reachable PC32 before Back properties. | 0 values on normal completion. |
| 46 | `catalogSkip` | 2 | `root/proto45 @30908` | 4004-4107 | Empty list returns; unsorted list or sorttype 0 adds `10*A1`; sorted scan advances by iteration count times A1 on the first changed key or reaches last/zero endpoint, then clamps. | 0 values. |
| 47 | `selectedBorder` | 3 | `root/proto46 @31567` | 4110-4166 | A1 nonnil (including numeric 0) requests visibility for current `work.index`, not A1; only exact-false A2 selects Collapsed, while nil/0/true A2 select Visible; A1 nil with selected=-1 and nil A2 is a bare return, else requests all rows collapsed. | 0 values. |
| 48 | `updateNumber` | 3 | `root/proto47 @31997` | 4169-4194 | Stores `num1` or `num2` only when the named control's `IsKeyboardFocusWithin` result is exact `true`; numeric 1 does not satisfy this Lua equality. | 0 values. |
| 49 | `updateStackPrint` | 1 | `root/proto48 @32274` | 4197-4298 | Iterates package-1 rows and stops only when `isExistItem` is exact false; subtracts parent count, requests hidden visibility for zero remainder, tests row `stackable` against numeric 1 exactly, and requests text id 225 only on that exact value. | 0 values. |
| 50 | `updateStackPrintRepairItem` | 5 | `root/proto49 @32996` | 4301-4342 | Reads the item; hidden visibility requires exact true from `isRepairable` or `isEquipment`, other normal results request visible visibility, and missing items are untouched. | 0 values. |
| 51 | `gotoParent` | 2 | `root/proto50 @33279` | 4345-4396 | Nil parent takes a bare 0-value return; with parent, mode 415/no operation requests `setRecipeIndex(0,listbox)`, then local mode 0/recipeclosed/modal false, parent focus, optional slot help, and `returnFocus`. | 0 values without parent; otherwise `TAILCALL`s dynamic parent `returnFocus` result. |
| 52 | `setItem` | 1 | `root/proto51 @33744` | 4399-4420 | If parent exists, calls dynamic `parent.setSlotItem(chosenPackage,chosenItem,num1)`; then calls dynamic `updateStackPrint` even without a parent. These are requests, not achieved stack refresh. | 0 values. |
| 53 | `removeItem` | 1 | `root/proto52 @33961` | 4423-4438 | If parent exists, calls dynamic `parent.clearMaterialSlot`; then calls dynamic `updateStackPrint` even without a parent. These are requests, not achieved stack refresh. | 0 values. |
| 54 | `getEmptySlotNum` | 1 | `root/proto53 @34105` | 4441-4453 | Parent present `TAILCALL`s `countEmptySlot`; no parent falls through. | Dynamic parent result width or 0 values. |
| 55 | `getSameItemNum` | 3 | `root/proto54 @34220` | 4456-4470 | Parent present `TAILCALL`s `countMaterialInSlot(A1,A2)`; no parent falls through. | Dynamic parent result width or 0 values. |
| 56 | `updatePlayerItem` | 3 | `root/proto55 @34348` | 4473-4538 | Selector 0 stores updatecount; 1/100 rebuild lists 1/2; 101/8/5 skip list rebuild; the updateListProperty call appends all `getListPropertyName` results after its fixed receiver prefix; counter drain refreshes list/focus/stack/bag as selected. | 0 values. |
| 57 | `displayLeftButtonHelp` | 3 | `root/proto56 @34909` | 4541-4578 | Sets step 0/edit mode 4, clears detail flags/page, requests grid 2 and title/help, and requests materia list hidden. | 0 values. |
| 58 | `displayLeftItemHelp` | 2 | `root/proto57 @35331` | 4581-4683 | Mode 415 returns false; otherwise sets step 1/list 8/edit mode 3/index A1, chooses title 3047/3031, requests detail, and special-cases row 0. | 1 false for mode 415; otherwise 0 values. |
| 59 | `openItemList` | 1 | `root/proto58 @36244` | 4686-4769 | Chooses mode 410/411, edit mode 1, step 1, tabs 1/2 visible, list 1/index 0, clears selection/chosen operation/recipe flag, and requests input enabled. | 0 values. |
| 60 | `removeItemOperate` | 2 | `root/proto59 @36997` | 4772-4831 | Mode 415 returns false; otherwise chooses mode 410/411, list 8/index A1+8, edit mode 2/step 2, grid 7, requests edit-command enable/focus and title. | 1 false for mode 415; otherwise 0 values. |
| 61 | `getSlotIcon` | 2 | `root/proto60 @37554` | 4834-4848 | Calls dynamic `getListPropertyName(8)`, passes its first result to `getListProperty`, and tailcalls `getListProperty(firstResult,A1,"icon")`; no unconditional `SlotItem_Maker` identity is proved. | `TAILCALL` dynamic `getListProperty` result width. |
| 62 | `openRecipe` | 1 | `root/proto61 @37699` | 4851-4857 | Sets `recipeopen=true`. | 0 values. |
| 63 | `closeRecipe` | 1 | `root/proto62 @37779` | 4860-4866 | Sets `recipeopen=false`. | 0 values. |
| 64 | `openRecipeList` | 2 | `root/proto63 @37859` | 4869-5039 | Nil A1 requests modal/focus, sets local mode 415/edit 5/list 5, requests tabs 1-4 hidden and tab 5 selected, and chooses empty grid 8/help 3082 or populated grid 9; non-nil requests a refresh and focus to this widget. | 0 values. |
| 65 | `openHistoryList` | 4 | `root/proto64 @39100` | 5042-5251 | Nil A1 requests modal/focus, sets mode 415/edit 5/list A2 with focus/index 0 and tabs 3/4; non-nil restores/clears A3. Its title setter has a fixed prefix plus all Header results; recipeopen true calls `_getParentWidget` at PC138, which may normally return nil, then PC139 performs an unguarded child-method lookup; a nonnil child receives focus/input-disabled requests and a nil child receives none. Recipeopen not exact true requests self focus/input true and clears recipeopen. | 0 values on normal completion; a nil parent result can fail at the subsequent unguarded PC139 lookup. |
| 66 | `focusRecipeList` | 1 | `root/proto65 @40560` | 5254-5262 | Calls `updateWindowDisplay(true)`. | 0 values. |
| 67 | `closeRecipeDetail` | 1 | `root/proto66 @40641` | 5265-5276 | Calls `selectedBorder()` then `updateWindowDisplay(true)`. | 0 values. |
| 68 | `syncItemWork` | 2 | `root/proto67 @40750` | 5279-5282 | Empty synchronization hook. | 0 values. |
| 69 | `operateSort` | 2 | `root/proto68 @40794` | 5285-5334 | Cycles/sets sort only when listbox=1, re-applies rows, and converts index/focus with strict -1<result and 0<=result guards before writing. | 1 boolean `true` at PC39 on reachable normal completion; opaque conversion results can prevent completion. |
| 70 | `displaySortType` | 2 | `root/proto69 @41182` | 5337-5348 | Forwards sort type, receiver, and `Button_SortStatus` to desktop display. | 0 values. |
| 71 | `changeSortType` | 1 | `root/proto70 @41313` | 5351-5363 | Stores the result of dynamic `desktopWidget.changeSortType(work.sorttype)`. | 0 values. |
| 72 | `saveSortType` | 1 | `root/proto71 @41448` | 5366-5376 | Forwards current sort type to dynamic desktop persistence. | 0 values. |

## Selected decoded branch locators

These zero-based decoded PCs and byte offsets anchor the consequential branch
and dynamic-call claims above without reproducing method bodies. The prototype
offset and LF window in the complete matrix remain the coverage locator for
every other method.

| method | decoded PC@byte offset | locator use |
|---|---|---|
| `getFormName` | `1@2588; 2@2592` | reachable one-string return and unreachable 0-value epilogue |
| `setInitialData` | `3@5655; 88@5995` | repair-mode selection and list initialization branch |
| `setNumberInput` | `4@6543; 8@6559; 12@6575` | distinct Minimum, setMaximum, and setValue calls |
| `updateWindowDisplay` | `1@7264; 2@7268; 17@7328; 18@7332; 43@7432; 44@7436; 52@7468; 53@7472; 55@7480; 59@7496` | edit-mode reads1/43/52 and comparisons2/44/53; mode read17/compare18; final A1 gate and zero-result return |
| `updateListFocus` | `2@7755; 5@7767; 32@7875; 35@7887; 36@7891; 51@7951; 54@7963; 58@7979; 235@8687` | list-8 false return, empty-arm write/request sequence, and convergent true return |
| `setGridVisibility` | `32@9805; 36@9821; 41@9841; 50@9877; 118@10149; 145@10257` | sort-status true/false request branches, detail-grid predicate, and list-5 collapse |
| `setWindowFocus` | `8@11035; 9@11039; 10@11043; 12@11051; 14@11059` | dynamic keyboard-getter call, self-equality gate, and conditional keyboard-control request |
| `getSelectedTab` | `0@12095; 2@12103; 3@12107; 4@12111` | dynamic selected-index call, +1 arithmetic, and one-value return |
| `getListBoxFocusNum` | `2@12660; 6@12676; 12@12700; 16@12716; 17@12720; 18@12724; 19@12728; 20@12732; 21@12736; 23@12744; 28@12764` | independent item-count zero arm, FilteredCount K read, empty four-zero return, two fresh `work.focus` chains (field reads at PCs 18 and 20), strict K/F2 comparison, local F1 replacement, and four-value return |
| `getListBoxItemNum` | `3@12545; 4@12549` | fixed receiver prefix, all property-name results, and dynamic count tailcall |
| `focusToIndex` | `6@12966; 8@12974; 21@13026` | empty/upper guard, lower-bound omission, and dynamic tailcall |
| `indexToFocus` | `28@13335` | exact one-value opaque return |
| `setItemToXml` | `8@14608; 65@14836; 154@15192; 158@15208; 163@15228; 249@15572` | source selector, nonnil-versus-nil A6 split, player fallback, nil resolved-item return, and final row-result branch |
| `setItemToXmlLight` | `8@16348; 17@16384; 39@16472; 95@16696; 107@16744; 112@16764` | package/index guard, repair catalog gate, focus comparison at PC107, and true return at PC112 |
| `makeListFromPackage` | `4@18584; 79@18884; 150@19168; 158@19200; 169@19244; 187@19316` | package rebuild/update/delete selector branches and affected missing-item last-row deletion |
| `setDummyItem` | `102@20823; 133@20947; 143@20987; 164@21071; 168@21087; 189@21171; 268@21487` | bn1/bv1/bh1 and bn3/bv3 loop ranges 1..3, bn5p/bn5v loop range 1..32, fixed defaults, and update request |
| `setReadyItem` | `2@22199; 8@22223; 18@22263` | virtual-item request and source-6 row request |
| `setSlotItem` | `12@22532; 20@22564; 31@22608; 34@22620; 47@22672; 88@22836` | fresh-read chain, row A1/source-1 request, exact-true stackability branch, all-value max-stack forwarding, and row update request |
| `findItemSetSlot` | `0@23266; 22@23354; 31@23390; 56@23490; 59@23502; 115@23726; 126@23770` | zero-value guard, three-result helper match gate, exact-true operation/stackability gates, parent request, and result |
| `getBagItemDataWithQuality` | `4@24263; 20@24327; 26@24351` | four-value native capture, exact-false normalization, and three-value return |
| `isOperateButtonEnable` | `6@26983; 21@27043; 44@27135; 67@27227` | empty/range/item/list/stack eligibility gates |
| `processUICommandOperate` | `2@27561; 21@27637; 36@27697; 54@27769` | guard, command dispatch, and dynamic continuation |
| `processUICommandCancel` | `2@28117; 12@28157; 26@28213` | guard, edit-mode split, and dynamic continuation |
| `processUICommandSelection` | `2@28544; 13@28588; 23@28628; 33@28668; 49@28732; 58@28768` | recipe/keyboard guards, ignored display call, non-415 exact-true operation gate, and mode-415 parent selection path |
| `processUICommandDefault` | `13@29244; 21@29276; 24@29288; 26@29296; 35@29332; 57@29420; 75@29492; 76@29496; 81@29516; 86@29536; 89@29548; 98@29584; 103@29604; 122@29680` | event guard, exact mouse nil/LT predicates, unguarded list-4 parent, dynamic Header title prefix/tail, both Back property writes, tab continuation, ButtonFocused properties, and skip dispatch |
| `processTimer` | `6@30489; 16@30529; 24@30561; 32@30593` | focus conversion, step refresh split, and reachable unsupported-step 0-value return |
| `catalogSkip` | `7@30936; 15@30968; 20@30988; 22@30996; 52@31116; 66@31172; 68@31180; 71@31192; 73@31200; 79@31224; 83@31240` | empty/list/sort branches, unsorted 10*A1 path, iteration*A1 changed-key path, end-point scan, and clamped result |
| `selectedBorder` | `4@31583; 7@31595; 24@31663` | selected-row, clear-selection, and collapse-all paths |
| `updateNumber` | `0@31997; 6@32021; 11@32041; 17@32065` | control split and exact-true focus predicates |
| `updateStackPrint` | `19@32350; 39@32430; 40@32434; 65@32534` | exact-false stop predicate, dynamic parent count call/subtraction, and exact numeric-1 stackable test |
| `gotoParent` | `2@33287; 10@33319; 35@33419; 40@33439` | parent guard, recipe-index request, and dynamic returnFocus |
| `updatePlayerItem` | `1@34352; 7@34376; 15@34408; 42@34516; 49@34544; 50@34548` | selector/rebuild and update-counter branches plus dynamic update-list prefix/tail |
| `openRecipeList` | `2@37867; 83@38191; 92@38227` | nil/non-nil entry, empty/populated grid split |
| `openHistoryList` | `0@39100; 80@39420; 81@39424; 87@39448; 114@39556; 135@39640; 138@39652; 139@39656; 141@39664` | nil entry, dynamic Header title prefix/tail, history selection, recipeopen branch, parent call that may return nil, unguarded child lookup, and child-nil split |
| `operateSort` | `0@40794; 30@40914; 39@40950` | work.listbox read at PC0, strict conversion guards, and reachable true return at PC39 |

## Work proxy and cross-method composition

The `_temp` declaration and subsequent `work` `SETTABLE`/`GETTABLE` operands
are script-level declarations, assignments, and current reads. They do not by
themselves establish a native type value, storage application, or readback.
The native workproxy boundary states that work members are per-instance cached
userdata, `_temp` declares the own scope, undeclared reads yield nil, and
undeclared writes have no store; its lifetime and destruction joins remain
native questions (`xivl-decomp:docs/script/widget-work-members.md:297-328`,
`:361-390`, `:486-506`).

`init` explicitly writes only the fields named in the startup section. Later
getters must therefore be read from their own operands. For example,
`setReadyItem` requests virtual-row construction without setting a parent slot, while
`setSlotItem` later fresh-reads `chosenPackage` and `chosenItem`; the setter
does not prove that a later getter preserves a catalog, package, or item
identity.

The following compositions are dynamically selected at runtime and preserve
only the result width shown in the matrix:

- `getListBoxItemNum`, `displayHelp`, and `getSlotIcon` tailcall dynamic/native
  methods, so their result values and widths remain callee-defined.
- `getEmptySlotNum` and `getSameItemNum` tailcall dynamic parent methods; a
  missing parent takes a bare return with 0 values.
- `gotoParent` clears local mode/modal state, then tailcalls the selected
  parent's `returnFocus`; a missing parent takes 0 values.
- `processUICommandOperate` and `processUICommandCancel` tailcall
  `previousSequence` or `gotoParent` only on their handled branches; guards and
  non-tail branches return 0 values.
- `findItemSetSlot` requests dynamic parent `setSlotData` only after its local
  row match and operation gate; `setItem` and `removeItem` request parent slot
  methods but always return 0 values.

These calls are operands and requests. A setter does not prove native storage,
a row writer does not prove rendered UI, a focus/input call does not prove
focus ownership, and a child lookup does not prove child creation, dispatch,
or destruction.

Every composed behavior and result in this contract is conditional on the
actual runtime binding selected for each dynamic call, including a self-method
lookup, and on normal completion of each ordinary call or `TAILCALL`. The
matrix records the Lua operands, branch predicates, local writes, and requested
property/UI effects; it does not promote an unselected helper's behavior or a
requested work/property write into achieved storage, rendering, or ownership.

## Detailed list, package, and material behavior

List ids map to `TabItem_1_Maker` through `TabItem_5_Maker`,
`SlotItem_Maker` (8), and `HelpCache_Maker` (9). `getPackageFromList` maps
1->1, 2->100, 3->101, 4->8, default->1. `setInitialData` sets source first
index 0/count 8 for list boxes 3, 4, and 5; it sets list 5's filtered key to
`visibility`, rebuilds packages, and requests dummy rows 0-16 only after the
initial list branch.

`makeListFromPackage` rebuilds list 1 from package 1 using capacity minus free
space and list 2 from package 100 using capacity. Each loop continues only
when `setItemToXmlLight` returns exact `true`; false, nil, or numeric 0 stop
the loop. Stale rows are requested for deletion and the property is updated.
An affected package/index requests an update or deletion for one row only for package 1 or
100; a missing item deletes the current last row (`count-1`). Package 101 and
unsupported selectors do not perform that list-row update.

`setItemToXml` source selectors are literal: 5 requests a virtual item from A4,
6 uses A6 and returns false for nil without an item lookup; 2 requests
bazaar data, 3 requests shop info then requests a virtual item. Only the
default selector path tests A6 at PC154, uses any nonnil value including
false, and selects a player lookup for nil. Its formal arity is 7 including the receiver,
although some callsites supply a trailing boolean that this body does not
read. `setItemToXmlLight` has formal arity 6 including the receiver; some
callsites supply trailing operands that this body does not read. It rejects
non-positive package/index, requests hidden repair-row visibility outside the
inclusive catalog range 10013001-10013005, uses list sort operands 11/12/91 as
selected by list, and returns true even when visibility is false. Its
focus-change comparison is at PC107 (`16744`), while the reachable true return
is PC112 (`16764`).

`setDummyItem` passes literal zero to catalog, quality, icon, itemKind, rare,
ex, isEquipment, itemlife, lifemax, mskill1/2, compati, eqrank, eqrankType,
`bn1`/`bv1`/`bh1` suffix keys for loop values 1..3, `bn3`/`bv3` suffix keys
for 1..3, `bn5p`/`bn5v` suffix keys for 1..32, and stack/reward/materia count
operands. The `name` and `stack` values are empty strings, not count values;
`nameStyle` is `TBL_null`, `polmax`/`mpvisible`/`mcvisible` are `Hidden`, and
`mivisible` is `Collapsed`; then it requests the list-property update. These
are setter operands, not native type, storage, or display guarantees.

The explicit currency map is:

`1000001->1`, `1000102->2`, `1000101->3`, `1000103->4`, `1000107->5`,
`1000106->6`, `1000104/1000108/1000109/1000105->-1`, `1000111->11`,
`1000110->12`, `1000112->-1`, `1000113->14`, `1000114->15`,
`1000115->16`, `1000116->17`, `1000117->18`, `1000118->19`,
`1000119->20`, `1000120->21`, `1000121->22`, `1000122->23`,
`1000123->24`; all other ids return -1.

The only caller continuation used here is the published fact at
`xivl-client-scripts:docs/local-guildleve-supplies-contract.md:132-134`:
the caller forwards unchanged slot/value pairs to `setReadyItem` and
`findItemSetSlot`. This does not establish the supplied value's catalog or
package identity. `setReadyItem(slot,value)` requests `createVirtualItem(value)`
and passes its result to the list-8 row setter through source 6 with
package/index 0/0, then requests a list update; it does not call a parent or
`setSlotData`.

`findItemSetSlot(slot,value)` takes 0 values when value is 0. Otherwise it
scans package 1 to native capacity over outer passes 1 through 4; its PC22
call captures exactly three helper results, compares the first and third
outputs of `getBagItemDataWithQuality` as shown in the matrix, and requires
`isOperateButtonEnable(1,index-1) == true` exactly. The four native outputs
are captured inside `getBagItemDataWithQuality`, not at this call. A
match reads the item again, passes row `slot+8` operands to the row setter, branches on
`_isStackable() == true` exactly (numeric 1 does not match), passes stack
count/max/stackable/text to setters, requests a list update, requests parent
`setSlotData(slot,1,index)`
when non-nil, calls `updateStackPrint`, and returns true only after the normal
local path completes; no match returns false. The `updateStackPrint` call is a
request and does not prove achieved stack refresh. With no parent, the later
`updateStackPrint` call can subtract a missing `getSameItemNum` result before
the true return. The native outputs are not
assigned catalog, package, or quality identities.

`isOperateButtonEnable` eligibility is explicit: there must be a nonempty
focusable list and an index below the item count (there is no negative-index
guard); the mapped package must be 1, 100, or 101; the player item must exist
and `_isEquipping` must be falsy; the list must be 1 or 8; and the row's
`stackCount` must differ from the first selected dynamic
`countMaterialInSlot(package,index)` result through `getSameItemNum`. A
no-parent helper can return zero values, padding that selected result to nil;
the code does not require an actual parent or count. Any failed gate returns
false; the final accumulated boolean is returned otherwise.
`findItemSetSlot` accepts it only with exact `true`.

`setSlotItem` fresh-reads selected package/index, requests row A1 in list 8
through source 1, and enters its stack branch only when `_isStackable() == true`
exactly (numeric 1 does not match). That branch passes count 1, forwards all
`_getMaxStack` results after the fixed `stackMax` setter prefix, and passes
stack text `"1"`; non-stackable
rows get max 1, stackable 0, and empty stack text. `setItem` requests dynamic
parent `setSlotItem(chosenPackage,chosenItem,num1)` and then calls dynamic
`updateStackPrint`; `removeItem` requests `clearMaterialSlot` and then calls
dynamic `updateStackPrint`. These are requests, not achieved stack refresh.
`getEmptySlotNum` and `getSameItemNum` tailcall parent count methods or return
0 values without a parent.

## Recipe, history, selection, sorting, and close behavior

`openRecipe` and `closeRecipe` only write `recipeopen` true/false. A nil
`openRecipeList` entry requests modal/focus state, sets local mode 415/edit mode
5/list 5, requests tabs 1-4 hidden and tab 5 selected, and chooses empty grid
8/help 3082 or populated grid 9. Its non-nil entry requests a refresh and focus
to this widget. A nil `openHistoryList` entry requests modal/focus state, sets mode
415/edit mode 5/list A2 with focus/index 0, shows tabs 3/4, and requests Back
for an empty list; its non-nil entry uses A3=0 to clear selection or A3-1 to
restore index/focus. When `recipeopen`, it asks `_getParentWidget` for a
dynamic parent; when `recipeopen == true`, PC138 may normally return nil but
PC139 then performs an unguarded `isRecipeWidgetOpen` member lookup. A non-nil
child receives focus/input-false requests and a nil child receives no
focus/input request. Only the `recipeopen ~= true` path requests self focus/input true
and clears `recipeopen`. These are requests, not proof of child creation or
destruction.

`processUICommandSelection` first requires `recipeopen` not exact `true`,
`chosenOperation == 0`, and a keyboard result other than exact `false` (nil
therefore proceeds). It stores `focus=A3` and `listbox=A4`, calls
`updateWindowDisplay(true)` without forwarding a result, and has no
mouse/timer/tab dispatcher. In non-415 mode, it calls
`isOperateButtonEnable`; only exact `true` calls `setItem` and refreshes
display. In mode 415 with no operation it asks the dynamic parent for
`setRecipeIndex(index+1,listbox)` and only when that parent is non-nil writes
`chosenOperation`, marks selection, and requests input false. Every path
returns 0 values.

`processUICommandDefault` has the same recipe/operation/keyboard (keyboard
rejects only exact `false`, so nil proceeds) and mouse/anchor guards: A5 must be
non-nil, A4 must be non-nil, and the actual `A4 < 0` predicate must be false
(NaN therefore passes that LT test if supplied). It schedules the 0.2 timer,
handles TabChanged with the
list-4 request/title/Back path, calls `updateNumber` for number changes, and
calls `catalogSkip(-1/+1)` for previous/next. Only TabChanged tailcalls
`updateWindowDisplay(true)`; all other recognized and guard paths return 0
values.

`processTimer` converts filtered focus to source index and writes `index` only
when the result passes `0 <= result`, clears selection, sets page to 0,
refreshes for step 1, or changes step 0 to step 1 and refreshes; unsupported
steps reach the reachable PC32 0-value return before requesting Back focus
properties. `catalogSkip` takes 0 values for no rows, moves by `10*A1` outside
sorted list 1, and for sorted list 1 compares native sort keys until the key
changes, adding iteration count times A1 at the first changed key; an unchanged
scan reaches the positive last-row or nonpositive zero endpoint, then clamps
focus to `[0,count-1]`. `selectedBorder` requests one row Visible or
Collapsed, or requests every row collapsed and stores selected=-1; an already clear
selection with nil arguments takes 0 values. Numeric 0 is nonnil in Lua and
therefore enters the single-row branch; only nil enters the clear-selection
branch. `updateNumber` stores `num1` or
`num2` only when `IsKeyboardFocusWithin == true` exactly; a numeric 1 is not
the same branch value.

Operate rejects an open recipe or nonzero chosen operation. Back/EditBack route
through `previousSequence` or `gotoParent(true)` according to edit mode;
EditCommand requests `removeItem` or `setItem`, clears selection, and tailcalls
`gotoParent(true)`; SortStatus calls `operateSort` and returns 0 values.
Cancel additionally rejects keyboard focus string `"0"`; edit mode 2 tailcalls
`gotoParent(true)`, otherwise it clears the common timer then tailcalls
`previousSequence`. Close only calls `setCommonTimer(nil)` and returns 0
values. `previousSequence` returns true for handled transitions, false for the
normal/repair unsupported step, and 0 values for other unhandled modes.

`gotoParent(returnHelp)` takes 0 values without a parent. In mode 415 with no
operation it requests `setRecipeIndex(0,listbox)`, changes mode to 410 unless
list 5 is active, sets mode 0 and `recipeopen=false`, requests modal false,
requests parent focus, optionally requests `displaySlotItemHelp`, and tailcalls the
selected parent's `returnFocus`. `closeRecipeDetail` clears selection then
refreshes; `focusRecipeList` refreshes; `syncItemWork` has no instructions.

## Native, UI, caller, and server boundaries

The Lua evidence establishes operand positions, local writes, branch polarity,
fresh reads, ordinary calls, tailcalls, and explicit result widths. It does not
establish native return types beyond the width or branch use observed here.
UI setters, list-property writers, parent methods, child lookups, modal/focus/
input requests, and desktop row/detail calls do not prove storage, rendering,
focus ownership, input acceptance, child creation, dispatch, destruction, or
readback.

The caller handoff remains limited to the cited local guildleve-supplies
contract. All other caller bodies, native item/catalog/package implementations,
parent/child storage, and lifetime joins are opaque. The craft progress boundary
at `xivl-client-scripts:docs/craft-command-progress-contracts.md:1-26` excludes
claims of craft success, quality, durability, XP, command eligibility,
inventory debit, reward/supply grant, server acceptance, or settlement. This
contract therefore reports only local UI/list/slot continuation and does not
promote any local true, parent call, or close path into a completed craft.
