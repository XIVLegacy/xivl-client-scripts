# General parameter 18 consumers

The retail Lua corpus gives `charaWork.battleTemp.generalParameter[18]` a
stable client presentation meaning. Native index 18 is Lua table slot 19.
`CharaBaseClass.getNormalDefence` reads that slot directly, and the Status and
Equipment widgets display its value as the English parameter `Defense`.

This is a client consumer identity, not a server formula or a native field
name. The spelling `getNormalDefence`, the control name
`Label_PhysicsDefense`, and the localized English title `Defense` remain
separate evidence rather than being normalized into a stronger gameplay noun.

## Exact consumer chain

`CharaBaseClass.initBattleSync` declares `battleTemp.generalParameter` as an
array of 35 `integer16` values. Its `battleParameter` update group includes
native element 18. The direct accessor in
`chara/charabaseclass_ffxivbattle` reads:

```text
native generalParameter[18] -> Lua generalParameter[19]
  -> CharaBaseClass.getNormalDefence
  -> StatusWidget.updateBattleParameter or EquipWidget.updateBattleParameter
  -> setDefence
  -> Label_PhysicsDefense.TextBlock_BaseParameter
```

Both widget setters convert the value with `tostring` and write it without a
unit lookup, formula, comparison, rounding, or clamp. Both initialize the row
title from `xtx_text_paramName` row 15019, whose English value is `Defense`.
It associates help row 70019 from `xtx__text_ui`, whose English text describes
the character's combined defense rating and damage from physical attacks.

The two widgets obtain the player through `WorldMaster._getMyPlayer`.
`lua/napi_index.json` assigns that N-API to the `WorldMaster` declaration in
`world/worldmaster_u`. `getNormalDefence` itself is Lua logic owned by the
`CharaBaseClass` declaration in `lua/registry.json`; it is not an N-API.

## Update path

`ActorBaseClass._bindWork_inl` selects the Lua `_bindWork_lua` implementation.
The `battleParameter` descriptor groups element 18 with the other displayed
battle values. `CharaBaseClass._onUpdateWork` forwards work changes to
`DesktopWidget.processCharacterParameterUpdated`. For the local player, either
`battleParameter` or `gameParameter` reaches the same refresh block. It looks
up the existing Status and Equipment widgets with `getWidget(3, name)` and
calls each nonnil widget's `update(group)`. It does not open an absent widget.
`EquipWidget.update` refreshes all three parameter groups; Status receives the
actual group. Both widgets also read the value during initialization.

This shared branch was established from the original Lua 5.1 instructions,
rather than the decompiler's malformed empty-branch rendering. In
`desktopwidget_connector` `root/proto78`, code offset `0xF20B`, zero-based
PCs 339-343 join either group at PC 344; an unrelated group leaves at PC 366.
Status is updated at PC 352. The Equipment lookup is at PCs 353-356 and its
conditional update at PC 361. Local-player guards precede the dispatch at
PCs 108-115. The canonical source locator is
`widget/desktopwidget_connector.lua:4841-5340`; its text alone cannot resolve
these branches.

The original resource is
`client/script/n1635q/65rzqvun1635q_7vww57qvs.le.lpb`, 213487 bytes,
SHA-256 `0F8CA1585BB97C40D36CBF120DD3F6FA6351927C4530E3FAD76A71582AF95425`.
Its decoded payload is 213474 bytes, SHA-256
`685A0A6DDA2D4AE6FE06A9C684E57EFD7E819938E145CB1A4A65DF56555BD621`;
the canonical Lua SHA-256 is
`9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01`.
The [coverage manifest](../manifests/retail_lua_coverage.json) pins that resource
and payload, and the [script manifest](../manifests/scripts.json) pins the Lua.
Static instruction replay distinguished both matching groups from an unrelated
group and rejected an inverted first comparison. This proves conditional
callback dispatch, without establishing native callback arrival or rendered
timing from a packet alone.

## Exhaustive bounds and rejected paths

The 2,671 scripts contain 46 recovered lexical `generalParameter` references,
all in the array declaration, sync descriptors, and accessors in the two
CharaBaseClass battle scripts. `getNormalDefence` has exactly three recovered
lexical references: its definition and the two widget calls above. This census
does not claim to recover a dynamically constructed key or an alias that loses
the token before the call; the direct getter and fixed generic callers are the
last identities preserved in the retail Lua text.

The generic `getPhysicalParameter(n)` accessor reads Lua slot `n + 3`, so an
argument of 16 could also reach slot 19. The corpus has 36 calls, all with
fixed arguments from 1 through 12. No recovered call reaches element 18 by
that generic path. The registry and N-API index expose no second receiver or
native accessor for this field.

The item helpers `getArmorDefence`, `getShieldDefence`, equipment append
parameter IDs, parameter-name/unit lookup, and item comparison presentation
do not read actor `generalParameter`. Their use of parameter title 15019 or
defense vocabulary does not join their item formulas to this actor slot. No
corpus consumer supplies an actor-field unit, a construction formula, a
comparison delta, or a server authority rule.

`python tools/general_parameter_18_consumers.py` re-enumerates the
complete corpus and rejects drift in the array descriptor, direct accessor,
generic accessor domain, update group, widget consumers, title row, and display
control. Its connector text check pins the canonical extraction spelling; it
does not validate the original shared-branch semantics above.

## Capture and implementation consequence

The independent capture census observed 141 -> 161 during one closed helm
transition and after-only values 147 and 169 for body and weapon observations.
The consumer chain establishes that those values feed the client's `Defense`
display; their magnitudes were not used to identify the field. The samples do
not establish how the total is calculated or whether every equipment change
must alter it.

A server implementation can treat property hash `0x8cae90db` as the
client-facing aggregate Defense value at `generalParameter[18]`. Supplying the authoritative
value there makes it available when the Status and Equipment widgets next read
their parameter groups.
Delivery of the local actor's `battleParameter` callback reaches the open
widgets through the proved branch. Receipt of raw property bytes alone does
not establish delivery of that callback or immediate rendering. This evidence
does not justify deriving the value from the
recovered item formulas, adding equipment bonuses locally, or treating the
observed transition as a universal update formula.

Evidence: `lua/scripts/actorbaseclass_u.lua`,
`lua/scripts/chara/charabaseclass.lua`,
`lua/scripts/chara/charabaseclass_battle.lua`,
`lua/scripts/chara/charabaseclass_ffxivbattle.lua`,
`lua/scripts/widget/desktopwidget_connector.lua`,
`lua/scripts/widget/equipwidget.lua`, `lua/scripts/widget/statuswidget.lua`,
`lua/registry.json`, `lua/napi_index.json`,
`xivl-client-data:csv/xtx_text_paramName.csv`,
`xivl-client-data:csv/xtx__text_ui.csv`, and
`xivl-client-structs:manifests/property_stream_hash_catalog.json` for the
native-to-Lua index convention,
`xivl-client-structs:manifests/gam_hash_names.json` for the exact GAM hash,
`xivl-captures:studies/equipment-property-correlation/derived/evidence-map.md`.
