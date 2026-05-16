# Engram candidate gap report — 2026-05-11 02:13 GMT+7

## Candidate created
- `E:\KY-DATA\OpenClaw\projects\engram-candidate\docs`
- `E:\KY-DATA\OpenClaw\projects\engram-candidate\openclaw-plugin-js`
- `E:\KY-DATA\OpenClaw\projects\engram-candidate\three-tier-engine`

## What the split tells us

### 1. `openclaw-plugin-js/`
- Closest to current OpenClaw plugin shape.
- Works in local-only mode if `apiKey` is empty.
- But this branch is mostly **Qdrant + FastEmbed wrapper**, not the deep three-tier local engine.
- Contains cloud/billing path in code, so if reused later must keep `apiKey` unset.
- File appears to have some encoding noise in comments, but logic is still readable.

### 2. `three-tier-engine/`
- This is the valuable branch if the goal is the real Engram recall logic.
- Core imports indicate extra Python/runtime dependencies:
  - `numpy`
  - `httpx`
  - `sklearn.cluster`
  - `kuzu`
  - `qdrant_client`
- So this branch is **not plug-and-play yet** in the current OpenClaw runtime.

## Smallest safe patch path
1. Treat `three-tier-engine/` as the main extraction target.
2. Keep `openclaw-plugin-js/` only as reference for current OpenClaw plugin wiring.
3. Do not wire either branch into active config yet.
4. Next safe step: inspect dependency list + map what is already present locally versus what would need isolated install.

## Recommendation
If continuing in order, the next branch should be:
- dependency audit for `three-tier-engine/`
- then adapter design to current OpenClaw plugin/runtime
- only then minimal config patch
