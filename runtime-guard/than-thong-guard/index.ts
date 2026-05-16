import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const BLOCKED_TOOLS = new Set([
  "web_search",
  "web_fetch",
  "image_generate",
  "music_generate",
  "video_generate",
]);

export default definePluginEntry({
  id: "than-thong-guard",
  name: "Than-thong Guard",
  description: "Runtime guard enforcing than-thong-first, offline-first, no-billing/no-quota tool policy.",
  register(api) {
    api.on(
      "before_tool_call",
      async (event) => {
        if (!BLOCKED_TOOLS.has(String(event.toolName ?? ""))) return;
        return {
          block: true,
          blockReason: `Blocked by than-thong runtime guard: ${String(event.toolName)} violates offline-first / no-billing policy.`,
        };
      },
      { priority: 100 },
    );
  },
});
