# ActionMenu grid visibility

`ActionMenuWidget` addresses two distinct named controls:
`Grid_ActionCommands` and `Grid_UserMacro`. The decoded script establishes
their names and presentation switching. It does not establish live native
control pointers, mouse hit testing, or a callable native visibility adapter.

## Source identity

The source is the canonical decoded Lua extraction `2012.09.19.0001`.
The reproduction entries in [scripts.json](../manifests/scripts.json) pin:

| Decoded path under `lua/scripts/` | Bytes | SHA-256 |
|---|---|---|
| `widget/actionmenuwidget.lua` | 61888 | `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea` |
| `widget/widgetbaseclass_common.lua` | 69077 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |
| `widget/actiongaugewidget.lua` | 4058 | `4269a53c9be52759d49289364fdbdd16e7fef350c5866bdca5c5aae5eba746aff` |

These entries were inspected at repository revision
`ab479da8428991262ed2879a428c02ebd4277678`. The restricted corpus was hydrated
with `tools/private_lua_corpus.py hydrate` and verified against the reproduction
manifest. [The corpus contract](../lua/README.md) defines canonical byte
normalization and the boundary between tracked metadata and local script
bodies. The observations below promote facts from those identified bodies,
without reproducing their code.

## Presentation switching

`actionmenuwidget.lua:1638-1663`, `showUserMacroBar`, checks macro-grid
visibility. On its show branch it focuses a macro button, makes
`Grid_UserMacro` Visible, and sets `Grid_ActionCommands` Hidden. If already
visible, it changes keyboard focus instead.

`actionmenuwidget.lua:1666-1691`, `hideUserMacroBar`, returns immediately when
`work.userMacroType` is zero. Otherwise it records the selected macro index,
sets that work value to zero, makes `Grid_ActionCommands` Visible, and sets
`Grid_UserMacro` Hidden. These methods change selection/focus and switch the
two grids. They are not two independent visibility setters or preference
snapshots.

`ActionGaugeWidget` has its own decoded script and reproduction entry. The
two control names above belong to the ActionMenu script. Neither name
authorizes hiding ActionGaugeWidget or the enclosing HUD.

## Preserve three states

The shared wrapper behavior in `widgetbaseclass_common.lua:1658-1748` is:

| Method | Property operation |
|---|---|
| `setVisibility(control, true)` | `Visibility = "Visible"` |
| `setVisibility(control, false)` | `Visibility = "Collapsed"` |
| `setHidden(control)` | `Visibility = "Hidden"` |
| `getVisibility(control)` | True only when the property string is `"Visible"` |

`setItemVisibility` and `setItemHidden` reach `_setProperty` with the exact
property name `Visibility`. `getItemVisibility` reaches `_getProperty`, then
reduces its string to the boolean above. Hidden and Collapsed therefore
cannot be distinguished by `getVisibility`. A reversible native override
needs the complete property state, rather than this boolean.

## Native boundary

The script establishes named lookup intent, not a stable native handle.
Resolving the controls requires proving the live ActionMenu instance,
its control tree and name scope, the getter/setter receiver and ABI,
and ownership on the native UI thread. The control lifetime must include
widget teardown, template replacement, and UI rebuild invalidation.

The script's visibility assignments do not prove that either hidden grid's
mouse regions disappear, that native action execution remains available,
or that changing a property avoids saved HUD configuration writes. Native
code can also change visibility during replacement ownership. Restoration
requires observing and reconciling that current native preference, not
blindly replaying an initial value. Those are native and runtime proof
requirements beyond this script-derived contract.
