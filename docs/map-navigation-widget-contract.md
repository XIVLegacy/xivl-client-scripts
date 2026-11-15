# Map navigation widget contract

`MapNavigationWidget` is the script half of the full map window. This page
records the conditions its `init` registers, its menu rows, how it answers
`Operate` and `Cancel` on a row, the region list, and its two zoom methods.
The form, its key bindings and the native zoom commands are recorded in
`xivl-decomp:docs/resource/minimap-base-tiles.md`, "Installed navigation
form" and "Zoom commands". Native map drawing and server behavior are
outside this page.

## Source identity

The input is one installed resource of client extraction `2012.09.19.0001`,
authenticated against the
[coverage manifest](../manifests/retail_lua_coverage.json).

| Decoded path under `lua/scripts/` | Installed resource under `client/script/` | Wrapper bytes | Decoded bytes / SHA-256 |
| --- | --- | ---: | --- |
| `widget/mapnavigationwidget.lua` | `n1635q/x9uw9o139q1vwn1635q.le.lpb` | 15740 | 15727 / `21cc7f2f9c6e2a56e02620e18748fa9dd70bf02dab6a889fd6083826d60528c2` |

`tools/retail_script.py` decoded the LPB and ran the pinned unluac. The
statements below are read from that decompiled body. PCs are not counted
here.

## Initialization

The script defines `MapNavigationWidget` on `WidgetBaseClass`. `init`
requests, in order:

- `setModal(true)`
- `setUICommandCondition("UILuaCommands.Activated")` and
  `setUICommandCondition("MapScreenControl.NaviRowUpdated")`
- `setTemplateConfirmCondition` and `setTemplateCancelCondition`, each with
  `"ControlTemplate_ListBoxItem_MenuItem"` and `"Button_MenuItem"`
- `initMenuList`

`initMenuList` adds 30 items to `ListBox_NavigationMenu` from the template
`ControlTemplate_ListBoxItem_MenuItem`, named `Item_Menu_1` to
`Item_Menu_30` by `getMenuItemName`, and sets each item's `Focusable` false
and `Visibility` `"Visible"`. `focusMenuListItem(n)` requests
`_setKeyboardFocusedControl("Item_Menu_" .. n, "Button_MenuItem")`.

## Row commands

`processUICommandEvent` receives the control name and the command:

- `UILuaCommands.Operate` on `Button_MarkerItem` passes
  `getTemplateUserWorkInt(1, item)` to `dispMarker`
- `UILuaCommands.Operate` on another control reads `IntData.Value0` of the
  row's `TextBlock_MenuItemName` and passes it to the callback of the current
  menu category: 1 `callbackTopMenuList`, 2 `callbackSelectRegionMenuList`,
  3 `callbackSelectPieceMenuList`
- `UILuaCommands.Cancel` on `Button_MenuItem` reads
  `getMenuCategoryPrevious`. A negative value requests
  `desktopWidget:closeWidgetDirect(self)`, and any other value
  `setMenuCategory(previous)`
- `UILuaCommands.MapClose` has an empty arm

No statement of this script names `UILuaCommands.EventMapNavigationClose`,
the command the window template sends on `MouseLeftButtonDown`.

## Top menu

`setTopMenuList` (title text 5205) sets the previous category to -1 and
requests `clearMenuListItem(1)`. That method calls
`setMenuListItemText(i, nil, "")` and `setMenuListItemData(i, -1, -1)` for
rows 1 to 30, and `setMenuListItemText` with an empty text sets the row's
`Visibility` to `"Collapsed"`. The method then fills rows by mode:

| Mode | Rows written |
| ---: | --- |
| 0 | row 1: text 5206, data 2, help 0, then row 2: text 1318, data -1, help 77309 |
| 1 | row 8: text 1318, data -1, help 77309 |
| other | row 1: text 1318, data -1, help 77309 |

In every mode it ends with `focusMenuListItem(1)`. In mode 1 row 1 is a
row the clear collapsed, so the keyboard focus request names a collapsed
item.

`callbackTopMenuList(row)` reads the row datum. In mode 1 a datum of 0 or
more is passed to `dispMarker`, and in other modes it is passed to
`setMenuCategory`. A negative datum requests
`desktopWidget:closeWidgetDirect(self)` in every mode. The `Cancel` arm of
`processUICommandEvent` above closes the widget for the previous category
-1 that this list sets.

What the native list does with a focus request on a collapsed item, and
which code fills rows 1 to 7 in mode 1, are outside this script.

| Method | Prototype / code start |
| --- | --- |
| `setMenuListItemText` | `root/proto14` / `0x1AF4` |
| `clearMenuListItem` | `root/proto17` / `0x1E9B` |
| `setTopMenuList` | `root/proto20` / `0x21A5` |
| `callbackTopMenuList` | `root/proto21` / `0x23AF` |

## Region list

The region list (title text 5205, previous category 2) holds these row data
values in order, with `focusMenuListItem(1)` at the end:

| Row data | Text | `callbackSelectRegionMenuList` |
| ---: | --- | --- |
| -2 | 5207 | `setDisplayLocation(-1, -1)` |
| -3 | 5210 | `setDisplayLocation(101, 2)` |
| 101 to 105 | 5201 with the region id | stores `work.regionId` and opens category 3 |
| -1 | 100125 | `setMenuCategory(1)` |

`setDisplayLocation(layout, rect)` sets `Layout` and `Rect` of
`CustomControl_MapNavigation`, then `Ready` false and `Ready` true.
`setSelectPieceMenuList` (title text 5205, previous category 2) requests
`aetheryte2DmapSheet` rows for the pair that
`desktopWidget:getAchieveAetheryteID(work.regionId, false)` returns.

## Zoom methods

`zoomOut` reads `Scale` of `CustomControl_MapNavigation` and returns when it
is at most 0.3. `zoomIn` reads it and returns when it is at least 2. Neither
method requests anything else, and no statement of this script calls them.
So the script plays no part in the `PageUp` and `PageDown` zoom, which the
form binds to native commands.
