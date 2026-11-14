# Desktop main stat handler and target release

`CharaBaseClass._onChangeActorMainStat` forwards every main stat change of a
character to `DesktopWidget.processCharacterActorMainStatUpdated`. For the
current target character that is not a player and is dead, the handler
clears the lock-on and the cursor target. This page records those script
branches. Which actors the client raises the callback for, and the meaning
of each main stat value, are outside it.

## Source identity

The inputs are two installed resources of client extraction
`2012.09.19.0001`, authenticated against the
[coverage manifest](../manifests/retail_lua_coverage.json).

| Decoded path under `lua/scripts/` | Installed resource under `client/script/` | Wrapper bytes | Decoded bytes / SHA-256 |
| --- | --- | ---: | --- |
| `chara/charabaseclass.lua` | `729s9/729s989r57y9rr.le.lpb` | 13821 | 13808 / `101cafa86ebcb362b502e47dd33e262ede31b4939cc7fe945ab571e1afd0d3a9` |
| `widget/desktopwidget_connector.lua` | `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | 213474 / `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |

`tools/retail_script.py` decoded each LPB. `ChunkReader` and `instruction`
from `tools/build_quest_contracts.py` read the prototypes. Prototype IDs and
PCs are zero-based, and operand counts include the receiver.

| Method | Prototype / code start / PCs |
| --- | --- |
| `CharaBaseClass._onChangeActorMainStat` | `root/proto32` / `0x2A70` / 26, three operands |
| `DesktopWidget.processCharacterActorMainStatUpdated` | `root/proto81` / `0x101D8` / 121, four operands |

## Forwarding

`_onChangeActorMainStat(self, A1, A2)` skips an unreachable `RETURN` at PCs
0-1 and asks the player's depiction judge to judge the nameplate of `self`
(PCs 2-9). For the player itself, when `A1` or `A2` equals 15, it calls
`desktopWidget:processUpdateChocoboStatus()` (PCs 10-18). It then always calls
`desktopWidget:processCharacterActorMainStatUpdated(self, A1, A2)` (PCs 19-24).

## Handler branches

The handler's operands after the receiver are the actor `A1` and the two
values `A2` and `A3`. It returns for a nil actor (PCs 4-6). PCs 7-15 read the
player, `getCurrentTargetCharacter()` as T, the player's `_getLockonTarget()`
as L and `_getCurrentTargetCursor()` as K.

For the player itself (PCs 20-76):

- when dead, it clears the lock-on with `_setLockonTarget(nil)`, calls
  `cancelSubTargetSelect()`, `setTargetCharacter(1, nil)` and
  `updateActionMenuWidget(false, false)`, stops the cast gauge of static child
  `ActionGaugeWidget` of widget 7, and outside an instance raid notifies
  worldMaster 25005 (PCs 24-58)
- otherwise, when `A2` equals 2 it calls `requestAutoLockonTarget()`, then
  `updateActionMenuWidget(false)` (PCs 59-65)
- in both cases it updates `EmoteListWidget` of widget 15 when present and
  calls `updateMainMenuWidget()` (PCs 66-75)

For another player that is T, it calls `updateActionMenuWidget(false)` (PCs
77-81).

For an actor that is not a player and is T (PCs 83-119):

- when T is dead and L is nil or equals the actor, it clears the lock-on when
  L is not nil, calls `setTargetCharacter(K, nil)`,
  `updateActionMenuWidget(false, false)` and `playSoundTargetCanceled()`
  (PCs 89-107)
- when T is dead and L is another actor, it calls `setTargetCharacter(K, L)`
  and `updateActionMenuWidget(false)` (PCs 109-115)
- when T is alive, it calls `updateActionMenuWidget(false)` (PCs 117-119)

An actor that is neither a player nor T changes nothing here.

## Reproduction

Decode each resource with `tools/retail_script.py`, read the root prototype
with `ChunkReader`, map each `CLOSURE` to the constant key of the `SETTABLE`
that stores it, and list the selected child prototype's instructions with
`instruction`.
