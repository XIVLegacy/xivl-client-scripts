# Personal chocobo lender client contract

This contract records the retail Lua surface of
`PopulaceChocoboLender`. It covers the personal-chocobo, rental, naming, and
barding paths without assigning names to caller values that the client does
not derive.

## Source and bytecode identity

The canonical class body is
`lua/scripts/chara/npc/populace/populacechocobolender.lua:1-1235` (source
SHA-256
`e3484f0a4adf83af895cc44fc18d69fcbf56304df0827c92c67a05bc08d9fdbf`). Its
retail resource is
`client/script/729s9/wu7/uvupy975/uvupy97572v7v8vy5w65s.le.lpb` (raw
SHA-256
`96ca9040e4e957140a0c29e8c687390a4f6604e0e59cee2052b706f365735c3b`,
decoded payload SHA-256
`76ec72f06dc67812f845cc9a715222d43134fbe11a8b120e16cd532248317395`).
The source and both LPB identities were matched through
`manifests/scripts.json` and `manifests/retail_lua_coverage.json`.

The naming widget called by `eventSetChocoboName` is
`lua/scripts/widget/ask/chocobonamingwidget.lua:1-322` (source SHA-256
`f8ba0c847b7a09bf0ed447ba780b3b7c61e7b0ffe7619730f2257b96a485b3e8`). Its
retail resource is
`client/script/n1635q/9rz/72v7v8vw9x1w3n1635q.le.lpb` (raw SHA-256
`cb07607799967f94e0d16389de2a078325aaadde13c5fb25ff1bf24fe017d653`,
decoded payload SHA-256
`875be316863f3bf0f2d6ce720ef4e292bde89a754d8dd79dbeba337c80653e67`).

Static checks used `tools/retail_script.py decode_lpb` and
`tools/build_quest_contracts.py` (`ChunkReader`, `instruction`, `call_record`,
`states_for`, and `walk`) for the prototype arities, calls, branches, and
returns below. Decompiled control flow was accepted only where it agreed with
the source and decoded instruction stream.

Every function below is a fixed Lua prototype (`vararg=false`). The decoded
prototype numbers and instruction counts are included to corroborate the
source arity and return sites:

| method | source lines | prototype | parameters including `self` | instructions | return shape |
| --- | ---: | ---: | ---: | ---: | --- |
| `initForEvent` | 11-68 | 0 | 1 | 48 | no explicit return |
| `eventTalkWelcome` | 71-129 | 1 | 2 | 47 | no explicit return |
| `eventAskMainMenu` | 132-231 | 2 | 8 | 100 | selector, or selector plus wardrobe code |
| `eventUseMyChocobo` | 234-329 | 3 | 3 | 81 | Boolean |
| `eventUseRentalChocobo` | 332-458 | 4 | 4 | 108 | Boolean |
| `eventInformationRental` | 461-560 | 5 | 1 | 86 | no explicit return |
| `eventTalkMyChocobo` | 563-630 | 6 | 2 | 54 | no explicit return |
| `eventSetChocoboName` | 633-650 | 7 | 2 | 12 | naming-widget result |
| `eventAfterChocoboName` | 653-719 | 8 | 3 | 54 | no explicit return |
| `eventCancelChocoboName` | 722-750 | 9 | 2 | 19 | no explicit return |
| `visibleChocobo` | 753-784 | 10 | 5 | 24 | no explicit return |
| `eventLookChocoboWare` | 787-935 | 11 | 2 | 130 | no explicit return |
| `eventSelectChocoboWare` | 938-1176 | 12 | 3 | 208 | integer code |
| `eventTalkStepBreak` | 1179-1235 | 13 | 2 | 46 | integer `0` |

## Initialization and town fields

`initForEvent(self)` loads text data 7604 under
`populaceChocoboLender`, constructs `townId` and `companyRank` schema entries
declared as `integer8`, and calls `initWork(nil, schema)`
(`populacechocobolender.lua:11-35`). The call is
`initWork(self, nil, townCompanySchema)`. The shared NpcBaseClass helper
declares `(self, A1, A2, A3)` but writes `A2` to `work._temp` and `A3` to
`work._sync`, so this three-argument call places the supplied schema in the
helper's `_temp` position and defaults `_sync` to `{}`. The native method
wrapper preserves this argument list, as established in the linked door
contract. The source sets `work.townId`
and `work.companyRank` directly after that call. It sets `townId` by actor
class. The helper's full byte identity and static locator are canonical in the
[door contract](map-object-door-client-contract.md#doorstandard-initialization).

| actor class ID | `work.townId` |
| ---: | ---: |
| 1500006 | 1 |
| 1500061 | 2 |
| 1500059 | 3 |

The `1000840` branch is empty, so this source does not assign it a town. It
then stores `work.companyRank = 31` and calls `_setGroundOn(false)`
(`populacechocobolender.lua:39-68`). No later function in this class reads
`companyRank`; it is not a demonstrated rank gate.

The personal issuance prerequisite is outside this lender class. The frozen
client-data notes name `2001004` Storm, `2001005` Serpent, `2001006` Flame
Chocobo Issuance, and `2001007` Chocobo Whistle as the relevant key items
(`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md:1425-1427`).
The lender source contains none of those IDs and does not call `hasItem` for
them. `eventUseMyChocobo` checks the menu result and calls
`A1._getBelongGrandCompany() > 0` only to decide whether to create the selected
cutscene; the accepted choice still returns `true` after the dialogue path.
Thus this class supplies no concrete issuance-item check or company-rank check.
In `eventAskMainMenu`, `A4`, `A5`, and `A6` are caller-provided macro flags,
not item IDs; local `A5` is forced false for actor class 1500059 or when the
player company does not equal `work.townId` (`populacechocobolender.lua:132-150`).
Rental is a separate path: it checks caller-supplied `A2` and `A3` plus the
wallet lookup described below, and neither grants nor checks the personal
issuance or whistle items.

## Talk and menu events

`eventTalkWelcome(self, A1)` starts talk turn 2 with `A1`, runs character
scheduler 353959936, and selects the welcome text from the actor class
(`populacechocobolender.lua:71-129`). It has no explicit return. The source
does not name the type of `A1` at this entry point.

`eventAskMainMenu(self, A1, A2, A3, A4, A5, A6, A7)` is the menu dispatcher
(`populacechocobolender.lua:132-231`). `A1` is a player-like object because
the method calls `A1._getBelongGrandCompany()` and passes it to the child
events. `A2` and `A3` are forwarded unchanged to `eventUseRentalChocobo`;
`A4`, `A5`, and `A6` are caller-provided macro flags; `A7` is forwarded to
`eventUseMyChocobo` and `eventSelectChocoboWare`. For actor class 1500059 the
method forces `A4`, `A5`, and `A6` to `false`. It also forces the local copy
of `A5` to `false` when `A1._getBelongGrandCompany()` does not equal
`work.townId`.

The exact menu macro argument order, including the explicit receiver and the
two repeated lender-self arguments, is
`worldMaster.askMultipleTextMacro(worldMaster, self, self, 1, 104, 7, 1, A4,
A5, A6, gatedA5, true, true, true, work.townId, 0, 0, 0, 0, 0, 0)`
(`root/proto2` PC 39 / offset 1736). The four values `A4`, `A5`, `A6`, and
`gatedA5` are menu flags; the call contains no issuance-item ID.

The menu macro result has these client-visible outcomes:

* `1` returns `1`.
* `2` calls `eventUseMyChocobo(A1, A7)`; a true result returns `2`, while a
  false result reopens the menu.
* `3` calls `eventSelectChocoboWare(A1, A7)`; a nonzero result returns two
  values, `3` and the selected code, while zero reopens the menu.
* `4` calls `eventLookChocoboWare(A1)` and reopens the menu.
* `5` calls `eventUseRentalChocobo(A1, A2, A3)`; a true result returns `5`,
  while a false result reopens the menu.
* `6` calls `eventInformationRental()` and reopens the menu.
* `7` returns `-3`.
* Any other result returns `0`.

The fixed prototype and those return branches are also present in decoded
prototype 2; the menu macro is at PC 39 / offset 1736, and the return sites are
offsets 1752, 1792, 1840 (two values), 1908, and 1972.

## Personal and rental paths

`eventUseMyChocobo(self, A1, A2)` invokes the exact macro call
`worldMaster.askMultipleTextMacro(worldMaster, self, self, 1, 78, 2, 0, true,
true)` at `root/proto3` PC 36 / offset 2511. On choice 1 it calls
`self.say(self, self, textId, 0)`, then
`worldMaster.say(worldMaster, self, 33)`, and starts the selected actor-class
cutscene with `cutScene.startCutScene(cutScene, 1, 61, 1, 0, A2)`.
`A1._getBelongGrandCompany() > 0` gates creation of that cutscene; `A2` is
passed as the final `startCutScene` argument, and this class does not derive or
validate it. The method returns `true` after the accepted path and `false` for
any other macro result (`populacechocobolender.lua:234-329`). The decoded true
and false returns are at offsets 2675 and 2683.

`eventUseRentalChocobo(self, A1, A2, A3)` first checks `A2 >= 10`
(`populacechocobolender.lua:332-370`). The source therefore consumes `A2` as
a caller-supplied numeric eligibility value. It does not calculate a level or
rank locally. The static table cross-check describes the corresponding
requirement as at least one class at level 10 and says the rental rate and
duration are runtime arguments
(`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md:1455-1457`).

When `A2 >= 10` and `A3 == true`, the method calls
`A1.getMoneyOnHand(A1, 1000001)` at `root/proto4` PC 40 / offset 3285 and
passes the result as `money` in the exact macro call
`worldMaster.askMultipleTextMacro(worldMaster, self, self, 2, 11, 2, 1, true,
true, 0, money, 0, 0)` at PC 55 / offset 3345. A positive confirmation calls
`self.say(self, self, textId, 0)` and `worldMaster.say(worldMaster, self, 33)`,
then performs the fade, talk-turn finish, and returns `true`; any other macro
result returns `false`. When `A3` is false, or when `A2 < 10`, the method
speaks the refusal path and returns `false`. `1000001` is the only literal
wallet lookup identifier in this method. The source contains no literal rental
price, price comparison, or deduction call, so the actual price and the
producer of `A2` and `A3` remain outside this frozen client evidence. The
decoded Boolean return sites are offsets 3437, 3449, and 3549.

The company input is separate from the numeric rental threshold: the menu
gates flag `A5` against `work.townId`, and personal and barding paths call
`A1._getBelongGrandCompany()`. `work.companyRank = 31` is stored during
initialization but never read by this class.

## Rental information and personal-chocobo presentation

`eventInformationRental(self)` chooses six actor-class dialogue IDs, runs
the corresponding schedulers, and has no explicit return
(`populacechocobolender.lua:461-560`).

`eventTalkMyChocobo(self, A1)` chooses an actor-class cutscene, fades the
player-like `A1`, and calls `visibleChocobo(A1, L3, true, true)` where the
source values for the three city-state actors are 1, 31, and 61
(`populacechocobolender.lua:563-630`). It has no explicit return.

`visibleChocobo(self, A1, A2, A3, A4)` does not read `A1`. `A2` is passed to
`_transformIntoChocobo(1080101, A2)` when `A3` is true; `A3` selects transform
versus cancel, and `A4` selects `_aimCameraChocobo(1080101)` versus camera
cancel (`populacechocobolender.lua:753-784`). It has no explicit return.

## Naming events

`eventSetChocoboName(self, A1)` calls
`worldMaster.say(worldMaster, self, 35)` at `root/proto7` PC 6 / offset 5293
when `A1 == true`, then returns
`desktopWidget.askChocoboNamingWidget(desktopWidget)` unchanged; the widget
call is at PC 9 / offset 5305 and the return follows at offset 5309
(`populacechocobolender.lua:633-650`). The naming widget's
character rules, length rules, and positive-result conversion are canonical in
[`Chocobo mount script contracts`](chocobo-mount-script-contracts.md#naming-widget);
this lender method adds no validation.

`eventAfterChocoboName(self, A1, A2)` uses the actor-class cutscene, hides the
chocobo with `visibleChocobo(A1, 0, false, false)`, and fades in after the
warp. `A2` is accepted but never read, and the function has no explicit
return (`populacechocobolender.lua:653-719`).

`eventCancelChocoboName(self, A1)` fades out, hides the chocobo with
`visibleChocobo(A1, 0, false, false)`, fades in, finishes the talk turn, and
has no explicit return (`populacechocobolender.lua:722-750`).

## Barding eligibility and return code

`eventLookChocoboWare(self, A1)` presents the barding choices but performs no
item possession check (`populacechocobolender.lua:787-935`). Its city-state
choice bases are:

| source path | base code | displayed item IDs |
| --- | ---: | --- |
| default and actor 1500006 | 1 | 2001017, 2001018, 2001019 |
| actor 1500061 | 31 | 2001020, 2001021, 2001022 |
| actor 1000840 | 61 | 2001023, 2001024, 2001025 |

The client-data cross-check identifies 2001017-2001025 as the nine city-state
bardings, three per city-state (`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md:1449-1453`).

`eventSelectChocoboWare(self, A1, A2)` derives the same three item IDs from
`A1._getBelongGrandCompany()`. Grand Company values 1, 2, and 3 select base
codes 1, 31, and 61 respectively, with item triples
2001017-2001019, 2001020-2001022, and 2001023-2001025. For any other return
from `_getBelongGrandCompany()`, the function's initial defaults remain base
1 and the first triple (`populacechocobolender.lua:938-976`).

It checks each item with the exact explicit-receiver calls
`A1.hasItem(A1, 101, itemId, 1)` (`populacechocobolender.lua:977-997`). The decoded
`root/proto12` checks are PCs 39, 45, and 51 / offsets 7698, 7722, and 7746.
`A2` is
the current choice code: the base code means no barding, and base plus 1, 2,
or 3 selects one of the three item IDs. The method derives
`currentSelection = A2 - baseCode + 1` and passes it as the first numeric
macro argument in
`worldMaster.askMultipleTextMacro(worldMaster, self, self, currentSelection,
91, 5, 1, available1, available2, available3, baseAvailable, true, item1,
item2, item3, 0, 0)` (`root/proto12` PC 108 / offset 7974). The availability
flag for the selected choice is forced false before this macro. A confirmed choice
returns its numeric code; canceling the selection returns integer `0`
(`populacechocobolender.lua:998-1176`). The method does not return an item ID
and does not show a separate purchase or deduction operation.

`eventTalkStepBreak(self, A1)` says the actor-class step-break text when
`A1 != 0`, finishes the talk turn, and always returns integer `0`
(`populacechocobolender.lua:1179-1235`).

The item IDs, Grand Company mapping, and `hasItem` calls close the client-side
barding eligibility contract. The frozen retail corpus does not expose the
upstream caller that supplies the rental threshold, the Boolean rental mode,
or the runtime rental price, so those values cannot be given stronger names
or literal values from this script.
