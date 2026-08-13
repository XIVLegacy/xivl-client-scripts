# Vendored client-structs input

`lua_api_index.json` is a promoted snapshot used as the default N-API
whitelist. `PROVENANCE.json` is authoritative for its source artifact,
source and promoted sha256 values, evidence tier, and transformation.

## Pin policy

- Normal regeneration reads this committed snapshot.
- Re-promote only from an explicit XIVLegacy/xivl-client-structs checkout and
  record both byte identities in `PROVENANCE.json`.
- Do not edit `lua_api_index.json` in place or silently refresh the pin.
