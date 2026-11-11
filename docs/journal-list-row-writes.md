# JournalListWidget row writes

`JournalListWidget` fills the lists named `ListBox` and `QuestComboBox` with
list property requests. This page records the script writes on the mode 1
active-quest path. It does not establish native list storage or template
binding.

## Mode 1 sequence

`initAsk` (`widget/ask/journallistwidget.lua:11-139`, `root/proto0`) stores the
mode, sets `work.questType` to 1, calls `createList` and then, for mode 1,
calls `createCategoryComboBox`. `createList` (lines 810-923, `root/proto10`)
clears `ListBox`. In mode 1 with quest type 1 it calls `addQuestList`,
`addActiveGuildleveList` and `addPassiveGuildleveList`, then calls
`updateListProperty("ListBox")`.

## Heading rows

`addListTitle` (lines 928-966, `root/proto11`) writes these attributes:

| Attribute | Wrapper | Value | PC of the name |
| --- | --- | --- | ---: |
| `template` | `setListPropertyTemplate` | `DataTemplate_ListBoxItem_Title` | Wrapper literal |
| `TitleText` | `setListText` | Supplied text key | 8 |
| `TitleHelpType` | `setListProperty` | 1 | 14 |
| `TitleHelpValue0` | `setListProperty` | Supplied help value | 20 |
| `JournalType` | `setListProperty` | 0 | 26 |

After its rows, each of these three list builders writes `NumberText` on the
heading index through `setListText` with text key 228. In `addQuestList` (lines 1114-1176,
`root/proto14`) that write is at PC 45.

## Quest rows

`addQuestList` writes `JournalIndex` at PC 28 and then calls `setListItem` with
journal type 3, the quest ID and text key 5001. `setListItem` (lines 1313-1559,
`root/proto17`) writes these attributes:

| Attribute | Value | PC of the name |
| --- | --- | ---: |
| `Name` | Text key with the journal ID, through `setListText` | 3 |
| `ItemColor` | `tostring(1)` | 10 |
| `VisibilityIconActive` | `Collapsed` | 18 |
| `VisibilityIconClear` | `Collapsed` | 24 |
| `VisibilityIconFail` | `Collapsed` | 30 |
| `VisibilityIconQuestActive` | `Collapsed` | 36 |
| `VisibilityIconQuestClear` | `Collapsed` | 42 |
| `CategoryIcon` | First `getJournalIconID` result when nonzero | 55 |
| `CategoryIconHelp` | Second `getJournalIconID` result when the first is nonzero | 61 |
| `VisibilityIconCategory` | `Collapsed` when the first result is zero | 68 |
| `VisibilityIconReward` | `Collapsed` | 74 |
| `VisibilityTextReward` | `Collapsed` | 80 |
| `JournalType` | Supplied journal type | 86 |
| `JournalID` | Supplied journal ID | 92 |

Journal types 1, 2 and 4 take a further status branch after these writes.

## Quest category rows

`createCategoryComboBox` (lines 490-531, `root/proto8`) calls
`addQuestComboBox` for categories 1 through 30 by default. It then calls
`updateListProperty("QuestComboBox")` (PC 27) and
`setSelectedIndex("ComboBox_Category_Quest", 0)` (PC 30). That wrapper writes
control property `SelectedIndex`.

`addQuestComboBox` (lines 536-805, `root/proto9`) writes each `QuestComboBox`
row:

| Attribute | Wrapper | Value | PC of the name |
| --- | --- | --- | ---: |
| `QuestItemName` | `setListText` | Category text key | 231 |
| `QuestIcon` | `setListProperty` | Category icon | 238 |
| `QuestType` | `setListProperty` | Category number | 244 |
| `ComboBoxItemHelpType` | `setListProperty` | 1, when a help value is set | 252 |
| `ComboBoxItemHelpValue0` | `setListProperty` | Help value, when set | 258 |

## Wrappers

In `widget/widgetbaseclass_common.lua`, `setListProperty` (lines 3100-3109)
forwards to `_setListProperty`, and `setListText` (lines 3173-3183) forwards to
`_setListTextProperty`. `setListPropertyTemplate` (lines 3248-3257) writes list
property `template` through `setListProperty`. `setSelectedIndex` (lines
2201-2212) writes `SelectedIndex` through `setControlProperty`.

## Source identity

Inputs are from FINAL FANTASY XIV build `2012.09.19.0001`. Canonical sources
match [scripts.json](../manifests/scripts.json) after the CRLF-pair-to-LF rule.
The original resource and decoded payload match
[retail_lua_coverage.json](../manifests/retail_lua_coverage.json).
PCs are zero-based and count instructions.

| Canonical source after `lua/scripts/` | Bytes / lines | SHA-256 |
| --- | --- | --- |
| `widget/ask/journallistwidget.lua` | 37468 / 1814 | `c103432e8671ee20493b4060d5d0958f608c967f211c2f73bee8aec6af96de87` |
| `widget/widgetbaseclass_common.lua` | 69077 / 3361 | `2057f6a4a94071bf8c9f2fa697bc0571b47da14a6bc4919a6d5491005417800f` |

| Original resource | LPB bytes / SHA-256 | Payload bytes / SHA-256 |
| --- | --- | --- |
| `n1635q/9rz/0vpsw9yy1rqn1635q.le.lpb` | 15297 / `a15c8bf36e8124c5c4f5be2ef189037894c98342c7c7eef5889ade16d975e6f3` | 15284 / `549bc61fe3c206f1dd080057948a201f2824a785d039fb9f97878d8a31491d33` |
