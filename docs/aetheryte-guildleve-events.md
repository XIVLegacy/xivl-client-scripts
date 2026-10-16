# Aetheryte guildleve events and Guardian's Aspect

`eventGLPlay` payload slot 6 is the current Guardian's Favor balance.
Slot 7 is the Favor cost offered for invoking Guardian's Aspect. The
parent and child aetherytes present that cost and balance in a confirmation
and return the choice. They do not apply the status or deduct Favor here.

## Argument numbering and evidence

The tables count explicit event payload arguments, excluding the receiver.
The decompiler calls the receiver `A0_2` and payload slots 1-9 `A1_2` through
`A9_2`. Thus the sixth formal parameter including the receiver is `A5_2`
(the faction-credit reward), while the sixth payload argument is `A6_2`
(the Favor balance). The arity of 10 in
`xivl-client-structs:manifests/lua_api_contract.json` includes the receiver.
These Lua positions do not independently establish the serialization of a
network event packet.

The findings below promote the named extraction's script observations, not
untracked decompiler bodies. Script locators are relative to `lua/scripts/`.
The source is retail 1.23b extraction `2012.09.19.0001`, decoded with
`xivl-client-structs:tools/decode_lpb.py`, decompiled with `unluac.jar`, and
canonicalized to LF by `tools/lua_corpus.py publish`. The producing pipeline
and output identity are recorded in [the script manifest](../manifests/scripts.json)
and [the corpus contract](../lua/README.md).

| Key | Decoded script | SHA-256 | Manifest locator |
|---|---|---|---|
| B | `chara/npc/object/aetheryte/aetherytebaseclass.lua` | `198ACEE5FB54F13C60F446B050A0F5B41E8EF0D1DD268699BCB71574588A1DCF` | `manifests/scripts.json:5649-5652` |
| P | `chara/npc/object/aetheryte/aetheryteparent.lua` | `AA4897A10FA0F024FDCB609D556751627B858EB9D20817069BAF42509359C3FA` | `manifests/scripts.json:5673-5676` |
| C | `chara/npc/object/aetheryte/aetherytechild.lua` | `B309CD10CBE2759016D8F07735871A118A3957186983AF365B1133224674DDD4` | `manifests/scripts.json:5667-5670` |
| S | `widget/ask/guildlevestartwidget.lua` | `F9B2769685C2985760330C46926AB5A45BF427011190998782BC0BB9E7591D64` | `manifests/scripts.json:14955-14958` |
| D | `widget/desktopwidget_connector.lua` | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` | `manifests/scripts.json:15399-15402` |
| J | `widget/ask/journaldetailwidget.lua` | `21B9F1B4900BBD3BD9826F852F6DD82BEAB914951A053CBC5A003ADA2B38B32D` | `manifests/scripts.json:15003-15006` |

B/P/C/S/D/J below refer to these exact script bytes and line numbers.
Their straight-line argument transfers and the explicit choice branches are
the evidence used here. No native or live validation is claimed.

## eventGLPlay

B `eventGLPlay:276-292` forwards all nine payload slots unchanged to
`self.processGuildlevePlaying`. The base implementation at B:295-298 is
empty. P:1441-1594 and C:171-324 override it. The classes inherit from
`AetheryteBaseClass` at P/C:2-8, and bind their actor text to
`aetheryteParent` and `aetheryteChild` at P:20-29 and C:11-20.

| Payload slot | Parameter | Supported name | Client use and confidence |
|---:|---|---|---|
| 1 | `A1_2` | `guildleveId` | Leve name in the main prompt and leve-link confirmation. High: P:1470,1507; C:200,237; parent text 146/154 and child text 35/43. |
| 2 | `A2_2` | `canLeveLink` | Availability flag for choice 2, Perform leve link. High: P:1465; C:195. |
| 3 | `A3_2` | `factionId` | First format argument to the leve-link confirmation, selecting its faction. High: P:1504; C:234; parent text 154 and child text 43. |
| 4 | `A4_2` | `areaFactionStanding` | Second format argument to that confirmation, displayed as faction standing. High: P:1505; C:235. |
| 5 | `A5_2` | `factionCreditReward` | Third format argument to that confirmation, displayed as the credit reward. High: P:1506; C:236. |
| 6 | `A6_2` | `currentGuardianFavor` | Main prompt balance and second format argument to Aspect confirmation. High: P:1472,1529; C:202,259; parent text 27/146 and child text 16/35. |
| 7 | `A7_2` | `guardianAspectFavorCost` | Nil becomes zero; positive enables choice 3. First format argument to Aspect confirmation. High: P:1446-1451,1528; C:176-181,258. |
| 8 | `A8_2` | `currentDifficulty` | Positive enables choice 4; value 1 prevents lowering. Otherwise the level selector receives this value minus one. High: P:1452-1455,1536-1564; C:182-185,266-294. |
| 9 | `A9_2` | `guildMarkClassId` | Non-nil, nonzero value is formatted into worldMaster text 50039 before leve linking, naming the class whose objectives avoid a guild-mark reduction. High for the displayed class, no server policy inferred: P:1483-1495; C:213-225. |

The restricted-choice flags are `(true, A2, A7 > 0, A8 > 0, false, true)`.
The main prompt receives `(A1, A7, A6, A8)` after those flags
(P:1456-1474; C:186-204). Its text conditions the Favor line on its second
format argument (`e803`, the cost), but prints its third (`e804`, the balance).
It prints difficulty using its fourth (`e805`).

Parent rows 147-152 and child rows 36-41 supply the six menu labels in order.
Choice 1 continues, 2 performs a leve link, 3 invokes Guardian's Aspect,
4 adjusts difficulty, and 6 abandons the levequest. Choice 5 is disabled.
Choices 2, 3, and 6 return their number only after confirmation result 1.
A declined confirmation repeats the main prompt. Choice 4 returns
`(4, selectedDifficulty)` only for a successful selection in 1-5
(P:1476-1588; C:206-317).

## eventGLBoost and the Favor binding

B `eventGLBoost:258-267` forwards its two payload slots unchanged to
`self.processGuildleveBoost`. The base implementation at B:270-273 is
empty. The overrides at P:1417-1438 and C:147-168 show the Aspect explanation,
ask for confirmation, and return the ask result unchanged.

| Payload slot | Parameter | Supported name | Client use and confidence |
|---:|---|---|---|
| 1 | `A1_2` | `currentGuardianFavor` | Second format argument to parent text 27 / child text 16. High: P:1433; C:163. |
| 2 | `A2_2` | `guardianAspectFavorCost` | First format argument to parent text 27 / child text 16. High: P:1432; C:162. |

Those two confirmation rows use `[@number:022003e80203]` in the minimum-Favor
clause and `[@number:022003e80303]` in the current-Favor clause. In this
format, `e802` selects the first supplied value and `e803` the second.
The direct boost call therefore formats `(cost, balance)` as `(A2, A1)`.
The playing-menu choice 3 formats the same rows as `(A7, A6)`
(P:1526-1530; C:256-260). This independently resolves the two playing slots
without using their relative size or a server's sample values.

## eventGLStart and widget argument reshuffling

B `eventGLStart:230-255` opens `Ask/GuildleveStartWidget` in mode 1.
Its widget payload is `(A1, A2, A3, A4, A5, A6, A7, A8, 0, A9)`.
The inserted zero occupies widget slot 9. Event slot 9 consequently reaches
widget slot 10. The event returns its supplied difficulty, slot 2, only
when the widget's second result is 1. Otherwise it returns nil.

| Event payload slot | Parameter | Supported name | Start-widget use and confidence |
|---:|---|---|---|
| 1 | `A1_2` | `guildleveId` | Widget slot 1 formats worldMaster text 33601 in the title. High: B:237; S:19-24. |
| 2 | `A2_2` | `difficulty` | Widget slot 2 selects the level label from 50016-50020 for values 1-5. Other values hide the level grid. High: B:238; S:43-94. |
| 3 | `A3_2` | `factionId` | Widget slot 3 selects the faction in UI text 4326 and must be positive to show that block. High: B:239; S:95-109. |
| 4 | `A4_2` | `areaFactionStanding` | Widget slot 4 is the second format argument of UI text 4326, Area Faction Standing. High: B:240; S:101. |
| 5 | `A5_2` | `factionCreditRewardEstimate` | Widget slot 5 is the third format argument of UI text 4326, the estimated faction-credit reward. High: B:241; S:102. |
| 6 | `A6_2` | `partyMemberOtherDutyWarning` | Widget slot 6 is the first condition in UI text 4325, warning that a party member is bound by another duty. High for presentation: B:242; S:116. |
| 7 | `A7_2` | `partyMemberTooFarWarning` | Widget slot 7 is the second condition in UI text 4325, warning that a party member is too far away. High for presentation: B:243; S:117. |
| 8 | `A8_2` | `currentClassGuildMarkWarning` | Widget slot 8 is the third condition in UI text 4325, warning that the current class cannot receive guild marks. High for presentation: B:244; S:118. |
| 9 | `A9_2` | `experienceReductionWarning` | Widget slot 10 is the fifth condition in UI text 4325, warning about class/level mismatch or class changes reducing awarded EXP. High for presentation: B:246; S:120. |

S:111-127 hides the attention block only when all five warning inputs are
zero. B:245 supplies zero to the fourth warning input, whose text concerns
other party members' class eligibility for guild marks. S:137-163 sets
result 1 for Begin and -1 for Discontinue or cancellation.

UI text 4326 uses `e802` to select Evaluating Faction, `e803` to print Area
Faction Standing, and `e804` to print the faction-credit reward. Consequently,
a value called `favorCount` supplied in eventGLStart's fourth payload slot
would be rendered as area faction standing when slot 3 is positive. This is
a display-route observation, not a judgment about a server's implementation.
The mapping name `favorCount` at
`xivl-client-data:tools/mappings/guildleve.py:21` identifies sheet column 24;
that mapping alone does not bind the column to eventGLStart.

## Detail widget boundary

B `eventGLSelectDetail:190-209` forwards event slots 1-7 and 9 to
`DesktopWidget.askActiveGuildleveDetailWidget`, omitting slot 8.
D:9971-10032 uses the first forwarded value as the journal ID when opening
`Ask/JournalDetailWidget` with mode 2 and journal type 1. Its detail call
receives `(nil, A2, A3, A4, A5, A6, A7, A8)` in the connector's numbering.
Thus the detail call receives original event slots `(nil, 2, 3, 4, 5, 6, 7, 9)`.
These positions are separate from the playing and start-event contracts.

J:733-738 creates an `Item_BoostTitle` / `Item_BoosttText` template with help
text 78530. That text describes the cost in Guardian's Favor for Aspect on
the levequest. In the type-1 `setDetailData` branch, J:1251-1274 explicitly
hides the boost title, its borders, and its text. The help string therefore
does not establish a displayed cost in this detail path or an eventGLStart
argument binding. The broader journal lifecycle is documented in
[Guildleve journal lifecycle](guildleve-journal-lifecycle.md).

## Guardian's Aspect flow and limits

1. The playing payload carries current Favor in slot 6 and
   activation cost in slot 7. A positive cost enables Invoke Guardian's aspect.
2. Choice 3, or `eventGLBoost(balance, cost)`, explains the temporary boon and
   confirms the displayed cost and balance using parent text 26/27 or child
   text 15/16.
3. Confirmation returns a client choice/result to the caller. These handlers
   neither deduct Favor nor apply Guardian's Aspect, and establish no EXP or
   reward arithmetic.

Client text names status 253002 Guardian's Aspect and describes increased
experience points (`xtx/status`, row 253002). `worldMaster` row 25093 says
that the player's Aspect is already active. Those rows establish the
client's terminology and intended presentation. The traced event handlers do
not reference either ID, test whether the status is active, enforce sufficient
Favor, apply a status, or compute a bonus.

### Unresolved and authority boundary

All explicit slots have a supported presentation name above. The producer of
these event arguments, the source of the current Favor balance, and whether
slot 7 equals sheet column 24 remain unresolved. The client does not prove
the server's Favor deduction, cap, recovery schedule, guardian identity,
status application or duration, bonus percentage, EXP recipient, completion
reward changes, or authoritative leve-link policy. A positive slot 7 controls
menu availability, but the Lua does not compare the balance against the cost.
The supplied current difficulty and text labels do not establish a server
scaling formula. Wire transport and server-side effects require separate
evidence.

The existing Lua API manifest retains decompiler parameter labels. Its owning
generator, `xivl-client-structs:tools/extractors/build_lua_api_contract.py:67-100`,
extracts those labels directly from function declarations. Its scope and
limitations identify them as positional labels. Semantic names in this
finding do not replace those generated source labels.

## Client-text identity

The text joins use the English column (CSV column `1`, except the status name
at `xtx_status` column `3`). File identities are pinned in
`xivl-client-data:manifests/tables.json` at the locators below. Row IDs are
keys, not physical line numbers. These are promoted text observations from
the private decoded corpus; the corpus bytes are not redistributed here.

| Source | Rows used | CSV SHA-256 | Manifest locator |
|---|---|---|---|
| `xivl-client-data:csv/aetheryteParent.csv` | 26-27, 146-150, 152-154, 158-159, 162, 164 | `8B02C6C8F7FEFA10D1D90D7EF79B4AE48EDC13F79F7FD0920D4D5A2CADF9E27C` | `manifests/tables.json:243-249` |
| `xivl-client-data:csv/aetheryteChild.csv` | 15-16, 35-39, 41-43, 47-48, 51, 53 | `0E4717FC041802BAB41F04AAB91A9DA8EAC7D3AF7FC7C7B421E552F7A400AB8A` | `manifests/tables.json:235-241` |
| `xivl-client-data:csv/xtx__text_ui.csv` | 4325-4326, 78530 | `23762A422118D99C4144A48B3495C52511B1B1B865E4FC50FDC61A973E3C6ECE` | `manifests/tables.json:5987-5993` |
| `xivl-client-data:csv/worldMaster.csv` | 25093, 33601, 50016-50020, 50039 | `2E2E2DD5CD9651388F6FA575B4229081AD0452165E78B725DF0A5B5B7CF7C643` | `manifests/tables.json:5891-5897` |
| `xivl-client-data:csv/xtx_status.csv` | 253002 | `60ECA3B76D1D9799589D9059ADEB1E7C3D142E07609A1AD0A053C5E75D9B96EE` | `manifests/tables.json:6307-6313` |

The decisive row pins below hash each complete UTF-8 physical CSV line,
excluding its CR/LF terminator. They preserve the positional text evidence
independently of the script interpretation.

| Source row | SHA-256 |
|---|---|
| `aetheryteParent:27` | `B375F4A200F97C70FE54744FD5F7983068CFA023AC03D04C20558DC7540FA583` |
| `aetheryteChild:16` | `054ED77FC6C3E60E0CE0D5B97B29DE726A6A3AAB14980EEDAD2DFDCB84DBA7D2` |
| `xtx/_text/ui:4326` | `982810D9DF0315325D6F2F05F452A8E06D0F5E034925460CA5A912685DD87D26` |
