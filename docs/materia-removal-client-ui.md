# Materia removal client UI

`PopulaceShopMateriaRemover` builds a removal selection from player package 1.
`MateriaRemoveWidget` includes an occupied package-1 slot only when
`getMateriaBindPermission(slot)` is truthy and its attached-materia count is
positive. The selected result carries that item from package 1 back to the NPC
script. The Lua does not establish what the native bind-permission predicate
means.

The NPC opens `MateriaDialogWidget` in mode 2. The dialog presents the supplied
price and hides its accept control when the player lacks enough money; the NPC
script treats result 1 as the accepted confirmation branch. These calls
establish the selection and confirmation UI only. They do not establish the
price formula, a gil debit, a materia-removal mutation, an outgoing command, or
the authoritative result.

On accepted result 1, the NPC script hides `MateriaRemoveWidget`, runs
character scheduler `70275093`, waits for that same scheduler to finish, then
returns true from the handler. The scheduler's effect is not established by
this call path.

Evidence:

- `lua/scripts/chara/npc/populace/shop/populaceshopmateriaremover.lua:220-277,328-362`
- `lua/scripts/widget/ask/materiaremovewidget.lua:2044-2070`
- `lua/scripts/widget/ask/materiadialogwidget.lua:152-176,211-234,399-519`

The canonical source bytes are pinned in `manifests/scripts.json`; the
corresponding LPB paths, sizes, SHA-256 values, decoded payload
hashes, and `matched-script` classifications are in
`manifests/retail_lua_coverage.json`.
