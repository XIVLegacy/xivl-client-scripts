# WidgetOpenCommand client boundary

The installed static-actor registry maps low ID 24228 to
`/Command/System/WidgetOpenCommand`
(`xivl-client-data:manifests/staticactor_class_paths.json:3213-3216`).
The corresponding client command accepts a widget-path argument and
varargs. Its installed bytecode performs these operations in order:

1. Calls `_string.sub(arg, 1, 1)`; the returned character is not used by
   the remaining instructions (`command`, `0x0000F3-0x000107`).
2. Calls `require("/Widget/" .. arg)` (`0x00010B-0x00011B`).
3. Calls `_createActor(nil, _string.gsub(arg, ".+/", ""), false, ...)`,
   forwarding the original varargs (`0x00011F-0x000147`).
4. Returns true (`0x00014B-0x00014F`).

The recovered Lua text at `command/system/widgetopencommand.lua:3-6`
prints only the `require` and true return. It omits the `_createActor`
call, so it is insufficient as a complete command contract. The bytecode
contains no argument allowlist or path check between the concatenated
`require` and actor creation. This says nothing about earlier command
dispatch gates, the behavior of the native actor factory, or which widget
arguments a historical server actually sent. A widget class file's
presence is not evidence that retail command 24228 opened it.

The installed LPB is
`client/script/7vxx9w6/rlrq5x/n1635qvu5w7vxx9w6.le.lpb`, SHA256
`F55ABE4E1388DBFB86BDD14AD27522855D8451AB014EAE1D0334C0B1018F5312`.
It decoded byte-for-byte to the recovered LUAC, SHA256
`CC1E3A7DD71DF83168BBDFE739DF7B71845C4FBC6D01CDBD04270D6C9577F3A4`.
The recovered-source identity is
`manifests/scripts.json:7652-7657`, SHA256
`15589DC895FF29F148B0A5BA4B74B564537F422B170A67142B3826C7C762022C`.
