# Chocobo mount script contracts

These are static client-script observations for the 1.23b extraction. They
describe predicates and UI calls, not a historically observed mount attempt,
server authorization, or active runtime state.

## Ride command and judge

Static actor class ID `320013` maps to `/Judge/ChocoboJudge` in the client-data
class-path manifest. `ChocoboJudge.isRiding` tests actor main state `15`;
`isRidingChocobo` and `isRidingGoobbue` additionally distinguish riding grade
`257` (not `257` for chocobo, `257` for Goobbue). `getRidingErrorTextId`
defaults an omitted error to `32507` and, for grade `257`, maps `26005` to
`26022`, `26010` to `26024`, `26013` to `26029`, `26014` to `26030`, and the
default `32507` to `32508`. `hasWhistle` tests whether `_getChocoboGrade()` is
non-nil; `hasGoobbueWhistle` returns `_isEnabledGoobbue()`. For grade `257`,
other error IDs have no explicit return in this method.

For command `12014`, `ChocoboRideCommand.canFireDetail` rejects an already
riding actor with `32501`. Its restriction error is `26002`, or `26020` when
the first supplied command argument is non-nil and not numeric zero. It rejects
when both `_canRideChocobo()` and `_isWarpRideChocobo()` are false, and also
rejects `_isPushingOut()`; either restriction returns the selected error. For
other command IDs, it requires `ChocoboJudge.isRiding`, otherwise returning
`32501`. The accepted branch returns `(true, 0)`. These are the script's local
gate and error values; they do not establish server-side acceptance or the
meaning of the text rows.

`docs/player-command-event-routes.md` separately records the PlayerBaseClass
dispatch and post-server follow-up for commands `12014` and `12015`.

## Naming widget

When `desktopWidget:isChinese()` is false, `ChocoboNamingWidget` accepts `A-Z`
and `a-z`, sets the text control's maximum length to `10`, and enables Decide
at length three or more. In the Chinese branch it enables IME input, uses a
maximum `maxZenHan` of `4`, and enables Decide for `getZenHanLength` values
from `3` through `4` unless the control's `IsValidFirst` property is false.
The script does not define what `IsValidFirst` validates.

Decide opens `CommonDialogWidget` with text parameter `7015` and the converted
name. A positive child result returns the converted name; other results return
an empty string. Closing the ask sets the base ask result to `2`. These calls
do not define the localized text or the server's name-validation policy.

## Rental timer widget

`ChocoboRentalTimerWidget.setTimer(expiry)` subtracts
`worldMaster._getServerTime()` from its argument and writes the result to the
timer label's `FloatData.Value0`, with the other timer properties set to
`IntData.Value0 = 1`, `FloatData.Value1 = 0`, and `FloatData.Value2 = 60`.
This method does not identify the caller or prove which packet or lifecycle
event supplies `expiry`.

## Evidence identity

`manifests/scripts.json` pins the canonical decoded-source hash for each logical
script path. The readable decompilation views inspected for the method-level
claims have different text hashes; they are not presented as byte-identical to
those canonical source files. Their source identity was checked against the
raw LPB SHA-256 and decoded-payload SHA-256 in
`manifests/retail_lua_coverage.json`.

| Logical script | LPB resource | LPB SHA-256 | Payload SHA-256 | Canonical source SHA-256 | Readable decompilation SHA-256; locator |
| --- | --- | --- | --- | --- | --- |
| `lua/scripts/command/game/prog/chocoboridecommand.lua` | `7vxx9w6/39x5/usv3/72v7v8vs1657vxx9w6.le.lpb` | `8b5cdea339b66c6eb2c8215b3f2ce2707e850e105b4e4cfc1aba937b15921594` | `8cbfd21bd8d3def502c83b4c9138dd2ef1d6d11a17ae37806b5d48632db26b38` | `64213d235d57b7437e998bc090f4c9270dd797910ac43f7a5a01c1a4afac5c03` | `2c4d5a9f9a2a7503e15414383b51702bf8ac5612b9d4aa4d23a32c3a16b04a3b`; `lua/command/game/prog/chocoboridecommand.lua:22-57` |
| `lua/scripts/judge/chocobojudge.lua` | `0p635/72v7v8v0p635.le.lpb` | `c9caa7c9080508c5d493ac1079501fec64e0d9b91d4f2c7cafae46fa2bdd6114` | `788bbba24ba8ceeb169048a28302c1edaae04b781baf90603f9e249bee7b9ea1` | `5943123f1197142c8bc9e0510d293f7231a33c1e09cb05d6be59d6997748ebac` | `8276b8a46f09b6d0a7439bca08daa517dac7d2a36c4d3e7e8692f08cd8b6704f`; `lua/judge/chocobojudge.lua:2-57` |
| `lua/scripts/widget/ask/chocobonamingwidget.lua` | `n1635q/9rz/72v7v8vw9x1w3n1635q.le.lpb` | `cb07607799967f94e0d16389de2a078325aaadde13c5fb25ff1bf24fe017d653` | `875be316863f3bf0f2d6ce720ef4e292bde89a754d8dd79dbeba337c80653e67` | `f8ba0c847b7a09bf0ed447ba780b3b7c61e7b0ffe7619730f2257b96a485b3e8` | `b031a21fefcb894b1232d90524f5986dfbf2c8f43dc719fba10743220f984898`; `lua/widget/ask/chocobonamingwidget.lua:3-91` |
| `lua/scripts/widget/chocoborentaltimerwidget.lua` | `n1635q/72v7v8vs5wq9yq1x5sn1635q.le.lpb` | `7ccb8bcf606a1269d58990e3622775b3c89382c46ad88bfced8e12437977edc0` | `01b651020d307913c71ab064a5d84b39b03a1855940d8f0c176af64d861e32e8` | `a0d77c36c3ea24b5c338ab29404c6c8cbcbae4547f721a1c007ac316d904a032` | `5be741d9891311d130205ccf377d522bb01bac096c72b00283a5c980dc8fdc61`; `lua/widget/chocoborentaltimerwidget.lua:6-15` |

The actor-class join is pinned by
`xivl-client-data:manifests/staticactor_class_paths.json:11236-11240`,
SHA-256 `d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
The script source and resource entries are pinned in
`manifests/scripts.json:7185-7188,9891-9894,14895-14898,15243-15246` and
`manifests/retail_lua_coverage.json:184-195,22594-22605,25533-25544,26448-26459`.
