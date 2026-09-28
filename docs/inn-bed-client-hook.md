# Inn bed client hook

`ObjectBed.initForEvent` initializes its local bed and login-event flags, then
calls `_readyInnBed(self)` on the current player. It sets the local
`isInLoginEvent` flag only when that call returns true. This records a direct
client call and its return gate; it does not establish native method semantics,
inn-storage behavior, login placement, dream-event activation, or a loading
screen cause.

`ObjectBed.askLogout` handles ask results `2` and `3` by choosing a four-value
pose tuple from the bed actor class and passing it to the player method
`_setPosDirInn`:

| Bed actor class ID | X | Y | Z | Direction |
| --- | ---: | ---: | ---: | ---: |
| `1200378` | `-162.42` | `0` | `-154.21` | `-1.56` |
| `1200379` | `157.55` | `0` | `165.05` | `-1.53` |
| `1200380` | `-2.65` | `0` | `3.94` | `-1.52` |

The setter call precedes fade-in and scheduler `83783680`. This pins the
arguments requested by this client path, not their coordinate frame, the
resulting rendered pose, a city-to-actor placement, or server-side login
placement.

Evidence locators: `ObjectBed.initForEvent` and `ObjectBed.askLogout` in the
reviewed decompile output (`objectbed.lua:3-18,27-90`, output SHA-256
`58e804433f7be5c0fe4302f9008fbe39244095a42596ded71bf8001267f9d889`). Its
bytecode SHA-256 `2850520b7136e646965f63eaaf6de04e6aa8a55ba214714a71dd489602f5dc9`
matches the decoded payload for LPB
`729s9/wu7/v8057q/v8057q856.le.lpb` (SHA-256
`4c056254fd1e8c2e3d010d978149da9e25b91f7965c8569b86aa4189c6df3500`). The
canonical source SHA-256 `1cb34158c8b8975758f60bd3ce0da8b70675cd838b65cd4be5688a1917cfaef1`
is pinned in `manifests/scripts.json`; the LPB identity and decoded payload
hash are pinned in `manifests/retail_lua_coverage.json`.
