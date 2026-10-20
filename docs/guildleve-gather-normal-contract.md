# GatherNormal Guildleve article contract

`PrivateGLBattleGatherNormal` has an empty `initAsGuildleve` override and
supplies article data and conditions for numeric indices 1 through 4.
The retail bytecode confirms a five-value article tuple and a one-value
condition result. It does not select this Director for a particular Guildleve
ID or establish objective progression.

## Source identity

The decoded script is
`lua/scripts/director/guildleve/privateglbattlegathernormal.lua`.
Its retail resource is
`client/script/61s57qvs/3p1y6y5o5/us1o9q53y89qqy539q25swvsx9y.le.lpb`.
The registry, reproduction manifest and retail coverage census record its
class, ciphered identity and hashes:
[registry](../lua/registry.json), [scripts](../manifests/scripts.json),
[retail coverage](../manifests/retail_lua_coverage.json).

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Original LPB | 954 | `2B91FB872B950EAAA696D1560FC6D82A840F441EC2D7B4B07025E81577CF43D3` |
| Decoded Lua 5.1 payload | 941 | `D5A3DA39BC36987FD9E28D3B53CF470EE8CA4E6088E4BAE05828F9A41677543E` |
| Canonical Lua, 85 lines | 1601 | `7CCDABEE8D2B59E35A2B470EA6AD2BA6F1C9AC29E64B705E2F0AF3CE0127A1FE` |

Reproduction used [retail_script.py](../tools/retail_script.py) and the
[pinned unluac](../tools/vendor/unluac/PROVENANCE.json), SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
After the documented CRLF-pair-to-LF normalization, its output matched the
canonical manifest exactly. The [corpus guide](../lua/README.md#extraction-pipeline)
describes the pipeline.

## Initialization and article values

Prototype ordinals below are zero-based children of the root. PCs are
one-based instruction ordinals; offsets are zero-based in the decoded payload.
For this wrapper, the corresponding original LPB byte offset is payload
offset plus 13, before XOR decoding.

The root requires `/Director/Guildleve/GuildleveBaseClass` and defines
`PrivateGLBattleGatherNormal` with that base. Its three children implement
the methods below. `initAsGuildleve` has only its receiver parameter and no
varargs. Its sole instruction is `RETURN A=0 B=1`, returning zero values
without calling the base, reading fields or forwarding arguments
(`root.0`, PC 1, offset `0x155`; canonical Lua lines 11-13).
This does not identify its external initialization caller.

Both article methods test equality with numeric 1, 2, 3 and 4. The index is
passed through unchanged. No zero-based conversion or string-to-number
conversion occurs.

| Method | Index equal to 1, 2, 3 or 4 | Other index |
| --- | --- | --- |
| `getArticleDataOnGuildleveInfo(index)` | `(typeResult, worldMaster, textResult, guildleveId, index)` | `(0, nil, 0, 0, 0)` |
| `getArticleCondition(index)` | First result of `self:getArticleConditionForInfo("get")` | `0` |

For an accepted index, the article method calls
`self:getArticleTypeForInfo("barFraction")`, then
`self:getTextIdForInfo("item")`, then `self:getGuildleveId()`.
It retains only the first result of each helper and returns exactly five
positions, including the second-position nil on the unsupported path.
It does not forward the article index to those helpers.
The condition method returns exactly one value on either path.

| Edge | Bytecode locator | Canonical Lua lines |
| --- | --- | --- |
| Article equality tests | `root.1`, PCs 7-17, offsets `0x199-0x1C1` | 24-31 |
| Article helper calls and unchanged index | `root.1`, PCs 18-30, offsets `0x1C5-0x1F5` | 32-47 |
| Five-value article return | `root.1`, PC 38, offset `0x215`, `RETURN A=7 B=6` | 57 |
| Condition equality tests | `root.2`, PCs 3-13, offsets `0x2EB-0x313` | 65-72 |
| Condition helper call | `root.2`, PCs 14-17, offsets `0x317-0x323` | 73-77 |
| One-value condition return | `root.2`, PC 20, offset `0x32F`, `RETURN A=2 B=2` | 82 |

The [journal lifecycle](guildleve-journal-lifecycle.md#objective-article-tuple-routing)
owns the downstream ten-slot article assembly and widget routing.
The [base Director contract](content-director-ui-contracts.md#guildleve-and-request-directors)
owns generic work updates and UI publication. Neither supplies the missing
caller of this concrete empty initialization override.

## Evidence boundary

This chunk has no per-ID selector. It passes through `getGuildleveId()`
without comparing it. Its helper keys do not prove helper result codes,
item requirements, object interactions, spawn composition, completion or
reward policy. The retail class-to-Guildleve binding, external initialization
arguments and objective-state producer remain unresolved.
