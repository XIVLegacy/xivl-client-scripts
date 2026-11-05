# Opening tutorial city contracts

The selected Gridania, Limsa and Ul'dah battle methods use the same ordered
class predicates to request their main battle lesson. Their later callable
methods differ. Class selection, stored input-device selection and external
event selection are three separate decisions.

The canonical source and original-bytecode findings are:

- [Initial Gridania](gridania-opening-tutorial-contract.md): Btl001 and Btl002;
  [additional branches](gridania-battle-tutorial-branches.md): Magic001 and
  Btl003/004.
- [Limsa](limsa-opening-tutorial-contract.md): Btl001, BtlMagic001 and
  Btl002/003/004.
- [Ul'dah](uldah-opening-tutorial-contract.md): the corresponding five battle
  methods and two selected scenario/Judge calls.

Those pages own exact input identities, operands, locators and source limits.
The comparison below applies only to their inspected methods, without
establishing a historical city-opening event sequence.

## Class and input selection

Each inspected class selector reads only the first state-main-skill result
as `s`, then retains one category result `c`. The first matching predicate
selects the lesson:

| Predicate in order | Selected infoID / title |
| --- | --- |
| `c == 21` | 10 / Casting Spells |
| `c == 29` or `c == 39` | 11 / Actions |
| Prior predicates false and `s == 7` | 9 / Battle Actions |
| Otherwise | 8 / Engaging in Combat |

The client helpers label categories 29 and 39 crafter and gatherer.
Both therefore have a local Actions opening request in these selected
methods. This does not establish an accepted starter action, the actual
player state or a historical invocation.

The [controller/content vocabulary](tutorial-widget-vocabularies.md) owns the
title keys and keyboard/gamepad values. The
[shared opener](tutorial-widget-opening-contract.md#complete-opener-partition)
overwrites its formal controller with the desktop's stored value before
choosing an alias. Numeric 2 chooses the P alias; other values choose K.
The Ask content dispatcher separately recognizes exact controller 1 for
keyboard and 2 for gamepad. A literal controller 2 in a city method does not
prove that it displayed gamepad content. Class predicates do not choose that
stored input-device value.

## Selected city flows

| City / selected methods | Target wait operand and main lesson request | Later callable methods within the published scope |
| --- | --- | --- |
| Gridania BtlMagic001 and Btl002 | Target wait 3201406; each independently reads class state and requests its selected infoID. | Btl003 has no success request and continues to infoID 1 and the final mask only for default/skill-7 branches. Btl004 requests success and inform row 90, then infoID 1 without a final mask. |
| Limsa BtlMagic001 and Btl002 | Target wait 3205403; each independently reads class state and requests its selected infoID. | Btl003 requests success for every class, but only its default/skill-7 branches continue to infoID 1, Moving the Camera, and the final mask. Btl004 requests success and an inform dialog, then infoID 1, without a final mask call. |
| Ul'dah BtlMagic001 and Btl002 | Target wait 3203301; each independently reads class state and requests its selected infoID. | Btl003 continues to infoID 12, Tactical Points, and the final mask only for default/skill-7 branches. Btl004 requests success and an inform dialog, then infoID 13, Weaponskills. |

All three inspected Btl001 methods request infoID 6, Active & Passive Modes.
The target/lesson methods request infoID 7, Targeting Enemy NPCs, before the
target wait. Their exact cinematic operands, masks and control-call order
remain in the city findings. The target-wait integers are distinct from
presentation operands; they are not actor identities established by this
comparison.

For these city calls, infoIDs 1/6/7/10 use the opener's creation-and-selection
wait branch. InfoIDs 8/9/11/12/13 use its other open branch with no following
explicit selection wait. This follows the requested infoID, rather than a
separate city or keyboard/gamepad predicate. The opener discards selection
results and returns zero values. Neither branch supplies an accept/cancel
answer or proves native creation, focus or rendering.

## Local and external continuation

The selected Limsa and Ul'dah battle methods do not call one another.
Gridania's Btl002 supplies no local call to Btl003, and its three additional
methods likewise do not call another battle tutorial method. A later method's
initial close request cannot establish that it followed an earlier lesson
for the same player. All such historical method selection remains external
to these contracts.

Ul'dah's separately inspected Judge declarations operate dialogue through
the forwarded actor. They contain no battle-widget or battle-method call.
The selected Event020_8 wrapper forwards one result; its matching Judge
declaration supplies numeric 2. Neither the method name nor that scalar
selects a subsequent tutorial event.

Use each local branch's actual class, widget and cleanup contract when
characterizing a consumer. Successful local return, a matching method name
or a requested widget does not join supplied and re-fetched players,
establish an external dispatcher, demonstrate target-wait completion or
prove accepted fresh-character progression.
