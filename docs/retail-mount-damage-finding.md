# Mount damage, Lamed, and bucking

Verdict: retained official documentation describes chocobo slowdown and bucking
after attacks. The 1.23b status sheets contain Lamed text for both chocobos and
Goobbues. These sources do not establish the damage trigger, threshold, or
bucking behavior actually applied by the 1.23b server, especially for Goobbues.

## Evidence

The retained official manual's `Getting Around`, `Chocobos` / `Riding Chocobos`,
states that mounted riders can take damage, attacks may slow their chocobo,
and excessive damage can make it throw the rider and flee. This is documented
intent for chocobos. It supplies no numeric threshold, probability, duration,
or Goobbue rule.
Source: `xivl-captures:sources/lodestone-manual/objects/pages/getting-around.md`,
SHA-256 `c97f6450afe67fa8490878a78af3b527d524f5dd3c6fc5ec7d409f5332bcaa3a`.
`xivl-captures:sources/lodestone-manual/manifest.yaml`, member
`pages/getting-around.md`, records its identity and 2015-01-08 snapshot.
`xivl-captures:studies/lodestone-manual/README.md`, `Evidence tier`, limits
this `web-tables` source to documented intent without runtime corroboration.

In extraction `2012.09.19.0001`, `xtx_status.csv` rows 230016, 230017 and
230018 have English name `Lamed` in column 3. Column 21 describes reduced
chocobo speed for 230016/230017 and reduced Goobbue speed for 230018.
These are text rows, not proof of application on damage.
Source: `xivl-client-data:manifests/tables.json`, `csv/xtx_status.csv`,
SHA-256 `60eca3b76d1d9799589d9059adeb1e7c3d142e07609a1ad0a053c5e75d9b96ee`.
`xivl-client-data:docs/status-names.md` owns the column mapping and the
static-sheet interpretation limits.

The [mount script contract](chocobo-mount-script-contracts.md#ride-command-and-judge)
identifies mounted main state 15 and grade 257 for Goobbue, plus local ride
admission and error remapping. Its `Evidence identity` section pins the
`ChocoboRideCommand` and `ChocoboJudge` LPB/payload identities. These methods
do not supply a damage-to-Lamed or damage-to-dismount rule.

## Unestablished boundary

`xivl-decomp:docs/net/chocobo-rental-state.md`, `Rental packet ownership` and
`Mounted completion callback`, establishes state and rental lifecycle paths
in `ffxivgame.exe` at VAs `0x0058CCA0` and `0x00703F60`. Its binary SHA-256 is
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Those paths do not establish a damage producer. The same binary's model
resolver at VA `0x0065E040`, documented in
`xivl-decomp:docs/actor/goobbue-mount-resolver.md`, selects appearance and
does not establish mount damage semantics. No damage threshold or historical
1.23b damage-to-buck sequence is established here.
