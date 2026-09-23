# Content command client route

The decoded 1.23b Lua corpus preserves a client route from director work to
the main-menu Content command. `DirectorBaseClass` exposes the retained
`contentCommand` and `contentCommandSub` values, and mirrors updates through
`PlayerBaseClass.setContentCommandVariation` into player work. The player
client-program getters read that mirror. `MainMenuWidget` renders command
24302 from the retained values; the desktop connector reads the same values
when dispatching the command.

The static-actor class-path manifest maps 24302 to
`/Command/System/ContentCommand` and separately maps 24301 to
`/Command/System/PlaceDrivenCommand`
(`xivl-client-data:manifests/staticactor_class_paths.json:3278-3284`). The
recovered `ContentCommand` script contains target-range checks, but its `fire`
method returns false. The separate 24301 touch path is not an alias for 24302:
the main menu and desktop dispatch keep them distinct, and instance-raid touch
uses the place-driven route.

This is a client-side work and menu route only. It does not establish which
native or other component supplies the retained values, their historical
values, or a server operation performed by command 24302.
A text scan of the decoded Lua corpus found no literal assignments to
`contentCommand` or `contentCommandSub`; this does not rule out a native or
other producer.

Evidence:

- `lua/scripts/director/directorbaseclass.lua:42-105,150-166,287-348`
- `lua/scripts/chara/player/playerbaseclass.lua:1502-1539,1595,2462-2480`
- `lua/scripts/chara/player/playerbaseclass_cliprog.lua:112-127`
- `lua/scripts/widget/mainmenuwidget.lua:1492-1545,1651-1667`
- `lua/scripts/widget/desktopwidget_connector.lua:13879-13897`
- `lua/scripts/command/system/contentcommand.lua:11-84,103-180`

The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.
