# Evidence and claims

This repository records extracted client Lua evidence and the derived indexes
that make it searchable. A claim must identify which class of artifact
supports it.

## Evidence classes

| Class | Supports | Does not support |
|---|---|---|
| Extraction from the shipped client and decompiled Lua | What the named extraction and decompiler recovered at `2012.09.19.0001` | Complete client contents, live client behavior, or server behavior |
| Promoted N-API catalog | A pinned API name to `BCS-Y` binding relationship | Runtime semantics of the binding |
| Generated registry, sidecars, and N-API index | Structural relationships derived from the committed corpus | New independent evidence |
| Validation and regeneration results | Repository integrity, determinism, and cross-file agreement | Correctness of the original client extraction |
| Explicit external `--lua-root` research input | Findings from a named decompile run when its provenance is recorded | A canonical repository fact before promotion |
| `live_validated` | Behavior verified against the retail 1.23b client in a recorded live session with an identified session record | Behavior outside the recorded live session |

`data/vendor/client-structs/PROVENANCE.json` is the authoritative source
identity and byte pin for the promoted N-API input.

## Generated field limits

`registry.json` class, method, and `require` fields are pattern-recovered from
decompiled text. A missing field means no supported pattern matched. It does
not establish that the client lacks the class, method, or dependency.

## What counts

An artifact counts as evidence only when it is identified, directly supports
the claim, and fits one of the classes above. Agent output, summaries, search
snippets, and unattributed statements are leads. Inspect the underlying
artifact before promoting a fact.

## Claims and names

Make the narrowest claim the artifact supports. State uncertainty when a class
name, path, API relationship, or interpretation is unresolved. Do not turn a
generated count or a schema-valid record into a claim about the retail client.

Use the decoded path and recorded class names as identifiers. If the corpus
does not establish a name, do not invent one. Keep ciphered and decoded names
linked through `registry.json`.

## Numbers in prose

Keep a figure when it carries the claim, including row counts, coverage
ratios, byte sizes, hashes, offsets, and extraction diffs. Preserve figures
inside quoted or transcribed source content verbatim.

Remove incidental figures. Make approximate figures exact or omit them, and
name the canonical artifact instead of duplicating a changing total.

## Citations

Use this form for promoted facts:

```text
repository-name:path/to/file
```

Add a stable row, symbol, or section locator when useful. When byte identity
matters, record a sha256 in `PROVENANCE.json` rather than in the citation
string. Commit hashes and date pins are not citations: repository histories
are rewritten before publication, and dated "as of" claims rot. Branch names,
working-tree paths, and sibling paths are not citations. Preserve the source
fields in `PROVENANCE.json` verbatim, including dates.
