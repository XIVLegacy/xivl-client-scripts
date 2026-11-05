# WidgetOpenCommand client boundary

The static-actor registry maps low ID 24228 to
`/Command/System/WidgetOpenCommand`
(`xivl-client-data:manifests/staticactor_class_paths.json:3213-3216`).
The corresponding client command accepts a widget-path argument and
varargs. Its bytecode performs these operations in order:

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

The LPB is
`client/script/7vxx9w6/rlrq5x/n1635qvu5w7vxx9w6.le.lpb`, SHA256
`F55ABE4E1388DBFB86BDD14AD27522855D8451AB014EAE1D0334C0B1018F5312`.
It decoded byte-for-byte to the recovered LUAC, SHA256
`CC1E3A7DD71DF83168BBDFE739DF7B71845C4FBC6D01CDBD04270D6C9577F3A4`.
The recovered-source identity is
`manifests/scripts.json:7652-7657`, SHA256
`15589DC895FF29F148B0A5BA4B74B564537F422B170A67142B3826C7C762022C`.

## RetainerNamingWidget ask result

The resource
`n1635q/9rz/s5q91w5sw9x1w3n1635q.le.lpb` (5,205 bytes, SHA-256
`e3fe5db48c6eb5921681a0c86180e38bac19230157fce70711bd091b186bbf53`)
has a 5,192-byte XOR-0x73 payload with SHA-256
`53546cd0d0702e27ed30fd3c27b2faf92f87b4ed9b011d8b9d3813eb676d1dc3`.
The payload decompiles with the pinned unluac JAR to the canonical
`lua/scripts/widget/ask/retainernamingwidget.lua`: 13,017 bytes, 578 lines,
SHA-256 `1c7483e0e54a93e8bc60c5e4a44158e31cf497983c927797015b7bc1308833c2`,
matching `manifests/scripts.json`.

In that chunk, `processUICommandClose` calls `setBaseAskResult(-3)` and sets
`work.askAnswer` to `-3` (lines 229-239). `processUICommandCancel` does the
same when its control is `Button_Cancel` (lines 242-259); the operation
handler has the same cancel branch (lines 262-297). `getAskResult` returns
numeric `-3` when `work.askAnswer == -3`; otherwise it returns the name data
when present or nil (lines 481-499). These are widget-level client
semantics. They do not prove that command 24228 historically opened this
widget or identify a subsequent caller or server effect.

## Command formal frame and factory tail

The authenticated canonical member
`lua/scripts/command/system/widgetopencommand.lua` declares this function at
line 11, ends it at line 37 and binds `command` at line 39
([script identity](../manifests/scripts.json#L7653)). In the original resource
pinned above, root CLOSURE/SETTABLE PCs 8/9 bind `root/proto0` to
`WidgetOpenCommand.command`. That prototype starts at `0xF3`, contains 25
instructions (PCs 0-24), and declares three fixed parameters with raw Lua 5.1
vararg flag 3. These canonical line locators are separate from its original
debug-line range 67-76. PCs here are zero-based.

Let the incoming Lua frame be `(C, P, S, V1, ..., Vn)`. These symbols name
positions, without assigning command, player or owner roles. `C`, `P` and `S`
are the three fixed slots. Missing fixed slots are nil-filled; only arguments
after the third fixed slot belong to the variadic sequence. The path is `S`:
MOVEs at PCs 2, 8 and 15 copy fixed register 2 into the arguments for
`_string.sub`, the `require` concatenation and `_string.gsub`, respectively.
Their CALLs are PCs 5, 10 and 18. Neither `C` nor `P` is read anywhere in this
prototype, and neither is inserted into the factory arguments.

If the preceding calls return normally, the factory request has exactly
`(nil, G, false, V1, ..., Vn)`, where `G` is the first result of the selected
`_string.gsub(S, ".+/", "")` call. Its CALL at PC 18 (`0x13B`) has B=4,C=2,
so any additional results are discarded. `_createActor` is looked up and
saved at PC 11 (`0x11F`) before `_string` and its `gsub` field are read at
PCs 13/14. That `_string` read is fresh after `require`, separate from the
earlier `sub` lookup. The factory request uses the saved factory value and
the selected `gsub` result, without another lookup of either.

VARARG PC 20 (`0x143`), A=9,B=0, expands the entire variadic sequence after
the three factory prefix values. Factory CALL PC 21 (`0x147`), B=0,C=2,
consumes that open argument range and retains one result. An empty tail adds
no argument. Explicit nil values, including trailing nils, remain arguments;
false, zero and other supplied values are forwarded without a local filter
or conversion. The retained factory result is unused, consistent with the
true return described above.

This establishes the local formal-to-factory mapping only. It does not
identify an actual command object or receiver, prove a tutorial widget alias
was supplied, establish a historical native dispatch frame, or turn the
factory request into an observed widget initialization callback. Those joins
require the actual native method selection, receiver and delivered typed
argument sequence.
