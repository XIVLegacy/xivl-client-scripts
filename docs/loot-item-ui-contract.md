# Loot item UI contract

The Main Menu checks package 5's count before adding command 0, then maps that
command to the desktop connector's `ItemListWidget` mode-3 opener. The count
check therefore gates this menu route indirectly. In mode 3, the widget
selects listbox 5, which reads capacity and item entries from package 5.

`ItemListWidget.operateGetDrop` calls the local command helper with the tuple
`(24223, item, item:getItemProperPackage(), 5, nil, nil, count)`. The share
widget also uses 24223 for self-claim/leave paths. Its other-member path calls
24225 with `(24225, item, 5, 5, nil, targetActor)`, where the helper resolves
the actor from the selected party-member index. The share widget's breakup
path resolves a package-5 item and calls `executePlayerItemWaste(5, slot)`;
the desktop connector then passes `(24226, item, 5)` to the local command
helper. `ItemSubWidget.Button_Trash` routes through
`ItemListWidget.operateTrash` to `ItemEditWidget`. The widget initializes
`chosenOperation` to 0; its Button_OK branch reaches the same waste helper only
when that field is still 0, Button_OK is enabled, `commandThrow` is active, and
`checkCertainItem` passes. Its count argument is not forwarded by the
connector helper. These are Lua helper arguments, not a recovered wire
payload or server effect.

This proves the package number and client-side UI argument routes only. It
does not identify package 5 with a server-side inventory, establish a global
package alias, or prove any command's server effect.

Evidence:

- `lua/scripts/widget/desktopwidget_connector.lua:4386-4413,13454-13474,14800-14935`
- `lua/scripts/widget/mainmenuwidget.lua:1346-1358,2141-2145`
- `lua/scripts/widget/itemlistwidget.lua:495-574,1692-1711,2905-3031,4613-4677,4680-4750`
- `lua/scripts/widget/itemsharewidget.lua:203-264,294-313,331-368`
- `lua/scripts/widget/itemeditwidget.lua:162-165,207-251,666-740`
- `lua/scripts/widget/itemsubwidget.lua:354-362`

The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding installed LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.
