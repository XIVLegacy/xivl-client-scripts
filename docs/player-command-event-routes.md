# Player command event routes

`PlayerBaseClass._onLoginEvent` obtains command `24105` with
`getSystemCommand` and passes it through the player's `command` method. In
`_onCommandEvent`, command `24105` first receives a local `fire` call; a true
result returns before `_callServerOnCommand`, while a false result continues
through the ordinary server-command route.

After `_callServerOnCommand`, command `12014` has a client-side follow-up. The
player reads `isRiding` from static actor `320013` and checks
`_isPushingOut`. If both are true, it notifies `worldMaster` with the text
resolved by `getRidingErrorTextId` using argument `26005`, then obtains and
executes command `12015` using its resolved command name and actor.

The static-actor class-path manifest maps `12014` and `12015` to
`/Command/Game/Prog/ChocoboRideCommand` and `24105` to
`/Command/System/LoginEventCommand`. These mappings and calls establish a
client dispatch path, not the server meaning of `26005`, a historical command
invocation, or the runtime effect of executing `12015`.

The static actor `320013` predicates and `ChocoboRideCommand.canFireDetail`
gates are documented with their LPB identities in
[`chocobo-mount-script-contracts.md`](chocobo-mount-script-contracts.md).

Evidence:

- `lua/scripts/chara/player/playerbaseclass.lua:1823-1881,3011-3020`; source
  SHA-256 `6226b3fa15dfdbad279b7db453f8a3b76fcb8b68bad6e14f5403d52987f76e4`,
  pinned at `manifests/scripts.json:6657-6660`.
- Retail LPB `729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`, SHA-256
  `32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e`,
  decoded payload SHA-256
  `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`,
  pinned at `manifests/retail_lua_coverage.json:5956-5971`.
- `xivl-client-data:manifests/staticactor_class_paths.json:58-64,3114-3116`,
  SHA-256
  `d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
