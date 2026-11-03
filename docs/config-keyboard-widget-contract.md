# Config keyboard widget contract

The retail Lua resources named `ConfigKeyboardWidget` and
`ConfigKeyboardAskWidget` are separate resources. The parent requests local
control setup, opens the distinct Ask resource for two button choices, sends a
save command on cancel or an enabled toggle, and reads a configuration flag to
set a toggle. The Ask resource sets its own cancel/focus/parameter/text
requests. These observations stop at Lua requests and local results.

## Resource identities

| Resource | Retail relative path | Class | Own methods | LPB bytes / SHA-256 | Decoded bytes / SHA-256 | Canonical LF bytes / SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| `widget/configkeyboardwidget` | `client/script/n1635q/7vw413z5l8v9s6n1635q.le.lpb` | `ConfigKeyboardWidget` | `init`, `processUICommandOperate`, `processUICommandCancel`, `processUICommandToggleButton`, `initToggleButton` | 1613 / `d360c57e4d76157a0521ca64a3d6d65b1f6aa91acc9ef915c6da6819006e5da9` | 1600 / `1889d1aad205e1ab60b8b7695b29fbce775f22fd53c27e59d8ed1cee2f3368e6` | 2872 / `041d50b6e9d474ac7d6a4b75f675a84cf8ba2acfc88e375018698f53dbd2038d` |
| `widget/configkeyboardaskwidget` | `client/script/n1635q/7vw413z5l8v9s69rzn1635q.le.lpb` | `ConfigKeyboardAskWidget` | `init` | 499 / `46a42f88aecfbb66981587efdbbff63d4a192da881e708d4394c14a19acedcb8` | 486 / `5cc6216da3d4494b574d7d99f992e504038834670900023ff88614db6a74e9c4` | 701 / `4a5d1470c5a65a4501193e1defbb60a9f25fa2e9e9fec1bc03aadd2d4573743a` |

The manifest, coverage census, registry, and call sidecars identify both
decoded paths separately. The sidecars report one `_defineClass` API and one
callsite for each resource; they do not supply runtime semantics.

Sources: `xivl-client-scripts:manifests/scripts.json:15279-15285`,
`xivl-client-scripts:manifests/retail_lua_coverage.json:25814-25829`,
`xivl-client-scripts:lua/registry.json:40351-40364`,
`xivl-client-scripts:lua/scripts/widget/configkeyboardwidget.calls.json`, and
`xivl-client-scripts:lua/scripts/widget/configkeyboardaskwidget.calls.json`.

## Parent resource

The root first requests `/Widget/WidgetBaseClass`, defines
`ConfigKeyboardWidget` with `WidgetBaseClass`, and makes five own-closure
binding attempts. The root has two fixed calls and a zero-result return. The
closure joins are source-derived from the root `CLOSURE` and `SETTABLE`
instructions; they are binding requests and do not guarantee host installation.
The bounded fixture conditionally resolves those admitted root closures into a
nominal frame object so the own `initToggleButton` call executes its original
words; this does not claim universal class installation or fallback behavior.

The canonical LF source windows are:

| Method | Canonical lines | Words | Calls (argument width -> result width) |
| --- | ---: | ---: | --- |
| `init` | 11-41 | 21 | 3->0, 4->0, 2->0, 2->0, 1->0, 2->0 |
| `processUICommandOperate` | 44-71 | 22 | 5->0 |
| `processUICommandCancel` | 74-88 | 9 | 3->0, 2->0 |
| `processUICommandToggleButton` | 91-113 | 16 | 3->0, 3->1, 3->0 |
| `initToggleButton` | 116-134 | 12 | 3->1, 2->open, open->0 |

The original bytecode return instruction for every parent method has result
width zero. The `open` widths above are retained: `getConfigFlag` supplies an
open result tuple to `setChecked`, whose open argument width forwards that
tuple after the fixed receiver and control arguments.

Finite traces distinguish raw native results from Lua's consumed results: the
fixed-width `getControlUserWorkInt` call keeps only its first result and pads a
missing result with nil, while the open `getConfigFlag` call forwards zero,
one, or multiple produced values unchanged. This is a bounded request trace,
not a native implementation claim.

### Initialization

`init(self)` requests, in order:

1. `setControlCommandCondition(self, "ToggleButton_Controler", "UILuaCommands.ToggleButton")`.
2. `setControlUserWorkInt(self, 1, "ToggleButton_Controler", 10)`.
3. `setConfirmCondition(self, "Button_TypeA")`.
4. `setConfirmCondition(self, "Button_TypeB")`.
5. `setCancelCondition(self)`.
6. `initToggleButton(self, "ToggleButton_Controler")`.

It returns zero values. When the admitted own-closure lookup resolves, the
method calls the closure owned by this same parent resource; the closure's
native work and flag requests are described below.

### Operate

`processUICommandOperate(self, unused, command, unused, unused)` compares the
command with the exact strings `Button_TypeA` and `Button_TypeB`. The first
maps to numeric choice `0`, the second to numeric choice `1`. Either choice
requests:

```text
desktopWidget.openChildWidget(
    desktopWidget, "ConfigKeyboardAskWidget", self, true, choice
)
```

The method has no request for any other command and returns zero values on the
bounded paths. The child request does not establish that the child opened, that
it accepted the choice, or that it later reports a result.

### Cancel and toggle

`processUICommandCancel` requests
`self.sendControlCommand("KeyConfig_Saver", "KeyConfig.Save")`, then requests
`desktopWidget.closeWidgetDirect(self)`, and returns zero values. Both are
requests; neither proves a save, persistence, close completion, or lifetime
transition. The bounded trace pins the first frame callable and then the fresh
desktop receiver/callable lookup for the later close request; it does not infer
that lookup from display labels.

`processUICommandToggleButton` first requests the same save command only when
its final argument is exactly Boolean `true`. It then requests
`self.getControlUserWorkInt(1, control)` and passes the first returned work
value to `desktopWidget.setConfigFlag(work, finalArgument)`. The method returns
zero values. The work value and final flag are forwarded as typed operands;
the setter request is not a completed configuration write.

### Toggle initialization

`initToggleButton(self, control)` requests
`self.getControlUserWorkInt(1, control)`, then captures `self.setChecked` before
the fresh `desktopWidget.getConfigFlag(work)` lookup. Its open result tuple is
forwarded through that captured callable as `self.setChecked(control, ...)`
after the fixed receiver and control. A zero result tuple therefore produces a
two-argument `setChecked` request, while a two-value tuple produces the
corresponding two typed values. The method returns zero values. The native
result tuple is a supplied bounded input here, not a claim about the native
implementation's actual flag count.

## Distinct Ask resource

The Ask root independently requests `/Widget/WidgetBaseClass`, defines
`ConfigKeyboardAskWidget` with `WidgetBaseClass`, and makes one own-`init`
closure binding attempt. It has one fixed-result-width-zero return and no
parent-method body is imported into this contract. The binding is a request;
the bounded fixture resolves the admitted closure only when its lookup is
present.

The canonical LF source window for `init` is lines 11-36. Its prototype has 18
words and four calls, all with fixed zero result width: 1->0, 2->0, 3->0,
3->0.

`init(self, choice)` requests, in order:

1. `self.setCancelCondition()`.
2. `self.setLogicalFocus("Button_2")`.
3. `self.setCommandParameter("Button_1", choice)`.
4. `self.setText("TextBlock_Text", textId)`.

The local text ID is numeric `1494` when `choice == 1` using Lua's strict
equality, including an integral floating-point `1.0` because Lua has one
numeric kind. Otherwise it is numeric `1493`, including a Boolean `true` and
nil. This method returns zero values. These are local requests only;
they do not prove focus ownership, command acceptance, modal completion, text
rendering, parent callbacks, or closure of either widget.

## Verification and limits

The complete original-word checks authenticated every root and admitted own
prototype word, root closure join, guard and jump, call/return width, capture
boundary, and canonical source window. Finite cases covered both operate
choices, unknown operate command, initialization, cancel, true/false toggle,
zero-work and one-value flag tails, zero/open flag tails, numeric choices,
Boolean-versus-number equality, and ordinary error prefixes. The replay set
covered 20 parent cases and 7 Ask cases. Each normal case asserted one complete ordered raw
event sequence, including entry frames, exact prototype and program-counter
coordinates for every call, nested entries and returns, argument/result types,
receiver identity, callable identity, and zero-result return. Error cases
retained the original nonterminal error and only the genuinely reached event
prefix. The input-only case list is checked against an independent
source-anchored literal oracle; the retained complete VM dump is not an
admitted expectation source.

Thirty corruption controls passed an unchanged baseline and then rejected
an actual mutation: a branch operand, a Boolean-versus-number result, a
receiver, a frame callable, an Ask callable, an Ask receiver, retained-error
continuations at outer and nested boundaries, two same-width confirm-call
order/PC mutations, an unused cancel argument, a forwarded work value, an Ask
Boolean text decision, fresh and stale desktop receiver/callable rebinds,
same-token spoofed owners for both globals and both resource natives, same-name
outer closure clones for both resources, and a global `require` callable for
each resource. Same-content table replacement and same-token helper-cache
replacement were rejected at the poststate gate while preserving their prior
call, error, and return evidence. A forged empty change list was also rejected
against the complete typed before/after pair.
Same-label and same-suffix object clones hit actual identity guards. A positive
getter-time `setChecked` rebind preserved the callable captured before the
getter, while a changed desktop receiver and callable were both pinned after
`sendControlCommand`; hoisted old receiver/callable variants hit their actual
identity guards. The Ask Boolean case preserved forwarded `true` while its
wrong text decision was rejected. Recursive snapshots retained function-valued
fields with raw identities and detected closure replacement, removal, same-label
table replacement, and same-token helper-cache replacement.
Recursive state snapshots remained unchanged across the request-only stubs, and
a nested mutation probe was detected, so request emission was not reported as
applied state.

Public reproduction uses the repository tool with caller-selected placeholders:

```powershell
python tools/retail_script.py --input <resource.le.lpb> --jar tools/vendor/unluac/unluac_2025_12_23.jar --decoded-out <payload.bin> --script-out <canonical.lua>
```

The supported unluac disassembly form is separate from the finite local
checks:

```powershell
java -Djava.io.tmpdir=<java-tmp> -jar tools/vendor/unluac/unluac_2025_12_23.jar --disassemble --output <disassembly.txt> <payload.bin>
```

The canonical output applies the tool's CRLF-pair-to-LF rule. The private finite
checks use the authenticated original payload and the pinned toolchain in a
separate local evidence lane; no private paths are needed to reproduce the
public decode command.

The following remain unbound: the WidgetBaseClass implementation, form bodies,
native helper implementations, keyboard binding and TLS routing, focus or
recipient policy, configuration-store mutation or persistence, apply success,
server effects, parent-to-Ask result delivery, and complete widget lifetime.
Existing keyboard movement and player movement native frontiers remain
separate evidence and are not reopened by these Lua names or requests.

Sources for those reused boundaries: `xivl-decomp:docs/input/keyboard-movement-bindings.md:1-19,109-120`,
`xivl-decomp:docs/input/player-movement-command-origin.md`,
`xivl-client-structs:docs/desktop-native-call-contract.md:59-86,155-173`, and
`xivl-client-structs:docs/user-config-store-contract.md:325-436`.
