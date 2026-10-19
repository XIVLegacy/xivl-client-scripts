# Map-object door client contract

The retail corpus contains two door initializers. `DoorStandard` constructs a
six-entry second schema table and drives its own reaction timers; `DoorServer`
constructs the two shared map entries and uses its final initializer argument
as a scheduler switch. The source identities and LPB identities below were
matched through `manifests/scripts.json` and `manifests/retail_lua_coverage.json`.

Static checks used `tools/retail_script.py decode_lpb` and
`tools/build_quest_contracts.py` (`ChunkReader`, `instruction`, `call_record`,
`states_for`, and `walk`) for prototype, call, branch, and return locators.
Decompiler control flow was accepted only where it agreed with the source and
decoded instruction stream.

## DoorStandard initialization

The canonical body is at
`lua/scripts/chara/npc/mapobj/doorstandard.lua:11-115` (source SHA-256
`f4656dbfd56e2170538138b7fe750fb0ec53240674f5c0161cea6a1abd6973a6`). Its
retail resource is
`client/script/729s9/wu7/x9uv80/6vvsrq9w69s6.le.lpb` (raw SHA-256
`ac568a3583bd11a39a7fdf91fbf9bc1750a871127a9b1911d7a3e57fe5a6dc3f`,
decoded payload SHA-256
`0087b00f4006a262486eda3e45606dd5bb229ff8c9fd1ece08ed811af69f4c1f`).

`NpcBaseClass._onInit` first passes fixed arguments `A2` and `A3` to the
superclass, then parses count-prefixed variadic segments before calling the
child `initForEvent` (`lua/scripts/chara/npc/npcbaseclass.lua:110-278`). That
source is SHA-256
`f18c6c3198db0402431ca6aa683b601afbf5a0dc5c22481b3c1da1deabef0dc2`; its
retail resource is `client/script/729s9/wu7/wu789r57y9rr.le.lpb` (raw
SHA-256 `3f1dcc3416f7e22db138a6dcc730b095f81f3d0ceb458a7ded7d5b0d17df55c9`,
decoded payload SHA-256
`1941c40b64cacd721d271b36e31017a24f908b8ea518f713b44da17bb4e57627`).
The shared `initWork` helper declares writes to temporary and synchronized
schema tables in `work._temp` and `work._sync`; its positional behavior is
addressed below (`lua/scripts/chara/npc/npcbaseclass.lua:311-327`).

The authenticated retail corpus contains the candidate superclass body
`CharaBaseClass._onInit(self, A1, A2)` at
`lua/scripts/chara/charabaseclass.lua:534-1126` (source SHA-256
`f17b3e62a137d8f524ba88d55296e1fb064512dc803f7a85dc980dd4bcbc9625`,
resource `client/script/729s9/729s989r57y9rr.le.lpb`, raw SHA-256
`c7cd1dad84f7d9b723f5a10fb66108da9d9d6ef5d7c15186b48ec55092465238`,
decoded payload SHA-256
`101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9`).
Its decoded body is `root/proto21` (three parameters, no vararg, code offset
6001, 474 instructions). The native superclass route is exposed by the
authenticated `lua/scripts/actorbaseclass_u.lua:14-21` wrapper (source SHA-256
`890997302a35d8217fb7c8f68105e9cc82dbfe7a77654348588bb7d4195986dd`,
resource `client/script/97qvs89r57y9rr_p.le.lpb`, raw SHA-256
`008c68b70373b9d8decf53d6dc53f1f2d384ddf8ee7e6e5a5e9bddef6a34504c`,
decoded payload SHA-256
`28d5d3b3fcd26cdb18394b3e9d937b3a5514cf8ff0b3b4c4196efda82d4596b1`),
which returns `_callSuperClassFunction_cpp` from decoded `root/proto1` PC 2 /
offset 587; the API catalog records this as BCS-Y-0403 but publishes no typed
argument signature or Lua parent link. The gate meanings in the table are
therefore conditional on that native route resolving `NpcBaseClass` to this
`CharaBaseClass` body; the NpcBase source itself proves only the values passed
to `_callSuperClassFunc`.

For the supplied six-value tail after the actor-class argument, the forwarding
chain is:

| position | supplied value | static destination and meaning |
| --- | --- | --- |
| fixed `A2` | `false` | Passed as the first superclass argument. If the native route resolves to `CharaBaseClass._onInit` `A1`, it is the `gameParameter` gate: it stores `charaWork.gameParameter`, gates common/event parameter sync setup, and gates parameter/event work bindings; `false` skips those branches. |
| fixed `A3` | `false` | Passed as the second superclass argument. If the native route resolves to `CharaBaseClass._onInit` `A2`, it is the battle-work gate: it gates `battleSave`/`battleTemp` setup, `initBattleSync`, and the non-player `battleSave.potencial` binding; `false` skips those branches. |
| variadic 1 | `0` | Lua numeric first segment count; `initForBattleCommon` is skipped. |
| variadic 2 | `0` | Lua numeric second segment count; `initForEventCommon` is skipped. |
| variadic 3 | `layout` | Caller value with no type declaration here; after the two zero counts it is forwarded as the first value to `initForBattle` and as child `DoorStandard.initForEvent` `A1`. |
| variadic 4 | `instance` | Caller value with no type declaration here; forwarded as the second value to `initForBattle` and as child `DoorStandard.initForEvent` `A2`. |

The two zero values are the common-segment counts: the source tests each with
`0 < count`, then advances by `count + 1`. With both counts zero, the next
selection index is three, so both `initForBattle(select(3, ...))` and the child
`initForEvent(select(3, ...))` see `layout, instance` (`npcbaseclass.lua:224-278`).
The inherited battle helper is authenticated at
`lua/scripts/chara/npc/npcbaseclass_battle.lua:7-70` (source SHA-256
`e277df19d98ce7abf062e9345fa5b73e051fe8085d15b07780d26d5e0470fbf0`, resource
`client/script/729s9/wu7/wu789r57y9rr_89qqy5.le.lpb`, raw SHA-256
`feea4b9c4d4e2336dc3f4b4d6d1128212d78628df20249d7157a401693d57dc5`, payload
SHA-256 `2f80ba2e710c6a4a762f280c778cd96db31a8996c9b4369a0399e96bbc8aa965`).
Its default `initForBattle` is empty, while a nonzero battle-common segment
would consume `aggro` (`integer8`), `partsName` (`integer32`), and eight
`partsExists` booleans (`npcbaseclass_battle.lua:13-68`). The event helper is
authenticated at `lua/scripts/chara/npc/npcbaseclass_event.lua:13-32` (source
SHA-256 `5417b1bdf762162cad240a84715d0fc85958dbe0181b653348a66c02ee4d7c80`,
resource `client/script/729s9/wu7/wu789r57y9rr_5o5wq.le.lpb`, raw SHA-256
`84a5098636ff289f4ecf4e164e84e44890895e8a9005fb102e04929c2bb74bf9`, payload
SHA-256 `4a3008dd8d2a91e7eb044e5555d2757468a9097bba5175992fb88f943bd07b6c`).
Its common initializer consumes no segment values; it only checks the extra
stat and may call `_setGroundOn(false)`.

The superclass decode corroborates these gates in `root/proto21`: the calls to
`initCommonParameterSync`, `initBattleSync`, and `initEventSyncWork` are PCs
168 / offset 6673, 211 / offset 6845, and 263 / offset 7053. The parameter
bindings are PCs 433-457 / offsets 7733-7829 and the battle `potencial` binding
is PC 467 / offset 7869 (`charabaseclass.lua:782-935, 1058-1117`).
This narrows the first two false values to the client-used Boolean gates in the
candidate CharaBase body; native dispatch evidence still withholds the direct
NpcBase-to-CharaBase parent link, a friendlier type name, and a typed
signature.

The child function is fixed-arity `DoorStandard.initForEvent(self, A1, A2,
A3)`, not a variadic six-value consumer. For this tail it receives
`A1=layout`, `A2=instance`, and `A3=nil`. For actor class 5900001 those two
values are used only as the two `_setReactionTriggerBox` arguments
(`doorstandard.lua:69-85`); they are not assigned to `_sync.layout` or
`_sync.instance`. A seventh overall tail value, after
`false,false,0,0,layout,instance`, would bind to the existing child `A3`, and
the child body never reads it. Only values after that method `A3` are discarded
by the fixed-arity call boundary. The constructed schema therefore has no
seventh slot, and the declared `layout` and `instance` types below are schema
declarations rather than types of the forwarded tail values. The decoded root
prototype has four parameters including `self`, no vararg, and 78 instructions.
Its `initWork` call is followed by the trigger and scheduler calls described
below.

There is a positional discrepancy in the shared schema helper that the frozen
corpus cannot resolve through a hidden wrapper. `NpcBaseClass.initWork` declares
`(self, A1, A2, A3)` but writes `A2` to `work._temp` and `A3` to `work._sync`,
defaulting each missing value to `{}` (`npcbaseclass.lua:311-327`; decoded
`root/proto13`, four parameters, 11 instructions, writes at PCs 4 / offset
3299 and 9 / offset 3319). `DoorStandard` passes exactly
`initWork(self, firstDummyTable, secondSixEntryTable)` at PC 37 / offset 425,
so this document reports the six declarations constructed by the source as a
second table and does not assert that they occupy runtime `work._sync`.
Resolving the placement requires a captured LGE method wrapper or runtime work
object; neither is present in the frozen corpus. Resolving the superclass
identity requires native parent-registration evidence or a runtime capture of
`_callSuperClassFunction_cpp` for this NpcBase object; the frozen catalogs do
not establish that link.

The trigger native boundary is also narrower than the schema declarations.
`DoorStandard` passes `("in", A1, A2, "door", nil)` and
`("out", A1, A2, "door", true)` (`doorstandard.lua:69-85`). The authenticated
`lua/scripts/chara/npc/npcbaseclass_u.lua:160-167` wrapper accepts `self` plus five Lua arguments and
returns `_setReactionTriggerBox_cpp` (source SHA-256
`74a54c805173f12c5513c2746c4ea65846f024438b0cf44116e77270da3faa0c`,
resource `client/script/729s9/wu7/wu789r57y9rr_p.le.lpb`, raw SHA-256
`1400e76a2735a079726a9920596f1b124c5f9bc912d0af6ff9635348f9cad6f8`,
decoded payload SHA-256
`26ff1eb8502d975cf8a23c34b211d49265e434998966762bd4bf0d0fccbf38ff`).
The decoded wrapper is `root/proto16`; its return is PC 2 / offset 2375. The
API catalogs identify BCS-Y-0212/BCS-Y-0334 and the native slot, but give no
argument widths or types. Therefore the caller values `layout` and `instance`
remain untyped at this boundary; their `integer16` declarations in
the constructed schema table do not prove trigger argument widths.

The declared work fields are ordered as follows:

| constructed table | slot | declared type | observed client use |
| --- | --- | --- | --- |
| first constructed table | `dummy` | `integer32` | Declared by the initializer; no read by this class. |
| second constructed table | `layout` | `integer16` | Declared by the initializer; no read by this class. |
| second constructed table | `instance` | `integer16` | Declared by the initializer; no read by this class. |
| second constructed table | `count` | `integer8` | The reaction body reads and updates `work.count`, incrementing on `in`, decrementing on the other reaction, and clamping at zero. |
| second constructed table | `timerAfterOpen` | `timer` | The reaction body writes a two-second delay or a server-time-derived remaining value; `processTimer` consumes it to schedule `clos`. |
| second constructed table | `timerAfterClose` | `timer` | The reaction body writes a two-second delay or a server-time-derived remaining value; `processTimer` consumes it to schedule `open`. |
| second constructed table | `serverTimeAnimation` | `integer32` | `_onReaction` reads it with the current server time to choose the timer delay; `processTimer` writes `_getServerTime()` before the opposite scheduler runs. |

The `timer` declarations include the literal `true` flag at
`doorstandard.lua:36-49`; this class does not expose a further name for that
flag. These six entries are the complete second-table schema constructed by
this initializer. The direct `initWork` assignment described above leaves the
runtime table placement unresolved. `initForEvent` accepts `A3` but never reads
it, and the decoded function is non-variadic, so only arguments after `A3` are
ignored by the Lua call boundary rather than being assigned to a hidden seventh
field.
The child `A1` and `A2` values are used only when actor class 5900001 installs
the `in` and `out` reaction boxes (`doorstandard.lua:69-85`).

The class installs three actor-class-specific actions:

* Actor class 5900001 binds the `in` and `out` reaction boxes, passing `A1`
  and `A2` into `_setReactionTriggerBox`.
* Actor class 5900003 starts scheduler `open` from offset 5.
* Actor class 5900004 starts scheduler `clos` from offset 5.

After those branches it calls `_setGroundOn(false)`
(`doorstandard.lua:88-115`). `_onReaction` compares its reaction name with
`in`, updates `count`, and starts `open` or `clos` immediately when the
server-time threshold has passed; otherwise it writes the matching timer
(`doorstandard.lua:118-201`). `processTimer` handles those two timer names,
refreshes `serverTimeAnimation`, and starts the opposite scheduler when the
count state requires it (`doorstandard.lua:204-241`). These are the only
consumers of the six declared second-table fields found in this class.

Static bytecode corroboration identifies `NpcBaseClass._onInit` as root/proto10
with parameters 4 and a vararg, with `_callSuperClassFunc` at PC 4 / offset
1983, the first count select at PC 89 / offset 2323, the battle-common call at
PC 98 / offset 2359, the event-common call at PC 117 / offset 2435, the
inherited battle call at PC 129 / offset 2483, and the child call at PC 135 /
offset 2507. The helper decode identifies the battle-common field selects at
PCs 24, 31, and 43 / offsets 442, 470, and 518, and the event-common
extra-stat and ground-off calls at PCs 1 and 6 / offsets 878 and 898. The
`DoorStandard.initForEvent` call sites are root/proto0 PC 37 / offset 425
(`initWork`), PCs 48 and 55 / offsets 469 and 497 (trigger boxes), PCs 64 and
73 / offsets 533 and 569 (`open` and `clos`), and PC 76 / offset 581 (ground
off). This confirms the forwarding order, source slot order, and fixed method
arity without assigning meanings to the unused `dummy`, `layout`, or `instance`
schema fields.

Q1 status is narrowed, not fully closed at the native boundaries. The Lua
forwarding chain, the two zero count slots, the candidate superclass gate uses,
the child `A1/A2` trigger positions, the seventh value's existing child `A3`
binding, the source-declared schema entries, and the `DoorServer` final branch
are closed by authenticated source and bytecode. The frozen corpus leaves the
NpcBase-to-CharaBase native parent identity, the runtime `initWork` table
placement, and native trigger argument widths/types open. The exact settling
specimen is a retail native trace that records (1) BCS-Y-0403
`_callSuperClassFunction_cpp` for this NpcBase object at NpcBase root/proto10
PC 4 / offset 1983, including the resolved class/method and converted Lua
argument types/values; (2) the post-`initWork` `work._temp` and `work._sync`
objects at DoorStandard PC 37 / offset 425 or NpcBase root/proto13 PCs 4 and 9
/ offsets 3299 and 3319; and (3) BCS-Y-0212/BCS-Y-0334
`_setReactionTriggerBox_cpp` at DoorStandard PCs 48 and 55 / offsets 469 and
497, including native argument conversions. The retail corpus is frozen, so
these are evidence requirements rather than acquisition steps.

## DoorServer comparison

The canonical `DoorServer.initForEvent` body is at
`lua/scripts/chara/npc/mapobj/doorserver.lua:11-62` (source SHA-256
`7cbd05f45800e60a21c7b59a728b42bc8115d97c88ce4a91703b37bbe784540c`). Its
retail resource is
`client/script/729s9/wu7/x9uv80/6vvsr5so5s.le.lpb` (raw SHA-256
`4aeeb74b47fb1bee784d73abacc7f54f517f42c47282f9efbe156b39ddd009df`,
decoded payload SHA-256
`4dfdefed20a6f1b433657252828729becffae17d1f4cf0b2c7a1e9718384fb6b`).
The canonical class and method inventory is in
[`registry.json`](../lua/registry.json) under `chara/npc/mapobj/doorserver`.

`DoorServer.initForEvent(self, A1, A2, A3)` constructs the same first-table
`dummy` field and second-table `layout` and `instance` fields
(`doorserver.lua:13-32`). It passes those tables as
`initWork(self, firstDummyTable, secondLayoutInstanceTable)` at PC 19 / offset
292, so the same helper positional discrepancy applies: the second table is
the source declaration, while runtime `_sync` placement is unresolved.
`A1` and `A2` are accepted but unused. When `A3`
is exactly `true`, actor class 5900015 requests scheduler `open` from offset
5; every other actor class requests `hide` from offset 5. For false or any
other non-true value, neither scheduler branch runs. The method then calls
`_setGroundOn(false)` (`doorserver.lua:33-62`). Its decoded root prototype
also has four parameters, no vararg, and 39 instructions; the bytecode contains
the `A3 == true` branch at PC 20 / offset 296, the `open` and `hide` calls at
PCs 29 and 34 / offsets 332 and 352, and the final ground-off call at PC 37 /
offset 364.

The shared field names do not establish shared runtime semantics: `DoorServer`
never reads `layout` or `instance`, while `DoorStandard` reads only its
`count`, timer, and server-time fields after initialization. Neither body
identifies the producer of an initial argument, actor placement, or collision
behavior.

## Beacon Fort status gate

The `BeaconFortGateGimmick` chunk matched the recovered LUAC
byte-for-byte (decoded SHA256
`17635FDA7214B70895AFFA0AA978E333F53779AE87D762295048DCAC5BD09EED`).
`initForGimmick` stores supplied show/hide scheduler names and an initial
`currentStatus` of zero, and tags the synced `status` field as `mapStat`.
`processUpdateWork` calls `executeScheduler` only when `status` differs from
`currentStatus`. Status 1 selects the supplied show name; other values select
the hide name. When the previous status is zero, `executeScheduler` calls
`_runBgSchedulerFromMidstream(name, 5)`; otherwise it calls
`_runBgScheduler(name)`, then retains the new status
(`beaconfortgategimmick.lua:3-67`; source identity
`manifests/scripts.json:572-577`). The script does not identify a retail
actor class ID, placement, status producer, or observed gate appearance.
