# Contributing

Contributions use a fork-and-pull-request workflow against `main`. Keep each
change focused, and open it only after all repository CI checks pass.

## Before contributing

Read the [corpus contract](lua/README.md) and the
[tooling reference](tools/README.md) before changing corpus metadata,
annotations, builders, schemas, or policy.

The Lua corpus is immutable retail evidence. Do not hand-edit decompiled
scripts, sidecars, or generated indexes. Regenerate owned products through
their documented tools. Shipped in-game identifiers are evidence and are
never renamed for style, clarity, or consistency.

Vendored inputs are pinned snapshots. Do not edit them in place or silently
refresh a pin. Re-promote from an explicit source and update the adjacent
provenance record with both byte identities.

Do not submit binary client input, LPB files, client archives, captures,
packet dumps, credentials, local settings, generated build output, or
maintainer-only working material. Do not add a license for the retail-derived
corpus or add locally supplied `.lua` files to the tracked tree.

## Pull requests

Keep one pull request to one documentation batch, annotation change, schema
change, or tooling slice. Explain the evidence and the regeneration path when
generated products change.

The contributor owns every submitted line, including AI-assisted work. If
you could not explain what your diff does and why it belongs, do not open the
pull request.
