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
recovered `ContentCommand` script divides the retained variation into
target-selection ranges. Its `canFire` method applies these checks:

| Variation range | Target check |
| --- | --- |
| `10000-19999` | No target is supplied. |
| `20000-29999` | No additional target restriction. |
| `30000-39999` | The target is a player. |
| `40000-49999` | The target is non-null and not a player. |
| `50000-59999` | The target is a member of the player's party. |

The recovered `fire` method returns false. These predicates establish client
target eligibility only; they do not identify any producer's selected
variation or a server operation for command 24302. The separate 24301 touch
path is not an alias for 24302: the main menu and desktop dispatch keep them
distinct, and instance-raid touch uses the place-driven route.

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

The canonical source bytes are pinned in `manifests/scripts.json` (the
`ContentCommand` source SHA-256 is
`8d6e8752eb1cf72db7b90239065ccde3cd2decfdca01f18901ab21f7ffdb2564`). The
corresponding retail LPB
`7vxx9w6/rlrq5x/7vwq5wq7vxx9w6.le.lpb` is pinned in
`manifests/retail_lua_coverage.json` (SHA-256
`15e0747fc6203b0752895b2af1e7781c7f79f71802be3ebbae791c22c81e23e7`;
decoded payload SHA-256
`84e673de8388d8252c3372892d40adaae64c7043327cc3f5f57a109c2fd05ef9`).
