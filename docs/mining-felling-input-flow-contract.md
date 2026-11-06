# Mining and Felling input workflow

`HarvestJudge` selects Mining for numeric command 22002 and Felling for
numeric command 22003. Its ask returns exactly `command,input,status`.
The input is a phase-dependent widget result, while status is the desktop
selection result. Neither value establishes an authoritative gathering outcome.

This contract checks the four original Judge methods' land branches and
shared argument/result handling. The complete [Mining widget](mining-input-widget-contract.md)
and [Felling widget](felling-input-widget-contract.md) contracts own their local
controls and getters. The [Fishing workflow](fishing-input-flow-contract.md)
owns command 22004 and the shared desktop wrappers. The
[gathering overview](gathering-marker-fishing-ui.md) owns markers and text.

## Actor, command and argument selection

Write the fixed Judge arguments as shown below. `self` is the Judge receiver,
A1 is the actor queried by `isPlayer`, and A2 is unused. Only an exactly-true
first `isPlayer(A1)` result reaches a desktop request. Nil, false, numeric
zero and numeric one do not satisfy that test. Access or call errors remain
errors, rather than a false return.

Let `path` be `Ask/MiningInputWidget` for command 22002 and
`Ask/FellingInputWidget` for command 22003. Each selected branch has one
`GETGLOBAL desktopWidget` followed by `SELF`, which captures that value for
both the method lookup and explicit receiver D. No later global read replaces
that receiver before the call, including if the lookup changes the global
binding. Separate Judge calls do not retain or authenticate one shared
desktop, actor or widget identity.

| Judge method | Command operand | Selected actual desktop call | Normal local return |
| --- | --- | --- | --- |
| `openInputWidget(self,A1,A2,A3,A4)` | A3 | `openEventModeWidgetYield(D,path,A4)` | Exactly one first helper result. |
| `orderInputWidget(self,A1,A2,A3,A4,A5)` | A5 | `updateEventModeWidget(D,path,A3,A4)` | Exactly one first helper result. |
| `askInputWidget(self,A1,A2,A3,A4,A5,A6,A7,A8,A9)` | A3 | `selectEventModeWidgetYield(D,path,primary,nil,extra,quit,nil,A4,nil,A9)` | Exactly `command,input,status`, adjusted below. |
| `closeInputWidget(self,A1,A2,A3)` | A3 | `closeEventModeWidget(D,path)` | Exactly one first helper result. |

The numeric command comparisons do not coerce string `"22002"` or
`"22003"`. A non-true player result or a command selecting none of the three
published gathering paths makes no desktop call. The open/order/close default
is one false; the ask default becomes `(0,0,false)`. Command 22004 has its
separate published Fishing branch and is not an unsupported-command case.

Open/order/close request one helper result, nil-padding zero results and
discarding extras. Their local false checks preserve that first value:
normally returned nil or numeric zero is not replaced with false. The pinned
desktop wrappers have their own Boolean contracts, described below.

The ask computes its local command choices before the player query:

| Land command | A4 equals numeric 1: primary | Every other A4: primary | quit |
| --- | ---: | ---: | ---: |
| 22002, Mining | 22701 | 22703 | 22702 |
| 22003, Felling | 22704 | 22705 | 22706 |

The secondary command is always nil. `extra` is nil exactly when A5 equals
numeric zero, otherwise it is 22710. Nil, false and string `"0"` A5 therefore
select 22710. The eight positions after `path` remain
`(primary,nil,extra,quit,nil,A4,nil,A9)`, including every nil position.
A4 and A9 are forwarded unchanged. A6, A7 and A8 have no land-branch argument
role. An omitted fixed argument is nil on entry, so omitted A4 selects the
non-1 primary and is still forwarded as nil.

The tail maps to five command slots, phase, an unused land-widget parameter,
and rare-effect control. Exact A4=1 selects the slider command; any other A4
selects the gauge command at the Judge. This does not normalize the phase:
only numeric 1 or 2 selects a child widget's corresponding setup branch.
An unrecognized phase operand makes neither phase assignment in the pinned
child. The child's later getter reads its then-current stored phase afresh.
Within either selected phase branch, A9 selects an effect start request only
when exactly true, a stop request when nonnil and not true, and no such request
when nil, under those child bindings. These local commands do not establish
a gathering formula.

## Selection result and the two input values

The selected desktop wrapper's initialization, show and wait behavior is
owned by [the Fishing wrapper contract](fishing-input-flow-contract.md#phase-setup-and-input-completion)
and its [wait/result section](fishing-input-flow-contract.md#wait-result-width-and-cleanup).
For the selected land path, initialization requests `getWidget(D,4,path)`.
For a nonnil first result W it requests reset, the complete parameter tail
and `show(W,true,true)` in order. Its `setAskParameter` result is discarded,
including a local false result. A normally completed nonnil initialization
continues to selection. Actual creation, method resolution and applied
storage remain conditions of the composition.

The pinned selection wrapper returns one false for a nil widget or an
exactly-false first wait result. Otherwise it returns literal true followed
by the complete open `getAskResult(W)` sequence. The
[Ask completion contract](ask-widget-result-state.md) distinguishes its
inherited completion poll from acceptance.

| Boundary | Result behavior |
| --- | --- |
| Mining getter, fresh stored phase=1 | Chosen command followed by the open slider `Value` getter results. |
| Mining getter, every other stored phase | Exactly chosen command and current power. |
| Felling getter, fresh stored phase=1 | Chosen command followed by the open slider `Value` getter results. |
| Felling getter, every other stored phase | Exactly chosen command and current angle. |
| Judge's selection CALL | Requests exactly three results as `status,command,input`. Missing results become nil and extras are discarded. |
| Judge's exact-false status branch | Replaces command and input with numeric zero, retaining false status. |
| Judge's normal final return | Exactly `command,input,status`. No conversion, range clamp or substitution between input samples occurs here. |

Consequently the pinned wrapper's normal failure becomes `(0,0,false)`.
With true status, a getter producing only the chosen command gives nil input;
extra slider results are truncated at the Judge's three-slot request. The
child's zero getter results and one nil getter result have different widths,
even though this Judge can adjust both to the same nil input. A substituted
wrapper returning nil, numeric zero or numeric one status would preserve its
adjusted command and input. The test is exact false, not Lua truthiness.

For a Mining phase-one ask, call the returned input A. For a later phase-two
ask, call it B. Under the pinned getter and actual stored phases, A is the
selected slider result and B is current power. Each ask obtains a new result;
the Judge neither saves A for the later ask nor replaces B with A. Felling
has the analogous slider/current-angle distinction. Which value an external
consumer forwards, and which value an authoritative gathering rule should
use, are separate questions. This contract establishes neither policy.

## Open, update and explicit close

The adopted open wrapper supplies
`openWidgetYield(D,4,path,nil,nil,false,A4)`. It returns false for a nil first
open result and true for any nonnil first result. Under the published
initialization route, A4 becomes the first `initAsk` data argument, used for
optional grade text by the land widgets. This A4 belongs to the open method;
the ask method's A4 is its separate phase operand.

The update wrapper performs a fresh category-4 lookup and forwards the order
method's A3/A4 to `updateAskParameter(W,A3,A4)`. The land widgets request
`updateHP(A3)` and, only for exact true A4, `displayEffect()`. The update
result is discarded. The wrapper returns false for a nil lookup and true
after a normal nonnil-widget update, including a normally returned HP refusal.
It does not prove the requested assignment or control update was applied.

Neither ask selection nor the child Cancel navigation closes the widget.
The linked child contracts distinguish Cancel focus changes, quit-command
completion and gauge completion. The explicit Judge close selects its path
independently and requests `closeEventModeWidget(D,path)`. The adopted wrapper
tail-forwards `closeWidget(D,4,path)`; the Judge retains one result.
The [direct close](content-director-ui-contracts.md#closewidgetdirect-behavior)
and [local cleanup](content-director-ui-contracts.md#closewidgetlocal-cleanup-request)
contracts own its conditional cleanup. A normal true result is a completed
Lua request, not proof of destruction. These four methods establish no
external event order or automatic close after returning an input.

## Original source identity and locators

The extraction is retail 1.23b `2012.09.19.0001`. The selected archive matched
[private_lua_corpus.json](../manifests/private_lua_corpus.json). The canonical
member matched [scripts.json](../manifests/scripts.json), row starting at
line 9921. The original and payload matched
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json), resource row
starting at line 138:

| Representation | Locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Canonical member, 427 lines | `lua/scripts/judge/harvest/harvestjudge.lua` | 9902 | `e097de09274574430d14fcafe02ce520cca1ba14ccf8cc42c57413d5cd9ca814` |
| Original LPB | `client/script/0p635/29so5rq/29so5rq0p635.le.lpb` | 4015 | `2797ec20a0f9ba01633332ddcc30c72154420f591832c234ff1b7f90b1c5d8c5` |
| Decoded Lua 5.1 payload | XOR-0x73 wrapper | 4002 | `3662486527fd2c4596ce8a2fd5c6220ba8bc5c15ba27492886ee56a4d8aa6315` |

Use `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/instruction`. Parse the complete
payload and check the root closure/assignment pairs. The assignment target
is a fresh `HarvestJudge` global read for each pair, not proof of one installed
class-table identity. All PCs and prototype indices below are zero-based.
Offsets are decoded-payload bytes, with PC n at `offset+4*n`.

| Method | Canonical source, including binding | Root closure/assignment PCs | Prototype / code offset / words | Selected original PCs |
| --- | --- | --- | --- | --- |
| `openInputWidget` | 69-108 | 20/21 | `root/proto4` / `0x43A` / 36 | Player CALL/test 2/3; command tests 5/14; Mining/Felling calls 11/20, B=4,C=2; final value return 34, B=2. |
| `orderInputWidget` | 111-153 | 23/24 | `root/proto5` / `0x5A3` / 39 | Player CALL/test 2/3; command tests 5/15; Mining/Felling calls 12/22, B=5,C=2; final value return 37, B=2. |
| `askInputWidget` | 156-265 | 26/27 | `root/proto6` / `0x715` / 124 | Phase test 4; land primary tests 6/10 and 18/22; quit tests 42/46; extra test 54; player CALL/test 58/59; selection tests 61/79; Mining/Felling calls 74/92, B=11,C=4; false test 114; return 122, B=4. |
| `closeInputWidget` | 383-419 | 35/36 | `root/proto9` / `0xE21` / 33 | Player CALL/test 2/3; command tests 5/13; Mining/Felling calls 10/18, B=3,C=2; final value return 31, B=2. |

These four prototypes contain 232 words in total. Only their land branches
and shared local glue are established here. The Fishing branch and desktop
wrapper original locators remain in the linked Fishing publication.
The Mining/Felling desktop `GETGLOBAL`/`SELF` pairs are respectively 7/8 and
16/17 for open, 7/8 and 17/18 for order, 63/64 and 81/82 for ask, and 7/8 and
15/16 for close. Their intervening argument setup preserves the captured
method and receiver registers through each selected CALL.

Focused original-instruction checks authenticated the archive, selected
member, LPB and payload, parsed the full payload and reproduced all four
root bindings and prototype metadata. Typed fixtures checked the two land
paths, exact player/command/phase predicates, nil command positions, omitted
fixed arguments, distinct numeric/Boolean/string values, receiver reads,
fixed result adjustment, exact-false normalization and explicit close.
In-memory controls changing a land command, the phase operand, the selected
result width or the false-test polarity were rejected. Fixtures use ordinary
objects with explicit helper returns. Eight focused fixtures replace the
global binding during the modeled method lookup and retain the captured
receiver. Eight controls inserting a later receiver global read are rejected.
Those fixtures test instruction data flow, not general metamethod behavior.
They do not execute native methods, metamethods, property storage or a real
widget.

Actual external invocation, delegate value O, complete typed frame, dynamic
callable selection, initialized storage, applied writes, fresh native readback
and same-widget identity remain unbound. No hit, yield, probability, depletion,
accepted action or settlement claim follows from this static caller contract.
