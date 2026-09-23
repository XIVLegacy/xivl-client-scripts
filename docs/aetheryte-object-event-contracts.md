# Aetheryte object event contracts

`AetheryteParent` and `AetheryteChild` implement separate restricted-choice
handlers. Their return values are client method results, not decoded action
names or proof of a server-side teleport.

## Parent selection

`eventAetheryteParentSelect` calls `askRestrictChoices` with text ID 117.
When its first argument is true, choice 2 can enter a second restricted-choice
menu using text ID 7. A zero second argument instead produces a `say` call
with text ID 34115 and returns nil. Otherwise text ID 145 is shown with that
argument, and the next five arguments provide the second menu's availability
flags: zero disables a slot, while any nonzero value enables it and is passed
through in order. A second-menu result of 6 returns nil; other results pass
through unchanged. When the first argument is not true, the second choice in
the text-117 menu is disabled.

For the text-117 menu, result 1 returns nil, result 3 returns -1, and result 5
returns -3. Result 4 shows text ID 328 and asks with text ID 329; it returns -2
only when that ask returns 1. Result 6 calls `showAetheryteTips` and has no
explicit return afterward.

## Child selection

`eventAetheryteChildSelect` calls `askRestrictChoices` with text ID 21. A
truthy first argument enables its choice-2 branch; otherwise that choice is
disabled. In the enabled branch, choice 2 shows text ID 31 with the fourth and
third arguments, then asks with text ID 32. It returns 2 only after answer 1
and unless the third argument is zero while the fourth is nonzero; that pair
instead shows text ID 34115 and returns nil. A declined confirmation returns
nil.

For the text-21 menu, result 1 returns nil, result 3 returns -1, and result 5
returns -3. Result 4 shows text ID 55 and asks with text ID 56; it returns -2
only when that ask returns 1. This method has no result-6 branch.

The text IDs and return codes do not reveal the menu labels, destination
identities, action meanings, or which server caller consumes each result.

## Evidence

The decoded `AetheryteParent` payload SHA-256 is
`4824C5921D56B262D47B40B82BC8366A795860B4DD9944ECDB41AC7FEE4E33E3`, pinned
to `lua/scripts/chara/npc/object/aetheryte/aetheryteparent.lua` in
`manifests/retail_lua_coverage.json:8247-8251`. The decoded `AetheryteChild`
payload SHA-256 is
`453A18028DBC5D1883954EA33EA1494DE1D83947212EE96DDDADA9DB8232D252`, pinned
to `lua/scripts/chara/npc/object/aetheryte/aetherytechild.lua` in
`manifests/retail_lua_coverage.json:8187-8191`.
