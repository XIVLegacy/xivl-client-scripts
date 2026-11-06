# NPC repair manual client contract

`PopulaceItemRepairer.readRepairManual` requests an initial question and,
only for numeric answer 1, repeats a topic menu. Numeric topics 1-4 request
ordered dialogue; every other topic result ends the loop. Its Boolean
return describes that local path. Instruction menus do not establish
repair eligibility, material use, restoration, charges or settlement.
The separate [repair request contract](repair-request-client-contract.md)
owns item-selection and confirmation behavior.

## Arguments and ordered requests

Write N for the supplied receiver. The method has two fixed parameters,
including N, and no varargs. The second parameter A1 is unused: it is
neither read, tested nor forwarded. Missing fixed arguments become nil;
extra arguments are ignored. No player, level or Boolean domain is
established for A1.

The first operation resolves `N.askExtendWidget` and requests this complete
argument frame, including the method receiver:

```text
(N,N,58,2,1,1)
```

Exactly one result is retained. Only equality with numeric 1 enters the
topic loop; nil, false, true, zero, numeric 2, cancellation values and
string `"1"` return exactly `(false)`. There is no truthiness test or
numeric-string conversion.

Each iteration resolves `N.askExtendWidget` again and requests:

```text
(N,N,61,5,1,1)
```

Only its first result is retained. The following comparisons occur in
order. Dialogue keys remain unlabeled because their text was not evaluated.

| Numeric topic result | Ordered dialogue keys |
| --- | --- |
| 1 | `67,68,69` |
| 2 | `70,71,72,73,74,75,76,98,99,100,101` |
| 3 | `77,78,79,80,81` |
| 4 | `82,83,84,85,86` |
| Every other result | No dialogue; exit the loop and return `(true)` |

For each key K, the method freshly reads global `worldMaster`, resolves
that value's `say` member and calls `(W,N,K)`, where W is that same global
value retained as the call receiver. It discards every speech result.
There is no formatter tail. The next key obtains a fresh global value and
member, so the sequence does not require all requests to use one W.
Completing a supported topic returns to the topic menu without repeating
the initial question. Topics may be selected repeatedly or in any order.

Result 5 is an exit by the default branch, as are -3, -2, -1, zero, nil,
false, true, string `"1"` and other values unequal to numeric 1-4.
No specific exit value is returned to the caller: each such topic result
produces exactly one Boolean true. The method has no iteration limit and
no finish-talk, cleanup or repair request. A supplied sequence of supported
topics can continue the loop; exhaustion of an authored fixture's answers
is a harness stop, not evidence of a retail hang.

There are no receiver, callable, type or helper-success guards before the
lookups and calls. A reached lookup or call error stops the method before
later requests or its normal return. Completed earlier speech requests
remain earlier requests. An error is not converted to false, retried or
caught. Additional ask results and all speech results are discarded.

## Conditional helpers and text metadata

If the dynamic ask member resolves the published
[inherited helper](request-warden-event-contract.md#widget-result-production),
its arguments mean `(receiver,textOwner,promptId,answerCount,flags,defaultIndex)`.
Both calls supply N as textOwner, flag 1 and default index 1. The helper's
consecutive-choice construction conditionally produces these requests:

| Caller prompt | Answer keys in index order | Formatter arguments |
| --- | --- | --- |
| 58 | `59,60` | None |
| 61 | `62,63,64,65,66` | None |

With the published flag-1 forwarding, the connector frame is
`(D,N,N,N,1,false,true,prompt,answers)`, including desktop receiver D.
The N positions are owner, speaker and text provider. Paging is false and
cancellation is true. The connector's opening frame is
`(D,4,"Ask/AskWidget",nil,nil,false)`; the widget's ask frame is
`(widget,N,N,1,false,true,prompt,answers)`. These are conditional requests,
not actual widget creation or delivered controls. The helper's open formatter forwarding is owned by
the [key-question contract](open-world-key-coffer-contract.md#confirmation-and-event-contract);
this caller supplies an empty tail. Conditional
[connector completion](camp-replacement-choice-flow.md#local-completion-result-and-cancellation)
can return zero for a nil opening or unsuccessful selection, while preserving
the first selected getter result. Thus zero gives false at the initial
question but true at the topic menu. The published Ask result contract can
request -3 for cancellation. Its actual UI event, label-to-result association,
stored state and delivered result remain separate inputs.

If each W's member resolves the published
[WorldMaster speech helper](worldmaster-message-arguments.md#generic-argument-route),
`(W,N,K)` forwards to `showMessage(D,W,40,N,K)` and then
`_appendMessagePool(D,W,40,N,K)`. There are no variadic formatter values.
Here N supplies the source-object position; W is the message receiver.
The helper contract does not authenticate an actual object, text lookup,
native message delivery or rendering.

Literal text-key metadata in this method is limited to prompts 58 and 61
and dialogue keys 67-86 and 98-101. Keys 59/60 and 62-66 are computed by
the conditional inherited helper, not literals in this method. The
published initializer declaration in
`xivl-client-data:docs/repair-menu-text-contract.md`, section "Initializer
declaration," requests bank 2204/schema `populaceItemRepairer`; it does not
prove this method's provider, schema, locale or initializer execution.
That adopted document is revision
`a78b2884295bf55d6a062c494b63acbaf7e1020c`, SHA-256
`80e51475038e95eede0e224f02d2b556175a324081d5d574bef44ca25be31285`.
The keys do not establish English topic labels.

## Source identity and verification

Source: `xivl-client-scripts:lua/scripts/chara/npc/populace/populaceitemrepairer.lua:356-538`,
`readRepairManual`, extraction `2012.09.19.0001`.
[scripts.json](../manifests/scripts.json), matching relativePath record,
pins the 15,881-byte, 742-line canonical source, SHA-256
`027ac93ef6e805ee4c2197d5fa7353a0ebdff125f6d52f0d6c08bedfb5218ea3`.
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json), matching
decodedScriptPath record, pins original resource
`729s9/wu7/uvupy975/uvupy9751q5xs5u91s5s.le.lpb`, 4,762 bytes, SHA-256
`3d2148a689cbf940bbfc80260fd3d5a540e75d4992cdbd296a36a1e0cf3e1e7d`;
its 4,749-byte decoded payload has SHA-256
`90d9858f42360f5078a0f567d17c3f1651832127f81bd146d293e33ee01889e7`.
[private_lua_corpus.json](../manifests/private_lua_corpus.json) owns the
canonical archive identity.

The original Lua 5.1 method is `root/proto2`, code offset 2488,
160 instructions, two fixed parameters, zero varargs/upvalues/children.
Root PCs 14/15 create and bind `readRepairManual`. The header declares
`PopulaceItemRepairer` with `NpcBaseClass` and requires
`/Chara/Npc/NpcBaseClass`; the dependency bodies were not inspected here.
PCs are zero-based. Initial/topic CALL PCs 6/18 have B=7,C=2: six
arguments including the receiver and one result. Dialogue CALL PCs
26/31/36, 44/49/54/59/64/69/74/79/84/89/94,
102/107/112/117/122 and 130/135/140/145/150 have B=4,C=1:
three arguments including the receiver and zero results. Result guards
are PCs 7,20,38,96,124; PC 10 tests the Boolean loop control.
Default topic PC 152 clears that control. Normal RETURN PCs 155/158
each have B=2 and return one Boolean. PCs 156/159 are unreachable from
the original entry under this control flow.

The exact selected canonical method parsed without repair. Finite authored
original-instruction and canonical-interpreter cases checked the literal
frames, topic sequences, fresh reads, discarded results, nil/false/zero,
missing/extra arguments, normal returns and stopping errors. Rejecting
controls checked guards, keys, providers, request order, widths and loop
exit. These checks covered 158 reachable original instructions; they were
authored Python checks, not Lua/native execution or retail observations.

The first uninspected edges are the actual `N.askExtendWidget` and
`worldMaster.say` bindings and invocation, followed by the selected
provider/text/formatter evaluation and delivered answer. The method's
menus and dialogue requests supply no class, skill, material, licence,
price, condition-restoration, payment or settlement rule.
