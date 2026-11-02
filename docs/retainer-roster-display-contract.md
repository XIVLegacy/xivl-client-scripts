# RetainerListWidget local display helpers

`lua/scripts/widget/retainerlistwidget.lua` contains local form-name, label,
status-icon, visibility and event-mode helpers. The eighteen selected methods
below describe Lua calls, field accesses and returns. Compositions require
the pinned local callable and normal completion of intervening accesses and
calls. UI setters remain requests; these instructions do not establish native
storage, rendering, focus, lifetime, incoming roster identity, employment,
ward deployment, ownership or server acceptance.

The [incoming roster source](bazaar-retainer-client-contracts.md#in-game-retainer-roster-source)
and [bell list selection](bazaar-retainer-client-contracts.md#summoning-bell-roster-selection)
own their separate group, ordinal and selection findings. These display
helpers do not bind an incoming group producer or a historical ward result.

## Resource identity

- LPB `n1635q/s5q91w5sy1rqn1635q.le.lpb`, 7004 bytes, SHA-256
  `D7C9313319B1D9A1F9A9B8A9E595EE8E8280050BD249456881C12D97D2F4EA84`:
  `manifests/retail_lua_coverage.json:27408-27420`.
- Decoded payload, 6991 bytes, SHA-256
  `FE3E8DD4D738B61564443B6C1E06D28804D19FF6293EB49FB01F8E4A6C1D7CE8`.
- Canonical LF source, 15897 bytes and 785 lines, SHA-256
  `2FED45C238CFF0302968882C75E707943E9C5E01149E6A28504C95AE70D84DA5`:
  `manifests/scripts.json:15837-15840`.
- Class/base/method inventory: `lua/registry.json:43372-43410` and
  `xivl-client-structs:manifests/lua_api_contract.json:184708`, the
  `scriptDeclarations` entry for `widget/retainerlistwidget`.

The source manifest's `pipeline` field records the corpus extraction path.
The following pinned tools are reproduction inputs; their identities do not
establish which versions produced the retained products:
`tools/retail_script.py`, SHA-256
`765327CF3DA90AACF8E36B185CE53AA0615F7705E9F9CCDC3A7243E3B6C0C391`,
and `tools/vendor/unluac/unluac_2025_12_23.jar`, 796256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`.
Instruction operands and offsets use
`tools/build_quest_contracts.py:ChunkReader` and `instruction`.

## Modal and name helpers

`setInitialData(self,value)` requests `self.setModal(self,value)`, forwarding
the argument without a truthiness or exact-Boolean test. It discards all
results and returns zero values. Its name does not establish invocation or
widget initialization.

`getFormItemName(self,index)` returns one result from concatenating
`"Item_RetainerSelect" .. index`. There is no tostring call or range guard.
Ordinary string and numeric operands concatenate; nil and Boolean operands
fail ordinary concatenation before a return. Metamethods and unsupported
coercions remain outside this contract.

The following getters make no calls and return exactly two literal strings:

| Getter | First result | Second result |
| --- | --- | --- |
| `getStatusName` | `Label_State` | `Content` |
| `getNickNameTitleName` | `TextBlock_NicknameTitle` | `Text` |
| `getNickNameName` | `TextBlock_Nickname` | `Text` |
| `getLvNameTitle` | `TextBlock_RaceTitle` | `Text` |
| `getLvName` | `TextBlock_Race` | `Text` |
| `getLocationTitleName` | `TextBlock_LocationTitle` | `Text` |
| `getLocationName` | `TextBlock_Location` | `Text` |

## Name, level and location requests

`setRetainerName(self,row,retainerId,name)`,
`setRetainerLevel(self,row,level)`,
`setRetainerLocation(self,row,location,area)` and
`setRetainerCondition(self,row,status)` first return zero values if either
of their first two explicit arguments equals nil or the empty string. They
do not use a Boolean truthiness guard: zero and false pass those comparisons.
Later concatenation or other operations can still fail for an unsupported
argument. All ordinary completed setter paths return zero values.

The name setter captures one form-name result and two results from each
nickname getter. It calls `tostring(6302)` and prefixes the first result with
`"@"`. It separately evaluates `"retainerId_" .. tostring(row) .. "[" ..
tostring(retainerId) .. "]"`; that local string is not passed to the property
requests. Both conversions still execute. The method then requests:

1. `_setProperty(self,form,titleControl,titleProperty,titleText)`.
2. `_setProperty(self,form,nameControl,nameProperty,name)`.

With the pinned getters and ordinary tostring, the title request uses
`TextBlock_NicknameTitle`, `Text` and `@6302`, and the name request uses
`TextBlock_Nickname`, `Text` and the original name value.

The level setter follows the same request order with the level getters,
`tostring(6307)` and an unused `"level_" .. tostring(row) .. "[" ..
tostring(level) .. "]"` local string. The title request uses the constructed
title text. The second request forwards the original level, including false
or zero, to the value control. The pinned getter literals are
`TextBlock_RaceTitle` and `TextBlock_Race`, both with property `Text`.

The location setter captures the form, title pair and value pair, then
requests the first result of `packTextParameter(self,6304)`. It supplies that
result to `_setProperty(self,form,titleControl,titleProperty,packed)` and
requests `setText(self,form .. ":" .. locationControl,6314,area,location)`.
The pinned value getter supplies `TextBlock_Location`; its second result is
not used by the text request. The packed result and text format do not prove
text resolution, a zone identity or native application.

Each method call performs its own SELF lookup. Each tostring call instead
performs a fresh global lookup, independently of a `self.tostring` member.
Getter results stay captured across later callbacks. A callback can change
the callable used by a later lookup; a callable already captured for a call
remains distinct from its actual SELF receiver.

## Condition icon requests

After its input guards, `setRetainerCondition` captures the form-name result
and requests two results from `getStatusName`. It does not use that returned
pair in the subsequent requests. The following exact numeric comparisons
select local text-code and icon values:

| Status | Local text code | Icon |
| ---: | ---: | ---: |
| 1 | 6301 | 266 |
| 2 | 6310 | 267 |
| 3 | 6311 | 200 |
| 4 | 6312 | 201 |
| 5 | 6313 | 202 |

Statuses 0 and 101, other unmatched ordinary values and Boolean true or false
leave icon zero. The text-code local is not passed to a text/property setter
in this method. It supplies no independent status meaning.

For a nonzero icon, the method requests `setIcon` for
`form .. ":IconControl_State"`, then `setVisibility` for that control with
literal true. It next requests `setHelpParameter` with arguments `(control,1,
textId)` for `IconControl_State/75602`, `Grid_Race/75603` and
`Grid_Location/75604`, each prefixed by `form .. ":"`. With icon zero it
instead requests only `setHidden(self,form .. ":IconControl_State")` after
the getter calls. No text setter, help clearing or accepted roster-state
transition follows from that path.

## List visibility and event mode

`setRetainerListMax(self,count)` compares numeric `0 < count`. It requests
`setInfomation(self,true)` when that comparison succeeds and
`setInfomation(self,false)` otherwise, discarding all results. It does not
assign a maximum or row count. Ordinary nil/Boolean relational operands fail
before that request; native coercion and metamethods remain unmodeled.

`setEventMode(self,value)` preserves only exact literal true. Every other
value becomes literal false, then the method attempts
`self.work.eventMode = value` and returns zero values.
`getEventMode(self)` freshly accesses `self.work.eventMode` and returns
exactly one value, including nil. The access does not establish persistence
or installation of the work object.

`setListItemVisible(self,index,visible)` first constructs
`"Item_RetainerSelect" .. index`. Its subsequent guard is the conjunction
`index < 0 and 8 < index`. No finite ordinary number satisfies both tests,
so ordinary numeric values such as -1 and 9 still request
`setVisibility(self,constructedName,visible)` and return one literal true.
The visible argument is forwarded unchanged, including nil. This guard does
not establish a usable row range. Concatenation and relational type failures
can precede the request, and the statically emitted false return does not
prove an ordinary numeric rejection case.

`setInfomation(self,value)` branches only on exact literal false. That value
requests `setVisibility(self,"ListBox_Retainer",false)` followed by
`setVisibility(self,"TextBlock_Message",true)`. Every other value, including
nil and zero, requests true for the list and false for the message. Both
normal paths return one literal true. The second setter is looked up after
the first call, so it can use a replacement callable while retaining the
actual self argument.

## Instruction records

The ledger contains direct children 1, 4-11, 13-17 and 21-24 only. Each has
zero nested children. The root's selected CLOSURE/SETTABLE words identify
source-level binding attempts, without runtime installation evidence.
Prototype PCs are zero-based; arity includes the receiver. Byte offsets name
the first and last instruction-word starts in the decoded payload. The last
word occupies three additional bytes. LF windows include both endpoint lines
and the terminating LF.

| Method | Proto | LF lines | Debug lines | Arity | Stack | Words | First/last word starts | Root SETTABLE PC/offset | Window SHA-256 |
| --- | ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| `setInitialData` | 1 | 162-170 | 160-162 | 2 | 5 | 4 | 2315/2327 | 12/80 | `485B5C7DB1050B49102C5050C671DBCC07940EA9DB78A47B6B102141DC9C8F0F` |
| `getFormItemName` | 4 | 284-292 | 251-253 | 2 | 4 | 5 | 3234/3250 | 21/116 | `CBE6BF9BD65612A235C8D7C931C5E36190F06E76BC0E4BCC3C87DCDC3675D765` |
| `getStatusName` | 5 | 295-302 | 261-263 | 1 | 3 | 4 | 3319/3331 | 24/128 | `26777D013D81CF6A77F5C923FF5D6C5E4EED7B0AE8584454F9BA4BD60B19C6B2` |
| `getNickNameTitleName` | 6 | 305-312 | 271-273 | 1 | 3 | 4 | 3405/3417 | 27/140 | `7474FBB3D042AE215DE048FAE0183F0D7F3B78BD8CAA2186CED232354545BAAC` |
| `getNickNameName` | 7 | 315-322 | 281-283 | 1 | 3 | 4 | 3500/3512 | 30/152 | `16E4032925DE65178304B05E564E0963209122A06C3D5266D7DFB0C5D612EC14` |
| `getLvNameTitle` | 8 | 325-332 | 291-293 | 1 | 3 | 4 | 3590/3602 | 33/164 | `BF0C409EA0FF329523173266A63547135CEAAB87C144799F866765AB077515AC` |
| `getLvName` | 9 | 335-342 | 301-304 | 1 | 3 | 4 | 3681/3693 | 36/176 | `13F7A0C970BFB73ED79FD8B790F2C05F9BE4565461323828237B346AD2510888` |
| `getLocationTitleName` | 10 | 345-352 | 311-313 | 1 | 3 | 4 | 3767/3779 | 39/188 | `654EB974EA27D3F6D4BCBC88F10F64CC03491554539D2828412A4EB880634868` |
| `getLocationName` | 11 | 355-362 | 321-323 | 1 | 3 | 4 | 3862/3874 | 42/200 | `964CF8A1EE91D8215D57B5058DA46DEB72A77F5FB73FA2CAD3660F6E5585E387` |
| `setRetainerName` | 13 | 403-452 | 373-400 | 4 | 17 | 45 | 4230/4406 | 48/224 | `9310D34358EF9A39568475B0EFC6A5730EBC2723DC58D13EAF19E06326EE821E` |
| `setRetainerLevel` | 14 | 455-504 | 411-435 | 3 | 16 | 45 | 4604/4780 | 51/236 | `7AD017A75E2E9B6F3DC93407C13490A451D309D9BFBDE34D9E90ED9D84CB360D` |
| `setRetainerLocation` | 15 | 507-548 | 447-473 | 4 | 16 | 36 | 4961/5101 | 54/248 | `24500FA2FA7A1A77BA2ECCF0D495AFAA52BAAF8F4CCAADC15135A45ABF0F6FD8` |
| `setRetainerCondition` | 16 | 551-658 | 484-562 | 3 | 14 | 99 | 5299/5691 | 57/260 | `08D94C1F4F1C3F3373E272389D74FF8A87DA8586952230ECA15A9633AFA60A78` |
| `setRetainerListMax` | 17 | 661-676 | 572-582 | 2 | 5 | 10 | 6091/6127 | 60/272 | `81BB5645480C28D547C64A46D78DA574A7D62C39E4903CF4FC68D856E1459229` |
| `setEventMode` | 21 | 713-722 | 641-648 | 2 | 3 | 6 | 6467/6487 | 72/320 | `1AC24230F62FA95BAC4997F021BBD625380AE31A431B27932481085554AEE469` |
| `getEventMode` | 22 | 725-732 | 657-660 | 1 | 2 | 4 | 6558/6570 | 75/332 | `349C90ACE02DEDA5FE92584A48331AD0EB7BC6723F471E9B77ED536C60918F49` |
| `setListItemVisible` | 23 | 735-753 | 670-686 | 3 | 8 | 16 | 6639/6699 | 78/344 | `344E11A6C813CCC5FCF7A3AE62181D18A56D295965172B5C3F1DC0D0B221CAFF` |
| `setInfomation` | 24 | 756-785 | 696-715 | 2 | 6 | 22 | 6805/6889 | 81/356 | `8A1469FC244EB51590A7D2D9012B5DB01D35D53E86BC4720C1B327FD6A15989B` |

### Direct-call operands

Every direct CALL has fixed B and C operands. R(A) holds the captured
function; R(A+1) through R(A+B-1) are the complete actual arguments.
SELF contributes the actual receiver to that vector. GETGLOBAL does
not supply a receiver. A request consumes C-1 results, padding short
returns with nil and truncating longer returns. C=1 discards all results.
There is no open result tail, TAILCALL or numeric loop in these methods.

| Method | CALL PC/offset | A/B/C | Function capture PC/op/key | Argument registers | Results |
| --- | --- | --- | --- | --- | ---: |
| `setInitialData` | 2/2323 | 2/3/1 | 0/SELF/`setModal` | R3,R4 | 0 |
| `setRetainerName` | 12/4278 | 4/3/2 | 10/SELF/`getFormItemName` | R5,R6 | 1 |
| `setRetainerName` | 14/4286 | 5/2/3 | 13/SELF/`getNickNameTitleName` | R6 | 2 |
| `setRetainerName` | 16/4294 | 7/2/3 | 15/SELF/`getNickNameName` | R8 | 2 |
| `setRetainerName` | 20/4310 | 10/2/2 | 18/GETGLOBAL/`tostring` | R11 | 1 |
| `setRetainerName` | 25/4330 | 11/2/2 | 23/GETGLOBAL/`tostring` | R12 | 1 |
| `setRetainerName` | 29/4346 | 13/2/2 | 27/GETGLOBAL/`tostring` | R14 | 1 |
| `setRetainerName` | 37/4378 | 11/6/1 | 32/SELF/`_setProperty` | R12,R13,R14,R15,R16 | 0 |
| `setRetainerName` | 43/4402 | 11/6/1 | 38/SELF/`_setProperty` | R12,R13,R14,R15,R16 | 0 |
| `setRetainerLevel` | 12/4652 | 3/3/2 | 10/SELF/`getFormItemName` | R4,R5 | 1 |
| `setRetainerLevel` | 14/4660 | 4/2/3 | 13/SELF/`getLvNameTitle` | R5 | 2 |
| `setRetainerLevel` | 16/4668 | 6/2/3 | 15/SELF/`getLvName` | R7 | 2 |
| `setRetainerLevel` | 20/4684 | 9/2/2 | 18/GETGLOBAL/`tostring` | R10 | 1 |
| `setRetainerLevel` | 25/4704 | 10/2/2 | 23/GETGLOBAL/`tostring` | R11 | 1 |
| `setRetainerLevel` | 29/4720 | 12/2/2 | 27/GETGLOBAL/`tostring` | R13 | 1 |
| `setRetainerLevel` | 37/4752 | 10/6/1 | 32/SELF/`_setProperty` | R11,R12,R13,R14,R15 | 0 |
| `setRetainerLevel` | 43/4776 | 10/6/1 | 38/SELF/`_setProperty` | R11,R12,R13,R14,R15 | 0 |
| `setRetainerLocation` | 12/5009 | 4/3/2 | 10/SELF/`getFormItemName` | R5,R6 | 1 |
| `setRetainerLocation` | 14/5017 | 5/2/3 | 13/SELF/`getLocationTitleName` | R6 | 2 |
| `setRetainerLocation` | 16/5025 | 7/2/3 | 15/SELF/`getLocationName` | R8 | 2 |
| `setRetainerLocation` | 19/5037 | 9/3/2 | 17/SELF/`packTextParameter` | R10,R11 | 1 |
| `setRetainerLocation` | 25/5061 | 10/6/1 | 20/SELF/`_setProperty` | R11,R12,R13,R14,R15 | 0 |
| `setRetainerLocation` | 34/5097 | 10/6/1 | 26/SELF/`setText` | R11,R12,R13,R14,R15 | 0 |
| `setRetainerCondition` | 14/5355 | 5/3/2 | 12/SELF/`getFormItemName` | R6,R7 | 1 |
| `setRetainerCondition` | 16/5363 | 6/2/3 | 15/SELF/`getStatusName` | R7 | 2 |
| `setRetainerCondition` | 64/5555 | 9/4/1 | 59/SELF/`setIcon` | R10,R11,R12 | 0 |
| `setRetainerCondition` | 70/5579 | 9/4/1 | 65/SELF/`setVisibility` | R10,R11,R12 | 0 |
| `setRetainerCondition` | 77/5607 | 9/5/1 | 71/SELF/`setHelpParameter` | R10,R11,R12,R13 | 0 |
| `setRetainerCondition` | 84/5635 | 9/5/1 | 78/SELF/`setHelpParameter` | R10,R11,R12,R13 | 0 |
| `setRetainerCondition` | 91/5663 | 9/5/1 | 85/SELF/`setHelpParameter` | R10,R11,R12,R13 | 0 |
| `setRetainerCondition` | 97/5687 | 9/3/1 | 93/SELF/`setHidden` | R10,R11 | 0 |
| `setRetainerListMax` | 4/6107 | 2/3/1 | 2/SELF/`setInfomation` | R3,R4 | 0 |
| `setRetainerListMax` | 8/6123 | 2/3/1 | 6/SELF/`setInfomation` | R3,R4 | 0 |
| `setListItemVisible` | 12/6687 | 4/4/1 | 9/SELF/`setVisibility` | R5,R6,R7 | 0 |
| `setInfomation` | 5/6825 | 2/4/1 | 2/SELF/`setVisibility` | R3,R4,R5 | 0 |
| `setInfomation` | 9/6841 | 2/4/1 | 6/SELF/`setVisibility` | R3,R4,R5 | 0 |
| `setInfomation` | 14/6861 | 2/4/1 | 11/SELF/`setVisibility` | R3,R4,R5 | 0 |
| `setInfomation` | 18/6877 | 2/4/1 | 15/SELF/`setVisibility` | R3,R4,R5 | 0 |

### Verification boundary

The selected 320 instruction words contain 38 direct CALL words.
The original-word fixtures exercise all eighteen selected methods in
72 finite cases with three corruption controls. Every normal result is
checked with recursive typed values. Selected cases also check complete
actual argument vectors, raw callable/receiver/table identity, assignment
attempts, the exact-false/exact-true distinctions, guards, status icons,
out-of-range numeric visibility requests, fixed result padding/truncation
and replacement callables. Ordinary concatenation and relational errors
are checked separately. These are finite mocked paths; native effects,
metamethods and exhaustive inputs remain outside the evidence.
