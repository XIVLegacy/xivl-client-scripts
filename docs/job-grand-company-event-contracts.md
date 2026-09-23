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

`Mnk0j6` preserves distinct Erik and Widargelt methods rather than one generic
quest-giver flow. `processEvent020_ERIC_Follow` and
`processEvent020_ERIC_PUB` are Erik-owned talk turns;
`processEventWIDARGELT_PUB` is a separate Widargelt-owned turn.
`processEventClear` owns information dialog 115 and job ability 27106.

The separation proves dialog and presentation ownership. It does not prove
which server actor advances the objective or which encounter state unlocks
each method.

Source: `lua/scripts/quest/scenario/mnk/mnk0j6.lua`, the three named speaker
methods and `processEventClear`.

### Black Mage

`Blm0j3.processEvent000` is a closed talk turn with text rows 11 through 13.
`processEvent005` is a longer introduction path: its fourth argument is passed
to text row 14, followed by rows 15 through 19 and 42 around a one-second
fade-out/fade-in pair. The argument is part of the client ABI and must not be
dropped or synthesized from the method name.

The two methods are distinct event phases. Finding both on the same quest
class does not make them interchangeable or establish their server-side actor
binding.

Source: `lua/scripts/quest/scenario/blm/blm0j3.lua`, methods
`processEvent000` and `processEvent005`.

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

### White Mage

`Whm0j1.processEventClear` opens a talk turn and deliberately leaves it open
after text row 24. `processEventClearNQ` performs the default fade-out, closes
that retained talk turn, waits one second, plays `whm0j110`, and performs the
default fade-in. The methods form a paired handoff; inserting an independent
event close between them changes the recovered client sequence.

Source: `lua/scripts/quest/scenario/whm/whm0j1.lua`, methods
`processEventClear` and `processEventClearNQ`.

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

The recovered Lua for these eight scripts was checked against the installed
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

Each recovered chunk matched the decoded installed LPB byte-for-byte. Source
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

The installed `SpecterNormalPld0j1` chunk (decoded SHA-256
`590e5e1044e94876fb9cd8e90dd7cfd57d4552881d9b0978aa97f77b2bc7e120`)
matched its recovered bytecode. Its entire body requires
`SpecterBaseClass` and declares the subclass; it contains no actor-class ID
or quest target binding. The separate retail actor-class/display join for
`2206901` is recorded in
`xivl-client-data:docs/job-quest-combat-display-joins.md`. Class-file
existence does not connect the two. Source locator:
`lua/scripts/chara/npc/monster/specter/specternormalpld0j1.lua`, with the
installed LPB path in its `.calls.json` sidecar.

## Grand Company distinctions

The three level-40 company scripts are separate scenario classes with
different salutes, speakers, branches, and movie ownership. Similar quest
roles do not justify sharing one client flow.

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

Sources:

- `lua/scripts/quest/scenario/gcl/gcl102.lua`.
- `lua/scripts/quest/scenario/gcg/gcg102.lua`.
- `lua/scripts/quest/scenario/gcu/gcu102.lua`.

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
