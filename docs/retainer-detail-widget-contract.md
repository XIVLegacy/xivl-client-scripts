# RetainerDetailWidget local contract

The pinned `RetainerDetailWidget` resource requests eight list rows and fixed
label content. Its wait/result methods read the current `askAnswer` member,
while its command handler returns no values on every local branch. The skill
methods have an omitted-argument arithmetic path described below. These facts
describe a named Lua receiver under supplied inputs; actual roster, opener,
ward, retainer identity and server transaction bindings remain unestablished.

## Resource and original method vectors

The retail LPB is `client/script/n1635q/s5q91w5s65q91yn1635q.le.lpb`,
2466 bytes, SHA-256
`61FC76AC8E620A35E77491D81A0DCB0DE0D8381F4605BD15357A8F88992E8127`.
The `tools/retail_script.py` route and pinned
`tools/vendor/unluac/unluac_2025_12_23.jar` (796256 bytes, SHA-256
`98BE0FA84AC73CA66DCE2842A2E4512226F4C611B6500DC96415571FC5538FCC`)
produced a 2453-byte decoded payload, SHA-256
`80630C144587992128B6E362E8D2331E83419715636CDCB69A8177C59CA52B4A`.
The canonical LF source is 5869 bytes and 279 lines, SHA-256
`E253A7BFB56F7A400EACDE3A24AEC20B20930E1F846CB2B02554DEC54AE41FC3`.
Identity records are `manifests/scripts.json:15824-15829` and
`manifests/retail_lua_coverage.json:27362-27376`.

`tools/build_quest_contracts.py:ChunkReader,instruction` parsed the original
Lua 5.1 operands. Prototype indices and PCs are zero-based; offsets are in
the decoded payload. The root has eight direct method prototypes and no
nested helper. Formal arities include self. API navigation is
`xivl-client-structs:manifests/lua_api_contract.json:183635-183757`.

| Method | Arity | Child prototype / code offset / words | LF source | Local results |
| --- | ---: | --- | --- | --- |
| `init` | 1 | `0 / 486 / 42` | 11-60 | Zero values. |
| `setRetainerGroupData` | 5 | `1 / 931 / 65` | 63-133 | One false on any nil data argument; otherwise zero values after calls. |
| `setRetainerBaseData` | 4 | `2 / 1395 / 14` | 136-149 | One false on any nil data argument; otherwise zero values. |
| `setRetainerSkillData` | 9 | `3 / 1549 / 33` | 152-196 | Zero values after all selected helper calls return. |
| `processWaitCallFunction` | 1 | `4 / 1823 / 9` | 199-211 | One boolean from the current-field comparison. |
| `getAskResult` | 1 | `5 / 1933 / 4` | 214-221 | One current-field value, including one nil if that is read. |
| `processUICommandEvent` | 6 | `6 / 2014 / 10` | 224-234 | Zero values on every local branch. |
| `setRetainerSkillDataLine` | 4 | `7 / 2174 / 39` | 237-279 | One false for either upper-bound rejection; one true after the local loop completes. |

Root `pc2/40` calls `require` with `"/Widget/WidgetBaseClass"`; `pc6/56`
calls `_defineClass` with `"RetainerDetailWidget"` and `"WidgetBaseClass"`.
Fresh global lookups, closures and `SETTABLE` instructions attempt the eight
method assignments at PCs 9,12,15,18,21,24,27,30; root `pc31/156`
returns zero values. Those operands do not prove class creation or successful
method installation. Local method compositions below require actual selection
of the pinned closures and normal completion. Lookups, native overrides,
callable objects and metamethods retain their own effects. Call tuples count
explicit Lua arguments; a callable object's `__call` can add an implicit one.

## Initialization and supplied group data

`init` executes the assignment operand `self.work._temp={}` at
`proto0 pc2/494`. The declaration table is empty. The
`xivl-decomp:docs/script/widget-work-members.md:116-174,293-324` contract
owns native work userdata and descriptor behavior; an empty declaration does
not establish a native initial value or later readback for `askAnswer`.

For numeric loop values i=1 through 8, the body makes these calls in order,
where N is the concatenation `Item_RetainerSelect` plus i:

1. `_addItem(self,nil,"ListBox_Retainer","ControlTemplate_ListBoxItem",N)`.
2. `_setProperty(self,N,"TemplateButton_AreaName","Content",<i as text>)`.
3. `_setProperty(self,N,N,"Focusable",false)`.
4. `setItemVisibility(self,nil,i,false)`.

The first three `CALL`s use `B=6,C=1` at `pc18/558`, `pc26/590`,
`pc32/614`; the fourth uses `B=5,C=1` at `pc39/642`. Every result is
discarded, and `pc41/650 RETURN B=1` returns no values. These operands
do not prove that rows were created or properties applied.

`setRetainerGroupData(self,A1,A2,A3,A4)` tests each data argument for nil
at PCs 2,4,6,8. Any nil returns one false at `pc11/975`; false and zero
are not nil. With four nonnil arguments, their values do not supply the
display content. The body issues `Content` and `Visibility="Visible"`
property calls, in that order for each of:

- `Label_State` (`pc18/1003`, `pc24/1027`).
- `Label_Nickname` (`pc31/1055`, `pc37/1079`).
- `Label_Lv` (`pc44/1107`, `pc50/1131`).
- `Label_LocationTytle` (`pc57/1159`, `pc63/1183`).

Each explicit tuple is `(self,nil,label,property,value)`. Every `Content`
value is the same fixed UTF-8 literal, hexadecimal
`E38386E382B9E38388E8A1A8E7A4BA` (code points U+30C6 U+30B9 U+30C8
U+8868 U+793A). Each call has `B=6,C=1`, and `pc64/1187` returns zero
values. No supplied name, level or location value is substituted by this body.

`setRetainerBaseData(self,A1,A2,A3)` likewise returns one false if any data
argument is nil (`proto2 pc9/1431`). Its nonnil path loads local label
strings and returns zero values at `pc13/1447`. It has no explicit property
call or field assignment.

## Skill calls and local arithmetic

`setRetainerSkillData(self,A1,A2,A3,A4,A5,A6,A7,A8)` has eight fixed data
parameters. It performs eight fresh member lookups and calls
`setRetainerSkillDataLine(self,i,Ai)` for i=1 through 8. CALL PCs are
3,7,11,15,19,23,27,31 at offsets 1561 through 1673, each `B=4,C=1`.
Thus each call has three explicit arguments including self, and discards all
results. The final `pc32/1677` returns zero values after normal completion.

The pinned line method has three data formals:
`setRetainerSkillDataLine(self,line,base,added)`. It returns one false if
`8 < line` or `8 < base` (`proto7 pc0/2174`, `pc4/2190`, false returns
at `pc3/2186`, `pc7/2202`). There is no explicit lower-bound test.
Its numeric loop runs i=1 through 8. When `base <= i`, the selected arm is
empty. Otherwise `pc31/2298 ADD` computes `base+added`, followed by the
comparison at `pc32/2302`; both arms of that latter comparison are empty.
The body forms `Label_Basic_i`, `Label_Added_i` and `Label_Blank_i` strings,
without an explicit `CALL` or `SETTABLE`, then returns one true at
`pc37/2322` after loop completion. Its final zero-result epilogue is
unreachable through these normal branches.

When the eight calls actually select that pinned line closure, the omitted
`added` formal is nil. For example, `line=1,base=1,added=nil` reaches the
true return without `ADD`; `line=1,base=2,added=nil` reaches `ADD` in the
first iteration. Ordinary number-plus-nil arithmetic then raises an error
unless an applicable arithmetic metamethod handles it. Supplying numeric
`added=0` permits that local arithmetic path to finish. No native skill
application or historical error observation follows from these local paths.

## Wait, result and command handling

`processWaitCallFunction` freshly reads `self.work.askAnswer` and returns
the result of `~= 0`: only numeric zero returns false, while nil, false,
true, 1 and -1 return true (`proto4 pc2/1831`, returns `pc5/1843`,
`pc7/1851`). `getAskResult` independently reads the current member and
returns exactly one value at `proto5 pc2/1941`. Its read need not equal
an earlier read, and these methods do not initialize the field.

`processUICommandEvent(self,A1,control,command,A4,A5)` checks
`"UILuaCommands.Cancel"`, then `"TemplateButton_Answer"` with
`"UILuaCommands.Operate"`. Those branches and the fallback return zero values
at `proto6 pc2/2022`, `pc7/2042`, `pc8/2046`. The method contains no
explicit call or field write. In particular, it supplies no local
`askAnswer` producer or completed close operation.

Property application, rendered output, group/member identities, actual
callback dispatch, field writers, lifetime, retainer/ward deployment and
server outcomes require their own evidence beyond this local resource.
