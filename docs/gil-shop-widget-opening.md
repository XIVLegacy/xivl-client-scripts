# Gil-shop widget opening

The recovered retail Lua separates opening `Ask/ShopBuyWidget` from waiting
for a purchase selection. `ShopBaseClass.openShopBuy` uses the desktop's
widget-creation yield path; `selectShopBuy` later uses its selection yield
path. These are separate client operations, not one combined user-input wait.

## Evidence identity

This is static analysis of extraction `2012.09.19.0001` for client 1.23b,
not a live timing measurement. The decoded input was hydrated with
`tools/private_lua_corpus.py hydrate` against
`manifests/private_lua_corpus.json`. That manifest pins the archive SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`
and expanded tree SHA-256
`05edcf81aec7ad28007c059991b6858665680f860bd1ed2aa5100e7fc120da0d`.
Direct source hashes matched these `manifests/scripts.json` records:

| Decoded path under `lua/scripts/` | SHA-256 |
|---|---|
| `chara/npc/populace/shop/populaceshopsalesman.lua` | `6685167A1C8120E48F7BD36A2DF783F404F3BEB0BABBC2672A393ECF22416ADA` |
| `chara/npc/populace/shop/shopbaseclass.lua` | `483220C5E7914B2406FC8184B69448980E46004945A7315203406475E52A5C9F` |
| `widget/desktopwidget.lua` | `5D3BFABF2E8A55EE2E64F607BDADA5F04046C9528E9E9ACA858E9AD9E232070A` |
| `widget/desktopwidget_connector.lua` | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| `widget/ask/shopbuywidget.lua` | `032B0C06D57300A810B9953DAD04BF794DEC096360944F4A3683CB2DC9797091` |
| `chara/player/playerbaseclass.lua` | `6226B3FA15DFDBAD279B7DBA453F8A3B76FCB8B68BAD6E14F5403D52987F76E4` |
| `widget/ask/askbaseclass.lua` | `642F3112D4663004FDC0B79DAF0A5FAF8B7588EAD58D2CD8E6747821BDA54ADB` |
| `widget/widgetbaseclass.lua` | `737A53B0472B510440735CF19A1D0A11FD100E69DF7F3EAB1178969A3D57B95C` |

The matching `.calls.json` sidecars identify the decoded/ciphered paths,
classes and native callsites. They are structural indexes; the method flow
below comes from inspecting the manifest-matched decoded bodies.

## Opening and selection boundaries

1. `PopulaceShopSalesman` inherits `ShopBaseClass`
   (`chara/npc/populace/shop/populaceshopsalesman.lua:1-8`).
2. `ShopBaseClass.openShopBuy` defaults a missing currency to 1000001 and
   calls `desktopWidget.openEventModeWidgetYield` with `Ask/ShopBuyWidget`,
   the shop actor, shop ID and currency (`shopbaseclass.lua:87-102`).
3. `openEventModeWidgetYield` calls `openWidgetYield` for widget slot 4 and
   returns success according to the resulting widget
   (`widget/desktopwidget_connector.lua:26175-26196`).
4. `openWidgetYield` attempts the open, waits for widget creation, then
   retrieves the widget. Failed attempts retry while the widget type is
   enabled, using `_wait(0.1)`; `waitWidgetCreateYield` separately polls
   `isCreateWidgetCommandPlaying` with `_wait(0.1)`
   (`desktopwidget_connector.lua:25910-25993`). These are conditional
   polling intervals, not a fixed opening duration.
5. The open routes through `openWidgetLocal` to `commandCreateWidget`
   (`desktopwidget_connector.lua:25077-25183`). The latter and the playing
   query use the local player's widget-command methods with system command
   24228 (`widget/desktopwidget.lua:119-163`). The recovered Lua does not
   establish the native scheduler's completion conditions or runtime cost.
6. `ShopBaseClass.selectShopBuy` subsequently calls
   `selectEventModeWidgetYield`, which initializes the existing event widget,
   waits through `selectWidgetYield`, and obtains `getAskResult`
   (`shopbaseclass.lua:117-133`,
   `desktopwidget_connector.lua:26239-26265`). Opening does not use this
   purchase-selection wait.

## Player widget-command gates

`PlayerBaseClass.commandAboutWidget` reads `_getServerTime`. It rejects a
non-forced request if the nonzero stored `widgetCommandBurstBlocker` is later
than that current value. It then rejects a non-forced request while the
resolved command name is already playing. Otherwise it calls
`_executeCommand` and stores the current time in the blocker
(`chara/player/playerbaseclass.lua:2576-2623`). The recovered body adds no
future cooldown interval. This does not establish how the native server-time
clock behaves during a live session.

`isCommandAboutWidgetPlaying` resolves the command name and forwards the
name and command actor to `_isCommandPlaying` (`:2626-2639`). Thus the
creation-yield loop polls a command predicate; it does not call the shop
widget's item-selection predicate. A retrying open and a command still
playing are distinct possible reasons for the yield to continue.

## Item-list initialization

The shared widget `_onInit` calls `initCommon`, sends the before-Lua-init
command, calls the widget's `init`, sends the after-Lua-init command, then
marks its shared initialized flag
(`widget/widgetbaseclass.lua:114-147`). `AskBaseClass.init` calls `initAsk`
(`widget/ask/askbaseclass.lua:11-48`), and `ShopBuyWidget.initAsk` calls
`setInitialData` (`widget/ask/shopbuywidget.lua:380-419`).

`ShopBuyWidget.setInitialData` obtains the catalog start index and builds its
item list before marking initialization complete and updating the window
(`widget/ask/shopbuywidget.lua:422-576`). `makeShopItemList` loops over the
catalog entries, calls `setItemToXml` for each and updates the list
(`:1464-1515`). The item branch obtains the shop item detail, creates a
virtual item and reads its icon (`:1273-1306`). The shop actor reads
`shopBaseSheet` and `shopItemSheet` with `_loadKeyTemporarily` and `_getData`
(`chara/npc/populace/shop/shopbaseclass.lua:11-54,253-308`). The widget's
`processBeforeShow` returns true (`shopbuywidget.lua:579-589`).

These calls identify client-side initialization work, not a measured
bottleneck or proof that every underlying native operation is local. No
fixed seconds-long wait is recovered in the inspected opening wrappers.
The evidence does not identify frame visibility, resource-loading cost,
command admission delay, or an event-packet acknowledgement timestamp.
The [command boundary](widget-open-command-boundary.md) also records a
known decompiler omission in command 24228; native and bytecode evidence
remain necessary before treating the recovered text as a complete contract.
