# Grand Company scenario selector paths

These eighteen selected methods retain one selector result, with different
company-specific dialogue and finalization paths. The original bytecode
distinguishes a caller-visible return from the presentation that precedes it.
The [GC recoverability record](gc-quest-recoverability.md) owns the complete
resource inventory and its client/server evidence boundary.

## Into the Dark offer and follow-up prompts

The three Into the Dark start methods return the single saved
`showQuestInfomation` result after a company-specific response and
`finishCliantTalkTurn`. Their later prompts return the single saved `ask`
result, but answer 1 bypasses both the response row and `finishCliantTalkTurn`.
This distinction is present in the original Lua bytecode.

In the following tables, A0 is the scenario receiver and text owner. A2 is the
receiver of the talk, salute, scheduler and prompt calls. A1 is forwarded as
the second explicit argument of `A2:startCliantTalkTurn(2, A1)`. These roles
describe observed parameter use, not independently identified caller objects.
Rows belong to the respective scenario's text sheet. `say(row)` abbreviates
`A2:say(A0, row, 0)`; scheduler values are the literal argument of
`A2:_runCharaScheduler`. Method arguments are numbered from A0, including the
receiver.

Each start method begins `startCliantTalkTurn(2, A1)`, then `doSalute(company,
33)` and `A0:_wait(1)`. The company values are 2 for Com5g1, 1 for Com5l1 and
3 for Com5u1. The saved salute result does not select a branch or become the
return value. The following calls precede `A0:showQuestInfomation()` in order:

| Start method | Introductory calls after the initial wait |
| --- | --- |
| `Com5g1.processEventFULKEStart` | say 2, 3, 4; scheduler 354086912; say 5, 6, 7; scheduler 354099200; wait 1.5; say 8, 58, 9; `A2:say(A0, 59, 0, 0, A3, A4, A5)` |
| `Com5l1.processEventGUINCUMStart` | say 2, 3, 4; scheduler 353976320; say 5, 6; scheduler 354086912; say 7, 64, 8, 9, 10 |
| `Com5u1.processEventAUBREYStart` | say 2, 3, 4; scheduler 354086912; say 5, 6, 64, 7, 8; scheduler 354103296; say 9 |

Com5g1's start declares six parameters; the other starts declare three. The
five explicit values following row 59 are exactly `0, 0, A3, A4, A5` when the
row's mode argument is included. No selected method computes or checks A3,
A4 or A5. Their producer and concrete caller values remain unknown.

| Method and canonical Lua lines | Result 1, in order | Every other result, in order | Return |
| --- | --- | --- | --- |
| `Com5g1.processEventFULKEStart`, `com5g1.lua:23-147` | scheduler 70795264; say 11; finish talk | scheduler 70832128; say 10; finish talk | One unchanged quest-information result |
| `Com5l1.processEventGUINCUMStart`, `com5l1.lua:23-137` | scheduler 354103296; say 12; finish talk | scheduler 354041856; say 11; finish talk | One unchanged quest-information result |
| `Com5u1.processEventAUBREYStart`, `com5u1.lua:23-131` | scheduler 354107392; say 11; finish talk | scheduler 354041856; say 10; finish talk | One unchanged quest-information result |
| `Com5g1.processEvent_020_1`, `com5g1.lua:543-576` | No further call | say 63; finish talk | One unchanged ask result |
| `Com5l1.processEvent_030_1`, `com5l1.lua:452-485` | No further call | say 42; finish talk | One unchanged ask result |
| `Com5u1.processEvent_020_1`, `com5u1.lua:386-419` | No further call | say 40; finish talk | One unchanged ask result |

The later prompts each declare A0-A2 and begin
`A2:startCliantTalkTurn(2, A1)`. Com5g1 says row 57 then asks row 38;
Com5l1 says row 61 then asks row 39; Com5u1 says row 61 then asks row 37.
Each ask is `A2:ask(A0, row, 2)` and retains exactly one result.

The original prototypes are `root/proto1` for all starts and `root/proto10`,
`root/proto7`, `root/proto5` for the Com5g1, Com5l1, Com5u1 later prompts.
The starts call the selector at PCs 76, 68, 63, compare it to 1 at PCs 77,
69, 64 and return one value at PCs 98, 90, 85 respectively. Every later
prompt calls ask at PC 13, compares at PC 14 and returns one value at PC 24.
Their trailing zero-value RETURN instructions are unreachable on these paths.
PCs are zero-based within each prototype. Source identities and inventory
remain in [the canonical quest contracts](../data/quest_contracts.json),
under `lua/scripts/quest/scenario/com/com5g1.lua`, `com5l1.lua` and
`com5u1.lua`.

These are static client presentation and return contracts. They do not prove
dungeon launch, party requirements, quest completion, historical invocation,
or what a caller does with the result. Existing [company offer contracts](job-grand-company-event-contracts.md#company-quest-offer-and-choice-branches)
cover other company starts.

## Grand Company 701 scenario choice contracts

The selected 701 scenario methods preserve the single `askExtendWidget`
result through dialogue finalization and return it unchanged. Their local
branches distinguish result 1 from every other result. The method names do
not establish authoritative acceptance, cancellation or quest-state mutation.

The SAN/title join in `xivl-client-data:docs/grand-company-quest-identities.md`
identifies Gcg701 as quest 111628, You Don't Have the Rite; Gcl701 as 111428,
The Weakest Link; and Gcu701 as 111828, Gore a Lizard, Hurry.

### Arguments and common effects

All six methods have three positional parameters A0-A2. A0 is supplied as
the quest argument to dialogue and selectors. A1 is passed unchanged to
`A2:startCliantTalkTurn(2,A1)`. A2 receives the dialogue, selector, scheduler,
salute and finalization calls. These are caller-supplied values, not recovered
concrete actor identities.

Every selector is `A2:askExtendWidget(A0,row,2,1,mode)`, with `CALL B=7,C=2`:
six arguments including the receiver and one result. All `say` calls below
are `receiver:say(A0,row,0)`. Unless labeled `worldMaster`, the receiver is A2.
Every branch finishes with `A2:finishCliantTalkTurn()` and returns exactly
one value, the unchanged selector result. No other local effect is hidden
between the listed calls and those returns.

### Company comparison

Each row lists the effects after `startCliantTalkTurn` and before the selector,
then the two selector branches. `scheduler(n)` means `A2:_runCharaScheduler(n)`.

| Method | Before selector | Selector row / mode / PC | Result 1 | Other result | Return PCs |
| --- | --- | --- | --- | --- | --- |
| Gcg701.processEventVORSAILEok | scheduler(353959936), say 26 | 27 / 1 / 18 | say 31, say 32, finish | say 30, finish | 33 / 42 |
| Gcg701.processEventVORSAILEstop | scheduler(353959936), say 33, worldMaster say 34 | 35 / 2 / 24 | say 54, finish | say 55, finish | 34 / 43 |
| Gcl701.processEventOK | scheduler(354095104), say 24 | 25 / 1 / 18 | say 29, say 30, finish | scheduler(70795264), say 28, finish | 33 / 45 |
| Gcl701.processEventExit | say 31, worldMaster say 32 | 33 / 2 / 21 | scheduler(70795264), say 36, finish | say 37, finish | 34 / 43 |
| Gcu701.processEvent005 | salute sequence, say 26 | 27 / 1 / 27 | scheduler(353959936), say 31, say 32, say 33, finish | scheduler(353964032), say 30, finish | 59 / 59 |
| Gcu701.processEvent010 | salute sequence, say 34, worldMaster say 35 | 36 / 2 / 33 | scheduler(353959936), say 39, finish | scheduler(353959936), say 40, finish | 55 / 55 |

Both Ul'dah methods call `A2:doSalute(3,43)` at PC 7. A zero result runs
scheduler 353959936 at PC 12; every other result skips that scheduler.
Both paths call `A0:_wait(1)` at PC 15 and continue to the dialogue and
selector. The salute result is separate from the selector result and is
not returned. This is a presentation branch, not an eligibility test.

The selector comparison is `EQ A=0` immediately after each selector call.
Equality skips the following jump into the alternative branch. Gridania and
Limsa each have two separate one-value `RETURN` sites. Ul'dah joins both
selector branches before finalization and its one-value return. The trailing
zero-value return instruction in each prototype is unreachable along these
normal paths. All instruction PCs here are zero-based.

### Original evidence and limits

The canonical records are `xivl-client-scripts:data/quest_contracts.json`,
selected by the following decoded script paths. They own full source,
resource and decoded-payload hashes, declaration records, calls and returns.
The original LPB and decoded-payload bytes were checked against those pins.

| Script under lua/scripts/quest/scenario/ | Original resource path | Selected prototypes / code offsets / instruction counts |
| --- | --- | --- |
| gcg/gcg701.lua | tp5rq/r75w9s1v/373/373cji.le.lpb | root/proto6 / 0xBBB / 44; root/proto7 / 0xD4D / 45 |
| gcl/gcl701.lua | tp5rq/r75w9s1v/37y/37ycji.le.lpb | root/proto6 / 0xAD9 / 47; root/proto7 / 0xC80 / 45 |
| gcu/gcu701.lua | tp5rq/r75w9s1v/37p/37pcji.le.lpb | root/proto6 / 0xBE1 / 61; root/proto7 / 0xDF4 / 57 |

The selected originals establish branch order, call arity and return dataflow.
Static checks cover both selector branches and both salute branches where
present. They do not establish the native meaning of scheduler values,
historical caller arguments, server interpretation of the returned result,
or authoritative quest acceptance, cancellation, completion or rewards.
The separately documented QuestDirectorGc*70101 content-information constants
and malformed-decompile control-flow limitation remain separate evidence.

## Company sidequest 304 offers and follow-up choices

The three selected 304 offer methods call `showQuestInfomation()` once,
branch on its first result, and return that same single result after their
closing presentation. Their company-specific effects are:

| Method | Result 1, in order | Other results, in order | Closing presentation |
| --- | --- | --- | --- |
| `Gcg304.processEventALAIREStart` | actor scheduler 354099200; say row 13 | actor scheduler 354078720; say row 12 | fade out, finish talk turn, wait, fade in |
| `Gcl304.processEventLilinaStart` | say row 9 | say row 8 | fade out, finish talk turn, wait, fade in |
| `Gcu304.processEventBERTHARStart` | actor scheduler 354107392; say rows 9, 10 | actor scheduler 70823936; say row 8 | finish talk turn |

Rows are arguments to the supplied actor's `say(self, row, 0)`. Scheduler
values are literal `_runCharaScheduler` arguments, without inferred animation
names. Both fade sequences use `(event, 1)` and `_wait(1)`.

Before the choice, Gcg304 and Gcl304 fade out, call the supplied actor's
`startCliantTalkTurn(1, event)`, wait 1, and fade in. Gcg304 then runs
scheduler 353976320 and selects row 2 when the fourth declared parameter
equals 1, otherwise row 3. It continues with rows 4, 5; scheduler 353984512;
rows 6, 7; scheduler 354086912; and rows 8, 9, 10, 11. Gcl304 instead speaks
rows 2, 3, 4, 35, 36, 5, 6, 7, 37, 38 in order.

Gcu304 starts `startCliantTalkTurn(2, event)`, runs scheduler 353984512,
and speaks row 2 with its fourth declared parameter as an additional argument,
then row 3. It runs scheduler 354066432, speaks rows 42, 4, 43, runs
scheduler 353976320, and speaks rows 5, 6, 7 before the choice. The supplied
fourth parameters' producers and actual invocation values remain unknown.
Parameter positions here include `self` as the first declared parameter.

Each class's `processEvent_010` calls its supplied actor's
`ask(self, row, 2)` exactly once and returns only that call's first result.
The row is 41 for Gcg304, 23 for Gcl304, and 38 for Gcu304. The result-1
comparison has no distinct effect: both paths reach the same return with the
saved value unchanged. These wrappers do not start or finish a talk turn.

Sources: [quest contracts](../data/quest_contracts.json), records
`lua/scripts/quest/scenario/gcg/gcg304.lua`, `gcl/gcl304.lua`, and
`gcu/gcu304.lua`, with the complete LPB and decoded-payload identities in each
record's `resource`. The selected methods are `root/proto1` (offer) and
`root/proto5` (follow-up). Zero-based bytecode PCs and decoded offsets are:

| Class | Offer selector / comparison / return PCs | Selector / return offsets | Follow-up ask / comparison / return PCs | Ask / return offsets |
| --- | --- | --- | --- | --- |
| Gcg304 | 78 / 79 / 111 | 897 / 1029 | 4 / 5 / 8 | 3358 / 3374 |
| Gcl304 | 66 / 67 / 93 | 886 / 994 | 4 / 5 / 8 | 2798 / 2814 |
| Gcu304 | 55 / 56 / 82 | 843 / 951 | 4 / 5 / 8 | 2743 / 2759 |

All selector calls request one result (`CALL C=2`), and the reached returns
emit one value (`RETURN B=2`). The follow-up jumps at PCs 6 and 7 both target
PC 8. This is recovered client presentation and return behavior; it does not
establish historical invocation, server objectives, quest admission, or the
action taken by a caller receiving the result.
