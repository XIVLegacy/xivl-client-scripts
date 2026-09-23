# Map-object door client contract

The recovered `Chara/Npc/MapObj/DoorServer.initForEvent` body comes from
`tools/outputs/lpb/decomp_further_20260617/lua/chara/npc/mapobj/doorserver.lua`
(SHA-256
`5abf5ebdbaf8e628fd7b8aacfd36cb4e98921174bf17479f71d9217c45de4eec`).
Its matching installed `client/script/729s9/wu7/x9uv80/6vvsr5so5s.le.lpb`
has SHA-256
`4aeeb74b47fb1bee784d73abacc7f54f517f42c47282f9efbe156b39ddd009df`.
The canonical class and method inventory is in
[`registry.json`](../lua/registry.json) under `chara/npc/mapobj/doorserver`.

The method initializes work fields named `layout` and `instance`. When its
final Boolean argument is true, actor class ID 5900015 requests background
scheduler `open` from offset 5; other IDs request `hide` from offset 5.
It then disables ground. A false final argument does not enter either
scheduler branch in the recovered body.

This is a client-side initialization branch, not proof of a particular
door's retail initial Boolean, its actor placement, the producer of that
argument, its later state transitions, or collision behavior. The
contributor's Darkhold barrier correction and server Lua dispatch are
implementation evidence, not a retail-state observation.
