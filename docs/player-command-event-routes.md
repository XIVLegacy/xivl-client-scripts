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
  SHA-256 `6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4`,
  pinned at `manifests/scripts.json:6657-6660`.
- Retail LPB `729s9/uy9l5s/uy9l5s89r57y9rr.le.lpb`, SHA-256
  `32182274f3886d0cdf6329f8a82e6592790c9b3038e00bebe5b2b38702bbd53e`,
  decoded payload SHA-256
  `1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`,
  pinned at `manifests/retail_lua_coverage.json:5956-5971`.
- `xivl-client-data:manifests/staticactor_class_paths.json:58-64,3114-3116`,
  SHA-256
  `d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.

## Information-request guard and record state

`PlayerBaseClass.canRequestInformation` reads
`self.playerWork.requestBurstBlocker` and returns exactly one Boolean:
whether that value is strictly less than the result of
`worldMaster:_getServerTime()`. Equality returns false. The helper does
not write the field.

`recordRequestInformation` takes only its player receiver and returns no
values. It reads `worldMaster:_getServerTime()` as `t0`, then reads the blocker
as `b`. When `t0 <= b + 1`, it calls `_getServerTime` again and stores that
second result plus `3` in `self.playerWork.requestBurstBlocker`. Otherwise it
calls `_getServerTime` again and stores the second result directly. Each
normal branch therefore uses two clock reads. The helper consumes no native
request result or acceptance flag.

The concrete caller is `CharaBaseClass.updateItemPackage`: it checks the local
player's guard, calls the receiver's `_updateItemPackage(package)` only when
the guard passes, then records the local player's request after the native
call returns normally. The original caller order is retained at
`xivl-decomp:docs/script/materia-command-dispatch.md`, "Package refresh and
publication" (`root/proto27`, CALL PCs `4`, `9`, `14`; source `1278-1306`,
revision `ae2b85946c0e353a90497b67046213f92680acbd`). This is a conditional
request attempt and player-state update. It does not establish request
acceptance, completion, response arrival or a historical successful request.

The selected helpers contain no nil or flag fallback. The blocker initializer,
other writers and server policy remain unbound. JournalCommand's dynamic
receiver is not identified by this separate local-player caller.

The page's evidence records pin the retail LPB and decoded-payload identities.
With zero-based PCs and half-open decoded-payload offsets, the guard is
`root/proto28`, PCs `0-10`, `[0x2DA5,0x2DD1)`, `11` words/`44` bytes. Its
strict comparison is PC `5`, with the one-result return at PC `9`. The writer
is `root/proto29`, PCs `0-20`, `[0x2E47,0x2E9B)`, `21` words/`84` bytes. Its
inclusive comparison is PC `6`, second clock calls are PCs `11` and `18`,
and stores are PCs `13` and `19`. Exact root class/name bindings are PCs
`96-101`, `[0x1A0,0x1B8)`: `GETGLOBAL PlayerBaseClass`, `CLOSURE`, then
`SETTABLE` bind each method to its child prototype. Both methods have one
fixed parameter, zero upvalues and no varargs. The producing tools are
`tools/retail_script.py` (`decode_lpb`) and
`tools/build_quest_contracts.py` (`ChunkReader`, `instruction`) at revision
`6a19d5909c1a454b9b0656ef75e311c5d7501f31`.

### Clock qualification

If these calls resolve to the documented native
`WorldMaster._getServerTime` binding and the receiver is accepted as native
`WorldMaster`, the call takes zero post-receiver arguments and returns exactly
one Lua number. The cached whole-second dword at `WorldMaster+0x60` is
interpreted as signed 32-bit and converted to double. The binding, receiver and return
conversion are canonical in
`xivl-client-structs:docs/world-master-native-call-contract.md`, Registration
and receiver and Return conversion. The source, whole-second unit and cache
initialization are canonical in
`xivl-decomp:docs/actor/cast-timing-clock.md`, Native clock model.

Under this binding, the guard compares the blocker with a whole-second
sample, and the writer's constants `1` and `3` are seconds offsets. The
writer still tests its first sample `t0` and stores its separate second
sample `t1`, with `3` added only on the inclusive branch. The native return
conversion does not preserve the unsigned interpretation of dwords with the
high bit set. The script arithmetic establishes neither a fixed elapsed wait
nor a request rate, persistence or server settlement rule. Actual invocations
were not observed. The selected writer does not bind the blocker's initial
value or other writers to this signed clock domain. The static composition
establishes no monotonic-clock guarantee.
