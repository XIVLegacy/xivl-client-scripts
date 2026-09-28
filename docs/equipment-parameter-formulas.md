# Equipment parameter formulas

The retail Lua extraction contains client-side helpers that predict item
parameters, combine equipment bonuses, and format parameter rows. This page
promotes the arithmetic and operational spreadsheet-column roles recovered
from those helpers. It does not assign server formulas, validation, or
authoritative item state.

## Evidence identity

The findings were recovered from ignored canonical decompiler output. The
tracked artifacts below preserve the source identity without publishing the
Lua bodies.

| Decoded script | Ciphered script | Retail LPB SHA-256 | Canonical Lua SHA-256 |
|---|---|---|---|
| `item/itembaseclass_common` | `1q5x/1q5x89r57y9rr_7vxxvw.lua` | `50BD1025AD4AD14C12E51F96F9C73894D990F0C452CD756E0D815D684E5C91F0` | `7620492917230C3E060ED84D3197BF164C234A3AB73E48A0939BC65107F6B7FA` |
| `item/normal/normalitembaseclass_common` | `1q5x/wvsx9y/wvsx9y1q5x89r57y9rr_7vxxvw.lua` | `D44575E450E425D34517E31E56B7712A83E20D5DFA9062F05B53C05A970FB77E` | `35A05383355D7205F58AD999710E5EAF92331C899C683873B823AEAD755645F0` |

Both scripts belong to extraction `2012.09.19.0001`. Their decoded-to-ciphered
mappings and recovered method names are in `lua/registry.json`. Canonical Lua
hashes and line counts are in `manifests/scripts.json`. LPB paths, hashes, and
wrapper identities are in `manifests/retail_lua_coverage.json`.

## Item parameter level adjustment

The four item parameter families use repeating `itemDataSheet` column groups:

| Parameter | Grow selector | Base value | Compatibility adjustment |
|---:|---:|---:|---:|
| 1 | 49 | 50 | 51 |
| 2 | 52 | 53 | 54 |
| 3 | 55 | 56 | 57 |
| 4 | 58 | 59 | 60 |

`getItemParam1LevelAdjustGrow` through
`getItemParam4LevelAdjustGrow` read the grow-selector columns. A negative raw
selector becomes nil. A nonnegative selector is passed through the supplied
actor's `judgeGrowColumn` helper with the caller's third argument. The
extraction does not name the selector domain or the third argument.

`getItemLevelAdjust` uses item level `I` from column 47 and the supplied
actor's main skill level `S`. Its default level-distance limits are -1 for an
underleveled actor and 15 for an actor above the item level. Therefore the
default leaves `S` unchanged when `I > S`, and uses
`S' = I + min(15, S - I)` when `I < S`.

For base parameter `B`, grow selector `g`, and the actor's grow lookup `G`, the
intermediate target is:

```text
T = B * G(S', g) / G(I, g)
```

When `I > S`, the returned level-adjusted value is
`B - (B - T) * 1.0`. When `I < S`, it is
`B + (T - B) * 0.7`. Equal levels return `B`. A nil grow selector also returns
`B`. The helper does not round or clamp the result.

When an actor argument is supplied, each `getItemParamN` caller then multiplies
that result by a compatibility factor. If the corresponding
compatibility-adjustment column is zero, the factor is 1. Otherwise, for the
recovered compatibility value `C` and column value `A`, the factor is
`C - (1 - C) * A`. Without an actor argument the factor is 1 and level
adjustment is skipped. No rounding follows this multiplication in the
recovered path.

### Separate normal-item level factor

`NormalItemBaseClass.calculateLevelAdjust(skillLevel, itemLevel)` is a
separate factor table. It returns 1 when the item level is nil or is not above
the supplied skill level. Otherwise it caps the positive level gap at 7 and
returns:

| Item-level band | Gap 1 | Gap 2 | Gap 3 | Gap 4 | Gap 5 | Gap 6 | Gap 7 or more |
|---|---:|---:|---:|---:|---:|---:|---:|
| 31 or higher | 0.7 | 0.6 | 0.5 | 0.4 | 0.3 | 0.2 | 0.1 |
| 11 through 30 | 0.9 | 0.8 | 0.7 | 0.6 | 0.5 | 0.4 | 0.3 |
| 10 or lower | 0.9 | 0.85 | 0.8 | 0.75 | 0.7 | 0.6 | 0.5 |

Here the gap is `itemLevel - skillLevel`. The helper performs no rounding. Its
recovered consumer uses this factor in a
client-side item degradation-rate calculation; that use does not establish a
server equipment formula.

## Equipment parameter combination

The equipment helpers give these columns exact operational roles:

| Columns | Recovered role |
|---|---|
| 71 through 74 | Four scalar condition-parameter bonus values, returned in order. |
| 75, 76 | One base append-parameter ID and value pair. |
| 77, 78 | One quality-gated parameter ID and value pair. |
| 79 through 90 | Six append-parameter ID and value pairs. |

`processGetConditionParameterBonus` returns columns 71 through 74 directly.
The extraction does not identify their individual condition names.

`processGetEquipmentAppendParameter` emits the column 75/76 pair when its ID
is not -1. `processGetEquipmentParameterBonus` returns empty arrays unless the
catalog ID is in the recovered equipment range 3,900,000 through 9,999,999,
then starts with that result. When
`getMainQuality()` is greater than 1, it appends the column 77/78 pair. It then
visits the six ID/value pairs in columns 79 through 90. An ID of -1 skips that
pair. A repeated ID adds its value to the first existing value for that ID;
otherwise the pair is appended in sheet order. No rounding, sorting, or clamp
is applied. The column 77/78 pair is appended without a duplicate check, so
the helper does not guarantee that every repeated ID is coalesced.

`getEquipmentParameterBonus(parameterId)` searches the combined ID list and
returns the corresponding value for the first match. It returns 0 when the
item is not equipment or the ID is absent.

`getEquipmentParameterBonusAtSlot(slot)` uses the same combined list as a
one-based presentation list. A slot above the list length, or a selected value
of zero, returns `(-1, 0, 0)`. Otherwise it asks `desktopWidget` for the
parameter ID's two unit values and returns the first unit value, the combined
numeric value, and the second unit value. This is a client display contract,
not a server slot layout.

## Quality and HQ behavior

For a `NormalItemBaseClass`, `getMainQuality` returns the synchronized
eight-bit integer `normalItemWork.mainQuality` but normalizes zero to 1. For
another item class it returns -1.

For a normal item, `getSubQuality` returns the three stored
eight-bit integer `normalItemWork.subQuality` entries. When the first entry is
zero, it returns `(1, 1, 1)` instead. For another item class it returns
`(-1, -1, -1)`.

The helper named `getItemHQValue(baseValue, multiplier)` uses
`getNameIndex()` as its gate. When that index is below 2, it returns the base
value unchanged. The meaningful recovered arithmetic when the index is at
least 2 selects between:

```text
baseValue + 1
ceil(baseValue * multiplier)
```

The emitted decompile passes a transient third register to `max`, so the exact
runtime call arity is unresolved; the two values above are the recovered
meaningful candidates. The ceiling operation is the only rounding recovered
in the promoted helper set. Recovered callers use multiplier 1.03 for six
weapon craft or harvest values and shield defence or rate, and 1.05 for weapon
damage power and armor defence. Ordinary weapon attack, rate, magic attack,
and magic rate bypass this helper.

The extraction does not establish that name index 2 means HQ. The separate
quality gate used by equipment parameter combination tests whether normalized
main quality is greater than 1 and does not call `getItemHQValue`.

## Unresolved and authority boundary

The extraction proves numeric column positions and their use, but not public
spreadsheet field names for columns 49 through 60 or 71 through 90. It also
does not resolve the grow-selector domain or the contents of `getGrowData`.
It also does not resolve the four condition names for columns 71 through 74,
the parameter-ID namespace, or the unit meanings returned by `desktopWidget`.
It does not resolve the
semantic meaning of name index 2 or the decompiler's transient third `max`
argument in `getItemHQValue`. `getEquipmentParameterBonusAtSlot` checks only
the upper slot bound, so zero, negative, and non-integer inputs remain outside
the supported presentation contract.

These helpers support client display and prediction behavior only. No claim
here assigns the same arithmetic to a server, proves equipment eligibility or
HQ authenticity, types a network field, or establishes persistence.
