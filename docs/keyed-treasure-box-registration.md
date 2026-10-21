# Keyed treasure-box registration contract

The original 1.23b Lua accepts a PublicTreasureBox with no class-specific
initializer tail, or a GimmickTreasureBox with a talk-range number followed
by a marker boolean. Both inherit the NPC initializer's actor-class value,
two superclass gates and two common-segment counts. Registration does not
automatically invoke either key question. A subsequent event must select the
coffer instance and its named helper.

This is a static client contract, with compatible argument compositions below.
No retained keyed registration/interaction authenticates a complete server
spawn sequence, actor-class number, condition record or opening policy.
The [open-world coffer finding](open-world-key-coffer-contract.md) owns key
items, confirmation text, capture coverage and the cadence discriminator.

## Registration envelope and appearance

These are separate client inputs. All native offsets below use retail
`ffxivgame.exe`, image base `0x00400000`, 15996808 bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
Application offsets exclude the 16-byte game-message prefix. Original PE
reads used pefile `2024.8.26` and Capstone `5.0.7`, x86-32. The existing
`xivl-decomp:docs/net/guildleve-initializer-route.md#native-body-and-prefix`
and `xivl-client-structs:docs/door-initialization-native-contract.md` own the
generic dispatch, superclass and argument-preservation proofs.

| Input | Original native consumer and observation |
| --- | --- |
| s2c `0x00CC`, application `+0x00` | `0x00774BDA..0x00774BE6` reads a dword and updates native context `+0x14` when different. This read does not supply the Lua `npcWork.actorClassId` assignment below. Its keyed-coffer value remains unbound. |
| `0x00CC`, application `+0x04` / `+0x24` | `0x00774BF0..0x00774BFB` / `0x00774C11..0x00774C1C` construct name/class strings. The nominal fields are 32 bytes each. Supply in-field NUL termination; the string constructor is not a field-width validator. |
| `0x00CC`, application `+0x44`, length `0xC0` | `0x00774C29..0x00774C36` creates the initializer reader. It consumes a tagged path string, five native Boolean controls and then typed Lua values. The path/controls are not Lua `_onInit` arguments. |
| s2c `0x00D6` | `0x0058D0C6..0x0058D108` reads appearance records at application `+8*i`: dword value at `+0`, byte index at `+4`, eight-byte stride. Count is a byte at application `+0x100`. `0x00586870..0x0058689C` writes accepted indices below 28 into actor `+0xAAC+4*index` and marks it dirty. It supplies no Lua initializer values. |

The `0x00D6` format has space for 32 records before its count; the inspected
loop does not clamp that count. Three bytes per record are not read there.
Its appearance values, complete packet extent and order relative to this
coffer's registration are not established by these Lua classes. See
`xivl-client-structs:docs/appearance-record-wire-contract.md` and
`xivl-decomp:docs/actor/appearance-path-decoder.md#wire-index-to-helper-field`.

The leaf class/path pairs are:

| Class field | Path string in the initializer reader | Lua parent |
| --- | --- | --- |
| `PublicTreasureBox` | `/Chara/Npc/Object/TreasureBox/PublicTreasureBox` | `TreasureBoxBaseClass`, then `NpcBaseClass` |
| `GimmickTreasureBox` | `/Chara/Npc/Gimmick/GimmickTreasureBox` | `GimmickNpcBaseClass`, then `NpcBaseClass` |

The leaf declarations are source lines `1-8`, root PCs `0-6`, with actual
require/definition CALL PCs `2/6`. Each base declares its NPC parent at the
same root PCs. These script names are separate from the numeric class value
and actor instance key.

For an ordinary non-current-player registration, an all-false control prefix
is a supported static composition. The first control selects the deferred
initialization arm; the other four skip optional native read bundles. The
five Boolean reads are CALLs at `0x00774CCE/0x00774CD5/0x00774DD1/0x00774E40/0x00774E8D`.
Helper `0x0078F840..0x0078F86B` consumes one byte, true only for `0x03`.
The remainder visitor is called at `0x00774FE9`; submission at `0x007750B0`
preserves its vector. The separate current-player arm and non-false optional
bundles require their own arguments.

Compatible reader contents are expressed here as typed tokens, not a captured
packet or a guaranteed complete spawn:

```text
Public:  S(public-path) F F F F F  I(C) F F I(0) I(0) END
Gimmick: S(gimmick-path) F F F F F I(C) F F I(0) I(0) N(R) B(M) END
```

Here `F=0x04` false, `B(M)=0x03/0x04` true/false, `S=0x02` plus
NUL-terminated string, `I=0x00` plus int32, `N=0x01` plus float32, and
`END=0x0F`. Numeric payloads use the generic decoder's default big-endian
interpretation; its historical mutable endian selector remains unobserved.
The generic typed-token consumers are in
`xivl-decomp:docs/script/delegate-command-producer.md#typed-values-and-bounds`.
The entire path, controls, values and END must fit inside the `0xC0` reader.
The reader excludes application `+0x104..+0x107`; padding is not another
initializer argument. These examples choose both superclass gates false,
not integer zero: zero is truthy in Lua.

## Lua initializer arguments

Source paths below are beneath `lua/scripts/`. Prototypes are zero-based
immediate children of the root. PCs and decoded chunk byte offsets are
zero-based. `SELF` looks up a method; the cited `CALL` invokes it.

`chara/npc/npcbaseclass.lua:110-281`, `root/proto10`, code `0x7AF`, has
formal arguments `(self,A1,A2,A3,...)`:

| Position after self | Consumer and type boundary |
| ---: | --- |
| 1: `C` / A1 | Stores `npcWork.actorClassId=C` at PC `79`, then `_bindWork(5001,"npcWork","actorClassId")` at CALL PC `84`. The local descriptor is `integer32`; 5001 is a local work binding, not the actor-class number or property hash. |
| 2: A2 | First superclass gate. CALL PC `4` passes A2/A3 to `CharaBaseClass._onInit`; it does not pass C or the open tail. A2 becomes the superclass's game-parameter/event-work truthiness gate. |
| 3: A3 | Second superclass gate, used for battle work. False skips the gated battle setup; it does not suppress the later NPC child dispatch. |
| 4 onward | Count-prefixed common sections followed by the class-specific tail, described below. The counts have no omitted-value defaults. |

`chara/charabaseclass.lua:534-1126`, `root/proto21`, code `0x1771`, confirms
the superclass gates. A1 tests include PCs `260/426` before event work and
bindings; A2 tests include PCs `99/208/458` before battle work. Actual
`initEventSyncWork` / `initBattleSync` CALL PCs are `263/211`.
Source `:1061`, PC `417`, stores `charaWork.gameParameter=A1`.

For NPC varargs `v`, let `b=v[1]`, `j=2+b`, `e=v[j]`, and `k=j+1+e`.
The router tests `b>0` (PC `90`) and, if true, calls
`initForBattleCommon(C,select(2,...))` at PC `98`. It tests `e>0`
(PC `109`, selected at PC `108`) and calls
`initForEventCommon(C,select(j+1,...))` at PC `117` when true. It then calls
`initForBattle(select(k,...))` and `initForEvent(select(k,...))`, at PCs
`129/135`. The suffix is open: VARARG/CALL preserve all selected arguments.
The values b/e are count markers; none of these uses `select("#",...)`.

With markers `0,0`, both common calls are skipped and `k=3`. The default
`initForBattle` is empty (`chara/npc/npcbaseclass_battle.lua:7-10`,
`root/proto0`, code `0x12E`, PC `0` RETURN). A nonzero battle-common section
would consume aggro, partsName and eight partsExists values, with descriptors
`integer8`, `integer32` and eight booleans (`:13-70`, `root/proto1`, code
`0x15A`, select CALL PCs `24/31/43`). The event-common initializer only tests
the extra ground stat and may call `_setGroundOn(false)`; it ignores its
supplied values (`npcbaseclass_event.lua:19-32`, `root/proto2`, code
`0x36A`, CALL PCs `1/6`).

| Selected initializer | Actual consumption after the two zero markers |
| --- | --- |
| Public `initForEvent(self)` | `chara/npc/object/treasurebox/publictreasurebox.lua:11-19`, `root/proto0`, code `0x11D`, CALL PC `2`: only `_setGroundOn(false)`. No class-specific values are needed by this body. Extra values are ignored. |
| Treasure base `initForEvent(self)` | `treasureboxbaseclass.lua:11-27`, `root/proto0`, code `0x10E`, PCs `0-10`: declares its temporary reserve and calls `processInitTreasureBox` at PC `9`. **Public overrides this without calling it.** The empty hook is `:30-34`, `root/proto1`, PC `0`. |
| Gimmick base `initForEvent(self,R,...)` | `chara/npc/gimmick/gimmicknpcbaseclass.lua:11-45`, `root/proto0`, code `0x149`: stores R as `gimmickNpcWork.talkRange` at PC `21`, then forwards only the remaining tail to `initForGimmick` at open CALL PC `24`. R has a `float` descriptor and no fallback value. |
| Gimmick box `initForGimmick(self,M)` | `gimmicktreasurebox.lua:11-30`, `root/proto0`, code `0x146`: stores M as boolean `work.mapMarkerVisible` at PC `9`, then calls `_setGroundOn(false)` at PC `12`. Its marker getter returns M (`:33-40`, `root/proto1`, PCs `0-2`). |

Public inherits talk range 7 and default talk-marker visibility true/type 6
(`npcbaseclass_event.lua:4-10/821-836`, `root/proto0/15/16`, code
`0x301/0x1570/0x15A4`, return PCs `1/1/1`). Gimmick's talk getter returns R
(`gimmicknpcbaseclass.lua:54-61`, `root/proto2`, code `0x284`, PCs `0-2`).
The [TalkCommand contract](talk-command-client-contract.md) owns the separate
range consumer; these getters do not install an enabled talk condition.

## Work declarations and publication boundary

| Work table | Original declaration / assignment | Server-publication implication |
| --- | --- | --- |
| `npcWork._temp` | `npcbaseclass.lua:118-162`, proto10 PCs `8-29`: `actorClassId:integer32`, `eventCommon:nesting:8`, `battleCommon:nesting:8`, `_assignForChild:64`. C is assigned locally as above. `_save` is empty at PCs `5-7`. | C belongs in the initializer. No separate property publication is established as necessary to set it on this path. |
| `npcWork._sync` | `:163-223`, proto10 PCs `30-77`: `pushCommand:integer16`, `pushCommandSub:integer32`, `pushCommandPriority:integer8`, `hateType:integer8`, `_assignForChild:16`. Tags group the three push fields under `pushCommand` and hateType under `hate`. | These are named generic NPC sync declarations, not keyed opening/key/reward state. They do not establish that all four must be published for a talk-only question. |
| `treasureBoxWork._temp` | Treasure base proto0 PCs `0-7`: only `_assignForChild:64`. | Public skips this initializer. No named treasure-box sync field is declared by either selected treasure-box chunk. Do not send a guessed opened/key/timer property from this reserve. |
| `gimmickNpcWork` | Gimmick base proto0 PCs `0-21`: `_temp` contains `talkRange:float` and `_assignForChild:60`; `_sync` contains only `_assignForChild:4`. | R is assigned by init. The reserve is not a named synchronized property to publish. |
| `work._temp` | Gimmick box proto0 PCs `0-9`: `mapMarkerVisible:boolean`, assigned M. | Marker visibility is initialized locally. No corresponding named `_sync` field is declared here. |

The property route, **when a field's writer has been registered**, is s2c
`0x0137` through `0x00775A30 -> 0x00775180`, property-map lookup and handler
slot 1 at `0x00775652`. Information descriptors select the writer family.
`xivl-decomp:docs/net/sync-writer.md#registered-property-apply` owns that
native proof and scalar/string framing limits. Source declarations alone do
not observe the per-instance registry or prove a field-specific packet.

The seed-zero backward Murmur2 full-path candidates below were recomputed
with `xivl-client-structs:tools/verify_murmur2.py` after its six vectors passed.
They are derived identifiers, not observed keyed-coffer records:

| Full path | Derived hash |
| --- | --- |
| `npcWork.pushCommand` | `0x03CF5B58` |
| `npcWork.pushCommandSub` | `0x1B8741F6` |
| `npcWork.pushCommandPriority` | `0x40E25304` |
| `npcWork.hateType` | `0x8E9C05BE` |

## Conditions, event delivery and key question

The selected classes install no coffer-specific talk/notice/push condition
record. Registering the class or sending appearance alone is not evidence of
an enabled talk event. The native SetTalkEventConditionReceiver at
`0x0089DF60..0x0089DF94` casts ActorBase to NpcBase and passes its name and
two byte-field addresses (`+4/+0x58/+0x59`) to `0x006F29B0`. That helper
constructs a condition variant and inserts it at NPC `+0xE8`
(`0x006F29DF..0x006F2A80`). This proves a separate generic condition consumer,
not the correct condition name, selectors or complete packet for either box.

| Lua hook | Original locator and observation |
| --- | --- |
| Talk | `npcbaseclass.lua:406-458`, `root/proto21/22`, code `0xF81/0x1091`: active `_onTalkEvent` calls `_callServerOnTalk(A1,A2)` at PC `21`; `_onTalkRequest` calls `_doServerOnTalk(A1,A2)` at PC `3`. Lock-on and target cleanup surround the active event call. Neither body calls a key helper automatically. |
| Push | `:516-562`, `root/proto25/26`, code `0x1245/0x1298`: `_onPushEvent` calls `_callServerOnPush(A1,A2)` at PC `3`. Request names `pushCommandIn` / `pushCommandOut` select place-command set/reset branches; other names call `_doServerOnPush` at PC `26`. This is generic NPC behavior, not a required coffer push registration. |
| Notice / rejection | Selected roots have no `_onNoticeEvent` or `_onNoticeRequest` definition or notice-condition setter. `_onTalkRejected`, `_onNoticeRejected` and `_onReaction` are empty (`:602-623`, `root/proto29/31/32`, PC `0` RETURN). No key check or refusal message follows from those hooks. |

For a server-side operation described as `callClientFunction`, the callable
client target must resolve to the **coffer instance**, with function name
`askUseKey` for Public or `askKeyItemUse` for Gimmick. `worldMaster` is the
text owner passed by those functions, not their method receiver. The client
does not establish a server API with that spelling or its argument order.

The generic s2c `0x0130` function route can supply this invocation if its
guards, actor references and function lookup succeed. Application fields are
trigger key `+0`, owner key `+4`, event type `+8`, event name `+9`, function
name `+0x29`, and typed arguments at `+0x49` (copied span `0x40`). Native
executor `0x0089E260 -> 0x006E1140 -> 0x00896F70` selects binding B: either
the resolved trigger or a lookup of the owner, depending on the metadata
classifier. Function lookup then prepares `(function,B-as-Lua-self,args...)`.
`xivl-decomp:docs/script/delegate-command-producer.md#incoming-record-and-receiver`
and its function/binding section own these instructions and readiness limits.
Do not substitute a native pointer, assume B from actor-ID high bits, or
claim an unobserved coffer trigger/owner pairing.

| Requested Lua frame | Prompt and return |
| --- | --- |
| `coffer:askUseKey(A1,A2)` | `publictreasurebox.lua:22-37`, `root/proto1`, code `0x167`, CALL PC `8`, RETURN PC `9`: calls `askExtendWidget(worldMaster,60023,2,1,1,A1,A2)` and returns its one result unchanged. It does not convert that result to a boolean. |
| Inherited Public widget call | `npcbaseclass_event.lua:418-493`, `root/proto11`, code `0xDFA`: mode-1 branch VARARG PC `37` and open CALL PC `38` preserve **both** A1/A2 after `{60024,60025}` in `askForEventMode(self,self,worldMaster,1,false,true,60023,choices,A1,A2)`. RETURN PC `72` preserves one result. |
| `coffer:askKeyItemUse(A1)` | `gimmicktreasurebox.lua:43-71`, `root/proto2`, code `0x248`, CALL PC `14`, comparison PC `15`, return PCs `18/20`: calls `askForEventMode(nil,nil,worldMaster,1,false,true,60023,{60024,60025},A1,1)`. Returns true only for widget result equal to 1, false otherwise. |

A1/A2 are event-supplied formatting arguments on the Public path; Gimmick
supplies A1 and literal 1. Their forwarding is bound, but the selected chunks
do not validate a key ID/type/count or select a zone's key. The unchanged
Public result and Gimmick boolean are Lua return contracts, not an observed
server reply or proof of consumption. The original `worldMaster.csv` English
header `1`, rows 60023/60024/60025 at physical lines 2213/2214/2215, supplies
the question and Yes/No choices, as recorded in the linked coffer finding.

## CSV identity and remaining discriminators

Python ZIP/CSV inspection authenticated the archive pinned by
`xivl-client-data:manifests/private_csv_corpus.json` (70110686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`)
and the selected members against `xivl-client-data:manifests/tables.json`:

| Member | SHA-256 | Observation |
| --- | --- | --- |
| `actorclass.csv` | `3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984` | 7984 data rows. Neither leaf/base class name nor path occurs. Header 5 is the only populated typed data column; no class-path field is recovered here. |
| `actorclass_graphic.csv` | `7da8241400530885e0a28ded04a03acf2771b0580a79c1f49f46ee0861010611` | 7831 data rows. No selected class-name/path literal. Numeric appearance rows alone do not join to either Lua class. |
| `worldMaster.csv` | `2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643` | The three prompt/choice rows agree with the literal script selections. |

No actorclass or actorclass_graphic row is authenticated as PublicTreasureBox
or GimmickTreasureBox. `xivl-client-data:tools/mappings/actor_class.py`
explicitly supplies classPath/eventConditions placeholders. Row 1200161's
captured guildleve-bonus association is a different class; see the coffer
finding's [actor identity](open-world-key-coffer-contract.md#keys-and-actor-identity).

The missing discriminator is a retained keyed transaction joining actor key,
class/path, numeric C, appearance, initializer vector, enabled condition and
incoming named helper call to the reply and inventory/message outcome.
It must fix the trigger/owner pairing and actual A1/A2 meanings. A
field-specific writer/transaction is also needed to authenticate any proposed
sync publication beyond the generic declared route. Static initialization
does not settle placements, key consumption, rewards, refusal priority,
despawn, relocation or timers.

## Original Lua identity and reproduction

All eight original LPBs, decoded payloads and reproduced sources matched
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json) and
[`scripts.json`](../manifests/scripts.json) at commit
`91b13060e4fd3a016bde576833babf14775fae37`, extraction `2012.09.19.0001`.
[`retail_script.py`](../tools/retail_script.py) decoded wrappers. Pinned
`unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`,
produced source/disassembly; a Lua 5.1 operand reader checked raw PCs, arities,
open arguments and returns. Resource paths are relative to `client/script/`.

| Source basename | Original LPB / SHA-256 |
| --- | --- |
| `publictreasurebox` | `729s9/wu7/v8057q/qs59rps58vm/up8y17qs59rps58vm.le.lpb` / `72d44e70d3f8a781855ae0813d2e26210b03c80c4f2dfaa7cb471856ff6fbdd6` |
| `treasureboxbaseclass` | `729s9/wu7/v8057q/qs59rps58vm/qs59rps58vm89r57y9rr.le.lpb` / `02f8bf9534d70cf79605f5129c278a7614e15d2a108d080443ab84dc59d9bc83` |
| `gimmicktreasurebox` | `729s9/wu7/31xx17z/31xx17zqs59rps58vm.le.lpb` / `914edf17071592e7756dc35a0299c60ad6f543aae0d14e083d05836121a30c2f` |
| `gimmicknpcbaseclass` | `729s9/wu7/31xx17z/31xx17zwu789r57y9rr.le.lpb` / `d685e404923bf98b945ab2d6dbf92b66d358c45051ab5d37da4d159c00319f87` |
| `npcbaseclass` | `729s9/wu7/wu789r57y9rr.le.lpb` / `3f1dcc3416f7e22db138a6dcc730b095f81f3d0ceb458a7ded7d5b0d17df55c9` |
| `npcbaseclass_event` | `729s9/wu7/wu789r57y9rr_5o5wq.le.lpb` / `84a5098636ff289f4ecf4e164e84e44890895e8a9005fb102e04929c2bb74bf9` |
| `npcbaseclass_battle` | `729s9/wu7/wu789r57y9rr_89qqy5.le.lpb` / `feea4b9c4d4e2336dc3f4b4d6d1128212d78628df20249d7157a401693d57dc5` |
| `charabaseclass` | `729s9/729s989r57y9rr.le.lpb` / `c7cd1dad84f7d9b723f5a10fb66108da9d9d6ef5d7c15186b48ec55092465238` |
