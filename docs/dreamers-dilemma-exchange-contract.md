# Dreamer's Dilemma exchange client contract

`Spl0g2`, `Spl0l2`, and `Spl0u2` each retain one `eventBricotExchange` menu
result and return either an accepted choice or numeric 5. The three variants
share the same selection and return logic and differ in presentation calls.
The retail title/class joins in
[Seasonal quest client contracts](seasonal-quest-client-contracts.md#retail-quest-identities)
identify the Gridania, Limsa Lominsa, and Ul'dah variants. They do not identify
invoking NPCs or historical activation paths.

## Original bytecode and canonical source

All three selected methods are `root/proto9`, with seven fixed parameters and
no varargs. The original Lua 5.1 chunks were decoded from the following
`client/script/tp5rq/r75w9s1v/ruy/` LPBs and parsed through complete EOF.
PCs below start at zero. Byte offsets start at zero in the decoded payload,
rather than the LPB wrapper. Each instruction occupies four bytes.

| Class | LPB basename; bytes; SHA-256 | Payload bytes; SHA-256 |
| --- | --- | --- |
| `Spl0g2` | `ruyj3h.le.lpb`; 6500; `bd717a5d07a482ac80a7aba47d16e55a456e55283e8df777404c625a11d7ac40` | 6487; `8baa03d50d58caf4387b2c4b358daac9cc06dbb6545c23139db7daca9b2cf65d` |
| `Spl0l2` | `ruyjyh.le.lpb`; 6494; `d58c1e5f4e5c5b48863bab9fb68fd986be37b621b4c9f7928ebfbc5c4cf643a7` | 6481; `f1fffa85b0d5bf8352dbe5643cbc7a73430cfc1206befcadaa83e7775320c39d` |
| `Spl0u2` | `ruyjph.le.lpb`; 6030; `5dd1748ea28ff472fd3372771b1316f90c49f12ecf5a7942565e10eb918f55f1` | 6017; `26899f3e03b5a316bab365969b092e5bdefcf39c58d2dfb6ac8dd79a32fd41ed` |

The canonical decoded archive `lua.zip` has SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The complete members below match [manifests/scripts.json](../manifests/scripts.json),
SHA-256 `86798306f71336ee494f12d395db3b8ea571a21224fbd99e2ef87ecd18c61300`.
Canonical text corroborates the selected methods. Original bytecode owns the
control-flow and result-count claims.

| Member under `quest/scenario/spl/` | Bytes; SHA-256 | Function start; class assignment |
| --- | --- | --- |
| `spl0g2.lua` | 17490; `54c4e5af3e69b18971b273e9a715b35c30f9c160f77edf64285191c2ca8e4c14` | lines 398; 644 |
| `spl0l2.lua` | 17259; `468c6164360d802678ab0adc6172c888357327a4fb12a5da01d3519c45e7c243` | lines 404; 654 |
| `spl0u2.lua` | 14976; `83c27d67db0e338206b4f1b4998a188a91b09e3e18cee27e79d9051a1d81cd46` | lines 370; 538 |

## Menu and local result

Parameter numbers start at zero. P0 owns fade/wait calls, P1 is passed into
talk/fade calls, P2 owns talk, scheduler, say, and ask calls, and P3-P6 are four
caller-supplied operands. Their historical producers and domains are unproved.

Each method makes exactly one ask call. Gridania and Ul'dah pass the tuple
`(P2, P0, 33, 5)` and Limsa Lominsa passes `(P2, P0, 32, 5)`, including the
implicit method receiver P2. All three instructions use `CALL A=8 B=5 C=2`,
which requests and retains one result in R8. Every other CALL requests zero
results. There is no repeated ask, confirmation ask, or retry loop in the
selected methods.

| Original instruction | Spl0g2 PC / byte offset | Spl0l2 PC / byte offset | Spl0u2 PC / byte offset |
| --- | --- | --- | --- |
| Single ask CALL | 28 / 3425 | 31 / 3513 | 20 / 3261 |
| R8 equals numeric 5 | 29 / 3429 | 32 / 3517 | 21 / 3265 |
| Fifth-choice RETURN | 47 / 3501 | 50 / 3589 | 25 / 3281 |
| R7 equals boolean true | 134 / 3849 | 140 / 3949 | 101 / 3585 |
| Accepted-choice RETURN | 185 / 4053 | 191 / 4153 | 138 / 3733 |
| Fallback RETURN | 133 / 3845 | 139 / 3945 | 100 / 3581 |
| Selected-count-2 RETURN | 212 / 4161 | 215 / 4249 | 151 / 3785 |

R7 starts as boolean false. Numeric choice 1 selects P3, 2 selects P4, 3
selects P5, and 4 selects P6. With ordinary numeric operands, the corresponding
`1 <= operand` test must pass. That path sets R7 true, then resets it false
when the same operand equals numeric 2. The later comparison tests this live
register against boolean true. It is not a constant `false == true` test.
Lua equality also keeps boolean true distinct from numeric 1.

The choice comparisons are PCs 49/58/67/76 in Gridania, 52/61/70/79 in
Limsa Lominsa, and 27/36/45/54 in Ul'dah. Their `1 <= operand` tests are
two instructions later, true loads four instructions later, equality-with-2
tests five instructions later, and false loads seven instructions later.
The prototype code starts at decoded offset 3313, 3389, and 3181 respectively,
so each listed PC has offset `code start + 4 * PC`. For example, Gridania
PC51@3517 tests `1 <= P3`, PC53@3525 sets R7 true, PC54@3529 tests `P3 == 2`,
and PC56@3537 resets R7 false on equality.

| Condition | Local return behavior |
| --- | --- |
| Retained ask result equals numeric 5 | Finish talk and return that result unchanged. |
| Retained result equals 1-4 and selected numeric operand is at least 1, except exactly 2 | Present the accepted-choice sequence, finish talk, and return that choice unchanged. |
| Retained result equals 1-4 and selected operand equals numeric 2 | Present the selected-count-2 sequence, finish talk, and return numeric 5. |
| Other modeled primitive result or selected numeric operand below 1 | Present the fallback sequence, finish talk, and return numeric 5. |

The fallback sets R8 to 5 at PC85@3653, PC88@3741, and PC63@3433.
The selected-count-2 path sets it to 5 at PC187@4061, PC193@4161, and
PC140@3741 respectively. Consequently, returned 5 does not identify a unique
exit reason. The explicit fifth-choice branch does not establish a native
cancel sentinel or the complete domain of ask results.

## Presentation differences

Gridania uses opening say row 26 and ask row 33. Limsa Lominsa uses 25 and 32
and adds scheduler 354054144 at PC21@3473 before the opening say. Ul'dah uses
26 and 33 and scheduler 70799360 at PC10@3221. Gridania and Limsa Lominsa
surround opening and exit talk with fades. Ul'dah omits those opening and exit
fades. All three accepted-choice sequences include their own internal fade.

| Path | Gridania say rows | Limsa Lominsa say rows | Ul'dah say rows |
| --- | --- | --- | --- |
| Fallback | 44,22,23,24,25 | 43,21,22,23,24 | 44,22,23,24,25 |
| Accepted choice | 27,28 | 26,27 | 27,28 |
| Selected operand equals 2 | 45 | 44 | 45 |

For fallback, all three pass scheduler 354041856 before the first say and
353964032 before the last. Limsa Lominsa and Ul'dah insert a 0.5 wait after
the first fallback say, at PC99@3785 and PC74@3477. Gridania omits that wait.
The accepted sequence passes scheduler 354111488, waits 1, presents the first
say, fades out, passes scheduler 354107392, waits 0.1, fades in, and presents
the second say. Gridania and Ul'dah also pass scheduler 354041856 before the
selected-count-2 say, at PC190@4073 and PC143@3753. Limsa Lominsa omits that
scheduler call. These are script arguments, without a native animation claim.

## Evidence limits

A focused offline model independently decoded all three original chunks and
checked 99 cases against explicit call tuples, call order, result counts,
branch outcomes, and returns. It exercised every reachable instruction and
every CALL, with numeric choices 1-5, out-of-menu primitives, boolean/numeric
distinctions, and each supplied operand below, at, and above the comparison
boundaries. It ran no Lua VM or native client code.

The instructions establish local menu and return behavior. They do not
authenticate item recipes, ownership, costs, grants, historical caller inputs,
actual native acknowledgment or cancel values, caller retries, NPC placement,
event calendars, inventory mutation, or progression. The four caller operands
are comparison inputs. The meaning and effects of opaque native methods remain
outside this finding.
