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
`DesktopWidget.processCharacterParameterUpdated`. For the local player, that
dispatcher has an explicit but empty `battleParameter` branch. The recovered
property-change route therefore stops there and does not prove an immediate
Status or Equipment widget redraw for element 18.

Both widgets read the value during initialization and their broader refresh
paths. `EquipWidget.update` refreshes all three parameter groups whenever that
method is called. `StatusWidget.update` would refresh the group if called with
`battleParameter`, but no recovered property dispatcher makes that call. The
empty desktop branch is the first unresolved callback boundary; it does not
make the direct display consumer ambiguous.

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
control.

## Capture and implementation consequence

The independent capture census observed 141 -> 161 during one closed helm
transition and after-only values 147 and 169 for body and weapon observations.
The consumer chain establishes that those values feed the client's `Defense`
display; their magnitudes were not used to identify the field. The samples do
not establish how the total is calculated or whether every equipment change
must alter it.

For Bahamut, property hash `0x8cae90db` can be treated as the client-facing
aggregate Defense value at `generalParameter[18]`. Supplying the authoritative
value there makes it available when the Status and Equipment widgets next read
their parameter groups.
This evidence does not prove that the property update alone
forces an immediate redraw, and it does not justify deriving the value from the
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
