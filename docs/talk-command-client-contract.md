# TalkCommand client contract

The static actor path catalog maps ID `24101` to
`/Command/System/TalkCommand` (`xivl-client-data:manifests/staticactor_class_paths.json:3101-3103`,
SHA-256
`d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`). The
matched `TalkCommand` script derives from `SystemCommandBaseClass`.

`TalkCommand.canFire` uses its sixth command argument (`A6` in the decoded
chunk) as the candidate target. If the player is in active mode, it requires
`_isActorMainStatMode(2)`; it then requires `isLiving()`, requires the target
to be an instance of `NpcBaseClass`, and delegates the final eligibility test
to `_canExecuteTalk(target)`. A failed gate returns false.

`TalkCommand.fire` uses the same argument as target. It compares
`target:getLimitedDistanceForTalk()` with the distance between the player and
target positions. When the limited distance is less than or equal to the
measured distance, it calls `worldMaster:alert(25081)` and returns true.
Otherwise it calls `_executeTalk(target)` and returns true. These are direct
client gates and call order; they do not identify the native eligibility
predicate's implementation or the effect of `_executeTalk`.

The bytecode does not establish which event-packet slot supplies `A6`, whether
a particular packet invokes command `24101`, or how command actor ownership
and NPC/object event ownership are handled. The static path mapping and script
body do not prove that a specific NPC or object uses this route.

## Provenance

The source is `lua/scripts/command/system/talkcommand.lua`, SHA-256
`b57ae2719e12bedc4451cdeb02f13fd04533a62d85748ea98da7f8321a15cf66`,
pinned in [`scripts.json`](../manifests/scripts.json). Its LPB is
`7vxx9w6/rlrq5x/q9yz7vxx9w6.le.lpb`, 836 bytes, SHA-256
`ad2e0c459b2c45c46af25b9f418c9d89eb86544e8630f8d218531223c940ddad`; the
decoded 823-byte payload SHA-256 is
`2717d0d91213fa21c3b6ddafa013b973eefbcfd27a147bfb61966e0cbc71df74`.
The payload is classified `matched-script` in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
