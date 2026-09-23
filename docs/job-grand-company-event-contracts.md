# Job and Grand Company event contracts

The recovered FFXIV 1.23b quest scripts preserve client-owned dialog,
cutscene, fade, widget, and reward-presentation sequences. They are useful for
assigning an event to the correct phase and speaker, but they do not contain
the lost server dispatcher, combat AI, spawn rules, success conditions, or
persistent return-point policy.

Source identities for these scripts are recorded in `manifests/scripts.json`.
Method names below are stable locators within the named canonical script.

## Job quest phase ownership

### Warrior

`War0j1.processEventClear` runs the main clear conversation and closes its talk
turn. `War0j1.processEventClearAfter` opens a new talk turn on its supplied
event owner, runs scheduler `354234368`, speaks text rows 35 and 36, and closes
that turn. The separate method proves a post-clear speaker-owned presentation;
it must not be folded into whichever NPC happens to grant the reward.

`War0j6.processEvent010` performs only the default fade-out/fade-in pair.
`processEvent020` inserts scene `war0j620` between that pair.
`processEventClear` owns the long information dialog, job ability 27189, and
the supplied job item. The client sequence does not identify the server battle
completion trigger or a post-battle world position.

Sources:

- `lua/scripts/quest/scenario/war/war0j1.lua`, methods
  `processEventClear` and `processEventClearAfter`.
- `lua/scripts/quest/scenario/war/war0j6.lua`, methods `processEvent010`,
  `processEvent020`, and `processEventClear`.

### Monk

`Mnk0j1.processEventGAGARUNAStart` tests its two extra arguments separately
against Lua boolean `true` and speaks row 42 if either matches; otherwise it
speaks row 6. Numeric `1` is not the same input. This is a client greeting
branch, not a recovered definition or producer for either argument.

`Mnk0j6` preserves distinct Erik and Widargelt methods rather than one generic
quest-giver flow. `processEvent020_ERIC_Follow` and
`processEvent020_ERIC_PUB` are Erik-owned talk turns;
`processEventWIDARGELT_PUB` is a separate Widargelt-owned turn.
`processEventClear` owns information dialog 115 and job ability 27106.

The separation proves dialog and presentation ownership. It does not prove
which server actor advances the objective or which encounter state unlocks
each method.

`Mnk0j6.processEvent020` is the separate item-presentation talk: it speaks
rows 41, 69-73, and 109-114 around `showGetJobItemWidget`, passing the
method's fourth argument as the item. The client method does not choose that
item or grant it. Its presence does not make the Erik-owned `020` methods
aliases of this path.

Sources: `lua/scripts/quest/scenario/mnk/mnk0j1.lua`, method
`processEventGAGARUNAStart`; `mnk/mnk0j6.lua`, the named `020` and speaker
methods plus `processEventClear`.

The separate `lua/scripts/director/quest/questdirectormnk0j601.lua` chunk requires
`QuestDirectorBaseClass` and declares itself directly on that base, with no
child methods. It is not a declared `SimpleQuestBattle` subclass in this
chunk. The LPB at
`client/script/61s57qvs/tp5rq/tp5rq61s57qvsxwzj0dji.le.lpb` decodes
byte-for-byte to the recovered chunk (SHA-256
`cb397ed9b9567e2d0b136c3c90a745440e898aa7b4c704545d404a525a941830`).
This identity does not recover inherited behavior, encounter rules, or a
server-side director owner.

### Black Mage

`Blm0j1.processEventYayakeStart` checks its fourth argument against numeric
zero. Only that value opens restricted choice row 52 after row 51. A nil
answer or numeric 2 speaks refusal row 55 and closes the talk; other answers
continue into the ordinary offer presentation. Nonzero fourth arguments skip
the restricted choice and also continue. The later
`showQuestInfomation` result is tested and returned once. The recovered Lua
prints `if 0 == 0` and a repeated return call, but the bytecode tests retained
register R4 at PC 40 and returns the saved result at PC 159. This client
branch does not identify the producer of the fourth argument or prove server
quest admission.

Source: `lua/scripts/quest/scenario/blm/blm0j1.lua`, LPB
`tp5rq/r75w9s1v/8yx/8yxj0i.le.lpb` (decoded SHA-256
`5b32a81c2264a0dac4e0f9b56c45c1f06cc0e0d07fc8ddfa1f714e9d0523d3d5`).
The donor raw chunk matches the decoded LPB exactly. Bytecode
locators: `processEventYayakeStart` PCs 4-41 (`0x44E-0x4E2`) and 123-160
(`0x62A-0x6BE`).

`Blm0j3.processEvent000` is a closed talk turn with text rows 11 through 13.
`processEvent005` is a longer introduction path: its fourth argument is passed
to text row 14, followed by rows 15 through 19 and 42 around a one-second
fade-out/fade-in pair. The argument is part of the client ABI and must not be
dropped or synthesized from the method name. Canonical
`xivl-client-data:csv/blm0j3.csv` row 14 (SHA-256
`c8d5bca21020ca0330f4975cddc3e2cd5fa76fc13a701580f621db2e0a5b20d2`)
uses that argument to select Hyur, Elezen, Lalafell, Miqo'te, or Roegadyn
in English text. The row does not define the server's numeric encoding or
the argument producer.

The two methods are distinct event phases. Finding both on the same quest
class does not make them interchangeable or establish their server-side actor
binding.

Source: `lua/scripts/quest/scenario/blm/blm0j3.lua`, methods
`processEvent000` and `processEvent005`.

`Blm0j4.processEventDOZOLMELOCStart` has two independent client choices.
Its `ask` of row 29, mode 2, selects row 3 versus row 32 early in the talk
(PCs 16-17, `0x474-0x478`). A later `showQuestInfomation` call independently
selects row 15 versus row 14 (PCs 110-111, `0x5EC-0x5F0`); the saved offer
result is returned after the talk. One choice cannot stand in for the other,
and neither proves an authoritative quest gate. Source:
`lua/scripts/quest/scenario/blm/blm0j4.lua`, LPB
`tp5rq/r75w9s1v/8yx/8yxj0f.le.lpb` (decoded SHA-256
`0e712e06d0b2fcc2185eb00a6a9d4614705155f6f7e21249dcccbb8158a0feb8`).
The donor raw chunk matches the decoded LPB exactly.

### Paladin

`Pld0j1.processEvent010` and `processEvent015` both play scene `pld0j110`,
show and notify public-information entry 25117 with item 11000558, and wait
five seconds. Their finalizers differ:

| Method | Finalizer |
| --- | --- |
| `processEvent010` | `startFadeInCutSceneAfterWarp` |
| `processEvent015` | `startFadeInCutSceneDefault` |

This is a real transition-ownership distinction. It does not identify the
destination or authorize treating either method as a generic quest intro.

Source: `lua/scripts/quest/scenario/pld/pld0j1.lua`, methods
`processEvent010` and `processEvent015`.

### Strict-boolean job scene finalizers

Five other job-scene wrappers each play their fixed NQ scene in mode 1 after
default fade-out, then choose the finalizer by comparing the fourth method
argument to Lua boolean `true`. Only `true` selects the default fade-in;
numeric 1, nil, and other values select the after-warp fade-in. This is a
client branch, not proof of the caller's argument, a warp, or a destination.

| Method | Scene | LPB | Decoded SHA-256 | Compare PC / offset |
| --- | --- | --- | --- | --- |
| `Mnk0j6.processEvent005` | `mnk0j610` | `xwz/xwzj0d.le.lpb` | `6abf02dff4fd1406f816d9fbb585b5abd20fae41166f3fd26c801e8a74619de4` | 7 / `0xD66` |
| `Blm0j6.processEventNQ01` | `blm0j610` | `8yx/8yxj0d.le.lpb` | `3d834beabc4a653ab7d2b8cb5894724372d474031df1b7136c7e9deb23b80c31` | 7 / `0x1A49` |
| `Pld0j5.processEvent_005NQ_1` | `pld0j510` | `uy6/uy6j0e.le.lpb` | `ffae894c2bc7f83b4be9f988e7959bbd412a92f8e15667378d889e111c8fb4f` | 7 / `0x5BD` |
| `Pld0j6.processEventNQ01` | `pld0j610` | `uy6/uy6j0d.le.lpb` | `c965a9223e8749f91092bf3a682398bc3f8fb526df7ce4919cccea75084743cf` | 7 / `0xD9B` |
| `Brd0j4.processEventNQ01` | `brd0j410` | `8s6/8s6j0f.le.lpb` | `93e55481f38c0846d7ac02428243d4e751dced596264273f1aa24fec70cd075e` | 7 / `0x8B8` |

All LPBs are under `client/script/tp5rq/r75w9s1v/`. The five donor raw
chunks match their decoded LPB payloads exactly. Canonical source locators
are the named methods in `lua/scripts/quest/scenario/mnk/mnk0j6.lua`,
`blm/blm0j6.lua`,
`pld/pld0j5.lua`, `pld/pld0j6.lua`, and `brd/brd0j4.lua`.

The same `Blm0j6` and `Pld0j6` chunks also expose separate
presentation methods. `Blm0j6.processEventAfget` calls the ability widget
with `(27316, 2)` at PC 12 (`0x1CDE`), then passes its fourth method argument
to the item widget at PC 19 (`0x1CFA`). `Pld0j6.processEventKokuti` calls the
ability widget with `(27148, 1)` at PC 12 (`0xC7F`), then passes its fourth
argument to the item widget at PC 19 (`0xC9B`). Pinned
`xivl-client-data:derived/command_battle_params.csv` names 27316 Burst and
27148 Hallowed Ground. The client methods do not choose the item argument
or prove that either ability or item was granted by a server.

### White Mage

`Whm0j2.processEvent005` is a self-contained presentation: its own talk
turn contains free-display-name speech for `2600009` on rows 42 and 43,
public-information dialog 52, and `showGetJobAbilityWidget(..., 27358, 2)`.
The shorter `onJobQuestCompleteFirst` and `onJobQuestCompleteSecond` hooks
present dialog 52 and that same ability separately. The script contains no
instruction to append both hooks to `processEvent005`; doing so would repeat
the presentation. The script does not establish its retail trigger, and the
free speaker does not establish a combat ally.

`Whm0j1.processEventClear` opens a talk turn and deliberately leaves it open
after text row 24. `processEventClearNQ` performs the default fade-out, closes
that retained talk turn, waits one second, plays `whm0j110`, and performs the
default fade-in. The methods form a paired handoff; inserting an independent
event close between them changes the recovered client sequence.

Source: `lua/scripts/quest/scenario/whm/whm0j1.lua`, methods
`processEventClear` and `processEventClearNQ`.

`Whm0j4.processEventNQ` plays `whm0j410` between default fade-out and
fade-in. `processEventLS` and `processEventLS2` separately call
`showEventBeforeNpsLS` with display `2700007` and rows 38 and 63. These are
distinct available client surfaces; their retail dispatcher, serial order,
fight trigger, and roster are not established by the script.

The following four decoded chunks match their LPBs byte-for-byte.
Method locators are in the named scripts under `lua/scripts/quest/scenario/`;
their `.calls.json` sidecars give the full ciphered LPB paths.

| Script | Decoded chunk SHA-256 |
| --- | --- |
| `mnk/mnk0j1` | `14a963f6efff83518fd7861706fecf7bf90f80207eea7d53ae3dbfa74b18a369` |
| `mnk/mnk0j6` | `6abf02dff4fd1406f816d9fbb585b5abd20fae41166f3fd26c801e8a74619de4` |
| `whm/whm0j2` | `74347fd33eefba6f5f718c977f114e7a5addafe406a03124c61f01bb782d1d56` |
| `whm/whm0j4` | `819ba233c3f6faaa64ea1e5c78785d1f409d016e7c510a17c64d9aeb2e57bf18` |

### AF item and stela presentations

Seven job scenarios define `processEvent_getAF_info`: `War0j4`, `Mnk0j5`,
`Whm0j5`, `Blm0j5`, `Pld0j4`, `Brd0j5`, and `Drg0j4`. Each takes an item
argument, runs scheduler 67108910, and calls
`showGetJobItemWidget(eventArgument, itemArgument, 0)`. `Whm0j5` first opens
public-information dialog 25 and waits eight seconds. The method presents a
supplied item; it neither chooses the item nor identifies a coffer, its
location, the number or order of acquisitions, or the server grant.

`Blm0j4.processEvent000_SEKIHI` presents world-master text row 33.
`processEvent005` presents row 24 and free-display-name row 25 with display
ID 4000257. Its separate completion methods open public-information dialog
40 and present job ability 27317. These calls do not bind display 4000257
to a unique stela actor or prove the interaction and reward transaction.

`Drg0j4.processEvent_NQ_Drg0j410` plays NQ scene `Drg0j410` between
default fade-out and fade-in. `processEvent_ALBERIC_Guidance` is a distinct
talk method. The scripts do not identify the destination actor or the
server event that orders those methods.

The recovered Lua for these eight scripts was checked against the
LPBs: each decoded chunk matched byte-for-byte. SHA-256 of each decoded chunk
is the exact source identity; method locators are in the named scripts under
`lua/scripts/quest/scenario/`, and their ciphered LPB paths are recorded in
the matching `.calls.json` sidecars:

| Script | Decoded chunk SHA-256 |
| --- | --- |
| `war/war0j4` | `995220bc430d0288476898a91d42bd91fac8370e202fa3b22dc38544e1196015` |
| `mnk/mnk0j5` | `eecd2a9a3a7cc1371db345285428573743918a4018259704b677423cd6a14347` |
| `whm/whm0j5` | `0645eb178aa78833c4a1b30561c6410ce1c6118d55dd56697f330616b78b4db7` |
| `blm/blm0j4` | `0e712e06d0b2fcc2185eb00a6a9d4614705155f6f7e21249dcccbb8158a0feb8` |
| `blm/blm0j5` | `0d2a3dc4a9e57cbe272a30956e639d8a631595e1a6c96a2081e5138a2f066911` |
| `pld/pld0j4` | `0c12edeeb502f3d0a01b8a3c7c682445117d7860bd8a18fc436d5e70b9e68297` |
| `brd/brd0j5` | `eda3af68bd1fc4e603a5f746cae78043449c8f908ca401f9fe8cceb8ad2257b9` |
| `drg/drg0j4` | `9b11029faff35302b207c77e09af1603acd5d3e40a775a0d013b1b7b49f256a1` |

### Early job battle director shells

The `QuestDirectorMnk0j101`, `QuestDirectorWhm0j101`,
`QuestDirectorPld0j101`, `QuestDirectorBrd0j101`, and
`QuestDirectorDrg0j101` chunks each contain only a requirement on
`SimpleQuestBattleBaseClass` and a subclass declaration. They add no
quest-specific method, target roster, count, wave rule, or success callback.
Inherited generic behavior is not thereby absent; these child chunks simply
cannot establish those quest-specific facts.

Each recovered chunk matched the decoded LPB payload byte-for-byte. Source
locators are the named scripts under
`lua/scripts/director/quest/simplequestbattle/`, with LPB paths in their
`.calls.json` sidecars. SHA-256 of the decoded chunks:

| Director | SHA-256 |
| --- | --- |
| `QuestDirectorMnk0j101` | `ddcee2ed445592c8f117bc1d0ec5c95af1d92363041b993d4ae90fa126d507fe` |
| `QuestDirectorWhm0j101` | `cef0d0218631f665d0254f5d147f5304d478be9f30d3cd3dea016fbd26f556b1` |
| `QuestDirectorPld0j101` | `f5c54ebbe16528675e3e1d02572cd217fef08b8453bfdd0231e3eb23962c4f44` |
| `QuestDirectorBrd0j101` | `bb8efebf21dc33e9d9d98bb2e48608a77ced2b4f3e99637699513971af6a5f35` |
| `QuestDirectorDrg0j101` | `2eca62e4c45e1484f96187e53cee5c277c868ebe96f901d291235a1706fbf808` |

The following additional quest director chunks follow the same two-line
require-and-declare pattern, with no subclass methods. Their base classes
vary; an empty child does not rule out inherited generic behavior. Each
recovered chunk matched its decoded LPB payload byte-for-byte. The path
column is relative to `lua/scripts/director/quest/`, and the matching
`.calls.json` sidecar records the LPB path.

| Director script | Decoded chunk SHA-256 |
| --- | --- |
| `questdirectorarc30601.lua` | `ccabcb837e54332a6062e69d399d92ed74188ce8d688ac11f75a16472f20690c` |
| `questdirectorarc30602.lua` | `bf4bc19307dcbbf1f7a94fa130b58a40d0e89150cc2ae5e35850bd657b889f64` |
| `simplequestbattle/questdirectorblm0j101.lua` | `4b91dbf7f4f582d4ef48ce2502a4567a3f36fe8bf21235278ddb7dbf7dcda80f` |
| `questdirectorblm0j601.lua` | `17e10b322d89cfeac65e1da12f5fba9741b23da7a83b51ba9cc323229cd4df45` |
| `simplequestbattle/questdirectorbrd0j401.lua` | `140886a58e25c947cebd2d61a7f4e6f6aa563c05e6a4a42dce309a45a173c09a` |
| `questdirectorbrd0j601.lua` | `3f0839f4d0071f1a22bd42af9764c62c1e7b0446263665474d85d25d823de9d3` |
| `questdirectorcnj30601.lua` | `202f69f08434db2368cc144963bc2a53a0cf1141217af37213afe78befc25805` |
| `questdirectorcnj30602.lua` | `34ec7c5ff7ef3ef1be62fbc6f3eae08d703d3708120b189a9e9ce60194996763` |
| `simplequestbattle/questdirectordrg0j601.lua` | `929e7aef760ba27c6b0d4984a0805ed78b66de572e11257ab8fd2b43fac402eb` |
| `questdirectorfsh30001.lua` | `3e0ff70fdc356baea768e99c7b5bb978fd866602f169ad6cf7766fe93a4faf33` |
| `questdirectorfsh30601.lua` | `d4123e98569121217caebeffe50f3438c0b10e17db4d6cc2e05922ffbbad84de` |
| `questdirectorgld20001.lua` | `0d22bf2e4d8ee4ff311444283ea141ba81a8e9d95fd4e20f6912727892b54cb2` |
| `questdirectorgld30601.lua` | `015df5d9bb75f46bcb550f6f321a5a9611949b8ebdc0c714cc0a8ab39fda3ec4` |
| `questdirectorhrv20001.lua` | `9dce66c981fea590473707d166c9b4cd38952cfe47101c29cc5fb43ea14d2c51` |
| `questdirectorhrv30001.lua` | `77329b1051881b9bbdf2df90cdbf3b22dafe1aaa9203edf9439c4cdf094fc4e8` |
| `questdirectorhrv30601.lua` | `da50f4b3e25cfad975a4e0a0ae75f3c6ddd9344ef4eabd7e6b49ea5bbed2b1e8` |
| `questdirectorhrv30602.lua` | `14284ec82117fe4f7a82d10ffa15095b96ae838ea37b123c0ed43fdac3b0cce5` |
| `questdirectorlnc30601.lua` | `e62dcaa1a7fea77f7a1d64d325cca7869546584e8bab9c5f60222a1fa5715c6f` |
| `questdirectormin20001.lua` | `8aa094cccc1e02cae245dc2f138574600539897a12e4b167fea4454035866b61` |
| `questdirectormin30001.lua` | `614c988cb4b18ca3574b561e72538a14d74badb86d989989d6de99a83188e8d6` |
| `questdirectormin30601.lua` | `34211dca664c4a072f45adcbd395a9c6a49932bcb94c283e9ce2f7a450cb954e` |
| `simplequestbattle/questdirectorwar0j301.lua` | `44d70dce639d63f52486318db546f20632216eaab9c1b6e4888cd66b944ac742` |
| `questdirectorwar0j601.lua` | `b23bce487a8eb361295411b9e3ba6fa39ee8b090140a0c90def132bf33937132` |
| `simplequestbattle/questdirectorwhm0j401.lua` | `dae9452f903ddcd61dee16ac3c0be229e7fe17b65c72e44ce6e4530578d905b1` |
| `questdirectorwvr20001.lua` | `93f8edc95be8776ec57ebede46c878b36f305724999a75e5e9275f8987659cf3` |
| `questdirectorwvr30001.lua` | `50a5d148c5f0e2dc81cc2fa664bd00337414116791b30556c1707d6305ece132` |
| `simplequestbattle/questdirectorwvr30601.lua` | `893495002371080ebea08294a4c3176e68a57b7e88aa44eeb02b09ad1ba0cb8d` |

The `SpecterNormalPld0j1` chunk (decoded SHA-256
`590e5e1044e94876fb9cd8e90dd7cfd57d4552881d9b0978aa97f77b2bc7e120`)
matched its recovered bytecode. Its entire body requires
`SpecterBaseClass` and declares the subclass; it contains no actor-class ID
or quest target binding. The separate retail actor-class/display join for
`2206901` is recorded in
`xivl-client-data:docs/job-quest-combat-display-joins.md`. Class-file
existence does not connect the two. Source locator:
`lua/scripts/chara/npc/monster/specter/specternormalpld0j1.lua`, with the
LPB path in its `.calls.json` sidecar.

## Grand Company distinctions

### Official enlistment presentation

The three `Com0*7` start methods each call
`askEventModeWidgetYield("Ask/GrandCompanyOfficialJoinWidget", 1, company)`
once, with company 1, 2, or 3, and consume its two return values separately.
The recovered Lua text repeats the call in an `if`, but the decoded Lua 5.1
bytecode has one `CALL` with two
results. On the accepted branch, each method presents its own company number
and literal rank 11 through `openGrandCompanyJoinEffectWidget`, then updates
the status widget. The FAQ menu remains a separate repeatable client path.
The end methods close the status presentation; neither method is a server
membership or points transaction.

| Script / start method | Company | Decoded chunk SHA-256 | LPB leaf |
| --- | ---: | --- | --- |
| `Com0l7.processEventGuincamStart` | 1 | `7fc28b2420c371d8148b99e2a8513b283adf12375d0ceb419b4b72bdb2373433` | `7vxjyc.le.lpb` |
| `Com0g7.processEventFulkeStart` | 2 | `c33194551226d96ad6d1d416b744b2c211fbb3457d4c67f4f2c9ac30b6aa83e8` | `7vxj3c.le.lpb` |
| `Com0u7.processEventAubreyStart` | 3 | `241134ea44074bf9855a3cefbd9dda50fd51fd39e5f04c2a533d78c513cfa8f9` | `7vxjpc.le.lpb` |

Each decoded chunk was matched byte-for-byte to its LPB under
`client/script/tp5rq/r75w9s1v/7vx/`. The corresponding canonical script
locators are `lua/scripts/quest/scenario/com/com0l7.lua`, `com0g7.lua`, and
`com0u7.lua`; their `.calls.json` sidecars provide full ciphered paths.
The two-result calls are at bytecode PCs 94, 99, and 86 respectively in the
named start methods. Company/rank widget calls are at PCs 110, 115, and 102.
These values describe client presentation, not an authoritative enlistment
condition or a retail-observed acceptance.

### Seal tutorial status widget

The separate `Com0*2` start methods open the Grand Company status widget
with their company argument, then set its displayed points to 0. Their
paired end/final methods set the displayed points to 250 and close the
widget after a wait. The LPBs decode byte-for-byte to the
recovered chunks:

| Script / LPB leaf | Start / open argument | End method | Decoded SHA-256 |
| --- | --- | --- | --- |
| `Com0l2` / `7vxjyh.le.lpb` | `processEventGUINCUMStart` / 1 | `processEventGUINCUMEnd` | `e73740a8efeecd5609e9ba47dd1404b58350350585dc0919c79b96c7f48629a1` |
| `Com0g2` / `7vxj3h.le.lpb` | `processEventFulkeStart` / 2 | `processEventFulkeEnd` | `cd98f56dd6cc8b364537b6125be17ec67cc64f209a24e2520fab3a6a5a84bf57` |
| `Com0u2` / `7vxjph.le.lpb` | `processEventAUBREYStart` / 3 | `processEventAUBREYFinal` | `80c320cafa8fc3448dc5d99ab4db6fc889630e5155aa5d18ee260ba0e80371ec` |

The source locators are `lua/scripts/quest/scenario/com/com0l2.lua`,
`com0g2.lua`, and `com0u2.lua`; their `.calls.json` sidecars give the
full ciphered paths. In the decoded bytecode, the start open/set calls
are at PCs 58/62, 53/57, and 56/60, respectively. The paired set/close
calls are at PCs 4/11, 4/11, and 1/8. These values are client UI
operations, not evidence that 250 seals were granted or that a failed
server transaction closed the widget.

The three level-40 company scripts are separate scenario classes with
different salutes, speakers, branches, and movie ownership. Similar quest
roles do not justify sharing one client flow.

At the earlier `101` phase, `Gcl101` itself defines
`processEventGuincumStart`, `processEventFulkeStart`, and
`processEventAubreyStart`. Its Aubrey method tests its fifth method argument
against Lua boolean `true` at PC 21 (`0xBFE`), selecting different rows
before reconverging. The separate `Gcg101` and `Gcu101` chunks
each define a class directly on `ScenarioBaseClass` and only an empty
`initText`; neither chunk supplies inheritance or a dispatcher into
`Gcl101`. Thus the three narrative methods exist, but these chunks do not
establish which client or server owner selected them in retail.

The decoded chunks match the LPBs exactly: `Gcl101` at
`tp5rq/r75w9s1v/37y/37yiji.le.lpb` (SHA-256
`b6575da42c43113f619c92abeff73be62ed449ae7002ef1e0f25015b69506cd5`),
`Gcg101` at `tp5rq/r75w9s1v/373/373iji.le.lpb` (SHA-256
`e8b460fccf04f74901e11fc934c8b55a3d2d97480656351f476d4f3f92960375`),
and `Gcu101` at `tp5rq/r75w9s1v/37p/37piji.le.lpb` (SHA-256
`756357ba5ebf12100641f5abaf47c35936f227f77e9efbca1a33245f7b908259`).
Canonical method locators are `lua/scripts/quest/scenario/gcl/gcl101.lua`,
`gcg/gcg101.lua`, and `gcu/gcu101.lua`.

| Script | Company-specific client contract |
| --- | --- |
| `Gcl102` | salute company 1; `processEventNQ` plays `gc01l210` and uses the after-warp finalizer |
| `Gcg102` | salute company 2; `processEventPfrymloefNQ` plays `gc01g210`, uses the default finalizer, then emits text row 58 |
| `Gcu102` | salute company 3; `processEvent015` plays `gc01u210` with the default finalizer; two additional elevator methods play `elv0u01a` and `elv0u02a` with after-warp finalizers |

`Gcu102.processEvent000_3`, `_4`, and `_5` each call
`isUpperRank(3, 11)` and choose different text rows for the true and false
branches. This is client presentation evidence for a rank-dependent branch,
not proof that the client is authoritative for promotion or quest admission.

Several methods accept an extra argument that changes dialog. For example,
`Gcg102.processEventQuinquerol` selects row 25 when its fourth argument equals
1 and rows 22 through 24 otherwise; both branches then converge on the same
remaining dialog. `Gcu102.processEvent005` similarly chooses row 19 or 20 from
its fourth argument before converging. Preserve these parameters as distinct
client inputs until their server producers are independently recovered.

The Echo prompts are separate methods from those NQ presentations.
`Gcg102.processEventPfrymloefNQF` and `Gcu102.processEvent010` each ask
`worldMaster` row 51030, mode 2, exactly once. Only answer 1 calls
`runCharaSchedulerPastAreaIn` with the player argument. The Gridanian method
also says row 39 on the other branch; the Ul'dahn method returns without that
extra line. Their decoded bytecode has one `ask` call at PC 11 (`0x1090` and
`0x114A`) and the conditional scheduler call at PC 16 (`0x10A4` and `0x115E`).
The repeated `ask` in recovered Lua return expressions is a decompiler
artifact, not a second prompt. No method-to-method transition or Echo
acceptance condition is established by these scripts.

The decoded `gcg102` and `gcu102` chunks match their LPBs exactly:
`tp5rq/r75w9s1v/373/373ijh.le.lpb` has decoded SHA-256
`1323f828a2592df94e5fbcec1db0c9de0b26154e40abd0f6c9bcdb7b5199f941d`;
`tp5rq/r75w9s1v/37p/37pijh.le.lpb` has decoded SHA-256
`1aac5bff87ce91ebc0d68b423330d784b18da14c0f26d1f40e2375f06e0afbad`.

Sources:

- `lua/scripts/quest/scenario/gcl/gcl102.lua`.
- `lua/scripts/quest/scenario/gcg/gcg102.lua`.
- `lua/scripts/quest/scenario/gcu/gcu102.lua`.

## Dragoon 60 presentation split

`Drg0j6.processEvent020` and `processEvent025` both play scene `Drg0j620`
in mode 1 after default fade-out. The former ends with the after-warp fade-in;
the latter uses the default fade-in. A separate `processEvent030` presents
ability 27268 and literal item 8032704 through job widgets after dialogue.
Those widget calls do not establish an authoritative reward grant, event
ordering, or a warp destination.

Source: `lua/scripts/quest/scenario/drg/drg0j6.lua`, LPB resource
`tp5rq/r75w9s1v/6s3/6s3j0d.le.lpb` (decoded SHA-256
`a6b34d7bcb9ec44a5c978d41ee05b1a9efd6dc5244935ca62bb0bbd5d607ddb`).
The donor bytecode matches the decoded chunk exactly. Relevant
locators are `processEvent020` PCs 3-9 (`0x78B-0x7A3`), `025` PCs 3-9
(`0x84E-0x866`), and `030` PCs 30-41 (`0x97B-0x9A7`).

## Shared cutscene boundary

The scenario helpers make the client-side ownership model explicit:

```text
startNQCutScene(sceneKey, mode, ...)
  -> createCutScene(sceneKey, quest)
  -> startCutScene(1, 61, mode, ...)
  -> delete the same scene object after completion
```

Default fade-in waits for map loading, fades in, and waits for fading.
After-warp fade-in is a distinct native-facing finalizer; its script body does
not contain a destination zone or coordinate. A consumer must preserve the
distinction without inventing the missing server transition.

Movie skipping acts on the same scene actor. It does not create a separate
quest-level success path, reward grant, or destination contract.

## Evidence boundary

These scripts prove ordered client API calls, literal scene keys, method
arguments, conditional branches, and talk-turn ownership. They do not prove
objective completion, combat composition, authoritative rank checks, rewards,
world placements, or the server event that chooses a method. Scene-local actor
positions and native cutscene record layouts belong to separate client-data or
decomp evidence and are not inferred here.
