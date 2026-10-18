# Seasonal event actor client contracts

## LemmingEventMoon2011 local class boundary

The canonical decoded member
`lua/scripts/chara/npc/monster/lemming/lemmingeventmoon2011.lua` is 195 bytes,
SHA-256 `ca43e47af4243b56a86ebcbd627e266c4b1b882618742225f932170b0944c5e6`.
It matched [manifests/scripts.json](../manifests/scripts.json), SHA-256
`86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`,
and the selected member in the decoded corpus archive, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Python ZIP reading and direct text inspection found only the require of
`/Chara/Npc/Monster/Lemming/LemmingBaseClass` and class definition
`LemmingEventMoon2011`, inheriting `LemmingBaseClass`, at lines 1-8.

No local method is present in this exact canonical decompile. The parent
class was not inspected for this finding. This does not establish an event
binding, monster placement, drop rule, quest or absence of inherited behavior.

## Valentione town-type selector

The 1.23b LPB at
`client/script/729s9/wu7/uvupy975/uvupy975o9y5wqx9rq5s.le.lpb`
has SHA-256
`cb03cf8f51b9ca0afff0f0e0c5def04d2870ac25adfcd606ac5b03ec954f83d8`.
`xivl-client-structs:tools/decode_lpb.py` produces Lua 5.1 bytecode
SHA-256 `024262c234b3d0623331c15896ece668cfb54610e79fd240f1942c7e0fef143b`,
identical to the independently recovered chunk. Its decompiled Lua text has
SHA-256 `978fe83761276859afcfd0fb9f1d9bf95a3a93f7401b4f4fa4f43ed229e09d2c`;
it is a separate decompile from the canonical corpus hash in
`manifests/scripts.json`. `lua/registry.json` maps the ciphered resource to
`chara/npc/populace/populacevalentmaster` and class
`PopulaceValentMaster`.

In `PopulaceValentMaster.getTownMasterType`, the recovered method compares
`getActorClassId()` and returns:

| Return | Compared actor class IDs |
| ---: | --- |
| 1 | `1001841`, `1001844`, `1001847` |
| 2 | `1001842`, `1001845`, `1001848` |
| 3 | `1001843`, `1001846`, `1001849` |
| 0 | Other IDs |

`valentAfirstAsk`, `valentANowTribe`, and `valentAchocolateGet` consume the
returned town type in dialogue arguments; `valentAfirstAsk` also presents
`askExtendWidget` row 3 with five options. `initForEvent` loads text set
8032, which is a text identifier in this call, not a weather command.

The comparison is direct client-script evidence for how this method treats
those IDs when invoked. It does not establish a retail registry binding from
each actor class ID to this script path, a city label for each return value,
an actor spawn, event availability, chocolate grant, or server-side choice
handling. The separate seasonal quest script calls are in
[Seasonal quest client contracts](seasonal-quest-client-contracts.md).
