# PlayerParameter TP consumer contract

For normal completion of the selected installed functions,
PlayerParameterWidget.updateTp selects row 3. Its consumer obtains the maximum
before the current value. The maximum getter returns numeric 0 when
hasGameParameter returns nil or false and numeric 3000 otherwise. The current
getter returns numeric 0 under the same branch condition and otherwise reads
charaWork.parameterTemp.tp directly. The desktop functions resolve the local
player separately and return these as their third tuple slots.

The consumer passes those operands unchanged to the TP property calls. The
primary and action-cost Maximum calls precede the primary Value call. This is
a static operand contract. It establishes no applied property, caption result
or general server TP cap.

## Source and method

The evidence is static extraction of selected installed client Lua resources
for supplied build 2012.09.19.0001. The resources and decoded chunks below are
identified independently of the generated script metadata. Their contents are
not distributed here.

The producing instruments are static LPB extraction with xivl extract-lpb and
independent Lua 5.1 parsing of the complete decoded chunks. The extractor
executable is 7360608 bytes with SHA-256
0a1480dddcee0d87343a000dadddb6815d48f2373392c2dc56396fc788ea86bd.
The method does not execute retail Lua or client code.

Each selected original LPB has the rle 0C wrapper. Decoding XOR 0x73 from
zero-based resource byte 13 yields its complete Lua 5.1 chunk. The method
checks the original size and hash, the decoded size and hash, the supported
Lua 5.1 header, and complete prototype and debug-table accounting through the
chunk's end. The four static extractor outputs agree byte-for-byte with
independent decoding of the original resources. See
[xivl-tools:docs/formats/lua-lpb.md](https://github.com/XIVLegacy/xivl-tools/blob/main/docs/formats/lua-lpb.md)
for the wrapper and bounded Lua 5.1 format contract.

### Resource identities

Resource paths are relative to client/script/. Logical names are the decoded
script identifiers. All hashes in this page are SHA-256.

| Id | Logical name | Original relative resource path |
|---|---|---|
| W | widget/playerparameterwidget | n1635q/uy9l5su9s9x5q5sn1635q.le.lpb |
| D | widget/desktopwidget_connector | n1635q/65rzqvun1635q_7vww57qvs.le.lpb |
| P | chara/charabaseclass_parameter | 729s9/729s989r57y9rr_u9s9x5q5s.le.lpb |
| C | chara/charabaseclass_cliprog | 729s9/729s989r57y9rr_7y1usv3.le.lpb |

| Id | Original bytes | Original SHA-256 |
|---|---:|---|
| W | 5073 | bd2056e45a2119fcd7778e17f2ad6baa9647eadd72e0c1068e07bdeadccb5422 |
| D | 213487 | 0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425 |
| P | 14673 | e60a1ad866e4275e2f4e2e536697ac78a4926161820ade6ac07d939c6cf446bc |
| C | 4508 | 06ac1ccf8aa9fdd612f4465f298b937138b9957ce67f3260bdea702da1bcb35f |

| Id | Decoded chunk bytes | Decoded chunk SHA-256 |
|---|---:|---|
| W | 5060 | bc63510ffde6412ea29f39bdf356a88258b106b7330ff580cb5312a4a6f36d43 |
| D | 213474 | 685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621 |
| P | 14660 | cbf1856bed20810193e8b7d3868bb469e6bf6955de781fe8ce285bdd050e4ee8 |
| C | 4495 | ce7f2b32b9c218a45cf16828983f2e1b59d81562e17ce60c0b849d2021b89f58 |

### Reproduction locators

Offsets are zero-based byte offsets in the decoded chunk. Prototype child
indices, constant indices and instruction PCs are zero-based. Code spans are
half-open. root.N denotes direct child N of the chunk root. PC spans include
both endpoints.

| Id | Installed method | Prototype | PC span | Code byte span |
|---|---|---|---|---|
| W | PlayerParameterWidget.updateTp | root.5 | 0-3 | [1491,1507) |
| W | PlayerParameterWidget.setParameter | root.9 | 0-46 | [2261,2449) |
| W | PlayerParameterWidget.setHPMPTPMaximum | root.11 | 0-18 | [2866,2942) |
| W | PlayerParameterWidget.setHPMPTPValue | root.12 | 0-9 | [3079,3119) |
| W | PlayerParameterWidget.getProgressBarControlName | root.18 | 0-25 | [4631,4735) |
| W | PlayerParameterWidget.getCostProgressBarControlName | root.19 | 0-25 | [4844,4948) |
| D | DesktopWidget.getPlayerGaugeMaxParameter | root.331 | 0-13 | [138963,139019) |
| D | DesktopWidget.getPlayerGaugeCurrentParameter | root.332 | 0-13 | [139136,139192) |
| P | CharaBaseClass.getTP | root.31 | 0-10 | [7703,7747) |
| P | CharaBaseClass.getTPMax | root.41 | 0-8 | [11980,12016) |
| C | CharaBaseClass.hasGameParameter | root.0 | 0-3 | [851,867) |

The chunk roots bind those children to their class methods at these locators.
Each PC/offset pair below refers to the root prototype. The key column is the
root constant index holding the method name.

| Id | Method | Closure PC / offset | Assignment PC / offset | Key constant |
|---|---|---|---|---:|
| W | updateTp | 23 / 124 | 24 / 128 | 10 |
| W | setParameter | 35 / 172 | 36 / 176 | 14 |
| W | setHPMPTPMaximum | 41 / 196 | 42 / 200 | 16 |
| W | setHPMPTPValue | 44 / 208 | 45 / 212 | 17 |
| W | getProgressBarControlName | 62 / 280 | 63 / 284 | 23 |
| W | getCostProgressBarControlName | 65 / 292 | 66 / 296 | 24 |
| D | getPlayerGaugeMaxParameter | 1071 / 4316 | 1072 / 4320 | 332 |
| D | getPlayerGaugeCurrentParameter | 1075 / 4332 | 1076 / 4336 | 333 |
| P | getTP | 97 / 420 | 98 / 424 | 34 |
| P | getTPMax | 127 / 540 | 128 / 544 | 44 |
| C | hasGameParameter | 1 / 36 | 2 / 40 | 1 |

The generated registry at source catalog revision
772df8626317292b5a531a9dccfd6b288a81a12b does not list the two desktop gauge
getters. Their identities here come from the original chunk root assignments,
not registry completeness. The registry's pattern-recovered fields and their
limits are described in [evidence and claims](ai_agents/evidence-and-claims.md#generated-field-limits).

To reproduce the selected finding, authenticate each original resource, obtain
its complete chunk with static extract-lpb or the documented byte-13 decode,
and require the decoded identity above. Parse the complete Lua 5.1 chunk,
resolve each named root assignment, and inspect the selected prototype and
constant locators. No decompiler inference or execution of the retail script
is required.

## TP operand order

updateTp supplies selector 3 to setParameter. The selected setParameter body
calls desktopWidget:getPlayerGaugeMaxParameter() first and retains its three
results in R2, R3 and R4. It next calls
desktopWidget:getPlayerGaugeCurrentParameter() and retains its three results
in R5, R6 and R7. Each tuple is ordered HP, MP, TP, so R4 and R7 are the TP
maximum and current operands.

For selector 3, setParameter passes R4 to setHPMPTPMaximum(3, maximum), then
R7 to setHPMPTPValue(3, current). No arithmetic, clamp, conversion or nil
fallback occurs along either operand path. With the implicit receiver self,
the resulting _setProperty argument order is:

| Order | Explicit arguments |
|---:|---|
| 1 | nil, ProgressBar_Tp, Maximum, maximum |
| 2 | nil, ProgressBar_actionCost_Tp, Maximum, maximum |
| 3 | nil, ProgressBar_Tp, Value, current |

The control and property names above are literal strings. The maximum and current operands
are passed unchanged. These are calls made by the script, conditional on
normal completion of the preceding calls. They establish no native
marshaling or property-application result.

Each desktop getter separately obtains worldMaster:_getMyPlayer(). The maximum
function calls getHPMax, getMPMax and getTPMax on its returned object and
returns those results in that order. The current function calls getHP, getMP
and getTP on its separately returned object and returns those results in that
order. Neither selected desktop function contains a nil receiver guard.
The functions do not establish a common player snapshot across the two
resolutions.

## Maximum and current return rules

CharaBaseClass.hasGameParameter directly returns
self.charaWork.gameParameter. CharaBaseClass.getTPMax calls that helper and
has this complete normal-return rule:

| Helper result | Maximum return |
|---|---:|
| nil or false | numeric 0 |
| any truthy value | numeric 3000 |

Numeric 0 is truthy in Lua and therefore selects 3000 when it is the helper
result. The complete getTPMax prototype contains nine instructions. Its value
returns are at PCs 5 and 7. The terminal empty return at PC 8 is bypassed by
both normal value-return branches. Constant 1 is numeric 0 at decoded offset
12042. Constant 2 is numeric 3000 at decoded offset 12051, with the Lua number
tag followed by an eight-byte little-endian floating value. The selected
maximum body has no native, equipment or work-maximum provider.

CharaBaseClass.getTP uses the same helper branch. It returns numeric 0 for nil
or false and otherwise directly reads and returns
self.charaWork.parameterTemp.tp. The complete current prototype contains
eleven instructions, with value returns at PCs 5 and 9. No scaling or clamp
appears in that read path.

The [work-binder declaration contract](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/work-binder-native-contract.md#charawork),
xivl-client-structs:docs/work-binder-native-contract.md, charaWork, records
parameterTemp.tp as integer16. Its
[initial-value](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/work-binder-native-contract.md#initial-values)
and [missing-storage](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/work-binder-native-contract.md#an-object-without-storage)
sections distinguish the pool-backed member from an object without storage.
Those are declaration and native-reader context from that source. The width
does not supply the literal maximum, an initial pool value or a packet writer.

The return rules assume that dispatch resolves to these selected functions
and that the receiver, method lookup, work lookup and preceding calls complete
normally. Errors on those paths are not converted into a zero fallback.

## Form and caption boundary

The [selected form declarations](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/sqwt-player-parameter-structure.md#selected-form-containment-and-attributes),
xivl-client-data:docs/sqwt-player-parameter-structure.md, record literal
Maximum and Value placeholders of 999 on ProgressBar_Tp. TextBlock_CurrentTp
binds to the Value of ProgressBar_Tp:StatusBar with converter parameter %.f.
The [selected template](https://github.com/XIVLegacy/xivl-client-data/blob/main/docs/sqwt-player-parameter-structure.md#resources-and-selected-template)
binds StatusBar.Maximum to the templated parent's Maximum and declares a
ValueChanged animation toward the parent's Value. These are static
containment and binding-shaped declarations. The placeholder 999 does not
establish the maximum consumed by the selected Lua functions.

The surviving providers are _getMyPlayer for the actual receiver and its
lifetime, work userdata for gameParameter and parameterTemp.tp storage and
contents, and _setProperty for native marshaling, control lookup and applied
properties. Their behavior is outside this operand finding. Actual class
dispatch, storage presence, initialization, synchronization, packet writes and
pool values are not observed here.

No native property application, event delivery, binding evaluation,
formatting, animation or rendered caption result is established. The two
player resolutions need not form one snapshot. The conditional script
literal is not a general server cap, and no live-client result is claimed.
