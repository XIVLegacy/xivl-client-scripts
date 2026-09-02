# Retail Lua resource coverage

The 2026-08-23 census found complete static resource coverage for the bounded
FFXIV 1.23b retail input. All 2,671 LPB resources under `client/script` were
valid supported wrappers and matched the independently recorded ciphered path
of one corpus script. The only other file was one SAN resource, classified as
non-script. No script, alias, wrapper variant, or extraction discrepancy
remained.

| Result | Count |
|---|---:|
| Files inventoried | 2,672 |
| Exact script matches | 2,671 |
| XOR-73 LPB wrappers | 2,670 |
| Raw LPB wrappers | 1 |
| Non-script resources | 1 |
| Missing corpus scripts | 0 |
| Missing retail resources | 0 |
| Duplicate aliases | 0 |
| Unsupported wrappers | 0 |
| Extraction failures | 0 |
| Ciphered-path mismatches | 0 |

`../manifests/retail_lua_coverage.json` is the durable census. Each resource
record contains only its relative resource path, normalized path, byte size,
SHA-256, wrapper classification, decoded payload size and SHA-256, and coverage
classification. It contains no retail payload bytes or machine-specific
absolute paths. Its inventory digest is
`C0BC21DE2626F619AD278C4E043F537A2B6C1CF3263D3110323CC31054B97CF2`.

## Evidence boundary

The generator requires the exact read-only `XIVLegacy/xivl-tools` commit
`d882f2d7432d6f7e569f9f5424af1a33a4938f83`. It also verifies the source hashes
of `src/formats/src/lua_path.rs` and `src/formats/src/lpb.rs` before scanning.
The census pins the tracked script manifest, registry, and a path/size/hash
inventory of all 2,671 call sidecars.

A match requires all of these independent checks:

1. The resource has a supported LPB wrapper and a Lua 5.1 payload signature.
2. The normalized resource path equals the registry's ciphered `.lua` path
   after only the documented `.lua` to `.le.lpb` suffix conversion.
3. The ASCII involution decodes the resource stem to the same canonical script
   path.
4. That canonical script is present in the reproduction manifest.

Magnitude, payload similarity, and modern game data are not match evidence.

## Discrepancy classifications

The generator defines zero-count classifications so future inputs have a stable
interpretation:

- `duplicate-alias` - multiple resource names normalize to one path or resolve
  to a script already covered by its exact ciphered resource.
- `missing-script` - a valid named LPB decodes to no script in the corpus.
- `missing-retail-resource` - a corpus script has no exact retail resource.
- `ciphered-path-mismatch` - a valid LPB decodes to a corpus script but is not
  that script's independently recorded ciphered resource.
- `non-script-resource` - a file is neither LPB-named nor LPB-wrapped.
- `non-script-wrapper` - a valid LPB is not named as a `.le.lpb` script.
- `unsupported-wrapper` - an LPB candidate has unsupported wrapper magic.
- `extraction-failure` - a supported wrapper is truncated or lacks the Lua 5.1
  signature after bounded extraction.
- `unsupported-path` - a path is non-ASCII, empty, or contains upward traversal.

## Reproduce and check

Use explicit local roots; neither path is retained in the output:

```powershell
python tools/retail_lua_coverage.py --client-root <retail-install> --tools-root <xivl-tools-checkout>
python tools/retail_lua_coverage.py --client-root <retail-install> --tools-root <xivl-tools-checkout> --check
```

The first command regenerates the census and the second requires byte-identical
JSON. `python tools/validate_corpus.py` validates the retained schema, internal
counts, ciphered-path matches, inventory digest, corpus hashes, sidecar
inventory, and tool pin without needing retail bytes.

This result proves exhaustive static coverage only for the recorded bounded
retail inventory. It does not prove decompiler semantic fidelity, live client
execution, or coverage of a different installation.
