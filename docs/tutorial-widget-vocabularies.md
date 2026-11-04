# Tutorial controller and Ask widget values

The recovered Ask/TutorialWidget accepts controller value 1 for its keyboard
text branch and 2 for its gamepad text branch. The mode selector assigns
result 2 to Button_1 and result 1 to Button_2. It disables Button_1 when
`worldMaster:_isKeyboardOnlyTutorial()` is exactly true. Its operate handler
copies the supplied operation argument into the base ask result.

`DesktopWidget.askTutorialDeviceType` defaults to 1, stores the selected
result in `tutorialDeviceType`, and returns that value. The tutorial opener
uses the stored type in place of its formal controller argument and builds
the alias `TutorialWidgetK` or `TutorialWidgetP` followed by the infoID.
These selected consumers establish the two values, not a complete enumeration
of every native input-device domain.

The content values below belong to `widget/ask/tutorialwidget.lua` and its
infoID dispatchers. The distinct `widget/tutorialwidget.lua` declares the
same class name with a different base and must not be merged into this table
without its own content trace. English title text is from
`xivl-client-data:csv/xtx__text_ui.csv`, column 1. The row for NPCs also
contains an encoded icon control.

| infoID | Title key | English title text | Pad / keyboard method starts |
| ---: | ---: | --- | --- |
| 1 | 9001 | Moving the Camera | 399 / 952 |
| 2 | 9006 | Getting Around | 419 / 972 |
| 3 | 9011 | Targeting Friendly NPCs | 453 / 1006 |
| 4 | 9016 | Speaking to Friendly NPCs | 490 / 1043 |
| 5 | 9021 | The Main Menu | 527 / 1080 |
| 6 | 9026 | Active & Passive Modes | 547 / 1100 |
| 7 | 9031 | Targeting Enemy NPCs | 567 / 1120 |
| 8 | 9036 | Engaging in Combat | 604 / 1157 |
| 9 | 9041 | Battle Actions | 638 / 1191 |
| 10 | 9046 | Casting Spells | 658 / 1211 |
| 11 | 9051 | Actions | 694 / 1247 |
| 12 | 9056 | Tactical Points (TP) | 735 / 1283 |
| 13 | 9061 | Weaponskills | 755 / 1303 |
| 14 | 9071 | NPCs | 791 / 1339 |
| 15 | 9076 | NPC Linkpearls | 827 / 1375 |
| 16 | 9081 | Journal | 861 / 1409 |
| 17 | 9006 | Getting Around | 898 / 1446 |
| 18 | 9086 | Defeat the enemy! | 932 / 1480 |

Slot 17 is occupied. Its Pad and Keyboard methods reuse slot 2's title 9006
and bodies 9008/9009, obtain the initial town, and call getTutorial2TownNPC.
Slot 2 calls initWidgetWithButton; slot 17 calls initWidgetNoButton. The
supported distinction is the button initialization, not a different title
or a missing numeric value. No editorial enum identifier is assigned here.

The infoID dispatchers are at lines 127-396 and the mode dispatcher at
11-75. The desktop controller helper is at
`widget/desktopwidget_connector.lua:9415-9464` and opener type/alias selection
at 9325-9337. This finding does not reconstruct the opener's complete
yield/non-yield partition from its flattened decompiled branch chain.

The [Gridania opening contract](gridania-opening-tutorial-contract.md#selected-widget-calls)
resolves the directly selected infoID 6/7/11 paths against original bytecode,
including controller override, argument forwarding and selection-result limits.

All scripts below are extraction `2012.09.19.0001`, normalized by the
canonical CRLF-pair-to-LF rule and authenticated against
`manifests/scripts.json` before inspection:

| Script under lua/scripts | Bytes | SHA-256 |
| --- | ---: | --- |
| widget/ask/tutorialwidget.lua | 34132 | `73980DDC53C4DF37A35537020B0DFED620D090F281CA3084BB19CEFB73817D4F` |
| widget/ask/tutorialmodeselectwidget.lua | 1133 | `4767E5C1D5647C37FB39FC6E36FC7FAA66ED8299FB189DBD1E8E87FB6FB59A02` |
| widget/desktopwidget_connector.lua | 660617 | `9C33F21C1F70A0056147E716D53300634EFABE5B744EF6E8690114DB21613A01` |
| widget/tutorialwidget.lua | 24508 | `733EE99341554EB6B6E9C5ABCCC75995B189264CD48C98CE7EF8F2316A787CDC` |

Title keys 9001-9061 above occur at text-sheet physical lines 1965-2013;
9071,9076,9081,9086 occur at 2022,2026,2030,2034. Bodies 9008 and 9009
are at 1970 and 1971. `xtx__text_ui(2).csv` does not contain these selected
keys. Their static title association does not establish a historical tutorial
invocation or successful rendered display. The native control, wait and
camera contracts remain in
`xivl-client-structs:docs/tutorial-control-native-contract.md`.
