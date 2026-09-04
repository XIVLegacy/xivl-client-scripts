# Retail-input validation

The normal asset-free corpus checks remain the merge requirement. The
retail-input
workflow adds manual checks for bounded, already tracked Lua claims. Each job
retains one sanitized attestation and never publishes LPB bytes, archives,
decoded chunks, decompiled source, or diagnostics.

## Approved check

| Item | Grant |
|---|---|
| Branch | `main` |
| Workflow | `.github/workflows/retail-checks.yml` |
| Evidence job | `Battle Command Script Checks` |
| Check | `battle-command-baseclass-v1` |
| Input manifest | `manifests/retail_inputs.json` |
| Check contract | `manifests/retail_battle_command_check.json` |
| Passing attestation | `manifests/retail_evidence/battle-command-baseclass.json` |
| Environment | `retail-evidence` |
| Input coordinate | `XIVLegacy/xivl-private-assets` |
| Shared actions | Immutable revision from `XIVLegacy/xivl-tools` |

The input grant pins `battle-command-baseclass-lpb-1.23b` to commit
`aeb52f6dbde95a793ee6d52be28de9f28a885b15`, its exact repository-relative
path, 1,507 bytes, and SHA-256
`74761459950b4dbafab6c879ea9a4c1437d4bfe8084058be2023e32add32e569`.
The grant permits only `battle-command-baseclass-v1`.

The `Decoded Lua Corpus Checks` job is separately granted by
`manifests/private_lua_corpus.json`. It pins
`decoded-lua-corpus-1.23b` to commit
`361cbed32b2d89f97dc6e40fcc5d9230a0412eaa`, path
`extracted/ffxiv-1.23b/client-scripts/lua.zip`, 14,385,427 bytes, and SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The archive expands to 2,671 manifest-matched scripts and 13,971,401 bytes
with tree SHA-256
`05edcf81aec7ad28007c059991b6858665680f860bd1ed2aa5100e7fc120da0d`.

## Trust boundary

Credentialed execution is manual `workflow_dispatch` from protected `main`.
The public preflight proves the dispatch event, branch, and checked-out SHA.
It also proves the current remote `main` SHA before the environment job can
start. It rejects
pull and merge refs and accepts no user-supplied input coordinate, revision,
hash, check, or toolchain value.

The environment secret is `RETAIL_INPUTS_TOKEN`. The pinned
`fetch-retail-input` action fixes the input repository and API boundary; this
check supplies only the token and four manifest-pinned declarations: commit,
path, size, and SHA-256. The token is used only for bounded commit,
reachability,
tree metadata, and one manifest-pinned blob request. The downloaded object is
checked for the declared size and SHA-256 before decoding.

The workflow keeps all input, intermediate output, and tool logs below one
mode-0700 temporary root. The pinned `finalize-retail-attestation` action
removes that root and checks the retained envelope on every outcome. Shell
tracing is disabled, API errors are reduced to a fixed label, and Java output
is captured rather than printed.

## Pinned toolchain and reproduction

The shared `setup-retail-toolchain` action at the pinned `xivl-tools` commit
installs the fixed Temurin JDK and no Ghidra for this Lua check. The
redistributable unluac artifact is vendored at
`tools/vendor/unluac/unluac_2025_12_23.jar`. Repository validation requires
796,256 bytes and SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
`LICENSE.txt` is the embedded MIT notice and `PROVENANCE.json` records the
dated SourceForge coordinate, retrieval date, identity, and upstream project.

`tools/retail_script.py` adapts the first-party LPB wrapper. It decodes the
approved LPB to a Lua 5.1 chunk, invokes the pinned JAR, and applies only the
exact CRLF-pair-to-LF canonicalization. The focused test runs the vendored JAR
twice over a synthetic Lua 5.1 chunk and checks the canonical output. The
expected decoded chunk is 1,494 bytes with SHA-256
`95d29680ba473e0090a3a90573d38e7ce13a9ca63759c7f846bc8a9e5fa83eb0`; the
canonical script is 2,533 bytes with SHA-256
`0eb0b8c77b05128461d94ca1a9bee9b65bccf397ab8efd60903c448915d1e757` and 144
lines. The regression test preserves the known 2,677-byte Windows JAR output
and its 144-byte CRLF reduction.

## Claim boundary

The repository-specific verifier compares only the named script's byte identity and safe metadata:
class `BattleCommandBaseClass`, its ten tracked method names, required base
path `/Command/Game/GameCommandBaseClass` and `_defineBaseClass` at line 5.
It also checks `_getData` at lines 75, 81, and 87. It does not prove the other
2,670 scripts,
Lua runtime semantics, decompiler semantic correctness, or any untracked
source interpretation.

The workflow runs a deliberate one-byte script mutation and requires the
repository-specific verifier to reject it. The shared finalizer and the local
retained-file/schema checks must both pass before the six-field attestation can
be uploaded with 30-day retention. A failure attestation is not tracked.

The full-corpus job independently checks the archive identity, every member
against `manifests/scripts.json`, and the aggregate tree identity. It hydrates
only a disposable external directory, runs the complete corpus validator with
`XIVL_LUA_SCRIPTS_DIR`, and rejects a mutated archive. Normal CI runs the same
contract and mutation tests without fetching the archive.

## Reproduced result

[Retail Checks run 32518216861](https://github.com/XIVLegacy/xivl-client-scripts/actions/runs/32518216861)
reproduced the tracked
[`battle-command-baseclass.json`](../../manifests/retail_evidence/battle-command-baseclass.json)
attestation byte-for-byte.
The retained file is 337 bytes with SHA-256
`da4ee314b07c6a865e5e40e45006493eaf41c47f9e5b067145b5ec85fdf05eff`.
Artifact allowlist, schema, cleanup, negative-control, and public-log leakage
reviews passed.

## Local checks

The normal checks run without the retail input. The focused retail contract plus
its mutation suite is:

```powershell
python tools\test_retail_script.py
python tools\test_private_lua_corpus.py
python tools\test_retail_lua_corpus.py
python tools\validate_corpus.py
```

With the supplied corpus available, leave `XIVL_CORPUS_ABSENT` unset and set
`XIVL_LUA_SCRIPTS_DIR` when it is hydrated outside the checkout. For a clean
public-tree check, set `XIVL_CORPUS_ABSENT=1`. Run `git diff --check`, an ASCII scan, actionlint when
available, vendor hash/license verification, and a staged tracked-file review
before publication. The LPB and decompiled outputs belong only in ignored
temporary storage during an owner-approved local rehearsal.
