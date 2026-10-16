# Ferry service and event scenes

Verdict: retained official documentation describes a Limsa Lominsa Lower
Decks-Western Thanalan ferry service, and the 1.23b client retains associated
scene resources. The historical 1.23b server route and its event-scene
selection remain unestablished. An optional second scene argument is not
evidence that a ferry voyage played two scenes.

## Evidence

The retained official manual's `Getting Around`, `Ferries`, connects Limsa
Lominsa Lower Decks (3, 5) with Western Thanalan (4, 26). It describes entering
through a counter NPC, automatically boarding the next departure, and exiting
through the destination counter NPC. This establishes documented service,
not an observed 1.23b voyage or another Vylbrand endpoint.
Source: `xivl-captures:sources/lodestone-manual/objects/pages/getting-around.md`,
SHA-256 `c97f6450afe67fa8490878a78af3b527d524f5dd3c6fc5ec7d409f5332bcaa3a`.
`xivl-captures:sources/lodestone-manual/manifest.yaml`, member
`pages/getting-around.md`, owns its retained identity and 2015-01-08 snapshot.
`xivl-captures:studies/lodestone-manual/README.md`, `Evidence tier`, classifies
the manual as `web-tables` and documented intent.

`xivl-decomp:docs/resource/ferry-scene-inventory.md` identifies these
1.23b resources and their authored boarding-related timelines:

| Resource | SHA-256 |
| --- | --- |
| `client/cut/vsl0l010/vsl0l010` | `6df2130a46e3683e94b1522b4d1bce4399464b7fca28698d1e1e90c4f5ccf083` |
| `client/cut/vsl0u010/vsl0u010` | `fef60bfdfa00ca8c26d697569cdcaefdb1192d66858f1f7ab0d35a369bd06b80` |

Their background clips name `sea_s0_lin01` and `wil_w0_lin01`, respectively.
`xivl-decomp:docs/resource/ferry-door-schedulers.md`, `Layout owners`, joins
those resources to Limsa layout 196 and Thanalan layout 496. Resource presence
and authored animation do not establish historical server selection.

The [Fisher ferry prompts](quest-event-client-contracts.md#fisher-ferry-prompts)
only return dialogue choices. They contain no travel call. The
[DftSrt wrapper](quest-event-client-contracts.md#dftsrt-travel-scene-wrapper)
fades out, plays its fourth argument, optionally plays a nonnil fifth
argument, then fades in after warp. Its `eventDeparture` body is canonical
`lua/scripts/quest/scenario/defaulttalk/dftsrt.lua:36-64`, SHA-256
`a8ed70ef14ae6eebce5c403c4982c72b3fbe84f0916409ca052274e97f685d48`.
The linked contract pins its LPB and payload. It hardcodes neither `vsl*`
key, route, destination, nor event owner.

## Unestablished boundary

The resource inventory does not join either scene to a historical invocation
of `DftSrt.eventDeparture`. The native static outbound constructors in
`xivl-decomp:docs/net/ferry-scene-notice-producer.md`, VAs `0x0076D610` and
`0x00763DC0`, likewise do not establish a runtime scene name or active route.
The finding pins `ffxivgame.exe` SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Server event ownership, actual departure/arrival selection, service schedule,
and observed operation specifically in 1.23b remain unresolved.
