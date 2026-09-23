# Inn bed client hook

`ObjectBed.initForEvent` initializes its local bed and login-event flags, then
calls `_readyInnBed(self)` on the current player. It sets the local
`isInLoginEvent` flag only when that call returns true. This records a direct
client call and its return gate; it does not establish native method semantics,
inn-storage behavior, login placement, dream-event activation, or a loading
screen cause.

Evidence: `lua/scripts/chara/npc/object/objectbed.lua:11-54`. The canonical
source bytes are pinned in `manifests/scripts.json`; the corresponding
LPB path, size, SHA-256, decoded payload hash, and `matched-script`
classification are in `manifests/retail_lua_coverage.json`.
