# AddressListNamingWidget contract

## Evidence identity

This contract is for the retail FFXIV 1.23b Lua extraction
`2012.09.19.0001`, scripts revision
`b560994442e445fdd76db7977de9939a5e9d63d6`. The selected logical resource is
`widget/addresslistnamingwidget.lua`; its canonical LF source is 23,962 bytes,
1,008 lines, SHA-256
`589c8b4ba71d22c67fede9f141d5a62eee118ab7bc1181e461b09be77618b03e`.

The matching LPB is
`n1635q/966s5rry1rqw9x1w3n1635q.le.lpb`, 6,883 bytes, SHA-256
`72c8a0258d942a4acee4e9f5748c1b4d4b74e9ef9125385a8ac0d45bb6c92ccb`.
Its decoded Lua 5.1 payload is 6,870 bytes, SHA-256
`ab4152d2300cfa431d1a9d9cbc85110190a05baec46f00a2bd243df8c5259b34`.
The canonical source is reproduced byte-for-byte by the pinned route.

The reproduction tools are `tools/retail_script.py`, 3,555 bytes, SHA-256
`765327cf3da90aacf8e36b185ce53aa0615f7705e9f9ccdc3a7243e3b6c0c391`,
vendored unluac `tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes,
SHA-256 `98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`,
and parser `tools/build_quest_contracts.py`, SHA-256
`a24fed11bee2e52b45513e49f37f3118226cd561227a8f44caf7f0a7d8cb9956`.

## Prototype and word locators

The root prototype has code offset 32 and 41 words. Root PC 2 is
`CALL A=0 B=2 C=1`, word `0x0100401c`, for `require`; PC 6 is
`CALL A=0 B=3 C=1`, word `0x0180401c`, for `_defineClass`.
For method index `i` in the declaration order below, root PC `8+3i` is
`CLOSURE A=1 Bx=i` and PC `9+3i` is `SETTABLE A=0 B=261+i C=1`; the key is the
listed method name. These words bind the exact 11 child prototypes.

| method | source lines | prototype first-last | code offset / words |
| --- | ---: | ---: | ---: |
| `init` | 11-326 | 53-160 | 579 / 255 |
| `setFocus` | 331-349 | 168-175 | 2562 / 16 |
| `processUICommandClose` | 354-361 | 187-189 | 2775 / 5 |
| `processUICommandCancel` | 366-409 | 200-217 | 2877 / 42 |
| `processUICommandOperate` | 414-619 | 228-304 | 3216 / 182 |
| `processUICommandApplicationOperate` | 624-648 | 316-329 | 4352 / 21 |
| `processUICommandDefault` | 653-779 | 341-404 | 4584 / 126 |
| `getInputName` | 784-820 | 413-428 | 5338 / 32 |
| `confirm` | 825-973 | 437-482 | 5658 / 124 |
| `ignoreFamilyName` | 978-995 | 490-498 | 6589 / 14 |
| `isChinese` | 1000-1006 | 506-508 | 6784 / 5 |

Each method word is at `code offset + 4*PC`. The following direct-call table
lists every CALL or TAILCALL as `PC:word`; the checker also verifies opcode,
target, A, B, C, and re-encoded word against the original payload.

| method | direct call words |
| --- | --- |
| `init` | `33:0100411c,35:0100411c,38:0180411c,41:0180411c,44:0180411c,47:0180411c,50:0180411c,53:0180411c,56:0180411c,59:0180411c,62:0180411c,65:0180411c,69:0200411c,73:0200411c,77:0200411c,81:0200411c,85:0200411c,89:0200411c,93:0200411c,97:0200411c,101:0200411c,105:0200411c,117:0200411c,120:0180411c,135:0200411c,138:0180411c,149:0280411c,155:0280411c,166:0200411c,169:0180411c,174:0280411c,178:0100811c,185:0280411c,189:0200411c,194:0280411c,198:0200411c,203:0280411c,208:0280411c,212:0200411c,221:0280411c,225:0200411c,230:0200411c,234:0200411c,239:0280411c,243:0200811c,247:0200415c,250:0180411c,253:0180411c` |
| `setFocus` | `6:0180409c,9:0100809c,14:0180409c` |
| `processUICommandClose` | `3:0180415c` |
| `processUICommandCancel` | `9:0180015d,19:0180015d,28:0180015d,34:0180015d,39:0180015d` |
| `processUICommandOperate` | `9:0180015d,19:0180015d,28:0180015d,34:0180015d,43:0100815c,47:0100419c,50:0180419c,54:0180019d,65:0180815c,69:0100819c,73:010041dc,77:018001dd,81:0100815c,90:0100819c,94:0100819c,98:0100819c,102:0180821c,105:0100819c,111:020041dc,115:018001dd,119:0100815c,124:0180815c,129:0180015d,133:0100815c,137:0100815c,142:0180015d,152:0180819c,156:0180821c,159:0100819c,165:020041dc,169:018001dd,174:0180815c,179:0180015d` |
| `processUICommandApplicationOperate` | `1:0100815c,8:0180415c,13:0180415c,19:0180415c` |
| `processUICommandDefault` | `1:0100819c,10:0180419c,16:0180419c,22:0180419c,32:0180419c,36:0180419c,43:0180419c,49:0180419c,59:0180419c,63:0180419c,69:0180419c,77:0180419c,83:0180419c,93:0180419c,97:0180419c,104:0180419c,114:0180419c,118:0180419c,124:0180419c` |
| `getInputName` | `5:018080dc,12:018080dc,17:018080dc,22:010080dc,28:018080dc` |
| `confirm` | `5:010080dc,9:010080dc,12:0180811c,24:0280415c,37:0280415c,41:018080dc,50:0280411c,60:0280411c,64:020040dc,68:020040dc,71:018040dc,74:010080dc,80:020040dc,84:020040dc,89:020040dc,93:020040dc,98:020040dc,102:020040dc,104:010080dc,109:018040dc,113:018040dc,117:020040dc,121:020040dc` |
| `ignoreFamilyName` | `1:0100805c,5:0100809c,9:0100009d` |
| `isChinese` | `2:0100005d` |

The checker separately compares all 79 conditional word locations (EQ sites)
and every RETURN word, including open returns. It records no inferred callee
body for a dynamic helper. It also pins all 15 `init` JMP destinations
independently; in particular, prototype `root/proto0` PC 127 word
`0x8000c016` targets PC 132. The payload digest and these semantic branch
target checks are separate evidence.

## Local contract

All methods receive the widget as A0. Lua 5.1 encodes B as argument count + 1;
the SELF receiver contributes to that count only when the instruction actually
supplies a receiver. C is result count + 1: C=1 discards results, C=2 keeps one
result, and C=0 preserves an open result tail. `TAILCALL` returns the callee's
selected tail directly.

Here, `western` and `Chinese` describe each individual language-query result,
not one captured locale. For each query, only a first result equal to Boolean
false by Lua equality selects the western branch; any other first result
selects the alternate/Chinese branch.

`init(mode, name, allowNumbers)` creates `work._temp` with fields
`mode:integer8`, `delete:boolean`, `confirm:boolean`, and a `name:string`
declaration carrying width 32. That declaration is metadata; this source does
not prove an input-acceptance limit. It then initializes `confirm=false`,
`name=""`, and mode to the supplied value or 0. It installs the widget's
cancel, close, confirm, application-operate, and tab-command conditions and
makes the widget modal and draggable. Modes 0 and 1 use message 3726, call
`confirm(false)`, then set `delete=false`. Modes 2 and 3 use message 3705,
call `confirm(true)`, set `delete=true`, write help text 3722 or 3724 with the
supplied A2 name, and only then assign `work.name=A2`. Mode 4 uses
message 3714, calls `confirm(true)` before writing help text 3725 and assigning
`work.name=A2`, and does not assign `work.delete`; its Decide branch therefore
reaches the mode-4 invite test only after the earlier `delete==true` test.
Western input configures alphabetic fields and, when `allowNumbers == 1`,
permits digits in the first field. Chinese input hides `Grid_Normal`, sets the
second field text to `!!!`, and copies the accepted-character property from the
third field. The method returns no values.

`setFocus(control)` does nothing for nil or the empty string. Otherwise it
calls `setLogicalFocus(control)`, reads the current keyboard-focused widget
from `desktopWidget`, and calls `setKeyboardFocusedControl(control)` only when
Lua `==` equality says that object equals the naming widget. The finite checks
pin raw object identity for this comparison; they do not prove metatable
`__eq` behavior. It returns no values.

`processUICommandClose` requests `desktopWidget.closeWidgetDirect(self)` with
CALL C=1, so the request's result is discarded and the method returns no
values. `processUICommandCancel` handles `Button_Cancel`: delete mode, mode 4,
and the ordinary non-confirmed path tail-call close; a confirmed ordinary path
tail-calls `confirm(false)`. Any other control tail-calls
`setFocus("Button_Cancel")`.

`processUICommandOperate` handles `Button_Cancel` with the same close or
confirm-false paths. For `Button_Decide`, delete mode obtains the dynamic
parent, sets its border and operation 21, then tail-calls close of self when
the parent exists, preserving the close result tail. Mode 4 calls
`desktopWidget.executePlayerPartyInviteByName(work.name)`; only a true local
return permits border reset and a tail-call close request for the parent,
preserving that result tail. The source does not prove invite acceptance or
server settlement. If the parent operation-21 request throws, the preceding
border request remains and the close call is not reached.

For other modes, an unconfirmed western form tests the exact Lua guards
`first ~= ""`, `second ~= ""`, and, on the fallback path,
`ignoreFamilyName() ~= 0`; these are comparisons, not truthiness tests, so nil
or false differs from the compared string or number. The values returned by
`getInputName` are not always both read: first is read and tested with exact
Lua `first ~= ""`; only when that succeeds is second read and tested with
exact Lua `second ~= ""`. If both differ from `""`, the method tail-calls
`confirm(true)`. If that pair test does not succeed, including `second == ""`,
it evaluates `ignoreFamilyName() ~= 0`; only if that comparison succeeds does
it freshly read first, compare that value with `~= ""`, and tail-call
`confirm(true)` when the fresh comparison also succeeds. An unconfirmed Chinese
Decide path tests `getInputName(3) ~= ""`
and then tail-calls `confirm(true)`. A confirmed western form freshly calls
`ignoreFamilyName()` and then freshly
reads the first input; if family names are not ignored it freshly reads the
second input and concatenates `first .. " " .. second`. It submits the result
to the dynamic parent with operation 31, then tail-calls
`desktopWidget.closeWidgetDirect(self)`, preserving that close call's result
tail. A confirmed Chinese form submits `third .. " " .. second` with operation
31 and likewise tail-calls close. Thus an earlier validation read does not
guarantee a later confirmation read. Missing parents and failed local
predicates return no values. These are client-side validation and local request
boundaries, not accepted names or friend-list mutation.

`processUICommandApplicationOperate` advances western Name -> Name_2 and
Name_2 -> Decide; Chinese Name_3 -> Decide. Other controls are ignored.
`processUICommandDefault` queries `isChinese()` first and applies these exact
maps. Western TabNext is Name -> Name_2, Name_2 -> Decide, Decide -> Cancel,
and Cancel -> Decide when `work.confirm` is true or Name otherwise. Western
TabPrevious is Name -> Cancel, Name_2 -> Name, Decide -> Cancel when confirmed
or Name_2 otherwise, and Cancel -> Decide. Chinese TabNext is Name_3 -> Decide,
Decide -> Cancel, and Cancel -> Decide when confirmed or Name_3 otherwise.
Chinese TabPrevious is Name_3 -> Cancel, Decide -> Cancel when confirmed or
Name_3 otherwise, and Cancel -> Decide. Unknown controls or commands do
nothing. Its focus changes are local requests.

`getInputName(2)` reads `TextBox_Name_2`, `getInputName(3)` reads
`TextBox_Name_3`, and all other selectors read `TextBox_Name`. Each call tests
the raw value with exact Lua `~= ""`; nil and false also differ from the empty
string. When that comparison succeeds, the call queries its own `isChinese()`
result: a Boolean false passes the raw value to `desktopWidget.convertNameText`,
while any other result returns the raw value unchanged. When the comparison is
false (the exact empty string), it returns that value without the language
query. The finite evaluator does not substitute Python truthiness or Lua
coercion/metamethod behavior for nil, false, or non-string converter values.

`confirm(true)` sets `work.confirm=true` before reading inputs or constructing
help text. Its first `self.isChinese()` query selects help construction: only
a Boolean false selects the western `getInputName()` and `getInputName(2)`
path; any other result selects the alternate `getInputName(3)` path. It writes
help text 3721 for mode 0 or 3723 for mode 1 using that path's names, shows
`Grid_Help`, hides `Grid_TextBox`, and focuses Cancel. It then makes a separate
direct `desktopWidget.isChinese()` query for button labels: only Boolean false
selects 1005/1006, while any other result selects 1007/1008. These are
separate queries, not one captured locale, and this contract does not assert a
runtime language change.
`confirm(false)` hides `Grid_Help` without clearing its contents, shows the text
grid, focuses Name or Name_3, and sets button content 3727/3728. It returns no
values.

`ignoreFamilyName` obtains the dynamic parent. If the parent window name is
`AddressListSubWidget`, it returns numeric zero. For another window it
tail-calls that parent's `ignoreFamilyName`; a missing parent returns zero.
`isChinese` is an open tail-call to `desktopWidget.isChinese`, preserving all
returned values.

## Verification and limits

The finite checker covers the root binding, all 11 method windows, all 145
direct calls, all 79 guard sites, every RETURN word, raw receiver and callable
identity, exact selected argument/result tuples, and 24 independent typed
fixtures. It distinguishes Boolean, numeric, nil, zero, object identity, and
open multiple-result tails. Each selected direct-call sequence is checked in
order with exact cardinality and raw receiver/callable identity; init requests
are checked as one exact ordered sequence with strict value types. The mode-0
init fixture selects 36 root-prototype direct calls and pins their raw
receiver/callable objects before execution. Ten
controls each run an unmutated passing baseline and then reject a paired
corruption: payload CALL-word, root-binding, request-tuple, extra request,
Boolean/numeric request swaps (`True` <-> `1`), receiver-identity, callable-identity,
init-callable-identity, init branch-target, and open-tail-result. Two
expected-error fixtures are exact: a parent operation-21 failure retains the
prior border request and suppresses close, while a nil converter reaches the
bounded unsupported-concat boundary after `confirm(true)` has set state.
The mode-2 baseline checks the resulting delete/confirm/name state and its
message/help requests before the independent init branch-target corruption.

The evaluator intentionally supports only the instructions and values reached
by these fixtures. It does not model arbitrary arithmetic, string coercion,
metamethods, libraries, native rendering, keyboard implementation, persistence,
social mutation, server settlement, or object destruction. A mock true return
from `executePlayerPartyInviteByName` proves only the local branch and exact
request tuple. A close request proves neither completed closure nor lifetime.
Static checks cover the full own word windows, but finite execution visits only
fixture-reached paths and does not claim complete instruction or branch
coverage. Representative source-only or unvisited paths include missing-parent
returns in operate, TabPrevious mappings in the default handler, the western
ignore-family fallback, and mode-3/mode-4 initialization setup.
The helper-error and nil-converter cases prove bounded request-prefix and
suppression behavior only; they do not prove native exception text or native
unwinding.
Dynamic helper/class/parent bindings remain conditional on the actual objects
and callables supplied at runtime; labels and owner-name pairs are not identity.
Exact parent class/receiver identity and actual object lifetime require separate
evidence.

## Reproduction

Use a plain `<scratch>` directory for every output and route temporary files
there. With the pinned source LPB and public tools available, run:

```powershell
python tools/retail_script.py `
  --input <client>/client/script/n1635q/966s5rry1rqw9x1w3n1635q.le.lpb `
  --jar tools/vendor/unluac/unluac_2025_12_23.jar `
  --decoded-out <scratch>/addresslistnamingwidget.decoded.luac `
  --script-out <scratch>/addresslistnamingwidget.reproduced.lua
java -jar tools/vendor/unluac/unluac_2025_12_23.jar `
  --disassemble --output <scratch>/addresslistnamingwidget.disassemble.txt `
  <scratch>/addresslistnamingwidget.decoded.luac
```

Inspect `root/proto0` through `root/proto10`, the root binding PCs above, and
each direct-call PC in the method table. For every selected word, the decoded
offset is the prototype code offset plus four times its PC. The retained finite
checks use independent typed expectations and paired baselines, but this public
decoder replay does not claim native or server behavior.
