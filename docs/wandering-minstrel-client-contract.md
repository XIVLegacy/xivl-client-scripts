# Wandering Minstrel client contracts

`PopulaceBountyPresenter` retains five event presentations and its
`initForEvent` method in the 1.23b extraction. The events issue dialogue,
scheduler, turn and fade calls, then return no values. Their only local
conditional is `eventJail` comparing its supplied A2 with literal Boolean
true. These methods do not select each other or locally test level, item
ownership, reward eligibility or duty admission.

The data identity and static text meanings are owned by
`xivl-client-data:docs/wandering-minstrel-text-rows.md`. A presentation named
before/after a gift does not establish a server grant or the order in which
the methods were historically invoked.

## Input identity and method

The game version is 1.23b, extraction `2012.09.19.0001`. The canonical source
member matched [scripts.json](../manifests/scripts.json), the containing
archive matched [private_lua_corpus.json](../manifests/private_lua_corpus.json),
and the installed LPB and decoded payload matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).

| Input | Path or representation | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical source | `lua/scripts/chara/npc/populace/populacebountypresenter.lua` | 11029 | `ED43F1A71B3B3D8E52E63DE889E1E338E6C010EEF4770C097DFAD3766AC8E522` |
| Retail LPB | `client/script/729s9/wu7/uvupy975/uvupy9758vpwqlus5r5wq5s.le.lpb` | 3646 | `42CC1B202FA4B4D78D23777C09E5E91789F441F930A90D0CA2D60BEB0F3811C4` |
| Decoded Lua 5.1 | XOR-0x73 payload of that LPB | 3633 | `5857DD00E850242A3F0C6E6E04C459F9110CA334463F156F537971A47FB5AE31` |

The canonical source has 560 lines. The directly reached helper members below
were also authenticated against their exact source, resource and payload
manifest entries. Paths are relative to `lua/scripts/`.

| Helper member | Bytes | Canonical source SHA-256 |
| --- | ---: | --- |
| `chara/npc/npcbaseclass.lua` | 12116 | `F18C6C3198DB0402431CA6AA683B601AFBF5A0DC5C22481B3C1DA1DEABEF0DC2` |
| `chara/npc/npcbaseclass_event.lua` | 20675 | `5417B1BDF762162CAD240A84715D0FC85958DBE0181B653348A66C02EE4D7C80` |
| `world/worldmaster_event.lua` | 7559 | `744487A7CAAA94E1C4D2056CC07686A894C6BA336BBD021BBFFEEBCEEF2AD099` |
| `widget/desktopwidget.lua` | 7929 | `5D3BFABF2E8A55EE2E64F607BDADA5F04046C9528E9E9ACA858E9AD9E232070A` |

`tools/retail_script.py` supplied LPB decoding; the fixed Lua 5.1 reader and
instruction decoder in `tools/build_quest_contracts.py` checked complete
presenter instruction coverage, closure bindings and selected helper calls.
This authenticates selected inputs without claiming a new full-corpus check.
No script body or generated product was changed.

PCs below are one-based within the named prototype, child indices are
zero-based, and offsets are bytes in the decoded payload, excluding the LPB
wrapper. Source locators use canonical decompile lines rather than original
debug-line numbers.

## Entry methods and text operands

A0 denotes the supplied method receiver; A1 and A2 remain supplied values.
None of these methods is variadic. Every presenter `CALL` discards results,
and each final `RETURN B=1` returns zero values. A1 is passed to the turn
helper and used as a scheduler/fade receiver where specified; its actual
runtime identity is not established by that role.

| Method / source assignment line | Child | Formal values | Root assignment PC / offset | Final return PC / offset |
| --- | --- | --- | --- | --- |
| `initForEvent`:24 | 0 | A0 | 10 / `0x44` | 8 / `0x1A9` |
| `eventAlreadyPresent`:75 | 1 | A0,A1 | 13 / `0x50` | 35 / `0x2B3` |
| `eventLowerLevel`:160 | 2 | A0,A1 | 16 / `0x5C` | 62 / `0x48A` |
| `eventBeforePresent`:314 | 3 | A0,A1 | 19 / `0x68` | 116 / `0x76E` |
| `eventAfterPresent`:350 | 4 | A0,A1; A1 unused | 22 / `0x74` | 24 / `0x91A` |
| `eventJail`:560 | 5 | A0,A1,A2 | 25 / `0x80` | 162 / `0xC67` |

Each root assignment follows the actual corresponding `CLOSURE`; methods were
not identified from adjacent child numbers alone. `initForEvent` requests
`_loadTextDataPermanently(A0,8016,"populaceBountyPresenter")` at child 0
PC4, offset `0x199`, then `_setGroundOn(A0,false)` at PC7, `0x1A5`.
The intended bank/name association does not prove successful native loading
or the later invocation's receiver and lifetime.

Define N(row) as the exact call tuple `(A0,A0,row,0)` to inherited NPC `say`,
including its receiver. Define M(row) as `(worldMaster,A0,row)` to
`WorldMaster.say`. The second A0 in N and explicit A0 in M remain the same
supplied presenter object. Both calls have an empty variadic formatter tail;
the NPC helper's zero argument is its fixed A3 selector, not a formatter value.

| Method | Ordered dialogue calls | Selected original locators |
| --- | --- | --- |
| Already | N(19), N(20) | Child 1 PCs18/29, offsets `0x26F`/`0x29B`; source51/65. |
| Lower | N(2), N(3), N(4), N(5), then M(6) after the last stage wait | Child 2 PCs18/29/40/51/59; source102/116/130/144/154. |
| Before | N(7) through N(15), in that order | Child 3 PCs18/29/40/51/62/73/84/95/106; source187-299. |
| After | N(16), then M(17), M(18) after its stage wait | Child 4 PCs8/16/21, offsets `0x8DA`/`0x8FA`/`0x90E`; source328/338/344. |
| Jail | N(21) if A2 is exactly true, otherwise N(22); then N(23),N(35),N(24),N(25),N(26),N(27),N(28),N(29),N(30),N(36),N(31),N(32),N(33),N(34) | Child 5 PCs14/20/25/30/41/52/57/68/79/90/101/106/117/128/142/159; source370-554. |

The used row-key union is exactly 2 through 36. Keys 35/36 are intentionally
interleaved; numerical order is not execution order.

Jail's sole comparison, child 5 PC8 at `0x9FF`, is `EQ A=0` between register
2 and Boolean true. The unequal path jumps at PC9 to the row-22 block; exact
true reaches row 21 and then jumps over row 22. False, nil, numbers 0/1,
strings and tables are not Boolean true. Both paths then share all remaining
calls and the same zero-value return. A2's producer and gameplay meaning are
unestablished; the friend/generic greeting text does not identify that flag.

## Scheduler, turn and fade sequence

In this table, S means `startCliantTalkTurn(A0,2,A1)`, F means
`finishCliantTalkTurn(A0)`, R(n) means `_runCharaScheduler(A0,n)` and W(n)
means `_waitForCharaSchedulerFinished(A0,n)`. Stage(n; rows) means R(n), the
listed N calls in order, then W(n). These are observed call operands, not
inferred animation names, time units or proof of completed presentation.

| Method | Ordered calls |
| --- | --- |
| Already | S; R(69750784); W(69750784); Stage(354086912;19); Stage(83955712;20); F. |
| Lower | S; R(69750784); W(69750784); Stage(354054144;2); Stage(69197824;3); Stage(83988480;4); Stage(354000896;5); M(6); F. |
| Before | S; R(69750784); W(69750784); Stage(354054144;7); Stage(69197824;8); Stage(83980288;9); Stage(354082816;10); Stage(354086912;11); Stage(83984384;12); Stage(354000896;13); Stage(84058112;14); Stage(83906560;15); R(354107392); W(354107392). |
| After | Stage(69197824;16); M(17); M(18); F. |
| Jail opening | S; R(69750784); N(21 or22); N(23); N(35); W(69750784). |
| Jail middle | Stage(354054144;24); Stage(69197824;25,26); Stage(83980288;27); Stage(354082816;28); Stage(354086912;29); Stage(83984384;30,36); Stage(354000896;31). |
| Jail ending | R(84058112); N(32); `_runCharaScheduler(A1,67112954)`; W(84058112); R(83906560); N(33); `_runCharaScheduler(A1,67112955)`; `_wait(A0,1)`; `_fadeOut(A1,2)`; `_wait(A0,2)`; N(34); `_fadeInAfterWarp(A1)`. |

Before contains no F; After contains no S. Neither method locally invokes the
other or a reward operation. Jail contains no F and no
W(83906560), and does not wait on either A1 scheduler. Its ending is child 5
PCs123-161, offsets `0xBCB`-`0xC63` (source508-557). The final fade method's
name does not establish a warp command, selected destination or arrival.

## Inherited message path

For the presenter's fixed A3 zero, `NpcBaseClass_event.say` first requests
`_runCharaScheduler(A0,403087360)`. It then forwards
`(desktopWidget,A0,38,A1,A2,...)` to `showMessage`. The selected provider A1
and row A2 are the presenter's explicit A0 and row. Thus each N call adds
this helper-level scheduler request before its desktop message call, without
a helper-level scheduler wait. The stage scheduler values above remain
separate operands.

The helper is child 8, assigned at root PC27, with source247-312. Selected
PC1 at `0x978` tests the fixed selector, PC5 at `0x988` requests the scheduler,
and PCs69/70 at the message tail use `VARARG B=0` and `CALL B=0 C=1`.
The message call is at `0xA8C`; PC71 returns no values.

`WorldMaster_event.say`, source111-124, child 4, instead forwards
`(desktopWidget,worldMaster,40,A0,row)` for these calls, without the NPC say
helper's scheduler request. Its root assignment is PC15; PCs7-9 preserve
the open variadic tail, discard results and return no values. The selected
call is at `0x4CB`. `DesktopWidget.showMessage`, source369-384, child 14,
forwards the same arguments to `_appendMessagePool`, preserving the variadic
tail. Its root assignment is PC57 and its selected call is at `0xF0C`.
The generic argument route is documented in
[WorldMaster message arguments](worldmaster-message-arguments.md).

The separate native evidence is owned by
`xivl-decomp:docs/script/worldmaster-message-pool.md`, registered callback
and call arguments, and `xivl-decomp:docs/script/actor-base-text-source.md`.
The native shared worker's index 2 after the desktop receiver is removed
holds the supplied Actor-compatible text provider; index 3 holds the row,
and subsequent values form the formatter tail. Under the published successful
source-initialization conditions, the WorldMaster sink therefore retains the
presenter source for rows 6/17/18. Merely using `WorldMaster.say` does not
replace it with the worldMaster text bank.

Those native contracts and `xivl-client-structs:docs/talk-native-contract.md`
record a yield request and message resume checker. Discarded Lua results and
zero-value returns do not imply no wait, dismissal or rendering. Actual
initialization, locale/field choice, receiver identity and completion remain
conditions. No new native executable body was traced for this finding.

The selected S helper uses mode 2, the supplied A1 position and A0's
orientation to issue look-at requests; F calls `_turnBack(A0)` and
`_cancelLookAt(A0)`. Their names and operands do not authenticate A1's runtime
type, historical eligibility or native animation/turn completion.

## Reproduction and limits

Authenticate the selected canonical members, installed LPBs and decoded
payloads before analysis. Use `tools/retail_script.py` decoding and the
fixed Lua reader/instruction decoder in `tools/build_quest_contracts.py`.
Bind the actual root `CLOSURE` to each method's `SETTABLE`, then check all
presenter callsites and return operands, the sole conditional and selected
helper vararg forwarding. The header is the fixed little-endian Lua 5.1
format `1B4C75615100010404040800`. A pinned unluac disassembly can independently
check the instruction sequence as described in
[Notice helper reproduction](notice-helper-contract.md#reproduction).
Keep source bodies, payloads and listings outside the tracked tree.

The six methods contain no local level/ownership lookup, item grant, duty
admission, ask/choice operation or callback installation. This is a finite
statement about the authenticated presenter prototypes, not every native
callee or the historical server. The method names and horn instructions do
not prove a selected reward transaction. The retained Goobbue announcement's
1.23a cutoff and the data extraction's later resident strings remain distinct
in `xivl-client-data:docs/wandering-minstrel-text-rows.md`.

Stronger gameplay claims need a preserved attributable dispatcher/invocation
joining a method to its A1/A2 values, followed by the required eligibility,
ownership, reward-persistence or duty-admission evidence. Scheduler/wait/fade
native effects, actual text/resource selection and accepted presentation
remain outside this static contract.
