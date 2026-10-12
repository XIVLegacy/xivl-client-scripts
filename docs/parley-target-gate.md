# Parley target gate

The decoded Lua 5.1 chunks for `CharaBaseClass`'s parameter methods,
`DesktopWidget`'s connector methods, and `MainMenuWidget` matched the
LPBs byte-for-byte after their 13-byte `rle` wrappers were
decoded (payload XOR `0x73`). The locators below are recovered method
names and source lines, not native executable addresses.

| Recovered class | LPB beneath `client/script/` | LPB SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- | --- |
| `chara/charabaseclass_parameter` | `729s9/729s989r57y9rr_u9s9x5q5s.le.lpb` | `e60a1ad866e4275e2f4e2e536697ac78a4926161820ade6ac07d939c6cf446bc` | `cbf1856bed20810193e8b7d3868bb469e6bf6955de781fe8ce285bdd050e4ee8` |
| `widget/desktopwidget_connector` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| `widget/mainmenuwidget` | `n1635q/x91wx5wpn1635q.le.lpb` | `c0e1782a3ca183fcaa520a16320946f62d3fc861c74978cde19ea20fcd064b0a` | `185d856d406d46ba7416444ddc2212b68036f7d56d0ee62148be2567630c90b2` |

The canonical `CharaBaseClass.isNegotiatable` body, lines 177-185 of
`chara/charabaseclass_parameter.lua`, returns `isPropertyEnabled(4)`.
`DesktopWidget.canTargetNegotiation`, lines 16573-16621 of
`widget/desktopwidget_connector.lua`, returns false unless ready-command
slot 16 is nonnull, the local player reports `enableNegotiation()`, the
current target exists, that target is not a player, and the target reports
`isNegotiatable()`. Only after those checks does it return true.

`MainMenuWidget.updateReadyCommand`, lines 1720-1795 of
`widget/mainmenuwidget.lua`, scans equipped ready commands. For command ID
29497 it additionally calls `canTargetNegotiation()` before adding a
ready-command menu entry with text ID 1104 and icon ID 30232. These are
client-side presentation and target-eligibility checks. They do not identify
the historical Man300 shaman target, prove which actor-class property flags
were active in a quest instance, give command 29497's EventStart payload,
or establish a negotiation result or quest transition. Class-path existence
and neighboring actor-class rows cannot close those joins.

Canonical `man300.csv` row `67` contains localized text but does not name a
specific NPC or provide an actor ID or class path. The member SHA-256 is
`4ac67d7fc1a50a75f292ff7a995b4de0242f85eed5de42cb4b07de30cecc6c1b`, pinned
at `xivl-client-data:manifests/tables.json:3790`. This row does not identify
the historical Parley target.

## Negotiation widget boundary

The decoded `NegotiationJudge`, `NegotiationWidget`, and
`NegotiationAbilityListWidget` chunks also matched their LPBs
byte-for-byte after wrapper decoding:

| Recovered class | LPB beneath `client/script/` | LPB SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- | --- |
| `judge/negotiation/negotiationjudge` | `0p635/w53vq19q1vw/w53vq19q1vw0p635.le.lpb` | `90823b625d2a41ee5d16b6d55aa9b85f03c178c91c8e9517155d713432c672a9` | `184d55b038ab4e5089af58ecd9037844a39d45b9b28ca01aa7d63fa8168d6ada` |
| `widget/ask/negotiationwidget` | `n1635q/9rz/w53vq19q1vwn1635q.le.lpb` | `dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1` | `33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd` |
| `widget/ask/negotiationabilitylistwidget` | `n1635q/9rz/w53vq19q1vw981y1qly1rqn1635q.le.lpb` | `dc365626983d6fd751f2a98b8075933fd52f442af5ba2c1ee27be07580fe2cce` | `bc6e6ec2a4afdadf1b18435f9cb4aa79efa6dc4849da2aa29ac5f113dc26736a` |

The recovered `NegotiationJudge` body opens or selects
`Ask/NegotiationListWidget` and `Ask/NegotiationAskWidget`, opens
`Ask/NegotiationWidget`, selects input from it, sends updates to it, and
closes it through DesktopWidget event-mode calls (methods
`openListWidget`, `openAskWidget`, `openNegotiationWidget`,
`inputNegotiationWidget`, `updateNegotiationWidget`, and
`closeNegotiationWidget`). Each branch tests `isPlayer()` before the
DesktopWidget call. Its separate `negotiationEmote` method calls
`_runCharaScheduler` on the supplied actor. This is a client UI wrapper,
not a turn, score, or outcome authority.

`NegotiationWidget.updateAskParameter` has direct bytecode comparisons
for update codes 1-29 (decoded chunk offsets beginning `0x227E`). The
canonical body, lines 1147-1632, ties several of those values to explicit
widget operations:

| Update code | Direct recovered operation |
| ---: | --- |
| 1-12 | Set a numbered tile's data, icon, visibility, and count text. |
| 14 | Set the negotiation gauge's `Maximum` and `Value` from the supplied inputs. |
| 15 | Set the achievement gauge's `Maximum` and `Value` from the supplied inputs. |
| 16, 17, 18 | Set `IconControl_Addition_1`, `_2`, or `_3` visibility from the first value after the code; when that value is true, send `UILuaCommands.SoundPlayAddItem` to the negotiation gauge. |
| 19 | Pass the first two values after the code to `negotiationWidgetDispSelected`. |
| 20 | Store five values in `work.ability1` through `work.ability5`; disable `Button_Ability` when `abilityCheck` returns false. |
| 21 | Show `Border_ArrowIconLeft` and hide `Border_ArrowIconRight` when the fourth value after the code is true; otherwise hide the left arrow and show the right. |
| 22 | Set the time gauge's `Maximum` from `work.time` and `Value` to zero. |
| 23, 24, 25 | Send player-operation, enemy-operation, or time-up sound commands respectively. |
| 26 | Copy the three `negotiationWidgetGetData` values of the tile named by the second value into the tile named by the first; show the destination icon and count text, hide the source icon and count text, and send `UILuaCommands.SoundPlayIconSet`. |
| 27 | Traverse twelve tile records and double or halve their displayed numeric values according to the supplied flag. |
| 28, 29 | Send `PauseLimitTimer` or `ResumeLimitTimer` to the time gauge. |

The rows for codes 16-21 and 26 follow the `updateAskParameter`
bytecode (`root/proto7`): codes 16, 17, and 18 at PCs 172-185, 187-200,
and 202-215 (offsets `0x252E`-`0x2562`, `0x256A`-`0x259E`, and
`0x25A6`-`0x25DA`); 19 at PCs 217-223 (`0x25E2`-`0x25FA`); 20 at PCs
225-245 (`0x2602`-`0x2652`); 21 at PCs 247-268 (`0x265A`-`0x26AE`); and
26 at PCs 326-390 (`0x2796`-`0x2896`). `abilityCheck` returns false only
when all five stored ability values equal `false` (lines 1635-1662).

`negotiationWidgetDispSelected` (lines 1932-2097) stores an index from 1
through 5 in the matching `work.selected` field and shows that
`Label_SelectedItem` icon. For a larger index it fills slot 6 when
`work.selected6` is 0; otherwise it shifts slots 2-6 into slots 1-5, stores
the new icon in slot 6, and redraws all six icons (`root/proto11`, PCs
0-142, offsets `0x3824`-`0x3A5C`; slot-6 test at PCs 75-80,
`0x3950`-`0x3964`).

The decompiler damages nested control flow elsewhere in this method,
including the recovered code 21 branch. These operations alone do not
establish valid server update sequences, widget acceptance, timer
duration, Parley scoring, item or ability identities, or a historical
Man300 negotiation result. Code 13 retains its raw method body as a lead
rather than published gameplay semantics.

## Negotiation widget results

`NegotiationWidget.processUICommandOperate` (lines 569-717) maps
`Button_ItemIcon_1` through `Button_ItemIcon_12` to `playerSelect(1)`
through `playerSelect(12)` (`root/proto1`, PCs 4-85, offsets
`0xFC5`-`0x1109`). `playerSelect` (lines 720-781) passes its argument to
`setBaseAskResult` and stores it in `work.select` unless it is 13. It then
stops the time gauge's limit timer, resets the gauge's `Maximum` to
`work.time` and `Value` to zero, and disables the twelve tile buttons and
`Button_Ability` (`root/proto2`, PCs 0-49, offsets `0x14BF`-`0x1583`; the
13 test is at PCs 12-15, `0x14EF`-`0x14FB`). `processUICommandDefault`
calls `playerSelect(13)` when it receives `UILuaCommands.TimerOver`
(`root/proto4`, PCs 2-6, offsets `0x17CD`-`0x17DD`).

`Button_Ability` proceeds only when `abilityCheck` returns true and no
`Ask/NegotiationAbilityListWidget` child is open. It then opens that child
with the five stored ability values and resumes the limit timer if the open
returns false (`root/proto1`, PCs 88-124, offsets `0x1115`-`0x11A5`). In
the child, `Button_AbilityCommand_1` through `Button_AbilityCommand_5` call
`playerAbilitySelect(1)` through `playerAbilitySelect(5)`.
`NegotiationAbilityListWidget.playerAbilitySelect` (lines 376-408) sets the
parent's ask result to its argument plus 14, so the five buttons yield
results 15-19. It also pauses the parent's limit timer, hides the chosen
button, and sends `UILuaCommands.SoundPlayAbility` to it (`root/proto6`,
PCs 0-22, offsets `0xD20`-`0xD78`; the addition is at PC 3, `0xD2C`).

`NegotiationWidget.processUICommandCancel` opens `CommonAskWidget` with
text IDs 7124, 7125, and 7126 and raw mode 2 (`root/proto3`, PCs 0-10,
offsets `0x170C`-`0x1734`). `processAskResult` sets the ask result to -1
only when the child result is 1 (`root/proto12`, PCs 0-4, offsets
`0x3C95`-`0x3CA5`).

The widget's local ask results are therefore tiles 1-12, time-up 13,
abilities 15-19, and confirmed cancel -1. They do not show how the judge
or server consumes a result, name the abilities, or establish any
result's gameplay effect.

A prior external lead, `parley/parley_decomp_2026-09-27.md` and
`quests/man300-toll-of-the-warden-parley/parley.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, listed these result values
and several update-code roles.
