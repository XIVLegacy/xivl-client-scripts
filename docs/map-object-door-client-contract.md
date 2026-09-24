# Map-object door client contract

The canonical `Chara/Npc/MapObj/DoorServer.initForEvent` body is at
`lua/scripts/chara/npc/mapobj/doorserver.lua:11-62`
(SHA-256
`7cbd05f45800e60a21c7b59a728b42bc8115d97c88ce4a91703b37bbe784540c`;
`manifests/scripts.json`).
Its matching `client/script/729s9/wu7/x9uv80/6vvsr5so5s.le.lpb`
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

## Beacon Fort status gate

The `BeaconFortGateGimmick` chunk matched the recovered LUAC
byte-for-byte (decoded SHA256
`17635FDA7214B70895AFFA0AA978E333F53779AE87D762295048DCAC5BD09EED`).
`initForGimmick` stores supplied show/hide scheduler names and an initial
`currentStatus` of zero, and tags the synced `status` field as `mapStat`.
`processUpdateWork` calls `executeScheduler` only when `status` differs from
`currentStatus`. Status 1 selects the supplied show name; other values select
the hide name. When the previous status is zero, `executeScheduler` calls
`_runBgSchedulerFromMidstream(name, 5)`; otherwise it calls
`_runBgScheduler(name)`, then retains the new status
(`beaconfortgategimmick.lua:3-67`; source identity
`manifests/scripts.json:572-577`). The script does not identify a retail
actor class ID, placement, status producer, or observed gate appearance.
