# Guildleve initializer arguments

The retail Lua initialization chain separates the client Director ID from
the Guildleve ID and its location/marker arguments. The selected methods
forward complete argument tails, including positional nil values:

```text
DirectorBaseClass._onInit(self, D, ...)
    directorWork.directorId = D
    self:init(...)

GuildleveBaseClass.init(self, G, L, X, Y, Z, ...)
    guildleveId = G
    aetheryteLocation = L
    exMarkerX, exMarkerY, exMarkerZ = X, Y, Z
    self:initAsGuildleve(...)
```

The stored Guildleve fields belong to `guildleveWork`. The selected root
declarations establish `PrivateGLBattleOrbNormal -> GuildleveBaseClass ->
DirectorBaseClass`. OrbNormal's `initAsGuildleve(self)` is a non-vararg,
empty method returning zero results. It does not consume extra arguments.
The base `init` and `initAsGuildleve` placeholders also return zero results.
Both forwarding calls discard all results. None returns a single nil value.

## Retained 12487 vector

The native route is recorded in
`xivl-decomp:docs/net/guildleve-initializer-route.md`. For the captured
ordinary non-current-player path, five Boolean controls follow the captured
path and precede the numeric remainder. The first false control selects
deferred initialization.
Descriptor vector preservation, historical branch/endian state and native
request/lifetime conditions remain prerequisites of the substitution below.

| Supplied non-self position at `_onInit` | Value | Lua consumer |
| ---: | ---: | --- |
| 1 | 20005 | `directorWork.directorId` |
| 2 | 12487 | `guildleveWork.guildleveId` |
| 3 | 6 | `guildleveWork.aetheryteLocation` |
| 4 | 0 | `guildleveWork.exMarkerX` |
| 5 | 0 | `guildleveWork.exMarkerY` |
| 6 | 0 | `guildleveWork.exMarkerZ` |

With that six-value input, the OrbNormal hook receives only self. The
captured path and five controls are not Lua arguments in this substitution.
The field name `directorId` does not identify a server implementation or
prove a static-table meaning for 20005. Location 6 remains a stored client
value without an assigned place name here. Static argument routing does not
establish that the historical request completed.

## Operand evidence

Children are zero-based beneath each root; PCs are one-based. Offsets are
zero-based decoded-payload offsets. Original LPB offsets are payload offsets
plus 13 before XOR decoding.

| Method | Child | Critical PCs / payload offsets |
| --- | ---: | --- |
| Director `_onInit` | 5 | Store D at PC56 / `0x5B6`; resolve `init`, open VARARG and CALL at PCs57-59 / `0x5BA..0x5C2`; zero-result return at PC60 / `0x5C6` |
| Director `init` placeholder | 6 | Zero-result return at `0x6FF` |
| Guildleve `init` | 17 | Stores G/L/X/Y/Z at PCs112/114/120/122/124 / `0x112C/0x1134/0x114C/0x1154/0x115C`; resolve hook/open VARARG/CALL at PCs125-127 / `0x1160..0x1168` |
| Guildleve hook placeholder | 18 | Zero-result return at `0x1486` |
| OrbNormal hook | 0 | Zero-result return at `0x152` |

Director root PCs17-18 bind `_onInit`; Guildleve root PCs60-61 bind `init`;
OrbNormal root PCs9-10 bind its hook. Director `_onInit` has two fixed
parameters including self; Guildleve `init` has six. Both use open VARARG
and `CALL B=0,C=1`. Their tails retain count and positional nils without a
table or length operation. OrbNormal declares one fixed parameter and no
varargs. Every selected return uses `RETURN B=1`, meaning zero results.

Director `_onInit` first calls `_callSuperClassFunc("_onInit")` with no D
or vararg tail in that explicit call. That helper's implementation and
possible effects remain outside this operand finding. Guildleve initialization
reads sheet field 21 for G with one requested result before storing
`timeLimit`; the existing [UI contract](content-director-ui-contracts.md#guildleve-and-request-directors)
owns the sheet and presentation uses.

## Source identity

These retail resources are relative to `client/script/`. Original and decoded
payload pins are in [retail_lua_coverage.json](../manifests/retail_lua_coverage.json),
with canonical source identities in [scripts.json](../manifests/scripts.json).

| Class / resource | Original LPB SHA-256 | Decoded payload SHA-256 |
| --- | --- | --- |
| DirectorBaseClass, `61s57qvs/61s57qvs89r57y9rr.le.lpb` | `7BCA9CCB9F130EA27EA8E43DD94AFDB6BA0ACF9F133F6294564988A281E72D7B` | `B63CD23139DC84B4E3C9D713C01278EE1D83F45A3658BA7587EEC66AF81BA93B` |
| GuildleveBaseClass, `61s57qvs/3p1y6y5o5/3p1y6y5o589r57y9rr.le.lpb` | `73559543D4E2192180C28AC8F8F6F3FB69EBF8BCBB47B2C11A69C837CFE8F303` | `BCAD3160D16813502529467CE5DA17BB3A9BC80C576CD71841708FE7859D7E84` |
| PrivateGLBattleOrbNormal, `61s57qvs/3p1y6y5o5/us1o9q53y89qqy5vs8wvsx9y.le.lpb` | `680FEE69BBE3DE582840D9C15283BBFCFB65612A8C6586A36FB19D3BA53BDB7E` | `AABF02993E673043AC68545E8AFE1B1B2896D3320E94F2EC6AB9AC6BBF432686` |

Original sizes are 3,867, 13,574 and 1,042 bytes; decoded sizes are 3,854,
13,561 and 1,029. A direct Python Lua 5.1 operand parser authenticated these
artifacts and inspected the three roots plus five named methods. Canonical
source text was not needed for these operand observations. The retained
capture and native findings supply the separate serialized-input evidence.
