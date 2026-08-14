# Vendored client-structs input

`lua_api_index.json` is a promoted snapshot used as the default N-API whitelist.
`PROVENANCE.json` is authoritative for its source artifact, source and promoted
sha256 values, source license, evidence tier, and transformation. Vendoring does
not relicense the snapshot.

## Pin policy

- Normal regeneration reads this committed snapshot.
- Re-promote only from an explicit XIVLegacy/xivl-client-structs checkout.
  Record both byte identities in `PROVENANCE.json`.
- Do not edit `lua_api_index.json` in place or silently refresh the pin.
