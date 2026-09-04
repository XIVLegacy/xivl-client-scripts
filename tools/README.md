# Tooling

Use this guide to run the repository checks and regenerate the owned corpus
indexes from their documented inputs.

## Commands

- Validate the repository with `python tools/validate_corpus.py`.
- Publish scripts and registry with
  `python tools/lua_corpus.py publish --lua-root <path>`. See [Corpus
  regeneration](../lua/README.md#regenerating-and-verifying).
- Regenerate N-API annotations with `python tools/lua_corpus.py annotate`. See
  [Corpus regeneration](../lua/README.md#regenerating-and-verifying).
- Build the hash contract with `python tools/lua_corpus.py manifest`. See
  [Corpus regeneration](../lua/README.md#regenerating-and-verifying).
- Check MyPlayer timer consumers with
  `python tools/myplayer_timer_consumers.py --check`. See [Consumer
  report](../docs/myplayer-timer-consumers.md).
- Check quest selector consumers with
  `python tools/quest_selector_consumers.py --check`. See [Consumer
  report](../docs/quest-selector-consumers.md).
- Check general parameter 18 consumers with
  `python tools/general_parameter_18_consumers.py`. See [Consumer
  report](../docs/general-parameter-18-consumers.md).
- Census retail Lua resources with
  `python tools/retail_lua_coverage.py --client-root <retail-install> --tools-root <xivl-tools-checkout>`.
  See [Coverage census](../docs/retail-lua-coverage.md).
- Package the local private Lua corpus with
  `python tools/private_lua_corpus.py package --output <archive.zip>`.
  The command verifies `lua/scripts` against `manifests/scripts.json` and
  writes a deterministic ZIP outside the source tree. Verify an existing
  package with `python tools/private_lua_corpus.py verify --package
  <archive.zip>`. Hydrate only an explicitly supplied absent or empty external
  directory with `python tools/private_lua_corpus.py hydrate --package
  <archive.zip> --destination <directory>`; hydration stages beside the target,
  verifies the complete tree, and publishes it atomically. Each command reports
  the file count, total bytes, and a tree SHA-256 over sorted member paths,
  sizes, and per-file SHA-256 values.

## Validation

The [checks workflow](../.github/workflows/checks.yml) is authoritative for
CI-covered checks. `validate_corpus.py` restricts tracked files to permitted
top-level groups and enforces required agent-tooling ignore lines, forbidden
paths, PE magic, absolute maintainer paths, and private-reference tokens. It parses
the tracked JSON, runs focused tests, validates schemas and referential
integrity, checks the reproduction manifest, verifies vendored inputs, and
checks paths listed by the docs index. With a locally supplied corpus it also
verifies every script hash and re-derives registry and callsite data.
It also validates the retained retail coverage census against its schema,
internal inventory digest, corpus and sidecar pins, and independently anchored
ciphered paths. Re-reading retail bytes is an explicit generator `--check`, not
part of portable repository validation.

The workflow checks whitespace against the event's reviewed revision range:
pull requests use base-to-head, pushes use before-to-after, and manual runs
check the dispatched commit against its parent.

Python with `jsonschema` is required.

## Lua corpus builder

The local `lua/scripts/` corpus is a user-supplied input. `lua_corpus.py`
exposes three independently runnable operations:

- `publish`: builds `lua/registry.json` and publishes decoded scripts from an
  explicit `--lua-root <path>`. It stages both outputs and installs them
  together only after the full source tree succeeds. `--output-root` is the
  only publication destination override.
- `annotate`: writes per-script `.calls.json` sidecars and `lua/napi_index.json`
  from the canonical local corpus and vendored N-API
  index. The N-API index also records `_cpp` receiver-class declarations and
  their declaring scripts from the corpus.
- `manifest`: writes `manifests/scripts.json`, the byte-for-byte reproduction
  contract for the canonical local corpus. Annotation and manifest paths are
  repository-owned and have no command-line overrides.

`_corpus.py` is the internal implementation shared by publication, annotation,
validation, and focused tests. It is not a human entry point.

`test_retail_script.py` remains a standalone runner because the credentialed
workflow invokes it directly. Its pass/fail summary is intentionally separate
from unittest discovery and forms part of that contract.

`data/vendor/` holds promoted inputs with immutable provenance. The
pin policy beside `PROVENANCE.json` is documented in
`data/vendor/client-structs/README.md`. Do not edit a vendored file in
place or silently refresh the pin.

## Quest selector report

`quest_selector_consumers.py` retains the 42 named two-selector quest rows plus
the 91 corresponding message callsites. Regenerate it only from the pinned
client-data CSV inputs:

```text
python tools/quest_selector_consumers.py --client-data-root <xivl-client-data-checkout>
```

The portable `--check` mode verifies the retained source hashes, corpus pins,
row counts, and local Lua callsites without requiring the sibling checkout.
