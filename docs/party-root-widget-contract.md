# PartyRootWidget local contract

This contract records the bounded local behavior recovered from one
authenticated retail FFXIV 1.23b Lua 5.1 resource. It covers the root binding,
the fourteen admitted methods, their contained instructions, supplied values,
local widget state, typed local requests, typed local returns, refusal paths,
and close requests. It does not claim native implementation, social mutation,
server acceptance, rendering, persistence, callback settlement, destruction,
or object lifetime.

## Evidence identity

The selected logical resource is `widget/partyrootwidget.lua`. The tracked
script manifest records its canonical identity as 24,952 bytes, 1,080 lines,
SHA-256 `c946473b4adac714203f7d5cb171d1d353ff4fb48e8c912a24527fd9b7e1a72f`
(`xivl-client-scripts:manifests/scripts.json:15723-15726`). The matching retail
resource is `n1635q/u9sqlsvvqn1635q.le.lpb`, 8,337 bytes, SHA-256
`a7a87de2ee4872b50bba39c7c85d8942e2d19cc6bbeeae97f511d3b1f04ae290`; its
coverage record binds an 8,324-byte payload with SHA-256
`ae5cdc973587d2e86b204dd9fabf9d98064d59f755d6e01588fec3fcd61ce4ef` to the
same logical script (`xivl-client-scripts:manifests/retail_lua_coverage.json:27588-27599`).
The tracked sidecar identifies the class as `PartyRootWidget` and records the
two promoted API names (`xivl-client-scripts:lua/scripts/widget/partyrootwidget.calls.json:1-18`).

The pinned reproduction tools were `tools/retail_script.py`, SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`, vendored
unluac `tools/vendor/unluac/unluac_2025_12_23.jar`, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`, and
`tools/build_quest_contracts.py`, SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`.
The decoded payload and canonical LF source reproduced those pinned identities
before semantic checks. No `luac` tool was used.

## Root and method envelope

The root first requires `/Widget/WidgetBaseClass`, defines
`PartyRootWidget` over `WidgetBaseClass`, then performs fourteen method binding
attempts in this order: `init`, `setFocus`, `processUICommandCancel`,
`processUICommandOperate`, `processUICommandDefault`, `update`,
`closeViewWidget`, `getEditMode`, `setEditMode`, `getSignal`, `setSignal`,
`updateChildWidgetStatus`, `updateJoinButton`, and `getPartyRoot`. The root has
50 original words. The fourteen admitted child prototypes contain 877 words;
all have no nested child prototype. Every binding, direct CALL or TAILCALL,
guard/JMP, and RETURN was read from the decoded payload. The retained child
matrix has 106 direct calls, 229 guard/JMP words, and 30 RETURN words; the root
window additionally has two CALL words and one RETURN word. All retain the
original A/B/C widths and decoded offsets.
The root code window starts at payload offset 32; each admitted child code window
is non-overlapping and ends within the 8,324-byte payload.
Own-method calls are fresh table lookups and unconditional source calls; the
local trace records the actual closure identity before each admitted call.

The function debug line locators below came from the decoded chunk and are not
canonical LF source lines. The canonical body is not present in the public
checkout; its identity is carried by the tracked manifest above and reproduced
from the pinned LPB for this bounded check. The full reproduced-source windows
are:

| method | canonical LF function window | canonical binding | decoded debug lines |
| --- | --- | --- | --- |
| `init` | 11-176 | 177 | 52-114 |
| `setFocus` | 180-197 | 198 | 123-128 |
| `processUICommandCancel` | 201-219 | 220 | 140-144 |
| `processUICommandOperate` | 223-335 | 336 | 155-218 |
| `processUICommandDefault` | 339-461 | 462 | 230-291 |
| `update` | 465-734 | 735 | 300-392 |
| `closeViewWidget` | 738-759 | 760 | 401-416 |
| `getEditMode` | 763-771 | 772 | 424-426 |
| `setEditMode` | 775-784 | 785 | 434-436 |
| `getSignal` | 788-796 | 797 | 444-446 |
| `setSignal` | 800-809 | 810 | 454-456 |
| `updateChildWidgetStatus` | 813-944 | 945 | 465-521 |
| `updateJoinButton` | 948-1071 | 1072 | 530-580 |
| `getPartyRoot` | 1075-1079 | 1080 | 588-590 |

## Local state and initialization

`init` replaces `work._temp` with nine ordered descriptor pairs:

```text
initialized/boolean, leaderWhenOpen/boolean, notSoloWhenOpen/boolean,
closeOK/boolean, edit/integer8, find/integer8, view/integer8,
party/integer8, root/integer8
```

It writes `initialized=false`, `edit=0`, `find=0`, `view=0`, `party=0`,
`root=1`, and `closeOK=false`. It requests cancel and close conditions,
confirm conditions for `Button_PcMatching_Edit`, `Button_PcMatching_Find`, and
`Button_PartyManager`, matching cancel conditions for those controls, and a
`UILuaCommands.PropertyChanged` condition on the edit control. It requests
modal and drag true, hides `Grid_Help`, writes text `tostring(8)` to
`TextBlock_Party_Max`, then freshly looks up and calls its own `update`, disables
the edit button, and freshly looks up and calls its own `setSignal` with numeric
`1` (decoded debug range 52-114; canonical
window 11-177 above). The bounded replay pins those own closures before each
call; this does not prove helper installation.

The supplied `desktopWidget.countPartyMember()` result is an actual input. If
it is greater than one, initialization writes `notSoloWhenOpen=true` and reads
`isMyPartyLeaderForMyPlayer()`, writing `leaderWhenOpen` to the Boolean outcome
of `leaderResult == true`. For a count at most one, both flags are written
false. The
bounded replay seeds nine distinct preexisting scalar values plus a distinct
`_temp` sentinel and verifies all nine ordered descriptor rows, descriptor
types, and all nine scalar writes; suppression and descriptor mutations are
rejected by separate controls. These are local control inputs, not a
server-side eligibility decision.

`setFocus(control)` forwards the supplied control to `setLogicalFocus`, reads
`desktopWidget._getKeyboardFocusedWidget()`, and forwards the control to
`setKeyboardFocusedControl` only when Lua `==` between that fresh result and
the receiver evaluates true (decoded debug range 123-128; canonical window
180-198). Lua `==` can invoke an unknown Lua or native `__eq` metamethod; these
plain fixture objects use identity, but this bounded result is not a universal
exact-identity theorem. The owned-widget and other-widget fixtures are
separate typed cases.

`getEditMode` and `getSignal` read `Button_PcMatching_Edit` properties
`IntData.Value3` and `IntData.Value2`, respectively, with open result tails.
`setEditMode` and `setSignal` write those same properties and return no
values. `getPartyRoot` returns its supplied receiver (decoded debug ranges
424-456 and 588-590; canonical windows are listed above).

## Commands and supplied inputs

`processUICommandCancel` closes the supplied receiver through
`desktopWidget.closeWidgetDirect` when `work.closeOK` is true or
`work.root == 2`; otherwise it returns without a request. Its extra command
arguments are not read (decoded debug range 140-144; canonical window 201-220).

`processUICommandOperate` first refuses when `work.party == 4`. When
`work.party == 3`, it reads the supplied root's
`getChildWidgetByWindowName("PartyManagerWidget")` result and resets `party`
to zero only when that result is nil. If `closeOK` is true and `root == 2`, it
issues a direct close before the control-specific path. The supplied control
name then selects these local requests:

| Control input | Guard and request | Local state/result |
| --- | --- | --- |
| `Button_PcMatching_Edit` | `getEditMode()==0`: open `PcMatchingEditWidget`, receiver, `true` | `true` result writes `edit=1` |
| `Button_PcMatching_Edit` | `getEditMode()==1`: open `PcMatchingViewWidget`, receiver, `true`, numeric `1` | `true` result writes `view=1` |
| `Button_PcMatching_Edit` | `getEditMode()==2`: open `PcMatchingViewWidget`, receiver, `true`, numeric `2` | `true` result writes `view=1` |
| `Button_PcMatching_Find` | requires `root >= 2`; open `PcMatchingFindWidget`, receiver, `true` | `true` result writes `find=1`; root below 2 refuses |
| `Button_PartyManager` | open `PartyManagerWidget`, receiver, `true` | `true` result writes `party=1` |

The call results are strict Boolean comparisons. A local `true` result selects
the write; this is not a server acceptance result. The exact original call
words are retained in the static ledger at `root/proto3` PCs 40, 54, 68,
86, and 99. The decoded debug range is 155-218; the canonical window is
223-336.

`processUICommandDefault` accepts a supplied command name. For
`UILuaCommands.PropertyChanged`, it reads a fresh signal. Signal `2` writes
`root=2`; when `initialized` is false it reads the supplied edit-mode property.
Modes `1` and `2` enable the edit control and choose content `2905` and `2906`,
respectively, without reading count, leader, or variation. Every other edit mode takes the fallback beginning with content
`2904`; with more than one party member, non-leader state changes it to `2905`
and disables edit, while a full party led by the player keeps `2904` and
disables edit. The remaining fallback path reads the supplied variation:
`10001` or `10002` disables edit, while every other value enables it. These are
fresh queries rather than one captured snapshot: the first count
above one followed by a fresh leader result of `false` writes
`leaderWhenOpen=false`; otherwise a later count query can select the full-party
branch, whose fresh leader `true` result writes `leaderWhenOpen=true`, or the
variation branch, which also writes `leaderWhenOpen=true`. The method writes
the selected content. An initialized widget stops after setting
`root=2`. For non-property command names, party `4` returns immediately;
party `3` reads `getChildWidgetByWindowName("PartyManagerWidget")` and resets
party to numeric `0` only when that result is nil. These values are local
display/control inputs, not policy proof
(decoded debug range 230-291; canonical window 339-462).

## Update and presentation

`update` reads a fresh party count. At count at most one, it disables
`Button_PartyManager`, sets help parameter zero, hides the party count controls,
and may reset edit mode/content when the opening flags show a non-leader
transition. This latch/close block is entered only when
`notSoloWhenOpen==true`; a false flag skips it even with idle children and
`root==2`. If all child-status flags are numerically `0` or `2` and `root==2`, it
sets `root=3` and requests direct close; otherwise it sets `closeOK=true`. A
`party==2` and `root==2` pair requests `closeChildWidget("PartyManagerWidget",
self)` and writes `party=3`.
The solo close branch at `root/proto5` PC 91 and the shared child-status close
branch at `root/proto11` PC 121 tail-return the direct-close helper's open
results; the child-status branch writes `root=3` before that request.

At count above one, it closes directly when `closeOK` and `root==2`; otherwise
it enables the party manager, writes `tostring(count)` to `TextBlock_Party`,
and shows the three count controls. A non-leader can disable edit mode and
close an edit or view child; a leader disables edit at count 8, otherwise
enables it, and can reset content from the opening flags. In particular,
`count=8`, leader `true`, `notSoloWhenOpen=true`, and
`leaderWhenOpen=false` continues with `setEditMode(0)` and content `2904`
(decoded debug range 300-392; canonical window 465-735). The
replay distinguishes numeric counts from Boolean leader results and retains
zero-result close requests. In the multi-member direct-close path, `root` is
written as numeric `3` before the close request; the close helper's open tail is
the method result.

`closeViewWidget` closes the view child when its supplied second argument is
nil. For any nonnil second argument it writes `closeOK=true`, `root=3`, and
tail-returns the result of `desktopWidget.closeWidgetDirect(self)` (decoded
debug range 401-416; canonical window 738-760).

`updateChildWidgetStatus` accepts a supplied child name and status. For a view
child, it first checks the preexisting `work.view == 1` numeric predicate and
changes that field to `2`; then any nonnil supplied status replaces it. Thus an
old value `1` with supplied status `1` ends at `1`. Status `5` tests
the resulting field, including a preexisting `5` with nil input, and may update
edit-button content/enabling based on fresh edit mode, party count and leader
results. For view status `5`, the non-leader count `>1`, edit-mode `2` path
disables edit and returns before the shared child-status close block; a leader
count `8` path also disables edit and returns from this child-status method
before its later content reset. Edit and find children advance status `1` to `2` and then replace from
any nonnil supplied status. The PartyManager branch advances `party` from `1`
to `2`; a nonnil status is written to `work.find` (the original field write is
retained as-is), and status `4` disables the party manager and sets
`closeOK=true`. After the child branch, the shared close check requests a close
when `closeOK==true` and `root==2`; the PartyManager status-`4` branch is the
local status path that sets this latch, while the view status-`5` path can
return before the shared check (decoded debug range 465-521; canonical window
813-945).

`updateJoinButton` reads the supplied desktop variation. Only `10001` and
`10002` enter the join-prompt cleanup. It fresh-reads child presence and edit
mode, closes eligible view/edit/find children, updates local view/edit state
for the branches that do so, and then checks the four child-status fields
numerically: each must be `0` or `2`. If all four are in that set and `root==2`,
it writes `root=3` before requesting direct close; at the direct-close PC the
helper call has fixed zero-result width and the following `RETURN B=1` makes the
method return zero results, regardless of the helper's supplied result.
Otherwise it sets `closeOK=true`.
Other variation values produce no local request (decoded debug range 530-580;
canonical window 948-1072).

## Earned local edges and limits

The bounded source earns these partial local-request edges, not native or
server behavior:

- `desktopWidget.openChildWidget` from `root/proto3` PCs 40, 54, 68, 86, and
  99, with the exact child name, supplied receiver, Boolean `true`, optional
  mode, one-result width, and strict-Boolean state write.
- `desktopWidget.closeWidgetDirect` from `root/proto2` PC 11,
  `root/proto3` PC 28, `root/proto5` PCs 91 and 125, `root/proto6` PC 15,
`root/proto11` PC 121, and `root/proto12` PC 102. At join PC 102 the `CALL`
has `C=1` and the following `RETURN` has `B=1`, so the close helper result is
discarded and `updateJoinButton` returns zero results; it does not prove
destruction.
- `desktopWidget.closeChildWidget` from `root/proto5` PCs 110, 184, 193, and
  212, `root/proto6` PC 6, and `root/proto12` PCs 28, 44, and 60, each with
  the original child name and supplied receiver.

No normal or Ask linkshell list/member/menu resource was included in this
bounded contract, so no resource edge was earned. Existing social command and native/server boundaries
remain owned by `xivl-client-scripts:docs/linkshell-party-command-contracts.md` and
`xivl-client-scripts:docs/search-recruitment-native-boundaries.md`.
Those pages establish that client command inputs and native recruitment routes
do not by themselves prove server mutation, eligibility, delivery, or reply
settlement (`linkshell-party-command-contracts.md:61-121`,
`search-recruitment-native-boundaries.md:57-85`).

The admitted evidence does not establish party leadership policy, roster
eligibility, recipients, locks, content acceptance, native effects,
network requests, callbacks, owner behavior, or lifetime. A child name and a
Boolean open/close result are local control-flow values only. The finite
evidence admits one opaque helper ordinary-error prefix and shows that a
swallow-and-continue corruption reaches later original calls; it does not
claim native error policy or server behavior.

## Verification and reproduction

The authored checker executes original decoded Lua 5.1 words in a bounded
instruction interpreter. It does not substitute a handwritten method model.
The admitted fixture literals were reconciled separately against the canonical
source windows and original CALL/TAILCALL words: each expected event carries a
literal callsite and typed request/result fields, while a separate evidence map
checks its source window, original word, opcode, operands, receiver/callable
roles, and result width before execution. The checker has no fixture-emission
path. A second literal source oracle independently records each case's branch
predicate, exact supplied method arguments/host inputs/seeds, selected original call-site sequence, and per-call argument/result
origins (LOADK/RK constants, supplied arguments, work fields, or named helper
inputs), plus typed local state/result and ordinary-error expectations. It is
checked before any VM execution and is not derived from observed events; a
paired wrong-operand mutation is rejected even when both retained event copies
are changed together.
The independent fixture file contains 30 typed cases covering initialization,
distinct focus results, cancel close, edit/view/find/party opens,
property-changed modes, solo and non-leader updates, full-party disable,
close nil/non-nil results, false and open nil/zero tails, child statuses, join
cleanup, an ordinary helper error prefix, and a no-op variation. It passed 139
recorded events and 16 corruption controls plus 16 positive
source-counterexample probes:
same-label wrong receiver/callable
rejected before helper invocation, two distinct initialization-write/descriptor
mutations including the init-error descriptor table and same-content table clone,
same-prefix root-write
rejection, strict unpinned-call rejection, ordinary-error suppression, paired
wrong-operand source-origin rejection, numeric-versus-Boolean equality, and
missing fresh `update`/`setSignal` lookups. The positive source
controls cover full-party content `2904`, the count-8 update content reset,
not-solo latch, status overwrite and status-5 early returns, direct-close tails, join numeric status gates,
non-property paths, cancel refusal, both root-close outcomes, distinct supplied
focus controls, and the changing-result default-fallback sequence
`count,leader,count,leader,variation` with a typed `setEnable(..., true)` request;
the local `leaderWhenOpen` and `root` field assertions remain separate. Each
corruption control has a passing baseline before its rejection assertion; the
positive probes assert source facts without pretending to be corruption
mutations. Event lists are exact in order and cardinality.

Finite coverage is not branch complete. Static-only or unvisited paths are
recorded exactly in the local finite receipt; they include the alternate
multi-member initialization leader branch, cancel refusal combinations,
additional edit modes, party-3 lookup reset, close-latch preambles, the
non-leader/leader update subbranches, alternate child status values, join
variation 10002 and absent-child paths, open-return false paths, and
discarded trailing RETURN words for the getter tails. These paths remain
bounded unknowns rather than generalized client policy.

Reproduce the public decode and disassembly artifacts with placeholders:

```powershell
python tools/retail_script.py --input <client>/client/script/n1635q/u9sqlsvvqn1635q.le.lpb --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <scratch>/partyrootwidget.decoded.luac --script-out <scratch>/partyrootwidget.reproduced.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <scratch>/partyrootwidget.disassemble.txt <scratch>/partyrootwidget.decoded.luac
```

These commands reproduce the payload, canonical source, and disassembly
artifacts. The finite typed fixtures and original-word interpreter are separate
local evidence and do not turn the reproduced decompile into live-client or
server evidence. The finite checker is maintained as separate local evidence;
it is not part of the two public artifact-reproduction commands.
