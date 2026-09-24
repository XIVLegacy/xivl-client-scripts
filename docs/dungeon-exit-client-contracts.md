# Dungeon exit client contracts

The 1.23b Lua scripts preserve several different exit prompts. The
source identities below join canonical Lua to
`client/script/` LPBs. The `ciphered` path is the registry path with `.lua`
replaced by `.le.lpb`; all hashes are SHA-256. Canonical source members are
under `lua/scripts/chara/npc/` in the pinned Lua corpus. The class and
method inventory is in [`registry.json`](../lua/registry.json), and the
source hashes are in [`scripts.json`](../manifests/scripts.json).

| Class and registry key under `chara/npc/` | LPB suffix / hash | Canonical Lua hash |
| --- | --- | --- |
| `RaidDungeonExit`, `object/raiddungeonexit` | `729s9/wu7/v8057q/s9166pw35vw5m1q.le.lpb` / `ec628b2a1e72f70551309d21218a697b6ee46db0ffa04de1eee7190edbc36279` | `70f5656b605db6ebbcf4b97742beefd7dd47754f1419ea3c2b93f469c12de399` |
| `InstanceRaidExit`, `object/instanceraidexit` | `729s9/wu7/v8057q/1wrq9w75s9165m1q.le.lpb` / `cc1d7f58075f7c0ecace5049c68240fe3e04c46642fad0ecb5caeb333e440b96` | `8075c364de5bf4916d51b25224dba05c22df2af2911839b29a9f81ef421cb62b` |
| `PrivateAreaPastExit`, `object/privateareapastexit` | `729s9/wu7/v8057q/us1o9q59s59u9rq5m1q.le.lpb` / `254f738b1aa6401ed9bd1bf0bbac463017089d5ce249b03211860b5b338be400` | `49fe7971d5db608fb508671a14d189da35ce666c2f1aa757a5c3401c070d5a19` |
| `GimmickNpcBaseClass`, `gimmick/gimmicknpcbaseclass` | `729s9/wu7/31xx17z/31xx17zwu789r57y9rr.le.lpb` / `d685e404923bf98b945ab2d6dbf92b66d358c45051ab5d37da4d159c00319f87` | `2e442c47948ad0858ddf7ee5e9c8828124b2fab39cb83bf7507ccacc0c3e431a` |
| `GimmickExitRect`, `gimmick/gimmickexitrect` | `729s9/wu7/31xx17z/31xx17z5m1qs57q.le.lpb` / `e394496682df9274616fa2710947f8dd16c96bbe2d7959d546aba49bb95e265e` | `ec1ddb1001a063b00a7ee8983271433eb5d3f193a47f6d93f9ddd23f9cb1d23c` |
| `GimmickTerminal`, `gimmick/gimmickterminal` | `729s9/wu7/31xx17z/31xx17zq5sx1w9y.le.lpb` / `c35f7ff4f40a8558d62d6a440a22bdc175db71c0c41cf5f8042b03ecb893137e` | `5bc7f7758127643c8ff5828eb3d7bee52023179ee1491e95c43dfa9822eb9d79` |
| `GimmickWarp`, `gimmick/gimmickwarp` | `729s9/wu7/31xx17z/31xx17zn9su.le.lpb` / `228f3debb77bfd75d665f17f338fddac5417c954c74b9375b3638be68c589456` | `204bd81b4889d2310c3a7f9bee0f3fc874f33a5da6296edacf0fbd4883e845b0` |

## Prompt and marker behavior

`RaidDungeonExit.initForEvent` loads text bank 6736 as `raidDungeonExit`.
Its `askYesNo` calls `askExtendWidget` with prompt rows selected by a type
argument. The recovered type-3 branch contains an invalid `break`, so its
relationship to the subsequent row-1 and row-4 calls is not settled by this
decompile. The class contains no proven destination or exit movement.

`InstanceRaidExit.initForEvent` disables ground. `askExit` passes world-master
text row 52042, response rows 52043 and 52044, and its argument to
`desktopWidget:askForEventMode`; it returns true only for response 1.
`GimmickNpcBaseClass.askExit` uses the same text rows and response test with
an optional event-mode argument defaulting to 1. Its `initForEvent` stores a
talk range and delegates to the child's `initForGimmick`.

`GimmickExitRect.initForGimmick` loads text bank 10064 as
`gimmickExitRect` and disables ground. `askExitWithPlaceNameId` asks rows
1/2/3, then rows 4/5/6 only after the first response is 1; it returns true
only after both responses are 1. The place-name ID is a method argument, not
a binding or destination inferred from the class name.

`GimmickTerminal.initForGimmick` loads bank 10096 as `gimmickTerminal`;
`eventTalkTerminal` forwards its argument to `worldMaster:say`.
`GimmickWarp.initForGimmick` loads bank 10112 as `gimmickWarp` and disables
ground. Its matched decoded payload confirms the `askWarp` mode branches:
mode 1 passes prompt row 1 and choices 2/3, mode 2 passes row 4 and choices
5/6, and mode 3 passes row 7 and choices 8/9 to
`desktopWidget:askForEventMode`. Mode 1 clears a nonzero second argument
before the call. Modes 2 and 3 pass a nonzero second argument as the optional
last argument; zero omits it. The method returns true only when the prompt
result is 1. This branch structure is supported by the matched payload
`1ce2926a5fc353f58eaafe6012a88a39c9965b5918e5d2f52af85c2bf7f8681d`
(`manifests/retail_lua_coverage.json`); the second argument's meaning and any
destination or actor binding are not established by this method.

`PrivateAreaPastExit` only disables ground in `initForEvent` and returns the
marker-range names `exit` and `caution`. Its retail client body does not
contain the contributor server's `CanExitPrivateArea`, message 34110, or
`WarpToPublicArea` logic.

## Evidence boundary

These are client-side UI and marker contracts. The files do not associate an
actor class ID or spawn with any of these class paths, and do not establish
private-area permission, server exit handling, return-point ownership,
destination, cleanup, or retail prompt outcome. Contributor SQL bindings and
server adapters are separate evidence, not a retail class-ID join. No live
retail probe is available to resolve those historical runtime questions.
