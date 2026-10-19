# The Heat Is On selector contract

`Spl0i1.processEventSUMFES001` passes seven item IDs to
`Ask/RewardSelectWidget` and consumes its second retained result. Original
bytecode establishes the caller's selector, confirmation, retry and return
paths. The [seasonal quest identities](seasonal-quest-client-contracts.md#retail-quest-identities)
join `Spl0i1` to The Heat Is On, quest ID `110799`.

## Inputs and source identity

The extraction is `2012.09.19.0001`. The LPB and payload pins are recorded in
[retail Lua coverage](../manifests/retail_lua_coverage.json). The canonical Lua
pin is recorded in [the script manifest](../manifests/scripts.json).

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `client/script/tp5rq/r75w9s1v/ruy/ruyj1i.le.lpb` | 10140 | `0e1a9f82c23094e4f5a42506f5ddff47acb7c742c4e4739a9d4d9f426863f34b` |
| Decoded `Spl0i1` payload | 10127 | `8fd5f3479823d8a0a143ddf2c26dd12db4a570dc732582cddfe0cb14e76ae08c` |
| Canonical `lua/scripts/quest/scenario/spl/spl0i1.lua` | 48738 | `7989e8680aa9d9010e40b9bcaad01c0168444784b9ea91b5c8727b7918143ccb` |

PCs below are zero-based, and byte offsets are decimal decoded-payload
offsets. The root assignment at PC `15`, byte `92`, binds `root/proto2` to
`Spl0i1.processEventSUMFES001`. The prototype has six fixed parameters, no
varargs and 1059 instructions starting at byte `2992`. The canonical function
is lines `529-1720`, with its assignment at line `1722`.

The independent decompile listed in the seasonal overview has SHA-256
`60fdeb1da8e58debeac792b7d471d5a2929aa02e3b8e24e3dae3cdcf454eeed3`.
That is a separate text artifact. The canonical source and original instruction
words identified above support this contract.

Parameter names here describe use: `R0` is a dialogue and widget argument,
`R1` is the initial talk-turn argument, and `R2` receives the talk, scheduler,
dialogue and ask methods. `R3` selects between two opening presentations by
equality with numeric `0`. `R4` selects numeric dialogue variants `0`, `1`
and `2`. `R5` is tested against numeric `1` in the outer menu's second branch.
These inputs do not identify cities, invoking actors or progression states.

## Selector arguments and presentation

The first call is `R2:startCliantTalkTurn(2, R1)` at PC `3`, byte `3004`.
After the opening presentation, the outer menu is
`R2:askExtendWidget(R0, 15, 4, 1, 1)` at PC `107`, byte `3420`.
Its numeric result `1` enters the selector loop.

The widget call at PC `125`, byte `3492`, is:

```text
desktopWidget:askEventModeWidgetYield(
  "Ask/RewardSelectWidget", 1, R0, 20, retained,
  3020604, 3020605, 3020606, 10012018, 10012019, 10012020, 10012021)
```

The seven item IDs are scalar arguments in this order. The method does not
construct a Lua item table. `retained` starts at `0` in PC `110`, byte `3432`.
`CALL B=14, C=3` retains two result slots in `R8-R9`. The method does not
consume the first result. PC `126`, byte `3496`, copies the raw second result
from `R9` to `R7` before normalization, preserving it for the next widget call.
This describes caller retention, not the producer's actual return arity.

The selector tests use `R9` at PCs `211`, `260`, `309`, `358`, `407`, `456`
and `505`, bytes `3836`, `4032`, `4228`, `4424`, `4620`, `4816` and `5012`.
For numeric variants `0`, `1` and `2`, a matching index supplies these trailing
`say` arguments:

| Second retained result | Item argument | Following substitution arguments |
| ---: | ---: | --- |
| 1 | 3020604 | `10012014, 1` |
| 2 | 3020605 | `10012016, 1` |
| 3 | 3020606 | `10012015, 1` |
| 4 | 10012018 | `10012014, 3` |
| 5 | 10012019 | `10012015, 3` |
| 6 | 10012020 | `10012016, 3` |
| 7 | 10012021 | `10012014, 10012015, 3, 3`; a second `say` supplies `10012016, 10012017, 3, 3` |

The first six entries use dialogue rows `23`, `58` or `85`, according to
`R4=0`, `1` or `2`. Entry seven uses row pairs `24/25`, `59/60` or `86/87`.
For example, PC `226`, byte `3896`, calls
`R2:say(R0, 23, 0, 3020604, 10012014, 1)`. Entry seven's variant-zero calls
are PCs `522/531`, bytes `5080/5116`.
These are displayed substitution values and counts, not server exchange recipes.

## Confirmation, retry and cancel

The selector confirmation is `R2:askExtendWidget(R0, 26, 2, 1, 1)` at
PC `592`, byte `5360`. The caller retains one result and compares it with
numeric `1` at PC `593`, byte `5364`, then numeric `-3` at PC `597`, byte `5380`.

| Condition | Caller behavior |
| --- | --- |
| Selector `i` in `1-7`, confirmation `1` | Adds `100` at PC `595`, byte `5372`, calls `finishCliantTalkTurn` at PC `680`, byte `5712`, and returns one value `i + 100` at PC `681`, byte `5716`. |
| Selector `-1` or `8` | Normalizes `-1` to `8` at PC `129`, byte `3508`, presents variant-specific dialogue and takes the shared finish-and-return path with value `8`. No confirmation call occurs. |
| Selector `-3` | Presents variant-specific dialogue, assigns `8` at PC `209`, byte `3828`, and takes the same finish-and-return path. No confirmation call occurs. |
| Confirmation `-3` | Presents variant-specific dialogue and assigns local `199` at PC `636`, byte `5536`. |
| Any other confirmation result unequal to numeric `1` | Presents variant-specific dialogue and assigns local `199` at PC `675`, byte `5692`. |
| Local result `199` | PC `676`, byte `5696`, sends control through PC `678`, byte `5704`, back to PC `111`, byte `3436`. The next widget call receives the preceding raw second result as `retained`. No finish call occurs before the retry. |

Results outside the named selector comparisons still reach confirmation.
The method does not establish a native result domain restricted to `1-7`
and the cancel values. Numeric results on that path undergo the same addition.
For example, raw `99` with confirmation `1` becomes local `199` and retries,
passing raw `99` to the next widget call.

## Other outer-menu paths

| Outer menu result | Caller behavior |
| --- | --- |
| `2` | Presents variant-specific rows `21/22`, `56/57` or `83/84`, including substitution arguments `10012014, 10012015, 10012016, 1`, then asks `R2:askExtendWidget(R0, 26, 2, 1, 1)` at PC `766`, byte `6056`. |
| `3` | Presents variant-specific dialogue and repeats the outer menu. |
| `4` | Calls finish at PC `1046`, byte `7176`, and returns one value `4` at PC `1047`, byte `7180`. |
| `-3` | Assigns `4` at PC `1051`, byte `7196`, calls finish at PC `1053`, byte `7204`, and returns one value `4` at PC `1054`, byte `7208`. |
| Any other result | Repeats the outer menu. |

In the outer menu's `2` branch, confirmation unequal to numeric `1` sets
local `199` and repeats the outer menu without finishing. If confirmation
equals `1` and caller `R5` equals numeric `1`, the method assigns `199`,
finishes at PC `810`, byte `6232`, and returns one value `199` at PC `811`,
byte `6236`. Here `199` is returned directly rather than tested as a retry.

Otherwise, the caller asks `R2:askExtendWidget(R0, 36, 4, 1, 1)` at PC `818`,
byte `6264`. Numeric choices `1`, `2` and `3` add `110`, then finish at
PC `914`, byte `6648`, and return one value `111`, `112` or `113` at
PC `915`, byte `6652`. Other results, including `-3`, set local `199` and
repeat the outer menu without finishing. All comparisons with the named
numbers are equality tests, not truthiness tests.

## Static verification and limits

Only the one pinned `Spl0i1` LPB was selected. It parsed completely to EOF.
The offline model used the original instruction words with opaque synthetic
callee results. It checked 312 cases covering selector indices, both opening
paths, the numeric dialogue variants and an unmatched variant, all prompt
branches, retries, cancel normalization, retained argument order and returns.
Eight synthetic instruction cases checked equality polarity and types, jump
targets and fixed result retention. Eleven semantic mutation guards changed
selector slots, item arguments, normalization, addition, retry, confirmation
or return operands and were rejected.

The cases exercised 977 of 981 syntactically reachable instructions, 1059 of
1063 syntactic control-flow edges and all 144 feasible callsites. The four
remaining instructions are PCs `997`, `999`, `1000` and `1001`. All feasible
predecessors of PC `996` carry `R6=199`: PC `912` requires that equality,
PC `957` follows the assignment at PC `956`, and PC `995` loads `199`
directly. Consequently PC `996` skips PC `997`; its finish and return at
PCs `1000/1001` cannot be reached. The final compiler epilogue at
PCs `1056-1058`, including its zero-value return, is also unreachable.
This is a static control-flow result, not observed retail execution.

The decoder was `tools/retail_script.py` SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`.
The parser and instruction/control-flow decoder were
`tools/build_quest_contracts.py` SHA-256
`db67cab44bb6a4b6b54ffa5dd333fd78e85f9b77cb8ac7067dd31c1aab6b16e2`.

The caller's second retained widget result and the widget's
[base result contract](reward-widget-result-contracts.md) are separate evidence
points. This selected chunk does not establish forwarding, actual native
producer arity, runtime result domain, inventory validation, consumption,
grants, eligibility, completion, historical dispatch, invoking NPC, city or
calendar availability. The other methods and native bindings remain outside
this finding.
