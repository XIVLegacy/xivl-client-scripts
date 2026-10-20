# Local guildleve supplies contract

The official manual describes local leve supplies as restricted crafting
inputs, including crystals, outside regular inventory. Owned high-quality
substitutions were a separate inventory expense.
The retained evidence does not recover a retail rule mapping every offered
variant to a recipe, or the Retry and abandon transitions for unused supplies.

## Confidence and source identity

- **A, direct artifact:** authenticated retail data, recovered client behavior,
  or a named capture. The artifact kind limits what the claim establishes.
- **B, documented intent:** the official 1.x manual. This supports the intended
  player contract, without proving the server's internal representation.
- **U, unresolved:** no attributable source selects the claimed rule.

The manual's provenance is owned by
`xivl-captures:sources/lodestone-manual/manifest.yaml:5-18` and its original page
URLs by `xivl-captures:studies/lodestone-manual/derived/file-inventory.csv:22,25`.
The retained `guildleves.md` is 8,037 bytes, SHA-256
`6ced977bff76a843368c8baa1a1200ee6dbc166396ce41c47240596678085953`.
The retained `synthesis.md` is 9,102 bytes, SHA-256
`7ab94e4526395c0388333a9e382c1f8605a0ca452b8283d164dae6504a9b3c84`.
These match manifest entries at lines 1068-1070 and 1116-1118.
The [manual study](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/lodestone-manual/README.md)
explains the documented-intent tier and preservation limits.

## What the player received, and when

| Claim | Confidence | Retail locator |
|---|---|---|
| Local materials were available only for the requested leve items and were outside regular inventory. | B | `xivl-captures:sources/lodestone-manual/objects/pages/guildleves.md:69` |
| The supply included crystals. Players did not need to supply their own items. | B | `xivl-captures:sources/lodestone-manual/objects/pages/synthesis.md:27,31` |
| After speaking to the client and receiving materials, selecting the leve under Requested Items automatically filled the synthesis material slots. The client or Adventurers' Guild could provide materials. | B | `guildleves.md:71`; `synthesis.md:27-29`, in the same manual source directory |
| An owned HQ version could replace an automatically filled material. That owned item was consumed when synthesis began. | B | `synthesis.md:27,31` |
| Completed requested items also stayed outside regular inventory and could not be used, sold or traded. | B | `guildleves.md:73-75` |
| Failed leves could be retried for one allowance. | B; A for the prompt | `guildleves.md:13`; [journal lifecycle](guildleve-journal-lifecycle.md#return-node-retry-and-local-synthesis-prompts), `CraftJudge.askRetryLocalleve`, WorldMaster 50144 |
| Every local leve received its supplies at offer acceptance, rather than at a client handoff. | U | The manual identifies both providers but does not enumerate which commissions use each timing. |
| Retry reissued physical inventory items, or had a particular unused-supply carryover/reset policy. | U | No retained attributable Retry request/response selects this behavior. |

The general synthesis paragraph at `synthesis.md:37` consumes owned crystals at
synthesis start. The explicit local-leve exception at lines 27 and 31 applies
to supplied materials and crystals. Applying the general paragraph to local
supplies would erase that exception. Conversely, the manual's word
"materials" does not prove an inventory grant or a server-side bag of stacks.

## Client data and variant mapping

**A, static data.** Local commissions use `passiveGL_craft`, resource
`0x01030068`, rather than the regional `guildleve` rows. The
[column finding](passivegl-craft-columns.md#columns-8-11) and
`xivl-client-data:docs/guildleve-names.md:72-95` own that distinction and the
independent row-ID-to-`xtx_quest` title join. CSV positions below are zero-based
after the row ID, following `xivl-client-data:tools/mappings/passivegl_craft.py:7-43`.
These are mapping names, not a recovered server schema:

| Block N | `objectiveItemIdN` | `objectiveQuantityN` | `numberOfAttemptsN` | `recommendedLevelN` | `rewardItemIdN` | `rewardQuantityN` |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 13 | 14 | 15 | 16 | 18 | 19 |
| 2 | 21 | 22 | 23 | 24 | 26 | 27 |
| 3 | 29 | 30 | 31 | 32 | 34 | 35 |
| 4 | 37 | 38 | 39 | 40 | 42 | 43 |

The following examples are authenticated `passiveGL_craft.csv` rows. Each
block tuple is `(objectiveItemId, objectiveQuantity, numberOfAttempts,
recommendedLevel, rewardItemId, rewardQuantity)`:

| Row ID; CSV line | Block 1 | Block 2 | Block 3 | Block 4 |
|---|---|---|---|---|
| 120202; 73 | `(8030420,2,4,1,6060008,1)` | `(8030420,3,5,1,8032501,1)` | `(8030420,4,6,1,8070320,1)` | `(8030420,5,7,1,8080615,1)` |
| 120214; 85 | `(9010054,2,4,5,10007101,3)` | `(9010055,3,5,15,10007104,3)` | `(9010056,4,6,25,10007126,3)` | `(9010057,5,7,40,10007116,3)` |

Row 120202 is *A Mother's Frippery*, mapped class 34, with dialogue tuple
`365,366,367,368` at positions 8-11. Row 120214 is *Strapped for Straps*,
mapped class 33, with tuple `337,338,339,340`. Titles are in
`xivl-client-data:derived/local_guildleve_names.csv`, rows 120202 and 120214.
The source file is 26,972 bytes, SHA-256
`2e2b68515f43ba2898bc3c4bf642332bd924687a4d771ba8d8d9733c539cd0ba`,
pinned by `xivl-client-data:manifests/tables.json:4099-4104`.

Neither the objective item nor the reward item is an ingredient field. The
card selector repeats `1,2,3,4,1,2,3,4`, but its connection to these blocks
remains unproved. Positions 8-11 join to `pgConv` dialogue rows, not material
lists, and their phase order varies. See
`xivl-client-scripts:docs/passivegl-craft-columns.md:65-118,228-237`.

**A, static recipe limit.** `recipe`, resource `0x0103018D`, has seven data
rows in this extraction. The CSV header at lines 1-2 has positions 0-14, with
only position 0 typed `s32`. In rows 1000001-1000007 (CSV lines 3-9), position
0 is respectively `3020002,3020003,3020004,3020004,4030004,4100004,3020005`.
Positions 1-14 are empty on all seven rows. No selected objective ID in the
two examples above equals any of those values. This sheet therefore supplies
neither a direct join for these examples nor an ingredient/crystal tuple.
It does not prove that retail had no other recipe provider.
The member is 267 bytes, SHA-256
`0d6eaf4b91a0dcac4c2111eb03f60e02346b24ad9863a0add3d489b2a793d649`,
pinned by `xivl-client-data:manifests/tables.json:4851-4856`.

**A, static text.** `pgConv` 366, English field 1 (CSV line 368), says that
Quartermaster Ayled will prepare the materials before inspection. Its
captured call is listed below. Text 367 (line 369) concerns inspecting and
delivering the finished items, not material quantities. For row 120035,
position 11 instead selects text 106 (line 108), which offers to provide
everything needed. This is narrative evidence of provision, with no item
IDs, quantities or fixed phase-column interpretation. `pgConv.csv` is pinned
at `xivl-client-data:manifests/tables.json:4131-4136`, SHA-256
`2c1ed71fe8c9344a674b1cd8135081195b8dca78fbeb1adbb4887bf1610f2818`.

`worldMaster` 40210 (CSV line 1520, English field 1) describes missing
client-provided materials; 40211 (line 1521) describes having used all supplied
materials. These text rows distinguish receipt from exhaustion, but do not
identify the server checks, their packet senders, or the bundle contents.
Row 50144 (line 1880) offers a reattempt for one allowance and retains rich
text conditional arms. `worldMaster.csv` is pinned at
`xivl-client-data:manifests/tables.json:5891-5897`, SHA-256
`2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`.

## Requested Items and recipe presentation

**A, recovered client behavior.** Retail `CraftCommand` itself has only
`isUseActionGauge` and `canAimForRelation` in the published registry
(`lua/registry.json:14803-14817`). Recipe and material UI behavior belongs to
the judge and widgets. The following eight method bodies identify the input
boundary without recovering a server recipe selector. A1 etc. are positional
arguments after self; prototype PCs and decoded offsets below are zero-based.

| Method; published Lua lines | Raw prototype; PCs; decoded offsets | Supported behavior |
|---|---|---|
| `judge/craft/craftjudge.lua`, `CraftJudge.start:277-439` | `root/proto17`; 0-152; `0x110F-0x136F` | Receives A1-A4 plus varargs. For a player, its normal opening branch passes mode `(A4 == true ? 1 : 0)`, `0`, A3 and the collected vararg table to `selectCraftItemSelectWidget`. A returned slot 0 keeps the corresponding supplied value; a positive slot uses `A1._getExtendedTemporaryItem(1,slot)`. It returns ItemBaseClass objects before other values, without declaring a recipe or material catalog schema. |
| Same script, `CraftJudge.confirmLeve:877-896` | `root/proto26`; 0-14; `0x20E1-0x2119` | If A3 is present, calls `askJournalDetailWidget(7,A3,A4,A6,A7,A8,A9)`. The omitted A5 is not an ingredient grant. |
| Same script, `CraftJudge.confirmRcp:453-470` | `root/proto19`; 0-12; `0x153A-0x156A` | Tailcalls `selectCraftRecipeDetailWidget(A3,A4,A5,A6,A7,A8,A9,A10)` without changing these eight values. |
| `widget/craftstartwidget.lua`, `CraftStartWidget.setInitialItems:1324-1545` | `root/proto20`; 0-192; `0x2E97-0x3197` | In `craftMode == 1`, copies A1-A8 directly into ready slots 1-8. Other modes use recipe helpers and `Grid_MaterialSlot_i` user-work values/counts. The supplied values' catalog/package identity is unresolved. |
| Same script, `setReadyMaterialInSlot:661-688` | `root/proto10`; 0-19; `0x1A88-0x1AD4` | Writes `IntData.Value2` and forwards the unchanged value to `CraftEditWidget.setReadyItem(slot,value)` when the child exists. |
| Same script, `setRecipeToSlot:2139-2192` | `root/proto29`; 0-40; `0x422A-0x42CA` | Handles clear/end sentinels 0/-1, otherwise forwards the slot/value pair to `CraftEditWidget.findItemSetSlot`. No crystal or package transaction is performed. |
| `widget/craftrecipewidget.lua`, `CraftRecipeWidget.setRecipeData:955-1299` | `root/proto11`; 0-293; `0x1C59-0x20E9` | Uses A1 as target item and stores A2 as `work.stack` only when `work.mode == 0`. Displays A3/A4 and A5/A6 required crystal ID/count pairs, A7 license item, A8 placement requirement and A9 facility. It calls `countCrystalInPackage` for displayed owned counts. This is recipe presentation, not a local-leve recipe join or inventory debit. |
| `widget/desktopwidget_connector.lua`, `DesktopWidget.selectCraftRecipeDetailWidget:11142-11222` | `root/proto210`; 0-66; `0x1A4B0-0x1A5B8` | Reads the start widget's facility. Outside recipe mode, directly calls `setRecipeData(A1..A8,facility)`. In recipe mode, passes `false,A1..A8,facility` to the widget opener instead. |

Lua paths in that table are relative to `lua/scripts/`. The readable source
hashes match `manifests/scripts.json`, and original LPB/decoded identities
match `manifests/retail_lua_coverage.json`:

| Script | Original LPB resource; bytes; SHA-256 | Decoded bytes; SHA-256 |
|---|---|---|
| `CraftJudge` | `0p635/7s94q/7s94q0p635.le.lpb`; 10,127; `fda277d6626fd0c381100cadd75628cae7be508f150bb2558364fe647ba07147` | 10,114; `0dff8463d2b685ff65a23afcf5e52e451e531e6fac194fd088adba3d05dbd0ff` |
| `CraftStartWidget` | `n1635q/7s94qrq9sqn1635q.le.lpb`; 22,112; `615f0a8068f1e322256814586a642b2d173e4fc5b633508b54b529fd6704d4e9` | 22,099; `3883c5c7f27535cc1635bfbfa7ef84d197cdd2bcab6ff502575c52ea927b568b` |
| `CraftRecipeWidget` | `n1635q/7s94qs571u5n1635q.le.lpb`; 11,529; `c4f29ad01ba26f092789b59261fc0a839a76580458db6052b7ed13bf2ed825e8` | 11,516; `bfc755d93fc35be5136f545a0adeedf172f9e3e126274a4eedab8e4b4f5a241d` |
| `DesktopWidget` connector | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb`; 213,487; `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | 213,474; `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |

These are value/object and display routes. The literal `1` in
`_getExtendedTemporaryItem(1,slot)` is not promoted to a proven supply package
identifier. The selected capture below supplies one eight-integer tuple.
The general provider that derives such a tuple from the selected commission
and recipe remains unbound. The recipe-mode opener's assignment through
`CraftRecipeWidget.init` is also unqualified here. A method named `initAsk`
does not appear in that widget's registry entry.

## Retained packets, events and text

The acceptance and completion recordings are independent observations, not a
continuous session. Source identities are owned by
`xivl-captures:sources/pcap-1.23b/manifest.yaml`:

| Capture ID | Bytes | SHA-256 |
|---|---:|---|
| `accept_local_leve.pcapng` | 50,676 | `3b4b071d88742a5d3c94a1e29ca6a4074cb6b9a9a60207118302fe22f932bd7c` |
| `local_leve_complete.pcapng` | 358,296 | `4f0793f354140478725bf2c30642a3458a854460f47fb11a7af635c8881d95cd` |

The [publisher capture finding](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/regional-guildleve-publisher-contract/derived/verdicts.md#local-comparison)
records `talkOfferWelcome`, `askOfferPack`, `askOfferRank`, `askOfferQuest`,
`talkOfferDecide` and `finishTalkTurn` on owner `0x44D80009`. The offer contains
120222 and 120202, the client returns index 2, and s2c `0x0137` publishes
`work.guildleveId[8]=202`. This is **A, observed journal insertion**, not an
attributable material grant or allowance debit.

The [local dialogue capture finding](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/local-guildleve-dialogue/README.md#intervening-observations)
owns the following **A, observed wire** rows. Frame and subevent indexes are
zero-based, capture packet indexes one-based, and order is direction-local.
All listed calls are main-lane s2c `0x0130`:

| Frame/subevent; capture packet | Event/method | Supplied integers |
|---|---|---|
| 14/0; 38 | `delegateEvent` / `processPgEvent` | text 365, then `0x151A9000` |
| 25/0; 79 | `delegateEvent` / `processPgEvent` | text 366, then `0x04136000` |
| 58/0; 186 | `delegateCommand` / `confirmLeve` | `120202,2,8030420,0,5,1,0` |
| 195/2; 658 | `delegateCommand` / `askContinueLocalleve` | `120202,8030420,1,3,4` |
| 362/2; 1240 | Same | `120202,8030420,2,3,3` |
| 464/2; 1581 | Same | `120202,8030420,3,3,2` |
| 497/0; 1734 | `delegateEvent` / `processPgEvent` | text 368, then `0x04140000` |

### One captured requested-item material tuple

**A, observed wire and static catalog matches.** The same completion capture
contains a more specific synthesis neighborhood. The following are main s2c
`0x0130` `delegateCommand` calls, wire owner `0xA0F055F1`. Each parameter
block begins with actor `0xA0F4E203`, the method string, then actor
`0xA0F055F1`; the table gives the remaining values:

| Frame/subevent; capture packet; lane event | Method | Remaining typed values | Application SHA-256 |
|---|---|---|---|
| 43/3; 128; 122 | `start` | integer 0, false, eight zero integers | `5d86942a90c9fe60dc62d5bc121d530f41701093c27a7dc7023b6721954d56d7` |
| 53/0; 174; 167 | `selectCraftQuest` | none | `b68997a2d7d43b897815213c1631992a8793db06ec89c6a3391bb8f9357a9cfd` |
| 63/0; 201; 195 | `start` | integer 0, true, integers `10005001,10005001,10007507,10005301,0,0,0,0` | `fbb8a08c55a34e800f1d8b865da768abe3f06679c85f1db8182d6e5515e27cd2` |
| 70/0; 232; 220 | `selectRcp` | integer `8030420` | `5ed68a72a681f8839043a6e5ad03c833e5f6edae9e2f312275da5e6f8a025049` |
| 72/0; 242; 222 | `confirmRcp` | integers `8030420,1,1000007,1,1000005,1,0,0` | `c4392589b87f2ba1a0aaca4128d231baf79535f5f132e4f207cb3c6ebaf493e0` |

All parameter blocks are 64 bytes at application offset `0x49`. The true
`start` has tag `0x03` at parameter offset 22, eight tag-0 integers at
23/28/33/38/43/48/53/58 and END at 63 with no padding. `confirmRcp` has END
at 62 and one zero padding byte. Boolean `0x03`/`0x04` means true/false, each
one byte, as established by
`xivl-decomp:docs/script/delegate-command-producer.md:96-115`. These eight
supplied values are integers, not tag-6 actor references. The same `start`
false/zero block recurs at frame 469/0, packet 1597, lane event 2107.

The exact catalog matches are:

| ID | English name | Observed role/value | `xtx_itemName.csv` line |
|---:|---|---|---:|
| 10005001 | Undyed Hempen Cloth | Two occurrences in the eight supplied integers | 5250 |
| 10007507 | Mole Sinew | One occurrence | 5458 |
| 10005301 | Hempen Yarn | One occurrence | 5295 |
| 8030420 | Hempen Dalmatica | `selectRcp` value and first `confirmRcp` integer | 2386 |
| 1000007 | Lightning Shard | `confirmRcp` integer followed by 1 | 11 |
| 1000005 | Wind Shard | `confirmRcp` integer followed by 1 | 9 |

Names use `xtx_itemName` data position 5 after the row ID (zero-based whole-row
field 6), as
mapped by `xivl-client-data:tools/mappings/items.py:4-9`. The 4,428,170-byte
member is pinned by `xivl-client-data:manifests/tables.json:6163-6168`, SHA-256
`917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2`.

The admitted `confirmRcp` and connector bodies bind the eight confirmation
integers unchanged to `setRecipeData` on the non-recipe branch. There the
required crystal inputs are Lightning Shard `1000007 x1` and Wind Shard
`1000005 x1`, with target item `8030420`, stack 1, license 0, placement 0
and facility supplied by the start widget. This is **A, conditional client
argument mapping**, not an observed debit. On the recipe-mode branch the
widget opener carries the same values plus inserted mode/facility, but the
final initialization assignment is not established by these inspected bodies.

This is a concrete material-presentation specimen for the 120202 crafting
neighborhood, not an acceptance inventory grant or a total-commission supply
count. Two cloth slot occurrences are not proof of how the server stored or
replenished that material. The requested item, target count 3 and initial
five-attempt value are consistent with mapped block 2 of row 120202. That
consistency does not prove the general selector or a derivation for other
variants. The reflective delegate's object resolution and selected binding
remain conditional as documented in
`xivl-decomp:docs/script/delegate-command-producer.md:3-8,82-86,149-162`.
Wire owner bits alone do not identify a historical player object or successful
Lua invocation.

### Progress, completion and Retry boundaries

`processPgEvent`'s wire owner is `0x44B00005`, separate from its serialized
player and quest actors. It displays the supplied `pgConv` text ID through
`PassiveGuildleveBaseClass.processPgEvent`; it does not select a sheet column.
The [dialogue producer finding](passivegl-dialogue-producer.md#intervening-craft-progress) identifies
the five `askContinueLocalleve` values as leve, requested item, current count,
target count and remaining attempts using `craftJudge` text 26. Thus the
observed count/attempt pairs are 1/3 with 4 left, 2/3 with 3 left, and 3/3 with
2 left. These are supplied presentation values, not ingredient quantities.

The same capture has s2c `0x0133` `attention` values
`40119,120202,1,3` (frame 191/7, packet 648),
`40119,120202,2,3` (357/7, packet 1230), and `40121,120202`
(461/14, packet 1576). These are progress/completion-neighborhood values,
not a supply grant. `0x0137` checked/done/zero writes likewise do not prove
an abandon or unused-supply mutation. The completion recording lacks a
nonzero slot-8 ID baseline, so its state writes cannot be joined to 120202
using the independent acceptance recording.

After text 368, completion-capture s2c frame 501 (packet 1751) contains three
generic inventory brackets. Their subevents are `0x016D` at 0/5/10,
`0x0146` at 1/6/11, `0x0148` at 2/7/12, `0x0147` at 3/8/13 and `0x016E`
at 4/9/14. **A, observed carrier sequence; U, supply attribution.** An item
record in this neighborhood is not evidence that materials were granted on
acceptance, reissued on Retry, or removed on abandon. No recipe, selected
variant or supplied-object join identifies it as such.

The local journal client request is
`command(24241,journalID,subindex,nil,nil)`, with Break `3` and Retry `5`.
The [journal lifecycle](guildleve-journal-lifecycle.md#command-mapping) and
`xivl-client-structs:manifests/guildleve_lifecycle.json:410-460` own its generic
c2s `0x012D` `commandRequest` carrier and the unbound response.
`CraftJudge.askRetryLocalleve` displays WorldMaster 50144 with choices
50145/50146, then 50149 with 50150/50151 on the abandon branch. These are
**A, client prompt routes**. They contain no inventory transaction.

The [journal wire census](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/guildleve-journal-command-wire/derived/verdicts.md)
found no structurally identifiable command 24241 request among its 54 captures
and 84 admitted clear-game lanes. Consequently no retained response is
attributable to local Retry `5` or Break `3` under that model. This bounds
retained evidence, not historical behavior outside the corpus.
The generic carriers indexed by `xivl-opcodes:opcodes.json` do not, by their
names alone, identify a supplied-item add, a removal, or a Retry regrant.

## Consumer contract and missing discriminators

An implementation can promote the following documented contract:

1. Keep provided local-leve inputs and outputs outside ordinary inventory.
   Scope them to the accepted commission and its Requested Items synthesis.
2. Include required crystals in the supplied inputs. A craft using only those
   inputs must not debit the player's normal ingredient or crystal stacks.
3. Debit an explicitly selected owned HQ replacement when synthesis begins.
   Do not treat all automatically filled slots as owned inventory selections.
4. Represent material receipt separately from the existence of the accepted
   leve. The client/Guild provider distinction must remain representable.
5. Present failed Retry as costing one allowance, while keeping its accepted
   server transaction and supply transition separate from the prompt.

This is an observable contract, not a recovered server storage design. An
attempt counter can represent consumable synthesis opportunities, but the
evidence does not prove that resetting attempts alone recovers the whole
material-receipt and recipe-selection contract.

Exact per-variant supplies require an attributable join from the selected
local-leve variant to its synthesis recipe/material tuple. Recipe output
matches and objective/reward columns do not supply that selector. Exact Retry
behavior additionally requires a request-correlated response showing whether
material receipt is retained or repeated, which recipe remains selected, and
how unused supply opportunities change. Abandon requires its own attributable
transition. No ordinary-inventory leftover removal or retention rule follows
from supplies that were never ordinary inventory stacks.

The captured Hempen Dalmatica material integers and conditional crystal tuple
are suitable as a bounded presentation fixture. They do not justify
multiplying a recipe by the mapped attempt count to invent an acceptance or
Retry grant. The missing discriminator is the authoritative variant/recipe
provider and its material-receipt transition, followed separately by the
request-correlated Retry or abandon supply-state transition.
