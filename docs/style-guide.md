# Style guide

Repository style covers authored Python, schemas, annotations, and
documentation. It does not establish Lua behavior, native API meaning,
evidence strength, or corpus provenance.

## General

- Prefer existing local patterns once they exist.
- Keep changes scoped to the annotation, index, or tool being changed.
- Use small, explicit functions and modules before adding abstractions.
- Follow the [comment policy](ai_agents/comments-and-prose.md) for source
  comments.
- Do not reformat decompiled scripts, immutable sidecars, vendored inputs, or
  generated indexes for style alone.

### Documentation

The public [documentation policy](ai_agents/README.md#documentation-policy) is
canonical for authored documentation. The
[evidence policy](ai_agents/evidence-and-claims.md) owns claim wording,
citations, confidence, and provenance.

## Python

- Use 4 spaces for indentation and no tabs.
- Use `lower_snake_case` for modules, functions, and variables,
  `UpperCamelCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Group imports as standard library, third-party packages, then local modules.
- Prefer `pathlib.Path` for filesystem paths and explicit text encodings.
- Keep command entry points thin; put reusable work in importable functions.
- Raise or report specific failures instead of using broad exception handlers.
- Add type annotations where they clarify annotation records, paths, or public
  helper contracts.
- Use Ruff 0.15.21 as the Python formatter and linter. Run `ruff check
  --no-cache tools` and `ruff format --check --no-cache tools` from the
  repository root.

## Corpus and structured data

- Preserve shipped identifiers and source-defined spelling exactly.
- Preserve schema-defined names, field order, identifiers, and null behavior.
- Edit canonical annotations, schemas, or builders, then regenerate owned
  output.
- Preserve the local indentation and ordering of hand-authored JSON.
- Never rename or rewrite retail-derived content to satisfy authored-code
  style.

## Verification

Use the owning commands in [tools/README.md](../tools/README.md). Formatting is
not a substitute for corpus, schema, provenance, or evidence validation.
