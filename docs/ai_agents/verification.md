# Verification

`.github/workflows/checks.yml` is the authoritative list of CI-covered checks,
and CI runs them on every pull request and push to `main`.

## Corpus-present check

CI declares `XIVL_CORPUS_ABSENT=1`. With the reproduced `lua/scripts/` corpus
present locally, leave that variable unset and run:

```powershell
Remove-Item Env:XIVL_CORPUS_ABSENT -ErrorAction SilentlyContinue
python tools/validate_corpus.py
```

Exit 0 proves all 2,671 scripts match their recorded sizes, SHA-256 hashes, and
line counts, and that the schemas, registry signals, sidecar callsites, N-API
index, vendored bindings, derived counts, and docs index agree with the corpus.
CI proves only the public metadata and repository shape.

## Corpus reproduction

After running the pinned external LPB pipeline against a user-owned client,
publish its explicit output and regenerate annotations:

```powershell
python tools/lua_corpus.py publish --lua-root C:\path\to\decompile-output
python tools/lua_corpus.py annotate
```

The expected result is a canonical `lua/scripts/` tree, registry, call
sidecars, and N-API index. Rebuilding `manifests/scripts.json` is reserved for
an intentional corpus version change and requires source review.

## Claim limits

A green gate establishes repository integrity and byte-for-byte reproduction
for the inputs present. It does not prove complete decompiler recovery, live
client behavior, or N-API runtime semantics. Record the pinned input, commands,
and output comparison for every research run.
