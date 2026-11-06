# Echo name-preparation request

`DesktopWidget.deleteChineseName` returns one nil for nil input. For any
other input it requests `isChinese` from its receiver. An exact false result
returns the input unchanged; every other first result tail-calls
`_string.gsub` with the input, literal pattern `" !!!"` and empty replacement.
The method name alone supplies no character, language or actor classification.

## Guard, request and results

The original method has two fixed parameters `(D, N)` and no variadic tail.
Missing positions become nil and extra actual values are discarded. Exact
nil `N` returns exactly one nil before accessing `D`. Non-nil input, including
false, zero or an empty string, reaches the receiver lookup.

It captures `D.isChinese`, calls it with exactly `(D)` and retains one result
`C`. Missing results become nil; extra results are discarded. Only literal
Boolean false returns exactly one unchanged `N`. The predicate body and its
runtime binding are separate boundaries, so no language configuration value
or classification follows from its name here.

Otherwise the method freshly reads global `_string`, obtains its `gsub`
field and tail-calls it with exactly `(N, " !!!", "")`. It passes no widget
or library receiver and no fourth replacement limit. The tailcall forwards
all normal results, including zero or multiple values, without adjustment.
The predicate can change `_string` or its field before that later lookup.
Lookup and call errors have no protected-call recovery.

The [parent converter](echo-pronoun-conversion.md#ordered-replacement-preparation)
retains one result from each such name-preparation call. Under that actual
method binding it therefore keeps the unchanged value or the library's first
result, nil when none is returned; any later results do not reach the
replacement value.

## Conditional standard-library meaning

If the obtained function has standard Lua 5.1 `string.gsub` behavior and the
input is a string, this exact pattern removes every occurrence of one ASCII
space followed by three exclamation marks. These characters are literal in
Lua patterns, and no start/end anchor is supplied. It is not restricted to
an end-of-name suffix and does not generally remove Chinese characters.
Standard `gsub` also returns a match count as its second result; the parent
converter's one-result capture discards it. These conditional semantics follow
the [Lua 5.1 gsub contract](https://www.lua.org/manual/5.1/manual.html#pdf-string.gsub)
and [pattern character rules](https://www.lua.org/manual/5.1/manual.html#5.4.1).

For example, synthetic string `"A !!! B !!!"` becomes `"A B"` with count2,
and `" !!!A"` becomes `"A"` with count1. `"A!!!"` has no matching space and
remains unchanged with count0. These are conditional library examples, with
no retail name value or historical output asserted.

The actual predicate/library bindings, selected actor/name values, locale,
native accepted-input domain, converted echo text and visible output remain
unestablished. No further helper or native body was studied for this result.

## Source identity and checks

The [converter source identity](echo-pronoun-conversion.md#source-identity-and-checks)
pins the retained archive, canonical connector, original LPB and decoded
payload at private-source revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`, extraction `2012.09.19.0001`.
Canonical `widget/desktopwidget_connector.lua` lines1097-1117 supply this
method. Original `root/proto18` has seventeen instructions, code offset32717,
two fixed parameters, raw vararg0, zero upvalues and no nested prototypes.
Root PCs54-56 obtain `DesktopWidget`, create the closure at PC55 and assign
the constant RK key `deleteChineseName` at PC56. PCs and payload offsets
are zero-based.

| Behavior | PCs | Decoded-payload offsets |
| --- | --- | --- |
| Exact-nil input and one-nil return | 0-3 | 32717-32729 |
| Predicate call, exact-false comparison and unchanged return | 4-8 | 32733-32749 |
| Fresh library/field lookup and three-argument tailcall | 9-14 | 32753-32773 |

The seventeen-word code range has SHA-256
`1b540b176e9bbe050114bc96ef96c70b2e3fd2669774ba04e7a7d7d2ccf65e93`.
`tools/retail_script.py` and `ChunkReader`/`instruction` in
`tools/build_quest_contracts.py` expose the authenticated original in memory.
A bounded check passed 21 source cases for nil/exact-false distinctions,
predicate result adjustment, original input/receiver frames, fresh library
lookup and complete result tails. Eight synthetic ASCII examples checked
the documented conditional literal-pattern model. Nine rejecting controls
covered guard, frame, return/result widths and a one-occurrence model.
Opaque predicate/library stubs and finite ASCII models establish only these
source and conditional examples; no actual Lua library, other helper body or
retail runtime was executed.
