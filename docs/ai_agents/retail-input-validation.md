# Retail-input validation

The normal asset-free corpus gate remains the merge gate. The retail-input
workflow is an additional manual check for one bounded, already tracked Lua
claim. It retains one sanitized attestation and never publishes LPB bytes,
decoded chunks, decompiled source, or diagnostics.

## Granted lane

| Item | Grant |
|---|---|
| Branch | `retail-battle-command-script-ci` |
| Workflow | `.github/workflows/retail-checks.yml` |
| Evidence job | `Battle Command Script Checks` |
| Check | `battle-command-baseclass-v1` |
| Input manifest | `manifests/retail_inputs.json` |
| Check contract | `manifests/retail_battle_command_check.json` |
| Passing attestation | `manifests/retail_evidence/battle-command-baseclass-v1.json` |
| Environment | `retail-evidence` |
| Input coordinate | `XIVLegacy/xivl-private-assets` |

The input grant pins `battle-command-baseclass-lpb-1.23b` to commit
`aeb52f6dbde95a793ee6d52be28de9f28a885b15`, its exact repository-relative
path, 1,507 bytes, and SHA-256
`74761459950b4dbafab6c879ea9a4c1437d4bfe8084058be2023e32add32e569`.
The grant permits only `battle-command-baseclass-v1`.

## Trust boundary

Credentialed execution is manual `workflow_dispatch` from protected `main`.
The public preflight proves the dispatch event, branch, checked-out SHA, and
current remote `main` SHA before the environment job can start. It rejects
pull and merge refs and accepts no user-supplied input coordinate, revision,
hash, check, or toolchain value.

The environment variable `RETAIL_INPUTS_REPOSITORY` is fixed to
`XIVLegacy/xivl-private-assets`; the environment secret is
`RETAIL_INPUTS_TOKEN`. The token is used only for bounded commit, reachability,
tree metadata, and one manifest-pinned blob request. The downloaded object is
checked for the declared size and SHA-256 before decoding.

The workflow keeps all input, intermediate output, and tool logs below one
mode-0700 temporary root. It removes that root on every outcome. Shell
tracing is disabled, API errors are reduced to a fixed label, and Java output
is captured rather than printed.

## Pinned toolchain and reproduction

The redistributable unluac artifact is vendored at
`tools/vendor/unluac/unluac_2025_12_23.jar`. The repository gate requires
796,256 bytes and SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.
`LICENSE.txt` is the embedded MIT notice and `PROVENANCE.json` records the
dated SourceForge coordinate, retrieval date, identity, and upstream project.

`tools/retail_script.py` adapts the first-party LPB wrapper and filename
cipher. It decodes the approved LPB to a Lua 5.1 chunk, invokes the pinned JAR,
and applies only the exact CRLF-pair-to-LF canonicalization. The expected
decoded chunk is 1,494 bytes with SHA-256
`95d29680ba473e0090a3a90573d38e7ce13a9ca63759c7f846bc8a9e5fa83eb0`; the
canonical script is 2,533 bytes with SHA-256
`0eb0b8c77b05128461d94ca1a9bee9b65bccf397ab8efd60903c448915d1e757` and 144
lines. The regression test preserves the known 2,677-byte Windows JAR output
and its 144-byte CRLF reduction.

## Claim boundary

The verifier compares only the named script's byte identity and safe metadata:
class `BattleCommandBaseClass`, its ten tracked method names, required base
path `/Command/Game/GameCommandBaseClass`, `_defineBaseClass` at line 5, and
`_getData` at lines 75, 81, and 87. It does not prove the other 2,670 scripts,
Lua runtime semantics, decompiler semantic correctness, or any untracked
source interpretation.

The workflow runs a deliberate one-byte script mutation and requires the
verifier to reject it. Only the six-field schema-valid attestation can be
uploaded as `retail-script-attestation/retail-evidence-attestation.json` with
30-day retention. A failure attestation is not tracked.

## Local checks

The normal gate runs without the retail input. The focused retail contract and
mutation suite is:

```powershell
python tools\test_retail_script.py
python tools\validate_corpus.py
```

With the supplied corpus available, leave `XIVL_CORPUS_ABSENT` unset for the
full hash and sidecar checks. For a clean public-tree check, set
`XIVL_CORPUS_ABSENT=1`. Run `git diff --check`, an ASCII scan, actionlint when
available, vendor hash/license verification, and a staged tracked-file review
before publication. The LPB and decompiled outputs belong only in ignored
temporary storage during an owner-approved local rehearsal.
