# Grand Company quest text-source bindings

The [SAN-selected Grand Company scenario set](gc-quest-recoverability.md#san-selected-source-coverage)
has 92 source classes for 102 quest IDs. Authentication of the original Lua 5.1 resources establishes
59 text-loader tuples and 33 empty `initText` bodies. The empty bodies belong
to the selected placeholder classes; they do not establish playable behavior.

Each original LPB wrapper and decoded chunk matches the size and SHA-256
recorded in [`data/quest_contracts.json`](../data/quest_contracts.json) and
[`manifests/retail_lua_coverage.json`](../manifests/retail_lua_coverage.json).
All 92 selected resources use the XOR-73 wrapper. Each chunk parses completely,
with no trailing bytes. The selected
decoded source members separately match [`manifests/scripts.json`](../manifests/scripts.json).

## Class assignment and loader arguments

The root chunk requires `/Quest/Scenario/ScenarioBaseClass` and calls
`_defineClass` with the selected class name and `ScenarioBaseClass`. It then
loads that class global, creates the particular child closure, and assigns it
to the `initText` member. Checking this root assignment identifies the actual
selected prototype rather than assuming that child zero is `initText`.
All 92 assignments agree with the retained class and declaration metadata.

Each of the 59 loader bodies has one fixed parameter, no varargs, no upvalues,
no nested prototypes, and exactly these instructions, using zero-based PCs:

| PC | Instruction | Effect established by the operands |
| --- | --- | --- |
| 0 | `SELF A=1 B=0 C=256` | Read `_loadTextDataPermanently` from parameter register 0 and copy that receiver to register 2. |
| 1 | `LOADK A=3 Bx=1` | Load the exact numeric constant into register 3. |
| 2 | `LOADK A=4 Bx=2` | Load the exact source-name constant into register 4. |
| 3 | `CALL A=1 B=4 C=1` | Call with three arguments: self, numeric literal, source name. Retain no results. |
| 4 | `RETURN A=0 B=1 C=0` | Return zero values. |

The 59 numeric/name tuples agree with the selected recovered-source bodies
and canonical metadata. Their names and adjusted numeric keys are unique
within this selection. The other 33 bodies have one fixed parameter, no
varargs, no upvalues, no constants, no nested prototypes, and only
`RETURN A=0 B=1 C=0` at PC 0. They contain no loader call.

## Native key and source-name boundary

The promoted
`xivl-decomp:docs/script/actor-base-text-source.md`, callback `0x006E7500`,
establishes the accepted-input rule: after removing the Lua receiver, add
`0x03A20000` to the captured numeric dword and keep the low 32 bits. For
example, Gcl107 supplies the exact literal `10496` (`0x2900`) and name
`gcl107`, yielding `0x03A22900` under that rule. The adjusted value is not
established as a row, duty identifier, or locale selector.

That native contract makes the source-name write conditional on a successful
named ExcelSheet lookup with a nonempty enabled-row range vector, either
immediately or through the retained deferred checker. Reusing a source name
can increment its existing count without making another numeric request.
For the WorldMaster message route to read the same supplied name, the quest
handle must still resolve the same initialized ActorBase receiver and the
required objects must remain valid.

The bytecode checks establish static class assignments, literal order, call
arity, and zero-result returns. They do not observe Lua invocation, a
historical load, name assignment, load readiness, runtime language, message
row, server state, duty behavior, or actor spawning. The other declared
methods remain outside this initializer check.

## Original definition joins

All 59 adjusted keys have an individually authenticated original definition
carrier under the conditional numeric resource path. Each carrier is 1,664
bytes with a final `0xF1`, and each decodes to 1,663 UTF-8 XML bytes with an
`ssd` root and version `0.1`. All five definitions in each document use the
exact name supplied by that script. Their mode is `client`; the languages
`ja`, `en`, `de`, `fr` and `chs` map respectively to logical field indices
0, 1, 2, 3 and 4. Each declares one `str` field and one block beginning at
row 0 with 501 slots. Declared slots do not identify enabled rows.

The `decode_document` reader in
`xivl-tools:tools/research/census_sheet_stack.py`, source SHA-256
`c45c8e55e85e8d666cfe4a12b92b877ac84e710c2ed30913ede7d5dd149e4441`,
produced the same bytes as the authenticated fixed-size native decoder
transcription for all 59 original carriers. The inputs share the supported
1,664-byte/F1 shape and masks `0x2D79` and `0xD285`; this comparison does
not generalize to other input shapes or observe native execution. The
`xivl-decomp:docs/script/actor-base-text-source.md` format and receiver
conditions apply.

Paths in the table are relative to `lua/scripts/quest/scenario/`. Every name
argument equals its source filename stem. The numeric literal is the original
Lua constant; the adjusted resource key applies the native u32-add rule.
The carrier SHA-256 identifies the original definition, not any referenced
data, enable or offset body.

| Source | Numeric literal | Adjusted key | Definition SHA-256 |
| --- | ---: | --- | --- |
| `com/com0g1.lua` | 5952 | `0x03A21740` | `186efc39d0f17d7e3214a332bb84b04535a286d5213a2433b755a20993c96b88` |
| `com/com0g2.lua` | 5968 | `0x03A21750` | `7fefabf9fafee05787fb25feadde7290b958466dec9f98f7526a12b480ee994a` |
| `com/com0g3.lua` | 5984 | `0x03A21760` | `73cd42940ec13db35346873fe6c4181f65e985acbb2f43827715c7b33f6ea212` |
| `com/com0g4.lua` | 6000 | `0x03A21770` | `249100701d041a6102d6faa39d94f744b642d683d33a58568bf4a8f63fd7245c` |
| `com/com0g5.lua` | 6016 | `0x03A21780` | `70c99cf5ae4b9e7d22480788b98063dc0fef0d18018726cb71e946d2cedf184e` |
| `com/com0g6.lua` | 6032 | `0x03A21790` | `97ec52265e20f70cb60df575000308bf1b2df7d13ee5f465ef406a3872891f28` |
| `com/com0g7.lua` | 6048 | `0x03A217A0` | `d7c96140209e51a1cdc100a109fd13e67d45662cd4428f59bea25b66dfee4cb4` |
| `com/com0l1.lua` | 6096 | `0x03A217D0` | `8a7d615cfbcb2a2c51c7def4b63c776c6bd98d7fe2876324e5056cacdbbf008c` |
| `com/com0l2.lua` | 6112 | `0x03A217E0` | `02b38d122bb9e3ece91b1efb21f3b049c19401223f0910c604ff252713af6848` |
| `com/com0l3.lua` | 6128 | `0x03A217F0` | `527d789423f283e1c5786451d3742c67e420e8a5863df14a812f26a093885cb1` |
| `com/com0l4.lua` | 6144 | `0x03A21800` | `4d0eca3d5f32ba277a00f767eb4e5f9a5699d027bd228f7dd25f47dd12fbecaa` |
| `com/com0l5.lua` | 6160 | `0x03A21810` | `02412bbb72bad237ce29fd78947d7782e5a6b498bb6e1aa48eba318a14665043` |
| `com/com0l6.lua` | 6176 | `0x03A21820` | `50fbf4a660950d12a2c0d14e81f510d29c8b97d20cb78f7bac241a8486e8df6c` |
| `com/com0l7.lua` | 6192 | `0x03A21830` | `4f5124fcc2966eecaf17c53744fda8653b8249847ed25ce48ef0df53d061d9c4` |
| `com/com0u1.lua` | 6240 | `0x03A21860` | `45850f7b8ef640046e310ddcd1cc91d03c905dea4d1ec46e55071d8785ae6394` |
| `com/com0u2.lua` | 6256 | `0x03A21870` | `ac08b530dcae4abaed7bb61a7234b1222427b91b49c0382bd0caadf6ce6ac654` |
| `com/com0u3.lua` | 6272 | `0x03A21880` | `5840e5eaccedc5e32b126859d86fc29acdc4b319206eae305916cd3241082afa` |
| `com/com0u4.lua` | 6288 | `0x03A21890` | `b1d0fa4060be7b70b4446e16febc1de96471e5a12d11ebaf0b7cb3ae640eb1a5` |
| `com/com0u5.lua` | 6304 | `0x03A218A0` | `4962a45c50ef5e0f34b343188439bbd839264686dc71e06ae2ca9e54c96e393d` |
| `com/com0u6.lua` | 6320 | `0x03A218B0` | `22c90471ef1a1fb4c22a1fe76e0de9a56bf7fd0d01f797af2a0f53571ea34f63` |
| `com/com0u7.lua` | 6336 | `0x03A218C0` | `9c1d3cb8d47f614c4bbdc05e62994e73e3bdce8da0e177e8e5cc887d0e36f0d3` |
| `com/com5g0.lua` | 6384 | `0x03A218F0` | `3f8f23d59beb6179ad6d56b78981be5bb09103b4a9fdb5f050acf8fba963ef47` |
| `com/com5g1.lua` | 6400 | `0x03A21900` | `f0d6058b4e4a15461d1b202621e73ca22a3a482694df194ce2fae541edd155eb` |
| `com/com5l0.lua` | 6480 | `0x03A21950` | `9a428f7cc7eb261bf68d5877adf526e74eab7a434727288c2a5f5e14652a43b2` |
| `com/com5l1.lua` | 6496 | `0x03A21960` | `b73610537e029d3d6af351492b46ff77d064052e36d1cbc747211368bd1f3df1` |
| `com/com5u0.lua` | 6576 | `0x03A219B0` | `67bf84e8f71e939e938ae92312bfe7e1d21a48d462cb6fc82b2dacf9c944b6e3` |
| `com/com5u1.lua` | 6592 | `0x03A219C0` | `b7a056cda3f56e4eec8fa9c5fa9a623fb0865e302f10d76da7a65189f9fa1b7a` |
| `gcg/gcg102.lua` | 7792 | `0x03A21E70` | `25caaeb45aef13729c100718254cea3006e47320ecbe11b7a9d73ec6777d34e8` |
| `gcg/gcg103.lua` | 8036 | `0x03A21F64` | `a90ff36349918ef82e8e05e401e1c06c8931ee5e2bc924ac80472a596f263bc0` |
| `gcg/gcg301.lua` | 6880 | `0x03A21AE0` | `43d6283cf26ccab4d1aeace975701c5b11823d16bc12a7da625aedae639802b6` |
| `gcg/gcg302.lua` | 6896 | `0x03A21AF0` | `83020434a4c5cd02f1e79f39733c2e91a7d2656349f32346dee73d8d599d5e47` |
| `gcg/gcg303.lua` | 6912 | `0x03A21B00` | `48fb29f29d2d4be9fb582a61aa79f592c455da057f52bb524890c08d5756f43a` |
| `gcg/gcg304.lua` | 6928 | `0x03A21B10` | `15d7e79daad0b6ac2b0ca3868d55c5bae56e7fa964800b779e58c05b4ce0fdce` |
| `gcg/gcg305.lua` | 7744 | `0x03A21E40` | `155c578857ce31707c5b3d651d35d444d1bc65d1d63001372e7692f13da445ba` |
| `gcg/gcg701.lua` | 7808 | `0x03A21E80` | `4faf9bb4b7a7c946bfb5355e4658b0fc8e004703f2b509cb04842cb4943506b5` |
| `gcg/gcg702.lua` | 10480 | `0x03A228F0` | `dfa308c9297aa4a4d129de07e6c3a1072f664e6094c77896b157ec39366ca51d` |
| `gcl/gcl101.lua` | 6976 | `0x03A21B40` | `31acb611399451c20eb3df6b32af73af97bdedd149781ceb1fa7a625191ff835` |
| `gcl/gcl102.lua` | 7824 | `0x03A21E90` | `598f9b253942a7ec36d944cfb6644038686b5426a6330cf74076a9de5ef6efa9` |
| `gcl/gcl103.lua` | 8068 | `0x03A21F84` | `5ce915a7724f3b6391ee7b63565cfacf9bcbb88d5dca8243f0d0fc8c9dc54adb` |
| `gcl/gcl104.lua` | 8084 | `0x03A21F94` | `85f0472d45ebdd23c1922f0a478ca8ad00d297a58aef7f086401502553dc2715` |
| `gcl/gcl105.lua` | 10336 | `0x03A22860` | `a607cd97e4fb9e9c0bdf9db28cc34afaae8abc9bec9384237fc16b950672dc77` |
| `gcl/gcl106.lua` | 10352 | `0x03A22870` | `fba812b69c326cbde44aa0f741ee687af61dd8cc8dce28feb8bcdd33ee92a4b1` |
| `gcl/gcl107.lua` | 10496 | `0x03A22900` | `f06d0646e46f0d02336e7bc209121462d1c33579a006402e13876053a642ec80` |
| `gcl/gcl301.lua` | 6992 | `0x03A21B50` | `596b379f26c3672b0f6e66b6787819daa21a2e4719bced9c9c34fe2e5030cc0d` |
| `gcl/gcl302.lua` | 7008 | `0x03A21B60` | `7396b748affa545ed9b9ed20590bf579bbcf3ad7ad667fcd1dd1a6efd420e423` |
| `gcl/gcl303.lua` | 7024 | `0x03A21B70` | `fc983edeeff6fc9edd6e1d04e8fd0edb151bcb10114664ec4cb8efd3377e9fa3` |
| `gcl/gcl304.lua` | 7040 | `0x03A21B80` | `32144401370042007554c6037038eba8a9bd2b90fdd8c941595486c85479e013` |
| `gcl/gcl305.lua` | 7760 | `0x03A21E50` | `7311a7b50e9e6cf456cb8afde89db8d81b79d55eb74fe2c5c5ae104a1d253596` |
| `gcl/gcl701.lua` | 7840 | `0x03A21EA0` | `d243b04d7ab052cc4598fd77141e5772f29a178c141a84a064906ec39f4facb0` |
| `gcl/gcl702.lua` | 10512 | `0x03A22910` | `51c4c9e984dd771fb06eff08d8095f178638affa8efb82f1b2a13f34040fcaa5` |
| `gcu/gcu102.lua` | 7856 | `0x03A21EB0` | `fef5d6f37cd49e19bd9a88407555a6d4e3cce57de4d3fc586f243a468c7703b4` |
| `gcu/gcu103.lua` | 8100 | `0x03A21FA4` | `b5e091c1054e16d0a6d57a032754636f76fd014ef6172c34a3f41ce83896015e` |
| `gcu/gcu301.lua` | 7104 | `0x03A21BC0` | `5bcd3225b75332c8bb39f611de0f79f56b9db5884ff9ed907076c3498aced894` |
| `gcu/gcu302.lua` | 7120 | `0x03A21BD0` | `716b2477cd0d374b00b4c8638e7d9a80dffc000b79dbca8a5693a195402955c1` |
| `gcu/gcu303.lua` | 7136 | `0x03A21BE0` | `21c2052ca7a960229fc40e598206e6f3f57d8ce1430722f060cbc650b9a0e482` |
| `gcu/gcu304.lua` | 7152 | `0x03A21BF0` | `4f882a0ec7cc51cc2db8d1b2e97343bb942bd01cd865dfb80e6eb03db752e16e` |
| `gcu/gcu305.lua` | 7776 | `0x03A21E60` | `1ae5a4b7e929a3b4f916ed542fcd87c8cd768a7d9f195d1971e1822f20101eef` |
| `gcu/gcu701.lua` | 7872 | `0x03A21EC0` | `22983899917c7ebb79cf7aaffb87350123fbb643ad4a7f130e271a8f99a960dc` |
| `gcu/gcu702.lua` | 10544 | `0x03A22930` | `863933abd3e63d8209dedea8b565b136d799c65423f6f56ac7b26bb25c21b9a8` |

The 33 empty local initializers are listed below, using the same path base.
Their bodies make no loader call; inherited behavior is outside this check.

- `com`: `com0g8.lua`, `com0g9.lua`, `com0l8.lua`, `com0l9.lua`, `com0u8.lua`,
  `com0u9.lua`, `com5g2.lua`, `com5g3.lua`, `com5g4.lua`, `com5g5.lua`,
  `com5l2.lua`, `com5l3.lua`, `com5l4.lua`, `com5l5.lua`, `com5u2.lua`,
  `com5u3.lua`, `com5u4.lua`, `com5u5.lua`.
- `gcg`: `gcg501.lua`, `gcg502.lua`, `gcg601.lua`, `gcg602.lua`, `gcg603.lua`.
- `gcl`: `gcl501.lua`, `gcl502.lua`, `gcl601.lua`, `gcl602.lua`, `gcl603.lua`.
- `gcu`: `gcu501.lua`, `gcu502.lua`, `gcu601.lua`, `gcu602.lua`, `gcu603.lua`.

The definition files explicitly name their block resources. Those referenced
bodies were not read for this result. The selected Gcl107 baseline in
`xivl-decomp:docs/script/actor-base-text-source.md`, Selected Gcl107 definition
and English source, separately qualifies three original English cells. This
definition census establishes no selected request mode, runtime language,
loaded sheet, row/field readiness, text result or quest availability. It does
not change the source census's limits on the other 695 declared methods.
