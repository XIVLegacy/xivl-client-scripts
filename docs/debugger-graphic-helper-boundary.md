# Debugger graphic-helper boundary

The shipped CharaBaseClass definitions of `_initGraphicNumber`,
`_setGraphicNumber`, `_setWeaponGraphic` and `_setArmorGraphic` are empty Lua
functions. The DEV and GM debuggers retrieve similarly named properties from
their current receiver and supply conversion results or literal presets. Those
calls do not identify an item catalog, construct a packed appearance record,
or establish the implementation selected on that receiver.

## Definitions and dynamic calls

In `lua/scripts/chara/charabaseclass_u.lua`, the definitions are:

| Property | Function lines | Formal parameters, including receiver |
|---|---|---:|
| `_initGraphicNumber` | 185-186 | 42 |
| `_setGraphicNumber` | 191-192 | 42 |
| `_setWeaponGraphic` | 197-198 | 3 |
| `_setArmorGraphic` | 203-204 | 3 |

Each body has no statements or explicit return. The nominal class definition
therefore supplies no field mutation or native call. A property replacement
or override requires its own source and receiver binding.

`CommandDebuggerDEV.executeSetCommand` dynamically retrieves these properties
from its supplied receiver argument:

| Actual call line | Property | Explicit values after the receiver |
|---:|---|---|
| 4502 | `_setWeaponGraphic` | `tonumber` results for slot suffix and first vararg |
| 4552 | `_setArmorGraphic` | `tonumber` results for slot suffix and first vararg |
| 4581 | `_setArmorGraphic` | Loop slot 0 through 5 inclusive and `tonumber` result for first vararg |

The selected branches perform no item-sheet lookup or component packing.
The converted value has no established catalogID or modelID namespace.
The actual receiver's class, current property implementation and effects remain
separate from the nominal CharaBaseClass declarations.

In `CommandDebuggerGM.command`, the selected parsed-mode command discriminator
is 20036. The second vararg selects a preset from 1 through 7. Each branch
retrieves `_setGraphicNumber` from its current receiver and calls it with that
receiver followed by 41 literal positional values. Actual call lines are
3311, 3359, 3407, 3455, 3503, 3551 and 3599. The source establishes literal
presets and arity, without component names or a conversion from item rows.

These dynamic calls do not make the helper names native APIs. The
[corpus index contract](../lua/README.md#canonical-form) also distinguishes
script-defined underscore helpers from the N-API whitelist. A reference count
alone does not establish an invocation, binding or implementation.

## Source identity and verification

Source: retail extraction `2012.09.19.0001`. The
[reproduction manifest](../manifests/scripts.json) pins these canonical Lua
members:

| Member under `lua/scripts/` | Bytes | SHA-256 |
|---|---:|---|
| `chara/charabaseclass_u.lua` | 16586 | `a60649dce0b051d781a0a041d738e1bc24e94987bfb8d7c682aa330439ff77c1` |
| `commanddebugger/commanddebuggerdev.lua` | 623458 | `9ce79f78f841c964222ec7a72f1a557406d1efa1ad75bc03685a55af8b5ba34a` |
| `commanddebugger/commanddebuggergm.lua` | 281241 | `cdbbf9929a1353399e372dde705d38c577f491587d64b577beb8d43a1aaa0301` |

Read-only Python source checks authenticated the canonical LF bytes, the four
empty definitions, dynamic property receivers, numeric conversions, loop bounds
and preset call arities. Literal tuples were checked by digest in memory.
Source hashes remained unchanged. No client execution, native target or
appearance-record mapping was established by this source check.
