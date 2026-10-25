# Camp favored-destination client contract

`PopulaceCampMaster.defTalk` presents favored-destination registration and
returns a local slot choice. It does not write favored state, debit currency,
or establish the server callback that consumes the choice.

## Manine and destination identity

The actor-class comparison with `1500068` selects speech rows 11 and 12 and
stores destination `1280062`. In `populaceCampMaster.csv`, English row 11
identifies Gatewarden Manine at Camp Bentbranch. Independently,
`actorclass.csv` row `1500068`, column 5, names display key `1300085`, whose
English display name is Manine. `aetheryte.csv` row `1280062`, column 0,
contains place key `2017` (Camp Bentbranch).

These joins identify a recognized actor class and destination within the
client method. They do not authenticate a spawned actor's script class,
position, zone variant or historical server dispatcher.

Source: `xivl-client-data:manifests/tables.json`, selected rows of
`actorclass.csv`, `xtx_displayName.csv`, `populaceCampMaster.csv`,
`aetheryte.csv` and `xtx_placeName.csv`. Columns are zero-based after the row
key. The corresponding script branch is `root/proto1` PCs 117-136,
decoded offsets `0x039C`-`0x03E8`.

## Supplied state and result

Write the method inputs as `(self, player, F1, F2, F3, S, T)`.
`F1..F3` are caller-supplied values tested against the selected destination.
Their historical producer and persistence are unbound. `S` and `T` affect
other actor branches; the Manine branch above does not read them.

| Condition or step | Client behavior |
| --- | --- |
| `F1 == nil` | Finish the talk turn and return no values. |
| Any of `F1..F3` equals `1280062` | Finish and return no values. |
| Otherwise | Ask owner/self text 45 in mode 2; only answer 1 continues. |
| Continued path | Say rows 48 and 49, then ask row 50 in mode 2; only answer 1 continues. |
| First zero among `F1..F3` | Save result 1, 2 or 3 respectively. |
| No zero | Ask row 53 in mode 4 with `F1,F2,F3`; retain its first result. |
| Replacement result nil or 4 | Finish and return that result unchanged. |
| Other replacement result | Resolve 1/2/3 to the corresponding supplied value, say row 59 with that old value and destination, then ask row 60 in mode 2. |
| Final confirmation other than 1 | Replace the saved result with nil. |
| Final tail | Finish the talk turn and return exactly one saved result. |

The original bytecode preserves replacement answer 4. It does not normalize
that answer to nil. An out-of-domain result from row 53 also has no explicit
range rejection here; the widget's actual result domain needs its own evidence.
This is a method with three input slots, not proof of an account-wide limit.

For destination `1280062`, the method supplies numeric `500` to speech row 49.
That row formats a displayed gil amount. This static presentation does not
prove a historical charge, successful registration, settlement, persistence,
or a global price. The text's reduced-anima explanation establishes wording,
not an independently observed cost calculation.

The smallest callback contract is therefore: supply the actor and player plus
three current destination values, await the local method result, and preserve
the distinction between no returned values, nil, numeric 4 and a selected
slot. The caller that associates that result with destination `1280062` and
publishes new state remains unbound. No standalone request opcode or result
packet is established by this method.

## Source identity and bytecode locators

Extraction: `2012.09.19.0001`. The selected LPB and decoded payload match
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json); the Lua
source matches [`scripts.json`](../manifests/scripts.json).

| Artifact | SHA-256 |
| --- | --- |
| `729s9/wu7/uvupy975/uvupy97579xux9rq5s.le.lpb`, 5,415 bytes | `4bba663d3dad4ac82585d024d2fdeaa120fe8c8135e19e203f669a2afef60e55` |
| Decoded chunk, 5,402 bytes | `a2a5c391524fd2bef5edf0fd1648354a17dffe651ee2d7ee23e6084a22833116` |
| `chara/npc/populace/populacecampmaster.lua`, 31,499 bytes | `0e514663ae4cdcdae67587c1825c0a19cc1a644ac9cbc1629adb4ebc807cef7d` |

The method is `root/proto1`, seven parameters, code offset `0x01C8`.
The state predicates and no-value exits are PCs 632-645 (`0x0BA8`-`0x0BDC`).
The two initial asks are PCs 646-680 (`0x0BE0`-`0x0C68`). Slot selection,
replacement and final confirmation are PCs 681-737 (`0x0C6C`-`0x0D4C`).
PC 740 (`0x0D58`) is `RETURN A=10 B=2`; the early exits use `B=1`.
The display-value branch is PCs 577-584 (`0x0ACC`-`0x0AE8`).

Reproduce the decoded chunk with `tools/retail_script.py` and inspect it with
`ChunkReader` and `instruction` in `tools/build_quest_contracts.py`. Check
CALL arity and branch targets rather than inferring them from decompiler
temporary names. No runtime registration or capture was performed.
