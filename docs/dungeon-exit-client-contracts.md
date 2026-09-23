# Dungeon exit client contracts

The installed 1.23b Lua scripts preserve several different exit prompts. The
source identities below join independently recovered Lua to installed
`client/script/` LPBs. The `ciphered` path is the registry path with `.lua`
replaced by `.le.lpb`; all hashes are SHA-256. Recovered Lua comes from the
contributor's `tools/outputs/lpb/decomp_more_20260617/lua/` for the object
classes and `decomp_further_20260617/lua/` for the gimmick classes. The
canonical class and method inventory is in [`registry.json`](../lua/registry.json).

| Class and registry key under `chara/npc/` | Installed LPB suffix / hash | Recovered Lua hash |
| --- | --- | --- |
| `RaidDungeonExit`, `object/raiddungeonexit` | `729s9/wu7/v8057q/s9166pw35vw5m1q.le.lpb` / `ec628b2a1e72f70551309d21218a697b6ee46db0ffa04de1eee7190edbc36279` | `17010d68da5a1033ca10c919d25ce407f46d461f670c6bf2c1f623fd7d62aefc` |
| `InstanceRaidExit`, `object/instanceraidexit` | `729s9/wu7/v8057q/1wrq9w75s9165m1q.le.lpb` / `cc1d7f58075f7c0ecace5049c68240fe3e04c46642fad0ecb5caeb333e440b96` | `8bf13b56cc7d4f0ab84187f77a63119d5f8905e2d05d08edda451b600ae7ec76` |
| `PrivateAreaPastExit`, `object/privateareapastexit` | `729s9/wu7/v8057q/us1o9q59s59u9rq5m1q.le.lpb` / `254f738b1aa6401ed9bd1bf0bbac463017089d5ce249b03211860b5b338be400` | `92e753226bfab0c1c58e1981c2dcbe3f643ac34b8fbed92d807b9961a9d79258` |
| `GimmickNpcBaseClass`, `gimmick/gimmicknpcbaseclass` | `729s9/wu7/31xx17z/31xx17zwu789r57y9rr.le.lpb` / `d685e404923bf98b945ab2d6dbf92b66d358c45051ab5d37da4d159c00319f87` | `ce52e980797e5a8dc3449b1580c18ce96db622353f9122d25e0429d0412ca8bc` |
| `GimmickExitRect`, `gimmick/gimmickexitrect` | `729s9/wu7/31xx17z/31xx17z5m1qs57q.le.lpb` / `e394496682df9274616fa2710947f8dd16c96bbe2d7959d546aba49bb95e265e` | `14a51814151875536761301944d96db1785e136a27aa03c82630c7c239fec301` |
| `GimmickTerminal`, `gimmick/gimmickterminal` | `729s9/wu7/31xx17z/31xx17zq5sx1w9y.le.lpb` / `c35f7ff4f40a8558d62d6a440a22bdc175db71c0c41cf5f8042b03ecb893137e` | `64c5280f6b179415a38144fecb4046122c773af3d38960eb823852938119cfad` |
| `GimmickWarp`, `gimmick/gimmickwarp` | `729s9/wu7/31xx17z/31xx17zn9su.le.lpb` / `228f3debb77bfd75d665f17f338fddac5417c954c74b9375b3638be68c589456` | `084c1a3d6f41a70161efce3f339e41452ef754487fa8551b4633e79303a709af` |

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
ground. `askWarp` has prompt-row groups 1/2/3, 4/5/6, and 7/8/9 in the
recovered body, but damaged control flow prevents assigning every selector
and optional argument to a reliable branch. The visible method asks through
`desktopWidget:askForEventMode` and returns true for response 1.

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
