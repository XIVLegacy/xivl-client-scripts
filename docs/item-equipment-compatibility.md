# Item compatibility eligibility

The retail item helper uses an item compatibility key and the actor's active
class or job to decide whether a simple equipment check can proceed. This page
records that narrow client contract. It does not promote a server equipment
policy, item unlock rules, tribe policy, or compatibility-based combat scaling.

## Evidence identity

The helper belongs to extraction `2012.09.19.0001`. Its committed script
identity is recorded at
`xivl-client-scripts:manifests/scripts.json:9729-9732`:
`lua/scripts/item/itembaseclass_common.lua`, 87762 bytes, SHA-256
`7620492917230C3E060ED84D3197BF164C234A3AB73E48A0939BC65107F6B7FA`.

The decoded corpus input is pinned by
`xivl-client-scripts:manifests/private_lua_corpus.json:2-14`: source commit
`40006d5d716583d78690a6f3ef50ca1bc41dddee`, source archive path
`extracted/ffxiv-1.23b/client-scripts/lua.zip`, and archive SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.

## Recovered helper contract

The following method relationships are recovered from
`item/itembaseclass_common.lua`:

1. `getItemCompatibilityKey` reads item-data field 48.
2. `getItemCompatibilityData` reads the compatibility sheet at the item key
   and column `8 + (skill - 1)`, then divides the stored integer by 100.
3. `getItemCompatibility` supplies the actor's value from
   `getMainClassOrJob` as the skill argument.
4. `canEquipSimple` rejects an exact compatibility value of zero before it
   applies tribe and required-level checks.

The fourth relationship supports a nonzero compatibility eligibility check.
It does not establish that every nonzero percentage is equivalent for combat
calculation, and it does not define the server's class, job, soul, level, or
tribe rules.

## Compatibility table identity

The compatibility table is identified by
`xivl-client-data:manifests/tables.json:1059-1062` as
`csv/compatibility.csv`, with SHA-256
`0B084A0AA4AB01AB2E2A3DE4BA0EE9C97257D5766F7855841D705854C0D862FE`.
The decoded CSV input pin is
`xivl-client-data:manifests/private_csv_corpus.json:2-14`: source commit
`8b38a02ce8ebf662b931092e46273251b38c58f0`, source archive path
`extracted/ffxiv-1.23b/client-data/csv.zip`, and archive SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.

The column convention is documented at
`xivl-client-data:docs/command-battle-params.md:31-47`: skill `N` reads
compatibility column `8 + (N - 1)`. The table's observed cell values are
`0`, `1`, `10`, `45`, `60`, `80`, and `100`; the client gate treats only the
zero result as ineligible.

The job-skill row identities are the compatibility keys 2119 through 2125,
joined to `xivl-client-data:csv/xtx_text_skillName.csv`. The table identity is
`xivl-client-data:manifests/tables.json:6379-6383`.

| Compatibility key | Skill id | Job |
|---:|---:|---|
| 2119 | 15 | MNK |
| 2120 | 16 | PLD |
| 2121 | 17 | WAR |
| 2122 | 18 | BRD |
| 2123 | 19 | DRG |
| 2124 | 26 | BLM |
| 2125 | 27 | WHM |

These row identities describe the source table join. They do not imply that a
weapon or item grants a job, and they do not replace the server's existing
class, job, soul, or level checks.
