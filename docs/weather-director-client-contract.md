# Weather director client contract

`WeatherDirectorBaseClass.init` declares synced `weatherDirectorWork.weatherId`
as an `integer16` under tag `weatherInfo`
(`weatherdirectorbaseclass.lua:3-31`). In `processUpdateWork`, the client
reads the local player's prior `getWeatherId()`. If it is nonzero, the
method calls `_setWeather(newWeatherId, 15)`; it skips that call when the
prior ID is zero. It then calls `setWeatherId(newWeatherId)` in either case
(`weatherdirectorbaseclass.lua:32-38`; decoded bytecode
`0x00024E-0x000292`). The transition literal 15 belongs to this director
path, not every area-weather update or opcode `0x000D` packet.

The installed
`client/script/61s57qvs/n59q25s/n59q25s61s57qvs89r57y9rr.le.lpb`
has SHA256 `4630DA60FEB9E82AAEE95957848C4565D8FD7AFB387CF8DD53946568B7027AE6`.
Its decoded LUAC matched the recovered chunk byte-for-byte, SHA256
`4E365241C5E2EE9291599A844D0F0D7EA7C921D3DD7AA1D3DFD8D0B80BD68E7A`.
The recovered source identity is `manifests/scripts.json:9500-9505`,
SHA256 `842BD1C6271152772EDBBCEC13C8A18B8230F7B0D76B865EE0011DF62022F62E`.
This script does not establish the historical producer of a weather ID,
the selected area resource, or a visible transition outcome. The separate
native packet-duration and resource-queue path is documented in
`xivl-decomp:docs/net/weather-transition-runtime.md`.
