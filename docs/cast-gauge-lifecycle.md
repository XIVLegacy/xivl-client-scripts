# Cast gauge lifecycle

`ActionMenuWidget.updateCastInfo` calls `ActionGaugeWidget.deleteCastGauge`
when the local player's `getCastCommand()` returns zero. `deleteCastGauge`
calls `hideWidget`, which hides the widget and disables visibility of its
command icon and text controls. This is a conditional script behavior when
`updateCastInfo` executes.

## Source identity

The source is the canonical decoded Lua extraction `2012.09.19.0001`.
[The reproduction manifest](../manifests/scripts.json) pins these bodies:

| Decoded path under `lua/scripts/` | Bytes | SHA-256 |
| --- | --- | --- |
| `widget/actionmenuwidget.lua` | 61888 | `81aafee07ca7f70ff31ee909f3883c9893dd6df941abd79c86f42c79bb1949ea` |
| `widget/actiongaugewidget.lua` | 4058 | `4269a53c9be52759d49289364fdbd16e7fef350c5866bdca5c5aae5eba746aff` |

The manifest entries were inspected at revision
`6c3b02b06fa9ba529469a798ade0ced4684ef467`. The identified bodies were
authenticated against those entries before direct inspection.
[The corpus contract](../lua/README.md) defines byte normalization and the
boundary between tracked metadata and restricted script bodies.

## Command and visibility branches

`actionmenuwidget.lua:739-761`, in `updateCastInfo`, reads `getCastCommand`.
A nonzero value is used to find a command slot and custom command. If both
lookups succeed, the gauge receives `startCastGauge`. The zero branch calls
`deleteCastGauge` directly.

`actiongaugewidget.lua:81-89`, `deleteCastGauge`, calls `hideWidget`.
`actiongaugewidget.lua:187-203`, `hideWidget`, calls `hide` and sets visibility
of `IconControl_MainCommand` and `TextBlock_MainCommand` to false. The method
name does not establish deletion of a native object.

## Timing boundary

The script branch does not establish when native work changes invoke
`updateCastInfo`, when queued result records are consumed, or which display
frame applies the visibility change. A received command-zero record alone
cannot prove those execution times or their order relative to result display.

The deadline calculation and command-zero visibility branch are distinct.
Neither the visibility branch nor the existence of `stopCastGauge` proves
that a deadline-zero write is required. These bodies do not establish a
producer's rounding rule, effective Chant state, or a cast-completion packet
sequence.
