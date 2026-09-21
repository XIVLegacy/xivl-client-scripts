# Raid object client contracts

The recovered 1.23b Lua corpus contains three generic raid-object classes and
one cutscene-preface judge. An independent decompile of the same decoded and
ciphered paths confirms a small set of constants and call sequences. The
independent outputs have different formatting and byte identities from the
canonical corpus, so they are corroborating research inputs rather than
replacement corpus files.

The machine-readable source identities, hashes, locators, and claim boundaries
are in
[`raid_object_client_contracts.json`](../manifests/raid_object_client_contracts.json).
The canonical class, method, dependency, and N-API inventories remain in
[`registry.json`](../lua/registry.json) and the corresponding tracked
`*.calls.json` sidecars.

## Object behavior

`RaidDungeonRect` derives from `NpcBaseClass`. Its recovered `initForEvent` and
`eventTalkStep0` bodies are empty. The class establishes an object type but no
rectangle trigger, transport, or server event behavior by itself.

`RaidDungeonWarp` also derives from `NpcBaseClass`. Its recovered methods have
three bounded behaviors:

- `initForEvent` permanently loads text sheet 6781 as `raidDungeonWarp`.
- `activateWarpDevice` invokes character scheduler 67493888.
- `askYesNo` routes a true argument to `askExtendWidget` with the recovered
  arguments `(self, 2, 2, 1, 2)`; the other branch calls `worldMaster:say`
  with selector 1.

These calls identify the client prompt and presentation route. They do not
establish a destination, entry requirement, server-side warp, or terminal
charge rule.

`RaidDungeonTreasureBox.processOpenDzemaelEpicQuestType` references offered
quest 110868, calls the quest object's `isDropDzemael` method, contains item
identifier 10011244, and uses system message 60027. It reaches character
scheduler 67932160 after the branch. The independent decompiler did not
recover the temporary assignment around item 10011244 cleanly, so the exact
item-test and success/failure branch association is unresolved.

The remaining treasure-box helpers read `dropSheet`, `dropTableSheet`, and
`dropQualitySheet`, build candidate item tuples, call `_canAddItem`, and expose
the temporary `mapMarkerVisible` value through
`isMapMarkerVisibleForTalkable`. This proves client-side consumption and
presentation structure only. It does not authenticate a particular drop-table
row, probability, item grant, inventory mutation policy, or server reward.

## Cutscene bridge

`CutSceneOnceBeaconPrefaceJudge.processEvent` performs this recovered client
sequence:

1. Fade out the local player and wait for fading.
2. Create a cutscene from the method's third and fourth arguments.
3. Start it with the literal arguments `(1, 61, 1)`.
4. Delete the cutscene object.
5. Fade in the local player and wait for fading.

The generic `CutScene` scripts independently inventory the load, play, replay,
skip, UI, widget, and finalization methods used by that bridge. The sequence
does not identify a particular scene resource, server trigger, actor roster,
world transform, or duration.

## Evidence boundary

The independent source manifest records decoded byte counts and installed
client paths but no LPB SHA-256 values. Its decompiled outputs are pinned in
the retained finding, and their decoded/ciphered paths, classes, methods, and
N-API calls agree with the separately produced canonical corpus metadata.
That agreement supports the constants and call sequences above; it does not
make the independent outputs canonical or resolve their decompiler ambiguity.
