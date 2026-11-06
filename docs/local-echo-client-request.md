# Parsed-key 107 echo request

`DesktopWidget.executeTextCommandLocal` routes numeric key 107 through
`convertPronouns` and then `echoText`. It passes the conversion's complete
return tail into the saved echo method and returns one echo result. The
selected static text-command row contains literal `/echo`. Actual slash
parser acceptance, helper behavior and displayed output remain separate
boundaries.

## Incoming values and guards

The method has ten fixed parameters and no variadic tail. In canonical source
notation, `D = A0_2` is the receiver, `K = A1_2` is the selector,
`P = A4_2` supplies indexed input, and `B = A8_2` participates in a common
guard. The selected path uses no other incoming formal. Omitted fixed
positions are nil, and extra actual arguments are discarded by this
nonvariadic function.

For numeric `K = 107`, the common prefix behaves as follows, assuming each
required lookup and call completes normally:

1. It reads `D.work.tutorialFlag`. Exact Boolean true returns the single
   value false before the selected requests. Other truthy values, such as
   numeric 1, do not satisfy this equality.
2. It freshly reads `D.work.lockUserControl`. Exact true skips the later
   subtarget query. Otherwise, exact `B == true` also skips that query.
   If neither condition holds, it calls the freshly obtained
   `D.isSubTargetSelectMode` with only `D` and retains one result. Only an
   exact true result selects the common blocked-state test.
3. In that blocked-state test, key 107 is an exemption. The comparison at
   PC64 takes the continuation to PC88, rather than the refusal body. A
   false blocked state reaches the same continuation. Thus the lock and
   subtarget conditions do not themselves reject this selected key.
4. It reads global `worldMaster` once, obtains `_getMyPlayer` from that
   value, calls it with that same value as receiver and retains one result.
   The selected clause does not use that result. Later dispatch comparisons
   reach the numeric key-107 comparison at PC284.

These are equality tests against numeric 107 and Boolean true, without
string or number coercion. The required `work` and `P` index operations are
not type checks. In particular, a nil `P` is not an accepted empty-input
representation. The named methods and the global remain dynamic bindings.

## Selected request and local result

The clause first reads `P[1]` and compares it with nil. A nil entry makes no
conversion or echo request and reaches the shared return with false. The
common `_getMyPlayer` call has already occurred. An empty string, false or
numeric zero is non-nil and takes the request path. This local distinction
does not establish that a helper accepts those values.

For a non-nil first read, the original instructions establish this order:

| Step | Lookup, call or continuation |
| --- | --- |
| 1 | Capture `D.echoText` and its receiver `D`. |
| 2 | Obtain `D.convertPronouns` with receiver `D`. |
| 3 | Freshly read `P[1]` again. The earlier tested value is not saved for this call. |
| 4 | Call the conversion with exactly `D` and that fresh value. Request all results. |
| 5 | Call the previously captured echo method with `D`, followed by the complete conversion result tail. Retain exactly one result. |
| 6 | Jump to the shared one-value return and return that result unchanged. |

The conversion call has fixed input width and open result width. The echo
call has open input width and fixed one-result width. A conversion returning
no values gives the echo method only its receiver. Returned nils retain their
positions. An echo method returning no values supplies nil to the fixed
one-result destination. False, nil and non-Boolean results are not normalized
to success or failure by this clause. A changed second indexed read can even
supply nil after the first read passed the guard.

The first conditional opaque call in the common prefix is
`isSubTargetSelectMode`; `_getMyPlayer` is another prerequisite call. The
selected clause's opaque edges are `convertPronouns` and the captured
`echoText`. Their bodies, result meanings and actual bindings are not
established here. Normal completion is required for the later call and local
return described above.

## Static spelling and log boundary

At `xivl-client-data:csv/xtx__textCommand.csv`, row key 107 has exact `/echo`
in zero-based physical CSV field indexes 6, 7, 10, 13 and 19. Their declared
headers are respectively `5`, `6`, `9`, `12` and `18`, each with type `str`.
The key occupies index 0. Only those selected cells and the two header
records support this association. These positions do not identify a locale
or establish which native parser recognizes the spelling. The
[standard-emote contract](standard-emote-command-contract.md#menu-and-typed-callers)
owns the analogous distinction between a static spelling, parsed key and
actual submitted line.

This path supplies no established pool-producer frame or SendLog record.
Its helper names alone do not identify a source, category, text owner, row
selector or parameter vector. The existing native publications remain
separate:

- `xivl-decomp:docs/resource/logcontrol-pool-feed.md`, Native arguments and
  record, distinguishes a pool source from its text owner and row selector.
- `xivl-decomp:docs/script/logcontrol-player-producer.md`, Player call frames,
  establishes specific player pool calls with their own operands.
- `xivl-decomp:docs/script/sendlog-sink-chain.md`, SL-07, describes network
  SendLog families and their sink selection.
- `xivl-decomp:docs/resource/logcontrol-text-lookup.md`, Sheet, row and column,
  requires the actual owner key, registered provider, row and configured
  default column.

Those publications at revision `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`
do not bridge the opaque helpers in this finding. No local-only transport,
log channel/category meaning, queued or published text, scheduling, rendered
line, server acceptance or historical behavior follows from the selected
static request.

## Source identity and reproduction

The extraction is `2012.09.19.0001`. Canonical source identities are in
[`scripts.json`](../manifests/scripts.json), original resources and decoded
payload identities in
[`retail_lua_coverage.json`](../manifests/retail_lua_coverage.json), and the
retained source archive declaration in
[`private_lua_corpus.json`](../manifests/private_lua_corpus.json).

| Input | Bytes | SHA-256 |
| --- | --- | --- |
| Canonical `lua/scripts/widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| Original `n1635q/65rzqvun1635q_7vww57qvs.le.lpb` | 213487 | `0f8ca1585bb97c40d36cbf120dd3f6fa6351927c4530e3fad76a71582af95425` |
| Decoded connector payload | 213474 | `685a0a6dda2d4ae6fe06a9c684e57efd7e819938e145cb1a4a65df56555bd621` |
| Retained Lua archive | 14385427 | `0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31` |
| Retained CSV archive | 70110686 | `006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0` |
| `xtx__textCommand.csv` | 12989 | `1c67abe0af10f211761a2211d928a5a49bf5a5d02445797be6fd5729fd911660` |

The Lua archive declaration records source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`. Data's declarations are
`xivl-client-data:manifests/private_csv_corpus.json` and
`xivl-client-data:manifests/tables.json`, selected table
`xtx__textCommand.csv`, at revision
`57bf830e55dfafc27feaa9a8736987d0528cd55c`. Its archive source revision is
`8b38a02ce8ebf662b931092e46273251b38c58f0`.

The original method is `root/proto463`, code offset 172394, in a 2147-word
prototype envelope. Root PCs1597-1600 load `DesktopWidget`, load the method
name into a register, create the closure and assign it using that register
key. The binding is not a constant-key `SETTABLE` assumption. Canonical
method source spans lines20182-22503; the selected clause is at20455-20464.
PCs and decoded-payload offsets are zero-based:

| Purpose | PCs | Decoded offsets |
| --- | --- | --- |
| Tutorial guard and selected early return | 0-25, selected comparisons only | 172394-172494 |
| Common lock, override and subtarget dependencies | 27-40 | 172502-172554 |
| Key-107 blocked-state exemption | 64-66 | 172650-172658 |
| Global/receiver getter and dispatch setup | 88-94 | 172746-172770 |
| Dispatch dependencies, with other bodies skipped | 105-106, 114-115, 123-124, 139-140, 148-149, 157-158 | 172814-173026, selected pairs only |
| Selected key comparison and clause | 284-296 | 173530-173578 |
| Shared one-value return | 2145 | 180974 |

PC64 and PC284 are two different references to literal 107. The jump after
PC64 targets PC67 when taken; equality for the selected key skips it and
uses PC66 to reach PC88. The jump after PC284 targets PC297 for a
nonmatching selector. These control dependencies do not admit either
refusal body or another command clause.

`tools/retail_script.py` decodes the authenticated LPB in memory.
`ChunkReader` and `instruction` in `tools/build_quest_contracts.py` expose
the original header, binding, guards and CALL widths. Selected canonical
operands agree with those instructions. A bounded original-instruction
check exercised 236 synthetic cases for exact Boolean guards, non-nil input,
fresh reads, empty and nil-bearing result tails, receiver identity and fixed
result adjustment. Ten changed guard, selector, receiver, entry-read and
call-width controls were rejected. These checks establish static source
agreement, without executing the retail client or any helper body.
