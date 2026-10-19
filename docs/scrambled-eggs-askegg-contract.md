# Scrambled Eggs askEgg result tuple

`Spl101.askEgg` retains twelve result slots from one
`Ask/EventItemSelectWidget` call and returns eight values. It tests its first
two retained values against literal `true`, derives an item argument from
four numeric comparisons, preserves five later values, and derives two flags.
This is local tuple construction, not a native result-domain or reward rule.

## Sources and locators

The [loading and start contract](scrambled-eggs-start-contract.md#sources-and-reproduction)
owns the exact original `ruyiji.le.lpb`, decoded payload, canonical
`spl101.lua` member and decoder identities. Only that one main LPB and
canonical member were selected here; the supplemental chunk was not read.
Its bytecode parsed completely through byte 883. The canonical `askEgg`
body is lines 19-68, with its assignment at line 70.

Root PC 8, decoded-payload byte 64, installs `root/proto1` as `askEgg`.
The prototype has one fixed parameter, no varargs and 86 instructions
starting at byte 300. PCs below are zero-based and byte offsets are decimal
decoded-payload offsets. Call the sole incoming parameter `p0`; its invoking
object and caller are unproved. The existing
[quest identity](seasonal-quest-client-contracts.md#retail-quest-identities)
joins `Spl101` to Scrambled Eggs, quest 110859.

## Widget arguments and caller retention

PC 16, byte 364, calls:

```text
desktopWidget:askEventModeWidgetYield(
  "Ask/EventItemSelectWidget", 11, p0, 201,
  10012001, 10012002, 10012003, 10012004, 10012022,
  10012024, 10012025, 10012026, 10012027, 10012028)
```

The ten item IDs are scalar arguments in this order. `CALL A=1, B=16,
C=13` passes fifteen Lua arguments including the widget receiver and retains
twelve slots in `R1-R12`. Call those slots `w1-w12`. Fixed-result adjustment
supplies nil for missing results and discards any extras; it does not establish
the producer's actual arity or the meanings of these slots.

PC 17, byte 368, initializes local `R13-R14` to nil. PCs 18/20, bytes
372/380, compare `w1/w2` with literal `true`. These are equality tests:
numeric `1` does not pass either gate.

## Local derivation and eight-value return

If both gates pass, `R13` is selected by exact numeric comparisons:

| `(w3,w4,w5,w6)` | Local `R13` | Assignment PC / byte |
| --- | ---: | --- |
| `(1,0,0,0)` | 10012001 | 30 / 420 |
| `(0,1,0,0)` | 10012002 | 40 / 460 |
| `(0,0,1,0)` | 10012003 | 50 / 500 |
| `(0,0,0,1)` | 10012004 | 60 / 540 |
| `(0,0,0,0)` | 0 | 70 / 580 |
| Other patterns | nil | No matching assignment |

Under the same gates, PC 71, byte 584, compares `w7` with numeric `1`.
Equality assigns literal `true` to `R14` at PC 73, byte 592; other values
leave it nil. If either initial gate fails, PC 75, byte 600, sets local
`R2` to false, while `R13/R14` remain nil. If both pass, `R2` remains true.

PCs 76-83 copy the result tuple. `RETURN A=15, B=9` at PC 84, byte 636,
returns exactly:

```text
(R13, w8, w9, w10, w11, w12, R14, R2)
```

Thus zero and nil remain distinct in the first position, and the seventh
position is true or nil rather than true or false. The five passthrough
values remain in their original order even when an initial gate fails.
The zero-value compiler epilogue at PC 85, byte 640, is unreachable after
the preceding unconditional return. There is one widget call, no local retry
and no talk-finish call in this method.

## Verification and boundary

Static Python interpretation of the original words checked 2951 opaque-result
cases, including all numeric 0/1/2 patterns, exact boolean gates, short and
extra result lists, and type distinctions. The cases exercised all 85
reachable instructions and all 107 syntactic reachable edges. Seven semantic
mutations of gate polarity, zero mapping, flags, passthrough slot, return
width and retained width were rejected. The check ran without a Lua VM.

The [loading contract](scrambled-eggs-start-contract.md) separately owns the
main/supplement relationship and selected G1Start prompt result. This method's
item arguments, numeric comparisons and return tuple do not identify native
slot meanings, cancel sentinels, inventory validation, item consumption, a
ring or other grant, eligibility, progression, invoking NPC, city, historical
availability or a server settlement rule. Widget forwarding and native result
arity/domain remain separate from this caller's fixed retention.
