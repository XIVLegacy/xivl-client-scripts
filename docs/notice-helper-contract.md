# Quest reward Notice helper

`QuestBaseClass.questBaseRewardSeting` calls the player's Notice loading
binding, requests the default quest cutscene fade-in with that player, and
passes literal `0.5` to the quest's `_wait`, in that order. The helper has no
conditional branch. The retail Lua 5.1 bytecode agrees with the canonical
decoded body and the helper claim in
`xivl-decomp:docs/event/notice-widget-lifetime.md`, section "Clearing the staged
target through Lua", at revision
`df77520ba62435402b12b8b8b5d6bc82e45c3e38`.

## Input identity

The extraction is `2012.09.19.0001`, game version `1.23b`. The source entry in
[scripts.json](../manifests/scripts.json) and the resource entry in
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json) identify these
exact inputs:

| Input | Path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical decoded body | `lua/scripts/quest/questbaseclass_common.lua` | 35511 | `CF61A5687DBC7B6ACCD26C8CD3A138DECC0372FB72518AC6F2054F125BC1465E` |
| Retail LPB | `client/script/tp5rq/tp5rq89r57y9rr_7vxxvw.le.lpb` | 13072 | `ECC3F7C6FB49DF196431494AA5AECE95EDE1C24CA1325AF11DDC993A3836322D` |
| Decoded Lua 5.1 payload | XOR-0x73 payload of that LPB | 13059 | `9379EE6832BDFA542273C7F43F065D7A15F9A730D9EF244BE9A565A1FAA53504` |

The canonical body has 1412 lines. The helper occupies lines 1019-1032 and
is assigned to `QuestBaseClass.questBaseRewardSeting` at line 1034. Its Notice
binding reference is also recorded at line 1022 in the
[call sidecar](../lua/scripts/quest/questbaseclass_common.calls.json).

## Bytecode locators

The payload header declares Lua 5.1, official format 0, little-endian,
4-byte integers, `size_t` and instructions, and 8-byte floating numbers.
With the pinned unluac disassembler, the helper is `main/f33`: child index 33
is zero-based, and PCs below are one-based within each prototype. The main
prototype's PCs 100-102 load `QuestBaseClass`, create child 33's closure, and
assign it under constant `k34`, the full string `questBaseRewardSeting`.
Unluac's inline comments truncate long names; the constant table preserves
their full spelling.

Child 33 has three fixed parameters, no varargs or upvalues, a six-register
stack, and nine instructions. Its original debug line range is 7816-7822,
which is distinct from canonical decompile line numbering. At entry, `R0`
is the quest receiver, `R1` is its player argument, and `R2` is an unused
third argument. These roles describe the observed call receivers, not native
type checks.

In the decoded payload, the prototype's debug-line header starts at byte
offset `0x23A6`; its instruction words span `0x23B6`-`0x23D6`. PC `n` is at
`0x23B6 + 4*(n-1)`. Direct little-endian word decoding corroborates the
disassembler's nine opcode and operand observations: the opcode occupies
bits 0-5, `A` bits 6-13, `C` bits 14-22, and `B` bits 23-31. `LOADK` uses
the combined `Bx` field in bits 14-31.

| Child 33 PCs | Observation |
| --- | --- |
| 1-2 | `SELF` selects `_fadeInNowLoadingForNoticeEventJustInArea` on `R1`. `CALL A=3 B=2 C=1` passes only that player receiver and discards results. No Boolean or other explicit argument is passed. |
| 3-5 | `SELF` selects `startFadeInCutSceneDefault` on `R0`; `MOVE` places the player `R1` in the next argument register. `CALL A=3 B=3 C=1` passes the quest receiver and player, discarding results. |
| 6-8 | `SELF` selects `_wait` on `R0`; `LOADK` loads numeric constant `k3=0.5`. `CALL A=3 B=3 C=1` passes the quest receiver and literal wait argument, discarding results. |
| 9 | `RETURN A=0 B=1` returns no values. |

The entire prototype contains only these receiver selections, calls, one
move, one constant load, and return. There is no test, jump, loop, conditional
early return, or Notice-state predicate in this helper. A call that yields or
fails can still delay or prevent subsequent execution. The ordering describes
the instruction path when each preceding call resumes normally.

## Reproduction

Use an explicit decoded scripts root as documented in the
[corpus contract](../lua/README.md#regenerating-and-verifying), hydrating the
recorded archive with `tools/private_lua_corpus.py` if needed. Verify the
source size, hash, and line count against its manifest entry before reading
the helper. Supply an explicit retail installation's `client/script` root
and verify the LPB size and hash against its coverage row before decoding.

The repository procedure uses `tools/retail_script.py` and its pinned unluac
tool at revision `af8bbd217037fabb3b40f601a1ae1450a52375de`.
Decode with `decode_lpb`, then verify the payload's
size, hash, and header above. Write the temporary payload outside the tracked
tree. Run the repository's pinned tool:

```text
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <temporary-listing> <temporary-payload>
```

The JAR's size and SHA-256 are pinned in
[PROVENANCE.json](../tools/vendor/unluac/PROVENANCE.json). Verify that pin
before execution. Check the main prototype's closure assignment and all nine
child instructions, using the full constant table to resolve call names.
Keep payloads, disassembly, and decoded script bodies ignored. Do not republish
or edit the canonical corpus to perform this check.

## Limits

This verifies the helper's static call contract. It does not independently
verify the native binding's target-clear stores, fade completion, the time
unit or scheduling behavior of `_wait`, a historical server invocation,
widget acceptance, or active-event destruction. The cited native finding
owns the separate target-staging and event-lifetime observations. This helper
has no direct EndEvent, widget-open, or continuation call.
