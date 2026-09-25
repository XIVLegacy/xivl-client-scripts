# Reward and delivery widget results

These recovered Ask widgets return client-side selections or acknowledgements.
Their result values do not prove a server grant, inventory mutation, or reward
authority.

`ContentRewardWidget` sets base ask result `1` for `Button_Confirm` and `-1`
for its cancel command (`contentrewardwidget.lua:344-351`). `RewardSelectWidget`
sets the result to `work.index + 1` for a valid item selection; its cancel and
close commands return `-1` (`rewardselectwidget.lua:520-541`).
`TreasureListWidget` stores the selected row as `A3 + 1`, opens a
`CommonAskWidget`, and copies the stored index into its ask result only when
that child result is `1`; closing the selector sets `-1`
(`treasurelistwidget.lua:34-62`). These are selection/confirmation results,
not item IDs or evidence that the selected reward was granted.

`QuestRewardWidget` sets result `1` for both operate and cancel when its mode is
`1` (`questrewardwidget.lua:64-72`), so that result cannot distinguish those
two UI actions. `QuestDeliveryWidget.getAskResult` returns a seven-value tuple:
chosen package, chosen item slot, chosen count, item name index, catalog ID,
attached materia count, and a final `-1` while waiting for price or `0`
otherwise. A canceled ask or missing item returns seven zeroes
(`questdeliverywidget.lua:1836-1889`). The tuple is a client selection/result;
it does not establish item ownership at the receiver, a server-side delivery,
or a completed quest or Hamlet mutation.

| Decoded script | Canonical source SHA-256 | Reviewed decompile output SHA-256 | LPB and decoded-payload identity |
| --- | --- | --- | --- |
| `lua/scripts/widget/ask/contentrewardwidget.lua` | `1a8973cb83bb82a9c1695b2aa4561081d5bd3c75d2104cc95443e281bfc0790b` | `d31d283d4b1cf830e15cacdcf4cfcde6def149052b716da5e6ce4e2423968187` | `n1635q/9rz/7vwq5wqs5n9s6n1635q.le.lpb`; LPB SHA-256 `c7e90eddf2671f4aab832f580d1c459fa4a1853cf27b1937c28d1e0ceecede94`; decoded payload SHA-256 `f0f91fbb8dae7a4fcfbe6a0baa8f27bbd2b54275cc2f0aee1dcc49ffe5be95a4` |
| `lua/scripts/widget/ask/rewardselectwidget.lua` | `ee220caa549be99a3b69b557822fabd64004125f6e33f6d91596fc6347899548` | `9e075b9d15cae3e480c085b37fcc592a142aee062907addb75deab9eba61e46f` | `n1635q/9rz/s5n9s6r5y57qn1635q.le.lpb`; LPB SHA-256 `71a3875baac970973bf38d6a2556ff5ba92c9b800b67b703c1338e4fdad87911`; decoded payload SHA-256 `49e4efc9b59917ca88ea3ee2af319012d79b0a434c559dda68935d8dff603a5b` |
| `lua/scripts/widget/ask/treasurelistwidget.lua` | `5ffe819e45ff3b2746af386acaaa43ba94ed9a9dcd256ce12463f6a35a165361` | `382aef7289ede540ffbcc7539e259d1445206e81c2a95028063f0e781750242b` | `n1635q/9rz/qs59rps5y1rqn1635q.le.lpb`; LPB SHA-256 `7c13cab369aa2064bfdd194a2add5827fb9a701870344ce5e4d5cacdaf30510c`; decoded payload SHA-256 `bf59a0cd6ea9b799cdef949785a2527de7c4a1ac6c1c7ed356e0b6bacc5df07e` |
| `lua/scripts/widget/ask/questrewardwidget.lua` | `1f12737ea03fbdd931654e3b47fdd745889e86cef5e0793ef2a6c933b1d9a03d` | `e39c889289ce1dc2b3e92f71e2d49f22da75f2ec5f27e3d0896ce749e096587f` | `n1635q/9rz/tp5rqs5n9s6n1635q.le.lpb`; LPB SHA-256 `bf3921862d3905791a22bfa8d1911c4835e8cae25f68af5b49d8102afbd887e1`; decoded payload SHA-256 `21f32f0fdbbbfcdd39100dfee22067cb6929f60685752f10b2bc7759f667cea4` |
| `lua/scripts/widget/ask/questdeliverywidget.lua` | `ba34706ada144e2f7d2d91c7acf6b4d6f31fcb9f9ec7a95a1a3d00345f35640d` | `b0311ccc3a72564f5e86d5421ec446dc4d3f2229fe8b5135496e9bcf06c416ae` | `n1635q/9rz/tp5rq65y1o5sln1635q.le.lpb`; LPB SHA-256 `224ce2413d952356856d6a58fdaf01ce7985fc751555aeb3b6f384f2db5ace63`; decoded payload SHA-256 `3985b32874a8a105dc464cbd2d703029fd79b48b78198382e2ce72a3a7ad9a08` |

Canonical source hashes are pinned in `manifests/scripts.json`; LPB identities
and decoded payload hashes are pinned in `manifests/retail_lua_coverage.json`.

## ContentRewardWidget caller routes

Each method below calls `askEventModeWidgetYield` for
`Ask/ContentRewardWidget` in mode `1`, passing its own actor instance and a
trailing `1`. These call sites establish a widget open request; they do not
prove that a reward was granted.

| Caller method | Decoded script | LPB resource and pinned identity |
| --- | --- | --- |
| `GuildleveWarpPoint.eventGuildleveReward` | `lua/scripts/chara/npc/object/guildlevewarppoint.lua` | `729s9/wu7/v8057q/3p1y6y5o5n9suuv1wq.le.lpb`; LPB SHA-256 `AAF4816A2542A8365F2738C9958083C07EDD9052ABA4E069CB29C830E63FF7A4`; decoded payload SHA-256 `1C6EEAC00FB31DCA16E9CF6064DC2EE37A64942B9707D8676305CE887D812186` (`retail_lua_coverage.json:8001-8011`) |
| `PopulaceGuildleveTester.eventGuildleveReward` | `lua/scripts/chara/npc/populace/populaceguildlevetester.lua` | `729s9/wu7/uvupy975/uvupy9753p1y6y5o5q5rq5s.le.lpb`; LPB SHA-256 `1682C91087183D0C248681DA9235C667C382ECCAF13EB2452AB771A23EB3194C`; decoded payload SHA-256 `E742FA6CA31E61BFBF647B5FBF4941A72FB7E83B588DF3CE6024052F27190993` (`retail_lua_coverage.json:7056-7066`) |
| `PopulaceCompanyGLPublisher.eventGLReward` | `lua/scripts/chara/npc/populace/populacecompanyglpublisher.lua` | `729s9/wu7/uvupy975/uvupy9757vxu9wl3yup8y1r25s.le.lpb`; LPB SHA-256 `0874F59A069F7A6F87B7A01B93D7D91D8D5DD14F749CFF02B05F7BCBCD15EFDF`; decoded payload SHA-256 `0AE20217500C331EC82F660A0A3762523CBC168B3DBCB37B995D2225934FC43C` (`retail_lua_coverage.json:7371-7381`) |
| `PopulaceFactionGLWorker.eventGuildleveReward` | `lua/scripts/chara/npc/populace/populacefactionglworker.lua` | `729s9/wu7/uvupy975/uvupy975497q1vw3ynvsz5s.le.lpb`; LPB SHA-256 `7B71CEC14520C737F79404B6B15DE7996BED6EEE7BAF0970E5D79F0495455883`; decoded payload SHA-256 `93DC837772665914D81C04993645B1CC90020084BF5F3E687DC49ED7DFB16E2D` (`retail_lua_coverage.json:7221-7231`) |

`GuildleveWarpPoint` also defines `getContentRewardItem` in the same pinned
payload (`root/proto8`). The lookup is gated on `work.glRewardItem > 0`
(PCs `006`-`007`, byte offsets `0xA5E`-`0xA62`). For selector arguments
`R1=1`, `R2=1`, `R3=2`, it loads `work.glRewardItem` through
`itemDataSheet:_getData` with field ID `36` (PCs `016`-`028`, byte offsets
`0xA86`-`0xAB6`). It compares the item ID with numeric constant `1000001` at
PC `031` (`0xAC2`). Equality returns the field-36 result, `nil`, `4405`, and
`work.glRewardNumber` at PC `038` (`0xADE`). Otherwise it returns the field-36
result, `nil`, `4406`, `work.glRewardItem`, and `work.glRewardNumber` at
PC `047` (`0xB02`). This is a client-side getter tuple. The constant's domain
meaning and any server-side grant or inventory effect are not established.
