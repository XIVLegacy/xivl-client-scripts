# Tooling

Use this guide to run the repository gate and regenerate the owned corpus
indexes from their documented inputs.

| Task | Entry point | Details |
|---|---|---|
| Validate the repository | See the [verification policy](../docs/ai_agents/verification.md) | [Checks workflow](../.github/workflows/checks.yml) |
| Publish scripts and registry | `python tools/lua_corpus.py publish --lua-root <path>` | [Corpus regeneration](../lua/README.md#regenerating) |
| Regenerate N-API annotations | `python tools/lua_corpus.py annotate` | [Corpus regeneration](../lua/README.md#regenerating) |
| Build the hash contract | `python tools/lua_corpus.py manifest` | [Corpus regeneration](../lua/README.md#regenerating-and-verifying) |

## Validation gate

The [checks workflow](../.github/workflows/checks.yml) is authoritative for
CI-covered checks. `validate_corpus.py` restricts tracked files to permitted
top-level groups and enforces required agent-tooling ignore lines, forbidden
paths, PE magic, absolute maintainer paths, and private-reference tokens.
It parses the tracked JSON, runs focused tests, validates schemas and referential
integrity, checks the reproduction manifest, verifies vendored inputs, and
enforces docs index coverage. With a locally supplied corpus it also verifies
every script hash and re-derives registry and callsite data.

The [verification policy](../docs/ai_agents/verification.md) owns the
corpus-present mode and its claim boundary. Python with `jsonschema` is
required.

## Lua corpus builder

The local `lua/scripts/` corpus is a user-supplied input. `lua_corpus.py`
exposes three independently runnable operations:

- `publish`: builds `lua/registry.json` and publishes decoded scripts from an
  explicit `--lua-root <path>`. It stages both outputs and installs them
  together only after the full source tree succeeds.
- `annotate`: writes per-script `.calls.json` sidecars and
  `lua/napi_index.json` from the local corpus and vendored N-API index.
- `manifest`: writes `manifests/scripts.json`, the byte-for-byte reproduction
  contract for the canonical local corpus.

`_corpus.py` is the internal implementation shared by publication,
annotation, validation, and focused tests. It is not a human entry point.

`data/vendor/` holds promoted inputs with immutable provenance. The
pin policy beside `PROVENANCE.json` is documented in
`data/vendor/client-structs/README.md`. Do not edit a vendored file in
place or silently refresh the pin.
