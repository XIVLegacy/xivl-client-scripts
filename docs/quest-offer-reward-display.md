# Quest-offer reward display calculation

`QuestDetailWidget` treats reward numeric column 2 as an icon and column 5 as
the amount input. For type -13 it combines that amount with quest column 51
through `Player.calcSkillPoint`, then passes the result to UI text key 5054.
For the same-key 111633 quest/reward rows, the helper's product before its
named ceil call is 5340. The icon value 534 is not a reward amount converted
by a factor of ten.

## Offer row selection

`QuestDetailWidget.initAsk` stores its supplied quest key in `work.questID`
and passes that key to `setRewardData` (`widget/ask/questdetailwidget.lua:38-41,
134-137`). `setRewardData:584-839` loads quest and quest-new-reward sheets at
that key. Its loop starts at base 0, advances by 13, processes entries whose
base+0 is 100, and stops when base+0 is 301, with at most 16 iterations.

Within a processed entry, base+1 selects the type, base+2 supplies the icon,
and base+5 supplies the amount input (639-675). For type -13, the method calls
the local player's `calcSkillPoint(questColumn51, amountInput)` and passes the
returned value to `setItemText(item,"TextBlock_RewardItem",5054,result)`
(761-777). Type -16 is a separate branch using text key 5060 and another field;
it is not the selected 111633 entry.

The column numbers are the original numeric header cells. The leading key
field is not column 0. Authenticated client-extraction rows for key 111633 are:

| Table / row locator | Numeric columns relevant to the offer |
|---|---|
| `quest.csv`, line 492 | 51 = 45 |
| `quest_new_reward.csv`, line 472, first block | 0 = 100; 1 = -13; 2 = 534; 5 = 6 |
| same reward row, block at base 52 | 52 = 100; 53 = -15; 57 = 6000 |
| same reward row, next block | 65 = 301 |

The cited quest/reward fields have type `s32` in the original second headers.
The base 52 entry uses the separate company-seal display branch at 717-747.
It is an offered value, not evidence of receipt.

## Calculation and formatting boundary

`Player.calcSkillPoint` (`chara/player/player_work.lua:675-689`) divides its
second argument by 100, calls `self:getSkillPointMax(firstArgument)`, and returns
`_math.ceil(maximum * dividedAmount)`. This body does not read the player's
current level, job or class, and does not apply a min/max clamp.

`CharaBaseClass.getSkillPointMax`
(`chara/charabaseclass_battle.lua:1895-2027`) has ordered table branches for
arguments up to 10, 20, 30, 40 and 50, followed by a 99999999 fallback. The supplied 45
selects the `<=50` table at 1996-2020 and its index 45-40 = 5. That entry is 89000
(2002,2012). Therefore these retained inputs produce the expression
`_math.ceil(89000 * (6 / 100))`, with product 5340 before the named rounding
call. An authored reconstruction using standard ceil also gives 5340; the
native `_math.ceil` implementation was not executed or analyzed.

`WidgetBaseClass.setItemText` (`widget/widgetbaseclass_common.lua:1859-1871`)
forwards the item/control, `Text` property, numeric text key and arguments to
`setTextProperty`. Its numeric-key branch (3276-3290) calls native
`_setTextProperty`. Exact native rendering/locale selection is outside this
Lua finding.

The independently authenticated `xtx__text_ui.csv` key 5054, line 1729, English
numeric column 1 contains a U+FF5E prefix and
`[@kilo:022206e802ff022c03] experience points`. Key 5052 at line 1727 has the
same carrier and wording without the prefix. These are text-cell contents;
this finding does not reconstruct the native `@kilo` formatter.

## Input and reward-path limits

`QuestBaseClass.getQuestId` returns `_getStaticActorID()`
(`quest/questbaseclass.lua:7-14`). `showQuestInfomation`
(`quest/questbaseclass_common.lua:785-822`) passes that key to
`DesktopWidget.askQuestDetailWidget` for keys 110600-119999 or 110001-110021.
The desktop helper (`widget/desktopwidget_connector.lua:10078-10094`) passes
`("Ask/QuestDetailWidget",1,3,key)` to `askEventModeWidgetYield`. The
receiver glue and historical invocation were not reconstructed. The widget's
supplied-key consumer is established separately by its `initAsk` body.

`QuestRewardWidget` is a separate path: its type -13 branch formats a supplied
second data argument with key 5052 (`widget/ask/questrewardwidget.lua:489-499`).
It does not use the offer calculation in that branch. The
[same-key reward route](quest-event-client-contracts.md#quest-journal-and-reward-presentation-widgets)
records the selector/caller boundary; it does not prove a server grant.

The calculation is compatible with the approximately 5,340 EXP offer in
`xivl-captures:studies/gc-quest-to-kill-a-raven-video-breakdown/derived/evidence-map.md`,
Confirmed, source time 0:15. That picture separately advertises 6,000 Serpent
Seals. It does not identify the historical
runtime quest key or authenticate a recording as the 1.23b client. An offered
amount, a text match and this static calculation do not establish receipt,
server settlement, EXP balance or normal/Hard equivalence.

## Source identity

Canonical decompiled sources are from extraction `2012.09.19.0001` and are
identified in `manifests/scripts.json`:

| Source | SHA-256 |
|---|---|
| `widget/ask/questdetailwidget.lua` | `0d1474c6b43cce61d90a75ba0fe32e2b1d77504fd396024ee32a8876ebc8c8ce` |
| `chara/player/player_work.lua` | `be4e0575c015d537c0fbbe0d103e3d02e95a36a0b4f9c085825669e740e81b04` |
| `chara/charabaseclass_battle.lua` | `ca7d9bd52320e8aa62ecd853a0ce8d9e2e0ddc76fc504729b501b14b9bfcd959` |
| `widget/widgetbaseclass_common.lua` | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| `quest/questbaseclass.lua` | `9c10eeefc10d1017cfec32930f8e3470cb89dba7f327f727063128b75c97f6b8` |
| `quest/questbaseclass_common.lua` | `cf61a5687dbc7b6accd26c8cd3a138decc0372fb72518ac6f2054f125bc1465e` |
| `widget/desktopwidget_connector.lua` | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/ask/questrewardwidget.lua` | `1f12737ea03fbdd931654e3b47fdd745889e86cef5e0793ef2a6c933b1d9a03d` |

`lua/registry.json` preserves ciphered/decoded path mappings;
`manifests/retail_lua_coverage.json` preserves original LPB/payload pins.
This focused check authenticated canonical archived source bytes, not a fresh
LPB decode or decompiler run. It did not execute retail artifacts.

Table identities are `xivl-client-data:manifests/tables.json`:
`quest.csv` SHA-256
`bdadece1907b7050aaeee7c94a2a2d395fe76b504e47cbb1616b57ba380209dc`;
`quest_new_reward.csv` SHA-256
`496d5e7d2e5057852f990e18f404524426d456c52cbcbd95544652494350ff66`;
`xtx__text_ui.csv` SHA-256
`23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
Original numeric/typed headers and selected same-key rows were checked directly
against those pins. Native formatter semantics, runtime invocation and grants
remain unverified.
