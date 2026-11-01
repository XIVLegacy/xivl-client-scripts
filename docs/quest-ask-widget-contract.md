# QuestAskWidget local interaction contract

`QuestAskWidget` is the local presentation and result-request widget used by
the published `QuestBaseClass.showQuestInfomation` fallback route. This page
describes only the five methods recovered from the admitted retail Lua
resource. It does not establish quest acceptance, completion, payout, journal
retirement, server acknowledgement, or rendered output.

## Evidence and method bindings

The source is the 1.23b extraction `2012.09.19.0001` resource
`n1635q/9rz/tp5rq9rzn1635q.le.lpb`, 3,271 bytes, SHA-256
`55F948982F586395FA539D8B4E83F3AB14A532EE84A328573B9F06501A4449E3`.
The wrapper decoder yields 3,258 bytes with SHA-256
`4F2FC50E4C186E96974FE134F0D9E7E58825B88CE7F33C0CE1F6459351A674E5`.
The pinned unluac output, canonicalized only from CRLF pairs to LF, is 5,518
bytes, 274 lines, SHA-256
`424A132C1C37B7998B3BBE380C62FBC28377CC414BE9DAB7F47A050752F29034`.
These identities are recorded in
`manifests/retail_lua_coverage.json:26733-26745` and
`manifests/scripts.json:15105-15108`. The method names, fixed arities, and
source windows are pinned in
`xivl-client-structs:manifests/lua_api_contract.json:151545-151620`; these are
LF-decompile windows, distinct from the original chunk's line-defined metadata.
The decompiler is the repository-pinned
`tools/vendor/unluac/unluac_2025_12_23.jar`, 796,256 bytes, SHA-256
`98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc`.

The root requires `/Widget/Ask/AskBaseClass`, defines
`QuestAskWidget` over `AskBaseClass`, and binds exactly five child prototypes:

| method | fixed arity | LF-decompile window | prototype | code start |
| --- | ---: | --- | --- | ---: |
| `initAsk` | 2 | lines 11 / 92 | `root/proto0` | 366 |
| `processUICommandOperate` | 5 | lines 95 / 110 | `root/proto1` | 1165 |
| `processUICommandCancel` | 5 | lines 113 / 121 | `root/proto2` | 1334 |
| `getQuestAskIconID` | 2 | lines 124 / 202 | `root/proto3` | 1421 |
| `getQuestCategory` | 2 | lines 205 / 274 | `root/proto4` | 2391 |

All prototype PCs and decoded-byte offsets are zero-based. Checks use
`ChunkReader.prototype` and `instruction` from
`xivl-client-scripts:tools/build_quest_contracts.py`. The root class binding is
at PC 6 / offset 56; method closures bind at PCs 9, 12, 15, 18, and 21 / offsets
68, 80, 92, 104, and 116. The child code starts are 366, 1165, 1334, 1421,
and 2391 for the five rows above. `initAsk` calls are at PCs 5, 8, 13, 19,
20, 25, 30, 34, 38, 42, 46, 50, 54, 59, and 61, with its zero-value return
at PC 62; operate compares at PCs 0 and 6, calls at 4 and 10, and returns at
11; cancel calls at PC 2 and returns at 3. Icon paired comparisons start at
PCs 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96,
and 102, with one-value returns at 5, 11, 17, 23, 29, 35, 41, 47, 53, 59,
65, 71, 77, 83, 89, 95, 101, and 107 plus icon-prototype default LOADK PC 108 /
offset 1853 and RETURN PC 109 / offset 1857.

Category threshold comparisons are at PCs 0, 5, 10, 15, 20, 23, 26, 31, 36,
39, 42, 47, 52,
55, 60, 65, 70, 75, 80, 85, 90, 95, 100, and 105, with one-value returns
at PCs 3, 8, 13, 18, 29, 34, 45, 50, 58, 63, 68, 73, 78, 83, 88, 93,
98, 103, and 108.

## Initialization

`initAsk(self, questID)` makes these local requests in order:

1. Set `self.work._temp` to a new table.
2. Set confirm conditions `Button_Approval` and `Button_Refusal`.
3. Set `TextBlock_QuestTitle` with text row `5001` and `questID`.
4. Resolve `self:getQuestCategory(questID)` and forward all dynamically
   resolved results as the remaining arguments to `TextBlock_ScenarioTitle`
   with text row `4028`. The call forwards all dynamic results. When the
   resolved member is the pinned local `root/proto4` and the ID is supported
   integer input, it supplies one integer; other resolved implementations have
   no result-width or result-value guarantee in this contract.
5. Set `TextBlock_SkillRank` with text row `5302` and `questID`.
6. Set `TextBlock_Client` with text row `5301` and `questID`.
7. Set visibility `false` for `TextBlock_Reward`, `TextBlock_RewardTitle`,
   `Border_RewardBg`, and `Border_RewardIcon`.
8. Call opaque `desktopWidget:getQuestIconID(questID)`. Use its first result in
   `setIcon("IconControl_QuestTitle", iconID)` and its second result in
   `setHelpParameter("IconControl_QuestTitle", 1, helpParameter)`.
9. Set the cancel condition and return zero values.

The four reward flags are literal `false`; this body does not assign nil or a
numeric zero to those controls. The setter calls are requests observed in Lua.
Inherited/native setter implementation, text lookup, icon lookup, help
parameter interpretation, and actual rendering remain outside this contract.

## Operate and cancel

`processUICommandOperate(self, A1, command, A3, A4)` uses receiver `self`,
reads only `command`, and ignores the other event arguments:

| command | local request | method return |
| --- | --- | --- |
| exact `Button_Approval` | `self:setBaseAskResult(1)` | zero values |
| exact `Button_Refusal` | `self:setBaseAskResult(2)` | zero values |
| any other value, including nil | no setter request | zero values |

`processUICommandCancel(self, A1, A2, A3, A4)` uses receiver `self`, ignores
its four non-receiver event arguments, requests `self:setBaseAskResult(2)`,
and returns zero values. These are base-result
setter requests. They do not prove quest acceptance, completion, payment,
inventory mutation, server state, or a later getter value.

## Quest icon ID lookup

For a supported numeric `questID`, `getQuestAskIconID(self, questID)` returns
exactly one integer. The matching ranges are inclusive; all other supported
numeric IDs use the default `295`.

| quest ID | result |
| --- | ---: |
| 110001-110059 | 295 |
| 110060-110079 | 206 |
| 110080-110099 | 203 |
| 110100-110119 | 204 |
| 110160-110179 | 207 |
| 110180-110199 | 205 |
| 110240-110259 | 233 |
| 110260-110279 | 234 |
| 110300-110319 | 212 |
| 110320-110339 | 209 |
| 110360-110379 | 213 |
| 110380-110399 | 211 |
| 110400-110419 | 210 |
| 110420-110439 | 215 |
| 110440-110459 | 214 |
| 110460-110479 | 217 |
| 110480-110499 | 218 |
| 110500-110519 | 219 |
| all other supported numeric IDs | 295 |

This is a pure local numeric ID-to-integer lookup. No getter, native call,
quest-state read, or nil/zero path occurs in the method body.

## Quest category lookup

For a supported integer `questID`, `getQuestCategory(self, questID)` returns
exactly one integer. The empty bytecode `elseif` arms jump to the shared
default path, not to later returned ranges. In `root/proto4`, the shared
default is LOADK PC 109 / offset 2827 followed by RETURN PC 110 / offset 2831;
the true paths
from `<110140`, `<110160`, `<110220`, `<110240`, and `<110300` at PCs 20, 23,
36, 39, and 52 use JMP PCs 22, 25, 38, 41, and 54 to default PC 109; their
false paths use JMP PCs 21, 24, 37, 40, and 53 to the next threshold. The
effective ranges are:

| integer quest ID | result |
| --- | ---: |
| below 110060 | 5 |
| 110060-110079 | 6 |
| 110080-110099 | 7 |
| 110100-110119 | 8 |
| 110120-110159 | 5 |
| 110160-110179 | 9 |
| 110180-110199 | 10 |
| 110200-110239 | 5 |
| 110240-110259 | 11 |
| 110260-110279 | 12 |
| 110280-110299 | 5 |
| 110300-110319 | 13 |
| 110320-110339 | 14 |
| 110340-110359 | 15 |
| 110360-110379 | 16 |
| 110380-110399 | 17 |
| 110400-110419 | 18 |
| 110420-110439 | 19 |
| 110440-110459 | 20 |
| 110460-110479 | 21 |
| 110480-110499 | 22 |
| 110500-110519 | 23 |
| 110520 and above | 5 |

This is also a pure local integer threshold lookup. It has no nil or zero
return path for supported integer IDs.

## Published fallback composition

The published `QuestBaseClass.showQuestInfomation` route invokes a detail
helper for its documented ID ranges and otherwise opens
`Ask/QuestAskWidget` with the supplied ID at
`xivl-client-scripts:docs/guildleve-journal-lifecycle.md:304-316`.
That lifecycle join proves only the widget path, scalar `1`, and supplied ID
at this route; it does not establish an unconditional wrapper selection.
The published Ask wrapper facts at
`xivl-client-scripts:docs/materia-meld-client-contract.md:134-143,159-168`
show that the `1` immediately after the widget path is the one-result request
on the event-mode route. The wrapper
supplies widget category `4` and forwards the remaining data arguments through
`askWidgetYield` and `AskBaseClass.init`.
Its one-result completion behavior is bounded by
`xivl-client-scripts:docs/materia-meld-client-contract.md:196-202`.
For requestedCount `1`, the published wrapper shape is one `false` on failure
and `(true, first actual inherited getAskResult value)` after completed
selection. That shape does not identify this widget's opaque setter request
with a later inherited getter value.

Composition requires both of these prerequisites: the actual published
event-mode wrapper is used, and the actual widget instance follows the
published `AskBaseClass.init` implementation with this pinned
`QuestAskWidget.initAsk` as its resolved target. The published
`QuestBaseClass.showQuestInfomation` fallback page establishes only the
`Ask/QuestAskWidget` path, scalar `1`, and supplied ID; it does not establish
that widget-instance class/init resolution. When both prerequisites hold, the
supplied `questID` reaches this pinned `initAsk`. That body makes the listed
text/icon and confirm/cancel-condition requests. A later invocation of the
pinned operate method requests base result `1` for `Button_Approval` or base
result `2` for `Button_Refusal`; the pinned cancel method requests base result
`2`. The wrapper's lifetime, result consumption, actual close/destruction,
render outcome, and any quest/server transition remain unresolved outside
these five methods.
