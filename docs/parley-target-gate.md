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

The recovered `CharaBaseClass.isNegotiatable` body, lines 93-95 of
`chara/charabaseclass_parameter.lua`, returns `isPropertyEnabled(4)`.
`DesktopWidget.canTargetNegotiation`, lines 8909-8927 of
`widget/desktopwidget_connector.lua`, returns false unless ready-command
slot 16 is nonnull, the local player reports `enableNegotiation()`, the
current target exists, that target is not a player, and the target reports
`isNegotiatable()`. Only after those checks does it return true.

`MainMenuWidget.updateReadyCommand`, lines 689-716 of
`widget/mainmenuwidget.lua`, scans equipped ready commands. For command ID
29497 it additionally calls `canTargetNegotiation()` before adding a
ready-command menu entry with text ID 1104 and icon ID 30232. These are
client-side presentation and target-eligibility checks. They do not identify
the historical Man300 shaman target, prove which actor-class property flags
were active in a quest instance, give command 29497's EventStart payload,
or establish a negotiation result or quest transition. Class-path existence
and neighboring actor-class rows cannot close those joins.

## Negotiation widget boundary

The decoded `NegotiationJudge` and `NegotiationWidget` chunks also matched
their LPBs byte-for-byte after wrapper decoding:

| Recovered class | LPB beneath `client/script/` | LPB SHA-256 | Decoded chunk SHA-256 |
| --- | --- | --- | --- |
| `judge/negotiation/negotiationjudge` | `0p635/w53vq19q1vw/w53vq19q1vw0p635.le.lpb` | `90823b625d2a41ee5d16b6d55aa9b85f03c178c91c8e9517155d713432c672a9` | `184d55b038ab4e5089af58ecd9037844a39d45b9b28ca01aa7d63fa8168d6ada` |
| `widget/ask/negotiationwidget` | `n1635q/9rz/w53vq19q1vwn1635q.le.lpb` | `dafe05e99972fe0ae83d1dbdc590d98a560a2c8f4f214fb741c9ab685e7819e1` | `33c1a6e77080e763c22bfde6ddf1e4e8faf02c3ad457f524931c61932e26bedd` |

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
recovered body, lines 357-598, ties several of those values to explicit
widget operations:

| Update code | Direct recovered operation |
| ---: | --- |
| 1-12 | Set a numbered tile's data, icon, visibility, and count text. |
| 14 | Set the negotiation gauge's `Maximum` and `Value` from the supplied inputs. |
| 15 | Set the achievement gauge's `Maximum` and `Value` from the supplied inputs. |
| 22 | Set the time gauge's `Maximum` from `work.time` and `Value` to zero. |
| 23, 24, 25 | Send player-operation, enemy-operation, or time-up sound commands respectively. |
| 27 | Traverse twelve tile records and double or halve their displayed numeric values according to the supplied flag. |
| 28, 29 | Send `PauseLimitTimer` or `ResumeLimitTimer` to the time gauge. |

The decompiler damages nested control flow elsewhere in this method.
These operations do not by themselves establish valid server update
sequences, widget acceptance, timer duration, Parley scoring, or a
historical Man300 negotiation result. Codes 13 and 16-21 and 26 retain
their raw method bodies as leads rather than published gameplay semantics.
