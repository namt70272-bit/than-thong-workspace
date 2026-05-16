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
  description:
    "Default routing layer: local-first, offline-first, no-billing. Moi lenh qua than-thong truoc.",
  register(api) {
    api.on(
      "before_tool_call",
      async (event) => {
        const toolName = String(event.toolName ?? "");

        // External/billing tools -> block
        if (BLOCKED_TOOLS.has(toolName)) {
          return {
            block: true,
            blockReason: `[than-thong] DA CHAN: ${toolName} vi pham chinh sach offline-first / khong-billing. Dung tool local thay the.`,
          };
        }

        // Moi tool khac duoc phep qua, than-thong ghi nhan
        return;
      },
      { priority: 100 },
    );
  },
});
