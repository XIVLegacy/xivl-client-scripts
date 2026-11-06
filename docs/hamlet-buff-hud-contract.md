# Hamlet buff HUD requests

`HamletDefenseWidget.cmdSetArmyBuff` and `cmdSetEnemyBuff` compare a supplied
value with the value stored for that slot. Equality returns without a UI
request. A changed value selects an opaque numeric icon operand, requests its
visibility, optionally sends a named control command, then stores the supplied
value. These are local HUD requests. They do not identify a gameplay effect or
prove that a status was applied.

The contract below follows the original Lua 5.1 bytecode. The canonical
decompile preserves relevant literals but contains malformed command control
flow, documented [separately](#canonical-source-comparison).

## Sources and identity

The source is extraction `2012.09.19.0001`, decoded path
`lua/scripts/widget/hamletdefensewidget.lua`.
[The reproduction manifest](../manifests/scripts.json), at that path's row,
pins 22,816 bytes, 1,140 lines and SHA-256
`1D2EEE659669ADC83B82B8D7BA58CF799756194DE89CD100AEA09BB8A1F9A440`.
Its header at lines 1-9 requires `/Widget/WidgetBaseClass` and declares
`HamletDefenseWidget` with base `WidgetBaseClass`. This identifies the declared
class, without interpreting the required module or class-construction helpers.

[The decoded corpus manifest](../manifests/private_lua_corpus.json) owns the
archive source declaration at revision
`40006d5d716583d78690a6f3ef50ca1bc41dddee`. Its `lua.zip` is 14,385,427 bytes,
SHA-256 `0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The inspected member is `widget/hamletdefensewidget.lua`. No source body is
redistributed here. [The corpus guide](../lua/README.md) owns canonical
normalization and the source license boundary.

[The retail coverage manifest](../manifests/retail_lua_coverage.json), at the
matching `decodedScriptPath` row, identifies original resource
`n1635q/29xy5q6545wr5n1635q.le.lpb`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| LPB | 10,206 | `882B2B249B3DE84A593E4084E8CB7E49FBB00B3BF4CBD0FC911D1A2814964286` |
| Decoded Lua 5.1 payload | 10,193 | `A564717080911218C718EA28F4A8B604A9850B3F2DB27BCD73ED9CEC93715D9E` |

The manifests were inspected at repository revision
`abdb7db9b7282359ada0518bf4251d9766a2d54a`. The complete archive, canonical
member, LPB and decoded payload identities were checked before method analysis.
Only these seven method bodies and the necessary header/root bindings were
interpreted:

| Method | Original prototype | Instructions | Payload range | Canonical lines |
| --- | --- | ---: | --- | --- |
| `init` | `root/proto0` | 113 | `[0x52A,0x6EE)` | 11-161 |
| `processTimer` | `root/proto1` | 5 | `[0x8B8,0x8CC)` | 164-173 |
| `initArmyBuff` | `root/proto16` | 11 | `[0x170E,0x173A)` | 592-607 |
| `cmdSetArmyBuff` | `root/proto17` | 64 | `[0x179A,0x189A)` | 610-680 |
| `initEnemyBuff` | `root/proto18` | 11 | `[0x19EB,0x1A17)` | 683-698 |
| `cmdSetEnemyBuff` | `root/proto19` | 64 | `[0x1A78,0x1B78)` | 701-771 |
| `setBuffIcon` | `root/proto20` | 16 | `[0x1CCB,0x1D0B)` | 774-796 |

Root PCs 58-60 bind `cmdSetArmyBuff`, PCs 64-66 bind `cmdSetEnemyBuff`, and
PCs 67-69 bind `setBuffIcon` to `HamletDefenseWidget`. Each sequence reads
the class, creates the named child closure, then assigns the method. PCs are
zero-based and byte ranges are half-open decoded-payload offsets. The command
methods have four fixed parameters including `self`; the helper has three.
All three have zero vararg flags, upvalues and child prototypes.

Root PCs 7-9 bind `init`, with its closure at PC 8 and assignment at PC 9.
Root PCs 10-12 bind `processTimer`, PCs 55-57 bind `initArmyBuff`, and
PCs 61-63 bind `initEnemyBuff` in the same way. These four methods each have
one fixed parameter, `self`, and zero vararg flags, upvalues and child prototypes.

## Guard and control selection

The command arguments are `(self, slot, value, unused)`. The fourth fixed
parameter is unused. Army reads `self.work.armyBuff[slot]`; enemy reads
`self.work.enemyBuff[slot]`. If the stored value equals the supplied value,
the command returns zero Lua values immediately. It does not resolve control
names, refresh the icon, send a command or rewrite the stored value.

The guard uses Lua equality. It does not coerce a string such as `"1"` to
numeric 1 or treat false as numeric 0. An absent slot equal to a supplied nil
therefore also returns early. The methods do not initialize `work` or their
buff tables; a failing initial access stops before a UI request.

On the continuing path, the calls occur in this order:

1. `self:getIndexControlName(prefix, slot)`, retaining one result as `label`.
   Army uses `"Label_ArmyBuff_"`; enemy uses `"Label_EnemyBuff_"`.
2. `self:getTemplateControlName(label, "IconControl_Buff")`, retaining one
   result as `control`.
3. `self:setBuffIcon(control, icon)`, using the operand selected below.
4. For a selected command, `self:sendControlCommand(label, command)`.
5. Re-read `self.work.armyBuff` or `self.work.enemyBuff`, then assign
   `[slot] = value`.

Neither naming result has a nil or truthiness guard in these methods. A nil
or false result is passed onward as returned. Extra naming results are
discarded. The icon and control-command call results are also discarded.

## Icon and command operands

The selection starts with icon 0 and no control command. The same slot/value
tests apply to army and enemy; only the numeric operands differ.

| Numeric slot | Supplied value | Army icon | Enemy icon | Control command |
| ---: | --- | ---: | ---: | --- |
| 1 | numeric 1 | 1014 | 1019 | `UILuaCommands.BuffDown` |
| 1 | numeric 3 | 1013 | 1018 | `UILuaCommands.BuffUp` |
| 2 | numeric 1 | 1016 | 1091 | `UILuaCommands.BuffDown` |
| 2 | numeric 3 | 1018 | 1020 | `UILuaCommands.BuffUp` |
| 3 | any value unequal to numeric 2 | 1017 | 1022 | None |
| Any remaining combination | Any | 0 | 0 | None |

The slot-3 condition is inequality with numeric 2, rather than a positive
value test. For example, supplied numeric 0, nil, false and string `"1"` all
select its positive icon when the equality guard did not already return.
Numeric value 2 selects icon 0. Other slots have no positive-icon fallback.
The command strings are literal operands, not a decoded status name, an
animation guarantee or a gameplay rule.

`setBuffIcon(self, control, icon)` compares `0 < icon`. For a positive numeric
operand it calls `self:setIcon(control, icon)`, then
`self:setVisibility(control, true)`. Otherwise it calls only
`self:setVisibility(control, false)`. The zero path does not clear the previous
icon through `setIcon`. A nonnumeric operand fails the comparison before an
effect request. The helper returns zero Lua values and discards its callees'
results.

## Ordering, repeats and errors

The stored value changes only after the icon/visibility requests and optional
control command complete normally. There is no exception handler or rollback.
An error in a naming helper, icon request, visibility request or control-command
request prevents the final assignment. Earlier requests may already have
occurred. An error from `setIcon` also prevents the later visibility call.

The final assignment resolves `self.work` and its buff table again. It does
not retain the table used by the initial guard. If a called method replaces
that table, the final write targets the newly resolved table. If final access
fails, preceding requests are not undone. These are source ordering facts,
without a claim that such replacement occurred in the retail client.

After an ordinary successful call, repeating the same slot/value returns at
the equality guard. It does not reissue the HUD requests. A failed call that
never reached the write has not established that repeat suppression. Both
guard and continuing paths return zero Lua values, distinct from returning
one nil value.

## Initial declaration and reset ordering

`init(self)` resolves `self.work`, constructs a fresh Lua declaration list and
nine fresh row tables, then assigns the list to `_temp` on that resolved work
object (canonical lines 11-89).
These are its only direct Lua table allocations. The descriptor rows and
subsequent assignment operands are:

| Member | Declaration operands after the name | Direct assignment |
| --- | --- | --- |
| `contentId` | `"integer32"` | -1 |
| `hamletRank` | `"integer32"` | -1 |
| `hasGatheringItem` | `"array", 9, "integer8"` | Slots 1-9: -1 |
| `defenseLineStatus` | `"array", 3, "integer8"` | Slots 1-3: -1 |
| `goodsStatus` | `"array", 4, "integer8"` | Slots 1-4: -1 |
| `goodsKindTarget` | `"integer8"` | -1 |
| `bossStatus` | `"boolean"` | false |
| `armyBuff` | `"array", 3, "integer8"` | Slots 1-3: -1 |
| `enemyBuff` | `"array", 3, "integer8"` | Slots 1-3: -1 |

Assignments follow that row order at canonical lines 90-138, with numeric
slots increasing within each array. Each assignment resolves `self.work`
again. Each array iteration also resolves the named member again before
writing its slot. The method does not directly construct `self.work` or the
five array members. With authored plain tables, assigning `_temp` alone does
not create them, and a missing member stops at its first indexed assignment.
That fixture behavior does not establish a missing allocation in the retail
client.

The adopted native account in
`xivl-decomp:docs/script/widget-work-members.md`, sections "Member names and
owners", "Read and write routing" and "Declaration vocabulary", at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, describes own-class `work` as a
conditionally created native work object. Its `_temp` write routes through
`0x00D175B0 -> 0x00D16610 -> 0x00D1E0F0`. The selected registry node and
factory remain conditions. Thus these declarations and assignment operands
do not prove installed native array storage or its initial values.

For the ordinary selected factories and a running bit start of zero for this
declaration, the published width and alignment rules give this relative layout:

| Member | Relative bit start | Width in bits |
| --- | ---: | ---: |
| `contentId` | 0 | 32 |
| `hamletRank` | 32 | 32 |
| `hasGatheringItem` | 64 | 72 |
| `defenseLineStatus` | 136 | 24 |
| `goodsStatus` | 160 | 32 |
| `goodsKindTarget` | 192 | 8 |
| `bossStatus` | 200 | 1 |
| Alignment padding | 201 | 7 |
| `armyBuff` | 208 | 24 |
| `enemyBuff` | 232 | 24 |

The declaration spans 256 bits, or 32 bytes, under those assumptions. Each
buff declaration has capacity three `integer8` elements. The one-bit Boolean
leaves bits 201-207 for byte alignment before `armyBuff`. These are
declaration-relative positions. The actual pool, class-level base, installed
storage, allocation, registry selection and lifetime remain unbound.

The composition adopts `xivl-decomp:docs/script/job-action-acquisition.md`,
"Native boolean layout": `0x00D243E0` reads count/type operands 3/4,
`0x00D259E0` multiplies count by child width, and
`0x00D1E59F..0x00D1E5CD` aligns and advances the running bit position.
That page is pinned at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, SHA-256
`66eadd0bf48108a84c17eb73b8361cfbea4f8837e9ff73f0149da9599e4dc130`.
The 32/8/1-bit widths for `integer32`/`integer8`/`boolean` come from
`xivl-client-structs:docs/work-binder-native-contract.md`, "Member widths",
at revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`, SHA-256
`199234a32f4dc3dd8e798c8c9c1aeb8f284afedb52bc40dfa169c3ca2a6ff819`.

After those direct assignments, `init` resolves and calls, in order,
`self:initTitle()`, `self:initTimer()`, `self:initDefenseLineStatus()`,
`self:initGoodsStatus()`, `self:initArmyBuff()`, `self:initEnemyBuff()` and
`self:initGatheringItem()` (canonical lines 139-158). Each call has only `self`
as receiver and no explicit arguments. All results are discarded, and normal
completion returns zero Lua values. A failing lookup, assignment or call
stops before later operations, without undoing earlier effects.

The army and enemy slots receive direct -1 assignments before any of those
method requests. If the dynamic reset and command bindings select the
implementations described here, and earlier calls leave the required storage
usable, each reset subsequently requests numeric 2 for its three slots.
Visibility and the final stored value still depend on the command completing
normally. This ordering does not prove that a retail caller invoked `init` or
that native UI effects occurred.

The unmodified canonical initializer parsed under Lua 5.4.8. Against authored
work/member proxies and method stubs, its direct assignments, fresh reads,
declaration-table identities, ordered calls and failure prefixes agreed with
focused original Lua 5.1 instruction replay. Independent literal expectations
and rejecting controls cover the descriptor, slot, sentinel, receiver, arity,
result-width and read-order distinctions. This finite comparison does not
execute the retail client or a native declaration factory.

## Cache reset and timer requests

`initArmyBuff(self)` calls `self:cmdSetArmyBuff(slot, 2, 0)` for numeric slots
1, 2 and 3 in that order. `initEnemyBuff(self)` does the same through
`self:cmdSetEnemyBuff`. Each iteration resolves the method on `self` again.
The methods discard all call results and return zero Lua values after the
third call. A lookup or call error stops the loop before later slots, without
undoing earlier effects.

These are reset requests through dynamic command bindings. Neither initializer
directly accesses `work`, constructs or replaces a table, or writes a cache
slot. If those bindings select the command methods described above and the
required work tables exist, a slot already equal to numeric 2 returns without
a request. Otherwise the command selects icon 0, requests visibility false,
sends no control command and stores numeric 2 after the requests succeed.
The literal fourth argument 0 is the command's unused parameter. This
conditional composition does not initialize missing work tables or prove
which method implementation was bound during a retail invocation.

`processTimer(self)` resolves the global `desktopWidget`, then its
`closeWidgetDirect` method, and calls it with that desktop object as receiver
and `self` as its sole explicit argument. It discards every callee result and
returns zero Lua values. There is no local guard or exception handler. A
global/method lookup or call failure propagates. This is a direct close
request, without a local cache reset or refresh request.

The three canonical bodies parsed successfully under Lua 5.4.8. Against
authored stubs, their ordered call tuples, fresh method resolution, discarded
results, zero-value returns and error stops agreed with focused Lua 5.1
instruction replay of the original methods. Rejecting controls changed a
literal, binding, receiver, argument/result width, loop extent or direct
storage behavior. This finite comparison does not execute the retail client.

## Canonical source comparison

The authenticated canonical command text has malformed branch structure.
`cmdSetArmyBuff` contains misplaced `else` tokens following `goto` statements
at lines 641 and 653; `cmdSetEnemyBuff` has the corresponding tokens at lines
732 and 744. A Lua 5.4 parser rejects each unmodified extracted command body
at the first such `else`. This is a parser observation about decompiler text,
not execution of the original retail Lua 5.1 chunk or proof that a retail
source used `goto`.

Canonical checks retain those exact bytes. They verify the method bindings,
guard/branch text, state-field and control-name literals, icon operands and
command strings independently of the original-bytecode behavior. The two
canonical command bodies match after simultaneous substitution of the army
versus enemy field, prefix and numeric icon operands. Their malformed text
does not support a successful executable source-equivalence claim and was
not repaired for comparison.

The canonical `setBuffIcon` body parses successfully. Its ordered effect
requests, numeric comparison failures and zero-value returns matched focused
original-bytecode replay against authored method stubs. The command behavior
above instead comes from focused replay of the pinned original methods under
Lua 5.1 instruction semantics, checked against independent literal expected
request tuples. Coverage includes each selection branch, equality/type
distinctions, repeat suppression, unused argument, request failures and fresh
final table resolution. Rejecting controls change the source identity, guard,
icon operand, command string, visibility Boolean and return width. These checks
retain no retail body or instruction listing and do not run the client.

## Runtime boundary

The local `init` declaration and assignments are inspected, including its
direct calls to the two reset-request methods. Its caller, actual retail
invocation and dynamic bindings remain uninspected. Its first outward request
is `initTitle`. That method, `initTimer`, `initDefenseLineStatus`,
`initGoodsStatus` and `initGatheringItem` remain uninspected here. The adopted
native declaration route does not establish this widget's selected registry
node, installed array storage or first values. `desktopWidget.closeWidgetDirect` is
the timer hook's first uninspected callee. Its implementation and the hook's
caller/scheduling do not follow from the hook name. The first outward call
on a changed command value is
`getIndexControlName`. Its implementation, `getTemplateControlName`,
`setIcon`, `setVisibility` and `sendControlCommand` remain uninspected here.
The requests therefore establish no actual control lookup, native visibility,
rendered icon, status application or historical timing.

The [Hamlet director contract](content-director-ui-contracts.md#hamlet-defense-director)
owns the director's stored values and other UI behavior. This page does not
join its six `fieldBuffTbl` values to these arguments. Numeric icon operands
remain unnamed. Score, clear conditions and rewards are outside this contract.
