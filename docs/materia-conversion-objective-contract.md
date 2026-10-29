# Materia conversion objective and result boundary

Quest `110812`, **Forging the Spirit**, is the recovered materia-conversion
tutorial. Its class is `/Quest/Scenario/Etc/Etc102`, and its journal explicitly
asks for a piece of gear to be converted into materia. The server receipt
that advances that objective remains **UNESTABLISHED**. The separate
conversion command `24240` and its result display do not establish that edge.

## Quest identity and objective

| Quest | Recovered identity and instruction | Source and locator | Confidence and boundary |
| --- | --- | --- | --- |
| `110812` | `Forging the Spirit`; `/Quest/Scenario/Etc/Etc102`; level `18`, eligibility `All`. Wil journal row `434` asks the player to convert a piece of gear into materia using Swynbroes's loaned device. | `xivl-client-data:csv/xtx_quest.csv`, row `110812`, columns `2,14,41`; `csv/quest.csv`, row `110812`, column `51`; `manifests/staticactor_class_paths.json`, entry `110812`; `csv/xtx_journalxtxWil.csv`, row `434`, English column `1`. | High for extracted identity and objective text. No server state predicate is recovered. |
| `110813` | `Joining the Spirit`; `/Quest/Scenario/Etc/Etc103`; the dialogue teaches gathering catalysts through Fingerprints of the Gods and later praises obtaining a catalyst. | Same title/class artifacts, entry `110813`; `xivl-client-data:csv/etc103.csv`, English column `1`, rows `2,6,11,13-17`; `lua/scripts/quest/scenario/etc/etc103.lua:11-307`. | High for the catalyst tutorial. It does not identify the conversion objective. |
| `110814` | `Waking the Spirit`; `/Quest/Scenario/Etc/Etc104`; the separate melding/tool quest. | [Quest 110814 and the melder tool](materia-meld-client-contract.md#quest-110814-and-the-melder-tool). | Reused static contract. Its grant, dispatch and runtime gate limits remain unchanged. |

Column numbers exclude the row key. Quest `110812` column `14` contains
conditional references to `xtx/journalxtxWil` row `434`. Its compact row
operand `f2 01 b2` is `434`, not a neighboring row or a quest-state value.
Columns `46-50` reference row `433`, whose English text describes learning
from Swynbroes before the test. The integer rule is
`xivl-tools:src/formats/src/richstring.rs`, `decode_integer`.
The active conditional branch and server objective encoding are not
established by these text references.

`Etc102.initText` loads resource `7408,"etc102"`. The offer method returns
the single `showQuestInfomation` result; equality to `1` selects instruction.
That is an offer decision, not a conversion receipt.
`processEvent_000` checks current package-1 items using
`checkEquipItemMaterialize`, then presents suitable, unsuitable or
insufficient-spiritbond guidance. The helper reads the current item,
`getNormalItemFitness` and `getMaterializePermission`. It does not test that a
conversion occurred or compare before/after inventory.

`processEvent_005` presents row `22`, which praises a first materia creation.
Its supplied fourth positional argument equal to `1` selects row `23`;
the other branch selects row `24`. The remaining dialogue discusses melding
and the device. The method finishes the talk turn and returns zero values.
Its scheduler, wait and dialogue calls do not grant an item, write quest
state, inspect the converted gear or explain why this event was selected.
Completion narration therefore does not establish the server's completion
test.

Canonical Lua: `quest/scenario/etc/etc102.lua:11-460`, especially
`processEvent_000:254-341`, `checkEquipItemMaterialize:345-373` and
`processEvent_005:377-460`. Text: `xivl-client-data:csv/etc102.csv`, English
column `1`, rows `13,15-19,22-26,36-37`.

## Separate conversion command

`ItemListWidget.operateMaterialize` opens `Ask/MateriaDialogWidget` with
data mode `1` and the selected inventory index after local eligibility
checks. The dialog's mode-1 `Button_OK` branch calls
`DesktopWidget.executePlayerMaterializeCommand(index)` and closes the dialog.
These checks and UI closure do not acknowledge a server transaction.

The helper resolves `getItem(localPlayer,1,index)`. A missing item returns
one `false`; otherwise it tail-returns:

```text
executePlayerCommandLocal(24240,item)
```

The existing fixed wrapper supplies its remaining eight nil operands.
Command `24240` maps to `/Command/System/ItemMaterializeCommand`.
Its `command.csv` priority column `29` is `-1` and craft-judge column `32`
is `false`, selecting the existing `commandRequest` Lua route.
`ItemMaterializeCommand.canFire` and `isDesktopCommandMode` each return one
`true`. These local booleans do not establish transmission or acceptance.
The [command transport](bazaar-retainer-client-contracts.md#command-identity-and-route)
owns the inherited request and conditional native fallback boundaries.

`ItemMaterializeCommand.showResult(A0,A1,A2)` calls
`A1:_createVirtualItem(A2,1,1)`, then
`openEventModeWidgetYield("Ask/MateriaInformWidget",true,virtualItem)`.
If opening returns exactly `true` and the subsequent widget lookup is nonnil,
it shows that widget, calls `_wait(3)` and closes the event widget. It returns
zero values.
The supplied `true` selects positive result presentation; it is not a
returned transaction-success flag. This body supplies no original gear
identity, item removal, persistent materia insertion or quest-state write.
Its incoming selector and invocation arguments are unobserved here.

Canonical Lua: `widget/itemlistwidget.lua:4928-5064`,
`widget/ask/materiadialogwidget.lua:11-179,240-395`,
`widget/desktopwidget_connector.lua:18634-18648`, and
`command/system/itemmaterializecommand.lua:11-66`.
Static command mapping: `xivl-client-data:manifests/staticactor_class_paths.json`,
entry `24240`; `csv/command.csv`, row `24240`.

## Receipt and state qualification

| Item/objective | Receipt or transition | Closest proven retail fact | Source and locator | Confidence | Remaining gap and finite source boundary |
| --- | --- | --- | --- | --- | --- |
| Quest `110812` conversion objective | **UNESTABLISHED**: packet, item-change condition or script callback that advances the objective. | Wil row `434` explicitly requests gear conversion; `Etc102.processEvent_005` narrates first creation and returns no values. | [Quest identity and objective](#quest-identity-and-objective); original Etc102 prototype `0.5`, text CALL PC `14` at `0xAFD`, RETURN PC `63` at `0xBC1`. | High for static identity, text and callback behavior; no authoritative receipt attribution. | A conversion occurrence causally joined to the selected quest objective/state transition and event selector. The exact quest/class, its journal/text, all six Etc102 methods and the conversion caller/result prototypes supply no such join. |
| Conversion command `24240` | **UNESTABLISHED**: attributable acceptance/refusal, persistent gear-to-materia mutation and quest consequence. | Selected package-1 item reaches the local command helper; separately, `showResult` creates a virtual item from supplied `A2` and presents it. | [Separate conversion command](#separate-conversion-command); connector `0.424`, TAILCALL PC `14` at `0x2765F`; command `0.2`, creation CALL PC `4` at `0x1B2`, RETURN PC `28` at `0x212`. | High for the static local calls; request-to-result pairing remains unobserved. | Executed request/item identity -> actual incoming receiver/selector/full arguments -> authoritative removal/insertion -> quest-state update. Local true, positive presentation and a generic inventory callback cannot replace this chain. Finite sources are the exact conversion command, selected ItemList/Dialog/connector methods and the quest resources above. |

No received numeric opcode or required inventory-event order is established
for this objective. The shared item-publication machinery described in
`xivl-client-structs:docs/bazaar-native-wire-contract.md#incoming-package-operations-and-publication`
only explains how compatible received state can become visible. It does not
attribute that state to conversion or quest `110812`. The inspected quest and
conversion resources identify no attributable retained transaction.
The separate melding selector ceiling is unchanged. New retail acquisition
is unavailable.

## Source identity and reproduction

Extraction `2012.09.19.0001`, retail 1.23b. The decoded archives matched
[`private_lua_corpus.json`](../manifests/private_lua_corpus.json) and
`xivl-client-data:manifests/private_csv_corpus.json`. Each selected decoded
member matched its size and SHA-256 in
[`scripts.json`](../manifests/scripts.json) or
`xivl-client-data:manifests/tables.json`. The original LPBs and decoded
payloads matched [`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).

The selected CSV member SHA-256 values are:

| Member | SHA-256 |
| --- | --- |
| `xtx_quest.csv` | `938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719` |
| `quest.csv` | `bdadece1907b7050aaeee7c94a2a2d395fe76b504e47cbb1616b57ba380209dc` |
| `xtx_journalxtxWil.csv` | `80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694` |
| `etc102.csv` | `9638d77dff45a7c7fb56c150815df7e42c267590d5510b8018f63e7b68c02e7b` |
| `etc103.csv` | `e36ef00a85aaef3082ff8af9063c1f4bef7a1e346d26a99bc3c50e7034847008` |
| `command.csv` | `14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848` |

Instruction observations used `tools/retail_script.py:decode_lpb` and the
Lua 5.1 `ChunkReader`, control-flow states and instruction decoder in
`tools/build_quest_contracts.py`, without running the client. Prototype
indices and PCs are zero-based; offsets identify the decoded payload.

| Decoded member below `lua/scripts/` | Decoded payload SHA-256 | Selected original locators |
| --- | --- | --- |
| `quest/scenario/etc/etc102.lua` | `8f187da6e458a905e628261db1e95c5021830c1e38940529eeae220ee6aad3d8` | Text load `0.0` PC `3`, `0x1B5`; offer `0.1` PC `31`, `0x294`; equipment helper `0.4`; event `0.5`. |
| `quest/scenario/etc/etc103.lua` | `68c453457905c8d0c12c5f0559cf84feecb4c81d0d8b604b09bb682665375232` | Text load `0.0` PC `3`, `0x183`; catalyst-success text `0.4` PC `14`, `0x7E5`. |
| `command/system/itemmaterializecommand.lua` | `c4e9b0572601b84436cf35bce6b3920d165f41ae73181075cc75f99b4ebe2450` | `showResult` `0.2`, presentation CALL PC `10`, `0x1CA`; zero-value RETURN PC `28`, `0x212`. |
| `widget/itemlistwidget.lua` | `f92b2bef0eac76acfc8896da338275659e14a8b826d944cc39634eb6defadded` | `operateMaterialize` `0.55`, child-widget CALL PC `77`, `0x925C`. |
| `widget/ask/materiadialogwidget.lua` | `2caff3e69962c1c19a10b90fe3880326e7de7d9051c3812280624519cb1922ab` | Mode-1 confirmation `0.2`, helper CALL PC `10`, `0x4E8`; close CALL PC `31`, `0x53C`. |
| `widget/desktopwidget_connector.lua` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` | Conversion helper `0.424`, item lookup CALL PC `6`, `0x2763F`; command TAILCALL PC `14`, `0x2765F`. |
