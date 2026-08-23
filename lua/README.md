# Lua Script Corpus

This contract describes a local decompiled FFXIV 1.23b Lua corpus and its
tracked metadata derived from extraction `2012.09.19.0001`.

## Tracked and local content

- `scripts/<decoded-path>.lua` - local-only decompiled source supplied by the
  user. Git ignores these files.
- `scripts/<decoded-path>.calls.json` - tracked per-script metadata containing:
  N-API names and line locations, decoded and ciphered paths, class names, and counts.
  It does not contain script statements or reconstructive source data.
- `registry.json` - tracked script tree metadata: ciphered-to-decoded mapping,
  class and method names, `require` dependencies, and line counts.
- `napi_index.json` - tracked inverted N-API callsite index joined to the
  vendored `data/vendor/client-structs/lua_api_index.json` bindings. Each API
  also records any receiver-class `_cpp` declarations recovered from the
  corpus and the script that declared them.
- `../manifests/scripts.json` - tracked per-script reproduction contract with
  canonical paths, byte sizes, line counts, and SHA-256 hashes.

The tracked metadata describes the corpus but cannot recreate script bodies.
The retail-derived `.lua` files remain outside the repository and must not be
redistributed.

## Canonical form

The hashes describe canonical decompiler output, not byte-identical Windows
decompiler output. `lua_corpus.py publish` replaces each CRLF byte pair
(`0D 0A`) with LF (`0A`). It does not alter bare CR bytes, trailing whitespace,
indentation, text encoding, or final-newline presence.

An N-API reference is an exact match between an underscore-prefixed Lua
identifier at a word boundary and an entry in the vendored whitelist. Calls,
member and method access, callback assignment, and string-literal references count.
Script-defined underscore helpers do not.

## Extraction pipeline

The required decoder and orchestrator are cross-repository research tools:

- https://github.com/XIVLegacy/xivl-client-structs/blob/main/tools/decode_lpb.py
- https://github.com/XIVLegacy/xivl-client-structs/blob/main/tools/lpb_pipeline.py

`unluac.jar` is user-supplied and is not distributed by either repository.
The pipeline is:

```text
.le.lpb from the user's client
  -> decode_lpb.py, invoked by lpb_pipeline.py
  -> Lua 5.1 bytecode
  -> user-supplied unluac.jar
  -> ciphered decompile output
  -> lua_corpus.py publish
  -> canonical decoded .lua paths and LF normalization
```

The pinned `decode_lpb.py` implements the filename cipher. This repository
applies the same involution in `_corpus.decode_filename_segment` when publishing,
so every ciphered name maps deterministically to one canonical decoded name.

## Regenerating and verifying

1. Run `lpb_pipeline.py` from `xivl-client-structs` against a user-owned
   Final Fantasy XIV 1.23b installation, passing the user-supplied
   `unluac.jar` as required by that tool.
2. From this repository, publish the explicit decompile output:

   ```console
   python tools/lua_corpus.py publish --lua-root <path-to-decompile-output>
   ```

3. Regenerate the tracked derived metadata:

   ```console
   python tools/lua_corpus.py annotate
   ```

4. Run `python tools/validate_corpus.py` to verify the local corpus against the
   2,671 recorded rows.

Maintainers can rebuild the reproduction contract after an intentional corpus
version change with `python tools/lua_corpus.py manifest`. Hash changes require
source review. Do not alter a recorded hash to make validation pass.

## Coverage

- 2,671 scripts have canonical decoded paths.
- 2,650 scripts have at least one extracted class name. Twenty-one do not,
  including 19 one-line stubs.
- 2,585 scripts have at least one `require` dependency.

The [retail Lua resource census](../docs/retail-lua-coverage.md) independently
checks whether the bounded retail `client/script` inventory covers these paths.

## License boundary

The tracked authored tooling, schemas, documentation, and non-reconstructive
metadata are licensed under the repository's MIT license. The user-supplied
retail-derived `.lua` corpus is not covered by that license and is not
redistributable.
