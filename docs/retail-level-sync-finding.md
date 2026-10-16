# Party level sync and status 223995

Verdict: status 223995 and a level-sync label are absent from the bounded
1.23b status-sheet extraction. That result does not establish whether 1.23b
had party level sync through another path, or whether the feature was
introduced only in ARR.

## Evidence

`xivl-client-data:docs/status-names.md`, `Selected name families`, owns the
sheet result: neither `status.csv` nor `xtx_status.csv` contains row 223995.
Neither source's Japanese or English names/descriptions contains the checked
level-sync label. The export contains all 399 status rows, including row 0.
Extraction `2012.09.19.0001` and source identities are pinned in
`xivl-client-data:manifests/retail_sheet_exports.json`:

| Source | SHA-256 |
| --- | --- |
| `csv/status.csv` | `3b09a76123b0fd8aba320dc5513e8182820fef409cf9d40f0b522b10b11d02ec` |
| `csv/xtx_status.csv` | `60eca3b76d1d9799589d9059adeb1e7c3d142e07609a1ad0a053c5e75d9b96ee` |

An additional case-insensitive text check of `xtx__textCommand.csv` and
`xtx_command.csv` finds no literal `level sync` or `level-sync` label. These
are 125 text-command rows and 1,662 command-name/description rows,
respectively, identified by `xivl-client-data:manifests/tables.json`:

| Source | SHA-256 |
| --- | --- |
| `csv/xtx__textCommand.csv` | `1c67abe0af10f211761a2211d928a5a49bf5a5d02445797be6fd5729fd911660` |
| `csv/xtx_command.csv` | `2aa0b20822df0b2270918d9ac5525c86a34a941d7c66d17a106add1b2d6567d3` |

The [party command contract](linkshell-party-command-contracts.md#command-inputs)
establishes invitation, membership, leadership and targeting routes for its
listed commands. It does not establish a level-sync operation. The separate
[party-buff contract](status-parameters-party-buffs.md#party-buff-identity-and-effect)
identifies 223193/223194 as light/full party presentation inputs. Those
party-bonus identities do not supply a level-sync status or command.

## Unestablished boundary

The text checks are bounded string results, not a complete native command or
server capability census. Computed dispatch, another label, a native path,
or a server rule is outside this evidence. No absence of a feature, an
ARR introduction date, or a replacement status ID follows from the missing
row or the listed party commands.
