# CutScene initialization callback branches

The retained `CutScene._onInitializationClip` Lua body acts only when its
first data argument equals `Personage`. A first string `PreviewSetupClip`
takes the direct zero-result return without reading the remaining arguments,
work fields or helper functions. This is a conditional fact about the selected
Lua definition, separate from native setup effects and actual callback binding.

## Source and selected method

The source is retail 1.23b extraction `2012.09.19.0001`, resource
`39x569q9/7pqr75w5_7vxxvw.le.lpb`, 9,125 bytes, SHA-256
`A5279136C0EE8F6EF2342FD22AF2B9CD12F9B6AFF5A4FEFF4BC0FC21367F5321`.
Its decoded Lua 5.1 chunk is 9,112 bytes, SHA-256
`7EF33408C579F2D1EDE120D9751851BD39B77DD1B6CA6A0AA821B413FE11B4FD`.
Canonical LF `gamedata/cutscene_common.lua` is 46,939 bytes, 1,316 lines,
SHA-256
`F6DB9559B3F805D2738C073C7DB9DD102FD5C33A056E789FF2FB2F8AFF395BD1`.
The identities are pinned in `manifests/scripts.json:9519-9522` and
`manifests/retail_lua_coverage.json:814-827`.

`tools/retail_script.py` decoded the resource and invoked the pinned
`tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
`ChunkReader` and `instruction` from `tools/build_quest_contracts.py`
recovered the selected original operands. Offsets below are decimal decoded
chunk bytes, and PCs are zero-based within the named prototype.

Root PC 0, byte 32, gets global `CutScene`. PC 1, byte 36, forms child
prototype 0, and PC 2, byte 40, attempts `SETTABLE` with that closure, the
resolved target and key `_onInitializationClip`. A `__newindex` handler can
redirect or discard that write; installation requires the assignment's actual
semantics and persistence.
The source inspection covered that installation and `root/proto0` only.
The selected prototype has two fixed parameters, a vararg tail, 22
instructions and code start byte 381. Its LF-decompile window is lines 4-30;
the original chunk's line-defined metadata is 66-112. The receiver/method
window is also indexed at
`xivl-client-structs:manifests/lua_api_contract.json:38456-38477`.
Root assignment alone does not establish the later table contents or selected
callback function.

## First argument and direct return

The formal inputs are `(self, kind, ...)`. PC 0, byte 381, compares kind
with literal `Personage` using `EQ A=0`. A false comparison executes the
JMP at PC 1, byte 385, whose destination is PC 21, byte 465.
That instruction is `RETURN B=1`, returning zero values.

For the actual string `PreviewSetupClip`, the body path is therefore
`0 -> 1 -> 21`. It does not execute `VARARG`, call a function, or read self
or its work fields on that path. The same direct path applies whenever the
comparison is false. These are body instructions, not a claim that native
event handling, function entry or the enclosing request had no other effects.

## Personage path

An equal comparison skips PC 1 and reaches PC 2, which resolves global
`select`. PC 4, byte 397, is `VARARG A=5,B=0`; PC 5, byte 401, calls the
resolved value with `B=0,C=2`. Its explicit arguments are literal 1 followed
by the complete vararg tail, and it keeps exactly one result T. There is no seven-value
tail limit implied by a decompiler's temporary variable list. If that global
is standard `select`, T is the first vararg; the source itself uses the
actually resolved value and result. The CALL operands describe explicit
arguments: callable-object dispatch through `__call` inserts the callable
object before them. A noncallable resolution does not return normally. The
same qualification applies to the helper call below.

The body computes `#T` once, initializes a numeric loop from 1 with step 1,
and indexes T at each selected i. `FORPREP` at PC 9, byte 417, reaches
the `FORLOOP` at PC 20, byte 461; its body target is PC 10, byte 421.
T must support the length operation; index and comparison support is needed
only for iterations actually entered. An empty loop performs no index read.
The method supplies
no separate validation or error conversion for those operations.

At PC 11, byte 425, a true `T[i] <= 19999` comparison skips the helper
path. A false comparison reaches PC 14. That path freshly obtains
`self.work.actorclassSheet`, resolves its `_loadKeySemipermanently` member,
and separately reads T[i] twice. PC 19, byte 457, calls that member with
`B=4,C=1`: the resolved sheet value and the two freshly read values as explicit
arguments, with zero
requested results. A stable ordinary list and unchanged lookup inputs make
those two values equal to the tested entry; the bytecode alone does not
guarantee that equality across index/member effects or aliases.

The helper's name and the field name do not establish successful key loading,
sheet identity, resource readiness or any visible actor effect. Helper calls,
member/index effects and their normal return remain conditions. The loop's
only normal exit reaches PC 21 and returns zero values; it does not forward
helper results to the callback caller.

## Conditional preview composition

The selected native producer and argument path are owned by
`xivl-decomp:docs/resource/cut-preview-event-consumer.md`. That source
distinguishes the first string-argument source `PreviewSetupClip` from the
lookup-name source `_onInitializationClip`, with explicit constructor-return,
string-preservation, key/type/control and request conditions.

If the actual callback invocation selects this retained Lua prototype and
passes the corresponding frame prefix `(self,"PreviewSetupClip",ownerString)`,
the direct-return branch above does not inspect or dispatch on ownerString.
It does not call a Lua function selected by `PreviewSetupClip` from this body.
This does not determine which Lua class or method the native request actually
selected. It also does not undo or classify the native string assignment that
precedes that request.

The actual event binding, class/table persistence, later native use of the
owner string, clip lifetime, scene playback, completion, text-sheet selection
and authoritative quest-state changes remain separate evidence questions.
