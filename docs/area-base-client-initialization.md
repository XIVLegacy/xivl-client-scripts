# Area-base client initialization

`AreaBaseClass._onInit` declares area work fields for `actorNumber`,
`isInstanceRaid`, and `isEntranceDesion`. It stores parameter `A2` in
`areaWork.isInstanceRaid` and `A3` in `areaWork.isEntranceDesion`, passes `A2`
to `_setInstanceRaid`, and sets the loop interval to 1. The
`isInstanceRaid()` and `isEntranceDesion()` getters return those stored fields.
This records the client call and retained values; it does not establish the
native effect of `_setInstanceRaid` or justify changing any server bind flag.

When the `desktopWidget` actor does not exist, `_onInit` calls
`loadCommonTableData` with the current region and zone name, then calls
`_loadSpreadSheetPermanently`. The separately recovered
`AreaBaseClass.loadCommonTableData` body prepares the `tribe`, `quest`,
`quest_reward`, `quest_new_reward`, `guildleve`, `guildleve_UI`,
`passiveGL_craft`, `passiveGL_icon`, `shopBase`, `shopItem`, `marketItem`,
`gcSealShopItem`, `gcRank`, `blackMarket`, `itemGcExSupply`,
`itemHamletSupply`, `materia`, `compatibility`, `mapNavi_data`,
`aetheryte_2Dmap`, `guildlevePack`, and `achievement` sheets. These are
client-side preparation calls, not proof of table contents or runtime
availability.

`PrivateAreaBaseClass._onInit` forwards its incoming initialization arguments
to the superclass, creates an empty `privateAreaWork._save` table and a
`privateAreaWork._temp` entry named `_assignForChild` with value 64, then calls
`init(_getZoneName())`. The class's own `init` body is empty. This records the
base-class initialization shape; it does not establish private-area entry
policy or a runtime owner.

The inn-only `cutReplaySheet` creation and finalization path is documented in
[Cutscene replay and skip client contract](cutscene-replay-skip-contract.md#inn-replay-selection).

## Provenance

The 1.23b `AreaBaseClass` source is
`lua/scripts/area/areabaseclass.lua`, SHA-256
`ebc3601cab6c59afbf0234dd4a35e879567ad44b13b4252948adcdb4b51237a8`.
Its LPB is `9s59/9s5989r57y9rr.le.lpb`, SHA-256
`6f4607febef2f74a1a6da45bda66b2763e0d70f00059999228b80c2e280b00f7`; the
decoded 4,641-byte payload SHA-256 is
`de04f1b74fd9a79e56316eb79231592e1f98a21333526e2a95fe8f0552644239`.
The separate layout source is `lua/scripts/area/areabaseclass_layout.lua`,
SHA-256 `ab17a0177b7f7777887997a5dec3cd29a56c4f7d4ca32ae27743f65821b27add`.
Its LPB is `9s59/9s5989r57y9rr_y9lvpq.le.lpb`, SHA-256
`468fb9d3417c0fd5f7d4859513ac11535c67d76643a61bff00abd3157cf09e2e`; the
decoded 822-byte payload SHA-256 is
`10d4bd6ef474707961c77c4ef2d125f776737cbbbea5cbb9d676928ac6534e25e`.
Both resources are classified `matched-script` in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json), with source
identities in [`scripts.json`](../manifests/scripts.json).

`PrivateAreaBaseClass` is
`lua/scripts/area/privatearea/privateareabaseclass.lua`, SHA-256
`3261a08d2c5fabfd300d75b5427047038549971e80ecf4b605026af7c56346c2`.
Its LPB is
`9s59/us1o9q59s59/us1o9q59s5989r57y9rr.le.lpb`, SHA-256
`63be0189b6cac0fed88966cc9617d7e022c2414d6ed10721368c73b13476e988`; the
decoded 440-byte payload SHA-256 is
`fe4c23c939d9597dfb9cd4bb0577c3c72fc65c3f5b42e13b62e5ffd36cbbe6f1`.
