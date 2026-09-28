# Market search and bazaar client contracts

`ItemSearchWidget` holds three local selection phases: market, item type, and
item. Selecting a market advances to item-type selection; selecting a type
advances to item selection. The selected values are retained as `market`,
`itemType`, and `itemId` fields. Cancel or Back from item selection returns to
item-type selection, and from item-type selection returns to market selection.
Cancel from the market phase returns base result `-1`; Close also returns
`-1`, and the Back control at the market phase does the same. These are UI
transitions only; by themselves they do not establish a request, search
response, or result set.

`MarketEntrance.eventPushChoiceAreaOrQuest` has two conditional call sites to
`DesktopWidget.askItemSearchWidget()` (`marketentrance.lua:87,95`).
`PopulaceBranchsVendor.eventSearchItemAsk` calls the same method at line 265 on
its `L4_10 == 1` branch (`populacebranchsvendor.lua:252-272`). The desktop
wrapper calls `_waitForItemSearchWidget()` (`desktopwidget_connector.lua:10099-10102`).
`DesktopWidget._waitForItemSearchWidget_inl` returns the pair `"self"` and
`"_waitForItemSearchWidget_cpp"` (`desktopwidget_u.lua:271-277`). These are
static routes in recovered Lua. They do not establish runtime invocation,
widget display, request protocol, response, or results.

`DesktopWidget.orderBazaarWidget` resolves its target actor and, for mode `1`,
opens `BazaarListWidget`. When the target is not the local player, it calls
`updateItemPackage(8)`, waits for the widget, and then calls
`updateBazaarPackage`. `BazaarListWidget.processBeforeShow`, when its first
argument is not `true`, closes the widget if its error flag is true or its
actor is invalid. These calls do not
prove that the package update succeeded, explain the native meaning of `8`,
or establish server request/response behavior.

| Decoded script | Canonical source SHA-256 | Reviewed decompile output SHA-256 | LPB and decoded-payload identity |
| --- | --- | --- | --- |
| `lua/scripts/widget/ask/itemsearchwidget.lua` | `a14b0b34b68f950836be5121c28f4b2b13689ec27be0496e253886b1165c6b54` | `c140bce77345ff120e18449a78f826f389d723eb8c872ac7763a7a433c1423bb` | `n1635q/9rz/1q5xr59s72n1635q.le.lpb`; LPB SHA-256 `2a3b496d7c16dea9c78e4310701268c9aa5097a36e72a1133788129ce577e9b9`; decoded payload SHA-256 `dd3ce6a7f7be1b5bf5939c961bce525337201635c2b4256602119cd1d9638522` |
| `lua/scripts/widget/desktopwidget_connector.lua` | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` | `c5480f97a81c08f8640b4d250c0e20694b2a697c4dc9b1e0d343a230c8cbcbe0` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`; LPB SHA-256 `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425`; decoded payload SHA-256 `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `lua/scripts/chara/npc/object/marketentrance.lua` | `8ac0df4222607df27e0da33afb187ce8b0906d572b936d9620f3446e2f6ba5a1` | `86a5f936578a813276272fa48069c58a23153834ef6d3787edd24dc35aa24018` | `729s9/wu7/v8057q/x9sz5q5wqs9w75.le.lpb`; LPB SHA-256 `9dd189aba6d613b21f6019928b9c6e7d53ff5d7db2542d01ebc769972781db30`; decoded payload SHA-256 `f2d08b15cadf12a03fc180898a2e63efa2f1343a991379561586b93c4f586100` |
| `lua/scripts/chara/npc/populace/populacebranchsvendor.lua` | `7e9970c0ba2e4a351310f87f843195ca3e237fdd601e94537bb07c2d08416b95` | `b62f930ed13adf24696149e4a9c25bc7408b0d1c0710c5121f813199c87dc7af` | `729s9/wu7/uvupy975/uvupy9758s9w72ro5w6vs.le.lpb`; LPB SHA-256 `99dfef67c9b400f993fa9b30483338b977205c54bb6e2ac3cada86d8d66716a5`; decoded payload SHA-256 `5a4f4ed579c89ab9df6f28c4b0b194d95c8c496fe2373b990a2257115ecc3542` |
| `lua/scripts/widget/desktopwidget_u.lua` | `d5c6c1ca8ef11d7238f00f46280d3a5d48bc91a3261e9de407b21347f03a768b` | `395efd54dfba90073c1b57ebd2138a77aae379721e57216ab78f107719dcec93` | `n1635q/65rzqvun1635q_p.le.lpb`; LPB SHA-256 `ba43cd71b0c5a36a74ff947a6bd00c2b7bfe3942be85b72dec504ff848fd5b22`; decoded payload SHA-256 `ce7cbc20ea49771cccb4066980ed42afdf4ac088e8bb776f143ef75e6f25cb58` |
| `lua/scripts/widget/bazaarlistwidget.lua` | `f539b71353ee2860f535bc962ca2038ecf51bf99fdbeca314ed1eaa20bc39164` | `80da3448e2bfd19aef03356ad308d75153fc90278bdc8cfeeb58891a4f5593ba` | `n1635q/89k99sy1rqn1635q.le.lpb`; LPB SHA-256 `8911334e4b425343fa491a3170c38fe6982449104eaea8f0c88860c97bd17a95`; decoded payload SHA-256 `ca5cbcbeca34331a7e1c9ef411d7dca5ebe75c0d13c91dcbeaec9a7921571ce7` |

Source locators in the reviewed decompile outputs:

- `ItemSearchWidget` phases and cancel/Back behavior (`itemsearchwidget.lua:21-40,85-171`).
- Market caller branches (`marketentrance.lua:87,95`) and vendor caller branch (`populacebranchsvendor.lua:252-272`).
- Search wrapper and bridge-name mapping (`desktopwidget_connector.lua:10099-10102`; `desktopwidget_u.lua:271-277`).
- Bazaar target and package call (`desktopwidget_connector.lua:5063-5093`).
- Invalid-target/error close (`bazaarlistwidget.lua:153-157`).

Output hashes pin these line locators. Canonical source hashes are pinned in
`manifests/scripts.json`; LPB identities and decoded payload hashes are pinned
in `manifests/retail_lua_coverage.json`.
